# 第六批生图需求：第二版第二轮（2026-10-18）

方案见 [`../plan_v2_round2.md`](../plan_v2_round2.md)。本批共 12 张，P0 九张，P1 三张。

## 交付规则

沿用前几批：

- 16:9，1672×941，原生分辨率，不要插值放大；
- 标"透明"的出透明底 PNG；
- 不要文字、logo、水印；
- 成对图（a / b）在前一张上做**局部编辑**，编辑区以外逐像素不动，并附编辑区遮罩；
- 文件名按下表，放进 `ClaudeVer/gen/`，另写 `README_round6.md`。

**参考图：**

- 有里榭娜的，附 `lishenna_ref_sheet.png`；服装只用《奏绝》这一版；
- 有洛菈米亚的，附 `ref_sheet.png`。**宝石在她的右太阳穴**：正面看在画面左侧，脸朝右的侧面看得到，脸朝左的侧面看不到，背影里如果露出来，在头的画面右侧；
- 画风参考附 `offer_pose.png`、`lishenna_stand.png`、`listen_profile.png`：干净的动画线稿、平涂加少量柔和阴影、略暖的色调；不要卡面那种高饱和霓虹厚涂。

**分寸（这一批有变化）：** 用户同意两人**贴贴**：脸贴脸、靠肩、挽手、侧面搂抱都可以。**仍然不要亲吻**；两人穿着完整；不要低角度、不要腿朝镜头的构图，不要任何性感化的姿势或镜头。猫娘只做表情和手势的萌，不要道具。

**不要画红线。** 红线全部由代码画；勾小指的地方只画手。

## 通用段落

```
STYLE: clean anime line art, flat cel shading with soft secondary shadows, slightly warm palette, crisp edges,
matching the attached MV frames. Not the glossy neon card-art rendering.

RALMIA (exactly as in the attached ref_sheet): long blonde hair with an ahoge, cyan eyes, a cyan gem on her RIGHT temple
(on the LEFT of the image when she faces the viewer), white-and-black mechanical suit with cyan lights, a red neck bow,
black mechanical hands with cyan palm cores.

LISHENNA ("Diva" outfit only, exactly as in the attached lishenna_ref_sheet): long coral-pink hair with straight bangs,
blue-violet eyes, black-and-white checkered hairband with two black rabbit-ear-like loops, two floating gold-rimmed
speaker discs with cyan sigils beside her head; oversized white off-the-shoulder jacket with puffy sleeves, sleeveless
white top, cyan neck bow and cyan tie, black high-waisted shorts with suspender straps and the silver buckle, black
thigh-high socks, chunky white sneakers with purple laces.

Fully clothed, eye-level camera, wholesome and affectionate. No kissing. No red thread (it is drawn in code).
```

## 清单

| 编号 | 文件名 | 透明 | 优先 | 用在 |
|---|---|---|---|---|
| L13a | `creation_plate.png` | 否 | P0 | 85–89 秒神卡、174–177 秒画中画：只有背景 |
| L13b | `creation_hand_ralmia.png` | 是 | P0 | 同上：洛菈米亚的手 |
| L13c | `creation_hand_lishenna.png` | 是 | P0 | 同上：里榭娜的手（重画指尖） |
| L11a | `cube_together.png` | 是 | P0 | 70–74 秒立方体里的合照 |
| L11b | `cube_alone.png` | 是 | P0 | 114.6 秒：里榭娜被删掉，洛菈米亚抱着空气 |
| L12a | `ledge_together.png` | 否 | P0 | 107–111 秒崖边并肩坐 |
| L12b | `ledge_alone.png` | 否 | P0 | 113.9 秒：里榭娜化成光点飘走以后 |
| L15a | `cat_ralmia_v2.png` | 是 | P0 | 81.6–85.3 秒猫卡（替换 `cat_ralmia.png`） |
| L15b | `cat_ralmia_v2b.png` | 是 | P0 | 同上，配对的另一个表情 |
| L9a | `lishenna_sit.png` | 是 | P1 | 35–44 秒：坐在圆周线、切线、渐近线上 |
| L9b | `lishenna_sit_b.png` | 是 | P1 | 同上，晃脚的另一拍 |
| L14 | `ending_together.png` | 是 | P1 | 结尾 207–212 秒：两人脸贴脸 |

L9a 标成 P1，只是因为它不涉及修错；用户很在意 35–48 秒没有角色，能早出就早出。

---

### L13a / b / c：神卡拆成三层

**为什么要重出：** `creation_inverse_v2.png` 里，里榭娜食指的最前端是从旧图锁下来的男人指尖像素，肤色和形状都接不上（附图 `creation_inverse_v2.png`，指尖在 (826, 403) 附近）。这次三层分开出，代码分别移动两只手，指尖在画面中央相遇。

**共同要求：**

- 三张都在 `creation_inverse_v2.png` 的同一张画布上：构图、尺寸、位置都不变；
- **L13a 背景：** 只有深色水墨背景，两只手和袖子都去掉，补成完整的背景；
- **L13b 洛菈米亚的手（透明）：** 从左上伸下来的黑色机械手和前臂，和现在**完全一样**，只是抠出来；
- **L13c 里榭娜的手（透明）：** 从右下伸上来，白色蓬袖口，**重新画食指和指尖**：自然的指尖和指甲，肤色和整只手一致，指向左上方，伸出的方向和现在一样；指尖最前端大约在 (826, 403)（按 1672 宽计）；
- 两只手的边缘干净，不带背景色的半透明毛边（会叠在不同的位置）。

```
L13a: The attached creation_inverse_v2 image with BOTH hands and sleeves removed: only the dark ink-wash background
remains, completed naturally where the hands were. Same canvas.
L13b: Only the black mechanical hand and forearm reaching down from the upper left, exactly as in the attached image,
cut out on a transparent background, same position on the same canvas.
L13c: Only LISHENNA's hand reaching up from the lower right out of her puffy white sleeve, on a transparent background,
same position on the same canvas. Redraw the index finger and its tip properly: a natural slender fingertip with a
nail, the same skin tone as the rest of her hand, pointing to the upper left in the same direction as now; the very
tip of the finger at about (826, 403). [STYLE] [LISHENNA]
```

### L11a / L11b：立方体里的合照（透明，成对）

**用途：** 70–74 秒，窗口折成立方体，把两人关在里面（"Though we are trapped in this strange, strange simulation"）。现在两人各自呆站，换成贴贴的合照。114.6 秒用 L11b：里榭娜被系统选中删除以后，洛菈米亚还保持着被抱住的姿势。

**L11a 构图：**

- 两人全身站立，正面朝镜头，平视；
- 洛菈米亚在画面左边，里榭娜在右边；
- 里榭娜侧过身，双手抱住洛菈米亚的胳膊，**脸颊贴着洛菈米亚的脸颊**，眯眼笑，另一只手比 V 字（或者麦克风拿在手里）；
- 洛菈米亚被突然抱住，有点惊讶，脸红，嘴角在笑；她的一只手被抱着，另一只手不知所措地举在胸前；
- 两人站得紧，轮廓连成一个整体；整体在画面中央，高度约占画面的 92%，脚踩在画面底部附近；
- 洛菈米亚的宝石在画面左侧（她的右太阳穴），不要被里榭娜挡住。

**L11b（在 L11a 上局部编辑）：** 去掉里榭娜和她的悬浮圆盘；**洛菈米亚的姿势、表情一点不改**，被抱着的那只胳膊还停在原处，脸还歪向原来贴着的方向。只补上里榭娜原来挡住的洛菈米亚身体部分。

```
L11a: Full-body RALMIA and LISHENNA standing close together, facing the viewer, eye-level camera. RALMIA on the left,
LISHENNA on the right. LISHENNA turns in and hugs RALMIA's arm with both hands, pressing her cheek against RALMIA's
cheek with a happy squint, flashing a peace sign with her free hand. RALMIA, caught by surprise, blushes and smiles;
her free hand is raised awkwardly in front of her chest. One combined silhouette, centred, about 92% of the frame
height, feet near the bottom edge. RALMIA's temple gem stays visible on the left of the image.
transparent background. [STYLE] [RALMIA] [LISHENNA]
L11b (inpaint on L11a, same canvas): remove LISHENNA and her speaker discs entirely. RALMIA's pose and expression stay
exactly the same: her arm stays where it was being hugged and her head still leans towards where LISHENNA's cheek was.
Only fill in the parts of RALMIA that LISHENNA used to cover. transparent background.
```

### L12a / L12b：崖边并肩坐（成对，不透明）

**用途：** 107–111 秒 "then I can finally be COMPLETION"，这是全片最满的一小节。113.9 秒用 L12b：里榭娜化成光点飘走以后，只剩洛菈米亚。

**L12a 构图：**

- **和第一批的世界是同一个地方**（附 `_qa/world_composite.jpg`、`world_L4_fore.png`、`world_L2_city.png`）：深色金属骨架的崖边平台、远处的白色拱门和高塔、水面、正在下沉的夕阳；
- 镜头在两人身后、略高，中景：两人约占画面高度的一半；
- 两人**并肩坐在崖边，脚悬在边外**，背对镜头看着夕阳；
- 里榭娜坐在左边，**把头靠在洛菈米亚的肩上**；洛菈米亚的头也轻轻歪向她；
- 两人中间的手放在岩石上，**小指勾在一起**（手要清楚可见，不要画线）；
- 里榭娜的悬浮圆盘在她头边；背影里看不到脸；如果看得到洛菈米亚的宝石，在她头的画面右侧；
- 夕阳在画面右侧，逆光，暖金色。

**L12b（在 L12a 上局部编辑）：** 去掉里榭娜和她的圆盘；洛菈米亚的姿势完全不变，头还歪着，伸过去勾小指的手还放在原处，小指空着。补好里榭娜原来挡住的背景。

```
L12a: The same world as the attached frames (the dark metal-framed cliff ledge, white arches and towers in the
distance, the water, the setting sun). Medium shot from behind and slightly above: RALMIA and LISHENNA sit side by side
on the edge of the ledge with their legs dangling over it, their backs to the viewer, watching the sunset. LISHENNA
on the left rests her head on RALMIA's shoulder; RALMIA tilts her head towards her. Between them their hands rest on
the rock with the little fingers hooked together, clearly visible. Warm golden backlight, the sun on the right.
The two figures take about half of the frame height. [STYLE] [RALMIA] [LISHENNA]
L12b (inpaint on L12a, same canvas): LISHENNA and her speaker discs are gone, the background behind her restored.
RALMIA is exactly the same: her head still tilted, her hand still resting where their little fingers were hooked,
now hooked to nothing.
```

### L15a / L15b：猫娘洛菈米亚（透明，成对）

**用途：** 81.6–85.3 秒主歌 2 的第三张标本卡（"If I'm a tabby cat, then I'll purr for your enjoyment"）。上一版 `cat_ralmia.png` 的腿和尾巴画错了，整张换掉。两张配对图按拍切换，配着呼噜的波形。

**L15a 构图：**

- **洛菈米亚的上半身**，到腰；正面略侧，平视；
- 头上一对猫耳（和发色相近的金色虎斑，内侧浅色），蓬松；**不要画尾巴和腿**；
- 双手握成松松的拳当猫爪，举在脸颊两侧，做"喵"的卖萌手势；歪头，**单眼眨眼**，嘴型是 "ω"，脸红；
- 服装是她原本的样子（红领结）；宝石在画面左侧；
- 构图端正，不强调胸部；人物在画面中央，高度约占画面的 90%。

**L15b（在 L15a 上局部编辑，只改脸）：** 双眼眯成满足的弧线（"^ ^"），嘴角更翘，像在被摸头时呼噜。手、猫耳、身体都不动。

```
L15a: Waist-up RALMIA as a cat-girl, facing the viewer at a slight angle, eye-level camera. Fluffy cat ears in a
golden tabby pattern close to her hair colour on her head; NO tail, no legs in frame. Both hands curled into loose
"paws" raised beside her cheeks in a playful "nya" pose; head tilted, one eye winking, an "ω"-shaped cat mouth,
blushing. Her usual outfit with the red neck bow; the temple gem on the left of the image. Modest, wholesome framing.
Centred, about 90% of the frame height. transparent background. [STYLE] [RALMIA]
L15b (inpaint on L15a, face only): both eyes closed into content happy arcs, the smile a little wider, as if purring
while being petted. Hands, ears and body unchanged.
```

### L9a / L9b：里榭娜坐着（透明，成对，P1）

**用途：** 35–44 秒，她坐在洛菈米亚给她的每一样东西上：圆展开成的那条线、正弦的切线（会跟着倾斜摇摆）、渐近线（洛菈米亚从下方飞来够她的鞋尖）。所以要坐在一根**看不见的水平细杆**上。

**L9a 构图：**

- 全身，坐在一根看不见的水平细杆上（**不要画杆**），**臀部下沿是一条水平直线**；
- 身体 3/4 朝向画面左侧，低头往左下方看，带点得意、又期待的笑；
- 双手撑在身体两侧的杆上（一只手里松松地拿着麦克风）；
- 双脚自然悬空，**一只脚向前踢起，一只脚垂下**；
- 悬浮圆盘在头边；人物在画面中央，高度约占画面的 80%，四周留空（会被旋转）。

**L9b（在 L9a 上局部编辑，只改小腿和鞋）：** 两只脚交换：原来踢起的那只垂下，原来垂下的那只踢起。上身、手、头一点不动。两张交替就是在晃脚。

```
L9a: Full-body LISHENNA sitting on an invisible thin horizontal bar (do not draw the bar; the underside of her seat is
a straight horizontal line). Body turned three-quarters toward the LEFT of the frame, looking down to the lower left
with a smug, expectant smile. Both hands rest on the bar beside her hips, a microphone held loosely in one. Legs
dangle freely: one foot kicked forward, the other hanging down. Speaker discs beside her head. Centred, about 80% of
the frame height, generous empty space around (the image will be rotated). transparent background. [STYLE] [LISHENNA]
L9b (inpaint on L9a, lower legs and shoes only): the two feet swap: the kicked one hangs down and the hanging one
kicks forward. Everything above the knees unchanged.
```

### L14：结尾，脸贴脸（透明，P1）

**用途：** 全片最后的画面（207–212 秒）：歌停了，她撕开自己的世界跑出来，终于碰到了你。先以线稿浮起，再上色，下面一行 `touch = true`。

**构图：**

- 两人的上半身（胸口以上），正面，平视；洛菈米亚在左，里榭娜在右；
- **脸贴着脸**，两人都闭着眼，很安静、很满足；里榭娜嘴唇微张，在轻轻哼歌；
- 两人的手举到下巴下方、两张脸中间，**小指勾在一起**（手清楚可见，不要画线）；
- 洛菈米亚的宝石在画面左侧，看得见；里榭娜的圆盘在她头的右后方；
- 人物在画面中央，高度约占画面的 85%。

```
L14: Chest-up RALMIA (left) and LISHENNA (right) facing the viewer, eye-level, cheek pressed to cheek, both eyes closed,
calm and content; LISHENNA's lips slightly parted, softly humming. Their hands are raised between and just below their
chins with the little fingers hooked together, clearly visible. RALMIA's temple gem visible on the left of the image;
LISHENNA's speaker discs behind her head on the right. Centred, about 85% of the frame height.
transparent background. [STYLE] [RALMIA] [LISHENNA]
```

---

## 拿到图以后我会做的检查

- 宝石的位置；里榭娜的服装（青色领结和领带、黑白格发带、紫色鞋带）；
- 成对图编辑区外是否逐像素不变；
- L13：两只手的指尖位置和方向；三层叠回去是否还原成原图的构图；
- L9：臀部下沿是否水平，好放到线上；
- 透明图的边缘有没有偏色的半透明毛边（上一批发丝边缘偏红，我这边已经能自动清理，但最好源头就干净）。
