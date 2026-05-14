# Momo Transparent Imagegen

`momo-transparent-imagegen` is a Codex skill for generating transparent-background PNG/WebP images from natural-language prompts.

It is meant for requests like:

- "Generate a game coin PNG, no background."
- "Create a sticker of a smiling apple with transparent background."
- "生成一张苹果图标，透明底。"
- "画一个游戏金币 png，无背景。"

中文文档见 [README.zh-CN.md](README.zh-CN.md)。

## What It Does

- Detects transparent-background requests in English and Chinese.
- Writes stronger prompts for clean background removal.
- Chooses a chroma-key color:
  - `#00FF00` by default
  - `#FF00FF` when the subject is too close to the default green key
- Requires:
  - flat solid key background
  - no shadows
  - no gradients
  - no reflections
  - no floor plane
  - crisp edges
  - generous padding
  - key color absent from the subject
- Uses the system helper:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py"
```

- Provides a lightweight `scripts/inspect_alpha.py` QC helper.

## Install

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/marvellouspizza/momo-transparent-imagegen.git ~/.codex/skills/momo-transparent-imagegen
```

Invoke it explicitly with:

```text
Use $momo-transparent-imagegen: generate a game coin PNG with no background.
```

Or in Chinese:

```text
Use $momo-transparent-imagegen：生成一张游戏金币 png，无背景，透明底。
```

## Transparency Workflow

The skill uses built-in image generation on a clean chroma-key source, then removes that background locally and validates the alpha channel:

```text
built-in image_gen -> flat chroma-key source -> remove_chroma_key.py -> transparent PNG
```

If a request involves difficult edges such as hair, glass, smoke, glow, or translucent materials, the skill should explain the risk before using a fallback workflow.

## Good Candidates

- Game icons
- UI icons
- Item art
- Props
- Product cutouts
- Stickers
- Logos or marks
- Simple game sprites

## Risky Candidates

- Hair, fur, feathers
- Smoke, fog, dust, fire, glow
- Glass, liquid, translucent fabric
- Realistic reflections
- Soft shadows
- Subjects whose colors conflict with all practical key colors

## Alpha QC

Inspect a transparent PNG:

```bash
python3 scripts/inspect_alpha.py output.png
```

JSON output:

```bash
python3 scripts/inspect_alpha.py output.png --json
```

## Files

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/openai.yaml
├── references/
│   ├── prompt-patterns.md
│   └── qc-checklist.md
└── scripts/
    └── inspect_alpha.py
```
