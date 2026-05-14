# Map and Sprite Routing

This reference distills map/sprite production rules inspired by agent-sprite-forge-style workflows. Use it to choose generation shape and deliverables.

## Sprite Asset Types

- `player`: controllable hero.
- `npc`: role-readable non-player character.
- `creature`: monster, beast, spirit, boss, summon.
- `character`: humanoid unit that is not clearly player or NPC.
- `spell`: cast + projectile + impact bundle.
- `projectile`: traveling loopable object.
- `impact`: hit burst, explosion, contact effect.
- `prop`: item, weapon, shrine object, pickup, deployable.
- `summon`: conjured unit or entrance effect.
- `fx`: generic visual effect sheet.

## Action Defaults

- `idle`: 2x2 for standard actors; 3x3 for large creatures or showcase loops.
- `walk`: 4x4 for top-down four-direction movement; 2x2 for compact side-view movement.
- `run`: 2x2 or 2x3.
- `attack`: 2x2 or 2x3 body-only for heroes; separate slash/impact FX.
- `shoot`: body sheet plus separate projectile/muzzle/impact.
- `cast`: 2x3.
- `hurt`: 2x2.
- `death`: 2x3 or 4x4 for richer disappear/collapse.
- `projectile`: 1x4 or 2x2.
- `impact` / `explode`: 2x2.

## Actor Sheet Guardrails

- Do not use raw single-row sheets for animated bodies unless the engine specifically requires a delivery strip and the frames are assembled after QC.
- Do not pack unrelated hero actions into one raw generated sheet.
- Generate one action family per raw sheet, then assemble an engine atlas deterministically if required.
- Keep wide slash arcs, muzzle flashes, projectiles, dust trails, and impact bursts separate from hero body sheets unless the runtime supports wider per-action cells and explicit origins.
- Preserve identity, scale, body height, and anchor line across frames.

## Map Modes

| Mode | Use when | Deliverables |
| --- | --- | --- |
| `tile_mode` | RPG routes, towns, grid-perfect editors, Godot TileMap, Tiled, LDtk. | Tileset art, tile layers, object layers, collision, exits, preview. |
| `scene_mode` | Top-down/cozy/action scene with beautiful base plus props. | Foundation base, dressed reference, separate props, placement metadata, collision/zones, preview. |
| `side_scroll_mode` | Platformer, runner, brawler, side-view action, Metroidvania. | Parallax layers, stage reference, platform/object sprites, hazards, pickups, checkpoints, collision, camera bounds. |
| `grid_mode` | Tactical RPG, factory, board/card battler. | Grid dimensions, tile/cell art, terrain metadata, build/walk flags, object slots, preview. |
| `room_chunk_mode` | Roguelike rooms, modular dungeons, procedural assembly. | Chunks, sockets/exits, collision, spawn markers, seam validation, assembled preview. |
| `baked_scene_mode` | Fixed background, title/menu, visual novel, battle background. | One image plus optional coarse zones; no editable runtime object expectation. |

## Layer Separation

For playable maps, do not treat a single beautiful image as the whole runtime map unless the user explicitly asks for a flat background.

Base/foundation layers may include:

- ground material
- paths
- water or cliff edges
- low terrain markings
- floor patterns
- empty pads for props

Base/foundation layers must not include:

- tall props
- buildings
- trees
- crates/chests
- doors/gates
- pickups
- hazards
- traps
- actors/enemies/NPCs
- UI/text/labels
- foreground occluders

## Prop Strategy

- Use square 2x2, 3x3, or 4x4 prop packs only for compact props.
- Use one-by-one generation for large, tall, irregular, important, animated, identity-sensitive, or collision-aligned props.
- Use 1x3 or 1x4 strips for repeatable floors/platforms/bridges: left cap, middle repeat, right cap, optional slope/corner/end.
- Use custom wide packs for several similar wide objects with explicit non-square cells.
- Never mix compact decorative props with platforms, buildings, gates, ladders, long hazards, or tileset pieces in one square pack.

## Metadata to Record

For sprites:

- rows/cols, frame order, action, direction, anchor, cell size, frame count, output paths.

For maps:

- map mode, visual model, object model, collision model, engine target, canvas size, layer order, placement data, collisions, zones, exits, spawns, camera bounds.

For Godot:

- target path, Texture2D import settings, filter, mipmap, compression, pivot, Y-sort, scene hookup notes, 9-slice margins, tile size, collision layer expectations.
