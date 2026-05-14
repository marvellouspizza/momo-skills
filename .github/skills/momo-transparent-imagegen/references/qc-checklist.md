# Transparent Image QC Checklist

Run this checklist before returning or saving a transparent asset.

## Alpha

- Output file is PNG or WebP.
- File has an alpha channel.
- All four corners are fully transparent.
- There are enough opaque pixels to indicate the subject survived extraction.
- Transparent pixel ratio is plausible for an isolated subject.

## Edge Quality

- No obvious key-color fringe.
- No matte halo around the subject.
- No leftover flat key-color islands.
- No cropped body parts, corners, tails, weapon tips, smoke trails, text, or important details.
- No baked floor plane, cast shadow, contact shadow, reflection, or background object.

## Subject Quality

- The subject matches the user prompt.
- The whole object is visible and centered with usable padding.
- Small icons/sprites remain readable at expected size.
- Text is absent unless explicitly requested.
- Generated logos or marks do not copy known brands.

## Remediation

- Thin key fringe: rerun `remove_chroma_key.py` with `--edge-contract 1`.
- Stair-stepped opaque edge: try `--edge-feather 0.25`.
- Subject contains key color: regenerate with a different key color.
- Soft translucent subject fails: ask before using true/native transparency fallback.
