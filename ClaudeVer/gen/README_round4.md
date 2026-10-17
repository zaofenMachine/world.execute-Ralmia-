# 第四批：里榭娜第二版素材

按 [request_v2.md](request_v2.md) 完成 L0 与后续全部 7 张，包含 P1 漂浮图。全部为 1672×941 原生 PNG，使用内置 image_gen；未放大或改动 MV 代码。

## 角色基准

用户通过的 [lishenna_ref_sheet_v3.png](lishenna_ref_sheet_v3.png) 已同步到正式名称 [lishenna_ref_sheet.png](lishenna_ref_sheet.png)。后续每次生成及修订均附带该设定图。腰扣按用户接受的近似版本沿用，短裤纯黑，无灰白侧拼片；旧设定版本保留。

## 素材

| 编号 | 文件 | 内容 | 底色 |
|---|---|---|---|
| L1 | [pinky_promise_v2.png](pinky_promise_v2.png) | 里榭娜与机械手勾小指 | 纸底 |
| L2 | [creation_inverse_v2.png](creation_inverse_v2.png) | 指尖相对，里榭娜蓬袖 | 墨底 |
| L3a | [stage.png](stage.png) | 演唱会，三块纯白屏幕 | 不透明 |
| L3b | [stage_empty.png](stage_empty.png) | 散场，黑屏、话筒架与一盏工作灯 | 不透明 |
| L4 | [lishenna_walk.png](lishenna_walk.png) | 走开背影，手与小指可见 | 透明 RGBA |
| L6 | [lishenna_stand.png](lishenna_stand.png) | 朝画面左侧的三分之四站姿 | 透明 RGBA |
| L5 | [lishenna_float.png](lishenna_float.png) | 闭眼漂浮哼唱，预留旋转边距 | 透明 RGBA |
| L1 配套 | [pinky_alone_v2.png](pinky_alone_v2.png) | 细手臂版独手 B，与新版勾指 A 配对 | 纸底 |

## 配对与验收

- L1 初版在原勾指图上局部编辑。随后按用户反馈收细机械前臂、缩小里榭娜蓬袖；中央手指、掌心核心和红线结保持像素一致。左侧手臂已按反馈改变，不再与旧独手图叠用，请使用配套 `pinky_alone_v2.png`。
- L2 在原神卡图上局部编辑；机械手与接触点的固定区域逐像素一致。
- L3b 在 L3a 上编辑人物、观众、灯光与屏幕；屏幕框及锁定的结构线条恢复 A 像素。灯光影响区域的结构明暗随散场变化，不宣称全幅结构颜色相同。
- 以上三组编辑区外变化均为 0 像素；掩膜和统计见 [validation.json](_qa/round4/validation.json)。视觉检查后已清除旧手及人物腿部残影。
- 三块屏幕内侧已按用户授权统一为精确 RGB(255,255,255) / RGB(0,0,0)，A/B 使用相同边界。提供 [合并遮罩](_qa/round4/stage_screens_mask.png) 及分屏遮罩 `stage_screen_1_mask.png` 至 `stage_screen_3_mask.png`，1–3 对应左、中、右；边界坐标记录在验收 JSON。
- 透明图主体高度（alpha>32）分别约 97.1%、94.9%、80.8%；漂浮图上下分别留约 100 / 81 像素。
- 旧版原镜头仍保留；正式设定名称已更新为通过的 v3，新版勾指图按反馈修订。修订前文件保存在生产目录。

## 记录与预览

- [整批总览](_qa/round4/contact_sheet.jpg)
- [舞台切换](_qa/round4/stage_switch.gif)、[新版勾指与独手配对](_qa/round4/pinky_v2_pair.gif)、[指尖切换](_qa/round4/creation_switch.gif)
- [完整提示词与输入图记录](_production/round4/prompts.json)
- [像素锁定与验收脚本](_production/round4/validate_and_lock.py)
- AI 原始输出保存在 `_production/round4/raw/`。

## 手臂与袖子比例反馈

已通过内置 image_gen 局部编辑，收细左侧机械前臂与腕部、减小右侧蓬袖。手指、红线结及掌心核心维持原位，编辑区外 0 像素变化。配套独手 B 在修订后的 A 上局部移除人手生成，其余区域锁定，避免切换回旧的粗手臂。旧 `pinky_alone.png` 保留供第一版使用。

[修改前后对比](_qa/round4/pinky_proportion_before_after.jpg) · [生成提示词](_production/round4/pinky_proportion_feedback.json) · [专项验收](_qa/round4/pinky_proportion_validation.json)。已有 50 张 PNG 中只替换了用户指定的 `pinky_promise_v2.png`，其余 49 张哈希不变；新增配套独手图一张。
