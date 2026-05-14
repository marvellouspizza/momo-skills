#!/usr/bin/env python3
"""Inspect PNG alpha information without requiring Pillow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import zlib
from typing import Any


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def paeth(left: int, up: int, up_left: int) -> int:
    p = left + up - up_left
    pa = abs(p - left)
    pb = abs(p - up)
    pc = abs(p - up_left)
    if pa <= pb and pa <= pc:
        return left
    if pb <= pc:
        return up
    return up_left


def parse_png(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(f"Not a PNG file: {path}")

    offset = len(PNG_SIGNATURE)
    chunks: dict[bytes, list[bytes]] = {}
    width = height = bit_depth = color_type = interlace = None

    while offset < len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        ctype = data[offset + 4 : offset + 8]
        cdata = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        chunks.setdefault(ctype, []).append(cdata)
        if ctype == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, interlace = struct.unpack(
                ">IIBBBBB", cdata
            )
        if ctype == b"IEND":
            break

    if width is None or height is None or bit_depth is None or color_type is None:
        raise ValueError(f"Missing PNG IHDR: {path}")

    result: dict[str, Any] = {
        "path": str(path),
        "width": width,
        "height": height,
        "bit_depth": bit_depth,
        "color_type": color_type,
        "has_alpha": color_type in {4, 6} or b"tRNS" in chunks,
        "transparent_corners": None,
        "transparent_pixels": None,
        "partial_alpha_pixels": None,
        "opaque_pixels": None,
        "transparent_ratio": None,
        "note": "",
    }

    if bit_depth != 8 or interlace != 0:
        result["note"] = "Alpha counts require 8-bit non-interlaced PNG."
        return result

    if color_type not in {4, 6}:
        result["note"] = "No direct alpha channel to count." if b"tRNS" not in chunks else "Indexed tRNS alpha not expanded by this inspector."
        return result

    channels = 4 if color_type == 6 else 2
    bpp = channels
    scanline_len = width * bpp
    raw = zlib.decompress(b"".join(chunks.get(b"IDAT", [])))
    rows: list[bytearray] = []
    cursor = 0
    previous = bytearray(scanline_len)

    for _y in range(height):
        filter_type = raw[cursor]
        cursor += 1
        row = bytearray(raw[cursor : cursor + scanline_len])
        cursor += scanline_len

        for i in range(scanline_len):
            left = row[i - bpp] if i >= bpp else 0
            up = previous[i]
            up_left = previous[i - bpp] if i >= bpp else 0
            if filter_type == 1:
                row[i] = (row[i] + left) & 0xFF
            elif filter_type == 2:
                row[i] = (row[i] + up) & 0xFF
            elif filter_type == 3:
                row[i] = (row[i] + ((left + up) // 2)) & 0xFF
            elif filter_type == 4:
                row[i] = (row[i] + paeth(left, up, up_left)) & 0xFF
            elif filter_type != 0:
                raise ValueError(f"Unsupported PNG filter {filter_type} in {path}")

        rows.append(row)
        previous = row

    alphas: list[int] = []
    for row in rows:
        alphas.extend(row[i] for i in range(channels - 1, len(row), channels))

    transparent = sum(1 for alpha in alphas if alpha == 0)
    partial = sum(1 for alpha in alphas if 0 < alpha < 255)
    opaque = sum(1 for alpha in alphas if alpha == 255)
    total = len(alphas)

    def alpha_at(x: int, y: int) -> int:
        return rows[y][x * channels + channels - 1]

    result.update(
        {
            "transparent_corners": all(
                alpha_at(x, y) == 0
                for x, y in [
                    (0, 0),
                    (width - 1, 0),
                    (0, height - 1),
                    (width - 1, height - 1),
                ]
            ),
            "transparent_pixels": transparent,
            "partial_alpha_pixels": partial,
            "opaque_pixels": opaque,
            "transparent_ratio": round(transparent / total, 6) if total else None,
        }
    )
    return result


def markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Path | Size | Alpha | Transparent corners | Transparent ratio | Opaque px | Partial px | Note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {path} | {width}x{height} | {has_alpha} | {transparent_corners} | {transparent_ratio} | {opaque_pixels} | {partial_alpha_pixels} | {note} |".format(
                **row
            )
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("png", nargs="+", help="PNG file(s) to inspect.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()

    rows = [parse_png(Path(raw).expanduser()) for raw in args.png]
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print(markdown(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
