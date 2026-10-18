# 第五批生图需求：第二版补图（2026-10-18）

方案见 [`../plan_v2b.md`](../plan_v2b.md)。本批共 2 张：P0 一张，P1 一张。第四批已交付的 8 张都继续用，不需要重出。

## 交付规则

沿用前几批：

- 16:9，1672×941；
- 标"透明"的出透明底 PNG；
- 不要文字、logo、水印；
- 文件名按下表，放进 `ClaudeVer/gen/`；
- **每张都附上 `lishenna_ref_sheet.png`**（角色基准），服装只用《奏绝》这一版；
- **画风跟前几批一致**（附上 `listen_profile.png` 和 `lishenna_stand.png` 做画风参考）：干净的动画线稿、平涂加少量柔和阴影、略暖的色调；不要卡面那种高饱和霓虹厚涂；
- **分寸：** 穿着完整，平视镜头，不要低角度，不要性感化的姿势或构图。

## 通用段落

```
STYLE: clean anime line art, flat cel shading with soft secondary shadows, slightly warm palette, crisp edges,
matching the attached MV frames (listen_profile, lishenna_stand). Not the glossy neon card-art rendering.

LISHENNA (Shadowverse, "Diva" outfit only, exactly as in the attached lishenna_ref_sheet): long coral-pink hair with
straight bangs, blue-violet eyes, black-and-white checkered hairband with two black rabbit-ear-like loops, two floating
gold-rimmed round speaker discs with cyan sigils beside her head; oversized white off-the-shoulder jacket with puffy
sleeves, sleeveless white top, cyan neck bow and cyan tie, black high-waisted shorts with suspender straps and the
silver buckle, black thigh-high socks, chunky white sneakers with purple laces. Fully clothed, eye-level camera.
```

## 清单

| 编号 | 文件名 | 透明 | 优先 | 用在 |
|---|---|---|---|---|
| L7 | `lishenna_front.png` | 是 | P0 | 126–133 秒：满屏代码雨聚成她的巨大轮廓（只用轮廓做遮罩，也会淡淡透出本图） |
| L8 | `lishenna_sing_profile.png` | 否（纸底） | P1 | 103.7–107.4 秒：和洛菈米亚闭眼聆听的侧脸面对面 |

---

### L7 `lishenna_front.png`：正面全身（透明）

**用途：** "Challenging your god"那一段，洛菈米亚的背影前方，滚动的源代码聚成一个巨大的里榭娜。这张图主要当**轮廓遮罩**用，所以轮廓要清楚、好认。

**要求：**

- 全身**正面**，左右大致对称，平视镜头，**不要仰拍**；
- 双臂微微张开、离开身体（轮廓里手臂和躯干之间要看得到空隙），掌心朝前，像偶像在演出高潮时向全场张开双手；麦克风握在右手；
- 两只悬浮音箱圆盘一左一右，在头的两侧，和头之间也留出空隙；
- 眼睛直视前方，嘴角带一点自信、得意的笑；
- 人物在画面正中，高度约占画面的 95%，脚踩在画面底部附近。

```
Full-body FRONT view of LISHENNA standing, roughly symmetrical, eye-level camera (not a low angle). Both arms held
slightly out from the body with clear gaps between arms and torso, palms facing forward, like an idol opening her arms
to the whole crowd at the climax of a show; a handheld microphone in her right hand. The two floating speaker discs
hover on either side of her head with a clear gap between each disc and the head. Looking straight ahead with a small
confident, slightly smug smile. Centred, the figure about 95% of the frame height, feet near the bottom edge.
Clean, readable silhouette. transparent background. [STYLE] [LISHENNA]
```

### L8 `lishenna_sing_profile.png`：闭眼轻唱的侧脸（纸底，P1）

**用途：** 和洛菈米亚闭眼聆听的侧脸（附图 `listen_profile.png`）组成一对：一个唱，一个听。两张图会在片子里左右对放、脸对着脸，中间连一条旋律线。

**要求：**

- **构图、镜头、大小都和附图 `listen_profile.png` 一致：** 头肩的侧脸，**脸朝画面左侧**，脸前方留出大片空白纸底；头发向画面右侧飘；
- 闭眼，嘴唇微张，正在轻轻地唱，表情放松、专注；
- 手持麦克风，靠近下巴和嘴边，但**不要挡住嘴和脸的轮廓**；
- 悬浮音箱圆盘只露出靠后的那一只（在头的后方），不要挡脸；
- 纸底颜色和 `listen_profile.png` 一样。

```
Head-and-shoulders PROFILE of LISHENNA facing the LEFT of the frame, same camera, framing, scale and paper background as
the attached listen_profile.png, with a wide empty paper area in front of her face; her long coral-pink hair flows
toward the right edge. Eyes closed, lips slightly parted, softly singing with a relaxed, absorbed expression. She holds
a handheld microphone near her chin without covering her lips or the profile line of her face. Only the far speaker
disc is visible, behind her head; nothing covers her face. Same warm paper background as listen_profile.png.
[STYLE] [LISHENNA]
```

---

## 拿到图以后我会做的检查

- L7：轮廓抠出来后，手臂、圆盘与身体的空隙是否清楚；
- L8：和镜像后的 `listen_profile` 左右对放，两张脸的高度、大小、纸底色是否对得上；
- 两张：宝石不涉及（只有洛菈米亚有）；服装是否和设定图一致（青色领结和领带、黑白格发带、紫色鞋带）。
