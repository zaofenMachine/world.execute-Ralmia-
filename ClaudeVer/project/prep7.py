"""Fourth GPT batch (v2: Lishenna, see ClaudeVer/gen/README_round4.md) -> assets/n_*  (same treatment as prep3/5/6).
New names only -- the v1 assets (n_pinky, n_creation, n_lab, n_creator_*) are left untouched so v1 still renders.
  n_pinky2 / n_pinky2_alone / n_pinky2_alone_clean   pinky_promise_v2 + pinky_alone_v2 (pixel-aligned pair)
  n_creation2                                        creation_inverse_v2 (fingertips where they were in v1)
  n_stage / n_stage_empty / n_stage_screens / n_stage_sticks
  n_lish_walk / n_lish_stand / n_lish_float          transparent; fringe colours decontaminated (no red rim on ink)
  n_lish_face / n_lish_sheet                         from lishenna_ref_sheet, for the simulation windows
  n_lish_front (L7) and n_lish_sing (L8)             only when those files exist in gen/
Anchors (1920 coords) -> ../gen/_qa/round4/anchors_v2.json
usage: python prep7.py          images + anchors
       python prep7.py frag     v2 FRAGMENTS tiles (assets/frag2_*.png + frag2.json) from qa_v2/q*.jpg
"""
import cv2, numpy as np, os, json, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'gen'); A = os.path.join(HERE, 'assets')
src3 = open(os.path.join(HERE, 'prep3.py'), encoding='utf-8').read()
for fn in ('def xdog', 'def resize', 'def line_of', 'def ink'):
    blk = src3[src3.index(fn):]; blk = blk[:blk.index('\n\n')]; exec(blk)          # reuse prep3's helpers
S = 1920 / 1672

def decontaminate(im):
    """RGBA: the semi-transparent fringe takes the colour of the nearest solid pixels (normalised convolution)"""
    rgb = im[..., :3].astype(np.float32); a = im[..., 3]
    solid = (a >= 230).astype(np.float32)
    acc = np.zeros_like(rgb); wsum = np.zeros(a.shape, np.float32)
    for s in (2, 5, 12):
        w = cv2.GaussianBlur(solid, (0, 0), s)
        acc_s = cv2.GaussianBlur(rgb * solid[..., None], (0, 0), s)
        take = (wsum < 1e-3) & (w > 1e-3)
        acc[take] = acc_s[take] / w[take, None]; wsum[take] = 1
    out = rgb.copy(); fr = (a < 230) & (wsum > 0)
    out[fr] = acc[fr]
    return np.dstack([np.clip(out, 0, 255).astype(np.uint8), a])

def save(nm, im):
    rgb = im[..., :3]; al = im[..., 3] if im.shape[2] == 4 else None
    ln = line_of(rgb, al); hd = ink(rgb, ln)
    if al is not None:
        cv2.imwrite(f'{A}/n_{nm}_hd.png', np.dstack([hd, al]))
        lg = (ln * 255).astype(np.uint8)
        cv2.imwrite(f'{A}/n_{nm}_line.png', np.dstack([lg, lg, lg, ((1 - ln) * al).astype(np.uint8)]))
    else:
        cv2.imwrite(f'{A}/n_{nm}_hd.png', hd)
        cv2.imwrite(f'{A}/n_{nm}_line.png', (ln * 255).astype(np.uint8))
    return hd

def load(src, rgba=False):
    im = cv2.imread(os.path.join(SRC, src + '.png'), cv2.IMREAD_UNCHANGED)
    if rgba: im = decontaminate(im)
    return resize(im)

def bottom_centre(al, thr=32):
    ys, xs = np.nonzero(al > thr); b = ys.max(); sel = ys > b - 8
    return float(xs[sel].mean()), float(b), int(ys.min())

def frag(qa_dir='qa_v2', prefix='frag2'):
    """the bridge's memory mosaic: 96 tiles from the contact sheets of the rendered 0-100 s (see prep5.py)"""
    tiles = {}
    for q in sorted(glob.glob(os.path.join(HERE, qa_dir, 'q*.jpg'))):
        s = int(os.path.basename(q)[1:-4]); im = cv2.imread(q)
        for i in range(32):
            r, c = divmod(i, 4); tl = im[r * 225:(r + 1) * 225, c * 400:(c + 1) * 400]
            if tl.size and tl.mean() > 2: tiles[round((s * 32 + i) * 0.25, 2)] = tl
    KEEP = [(16.9, 22.3), (22.5, 28.2), (55.0, 60.6), (63.1, 66.7), (70.6, 74.1), (85.4, 89.0)]   # her, her song, or the red thread
    out = []
    for i, t in enumerate(np.arange(4.0, 100.0, 1.0)):
        tt = min(tiles, key=lambda x: abs(x - t))
        cv2.imwrite(f'{A}/{prefix}_{i:02d}.png', cv2.resize(tiles[tt], (160, 90), interpolation=cv2.INTER_AREA))
        out.append(dict(i=i, t=float(tt), keep=any(a <= tt <= b for a, b in KEEP)))
    json.dump(out, open(f'{A}/{prefix}.json', 'w'))
    print('fragments', len(out), 'keep', sum(o['keep'] for o in out))

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'frag':
    frag(); raise SystemExit

anc = {}
# ---- the pairs
for src, nm in (('pinky_promise_v2', 'pinky2'), ('pinky_alone_v2', 'pinky2_alone'), ('creation_inverse_v2', 'creation2'),
                ('stage', 'stage'), ('stage_empty', 'stage_empty')):
    save(nm, load(src))
print('pairs ok')

# pinky2_alone without the two hanging tails of the thread (the knot stays painted), as prep5 did for v1
im = cv2.imread(f'{A}/n_pinky2_alone_hd.png'); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
m = (((hsv[..., 0] < 10) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 90) & (hsv[..., 2] > 70)).astype(np.uint8)
m[:522] = 0; m[:, :925] = 0; m[:, 1030:] = 0
cv2.imwrite(f'{A}/n_pinky2_alone_clean.png', cv2.inpaint(im, cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=3) * 255, 7, cv2.INPAINT_TELEA))
# the thread knot and the palm core, measured on the new picture (the edit kept them in place; check, don't assume)
im = cv2.imread(f'{A}/n_pinky2_hd.png'); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
red = (((hsv[..., 0] < 10) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 110) & (hsv[..., 2] > 80))
ys, xs = np.nonzero(red[400:650, 850:1060]); anc['pinky2_red_centroid'] = [float(xs.mean() + 850), float(ys.mean() + 400)]
cy_ = (hsv[..., 0] > 80) & (hsv[..., 0] < 100) & (hsv[..., 1] > 120) & (hsv[..., 2] > 150)
ys, xs = np.nonzero(cy_[450:720, 420:700]); anc['pinky2_core_centroid'] = [float(xs.mean() + 420), float(ys.mean() + 450)]

# ---- stage: the three screens (GPT's mask, exact white / black inside) and the light sticks of the crowd
sm = cv2.imread(os.path.join(SRC, '_qa', 'round4', 'stage_screens_mask.png'), cv2.IMREAD_GRAYSCALE)
sm = cv2.resize(sm, (1920, 1081), interpolation=cv2.INTER_LINEAR)[:1080]
sm = cv2.GaussianBlur(sm, (0, 0), 0.7)
cv2.imwrite(f'{A}/n_stage_screens.png', np.dstack([np.zeros_like(sm)] * 3 + [sm]))
ys, xs = np.nonzero(sm > 128); anc['stage_screens_bbox'] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
scr = []
for i in (1, 2, 3):
    m_ = cv2.imread(os.path.join(SRC, '_qa', 'round4', f'stage_screen_{i}_mask.png'), cv2.IMREAD_GRAYSCALE)
    ys, xs = np.nonzero(m_ > 128); scr.append([round(xs.min() * S), round(ys.min() * S), round((xs.max() + 1) * S), round((ys.max() + 1) * S)])
anc['stage_screens'] = scr
st = cv2.imread(f'{A}/n_stage_hd.png'); hsv = cv2.cvtColor(st, cv2.COLOR_BGR2HSV)
sticks = ((hsv[..., 2] > 200) & ((hsv[..., 1] > 60) | (hsv[..., 2] > 235))).astype(np.uint8)
sticks[:880] = 0                                              # the crowd is the bottom strip
sticks = cv2.morphologyEx(sticks, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
sk = cv2.GaussianBlur(sticks.astype(np.float32) * 255, (0, 0), 1.0).astype(np.uint8)
cv2.imwrite(f'{A}/n_stage_sticks.png', np.dstack([np.zeros_like(sk)] * 3 + [sk]))
anc['stage_sticks_px'] = int(sticks.sum())
print('stage ok', scr)

# ---- Lishenna, transparent
wk = load('lishenna_walk', True); save('lish_walk', wk)
fx, fy, top = bottom_centre(wk[..., 3])
anc['lish_walk'] = dict(feet=[round(fx), round(fy)], height=round(fy - top), pinky=[round(600 * S), round(538 * S)])

fl = load('lishenna_float', True); save('lish_float', fl)
ys, xs = np.nonzero(fl[..., 3] > 32)
anc['lish_float'] = dict(centre=[round((xs.min() + xs.max()) / 2), round((ys.min() + ys.max()) / 2)], height=int(ys.max() - ys.min()))

def standing(src, nm, h=1000):
    """a standing cut-out on the 1920 canvas: h px tall, feet at (960, 1050), like n_offer / n_creator_back"""
    sd = cv2.imread(os.path.join(SRC, src + '.png'), cv2.IMREAD_UNCHANGED); sd = decontaminate(sd)
    ys, xs = np.nonzero(sd[..., 3] > 32); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    fig = sd[y0:y1, x0:x1]; s = h / fig.shape[0]
    fa = fig[..., 3:4].astype(np.float32) / 255
    pm = cv2.resize(np.concatenate([fig[..., :3] * fa, fa * 255], 2), (round(fig.shape[1] * s), h), interpolation=cv2.INTER_LANCZOS4)
    al = np.clip(pm[..., 3:4], 0, 255); rgb = np.where(al > 0.5, pm[..., :3] / np.maximum(al / 255, 1e-3), 0)
    fig = np.concatenate([np.clip(rgb, 0, 255), al], 2).astype(np.uint8)
    bx, _, _ = bottom_centre(fig[..., 3])
    can = np.zeros((1080, 1920, 4), np.uint8); ox = int(round(960 - bx))
    xa, xb = max(0, ox), min(1920, ox + fig.shape[1])
    can[1050 - h:1050, xa:xb] = fig[:, xa - ox:xb - ox]
    save(nm, can)
    return dict(feet=[960, 1050], height=h)

anc['lish_stand'] = standing('lishenna_stand', 'lish_stand')

# ---- from the reference sheet: the close-up (a window of her face) and the whole sheet
rs = cv2.imread(os.path.join(SRC, 'lishenna_ref_sheet.png'))
face = rs[150:510, 1020:1660]                                  # 16:9 around the face of the close-up
save('lish_face', cv2.resize(face, (1920, 1080), interpolation=cv2.INTER_CUBIC))
save('lish_sheet', resize(rs))

# ---- L7 / L8, once they are delivered
if os.path.exists(os.path.join(SRC, 'lishenna_front.png')):
    anc['lish_front'] = standing('lishenna_front', 'lish_front')
if os.path.exists(os.path.join(SRC, 'lishenna_sing_profile.png')):
    save('lish_sing', load('lishenna_sing_profile'))

# ---- sixth batch (gen/request_v2c.md), whichever have arrived. pairs are resized identically, so they stay aligned
R6 = [('creation_plate', 'cr_plate', False), ('creation_hand_ralmia', 'cr_hand_r', True), ('creation_hand_lishenna', 'cr_hand_l', True),
      ('cube_together', 'cube_together', True), ('cube_alone', 'cube_alone', True),
      ('ledge_together', 'ledge2', False), ('ledge_alone', 'ledge2_alone', False),
      ('cat_ralmia_v2', 'cat2', True), ('cat_ralmia_v2b', 'cat2b', True),
      ('lishenna_sit', 'lish_sit', True), ('lishenna_sit_b', 'lish_sit_b', True), ('ending_together', 'ending', True)]
for src, nm, rgba_ in R6:
    if os.path.exists(os.path.join(SRC, src + '.png')):
        save(nm, load(src, rgba_)); print('round 6:', nm)
if os.path.exists(f'{A}/n_ending_hd.png'):                     # the chest-up crop ends in a hard line: feather it
    for suf in ('_hd', '_line'):
        im = cv2.imread(f'{A}/n_ending{suf}.png', cv2.IMREAD_UNCHANGED)
        ys, _ = np.nonzero(im[..., 3] > 32); b = ys.max()
        ramp = np.clip((b - np.arange(1080)) / 170.0, 0, 1)[:, None]
        im[..., 3] = (im[..., 3] * ramp).astype(np.uint8); cv2.imwrite(f'{A}/n_ending{suf}.png', im)
# Lishenna alone, cut out of each pair (what is in "together" and not in "alone"): the select box, the points she becomes
if os.path.exists(f'{A}/n_cube_alone_hd.png'):
    t_ = cv2.imread(f'{A}/n_cube_together_hd.png', cv2.IMREAD_UNCHANGED); a_ = cv2.imread(f'{A}/n_cube_alone_hd.png', cv2.IMREAD_UNCHANGED)
    m = ((t_[..., 3] > 128) & (a_[..., 3] < 64)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    ys, xs = np.nonzero(m); anc['cube_lish_bbox'] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    ys, xs = np.nonzero(t_[..., 3] > 32); anc['cube_together'] = dict(feet=[int((xs.min() + xs.max()) / 2), int(ys.max())], height=int(ys.max() - ys.min()))
if os.path.exists(f'{A}/n_ledge2_alone_hd.png'):
    t_ = cv2.imread(f'{A}/n_ledge2_hd.png').astype(int); a_ = cv2.imread(f'{A}/n_ledge2_alone_hd.png').astype(int)
    m = (np.abs(t_ - a_).sum(2) > 40).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n_, lab_, st_, _ = cv2.connectedComponentsWithStats(m, 8)
    big = 1 + np.argsort(st_[1:, cv2.CC_STAT_AREA])[::-1][:3]                 # her, and her two speaker discs
    m = np.isin(lab_, big[st_[big, cv2.CC_STAT_AREA] > 400]).astype(np.float32)
    al = (cv2.GaussianBlur(m, (0, 0), 1.0) * 255).astype(np.uint8)
    cv2.imwrite(f'{A}/n_ledge2_lish.png', np.dstack([t_.astype(np.uint8), al]))
    ys, xs = np.nonzero(m); anc['ledge2_lish_bbox'] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

# ---- round 2: the two faces as oscilloscope traces (44-48 s, X-Y mode): line strength as an A8-style mask, 960x540,
# both heads the same height and centred, lines thickened a little so they survive as phosphor
def scope_mask(ln, box, nm, h=820):
    x0, y0, x1, y1 = box
    m = (1 - ln[y0:y1, x0:x1]).astype(np.float32)
    s = h / m.shape[0]; m = cv2.resize(m, (round(m.shape[1] * s), h), interpolation=cv2.INTER_AREA)
    m = cv2.dilate(m, np.ones((2, 2), np.uint8))
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]].astype(np.float32)          # soft edges: no square crop
    d = ((xx / m.shape[1] - 0.5) / 0.5) ** 2 + ((yy / m.shape[0] - 0.42) / 0.58) ** 2
    m *= np.clip((1.0 - d) / 0.35, 0, 1)
    can = np.zeros((1080, 1920), np.float32); ox = 960 - m.shape[1] // 2; oy = 560 - h // 2
    can[oy:oy + h, ox:ox + m.shape[1]] = m
    can = cv2.resize(can, (960, 540), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'{A}/n_scope_{nm}.png', np.clip(can * 1.35 * 255, 0, 255).astype(np.uint8))
ra = cv2.imread(f'{A}/n_portrait2_line.png', cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
scope_mask(ra, (500, 0, 1500, 1080), 'ralmia')
rs_ln = line_of(rs)                                             # the reference sheet's close-up, native 1672 px
scope_mask(rs_ln, (1040, 50, 1672, 760), 'lish')

# ---- round 3: the figures of 39-44 s as phosphor line art (like the AC/DC faces): line strength as a grey mask on the
# 1920 canvas scaled by TRACE_F, lines found at that size (so they stay solid), plus the silhouette edge
TRACE_F = 0.6
def trace_mask(src_png, nm):
    if not os.path.exists(f'{A}/{src_png}.png'): return
    im = cv2.imread(f'{A}/{src_png}.png', cv2.IMREAD_UNCHANGED)
    w, h = round(1920 * TRACE_F), round(1080 * TRACE_F)
    a = cv2.resize(im[..., 3], (w, h), interpolation=cv2.INTER_AREA)
    rgb = cv2.resize(im[..., :3], (w, h), interpolation=cv2.INTER_AREA)
    ln = line_of(rgb, a)
    m = (1 - ln) * (a.astype(np.float32) / 255)
    edge = cv2.Canny((a > 110).astype(np.uint8) * 255, 50, 150).astype(np.float32) / 255
    m = np.maximum(m, cv2.GaussianBlur(edge, (0, 0), 0.6) * 1.4)
    cv2.imwrite(f'{A}/n_trace_{nm}.png', np.clip(m * 255, 0, 255).astype(np.uint8))
for src_png, nm in (('n_lish_sit_hd', 'sit'), ('n_lish_sit_b_hd', 'sit_b'), ('n_dash_full_hd', 'dash')):
    trace_mask(src_png, nm)

json.dump(anc, open(os.path.join(SRC, '_qa', 'round4', 'anchors_v2.json'), 'w'), indent=1)
print(json.dumps(anc, indent=1))
