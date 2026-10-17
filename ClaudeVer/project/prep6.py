"""Third GPT batch (ClaudeVer/gen, see README_round3.md) -> assets/n_*  (same treatment as prep3.py / prep5.py).
cat_ralmia = her as a cat-girl, for the verse-2 cat card; role_s / role_m = the S / M personality switch (pixel-aligned pair).
usage: python prep6.py
"""
import cv2, numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'gen'); A = os.path.join(HERE, 'assets')
src3 = open(os.path.join(HERE, 'prep3.py')).read()
for fn in ('def xdog', 'def resize', 'def line_of', 'def ink'):
    blk = src3[src3.index(fn):]; blk = blk[:blk.index('\n\n')]; exec(blk)          # reuse prep3's helpers

NAMES = {'cat_ralmia': 'cat', 'role_s': 'role_s', 'role_m': 'role_m'}

for src, nm in NAMES.items():
    im = cv2.imread(os.path.join(SRC, src + '.png'), cv2.IMREAD_UNCHANGED)
    im = resize(im)
    rgb = im[..., :3]; al = im[..., 3]
    ln = line_of(rgb, al); hd = ink(rgb, ln)
    cv2.imwrite(f'{A}/n_{nm}_hd.png', np.dstack([hd, al]))
    lg = (ln * 255).astype(np.uint8)
    cv2.imwrite(f'{A}/n_{nm}_line.png', np.dstack([lg, lg, lg, ((1 - ln) * al).astype(np.uint8)]))
print('round3 images ok')
