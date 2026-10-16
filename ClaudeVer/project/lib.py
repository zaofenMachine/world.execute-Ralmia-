"""Small motion-graphics toolkit: cairo vector drawing + fontTools/harfbuzz text + cv2 post."""
import math, random, functools
import numpy as np, cv2, cairo
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

W, H, FPS = 1920, 1080, 60
BPM = 130.0
P = 60.0 / BPM          # one beat
T0 = 0.34               # first downbeat
def B(k):               # time of beat k (k may be fractional; 0.25 = 16th)
    return T0 + k * P

import os
WORK = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette
def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
INK   = hexc('#080b10')
INK2  = hexc('#121822')
BONE  = hexc('#efe8d8')
PAPER = hexc('#efe6d2')
CYAN  = hexc('#62d8ea')
RED   = hexc('#e5484d')
GREY  = hexc('#6b7480')
SEPIA = hexc('#2a2420')

# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def prog(t, a, b):
    if b <= a: return 1.0 if t >= a else 0.0
    return clamp((t - a) / (b - a))
def lerp(a, b, u): return a + (b - a) * u
def eo_cubic(u): u = clamp(u); return 1 - (1 - u) ** 3
def eo_quint(u): u = clamp(u); return 1 - (1 - u) ** 5
def eo_expo(u):  u = clamp(u); return 1.0 if u >= 1 else 1 - 2 ** (-10 * u)
def ei_cubic(u): u = clamp(u); return u ** 3
def eio_cubic(u):
    u = clamp(u); return 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2
def eo_back(u, s=1.70158):
    u = clamp(u) - 1; return 1 + (s + 1) * u ** 3 + s * u ** 2
def eo_elastic(u):
    u = clamp(u)
    if u in (0, 1): return u
    return 2 ** (-10 * u) * math.sin((u * 10 - 0.75) * (2 * math.pi) / 3) + 1
def pulse(t, at, dur=0.25):
    """1 at `at`, exponential decay afterwards."""
    if t < at: return 0.0
    return math.exp(-(t - at) / dur * 4)

# ---------------------------------------------------------------- fonts
class _Pen(BasePen):
    def __init__(self, gs):
        super().__init__(gs); self.ops = []
    def _moveTo(self, p): self.ops.append(('M', p))
    def _lineTo(self, p): self.ops.append(('L', p))
    def _curveToOne(self, a, b, c): self.ops.append(('C', a, b, c))
    def _closePath(self): self.ops.append(('Z',))
    def _endPath(self): self.ops.append(('Z',))

class Font:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.upem = self.tt['head'].unitsPerEm
        self.order = self.tt.getGlyphOrder()
        face = hb.Face(hb.Blob.from_file_path(path))
        self.hb = hb.Font(face)
        os2 = self.tt['OS/2']
        self.cap = (getattr(os2, 'sCapHeight', 0) or int(self.upem * 0.7)) / self.upem
        self.xh = (getattr(os2, 'sxHeight', 0) or int(self.upem * 0.5)) / self.upem
        self._cache = {}
    def ops(self, g):
        if g not in self._cache:
            pen = _Pen(self.gs); self.gs[g].draw(pen); self._cache[g] = pen.ops
        return self._cache[g]
    @functools.lru_cache(maxsize=4096)
    def shape(self, text, track=0.0):
        """-> (list of (glyph, x_em, char_index), width_em). track in em."""
        if not text: return (), 0.0
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": False})
        out, x = [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.order[info.codepoint], (x + pos.x_offset) / self.upem, info.cluster,
                        pos.x_advance / self.upem))
            x += pos.x_advance + track * self.upem
        w = (x - track * self.upem) / self.upem if out else 0
        return tuple(out), w
    def width(self, text, size, track=0.0):
        return self.shape(text, track)[1] * size
    def glyph_path(self, ctx, g, x, y, size):
        s = size / self.upem
        for op in self.ops(g):
            c = op[0]
            if c == 'M': ctx.move_to(x + op[1][0] * s, y - op[1][1] * s)
            elif c == 'L': ctx.line_to(x + op[1][0] * s, y - op[1][1] * s)
            elif c == 'C':
                (a, b, d) = op[1:]
                ctx.curve_to(x + a[0] * s, y - a[1] * s, x + b[0] * s, y - b[1] * s, x + d[0] * s, y - d[1] * s)
            elif c == 'Z': ctx.close_path()
    def glyphs(self, text, x, y, size, align='left', track=0.0):
        """Layout -> list of dict(g, x, y, w, ch, i) in px (baseline y)."""
        gl, w = self.shape(text, track)
        x0 = x - (w * size if align == 'right' else w * size / 2 if align == 'center' else 0)
        res = []
        for n, (g, gx, cl, adv) in enumerate(gl):
            res.append(dict(g=g, x=x0 + gx * size, y=y, w=adv * size, ch=text[cl] if cl < len(text) else '', i=n))
        return res
    def text_path(self, ctx, text, x, y, size, align='left', track=0.0):
        for d in self.glyphs(text, x, y, size, align, track):
            self.glyph_path(ctx, d['g'], d['x'], d['y'], size)

F = {}
def fonts():
    if not F:
        d = WORK + '/fonts/'
        F['heavy'] = Font(d + 'BSD-900.ttf')
        F['bold'] = Font(d + 'BSD-700.ttf')
        F['thin'] = Font(d + 'BSD-300.ttf')
        F['mono'] = Font(d + 'IBMPlexMono-Regular.ttf')
        F['monom'] = Font(d + 'IBMPlexMono-Medium.ttf')
        F['monol'] = Font(d + 'IBMPlexMono-Light.ttf')
        F['serif'] = Font(d + 'InstrumentSerif-Italic.ttf')
        F['serifr'] = Font(d + 'InstrumentSerif-Regular.ttf')
        F['cjk'] = Font(d + 'NotoSerifCJK-Bold-subset.ttf')      # only 넷 六 一二三四五 (subset, OFL)
    return F

# ---------------------------------------------------------------- drawing helpers
def rgba(ctx, c, a=1.0):
    ctx.set_source_rgba(c[0], c[1], c[2], a)

def fill_bg(ctx, c):
    rgba(ctx, c); ctx.paint()

def partial_stroke(ctx, frac, start=0.0, parallel=True):
    """Stroke only fraction [start, frac] of the current path (each sub-path in parallel)."""
    flat = ctx.copy_path_flat(); ctx.new_path()
    subs, cur = [], []
    for kind, pts in flat:
        if kind == cairo.PATH_MOVE_TO:
            if len(cur) > 1: subs.append(cur)
            cur = [pts]
        elif kind == cairo.PATH_LINE_TO: cur.append(pts)
        elif kind == cairo.PATH_CLOSE_PATH:
            if cur: cur.append(cur[0])
    if len(cur) > 1: subs.append(cur)
    if not subs: return
    def draw_sub(pts, a, b):
        segs = [math.dist(pts[i], pts[i+1]) for i in range(len(pts) - 1)]
        L = sum(segs)
        if L <= 0: return
        A, Bv = a * L, b * L
        acc = 0.0; started = False
        for i, s in enumerate(segs):
            p, q = pts[i], pts[i+1]
            s0, s1 = acc, acc + s
            if s1 >= A and s0 <= Bv and s > 0:
                u0 = clamp((A - s0) / s); u1 = clamp((Bv - s0) / s)
                pa = (lerp(p[0], q[0], u0), lerp(p[1], q[1], u0))
                pb = (lerp(p[0], q[0], u1), lerp(p[1], q[1], u1))
                if not started: ctx.move_to(*pa); started = True
                ctx.line_to(*pb)
            acc = s1
    if parallel:
        for s in subs: draw_sub(s, start, frac)
    else:
        lens = []
        for s in subs: lens.append(sum(math.dist(s[i], s[i+1]) for i in range(len(s) - 1)))
        tot = sum(lens); acc = 0
        for s, l in zip(subs, lens):
            a = (start * tot - acc) / l if l else 0; b = (frac * tot - acc) / l if l else 0
            if b > 0 and a < 1: draw_sub(s, clamp(a), clamp(b))
            acc += l
    ctx.stroke()

def line(ctx, x0, y0, x1, y1, c, a=1.0, w=1.5):
    rgba(ctx, c, a); ctx.set_line_width(w); ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.stroke()

def text(ctx, key, s, x, y, size, c, a=1.0, align='left', track=0.0):
    f = fonts()[key]; ctx.new_path(); f.text_path(ctx, s, x, y, size, align, track); rgba(ctx, c, a); ctx.fill()

def text_w(key, s, size, track=0.0):
    return fonts()[key].width(s, size, track)

def type_on(s, t, t0, rate):
    """Characters of s visible at time t, typing starting t0 with `rate` seconds/char."""
    if t < t0: return ''
    return s[:int((t - t0) / rate) + 1]

GLYPHS_SCRAMBLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&*+=/<>'
def scramble(s, t, t0, per, seed=0, settle=0.0):
    """Decode effect: chars resolve one by one every `per` sec starting t0; unresolved chars random."""
    rnd = random.Random(int(t * 30) + seed)
    out = []
    for i, ch in enumerate(s):
        tl = t0 + i * per + settle
        if ch == ' ' or t >= tl: out.append(ch)
        elif t >= t0 + i * per - 0.25: out.append(rnd.choice(GLYPHS_SCRAMBLE))
        else: out.append(' ')
    return ''.join(out)

# ---------------------------------------------------------------- images
_IMG = {}
def surf(name):
    """cairo ImageSurface from assets/<name>.png (BGR or BGRA)."""
    if name not in _IMG:
        im = cv2.imread(f'{WORK}/assets/{name}.png', cv2.IMREAD_UNCHANGED)
        if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGRA)
        elif im.shape[2] == 3: im = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)
        else:  # premultiply
            a = im[..., 3:4].astype(np.float32) / 255
            im = np.concatenate([(im[..., :3] * a).astype(np.uint8), im[..., 3:4]], 2)
        im = np.ascontiguousarray(im)
        s = cairo.ImageSurface.create_for_data(im, cairo.FORMAT_ARGB32, im.shape[1], im.shape[0], im.strides[0])
        _IMG[name] = (s, im)
    return _IMG[name][0]

def draw_img(ctx, name, a=1.0, scale=1.0, cx=W/2, cy=H/2, ox=0.0, oy=0.0, filt=cairo.FILTER_GOOD):
    """Draw image (1920x1080 asset) scaled about (cx,cy) then offset."""
    s = surf(name)
    ctx.save()
    ctx.translate(cx + ox, cy + oy); ctx.scale(scale, scale); ctx.translate(-cx, -cy)
    ctx.set_source_surface(s, 0, 0); ctx.get_source().set_filter(filt)
    ctx.paint_with_alpha(a)
    ctx.restore()

# ---------------------------------------------------------------- textures / post
_rng = np.random.default_rng(7)
GRAIN = [(_rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)) for _ in range(6)]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.32 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.4).clip(0.55, 1)[..., None]

def paper_tex():
    if 'paper' not in _IMG:
        r = np.random.default_rng(3)
        n = r.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
        n = cv2.resize(cv2.GaussianBlur(n, (0, 0), 1.2), (W, H))
        fib = r.normal(0, 1, (H, W)).astype(np.float32)
        fib = cv2.GaussianBlur(fib, (0, 0), sigmaX=6, sigmaY=0.6)
        base = np.array(PAPER[::-1], np.float32) * 255
        img = base[None, None, :] + (n * 5 + fib * 4)[..., None]
        img = np.concatenate([img.clip(0, 255).astype(np.uint8), np.full((H, W, 1), 255, np.uint8)], 2)
        img = np.ascontiguousarray(img)
        s = cairo.ImageSurface.create_for_data(img, cairo.FORMAT_ARGB32, W, H, img.strides[0])
        _IMG['paper'] = (s, img)
    return _IMG['paper'][0]

def paper_bg(ctx):
    ctx.set_source_surface(paper_tex(), 0, 0); ctx.paint()

def post(buf, fr, glow=0.35, ab=0.0, grain=0.035, flash=0.0, vignette=True, glow_thresh=170):
    """buf: HxWx4 uint8 BGRA from cairo. returns HxWx3 uint8 BGR."""
    img = buf[..., :3].astype(np.float32)
    if glow > 0:
        small = cv2.resize(buf[..., :3], (W // 4, H // 4), interpolation=cv2.INTER_AREA).astype(np.float32)
        lum = small.max(2, keepdims=True)
        m = np.clip((lum - glow_thresh) / (255 - glow_thresh), 0, 1)
        b1 = cv2.GaussianBlur(small * m, (0, 0), 3); b2 = cv2.GaussianBlur(small * m, (0, 0), 12)
        g = cv2.resize(b1 * 0.6 + b2 * 0.8, (W, H), interpolation=cv2.INTER_LINEAR)
        img += g * glow
    if ab > 0.3:
        s = int(round(ab))
        b, g_, r = img[..., 0], img[..., 1], img[..., 2]
        r2 = np.roll(r, s, 1); b2_ = np.roll(b, -s, 1)
        img = np.stack([b2_, g_, r2], 2)
    if flash > 0:
        img = img * (1 - flash) + 255 * flash
    if vignette:
        img *= VIG
    if grain > 0:
        gn = cv2.resize(GRAIN[fr % len(GRAIN)], (W, H), interpolation=cv2.INTER_NEAREST)
        img += (gn * 255 * grain)[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)
