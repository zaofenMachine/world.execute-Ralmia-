# 项目上下文交接文档 —— world.execute(me); × 洛菈米亚 MV

最后更新：2026-10-16。这份文档写给接手这个项目的人或 AI。读完它，再读 `ClaudeVer/plan_0-60s.md`，就能无缝继续工作。

---

## 0. 换到新机器后先做这几件事

1. 把整个 `D:\Project\MV` 文件夹拷到新机器，路径不必相同，代码全部使用相对路径。
2. 安装 Python 3.10 或更高版本，以及 ffmpeg，并确保 ffmpeg 已加入 PATH。然后执行：
   ```
   cd ClaudeVer\project
   pip install numpy opencv-python pycairo uharfbuzz fonttools
   python render.py still test.jpg 1.6,6.9,19.9 0.25 3
   ```
   能生成 `test.jpg`，说明渲染环境正常。
3. 读本文第 1 节（用户偏好）和第 10 节（下一步）。
4. 检查 `ClaudeVer\gen\` 里有没有 GPT 生成好的新图，规格见 `plan_0-60s.md` 第四节。

---

## 1. 项目和用户

- **用户：** linfeng。他让多个 AI 智能体分别制作同一首歌的 MV，然后比较它们的审美和能力。
- **歌曲：** Mili 的《world.execute(me);》，时长 3:32，文件在 `Audio/`。
- **角色：** 《影之诗》（Shadowverse）里的洛菈米亚。官方英文名是 **Ralmia**，日文 ララミア；中文玩家圈也写作"洛菈米亚"。用户写的是"洛拉米亚"，指的是同一个角色。"Loramia"不是官方译名。
- **当前任务线：** "Claude 版"（ClaudeVer）。用户明确要求：**不要参照 Astra 版本，也不要沿用用户给 Astra 版提过的要求，要发挥自己的审美和对歌曲的理解**，并结合角色设定。Astra 版的图片可以复用，也可以全部推翻重新生成。
- **用户的工作方式和偏好：**
  - 喜欢先看计划，再执行。
  - 会让 GPT 帮忙生成图片，所以需要列出详细的生图规格。
  - 重视审美判断，以及有数据支撑、有时间点的具体自评。
  - 用中文交流。
  - 交付节奏：每轮做一段（先做前 30 秒），然后整体打磨前一分钟。
  - 用户曾经批评过别的版本的问题，这些也是通用的审美底线：画面太静、整图平移或旋转、歌词当字幕放、用重复元素敷衍、AI 味重、画面不卡节拍。
- **AI 环境的教训：** 中间文件必须放在用户能看到的目录里。之前放在临时目录，用户找不到。

---

## 2. 历史时间线

| 日期 | 事件 | 产物 |
|---|---|---|
| 2026-10-15 | 评审 ChatGPT dot 制作的 Astra 版（`AstraVer/world_execute_me_complete.mp4`）。结论：用户调过的前一分钟不错；放养的后段大幅退化，54 秒画面冻结、歌词字幕化、人物缺席；两段都不卡拍 | `review/MV评审.md`、`review/overview.png`、`review/beat_grid_130bpm.csv`、`review/sheets/` |
| 2026-10-15 | Claude 版前 30 秒完成：1080p，60 帧 | `ClaudeVer/world_execute_me_Ralmia_0-30s.mp4`（约 70MB，18Mbps） |
| 2026-10-16 | 写出前一分钟的完善计划和 16 张生图需求，交给用户转 GPT 生成 | `ClaudeVer/plan_0-60s.md`，空文件夹 `ClaudeVer/gen/` |
| 2026-10-16 | 整理工程，使其可迁移，并写本文档 | `ClaudeVer/project/`、`CONTEXT.md` |
| 2026-10-16 | 工程迁到 `F:\Project\world.execute-Ralmia-`。做完 A 线：Simulation 改 2×2→4×4 渲染阶段、Zeno 第 56 拍半拍全停 + 红线颤动、HUD 日志避让大字；30–60 秒 12 个矢量镜头（`scenes3.py`）。出 0–60 秒草稿 | `ClaudeVer/world_execute_me_Ralmia_0-60s_draft.mp4`（59.42 秒，18Mbps） |
| 2026-10-16 | GPT 的 16 张图已放进 `ClaudeVer/gen/`（附 README 和 `_qa/`）。成对图已复核：差异只在眼睛横带 / 红线区域内 | — |
| 2026-10-16 | B 线完成：16 张新图全部接入（`prep3.py` → `assets/n_*`），Astra 旧图已全部退出成片。精修版 0–59.41 秒 | `ClaudeVer/world_execute_me_Ralmia_0-60s.mp4`（18Mbps）、`project/out.mp4`（crf14 母版） |
| 2026-10-16 | 用户确认：线稿加深可以；零件密度合适；15.1 / 18.8 秒冲刺闪入压住了拍。写出全片计划和第二批生图需求 | `ClaudeVer/plan_full.md` |
| 2026-10-16 | 第一轮（第二幕）完成：副歌 1、主歌 2 标本卡、切换段，第二批图未到，全部用占位；同时把 HUD 日志换成原程序 GodDrinksJava 的行，54 秒年份尺改成 617 A.D. / 3691 B.C. | `ClaudeVer/world_execute_me_Ralmia_0-104s_round1.mp4`（0–103.72 秒） |

**第二批图（21 张）已到并审核完（`gen/README_round2.md`、`gen/feedback_round2.md`）：** 只有 back_reach 要重出（读起来像挥手）；listen_profile、reach_camera 的宝石画到了左太阳穴，接入时水平翻转；夜空自带月亮，要删掉 scenes4 里代码画的月亮。

**最新（2026-10-17，第四轮计划）：** 见 `ClaudeVer/plan_round4.md`。
- 用户指出 12 声 EXECUTION 从约 148 秒才开始。133.3–147.6 秒（k288–319）其实是无人声的间奏；12 声暂定在 k319–324.5、按八分音符排，**起止时间等用户亲耳确认**。
- 133–148 秒改成她的第一人称视角走廊，画面里不出现她。
- 猫卡换成猫娘化的她（#27），S/M 改成她在抖S / 抖M 两种性格间切换（#28a/b，只做表情梗，不要任何道具）。生图需求见 `gen/request_round3.md`，原来请求的 run_front_b 已撤回。

**当前状态（2026-10-17）：** 0–162.8 秒第三版已交付（`ClaudeVer/world_execute_me_Ralmia_0-163s_round3.mp4`）。第二幕的占位已全部换成新图，用户提的 4 条意见和我自己列的弱点都改了。下一轮做第五、六幕（162.8 秒到结尾）。可选的生图需求见 `gen/request_round3.md`（run_front 的另一步）。

**这一轮的设计决定：**
- **亮暗：** 保留暖纸和墨黑两种底，但规定为"纸 = 她造出来、手绘的世界，墨 = 系统 / 运行"。同一段里不再来回切：主歌 2 前三张标本卡统一用纸底，只有"神"那张是墨底；trance 不再做反相，而是漂白成纸色，再接 VIBRATIONS 的纸底。
- **切线：** "you" 在 84.5–88 拍内从右到左连续滑过波形，每拍轻跳一下。
- **67–70 秒：** 她先以线稿浮起，按 RUN 时颜色从掌心向外铺开，掌心核心随拍发光。
- **133–144 秒：** 改成迎面纵深的"世界走廊"，她用 run_front 冲向镜头（带残影），两侧是死掉的窗口，每声 EXECUTION 处决正在擦身而过的那个世界。
- **其他：** 主歌 2 的"神"直接用 creation_inverse，沿指缝切开再在 k189 合拢；副歌 1 他的桌前那段，模拟画面直接放进三块显示器里（遮罩是 `n_lab_screens`）。

第三、四幕的拍号（Whisper small + 提示词 + 人声能量对照）：
- VIBRATIONS k229.5、COMPLETION k238.25；
- "you have left" ×6：k240 / 242.5 / 244.5 / 246.25 / 248.5 / 250.5；
- ISOLATION k253、FRAGMENTS k262.75、DISHEARTENED k270.5、ILLEGAL k283、ARGUMENTS k285；
- 12 声 EXECUTION 暂定每 2 拍一声（k288–310），**未能自动识别，需要人耳确认**；
- 报数 EINS…六 在 k325.5 起每 0.75 拍一个，第 13 声 EXECUTION 在 k330。

新文件：
- `scenes5.py`：s_chorus2 / s_bridge；
- `scenes6.py`：s_executions / s_count；
- `prep5.py`：第二批图 → `assets/n_*`，listen / reach 已翻转；另外生成拼图碎片 `frag_*.png`，以及去掉垂线的 `n_pinky_alone_clean`；
- `fonts/NotoSerifCJK-Bold-subset.ttf`：只含 넷、六（OFL），在 `lib.fonts()` 里的键是 `'cjk'`。

**用户对人设的最终纠正（写在 gen/README.md 里）：** 她是**长发**、戴**红色领结**（音速版白裙装甲），优先于 plan 里的"齐肩发"和"红色只给红线"。所以接入新图后，红色不再是红线独占，代码里的红色仍只用于红线 / touch / 音障，但画面里会出现她的红领结。

---

## 3. 目录结构

```
D:\Project\MV\
├─ CONTEXT.md                      ← 本文档
├─ Audio\Mili - world.execute (me) ;.mp3      原曲（211.97 秒）
├─ AstraVer\
│   ├─ world_execute_me_complete.mp4          dot 做的 Astra 版成片（参考和对比用）
│   └─ Images\                                Astra 版图片（7 张 PNG，1672×941，暖纸色手绘风）
│       ├─ originals_verified\  eye_closed_A / eye_open_B / hand_creation_D2 / world_open_F
│       ├─ originals_candidates\ hand_gap_C2 / hand_near_C3 / world_unfinished_F0
│       └─ README.txt, manifest.json, preview.jpg
├─ review\                         对 Astra 版的评审报告和数据
└─ ClaudeVer\
    ├─ world_execute_me_Ralmia_0-30s.mp4      Claude 版 0–30 秒成片
    ├─ plan_0-60s.md                          前一分钟计划 + 第一批生图规格
    ├─ plan_full.md                           59.4 秒至结尾的完整计划、全曲结构表、对第一批图的反馈、第二批生图清单（#0b、#11–#26）（必读）
    ├─ gen\                                   放 GPT 生成的新图（目前为空）
    └─ project\                               工程（源码 + 素材 + 数据）
        ├─ lib.py        工具库：节拍、调色板、缓动、字形文字、描边动画、图片、纸纹
        ├─ scenes.py     镜头 S1–S4 + HUD
        ├─ scenes2.py    镜头 S5–S8 + 间奏 I1–I8
        ├─ scenes3.py    30–59.41 秒镜头 S9–S20（points → so deeply），文件开头有歌词时间表 K_* 和 LY
        ├─ prep2.py      旧图的额外素材（world_open_F_flat、hand_gap_C2_clean、thread_C2.json）；B 线后成片已不再使用
        ├─ scenes4.py    第二幕 59.41–103.72 秒：s_chorus1 / s_verse2 / s_switch，以及窗口缩略图缓存 thumb()、win()、her()、creator() 剪影等工具
        ├─ codelog.py    HUD 日志 = 原程序 GodDrinksJava 的逐行代码（自写的行用 // 注释），scenes3 会用它替换 LOG
        ├─ prep4.py      第一轮占位：n_her_front（从设定图抠出的正面全身）、n_wL1_night / n_wL2_night（程序生成的夜晚）
        ├─ prep3.py      新图（gen/）→ assets/n_<名>_full/_line/_hd（1672×941 放大到 1920×1080，透明图保留 alpha；_hd = 原图乘 25% 线稿再略加暖）；另出 n_hand_gap_clean + thread_gap.json、n_parts_0..13 + parts.json、n_world_hd/_line/_flat（四层合成）
        ├─ words_29.json 29–61 秒 Whisper 逐词时间
        ├─ render.py     时间线、合成（辉光、色差、闪白、暗角、颗粒）、编码、出单帧
        ├─ mux.py        拼接分段 + 混入原曲音频 + 淡出 → out.mp4 / out_delivery.mp4
        ├─ qa.py         自查：每 0.25 秒一帧的拼图 + 硬切卡点统计 + 冻结段检测
        ├─ prep.py       把 Astra 的图处理成 1920×1080 的 _full / _line（XDoG 线稿）/ _hd（线稿+平涂）
        ├─ make_fonts.py 把可变字体实例化成静态字重（会去除重叠轮廓）
        ├─ make_words.py 用 Whisper 生成逐词歌词时间戳
        ├─ beats.py      用 Beat This! 做节拍检测
        ├─ beats.json / words.json   节拍数据，以及 0–34 秒的逐词歌词
        ├─ fonts\        Big Shoulders Display（可变字体原件 + BSD-900/700/300）、IBM Plex Mono（Light/Regular/Medium）、Instrument Serif（Italic/Regular），全部是 OFL 授权
        ├─ assets\       prep.py 的输出（7 张图 × 3 个版本）
        ├─ qa\           上一版的自查拼图
        ├─ requirements.txt, README.md
        └─ mux.sh        已废弃（沙盒里删不掉，可以手动删除）
```

**没有拷过来的东西：** 6 个分段 mp4（合计约 400MB）和无损母版（约 400MB）都留在旧会话的临时目录里，不用管。用源码重新渲染就能得到，见第 4 节。

---

## 4. 环境与运行

**必需依赖：** numpy、opencv-python、pycairo、uharfbuzz、fonttools，以及在 PATH 里的 ffmpeg。

**可选依赖：**
- skia-pathops：只有重新执行 `make_fonts.py` 时才需要。
- librosa、soundfile、faster-whisper、torch（CPU 版）、beat_this（`pip install git+https://github.com/CPJKU/beat_this.git`）：用来重做音频分析。

**常用命令（都在 `ClaudeVer/project` 里执行）：**

```
python render.py still preview.jpg 1.5,3.6,10.9,19.9 0.25 4
```
出单帧拼图。参数依次是：时间点、缩放比例、列数。

```
python render.py enc 0 5 chunks/c0.mp4
```
渲染一段。区间是左闭右开，用帧号对齐，所以分段之间可以无缝拼接。

上一版用了 6 段：0–5、5–10、10–15、15–20、20–25、25–30.45 秒。各段可以多开几个进程并行渲染。

```
python mux.py 59.41              # 普通 PC：一次做完 master + delivery
python mux.py 59.41 master       # 只拼 out.mp4（流复制，快）
python mux.py 59.41 dchunk 3     # 把 chunks/c3.mp4 转成 18Mbps 的 chunks/d3.mp4，可多进程并行
python mux.py 59.41 deliver      # 拼 chunks/d*.mp4 + 音频 → out_delivery.mp4
```
拼接 `chunks/c*.mp4`，混入原曲，最后 0.4 秒淡出。`out.mp4` 是 crf14 母版（0–60 秒约 800MB），`out_delivery.mp4` 是 18Mbps 交付版。0–60 秒用 12 段：0–5、5–10 … 50–55、55–59.41（结束时间 = `scenes3.END2`）。

```
python qa.py out_delivery.mp4
```
自查：生成拼图 `qa/q*.jpg`，并打印卡点统计和冻结段。

**渲染速度参考：** 在旧环境（2 核虚拟机）里，单进程约每帧 0.13 秒，30 秒的片子约 4 分钟（两个进程并行时）。普通 PC 会更快。

**Windows 注意事项：**
- 如果 pycairo 的 pip 安装失败，可以用 conda：`conda install -c conda-forge pycairo`。
- 路径里有空格和分号（音频文件名），mux.py 已经处理好。

---

## 5. 音乐数据（重要，所有卡点都基于这些数据）

- **速度：** BPM 130，非常稳定，全曲没有漂移。
- **节拍公式：** `t(k) = 0.34 + k × 60/130`，也就是 `0.34 + 0.461538·k` 秒。代码里写作 `B(k)`，k 可以是小数：k+0.25 是十六分音符，k+0.125 是三十二分音符。
- **强拍：** 每 4 拍一个（k 是 4 的倍数），一小节长 1.846 秒。
- **军鼓：** 15 秒以后，军鼓（高频能量峰）落在每小节的第 2 拍和第 4 拍，也就是 k 为奇数的位置。
- **结构：**
  - 0–14.2 秒：主歌，伴奏稀疏。
  - 14.19 秒（k30）：低频骤停，是 drop 前的空拍。
  - 15.11 秒（k32）：间奏全力进入，持续到 29.88 秒（k64）。
  - 28.96–29.42 秒：fill 过门上扬。
  - 29.88 秒：低频收住，人声在 30.0 秒回来。
- **0–15 秒逐词时间：** 来自 Whisper，已经对照节拍网格校正过，存在 `words.json`。
  - Switch 0.00 / on 0.58 / the 1.04 / **power 1.24** / line 1.46
  - Remember 2.28 / to 2.34 / put 2.78 / on 3.02 / **protection 3.30**
  - Lay 4.18 / down 4.24 / your 4.70 / **pieces 4.92**
  - and 5.34 / let's 5.80 / begin 6.10 / **object 6.44** / **creation 6.84**
  - Fill 7.86 / in 7.94 / my 8.36 / **data 8.60** / **parameters 8.98–10.1**
  - **Initialization 10.52–11.08**
  - Set 11.56 / up 11.58 / our 12.06 / new 12.32 / **world 12.52**
  - and 12.90 / let's 13.16 / begin 13.44 / the 13.84 / **simulation 14.10–14.88**
- **30–60 秒（近似值，来自对 Astra 视频音轨的识别）：**
  - points 31.1 / dimension 32.9
  - circle 34.5 / circumference 36.5
  - sine 38.2 / tangents 40.3
  - infinity 41.6 / limitation 43.7
  - current 45.4 / AC ≈46 / DC ≈47
  - vision 49.1 / dizzy ≈49.6–51.6
  - travel 52.8 / A.D. 53.8 / B.C. ≈54.8
  - unite 56.4 / deeply ≈57.5–59.2
  - 副歌 "If I can" 从 ≈59.3 开始

  **已执行 `make_words.py 29 32`，定稿的关键词拍号（k）在 `scenes3.py` 开头：** points 66.5 / dimension 70.5 / circle 74 / circumference 78.25 / sine 82 / tangents 87 / infinity 89.5 / limitation 94 / Switch 95 / current 97.5 / AC 100 / DC 102 / blind 103.5 / vision 105.5 / so 107 / dizzy 108 / so 109.5 / dizzy 110 / travel 113.5 / A.D. 116 / B.C. 118 / unite 121.5 / so 123 / deeply 124 / so 125 / deeply 126 / 副歌 "If I can" 起于 k127.5，第一个强拍 k128 = 59.41 秒。Whisper 把若干词听错（sit→settle、tangents→entrance、blind→combine、dizzy→they'll see），时间可信、词以歌词为准。
- **各小节的强拍时间（30–60 秒）：** 31.72、33.57、35.42、37.26、39.11、40.95、42.80、44.64、46.49、48.34、50.18、52.03、53.88、55.72、57.57、59.41。

---

## 6. 角色设定调研（Ralmia / 洛菈米亚）

**来源：**
- Shadowverse Fandom Wiki 的 Ralmia、Ralmia Sonic Racer、Ralmia Astrowing、Supersonic Breakthrough 词条；
- GameWith 和旅法师营地的中日文攻略。

**已确认的设定：**
- 外表是金发碧眼的少女，本体是"最快的机构"。种族是机械（Machina）加造物（Artifact），职业是复仇者（Portalcraft / ネメシス）。
- 卡牌：
  - 初版「音速の機構・ララミア」（Sonic Racer）：收录于「ナテラ崩壊」（World Uprooted）卡包，画师 Ponzu。
  - 重制版「アストロウィング・ララミア」（Astrowing）：收录于「十禍闘争」（Omen of Storms）卡包，画师 ko-yahu。
  - 《Shadowverse: Worlds Beyond》里的「ブーストエクステンド・ララミア」。
- 她的操作系统叫 **Ōmeteōtl**，是阿兹特克神话里的二元创世神。台词："Activating Ōmeteōtl. All systems, stand by."
- **废弃实验室笔记**（Sonic Racer 的背景文字）："Thanks to the quick progress of technology… She is swifter than sound and rivals light… Nothing, not one thing, can touch her."
- 和"破坏之绝杰"里榭娜（Lishenna）交手后，她突破了音速。进化后台词："I realized it's better to run with the melody than from it. Music actually pushes me forward—faster! … swifter than light!"
- Astrowing 版台词："The Trial of Destruction isn't in my task list … Catch me if you can!"
- 日文配音是佐藤利奈。

**还没有确认的：** 官方卡图的具体服装我没有亲眼看过（日文百科被 Cloudflare 拦截了）。生图规格里写的是"服装以官方卡图为准"，需要生图方自己查。Astra 版图片里的造型（右太阳穴的青色宝石、黑色分节机械手、掌心核心）是 dot 自己的设计，不一定是官方造型。

---

## 7. 美术系统（Claude 版）

- **概念：** 代码（墨黑底，运行）对造物（暖纸底，手绘），这组二元对立呼应 Ōmeteōtl 这位二元神。叙事是：她被"启动并构建"出来 → 她的本性是速度 → 她碰不到任何东西。
- **调色板**（定义在 `lib.py`）：

| 名字 | 色值 | 用途 |
|---|---|---|
| INK | `#080b10` | 暗场底色 |
| INK2 | `#121822` | 暗场中的次级面 |
| BONE | `#efe8d8` | 暗场里的主文字和线条 |
| PAPER | `#efe6d2` | 纸场底色 |
| SEPIA | `#2a2420` | 纸场里的文字和线条 |
| CYAN | `#62d8ea` | **只用于**她的核心、系统、能量 |
| RED | `#e5484d` | **只用于**红线、touch: null、音障 |
| GREY | `#6b7480` | 次要信息 |

- **字体分工：**

| 代码里的键名 | 字体 | 用途 |
|---|---|---|
| `heavy`（BSD-900） | Big Shoulders Display 900 | 冲击性的关键词 |
| `bold`（BSD-700） | Big Shoulders Display 700 | 次级标题，如 PARAMETERS、INITIALIZATION |
| `thin`（BSD-300） | Big Shoulders Display 300 | 细体，如 OBJECT、SPEED OF SOUND |
| `mono` / `monom` / `monol` | IBM Plex Mono | 代码、标注、数值 |
| `serif` | Instrument Serif Italic | 歌词里的"人声连接词"，如 Switch on the、Remember to put on |

- **HUD**（`scenes.py` 里的 `hud()`）：
  - 四角有细线定位标记。
  - 左上角：`ŌMETEŌTL RALMIA / MACHINA`，下面是 3 行启动日志，按歌词逐行打出，对应 `LOG` 列表。
  - 右上角：时间码，加 4 个节拍方块，当前拍会亮起，强拍是青色。
  - 底部保持干净。
- **后期**（`render.py` 里的 `composite()`）：
  - 场景同时画两层：主层 `c`，以及半分辨率的辉光层 `g`。要发光的元素在 `g` 上再画一遍，合成时模糊后叠加上去。
  - 场景函数返回一个 fx 字典，可用的键：
    - `glow`：辉光强度系数；
    - `ab`：色差位移，单位是像素；
    - `flash`：闪白，取值 0–1；
    - `vig`：暗角强度，纸场用 0.4；
    - `grain`：颗粒。
- **图片处理**（`prep.py`）：
  - `_line`：XDoG 线稿，用于"线稿阶段"，以 MULTIPLY 模式叠加。
  - `_hd`：mean-shift 平涂乘以线稿，做出手绘的赛璐珞质感，减少 AI 味。成片里用的都是这个版本。

---

## 8. 0–30 秒分镜和代码对照

| 区间 | 函数 | 内容 | 用到的图 |
|---|---|---|---|
| 0–B4（0–2.19 秒） | `scenes.s_power` | 光标拉成电力线，带标尺刻度，电流脉冲在第 1、2、3、3.5 拍跑过。"Switch on the" 先大字居中，POWER 落下时缩到左上角。POWER 每个字母按三十二分音符落下，被电流"充电"点亮。电源键在第 2.5 拍画出、第 3 拍点亮，并放出冲击环。L·I·N·E 字母铺在线上 | 无 |
| B4–B8 | `scenes.s_protect` | 蜂窝格子按环从中心向外出现。第 6 拍（protection）护盾波纹扩散、圆框画出，PROTECTION 字母从中心向两侧出现。第 7 拍方括号合拢，显示 INTEGRITY 100% | 无 |
| B8–B12 | `scenes.s_pieces` | 纸底点阵加 6 个虚线格。P-I-E-C-E-S 每半拍落下一个，带旋转、挤压回弹、硬投影和落地标记。第 11 拍整体轻压一下 | 无 |
| B12–B16 | `scenes.s_object` | 第 12 拍画辅助线、点阵逐点出现；第 13 拍青色扫描线扫出线稿；第 14 拍从核心向外圆形扩散上色；第 15 拍核心发光。标注 core / ŌMETEŌTL。OBJECT（细体）逐字打出，CREATION 先描边、第 15 拍填实 | hand_creation_D2 |
| B16–B21 | `scenes2.s_data` | DATA 先描出轮廓，内部滚动二进制字符，第 17–18 拍按 8 级阶梯灌满，第 18 拍闪光，第 20 拍横切故障。右侧是参数表：开始时是空白表单，第 18.7 拍 PARAMETERS 解码出现，第 19 拍起逐行填写 name / class / os / speed / **touch null（红色）** | 无 |
| B21–B24 | `scenes2.s_init` | 只露一条缝的闭眼特写。INITIALIZATION 从第 22 拍开始乱码解码，每个字母 0.031 秒。下方进度条分 8 级走到第 23 拍，此时睁眼（交叉溶解，虹膜处有青色环），然后缝隙张开到全屏 | eye_closed_A、eye_open_B |
| B24–B28 | `scenes2.s_world` | 从消失点画出透视线；世界切成 24 根竖条，从离太阳最近的开始依次升起；第 26 拍从太阳处圆形扩散补全世界，太阳辉光。"Set up our new" 的字落在天空，WORLD 叠在右下的水面上（MULTIPLY 墨色） | world_unfinished_F0、world_open_F |
| B28–B32 | `scenes2.s_sim` | 世界缩进一个窗口（带标题栏），第 29 拍变成 3×3，第 30 拍变成 7×7（部分窗口染色或闪烁），SIMULATION 逐字出现。第 31 拍像老电视一样关机：先压成一条线，再缩成一个点 | world_open_F 等 |
| B32–B36 | `scenes2.s_velocity` | 第 32 拍闪白。放射状星流，速度随拍加快。中央是速度读数，在第 32/33/34/35/35.5 拍跳为 0 / 85 / 170 / 255 / 340.29。SPEED OF SOUND | 无 |
| B36–B40 | `scenes2.s_doppler` | 多普勒效应：每个十六分音符发出一圈声波，拍上的那圈是青色、加粗；声源加速到 M=1。显示 SOUND BARRIER 和大号读数 M x.xx | 无 |
| B40–B48 | `scenes2.s_mach` | 第 40 拍音爆（闪白、冲击环、色差）。马赫锥：M 在第 40–47 拍依次为 1.25 / 2 / 3 / 5 / 8 / 14 / 30 / 80，锥角越来越窄。SWIFTER / THAN / SOUND 在第 40/41/42 拍砸进来；第 44 拍起光速横条纹出现，RIVALS（第 44 拍）、LIGHT（第 46 拍），读数 c 计到 299 792 458。第 47–48 拍整体白化 | 无 |
| B48–B52 | `scenes2.s_gap` | 从白场里浮出伸手图，缓慢推进，并平移到构图位置。第 49 拍出现尺寸标注 d，第 50 拍显示 "d -> 0"。右下角 "Nothing, not one thing," 逐词出现 | hand_gap_C2 |
| B52–B58 | `scenes2.s_zeno` | 矢量版的芝诺悖论：每拍前半拍间隙缩小一半，后半拍画面放大一倍，所以间隙看上去不变，d 一直在减半。手指是带剖面线、分节和铆钉的机械指节，加红线和分形网格。右下角 "can touch her." | 无 |
| B58–B60 | `scenes2.s_near` | 从 9 倍放大快速拉回到手部近景，显示 d != 0，右侧是整句引文和来源 | hand_near_C3 |
| B60–30.45 秒 | `scenes2.s_title` | 按三十二分音符逐字打出 `world.execute(me);`，带语法高亮（me 是红色），加光标；第 62.3 拍起字符开始抖动、辉光增强；第 64 拍（29.88 秒）"回车"，整行炸成约 4600 个点，承接 30 秒的 "If I'm a set of points" | 无 |

**上一版的自查数据：**
- 57 个硬事件，与八分音符网格的偏差中位数为 17.7 毫秒，63% 在 35 毫秒以内。没对上的都是连续动画，比如 22 秒左右的光速条纹。
- 没有超过 1.3 秒的冻结画面。

---

## 9. 代码约定和坑

- **场景函数签名：** `fn(c, g, t) -> fx`。其中 `c` 是主画布，`g` 是辉光画布（已经做过 0.5 倍缩放，可以直接用 1920×1080 坐标画），`t` 是全局时间（秒）。新增场景时，在 `render.py` 的 `TIMELINE` 里加一行。
- **时间都用 `B(k)` 表示**，不要写死秒数；只有歌词的逐词时间直接用秒。
- **常用工具函数：**

| 函数 | 作用 |
|---|---|
| `prog(t, a, b)` | 把 t 在区间 [a, b] 内的进度映射到 0–1 |
| `eo_cubic` / `eo_expo` / `eo_back` / `eio_cubic` / `ei_cubic` | 缓动曲线 |
| `pulse(t, at, dur)` | 从时刻 at 开始衰减的脉冲 |
| `words(...)` | 逐词出现的一行字 |
| `text(c, key, s, x, y, size, col, a, align, track)` | 写一行文字 |
| `fonts()[key].glyphs(...)` | 逐字形布局，用于逐字动画 |
| `glyph_path(...)` | 把单个字形加入路径 |
| `partial_stroke(c, frac)` | 只描当前路径的一部分，用于描边生长动画 |
| `scramble(...)` | 乱码解码效果 |
| `type_on(...)` | 打字机效果 |
| `draw_img(...)` / `surf(name)` | 读取 `assets/<name>.png` 并绘制 |
| `paper_bg` / `dotgrid` | 纸纹背景、点阵 |

- **已经踩过的坑：**
  1. 可变字体实例化后，W 之类的字母会有重叠轮廓导致的镂空。必须用 `OverlapMode.REMOVE`，这一步需要 skia-pathops。
  2. 对空字符串做 harfbuzz 排版会返回 None，已经在 `Font.shape` 里处理过。
  3. 把图片缩放、平移后，要检查它是否还盖满画面。之前出现过眼睛特写和手部近景露出黑边的情况。计算方法：在 x 和 y 两个方向上都要满足 `tx - ex·sc ≤ 0` 且 `tx + (W - ex)·sc ≥ W`，其中 tx 是图片锚点在屏幕上的位置，ex 是锚点在图片里的坐标，sc 是缩放比例，y 方向同理。
  4. BONE 色的字放在浅色小窗上会看不见。字的位置要避开浅色区域，或者给字加深色描边。
  5. HUD 的日志会压到左上角的大字（比如 SWIFTER），待修。
  6. Whisper 对唱歌的识别偶尔会出错，比如把 "points" 后面的词识别成 "emission"、把 "tangents" 识别成 "hydrants"。时间点可以信，词以已知歌词为准。
  7. 交付文件要转成 18Mbps。crf14 的母版大约 400MB，不适合交付。
  8. **IBM Plex Mono 和 Instrument Serif 都没有希腊字母**（β、Δ、θ 会变成缺字）。π、∞、→、·、Ō、° 有。读数里用 `a`、`v/c`、`dt` 代替。
  9. 红色在代码里只给红线 / touch / 音障。旧版 Simulation 小窗用过红色染色，已去掉。
- **本次 AI 环境的限制（2026-10-16，F 盘会话）：**
  - bash 单次调用上限约 180 秒；后台进程随调用结束被杀（bwrap --die-with-parent），所以每次调用并行渲染 2 段 × 5 秒（约 70 秒）。
  - 连接文件夹里不能 `rm`（Operation not permitted），但可以覆盖写。`chunks/`、`video.mp4`、`list_*.txt` 是中间文件，可手动删除。
  - 2 核、3GB 内存；单帧约 0.05–0.12 秒。
- **旧 AI 环境的限制（换机器后多半不存在了）：**
  - bash 单次调用上限约 180 秒，后台进程在调用结束时会被杀掉，所以只能分段渲染；
  - 没有 GPU；
  - HuggingFace 下载偶尔失败；
  - CPU 虚拟化曾经没开，导致虚拟机启动失败。

---

## 10. 下一步

完整计划见 `ClaudeVer/plan_0-60s.md`。要点如下：

**A. 不需要等图的工作：✅ 已完成（2026-10-16）。** 30–60 秒的分镜：

| 拍号 | 函数（scenes3.py） | 内容 | 当前占位图 → 应换的新图 |
|---|---|---|---|
| 64–68 | `s_points` | 标题炸开的点在 65–66 拍聚成她的脸（粉笔线描式点云，虹膜和宝石青色），66 / 67 拍点数翻倍到 18 432，POINTS 点阵字 | eye_open_B → `portrait_front`（改 `FACE_SRC`、`FACE_CYAN`） |
| 68–72 | `s_dimension` | 点逐个塌成一点（0D）→ 线（1D）→ 面（2D）→ 70.5 拍挤出立方体（3D），脸作为 3D 浮雕点云装在里面旋转 | 同上 |
| 72–76 | `s_circle` | 立方体被吸进圆心，圆规作图、半径扫一圈；74 拍切到纸底，从掌心核心拉远露出整只手 | hand_creation_D2 → `hand_palm`（改 `GEM`、`GEM_R`） |
| 76–80 | `s_circum` | 圆按拍滚动、四分之一圈一步把圆周"剥"成 2πr 的线，CIRCUMFERENCE 排在线上；79.4 拍卷回成圆 | 无 |
| 80–88 | `s_sine` | 单位圆转出正弦（波峰落偶数拍），84 拍起切线跳拍、"you" 坐在切线上随波摇；87 拍 44 条切线一起长出来 | 无 |
| 88–95 | `s_infinity` | 曲线逼近渐近线，89.5 拍画 ∞，91 拍 ∞ 飞到渐近线尽头（x→∞），92 拍渐近线变成 "you"，94 拍 LIMITATION 坐在线上 + lim f(x) = you | 无 |
| 95–103 | `s_scope` | 示波器像 CRT 开机（呼应 14.7 秒的关机），CURRENT 骑在波上，AC 字形本身是波，102 拍 DC"啪"地拉平 | 无 |
| 103–106.5 | `s_blind` | DC 那条线张开成眼缝；光圈叶片按拍收缩，颜色抽走只剩线稿，105.5 拍闭眼，VISION 解码后再乱码消失（INITIALIZATION 的镜像） | eye_open_B / eye_closed_A → `eye_open` / `eye_closed`（改 `IRIS`） |
| 106.5–111.5 | `s_dizzy` | 无限缩放的环 + 三臂螺旋，108 / 110 拍方向反转，DIZZY 环形字 | 可加 `floating` |
| 111.5–119 | `s_spacetime` | 光锥图：世界线 113.5 拍贴上光锥（travel），之后越过水平线倒向过去；116 拍 A.D.、118 拍 B.C.，年份尺倒退到公元前 3000 | 无 |
| 119–123 | `s_unite` | 回到 22 秒的手；红线（矢量重画）121 拍碰到指尖，d = 0；121.5 拍绕两圈打结；touch null → true | hand_gap_C2_clean → `hand_gap` / `hand_tied` |
| 123–128 | `s_deeply` | 推进绳结，红线变成电路走线，拉远后是缠着红线的青色核心；126 / 127 拍脉冲沿电路流进核心，128 拍收成一点 | 可加 `pinky_promise` |

**B. 新图接入：✅ 已完成（2026-10-16）。** 每张图用在哪里：

| 图 | 用在 | 锚点（1920 坐标） |
|---|---|---|
| parts_exploded（14 件） | 3.7–5.9 秒 Pieces：字母落在八分音符，12 个零件落在中间的十六分音符，核心宝石最后在 k11 落位并发光 | `parts.json` |
| hand_palm | 5.9–7.7 秒 Object Creation；34.5 秒"圆就是掌心核心" | 核心 (1228, 562)，r≈73 |
| eye_closed / eye_open | 9.7–11.4 秒 INITIALIZATION（睁眼时两个虹膜各有一圈对焦环）；48–49.5 秒 blind my vision（双眼光圈按拍收拢、颜色抽成线稿） | 双眼之间 (965, 538)，虹膜 (546, 540) / (1383, 537)，r≈118 |
| world_L1–L4 | 11.4–13.3 秒 World：天空从上落下（k24.5）→ 远城升起（k25）→ 钢架从左滑入（k25.5）→ 前景和她升起（k26，太阳辉光），之后按深度视差平移 | 地平线 y≈682，太阳 (1246, 574) |
| 四层合成 n_world | 13.3–15 秒 Simulation 的四个渲染阶段 | — |
| dash_launch / dash_full | 15.11 秒（k32）、18.80 秒（k40）各闪 5 帧：原画加拖影 2 帧 → 骨白剪影 2 帧 → 青色轮廓 1 帧 | — |
| hand_gap | 22.5–28 秒 gap / near；55–56.7 秒 unite（用抹掉红线的 clean 版，红线矢量重画） | 指尖 (1314, 190)，线头 (1366, 168) |
| hand_tied | 56.7 秒起矢量绳结交接给原画；57 秒推进绳结 | 绳圈中心 (1247, 230) |
| portrait_front | 30–33.6 秒点云脸、3D 浮雕 | 脸中心 (930, 470)，虹膜 (858, 488) / (1007, 457)，太阳穴宝石 (756, 300) |
| floating | 49.5–52 秒 dizzy，在螺旋中心慢转 | 中心 (961, 552) |
| pinky_promise | 58.95–59.41 秒落点：从矢量核心推进，变成她掌心的核心，再拉出勾小指的整幅画 | 核心 (558, 587)，红线结 (955, 535) |

**下一轮建议：** 59.41 秒的副歌 "If I can, if I can give you all the stimulations" 可以从勾小指画面直接接下去。目前它只停留了 0.46 秒，作为下一段的开头会更从容。

**交付习惯：**
- 成片放在 `ClaudeVer/`，工程放在 `ClaudeVer/project/`。
- 回复里附上自评：做得好的、自己觉得还弱的、需要用户亲耳确认的地方（AI 听不到声音，只能靠节拍数据卡点）。
