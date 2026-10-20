# 第八批：光速下时间停止

依据 [request_v3a.md](request_v3a.md)，完成 **3 张必需图 + 1 张可选图**。最终均为 **1672×941、透明 RGBA PNG**，由内置 image_gen 生成；角色参考和本轮三张风格图随每次生成提供，原始输出与提示词均已保存。

| 文件 | 构图与关键检查 | 可见范围 |
|---|---|---|
| [peek_frozen.png](peek_frozen.png) | 左侧洛菈米亚右向侧面冻结；右侧里榭娜前倾观察。脸、手臂与发丝间有空隙，无接触；右太阳穴宝石可见，金发和两条红领结尾向后，粉发自然下垂。 | 约 85.23% 画高 |
| [lishenna_wink.png](lishenna_wink.png) | 正面胸像，前倾歪头，一眼眨、一眼看镜头，双上臂朝后，双手在裁切范围外；两音箱和完整头饰。 | 约 90.01% 画高 |
| [lishenna_wave_back.png](lishenna_wave_back.png) | 背向走开，从自己的左肩回看；左手肩高轻挥、右手麦克风下垂。 | 约 85.02% 画高，下边界 y=866（约 92%） |
| [ralmia_frozen_34.png](ralmia_frozen_34.png) | 右前方 3/4 冲刺，全身向右；可见脸、右太阳穴宝石、黑机械手及青色掌心；长发、衣摆和红领结向后。 | 约 84.99% 画宽 |

## 修订与验收

- 四张独立资产并行生成，单张内部的局部修订依次完成。本批不是 A/B 动画配对，不需要四图之间逐像素对齐。
- 双人图修正了向下垂的领结尾和过近的前臂，随后补好左侧金发与躯干边界。原本悬在透明画布内的竖直裁口已消除；底部保留正常胸像裁切。Alpha>128 的两个人物连通域分离，与目视空隙检查一致。
- 眨眼图补全了最初触边的头饰，再缩小定位。
- 挥手图局部删除错误新增的袖子青色小蝴蝶结。真正肩部青色片及背后长片保留；[编辑遮罩](_qa/round8/wave_sleeve_edit_mask.png)之外 **1,570,285 像素变化为 0**，透明通道未变。
- 冲刺图局部修正红领结，使两条尾部均向后飘。没有地面、推进火焰、速度线或背景光效。
- 仅做已授权的缩小／平移定位、透明边缘清理和局部像素回填，没有插值放大。各自原图、定位参数与修补记录均可复查。
- 最终 PNG 可正常解码，尺寸和透明通道符合要求；既有 **67 张 PNG 的 SHA256 全部未变**。独立视觉复核已通过。

## 预览

- [四图总览](_qa/round8/contact_sheet.jpg)
- [线稿轮廓检查](_qa/round8/lineart_contact_sheet.jpg)
- [点阵可读性检查](_qa/round8/dot_contact_sheet.jpg)
- [挥手图袖子修正前后](_qa/round8/wave_sleeve_before_after.png)

线稿和点阵图是检查轮廓的简化预览，不是 MV 最终渲染效果。

## 记录与复现

- [完整提示词索引](_production/round8/prompts.json)
- [整批数值验收](_qa/round8/validation.json)
- [独立视觉验收](_qa/round8/visual_review.json)
- [双人图整理脚本](_production/round8/peek_finalize.py)
- [眨眼图整理脚本](_production/round8/wink_finalize.py)
- [挥手图定位脚本](_production/round8/wave_register.py)，再执行[袖子局部修正](_production/round8/wave_sleeve_apply.py)
- [冲刺图整理脚本](_production/round8/frozen_finalize.py)
- [整批验收与预览脚本](_production/round8/audit_all.py)

本轮交付图片和记录；没有修改 MV 代码或重新渲染成片。
