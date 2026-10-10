#!/usr/bin/env node

import { existsSync } from "node:fs";
import {
  mkdir,
  readFile,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const CANVAS = {
  width: 1080,
  height: 1440,
  safeArea: {
    x: 96,
    y: 96,
    width: 888,
    height: 1248,
  },
};

const DEFAULT_OUT = "local-output/imagegen-cards";
const MODE_DOC = "mode-imagegen-text-card.md";
const TEMPLATE_FILE_NAME = "template.html";
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const PAGE_WEIGHT_LIMIT = 600;
const DEFAULT_ACCENT_COLOR = "#1D1D1F";
const requireFromCwd = createRequire(join(process.cwd(), "package.json"));

const STYLE_PRESETS = {
  "minimal-magazine": {
    nameZh: "极简杂志",
    prompt:
      "极简高端杂志封面背景，留白充足，柔和纸张质感，克制的几何层次，优雅、安静、现代。",
    overlay: {
      color: "rgba(255, 255, 255, 0.62)",
      blurPx: 1.2,
    },
  },
  "film-photo": {
    nameZh: "胶片摄影",
    prompt:
      "胶片摄影质感背景，自然光、细腻颗粒、柔和景深、温暖真实的生活氛围，画面中心干净。",
    overlay: {
      color: "rgba(255, 255, 255, 0.58)",
      blurPx: 1.4,
    },
  },
  "cyber-glass": {
    nameZh: "赛博玻璃",
    prompt:
      "赛博朋克玻璃拟态背景，霓虹反射、透明材质、深色空间、边缘有光效，中心区域保持低对比。",
    overlay: {
      color: "rgba(7, 12, 22, 0.42)",
      blurPx: 1.6,
      textColor: "#f8fafc",
    },
  },
  "soft-illustration": {
    nameZh: "柔和插画",
    prompt:
      "柔和插画风背景，轻盈色块、手绘纹理、浅景深、亲切但不幼稚，中心留出安静阅读空间。",
    overlay: {
      color: "rgba(255, 255, 255, 0.6)",
      blurPx: 1.2,
    },
  },
  "ink-wash": {
    nameZh: "国风水墨",
    prompt:
      "现代国风水墨背景，宣纸肌理、淡墨层次、留白、克制的东方构图，中心区域干净淡雅。",
    overlay: {
      color: "rgba(255, 255, 255, 0.54)",
      blurPx: 1,
    },
  },
  "trend-poster": {
    nameZh: "潮流海报",
    prompt:
      "潮流海报背景，强烈视觉节奏、渐变光影、抽象图形、时尚编辑感，文字区域低干扰。",
    overlay: {
      color: "rgba(255, 255, 255, 0.64)",
      blurPx: 1.8,
    },
  },
};

const REQUIRED_BACKGROUND_CONSTRAINTS = [
  "不要生成任何文字、字母、数字、logo、水印、签名或 UI 文案。",
  "背景必须适合叠加中文标题、正文、引用和页码。",
  "中心文字区域保持低细节、低对比、无强边缘、无复杂主体遮挡。",
  "视觉重点可以放在四周边缘，允许边缘区域出现风格化纹理、光影、抽象装饰和空间层次。",
  "竖版海报背景，比例 3:4，适配 1080x1440。",
  "只生成背景图，不要模拟卡片文字排版。",
].join("\n");

const SENTENCE_SPLIT_PATTERN = /(?<=[。！？!?；;])\s*/u;

const usage = () => `
Usage:
  node generate-imagegen-cards.mjs prepare --input ./article.md --style "赛博朋克玻璃质感" --out local-output/imagegen-cards
  node generate-imagegen-cards.mjs prepare --input ./article.md --preset minimal-magazine --out local-output/imagegen-cards
  node generate-imagegen-cards.mjs compose --out local-output/imagegen-cards

Commands:
  prepare   生成纯文字 HTML、imagegen prompt 和 manifest
  compose   读取 backgrounds/page-XX.png，合成 exports/page-XX.png

Options:
  --input <file>       prepare 必填
  --out <dir>          输出目录，默认 ${DEFAULT_OUT}
  --style <prompt>     用户自定义 imagegen 风格提示词
  --preset <name>      内置风格：${Object.keys(STYLE_PRESETS).join(", ")}
  --template <file>    poster_template.html 路径，默认自动查找
  --clean              prepare 前清空输出目录
`;

const parseArgs = (argv) => {
  const [command, ...rest] = argv;
  const options = { command };

  for (let index = 0; index < rest.length; index += 1) {
    const token = rest[index];
    if (!token.startsWith("--")) {
      throw new Error(`未知参数：${token}`);
    }

    const key = token.slice(2);
    if (key === "clean") {
      options.clean = true;
      continue;
    }

    const value = rest[index + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`参数 --${key} 缺少值`);
    }

    options[key] = value;
    index += 1;
  }

  return options;
};

const escapeHtml = (value) =>
  value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

const inlineMarkdown = (value) =>
  escapeHtml(value).replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

const stripMarkdown = (value) =>
  value
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/^>\s?/gm, "")
    .replace(/[*_`>#-]/g, "")
    .replace(/\s+/g, " ")
    .trim();

const countText = (value) => Array.from(stripMarkdown(value)).length;

const templateCandidates = (templateOption) =>
  [
    templateOption ? resolve(templateOption) : null,
    join(process.cwd(), "poster_template.html"),
    join(SCRIPT_DIR, "poster_template.html"),
    join(SCRIPT_DIR, "..", "references", "poster_template.html"),
  ].filter(Boolean);

const findTemplateFile = (templateOption) => {
  const candidates = templateCandidates(templateOption);
  const templateFile = candidates.find((candidate) => existsSync(candidate));
  if (!templateFile) {
    throw new Error(
      `找不到 poster_template.html。请传入 --template <file>，已尝试：\n${candidates.join("\n")}`,
    );
  }

  return templateFile;
};

const normalizeTemplate = (template) =>
  template.replaceAll("background: var(--bg);", "background: transparent;");

const replaceTemplateVariables = (
  template,
  { bodyHtml, pageInfo, headerBlock, titleBlock, bgColor = "transparent", accentColor = DEFAULT_ACCENT_COLOR },
) =>
  template
    .replaceAll("{{BG_COLOR}}", bgColor)
    .replaceAll("{{ACCENT_COLOR}}", accentColor)
    .replaceAll("{{HEADER_BLOCK}}", headerBlock)
    .replaceAll("{{TITLE_BLOCK}}", titleBlock)
    .replaceAll("{{BODY_HTML}}", bodyHtml)
    .replaceAll("{{PAGE_INFO}}", pageInfo);

const renderHeaderBlock = (runningTitle) =>
  runningTitle
    ? `<div class="header"><span class="running-title">${escapeHtml(runningTitle)}</span></div>`
    : "";

const renderTitleBlock = (title) =>
  title ? `<div class="title-area"><h1>${inlineMarkdown(title)}</h1></div>` : "";

const isShortStandaloneTitle = (block, index) => {
  const text = stripMarkdown(block);
  return index === 0 && text.length > 0 && text.length <= 22 && !/[。！？!?；;，,：:]/u.test(text);
};

const isHighlight = (block) => {
  const text = stripMarkdown(block);
  return (
    text.length > 0 &&
    text.length < 25 &&
    !block.includes("\n") &&
    !/[。！？!?；;]$/u.test(text)
  );
};

const splitLongParagraph = (text) => {
  if (countText(text) <= 260) {
    return [text];
  }

  const sentences = text.split(SENTENCE_SPLIT_PATTERN).filter(Boolean);
  if (sentences.length <= 1) {
    return [text];
  }

  const chunks = [];
  let current = "";
  for (const sentence of sentences) {
    const next = `${current}${sentence}`;
    if (countText(next) > 180 && current) {
      chunks.push(current.trim());
      current = sentence;
    } else {
      current = next;
    }
  }

  if (current.trim()) {
    chunks.push(current.trim());
  }

  return chunks;
};

const parseBlocks = (markdown) => {
  const normalized = markdown.replace(/\r\n/g, "\n").trim();
  if (!normalized) {
    throw new Error("输入文档为空。");
  }

  const rawBlocks = normalized.split(/\n{2,}/);
  const elements = [];
  let documentTitle = "";

  rawBlocks.forEach((rawBlock, blockIndex) => {
    const block = rawBlock.trim();
    if (!block) {
      return;
    }

    if (block.startsWith("```")) {
      const code = block.replace(/^```[^\n]*\n?/, "").replace(/\n?```$/, "");
      elements.push({ type: "code", text: code });
      return;
    }

    const headingMatch = block.match(/^(#{1,3})\s+(.+)$/u);
    if (headingMatch) {
      const level = headingMatch[1].length;
      const text = headingMatch[2].trim();
      if (level === 1 && !documentTitle) {
        documentTitle = stripMarkdown(text);
        elements.push({ type: "h1", text });
      } else {
        elements.push({ type: "h2", text });
      }
      return;
    }

    if (!documentTitle && isShortStandaloneTitle(block, blockIndex)) {
      documentTitle = stripMarkdown(block);
      elements.push({ type: "h1", text: block });
      return;
    }

    if (block.split("\n").every((line) => line.trim().startsWith(">"))) {
      const text = block
        .split("\n")
        .map((line) => line.replace(/^>\s?/, ""))
        .join("\n")
        .trim();
      elements.push({ type: "quote", text });
      return;
    }

    if (block.split("\n").every((line) => /^\s*[-*+]\s+/.test(line))) {
      const items = block
        .split("\n")
        .map((line) => line.replace(/^\s*[-*+]\s+/, "").trim())
        .filter(Boolean);
      elements.push({ type: "list", items });
      return;
    }

    const itemMatch = block.match(/^([^：:]{2,18})[：:]\s*(.+)$/su);
    if (itemMatch && !block.includes("\n")) {
      elements.push({
        type: "item",
        label: itemMatch[1].trim(),
        text: itemMatch[2].trim(),
      });
      return;
    }

    for (const paragraph of splitLongParagraph(block)) {
      elements.push({
        type: isHighlight(paragraph) ? "highlight" : "paragraph",
        text: paragraph,
      });
    }
  });

  if (!documentTitle) {
    const firstText = elements.find((element) => element.text)?.text ?? "未命名卡片";
    documentTitle = stripMarkdown(firstText).slice(0, 24) || "未命名卡片";
  }

  return { documentTitle, elements };
};

const elementWeight = (element, isContinuation = false) => {
  const runningTitleWeight = isContinuation ? 70 : 0;
  if (element.type === "h1" || element.type === "h2") {
    return runningTitleWeight + countText(element.text) * 6;
  }
  if (element.type === "highlight") {
    return runningTitleWeight + countText(element.text) * 3;
  }
  if (element.type === "quote") {
    return runningTitleWeight + countText(element.text) * 1.7;
  }
  if (element.type === "list") {
    return (
      runningTitleWeight +
      element.items.reduce((total, item) => total + countText(item) * 1.8, 0)
    );
  }
  if (element.type === "item") {
    return runningTitleWeight + (countText(element.label) + countText(element.text)) * 1.8;
  }
  if (element.type === "code") {
    return runningTitleWeight + countText(element.text) * 2.2;
  }
  return runningTitleWeight + countText(element.text) * 1.4;
};

const isHeading = (element) => element.type === "h1" || element.type === "h2";

const paginate = (elements) => {
  const pages = [];
  let current = [];
  let currentWeight = 0;

  for (const element of elements) {
    const continuation = pages.length > 0 && current.length === 0;
    const weight = elementWeight(element, continuation);
    const wouldOverflow =
      current.length > 0 && currentWeight + weight > PAGE_WEIGHT_LIMIT;
    const canSplitBefore =
      !isHeading(element) && !(current.length === 1 && isHeading(current[0]));

    if (wouldOverflow && canSplitBefore) {
      pages.push(current);
      current = [element];
      currentWeight = elementWeight(element, true);
    } else {
      current.push(element);
      currentWeight += weight;
    }
  }

  if (current.length > 0) {
    pages.push(current);
  }

  return pages.length > 0 ? pages : [elements];
};

const elementToHtml = (element) => {
  if (element.type === "h2") {
    return `<div class="divider"></div>\n<h2>${inlineMarkdown(element.text)}</h2>`;
  }
  if (element.type === "highlight") {
    return `<p class="highlight">${inlineMarkdown(element.text)}</p>`;
  }
  if (element.type === "quote") {
    return `<blockquote><p>${inlineMarkdown(element.text)}</p></blockquote>`;
  }
  if (element.type === "list") {
    const items = element.items
      .map((item) => `<li>${inlineMarkdown(item)}</li>`)
      .join("\n");
    return `<ul>\n${items}\n</ul>`;
  }
  if (element.type === "item") {
    return `<div class="item"><p class="label">${inlineMarkdown(
      element.label,
    )}</p><p>${inlineMarkdown(element.text)}</p></div>`;
  }
  if (element.type === "code") {
    return `<pre><code>${escapeHtml(element.text)}</code></pre>`;
  }
  return `<p>${inlineMarkdown(element.text)}</p>`;
};

const summarizeElements = (elements) => {
  const text = stripMarkdown(
    elements
      .map((element) => {
        if (element.items) return element.items.join(" ");
        if (element.label) return `${element.label} ${element.text}`;
        return element.text ?? "";
      })
      .join(" "),
  );
  return text.slice(0, 80) || "中文知识卡片背景";
};

const createPrompt = ({ preset, style, documentTitle, pageSummary, pageNumber, totalPages }) => {
  const presetPrompt = preset ? STYLE_PRESETS[preset]?.prompt : "";
  const stylePrompt = [presetPrompt, style].filter(Boolean).join("\n");
  const finalStyle = stylePrompt || STYLE_PRESETS["minimal-magazine"].prompt;

  return [
    "Use case: stylized-concept",
    "Asset type: vertical background image for a Chinese text card",
    `Primary style request:\n${finalStyle}`,
    `Series title: ${documentTitle}`,
    `Current card theme (${pageNumber}/${totalPages}): ${pageSummary}`,
    "Composition: leave the central reading area quiet and low-detail; keep stronger visual interest near the edges and corners.",
    "Negative constraints:",
    REQUIRED_BACKGROUND_CONSTRAINTS,
  ].join("\n\n");
};

const getOverlay = (preset) => ({
  color: "rgba(255, 255, 255, 0.6)",
  blurPx: 1.2,
  textColor: "#101828",
  ...(preset ? STYLE_PRESETS[preset]?.overlay : {}),
});

const renderTextCardHtml = ({ template, bodyHtml, pageInfo, runningTitle, title }) =>
  replaceTemplateVariables(template, {
    bodyHtml,
    pageInfo,
    headerBlock: renderHeaderBlock(runningTitle),
    titleBlock: renderTitleBlock(title),
  });

const renderCompositeHtml = ({ template, pageData, backgroundUrl, overlay }) => {
  const textHtml = renderTextCardHtml({
    template,
    bodyHtml: pageData.bodyHtml,
    pageInfo: pageData.pageInfo,
    runningTitle: pageData.runningTitle,
    title: pageData.titleText,
  });
  const compositeStyle = `
<style>
  html,
  body {
    background: #fff !important;
  }

  .background-layer,
  .readability-layer {
    position: fixed;
    inset: 0;
    width: ${CANVAS.width}px;
    height: ${CANVAS.height}px;
  }

  .background-layer {
    object-fit: cover;
    z-index: 0;
  }

  .readability-layer {
    background: ${overlay.color ?? "rgba(255, 255, 255, 0.6)"};
    backdrop-filter: blur(${overlay.blurPx ?? 1.2}px);
    z-index: 1;
  }

  .card {
    position: relative;
    z-index: 2;
    background: transparent !important;
  }
</style>`;

  return textHtml
    .replace("</head>", `${compositeStyle}\n</head>`)
    .replace("<body>", `<body>\n  <img class="background-layer" src="${backgroundUrl}" alt="" />\n  <div class="readability-layer"></div>`);
};

const pageFileName = (index, ext) => `page-${String(index).padStart(2, "0")}.${ext}`;

const ensureDir = async (dir) => mkdir(dir, { recursive: true });

const writeJson = async (file, data) =>
  writeFile(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");

const backgroundToDataUrl = async (file) => {
  const buffer = await readFile(file);
  const lowerFile = file.toLowerCase();
  const mime = lowerFile.endsWith(".webp")
    ? "image/webp"
    : lowerFile.endsWith(".jpg") || lowerFile.endsWith(".jpeg")
      ? "image/jpeg"
      : "image/png";

  return `data:${mime};base64,${buffer.toString("base64")}`;
};

const loadChromium = async () => {
  const errors = [];
  for (const packageName of ["@playwright/test", "playwright"]) {
    try {
      return (await import(packageName)).chromium;
    } catch (error) {
      errors.push(`${packageName}: ${error.message}`);
    }

    try {
      return requireFromCwd(packageName).chromium;
    } catch (error) {
      errors.push(`${packageName} from cwd: ${error.message}`);
    }
  }

  throw new Error(
    `找不到 Playwright。请在当前工作区安装 @playwright/test 或 playwright。\n${errors.join("\n")}`,
  );
};

const prepare = async (options) => {
  if (!options.input) {
    throw new Error("prepare 需要 --input <file>");
  }

  const inputFile = resolve(options.input);
  const outDir = resolve(options.out ?? DEFAULT_OUT);
  const preset = options.preset;

  if (preset && !STYLE_PRESETS[preset]) {
    throw new Error(
      `未知 preset：${preset}。可用 preset：${Object.keys(STYLE_PRESETS).join(", ")}`,
    );
  }

  if (options.clean) {
    await rm(outDir, { recursive: true, force: true });
  }

  const markdown = await readFile(inputFile, "utf8");
  const { documentTitle, elements } = parseBlocks(markdown);
  const pagedElements = paginate(elements);
  const overlay = getOverlay(preset);
  const templateSourceFile = findTemplateFile(options.template);
  const template = normalizeTemplate(await readFile(templateSourceFile, "utf8"));

  await ensureDir(join(outDir, "pages"));
  await ensureDir(join(outDir, "prompts"));
  await ensureDir(join(outDir, "backgrounds"));
  await ensureDir(join(outDir, "exports"));
  await writeFile(join(outDir, TEMPLATE_FILE_NAME), template, "utf8");

  const pages = [];

  for (let index = 0; index < pagedElements.length; index += 1) {
    const pageNumber = index + 1;
    const totalPages = pagedElements.length;
    const pageElements = pagedElements[index];
    const titleElement = index === 0
      ? pageElements.find((element) => element.type === "h1")
      : null;
    const bodyElements = pageElements.filter((element) => element !== titleElement);
    const bodyHtml = bodyElements.map(elementToHtml).join("\n");
    const pageInfo = totalPages > 1 ? `${pageNumber} / ${totalPages}` : "";
    const runningTitle = index > 0 ? documentTitle : "";
    const titleText = titleElement?.text ?? "";
    const htmlFile = `pages/${pageFileName(pageNumber, "html")}`;
    const promptFile = `prompts/${pageFileName(pageNumber, "txt")}`;
    const backgroundFile = `backgrounds/${pageFileName(pageNumber, "png")}`;
    const pageSummary = summarizeElements(pageElements);
    const prompt = createPrompt({
      preset,
      style: options.style,
      documentTitle,
      pageSummary,
      pageNumber,
      totalPages,
    });

    await writeFile(
      join(outDir, htmlFile),
      renderTextCardHtml({
        template,
        bodyHtml,
        pageInfo,
        runningTitle,
        title: titleText,
      }),
      "utf8",
    );
    await writeFile(join(outDir, promptFile), `${prompt}\n`, "utf8");

    pages.push({
      index: pageNumber,
      title: documentTitle,
      summary: pageSummary,
      htmlFile,
      promptFile,
      backgroundFile,
      exportFile: null,
      bodyHtml,
      pageInfo,
      runningTitle,
      titleText,
      overlay,
    });
  }

  const manifest = {
    version: 1,
    generator: "generate-imagegen-cards.mjs",
    modeDocument: MODE_DOC,
    templateFile: TEMPLATE_FILE_NAME,
    templateSource: templateSourceFile,
    sourceInput: relative(process.cwd(), inputFile),
    createdAt: new Date().toISOString(),
    canvas: CANVAS,
    style: {
      preset: preset ?? null,
      presetNameZh: preset ? STYLE_PRESETS[preset].nameZh : null,
      userPrompt: options.style ?? null,
    },
    backgroundGeneration: {
      provider: "codex-built-in-imagegen",
      note:
        "脚本不调用 OpenAI API。请用 Codex 内置 imagegen 根据 prompts/page-*.txt 生成背景，并保存到 backgrounds/page-*.png。",
      requiredConstraints: REQUIRED_BACKGROUND_CONSTRAINTS.split("\n"),
    },
    pages,
  };

  await writeJson(join(outDir, "manifest.json"), manifest);

  console.log(`Prepared ${pages.length} card page(s) at ${relative(process.cwd(), outDir)}`);
  console.log("Next: use Codex built-in imagegen with prompts/page-*.txt, then run compose.");
};

const loadManifest = async (outDir) => {
  const manifestFile = join(outDir, "manifest.json");
  if (!existsSync(manifestFile)) {
    throw new Error(`找不到 manifest：${manifestFile}。请先运行 prepare。`);
  }

  return JSON.parse(await readFile(manifestFile, "utf8"));
};

const assertBackgroundsExist = async (outDir, manifest) => {
  const missing = [];
  for (const page of manifest.pages) {
    const backgroundFile = join(outDir, page.backgroundFile);
    if (!existsSync(backgroundFile)) {
      missing.push(page.backgroundFile);
      continue;
    }
    const info = await stat(backgroundFile);
    if (!info.isFile() || info.size === 0) {
      missing.push(page.backgroundFile);
    }
  }

  if (missing.length > 0) {
    throw new Error(`缺少背景图，请先用内置 imagegen 生成并保存：\n${missing.join("\n")}`);
  }
};

const compose = async (options) => {
  const outDir = resolve(options.out ?? DEFAULT_OUT);
  const manifest = await loadManifest(outDir);
  await assertBackgroundsExist(outDir, manifest);
  await ensureDir(join(outDir, "exports"));
  const template = await readFile(join(outDir, manifest.templateFile ?? TEMPLATE_FILE_NAME), "utf8");

  const chromium = await loadChromium();
  const browser = await chromium.launch();

  try {
    for (const pageData of manifest.pages) {
      const page = await browser.newPage({
        viewport: { width: CANVAS.width, height: CANVAS.height },
        deviceScaleFactor: 1,
      });
      const backgroundPath = resolve(outDir, pageData.backgroundFile);
      const backgroundUrl = await backgroundToDataUrl(backgroundPath);
      const html = renderCompositeHtml({
        template,
        pageData,
        backgroundUrl,
        overlay: pageData.overlay ?? getOverlay(manifest.style?.preset),
      });
      await page.setContent(html, { waitUntil: "networkidle" });
      await page.screenshot({
        path: join(outDir, pageData.exportFile ?? `exports/${pageFileName(pageData.index, "png")}`),
        type: "png",
        clip: {
          x: 0,
          y: 0,
          width: CANVAS.width,
          height: CANVAS.height,
        },
      });
      await page.close();
      pageData.exportFile = `exports/${pageFileName(pageData.index, "png")}`;
    }
  } finally {
    await browser.close();
  }

  manifest.composedAt = new Date().toISOString();
  await writeJson(join(outDir, "manifest.json"), manifest);
  console.log(`Composed ${manifest.pages.length} PNG file(s) at ${relative(process.cwd(), join(outDir, "exports"))}`);
};

const main = async () => {
  const options = parseArgs(process.argv.slice(2));
  if (!options.command || options.command === "--help" || options.command === "help") {
    console.log(usage().trim());
    return;
  }

  if (options.command === "prepare") {
    await prepare(options);
    return;
  }

  if (options.command === "compose") {
    await compose(options);
    return;
  }

  throw new Error(`未知命令：${options.command}\n${usage()}`);
};

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
