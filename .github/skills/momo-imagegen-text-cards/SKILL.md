---
name: momo-imagegen-text-cards
description: Generate finished Chinese image card series from text, Markdown files, article notes, URL summaries, or paper summaries. Use when the user asks to turn text into cards, finished cards, imagegen cards, text-over-background cards, 小红书/微信图文卡片, or wants real HTML text composited over AI-generated backgrounds.
---

# Momo Imagegen Text Cards

Create finished vertical PNG card series by combining real HTML text with Codex built-in imagegen backgrounds.

## Core Rule

Do not use OpenAI API keys or external image APIs. Use the built-in `image_gen` tool for backgrounds. The bundled Node script only prepares text cards, prompts, and final composition.

## Workflow

1. Create a summarized card draft before running the script.
   - If the user provides inline long text, do not pass the raw text directly to the script.
   - First rewrite it into a concise Markdown card draft with 4-6 cards by default, unless the user asks for another count.
   - Each card should contain one clear heading plus 1-3 short paragraphs or labeled points.
   - Preserve the original argument, key examples, concrete numbers, and final takeaway; remove repetition and article-like connective tissue.
   - If the user provides a file or URL, first obtain clean Markdown, then summarize it into this same card draft shape.
   - Write the summarized draft to a source file outside the output directory, such as `<workspace>/local-output/imagegen-text-cards-sources/<slug>.md`, so `--clean` cannot delete it.
2. Run prepare:
   ```bash
   node ~/.codex/skills/momo-imagegen-text-cards/scripts/generate-imagegen-cards.mjs prepare \
     --input <summarized-source.md> \
     --preset minimal-magazine \
     --style "<user style prompt if provided>" \
     --out <output-dir> \
     --clean
   ```
3. For each `prompts/page-XX.txt`, call built-in `image_gen` once using that prompt.
4. Copy each generated image from `$CODEX_HOME/generated_images/...` into `<output-dir>/backgrounds/page-XX.png`. Leave the original generated image in place.
5. Run compose:
   ```bash
   node ~/.codex/skills/momo-imagegen-text-cards/scripts/generate-imagegen-cards.mjs compose --out <output-dir>
   ```
6. Show the final PNGs from `<output-dir>/exports/page-XX.png` using Markdown image tags, and report the output directory.

## Output Directory

Prefer `<workspace>/local-output/imagegen-text-cards/<short-slug>` when the user does not specify a destination. The prepare command can also generate a timestamped default if `--out` is omitted, but for full automation pass an explicit `--out` so compose can reuse it.

## Style Presets

Use `--preset minimal-magazine` by default. Other built-in presets:

- `film-photo`
- `cyber-glass`
- `soft-illustration`
- `ink-wash`
- `trend-poster`

Use `--style` to append user-specific style instructions. The script always adds constraints that forbid text, letters, logos, watermarks, and busy center detail in generated backgrounds.

## Text Card Rules

The text-to-card logic follows `references/mode-imagegen-text-card.md`, adapted from the user's rainbow-card prompt:

- Real HTML text only; never bake generated Chinese text into the background image.
- 1080x1440 card canvas.
- Long input must be summarized before prepare; the local script formats card drafts but does not call an LLM by itself.
- Render HTML through `poster_template.html`; do not recreate the template CSS in the script.
- Reuse rainbow-mode content rules for headings, quotes, bold text, highlights, item groups, dividers, visual weights, greedy pagination, and page numbers.
- Keep rainbow-mode HTML semantics: `<h1>`, `<h2>`, `.highlight`, `.item`, `.label`, `.subtitle`, and `.divider`.
- Do not add custom title rewriting, title subtitles, semantic title line splitting, `title-divider`, `section-divider`, or `point-label`.

## Verification

Before claiming success:

- Confirm `manifest.json` lists every page.
- Confirm every `backgrounds/page-XX.png` exists.
- Run compose successfully.
- Confirm every `exports/page-XX.png` is a `1080 x 1440` PNG.
- Visually inspect at least the first export and make sure the AI background is visible behind real text.
