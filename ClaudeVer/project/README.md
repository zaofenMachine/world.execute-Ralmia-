# world.execute(me); × Ralmia — 工程说明

完整的项目上下文见 `../../CONTEXT.md`，计划和生图规格见 `../plan_0-60s.md`。

```
pip install numpy opencv-python pycairo uharfbuzz fonttools   # 另需 ffmpeg 在 PATH 里
python render.py still preview.jpg 1.5,3.6,10.9 0.25 4        # 出单帧拼图
python render.py enc 0 5 chunks/c0.mp4                         # 渲染分段（可以多进程并行）
python mux.py 30.45                                            # 拼接 + 混入原曲 → out.mp4 / out_delivery.mp4
python qa.py out_delivery.mp4                                  # 自查：拼图 + 卡点统计 + 冻结检测
```

**各文件作用：**

- `lib.py`：工具库。
- `scenes.py` / `scenes2.py`：各镜头。
- `render.py`：时间线和合成。
- `prep.py`：Astra 图片 → `assets/` 下的 `_full` / `_line` / `_hd` 三个版本。
- `make_fonts.py`：字体实例化。
- `make_words.py`：生成歌词时间戳。
- `beats.py`：节拍检测。

`mux.sh` 已废弃。
