# Momo Transparent Imagegen

`momo-transparent-imagegen` 是一个 Codex skill，用于根据自然语言提示词生成透明底 PNG/WebP 图片。

适合这类请求：

- 生成一张苹果图标，透明底。
- 画一个游戏金币 png，无背景。
- 根据这张参考图生成透明底贴纸。
- Generate a game coin PNG, no background.
- Create a sticker with transparent background.

English documentation: [README.md](README.md)。

## 它能做什么

- 识别中文和英文透明底请求。
- 自动加强提示词，让图更适合去底。
- 自动选择 chroma-key 颜色：
  - 默认 `#00FF00`
  - 如果主体颜色接近默认绿色 key，改用 `#FF00FF`
- 在 prompt 中强制要求：
  - 纯色背景
  - 无阴影
  - 无渐变
  - 无反射
  - 无地面 / 桌面
  - 边缘清晰
  - 主体留足边距
  - 主体不要使用 key color
- 使用系统脚本去底：

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py"
```

- 提供 `scripts/inspect_alpha.py` 做透明 PNG 检查。

## 安装

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/marvellouspizza/momo-transparent-imagegen.git ~/.codex/skills/momo-transparent-imagegen
```

显式调用：

```text
Use $momo-transparent-imagegen：生成一张游戏金币 png，无背景，透明底。
```

自然语言触发示例：

- 生成一张苹果图标，透明底。
- 画一个游戏金币 png，无背景。
- 生成一个游戏道具图标，透明背景。
- 参考这张图生成一个透明底贴纸。
- 生成一个 UI 图标 alpha PNG。

## 透明底工作流

这个 skill 会先用内置 imagegen 生成干净的纯色 chroma-key 源图，再本地去底并检查 alpha：

```text
内置 imagegen -> 纯色 chroma-key 源图 -> remove_chroma_key.py 去底 -> 透明 PNG
```

如果遇到毛发、玻璃、烟雾、柔光、半透明材质等复杂边缘，skill 应该先解释风险，再决定是否使用 fallback 工作流。

## 适合生成

- 游戏图标
- UI 图标
- 道具图
- 商品抠图
- 贴纸
- logo / 标志
- 简单游戏 sprite
- 拾取物 / 金币 / 宝石 / 材料图

## 高风险对象

- 复杂头发、毛发、羽毛
- 烟雾、雾气、灰尘、火焰、柔光
- 玻璃、液体、半透明布料
- 真实反光物体
- 软阴影
- 主体颜色和 key color 冲突的图片

## Alpha 检查

检查透明 PNG：

```bash
python3 scripts/inspect_alpha.py output.png
```

输出 JSON：

```bash
python3 scripts/inspect_alpha.py output.png --json
```
