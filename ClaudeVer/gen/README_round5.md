# 第五批：第二版补图

按 [request_v2b.md](request_v2b.md) 完成两张，含 P1。两张均为 1672×941 原生 PNG，使用内置 image_gen，未插值放大。每次生成与修订均附带已通过的 `lishenna_ref_sheet.png`，风格参考为 `listen_profile.png`、`lishenna_stand.png`。

| 编号 | 文件 | 用途 | 格式 |
|---|---|---|---|
| L7 | [lishenna_front.png](lishenna_front.png) | 代码神像的正面轮廓；右手持麦克风 | 透明 RGBA |
| L8 | [lishenna_sing_profile.png](lishenna_sing_profile.png) | 左向侧脸，闭眼轻唱，后方一只圆盘 | 纸底 RGB |

L7 初稿的长发填满了臂身空隙，已通过局部编辑展开双臂、收拢身后头发并外移圆盘。最终采用正面、平视构图，纯黑短裤、青领结和领带、格纹发带、紫鞋带沿用人物基准。主体含头饰约占画高 97.1%，未裁切。alpha>128 口径下主体与两只圆盘为三个分离组件；y=400 处双侧臂身透明间隙约 66 / 57 像素。

L8 在原 `listen_profile.png` 上替换角色生成，匹配原镜头的脸部位置、大小与纸底。左向闭眼轻唱，嘴唇微张，麦克风从下方靠近而未遮嘴。角色／手持麦克风区域之外回填原纸底像素，变化数为 0。局部五官轮廓有角色差异，原画布内两张脸的唇线高度约差 15 像素；合成时可据实际嘴部位置接旋律线。

已有 51 张 PNG 的 SHA256 均不变；未改 MV 代码、既有素材或成片。

- [两张素材与黑白轮廓总览](_qa/round5/contact_sheet.jpg)
- [面对面预览](_qa/round5/profiles_facing_compare.jpg)：仅预览中水平翻转洛菈米亚的聆听图，两张图以相同缩放并排；原文件未翻转。
- [正面轮廓遮罩](_qa/round5/lishenna_front_silhouette.png)：alpha>128 导出的黑白 QA 图；实际合成也可直接读取源 PNG 的 alpha。
- [完整提示词与修订记录](_production/round5/prompts.json)
- [验收数据](_qa/round5/validation.json)、[验收及背景锁定脚本](_production/round5/validate.py)

原始生成结果保存在 `_production/round5/raw/`。
