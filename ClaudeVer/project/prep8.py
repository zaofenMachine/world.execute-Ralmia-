"""v3: one look for every GPT picture (plan_v3.md, section 8). For each picture asset writes two variants next to it:
  <name>__r.png   raster -- the machine's own display: 1-bit ordered dither (bone / ink) in 3 px cells, her core's cyan kept
  <name>__m.png   two-colour manga print -- black ink + screentone, one spot ink per character (Ralmia's hair ochre,
                  Lishenna's coral), cyan kept where the picture is cyan
lib.surf() swaps them in by register (lib.REG): ink shots read __r, paper shots __m; full colour only at the very end.
usage: python prep8.py [name ...]      (no names: every n_*_hd / n_parts_* / n_*_clean / n_world_flat picture)"""
import os, sys, glob, math
import cv2, numpy as np
from concurrent.futures import ProcessPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets')
src3 = open(os.path.join(HERE, 'prep3.py'), encoding='utf-8').read()
for fn in ('def xdog', 'def line_of'):
    blk = src3[src3.index(fn):]; blk = blk[:blk.index('\n\n')]; exec(blk)

B = lambda h: np.array([int(h[5:7], 16), int(h[3:5], 16), int(h[1:3], 16)], np.float32)   # '#rrggbb' -> BGR
INK, BONE, PAPER, SEPIA, CYAN = B('#080b10'), B('#efe8d8'), B('#efe6d2'), B('#2a2420'), B('#62d8ea')
OCHRE, CORAL = B('#d6a85c'), B('#de8078')
PX = 3                                        # raster cell, px at 1920
SIMPLIFY = ('n_stage', 'n_ledge2', 'n_world', 'n_wL', 'n_lab')   # busy scenes: flatten before the line pass
NO_CYAN = ('n_lish', 'n_cr_hand_l', 'n_stage_hd', 'n_peek_lish')   # Lishenna alone: her costume's teal is not cyan (cyan = Ralmia's core / system only)
# the two of them in one picture: cyan kept only in the x range of Ralmia's side (canvas px)
CYAN_KEEP = {'n_ending_hd': (0, 905), 'n_cube_together_hd': (0, 900), 'n_peek_frozen_hd': (0, 1000),
             'n_ledge2_hd': (995, 1920)}
# the stage and the ledge (user, 2026-10-20: too soft): raster in 2 px cells, error diffusion (Atkinson) instead of the
# ordered 3 px dither, from the picture itself rather than the flattened one
FINE = ('n_stage', 'n_ledge2')
FINE_PX = 2

def masks(base):
    hsv = cv2.cvtColor(base, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    cyan = (h > 80) & (h < 100) & (s > 110) & (v > 140)
    blonde = (h >= 12) & (h <= 32) & (s > 80) & (v > 120)
    pink = ((h <= 6) | (h >= 165)) & (s > 95) & (v > 110)                    # her hair -- not skin, not blush
    pink = cv2.morphologyEx(pink.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)).astype(bool)
    return cyan, blonde, pink

def parts(im, simplify, keep_cyan=True, cyan_x=None):
    """cyan_x: (x0, x1) canvas range where cyan is kept"""
    rgb = im[..., :3]; a = im[..., 3].astype(np.float32) / 255 if im.shape[2] == 4 else np.ones(im.shape[:2], np.float32)
    base = cv2.pyrMeanShiftFiltering(rgb, 10, 28) if simplify else cv2.bilateralFilter(rgb, 9, 40, 9)
    al = im[..., 3] if im.shape[2] == 4 and im[..., 3].min() < 255 else None
    ln = line_of(base if simplify else rgb, al)
    lum = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    cyan, blonde, pink = masks(base)
    if not keep_cyan: cyan = np.zeros_like(cyan)
    if cyan_x is not None:
        k = cyan.shape[1] / 1920; cyan[:, :int(cyan_x[0] * k)] = False; cyan[:, int(cyan_x[1] * k):] = False
    return rgb, a, ln, lum, cyan, blonde, pink

def dots(shape, period, angle):
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float32)
    ca, sa = math.cos(angle), math.sin(angle)
    u, v = (xx * ca + yy * sa) * 2 * math.pi / period, (-xx * sa + yy * ca) * 2 * math.pi / period
    return (np.cos(u) + np.cos(v)) * 0.25 + 0.5

def manga(im, simplify, keep_cyan=True, cyan_x=None):
    rgb, a, ln, lum, cyan, blonde, pink = parts(im, simplify, keep_cyan, cyan_x)
    lum = np.clip((lum - 0.08) / 0.84, 0, 1)
    d = dots(lum.shape, 5.0 * rgb.shape[1] / 960, math.radians(45))
    tone = np.where(lum > 0.78, 1.0, np.where(lum > 0.52, (d > 0.28).astype(np.float32),
                    np.where(lum > 0.26, (d > 0.62).astype(np.float32), 0.0)))
    pen = cv2.erode(ln, np.ones((2, 2), np.uint8))
    out = SEPIA + (PAPER - SEPIA) * (tone * pen)[..., None]
    out[cyan] = CYAN
    for m, col in ((blonde, OCHRE), (pink, CORAL)):                         # the spot inks, overprinted
        mk = cv2.GaussianBlur(cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 1.2)
        mk = np.roll(mk, (2, 2), (0, 1))                                    # a touch of misregistration
        out = out * (1 - mk[..., None] * (1 - col / 255))
    return np.dstack([np.clip(out, 0, 255).astype(np.uint8), (a * 255).astype(np.uint8)])

BAYER = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38],
                  [60, 28, 52, 20, 62, 30, 54, 22], [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                  [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]], np.float32) / 64
def atkinson(small):
    """1-bit error diffusion (Atkinson: 3/4 of the error passed on, so lights and darks stay clean)"""
    sh, sw = small.shape
    e = np.pad(small.astype(np.float32), ((0, 2), (2, 2))); out = np.zeros((sh, sw), np.float32)
    for y in range(sh):
        row, nxt, nn = e[y], e[y + 1], e[y + 2]
        for x in range(sw):
            xx = x + 2; old = row[xx]; new = 1.0 if old > 0.5 else 0.0
            out[y, x] = new; er = (old - new) / 8
            row[xx + 1] += er; row[xx + 2] += er; nxt[xx - 1] += er; nxt[xx] += er; nxt[xx + 1] += er; nn[xx] += er
    return out

def raster(im, simplify, keep_cyan=True, cyan_x=None, px=PX, diffuse=False):
    rgb, a, ln, lum, cyan, blonde, pink = parts(im, simplify, keep_cyan, cyan_x)
    h, w = lum.shape; sw, sh = max(1, int(w / px)), max(1, int(h / px))
    small = cv2.resize(lum * ln, (sw, sh), interpolation=cv2.INTER_AREA)
    small = np.clip((small - 0.06) / 0.86, 0, 1) ** 1.1
    up = lambda x: cv2.resize(x, (w, h), interpolation=cv2.INTER_NEAREST)
    if diffuse: bit = up(atkinson(small))
    else:
        th = np.tile(BAYER, (sh // 8 + 1, sw // 8 + 1))[:sh, :sw]
        bit = up((small > th).astype(np.float32))
    out = INK + (BONE - INK) * bit[..., None]
    cy = up(cv2.resize(cyan.astype(np.float32), (sw, sh), interpolation=cv2.INTER_AREA)) > 0.4
    out[cy] = CYAN
    al = up((cv2.resize(a, (sw, sh), interpolation=cv2.INTER_AREA) > 0.5).astype(np.float32))   # crisp cells at the edge too
    return np.dstack([np.clip(out, 0, 255).astype(np.uint8), (al * 255).astype(np.uint8)])

def one(path):
    name = os.path.basename(path)[:-4]
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if im is None or im.ndim < 3: return name, 'skip'
    simp = any(name.startswith(p) for p in SIMPLIFY)
    kc = not any(name.startswith(p) for p in NO_CYAN)
    cx = CYAN_KEEP.get(name)
    fine = any(name.startswith(p) for p in FINE)
    cv2.imwrite(os.path.join(A, f'{name}__r.png'), raster(im, simp and not fine, kc, cx, FINE_PX if fine else PX, fine))
    cv2.imwrite(os.path.join(A, f'{name}__m.png'), manga(im, simp, kc, cx))
    return name, 'ok'

def targets(names):
    if names: return [os.path.join(A, n + '.png') for n in names]
    pats = ['n_*_hd.png', 'n_parts_*.png', 'n_*_clean.png', 'n_world_flat.png']
    fs = sorted({f for p in pats for f in glob.glob(os.path.join(A, p))})
    return [f for f in fs if '__' not in os.path.basename(f)]

if __name__ == '__main__':
    fs = targets(sys.argv[1:])
    with ProcessPoolExecutor(max(1, (os.cpu_count() or 4) - 2)) as ex:
        res = list(ex.map(one, fs))
    print(len(res), 'pictures,', sum(1 for _, r in res if r == 'ok'), 'treated')
