# world.execute(me); × 洛菈米亚（Ralmia）—— 前一分钟完善计划 + 生图需求

## 一、整体思路（沿用 0–30 秒已定的方向）

**叙事主线：** 她是被"造"出来的程序（0–15 秒），她的天性是快（15–30 秒），但她碰不到任何东西（22–28 秒）。30–60 秒她开始用数学语言说"我能给你什么"。到 56 秒的 "unite"，那根始终差一点够不到的红线，第一次绕上了她的手指。这样，前一分钟本身就是一段有起伏、有回收的完整故事。

**美术系统：**

- 底色在两种之间切换：墨黑底（代码、运行）和暖纸底（手绘、造物），二者的对立同时也对应了她的系统名 Ōmeteōtl 这位"二元之神"。
- 用色：
  - 青色只给她的核心、眼睛和发光部件；
  - 红色只给红线。
- 字体：
  - Big Shoulders 粗体负责冲击；
  - Plex Mono 负责代码；
  - Instrument Serif 斜体负责人声里的连接词。

**新图的用法：** 新图全部当"演员"用，不当"背景板"。人物尽量做成透明底的分层素材，由代码负责动作和合成，避免整图平移。

## 二、0–30 秒的修改清单

| 段落 | 问题 | 改法 | 是否需要新图 |
|---|---|---|---|
| 3.7–5.9 秒 Pieces | 只有字母落位，和"她的零件"没有关系 | 字母和她的机械臂零件交替落进格子，最后一格是核心宝石 | 需要：#2 |
| 5.9–7.7 秒 Creation | 旧手图和新人设可能不统一 | 换新图；点阵→线稿→上色的流程保留 | 需要：#1 |
| 9.7–11.4 秒 Initialization | 眼睛构图偏侧脸，缝里看到的信息少 | 换成正面特写，虹膜带机械光圈，睁眼时光圈"对焦" | 需要：#3a、#3b |
| 11.4–13.3 秒 World | 整张图切成竖条升起，没有纵深 | 改成分层"搭布景"：天空→远城→中景废墟→前景人物逐层升起，搭好后有轻微视差 | 需要：#4 的四层 |
| 13.3–15.1 秒 Simulation | 7×7 太密，小窗看不清 | 改成 2×2 再到 4×4，每格是不同"渲染阶段"（线框、线稿、平涂、成品），表示一次次迭代 | 不需要 |
| 15.1 秒、18.8 秒 两个强拍 | 间奏全是抽象图形，没有她 | 在这两个强拍上各闪入 2–4 帧她冲刺的剪影，再接回矢量画面 | 需要：#5、#6 |
| 22.5–28 秒 Zeno 段 | 每拍节奏一样，偏平 | 第 56 拍加一次"全停"半拍再继续，红线随逼近轻微颤动 | 用 #7a 替换旧图 |
| 全片 HUD | 左上的日志压到大字（如 SWIFTER） | 大字占用区域时日志自动隐去 | 不需要 |

## 三、30–60 秒分镜

时间是按节拍网格和歌词识别得出的近似值；拍号 k 对应 0.34 + k × 0.4615 秒。

| 时间 | 歌词 | 画面设计 | 新图 |
|---|---|---|---|
| 29.9–31.7 秒 | If I'm a set of points | 承接上一段炸开的点云。点重新聚成她的正脸，正脸只由点构成，每拍点的密度翻倍 | #8 |
| 31.7–33.6 秒 | then I will give you my dimension | 点逐级升维：一个点拉成线（1D）→ 扫成面（2D）→ 挤出立方体（3D），在强拍上一级一级跳。线框立方体里装着她的脸 | 不需要 |
| 33.6–35.4 秒 | If I'm a circle | 立方体塌成一个圆，这个圆就是她掌心的核心宝石（青色），半径线转一圈 | 不需要 |
| 35.4–37.3 秒 | then I will give you my circumference | 圆周被"剥开"拉直成一条长 2πr 的线段，CIRCUMFERENCE 沿这条线排字 | 不需要 |
| 37.3–39.1 秒 | If I'm a sine wave | 让圆继续转，投影出正弦波（单位圆生成正弦的经典图），圆和波保持连续，不切镜 | 不需要 |
| 39.1–41.0 秒 | then you can sit on all my tangents | 一条切线沿正弦波滑动，线上坐着一个小小的 YOU（矢量小人或字母），每拍换一个切点 | 不需要 |
| 41.0–42.8 秒 | If I approach infinity | 一条曲线无限贴近渐近线，同时用参数方程把 ∞ 画出来。回扣前面的 d 永远到不了 0 | 不需要 |
| 42.8–44.6 秒 | then you can be my limitation | 那条渐近线就是 YOU，曲线永远贴着它；配 lim 记号的排版 | 不需要 |
| 44.6–46.5 秒 | Switch my current | 示波器画面，交流正弦波满屏滚动，CURRENT 用波形描出来 | 不需要 |
| 46.5–48.3 秒 | to AC, to DC | AC 在拍上抖动，到 DC 时波形"啪"地拉成一条直线；两个字母本身就是波形 | 不需要 |
| 48.3–49.7 秒 | and then blind my vision | 回到眼睛：光圈收缩，眼睑合上，色彩从画面抽走，只剩描边（你认可过的闭眼方向，我用自己的方式做） | #3a、#3b |
| 49.7–52.0 秒 | so dizzy, so dizzy | 黑底上旋转的螺旋矢量，配她倒悬漂浮的透明素材，两次 dizzy 各转一次方向；字随正弦扭曲 | #9 |
| 52.0–53.9 秒 | Oh, we can travel | 时空图：光锥加世界线。她的速度"超过光"时，世界线越过 45 度，倒向过去（物理上超光速意味着时间逆行），直接接上她的设定 | 不需要 |
| 53.9–55.7 秒 | to A.D., to B.C. | 光锥上方的未来标 A.D.，下方的过去标 B.C.，年份刻度尺在拍上飞速倒退（复用开场的标尺元素） | 不需要 |
| 55.7–57.6 秒 | and we can unite | 回到手。红线终于绕上手指，22–28 秒"碰不到"的悬念在这里回收 | #7a、#7b |
| 57.6–59.4 秒 | so deeply, so deeply | 镜头推进绳结，绳结的纹理变成电路，红线沿电路走成小指上的红线 | #10 |
| 59.4 秒起 | If I can（副歌） | 副歌起点作为本段收尾。下一轮再做 | 视下一轮需要 |

## 四、生图需求

### 交付规则（请转给 GPT）

1. **尺寸：** 16:9，最好 2560×1440 或以上。如果只能出 1536×1024，请把主体放在中间的 16:9 安全区里，也就是上下各留约 80px 可以裁掉。
2. **透明底：** 标了"透明底"的图请出带 alpha 通道的 PNG。如果做不到透明，就用纯平 `#EFE6D2` 底，不要纹理和投影。
3. **成对图：** 标了"成对"的图，B 必须在 A 的基础上用局部编辑生成。构图、角度、线条位置必须和 A 完全一致，只改说明里那一处，否则两张图叠在一起时会跳。
4. **禁止项：** 不要文字、不要 logo、不要水印、不要 UI 元素。
5. **命名和存放：** 放进 `D:\Project\MV\ClaudeVer\gen\`，文件名用下面写的。
6. **人物一致性：** 先出 #0 设定图，之后每一张都把它当参考图一起喂进去。

### 通用风格段（每张提示词都放在最前面）

```
STYLE: hand-drawn Japanese anime illustration, confident ink linework with varied line weight,
flat cel colours with at most one shadow tone, subtle paper grain, restrained palette:
warm paper white #EFE6D2, ink black #080B10, steel greys, blonde hair #E8C063,
single accent cyan #62D8EA used ONLY on her core gem / eyes / glowing mechanical parts,
single accent red #E5484D used ONLY on the red thread.
NO text, NO logo, NO watermark, NO UI, NO lens flare, NO bokeh, NO glossy 3D render,
NO heavy airbrush gradients, NO extra characters unless specified.
CHARACTER: Ralmia (ララミア / 洛菈米亚) from Shadowverse — a girl-shaped high-speed machine
("Machina / Artifact"); use her official card art (音速の機構・ララミア, アストロウィング・ララミア)
as costume reference. Keep: shoulder-length blonde hair, blue eyes, oval cyan gem ornament at
her right temple, mechanical arms with black segmented fingers, white armour plates, a cyan core
in each palm, racer / booster mechanical parts. Fully clothed, non-sexualised, youthful but
not childish.
```

**关于人设，有一点要先说明：** 我只查到了她的文字设定（金发碧眼、机械造物、以速度为核心），没有看到官方卡图本身，所以"服装以官方卡图为准"要交给 GPT 去查、去对照。如果你希望延续 Astra 那批图的造型（太阳穴宝石加机械手），把那几张图也一起作为参考图喂进去就行；我这边两种造型都能接。

### 图片清单

#### #0 设定图 `ref_sheet.png`（P0，只做参考，不进成片）

- **用途：** 给后面所有图做人物一致性的参考。
- **构图：** 一张图里放全身正面、全身侧面（面朝右）、全身背面，再加一个胸像特写和一只张开的机械手掌（掌心核心可见）。
- **背景：** 纯纸色底。
- **提示词：** `character reference sheet, front / right-side / back full-body views in neutral standing pose, plus a bust close-up and an open mechanical palm detail, evenly spaced, plain paper background`

#### #1 掌心造物 `hand_palm.png`（P0，透明底）

- **用途：** 5.9–7.7 秒的 object creation，以及 33.6 秒的"圆就是掌心宝石"。
- **构图：** 右手机械手掌朝上，略微俯视。掌心核心位于画面约（62%，45%）处，五指微张、略弯，像托着什么东西。前臂从右下角出画。
- **要求：** 关节分段要清楚，线稿要干净。代码会提取这张图的线稿做"点阵→线稿→上色"，所以线条不能糊。
- **提示词：** `her right mechanical hand, palm up, slightly from above, fingers gently spread and curved as if holding something invisible, cyan core glowing softly in the centre of the palm, forearm exits frame bottom-right, transparent background`

#### #2 零件拆解图 `parts_exploded.png`（P0，透明底）

- **用途：** 3.7–5.9 秒 "lay down your pieces"。我会把每个零件单独抠出来，让它们一个个落进格子。
- **构图：** 机械前臂和手的爆炸拆解图，正俯视、平铺。共 12–14 个独立零件：多节指骨、掌板、核心宝石、腕环、前臂护甲片、几颗螺栓。零件之间至少留 60px 空隙，互不重叠、互不遮挡，大致排成松散的网格。
- **风格：** 像手绘的机械说明书插图，墨线加平涂。
- **提示词：** `exploded-view technical illustration of her mechanical forearm and hand, 12-14 separate parts laid flat top-down in a loose grid with generous empty space between parts (no overlap), finger segments, palm plate, cyan core gem, wrist ring, armour plates, a few screws, hand-drawn instruction-manual feel, transparent background`

#### #3a / #3b 眼睛特写，睁眼 / 闭眼（P0，成对）

- **用途：** 9.7–11.4 秒 initialization，以及 48.3–49.7 秒 "blind my vision"。
- **#3a `eye_open.png`：** 近乎正面的极近特写，画面内只有双眼加鼻梁上半，或者一只眼占主导。关键信息全部压在画面竖向 35%–65% 的横带里，因为这段会用一条细缝来展示。虹膜是蓝色，带一圈细细的机械光圈叶片（像相机光圈），瞳孔中心有极小的青色亮点。几缕发丝横过画面。背景是纸色。
- **#3b `eye_closed.png`：** 在 #3a 上局部编辑，只把眼睑合上，睫毛下垂。其余一律不动。
- **提示词（3a）：** `extreme close-up of her eyes, near-frontal, all key detail inside the central horizontal band (35%-65% of height), blue irises with a fine ring of mechanical aperture blades like a camera iris, tiny cyan point light in each pupil, a few strands of blonde hair crossing, paper background`
- **提示词（3b，编辑）：** `same image, only change: eyes gently closed, lashes down; keep everything else pixel-aligned`

#### #4 世界分层四张 `world_L1_sky.png` … `world_L4_fore.png`（P0，L2–L4 透明底）

- **用途：** 11.4–13.3 秒 "set up our new world"，四层像搭布景一样依次升起。
- **尺寸：** 最好宽于 16:9，例如 3200×1440，给视差移动留出余量。四张图尺寸必须完全相同，地平线高度一致。
- **L1 天空：** 暖色黄昏，大块平涂的云带，没有任何地面物体。不透明。
- **L2 远景城：** 地平线位于画面高度约 58%。远处是废墟般的白色城市，有巨大的拱门、长桥和尖塔，太阳在拱门里。地平线以上透明，以下是平静的水面倒影。
- **L3 中景：** 左侧一座残破的巨大拱形钢架，或者实验室遗迹框架，占画面左侧约 30%。其余透明。
- **L4 前景：** 左下角是悬崖或平台的边缘。她站在边缘，背对镜头望向远城，身高约占画面高度 15%，头发和红色发带向右飘。其余透明。
- **L4 的附加要求：** 人物和平台最好能分开。如果分不开，至少人物的轮廓要清楚。
- **提示词（各层）：** `layer N of a 4-layer parallax set, identical canvas size and horizon line at 58% height…`（每一层再接上对应的描述）

#### #5 起跑 `dash_launch.png`（P0，透明底）

- **用途：** 15.1 秒间奏落下的那一拍，闪入 2–4 帧。
- **构图：** 全身侧面，面朝右，低身起跑姿态，像短跑运动员蹬出那一刻。背后和脚部的推进器喷出青色光。头发和发带向后拉直。全身在画面中占约 70% 高度。
- **提示词：** `full-body side view facing right, explosive sprint-start / launch pose, low and coiled, boosters on back and legs flaring cyan, hair and ribbon streaming straight back, transparent background`

#### #6 全速 `dash_full.png`（P0，透明底）

- **用途：** 18.8 秒冲破音障的强拍，以及 20.6 秒 "rivals light"。
- **构图：** 面朝右的水平高速冲刺，或贴地飞行，身体前倾约 30°，一只手向前伸。表情专注，嘴角带一点得意（她的台词是"Catch me if you can!"）。
- **提示词：** `full-body side view facing right, flying / dashing horizontally at extreme speed, body leaning forward ~30°, one arm reaching ahead, focused face with a confident little smirk, transparent background (no motion blur — I add it in code)`

#### #7a / #7b 指尖与红线：差一点 / 系上（P0，成对）

- **用途：** #7a 用在 22.5–28 秒"碰不到"；#7b 用在 55.7–57.6 秒 "unite"。
- **#7a `hand_gap.png`：** 沿用旧图的构图，因为代码已经按这个构图写好了。深色纸底 `#14100D`，带干笔刷痕。她的机械右手从左下伸向右上，食指伸直，指尖位于约（68%，18%）处。一根红线从右上角垂下，线头停在指尖右边，间隙约为画面宽度的 2–3%，两者绝对不接触。
- **#7b `hand_tied.png`：** 在 #7a 上局部编辑，只改红线：红线在食指第一节上绕两圈，打一个小结，余下的线头向右上延伸出画。手的姿态完全不动。
- **提示词（7a）：** `her mechanical right hand reaching from bottom-left toward top-right, index finger extended, fingertip at ~(68%,18%); a single red thread hangs from the top-right corner and ends just to the right of the fingertip with a small clear gap (~2-3% of frame width), never touching; dark ink-paper background with dry-brush strokes`
- **提示词（7b，编辑）：** `same image, only change: the red thread now wraps twice around the first segment of the index finger and is tied in a small knot, loose end continuing to the top-right; hand unchanged`

#### #8 正脸胸像 `portrait_front.png`（P0）

- **用途：** 29.9–31.7 秒，由点云聚成她的脸；副歌也可能复用。
- **构图：** 胸像，3/4 侧到正面之间，看向镜头，神情平静，带一点点好奇。脸的中心位于约（50%，42%）。
- **要求：** 明暗对比清楚，线条干净，因为代码要按亮度采样成点，糊的地方会散成一团。
- **背景：** 纯纸色底，或透明底。

#### #9 倒悬漂浮 `floating.png`（P1，透明底）

- **用途：** 49.7–52 秒 "so dizzy"。
- **构图：** 她在虚空中倒悬或翻滚漂浮，闭眼，头发呈放射状散开，四肢放松。全身居中，四周留足空间，方便我做旋转。
- **提示词：** `floating upside-down / tumbling in a void, eyes closed, hair spread out radially, limbs relaxed, centred with lots of empty space around, transparent background`

#### #10 小指红线 `pinky_promise.png`（P1）

- **用途：** 57.6–59.4 秒 "so deeply"，作为 unite 之后的情感落点。
- **构图：** 两只手在画面中央勾着小指：左边是她的机械手（黑色分节，掌心有微微的青光），右边是一只人类的手（成年人，袖口是白大褂，暗示"造她的人"，也就是歌里的 you）。红线绕在两根小指上。背景是暖纸色，留白要多。
- **提示词：** `close-up of two hands linking pinkies at centre: left is her black segmented mechanical hand with a faint cyan glow, right is an adult human hand with a white lab-coat cuff; a red thread wrapped around both little fingers; warm paper background, lots of negative space`

### 生图优先级

- **P0：** #0、#1、#2、#3a、#3b、#4 的四层、#5、#6、#7a、#7b、#8，共 14 张。有了这些，前一分钟就能完整做出来。
- **P1：** #9、#10。没有也能做：dizzy 用纯矢量螺旋，so deeply 用绳结推进画面。

## 五、执行顺序

1. **现在就能做（不用等图）：** 修改第二节表里不需要新图的项（Simulation、HUD、Zeno 节奏）；把 30–60 秒的矢量镜头全部做出来，需要新图的位置先用旧图或灰色占位。
2. **图到位以后：** 抠图并检查成对图是否对齐，然后换进片中，重渲 0–60 秒。
3. **交付：**
   - 先交 30–60 秒草稿，包含已经能用的图；
   - 再交整一分钟的精修版；
   - 最后附每 0.25 秒一帧的拼图和卡点数据。

生图期间你不用等我，我会先推进第 1 步。哪张图出来，放进 `gen\` 文件夹，我检查对齐和画风；不合格的会写清楚哪里不对，方便你让 GPT 重出。
