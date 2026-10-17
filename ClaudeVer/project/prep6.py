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

# ---- her hand from pinky_alone (thread tails already painted out: n_pinky_alone_clean), paper keyed out -> n_pinky_hand_cut
im = cv2.imread(f'{A}/n_pinky_alone_clean.png')
bg = np.median(im[:200].reshape(-1, 3), 0)
d = np.abs(im.astype(int) - bg).sum(2)
m = (d > 40).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
n_, lab_, st_, _ = cv2.connectedComponentsWithStats(m, 8)
m = (lab_ == 1 + int(np.argmax(st_[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
ff = m.copy(); mk = np.zeros((m.shape[0] + 2, m.shape[1] + 2), np.uint8); cv2.floodFill(ff, mk, (0, 0), 1); m[ff == 0] = 1
al = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.0)
cv2.imwrite(f'{A}/n_pinky_hand_cut.png', np.dstack([im, (al * 255).astype(np.uint8)]))
print('pinky hand cut ok')
