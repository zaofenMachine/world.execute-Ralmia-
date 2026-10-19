# 第七批：向右散步、边走边唱

依据 [request_v2d.md](request_v2d.md)，交付两张 1672×941 透明 RGBA PNG。

| 文件 | 动作 |
|---|---|
| [lishenna_stroll_a.png](lishenna_stroll_a.png) | 近侧左脚在前，空闲左臂向后摆 |
| [lishenna_stroll_b.png](lishenna_stroll_b.png) | 远侧右脚在前，空闲左臂向前摆 |

人物向画面右侧走，麦克风保持在嘴边。服装沿用已通过的《奏绝》设定，包含青色领结／领带、纯黑短裤、黑白格发带、紫色鞋带；风格参考同时附了站姿与坐姿图。

## 配对与定位检查

- B 在 A 上通过内置 image_gen 局部编辑；随后局部修正腿部相位，并补全旧摆臂移开后露出的发束。
- 编辑范围覆盖腿、鞋、空闲摆臂，以及摆臂移开或遮挡的小块头发／躯干。编辑区外 **1,386,449 个像素，变化数 0**。
- 头部和 y<300 区域原像素锁定。麦克风及持麦手臂另有 **18,045 个像素锁定，变化数 0**。
- A/B 可见人物高度均为约 **84.91%**；头顶约 y=49。两张的前、后鞋底接地点均为 **y=847**，约画高 90%。接地点按 Alpha>128 统计，已检查透明边缘。
- A 的原始整图输出为 1672×941，在同尺寸画布中仅缩小至 91.12% 并平移定位，没有放大。为对齐地面，A 后鞋下移 8 px，B 后／前鞋分别上移 5／3 px，踝部小范围过渡；原始生图均保留。
- 既有 **65 张 PNG 的 SHA256 均未变化**。

遮罩白色为允许编辑，黑色为从 A 原样保留：[stroll_edit_mask.png](_qa/round7/stroll_edit_mask.png)。

## 预览

- [A/B 并排](_qa/round7/stroll_compare.jpg)
- [A/B 交替动画](_qa/round7/stroll_switch.gif)
- [脚底同一水平线](_qa/round7/groundline_preview.jpg)
- [线稿轮廓检查](_qa/round7/lineart_preview.jpg)

线稿预览采用简单边缘提取，仅用于检查轮廓和主要线条，不替代 MV 中最终的荧光线稿处理。

## 记录与复现

- [提示词与源输出索引](_production/round7/prompts.json)
- [数值验收](_qa/round7/validation.json)
- [独立视觉验收](_qa/round7/visual_review.json)
- [A 定位脚本](_production/round7/prepare_a.py)
- [B 局部锁定、遮罩与预览脚本](_production/round7/finalize_pair.py)

所有角色内容由内置 image_gen 生成，脚本只用于已授权的缩小／平移定位、透明边缘清理、编辑区外像素回填及验收预览。本批仅交付图片和记录，没有修改 MV 代码或重渲成片。
