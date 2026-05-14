# Workflow Status Gates

Use these status gates for every generated game art pack.

## Status Values

| Status | Meaning | May enter runtime assets? |
| --- | --- | --- |
| `Draft` | Planned but not generated. | No |
| `Generated` | Output exists and awaits review/QC. | No |
| `Needs Revision` | Output needs prompt changes or regeneration. | No |
| `Rejected` | Do not use. Keep for provenance only. | No |
| `Approved for Expansion` | Style or candidate direction is accepted. It may guide more generation. | No |
| `Approved for Game Asset` | User explicitly approved this candidate or derived runtime output group for game use. | Eligible for controlled intake only |
| `Godot Ready` | Destination, slicing, naming, pivot, import settings, and QC are documented. | Not copied yet unless task says intake |
| `Imported` | Approved files have been exported/copied to runtime asset paths and import metadata exists when applicable. | Already intaken |
| `Verified` | Runtime visuals were checked in game/editor/tests. | Yes |

## Gate Rules

- Do not treat reference images or first-pass samples as game assets.
- Do not promote a whole source sheet when only derived slices are approved.
- Do not copy to `assets/` from `Approved for Expansion`.
- Do not use "approved" in a filename as evidence of `Approved for Game Asset`; only tracking rows count.
- Preserve source prompts, source paths, generation dates if known, review notes, and QC notes.
- Record why deferred assets remain deferred.

## First Approval Gate

The first user approval should normally answer only:

- Does the style direction work?
- Are proportions, palette, linework, and mood acceptable?
- Which small changes are needed before full expansion?

After this gate, mark samples as `Approved for Expansion`.

## Game Asset Approval Gate

Before marking any resource `Approved for Game Asset`, record:

- Candidate or derived output group ID.
- Source path and prompt record.
- Approved runtime use.
- Target runtime directory.
- QC result.
- Known limitations.
- User approval statement or Controller decision reference.

## Intake Checklist

Before copying/exporting files into runtime asset paths:

- Tracking row says `Approved for Game Asset`.
- The exact approved file set is named.
- Source candidate files remain unchanged.
- Runtime filenames are lowercase snake_case and versioned with `v###`.
- Target paths are documented.
- Pivot/anchor, slicing, Y-sort, collision/interaction anchors, filter, mipmap, compression, and 9-slice notes are recorded where relevant.
- Binary file rules such as Git LFS are understood.
- `.DS_Store`, temporary files, rejected variants, contact sheets, and rough references are excluded.

## Suggested Target Paths

Use these defaults when the target project has no stronger convention:

```text
assets/art/characters/
assets/art/enemies/
assets/art/npcs/
assets/art/environment/terrain/
assets/art/environment/props/
assets/art/environment/interactables/
assets/art/environment/hazards/
assets/art/environment/crops/
assets/art/maps/
assets/art/ui/hud/
assets/art/ui/panels/
assets/art/ui/icons/
assets/art/ui/touch_controls/
assets/art/vfx/combat/
assets/art/vfx/farm_tools/
assets/art/vfx/pickups/
```
