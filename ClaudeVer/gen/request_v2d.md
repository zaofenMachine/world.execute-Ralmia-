# 第七批生图需求：22–28 秒"阿基里斯追不上乌龟"（2026-10-19）

方案见 [`../plan_v2_round6.md`](../plan_v2_round6.md)。本批共 2 张，成对。

## 交付规则

沿用前几批：

- 16:9，1672×941，原生分辨率；透明底 PNG；
- 不要文字、logo、水印；
- B 在 A 上**局部编辑**，编辑区以外逐像素不动，并附编辑区遮罩；
- 附 `lishenna_ref_sheet.png`（服装只用《奏绝》这一版）；画风参考附 `lishenna_stand.png`、`lishenna_sit.png`；
- 文件名按下表，放进 `ClaudeVer/gen/`，另写 `README_round7.md`。

这两张会被代码转成**线稿**（荧光线条）来用，所以**轮廓和主要线条要清楚**，比上色更重要。

**分寸：** 穿着完整，平视镜头，不要低角度，不要性感化的姿势。

## 清单

| 编号 | 文件名 | 透明 | 用在 |
|---|---|---|---|
| L17a | `lishenna_stroll_a.png` | 是 | 22.5–28 秒：她在前面边走边唱，洛菈米亚在后面追 |
| L17b | `lishenna_stroll_b.png` | 是 | 同上，下一步（A/B 交替就是走路） |

### L17a / L17b：侧面朝右，边走边唱

**构图：**

- 全身，**正侧面，朝画面右侧走**（向右走，背对左边追来的洛菈米亚）；平视；
- 悠闲、轻快的散步，一点都不赶；**一只手拿麦克风在嘴边唱歌**，另一只手自然摆动；
- 可以稍微回头往左后方瞟一眼，嘴角带一点得意的笑（知道有人在追她）；
- 头发和外套下摆向后飘；悬浮音箱圆盘跟在头边；
- 人物在画面中央，脚底踩在画面下方约 90% 高度处，人物高度约占画面的 85%；
- **A：** 左脚在前；**B（在 A 上局部编辑，只改腿、脚和摆动的那只手）：** 右脚在前，摆动的手换到另一侧。上身、头、拿麦克风的手都不动。

```
Full-body LISHENNA in strict side view walking to the RIGHT of the frame, eye-level camera. A light, unhurried, carefree
stroll. One hand holds a microphone at her lips, singing; the other arm swings naturally. She glances back over her left
shoulder with a small smug smile, as if she knows someone is chasing her. Hair and the hem of her oversized jacket flow
back; the floating speaker discs follow beside her head. Centred, about 85% of the frame height, feet at about 90% of
the frame height. Clear outline and clean main lines (it will be turned into line art). transparent background.
[STYLE] [LISHENNA]
B (inpaint on A, legs, feet and the swinging arm only): the other foot forward and the free arm swung to the other
side -- the next step of the same walk. Head, upper body and the microphone hand unchanged.
```

## 拿到图以后我会做的检查

- 脚底是否在同一条水平线上，A/B 交替时上身是否完全不动；
- 转成线稿以后，轮廓是否清楚；
- 服装（青色领结和领带、黑白格发带、紫色鞋带）。
