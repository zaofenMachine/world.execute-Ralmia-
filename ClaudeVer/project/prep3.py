"""New GPT images (ClaudeVer/gen) -> assets/n_*.png at 1920x1080.
For every image:  n_<name>_full.png (RGB or RGBA), n_<name>_line.png (XDoG line art, grey; RGBA if the source has alpha),
                  n_<name>_hd.png (full image with a light ink pass: line art multiplied in at 25 %, slightly warmed).
Extra:  n_hand_gap_clean.png (painted thread removed), thread_gap.json (thread centre line),
        n_parts_<i>.png (each exploded part cut out, RGBA), parts.json (part boxes, 1920 coords).
usage: python prep3.py
"""
import cv2, numpy as np, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'gen')
A = os.path.join(HERE, 'assets')
S = 1920 / 1672                     # native -> 1920 scale

NAMES = {'hand_palm': 'hand_palm', 'parts_exploded': 'parts', 'eye_open': 'eye_open', 'eye_closed': 'eye_closed',
         'world_L1_sky': 'wL1', 'world_L2_city': 'wL2', 'world_L3_mid': 'wL3', 'world_L4_fore': 'wL4',
         'dash_launch': 'dash_launch', 'dash_full': 'dash_full', 'hand_gap': 'hand_gap', 'hand_tied': 'hand_tied',
         'portrait_front': 'portrait', 'floating': 'floating', 'pinky_promise': 'pinky'}

def xdog(gray, sigma=1.0, k=1.6, p=28, eps=-0.012, phi=14):
    g = gray.astype(np.float32) / 255
    a = cv2.GaussianBlur(g, (0, 0), sigma); b = cv2.GaussianBlur(g, (0, 0), sigma * k)
    d = (1 + p) * a - p * b
    return np.clip(np.where(d >= eps, 1.0, 1 + np.tanh(phi * (d - eps))), 0, 1)

def resize(im):
    if im.shape[2] == 4:
        a = im[..., 3:4].astype(np.float32) / 255
        pm = np.concatenate([im[..., :3] * a, a * 255], 2)
        pm = cv2.resize(pm, (1920, 1081), interpolation=cv2.INTER_LANCZOS4)[:1080]
        al = np.clip(pm[..., 3:4], 0, 255)
        rgb = np.where(al > 0.5, pm[..., :3] / np.maximum(al / 255, 1e-3), 0)
        return np.concatenate([np.clip(rgb, 0, 255), al], 2).astype(np.uint8)
    return cv2.resize(im, (1920, 1081), interpolation=cv2.INTER_LANCZOS4)[:1080]

def line_of(rgb, alpha=None):
    base = rgb.astype(np.float32)
    if alpha is not None:
        a = alpha[..., None].astype(np.float32) / 255
        base = base * a + 255 * (1 - a)
    gray = cv2.cvtColor(cv2.bilateralFilter(base.astype(np.uint8), 7, 30, 5), cv2.COLOR_BGR2GRAY)
    ln = xdog(gray)
    inv = ((1 - ln) > 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 8)
    keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 30
    return np.where(keep[lab], ln, 1.0)

def ink(rgb, ln):
    out = rgb.astype(np.float32) * (0.75 + 0.25 * ln[..., None])
    out = out * np.array([0.97, 1.0, 1.02], np.float32)          # BGR: a touch warmer
    return np.clip(out, 0, 255).astype(np.uint8)

out_info = {}
for src, nm in NAMES.items():
    im = cv2.imread(os.path.join(SRC, src + '.png'), cv2.IMREAD_UNCHANGED)
    im = resize(im)
    rgb = im[..., :3]; al = im[..., 3] if im.shape[2] == 4 else None
    ln = line_of(rgb, al)
    hd = ink(rgb, ln)
    if al is not None:
        cv2.imwrite(f'{A}/n_{nm}_full.png', im)
        cv2.imwrite(f'{A}/n_{nm}_hd.png', np.dstack([hd, al]))
        lg = (ln * 255).astype(np.uint8)
        cv2.imwrite(f'{A}/n_{nm}_line.png', np.dstack([lg, lg, lg, ((1 - ln) * al).astype(np.uint8)]))
    else:
        cv2.imwrite(f'{A}/n_{nm}_full.png', im)
        cv2.imwrite(f'{A}/n_{nm}_hd.png', hd)
        cv2.imwrite(f'{A}/n_{nm}_line.png', (ln * 255).astype(np.uint8))
    out_info[nm] = im.shape
    if nm == 'hand_gap':
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
        m = (((hsv[..., 0] < 10) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 90) & (hsv[..., 2] > 70)).astype(np.uint8)
        m[:, :1340] = 0
        n_, lab_, st_, _ = cv2.connectedComponentsWithStats(m, 8)
        m = (lab_ == 1 + int(np.argmax(st_[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)   # the thread = biggest red blob
        core = m.copy()
        clean = cv2.inpaint(hd, cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=4) * 255, 9, cv2.INPAINT_TELEA)
        cv2.imwrite(f'{A}/n_hand_gap_clean.png', clean)
        ys, xs = np.nonzero(core); pts = []
        for x in range(int(xs.min()), int(xs.max()) + 1, 12):
            sel = np.abs(xs - x) <= 3
            if sel.sum(): pts.append((float(x), float(ys[sel].mean())))
        json.dump(pts, open(f'{A}/thread_gap.json', 'w'))
        print('thread', len(pts), pts[0], pts[-1])
    if nm == 'parts':
        anc = json.load(open(os.path.join(SRC, '_qa', 'anchors.json')))
        boxes = []
        for i, (x0, y0, x1, y1) in enumerate(anc['parts_bounds']):
            X0, Y0, X1, Y1 = int(x0 * S) - 6, int(y0 * S) - 6, int(x1 * S) + 7, int(y1 * S) + 7
            cut = np.dstack([hd, al])[Y0:Y1, X0:X1]
            cv2.imwrite(f'{A}/n_parts_{i}.png', cut); boxes.append((X0, Y0, X1, Y1))
        json.dump(boxes, open(f'{A}/parts.json', 'w'))

# the four world layers flattened into one picture (+ line / flat / ink stages for the Simulation grid)
def over(dst, name):
    im = cv2.imread(f'{A}/n_{name}_hd.png', cv2.IMREAD_UNCHANGED).astype(np.float32)
    if im.shape[2] == 3: return im
    a = im[..., 3:4] / 255
    return im[..., :3] * a + dst * (1 - a)
comp = over(None, 'wL1')
for nm in ('wL2', 'wL3', 'wL4'): comp = over(comp, nm)
comp = comp.astype(np.uint8)
cv2.imwrite(f'{A}/n_world_hd.png', comp)
cv2.imwrite(f'{A}/n_world_line.png', (line_of(comp) * 255).astype(np.uint8))
flat = cv2.pyrMeanShiftFiltering(cv2.resize(comp, (960, 540)), 8, 18)
cv2.imwrite(f'{A}/n_world_flat.png', cv2.bilateralFilter(cv2.resize(flat, (1920, 1080), interpolation=cv2.INTER_CUBIC), 9, 40, 9))
print('ok', out_info)
