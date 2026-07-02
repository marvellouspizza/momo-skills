# QA Reference

Use this for revisions and final checks.

## Required Checks

- The site has a loader/intro plus exactly 12 complete sections.
- Every section has assigned `NM-*` modules in `MOTION_BRIEF.md`.
- The central reference object is visible and materially important across the narrative.
- The central object is true 3D by default: GLB or procedural Three.js geometry. A flat image plane as the hero object fails QA unless the user explicitly approved a 2D/2.5D downgrade.
- Scroll feels continuous and choreographed, not a stack of independent fade-ins.
- The first viewport has a giant narrative title and object signal.
- Split text blur/scale appears in at least the opening and one later section.
- Fixed glass CTA exists and has hover/click burst behavior.
- Every fixed header/menu/CTA/in-page anchor is clicked in QA. Each direct navigation target must show that section's readable heading, body, or clear copy role in the resulting viewport; it must not land on a blank lead-in with only the 3D object/background visible.
- Sound/ambient control exists and is user-controlled.
- Desktop cursor exists and is disabled on tablet/mobile.
- The final section shifts to dark or high-contrast mood.
- Mobile retains the style with adapted framing.
- No Noomo runtime assets are referenced.
- Build succeeds and local preview opens.

## User-Guided Preview Review

Do not require screenshot-based acceptance. Start the local preview and ask the user to inspect:

- Section completeness.
- Scroll rhythm.
- Object motion and material feel.
- Text reveals.
- CTA, cursor, sound/ambient controls.
- Mobile layout if relevant.

Then revise while preserving the motion language and 12-section structure.
