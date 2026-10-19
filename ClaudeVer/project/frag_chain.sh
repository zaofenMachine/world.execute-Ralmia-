#!/bin/sh
# 0-105 s -> qa sheets -> fragments (the bridge and the escape show tiles of the film itself).
# run after anything before 100 s changed, then re-render chunks 23-25 and 38-39.   usage: sh frag_chain.sh
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CH=chunks_v3; QA=qa_v3
cd "$HERE"
# the list needs Windows paths for ffmpeg.exe (an /f/... path from sh is not found)
python -c "import os; open('list_frag.txt', 'w').write(''.join(\"file '%s'\n\" % os.path.abspath('$CH/c%d.mp4' % i) for i in range(21)))"
ffmpeg -v error -y -f concat -safe 0 -i list_frag.txt -c copy "$CH/_0-105.mp4"
python qa.py "$CH/_0-105.mp4" $QA
python prep7.py frag
