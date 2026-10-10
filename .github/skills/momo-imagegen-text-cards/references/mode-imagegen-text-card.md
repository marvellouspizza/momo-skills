# 模具：Imagegen 多卡（基于彩虹多卡）

## 步骤 1：读取模板

读取 `poster_template.html`。脚本使用模板中的变量系统渲染卡片，不再手写另一套 HTML/CSS。

默认查找顺序：

- 命令行传入的 `--template <file>`
- 当前工作目录的 `poster_template.html`
- 脚本目录的 `poster_template.html`
- skill 的 `references/poster_template.html`

## 步骤 1.5：配色

不使用彩虹模具固定白底作为最终背景：

- 模板仍保留 `{{BG_COLOR}}` 和 `{{ACCENT_COLOR}}` 变量
- `{{BG_COLOR}}` 渲染为 `transparent`
- `{{ACCENT_COLOR}}` 渲染为默认强调色
- 背景、风格、质感和氛围图交给 Codex 内置 imagegen 生成
- HTML 文字层使用模板原有 `.card`、`.title-area`、`.content`、`.footer` 等结构

## 步骤 2：内容预处理

- 识别标题行（`#`/`##`/`###` 开头，或独立短行）
- 识别引用块（`>` 开头）
- 识别加粗（`**text**`）
- **识别金句**：独立成段的短句（通常 < 25 字），承载核心洞察，用 `.highlight` 渲染
- 按空行分割为段落列表

## 步骤 3：计算视觉重量

模板在 1080x1440 全分辨率渲染，正文 36px，行高 1.7。

- 普通段落：字符数 × 1.4
- 标题行（h1 首卡 84px）：字符数 × 6.0
- 金句（`.highlight` 40px + 左边框 + 上下留白）：字符数 × 3.0
- `.item` 条目组（label + 正文）：字符数 × 1.8
- 引用块：字符数 × 1.7
- 分割线（divider）：固定 60 权重
- 代码块：字符数 × 2.2
- Running title（续页头部）：固定 70 权重

## 步骤 4：贪心切分

- 阈值：每卡约 **600** 字符等价视觉重量
- 逐段累加，超过阈值时在当前段之前切分
- **切分规则**：
  - 绝不在句子中间切
  - 优先在段落/条目/章节边界切
  - 标题不落单（必须跟至少一个内容元素在同一卡）
  - 超长单段在句号处强制切
  - 一个章节（h2 + 3 items）通常刚好一卡

**特殊情况**：
- 只有一张卡：不显示页码
- 多张卡：显示 `1 / N` 格式页码

## 步骤 5：格式化为 HTML

**基础元素：**
- 普通段落 → `<p>文本</p>`
- 章节标题（##/### 级别） → `<h2>标题</h2>`
- 引用 → `<blockquote><p>引用</p></blockquote>`
- 加粗 → `<strong>文本</strong>`
- 列表 → `<ul><li>...</li></ul>`

**金句（独立成段的核心洞察短句，视觉突出）：**
```html
<p class="highlight">金句文本</p>
```
判断标准：独立成段、< 25 字、承载关键洞察。用 `.highlight` 而非 `<p><strong>`。

**条目组（有标题+正文的并列条目）：**
```html
<div class="item">
  <p class="label">条目标题</p>
  <p>条目正文</p>
</div>
```

**副标题标签：**
```html
<p class="subtitle">标签文字</p>
```

**分割线（章节之间）：**
```html
<div class="divider"></div>
```

## 步骤 6：渲染与合成

对每张卡片，用 `poster_template.html` 替换模板变量，并输出 imagegen 背景 prompt：

| 项目 | 规则 |
|------|------|
| `{{BG_COLOR}}` | `transparent` |
| `{{ACCENT_COLOR}}` | 默认强调色 |
| 背景 | 使用 Codex 内置 imagegen 生成，compose 时叠在模板文字层下方 |
| `HEADER_BLOCK` | 续页卡：`<div class="header"><span class="running-title">文章标题</span></div>`；首卡或单卡：空字符串 |
| `TITLE_BLOCK` | 首卡有标题时：`<div class="title-area"><h1>标题</h1></div>`；续页卡或无标题时：空字符串 |
| `BODY_HTML` | 步骤 5 生成的 HTML |
| `PAGE_INFO` | 多卡时 `1 / 3`，单卡时空字符串 |
| 最终输出 | 底层 imagegen 背景 + 中层自动蒙层 + 顶层真实 HTML 文字，导出 PNG |
