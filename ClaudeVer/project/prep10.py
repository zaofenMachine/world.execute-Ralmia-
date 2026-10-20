"""v3 round 8 (gen/request_v3a.md): the pictures of the time-stop shots, same treatment as prep7.py (fringe colours
decontaminated, 1672x941 -> the 1920x1080 canvas, XDoG line + ink pass), then prep8.py for their raster / manga.
  peek_frozen        -> n_peek_frozen      A2: Lishenna leans in to the held Ralmia (Ralmia left, a clear gap)
  lishenna_wink      -> n_lish_wink        A3: through Ralmia's held optics
  lishenna_wave_back -> n_lish_wave_back   A4: strolling off, a wave over her shoulder
  ralmia_frozen_34   -> n_ralmia_frozen    A1 / A4: Ralmia held mid-dash, three-quarter front
Anchors (1920 canvas) -> ../gen/_qa/round8/anchors_v3.json.   usage: python prep10.py"""
import os, json, subprocess, sys
import cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets'); SRC = os.path.join(HERE, '..', 'gen')
src3 = open(os.path.join(HERE, 'prep3.py'), encoding='utf-8').read()
for fn in ('def xdog', 'def resize', 'def line_of', 'def ink'):
    blk = src3[src3.index(fn):]; blk = blk[:blk.index('\n\n')]; exec(blk)
src7 = open(os.path.join(HERE, 'prep7.py'), encoding='utf-8').read()
for fn in ('def decontaminate', 'def save', 'def load', 'def bottom_centre'):
    blk = src7[src7.index(fn):]; blk = blk[:blk.index('\n\n')]; exec(blk)

PICS = [('peek_frozen', 'peek_frozen'), ('lishenna_wink', 'lish_wink'), ('lishenna_wave_back', 'lish_wave_back'),
        ('ralmia_frozen_34', 'ralmia_frozen')]
anc = {}
for src, nm in PICS:
    im = load(src, True); save(nm, im)
    al = im[..., 3]
    ys, xs = np.nonzero(al > 128)
    anc[nm] = dict(box=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())])
    if nm == 'lish_wave_back':
        fx, fy, top = bottom_centre(al); anc[nm].update(feet=[round(fx), round(fy)], height=round(fy - top))
    if nm == 'peek_frozen':                    # two figures, apart: held Ralmia (raster) and Lishenna (line) drawn separately
        k, lab, st, cen = cv2.connectedComponentsWithStats((al > 128).astype(np.uint8), 8)
        big = sorted(range(1, k), key=lambda i: -st[i, 4])[:2]
        rl, ll = sorted(big, key=lambda i: cen[i][0])          # left = Ralmia, right = Lishenna
        dr = cv2.distanceTransform((lab != rl).astype(np.uint8), cv2.DIST_L2, 5)
        dl = cv2.distanceTransform((lab != ll).astype(np.uint8), cv2.DIST_L2, 5)
        for who, keep in (('peek_ralmia', dr <= dl), ('peek_lish', dl < dr)):
            part = im.copy(); part[..., 3] = np.where(keep, al, 0); save(who, part)
        anc[nm]['left_area'], anc[nm]['right_area'] = int(st[rl, 4]), int(st[ll, 4])
    if nm == 'ralmia_frozen':                  # her forward hand: the right-most solid pixels
        rx = xs.max(); sel = xs > rx - 30; anc[nm]['tip'] = [int(rx), int(ys[sel].mean())]
os.makedirs(os.path.join(SRC, '_qa', 'round8'), exist_ok=True)
json.dump(anc, open(os.path.join(SRC, '_qa', 'round8', 'anchors_v3.json'), 'w'), indent=1)
print(json.dumps(anc))
subprocess.run([sys.executable, os.path.join(HERE, 'prep8.py')] + [f'n_{nm}_hd' for _, nm in PICS] + ['n_peek_ralmia_hd', 'n_peek_lish_hd'], check=True)
