"""v3-only shots. render.py puts OVERRIDE in front of the v2 TIMELINE when V3 is on; v2's own scenes stay as they were.

22.5-28 s (plan_v3_chase.md, A): at the speed of light her own time (proper time, tau) stops. Everything that is hers
-- her body, the streaks of LIGHT hanging in the air, her panel (panel.FREEZE) -- is held, drawn as the raster of a
held frame; the only things still moving are Lishenna (line art) and her song (lavender rings). The fastest machine is
not out-run: she is caught, by someone strolling. Cuts land on the off-beat accents k48.5, 50.5, ... (one every 2 beats).
  A0 k48     out of the white of LIGHT, the white dithers away: the frame is already held
  A1 k48.5   wide: Ralmia held mid-dash; Lishenna strolls in from the right and stops in front of her; two clocks
  A2 k52.5   close two-shot: Lishenna leans in to look at the held face (no contact)       [V3-1 peek_frozen]
  A3 k54.5   through Ralmia's held optics: Lishenna leans into the lens, winks             [V3-2 lishenna_wink]
  A4 k56.5   she strolls off, glancing back; the held frame cracks from Ralmia's fingertip [V3-3 lishenna_wave_back]
  A5 k58.5   the cracks run over the frame, k59.5 it shatters, white -> k60 world.execute(me); time runs again
The pictures in [] are round 8 (gen/request_v3a.md, prep10.py); without them the shots fall back to v2 stand-ins."""
from lib import *
import lib, random
import scenes3 as S3
import panel as PNL

def _has(name): return os.path.exists(f'{WORK}/assets/{name}.png')

_M = {}
def line_mask(name):
    """A8 surface of a line picture's strokes (dark lines on white or on transparent -> opaque)"""
    if name not in _M:
        im = cv2.imread(f'{WORK}/assets/{name}.png', cv2.IMREAD_UNCHANGED)
        if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        g_ = cv2.cvtColor(im[..., :3], cv2.COLOR_BGR2GRAY).astype(np.float32)
        a = im[..., 3].astype(np.float32) / 255 if im.shape[2] == 4 else np.ones_like(g_)
        m = np.clip((255 - g_) * a * 1.6, 0, 255)
        hh, ww = m.shape; st = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, ww)
        buf = np.zeros((hh, st), np.uint8); buf[:, :ww] = m.astype(np.uint8)
        _M[name] = (cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_A8, ww, hh, st), buf)
    return _M[name][0]

def lines_at(c, g, name, x, y, sc, anchor, col=BONE, a=1.0, ga=0.35):
    for cc, aa in ((c, a), (g, a * ga)):
        cc.save(); cc.translate(x, y); cc.scale(sc, sc); cc.translate(-anchor[0], -anchor[1])
        rgba(cc, col, aa); cc.mask_surface(line_mask(name), 0, 0); cc.restore()

def img_at(c, name, x, y, sc, anchor, a=1.0):
    c.save(); c.translate(x, y); c.scale(sc, sc); c.translate(-anchor[0], -anchor[1])
    c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a); c.restore()

# her held dash: the round-8 three-quarter picture if it is there (prep10.py), else v2's side-on dash. fingertip, canvas px
HELD, R_TIP = ('n_ralmia_frozen_hd', (1774, 586)) if _has('n_ralmia_frozen_hd') else ('n_dash_full_hd', (1760, 535))
R_FACE = (1468, 345)                              # (n_dash_full_hd) for the A2 stand-in
WAVE_FEET = (875, 994)                            # n_lish_wave_back: bottom centre (gen/_qa/round8/anchors_v3.json)
WINK_DISC = (549, 471)                            # n_lish_wink: her right speaker disc
PEEK_DISC = (1653, 344)                           # n_peek_frozen: Lishenna's far speaker disc

def stroll(c, g, x, feet_y, sc, t, walking, a=1.0):
    """Lishenna strolling to the LEFT (the v2 stroll pair, mirrored): A/B by beat while walking. Returns her mic."""
    b = walking and int(math.floor((t - T0) / P)) % 2 == 1
    for cc in (c, g):
        cc.save(); cc.translate(x, 0); cc.scale(-1, 1); cc.translate(-x, 0)
    S3.phosphor(c, g, 'stroll_b' if b else 'stroll_a', x, feet_y, sc, S3.L_FEET, t, BONE, a, 0.0, 1.0, 1.0, 0.35)
    for cc in (c, g): cc.restore()
    return (x - (S3.L_MIC[0] - S3.L_FEET[0]) * sc, feet_y + (S3.L_MIC[1] - S3.L_FEET[1]) * sc)

def song_rings(c, g, x, y, t, rmax=900, a=0.5, n=3):
    """her song, still moving: a ring out of her speaker on each accent (every 2 beats, on the off-beat)"""
    kk = (t - T0) / P
    for j in range(n):
        ka = 48.5 + 2 * (math.floor((kk - 48.5) / 2) - j)
        u = (t - B(ka)) / (2.6 * P)
        if not 0 <= u < 1: continue
        for cc, aa, lw in ((c, a, 2.2), (g, a * 0.6, 5)):
            rgba(cc, LISH, aa * (1 - u) ** 1.5); cc.set_line_width(lw); cc.new_path()
            cc.arc(x, y, 30 + rmax * eo_cubic(u), 0, 6.283); cc.stroke()

_rng = np.random.default_rng(3)
SHARDS = [(_rng.uniform(-100, W), _rng.uniform(70, H - 70), _rng.uniform(30, 280), _rng.uniform(0.15, 0.6), _rng.uniform(1, 3))
          for _ in range(150)]
def held_streaks(c, t, a=1.0, sc=1.0):
    """the streaks of LIGHT, stopped in the air, drifting a hair (so the hold never reads as a stuck frame)"""
    dt = t - B(48)
    for x, y, L, aa, w in SHARDS:
        rgba(c, BONE, aa * a); c.rectangle(x + dt * 3 * sc, y, L * sc, w); c.fill()

def tau_label(c, x, y, a=1.0):
    tf = PNL.FREEZE_T
    text(c, 'math', 'τ', x, y, 30, CYAN, 0.95 * a)
    text(c, 'monom', f'{int(tf // 60):02d}:{tf % 60:05.2f}', x + 26, y, 26, CYAN, 0.95 * a)
    text(c, 'monom', 'HOLD', x, y + 30, 17, CYAN, 0.7 * a, track=0.2)

def t_label(c, x, y, t, a=1.0):
    text(c, 'math', 't', x, y, 30, BONE, 0.9 * a)
    text(c, 'monom', f'{int(t // 60):02d}:{t % 60:05.2f}  →', x + 22, y, 26, BONE, 0.9 * a)

def push(c, g, u, k=0.035):
    s_ = 1 + k * u
    for cc in (c, g): cc.save(); cc.translate(W / 2, H / 2); cc.scale(s_, s_); cc.translate(-W / 2, -H / 2)
def pop(c, g):
    for cc in (c, g): cc.restore()

# ---------------------------------------------------------------- the shots
def a1(c, g, t):
    kk = (t - T0) / P
    held_streaks(c, t)
    img_at(c, HELD, 560, 560, 0.62, (960, 540))
    tau_label(c, 250, 820)
    walk = prog(t, B(48.75), B(51.5))
    lx = lerp(2150, 1450, walk)
    mic = stroll(c, g, lx, 930, 0.62, t, 0 < walk < 1)
    song_rings(c, g, mic[0], mic[1], t, 1000)
    t_label(c, lx - 110, 300, t, eo_cubic(prog(t, B(49.2), B(49.6))))
    ub = eo_expo(prog(t, B(48.5), B(48.5) + 0.25))         # the keyword lands on the first accent
    if ub > 0:
        c.save(); c.translate(120, 250); c.scale(lerp(1.12, 1, ub), lerp(1.12, 1, ub))
        text(c, 'math', 'Δτ = 0', 0, 0, 150, BONE, 0.95 * ub); c.restore()

def a2(c, g, t):
    if _has('n_peek_ralmia_hd'):                      # V3-1: held Ralmia in raster, Lishenna alive in line, a hand's width apart
        u = prog(t, B(52.5), B(54.5))
        held_streaks(c, t, 0.4, 1.6)
        img_at(c, 'n_peek_ralmia_hd', 960, 540, 1.0, (960, 540))
        lean = 10 * eo_cubic(u)                           # she leans in a little closer: the only thing moving
        lines_at(c, g, 'n_peek_lish_line', 960 - lean, 540 + 0.4 * lean, 1.0, (960, 540), BONE, 1.0, 0.5)
        song_rings(c, g, PEEK_DISC[0] - lean, PEEK_DISC[1], t, 800, 0.45)
        tau_label(c, 120, 1000)
        return
    # stand-in: her held face, big, left; Lishenna (the stroll, held) close in front of it
    held_streaks(c, t, 0.4, 1.6)
    img_at(c, 'n_dash_full_hd', 600, 470, 1.8, R_FACE)
    sc = 1.3; fx_, fy_ = 1250, 330
    mic = stroll(c, g, fx_ + (840 - S3.L_FEET[0]) * sc, fy_ + (S3.L_FEET[1] - 190) * sc, sc, t, False)
    song_rings(c, g, mic[0], mic[1], t, 900, 0.4)
    tau_label(c, 120, 1000)

def a3(c, g, t):
    u = prog(t, B(54.5), B(56.5))
    held_streaks(c, t, 0.45, 1.3)
    face = 'n_lish_wink_line' if _has('n_lish_wink_line') else 'n_lish_face_line'
    sc = lerp(0.78, 0.84, eo_cubic(u))                      # she leans in, the only thing that moves
    lines_at(c, g, face, 980, 600, sc, (960, 540))
    dx, dy = (WINK_DISC if face == 'n_lish_wink_line' else (400, 420))
    song_rings(c, g, 980 + (dx - 960) * sc, 600 + (dy - 540) * sc, t, 760, 0.45)
    for (sx, sy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):    # her optics' frame, held
        x0, y0 = 960 + sx * 820, 540 + sy * 430
        for cc, aa in ((c, 0.9), (g, 0.4)):
            line(cc, x0, y0, x0 - sx * 70, y0, CYAN, aa, 2.5); line(cc, x0, y0, x0, y0 - sy * 70, CYAN, aa, 2.5)
    text(c, 'monom', 'OPTICS', 180, 160, 20, CYAN, 0.85, track=0.2); text(c, 'mono', 'frame held', 180, 188, 18, CYAN, 0.6)
    tau_label(c, 180, 930)

_cr = np.random.default_rng(11)
def _crack(i, n_seg, spread):
    r = np.random.default_rng(100 + i); ang = r.uniform(-math.pi, math.pi); pts = [(0.0, 0.0)]
    for j in range(n_seg):
        ang += r.uniform(-0.5, 0.5); L = r.uniform(40, 120) * spread
        pts.append((pts[-1][0] + math.cos(ang) * L, pts[-1][1] + math.sin(ang) * L))
    return pts
CRACKS = [(56.75 + 0.2 * i, _crack(i, 6, 1.0)) for i in range(8)] + [(58.5 + 0.06 * i, _crack(20 + i, 9, 1.9)) for i in range(18)]
def cracks(c, g, ox, oy, t):
    for k0, pts in CRACKS:
        u = prog(t, B(k0), B(k0 + 0.5))
        if u <= 0: continue
        n = (len(pts) - 1) * eo_cubic(u)                   # segments drawn so far
        for cc, aa, lw in ((c, 0.9, 1.5), (g, 0.55, 3.5)):
            rgba(cc, CYAN, aa); cc.set_line_width(lw); cc.move_to(ox, oy)
            for j in range(1, int(n) + 1): cc.line_to(ox + pts[j][0], oy + pts[j][1])
            fr_ = n - int(n)
            if int(n) < len(pts) - 1 and fr_ > 0:
                p0, p1 = pts[int(n)], pts[int(n) + 1]
                cc.line_to(ox + lerp(p0[0], p1[0], fr_), oy + lerp(p0[1], p1[1], fr_))
            cc.stroke()

A4_R = (640, 620, 1.05)
def a4(c, g, t):
    u = prog(t, B(56.5), B(59.5))
    held_streaks(c, t)
    wave = _has('n_lish_wave_back_line')
    back, feet = ('n_lish_wave_back_line', WAVE_FEET) if wave else ('n_lish_walk_line', (960, 1050))
    sc = lerp(0.70, 0.46, eo_cubic(u)); fy = lerp(880, 760, eo_cubic(u))   # strolling off into the distance
    lines_at(c, g, back, 1690, fy, sc, feet, BONE, 1.0, 0.6)
    lines_at(c, g, back, 1690, fy, sc, feet, BONE, 0.6, 0.0)             # twice: the thin XDoG line reads at this size
    song_rings(c, g, 1690, fy - sc * 820, t, 600, 0.4)
    x, y, s_ = A4_R
    img_at(c, HELD, x, y, s_, (960, 540))
    tip = (x + (R_TIP[0] - 960) * s_, y + (R_TIP[1] - 540) * s_)
    cracks(c, g, tip[0], tip[1], t)
    tau_label(c, 120, 980)
    t_label(c, 1560, 250, t, 0.8)
    return tip

# the shatter: the held frame breaks into triangles, flung out from her fingertip
_sr = np.random.default_rng(21)
_GX, _GY = 11, 7
_PTS = [[(i * W / (_GX - 1) + (_sr.uniform(-60, 60) if 0 < i < _GX - 1 else 0),
          j * H / (_GY - 1) + (_sr.uniform(-50, 50) if 0 < j < _GY - 1 else 0)) for i in range(_GX)] for j in range(_GY)]
TRIS = []
for j in range(_GY - 1):
    for i in range(_GX - 1):
        a_, b_, c_, d_ = _PTS[j][i], _PTS[j][i + 1], _PTS[j + 1][i + 1], _PTS[j + 1][i]
        TRIS += [(a_, b_, c_), (a_, c_, d_)] if (i + j) % 2 else [(a_, b_, d_), (b_, c_, d_)]
SPIN = [_sr.uniform(-1.6, 1.6) for _ in TRIS]

def s_timestop(c, g, t):
    fill_bg(c, INK)
    fx = {}
    kk = (t - T0) / P
    if kk < 52.5:
        push(c, g, prog(t, B(48), B(52.5))); a1(c, g, t); pop(c, g)
    elif kk < 54.5:
        push(c, g, prog(t, B(52.5), B(54.5))); a2(c, g, t); pop(c, g)
    elif kk < 56.5:
        a3(c, g, t)
    elif kk < 59.5:
        push(c, g, prog(t, B(56.5), B(59.5)), 0.05); a4(c, g, t); pop(c, g)
    else:                                                       # k59.5: shatter
        s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c2 = cairo.Context(s2)
        gs2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, W // 2, H // 2); g2 = cairo.Context(gs2); g2.scale(0.5, 0.5)
        fill_bg(c2, INK); push(c2, g2, 1.0, 0.05); tip = a4(c2, g2, B(59.49)); pop(c2, g2); s2.flush()
        tip = (W / 2 + (tip[0] - W / 2) * 1.05, H / 2 + (tip[1] - H / 2) * 1.05)
        u = prog(t, B(59.5), B(60))
        rgba(c, BONE, eo_cubic(u) * 0.95); c.paint()
        for (tri, sp) in zip(TRIS, SPIN):
            cx_ = sum(p[0] for p in tri) / 3; cy_ = sum(p[1] for p in tri) / 3
            dx, dy = cx_ - tip[0], cy_ - tip[1]; dd = math.hypot(dx, dy) + 1
            v = 1400 / (0.35 + dd / 700) * u ** 1.5
            c.save(); c.translate(cx_ + dx / dd * v, cy_ + dy / dd * v); c.rotate(sp * u); c.translate(-cx_, -cy_)
            c.move_to(*tri[0]); c.line_to(*tri[1]); c.line_to(*tri[2]); c.close_path(); c.clip()
            c.set_source_surface(s2, 0, 0); c.paint_with_alpha(1 - u ** 2)
            c.restore()
            if u < 0.5:
                rgba(c, CYAN, 0.8 * (1 - 2 * u)); c.set_line_width(1.2)
                c.move_to(*tri[0]); c.line_to(*tri[1]); c.line_to(*tri[2]); c.close_path(); c.stroke()
        fx['flash'] = 0.5 * eo_cubic(u)
    if kk < 48.5:                                               # A0: the white of LIGHT dithers away into the hold
        u = prog(t, B(48), B(48.5))
        m = (lib_bayer_full() >= eo_cubic(u)).astype(np.uint8) * 255
        st = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, W)
        buf = np.zeros((H, st), np.uint8); buf[:, :W] = m
        ms = cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_A8, W, H, st)
        rgba(c, BONE, 1); c.mask_surface(ms, 0, 0)
    for ka in (48.5, 50.5, 52.5, 54.5, 56.5, 58.5):
        fx['ab'] = fx.get('ab', 0) + 2.2 * pulse(t, B(ka), 0.14)
    return fx

_BF = []
def lib_bayer_full():
    """the 8x8 ordered-dither threshold of prep8.py, in 3 px cells, over the frame"""
    if not _BF:
        bay = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38],
                        [60, 28, 52, 20, 62, 30, 54, 22], [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                        [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]], np.float32) / 64 + 1 / 128
        sm = np.tile(bay, (H // 24 + 1, W // 24 + 1))[:H // 3 + 1, :W // 3 + 1]
        _BF.append(np.repeat(np.repeat(sm, 3, 0), 3, 1)[:H, :W])
    return _BF[0]

# ================================================================ chorus 3, k368-371.5: the rewind (plan_v3.md section 7)
# "If I can have you back": the film itself runs backwards, 160 s -> the pinky promise at 57.8 s, first on 16ths then
# on 32nds, and lands on "back" (k371.5), where v2's pinky frame takes over. Frames: prep9.py (assets/rewind3_NN.jpg).
REWIND_CUTS = [368 + 0.25 * i for i in range(4)] + [369 + 0.125 * j for j in range(20)]   # 16ths, then 32nds
REWIND_SRC = [round(160.0 - (160.0 - 57.8) * n / (len(REWIND_CUTS) - 1), 2) for n in range(len(REWIND_CUTS))]
_RW = {}
def rewind_frame(n):
    if n not in _RW:
        path = f'{WORK}/assets/rewind3_{n:02d}.jpg'
        im = cv2.imread(path) if os.path.exists(path) else None
        if im is None: _RW[n] = None
        else:
            im = np.ascontiguousarray(np.dstack([im, np.full(im.shape[:2], 255, np.uint8)]))
            _RW[n] = (cairo.ImageSurface.create_for_data(im, cairo.FORMAT_ARGB32, im.shape[1], im.shape[0], im.strides[0]), im)
    return _RW[n][0] if _RW[n] else None

def s_rewind(c, g, t):
    fill_bg(c, INK)
    kk = (t - T0) / P
    n = max(i for i, k in enumerate(REWIND_CUTS) if kk >= k)
    sf = rewind_frame(n)
    r = random.Random(n * 31)
    jy = r.uniform(-6, 6)
    if sf is not None:                                          # every other cut a little closer, a little off: each one reads as a cut
        z = 1.0 if n % 2 == 0 else 1.14; jx = 0 if n % 2 == 0 else r.uniform(-90, 90)
        c.save(); c.translate(W / 2 + jx, H / 2 + jy); c.scale(z, z); c.translate(-W / 2, -H / 2); c.scale(W / sf.get_width(), H / sf.get_height())
        c.set_source_surface(sf, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint(); c.restore()
    else:
        text(c, 'mono', f'[ rewind frame {n} : run prep9.py ]', 960, 540, 30, GREY, 0.8, align='center')
    for y in range(0, H, 4): rgba(c, INK, 0.16); c.rectangle(0, y, W, 1.5); c.fill()        # the scanlines of a tape
    by = (H - (t * 1900) % (H + 200)) + 100                                                   # the tracking band, rolling up
    for k in range(10):
        rgba(c, BONE, 0.05 + 0.03 * r.random()); c.rectangle(0, by + k * 6, W, 3 + 4 * r.random()); c.fill()
    src = REWIND_SRC[n]
    text(c, 'monom', 'REWIND', 96, 120, 30, BONE, 0.95, track=0.3)
    for k in range(2):                                                                        # the two triangles, drawn
        x0 = 300 + k * 30; rgba(c, BONE, 0.95); c.move_to(x0 + 26, 96); c.line_to(x0, 108); c.line_to(x0 + 26, 120); c.close_path(); c.fill()
    text(c, 'heavy', f'{int(src // 60):02d}:{src % 60:05.2f}', W - 96, 1000, 120, BONE, 0.95, align='right')
    text(c, 'mono', '→ 00:57.80   you & me', W - 96, 1040, 20, CYAN, 0.8, align='right', track=0.1)
    return {'ab': 3 + 4 * pulse(t, B(REWIND_CUTS[n]), 0.06), 'glow': 0.5, 'vig': 0.6}

# ================================================================ the end: four steps to colour (plan_v3.md section 8)
# after the song stops (k448) the two of them come in as the film's whole look, one step a half beat on 208-209 s:
# raster (the system sees her) -> line -> two-colour print (memory) -> full colour (touch = true). The only colour in v3.
import scenes7 as S7
STEPS = [(448.5, 'r'), (450.0, 'l'), (450.5, 'm'), (451.0, None)]
T_TOUCH = B(451.5)
def ending_picture(c, g, t):
    name = S7.ENDING; ts = t - B(S7.K_SILENCE)
    step = [v for k, v in STEPS if t >= B(k)]
    if not step: return
    st = step[-1]; t0 = B([k for k, v in STEPS if t >= B(k)][-1])
    a = eo_cubic(prog(t, B(448.5), B(448.5) + 0.35)) if st == 'r' else 1.0
    sc = 0.94 * (1 + 0.012 * ts)
    c.save(); c.translate(960, 540); c.scale(sc, sc); c.translate(-960, -540)
    if st == 'l':
        rgba(c, SEPIA, 0.95); c.mask_surface(surf(name.replace('_hd', '_line')), 0, 0)
    else:
        nm = name if st is None else f'{name}__{st}'
        reg, lib.REG[0] = lib.REG[0], None                       # the picture as it is: no register over it
        c.set_source_surface(surf(nm), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a)
        lib.REG[0] = reg
    c.restore()
    fl = pulse(t, t0, 0.12) if st != 'r' else 0
    if fl > 0.02: rgba(c, (1, 1, 1), 0.35 * fl); c.paint()

def escape_out_v3(c, g, t):
    lib.BG[0] = 'paper'                                          # outside is warm light: the paper register, not the ink one
    if t < B(S7.K_SILENCE): return S7.escape_out(c, g, t)
    fx = {}
    S7.outside_light(c, g)
    fall = ei_cubic(prog(t, B(S7.FINAL_EX), B(S7.FINAL_EX) + 0.85))
    if fall < 1:
        ys, wy, f = S7.tear_open(t)
        for side in (-1, 1): S7.paper_piece(c, side, ys, wy, f, side * 760 * fall, 1000 * fall * fall, side * 0.28 * fall)
    for kb in np.arange(444.0, 448.5, 0.5):
        u = prog(t, B(kb), B(kb) + 1.6)
        if 0 < u < 1:
            r = 40 + 1300 * eo_cubic(u); big = 1.0 if kb % 1 == 0 else 0.6
            for cc, aa, lw in ((c, big * (1 - u) ** 0.7, big * (6.0 * (1 - u) + 1.5)), (g, 0.7 * big * (1 - u), 10)):
                rgba(cc, LISH_P if cc is c else LISH, aa); cc.set_line_width(lw); cc.new_path(); cc.arc(S7.TEAR_X, 540, r, 0, 6.283); cc.stroke()
    if t < B(S7.K_SILENCE) + 0.3:                                    # the last EXECUTION, going
        u = 1 - prog(t, B(S7.K_SILENCE), B(S7.K_SILENCE) + 0.3)
        c.save(); c.translate(960, 640)
        c.new_path(); fonts()['heavy'].text_path(c, 'EXECUTION', 0, 0, 330, 'center')
        rgba(c, (1, 0.985, 0.94), 0.9 * u); c.set_line_width(16); c.stroke_preserve(); rgba(c, INK, u); c.fill(); c.restore()
    ending_picture(c, g, t)
    # what is left of the system: one task, done
    if t >= T_TOUCH:
        u = eo_cubic(prog(t, T_TOUCH, T_TOUCH + 0.4))
        x0, y0 = 130, 990
        rgba(c, SEPIA, 0.9 * u); c.set_line_width(2.4); c.move_to(x0, y0 - 9); c.line_to(x0 + 7, y0 - 2); c.line_to(x0 + 20, y0 - 18); c.stroke()
        text(c, 'mono', 'touch(you)', x0 + 36, y0, 26, SEPIA, 0.9 * u)
        text(c, 'monom', 'true', x0 + 36 + text_w('mono', 'touch(you)   ', 26), y0, 26, RED, 0.95 * u)
        uh = prog(t, T_TOUCH + 0.8, T_TOUCH + 1.2)
        if uh > 0:
            text(c, 'mono', type_on('me.hum();', t, T_TOUCH + 0.8, 0.05), x0 + 36, 1030, 20, SEPIA, 0.6)
            reach = prog(t, T_TOUCH + 1.1, T_TOUCH + 2.2)
            for cc, aa, lw in ((c, 0.8, 1.4), (g, 0.3, 3)):
                rgba(cc, LISH_P if cc is c else LISH, aa); cc.set_line_width(lw); cc.new_path()
                for n_ in range(0, 161):
                    if n_ / 160 > reach: break
                    x = 300 + 360 * n_ / 160
                    e = math.sin(math.pi * n_ / 160) * (0.6 + 0.4 * math.sin(t * 1.3 + n_ * 0.05))
                    (cc.move_to if n_ == 0 else cc.line_to)(x, 1023 - 5 * e * math.sin(n_ * 0.28 - t * 2.2))
                cc.stroke()
    fx['ab'] = 3 * sum(pulse(t, B(k), 0.15) for k, _ in STEPS[1:])
    fx['vig'] = 0.3; fx['grain'] = 0.03; fx['glow'] = 0.6
    return fx

OVERRIDE = [(B(48), B(60), s_timestop), (B(368), B(371.5), s_rewind), (B(S7.K_LEAP), 999.0, escape_out_v3)]
