# Transparent Image Prompt Patterns

Use these patterns when generating source images for transparent-background output.

## Key Color Selection

- Default key: `#00FF00`.
- Use `#FF00FF` when the subject includes green hues, plants, grass, foliage, green clothing, green UI, or any color too close to the default green key.
- Avoid blue key colors for blue subjects.
- If no practical key color avoids the subject palette, warn that chroma-key extraction is risky.

## Standard Prompt Scaffold

```text
Use case: background-extraction
Asset type: transparent PNG/WebP candidate
Primary request: <user's requested subject>
Subject: <single clear subject, full object visible>
Style/medium: <illustration/photo/3D/game sprite/UI icon/etc.>
Composition/framing: single centered subject, generous padding on all sides, no cropping
Scene/backdrop: perfectly flat solid <KEY_COLOR> chroma-key background for local background removal
Constraints: background must be one uniform color with no shadows, no cast shadow, no contact shadow, no gradients, no texture, no floor plane, no reflections, and no lighting variation. Keep the subject fully separated from the background with crisp clean edges. Do not use <KEY_COLOR> anywhere in the subject. No watermark. No text unless explicitly requested.
Avoid: halos, glow bleeding into the background, soft shadow, background objects, edge cropping, partially hidden subject, transparent-looking glass/smoke unless user accepts risk.
```

## Game Asset Prompt Add-On

Use for sprites, props, items, icons, pickups, and UI assets:

```text
Game-readability: make the silhouette clear at small size, with stable shape language and strong object identity.
Runtime suitability: full object visible, clean outline, no baked ground shadow, no floor plane, no background scene, no labels.
```

## Product Cutout Prompt Add-On

Use for product or object cutouts:

```text
Preserve product identity and material details. Keep the object fully visible and isolated. No reflection, no tabletop, no studio floor, no shadow under the object.
```

## Sticker / Icon Prompt Add-On

Use for sticker-like requests:

```text
Sticker/icon suitability: bold readable silhouette, clean outer contour, simple interior detail, no tiny fragile edge particles.
```

## Risk Warning Triggers

Warn before generation when the requested subject relies on:

- hair, fur, feathers, smoke, dust, fog, mist
- glass, liquids, translucent materials, lace, semi-transparent fabric
- soft shadows, realistic reflections, glowing effects that need alpha falloff
- subject colors that overlap every practical key color

Suggested wording:

```text
This can be generated as a transparent PNG, but clean background removal may be risky because <reason>. I will use a flat chroma-key source with stronger edge constraints first; if QC fails, the next step is true transparency fallback after confirmation.
```
