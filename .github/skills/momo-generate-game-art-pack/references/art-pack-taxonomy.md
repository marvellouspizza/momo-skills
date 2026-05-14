# Art Pack Taxonomy

Use this reference to choose a v1 art pack scope. Start with one preset, then add optional categories only when the user asks for a broader menu.

## Presets

| Preset | Use when | First approval gate | Default categories |
| --- | --- | --- | --- |
| `minimal_playable_pack` | The user wants the smallest playable resource set. | Fixed six direction samples. | Player, one enemy, core terrain, drops, core interactables, HUD/hotbar, inventory basics, core VFX. |
| `topdown_rpg_pack` | Top-down or 3/4 RPG, adventure, cozy action, town/field exploration. | Fixed six direction samples. | Player, NPCs, enemies, tiles/terrain, props, interactables, pickups, UI, dialogue frame, VFX. |
| `cozy_farming_pack` | Farming, crafting, home decoration, collecting. | Fixed six direction samples. | Crops, seeds, plots, tools, farm feedback, gatherables, crafting objects, home props, shop UI, inventory UI. |
| `combat_action_pack` | Combat-first action loop or arena game. | Fixed six direction samples. | Hero actions, enemy actions, projectiles, impacts, hit/death VFX, drops, combat HUD, skill icons. |
| `side_scroller_pack` | Platformer, runner, side-view shooter, brawler, Metroidvania. | Fixed six direction samples. | Hero actions, side enemies, parallax layers, platforms, hazards, pickups, checkpoints, doors, combat FX, HUD. |
| `tactical_grid_pack` | Tactical RPG, board battler, factory/grid game. | Fixed six direction samples. | Unit sprites, terrain tiles, cursor/selection states, effect overlays, grid UI, objective icons, resource nodes. |
| `monster_taming_pack` | Creature collecting, evolution, battles, overworld routes. | Fixed six direction samples. | Player, creature line, wild creatures, battle FX, route tiles, encounter zones, UI icons, creature status panels. |
| `full_v1_pack` | The user wants a broad starter art kit. | Fixed six direction samples. | All core categories below, limited to first playable-loop depth. |

## Detailed Categories

### Actors

- Player or hero.
- Alternate player outfits or color variants.
- NPC roles: merchant, quest giver, healer, villager, guide, guard.
- Companion, pet, summon, or helper unit.
- Enemy families: basic, ranged, tank, flyer, hazard creature, elite, boss.
- Evolution or growth lines for creature games.
- Actor states: idle, walk, run, attack, shoot, cast, hurt, death, jump, hover, charge.

### Combat and FX

- Melee body animation.
- Wide slash / weapon trail as separate FX.
- Ranged body animation.
- Projectile loop.
- Impact burst.
- Explosion / vanish / death puff.
- Hit flash or damage marker.
- Dodge, dash, guard, shield, heal, buff, debuff.
- Warning telegraphs: circle, cone, line, area marker.
- Loot drop sparkle and pickup feedback.

### Maps and Levels

- `tile_mode`: editable tilesets and tile/object layers.
- `scene_mode`: foundation map plus separate props and placement metadata.
- `side_scroll_mode`: parallax layers plus platforms/objects/collision.
- `grid_mode`: logical grid with terrain/cost/build flags.
- `room_chunk_mode`: modular rooms with exits/sockets.
- `baked_scene_mode`: fixed backgrounds, title/menu art, battle backgrounds.
- Map subtypes: town, route, field, farm, home, dungeon, cave, shrine, forest, arena, shop, interior, boss room.

### Environment and Props

- Compact props: rocks, shrubs, flowers, logs, crates, barrels, sacks, pots, lamps, signs.
- Large props: trees, gates, doors, buildings, bridges, statues, towers, arches.
- Interactables: chest, mailbox, shop counter, workbench, crafting table, save point, portal, switch.
- Gatherables: ore, herb, mushroom, wood, fruit, fish spot, resource node.
- Hazards: spikes, brambles, poison puddle, cracked ground, traps.
- Foreground occluders: tree canopy, doorway, curtain, overhang, arch top.
- Terrain pieces: grass, dirt, path, water edge, cliff, stairs, floor, wall, platform, ledge.

### Gameplay Systems

- Farming: seed packets, crop stages, harvest items, field plot states, water/tilled feedback.
- Gathering: resource nodes, depleted states, respawn markers, collection VFX.
- Crafting: materials, tools, workstations, recipe icons, progress/complete feedback.
- Home decoration: furniture, decor props, placement ghost, invalid placement marker.
- Shop/economy: coins, price tags, shop panel, item cards, sell box.
- Questing: quest item icons, exclamation/question markers, objective pins.
- Inventory/items: consumables, materials, equipment, tools, weapons, key items.

### UI

- HUD: health, stamina/mana, time/day, weather, currency, minimap, objective tracker.
- Hotbar: slot, selected slot, disabled slot, quantity badge.
- Inventory: panel, grid slot, item detail, tabs, scrollbar, tooltip.
- Dialogue: text panel, nameplate, choice buttons, portrait frame.
- Shop/crafting: list rows, recipe cards, price badges, quantity stepper.
- Pause/settings: modal panel, toggles, sliders, back/confirm/cancel buttons.
- Mobile/touch: joystick, attack, dodge, interact, inventory, pause, tool switch.
- Icons: items, skills, status, warnings, controls, map markers.

### Metadata and Engine Handoff

- Slicing manifest.
- Runtime filename plan.
- Pivot / anchor / baseline.
- Y-sort and render layer.
- Collision footprint.
- Interaction anchor.
- Tile size, grid origin, terrain semantics.
- 9-slice margins for panels.
- Texture filter, mipmap, compression.
- Parallax scroll factors.
- Spawn points, exits, zones, camera bounds.

## Expansion Rules

- Do not choose `full_v1_pack` automatically for a new user. Start with `minimal_playable_pack` unless they explicitly ask for broad coverage.
- Always run the complete six-sample first approval gate before full expansion.
- After style approval, generate all selected categories as candidates, not as final runtime assets.
- Keep rare or high-risk categories optional: bosses, large buildings, complex parallax stacks, full tile autotiling, animated UI, and large hero action atlases.
