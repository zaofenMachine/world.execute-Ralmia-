"""Round-1 placeholders (until the second GPT batch arrives).
- n_her_front_hd.png : her front full-body cut out of ref_sheet (stands in for #13 offer_pose), RGBA, 1920x1080 canvas, centred
- n_wL1_night_hd.png / n_wL2_night_hd.png : procedural night versions of world L1 / L2 (stand in for #16a / #16b)
usage: python prep4.py   (run after prep3.py)
"""
import cv2, numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, 'assets'); G = os.path.join(HERE, '..', 'gen')

# ---- her, front view, from the reference sheet
im = cv2.imread(os.path.join(G, 'ref_sheet.png'))
bg = np.median(im.reshape(-1, 3), 0)
d = np.abs(im.astype(int) - bg).sum(2)
m = (d > 34).astype(np.uint8)
m[:, 462:] = 0                                            # the side view starts right of here
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
m = (lab == keep).astype(np.uint8)
# fill holes (paper showing between strands stays, but enclosed holes in the figure close)
ff = m.copy(); h_, w_ = m.shape; mask = np.zeros((h_ + 2, w_ + 2), np.uint8)
cv2.floodFill(ff, mask, (0, 0), 1); holes = (ff == 0); m[holes & (d > 12)] = 1
alpha = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.0)
x, y, w, h = cv2.boundingRect(m)
fig = np.dstack([im, (alpha * 255).astype(np.uint8)])[y:y + h, x:x + w]
# place on a 1920x1080 canvas, figure 960 px tall, centred
s = 960 / h
fig = cv2.resize(fig, (int(w * s), 960), interpolation=cv2.INTER_LANCZOS4)
can = np.zeros((1080, 1920, 4), np.uint8)
x0 = 960 - fig.shape[1] // 2; y0 = 1080 - 960 - 30
can[y0:y0 + 960, x0:x0 + fig.shape[1]] = fig
cv2.imwrite(f'{A}/n_her_front_hd.png', can)
print('her_front', fig.shape, 'core approx', x0 + int((0.5) * fig.shape[1]))

# ---- night sky (L1) : moonlit cloud bands on deep blue, baked stars
L1 = cv2.imread(f'{A}/n_wL1_hd.png').astype(np.float32) / 255
lum = L1.mean(2)
yy = np.linspace(0, 1, 1080)[:, None]
top = np.array([0.20, 0.08, 0.04]); hor = np.array([0.42, 0.26, 0.16])      # BGR deep blue -> dusk blue
grad = top[None, None, :] * (1 - yy[..., None]) + hor[None, None, :] * yy[..., None]
cloud = np.clip((lum - lum.mean()) * 2.2, -0.4, 0.6)
night = grad * (1 + cloud[..., None] * np.array([0.9, 0.95, 1.1]))
rng = np.random.default_rng(5)
for _ in range(900):
    sx, sy = rng.integers(0, 1920), int(rng.random() ** 1.6 * 640)
    b = rng.random() ** 3 * 0.9 + 0.1
    if cloud[sy, sx] > 0.15: continue
    cv2.circle(night, (int(sx), sy), 1 if b < 0.7 else 2, (b * 0.95, b * 0.97, b), -1, cv2.LINE_AA)
cv2.imwrite(f'{A}/n_wL1_night_hd.png', np.clip(night * 255, 0, 255).astype(np.uint8))

# ---- night city (L2): no sun, dark blue stone, warm windows and their reflections
L2 = cv2.imread(f'{A}/n_wL2_hd.png', cv2.IMREAD_UNCHANGED)
rgb = L2[..., :3].astype(np.float32) / 255; al = L2[..., 3].astype(np.float32) / 255
HOR = 682; SUN = (1246, 574)
Y, X = np.mgrid[0:1080, 0:1920]
l2 = rgb.mean(2)
sun = (((X - SUN[0]) ** 2 + (Y - SUN[1]) ** 2) < 112 ** 2) & (Y < HOR) & (l2 > 0.72)
al[sun] = 0
dark = rgb * np.array([0.42, 0.30, 0.24]) + np.array([0.06, 0.03, 0.02])
# water: kill the sun's reflection column
refl = (Y > HOR) & (np.abs(X - SUN[0]) < 170) & (l2 > 0.7)
dark[refl] = np.minimum(dark[refl], np.array([0.42, 0.34, 0.30]))     # soften the sun column into a moon-ish glint
lights = dark.copy()
cand = np.argwhere((al > 0.9) & (Y < HOR - 6) & (Y > 300) & (l2 > 0.45))
pick = cand[rng.choice(len(cand), 420, replace=False)]
for (py, px) in pick:
    c = (0.45 + 0.2 * rng.random(), 0.72 + 0.1 * rng.random(), 1.0)     # warm (BGR)
    cv2.rectangle(lights, (int(px), int(py)), (int(px) + 1, int(py) + 2), c, -1)
    ry = 2 * HOR - py
    if ry < 1080 and al[min(ry, 1079), px] > 0.5:
        cv2.line(lights, (int(px), int(ry)), (int(px), int(ry) + 10), tuple(v * 0.5 for v in c), 1)
out = np.dstack([np.clip(lights * 255, 0, 255), al * 255]).astype(np.uint8)
cv2.imwrite(f'{A}/n_wL2_night_hd.png', out)
print('night ok')
