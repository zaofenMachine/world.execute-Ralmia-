"""Rebuild only the FRAGMENTS tiles (assets/frag_*.png + frag.json) from qa/q*.jpg -- run after qa.py on a fresh 0-100 s
render, whenever anything before 100 s changed (the bridge's memory mosaic and the escape both use them).
The block itself lives in prep5.py; this runs just that part, so the round-2 images are not regenerated."""
import os, json, glob, cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets')
src = open(os.path.join(HERE, 'prep5.py'), encoding='utf-8').read()
blk = src[src.index('# ---- FRAGMENTS'):]; blk = blk[:blk.index('\n\n')]
exec(blk)
