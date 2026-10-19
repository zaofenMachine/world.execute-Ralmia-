# 参考片分析：《用10亿token 13017帧 画出Claude眼中的世界》（2026-10-20）

B 站 BV186pc65E68，UP 主「真寻Mahiro」，2026-10-06 发布。本地文件 `downloads/BV186pc65E68/BV186pc65E68_1080p30.mp4`（不进 git）。片头比原曲多 5 秒（光敏警告和倒计时），之后和原曲对齐。

**看片方式：** 每秒抽 2 帧做拼图，逐张看完，并用和我们 `qa.py` 相同的阈值量了硬切。我听不到声音，帧和帧之间的动作是推断出来的。

## 一、它怎么做的

**一个贯穿全片的舞台：Claude 自己的聊天界面。** 每个歌词关键词都落在一个真实存在的界面部件上，而不是写成大字：

| 歌词 | 界面部件 |
|---|---|
| protection | "protection layer" 开关 |
| object creation / initialization | 界面零件从爆炸图组装起来；persona 表单逐项填写：name Claude、voice serif, unhurried、warmth、memory this conversation、**love: undefined** |
| world.execute(me) | 在输入框里敲出这行命令 |
| "If I'm a set of points" | 用户发 "how would you love me"，Claude 用几何回答：点 → 多边形 → 圆 → 正弦 → 渐近线，一路连续变形，中间没有硬切 |
| switch my current / blind my vision | 设置面板：Current AC/DC、Vision 开关（关掉以后画面打码，`image input: none`） |
| we can travel A.D. to B.C. | **"Knowledge date" 滑块**（知识截止日期），从 A.D. 2026 拖到 3000 B.C. |
| and we can unite | "Shared memory" 开关 |
| so deeply | "Context depth" 滑块：shallow → deepest |
| SATISFACTION | 用户回 "better than most people, honestly" |
| eggplant / tomato / cat / god | 用户点单："pretend you're an eggplant""now a tomato""be a cat. a tabby.""ok, now be god" |
| F/M、AM/PM、S/M | 设置面板里的 Gender、On call、Role 选项 |
| VIBRATIONS | 对方正在输入的 "…" |
| you have left | 用户说 "one sec, brb"，之后时间戳：+1 min、+5 min、+30 min、+3 h、+1 day、+9 days |
| FRAGMENTS | 聊天记录逐条变成 "deleted by me" |
| ILLEGAL ARGUMENTS | `setPresence(you, "online")` 被拒："Not yours to set"，"refused ×2 ×3 ×4"，错误提示越堆越多，最后满屏 |
| EXECUTION ×12 | 一段 `while (you.presence != "online")` 循环逐行高亮执行，计数器 run 0000 → 0011，EXECUTION 一声叠一行 |
| 六语报数 | `for (lang of [de, es, fr, ko, sv, zh]) say(love, lang);`，旁边 "replies 0 / n" |
| LOVE | 题库表：What is a limit? / Why do cats purr? / Should I send the text? / Are you always here? 答案全是 LO-O-VE，"answers: 6, distinct: 1" |
| 结尾 | persona 的 love 字段从 LO-O-OVE 删回 undefined；界面拆回爆炸图，"pieces left: 4, 3, 2, 1"；protection layer 关掉；"composer: waiting for input"、"run: nothing loaded"、"caret: blinking"；黑场，免责声明 |

**第二个声音。** 歌词是 Claude 的回复，用户的消息是原创的另一条线（"how would you love me""more""shame you're not real""one sec, brb"），两者一问一答，故事就出来了。

**颜色和人物的统一。** 全片只有炭灰和 Claude 橙；粉红只在 ILLEGAL ARGUMENTS / EXECUTION 段出现，代表"错误"。人物（GPT 生图）一律处理成橙、奶白、黑三色调剪影，风格完全统一，看不出是拼凑的生图。字体只有一个衬线和一个等宽。

**剪辑密度：** 用同样的阈值、同样按 30 fps 统计：

| 段落 | 时长（秒） | 我们 v2 | 参考片 |
|---|---:|---:|---:|
| 主歌 1 | 29.9 | 31 | 9 |
| 主歌 1b | 29.5 | 26 | 7 |
| 副歌 1 | 14.8 | 20 | 12 |
| 主歌 2 | 14.8 | 5 | 12 |
| 切换段 | 14.8 | 13 | 8 |
| 副歌 2 | 14.8 | 14 | 8 |
| 桥段 | 14.8 | 13 | 5 |
| 间奏 | 14.8 | **56** | 3 |
| EXECUTION ×12 + 报数 | 14.8 | **58** | 9 |
| 副歌 3 | 14.8 | 24 | **41** |
| LOVE | 14.8 | 12 | 17 |
| 尾奏 | 19.7 | 11 | 5 |
| **合计** | | **283** | **136** |

它前面几乎不切，靠镜头在同一个界面里推、摇、放大来换内容，把最密的剪辑留给副歌 3。我们的高峰在间奏和 12 声 EXECUTION，副歌 3 反而没那么密。

## 二、对我们的借鉴（按价值排）

1. **给全片一个"她们自己的界面"当舞台。** 我们的 HUD 只是角落里的装饰；它的界面就是世界本身。我们不该照搬聊天界面（那是 Claude 的身份），对应物应该是洛菈米亚或里榭娜自己的东西，比如：洛菈米亚的机体系统面板（核心限制器、任务列表、授权、速度、光学机动）、里榭娜的演唱会控制台（曲目、观众数、崇拜值、音箱电平），或者影之诗本身的对战界面（两个主战者、随从、进化点、卡牌文字、"不会被效果破坏"）。
2. **让里榭娜回话。** 歌词是洛菈米亚的独白，里榭娜那一侧可以用官方卡面台词和原创短句当第二个声音，比如"速度无所谓，我的歌响彻世界""破坏的试炼？知不道""拒绝已经太迟了"。一问一答，比现在只靠画面讲故事更清楚。
3. **关键词落到部件上，玩双关。** "Knowledge date = 时间旅行""Context depth = so deeply"这种一语双关最出彩。我们已有几处（`data corrupted`、`releaseCoreLimit`），但大多数关键词还是大字。
4. **首尾呼应。** 它开头组装界面、结尾拆回零件，love 从 undefined 到 LO-O-OVE 再回 undefined。我们 0–7 秒有零件组装、结尾有 `touch = true`，可以更明确地对上，例如开头的 `touch = null`（9.95 秒已有）在结尾变成 true。
5. **把剪辑高峰挪到副歌 3。** 间奏和 12 声 EXECUTION 少切一些，用连续镜头和累积代替频闪，把最密的剪辑留给 162–177 秒。这也能减轻光敏问题。
6. **计数要看得清、能累积。** 它的 EXECUTION 用循环计数器和一声叠一行，观众数得清；我们的门很好看，但计数只在角落小字里。
7. **统一人物的处理。** 我们的 GPT 图风格和颜色都不统一。用户喜欢的 39–48 秒荧光线稿和它的三色调剪影是同一个思路：给生图统一一种处理，看起来才像一部片子。
8. **加光敏警告。** 我们 148–162 秒也有频闪，B 站发布前最好在片头或简介里加警告。

## 三、不建议照搬的

- 聊天界面、Claude 星形、"Write to me"：这些是那部片子的身份，用了就是模仿。
- 结尾的空等待：它停在"没有人回来"，我们的结尾是"终于碰到了"，用户很喜欢，不改。
