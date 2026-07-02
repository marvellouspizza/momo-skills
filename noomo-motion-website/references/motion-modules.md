# Transferable Motion Modules

Use every visible Noomo behavior as an engineering module. Assign modules to sections rather than sprinkling generic effects.

Confidence labels:

- `source-derived`: recovered from local source, CSS, assets, or GLB structure.
- `observed`: verified in local preview.
- `inferred`: implementation model for recreating the effect.

## NM-001 Synthetic Smooth Scroll Timeline

Source confidence: source-derived.

Noomo maps an artificially long page to a global progress value. The original uses ScrollSmoother-like behavior with `smooth: 1.5`, `normalizeScroll: true`, `smoothTouch: true`, and section lengths summing to about `4230vh`.

Implementation: use Lenis + GSAP ticker. Define 12 normalized section ranges and expose global progress to CSS variables, ScrollTrigger timelines, and R3F scene state.

## NM-002 Click-to-Start Launch

Source confidence: source-derived.

First click starts the experience, enables sound permission, hides the prompt, and scrolls forward automatically. Desktop target is roughly `2 * viewportHeight` over `3s` with linear ease; mobile target is roughly `1.15 * viewportHeight`.

Implementation: show `Click to start` or equivalent, then trigger Lenis/GSAP scrollTo and set `experienceStarted`.

## NM-003 Feathered Radial Preloader Mask

Source confidence: source-derived.

Preloader uses a pale violet gradient and radial mask reveal with a feathered edge. Reference values: `--reveal-radius: 0vmax`, `--reveal-feather: 14vmax`.

Implementation: animate CSS custom properties for `mask-image: radial-gradient(...)`. Keep loader separate from the 12 sections.

## NM-004 Full-Viewport Reference Object

Source confidence: observed + source-derived.

The central object fills the viewport, carries the story, and remains visually present across major scroll beats. It may be glass, flame, crystal, mist, or a theme-specific material.

Implementation: prefer R3F. If no 3D model exists, use layered transparent images, planes, masks, particles, displacement, and fragments.

## NM-005 Split Text Blur-Scale Scatter

Source confidence: source-derived.

Large text splits into characters. On scroll, chars fade, scale to about `1.3`, and blur to about `8px`; negative stagger creates a reverse wave. Reference stagger: H1 `-0.05`, H2 `-0.03`.

Implementation: create char spans and animate with GSAP/ScrollTrigger scrub.

## NM-006 Camera Timeline Scroll Scrub

Source confidence: source-derived.

Noomo uses GLB timelines for camera, target, object, lights, feather, floor, and project anchors. The generated site must recreate this idea with code-defined keyframes if custom GLB timelines are unavailable.

Implementation: define camera/object/light keyframes per section and interpolate from global progress.

## NM-007 Iridescent Glass Material

Source confidence: source-derived.

Reference material uses refraction, reflection, iridescence, fringe, brightness peaks, and thickness. Reference values include `iorStart: 1.2`, `iorDelta: 0.3`, `fringeCurve: 5`, `fringeMix: 1`, `colorBoost: 2`.

Implementation: use `MeshPhysicalMaterial` with transmission, ior, roughness, thickness, env lighting, and optional shader/postprocessing.

## NM-008 Pointer Fluid Distortion

Source confidence: source-derived.

Pointer input feeds a fluid-like displacement map in the original. Generated sites may use a lighter equivalent when needed.

Implementation: use shader/FBO for high fidelity, or CSS radial gradients and pointer variables for local distortion.

## NM-009 Anchor Field

Source confidence: source-derived + observed.

Noomo uses project anchors along the 3D timeline. Generated sites can map anchors to features, ingredients, rituals, benefits, proof points, or cases.

Implementation: create 4-7 hoverable anchors with title/category/link metadata and scene response.

## NM-010 Fixed CTA Burst + Letter Wave

Source confidence: source-derived.

Fixed bottom CTA triggers a large circle burst and character wave. Reference burst scales about `0.2 -> 26`, opacity `.99 -> 0`, duration `3`, ease `power3.out`. Letter delay follows `abs(index-anchor) * .04`.

Implementation: split button text into spans, create a fixed burst layer, and invert text/icon color by section luminance.

## NM-011 Sound Gate and Visualizer

Source confidence: source-derived.

Audio activates after user interaction. Circular sound control uses vertical lines with `1s` looping stagger delays around `.0/.2/.4/.6/.8`; hover rotates border by 180 degrees.

Implementation: default off/muted. Provide visible toggle and ambient-state animation even if no real audio file is present.

## NM-012 Liquid Glass Cursor

Source confidence: source-derived.

Desktop cursor follower has an inner/outer circular glass motif, a rotating ring, and short hover text. It is hidden on tablet/mobile.

Implementation: fixed pointer follower with lerped transform; disable at `max-width: 1024px`.

## NM-013 Footer Contact Reveal

Source confidence: source-derived.

Near the bottom, contact/footer elements reveal from `y: 15`, opacity `0`, and `filter: blur(8px)` with stagger `.2`.

Implementation: ScrollTrigger timeline with scrub near the final section.

## NM-014 Mobile Glass Menu

Source confidence: source-derived.

Mobile nav becomes a rounded glass menu with masked gradient border and backdrop blur.

Implementation: compact fixed button, full menu overlay if needed, same color roles as desktop.

## NM-015 Sparse Center Text Reveal

Source confidence: observed.

Short phrases appear in central space with subtle y/opacity/blur motion. This is a content rhythm module, not just an animation.

Implementation: keep copy concise; avoid dense cards.

## NM-016 Light-to-Dark Mood Inversion

Source confidence: observed + source-derived.

The narrative shifts from pale glass/fog to dark fire/high contrast near the end.

Implementation: interpolate CSS variables, fog color, light intensity, object emissive color, and CTA contrast.

## NM-017 Particle/Sprite Trail

Source confidence: source-derived.

Small sprites, feathers, trails, and particles reinforce object motion and scene transitions.

Implementation: use R3F points/instancing or CSS particles. Pull colors from the reference object highlight palette.

## NM-018 Crystal/Object Fragment Anchors

Source confidence: source-derived.

Noomo uses multiple crystal models as project anchors. Generated sites should fragment the user object into theme-specific shards, petals, labels, droplets, leaves, sparks, or tiles.

Implementation: build about seven fragment groups that enter, rotate, and respond to hover.

## NM-019 Ambient Scene Layers

Source confidence: source-derived.

Background layers such as waves, mountains, noise, ice, floor, and sun create depth.

Implementation: use fixed CSS layers, Three planes, gradients, and noise textures with slower parallax than foreground.

## NM-020 Animation State Switching

Source confidence: source-derived.

The original bird switches among idle, pulse, close-up, and glide-like clips. Generated sites must change object state across sections.

Implementation: use animation mixer if assets support it; otherwise use camera, deformation, shader intensity, particles, and fragment spread as state changes.

