#!/usr/bin/env python3
"""Create starter tracking docs for a generated game art pack."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "assets" / "templates"


def render_template(text: str, pack_name: str) -> str:
    return (
        text.replace("{{PACK_NAME}}", pack_name)
        .replace("{{DATE}}", date.today().isoformat())
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output directory for tracking docs.")
    parser.add_argument("--pack-name", default="v1-art-pack", help="Human-readable pack name.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for template in sorted(TEMPLATE_DIR.glob("*.md")):
        target = out_dir / template.name
        if target.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite existing file: {target}")
        target.write_text(render_template(template.read_text(), args.pack_name), encoding="utf-8")
        written.append(target)

    print(f"Created {len(written)} tracking docs in {out_dir}")
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
