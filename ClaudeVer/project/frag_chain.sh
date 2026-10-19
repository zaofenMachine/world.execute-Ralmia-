#!/bin/sh
# 0-105 s -> qa sheets -> fragments (the bridge and the escape show tiles of the film itself).
# run after anything before 100 s changed, then re-render chunks 23-25 and 38-39.   usage: sh frag_chain.sh
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CH=chunks_v3; QA=qa_v3
cd "$HERE"
: > list_frag.txt
for i in $(seq 0 20); do echo "file '$HERE/$CH/c$i.mp4'" >> list_frag.txt; done
ffmpeg -v error -y -f concat -safe 0 -i list_frag.txt -c copy "$CH/_0-105.mp4"
python qa.py "$CH/_0-105.mp4" $QA
python prep7.py frag
