---
name: momo-generate-game-art-pack
description: "Generate reviewed 2D game art packs from user reference images. Use when Codex needs to turn style references into a reusable v1 game art resource pipeline: style definition, first-pass approval samples, batch image-generation prompts, candidate asset records, QC notes, slicing plans, naming conventions, Godot or engine import notes, and optional full-pack expansion after one style approval gate. Triggers include requests for full game art packs, v1 base art, sprite packs, map art packs, UI/icon packs, generated game assets from references, reusable imagegen art pipelines, and Chinese requests such as 参考这个图片生成游戏美术资源, 根据参考图生成游戏美术资源, 上传参考图生成 v1 游戏美术资源包, 用这些图片生成角色场景 UI 图标地图怪物资源, 先分析这些参考图的美术风格再生成 6 张方向审核样张."
---

# Generate Game Art Pack

## Overview

Create a reviewed 2D game art production flow from a small set of user reference images. The skill is generic: adapt to the target game genre, perspective, engine, and pack preset instead of assuming one fixed project.

Use built-in image generation for creative raster art. Use local scripts only for deterministic documentation, chroma-key cleanup, slicing/QC assistance, metadata, manifests, and template creation.

## Core Workflow

1. **Collect inputs**
   - Treat user images as style inspiration only unless they explicitly say an image is an edit target.
   - Record reference roles: palette, linework, proportion, UI mood, map mood, material language, or composition.
   - Infer game genre, perspective, target engine, art style, and desired pack preset. If unknown, choose `minimal_playable_pack`.

2. **Define style before generating**
   - Produce a style definition draft covering character proportions, shape language, map view, layer model, palette, lighting, materials, UI tone, animation approach, prompt style terms, and anti-copy rules.
   - Include explicit "do not copy" constraints for protected or user-provided references.
   - Do not generate the full pack until the user approves the style definition or asks to proceed with the recommended default.

3. **Generate the fixed six-image approval batch**
   - First style gate always uses the complete six direction samples: player/hero, basic enemy/creature, home/farm scene, wild/combat scene, HUD, and inventory/item panel.
   - Do not reduce this gate to a partial category-only or shortened approval flow. UI and map resources can still be expansion categories, but the style gate stays complete.
   - Mark these outputs as `Approved for Expansion` only after user approval. They are not runtime assets.

4. **Expand after approval**
   - After the user approves the first batch style, continue generating the selected pack without stopping for more style approval.
   - Still keep every output in candidate/tracking docs. Do not copy into runtime asset folders or mark `Approved for Game Asset` unless the user explicitly approves that gate.
   - Use the category menus in `references/art-pack-taxonomy.md`.

5. **Record every batch**
   - Use the templates in `assets/templates/` or run `scripts/create_art_pack_docs.py`.
   - Record prompt, purpose, source/reference role, output path, status, review result, QC risks, and next gate.
   - Prefer lowercase snake_case runtime names with `v###` version suffixes.

6. **QC and import planning**
   - For generated transparent resources, validate dimensions, alpha, transparent corners, edge residue, slicing feasibility, and game-scale readability.
   - For maps, keep foundation/base art separate from runtime props, collision, zones, exits, spawns, and foreground occluders.
   - For Godot, record pivot/anchor, Y-sort, texture filter, mipmap, compression, 9-slice, scale, frame order, and target path.

## Pack Selection

Read `references/art-pack-taxonomy.md` when choosing what to generate. Prefer a named preset:

- `minimal_playable_pack`
- `topdown_rpg_pack`
- `cozy_farming_pack`
- `combat_action_pack`
- `side_scroller_pack`
- `tactical_grid_pack`
- `monster_taming_pack`
- `full_v1_pack`

If the user asks for "more categories" or "let users choose", present the preset menu plus the detailed category checklist. Do not force all categories into the first run.

## Prompting

Read `references/prompt-patterns.md` before writing image prompts. Keep prompts explicit about:

- use case and asset type
- reference image role
- perspective and runtime use
- palette and linework
- sheet/grid shape when applicable
- solid chroma-key background for transparent candidates
- no text, logo, watermark, labels, or copied reference motifs

For transparent candidate assets, prefer a flat `#FF00FF` chroma-key background and then local cleanup/QC. Use true native transparency only when the available image-generation workflow explicitly supports it and the user has approved that path.

## Status Gates

Read `references/workflow-status-gates.md` before promoting anything.

Important defaults:

- `Approved for Expansion` means style or candidate direction is accepted. It is not permission to ship or import.
- `Approved for Game Asset` requires explicit user approval for a specific candidate or derived runtime output group.
- Do not copy candidate images into a runtime `assets/` tree unless the approval record says `Approved for Game Asset` and the task explicitly includes intake.
- Source sheets and references remain provenance. Runtime assets should be sliced/exported outputs with stable names.

## Map and Sprite Routing

Read `references/map-and-sprite-routing.md` when the request involves map modes, prop packs, animation sheets, or engine-ready metadata.

Use these principles:

- Generate actor/body action sheets separately from wide FX, projectiles, impacts, and muzzle/slash effects.
- Do not pack unrelated hero actions into one raw generated sheet; assemble engine atlases only after per-action QC.
- For playable maps, do not ship a single baked image unless the user explicitly asks for a flat background.
- Foundation map layers should contain only ground and low terrain; props, interactables, hazards, actors, pickups, and foreground occluders must be separate runtime objects or metadata.

## Resources

- `references/art-pack-taxonomy.md`: pack presets and detailed resource categories.
- `references/prompt-patterns.md`: style definition and image prompt templates.
- `references/workflow-status-gates.md`: approval gates, review statuses, and intake rules.
- `references/map-and-sprite-routing.md`: map/sprite routing based on agent-sprite-forge-style contracts.
- `assets/templates/`: reusable tracking document templates.
- `scripts/create_art_pack_docs.py`: create a starter docs folder from templates.
- `scripts/qc_image_manifest.py`: inspect PNG dimensions/alpha and emit a QC table.
