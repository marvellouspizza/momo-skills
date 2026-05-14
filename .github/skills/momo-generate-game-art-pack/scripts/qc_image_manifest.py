#!/usr/bin/env python3
"""Inspect PNG candidates and emit a simple QC manifest."""

from __future__ import annotations

import argparse
import struct
import json
from pathlib import Path
from typing import Any


def iter_images(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            found.extend(sorted(path.rglob("*.png")))
        elif path.suffix.lower() == ".png":
            found.append(path)
    return found


def inspect_image(path: Path) -> dict[str, Any]:
    try:
        from PIL import Image
    except ImportError:
        return inspect_png_header(path)

    with Image.open(path) as image:
        width, height = image.size
        mode = image.mode
        has_alpha = mode in {"RGBA", "LA"} or "transparency" in image.info
        transparent_corners = False
        if has_alpha:
            rgba = image.convert("RGBA")
            corners = [
                rgba.getpixel((0, 0))[3],
                rgba.getpixel((width - 1, 0))[3],
                rgba.getpixel((0, height - 1))[3],
                rgba.getpixel((width - 1, height - 1))[3],
            ]
            transparent_corners = all(alpha == 0 for alpha in corners)

    return {
        "path": str(path),
        "width": width,
        "height": height,
        "mode": mode,
        "has_alpha": has_alpha,
        "transparent_corners": transparent_corners,
        "inspection": "pillow",
    }


def inspect_png_header(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise SystemExit(f"Not a PNG file: {path}")
        length = struct.unpack(">I", handle.read(4))[0]
        chunk_type = handle.read(4)
        if chunk_type != b"IHDR" or length < 13:
            raise SystemExit(f"Missing PNG IHDR: {path}")
        data = handle.read(length)

    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[:10])
    modes = {
        0: "grayscale",
        2: "rgb",
        3: "indexed",
        4: "grayscale_alpha",
        6: "rgba",
    }
    return {
        "path": str(path),
        "width": width,
        "height": height,
        "mode": f"png_{modes.get(color_type, 'unknown')}_{bit_depth}bit",
        "has_alpha": color_type in {4, 6},
        "transparent_corners": "unknown_without_pillow",
        "inspection": "png_header",
    }


def markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Path | Size | Mode | Alpha | Transparent corners | Inspection | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {path} | {width}x{height} | {mode} | {has_alpha} | {transparent_corners} | {inspection} |  |".format(**row)
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="PNG files or directories to inspect.")
    parser.add_argument("--json-out", help="Optional JSON output path.")
    parser.add_argument("--md-out", help="Optional Markdown output path.")
    args = parser.parse_args()

    rows = [inspect_image(path) for path in iter_images(args.inputs)]
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(markdown(rows), encoding="utf-8")

    if not args.json_out and not args.md_out:
        print(markdown(rows), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
