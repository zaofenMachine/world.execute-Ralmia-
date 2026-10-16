"""Extra assets for the 0-60 s pass (run after prep.py).
- world_open_F_flat.png : flat-colour stage without line art (for the Simulation "render stages")
- hand_gap_C2_clean.png  : hand_gap_C2_hd with the painted red thread removed, so the thread can be animated in code
- thread_C2.json         : centre line of the painted thread (image coords), used to redraw it as a vector
usage: python prep2.py
"""
import cv2, numpy as np, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, 'assets')

# 1) flat stage of the world (same filter chain as prep.py, minus the line multiply)
im = cv2.imread(f'{A}/world_open_F_full.png')
flat = cv2.pyrMeanShiftFiltering(cv2.resize(im, (960, 540)), 8, 16)
flat = cv2.resize(flat, (1920, 1080), interpolation=cv2.INTER_CUBIC)
flat = cv2.bilateralFilter(flat, 9, 40, 9)
cv2.imwrite(f'{A}/world_open_F_flat.png', flat)

# 2) remove the painted red thread from the hand
hd = cv2.imread(f'{A}/hand_gap_C2_hd.png')
hsv = cv2.cvtColor(hd, cv2.COLOR_BGR2HSV)
m = (((hsv[..., 0] < 10) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 90) & (hsv[..., 2] > 70)).astype(np.uint8)
m[:, :1340] = 0
core = m.copy()
m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=4)
clean = cv2.inpaint(hd, m * 255, 9, cv2.INPAINT_TELEA)
cv2.imwrite(f'{A}/hand_gap_C2_clean.png', clean)

# 3) thread centre line (x -> mean y), resampled every 12 px
ys, xs = np.nonzero(core)
pts = []
for x in range(int(xs.min()), int(xs.max()) + 1, 12):
    sel = np.abs(xs - x) <= 3
    if sel.sum(): pts.append((float(x), float(ys[sel].mean())))
json.dump(pts, open(f'{A}/thread_C2.json', 'w'))
print('ok', len(pts), 'thread points', pts[0], pts[-1])
