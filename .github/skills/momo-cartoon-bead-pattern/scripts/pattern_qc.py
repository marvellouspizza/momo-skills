#!/usr/bin/env python3
"""Audit sparse bead data; optionally export previews/charts. No image-to-art conversion."""
import argparse
from collections import Counter
import csv
import html
import json
from pathlib import Path
import re
import sys

HEX = re.compile(r'^#[0-9a-fA-F]{6}$')
KEY = re.compile(r'^(0|[1-9][0-9]*)$')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'JSON 重复键: {key}')
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def read_catalog(path):
    if path is None:
        return None
    raw = read_json(path)
    colors = raw.get('colors') if isinstance(raw, dict) else raw
    if not isinstance(colors, list) or not colors:
        raise ValueError('色卡需要非空 colors 数组或颜色数组')
    result = {}
    for color in colors:
        if not isinstance(color, dict) or not isinstance(color.get('id'), str) or not color['id'].strip():
            raise ValueError('色卡颜色缺少有效 id')
        if not isinstance(color.get('hex'), str) or not HEX.fullmatch(color['hex']):
            raise ValueError(f"色卡 RGB 无效: {color['id']}")
        if color['id'] in result:
            raise ValueError(f"色卡 id 重复: {color['id']}")
        result[color['id']] = {**color, 'hex': color['hex'].lower()}
    return result


def components(keys, size):
    remaining = set(keys)
    sizes = []
    while remaining:
        queue = [remaining.pop()]
        i = 0
        while i < len(queue):
            key = queue[i]
            i += 1
            x, y = key % size, key // size
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if not (0 <= x+dx < size and 0 <= y+dy < size):
                    continue
                other = (y+dy)*size+x+dx
                if other in remaining:
                    remaining.remove(other)
                    queue.append(other)
        sizes.append(len(queue))
    return sorted(sizes, reverse=True)


def audit(raw, catalog, target, tolerance, expected_colors, allow_disconnected):
    report = {'ok': False, 'errors': [], 'warnings': [], 'catalogVerified': catalog is not None}
    errors, warnings = report['errors'], report['warnings']
    if not isinstance(raw, dict):
        errors.append('图纸必须是 JSON 对象')
        return report, None
    if not isinstance(raw.get('name'), str) or not raw['name'].strip():
        errors.append('图纸 name 不能为空')
    size = raw.get('boardSize')
    if type(size) is not int or not 1 <= size <= 4096:
        errors.append('boardSize 必须为 1–4096 的整数；不能省略或默认为 52')
        return report, None
    cells, codes = raw.get('cells'), raw.get('cellCodes')
    if not isinstance(cells, dict) or not cells or not isinstance(codes, dict):
        errors.append('需要非空 cells 对象和 cellCodes 对象')
        return report, None
    if set(cells) != set(codes):
        errors.append(f'格子/色号键不一致：缺少 {len(set(cells)-set(codes))} 个，孤儿 {len(set(codes)-set(cells))} 个')
    valid = {}
    id_hex = {}
    for key, color in cells.items():
        if not KEY.fullmatch(key) or int(key) >= size*size:
            errors.append(f'格子越界或键格式无效: {key}')
            continue
        if not isinstance(color, str) or not HEX.fullmatch(color):
            errors.append(f'RGB 无效: {key}')
            continue
        code = codes.get(key)
        if not isinstance(code, str) or not code.strip():
            errors.append(f'色号无效或缺失: {key}')
            continue
        color = color.lower()
        if code in id_hex and id_hex[code] != color:
            errors.append(f'同一个色号对应多个 RGB: {code}')
        id_hex[code] = color
        if catalog is not None:
            if code not in catalog:
                errors.append(f'色卡中没有色号: {code}')
            elif catalog[code]['hex'] != color:
                errors.append(f'格子 {key} 的 RGB 与色号 {code} 不匹配')
        valid[key] = color
    if errors:
        report['errors'] = list(dict.fromkeys(errors))
        return report, None

    keys = [int(key) for key in valid]
    counts = Counter(codes[key] for key in valid)
    xs, ys = [key % size for key in keys], [key // size for key in keys]
    bounds = {'minCol': min(xs), 'maxCol': max(xs), 'minRow': min(ys), 'maxRow': max(ys)}
    blocks = components(keys, size)
    if abs(len(keys)-target) > target*tolerance:
        errors.append(f'有效颗数 {len(keys)} 超出目标 {target} 的 ±{tolerance:.0%}')
    if len(counts) != expected_colors:
        errors.append(f'实际使用 {len(counts)} 种色号，要求 {expected_colors} 种')
    if not allow_disconnected and len(blocks) != 1:
        errors.append(f'图案分为 {len(blocks)} 个四邻域连通块: {blocks}')
    if catalog is None:
        warnings.append('未提供色卡，未验证品牌色号映射')
    if len(set(valid.values())) != len(counts):
        warnings.append('不同色号存在相同 RGB；确认并非用别名凑色数')
    rare = {code: count for code, count in counts.items() if count < 3}
    if rare:
        warnings.append('存在少于 3 颗的颜色；检查是否必要的高光/五官，避免无意义碎点')
    if not any(max(int(color[i:i+2], 16) for i in (1, 3, 5)) <= 12 for color in valid.values()):
        warnings.append('未检测到近黑色，需确认用户要求的黑色勾线')
    palette = []
    for code, count in counts.most_common():
        item = catalog.get(code, {}) if catalog is not None else {}
        palette.append({'id': code, 'code': str(item.get('code') or code), 'hex': id_hex[code], 'count': count})
    report.update(ok=not errors, name=raw['name'], boardSize=size, count=len(keys), colors=len(counts),
                  visibleColors=len(set(valid.values())), bounds=bounds,
                  width=max(xs)-min(xs)+1, height=max(ys)-min(ys)+1,
                  components=blocks, rareColors=rare, palette=palette)
    normalized = {**raw, 'cells': valid, 'cellCodes': {key: codes[key] for key in valid}}
    return report, normalized


def export(pattern, report, directory):
    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError('导出 PNG 需要 Pillow；仅校验时可省略 --out') from exc
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    bounds, size = report['bounds'], report['boardSize']
    cols, rows = report['width'], report['height']
    scale = max(1, min(10, 2000 // max(cols+6, rows+6)))
    image = Image.new('RGB', ((cols+6)*scale, (rows+6)*scale), 'white')
    draw = ImageDraw.Draw(image)
    for key, color in pattern['cells'].items():
        x, y = int(key) % size-bounds['minCol']+3, int(key)//size-bounds['minRow']+3
        draw.rectangle((x*scale, y*scale, (x+1)*scale-1, (y+1)*scale-1), fill=color)
    image.save(out/'preview.png')
    (out/'pattern.json').write_text(json.dumps(pattern, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    with (out/'colors.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(('id', 'code', 'hex', 'count'))
        writer.writerows((p['id'], p['code'], p['hex'], p['count']) for p in report['palette'])
    cell, label_rows = 28, (report['colors']+3)//4
    width, height = max(640, cols*cell+88), rows*cell+140+label_rows*34
    esc = lambda value: html.escape(str(value), quote=True)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="white"/><g font-family="Arial,sans-serif">',
           f'<text x="44" y="32" font-size="24">{esc(pattern["name"])}</text>',
           f'<text x="44" y="57" font-size="15">{report["count"]} beads · {report["colors"]} colors · {cols} × {rows} · board {size} × {size}</text>']
    by_id = {p['id']: p for p in report['palette']}
    for x in range(cols):
        if x == 0 or (x+bounds['minCol']+1) % 5 == 0:
            svg.append(f'<text x="{44+(x+.5)*cell}" y="82" text-anchor="middle" font-size="10">{x+bounds["minCol"]+1}</text>')
    for y in range(rows):
        if y == 0 or (y+bounds['minRow']+1) % 5 == 0:
            svg.append(f'<text x="35" y="{94+(y+.65)*cell}" text-anchor="end" font-size="10">{y+bounds["minRow"]+1}</text>')
    for key, color in pattern['cells'].items():
        x = 44+(int(key) % size-bounds['minCol'])*cell
        y = 94+(int(key)//size-bounds['minRow'])*cell
        r, g, b = (int(color[i:i+2], 16) for i in (1, 3, 5))
        ink = '#222' if r*.299+g*.587+b*.114 > 155 else '#fff'
        label = by_id[pattern['cellCodes'][key]]['code']
        font_size = min(8, 24/max(1, len(label)) * 1.5)
        svg.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{color}" stroke="#888" stroke-width=".4"/>'
                   f'<text x="{x+cell/2}" y="{y+cell*.64}" text-anchor="middle" fill="{ink}" font-size="{font_size}">{esc(label)}</text>')
    for i, item in enumerate(report['palette']):
        x, y = 44+(i % 4)*(width-88)/4, rows*cell+125+(i//4)*34
        svg.append(f'<rect x="{x}" y="{y-13}" width="16" height="16" fill="{item["hex"]}" stroke="#aaa"/>'
                   f'<text x="{x+24}" y="{y}" font-size="12">{esc(item["code"])} × {item["count"]}</text>')
    svg.append('</g></svg>')
    (out/'chart.svg').write_text(''.join(svg), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pattern', type=Path)
    parser.add_argument('--catalog', type=Path)
    parser.add_argument('--target', type=int, default=4000)
    parser.add_argument('--tolerance', type=float, default=.05)
    parser.add_argument('--colors', type=int, default=32)
    parser.add_argument('--allow-disconnected', action='store_true')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.target <= 0 or args.colors <= 0 or not 0 <= args.tolerance <= 1:
        parser.error('目标颗数与色数必须为正数，tolerance 必须在 0–1')
    try:
        report, pattern = audit(read_json(args.pattern), read_catalog(args.catalog), args.target,
                                args.tolerance, args.colors, args.allow_disconnected)
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out/'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({key: value for key, value in report.items() if key != 'palette'}, ensure_ascii=False, indent=2))
        if not report['ok']:
            return 1
        if args.out:
            export(pattern, report, args.out)
        return 0
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        print(f'错误: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
