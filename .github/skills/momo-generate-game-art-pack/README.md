# Generate Game Art Pack

`momo-generate-game-art-pack` is a Codex skill for turning a small set of visual reference images into a reviewed, production-oriented 2D game art pack workflow.

It is designed for teams or solo creators who want a repeatable pipeline:

1. Upload several reference images.
2. Define a game art style without copying the references.
3. Generate the fixed six-image approval batch.
4. After style approval, expand into a selected v1 art pack.
5. Track prompts, candidates, QC, slicing plans, naming, and engine import notes.

The skill is generic and can adapt to top-down RPGs, cozy farming games, action combat prototypes, side-scrollers, tactical grid games, monster-taming games, and broader v1 starter kits.

中文文档见 [README.zh-CN.md](README.zh-CN.md)。

## What It Does

- Creates a style definition draft from user-provided reference images.
- Uses references as inspiration only; it explicitly avoids copying characters, poses, costumes, layouts, logos, or distinctive motifs.
- Generates the required first approval batch:
  - one player or hero sample
  - one basic enemy or creature sample
  - one home/farm or safe-base scene sample
  - one wild/combat or dangerous-area scene sample
  - one HUD sample
  - one inventory or item-panel sample
- Expands the approved style into configurable v1 pack presets.
- Records every prompt, purpose, status, review result, QC risk, and next gate.
- Supports candidate tracking for sprites, props, maps, UI, icons, VFX, and Godot-style import planning.
- Separates `Approved for Expansion` from `Approved for Game Asset` so preview art does not accidentally become runtime art.

## Pack Presets

The skill includes these pack presets:

- `minimal_playable_pack`
- `topdown_rpg_pack`
- `cozy_farming_pack`
- `combat_action_pack`
- `side_scroller_pack`
- `tactical_grid_pack`
- `monster_taming_pack`
- `full_v1_pack`

Detailed category guidance lives in [`references/art-pack-taxonomy.md`](references/art-pack-taxonomy.md).

## Repository Layout

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── templates/
├── references/
│   ├── art-pack-taxonomy.md
│   ├── map-and-sprite-routing.md
│   ├── prompt-patterns.md
│   └── workflow-status-gates.md
└── scripts/
    ├── create_art_pack_docs.py
    └── qc_image_manifest.py
```

## Installation

Clone or copy this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/marvellouspizza/momo-generate-game-art-pack.git ~/.codex/skills/momo-generate-game-art-pack
```

After that, invoke it in Codex with:

```text
Use $momo-generate-game-art-pack to turn my reference images into a reviewed v1 2D game art pack.
```

## Typical Workflow

1. Ask the user for reference images or use the images already attached.
2. Draft the art style definition.
3. Wait for style confirmation.
4. Generate the fixed six-image approval batch.
5. Mark approved samples as `Approved for Expansion`.
6. Expand the selected pack preset.
7. Run QC and document slicing/import notes.
8. Only mark specific candidates or derived runtime groups as `Approved for Game Asset` after explicit approval.

## Included Scripts

Create starter tracking docs:

```bash
python3 scripts/create_art_pack_docs.py --out docs/art-pack --pack-name my-game-v1
```

Inspect PNG dimensions and alpha information:

```bash
python3 scripts/qc_image_manifest.py path/to/images --md-out qc_manifest.md
```

`qc_image_manifest.py` can use Pillow when installed, but falls back to PNG header inspection for basic size and alpha checks.

## Status Gate Philosophy

Generated art is not a game asset by default.

The skill uses this gate flow:

```text
Draft -> Generated -> Approved for Expansion -> Approved for Game Asset -> Godot Ready -> Imported -> Verified
```

This keeps direction samples, candidate sheets, runtime slices, and imported engine assets clearly separated.

## Notes

- Creative raster art should come from built-in image generation.
- Scripts are deterministic helpers only.
- For transparent candidates, the default workflow uses a flat chroma-key background plus local cleanup/QC.
- For playable maps, foundation/base layers should not bake in runtime-controlled props, actors, hazards, UI, or collision-critical objects.
