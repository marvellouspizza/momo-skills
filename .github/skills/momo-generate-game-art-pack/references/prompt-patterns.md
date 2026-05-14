# Prompt Patterns

Use these patterns to write prompts manually. Do not outsource creative prompt writing to a script.

## Style Definition Draft

Before generating the first batch, summarize:

- Character proportion and shape language.
- Scene perspective and spatial layers.
- Palette, lighting, materials, and contrast.
- UI tone and readability rules.
- Animation or pseudo-animation strategy.
- Unified imagegen style words.
- Banned motifs and anti-copy constraints.

## First Approval Batch

The default and required first approval batch contains exactly six art-direction review samples:

1. Player/hero direction sample.
2. Basic enemy/creature direction sample.
3. Home/farm or safe-base scene direction sample.
4. Wild/combat or dangerous-area scene direction sample.
5. HUD direction sample.
6. Inventory/item-panel direction sample.

Mark first batch output as review samples only. Do not call them final assets.
Do not reduce this gate to fewer samples or to one-category samples. The six-sample review is what locks cross-category style consistency.

## Generic Style Prompt Scaffold

```text
Use case: stylized-concept
Asset type: art direction review sample only, not a final game asset
Primary request: <specific sample or asset>
Input images: Use the attached images only as abstract inspiration for palette, linework, mood, shape language, and material treatment. Do not copy characters, poses, costumes, compositions, symbols, logos, or distinctive motifs.
Game context: <genre, perspective, target engine if known>
Subject: <asset subject>
Perspective: <topdown | 3/4 top-down | side-view | UI mockup | etc.>
Style: <approved style words>
Palette: <approved palette, contrast, saturation, shadow rules>
Readability: clear silhouette, game-scale readable, stable shape language, no excessive tiny detail.
Avoid: copied reference content, third-party IP, text, logo, watermark, muddy colors, blurry outlines, unwanted perspective.
```

## Transparent Candidate Prompt Scaffold

```text
Use case: stylized-concept
Asset type: transparent candidate sheet for later slicing and QC
Primary request: <asset or sheet>
Sheet layout: <single asset | 2x2 | 3x3 | 4x4 | custom grid | row-major list>
Runtime use: <how the game will use this asset>
Style reference: Use the approved style definition only. Keep palette, line weight, material language, and proportions consistent.
Background: perfectly flat solid #FF00FF chroma-key background in every cell. No shadows, gradients, texture, floor plane, border, guide marks, labels, or text.
Containment: every object fully inside its cell with generous magenta margin. No object, limb, weapon, sparkle, leaf, smoke, or fragment may touch or cross a cell edge.
Consistency: same scale, same camera angle, same lighting, same identity family across cells.
Avoid: copied reference motifs, baked UI text, edge cropping, unintended color cast, over-detail, noisy texture, mixed perspective.
```

## Map Foundation Prompt Scaffold

Use for playable/editable maps before generating props.

```text
Create a <perspective> 2D game map foundation layer.
This is a BASE / FOUNDATION MAP ONLY for a layered runtime scene.
Include only ground, paths, terrain materials, water/edge shapes, floor markings, low terrain details, and empty prop pads.
Do not include runtime-controlled objects: no buildings, trees, crates, chests, doors, signs, pickups, hazards, enemies, NPCs, player characters, UI, text, labels, or foreground occluders.
Make walkable routes and zone boundaries readable.
Use the approved art style and palette.
No logo, no watermark, no text.
```

## Prop Pack Prompt Scaffold

Use square prop packs only for compact props.

```text
Create exactly one <ROWS>x<COLS> transparent prop candidate sheet.
Each cell contains one separate static compact environmental prop in row-major order:
1. <prop>
2. <prop>
...
All props share the same biome, palette, perspective, lighting, and approved art style.
Every prop is fully visible, centered, and contained in the central 50% to 60% of its cell with generous flat #FF00FF margin.
This sheet must contain only compact props. Do not include floors, platforms, bridges, walls, ladders, long hazards, gates, doors, buildings, wide trees, roads, ramps, slopes, or collision-critical objects.
Background is 100% solid flat #FF00FF. No shadows, labels, UI, watermark, numbers, arrows, borders, grid lines, or readable letters.
```

## UI Prompt Scaffold

```text
Use case: ui-mockup
Asset type: UI direction sample or candidate component sheet
Primary request: <HUD / inventory / icons / controls>
Runtime use: <screen or system>
Style: match approved game art style while prioritizing readability.
Layout: stable, uncluttered, no baked text unless the user explicitly provides exact text.
Components: <list of slots, bars, buttons, tabs, panels, icons>
States: normal, hover/selected, disabled, warning, pressed where relevant.
Palette: <approved palette>
Avoid: generated readable text, tiny illegible detail, heavy shadows, low contrast, copied UI from references, logo, watermark.
```

## Anti-Copy Checklist

Always include:

- Use references as abstract inspiration only.
- Do not copy specific characters, costumes, props, poses, compositions, logos, UI layouts, symbols, or distinctive motifs.
- Create original assets for the user's game.
- Avoid third-party IP or recognizable franchise style imitation.
