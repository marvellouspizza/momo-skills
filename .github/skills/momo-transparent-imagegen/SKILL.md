---
name: momo-transparent-imagegen
description: "Generate transparent-background PNG/WebP raster images from prompts or references. Use when Codex should create icons, stickers, product cutouts, game sprites, UI icons, props, item art, decals, logos, or other standalone bitmap subjects with transparent background, alpha PNG, no background, cutout, isolated subject, or PNG asset output. Chinese triggers include 生成一张 xx 图透明底, 透明背景, 无背景, png, 生成 png 图, 参考图生成透明底图片, 生成游戏图标透明底, 生成游戏美术资源透明底. Default workflow uses built-in image_gen on a flat chroma-key background plus local alpha extraction, not native gpt-image-2 transparency."
---

# Momo Transparent Imagegen

## Overview

Create transparent-background PNG/WebP assets from natural-language image requests. This skill exists for requests like "生成一张苹果图标，透明底", "game coin PNG, no background", "transparent sticker", "alpha PNG", or "cutout asset".

The default path is **built-in `image_gen` + flat chroma-key background + local alpha extraction**. Do not promise native transparency from `gpt-image-2`; that path does not support `background=transparent` in the existing CLI/helper workflow.

## Trigger Interpretation

Treat the request as transparent-output work when the user says any of:

- Chinese: `透明底`, `透明背景`, `无背景`, `去背景`, `抠图`, `png`, `生成 png 图`, `参考图生成透明底图片`, `生成游戏图标透明底`.
- English: `transparent background`, `no background`, `alpha PNG`, `PNG cutout`, `sticker`, `isolated subject`, `transparent icon`.

If the user only says `PNG`, treat it as a transparent-output request when the subject is a standalone asset, icon, sprite, sticker, product cutout, UI element, prop, item, logo mark, decal, or game art asset. If the user asks for a full scene, photo, poster, or background image and only mentions PNG as a file format, keep the background unless they also ask for transparency.

## Suitability Gate

Best candidates for chroma-key transparency:

- simple opaque icons
- stickers and decals
- product cutouts
- game sprites, props, items, weapons, coins, pickups
- UI icons and buttons
- logos or marks without fine translucent edges

High-risk candidates:

- complex hair, fur, feathers, smoke, dust, fog, fire with soft edges
- glass, liquids, translucent fabric, semi-transparent objects
- reflective objects, realistic shadows, soft cast shadows
- subjects whose required colors conflict with practical key colors

For high-risk candidates, explain the risk briefly before generation if it could materially affect quality. If the user asks for true/native transparency, or if chroma-key removal fails QC, explain that the default path is chroma-key removal and ask before switching to CLI true-transparent fallback.

## Default Workflow

1. Decide whether the request is a new image or an edit/reference-based image.
2. Pick a key color:
   - Use `#00FF00` by default.
   - Use `#FF00FF` when the subject contains green hues, plants, grass, foliage, or any color too close to the default green key.
   - Avoid key colors that must appear in the subject.
3. Rewrite the prompt using `references/prompt-patterns.md`.
4. Use built-in `image_gen` to generate a source image on the flat key background.
5. Copy the selected generated source from `$CODEX_HOME/generated_images/...` into the project or a working folder.
6. Run the system helper:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
  --input <source.png> \
  --out <final-transparent.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill
```

7. Validate with `scripts/inspect_alpha.py`.
8. If a colored fringe remains, retry once with `--edge-contract 1`. Use `--edge-feather 0.25` only for visibly stair-stepped opaque edges, not for glass/smoke/soft-shadow subjects.
9. Return the final transparent PNG/WebP path, the source chroma-key path if saved, the key color, and the prompt used.

## Prompt Contract

Every transparent-output prompt must include:

- perfectly flat solid key background
- no shadows, cast shadows, contact shadows, floor plane, gradients, texture, reflections, or lighting variation in the background
- full subject visible with generous padding
- crisp silhouette / clean readable edges
- do not use the key color anywhere in the subject
- no watermark, no logo unless the user requests a logo, no text unless text is explicitly requested

Read `references/prompt-patterns.md` for copy-ready scaffolds.

## Native Transparency Fallback

Do not silently switch to CLI fallback or another model for native transparency.

If needed, say:

```text
The default path uses built-in image generation on a flat chroma-key background plus local alpha extraction. This request may need true/native transparency because <reason>. In the current helper workflow, gpt-image-2 does not support background=transparent; true transparency requires the CLI fallback with a model that supports transparent background and an OPENAI_API_KEY. Do you want me to use that fallback?
```

Only proceed with CLI fallback after explicit confirmation, unless the user already explicitly requested that fallback/model/path.

## Resources

- `references/prompt-patterns.md`: prompt scaffolds and key-color selection.
- `references/qc-checklist.md`: alpha and edge quality checklist.
- `scripts/inspect_alpha.py`: dependency-light PNG alpha inspection.
