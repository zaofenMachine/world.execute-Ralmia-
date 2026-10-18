# 第六批：第二版第二轮图片

依据 [request_v2c.md](request_v2c.md) 完成全部 12 张（P0 九张、P1 三张）。均为 1672×941 PNG；9 张透明 RGBA、3 张不透明。图片通过内置 image_gen 生成；人物比例定位按用户授权仅缩小／平移，不做插值放大。已有 53 张 PNG 的 SHA256 全部未变。

## 文件

| 编号 | 文件 | 说明 |
|---|---|---|
| L13a | [creation_plate.png](creation_plate.png) | 只有水墨背景，原手臂遮挡处补全 |
| L13b | [creation_hand_ralmia.png](creation_hand_ralmia.png) | 同画布机械手透明层 |
| L13c | [creation_hand_lishenna.png](creation_hand_lishenna.png) | 同画布自然手透明层，指尖重画 |
| L11a | [cube_together.png](cube_together.png) | 贴脸、挽住胳膊的全身合照 |
| L11b | [cube_alone.png](cube_alone.png) | 局部移除里榭娜；洛菈米亚维持姿势与表情 |
| L12a | [ledge_together.png](ledge_together.png) | 原世界崖边，靠肩坐着，中央勾小指 |
| L12b | [ledge_alone.png](ledge_alone.png) | 局部移除里榭娜，洛菈米亚和场景锁定 |
| L15a | [cat_ralmia_v2.png](cat_ralmia_v2.png) | 腰以上、无尾无腿、猫爪与单眼眨眼 |
| L15b | [cat_ralmia_v2b.png](cat_ralmia_v2b.png) | 只改脸为满足的闭眼表情 |
| L9a | [lishenna_sit.png](lishenna_sit.png) | 不可见细杆坐姿，一脚踢起 |
| L9b | [lishenna_sit_b.png](lishenna_sit_b.png) | 同一上身，只交换小腿和鞋的动作 |
| L14 | [ending_together.png](ending_together.png) | 胸以上、闭眼贴脸、下巴下勾小指 |

本批没有红线；红领结属于洛菈米亚的原服装。角色参考使用已通过的两张设定图。宝石方向、黑机械手、里榭娜纯黑短裤和青色领结领带均已视觉核对。

## 配对像素检查

B 均通过对应 A 的局部编辑生成，随后回填编辑区外的 A 原始像素。遮罩为同画布黑白 PNG，白色表示允许编辑。

| 配对 | 编辑区外像素 | 变化数 | 遮罩 |
|---|---:|---:|---|
| 立方体 | 809,209 | 0 | [cube_edit_mask.png](_qa/round6/cube_edit_mask.png) |
| 崖边 | 1,481,317 | 0 | [ledge_edit_mask.png](_qa/round6/ledge_edit_mask.png) |
| 猫娘 | 1,557,881 | 0 | [cat_face_edit_mask.png](_qa/round6/cat_face_edit_mask.png) |
| 晃脚 | 1,372,562 | 0 | [sit_edit_mask.png](_qa/round6/sit_edit_mask.png) |

猫娘两张全图 Alpha 一致。晃脚图 y<490 的上身完全一致，双手与麦克风另外锁定；修改区域涵盖小腿、鞋、后侧黑袜膝盖轮廓及原脚移走后的透明区域。立方体独自版补出了被遮挡的机械胳膊，修正了生成结果中误画成肤色的手。

2026-10-18 最终按用户蓝／红示意图修正：近侧的左小腿从画面右侧膝盖向左踢出，在前景遮住后方垂下的右小腿；踢腿高度收低到接近 A。此前把踢腿放到后方，以及将双腿分开的结果均已替换。当前 `lishenna_sit_b.png` 使用内置 image_gen 在 A 上局部编辑，随后局部补好后膝连接。保持生成结果原画布坐标，没有拆出、平移或缩放肢体。编辑区外 1,372,562 个像素变化为 0，双手与麦克风锁定区域 6,793 个像素变化为 0。A 和其余 63 张根目录 PNG 未改。[局部预览](_qa/round6/sit_corrected_leg_detail.jpg)、[姿势提示词](_production/round6/sit_foot_direction_attempt5.json)、[后膝修补提示词](_production/round6/sit_foot_direction_attempt6.json)、[处理记录](_production/round6/sit_foot_direction_feedback.json)、[修正验收](_qa/round6/sit_foot_direction_validation.json)。

## 神卡三层

- 三张保持原画布坐标。机械手不透明内部的 159,276 个像素 RGB 已恢复为原图，边缘采用透明抠图及去底色处理。
- 里榭娜的指尖先在完整画面上重新绘制，再单独提取；不再使用旧灰青色指尖。透明层按整数平移 (+8,+9) 像素登记，指尖约在 (826,403)，不缩放。
- 叠合后两指 alpha>128 的最近边缘间距约 2.24 像素，可由后续两手运动的终点微调到接触；两层均可独立移动。
- [三层叠合预览](_qa/round6/creation_layers_composite.jpg)、[指尖放大检查](_qa/round6/creation_fingertips_detail.png)、[背景编辑遮罩](_qa/round6/creation_plate_edit_mask.png)。

## 构图定位

立方体合照约 92% 画高；猫娘约 90%；坐姿 A 约 80%；结尾约 85%。崖边人物约 57.6%，比需求的半画高略大。晃脚两张的最远旋转半径均小于画布半高，可围绕中心完整旋转。坐姿放到代码细线时可参考支点 y≈550，详见 [座部与手部检查](_qa/round6/sit_support_detail.png)。

所有生成输入、修订和源输出记录在 [prompts.json](_production/round6/prompts.json) 及其引用的分组记录；中断前的调用也已从本任务记录恢复。风格和世界参考被整理为拼图，解决单次最多 5 张参考图的限制。

## 预览与复现

- [12 张总览](_qa/round6/contact_sheet.jpg)
- [立方体切换](_qa/round6/cube_switch.gif)
- [崖边切换](_qa/round6/ledge_switch.gif)
- [猫娘切换](_qa/round6/cat_switch.gif)
- [晃脚切换](_qa/round6/sit_switch.gif)
- [整批验收 JSON](_qa/round6/validation.json)
- [根组像素锁定脚本](_production/round6/finalize_root_assets.py)
- [整批验收脚本](_production/round6/audit_all.py)

未替换 MV 代码或重渲成片；本次交付图片、遮罩和验收资料。
