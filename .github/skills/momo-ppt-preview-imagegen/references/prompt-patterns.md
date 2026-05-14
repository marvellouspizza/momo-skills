# Prompt Patterns

## Two-Reference PPT Preview

Use this when the user gives a style reference and a structure/content reference.

```text
Generate a single high-resolution raster image: a PPT template preview page, like a marketplace preview sheet showing many slide thumbnails.

Use [STYLE_REFERENCE] as the PPT's visual style: [STYLE_TRAITS]. Use [STRUCTURE_REFERENCE] only for the idea of a template preview gallery: [STRUCTURE_TRAITS].

Create [COUNT] slide thumbnails in a [GRID] grid. Each thumbnail should look like one slide from the same presentation deck. Theme: [THEME]. Include these slide types: cover, agenda, overview, feature/pricing, comparison, timeline, data dashboard, workflow/process, testimonial/quote, closing/contact.

Add a top header: small label "[LABEL]", large title "[TITLE]", subtitle "[SUBTITLE]".

Major headings should be readable; small body text can be abstract placeholder lines. No phone status bar, no black app viewer background, no back button, no 1/1 badge, no watermarks, no PPT editor chrome.
Aspect ratio: [ASPECT_RATIO].
```

## Hand-Drawn SaaS Style Traits

Use when the style reference resembles a clean hand-drawn SaaS/PPT page:

```text
clean white background, playful hand-drawn UI aesthetic, thick slightly imperfect black outlines, lightly tilted cards, simple doodle icons, warm yellow star/sparkle accents, vivid blue accent text, friendly modern typography, minimal shadows, airy spacing
```

## Corporate Tech Preview Traits

Use when the structure/content reference resembles a blue corporate deck gallery:

```text
two-column grid of slide thumbnails, blue-and-white corporate technology deck, cover slide, about-us slide, timeline slide, data/stat slides, architecture/building imagery, soft blue gradients, dashboard-like number blocks, consistent logo area
```
