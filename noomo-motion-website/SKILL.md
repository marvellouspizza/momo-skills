---
name: noomo-motion-website
description: Generate complete standalone Vite React visual narrative single-page websites that transfer the Noomo reference site's high-fidelity motion language, UI language, scroll choreography, loading experience, immersive controls, and 12-section structure onto a user's own theme, content, colors, and reference object. Use when the user asks for a Noomo-style site, Noomo motion replication, a visual storytelling website with Noomo-like animation, or a reusable skill-generated animated single-page website.
---

# Noomo Motion Website

Generate a complete independent Vite React project that applies the Noomo Motion Language to the user's own subject. Preserve the motion and UI system; replace the content, palette, object, copy, and narrative with the user's theme.

## Load References

Load only what the task needs:

- For every generation task, read `references/section-blueprint.md`, `references/motion-modules.md`, `references/ui-language.md`, and `references/implementation.md`.
- For revisions or QA, also read `references/qa.md`.
- Use `scripts/create_project.py` to create the starter project directory when beginning a new generated site.

## Default Output

Create a full project at:

```text
generated/noomo-motion-{slug}/
```

The generated project must be standalone and deployable. Do not reference the Noomo source site's `_nuxt`, original models, textures, images, audio, JavaScript chunks, or private resources at runtime.

## Intake

Proceed with sparse input. Ask only for critical gaps that block generation.

Minimum useful input:

- Website theme or brand.
- Audience or desired feeling, if provided.
- One reference object image, if provided.
- Optional colors or required content.

If the user gives no reference image, generate or propose a reference object first. For image generation, use Codex Imagen-2 when available and save derived assets inside the generated project's deployable assets folder.

## Required Structure

Always generate a visual narrative single-page website with exactly 12 complete Narrative Sections by default. Loading and entering are required, but they do not count as one of the 12 sections.

Do not collapse sections, replace sections with placeholders, or ship a hero-only page. Each section must have:

- A reader-facing heading or clear visual/copy role.
- Publishable copy.
- A Section Motion Responsibility.
- Assigned `NM-*` motion modules.
- A responsive mobile treatment.

## Navigation Reachability Rule

Fixed header links, menu items, CTA anchors, and in-page feature anchors must never land on a blank scroll lead-in or a pure camera-transition span. Long Noomo sections may use large `vh` ranges for scroll choreography, but direct navigation must target a readable content moment.

Implementation requirements:

- Each navigable section must expose a content target such as `[data-section-content]` that contains the reader-facing heading/body for that section.
- Header/menu anchors must either use Lenis/GSAP `scrollTo` to move to that content target with an offset, or use real fragment targets placed on the content target rather than the long outer section shell.
- Do not rely on native `href="#section-id"` when the section is hundreds of viewport-heights tall and the visible copy is vertically centered or delayed.
- After direct navigation, the viewport must show the section's key heading or clear visual/copy role without requiring the user to scroll further.
- Preserve meaningful URLs by updating the hash after custom smooth navigation.

## Required Motion Stack

Use the strong default stack:

- Vite + React.
- GSAP + ScrollTrigger + `@gsap/react`.
- Lenis for smooth scrolling.
- Three.js or React Three Fiber for the primary object scene.
- Shader-like material treatment through Three.js, CSS masks, SVG filters, or canvas where practical.
- Local generated assets under `public/assets/generated/`.

## Generation Workflow

1. Define the theme model: audience, promise, emotional tone, 12-section story, and color roles.
2. Choose the Reference Object treatment automatically with true 3D as the default: imported GLB when available, otherwise procedural Three.js geometry. Use layered 2.5D only as a user-approved downgrade or as supporting texture/mask/background material.
3. Create the project with `scripts/create_project.py`.
4. Implement the 12 sections, global fixed UI, loading/intro, cursor, sound toggle or ambient control, and bottom CTA.
5. Build the scroll engine: Lenis + GSAP ticker + normalized section progress + ScrollTrigger timelines.
6. Implement the primary object scene and bind it to scroll progress.
7. Generate `MOTION_BRIEF.md` documenting all sections, modules, object treatment, colors, and mobile choices.
8. Run install/build checks and start a local preview server.
9. Give the user the local preview URL for user-guided review.

## Fidelity Rules

- High-fidelity motion recreation outranks convenience.
- Do not treat a previous generated site as a reusable page template. Reusing scroll plumbing, asset loading, or utility components is allowed, but the section composition, content hierarchy, visual motifs, interaction metaphors, and supporting UI must be redesigned for the user's subject. A tea/product ritual site, a virtual character IP site, a venue site, and a tool site should not share the same visible layout with swapped copy and colors.
- Before final QA, run an anti-reskin check: name at least three visible choices that are specific to the current subject and would be inappropriate for the most recently generated unrelated site. If the page would still make sense after swapping only the title/object/palette, it fails QA and must be revised.
- The primary visual object must be true 3D by default: imported GLB or procedural Three.js geometry. A 2D image plane or 2.5D layered image may support textures, references, masks, particles, or background plates, but it must not be the central object unless the user explicitly accepts that downgrade.
- For high-fidelity hero objects, prefer a generated or authored GLB pipeline over JSX-only primitives. Use Blender when available to model/export the reference object, then load the GLB in R3F and apply runtime materials, camera choreography, and scroll-bound animation.
- Preserve scroll rhythm, camera choreography, object centrality, glass/iridescent material atmosphere, text blur/scale reveals, fixed immersive controls, cursor behavior, loading reveal, and dark final transition.
- Theme skinning is allowed; motion structure is not optional.
- Mobile must be same-style high fidelity, with independent framing where needed.
- Sound is conservative by default: off until user interaction, always controllable.
- Use publishable content, never lorem ipsum or TODO copy.

## Deliverables

Each generated project must include:

- `package.json`, `index.html`, Vite config, React source, styles, and assets.
- `MOTION_BRIEF.md`.
- A running local preview URL.
