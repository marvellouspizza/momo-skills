#!/usr/bin/env python3
"""Validate a release and register it under a shared portfolio publication lock."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit, urlunsplit


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def web_url(value):
    require(isinstance(value, str), 'url must be a string')
    u = urlsplit(value.strip())
    require(u.scheme == 'https' and u.hostname and not u.username and not u.password,
            'url must be a public HTTPS page without credentials')
    require(u.hostname not in ('localhost', '127.0.0.1', '::1'), 'localhost cannot be published')
    require(not u.fragment, 'use the application URL without a fragment')
    return urlunsplit((u.scheme, u.netloc.lower(), u.path or '/', u.query, ''))


def atomic_write(path, data):
    require(not path.is_symlink(), f'refusing symlink: {path}')
    fd, temp = tempfile.mkstemp(prefix='.publish-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def register(manifest, root):
    p = read_json(manifest)
    require(isinstance(p, dict), 'manifest must be an object')
    require(isinstance(p.get('id'), str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p['id']),
            'invalid project id')
    for key in ('name', 'description'):
        value = p.get(key)
        require(isinstance(value, str) and value.strip(), f'missing {key}')
        p[key] = value.strip()
        require(len(p[key]) <= 14 and len(p[key].encode('utf-16-le')) // 2 <= 14,
                f'{key} exceeds 14 characters')
    p['url'] = web_url(p.get('url'))
    require(isinstance(p.get('sourceDir'), str) and Path(p['sourceDir']).is_absolute(),
            'sourceDir must be absolute')
    source = Path(p['sourceDir']).resolve(strict=True)
    require(source.is_dir(), 'sourceDir must exist')
    p['sourceDir'] = str(source)
    logo_name = p.get('logo')
    require(isinstance(logo_name, str) and Path(logo_name).name == logo_name
            and logo_name.lower().endswith('.png'), 'logo must be a PNG filename beside the manifest')
    logo = manifest.parent / logo_name
    require(not logo.is_symlink(), 'logo must be a regular local file')
    require(logo.stat().st_size <= 5_000_000, 'logo exceeds 5 MB')
    data = logo.read_bytes()
    require(len(data) >= 33 and data[:8] == b'\x89PNG\r\n\x1a\n' and data[12:16] == b'IHDR',
            'invalid PNG header')
    width, height = struct.unpack('>II', data[16:24])
    require(width == height and width > 0, 'logo must be square')
    submissions = root / 'project-submissions'
    require(not submissions.is_symlink(), 'submission directory must not be a symlink')
    submissions.mkdir(exist_ok=True)
    destination = submissions / p['id']
    found = False
    for existing in submissions.glob('*/project.json'):
        require(not existing.is_symlink() and not existing.parent.is_symlink(), 'symlink in submissions')
        old = read_json(existing)
        old_url = old.get('url', '')
        same_url = bool(old_url) and urlsplit(old_url)._replace(path=urlsplit(old_url).path or '/').geturl() == p['url']
        if old.get('id') == p['id']:
            require(not found, 'duplicate existing id; reconcile before publishing')
            found = True
            if old.get('sourceDir'):
                require(Path(old['sourceDir']).resolve() == source, 'id belongs to another source project')
            else:
                require(same_url, 'existing id has no sourceDir and a different URL; reconcile manually')
            destination = existing.parent
        else:
            require(not same_url, f'URL already belongs to {old.get("id")}')
    require(not destination.is_symlink(), 'destination must not be a symlink')
    destination.mkdir(exist_ok=True)
    logo_filename = 'logo-' + hashlib.sha256(data).hexdigest()[:16] + '.png'
    atomic_write(destination / logo_filename, data)
    result = {key: p[key] for key in ('id', 'name', 'description', 'url', 'sourceDir')}
    result['logo'] = logo_filename
    atomic_write(destination / 'project.json', (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode())
    print(json.dumps({'status': 'registered_locally', 'manifest': str(destination / 'project.json')}, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--portfolio', type=Path)
    parser.add_argument('--lock-timeout', type=float, default=600)
    parser.add_argument('--after', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    profile = read_json(Path(__file__).resolve().parents[1] / 'references/profile.json')
    root = (args.portfolio or Path(profile['portfolioRoot'])).resolve(strict=True)
    require(root.is_dir() and (root / 'scripts/import-projects.mjs').is_file(), 'not a portfolio checkout')
    require(args.lock_timeout >= 0, 'lock timeout must not be negative')
    lock_path = root / '.project-publish.lock'
    require(not lock_path.is_symlink(), 'lock must not be a symlink')
    with lock_path.open('a') as lock:
        deadline = time.monotonic() + args.lock_timeout
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise ValueError('another publication holds the portfolio lock; retry when it finishes')
                time.sleep(min(0.2, max(0, deadline - time.monotonic())))
        register(args.manifest.resolve(strict=True), root)
        if args.after:
            return subprocess.run(args.after, cwd=root).returncode
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f'Publication failed: {error}', file=sys.stderr)
        sys.exit(1)
