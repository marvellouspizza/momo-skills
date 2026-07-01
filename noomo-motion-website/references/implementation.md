# Implementation Reference

## Project Shape

Create:

```text
generated/noomo-motion-{slug}/
  package.json
  index.html
  vite.config.js
  src/
    main.jsx
    App.jsx
    styles.css
    data/site.js
    components/
    motion/
  public/
    assets/generated/
  MOTION_BRIEF.md
```

Use `scripts/create_project.py` to create the base structure.

## Required Dependencies

Runtime: `react`, `react-dom`, `gsap`, `@gsap/react`, `lenis`, `three`, `@react-three/fiber`, `@react-three/drei`, `lucide-react`.

Dev: `vite`, `@vitejs/plugin-react`.

## Scroll Engine Pattern

Use one animation loop:

```js
gsap.ticker.add((time) => lenis.raf(time * 1000))
gsap.ticker.lagSmoothing(0)
```

Use CSS variables for global progress and section-local state:

```js
document.documentElement.style.setProperty('--motion-progress', progress)
document.documentElement.style.setProperty('--scene-dark', darkProgress)
```

## Direct Navigation Pattern

Noomo sections are often much taller than the viewport. Do not let fixed navigation links jump to the top of those long section shells if the readable copy is centered, delayed, pinned, or revealed later in the section. This creates blank "middle pages" with only the 3D scene visible.

Use a dedicated content target inside every navigable section:

```jsx
<section id={section.id} className="story-section">
  <div className="section-inner" data-section-content>
    <h2>{section.title}</h2>
    <p>{section.body}</p>
  </div>
</section>
```

Intercept header/menu clicks and scroll to the content target, not the section shell:

```js
function navigateToSection(targetId) {
  const section = document.getElementById(targetId)
  const content = section?.querySelector('[data-section-content]') || section
  if (!content) return

  const contentTop = content.getBoundingClientRect().top + window.scrollY
  const offset = Math.min(window.innerHeight * 0.28, 260)
  lenis.scrollTo(Math.max(0, contentTop - offset), {
    duration: 1.25,
    easing: (value) => 1 - Math.pow(1 - value, 3),
  })
  window.history.pushState(null, '', `#${targetId}`)
}
```

For the first section, scroll to top or a small intro offset. For final/contact links, target the final section's actual contact/heading block. The required QA is: click every fixed nav item and confirm the first viewport after navigation contains the destination heading or key copy.

## Object Scene Pattern

Use R3F for the central object. The default central object must be true 3D: imported GLB or procedural Three.js geometry. If no custom 3D model exists, build the object procedurally from meshes.

- High-fidelity route: generate or author a GLB with Blender, Spline, an AI 3D tool, or another 3D modeler. Load it with `useGLTF`, traverse named meshes, and apply runtime materials/animation.
- Procedural base forms: lathe geometry, extrusions, cones, cylinders, spheres, torus rims/handles, custom `BufferGeometry`, or instanced meshes.
- Material parts: transparent glass shell, liquid/inner volume, crystal/faceted motif, bubbles, fragments, particles, rim glints, and ambient scene layers.
- 6-12 3D fragment meshes around it.
- Points or instanced meshes for particles.
- MeshPhysicalMaterial or shader-like material for glass highlights.
- Fog and lights interpolated from scroll progress.

Imported GLB rendering rule: when a GLB is the primary object, add a local R3F environment reflection setup by default. Use `@react-three/drei` `Environment` with local `Lightformer` panels or equivalent in-scene reflection geometry; do not rely on remote HDRI presets. Glass, liquid, crystal, metal, and glossy PBR assets often look correct in a GLB viewer but dull, gray, or flat in the webpage without environment reflections. Preserve the imported GLB's PBR textures/materials when they are good; prefer non-destructive tuning such as roughness, clearcoat, emissive intensity, tone mapping exposure, and `envMapIntensity` instead of replacing every imported material.

Generated 2D images may be used as reference, texture, mask, color source, or background plate. Do not use a flat image plane as the primary hero object unless the user explicitly confirms a 2D/2.5D downgrade. Do not copy Noomo's phoenix model or textures.

## Blender GLB Pattern

When Blender is available and the object is high precision:

1. Create `scripts/create_{slug}_glb.py`.
2. Generate named meshes for each semantic part: shell, rim, liquid, main motif, fragments, bubbles, anchors.
3. Export `public/assets/generated/{slug}-high.glb`.
4. Load the GLB with `useGLTF('/assets/generated/{slug}-high.glb')`.
5. Traverse named meshes and tune materials non-destructively when the imported PBR material is usable. Replace with Three.js `MeshPhysicalMaterial` or custom shaders only for known semantic layers that need runtime control.
6. Bind object groups, fragments, bubbles, and material parameters to scroll progress.

Coordinate rule: model in Blender's native Z-up coordinate system. Do not build Blender geometry as if Y were vertical; Blender's glTF exporter converts Z-up to glTF/Three's Y-up. If Blender geometry is authored Y-up, the object can appear in Three as a top-down or sideways view. Verify exported GLB orientation in Three, not only in Blender.

For cups, bowls, liquids, plates, pools, or similar horizontal surfaces, verify in Three that the liquid surface has large X/Z bounds and very small Y thickness. If the liquid appears as a vertical sheet or top-down disk from the intended camera, fix the Blender axis model and re-export.

JSX-only primitive geometry is acceptable for fast draft previews, but it is not the high-fidelity default for the primary hero object.

## Text Motion Pattern

Split high-impact headings into chars. Animate opacity, blur, y, and scale with ScrollTrigger scrub. Keep ordinary body copy readable and do not over-split everything.

## Mobile Pattern

Use a separate mobile scene framing:

- Larger object in early sections.
- Shorter auto-start scroll target.
- Less hover dependency.
- Cursor hidden.
- Glass menu button instead of full nav if needed.

Mobile is same-style high fidelity, not a simplified static fallback.

## Asset Rules

Generated assets must live under `public/assets/generated/`. Acceptable derived assets include reference renders, masks, texture swatches, particle palettes, and poster/background textures. The primary object should remain real 3D; generated images should not replace the modeled object by default.

## Motion Brief

Write `MOTION_BRIEF.md` with:

- Theme summary.
- Reference object treatment.
- Color role mapping.
- 12 sections with section responsibility, copy, and module IDs.
- UI modules used.
- Mobile strategy.
- Local preview notes.
