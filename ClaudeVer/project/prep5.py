"""Second GPT batch (ClaudeVer/gen, see README_round2.md) -> assets/n_*  (same treatment as prep3.py).
listen_profile and reach_camera are mirrored: the temple gem was painted on the wrong side (feedback_round2.md).
Also builds the FRAGMENTS contact sheet from qa/q*.jpg (every 0.25 s of the rendered film): assets/frag_*.png + frag.json.
usage: python prep5.py   (run qa.py on a render that covers 0-103.7 s first)
"""
import cv2, numpy as np, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'gen'); A = os.path.join(HERE, 'assets')
src3 = open(os.path.join(HERE, 'prep3.py')).read()
for fn in ('def xdog', 'def resize', 'def line_of', 'def ink'):
    blk = src3[src3.index(fn):]; blk = blk[:blk.index('\n\n')]; exec(blk)          # reuse prep3's helpers

NAMES = {'creator_sheet': 'creator_sheet', 'lab_desk': 'lab', 'lab_desk_empty': 'lab_empty', 'pinky_alone': 'pinky_alone',
         'offer_pose': 'offer', 'spec_eggplant': 'spec_egg', 'spec_tomato': 'spec_tomato', 'spec_tabbycat': 'spec_cat',
         'creation_inverse': 'creation', 'world_L1_night': 'wL1n', 'world_L2_city_night': 'wL2n', 'eye_tear': 'eye_tear',
         'sitting_alone': 'sitting', 'back_reach': 'back_reach', 'reach_camera': 'reach', 'creator_walk': 'creator_walk',
         'listen_profile': 'listen', 'run_front': 'run_front', 'blackboard': 'blackboard', 'escape_leap': 'escape',
         'portrait_front_v2': 'portrait2'}
FLIP = {'listen_profile', 'reach_camera'}

for src, nm in NAMES.items():
    im = cv2.imread(os.path.join(SRC, src + '.png'), cv2.IMREAD_UNCHANGED)
    if src in FLIP: im = im[:, ::-1].copy()
    im = resize(im)
    rgb = im[..., :3]; al = im[..., 3] if im.shape[2] == 4 else None
    ln = line_of(rgb, al); hd = ink(rgb, ln)
    if al is not None:
        cv2.imwrite(f'{A}/n_{nm}_hd.png', np.dstack([hd, al]))
        lg = (ln * 255).astype(np.uint8)
        cv2.imwrite(f'{A}/n_{nm}_line.png', np.dstack([lg, lg, lg, ((1 - ln) * al).astype(np.uint8)]))
    else:
        cv2.imwrite(f'{A}/n_{nm}_hd.png', hd)
        cv2.imwrite(f'{A}/n_{nm}_line.png', (ln * 255).astype(np.uint8))
print('round2 images ok')

# ---- FRAGMENTS: tiles from the QA contact sheets (each sheet: 4 x 8 tiles of 400x225, one tile per 0.25 s)
tiles = {}
for q in sorted(glob.glob(os.path.join(HERE, 'qa', 'q*.jpg'))):
    s = int(os.path.basename(q)[1:-4]); im = cv2.imread(q)
    for i in range(32):
        r, c = divmod(i, 4); tl = im[r * 225:(r + 1) * 225, c * 400:(c + 1) * 400]
        if tl.size and tl.mean() > 2: tiles[round((s * 32 + i) * 0.25, 2)] = tl
KEEP = [(22.5, 28.2), (55.0, 60.6), (63.1, 66.7), (70.6, 74.1), (85.4, 89.0), (96.4, 99.9)]   # him, or the red thread
times = [t for t in np.arange(4.0, 100.0, 1.0)]                                                  # 96 tiles = 12 x 8
out = []
for i, t in enumerate(times):
    tt = min(tiles, key=lambda x: abs(x - t))
    cv2.imwrite(f'{A}/frag_{i:02d}.png', cv2.resize(tiles[tt], (160, 90), interpolation=cv2.INTER_AREA))
    out.append(dict(i=i, t=float(tt), keep=any(a <= tt <= b for a, b in KEEP)))
json.dump(out, open(f'{A}/frag.json', 'w'))
print('fragments', len(out), 'keep', sum(o['keep'] for o in out))

# ---- pinky_alone without the two hanging tails of the thread (the knot stays painted); tails are redrawn as vectors
im = cv2.imread(f'{A}/n_pinky_alone_hd.png'); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
m = (((hsv[..., 0] < 10) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 90) & (hsv[..., 2] > 70)).astype(np.uint8)
m[:522] = 0; m[:, :925] = 0; m[:, 1030:] = 0
cv2.imwrite(f'{A}/n_pinky_alone_clean.png', cv2.inpaint(im, cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=3) * 255, 7, cv2.INPAINT_TELEA))
print('pinky_alone_clean ok')

# ---- the creator, standing, back view, cut out of creator_sheet (paper keyed out) -> n_creator_back_hd (1920 canvas, feet at (960, 1050))
im = cv2.imread(os.path.join(SRC, 'creator_sheet.png'))
bg = np.median(im.reshape(-1, 3), 0)
d = np.abs(im.astype(int) - bg).sum(2)
m = (d > 34).astype(np.uint8); m[:, 470:] = 0
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n_, lab_, st_, _ = cv2.connectedComponentsWithStats(m, 8)
m = (lab_ == 1 + int(np.argmax(st_[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
ff = m.copy(); mk = np.zeros((m.shape[0] + 2, m.shape[1] + 2), np.uint8); cv2.floodFill(ff, mk, (0, 0), 1); m[ff == 0] = 1
al = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.0)
x, y, w, h = cv2.boundingRect(m)
fig = np.dstack([im, (al * 255).astype(np.uint8)])[y:y + h, x:x + w]
s = 1000 / h; fig = cv2.resize(fig, (int(w * s), 1000), interpolation=cv2.INTER_LANCZOS4)
can = np.zeros((1080, 1920, 4), np.uint8); x0 = 960 - fig.shape[1] // 2
can[50:1050, x0:x0 + fig.shape[1]] = fig
rgb = can[..., :3]; ln = line_of(rgb, can[..., 3]); cv2.imwrite(f'{A}/n_creator_back_hd.png', np.dstack([ink(rgb, ln), can[..., 3]]))
print('creator_back ok', fig.shape)

# ---- the three monitors in lab_desk as an alpha mask (his head stays in front)
lab = cv2.imread(f'{A}/n_lab_hd.png'); gl = cv2.cvtColor(lab, cv2.COLOR_BGR2GRAY)
sm = cv2.morphologyEx((gl > 196).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
sm[380:] = 0; sm[:100] = 0
sm = cv2.GaussianBlur(sm.astype(np.float32) * 255, (0, 0), 0.8).astype(np.uint8)
cv2.imwrite(f'{A}/n_lab_screens.png', np.dstack([np.zeros_like(sm)] * 3 + [sm]))
print('lab screens ok')
