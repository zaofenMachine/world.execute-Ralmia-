# 第二批 21 张图审核反馈（2026-10-16）

**结论：** 21 张中 20 张可以直接用。**只有 1 张需要重出：`back_reach.png`。** 另有 2 张的太阳穴宝石画到了左边，我会在代码里水平翻转，不用重出，但以后请注意。

## 已核对、没问题的项目

- **三组局部编辑：** lab_desk → lab_desk_empty、pinky_promise → pinky_alone、eye_open → eye_tear，我逐像素复核过，编辑区外完全一致，内容也对。泪滴落在她的左眼（画面右侧）下方，椅子转开了，红线松垂下来。
- **夜景：**
  - world_L2_city_night 和日景相比，alpha 只在太阳区域有差异（x 1035–1186、y 453–591），建筑轮廓完全一致。
  - world_L1_night 和日景交叉溶解时云带基本重合，过渡自然。
  - 夜空自带月亮，我会删掉代码里自己画的那个。
- **透明素材：** 12 张的抠图边缘放在深色底上检查过，没有白边或灰边。
- **"他"的一致性：** creator_sheet、lab_desk、creator_walk、creation_inverse 里都没有露脸，黑短发、白大褂、成年人的手，全部一致。
- **服装：** 和 ref_sheet 一致。

## 需要重出：`back_reach.png`（#20）

**问题：** 举起的右手在头的高度、偏在身体外侧，五指张开、掌心朝向镜头，读起来像在**挥手打招呼**，不像"按在一面看不见的墙上"。头也没有低下去。这张用在桥段 ILLEGAL ARGUMENTS（她手按源代码墙对抗"神"），情绪必须是压抑和抵抗，挥手的感觉完全不对。

**重出提示词（附 ref_sheet）：**

```
full-body back view, she stands close to an invisible wall directly in front of her.
Her right palm is pressed FLAT against that wall at shoulder height, slightly in front of her face,
elbow bent, forearm foreshortened toward the wall — we see the BACK of her black mechanical hand,
fingers together and pressed, not spread, not waving.
Left arm hangs straight down at her side, hand clenched into a fist.
Head bowed forward, forehead almost touching the wall. Shoulders slightly hunched, tense.
Long blonde hair falls straight down her back. transparent background.
```

## 宝石位置画反了（我自己翻转，不用重出）

她的宝石在**右**太阳穴：正面看在画面左侧，脸朝右的侧面能看到，脸朝左的侧面看不到。下面两张画到了左太阳穴：

- **listen_profile.png：** 脸朝左，却看得到宝石。我会水平翻转成脸朝右，不影响使用。
- **reach_camera.png：** 正面特写，宝石在画面右侧。我会水平翻转，伸出的手随之变成她的左手。她两只手都是机械手，所以没问题。

以后出正面或侧面的图，请按这个规则检查一遍。

## 小问题（可以接受，不必重出）

- **spec_tomato：** 整个番茄都做成了白色装甲，失去了番茄的样子，单看更像南瓜或大蒜；靠右边的横切面和标签才认得出来。茄子保留了紫色果皮，两者处理不一致。我理解是为了避开红色（红色只给红线和领结），这个取舍我接受。
- **spec_tabbycat：** 毛发是细密的写实笔触，比其他图更"绘画感"，和墨线加平涂的整体画风有些距离。成片里它只出现约 3.7 秒，而且放在纸底标本卡上，问题不大。
- **"他"的手：** creator_sheet 和 creation_inverse 里的手偏成熟、能看到青筋，而第一批 pinky_promise 里的人手偏年轻光滑。两只手不会出现在相邻的镜头里，先不处理。
- **分辨率：** 仍然是 1672×941。这批的特写都单独出了构图（creation_inverse、reach_camera、listen_profile、portrait_front_v2），比上一批好用很多。
