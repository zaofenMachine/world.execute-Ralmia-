# 0–60 秒图片素材交付

根目录为 16 张最终 PNG：14 张 P0、2 张 P1。使用内置 image_gen 生成，未使用 API / CLI 付费回退。

## 人物版本

统一使用 ref_sheet.png：音速版白裙装甲、长金发、红色领结 / 领口、右太阳穴青色宝石、黑色分节机械手与掌心核心。长发和红领结按用户最终纠正执行，优先于计划中的齐肩发及“红色只给红线”。后续每张生成和修订均附带这张设定图。

官方服装参考：
- [音速の機構・ララミア](https://shadowverse-portal.com/card/116841010?lang=ja)
- [アストロウィング・ララミア](https://shadowverse-portal.com/card/123841010?lang=ja)

## 文件清单

| 文件 | 用途 | 透明 |
|---|---|---|
| ref_sheet.png | 第 0 张统一人物设定 | 否 |
| hand_palm.png | 掌心造物 | 是 |
| parts_exploded.png | 14 件机械零件 | 是 |
| eye_open.png | 睁眼 A | 否 |
| eye_closed.png | 闭眼 B，A 的局部编辑 | 否 |
| world_L1_sky.png | 天空层 | 否 |
| world_L2_city.png | 远城、太阳、水面 | 是 |
| world_L3_mid.png | 左侧废墟钢架 | 是 |
| world_L4_fore.png | 前景平台及背面人物 | 是 |
| dash_launch.png | 起跑 | 是 |
| dash_full.png | 全速飞行 | 是 |
| hand_gap.png | 指尖与红线有间隙 A | 否 |
| hand_tied.png | 红线绕指两圈并打结 B，A 的局部编辑 | 否 |
| portrait_front.png | 正脸胸像 | 否 |
| floating.png | P1 倒悬漂浮 | 是 |
| pinky_promise.png | P1 勾小指与红线 | 否 |

## 验收

- 两张 B 均由对应 A 通过 image_gen 局部编辑生成，随后按用户授权回填编辑区域之外的 A 原始像素。
- 闭眼组编辑区域外 1,253,104 个像素完全相同；红线组编辑区域外 1,559,086 个像素完全相同。两组变化数均为 0。
- 眼睛编辑区保留交叉金发的原始金色像素；眉毛、鼻梁及其余画面来自 A。红线编辑仅取新旧红线及抗锯齿边缘的联合区域，手的其余部分全部来自 A。
- 透明素材均为真正带 alpha 的 RGBA PNG，不含绘制出来的棋盘背景。
- 四张世界层均为 1672×941，可直接同坐标叠合。world_L4_fore 人物与平台保持一张图，轮廓清楚。
- 拆解图实测 14 个独立零件；alpha > 128 口径下，最小间距 82.61 px。
- 漂浮图不透明轮廓到画布中心的最大距离约 338.21 px，小于半高 470.5 px，原位完整旋转有边距。

## 尺寸与构图边界

工具实际输出接近 16:9 的 1672×941；dash_full.png 为 1671×941。未达到期望的 2560×1440，保留原生图，未插值放大冒充更高分辨率。

计划中的坐标是构图引导，生成结果有偏差。合成请读取 _qa/anchors.json 的实际锚点：掌心核心约 (0.6400, 0.5191)，远城水线约 y=0.6312。前景人物约占画面高度 20%，大于计划中的约 15%。世界层采用与主素材相近的 16:9 画布，未扩成 3200×1440 宽幅。上述位置和尺寸差异已明列，避免直接套用期望坐标造成错位。

## 复查与生产记录

- _qa/contact_sheet.jpg：全部素材缩略图。
- _qa/world_composite.jpg：四层合成视觉预览。
- _qa/eyes_blink.gif、thread_blink.gif：成对切换预览。
- _qa/validation.json：尺寸、alpha、配对区域像素验证。
- _qa/anchors.json：零件边界及合成锚点。
- _production/prompts.json：最终提示词、参考输入、生成来源及修订。
- _production/raw/：回填前的 AI 局部编辑及部分修订前素材。
- _production/lock_pairs_and_qa.py：可重复执行的配对锁定与验收。
- _production/geometry_qa.py：零件间距与旋转边距验收。
- _superseded_short_hair/：不符合人物设定的早期版本，仅作备份，不用于成片。

本次只交付图片和验收记录，尚未替换进 MV 或重渲成片。
