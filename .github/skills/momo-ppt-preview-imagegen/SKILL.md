---
name: momo-ppt-preview-imagegen
description: Generate a single image that looks like a PPT template preview page from one or more reference images. Use when the user asks to apply the visual style of one screenshot/image to the layout/content of another screenshot/image, especially for "PPT template preview", "PPT preview poster", "template gallery", "preview sheet", "根据截图1风格生成截图2一样的预览页", or requests to use built-in image-2/image generation for slide-template preview images.
---

# Momo PPT Preview Imagegen

## Goal

Create a raster image of a PPT template preview page: a single poster/sheet showing multiple slide thumbnails in a coherent deck style. The output is an image, not a `.pptx` file, unless the user explicitly asks for an editable deck.

## Workflow

1. Identify reference roles:
   - Style reference: colors, illustration style, typography mood, borders, shadows, spacing, decorative elements.
   - Structure/content reference: preview-page composition, number of thumbnails, slide types, theme, information density.
   - If the user says "截图 1 的风格，截图 2 的样子", treat screenshot 1 as style and screenshot 2 as preview-gallery structure.

2. Inspect local image paths when needed:
   - If screenshots are attached in the conversation, use them as visual context.
   - If the user only provides local paths, inspect them with the available image-viewing tool before generating.

3. Clarify only when necessary:
   - Do not ask if the user already gave a style image and a structure image.
   - Make a reasonable theme choice from the references unless the requested subject is missing or contradictory.

4. Generate with the image generation tool:
   - Use the built-in image generation capability when the user says "image-2" or asks to generate an image.
   - Ask for one finished image, not intermediate sketches.
   - Prefer a vertical preview-poster aspect ratio such as 9:16 when matching phone-like gallery screenshots, or 16:9/4:3 only if the user asks for a landscape preview.

5. Keep the final response short:
   - After image generation, do not over-explain.
   - If a file path is needed, reference the generated artifact path only if available from the tool/session.

## Prompt Recipe

Build the generation prompt with these blocks:

1. Output type:
   - "Generate a single high-resolution raster image: a PPT template preview page / template gallery poster."

2. Style transfer:
   - Name the style reference explicitly.
   - Extract visible traits instead of saying only "same style".
   - Include: background, line quality, color palette, typography mood, card treatment, icons, decorative accents, spacing.

3. Preview-page structure:
   - Specify the grid: commonly `2 columns x 5 rows` for a catalog-like preview sheet.
   - Specify each thumbnail as a slide preview, not a pricing card or app screen.
   - Request slight thumbnail variation while preserving one deck identity.

4. Slide inventory:
   - Include likely deck pages: cover, agenda, overview, pricing/features, comparison, timeline, dashboard/data, workflow/process, testimonial/quote, closing/contact.
   - Adapt these to the user's topic.

5. Negative constraints:
   - Exclude phone UI, black app background, status bar, back button, "1/1" badge, watermarks, browser chrome, and unrelated screenshot artifacts.
   - Exclude real PPT editor UI unless the user asks for an editor mockup.

6. Text handling:
   - Major headings should be readable.
   - Small body text may be abstract placeholder lines.
   - Use the user's requested language when obvious; otherwise preserve language from the content reference.

See `references/prompt-patterns.md` for compact reusable prompt patterns.

## Quality Bar

- The image must read immediately as a PPT template preview sheet.
- The style reference should dominate the visual language; the content reference should dominate the composition.
- Thumbnail cards should look like slides from one coherent deck, not independent posters.
- Major titles and labels should not overlap borders or each other.
- If the structure reference is a phone screenshot, translate the gallery content out of the phone frame.
