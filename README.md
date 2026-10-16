# world.execute(me); × Ralmia

以 Mili《world.execute(me);》与《影之诗》角色 Ralmia（ララミア／洛菈米亚）为主题的 MV 制作工程。

## 当前进度

截至 2026-10-17，Claude 版已制作到约 162.8 秒（第三版）；第四轮调整计划见 [plan_round4.md](ClaudeVer/plan_round4.md)。这是一份制作中的工程，并非全曲最终成片。

## 目录

- [CONTEXT.md](CONTEXT.md)：项目交接、设计决定、历史进度和待办事项。
- [ClaudeVer/project/](ClaudeVer/project/)：Python 渲染器、分镜、时间线、字体和已处理素材。
- [ClaudeVer/gen/](ClaudeVer/gen/)：原始生成图片、素材规格、反馈、生产脚本及验收记录。
- [ClaudeVer/plan_full.md](ClaudeVer/plan_full.md)：全片计划。
- [AstraVer/Images/](AstraVer/Images/)：早期版本恢复的图片及来源清单。
- `Audio/`：工程使用的原曲音频。
- [review/](review/)：早期版本评审、节拍网格和评审缩略图。

## 环境与预览

使用 Python 3.10 或更高版本；视频编码另需将 `ffmpeg` 加入 PATH。安装渲染所需依赖：

```sh
python -m pip install numpy opencv-python pycairo uharfbuzz fonttools
cd ClaudeVer/project
python render.py still preview.jpg 1.6,6.9,19.9 0.25 3
```

`requirements.txt` 还列出了节拍分析、语音识别和字体重新实例化使用的可选依赖；直接预览现有工程不需要安装这些分析工具。预处理图片及字体已随仓库保留，无需先重跑 `prep*.py`。

渲染及拼接示例（从仓库根目录启动）：

```sh
cd ClaudeVer/project
python -c "from pathlib import Path; Path('chunks').mkdir(exist_ok=True)"
python render.py enc 0 5 chunks/c0.mp4
python mux.py 5
python qa.py out_delivery.mp4
```

以上只渲染前 5 秒。制作更长版本时，需要按时间顺序输出完整连续的 `chunks/c0.mp4`、`c1.mp4` 等分段，再向 `mux.py` 传入对应的总时长。重新渲染不同长度的版本前，应移走旧分段，以免一并拼入。

## 版本控制范围

保留源码、原始图片、当前处理后的图片、字体、音频、计划和验收记录。处理后图片也直接纳入版本控制，以便保留当前成片所用的精确素材状态。

视频成片、视频分段、Python 缓存、临时拼接列表、渲染抽帧和已弃用的短发设定实验由 `.gitignore` 排除，仍留在本地。成片需要通过渲染生成，或另行分发。

`gen/_production/` 内的脚本和 JSON 保留历史生产来源；部分记录含原制作环境的绝对路径，部分脚本会覆盖素材或要求外部生成图片，不能直接视为跨机器的一键重建流程。日常渲染入口使用工程内的相对路径。

歌曲、角色和字体等素材的权利归各自权利人所有；本仓库没有为这些素材授予新的使用许可。
