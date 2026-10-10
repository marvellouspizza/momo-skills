# 生成与修改提示

将模板中的参数换成当前用户已确认的信息。模板是设计起点，不是固定角色、固定款数或额外审批要求。不要把所有输入图都当作必须保留身份的编辑目标。

## 卡通原画样稿

```text
Create ONE original full-body chibi cartoon character for design approval.
Reference A provides [theme, identity cues, palette].
Reference B provides [big-head proportions, expressive eyes, clear outlines] only.
Create a distinct design; do not reproduce reference B's exact hairstyle, outfit or pose.
Key traits: [2-4 easily recognizable features].
Clean black cartoon linework, large expressive eyes, compact body, clear silhouette.
Simplified flat color areas suitable for a later [target bead count]-bead adaptation.
This is a cartoon concept, not yet a counted bead pattern.
Plain white background, full figure visible, no text, no mockup, exactly one character.
```

用户仅要求“勾线改成黑色”时，编辑已确认图：改轮廓及结构线，保留脸、姿态、配色和配件。不要趁机换角色。

## 独立拼豆像素稿

```text
Redesign the approved character as ONE deliberately authored LOW-RESOLUTION
PIXEL ART sprite for about [N] occupied square bead cells.
The cartoon reference is identity and palette inspiration, not a tracing target.
The bead reference demonstrates readable pixel clusters, not a character to copy.

Retain: [key identity cues]. Simplify or remove: [specific unnecessary details].
Allocate enough grid cells to the face: a dominant large head, spacious eyes,
separate lashes/iris/eye whites, and visible white highlights.
Short clear limbs; compact wings/hair/props that do not shrink the face.
Hair in a few broad locks; skirt in a few broad fold shapes; simple accessories.

Plan around [estimated occupied width × height] square cells, with [N] occupied
cells after background removal. The numerical count will be checked later.
Consistent coarse square pixel lattice, clean pure black stepped contours,
[C] purposeful flat palette tones arranged into coherent highlight and shadow clusters.
No dithering, gradients, anti-aliasing, tiny lace, fine veins, texture or noisy speckles.
Full body, connected silhouette, white margins, no grid lines or bead holes,
no text, no wall, no photograph or mockup. Exactly one sprite.
```

生成工具不保证严格像素格、32 色或 4000 颗；这些是设计目标，必须在编码后实测。生成图本身没有真实逐格数据时，标为像素设计稿。

## 返工应对

| 实际图纸的问题 | 下一步 |
|---|---|
| 脸太小，五官挤成团 | 增大头脸，缩短身体/缩小翅膀与道具；重画眼睛，保留单独高光格 |
| 发丝、花纹、蕾丝变碎点 | 删装饰，将头发和衣服改成连续大色块 |
| 眼镜和眼睛混在一起 | 扩大镜片内部留白，调整刘海，减少镜框重叠 |
| 黑线被量化成灰色或断开 | 检查采样对齐与原色投票，保护黑色轮廓，逐格补足关键结构 |
| 实际色数少于要求 | 先检查导出统计；在头发、衣服、翅膀等材质中设计有意义的明暗色块，再重新匹配色卡 |
| 达到颗数但画面仍不清楚 | 重做像素设计，不通过放大预览、插值或更多噪点掩盖 |
| 花饰或翅膀悬空 | 在设计上贴合主体或增加合理连接；不要为了连通机械穿过空白画直线 |
| 用户认可风格并说继续 | 按已确认范围扩展，沿用规格；每款用新的发型、服装、配件和姿态区分 |

## 可复用的经验

一次六款蝴蝶主题项目使用了“花冠双辫、眼镜抱书、长发花篮、闭眼玫瑰坐姿、白裙芭蕾”等辨识特征，实际图纸约 3950–4000 颗、32 色、约 60–70 格宽与 90–104 格高。它说明大头、短身、适度收缩配件可以保住五官；这些角色、尺寸和数量不是其他任务的强制配置。
