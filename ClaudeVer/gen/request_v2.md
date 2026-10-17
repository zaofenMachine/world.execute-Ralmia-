# 第四批生图需求：第二版（里榭娜）（2026-10-17）

方案见 [`../plan_v2.md`](../plan_v2.md)。本批共 8 张：P0 七张，P1 一张。

## 交付规则

沿用前三批：

- 16:9（与前几批同尺寸，1672×941 即可）；
- 标"透明"的出透明底 PNG；
- 不要文字、logo、水印；
- 成对图在前一张上做**局部编辑**，编辑区以外逐像素不动；
- 文件名按下表，放进 `ClaudeVer/gen/`。

本批新增：

1. **先出 L0（里榭娜设定图），我确认后再出其余几张。** 其余每一张都要同时附上 L0。
2. 画面里有洛菈米亚的（L1、L2 里她的机械手），同时附上 `ref_sheet.png`。
3. **画风跟前几批一致**（附上 `offer_pose.png` 和 `creation_inverse.png` 做画风参考）：干净的动画线稿、平涂加少量柔和阴影、略暖的色调。不要照搬卡面那种高饱和霓虹的厚涂。
4. 里榭娜的服装只用**《奏绝》这一版**（参考 `_references/official_lishenna_diva.png`、`_references/official_lishenna_returning.png`，以及你手上那张完整立绘）。其他版本的服装一律不要。
5. **分寸：** 全部穿着完整，不要卡面那种低角度、腿朝镜头的构图，不要性感化的姿势或镜头。两人之间只到勾小指、指尖相对为止，不要亲吻、拥抱。

## 通用段落

```
STYLE: clean anime line art, flat cel shading with soft secondary shadows, slightly warm palette, crisp edges,
matching the attached MV frames (offer_pose, creation_inverse). Not the glossy neon card-art rendering.

LISHENNA (Shadowverse, "Diva" outfit only): a young idol with long coral-pink hair and straight bangs, blue-violet
eyes, a black-and-white checkered hairband with two black rabbit-ear-like loops, two floating gold-rimmed round
speaker discs with cyan sigils hovering beside her head; an oversized white off-the-shoulder jacket with puffy
sleeves, a sleeveless white top, a cyan neck bow and cyan tie, black high-waisted shorts with suspender straps and a
silver buckle, black thigh-high socks, chunky white sneakers with purple laces. Confident, playful, a little smug.
Fully clothed, no suggestive pose or camera angle.
```

## 清单

| 编号 | 文件名 | 透明 | 优先 | 替换 | 用在 |
|---|---|---|---|---|---|
| L0 | `lishenna_ref_sheet.png` | 否 | P0 | — | 只做参考 |
| L1 | `pinky_promise_v2.png` | 否 | P0 | `pinky_promise.png` | 57–59 秒勾小指；之后作为窗口、碎片、倒带反复出现 |
| L2 | `creation_inverse_v2.png` | 否 | P0 | `creation_inverse.png` | 85–89 秒神卡；174–177 秒画中画 |
| L3a | `stage.png` | 否 | P0 | `lab_desk.png` | 62.7–66.4 秒；"you have left" 第二处 |
| L3b | `stage_empty.png` | 否 | P0 | `lab_desk_empty.png` | "you have left" 第二处（112 秒） |
| L4 | `lishenna_walk.png` | 是 | P0 | `creator_walk.png` | 107–111 秒崖边；115–118 秒走进光里；188–192 秒 "you are free" |
| L6 | `lishenna_stand.png` | 是 | P0 | `creator_sheet` 抠出的背影 | 70–74 秒立方体里和她并肩 |
| L5 | `lishenna_float.png` | 是 | P1 | trance 里的 `creator_walk` | 100–103.7 秒 trance。没有这张就用 L4 |

---

### L0 `lishenna_ref_sheet.png`：里榭娜设定图

**用途：** 之后每张图的角色依据，相当于洛菈米亚的 `ref_sheet.png`。

**构图：** 纸色底。同一画布上排三个全身站姿：正面、左侧面、背面，加一个脸部特写（正面，带悬浮音箱圆盘）。站姿自然，双手垂在身侧，不拿麦克风。三个全身高度一致。

```
Character reference sheet of LISHENNA on a plain warm paper background: full-body front view, left side view and back
view standing in a relaxed neutral pose (arms at her sides, no microphone), all three the same height, plus one
head-and-shoulders close-up from the front with the floating speaker discs. [STYLE] [LISHENNA]
```

### L1 `pinky_promise_v2.png`：勾小指（在 `pinky_promise.png` 上局部编辑）

**用途：** 全片最重要的一帧：57–59 秒她和"你"勾小指。之后倒带回到的也是这一帧。

**要求：**

- **只改画面右半边。** 把男性的手和白大褂袖子换成里榭娜的手：纤细的女性手，白色宽松外套的蓬袖口从右边画框外伸进来，手背朝上，小指和洛菈米亚的机械小指勾在一起。
- **左半边逐像素不动**：洛菈米亚的机械手、掌心核心、红线结都不动。这样才能和 `pinky_alone.png` 继续成对叠用。
- 红线结的位置不变（大约在 (955, 535)，按 1920 宽计）。

```
Inpaint only the right half of the attached image: replace the man's hand and lab-coat sleeve with LISHENNA's hand —
a slender girl's hand coming in from the right edge out of the puffy white sleeve of her oversized jacket, back of the
hand up, her little finger hooked with the robot girl's black mechanical little finger exactly where the man's was.
Keep every pixel of the left half (the mechanical hand, its cyan palm core, the red thread knot) unchanged. Same paper
background and line style.
```

### L2 `creation_inverse_v2.png`：神卡（在 `creation_inverse.png` 上局部编辑）

**用途：** 85–89 秒"我是唯一的神，你是我存在的证明"，两只手的指尖在 k189 相触。174–177 秒的画中画也用这张。

**要求：**

- 只改从**右下**伸上来的那只手：换成里榭娜的手（同 L1 的手和蓬袖口），食指伸向左上，**指尖停在原来那个位置**（大约 (948, 463)，按 1920 宽计），伸出的方向也和原来一致。
- 洛菈米亚从左上伸下来的机械手、背景、构图全部不动。

```
Inpaint only the lower-right hand of the attached image: replace the adult man's hand and sleeve with LISHENNA's hand
reaching up from the lower right out of the puffy white sleeve of her jacket, index finger extended toward the upper
left. The fingertip must stay exactly where the original fingertip is, pointing in the same direction. Keep the black
mechanical hand from the upper left and the dark ink background unchanged.
```

### L3a / L3b `stage.png` / `stage_empty.png`：演唱会舞台（成对）

**用途：** 替换"他坐在研究所桌前"那一镜。里榭娜在舞台上唱歌，身后三块巨型屏幕里放洛菈米亚做的模拟（屏幕内容由我合成）。

**L3a 构图：**

- 夜场演唱会，镜头在观众席中后方、略高的位置，看向舞台。
- 舞台中央是里榭娜，全身，大约占画面高度的 1/3。她一手举麦克风唱歌，另一手伸向观众，悬浮音箱圆盘在头边。
- 舞台后方并排三块大屏幕：中间大，左右略小，占画面上半部。**屏幕内容必须是纯白、完全平涂、没有任何图案和渐变**，我要把它们抠出来做遮罩。
- 前景下方是观众的剪影和荧光棒海。**荧光棒只用粉色、紫色和暖白**，不要青色和红色（这两种颜色在片子里另有专门用途）。
- 舞台灯光以暖白和品红为主。

**L3b（在 L3a 上局部编辑）：** 散场以后。里榭娜不见了，原位只剩一支立着的麦克风架；三块屏幕关掉（纯黑）；观众和荧光棒全部消失，只剩空荡的场地；灯光只剩一盏昏暗的工作灯。舞台结构、屏幕边框、镜头角度逐像素不变。

```
L3a: A night concert seen from the middle of the audience, slightly elevated. LISHENNA stands centre stage, full body,
about one third of the frame height, singing into a handheld microphone with her other hand reaching out to the crowd,
her floating speaker discs beside her head. Behind her, three huge stage screens side by side (the centre one larger)
fill the upper half of the frame: the screens are PURE FLAT WHITE with no image, no gradient, no texture (they will be
masked and replaced). Foreground: silhouettes of the audience and a sea of light sticks in pink, purple and warm white
only — no cyan, no red. Warm white and magenta stage lights. [STYLE] [LISHENNA]

L3b (inpaint on L3a, same canvas): after the show. LISHENNA is gone; a single microphone on a stand remains where she
stood. The three screens are switched off (flat black). The audience and light sticks are gone, the floor is empty.
Only one dim work light. Stage structure, screen frames and camera are pixel-identical to L3a.
```

### L4 `lishenna_walk.png`：走开的背影（透明）

**用途：** 替换"他的背影"。同一张图用在三处：崖边和她并肩站着（缩得很小）、走进光里离开、"you are free" 走向舞台的光。

**要求：**

- 全身背影，正在走开（迈步），步子轻快、有点潇洒，头发和外套下摆往后飘。
- **一只手垂在身侧、稍微离开身体，小指清楚可见**：红线由我从这里接出去（只画到手边，不要画线）。
- 看不到脸；悬浮音箱圆盘跟在头边。
- 人物在画面中央，高度约占画面的 95%，脚踩在画面底部附近。

```
Full-body back view of LISHENNA walking away from the viewer, mid-stride, a light and confident step, hair and the hem
of her oversized jacket swaying back. One hand hangs at her side slightly away from the body with the little finger
clearly visible (do not draw any thread). Face not visible. Floating speaker discs beside her head. Centred, the
figure about 95% of the frame height, feet near the bottom edge. transparent background. [STYLE] [LISHENNA]
```

### L6 `lishenna_stand.png`：站姿（透明）

**用途：** 70–74 秒，窗口拼成的立方体里，她站在洛菈米亚（`offer_pose`，张开双手）的右边。

**要求：** 全身，3/4 正面，身体朝向画面左侧（朝着洛菈米亚）；一手拿麦克风垂在身侧，另一手叉腰或轻轻挥手；自信、带点得意的偶像式微笑。镜头平视，**不要低角度**。人物在画面中央，高度约 95%。

```
Full-body LISHENNA standing, three-quarter front view turned toward the left of the frame, eye-level camera (not a
low angle). One hand holds a microphone lowered at her side, the other on her hip; a confident, slightly smug idol
smile. Floating speaker discs beside her head. Centred, about 95% of the frame height. transparent background.
[STYLE] [LISHENNA]
```

### L5 `lishenna_float.png`：漂浮哼唱（透明，P1）

**用途：** 100–103.7 秒 trance。她和漂浮的洛菈米亚（`floating.png`）绕着同一个圆心慢慢转。

**要求：** 全身，像在失重中漂浮，身体微微倾斜；闭眼，轻轻哼唱，表情放松、陶醉；头发和外套向四周散开；麦克风松松地握在手里。人物在画面中央，高度约 75%，四周留白（会被旋转）。

```
Full-body LISHENNA floating weightlessly, body gently tilted, eyes closed, softly humming with a relaxed, entranced
expression; hair and jacket drifting outward in all directions; a microphone held loosely in one hand. Centred, about
75% of the frame height, generous empty space around (the image will be rotated). transparent background.
[STYLE] [LISHENNA]
```
