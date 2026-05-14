# Generate Game Art Pack

`momo-generate-game-art-pack` 是一个 Codex skill，用于把用户上传的数张参考图转化为可审核、可扩展、可追踪的 2D 游戏 v1 美术资源生产流程。

它适合个人开发者或小团队，把“参考图 -> 风格定义 -> 小样审核 -> 扩展资源包 -> QC -> 入库规划”这套流程固定下来。

English documentation: [README.md](README.md)。

## 它能做什么

- 根据用户参考图生成“游戏美术风格定义草案”。
- 只把参考图作为风格灵感，避免复刻角色、姿势、服装、构图、logo 或其他独特元素。
- 先生成固定 6 张方向样张供用户审核：
  - 1 个主角 / 玩家方向样张
  - 1 个基础敌人 / 怪物方向样张
  - 1 个农场 / 家园 / 安全区方向样张
  - 1 个野外战斗 / 危险区域方向样张
  - 1 个 HUD 方向样张
  - 1 个背包 / 物品面板方向样张
- 用户确认画风后，再扩展完整 v1 美术候选包。
- 记录每张图的 prompt、用途、状态、审核结果、QC 风险和下一步。
- 支持 sprite、地图、道具、UI、图标、VFX、Godot import notes 等资源追踪。
- 明确区分 `Approved for Expansion` 和 `Approved for Game Asset`，避免方向样张误入正式资源。

## 资源包预设

skill 内置这些资源包预设：

- `minimal_playable_pack`：最小可玩闭环资源
- `topdown_rpg_pack`：俯视 RPG / 探索游戏资源
- `cozy_farming_pack`：农场 / 家园 / 采集 / 制作资源
- `combat_action_pack`：战斗动作资源
- `side_scroller_pack`：横版 / 平台跳跃 / side-view 资源
- `tactical_grid_pack`：战棋 / 网格 / 策略资源
- `monster_taming_pack`：怪物收集 / 养成资源
- `full_v1_pack`：较完整的 v1 初始资源包

详细分类见 [`references/art-pack-taxonomy.md`](references/art-pack-taxonomy.md)。

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── templates/
├── references/
│   ├── art-pack-taxonomy.md
│   ├── map-and-sprite-routing.md
│   ├── prompt-patterns.md
│   └── workflow-status-gates.md
└── scripts/
    ├── create_art_pack_docs.py
    └── qc_image_manifest.py
```

## 安装

把这个仓库 clone 到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/marvellouspizza/momo-generate-game-art-pack.git ~/.codex/skills/momo-generate-game-art-pack
```

之后在 Codex 中这样调用：

```text
Use $momo-generate-game-art-pack to turn my reference images into a reviewed v1 2D game art pack.
```

## 中文触发示例

正式 skill 调用名仍然是 `$momo-generate-game-art-pack`。为了让 Codex 更容易在中文请求中识别这个 skill，也可以使用下面这些自然语言说法：

- 参考这个图片生成游戏美术资源。
- 根据参考图生成游戏美术资源。
- 上传参考图生成 v1 游戏美术资源包。
- 用这些图片生成角色、场景、UI、图标、地图、怪物资源。
- 先分析这些参考图的美术风格，再生成 6 张方向审核样张。

## 推荐流程

1. 用户上传参考图。
2. skill 先输出“游戏美术风格定义草案”。
3. 用户确认风格方向。
4. 生成固定 6 张方向审核样张。
5. 用户通过后，样张只标记为 `Approved for Expansion`。
6. 根据用户选择的资源包预设继续扩展候选资源。
7. 对候选资源做 QC、切片清单、命名规则和 import notes。
8. 只有用户明确批准的候选或派生 runtime 输出，才能标记为 `Approved for Game Asset`。

## 附带脚本

生成一套资源追踪文档：

```bash
python3 scripts/create_art_pack_docs.py --out docs/art-pack --pack-name my-game-v1
```

检查 PNG 尺寸和 alpha 信息：

```bash
python3 scripts/qc_image_manifest.py path/to/images --md-out qc_manifest.md
```

`qc_image_manifest.py` 在安装 Pillow 时会读取更完整的信息；没有 Pillow 时，也会退回到 PNG header 检查基础尺寸和 alpha 类型。

## 状态门禁

生成出来的图默认不是正式游戏资源。

skill 使用这条状态流：

```text
Draft -> Generated -> Approved for Expansion -> Approved for Game Asset -> Godot Ready -> Imported -> Verified
```

这样可以清楚区分方向样张、候选 sheet、正式派生切片和已导入引擎的 runtime 资源。

## 注意

- 创意图片应来自内置 imagegen。
- 脚本只做确定性处理，例如模板生成、QC、manifest、切片辅助。
- 透明候选资源默认使用纯色 chroma-key 背景，然后本地去底和 QC。
- 对于可玩地图，base / foundation 层不应烘焙运行时可控物体，例如 props、actor、敌人、拾取物、UI、hazard 或碰撞关键对象。
