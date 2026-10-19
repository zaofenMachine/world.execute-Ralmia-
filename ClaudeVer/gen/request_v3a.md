# 第八批生图需求：第三版 22.5–28 秒"光速下时间停止"（2026-10-20）

方案见 [`../plan_v3_chase.md`](../plan_v3_chase.md) 方案 A。本批 3 张必须 + 1 张可选。

## 交付规则

沿用前几批：

- 16:9，1672×941，原生分辨率；**透明底 PNG**；
- 不要文字、logo、水印；
- 文件名按下表，放进 `ClaudeVer/gen/`，另写 `README_round8.md`；
- 有里榭娜的附 `lishenna_ref_sheet.png`（服装只用《奏绝》这一版）；有洛菈米亚的附 `ref_sheet.png`。**宝石在她的右太阳穴**：正面看在画面左侧；脸朝右的侧面看得到，脸朝左的看不到；
- 画风参考附 `lishenna_stand.png`、`lishenna_stroll_a.png`、`dash_full.png`。

这几张会被代码转成**线稿 / 点阵**来用，所以**轮廓和主要线条要清楚**，比上色更重要。背景必须干净透明，不要地面、不要特效光。

**分寸：** 穿着完整、平视镜头；不要亲吻，不要身体接触（这一段的意思就是"碰不到"），不要性感化的姿势或镜头。

## 通用段落

```
STYLE: clean anime line art, flat cel shading with soft secondary shadows, slightly warm palette, crisp edges,
matching the attached MV frames. Not the glossy neon card-art rendering. Clear outlines (it will be turned into line art).

RALMIA (exactly as in the attached ref_sheet): long blonde hair with an ahoge, cyan eyes, a cyan gem on her RIGHT temple
(on the LEFT of the image when she faces the viewer; visible when she faces right), white-and-black mechanical suit
with cyan lights, a red neck bow, black mechanical hands with cyan palm cores.

LISHENNA ("Diva" outfit only, exactly as in the attached lishenna_ref_sheet): long coral-pink hair with straight bangs,
blue-violet eyes, black-and-white checkered hairband with two black rabbit-ear-like loops, two floating gold-rimmed
speaker discs with cyan sigils beside her head; oversized white off-the-shoulder jacket with puffy sleeves, sleeveless
white top, cyan neck bow and cyan tie, black high-waisted shorts with suspender straps and the silver buckle, black
thigh-high socks, chunky white sneakers with purple laces. Playful, a little smug.

Fully clothed, eye-level camera. No kissing, no touching. transparent background.
```

## 清单

| 编号 | 文件名 | 优先 | 用在 |
|---|---|---|---|
| V3-1 | `peek_frozen.png` | 必须 | A2（24.6 秒）：两人近景，里榭娜凑近看停住的洛菈米亚 |
| V3-2 | `lishenna_wink.png` | 必须 | A3（25.5 秒）：洛菈米亚的视角，里榭娜对着镜头眨眼 |
| V3-3 | `lishenna_wave_back.png` | 必须 | A4（26.4 秒）：走开，回头挥手 |
| V3-4 | `ralmia_frozen_34.png` | 可选 | A1 / A4：冲刺的 3/4 正面，看得到脸 |

### V3-1：里榭娜凑近看停住的洛菈米亚

**构图：** 胸部以上的两人近景，平视。

- **洛菈米亚在左：** 正侧面，脸朝右，像飞行冲刺时被定格：身体前倾，一只手臂向前伸出画面右下；头发和领结全部笔直地向后飘（时间停在高速的那一刻）；眼睛睁大、目光直视前方，**表情凝固**，不看里榭娜；
- **里榭娜在右：** 面朝左，**弯腰、双手背在身后**，脸凑到离洛菈米亚的脸大约一个手掌远的地方，好奇又得意地打量她，歪头，嘴角带笑；她的头发自然垂落（她没有被定格）；悬浮音箱在她头边；
- **两人之间留出明显的空隙，不接触**；
- 两人的脸在画面中间偏上，人物大约占画面高度的 85%。

```
V3-1: Chest-up two-shot, eye-level. LEFT: RALMIA in strict side view facing RIGHT, frozen mid-flight at full speed:
leaning forward, one arm reaching forward out of the frame, her long blonde hair and red bow streaming straight back
as if time stopped at top speed; eyes wide, fixed straight ahead, expression frozen; she does not look at Lishenna.
Her right temple gem visible. RIGHT: LISHENNA facing LEFT, bending forward at the waist with both hands clasped
behind her back, her face about a hand's width from Ralmia's face, peering at her with amused curiosity, head tilted,
small teasing smile; her own hair hangs naturally (she is not frozen); speaker discs beside her head. A clear gap
between them -- no contact. Faces slightly above centre, figures about 85% of the frame height.
[STYLE] [RALMIA] [LISHENNA]
```

### V3-2：里榭娜对着镜头眨眼

**构图：** 里榭娜一个人，胸部以上，**正面朝着镜头、上身前倾**，好像凑过来看镜头（镜头就是洛菈米亚的眼睛）；双手背在身后；歪头，**一只眼睛眨着**，另一只看着镜头，调皮的笑；两个音箱圆盘在头两侧；脸在画面中央，头顶到胸口占满画面高度的大约 90%。

```
V3-2: LISHENNA alone, chest-up, facing the camera and leaning forward towards it as if peering closely into the lens;
both hands clasped behind her back; head tilted, winking one eye, the other eye looking straight into the camera,
playful grin. The two speaker discs on either side of her head. Face centred, head to chest filling about 90% of the
frame height. Eye-level. [STYLE] [LISHENNA]
```

### V3-3：走开时回头挥手

**构图：** 全身背影，朝画面深处走开（和现有的 `lishenna_walk.png` 同一个角度）；**回头从左肩看向镜头**，得意地笑；空着的那只手举到肩膀高度，轻轻挥一下；另一只手拿着麦克风垂在身侧；音箱圆盘在头边。人物在画面中央，脚底在画面高度约 92% 处，人物高度约占画面的 85%。

```
V3-3: Full-body LISHENNA seen from behind, walking away into the distance (same angle as the attached
lishenna_walk.png), glancing back over her LEFT shoulder at the camera with a smug little smile; her free hand raised
to shoulder height in a small, casual wave; the other hand holds the microphone loosely at her side. Speaker discs
beside her head. Centred, feet at about 92% of the frame height, figure about 85% of the frame height.
[STYLE] [LISHENNA]
```

### V3-4（可选）：洛菈米亚冲刺，3/4 正面

**构图：** 全身，身体水平、在高速飞行中，**从她右前方 3/4 的角度看过去**（看得到脸和右太阳穴的宝石），朝画面右侧冲；一只手臂伸向前方，手张开；眼睛睁大、很专注；头发、外套下摆、领结都笔直地向后飘。人物在画面中央，占画面宽度约 85%。

```
V3-4: Full-body RALMIA flying horizontally at full speed towards the RIGHT of the frame, seen from a three-quarter
front angle from her right side (her face and right-temple gem visible). One arm stretched forward with the hand
open, eyes wide and intent; hair, coat tails and red bow streaming straight back. Centred, about 85% of the frame
width. [STYLE] [RALMIA]
```

## 拿到图以后我会做的检查

- 宝石的位置、服装（里榭娜的青色领结和领带、黑白格发带、紫色鞋带）；
- V3-1 两人之间有没有空隙，洛菈米亚的头发是不是向后飘、里榭娜的是不是自然垂着；
- 转成线稿 / 点阵以后，轮廓是否清楚。
