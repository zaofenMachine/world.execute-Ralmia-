"""world.execute(me); x Ralmia — 30–60 s.  'If I'm a set of points' … 'so deeply, so deeply'.
Every hard event sits on B(k). Connective words use Whisper times (words_29.json, see LY below)."""
from scenes2 import *
import json

# ---------------------------------------------------------------- lyric timing (seconds)
# keywords snapped to the beat grid (k in comments); connective words straight from words_29.json
K_POINTS, K_DIM, K_CIRCLE, K_CIRC = 66.5, 70.5, 74, 78.25
K_SINE, K_TAN, K_INF, K_LIM = 82, 87, 89.5, 94
K_SWITCH, K_CURRENT, K_AC, K_DC = 95, 97.5, 100, 102
K_BLIND, K_VISION = 103.5, 105.5
K_SO1, K_DIZ1, K_SO2, K_DIZ2 = 107, 108, 109.5, 110
K_TRAVEL, K_AD, K_BC, K_UNITE = 113.5, 116, 118, 121.5
K_SO3, K_DEEP1, K_SO4, K_DEEP2 = 123, 124, 125, 126
END2 = B(128)                    # 59.41 s, chorus "If I can" starts here (next round)

LOG.extend([(B(64), 'points = explode()'), (B(68), 'dim++'), (B(72), 'r = 1'), (B(76), 'C = 2*PI*r'),
            (B(80), 'y = sin(theta)'), (B(84), 'tangent(you)'), (B(88), 'x -> inf'), (B(92), 'lim = you'),
            (B(95), 'switch(current)'), (B(100), 'mode = AC'), (B(102), 'mode = DC'), (B(103), 'vision.blind()'),
            (B(106.5), 'gyro: drift'), (B(111.5), 'v > c'), (B(116), 't < 0'), (B(119), 'touch(you)'),
            (B(121.5), 'touch = true'), (B(123), 'link.depth++')])
LOG.sort(key=lambda e: e[0])
from codelog import CODE_LOG, ADDED
LOG[:] = CODE_LOG                 # the HUD now types the song's own source code

def lyric(c, items, t, col=BONE, x=150, y=248, size=70, a=0.95):
    words(c, 'serif', items, t, x, y, size, col, a)

def glyph_pop(c, key, s, x, y, size, col, t, t0, per, a=1.0, align='left', track=0.0, drop=40, dur=0.12, g=None, ga=0.0):
    """Letters appear one by one (per seconds apart) with a short drop."""
    f = fonts()[key]
    for d in f.glyphs(s, x, y, size, align, track):
        ti = t0 + d['i'] * per
        u = prog(t, ti, ti + dur)
        if u <= 0: continue
        dy = -drop * (1 - eo_back(u, 2.0))
        for cc, aa, cl in ((c, a, col), (g, ga, CYAN)):
            if cc is None or aa <= 0: continue
            cc.new_path(); f.glyph_path(cc, d['g'], d['x'], d['y'] + dy, size); rgba(cc, cl, aa * min(1, u * 3)); cc.fill()

def warp_path(c, fn):
    """Re-emit the current path with every (flattened) point mapped through fn(x, y)."""
    flat = c.copy_path_flat(); c.new_path()
    for kind, pts in flat:
        if kind == cairo.PATH_MOVE_TO: c.move_to(*fn(*pts))
        elif kind == cairo.PATH_LINE_TO: c.line_to(*fn(*pts))
        elif kind == cairo.PATH_CLOSE_PATH: c.close_path()

def draw_points(c, X, Y, col, a, size):
    if a <= 0.004 or len(X) == 0: return
    rgba(c, col, a); h = size / 2
    for x, y in zip(X.tolist(), Y.tolist()): c.rectangle(x - h, y - h, size, size)
    c.fill()

# ---------------------------------------------------------------- her face as a point cloud
_FACE = {}
FACE_SRC = 'n_portrait'          # gen/portrait_front.png
FACE_FROM = (930, 470)            # face centre in the image ...
FACE_TO = (1170, 500)             # ... lands here on screen
FACE_SC = 1.0
FACE_CYAN = [(858, 488, 22, 27), (1007, 457, 22, 27), (756, 300, 20, 34)]   # irises + temple gem (image px)
def face_cloud(n=18432, seed=2):
    if 'x' not in _FACE:
        hd = cv2.imread(f'{WORK}/assets/{FACE_SRC}_hd.png').astype(np.float32) / 255
        ln = cv2.imread(f'{WORK}/assets/{FACE_SRC}_line.png', 0).astype(np.float32) / 255
        lum = hd.mean(2)
        sat = cv2.cvtColor((hd * 255).astype(np.uint8), cv2.COLOR_BGR2HSV)[..., 1].astype(np.float32) / 255
        hsv = cv2.cvtColor((hd * 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
        tone = np.clip(0.9 - lum, 0, 1)
        w = 1.6 * (1 - ln) ** 1.5 + 0.12 * tone
        yy_, xx_ = np.mgrid[0:H, 0:W]
        cyanish = np.zeros((H, W), bool)
        for (cx_, cy_, rx_, ry_) in FACE_CYAN:                  # iris / gem regions (hand-marked for this image)
            cyanish |= ((xx_ - cx_) / rx_) ** 2 + ((yy_ - cy_) / ry_) ** 2 < 1
        w[cyanish] = 0.25 + 1.4 * tone[cyanish]
        w[:, :520] *= np.linspace(0.0, 1, 520)[None, :] ** 1.5  # far-left hair thins out (room for type)
        w *= np.clip((1010 - yy_) / 260, 0, 1) ** 1.3            # keep it a face: fade out below the collar
        ex_ = np.minimum(np.minimum(xx_, W - 1 - xx_), np.minimum(yy_, H - 1 - yy_) * 1.6)
        w *= np.clip(ex_ / 160, 0, 1) ** 1.5                     # no hard frame edges
        p = (w.ravel() + 1e-9); p /= p.sum()
        r = np.random.default_rng(seed)
        idx = r.choice(p.size, n, replace=False, p=p)
        ys, xs = np.divmod(idx, W)
        _FACE['cyan'] = cyanish[ys, xs]
        _FACE['x'] = (xs + r.random(n) - 0.5 - FACE_FROM[0]) * FACE_SC + FACE_TO[0]
        _FACE['y'] = (ys + r.random(n) - 0.5 - FACE_FROM[1]) * FACE_SC + FACE_TO[1]
        _FACE['lum'] = lum[ys, xs]
        _FACE['ph'] = r.random(n) * 6.283
        _FACE['delay'] = r.random(n)
    return _FACE

_TPA = {}
def title_arrays():
    if not _TPA:
        L = title_layout()
        _TPA['x'] = np.array([p[0] for p in L['pts']], np.float32)
        _TPA['y'] = np.array([p[1] for p in L['pts']], np.float32)
        _TPA['vx'] = L['vel'][:, 0].astype(np.float32); _TPA['vy'] = L['vel'][:, 1].astype(np.float32)
    return _TPA

_DOTW = {}
def dot_word(s, x, y, size, step=11, key='heavy'):
    """Dot-matrix rendering of a word: list of (x, y, column index)."""
    k = (s, x, y, size, step)
    if k not in _DOTW:
        f = fonts()[key]
        ss = cairo.ImageSurface(cairo.FORMAT_A8, W, H); cc = cairo.Context(ss)
        f.text_path(cc, s, x, y, size); cc.set_source_rgba(0, 0, 0, 1); cc.fill(); ss.flush()
        m = np.ndarray((H, ss.get_stride()), np.uint8, ss.get_data())[:, :W]
        out = []
        for yy in range(int(y - size), int(y + 10), step):
            for xx in range(int(x), W, step):
                if 0 <= yy < H and m[yy, xx] > 128: out.append((xx, yy, (xx - x) // step))
        _DOTW[k] = out
    return _DOTW[k]

def face_state(t):
    """Screen positions of the face cloud at time t (after the gather), with breathing."""
    F = face_cloud()
    br = 0.8
    X = F['x'] + np.sin(t * 1.7 + F['ph']) * br
    Y = F['y'] + np.cos(t * 1.3 + F['ph'] * 1.3) * br
    return X, Y

# ================================================================ S9 POINTS  [B64, B68)
def s_points(c, g, t):
    fill_bg(c, INK)
    fx = {}
    TA = title_arrays(); F = face_cloud()
    n0 = len(TA['x'])
    tb = B(64); dt = max(0.0, t - tb)
    sp = 1 - math.exp(-dt * 3.5)
    ex = TA['x'] + TA['vx'] * sp * 0.9 + np.sin(TA['y'] * 0.05 + t * 2) * 6 * sp
    ey = TA['y'] + TA['vy'] * sp * 0.9
    ug = eio_cubic(prog(t, B(65), B(66)))
    FX, FY = face_state(t)
    tx, ty = FX[:n0], FY[:n0]
    # swirl while gathering: sideways offset that vanishes at both ends
    sw = math.sin(math.pi * ug) * 90
    X = ex + (tx - ex) * ug + sw * np.sin(F['ph'][:n0])
    Y = ey + (ty - ey) * ug + sw * np.cos(F['ph'][:n0])
    cy_ = F['cyan'][:n0] & (ug > 0.6)
    size = 3.2 - 0.6 * ug
    draw_points(c, X[~cy_], Y[~cy_], BONE, 0.95, size)
    draw_points(c, X[cy_], Y[cy_], CYAN, 0.95, size)
    # density doubles on k66 and k67: new points pop in at their targets
    count = n0
    for gen, kb in ((1, 66.0), (2, 67.0)):
        if t < B(kb): break
        a0, a1 = n0 * (2 ** (gen - 1)), n0 * (2 ** gen)
        de = F['delay'][a0:a1] * P / 2
        u = np.clip((t - B(kb) - de) / 0.08, 0, 1)
        vis = u > 0
        count = a0 + int(vis.sum())
        for lo, hi in ((0.0, 0.5), (0.5, 1.01)):
            m = vis & (u >= lo) & (u < hi)
            mc = m & F['cyan'][a0:a1]; mb = m & ~F['cyan'][a0:a1]
            aa = 0.5 if hi < 1 else 0.9
            draw_points(c, FX[a0:a1][mb], FY[a0:a1][mb], BONE, aa, 2.6)
            draw_points(c, FX[a0:a1][mc], FY[a0:a1][mc], CYAN, aa, 2.6)
    if t >= B(66): count = max(count, n0)
    # glow: every point flashes on "points"
    pf = pulse(t, B(K_POINTS), 0.4) + 0.5 * pulse(t, B(66), 0.25) + 0.5 * pulse(t, B(67), 0.25)
    if pf > 0.02:
        nn = count
        draw_points(g, FX[:nn][F['cyan'][:nn]], FY[:nn][F['cyan'][:nn]], CYAN, min(1, pf), 4)
        draw_points(g, FX[:nn:3], FY[:nn:3], BONE, 0.35 * min(1, pf), 3)
    # cyan glow on the iris & gem always
    if ug > 0.6:
        m = F['cyan'][:max(count, n0)]
        draw_points(g, FX[:len(m)][m], FY[:len(m)][m], CYAN, 0.5, 4)
    # POINTS as a dot matrix
    if t >= B(K_POINTS):
        dots = dot_word('POINTS', 120, 1000, 250, 12)
        for (x, y, col) in dots:
            ti = B(K_POINTS) + col * 0.0035
            u = eo_cubic(prog(t, ti, ti + 0.06))
            if u <= 0: continue
            s_ = 6 * u
            rgba(c, BONE, 0.95); c.rectangle(x - s_ / 2, y - s_ / 2, s_, s_)
        c.fill()
    lyric(c, [('If', 30.00), ("I'm", 30.18), ('a', 30.64), ('set', 30.76), ('of', 30.88)], t)
    text(c, 'mono', f'n = {count:,}'.replace(',', ' '), W - 130, 1000, 24, CYAN, 0.85 * prog(t, B(64.5), B(65)),
         align='right', track=0.12)
    fx['flash'] = 0.25 * pulse(t, B(K_POINTS), 0.12)
    fx['ab'] = 4 * pulse(t, B(66), 0.2) + 4 * pulse(t, B(67), 0.2) + 3 * pulse(t, B(K_POINTS), 0.2)
    fx['glow'] = 1.0
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ S10 DIMENSION  [B68, B72)
CUBE = 230
def rot3(X, Y, Z, rx, ry):
    cy_, sy_ = math.cos(ry), math.sin(ry)
    X2 = X * cy_ + Z * sy_; Z2 = -X * sy_ + Z * cy_
    cx_, sx_ = math.cos(rx), math.sin(rx)
    Y2 = Y * cx_ - Z2 * sx_; Z3 = Y * sx_ + Z2 * cx_
    return X2, Y2, Z3

def proj(X, Y, Z, cx=960, cy=580, f=1700):
    s = f / (f + Z)
    return cx + X * s, cy + Y * s, s

def cube_angles(t):
    e = eo_cubic(prog(t, B(K_DIM), B(K_DIM) + 0.35))
    ry = 0.62 * e + 0.16 * max(0, t - B(K_DIM)) - 0.42 * eo_back(prog(t, B(71), B(71) + 0.25)) \
         + 0.30 * eo_back(prog(t, B(71.5), B(71.5) + 0.25))
    rx = -0.22 * e - 0.04 * max(0, t - B(K_DIM))
    return rx, ry, e

def face3d():
    F = face_cloud()
    k = 0.33
    X = (F['x'] - FACE_TO[0]) * k
    Y = (F['y'] - FACE_TO[1] - 60) * k
    Z = -np.clip(0.85 - F['lum'], 0, 1) * 70 + np.where(F['cyan'], -25, 0) + 0.0004 * (X ** 2 + Y ** 2)   # gentle relief, cheeks curve back
    return X, Y, Z

def draw_cube(c, g, t, scale=1.0, alpha=1.0, depth=1.0):
    rx, ry, e = cube_angles(t)
    s = CUBE * scale; hz = CUBE * scale * depth
    V = [(x, y, z) for x in (-s, s) for y in (-s, s) for z in (-hz, hz)]
    Pp = []
    for (x, y, z) in V:
        X, Y, Z = rot3(x, y, z, rx, ry); Pp.append(proj(X, Y, Z))
    edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count('1') == 1]
    for cc, aa, lw, col in ((c, alpha, 2.2, BONE), (g, 0.4 * alpha, 3, CYAN)):
        rgba(cc, col, aa); cc.set_line_width(lw)
        for a, b in edges:
            cc.move_to(Pp[a][0], Pp[a][1]); cc.line_to(Pp[b][0], Pp[b][1])
        cc.stroke()
    for p_ in Pp:
        rgba(c, BONE, alpha); c.rectangle(p_[0] - 4, p_[1] - 4, 8, 8); c.fill()
    return rx, ry

def s_dimension(c, g, t):
    fill_bg(c, INK)
    fx = {}
    dotgrid(c, BONE, 0.05)
    cx, cy = 960, 580
    # 0D: the face implodes to a single point on the downbeat
    ui = prog(t, B(68), B(68) + 0.27)
    if ui < 1:
        FX, FY = face_state(t); F = face_cloud()
        F_ = face_cloud()
        uu = np.clip((t - B(68) - F_['delay'] * 0.12) / 0.14, 0, 1)
        uu = 1 - (1 - uu) ** 3
        X = FX + (cx - FX) * uu; Y = FY + (cy - FY) * uu
        draw_points(c, X[~F['cyan']], Y[~F['cyan']], BONE, 0.9, 2.6)
        draw_points(c, X[F['cyan']], Y[F['cyan']], CYAN, 0.9, 2.6)
    dim = 0 if t < B(69) else 1 if t < B(70) else 2 if t < B(K_DIM) else 3
    if t >= B(68) + 0.15 and t < B(K_DIM):
        u1 = eo_expo(prog(t, B(69), B(69) + 0.16))
        u2 = eo_expo(prog(t, B(70), B(70) + 0.2))
        hw = CUBE * u1; hh = CUBE * u2
        if dim == 0 or u1 <= 0:
            for cc in (c, g):
                rgba(cc, BONE if cc is c else CYAN, 1); cc.arc(cx, cy, 7 + 6 * pulse(t, B(68) + 0.2, 0.4), 0, 6.283); cc.fill()
        else:
            # sweep lines left behind by the moving edge
            if u2 > 0:
                nlines = 10
                for i in range(nlines + 1):
                    yy = cy - hh + 2 * hh * i / nlines
                    line(c, cx - hw, yy, cx + hw, yy, BONE, 0.18, 1)
                rgba(c, BONE, 0.04); c.rectangle(cx - hw, cy - hh, 2 * hw, 2 * hh); c.fill()
            for cc, aa, lw, col in ((c, 1, 2.4, BONE), (g, 0.5, 3, CYAN)):
                rgba(cc, col, aa); cc.set_line_width(lw)
                cc.move_to(cx - hw, cy - hh); cc.line_to(cx + hw, cy - hh); cc.stroke()
                if u2 > 0:
                    cc.move_to(cx - hw, cy + hh); cc.line_to(cx + hw, cy + hh)
                    cc.move_to(cx - hw, cy - hh); cc.line_to(cx - hw, cy + hh)
                    cc.move_to(cx + hw, cy - hh); cc.line_to(cx + hw, cy + hh); cc.stroke()
            for sx in (-1, 1):
                for sy in ((-1, 1) if u2 > 0 else (0,)):
                    rgba(c, BONE, 1); c.rectangle(cx + sx * hw - 4, cy + sy * hh - 4, 8, 8); c.fill()
            # ticks on the 1D line
            if u2 <= 0:
                for i in range(-10, 11):
                    x = cx + hw * i / 10
                    line(c, x, cy + 8, x, cy + (22 if i % 5 == 0 else 14), BONE, 0.5, 1.2)
    if t >= B(K_DIM):
        de = eo_back(prog(t, B(K_DIM), B(K_DIM) + 0.3), 1.4)
        rx, ry = draw_cube(c, g, t, depth=max(0.001, de))
        # the face as a 3-D relief inside the cube
        uf = prog(t, B(71), B(71) + 0.25)
        if uf > 0:
            X3, Y3, Z3 = face3d(); F = face_cloud()
            n = int(len(X3) * 0.6)
            sc_ = eo_cubic(uf)
            Xr, Yr, Zr = rot3(X3[:n] * sc_, Y3[:n] * sc_, Z3[:n] * sc_ * de, rx, ry)
            px, py, s = proj(Xr, Yr, Zr)
            m = F['cyan'][:n]
            draw_points(c, px[~m], py[~m], BONE, 0.8, 2.2)
            draw_points(c, px[m], py[m], CYAN, 1, 2.6)
            draw_points(g, px[m], py[m], CYAN, 0.6, 4)
    # dimension readout
    labs = ['0D', '1D', '2D', '3D']
    kbs = [68, 69, 70, K_DIM]
    for i, lb in enumerate(labs):
        on = (i == dim)
        ua = prog(t, B(kbs[i]), B(kbs[i]) + 0.05)
        text(c, 'monom', lb, 1530 + i * 82, 860, 34, CYAN if on else BONE, (1 if on else 0.3) * max(ua, 0.3), track=0.05)
    text(c, 'heavy', labs[dim], 1530, 800, 170, BONE, 0.95)
    if t >= B(K_DIM):
        glyph_pop(c, 'thin', 'DIMENSION', 120, 1000, 150, BONE, t, B(K_DIM), P / 8, track=0.12, drop=0)
    lyric(c, [('then', 31.54), ('I', 31.64), ('will', 31.88), ('give', 32.10), ('you', 32.34), ('my', 32.58)], t)
    fx['flash'] = 0.35 * pulse(t, B(68) + 0.2, 0.12)
    fx['ab'] = 4 * (pulse(t, B(69), 0.2) + pulse(t, B(70), 0.2) + pulse(t, B(K_DIM), 0.25) + pulse(t, B(71.5), 0.2))
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ S11 CIRCLE  [B72, B76)
GEM = (1228, 562); GEM_R = 73        # n_hand_palm: palm core centre and radius (image px)
def s_circle(c, g, t):
    fx = {}
    R0 = 240; R1 = 150; cx, cy = 960, 580
    R = lerp(R0, R1, eio_cubic(prog(t, B(73.5), B(K_CIRCLE) - 0.02)))
    if t < B(K_CIRCLE):
        fill_bg(c, INK)
        dotgrid(c, BONE, 0.05)
        # the cube is sucked into the centre while the circle is drawn
        us = eo_expo(prog(t, B(72), B(72) + 0.3))
        if us < 1: draw_cube(c, g, t + 0.6 * us, scale=1 - us, alpha=1 - us)
        uc = eo_expo(prog(t, B(72), B(72) + 0.35))
        for cc, aa, lw, col in ((c, 1, 3, BONE), (g, 0.5, 4, CYAN)):
            rgba(cc, col, aa); cc.set_line_width(lw); cc.new_path()
            cc.arc(cx, cy, R, -math.pi / 2, -math.pi / 2 + 2 * math.pi * uc); cc.stroke()
        # compass construction: ticks, centre, a radius sweeping one turn
        for i in range(72):
            a_ = i / 72 * 2 * math.pi
            if a_ > 2 * math.pi * uc: break
            L = 16 if i % 6 == 0 else 8
            line(c, cx + math.cos(a_) * (R + 8), cy + math.sin(a_) * (R + 8), cx + math.cos(a_) * (R + 8 + L),
                 cy + math.sin(a_) * (R + 8 + L), BONE, 0.45, 1.2)
        ur = eio_cubic(prog(t, B(72.5), B(73.5)))
        if t >= B(72.5):
            ang = -math.pi / 2 + 2 * math.pi * ur
            rgba(c, BONE, 0.07); c.move_to(cx, cy); c.arc(cx, cy, R, -math.pi / 2, ang); c.close_path(); c.fill()
            for cc, aa in ((c, 1), (g, 0.6)):
                line(cc, cx, cy, cx + math.cos(ang) * R, cy + math.sin(ang) * R, CYAN, aa, 2.5)
            text(c, 'monom', 'r', cx + math.cos(ang) * R * 0.5 + 14, cy + math.sin(ang) * R * 0.5 - 10, 30, CYAN, 0.9)
        rgba(c, BONE, 1); c.arc(cx, cy, 5, 0, 6.283); c.fill()
        text(c, 'mono', f'r = 1     C = {2 * math.pi * ur:.4f}', cx, cy + R + 90, 22, BONE, 0.6 * uc, align='center', track=0.15)
        lyric(c, [('If', 33.34), ("I'm", 33.80), ('a', 34.34)], t)
        hud(c, t, True, a=0.7)
        fx['ab'] = 4 * pulse(t, B(72), 0.25)
        return fx
    # --- on "circle": the circle IS the core in her palm. cut to paper, zoom out from the gem.
    paper_bg(c)
    dotgrid(c, SEPIA, 0.10)
    uz = eo_expo(prog(t, B(K_CIRCLE), B(K_CIRCLE + 1)))
    push = 1 + 0.06 * eio_cubic(prog(t, B(K_CIRCLE + 1), B(76)))
    sc0 = R1 / GEM_R
    sc = lerp(sc0, 1.0, uz) * push
    ax, ay = lerp(cx, GEM[0], uz), lerp(cy, GEM[1], uz)
    ax, ay = ax + (ax - 960) * (push - 1) * 0, ay
    c.save(); c.translate(ax, ay); c.scale(sc, sc); c.translate(-GEM[0], -GEM[1])
    c.set_source_surface(surf('n_hand_palm_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
    c.restore()
    rr_ = GEM_R * sc
    for cc, aa, lw, col in ((c, 0.9, 2.2, SEPIA), (g, 0.8 * pulse(t, B(K_CIRCLE), 0.6) + 0.25, 4, CYAN)):
        rgba(cc, col, aa); cc.set_line_width(lw); cc.new_path(); cc.arc(ax, ay, rr_ + 6, 0, 6.283); cc.stroke()
    ua = eo_cubic(prog(t, B(K_CIRCLE + 0.5), B(K_CIRCLE + 0.5) + 0.25))
    if ua > 0:
        ex_, ey_ = ax + 300 * ua, ay - 200 * ua
        line(c, ax + (rr_ + 6) * 0.83, ay - (rr_ + 6) * 0.55, ex_, ey_, INK, 0.8, 1.4)
        line(c, ex_, ey_, ex_ + 260 * ua, ey_, INK, 0.8, 1.4)
        text(c, 'mono', type_on('r = 1', t, B(K_CIRCLE + 0.5), 0.03), ex_ + 4, ey_ - 36, 16, INK, 0.6)
        text(c, 'monom', type_on('ŌMETEŌTL core', t, B(K_CIRCLE + 0.6), 0.025), ex_ + 4, ey_ - 10, 24, INK, 0.9, track=0.1)
    lyric(c, [('If', 33.34), ("I'm", 33.80), ('a', 34.34)], t, col=SEPIA, x=130, y=640)
    glyph_pop(c, 'thin', 'CIRCLE', 124, 860, 230, INK, t, B(K_CIRCLE), P / 8, track=0.06, drop=0)
    fx['flash'] = 0.5 * pulse(t, B(K_CIRCLE), 0.1)
    fx['ab'] = 5 * pulse(t, B(K_CIRCLE), 0.25); fx['vig'] = 0.4; fx['grain'] = 0.03
    hud(c, t, False)
    return fx

# ================================================================ S12 CIRCUMFERENCE  [B76, B80)
CC_X, CC_Y, CC_R = 330, 560, 170
def roll_phi(t):
    """unrolled angle (0..2pi): quarter turns on the beat, last one on 'circumference'; rolls back up for the sine."""
    phi = 0.0
    for kb in (76.5, 77, 77.5, K_CIRC):
        phi += math.pi / 2 * eo_cubic(prog(t, B(kb), B(kb) + 0.22))
    back = eio_cubic(prog(t, B(79.4), B(80) - 0.02))
    return phi * (1 - back)

def s_circum(c, g, t):
    paper_bg(c)
    fx = {}
    dotgrid(c, SEPIA, 0.10)
    phi = roll_phi(t)
    R = CC_R; yb = CC_Y + R
    xc = CC_X + R * phi
    # baseline + quarter ticks
    ub = eo_expo(prog(t, B(76), B(76) + 0.3))
    line(c, CC_X - 120, yb, CC_X - 120 + 1500 * ub, yb, SEPIA, 0.35, 1.2)
    labels = ['0', 'π/2 r', 'π r', '3π/2 r', '2π r']
    for i in range(5):
        x = CC_X + R * math.pi / 2 * i
        if xc + 1 < x and i > 0: continue
        line(c, x, yb + 8, x, yb + 30, SEPIA, 0.8, 1.4)
        text(c, 'mono', labels[i], x, yb + 58, 20, SEPIA, 0.75, align='center')
    # laid-out part
    for cc, aa, lw, col in ((c, 1, 5, INK), (g, 0.0, 6, CYAN)):
        if aa <= 0: continue
        rgba(cc, col, aa); cc.set_line_width(lw); cc.move_to(CC_X, yb); cc.line_to(xc, yb); cc.stroke()
    # remaining arc
    rem = 2 * math.pi - phi
    if rem > 0.002:
        rgba(c, INK, 1); c.set_line_width(5); c.new_path()
        c.arc_negative(xc, CC_Y, R, math.pi / 2, math.pi / 2 - rem); c.stroke()
        # spoke rotating with the roll
        ang = -math.pi / 2 + phi
        line(c, xc, CC_Y, xc + math.cos(ang) * R, CC_Y + math.sin(ang) * R, SEPIA, 0.6, 1.4)
        rgba(c, INK, 1); c.arc(xc, CC_Y, 5, 0, 6.283); c.fill()
        # the free end of the peel
        fa = math.pi / 2 - rem
        rgba(c, RED if False else INK, 1); c.arc(xc + math.cos(fa) * R, CC_Y + math.sin(fa) * R, 6, 0, 6.283); c.fill()
    rgba(c, INK, 1); c.arc(CC_X, yb, 6, 0, 6.283); c.fill()
    # v2: she is sitting at the far end of the line, waiting for it to roll out to her
    end_x = CC_X + 2 * math.pi * R + 330                         # past the C = 2πr label
    ua_ = eo_cubic(prog(t, B(76), B(76) + 0.35))
    lish_sit(c, end_x, yb, 0.33, ua_, 0.0, t)
    # CIRCUMFERENCE laid along the 2πr line
    L = 2 * math.pi * R
    if t >= B(K_CIRC) and t < B(79.4) + 0.15:
        f = fonts()['bold']; track = 0.02
        size = L / f.shape('CIRCUMFERENCE', track)[1]
        la = 1 - prog(t, B(79.4), B(79.4) + 0.15)
        glyph_pop(c, 'bold', 'CIRCUMFERENCE', CC_X, yb - 14, size, INK, t, B(K_CIRC), 0.028, a=la, track=track, drop=70)
        uu = eo_cubic(prog(t, B(78.75), B(78.75) + 0.3))
        text(c, 'monom', 'C = 2πr', CC_X + L + 40, yb - 50, 44, INK, uu * la)
        text(c, 'mono', f'= {2 * math.pi * uu:.6f} r', CC_X + L + 40, yb - 12, 22, SEPIA, 0.8 * uu * la)
    lyric(c, [('then', 35.26), ('I', 35.34), ('will', 35.60), ('give', 35.80), ('you', 36.04), ('my', 36.28)], t, col=SEPIA)
    fx['ab'] = 3 * pulse(t, B(K_CIRC), 0.25); fx['vig'] = 0.4; fx['grain'] = 0.03
    fx['flash'] = 0.0
    hud(c, t, False)
    return fx

# v2 round 2: "then you can sit on all my ..." -- Lishenna sits on what Ralmia gives her. n_lish_sit: the underside of
# her seat is a horizontal line through SIT_SEAT (canvas px); the A/B pair swings her feet, one swap per beat
SIT_SEAT = (960, 552)
TRACE_F = 0.6                           # n_trace_* are the 1920 canvas at this scale (prep7.py)
_TRC = {}
def phosphor(c, g, name, x, y, sc, anchor, t, col=BONE, a=1.0, rot=0.0, wob=1.0, reveal=1.0, ga=0.5):
    """v2 round 3: a figure drawn by the beam, like the AC/DC faces: its line art (n_trace_<name>) as light, with a
    little scope wobble; reveal < 1 draws it in from the top, the beam line at the front"""
    if a <= 0.01: return
    if name not in _TRC:
        m = cv2.imread(f'{WORK}/assets/n_trace_{name}.png', cv2.IMREAD_GRAYSCALE).astype(np.float32)
        hh, ww = m.shape; yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        _TRC[name] = (m, xx, yy, cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, ww))
    m, xx, yy, stride = _TRC[name]
    if wob > 0:
        ph = t * 9
        m = cv2.remap(m, xx + wob * (0.8 * np.sin(yy / 9 + ph) + 0.5 * np.sin(yy / 31 - ph * 1.7)), yy, cv2.INTER_LINEAR)
    hh, ww = m.shape
    ry = None
    if reveal < 1:
        m = m.copy(); ry = int(hh * reveal); m[ry:] = 0
    buf = np.zeros((hh, stride), np.uint8); buf[:, :ww] = np.clip(m * a, 0, 255).astype(np.uint8)
    sf = cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_A8, ww, hh, stride)
    k = sc / TRACE_F
    for cc, aa in ((c, 1.0), (g, ga)):
        cc.save(); cc.translate(x, y); cc.rotate(rot); cc.scale(k, k); cc.translate(-anchor[0] * TRACE_F, -anchor[1] * TRACE_F)
        rgba(cc, col, aa); cc.mask_surface(sf, 0, 0)
        if ry is not None and 0 < ry < hh:                       # the beam, across the figure only
            band = _TRC[name][0][max(0, ry - 12):ry + 12].max(0)
            xs_ = np.nonzero(band > 40)[0]
            if len(xs_):
                rgba(cc, col, 0.8 * aa); cc.set_line_width(2 / k); cc.move_to(xs_[0] - 20, ry); cc.line_to(xs_[-1] + 20, ry); cc.stroke()
        cc.restore()

# v2 round 4: 39-44 s, simpler -- Ralmia is the curve (as she is the wave), Lishenna is only a face of light.
# TANGENTS: her face (the AC/DC trace, n_scope_lish) appears only where Ralmia's tangents have swept -- "you can sit on all
# my tangents" = she is made of them. LIMITATION: the same face, small, rests on the asymptote; it gets clearer as the
# curve closes in on it, and the curve never arrives
_LF = {}
def lish_face_mask():
    if 'm' not in _LF: _LF['m'] = cv2.imread(f'{WORK}/assets/n_scope_lish.png', cv2.IMREAD_GRAYSCALE)
    return _LF['m']
TF_C, TF_S = (1190, 520), 1.62                   # tangents: where the face centre (mask (465, 280)) lands, and its scale
def tangent_face(c, g, t):
    m = lish_face_mask()                         # 960 x 540; to screen: x = TF_C + (mx - 465) * TF_S
    M = np.float32([[TF_S, 0, TF_C[0] - 465 * TF_S], [0, TF_S, TF_C[1] - 280 * TF_S]]) * 0.5   # into a half-res screen
    face = cv2.warpAffine(m, M, (960, 540), flags=cv2.INTER_AREA if TF_S < 2 else cv2.INTER_LINEAR)
    rv = np.zeros((540, 960), np.uint8)
    tau = B(84.5)
    while tau <= t:                              # every tangent she has drawn so far leaves a stripe of the face lit
        ride = prog(tau, B(84.5), B(88))
        xt = lerp(1700, 240, ride * 0.85 + 0.15 * eio_cubic(ride))
        yy = wave_y(xt, tau); mm = wave_slope(xt, tau); nrm = math.hypot(1, mm); dx, dy = 1 / nrm, mm / nrm
        cv2.line(rv, (int((xt - dx * 560) / 2), int((yy - dy * 560) / 2)), (int((xt + dx * 560) / 2), int((yy + dy * 560) / 2)), 255, 20)
        tau += 1 / 30
    if t >= B(K_TAN):                            # ...and all my tangents light the rest
        for i in range(44):
            xx = 30 + i * (W - 60) / 43
            uu = eo_expo(prog(t, B(K_TAN) + abs(xx - 960) / 5000, B(K_TAN) + abs(xx - 960) / 5000 + 0.25))
            if uu <= 0: continue
            yy = wave_y(xx, t); mm = wave_slope(xx, t); nrm = math.hypot(1, mm); dx, dy = 1 / nrm, mm / nrm
            Lh = 330 * uu
            cv2.line(rv, (int((xx - dx * Lh) / 2), int((yy - dy * Lh) / 2)), (int((xx + dx * Lh) / 2), int((yy + dy * Lh) / 2)), 255, 26)
    rv = cv2.GaussianBlur(rv, (0, 0), 3)
    arr = ((face.astype(np.uint16) * rv) // 255).astype(np.uint8)
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, 960)
    buf = np.zeros((540, stride), np.uint8); buf[:, :960] = arr
    sf = cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_A8, 960, 540, stride)
    for cc, aa in ((c, 0.95), (g, 0.35)):
        cc.save(); cc.scale(2, 2); rgba(cc, BONE, aa); cc.mask_surface(sf, 0, 0); cc.restore()

def face_on_line(c, g, x, y, h, a, t):
    """the face standing on a line at (x, y): the bottom of the mask's figure (y 475) on the line, h px tall"""
    if a <= 0.01: return
    m = lish_face_mask(); k = h / (475 - 87)
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, 960)
    if 'sf' not in _LF:
        buf = np.zeros((540, stride), np.uint8); buf[:, :960] = m; _LF['buf'] = buf
        _LF['sf'] = cairo.ImageSurface.create_for_data(buf, cairo.FORMAT_A8, 960, 540, stride)
    for cc, aa in ((c, a), (g, 0.4 * a)):
        cc.save(); cc.translate(x, y); cc.scale(k, k); cc.translate(-465, -475)
        rgba(cc, BONE, aa); cc.mask_surface(_LF['sf'], 0, 0); cc.restore()

def lish_trace(c, g, x, y, sc, t, a=1.0, rot=0.0, reveal=1.0):
    """Lishenna sitting, as phosphor line art; the feet swing on the beat (the A/B pair)"""
    b = int(math.floor((t - T0) / P)) % 2 == 1
    phosphor(c, g, 'sit_b' if b else 'sit', x, y, sc, SIT_SEAT, t, BONE, a, rot, 1.0, reveal, 0.35)

def lish_sit(c, x, y, sc, a=1.0, rot=0.0, t=0.0, swing=True):
    if a <= 0.003: return
    b = swing and int(math.floor((t - T0) / P)) % 2 == 1
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc); c.translate(-SIT_SEAT[0], -SIT_SEAT[1])
    c.set_source_surface(surf('n_lish_sit_b_hd' if b else 'n_lish_sit_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint_with_alpha(min(1, a)); c.restore()

# ================================================================ v2 round 6: ACHILLES AND THE TORTOISE  [B48, B60)
# replaces the gap / Zeno / near shots of v1 (the fingertip and the loose end). the fastest thing in the world can never
# catch the slowest: each beat Ralmia (cyan line art) reaches the place where Lishenna (bone line art) was -- and Lishenna
# has strolled on by half that. after every step the camera zooms x2 so the picture repeats exactly (Zeno's halving).
# her song, the lavender string, trails from her microphone back to just ahead of Ralmia's hand. k56: half a beat stopped,
# only the string shakes. k58: pull back; a loupe on the gap: d != 0. "Nothing, not one thing, can touch her."
STROLL = os.path.exists(f'{WORK}/assets/n_trace_stroll_a.png')
if STROLL:
    _A = json.load(open(os.path.join(WORK, '..', 'gen', '_qa', 'round4', 'anchors_v2.json')))['lish_stroll']
    L_FEET, L_H, L_BACK = tuple(_A['feet']), _A['height'], _A['back_x']
else:                                             # her standing picture, mirrored (n_trace_stand_m): she just stands and sings
    L_FEET, L_H, L_BACK = (960, 1050), 1000, 668
L_MIC = (L_BACK + 70, L_FEET[1] - 0.62 * L_H)    # roughly her hand / microphone side (canvas px)
A_LX, A_GY, A_LS = 1210, 860, 0.56                # where her back sits, the ground, her scale
A_G = 700                                         # screen gap from Ralmia's hand to Lishenna's back at the start of each step
A_RS, A_RY = 0.40, -330                           # Ralmia's scale; her fingertip's height above the ground
DASH_TIP = (1843, 539)                            # her outstretched fingertip in n_dash_full
def lish_walker(c, g, x_back, t, n, a=1.0):
    name = ('stroll_b' if n % 2 else 'stroll_a') if STROLL else 'stand_m'
    fx = x_back + (L_FEET[0] - L_BACK) * A_LS
    bob = (6 * abs(math.sin(math.pi * (t - T0) / P))) if STROLL else 0
    phosphor(c, g, name, fx, A_GY - bob, A_LS, L_FEET, t, BONE, a, 0.0, 1.0, 1.0, 0.4)
    return (fx + (L_MIC[0] - L_FEET[0]) * A_LS, A_GY - bob + (L_MIC[1] - L_FEET[1]) * A_LS)

def ralmia_flyer(c, g, hx, t, a=1.0, ghosts=0.0):
    hy = A_GY + A_RY
    for k, aa in ((2, 0.15), (1, 0.3)):
        if ghosts > 0.02: phosphor(c, g, 'dash', hx - 120 * k * ghosts, hy, A_RS, DASH_TIP, t, CYAN, aa * a, 0.0, 0.0, 1.0, 0.2)
    phosphor(c, g, 'dash', hx, hy, A_RS, DASH_TIP, t, CYAN, a, 0.0, 1.0, 1.0, 0.55)
    return hx, hy

def zoom_grid(c, P_, Zc, a=1.0):
    lv = math.log2(max(Zc, 1e-6))
    for j in range(2):
        cell = 40 * 2 ** (lv % 1 + j)
        aa = a * (0.07 * (1 - (lv % 1)) + 0.03 if j == 0 else 0.07 * (lv % 1))
        rgba(c, BONE, aa); c.set_line_width(1)
        x = P_ % cell
        while x < W: c.move_to(x, 0); c.line_to(x, H); x += cell
        y = A_GY % cell
        while y < H: c.move_to(0, y); c.line_to(W, y); y += cell
        c.stroke()

def s_achilles(c, g, t):
    from scenes2 import song_string
    fill_bg(c, INK)
    fx = {}
    kk = (t - T0) / P
    if kk < 49:                                   # Ralmia comes in out of the white of LIGHT; Lishenna already ahead
        n, approach, zoom, kf = 0, 0.0, 0.0, 0.0
        enter = eo_expo(prog(t, B(48), B(48) + 0.45))
    else:
        kr = kk - 49
        frozen = 7.0 <= kr < 7.5
        kf = 7.0 if frozen else (7.0 + (kr - 7.5) * 2 if 7.5 <= kr < 8.0 else kr)
        n = math.floor(kf); ph = kf - n
        approach = eo_cubic(clamp(ph / 0.45)); zoom = eo_expo(clamp((ph - 0.5) / 0.4))
        enter = 1.0
    if kk >= 58:                                  # the pull-back (see below): the last step's state, held
        n, approach, zoom = 9, 1.0, 0.0
    s_ = 2 ** zoom; P_ = A_LX + A_G                  # zoom x2 about a point ahead of her: the picture repeats
    Zc = 2 ** (n + zoom)
    lb = A_LX + (A_G / 2) * approach              # her back, strolling on
    hx = A_LX - A_G + A_G * approach              # Ralmia's hand reaches where her back was
    lb, hx = P_ + (lb - P_) * s_, P_ + (hx - P_) * s_
    hx = lerp(-500, hx, enter)
    frozen_now = kk >= 49 and 7.0 <= kk - 49 < 7.5
    zoom_grid(c, P_, Zc, 1.0)
    line(c, 0, A_GY, W, A_GY, BONE, 0.45, 1.4)
    if kk < 58:
        mic = lish_walker(c, g, lb, t, n)
        rh = ralmia_flyer(c, g, hx, t, eo_cubic(prog(t, B(48), B(48) + 0.2)), (1 - approach) * (approach > 0) + 0.6 * (1 - enter))
        # her song: the string from her microphone back to just ahead of Ralmia's hand
        end = (rh[0] + 14, rh[1] - 4)
        pts = [(lerp(end[0], mic[0], u), lerp(end[1], mic[1], u) + 26 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 70)]
        song_string(c, g, pts, t, 3.4, 0.6, 9 if frozen_now else 5, 1.0, LISH, 'end', 90, 420)
        for kb in range(48, math.floor(kk) + 1):  # a wavefront from her, each beat: the song reaches Ralmia (Ralmia can't reach her)
            u = prog(t, B(kb), B(kb) + 1.1)
            if 0 < u < 1:
                rgba(c, LISH, 0.35 * (1 - u)); c.set_line_width(2); c.new_path(); c.arc(*mic, 40 + 1300 * eo_cubic(u), 0, 6.283); c.stroke()
        # the distance
        dval = 0.5 ** n * (1 - 0.5 * approach)
        y_d = A_GY - 560
        line(c, rh[0], y_d, lb, y_d, CYAN, 0.9, 1.6)
        line(c, rh[0], y_d - 10, rh[0], y_d + 10, CYAN, 0.9, 1.6); line(c, lb, y_d - 10, lb, y_d + 10, CYAN, 0.9, 1.6)
        text(c, 'monom', f'd = {dval:.6f}', (rh[0] + lb) / 2, y_d - 18, 28, CYAN, enter, align='center')
        if kk >= 49:
            terms = ' + '.join(f'1/{2 ** (i + 1)}' for i in range(min(n + 1, 4))) + (' + ...' if n >= 4 else '')
            text(c, 'math', f'{terms}  =  {1 - dval:.6f}', 130, 1000, 30, BONE, 0.85)
        text(c, 'mono', f'zoom  x{Zc:,.0f}'.replace(',', ' '), W - 130, 1000, 26, BONE, 0.7, align='right', track=0.1)
        text(c, 'mono', 'lim d -> 0     d != 0', W - 130, 960, 22, BONE, 0.5, align='right', track=0.1)
        if t < B(52):
            words(c, 'serif', [('Nothing,', B(48)), ('not', B(48.5)), ('one', B(49)), ('thing,', B(49.5))], t,
                  W - 130 - text_w('serif', 'Nothing, not one thing,', 80), 200, 80, BONE, 0.95)
        else:
            words(c, 'serif', [('can', B(54)), ('touch', B(54.5)), ('her.', B(55))], t,
                  W - 130 - text_w('serif', 'can touch her.', 92), 200, 92, BONE, 0.95)
        fx['ab'] = 3 * pulse(t, B(49 + n + 0.5), 0.15) + 3 * pulse(t, B(48), 0.2)
        fx['flash'] = 0.9 * (1 - eo_cubic(prog(t, B(48), B(48) + 0.25)))
    else:
        # k58: the pull-back. at this distance they look as if they touch -- the loupe says they don't
        u = eo_expo(prog(t, B(58), B(58) + 0.5))
        gap = 5.0
        lb2 = A_LX + 40; hx2 = lb2 - gap
        mic = lish_walker(c, g, lb2, t, 9)
        rh = ralmia_flyer(c, g, hx2, t)
        end = (rh[0] + 4, rh[1] - 4)
        pts = [(lerp(end[0], mic[0], v), lerp(end[1], mic[1], v) + 10 * math.sin(math.pi * v)) for v in np.linspace(0, 1, 50)]
        song_string(c, g, pts, t, 3.4, 0.6, 4, 1.0, LISH, 'end', 90, 420)
        lp = (hx2 + gap / 2, rh[1]); lc = (lerp(lp[0], 760, u), lerp(lp[1], 300, u)); R_ = lerp(10, 170, u); Zl = 5
        c.save(); c.new_path(); c.arc(*lc, R_, 0, 6.283); c.clip(); fill_bg(c, INK)
        c.translate(*lc); c.scale(Zl, Zl); c.translate(-lp[0], -lp[1])
        phosphor(c, g, 'dash', hx2, rh[1], A_RS, DASH_TIP, t, CYAN, 1.0, 0.0, 0.0, 1.0, 0.0)
        lish_walker(c, g, lb2, t, 9)
        c.restore()
        for cc, aa in ((c, 0.85), (g, 0.4)):
            rgba(cc, BONE, aa); cc.set_line_width(2); cc.new_path(); cc.arc(*lc, R_, 0, 6.283); cc.stroke()
        line(c, lp[0] + (lc[0] - lp[0]) * 0.0, lp[1], lc[0] + R_ * 0.7, lc[1] + R_ * 0.7, BONE, 0.4 * u, 1.2)
        ul = eo_cubic(prog(t, B(58.5), B(58.5) + 0.2))
        text(c, 'monom', 'd != 0', lc[0] - R_ - 30, lc[1] + 10, 30, CYAN, ul, align='right')
        qs = 'Nothing, not one thing, can touch her.'
        words(c, 'serif', [(qs, B(58.5))], t, W - 130 - text_w('serif', qs, 64), 200, 64, BONE, 0.9)
        text(c, 'mono', type_on('— abandoned lab note, project ŌMETEŌTL', t, B(59), 0.02), W - 130, 260, 20, BONE, 0.5, align='right')
        fx['ab'] = 3 * pulse(t, B(58), 0.2)
    fx['grain'] = 0.04
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ S13 SINE + TANGENTS  [B80, B88)
LAM = 640.0
def theta(t): return math.pi / 2 + math.pi * (t - B(80)) / P       # crest on every even beat
def wave_xe(t): return lerp(600, -60, eio_cubic(prog(t, B(84), B(84.6))))
def wave_y(x, t):
    return CC_Y - CC_R * math.sin(theta(t) - (x - wave_xe(t)) * 2 * math.pi / LAM)
def wave_slope(x, t):
    return CC_R * (2 * math.pi / LAM) * math.cos(theta(t) - (x - wave_xe(t)) * 2 * math.pi / LAM)

def s_sine(c, g, t):
    fill_bg(c, INK)
    fx = {}
    dotgrid(c, BONE, 0.05)
    xe = wave_xe(t)
    th = theta(t)
    R = CC_R; cx, cy = CC_X + (xe - 600), CC_Y
    # axis
    line(c, 0, cy, W, cy, BONE, 0.18, 1)
    # unit circle + rotating radius (slides out when the tangents arrive)
    if cx > -R - 20:
        line(c, cx - R - 30, cy, cx + R + 30, cy, BONE, 0.3, 1); line(c, cx, cy - R - 30, cx, cy + R + 30, BONE, 0.3, 1)
        rgba(c, BONE, 0.9); c.set_line_width(2.5); c.new_path(); c.arc(cx, cy, R, 0, 6.283); c.stroke()
        px, py = cx + R * math.cos(th), cy - R * math.sin(th)
        for cc, aa in ((c, 1), (g, 0.7)):
            line(cc, cx, cy, px, py, CYAN, aa, 2.5)
            rgba(cc, CYAN, aa); cc.arc(px, py, 9, 0, 6.283); cc.fill()
        line(c, px, py, px, cy, CYAN, 0.35, 1.2)
        c.set_dash([5, 6]); line(c, px, py, xe, py, BONE, 0.5, 1.2); c.set_dash([])
        deg = (math.degrees(th) % 360)
        text(c, 'mono', f'a = {deg:05.1f}°', cx - R, cy + R + 60, 22, BONE, 0.7, track=0.1)
        text(c, 'mono', f'sin a = {math.sin(th):+.3f}', cx - R, cy + R + 92, 22, CYAN, 0.85, track=0.1)
    # the wave, emitted from xe at one wavelength per revolution
    front = xe + (t - B(80)) * LAM / (2 * P) if t < B(84) else W + 100
    x1 = min(W + 20, front)
    if x1 > xe:
        for cc, aa, lw, col in ((c, 0.95, 3, BONE), (g, 0.35 + 0.65 * pulse(t, B(K_SINE), 0.6), 4, CYAN)):
            rgba(cc, col, aa); cc.set_line_width(lw); cc.new_path()
            x = xe
            cc.move_to(x, wave_y(x, t))
            while x < x1:
                x = min(x1, x + 6); cc.line_to(x, wave_y(x, t))
            cc.stroke()
    # labels
    if t < B(84):
        lyric(c, [('If', 37.03), ("I'm", 37.50), ('a', 38.06)], t)
        if t >= B(K_SINE):
            glyph_pop(c, 'thin', 'SINE WAVE', 120, 1000, 150, BONE, t, B(K_SINE), P / 8, track=0.12, drop=0)
            text(c, 'monom', type_on('y = sin(a)', t, B(K_SINE) + 0.1, 0.03), W - 130, 1000, 30, CYAN, 0.9, align='right')
    else:
        # one tangent, with "you" sitting on it; it hops on the beat and rocks with the wave
        xt = None
        if t >= B(84.5):
            ride = prog(t, B(84.5), B(88))
            xt = lerp(1700, 240, ride * 0.85 + 0.15 * eio_cubic(ride))
        if t >= B(84.5): tangent_face(c, g, t)
        # all my tangents
        if t >= B(K_TAN):
            for i in range(44):
                xx = 30 + i * (W - 60) / 43
                de = abs(xx - (xt or 960)) / 5000
                uu = eo_expo(prog(t, B(K_TAN) + de, B(K_TAN) + de + 0.25))
                if uu <= 0: continue
                yy = wave_y(xx, t); m = wave_slope(xx, t)
                nrm = math.hypot(1, m); dx, dy = 1 / nrm, m / nrm
                Lh = 330 * uu
                line(c, xx - dx * Lh, yy - dy * Lh, xx + dx * Lh, yy + dy * Lh, BONE, 0.32, 1.2)
        if xt is not None:
            ua = eo_cubic(prog(t, B(84.5), B(84.5) + 0.15))
            yy = wave_y(xt, t); m = wave_slope(xt, t)
            nrm = math.hypot(1, m); dx, dy = 1 / nrm, m / nrm
            Lh = 560 * ua
            for cc, aa in ((c, 1), (g, 0.3)):
                line(cc, xt - dx * Lh, yy - dy * Lh, xt + dx * Lh, yy + dy * Lh, BONE, 0.9 * aa, 2)
            for cc, aa in ((c, 1), (g, 0.8)):
                rgba(cc, CYAN, aa * ua); cc.arc(xt, yy, 8, 0, 6.283); cc.fill()
            text(c, 'mono', f"y' = {-m:+.3f}", W - 130, 1000, 26, CYAN, 0.85 * ua, align='right', track=0.1)
        lyric(c, [('then', 38.86), ('you', 39.02), ('can', 39.24), ('sit', 39.46), ('on', 39.70), ('all', 39.92), ('my', 40.20)], t)
        if t >= B(K_TAN):
            glyph_pop(c, 'thin', 'TANGENTS', 120, 1000, 150, BONE, t, B(K_TAN), P / 8, track=0.12, drop=0)
    fx['ab'] = 3 * pulse(t, B(K_SINE), 0.3) + 3 * pulse(t, B(K_TAN), 0.25) + 2 * pulse(t, B(85), 0.2) + 2 * pulse(t, B(86), 0.2)
    fx['flash'] = 0.3 * (1 - prog(t, B(80), B(80) + 0.1))
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ S14 INFINITY + LIMITATION  [B88, B95)
YA = 330
DASH_HAND = (1748, 535)                 # her outstretched palm core in n_dash_full
def asym_gap(x, t):
    s = 110 * max(0, t - B(88))
    return 560 / (1 + max(0, x + s - 60) / 150) ** 1.05

def lemniscate(cc, cx, cy, a, frac=1.0, n=240):
    cc.new_path()
    for i in range(int(n * frac) + 1):
        s = 2 * math.pi * i / n
        d = 1 + math.sin(s) ** 2
        x, y = cx + a * math.cos(s) / d, cy + a * math.sin(s) * math.cos(s) / d
        (cc.move_to if i == 0 else cc.line_to)(x, y)

def s_infinity(c, g, t):
    fill_bg(c, INK)
    fx = {}
    dotgrid(c, BONE, 0.05)
    # asymptote (becomes "you")
    ua = eo_expo(prog(t, B(88), B(88) + 0.3))
    you = prog(t, B(92), B(92) + 0.05)
    if you < 1:
        c.set_dash([10, 8]); line(c, 0, YA, W * ua, YA, BONE, 0.5, 1.5); c.set_dash([])
    if you > 0:
        for cc, aa in ((c, 0.95), (g, 0.4 * pulse(t, B(92), 0.6) + 0.1)):
            line(cc, 0, YA, W, YA, BONE, aa, 3)
    # v2: the asymptote is her: her face rests on it, clearer the closer the curve comes
    LX = 1470
    # the curve, always approaching
    xh = lerp(60, W + 40, eo_cubic(prog(t, B(88), B(89.5))))
    for cc, aa, lw, col in ((c, 1, 3, BONE), (g, 0.35, 4, CYAN)):
        rgba(cc, col, aa); cc.set_line_width(lw); cc.new_path()
        x = 60; cc.move_to(x, YA + asym_gap(x, t))
        while x < xh: x = min(xh, x + 8); cc.line_to(x, YA + asym_gap(x, t))
        cc.stroke()
    hx = min(xh, W - 260); hy = YA + asym_gap(hx, t)
    near = clamp(1 - asym_gap(hx, t) / 120)                        # 0 far .. 1 as close as it ever gets
    face_on_line(c, g, LX, YA + 30, 330, eo_cubic(prog(t, B(88), B(88) + 0.4)) * (0.35 + 0.65 * near), t)
    for cc in (c, g):
        rgba(cc, CYAN, 1); cc.arc(hx, hy, 8, 0, 6.283); cc.fill()
    line(c, hx + 24, YA + 4, hx + 24, hy - 4, CYAN, 0.8, 1.2)
    text(c, 'mono', f'd = {asym_gap(hx, t) / 560:.6f}', hx + 36, (YA + hy) / 2 + 8, 22, CYAN, 0.9)
    # infinity: drawn big on the word, then sent to the far end of the asymptote
    if t >= B(K_INF):
        ud = eo_cubic(prog(t, B(K_INF), B(K_INF) + 0.35))
        um = eio_cubic(prog(t, B(91), B(91) + 0.35))
        lx, ly, la = lerp(1000, W - 150, um), lerp(700, YA, um), lerp(440, 95, um)
        for cc, aa, lw, col in ((c, 1, lerp(10, 4, um), BONE), (g, 0.6 + 0.4 * pulse(t, B(K_INF), 0.5), lerp(12, 6, um), CYAN)):
            lemniscate(cc, lx, ly, la, ud); rgba(cc, col, aa); cc.set_line_width(lw); cc.stroke()
        s = 2 * math.pi * (t - B(K_INF)) / (2 * P)
        d = 1 + math.sin(s) ** 2
        px, py = lx + la * math.cos(s) / d, ly + la * math.sin(s) * math.cos(s) / d
        if ud >= 1:
            for cc in (c, g):
                rgba(cc, CYAN, 1); cc.arc(px, py, lerp(11, 6, um), 0, 6.283); cc.fill()
        if um > 0:
            text(c, 'monom', 'x → ∞', W - 150, YA + 70, 26, BONE, 0.8 * um, align='center')
    # lyric
    if t < B(90.8):
        lyric(c, [('If', 40.95), ('I', 41.28), ('approach', 41.34)], t)
    else:
        lyric(c, [('then', 42.24), ('you', 42.70), ('can', 42.94), ('be', 43.14), ('my', 43.40)], t, y=900)
    # LIMITATION sits on the asymptote; the lim notation underneath
    if t >= B(K_LIM):
        glyph_pop(c, 'bold', 'LIMITATION', 960, YA - 12, 170, BONE, t, B(K_LIM), P / 8, align='center', track=0.08, drop=60)
        uu = eo_cubic(prog(t, B(K_LIM + 0.5), B(K_LIM + 0.5) + 0.2))
        text(c, 'serifr', 'lim', 1180, 930, 110, BONE, uu)
        text(c, 'mono', 'x→∞', 1186, 975, 26, BONE, 0.8 * uu)
        text(c, 'serif', 'f(x) = you', 1340, 930, 92, BONE, uu)
    fx['flash'] = 0.3 * pulse(t, B(K_INF), 0.12) + 0.2 * pulse(t, B(K_LIM), 0.1)
    fx['ab'] = 3 * pulse(t, B(K_INF), 0.3) + 4 * pulse(t, B(K_LIM), 0.25) + 2 * pulse(t, B(92), 0.2)
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ S15 OSCILLOSCOPE  [B95, B103)
SX0, SY0, SX1, SY1 = 160, 150, 1760, 930
# v2 round 2: on CURRENT the scope goes to X-Y mode and the beam draws her face; AC = it alternates between her and
# Lishenna on every 8th; DC = both, steady, then flattened into the line. masks: prep7.py (n_scope_*, 960x540)
_SCF = {}
_SYY, _SXX = np.mgrid[0:540, 0:960].astype(np.float32)
def face_trace(c, g, name, t, col, a=1.0, wob=1.0, reveal=1.0, squash=0.0):
    if a <= 0.01: return
    if name not in _SCF: _SCF[name] = cv2.imread(f'{WORK}/assets/{name}.png', cv2.IMREAD_GRAYSCALE).astype(np.float32)
    m = _SCF[name]
    if wob > 0:
        ph = t * 9
        m = cv2.remap(m, _SXX + wob * (0.9 * np.sin(_SYY / 11 + ph) + 0.6 * np.sin(_SYY / 37 - ph * 1.7)), _SYY, cv2.INTER_LINEAR)
    if reveal < 1: m = m.copy(); m[int(540 * reveal):] = 0
    arr = np.ascontiguousarray(np.clip(m * a, 0, 255).astype(np.uint8))
    sf = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_A8, 960, 540, 960)
    for cc, k in ((c, 1.0), (g, 0.55 if col is CYAN else 0.3)):
        cc.save(); cc.translate(0, 540); cc.scale(1, max(1 - squash, 0.004)); cc.translate(0, -540); cc.scale(2, 2)
        rgba(cc, col, k); cc.mask_surface(sf, 0, 0); cc.restore()

def trace_y(x, t, A, lam):
    ph = math.pi * (t - B(95)) / P
    return 540 + A * math.sin(2 * math.pi * (x - SX0) / lam - ph)

def s_scope(c, g, t):
    fill_bg(c, INK)
    fx = {}
    on_x = eo_expo(prog(t, B(K_SWITCH), B(K_SWITCH) + 0.08))
    on_y = eo_expo(prog(t, B(K_SWITCH) + 0.06, B(K_SWITCH) + 0.24))
    fade_out = prog(t, B(102.5), B(103) - 0.03)
    # amplitude / wavelength by mode
    beat = math.floor((t - T0) / P)
    A = 195 * (1 + 0.15 * pulse(t, B(beat), 0.3))
    lam = 400
    if t >= B(K_AC):
        A = 240 * (1 + 0.25 * pulse(t, B(beat), 0.25) + 0.15 * pulse(t, B(beat + 0.5), 0.2)); lam = 300
    if t >= B(K_DC):
        dd = t - B(K_DC)
        A = 240 * math.exp(-dd * 16) * math.cos(dd * 60)
    c.push_group()
    fill_bg(c, INK)
    # graticule
    ga = 1 - fade_out
    for i in range(11):
        x = SX0 + i * (SX1 - SX0) / 10
        line(c, x, SY0, x, SY1, BONE, (0.3 if i == 5 else 0.12) * ga, 1)
    for j in range(9):
        y = SY0 + j * (SY1 - SY0) / 8
        line(c, SX0, y, SX1, y, BONE, (0.3 if j == 4 else 0.12) * ga, 1)
    for i in range(51):
        x = SX0 + i * (SX1 - SX0) / 50
        line(c, x, 540 - 6, x, 540 + 6, BONE, 0.3 * ga, 1)
    mode = 'DC' if t >= B(K_DC) else 'AC'
    text(c, 'mono', 'CH1   2.00 V/div', SX0 + 14, SY0 + 34, 22, BONE, 0.7 * ga, track=0.1)
    for i, md in enumerate(('AC', 'DC')):
        on = (md == mode)
        x = SX1 - 150 + i * 74
        rgba(c, CYAN if on else BONE, (0.9 if on else 0.3) * ga); c.set_line_width(1.4)
        c.rectangle(x, SY0 + 12, 58, 30); c.fill() if on else c.stroke()
        text(c, 'monom', md, x + 29, SY0 + 35, 20, INK if on else BONE, (1 if on else 0.4) * ga, align='center')
    text(c, 'mono', '50 ms/div      f = 2.17 Hz      130 BPM', SX0 + 14, SY1 - 18, 20, BONE, 0.5 * ga, track=0.1)
    xy = prog(t, B(K_CURRENT) - 0.05, B(K_CURRENT) + 0.12)          # v2: X-Y mode from CURRENT
    # trace with phosphor persistence
    for k, aa in ((3, 0.12 * (1 - xy)), (2, 0.25 * (1 - xy)), (1, 0.45 * (1 - xy)), (0, 1.0 - 0.9 * xy)):
        tt = t - k / 60
        Ak = A
        for cc, a2, lw, col in ((c, aa, 3, CYAN), (g, aa * 0.8, 5, CYAN)):
            rgba(cc, col if t < B(K_DC) else (BONE if cc is c else CYAN), a2); cc.set_line_width(lw); cc.new_path()
            x = SX0 if fade_out <= 0 else 0
            xend = SX1 if fade_out <= 0 else W
            x0_ = lerp(SX0, 0, fade_out); x1_ = lerp(SX1, W, fade_out)
            x = x0_; cc.move_to(x, trace_y(x, tt, Ak, lam))
            while x < x1_: x = min(x1_, x + 6); cc.line_to(x, trace_y(x, tt, Ak, lam))
            cc.stroke()
    # v2: the faces, drawn by the beam
    if t >= B(K_CURRENT):
        rv = prog(t, B(K_CURRENT), B(K_CURRENT) + P)
        if rv < 1:                                                    # the raster beam drawing her in
            by_ = 40 + 1000 * rv
            line(c, SX0, by_ - 40, SX1, by_ - 40, CYAN, 0.6, 2); line(g, SX0, by_ - 40, SX1, by_ - 40, CYAN, 0.8, 4)
        sq = eio_cubic(fade_out)
        if t < B(K_AC):
            face_trace(c, g, 'n_scope_ralmia', t, CYAN, 1.0, 1.0, min(1.0, rv * 1.04))
        elif t < B(K_DC):
            n8 = int((t - B(K_AC)) / (P / 2)); f8 = ((t - B(K_AC)) / (P / 2)) % 1.0
            sw = 1 - prog(f8, 0, 0.18)                                # a flash of both at each switch
            who, oth = ('n_scope_ralmia', 'n_scope_lish') if n8 % 2 == 0 else ('n_scope_lish', 'n_scope_ralmia')
            face_trace(c, g, who, t, CYAN if who == 'n_scope_ralmia' else BONE, 1.0, 1.6)
            face_trace(c, g, oth, t, CYAN if oth == 'n_scope_ralmia' else BONE, 0.5 * sw, 1.6)
        else:
            face_trace(c, g, 'n_scope_ralmia', t, CYAN, 0.9, 0.0, 1.0, sq)
            face_trace(c, g, 'n_scope_lish', t, BONE, 0.9, 0.0, 1.0, sq)
        text(c, 'monom', 'X-Y', SX1 - 228, SY0 + 35, 20, CYAN, 0.9 * (1 - fade_out), align='center')
        text(c, 'mono', 'CH1  me' + ('      CH2  you' if t >= B(K_AC) else ''), SX0 + 14, SY0 + 64, 20, BONE, 0.6 * (1 - fade_out), track=0.1)
    # CURRENT rides along the top
    if B(K_CURRENT) <= t < B(K_AC):
        f = fonts()['heavy']; size = 170
        lv = 1 - prog(t, B(99.75), B(K_AC))
        for i, ch in enumerate('CURRENT'):
            ti = B(K_CURRENT) + i * P / 8
            u = prog(t, ti, ti + 0.1)
            if u <= 0: continue
            x = 330 + i * 190
            y = 300 + 0.15 * (trace_y(x + 40, t, A, lam) - 540) - 60 * (i % 2)
            gl_ = f.glyphs(ch, x, y, size)[0]
            c.new_path(); f.glyph_path(c, gl_['g'], x, y - 40 * (1 - eo_back(u, 2)), size)
            rgba(c, BONE, lv * min(1, u * 3)); c.fill()
    # AC: letters made of a wave; DC: flat and solid
    f = fonts()['heavy']; size = 330
    if B(K_AC) <= t < B(K_DC):
        ua = eo_expo(prog(t, B(K_AC), B(K_AC) + 0.15)) * (1 - prog(t, B(101.75), B(K_DC)))
        amp = 16 + 22 * pulse(t, B(beat), 0.3) + 10 * pulse(t, B(beat + 0.5), 0.2)
        ph = math.pi * (t - B(95)) / P * 2
        c.new_path(); f.text_path(c, 'AC', 1700, 900, size, align='right', track=0.04)
        warp_path(c, lambda x, y: (x, y + amp * math.sin(x / 42 - ph)))
        rgba(c, INK, 0.88 * ua); c.fill_preserve()
        rgba(c, BONE, ua); c.set_line_width(4); c.stroke()
    if t >= B(K_DC):
        ud = eo_expo(prog(t, B(K_DC), B(K_DC) + 0.12))
        s_ = 1.12 - 0.12 * ud
        c.save(); c.translate(1700, 900); c.scale(s_, s_); c.translate(-1700, -900)
        text(c, 'heavy', 'DC', 1700, 900, size, BONE, ud * (1 - fade_out), align='right', track=0.04)
        c.restore()
    pat = c.pop_group()
    # CRT turn-on (mirror of the 14.7 s turn-off)
    if t >= B(K_SWITCH):
        sy = max(on_y, 0.004); sx = max(on_x, 0.001)
        m = cairo.Matrix(); m.translate(960, 540); m.scale(1 / sx, 1 / sy); m.translate(-960, -540)
        pat.set_matrix(m); c.set_source(pat); c.paint()
        if on_y < 1:
            rgba(g, BONE, 1 - on_y); g.rectangle(960 - 960 * sx, 536, 1920 * sx, 8); g.fill()
    else:
        # the tail of "limitation" (shouldn't happen: scene starts at K_SWITCH)
        pass
    lyric(c, [('Switch', 44.18), ('my', 44.88)] if t < B(98.5) else [('to', 45.94)] if t < B(101) else
          [('to', 47.20)] if t < B(102.5) else [('and', 47.70), ('then', 47.92)], t, x=190, y=1035, size=58)
    fx['flash'] = 0.5 * pulse(t, B(K_SWITCH), 0.1) + 0.3 * pulse(t, B(K_DC), 0.1)
    fx['ab'] = 5 * pulse(t, B(K_AC), 0.25) + 6 * pulse(t, B(K_DC), 0.2) + 2 * pulse(t, B(beat), 0.15) * (t >= B(K_AC)) * (t < B(K_DC))
    hud(c, t, True, a=0.6)
    return fx

# ================================================================ S16 BLIND MY VISION  [B103, B106.5)
def s_blind(c, g, t):
    fill_bg(c, INK)
    fx = {}
    sc = lerp(1.12, 1.2, prog(t, B(103), B(106.5)))          # same framing as INITIALIZATION (11 s), mirrored
    axs, ays = 960, 540
    def img(name, a, mult_line=False):
        c.save(); c.translate(axs, ays); c.scale(sc, sc); c.translate(-EYEC[0], -EYEC[1])
        if mult_line:
            rgba(c, PAPER, a); c.rectangle(0, 0, W, H); c.fill()
            c.set_operator(cairo.OPERATOR_MULTIPLY)
        c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a)
        c.set_operator(cairo.OPERATOR_OVER); c.restore()
    drain = eio_cubic(prog(t, B(104), B(K_VISION)))
    closed = prog(t, B(K_VISION), B(K_VISION) + 0.1)
    if closed < 1:
        img('n_eye_open_line', 1, True)
        img('n_eye_open_hd', 1 - drain)
    if closed > 0:
        img('n_eye_closed_line', closed, True)
    # iris apertures (both eyes): blades close on the beat
    R0 = IRIS_R * sc
    ra = 0.62
    for kb, rv in ((K_BLIND, 0.45), (104, 0.31), (104.5, 0.19), (105, 0.09), (K_VISION, 0)):
        if t >= B(kb): ra = lerp(ra, rv, eo_expo(prog(t, B(kb), B(kb) + 0.12)))
    ap = (1 - closed)
    if ap > 0 and t >= B(103.2):
        nb = 8
        for ix0, iy0 in IRISES:
            ix, iy = axs + (ix0 - EYEC[0]) * sc, ays + (iy0 - EYEC[1]) * sc
            for cc, aa, lw in ((c, 0.85 * ap, 1.6), (g, 0.6 * ap, 3)):
                rgba(cc, CYAN, aa); cc.set_line_width(lw)
                for i in range(nb):
                    a0 = 2 * math.pi * i / nb + (0.62 - ra) * 1.6
                    px, py = ix + math.cos(a0) * ra * R0, iy + math.sin(a0) * ra * R0
                    tx_, ty_ = -math.sin(a0), math.cos(a0)
                    cc.move_to(px - tx_ * 10, py - ty_ * 10); cc.line_to(px + tx_ * R0 * 0.95, py + ty_ * R0 * 0.95)
                cc.stroke()
                cc.new_path(); cc.arc(ix, iy, R0 * 0.98, 0, 6.283); cc.stroke()
        ix = axs + (IRISES[1][0] - EYEC[0]) * sc
        text(c, 'mono', f'f/{max(1.4, 0.62 / max(ra, 0.01) * 1.4):.1f}', ix + R0 + 20, ays - R0 + 10, 20, CYAN, 0.8 * ap)
    # letterbox slit: opens out of the DC line, closes after "vision"
    h = 200 * eo_expo(prog(t, B(103), B(103) + 0.3))
    h *= 1 - ei_cubic(prog(t, B(106), B(106.5) - 0.03))
    rgba(c, INK, 1); c.rectangle(0, 0, W, 540 - h); c.rectangle(0, 540 + h, W, 540 - h + 2); c.fill()
    line(c, 0, 540 - h, W, 540 - h, BONE, 0.3, 1.5); line(c, 0, 540 + h, W, 540 + h, BONE, 0.3, 1.5)
    # VISION decodes, then scrambles away (mirror of INITIALIZATION)
    yb = 540 - h - 70
    if t >= B(K_VISION) - 0.25:
        s = scramble('VISION', t, B(K_VISION), 0.031, seed=5)
        out = prog(t, B(106), B(106.5))
        if out > 0:
            rnd = random.Random(int(t * 30))
            s = ''.join(ch if rnd.random() > out else rnd.choice(GLYPHS_SCRAMBLE) for ch in s)
        text(c, 'bold', s, 960, max(yb, 300), 128, BONE, 1 - prog(t, B(106.3), B(106.5)), align='center', track=0.3)
    # progress bar running backwards
    yp = 540 + h + 70
    if h > 30:
        pr = 1 - math.floor(prog(t, B(K_BLIND), B(K_VISION)) * 8) / 8
        xL, xR = 360, 1560
        line(c, xL, yp, xR, yp, BONE, 0.25, 2)
        line(c, xL, yp, lerp(xL, xR, pr), yp, CYAN, 1, 3)
        text(c, 'mono', f'{int(pr * 100):03d}%', xR + 24, yp + 8, 22, CYAN, 0.9)
        text(c, 'mono', 'obj.vision()', xL - 24, yp + 8, 22, BONE, 0.5, align='right')
    lyric(c, [('and', 47.70), ('then', 47.92), ('blind', B(K_BLIND)), ('my', 48.54)], t, y=200)
    fx['ab'] = 3 * pulse(t, B(K_BLIND), 0.2) + 4 * pulse(t, B(K_VISION), 0.25)
    fx['grain'] = 0.035
    hud(c, t, True, a=0.6)
    return fx

# ================================================================ S17 DIZZY  [B106.5, B111.5)
def dizzy_angle(t):
    a = 0.9 * (t - B(106.5)) + 0.6 * (t - B(106.5)) ** 2
    a += 2.6 * eo_expo(prog(t, B(K_DIZ1), B(K_DIZ1) + 0.6))
    a -= 5.4 * eo_expo(prog(t, B(K_DIZ2), B(K_DIZ2) + 0.6))
    if t > B(K_DIZ2): a -= 2.4 * (t - B(K_DIZ2)) ** 1.5
    return a

def s_dizzy(c, g, t):
    fill_bg(c, INK)
    fx = {}
    cx, cy = 960, 560
    ang = dizzy_angle(t)
    grow = lerp(0.35, 1.0, eo_expo(prog(t, B(106.5), B(106.5) + 0.3)))
    col_ = 1 - ei_cubic(prog(t, B(111.0), B(111.5)))       # collapses into the spacetime origin
    c.save(); c.translate(cx, cy); c.rotate(0.05 * math.sin(t * 2.7)); c.scale(grow * col_ + 1e-3, grow * col_ + 1e-3)
    # infinite tunnel of rings (log zoom), each slightly off-centre
    zf = (t - B(106.5)) * 1.6 + 2 * eo_expo(prog(t, B(K_SO1), B(K_SO1) + 0.4)) + 2 * eo_expo(prog(t, B(K_SO2), B(K_SO2) + 0.4))
    for k in range(-2, 16):
        e = k + (zf % 1)
        r = 22 * 1.42 ** e
        if r > 1500: continue
        ox, oy = math.sin(t * 2.1 + k) * k * 4, math.cos(t * 1.7 + k * 1.3) * k * 4
        rgba(c, BONE, min(0.35, 0.05 + r / 2000)); c.set_line_width(1 + r / 600)
        c.new_path(); c.arc(ox, oy, r, 0, 6.283); c.stroke()
    # spiral arms
    for arm in range(3):
        for cc, aa, lw, col in ((c, 0.75, 2.2, BONE), (g, 0.35, 3, CYAN)):
            rgba(cc, col if arm == 0 else (BONE if cc is c else CYAN), aa * (1 if arm == 0 else 0.6)); cc.set_line_width(lw); cc.new_path()
            for i in range(260):
                th = i * 0.09
                r = 6 * th ** 1.55
                a_ = th + ang + arm * 2 * math.pi / 3
                (cc.move_to if i == 0 else cc.line_to)(math.cos(a_) * r, math.sin(a_) * r)
            cc.stroke()
    # her, adrift (gen/floating.png), turning slower than the spiral
    uf = eo_cubic(prog(t, B(106.5), B(106.5) + 0.35))
    if uf > 0:
        c.save(); c.rotate(ang * 0.35 + 0.4); s_ = 0.56 + 0.04 * uf; c.scale(s_, s_); c.translate(-961, -552)
        c.set_source_surface(surf('n_floating_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(0.95 * uf)
        c.restore()
    # DIZZY on rings, turning opposite ways
    f = fonts()['heavy']
    for kb, radius, sgn, key, size in ((K_DIZ1, 330, 1, 'heavy', 120), (K_DIZ2, 520, -1, 'thin', 110)):
        if t < B(kb): continue
        u = eo_expo(prog(t, B(kb), B(kb) + 0.3))
        ff = fonts()[key]
        s = 'DIZZY · DIZZY · DIZZY · '
        n = len(s)
        for i, ch in enumerate(s):
            if ch == ' ': continue
            a_ = sgn * ang * 0.6 + 2 * math.pi * i / n
            r_ = radius * (0.6 + 0.4 * u)
            c.save(); c.rotate(a_); c.translate(0, -r_)
            gl_ = ff.glyphs(ch, 0, 0, size)[0]
            c.new_path(); ff.glyph_path(c, gl_['g'], -gl_['w'] / 2, 0, size); rgba(c, BONE, u * 0.95); c.fill()
            c.restore()
    c.restore()
    # "so" on each lead-in
    for kb in (K_SO1, K_SO2):
        u = eo_cubic(prog(t, B(kb), B(kb) + 0.12)) * (1 - prog(t, B(kb) + 0.5, B(kb) + 0.8))
        if u > 0: text(c, 'serif', 'so', cx + 520, cy + 40, 110, BONE, u, align='center')
    lyric(c, [('so', B(K_SO1)), ('dizzy,', B(K_DIZ1))] if t < B(109.3) else [('so', B(K_SO2)), ('dizzy', B(K_DIZ2))], t,
          x=150, y=1010, size=64)
    fx['ab'] = 6 * pulse(t, B(K_DIZ1), 0.3) + 6 * pulse(t, B(K_DIZ2), 0.3) + 2.5 * abs(math.sin(t * 3))
    fx['flash'] = 0.25 * pulse(t, B(K_DIZ1), 0.1) + 0.25 * pulse(t, B(K_DIZ2), 0.1)
    hud(c, t, True, a=0.6)
    return fx

# ================================================================ S18 SPACETIME  [B111.5, B119)
O = (960, 560)
def wl_alpha(t):
    """worldline angle from the time axis (deg): <45 slower than light, 45 = light, >90 = into the past."""
    a = 0.0
    for kb, v in ((112, 0), (112.5, 26.6), (113, 42.0), (K_TRAVEL, 45.0), (114, 62), (114.5, 90), (115, 118), (K_AD, 150),
                  (117, 165), (K_BC, 178)):
        if t >= B(kb): a = lerp(a, v, eo_back(prog(t, B(kb), B(kb) + 0.2), 1.5))
    return a

def era(y):
    y = int(round(y))
    return (f'{y}', 'A.D.') if y > 0 else (f'{1 - y}', 'B.C.')

def year_at(t):
    """2026 -> 617 A.D. -> (through year 0) -> 3691 B.C.: the two numbers are from the song's code (timeTravelForTwo)."""
    if t < B(K_AD): return 2026
    if t < B(117.5): return lerp(2026, 617, eo_cubic(prog(t, B(K_AD), B(117.2))))
    if t < B(K_BC): return lerp(617, 1, ei_cubic(prog(t, B(117.5), B(K_BC))))
    return lerp(0, -3690, eo_expo(prog(t, B(K_BC), B(119) - 0.05)))

def s_spacetime(c, g, t):
    fill_bg(c, INK)
    fx = {}
    ox, oy = O
    ua = eo_expo(prog(t, B(111.5), B(111.5) + 0.35))
    # light cone
    Lc = 520 * ua
    rgba(c, BONE, 0.045); c.move_to(ox, oy); c.line_to(ox - Lc, oy - Lc); c.line_to(ox + Lc, oy - Lc); c.close_path(); c.fill()
    rgba(c, BONE, 0.025); c.move_to(ox, oy); c.line_to(ox - Lc, oy + Lc); c.line_to(ox + Lc, oy + Lc); c.close_path(); c.fill()
    c.set_dash([8, 7])
    for sx in (-1, 1):
        for sy in (-1, 1):
            line(c, ox, oy, ox + sx * Lc, oy + sy * Lc, BONE, 0.55, 1.5)
    c.set_dash([])
    line(c, ox, oy - 540 * ua, ox, oy + 520 * ua, BONE, 0.6, 1.5)
    line(c, ox - 900 * ua, oy, ox + 900 * ua, oy, BONE, 0.6, 1.5)
    text(c, 'monom', 'ct', ox + 14, oy - 500 * ua, 24, BONE, 0.8 * ua)
    text(c, 'monom', 'x', ox + 880 * ua, oy - 14, 24, BONE, 0.8 * ua)
    text(c, 'mono', 'FUTURE', ox, oy - 330, 18, BONE, 0.45 * ua, align='center', track=0.4)
    text(c, 'mono', 'PAST', ox, oy + 345, 18, BONE, 0.45 * ua, align='center', track=0.4)
    text(c, 'mono', 'ELSEWHERE', ox - 620, oy - 18, 18, BONE, 0.35 * ua, align='center', track=0.4)
    text(c, 'mono', 'ELSEWHERE', ox + 620, oy - 18, 18, BONE, 0.35 * ua, align='center', track=0.4)
    text(c, 'mono', 'c', ox + Lc * 0.72 + 12, oy - Lc * 0.72, 22, BONE, 0.6 * ua)
    # her worldline
    al = math.radians(wl_alpha(t))
    dx, dy = math.sin(al), -math.cos(al)
    if t >= B(112):
        ul = eo_expo(prog(t, B(112), B(112) + 0.25))
        Lw = 720 * ul
        line(c, ox - dx * Lw * 0.6, oy - dy * Lw * 0.6, ox, oy, CYAN, 0.3, 2)
        for cc, aa, lw in ((c, 1, 4), (g, 0.8, 6)):
            line(cc, ox, oy, ox + dx * Lw, oy + dy * Lw, CYAN, aa, lw)
        # a pulse runs out along it every beat
        ph = ((t - T0) / P) % 1
        for cc in (c, g):
            rgba(cc, BONE, 1 - ph); cc.arc(ox + dx * Lw * ph, oy + dy * Lw * ph, 7, 0, 6.283); cc.fill()
        # angle arc from the time axis
        rgba(c, CYAN, 0.6); c.set_line_width(1.4); c.new_path()
        c.arc(ox, oy, 90, -math.pi / 2, -math.pi / 2 + al); c.stroke()
        deg = wl_alpha(t)
        if deg < 89.5: s = f'v/c = {math.tan(math.radians(deg)):.2f}'
        elif deg < 90.5: s = 'v/c = ∞'
        else: s = 'dt < 0'
        text(c, 'monom', s, ox + 110, oy + 50 if deg < 90 else oy - 40, 26, CYAN, 0.9 * ul)
    # light speed crossing flash
    fl = pulse(t, B(K_TRAVEL), 0.5)
    if fl > 0.02:
        for cc in (c, g):
            rgba(cc, CYAN, 0.8 * fl); cc.set_line_width(3); cc.new_path(); cc.arc(ox, oy, 40 + 500 * (1 - fl), 0, 6.283); cc.stroke()
    if t >= B(K_TRAVEL):
        glyph_pop(c, 'thin', 'TRAVEL', 120, 1000, 160, BONE, t, B(K_TRAVEL), P / 8, track=0.25, drop=0,
                  a=1 - prog(t, B(115.5), B(K_AD)))
    # year ruler (reuses the opening ruler language) + counter
    if t >= B(114.5):
        ur = eo_expo(prog(t, B(114.5), B(114.5) + 0.3))
        rx = 1640
        yv = year_at(t)
        line(c, rx, 120, rx, 120 + 840 * ur, BONE, 0.6, 1.5)
        step = 26; per = 100
        base = math.floor(yv / per)
        offs = (yv / per - base) * step
        for i in range(-18, 19):
            yy = oy + i * step + offs
            if yy < 120 or yy > 120 + 840 * ur: continue
            yr = (base - i) * per
            big = (yr % 500 == 0)
            line(c, rx, yy, rx + (30 if big else 14), yy, BONE, 0.6 if big else 0.3, 1.2)
            if big:
                n_, e_ = era(yr)
                text(c, 'mono', f'{n_} {e_}', rx + 40, yy + 6, 15, BONE, 0.45)
        line(c, rx - 30, oy, rx + 60, oy, CYAN, 0.9, 2)
        n_, e_ = era(yv)
        text(c, 'heavy', n_, rx - 40, oy - 190, 110, BONE, ur, align='right')
        text(c, 'monom', e_, rx - 40, oy - 310, 26, CYAN, ur, align='right', track=0.2)
        line(c, rx - 40, oy - 160, rx - 4, oy - 4, CYAN, 0.4 * ur, 1)
    # A.D. / B.C. slams at the top and bottom of the time axis
    for kb, s, y in ((K_AD, 'A.D.', 250), (K_BC, 'B.C.', 990)):
        if t >= B(kb):
            u = eo_expo(prog(t, B(kb), B(kb) + 0.14))
            c.save(); c.translate(ox - 520, y); sc_ = 1.25 - 0.25 * u; c.scale(sc_, sc_)
            text(c, 'heavy', s, 0, 0, 200, BONE, min(1, u * 2), align='center')
            c.restore()
    if t < B(114.5):
        lyric(c, [('Oh,', 51.80), ('we', 51.96), ('can', 52.26)], t)
    else:
        lyric(c, [('to', 53.24)] if t < B(117) else [('to', 54.36)], t)
    fx['ab'] = 5 * pulse(t, B(K_TRAVEL), 0.3) + 5 * pulse(t, B(K_AD), 0.2) + 5 * pulse(t, B(K_BC), 0.2) + 2 * pulse(t, B(114.5), 0.2)
    fx['flash'] = 0.3 * pulse(t, B(K_TRAVEL), 0.12) + 0.2 * pulse(t, B(K_AD), 0.1) + 0.2 * pulse(t, B(K_BC), 0.1)
    hud(c, t, True, a=0.6)
    return fx

# ================================================================ S19 UNITE  [B119, B123)
FT_ = np.array([1314.0, 190.0])                 # fingertip (n_hand_gap / n_hand_tied, pixel-aligned pair)
FD = np.array([0.894, -0.449])                   # finger axis, towards the tip
FN = np.array([0.449, 0.894])                    # finger normal
WRAP_C = np.array([1247.0, 230.0])               # where the painted loops sit in n_hand_tied
TIED_AT = 0.62                                   # beats after 'unite' when the vector knot hands over to the painting
_THR = {}
def thread_pts():
    if not _THR:
        _THR['p'] = np.array(json.load(open(f'{WORK}/assets/thread_gap.json')))
    return _THR['p']

def unite_cam(t):
    u = eio_cubic(prog(t, B(119), B(123)))
    M = np.array([1340.0, 179.0])
    anc = M + (WRAP_C - M) * u
    scr = np.array([1150.0, 272.0]) + (np.array([1000.0, 390.0]) - np.array([1150.0, 272.0])) * u
    sc = lerp(1.55, 2.6, u)
    return anc, scr, sc

def thread_shape(t):
    """thread polyline (image coords) + wrap progress."""
    P0 = thread_pts().copy()
    s = np.linspace(0, 1, len(P0))
    end_target = WRAP_C - FN * 25 + FD * 8
    um = eo_back(prog(t, B(120.5), B(121)), 1.3)
    d = (end_target - P0[0]) * um
    rj = random.Random(int(t * 60))
    amp = 2.5 * (1 - um)
    P0 += np.outer((1 - s) ** 2, d)
    P0[:6] += np.array([(rj.random() - 0.5) * amp, (rj.random() - 0.5) * amp])
    return P0

def wrap_path(uw, n=120):
    """two loops around the finger, (image coords), front/back flag per point."""
    out = []
    for i in range(int(n * uw) + 1):
        s = i / n
        ph = -math.pi / 2 + 2 * math.pi * 2 * s
        p = WRAP_C + FN * 25 * math.sin(ph) + FD * (7 * math.cos(ph) - 16 * s + 8)
        out.append((p, math.cos(ph) > 0))
    return out

def s_unite(c, g, t):
    fill_bg(c, INK)
    fx = {}
    anc, scr, sc = unite_cam(t)
    T = lambda p: (scr[0] + (p[0] - anc[0]) * sc, scr[1] + (p[1] - anc[1]) * sc)
    c.save(); c.translate(scr[0], scr[1]); c.scale(sc, sc); c.translate(-anc[0], -anc[1])
    c.set_source_surface(surf('n_hand_gap_clean'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
    # once the knot is tied the painting takes over (n_hand_tied is the same frame with the thread tied)
    ut = prog(t, B(K_UNITE + TIED_AT), B(K_UNITE + TIED_AT) + 0.12)
    if ut > 0:
        c.set_source_surface(surf('n_hand_tied_s_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(ut)
    c.restore()
    va = 1 - ut                                  # vector thread opacity
    P0 = thread_shape(t)
    lw = 3.0 * sc
    # v2: the string (her song) comes to her finger; it stops shaking as it is tied
    song_string(c, g, [T(p) for p in P0[::-1]], t, lw, 0.6, 2.4 * sc * (1 - eo_cubic(prog(t, B(K_UNITE), B(K_UNITE + TIED_AT)))),
                va, LISH, 'start', 70 * sc, 300 * sc)
    rgba(g, LISH, 0.25 * ut); g.set_line_width(lw * 1.8); g.new_path()
    for i, p in enumerate(P0[::-1]): (g.move_to if i == 0 else g.line_to)(*T(p))
    g.stroke()
    # wraps + knot
    uw = eo_cubic(prog(t, B(K_UNITE), B(K_UNITE) + 0.45))
    if uw > 0:
        wp = wrap_path(uw)
        for front in (False, True):
            for cc, aa, lw_ in ((c, (1 if front else 0.45) * va, lw), (g, (0.6 if front else 0.2) * va, lw * 1.8)):
                rgba(cc, LISH, aa); cc.set_line_width(lw_); cc.new_path()
                prev = None
                for p, fr in wp:
                    if fr == front:
                        (cc.line_to if prev is not None else cc.move_to)(*T(p)); prev = p
                    else: prev = None
                cc.stroke()
        uk = eo_back(prog(t, B(K_UNITE) + 0.45, B(K_UNITE) + 0.6), 2)
        if uk > 0:
            kp = WRAP_C + FN * 24 - FD * 14
            for cc, aa in ((c, va), (g, 0.8 * va)):
                rgba(cc, LISH, aa); cc.arc(*T(kp), 5 * sc * uk, 0, 6.283); cc.fill()
                rgba(cc, LISH, aa); cc.set_line_width(lw * 0.8); cc.new_path()
                a_ = T(kp); b_ = T(kp + FN * 26 * uk - FD * 10 * uk); d_ = T(kp + FN * 40 * uk + FD * 6 * uk)
                cc.move_to(*a_); cc.curve_to(*b_, *b_, *d_); cc.stroke()
    c.set_line_cap(cairo.LINE_CAP_BUTT); g.set_line_cap(cairo.LINE_CAP_BUTT)
    # contact
    fl = pulse(t, B(121), 0.5)
    if fl > 0.02:
        p = T(WRAP_C - FN * 25)
        for cc in (c, g):
            rgba(cc, RED, 0.8 * fl); cc.set_line_width(2.5); cc.new_path(); cc.arc(*p, 20 + 260 * (1 - fl), 0, 6.283); cc.stroke()
    # d readout: shrinking, then exactly 0
    a_ = T(FT_); b_ = T(P0[0])
    dist = float(np.linalg.norm(P0[0] - (WRAP_C - FN * 25)))
    dv = 0.0 if t >= B(121) else max(1e-6, dist / 400)
    ud = 1 - prog(t, B(122), B(122.5))
    if ud > 0:
        my_ = min(a_[1], b_[1]) - 60
        text(c, 'monom', f'd = {dv:.6f}' if dv > 0 else 'd = 0', (a_[0] + b_[0]) / 2 + 40, my_, 30,
             CYAN if dv > 0 else RED, ud, align='center')
    # touch: null -> true
    uu = eo_cubic(prog(t, B(119.5), B(119.5) + 0.2))
    tx_, ty_ = 1240, 960
    text(c, 'mono', 'touch', tx_, ty_, 30, GREY, uu)
    if t < B(K_UNITE) + 0.15:
        text(c, 'monom', 'null', tx_ + 190, ty_, 34, RED, uu)
        if t >= B(K_UNITE):
            line(c, tx_ + 186, ty_ - 12, tx_ + 186 + 84 * eo_cubic(prog(t, B(K_UNITE), B(K_UNITE) + 0.1)), ty_ - 12, RED, 1, 3)
    else:
        s = scramble('true', t, B(K_UNITE) + 0.15, 0.03, seed=7)
        text(c, 'monom', s, tx_ + 190, ty_, 34, RED, 1)
        gg = pulse(t, B(K_UNITE) + 0.25, 0.6)
        if gg > 0.02: text(g, 'monom', 'true', tx_ + 190, ty_, 34, RED, gg)
    line(c, tx_, ty_ + 22, tx_ + 520 * uu, ty_ + 22, RED, 0.5, 1.2)
    q = [('and', 55.10), ('we', 55.48), ('can', 55.96), ('unite.', B(K_UNITE))]
    lyric(c, q, t, x=W - 130 - text_w('serif', 'and we can unite.', 84), y=860, size=84)
    fx['flash'] = 0.6 * (1 - eo_cubic(prog(t, B(119), B(119) + 0.2))) + 0.25 * pulse(t, B(121), 0.12)
    fx['ab'] = 4 * pulse(t, B(121), 0.25) + 3 * pulse(t, B(K_UNITE), 0.2)
    fx['grain'] = 0.04
    hud(c, t, True, a=0.6)
    return fx

# ================================================================ S20 SO DEEPLY  [B123, B128)
_TR = {}
def traces():
    if not _TR:
        r = random.Random(17); out = []
        for i in range(14):
            a = 2 * math.pi * i / 14 + r.uniform(-0.12, 0.12)
            d = round(a / (math.pi / 4)) % 8
            pts = [(math.cos(a) * 88, math.sin(a) * 88)]
            x, y = pts[0]
            L = 0
            for k in range(r.randint(4, 7)):
                seg = r.uniform(60, 190)
                dx, dy = math.cos(d * math.pi / 4), math.sin(d * math.pi / 4)
                x, y = x + dx * seg, y + dy * seg; pts.append((x, y)); L += seg
                d = (d + r.choice((-1, 0, 1))) % 8
            out.append(pts)
        bg = []
        for i in range(70):
            x, y = r.uniform(-1400, 1400), r.uniform(-800, 800)
            pts = [(x, y)]; d = r.randrange(8)
            for k in range(r.randint(2, 4)):
                seg = r.uniform(40, 220); x += math.cos(d * math.pi / 4) * seg; y += math.sin(d * math.pi / 4) * seg
                pts.append((x, y)); d = (d + r.choice((-2, 0, 2))) % 8
            bg.append(pts)
        _TR['red'] = out; _TR['bg'] = bg
    return _TR

def poly_partial(cc, pts, frac, T):
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    Ltot = sum(segs); Lc = Ltot * frac; acc = 0
    cc.move_to(*T(pts[0]))
    end = pts[0]
    for i, s in enumerate(segs):
        if acc + s <= Lc:
            cc.line_to(*T(pts[i + 1])); end = pts[i + 1]
        else:
            u = (Lc - acc) / s if s else 0
            end = (lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u)); cc.line_to(*T(end)); break
        acc += s
    return end

def point_on(pts, frac):
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    Lc = sum(segs) * frac; acc = 0
    for i, s in enumerate(segs):
        if acc + s >= Lc:
            u = (Lc - acc) / s if s else 0
            return (lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u))
        acc += s
    return pts[-1]

PINKY_CORE = (558, 587); PINKY_CORE_R = 50; PINKY_KNOT = (955, 535)
def s_deeply(c, g, t):
    fill_bg(c, INK)
    fx = {}
    to_pinky = B(127)                                   # vector core -> her palm core in the pinky promise
    # part 1: push into the knot (the painting dissolves into dark)
    zi = eo_expo(prog(t, B(K_SO3), B(K_SO3) + 0.45))
    if t < B(K_DEEP1):
        anc, scr, sc0 = unite_cam(B(123))
        sc = sc0 * lerp(1, 3.2, zi)
        scr2 = np.array(scr) + (np.array([960.0, 540.0]) - np.array(scr)) * zi
        c.save(); c.translate(scr2[0], scr2[1]); c.scale(sc, sc); c.translate(-anc[0], -anc[1])
        c.set_source_surface(surf('n_hand_tied_s_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD)
        c.paint_with_alpha(1 - 0.9 * prog(t, B(123.5), B(K_DEEP1)))
        c.restore()
        # the knot glows as we go in
        kp = (scr2[0] + (WRAP_C[0] - anc[0]) * sc, scr2[1] + (WRAP_C[1] - anc[1]) * sc)
        rg = cairo.RadialGradient(kp[0], kp[1], 0, kp[0], kp[1], 60 * sc)
        rg.add_color_stop_rgba(0, *LISH, 0.4 * zi); rg.add_color_stop_rgba(1, *LISH, 0)        # lavender blooms more than red did
        g.set_source(rg); g.arc(kp[0], kp[1], 60 * sc, 0, 6.283); g.fill()
    elif t < to_pinky + 0.05:
        # part 2: inside. the knot is wired into her circuitry; pull back: it is tied around her core; then dive into the core
        zb = eo_expo(prog(t, B(K_SO4), B(K_SO4) + 0.5))
        zin = ei_cubic(prog(t, B(126.6), to_pinky))
        Z = lerp(1.0, 0.5, zb) * lerp(1, 3.4, zin) + 1e-3
        cx, cy = 960, 540
        T = lambda p: (cx + p[0] * Z, cy + p[1] * Z)
        TR = traces()
        ub = prog(t, B(K_DEEP1), B(K_DEEP1) + 0.5)
        rgba(c, BONE, 0.10 * ub); c.set_line_width(1.2)
        for pts in TR['bg']:
            c.move_to(*T(pts[0]))
            for p in pts[1:]: c.line_to(*T(p))
        c.stroke()
        for pts in TR['bg']:
            rgba(c, BONE, 0.14 * ub); c.arc(*T(pts[-1]), 3, 0, 6.283); c.fill()
        gr = eo_cubic(prog(t, B(K_DEEP1), B(K_DEEP1) + 0.9))
        for idx, pts in enumerate(TR['red']):
            for cc, aa, lw in ((c, 1, 3), (g, 0.5, 5)):
                rgba(cc, LISH, aa); cc.set_line_width(lw); cc.new_path()
                end = poly_partial(cc, pts, gr, T); cc.stroke()
            rgba(c, LISH, 1); c.arc(*T(end), 5, 0, 6.283); c.fill()
            if gr >= 1:
                rgba(c, INK, 1); c.arc(*T(end), 2.5, 0, 6.283); c.fill()
            pu = prog(t, B(K_DEEP2), B(K_DEEP2) + 0.45)          # pulses run inward to the core on "deeply"
            if 0 < pu < 1:
                p = point_on(pts, 1 - eo_cubic(pu))
                for cc in (c, g):
                    rgba(cc, BONE if cc is c else LISH, 1); cc.arc(*T(p), 6, 0, 6.283); cc.fill()
        uc = eo_cubic(prog(t, B(K_SO4), B(K_SO4) + 0.4))
        hit = pulse(t, B(K_DEEP2) + 0.45, 0.6)
        rc = 64 * Z
        if uc > 0:
            rg = cairo.RadialGradient(cx, cy, rc * 0.5, cx, cy, rc * 2.6)
            rg.add_color_stop_rgba(0, *CYAN, 0.5 * min(1, uc * (0.5 + hit))); rg.add_color_stop_rgba(1, *CYAN, 0)
            g.set_source(rg); g.arc(cx, cy, rc * 2.6, 0, 6.283); g.fill()
            rgba(c, CYAN, uc); c.arc(cx, cy, rc * 0.82, 0, 6.283); c.fill()
            rgba(c, BONE, 0.8 * uc); c.arc(cx - rc * 0.25, cy - rc * 0.3, rc * 0.18, 0, 6.283); c.fill()
        for cc, aa, lw in ((c, 1, 4), (g, 0.6, 7)):
            rgba(cc, LISH, aa); cc.set_line_width(lw)
            for rr_ in (rc * 1.02, rc * 1.16):
                cc.new_path(); cc.arc(cx, cy, rr_, 0, 6.283); cc.stroke()
            rgba(cc, LISH, aa); cc.arc(cx + rc * 1.1 * 0.7, cy - rc * 1.1 * 0.7, 6 * max(Z, 0.4), 0, 6.283); cc.fill()
        if uc > 0 and zin < 0.3:
            text(c, 'monom', 'ŌMETEŌTL', cx + 160 * Z + 40, cy - 120 * Z, 24, BONE, 0.8 * uc, track=0.15)
            text(c, 'mono', 'core  ·  tuned', cx + 160 * Z + 40, cy - 120 * Z + 30, 18, BONE, 0.8 * uc, track=0.15)   # v2: her song, wired into the core
    if t >= to_pinky:
        # the landing: her core is the one in her palm, and the thread ends on a pinky promise with her (v2: Lishenna's hand)
        rc_end = 64 * 0.5 * 3.4
        uz = eo_expo(prog(t, to_pinky, to_pinky + P * 0.6))
        sc = lerp(rc_end / PINKY_CORE_R, 1.0, uz) * (1 + 0.025 * prog(t, to_pinky + P * 0.6, END2))
        ax, ay = lerp(960, PINKY_CORE[0], uz), lerp(540, PINKY_CORE[1], uz)
        c.save(); c.translate(ax, ay); c.scale(sc, sc); c.translate(-PINKY_CORE[0], -PINKY_CORE[1])
        c.set_source_surface(surf('n_pinky2_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD)
        c.paint_with_alpha(prog(t, to_pinky - 0.01, to_pinky + 0.05))
        c.restore()
        kx, ky = ax + (PINKY_KNOT[0] - PINKY_CORE[0]) * sc, ay + (PINKY_KNOT[1] - PINKY_CORE[1]) * sc
        kg = pulse(t, to_pinky + P * 0.6, 0.7)
        rg = cairo.RadialGradient(kx, ky, 0, kx, ky, 110)
        rg.add_color_stop_rgba(0, *LISH, 0.25 + 0.6 * kg); rg.add_color_stop_rgba(1, *LISH, 0)
        g.set_source(rg); g.arc(kx, ky, 110, 0, 6.283); g.fill()
    pinky = t >= to_pinky
    lyric(c, [('so', B(K_SO3)), ('deeply,', B(K_DEEP1))] if t < B(124.8) else [('so', B(K_SO4)), ('deeply', B(K_DEEP2))], t,
          x=150, y=248, size=84, col=SEPIA if pinky else BONE, a=0.95)
    fx['ab'] = 4 * pulse(t, B(K_DEEP1), 0.25) + 3 * pulse(t, B(K_SO4), 0.2) + 4 * pulse(t, B(K_DEEP2) + 0.45, 0.2) + 4 * pulse(t, to_pinky, 0.2)
    fx['flash'] = 0.2 * pulse(t, B(K_DEEP1), 0.12) + 0.45 * pulse(t, to_pinky, 0.12) + 0.85 * ei_cubic(prog(t, END2 - 0.22, END2))
    fx['glow'] = 0.9
    if pinky: fx['vig'] = 0.4; fx['grain'] = 0.03
    hud(c, t, not pinky, a=0.6)
    return fx
