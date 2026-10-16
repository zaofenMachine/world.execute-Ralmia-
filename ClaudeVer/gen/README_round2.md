# plan_full 第二批图片交付

已按用户选定范围完成整批 21 张 PNG：P0 清单实际为 16 张，P1 为 5 张。文件均放在 gen 根目录，第一批 16 张保留。本次使用内置 image_gen，不使用 API / CLI 回退。

## 统一设定与画风

- 每张生成与修订均附 ref_sheet.png；洛拉米亚保持长金发、红领结、白色钟形装甲裙、黑色紧身机械结构与白靴。
- 先生成 creator_sheet.png。出现创造者的素材同时附 creator_sheet.png 和 ref_sheet.png；创造者只显示背影、遮脸侧面或成年人手部。
- 新增人物与物体强化了墨线压力变化、平涂及纸纹。夜景与泪眼等配对优先保留原素材风格和结构。
- 专门生成 creation_inverse.png 和 reach_camera.png 特写；listen_profile.png、portrait_front_v2.png 也采用头颈近景，不依赖全身图大幅裁切。
- 红色保留给红线、原有红领结及同款猫领结；机械番茄采用白装甲/黑分节/青核心配色，未引入红色果皮。

## 文件清单

| 编号 | 文件名 | 级别 | 透明 | 说明 |
|---|---|---|---|---|
| 0b | creator_sheet.png | P0 | 否 | 背面、遮脸侧面、成年双手参考 |
| 11a | lab_desk.png | P0 | 否 | 三块空白屏幕、创造者背影、咖啡杯与散纸 |
| 11b | lab_desk_empty.png | P0 | 否 | 11a 局部编辑移除人物、椅子微转 |
| 12 | pinky_alone.png | P0 | 否 | pinky_promise 局部编辑移除整只人手，红线松垂 |
| 13 | offer_pose.png | P0 | 是 | 正面张臂、双掌核心可见 |
| 14a | spec_eggplant.png | P0 | 是 | 机械茄子标本 |
| 14b | spec_tomato.png | P0 | 是 | 左整果、右横切面，同画布分离 |
| 14c | spec_tabbycat.png | P0 | 是 | 普通虎斑猫蜷睡、红领结 |
| 15 | creation_inverse.png | P0 | 否 | 左上机械手、右下成年人手，指尖实际相触 |
| 16a | world_L1_night.png | P0 | 否 | 原天空的夜色编辑，保留云带构图 |
| 16b | world_L2_city_night.png | P0 | 是 | 原远城夜景编辑，移除太阳、亮灯及水面倒影 |
| 18 | eye_tear.png | P0 | 否 | eye_open 局部编辑，仅画面右眼下增加一滴泪 |
| 19 | sitting_alone.png | P0 | 是 | 抱膝、额头抵膝，约半高构图与充足空白 |
| 20 | back_reach.png | P0 | 是 | 全身背影、右手按隐形墙，镜头看到手背 |
| 22 | reach_camera.png | P0 | 是 | 前景放大的右机械手、坚定泪眼特写 |
| 24 | creator_walk.png | P0 | 是 | 成年创造者迈步走远，小指短红线 |
| 17 | listen_profile.png | P1 | 否 | 朝左闭眼聆听、手在领口处，头颈近景 |
| 21 | run_front.png | P1 | 是 | 3/4 正面向镜头奔跑、青色推进器 |
| 23 | blackboard.png | P1 | 是 | 朝右举粉笔的人物，无黑板和文字 |
| 25 | escape_leap.png | P1 | 是 | 双臂张开、朝镜头跃出、自由的笑容 |
| 26 | portrait_front_v2.png | P1 | 否 | 领口以上、微张嘴和轻抬眉的安静好奇表情 |

## 配对验收口径

三张局部编辑先由 image_gen 在 A 上编辑，再按用户已授权方式回填编辑区外的原始像素。

| 配对 | 编辑区外像素数 | 编辑区外变化数 |
|---|---:|---:|
| lab_desk → lab_desk_empty | 1,139,618 | 0 |
| pinky_promise → pinky_alone | 1,041,939 | 0 |
| eye_open → eye_tear | 1,555,747 | 0 |

夜景与上述局部添加/移除不同：整张图的颜色都需改变，因此不声称夜景 RGB 逐像素相同。两张夜景均以对应日景作为编辑目标生成。远城额外锁定了原建筑透明轮廓：水线上方、移除太阳区域以外，alpha 变化为 0；y=594 以下水面 alpha 为 255。夜空的云带通过视觉对照检查，未宣称其轮廓每个像素完全相同。

12 张透明素材均为真正 RGBA PNG，alpha 同时包含 0 与 255。配对及夜景画布均为 1672×941。原生输出整体约 1672×941，个别独立素材有 1px 高度差，精确尺寸见 validation.json。未达到 2560×1440，未通过插值放大冒充高分辨率。

## 预览和生产记录

- _qa/round2/contact_sheet.jpg：21 张总览。
- _qa/round2/night_L1_L2_composite.jpg：夜空和远城叠合预览。
- _qa/round2/night_with_existing_foreground.jpg：再叠第一批中/前景的预览；中/前景仍是第一批日景配色。
- _qa/round2/lab_blink.gif、pinky_blink.gif、tear_blink.gif：配对切换检查。
- _qa/round2/validation.json：尺寸、透明通道和像素一致性报告。
- _qa/round2/*_edit_mask.png：局部编辑允许变化的区域。
- _production/round2/prompts.json：21 张完整提示词、参考输入、生成来源及修订。
- _production/round2/raw/：像素锁定前 AI 结果及修订备份。
- _production/round2/validate_and_lock.py：可重复执行的验收及像素锁定脚本。

本次任务范围为生图，未修改 MV 工程、歌词时间或音轨，也未执行 plan_full 中的成片渲染工作。



## feedback_round2 修订

仅重做并替换 back_reach.png：低头、收紧肩膀、右手五指并拢贴向前方隐形墙，背向镜头的机械手背不显示掌心核心，左拳下垂。已查看实际生成图及新旧对照。旧版备份在 _production/round2/raw/back_reach_before_feedback_round2.png；对照图在 _qa/round2/back_reach_feedback_compare.jpg。其他 36 张最终 PNG 的 SHA-256 校验一致。反馈注明由成片代码翻转的 listen_profile 和 reach_camera 保持原文件。完整提示词与修订来源见 _production/round2/back_reach_feedback_round2.json。
