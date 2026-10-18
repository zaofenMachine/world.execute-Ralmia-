from scenes import *

# ================================================================ S5 DATA  [B16, B21)
def s_data(c, g, t):
    fill_bg(c, INK)
    fx = {}
    words(c, 'serif', [('Fill', B(16)), ('in', 7.94), ('my', 8.36)], t, 130, 250, 76, BONE, 0.9)
    f = fonts()['heavy']; size = 480; base = 800; x0 = 112
    gl = f.glyphs('DATA', x0, base, size)
    top = base - size * f.cap
    # glitch slices on downbeat 20
    gli = pulse(t, B(20), 0.12)
    def data_path(cc, dx=0):
        cc.new_path()
        for d in gl: f.glyph_path(cc, d['g'], d['x'] + dx, d['y'], size)
    # inner data texture (binary columns) clipped to letters
    us = eo_cubic(prog(t, B(16), B(16) + 0.3))
    lvl_steps = 8
    lv = math.floor(prog(t, B(17), B(18)) * lvl_steps) / lvl_steps
    lv = eo_cubic(lv) if t < B(18) else 1.0
    fill_y = base - (base - top + 10) * lv
    c.save(); data_path(c); c.clip()
    rnd = random.Random(int(t * 20))
    rgba(c, CYAN, 0.55 * us)
    for col in range(x0, x0 + 1300, 22):
        off = (t * (200 + (col * 37) % 300)) % 26
        for yy in range(int(top) - 30, base + 30, 26):
            yv = yy + off
            if yv < fill_y:
                ch = '1' if rnd.random() > 0.5 else '0'
                fonts()['mono'].text_path(c, ch, col, yv, 20)
    c.fill()
    rgba(c, BONE, 1); c.rectangle(0, fill_y, W, H); c.fill()
    # level line
    if 0 < lv < 1:
        line(c, 0, fill_y, W, fill_y, CYAN, 1, 2)
    c.restore()
    if 0 < lv < 1:
        g.save(); data_path(g); g.clip(); line(g, 0, fill_y, W, fill_y, CYAN, 1, 6); g.restore()
    # outline drawn on
    data_path(c); rgba(c, BONE, 0.95); c.set_line_width(2.4); partial_stroke(c, us)
    # flash on "data"
    fl = pulse(t, B(18), 0.3)
    if fl > 0.01:
        data_path(g); rgba(g, CYAN, 0.7 * fl); g.fill()
    if gli > 0.05:
        # redraw horizontal slices displaced
        rr = random.Random(int(t * 60))
        for i in range(6):
            y0 = top + rr.random() * (base - top); hgt = 10 + rr.random() * 40
            dx = (rr.random() - 0.5) * 120 * gli
            c.save(); c.rectangle(0, y0, 1250, hgt); c.clip()
            rgba(c, INK, 1); c.paint()
            data_path(c, dx); rgba(c, BONE, 1); c.fill()
            c.restore()
    text(c, 'mono', f'fill  {int(lv * 100):3d}%', x0 + 6, base + 60, 20, CYAN, 0.8 * us)
    # parameter table
    tx = 1110
    upar = prog(t, B(18.7), B(18.7) + 0.01)
    uf = eo_cubic(prog(t, B(16) + 0.1, B(16) + 0.4))
    text(c, 'bold', 'PARAMETERS', tx, 330, 104, BONE, 0.12 * uf, track=0.03)
    if upar > 0:
        s = scramble('PARAMETERS', t, B(18.7), 0.025)
        text(c, 'bold', s, tx, 330, 104, BONE, 1, track=0.03)
    rows = [('name', 'RALMIA', BONE), ('class', 'MACHINA / ARTIFACT', BONE), ('os', 'ŌMETEŌTL', CYAN),
            ('speed', '> 340.29 m/s', BONE), ('touch', 'null', RED)]
    uf = eo_cubic(prog(t, B(16) + 0.1, B(16) + 0.4))
    for i, (k, v, col) in enumerate(rows):
        y = 430 + i * 74
        if uf > 0 and t < B(19) + i * 0.173:
            text(c, 'mono', k, tx, y, 30, GREY, 0.6 * uf)
            rgba(c, BONE, 0.25 * uf); c.set_dash([4, 6]); c.set_line_width(1.2)
            c.move_to(tx + 190, y + 6); c.line_to(tx + 190 + 500 * uf, y + 6); c.stroke(); c.set_dash([])
            if int(t * 4) % 2 == 0 and i == 0: rgba(c, CYAN, 0.8); c.rectangle(tx + 190, y - 26, 14, 30); c.fill()
    for i, (k, v, col) in enumerate(rows):
        tr = B(19) + i * 0.173
        u = eo_cubic(prog(t, tr, tr + 0.12))
        if u <= 0: continue
        y = 430 + i * 74
        text(c, 'mono', k, tx, y, 30, GREY, u)
        vv = scramble(v, t, tr, 0.012, seed=i)
        text(c, 'monom', vv, tx + 190, y, 34, col, u)
        ub = eo_cubic(prog(t, tr, tr + 0.25))
        line(c, tx, y + 22, tx + 690 * ub, y + 22, col if col != BONE else GREY, 0.6, 1.2)
        if col is RED:
            gg = pulse(t, tr + 0.1, 0.6)
            if gg > 0.02: text(g, 'monom', v, tx + 190, y, 34, RED, gg)
    fx['ab'] = 5 * gli + 4 * pulse(t, B(18), 0.2)
    hud(c, t, True)
    return fx

# ================================================================ S6 INITIALIZATION  [B21, B24)
EYEC = (965, 538)                       # between the eyes in n_eye_open / n_eye_closed (pixel-aligned pair)
IRISES = [(546, 540), (1383, 537)]; IRIS_R = 118
def eye_cam(t):
    sc = lerp(1.12, 1.17, prog(t, B(21), B(24))) - 0.06 * eio_cubic(prog(t, B(23), B(24)))
    return sc, 960, 540
def s_init(c, g, t):
    fill_bg(c, INK)
    fx = {}
    sc, tx_, ty_ = eye_cam(t)
    def img(name, a):
        c.save(); c.translate(tx_, ty_); c.scale(sc, sc); c.translate(-EYEC[0], -EYEC[1])
        c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a)
        c.restore()
    xo = prog(t, B(23), B(23) + 0.12)
    img('n_eye_closed_hd', 1)
    if xo > 0: img('n_eye_open_hd', xo)
    # irises focus: a ring of aperture ticks closes in on each iris after the eyes open
    uf = eo_expo(prog(t, B(23) + 0.05, B(23) + 0.45))
    fa = 1 - prog(t, B(23) + 0.6, B(24) - 0.05)
    if uf > 0 and fa > 0:
        for ix0, iy0 in IRISES:
            ix, iy = tx_ + (ix0 - EYEC[0]) * sc, ty_ + (iy0 - EYEC[1]) * sc
            r = IRIS_R * sc * (1.02 + 1.3 * (1 - uf))
            for cc, aa, lw in ((c, 0.85 * fa, 2), (g, 0.6 * fa, 3)):
                rgba(cc, CYAN, aa); cc.set_line_width(lw); cc.new_path(); cc.arc(ix, iy, r, 0, 6.283); cc.stroke()
                for k in range(8):
                    a_ = k * math.pi / 4 + (1 - uf) * 1.2
                    cc.move_to(ix + math.cos(a_) * r, iy + math.sin(a_) * r)
                    cc.line_to(ix + math.cos(a_) * (r + 18), iy + math.sin(a_) * (r + 18))
                cc.stroke()
    # letterbox slit
    h1 = 170 * eo_expo(prog(t, B(21), B(21) + 0.25))
    h = h1 + (540 - h1) * eio_cubic(prog(t, B(23) + 0.05, B(24) - 0.02))
    rgba(c, INK, 1); c.rectangle(0, 0, W, 540 - h); c.rectangle(0, 540 + h, W, 540 - h + 2); c.fill()
    line(c, 0, 540 - h, W, 540 - h, BONE, 0.25, 1); line(c, 0, 540 + h, W, 540 + h, BONE, 0.25, 1)
    # INITIALIZATION on the upper bar
    yb = 540 - h - 70
    if t >= B(22) - 0.25:
        s = scramble('INITIALIZATION', t, B(22), 0.031, seed=3)
        text(c, 'bold', s, 960, yb, 128, BONE, 1, align='center', track=0.22)
        done = pulse(t, B(22) + 13 * 0.031, 0.5)
        if done > 0.02: text(g, 'bold', 'INITIALIZATION', 960, yb, 128, CYAN, 0.6 * done, align='center', track=0.22)
    # progress on lower bar
    yp = 540 + h + 70
    pr = math.floor(prog(t, B(21), B(23)) * 8) / 8
    xL, xR = 360, 1560
    line(c, xL, yp, xR, yp, BONE, 0.25, 2)
    line(c, xL, yp, lerp(xL, xR, pr), yp, CYAN, 1, 3)
    for i in range(9):
        line(c, lerp(xL, xR, i / 8), yp - 8, lerp(xL, xR, i / 8), yp + 8, BONE, 0.3, 1)
    text(c, 'mono', f'{int(pr * 100):03d}%', xR + 24, yp + 8, 22, CYAN, 0.9)
    text(c, 'mono', 'obj.init()', xL - 24, yp + 8, 22, BONE, 0.5, align='right')
    fx['flash'] = 0.12 * pulse(t, B(23), 0.1)
    fx['ab'] = 3 * pulse(t, B(23), 0.2)
    fx['grain'] = 0.03
    hud(c, t, True)
    return fx

# ================================================================ S7 WORLD  [B24, B28)
VP = (1246, 682)                        # sun on the horizon (n_world layers)
LAYERS = [  # name, land beat, entry ('top' | 'bottom' | 'left'), parallax depth, label
    ('n_wL1_hd', 24.5, 'top', 0.12, 'L1  sky'),
    ('n_wL2_hd', 25.0, 'bottom', 0.35, 'L2  city / sun / water'),
    ('n_wL3_hd', 25.5, 'left', 0.75, 'L3  frame'),
    ('n_wL4_hd', 26.0, 'bottom', 1.0, 'L4  ledge / her'),
]
def world_layers(c, t, alpha=1.0):
    """The four layers as they stand at time t (entry motion + parallax pan). Returns nothing."""
    pan = 34 * max(0.0, t - B(24.5))
    zoom = 1.035 + 0.02 * prog(t, B(26), B(28))
    for name, kb, entry, depth, _ in LAYERS:
        u = prog(t, B(kb) - 0.06, B(kb) + 0.3)
        if u <= 0: continue
        e = eo_back(u, 1.3)
        ox, oy = -pan * depth, 0.0
        if entry == 'top': oy = -(1 - e) * (H + 60)
        elif entry == 'bottom': oy = (1 - e) * (H + 60)
        else: ox += -(1 - e) * 900
        c.save(); c.translate(960 + ox, 540 + oy); c.scale(zoom, zoom); c.translate(-960, -540)
        c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(alpha)
        c.restore()

def s_world(c, g, t):
    paper_bg(c)
    fx = {}
    vx, vy = VP
    ug = eo_cubic(prog(t, B(24), B(24) + 0.3))
    # perspective guides (the set is built on them)
    c.set_line_width(1.1)
    for i in range(18):
        ang = math.pi + math.pi * (i / 17.0)
        dx, dy = math.cos(ang), math.sin(ang)
        L = 2600 * ug
        rgba(c, SEPIA, 0.25); c.move_to(vx, vy); c.line_to(vx + dx * L, vy + dy * L * 0.6); c.stroke()
        rgba(c, SEPIA, 0.25); c.move_to(vx, vy); c.line_to(vx - dx * L * 0.3, vy - dy * L * 0.6); c.stroke()
    line(c, vx - 2600 * ug, vy, vx + 900 * ug, vy, SEPIA, 0.5, 1.4)
    world_layers(c, t)
    # layer tags as each flat lands
    for name, kb, entry, depth, lab in LAYERS:
        ua = pulse(t, B(kb) + 0.2, 0.9)
        if t >= B(kb) and ua > 0.03:
            text(c, 'mono', lab, 120, 1000 - LAYERS.index((name, kb, entry, depth, lab)) * 0, 18, SEPIA, 0.8 * ua, track=0.15)
    # sun flare when the last layer lands
    sun = pulse(t, B(26), 0.8)
    if sun > 0.01:
        sx_, sy_ = 1246, 574
        rg = cairo.RadialGradient(sx_, sy_, 0, sx_, sy_, 380)
        rg.add_color_stop_rgba(0, 1, 0.9, 0.65, 0.85 * sun); rg.add_color_stop_rgba(1, 1, 0.9, 0.65, 0)
        g.set_source(rg); g.arc(sx_, sy_, 380, 0, 2 * math.pi); g.fill()
    words(c, 'serif', [('Set', B(24)), ('up', 11.60), ('our', 12.06), ('new', B(26))], t, 760, 200, 80, SEPIA, 0.95)
    f = fonts()['heavy']; size = 360
    gl = f.glyphs('WORLD', 800, 990, size, track=0.02)
    for d in gl:
        ti = B(26.5) + d['i'] * P / 8
        u = prog(t, ti, ti + 0.14)
        if u <= 0: continue
        dy = -60 * (1 - eo_back(u, 2))
        c.new_path(); f.glyph_path(c, d['g'], d['x'], d['y'] + dy, size)
        c.set_operator(cairo.OPERATOR_MULTIPLY); rgba(c, INK, 0.92 * min(1, u * 3)); c.fill()
        c.set_operator(cairo.OPERATOR_OVER)
    fx['grain'] = 0.03; fx['vig'] = 0.4
    fx['ab'] = 2 * sum(pulse(t, B(kb), 0.15) for _, kb, *_ in LAYERS)
    hud(c, t, False)
    return fx

# ================================================================ S8 SIMULATION  [B28, B32)
def window(c, x, y, w, h, name, a=1.0, label='world.sim', tint=None):
    c.save(); c.rectangle(x, y, w, h); c.clip()
    s = w / W
    c.translate(x, y); c.scale(s, s)
    c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a)
    c.restore()
    if tint:
        rgba(c, tint[0], tint[1] * a); c.rectangle(x, y, w, h); c.fill()
    bar = max(6, h * 0.05)
    rgba(c, INK, 0.85 * a); c.rectangle(x, y, w, bar); c.fill()
    if bar > 14:
        text(c, 'mono', label, x + 10, y + bar * 0.72, bar * 0.55, BONE, 0.8 * a)
    rgba(c, BONE, 0.7 * a); c.set_line_width(1.3); c.rectangle(x, y, w, h); c.stroke()

STAGES = ['wireframe', 'lineart', 'flat', 'final']
def stage_cell(c, x, y, w, h, stage, a=1.0, label='', reveal=1.0):
    """One simulation instance, drawn at a given render stage (0 wire, 1 line, 2 flat, 3 final).
    reveal: 0..1 bucket-render wipe from left to right (cyan scan edge)."""
    if reveal <= 0: return
    s = w / W
    c.save(); c.rectangle(x, y, w * reveal, h); c.clip()
    if stage == 0:
        rgba(c, INK2, a); c.rectangle(x, y, w, h); c.fill()
        vx, vy = x + 1246 * s, y + 682 * s
        rgba(c, BONE, 0.45 * a); c.set_line_width(1)
        for i in range(14):
            ang = math.pi + math.pi * i / 13
            c.move_to(vx, vy); c.line_to(vx + math.cos(ang) * w * 1.6, vy + math.sin(ang) * w * 0.9)
        c.stroke()
        line(c, x, vy, x + w, vy, BONE, 0.7 * a, 1.2)
        for j in range(1, 6):       # receding grid on the ground plane
            yy = vy + (h - (vy - y)) * (j / 6) ** 1.8
            line(c, x, yy, x + w, yy, BONE, 0.25 * a, 1)
    elif stage == 1:
        rgba(c, PAPER, a); c.rectangle(x, y, w, h); c.fill()
        c.save(); c.translate(x, y); c.scale(s, s)
        c.set_operator(cairo.OPERATOR_MULTIPLY)
        c.set_source_surface(surf('n_world_line'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a)
        c.set_operator(cairo.OPERATOR_OVER); c.restore()
    else:
        c.save(); c.translate(x, y); c.scale(s, s)
        c.set_source_surface(surf('n_world_flat' if stage == 2 else 'n_world_hd'), 0, 0)
        c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a); c.restore()
    c.restore()
    if reveal < 1:
        for cc in (c,):
            line(cc, x + w * reveal, y, x + w * reveal, y + h, CYAN, 0.9 * a, 2)
    bar = clamp(h * 0.075, 6, 30)
    rgba(c, INK, 0.85 * a); c.rectangle(x, y, w, bar); c.fill()
    if bar > 11 and label:
        text(c, 'mono', label, x + 8, y + bar * 0.74, bar * 0.6, CYAN if stage == 3 else BONE, 0.85 * a)
    rgba(c, BONE, 0.6 * a); c.set_line_width(1.2); c.rectangle(x, y, w, h); c.stroke()

def s_sim(c, g, t):
    """'and let's begin the simulation': one world -> 2x2 render passes -> 4x4 instances iterating to final."""
    fill_bg(c, INK)
    fx = {}
    off = prog(t, B(31), B(31) + 0.2); off2 = prog(t, B(31) + 0.2, B(31) + 0.5)
    c.push_group()
    fill_bg(c, INK)
    dotgrid(c, BONE, 0.08)
    CY = 645
    u1 = eio_cubic(prog(t, B(28), B(28) + 0.3))
    if t < B(29):
        sc = lerp(1.0, 0.56, u1)
        w, h = W * sc, H * sc
        stage_cell(c, 960 - w / 2, CY - h / 2, w, h, 3, 1, 'world.sim  —  instance 0  ·  final')
    elif t < B(30):
        # 2x2: the same world shown at the four render passes, each bucket-rendered on a 16th
        u = eo_expo(prog(t, B(29), B(29) + 0.22))
        gap = 22; tw = lerp(W * 0.56, (1180 - gap) / 2, u); th = tw * 9 / 16
        for k in range(4):
            i, j = divmod(k, 2)
            x = lerp(960 - tw / 2, 960 - tw - gap / 2 + j * (tw + gap), u)
            y = lerp(CY - th / 2, CY - th - gap / 2 + i * (th + gap), u)
            rv = eo_cubic(prog(t, B(29) + k * P / 4, B(29) + k * P / 4 + P / 4))
            if k == 3: rv = 1.0          # the final pass is the window we came from
            stage_cell(c, x, y, tw, th, k if k < 3 else 3, 1, f'pass {k + 1}  ·  {STAGES[k]}', rv if k < 3 else 1)
    else:
        # 4x4: sixteen instances, each re-rendering one pass per 16th note until all are final
        n = 4; gap = 12
        u = eo_expo(prog(t, B(30), B(30) + 0.22))
        tw = (1180 - gap * (n - 1)) / n; th = tw * 9 / 16
        tot_w = n * tw + (n - 1) * gap; tot_h = n * th + (n - 1) * gap
        x0 = 960 - tot_w / 2; y0 = CY - tot_h / 2
        rr = random.Random(5)
        steps = int((t - B(30)) / (P / 4))
        for k in range(16):
            i, j = divmod(k, n)
            s0 = rr.randrange(0, 3); lag = rr.randrange(0, 3)
            st = min(3, s0 + max(0, steps - lag))
            x = lerp(960 - tw / 2, x0 + j * (tw + gap), u); y = lerp(CY - th / 2, y0 + i * (th + gap), u)
            t_st = B(30) + (lag + st - s0) * P / 4 if st > s0 else B(30)
            rv = eo_cubic(prog(t, t_st, t_st + P / 4)) if st > s0 else 1.0
            if st > s0 and rv < 1:      # previous pass stays underneath the wipe
                stage_cell(c, x, y, tw, th, st - 1, 1, '')
            stage_cell(c, x, y, tw, th, st, 1, f'#{k:02d}  iter {st + 1}', rv)
    words(c, 'serif', [('and', B(28)), ("let's", 13.30), ('begin', 13.44), ('the', 13.84)], t, 150, 248, 70, BONE, 0.95)
    if t >= B(30):
        f = fonts()['heavy']; size = 300
        for d in f.glyphs('SIMULATION', 960, CY + 110, size, align='center', track=0.02):
            ti = B(30) + d['i'] * 0.045
            u = eo_cubic(prog(t, ti, ti + 0.08))
            if u <= 0: continue
            c.new_path(); f.glyph_path(c, d['g'], d['x'], d['y'], size)
            rgba(c, INK, 0.9 * u); c.set_line_width(14); c.stroke_preserve()
            rgba(c, BONE, u); c.fill()
    hud(c, t, True)
    pat = c.pop_group()
    # CRT power-off
    sy = lerp(1, 0.004, ei_cubic(off)); sx = lerp(1, 0.0, ei_cubic(off2))
    if t < B(31) + 0.55:
        m = cairo.Matrix(); m.translate(960, 540); m.scale(1 / max(sx, 1e-4), 1 / max(sy, 1e-4)); m.translate(-960, -540)
        pat.set_matrix(m)
        c.set_source(pat); c.paint_with_alpha(1 - prog(t, B(31) + 0.45, B(31) + 0.55))
        if off > 0:
            gl_ = 1 - off2
            rgba(g, BONE, gl_); g.rectangle(960 - 960 * sx, 536, 1920 * sx, 8); g.fill()
    fx['ab'] = 3 * pulse(t, B(30), 0.3)
    return fx


# ---------------------------------------------------------------- her dash, flashed in for a few frames on a downbeat
DASH_FRAMES = 5
def dash_flash(c, g, t, t0, name):
    """Frames 0-1: the painting with a speed smear; 2-3: a bone silhouette with a cyan rim; 4: rim only.
    Returns the post-FX dict to merge, or None outside the window."""
    k = int(math.floor((t - t0) * FPS + 1e-6))
    if k < 0 or k >= DASH_FRAMES: return None
    fill_bg(c, INK)
    s_ = surf(name)
    if k <= 1:
        for off, a in ((-160, 0.18), (-90, 0.35), (-40, 0.6), (0, 1.0)):
            c.set_source_surface(s_, off - 30 * k, 0); c.paint_with_alpha(a)
    else:
        if k <= 3:
            rgba(c, BONE, 1 if k == 2 else 0.6); c.mask_surface(s_, 40 * (k - 1), 0)
        for cc, aa in ((g, 1.0),):
            rgba(cc, CYAN, aa); cc.mask_surface(s_, 40 * (k - 1), 0)
    return {'ab': 10 - 2 * k, 'flash': 0.0, 'glow': 1.0}

# ================================================================ I1 VELOCITY  [B32, B36)
_STARS = np.random.default_rng(11).random((420, 3))
def warp(c, g, t, speed, cx=960, cy=540, col=BONE, a=1.0, stretch=1.0, horiz=0.0):
    for i, (ang, r0, sz) in enumerate(_STARS):
        th = ang * 2 * math.pi
        d = ((r0 + t * speed * (0.6 + sz)) % 1.0)
        r = 40 + (d ** 2.2) * 1400
        L = (10 + 260 * d * speed) * stretch
        dx, dy = math.cos(th), math.sin(th) * (1 - horiz) + 0.0
        x0, y0 = cx + dx * r, cy + dy * r * 0.62
        x1, y1 = cx + dx * (r + L), cy + dy * (r + L) * 0.62
        aa = a * min(1, d * 3) * (0.35 + 0.65 * sz)
        cc_col = CYAN if i % 9 == 0 else col
        rgba(c, cc_col, aa); c.set_line_width(1 + 2 * sz * d); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()

def odometer(c, value, x, y, size, col, t, key='heavy', fmt='{:06.2f}', align='center'):
    s = fmt.format(value)
    f = fonts()[key]
    w = f.width(s, size)
    x0 = x - w / 2 if align == 'center' else x
    dw = f.width('0', size)
    cx = x0
    for ch in s:
        cw = f.width(ch, size)
        text(c, key, ch, cx, y, size, col)
        cx += cw
    return w

def s_velocity(c, g, t):
    fill_bg(c, INK)
    fx = {}
    k = (t - T0) / P
    sp = 0.25 + 0.35 * prog(t, B(32), B(36)) + 0.25 * pulse(t, B(math.floor(k)), 0.3)
    warp(c, g, t, sp)
    # stepped velocity readout, rolling digits
    steps = [(32, 0.0), (33, 85.07), (34, 170.15), (35, 255.22), (35.5, 340.29)]
    v = 0
    for kb, val in steps:
        if t >= B(kb):
            prev = v
            u = eo_cubic(prog(t, B(kb), B(kb) + 0.12))
            v = lerp(prev, val, u)
    f = fonts()['heavy']; size = 330
    s = f'{v:06.2f}'
    w = f.width(s, size); x0 = 960 - w / 2
    cx_ = x0
    for i, ch in enumerate(s):
        cw = f.width(ch, size)
        text(c, 'heavy', ch, cx_, 700, size, BONE)
        cx_ += cw
    p_ = pulse(t, B(35.5), 0.5)
    if p_ > 0.02: text(g, 'heavy', s, 960, 700, size, CYAN, 0.7 * p_, align='center')
    text(c, 'mono', 'VELOCITY   m/s', 960, 400, 26, CYAN, 0.9, align='center', track=0.4)
    u = eo_cubic(prog(t, B(35.5), B(35.5) + 0.2))
    if u > 0:
        text(c, 'thin', 'SPEED OF SOUND', 960, 830, 72, BONE, u, align='center', track=0.25)
    fl = 1.0 - prog(t, B(32), B(32) + 0.14)
    fx['flash'] = 0.9 * fl ** 2
    fx['ab'] = 4 * pulse(t, B(33), 0.2) + 4 * pulse(t, B(35), 0.2)
    df = dash_flash(c, g, t, B(32), 'n_dash_launch_hd')      # 15.1 s: she launches
    if df: fx.update(df)
    elif t < B(32) + 0.3: fx['flash'] = 0.6 * (1 - prog(t, B(32) + DASH_FRAMES / FPS, B(32) + 0.3)) ** 2
    hud(c, t, True)
    return fx

# ================================================================ I2 DOPPLER  [B36, B40) and I3/I4 MACH [B40, B48)
CS = 620.0   # px/s "speed of sound"
def mach_of(t):
    if t < B(36): return 0.25
    if t < B(40):
        u = prog(t, B(36), B(40)); return 0.25 + 0.75 * u ** 1.6
    seq = [(40, 1.25), (41, 2.0), (42, 3.0), (43, 5.0), (44, 8.0), (45, 14.0), (46, 30.0), (47, 80.0)]
    m = 1.0
    for kb, val in seq:
        if t >= B(kb): m = lerp(m, val, eo_cubic(prog(t, B(kb), B(kb) + 0.12)))
    return m

_XS = {}
def xs_at(t, dt=1 / 240):
    """integrated source position (world px), cached on a fine grid."""
    if not _XS:
        ts = np.arange(B(36) - 0.01, B(48) + 0.01, dt)
        v = np.array([mach_of(x) * CS for x in ts])
        _XS['t'] = ts; _XS['x'] = np.concatenate([[0], np.cumsum(v[:-1] * dt)])
    return float(np.interp(t, _XS['t'], _XS['x']))

# v2: Lishenna's song -- a fixed source off-screen left (the stage), one wavefront per beat at the speed of sound.
# below Mach 1 the fronts run through her (she is inside the song); past it they fall behind and never catch up again.
XW_SONG = -2600.0                       # world px; screen x -1010 in the Doppler shot: never on screen
def song_fronts(c, g, t, x_screen, sy, scale, a=1.0):
    for kb in range(18, 48):
        te = B(kb)
        if te > t: break
        r = CS * (t - te) * scale
        if r > 3800 or x_screen + r < -20: continue
        down = kb % 4 == 0
        aa = a * (0.85 if down else 0.55) * max(0.0, 1 - r / 3800) ** 0.5 * min(1.0, r / 60)
        for cc, k_, lw in ((c, 1.0, 3.0 if down else 2.0), (g, 0.5, 5)):
            rgba(cc, LISH, aa * k_); cc.set_line_width(lw); cc.new_path(); cc.arc(x_screen, sy, max(r, 0.1), 0, 2 * math.pi); cc.stroke()

def s_doppler(c, g, t):
    fill_bg(c, INK)
    fx = {}
    dotgrid(c, BONE, 0.06)
    # camera: source moves across screen in bar 2
    sx_world = xs_at(t)
    screen_x0 = 420
    cam = lambda xw: screen_x0 + xw * 0.55
    sy = 560
    te0 = B(36)
    n = int((t - te0) / (P / 4)) + 1
    for i in range(n):
        te = te0 + i * P / 4
        r = CS * (t - te) * 0.55
        if r > 2400: continue
        x = cam(xs_at(te))
        beat = (i % 4 == 0)
        aa = (0.85 if beat else 0.45) * max(0, 1 - r / 1900)
        rgba(c, CYAN if beat else BONE, aa); c.set_line_width(3.2 if beat else 1.6)
        c.new_path(); c.arc(x, sy, max(r, 0.1), 0, 2 * math.pi); c.stroke()
    song_fronts(c, g, t, cam(XW_SONG), sy, 0.55)
    x = cam(sx_world)
    for cc in (c, g):
        rgba(cc, CYAN, 1); cc.arc(x, sy, 15, 0, 2 * math.pi); cc.fill()
    line(c, screen_x0, sy, x, sy, CYAN, 0.35, 1.5)
    M = mach_of(t)
    text(c, 'heavy', f'M {M:4.2f}', 120, 990, 170, BONE, 0.95)
    text(c, 'mono', 'M = v / c', 130, 790, 26, CYAN, 0.85, track=0.2)
    kk = math.floor((t - T0) / P)
    pp = pulse(t, B(kk), 0.3)
    if pp > 0.02:
        for cc in (c, g):
            rgba(cc, CYAN, 0.8 * pp); cc.set_line_width(4); cc.new_path(); cc.arc(x, sy, 30 + 120 * (1 - pp), 0, 2 * math.pi); cc.stroke()
    um = eo_cubic(prog(t, B(38), B(38) + 0.3))
    if um > 0:
        line(c, x + 14, sy - 300, x + 14, sy + 300, RED, 0.6 * um * (0.5 + 0.5 * math.sin(t * 40)), 2)
        text(c, 'mono', 'SOUND BARRIER', x + 30, sy - 280, 20, RED, 0.85 * um, track=0.3)
    text(c, 'thin', 'SPEED OF SOUND', 960, 180, 60, BONE, 0.35, align='center', track=0.25)
    fx['ab'] = 3 * pulse(t, B(37), 0.2) + 3 * pulse(t, B(39), 0.2)
    hud(c, t, True)
    return fx

def s_mach(c, g, t):
    fill_bg(c, INK)
    fx = {}
    k = (t - T0) / P
    light = prog(t, B(44), B(48))
    dotgrid(c, BONE, 0.06 * (1 - light), ox=-xs_at(t) * 0.2)
    sxw = xs_at(t)
    srcx, sy = 1380, 560
    scale = 0.55
    te0 = B(36)
    n = int((t - te0) / (1 / 40)) + 1
    for i in range(max(0, n - 260), n):
        te = te0 + i / 40
        r = CS * (t - te) * scale
        if r > 2600: continue
        x = srcx + (xs_at(te) - sxw) * scale
        if x + r < -50: continue
        beat = abs(((te - T0) / P) - round((te - T0) / P)) < 0.013
        aa = (0.5 if beat else 0.16) * max(0, 1 - r / 2000) * (1 - light * 0.7)
        rgba(c, BONE, aa); c.set_line_width(2 if beat else 1)
        c.new_path(); c.arc(x, sy, max(r, 0.1), 0, 2 * math.pi); c.stroke()
    song_fronts(c, g, t, srcx + (XW_SONG - sxw) * scale, sy, scale, 1 - light)     # left behind
    M = max(mach_of(t), 1.0001)
    mu = math.asin(1 / M)
    L = 2600
    for cc in (c, g):
        rgba(cc, CYAN, 0.9); cc.set_line_width(3)
        cc.move_to(srcx - L * math.cos(mu), sy - L * math.sin(mu)); cc.line_to(srcx, sy)
        cc.line_to(srcx - L * math.cos(mu), sy + L * math.sin(mu)); cc.stroke()
        rgba(cc, BONE, 1); cc.arc(srcx, sy, 12, 0, 2 * math.pi); cc.fill()
    # light-speed streaks
    if light > 0:
        rnd = np.random.default_rng(4)
        ys = rnd.random(160) * H; sp = rnd.random(160)
        for y, s_ in zip(ys, sp):
            xx = (W + 400) - ((t * (2200 + 5000 * s_) * light + s_ * 3000) % (W + 800))
            Ls = 200 + 1400 * light * s_
            rgba(c, CYAN if s_ > 0.8 else BONE, 0.25 + 0.5 * light); c.set_line_width(1 + 2 * s_)
            c.move_to(xx, y); c.line_to(xx + Ls, y); c.stroke()
    # boom ring
    if t < B(41):
        r = eo_expo(prog(t, B(40), B(40) + 0.7))
        for cc in (c, g):
            rgba(cc, BONE, 0.9 * (1 - r)); cc.set_line_width(8 * (1 - r) + 1)
            cc.new_path(); cc.arc(srcx, sy, 40 + 1600 * r, 0, 2 * math.pi); cc.stroke()
    # words
    f = fonts()['heavy']
    def slam(word, kb, x, y, size, col=BONE, until=None, align='left'):
        if t < B(kb) or (until and t >= B(until)): return
        u = eo_expo(prog(t, B(kb), B(kb) + 0.14))
        c.save(); c.translate(x, y); s_ = 1.25 - 0.25 * u; c.scale(s_, s_)
        text(c, 'heavy', word, 0, 0, size, col, min(1, u * 2), align=align)
        c.restore()
    slam('SWIFTER', 40.0, 120, 330, 230, until=44)
    slam('THAN', 41.0, 120, 560, 230, until=44)
    slam('SOUND', 42.0, 120, 790, 230, until=44)
    slam('RIVALS', 44.0, 960, 410, 250, align='center')
    slam('LIGHT', 46.0, 960, 820, 340, col=BONE, align='center')
    # readouts
    text(c, 'mono', f'MACH {M:5.2f}', 120, 960, 34, CYAN, 0.9, track=0.15)
    if t >= B(45):
        cval = 299792458 * eo_cubic(prog(t, B(45), B(47)))
        text(c, 'monom', f'c = {int(cval):,} m/s'.replace(',', ' '), W - 120, 960, 34, BONE, 0.9, align='right')
    fx['ab'] = 12 * pulse(t, B(40), 0.3) + 4 * pulse(t, B(math.floor(k)), 0.15) * (math.floor(k) % 2)
    fx['flash'] = 0.85 * pulse(t, B(40), 0.18) + 0.6 * pulse(t, B(44), 0.15) + ei_cubic(prog(t, B(47), B(48))) ** 1.5
    df = dash_flash(c, g, t, B(40), 'n_dash_full_hd')          # 18.8 s: the sound barrier breaks, she is through it
    if df: fx.update(df)
    elif B(40) <= t < B(40) + 0.4: fx['flash'] = 0.7 * pulse(t, B(40) + DASH_FRAMES / FPS, 0.18)
    hud(c, t, True, a=1 - light * 0.6, log_a=1 - prog(t, B(40) - 0.08, B(40)) + prog(t, B(44), B(44) + 0.25))
    return fx

# ================================================================ I5 GAP  [B48, B52)
FT = (1314, 190); TH = (1366, 168)     # fingertip, thread end (n_hand_gap)
def s_gap(c, g, t):
    fill_bg(c, INK)
    fx = {}
    u = eio_cubic(prog(t, B(48), B(52)))
    sc = lerp(1.0, 1.55, u)
    mx, my = (FT[0] + TH[0]) / 2, (FT[1] + TH[1]) / 2
    px, py = lerp(mx, 1150, u), lerp(my, 272, u)
    c.save(); c.translate(px, py); c.scale(sc, sc); c.translate(-mx, -my)
    c.set_source_surface(surf('n_hand_gap_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
    c.restore()
    P2 = lambda p: (px + (p[0] - mx) * sc, py + (p[1] - my) * sc)
    a, b = P2(FT), P2(TH)
    ud = eo_cubic(prog(t, B(49), B(49) + 0.25))
    if ud > 0:
        # dimension line offset perpendicular
        ox, oy = 0, -46
        ax, ay, bx, by = a[0] + ox, a[1] + oy, b[0] + ox, b[1] + oy
        line(c, a[0], a[1] - 12, a[0], ay - 10, BONE, 0.7 * ud, 1.2)
        line(c, b[0], b[1] - 12, b[0], by - 10, BONE, 0.7 * ud, 1.2)
        mxp = (ax + bx) / 2
        line(c, mxp - (mxp - ax) * ud, ay, mxp + (bx - mxp) * ud, ay, BONE, 0.9, 1.4)
        for xx, sg in ((ax, 1), (bx, -1)):
            rgba(c, BONE, 0.9 * ud); c.move_to(xx, ay); c.line_to(xx + sg * 9, ay - 4); c.line_to(xx + sg * 9, ay + 4); c.fill()
        text(c, 'monom', 'd', mxp, ay - 18, 26, BONE, ud, align='center')
        text(c, 'mono', type_on('d -> 0', t, B(50), 0.04), mxp + 60, ay - 60, 22, CYAN, 0.9)
    q = [('Nothing,', B(48)), ('not', B(48.5)), ('one', B(49)), ('thing,', B(49.5))]
    wq = text_w('serif', 'Nothing, not one thing,', 84)
    words(c, 'serif', q, t, W - 130 - wq, 900, 84, BONE, 0.95)
    fx['flash'] = (1 - eo_cubic(prog(t, B(48), B(48) + 0.3)))
    fx['grain'] = 0.04
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ I6 ZENO  [B52, B58)
def s_zeno(c, g, t):
    fill_bg(c, INK)
    fx = {}
    kr = (t - B(52)) / P
    # beat 56: a half-beat full stop (only the thread trembles), then the approach + zoom catch up in the other half
    frozen = 4.0 <= kr < 4.5
    if frozen: kf = 4.0
    elif 4.5 <= kr < 5.0: kf = 4.0 + (kr - 4.5) * 2
    else: kf = kr
    n = math.floor(kf); ph = kf - n
    # gap halves in first half of a beat, then zoom x2 in the second half
    approach = eo_cubic(clamp(ph / 0.45))
    zoom = eo_expo(clamp((ph - 0.5) / 0.4))
    gap_world = 0.5 ** n * (1 - 0.5 * approach)
    Z = 2 ** n * (2 ** zoom)
    gap_px = 360 * gap_world * Z / 1.0
    cx, cy = 960, 520
    # fractal grid (two levels cross-fading)
    lv = math.log2(Z)
    for j in range(2):
        s_ = 2 ** (lv % 1 + j) * 30
        a_ = (0.10 if j == 0 else 0.10 * (lv % 1)) if j else 0.10 * (1 - (lv % 1)) + 0.04
        rgba(c, BONE, 0.08 if j == 0 else 0.04)
        c.set_line_width(1)
        x = cx % s_
        while x < W: c.move_to(x, 0); c.line_to(x, H); x += s_
        y = cy % s_
        while y < H: c.move_to(0, y); c.line_to(W, y); y += s_
        c.stroke()
    # fingertip: mechanical phalanx approaching from the left (curvature flattens with zoom)
    R = 300 * Z ** 0.5
    fx_ = cx - gap_px / 2
    def tip(cc, inset=0.0):
        cc.new_path(); cc.arc(fx_ - R, cy, R - inset, -math.pi / 2, math.pi / 2)
        cc.line_to(-10, cy + R - inset); cc.line_to(-10, cy - R + inset); cc.close_path()
    tip(c)
    lg = cairo.LinearGradient(fx_ - 2 * R, 0, fx_, 0); lg.add_color_stop_rgba(0, *INK2, 1); lg.add_color_stop_rgba(1, 0.20, 0.23, 0.27, 1)
    c.set_source(lg); c.fill()
    c.save(); tip(c); c.clip()
    rgba(c, BONE, 0.10); c.set_line_width(1)
    hs = 14
    for i in range(-80, 160):
        x = fx_ - i * hs
        c.move_to(x, cy - R); c.line_to(x - 2 * R, cy + R)
    c.stroke()
    rgba(c, BONE, 0.55); c.set_line_width(1.5)
    for i in range(1, 6):
        xx = fx_ - R * 0.42 * i
        c.move_to(xx, cy - R); c.line_to(xx, cy + R)
    c.stroke()
    for i in range(1, 6):
        xx = fx_ - R * 0.42 * i - R * 0.21
        for sgn in (-1, 1):
            rgba(c, BONE, 0.6); c.new_path(); c.arc(xx, cy + sgn * R * 0.55, max(2, R * 0.025), 0, 2 * math.pi); c.stroke()
    c.restore()
    tip(c, 14); rgba(c, BONE, 0.35); c.set_line_width(1.2); c.stroke()
    tip(c); rgba(c, BONE, 1); c.set_line_width(3); c.stroke()
    tip(g); rgba(g, CYAN, 0.25); g.set_line_width(6); g.stroke()
    # red thread on the right; trembles more the closer it gets (and most during the stop)
    tx = cx + gap_px / 2
    rj = random.Random(int(t * 60))
    amp = (1.0 + 1.1 * n) * (1.8 if frozen else 1.0)
    j1 = ((rj.random() - 0.5) * amp, (rj.random() - 0.5) * amp)
    j2 = ((rj.random() - 0.5) * amp * 3, (rj.random() - 0.5) * amp * 3)
    for cc, aa, lw in ((c, 1, 6), (g, 0.7, 10)):
        rgba(cc, RED, aa); cc.set_line_width(lw); cc.new_path()
        cc.move_to(tx + j1[0] * 0.5, cy + j1[1])
        cc.curve_to(tx + 200 + j2[0], cy - 40 * (1 / Z ** 0.3) + j2[1], tx + 600, cy + 160 / Z ** 0.3, W + 50, cy - 300 / Z ** 0.3)
        cc.stroke()
    # dimension
    line(c, fx_, cy - 140, fx_, cy - 60, BONE, 0.6, 1.2); line(c, tx, cy - 140, tx, cy - 60, BONE, 0.6, 1.2)
    line(c, fx_, cy - 100, tx, cy - 100, CYAN, 0.9, 1.6)
    dval = 0.5 ** n * (1 - 0.5 * approach)
    text(c, 'monom', f'd = {dval:.6f}', cx, cy - 130, 30, CYAN, 1, align='center')
    text(c, 'mono', f'zoom  x{Z:,.0f}'.replace(',', ' '), W - 120, 960, 28, BONE, 0.7, align='right', track=0.1)
    text(c, 'mono', 'lim d -> 0     d != 0', 120, 960, 28, BONE, 0.7, track=0.1)
    words(c, 'serif', [('can', B(54)), ('touch', B(54.5)), ('her.', B(55))], t, W - 130 - text_w('serif', 'can touch her.', 96), 880, 96, BONE, 0.95)
    fx['ab'] = 3 * pulse(t, B(52 + n + (0.75 if n == 4 else 0.5)), 0.15)
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ I7 NEAR  [B58, B60)
FT2 = (1314, 190); TH2 = (1366, 168)
def s_near(c, g, t):
    fill_bg(c, INK)
    fx = {}
    u = eo_expo(prog(t, B(58), B(58) + 0.5))
    sc = lerp(9.0, 2.0, u)
    mx, my = (FT2[0] + TH2[0]) / 2, (FT2[1] + TH2[1]) / 2
    px, py = lerp(960, 1180, u), lerp(520, 262, u)
    c.save(); c.translate(px, py); c.scale(sc, sc); c.translate(-mx, -my)
    c.set_source_surface(surf('n_hand_gap_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(min(1, u * 1.6))
    c.restore()
    a = (px + (FT2[0] - mx) * sc, py + (FT2[1] - my) * sc)
    b = (px + (TH2[0] - mx) * sc, py + (TH2[1] - my) * sc)
    ul = eo_cubic(prog(t, B(58.5), B(58.5) + 0.2))
    if ul > 0:
        line(c, a[0], a[1] - 50, b[0], b[1] - 50 + (a[1] - b[1]) * 0, CYAN, ul, 1.6)
        text(c, 'monom', 'd != 0', (a[0] + b[0]) / 2, a[1] - 70, 30, CYAN, ul, align='center')
    qs = 'Nothing, not one thing, can touch her.'
    words(c, 'serif', [(qs, B(58.5))], t, W - 130 - text_w('serif', qs, 64), 640, 64, BONE, 0.9)
    text(c, 'mono', type_on('— abandoned lab note, project ŌMETEŌTL', t, B(59), 0.02), W - 130, 700, 20, BONE, 0.5, align='right')
    fx['grain'] = 0.04
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ I8 TITLE  [B60, end)
_TP = {}
def title_layout():
    if not _TP:
        f = fonts()['monom']; size = 126
        s = 'world.execute(me);'
        cols = [BONE] * 5 + [GREY] + [CYAN] * 7 + [GREY] + [RED] * 2 + [GREY] + [BONE]
        gl = f.glyphs(s, 960, 590, size, align='center')
        # sample points per glyph
        pts = []
        for d, col in zip(gl, cols):
            ss = cairo.ImageSurface(cairo.FORMAT_A8, W, H); cc = cairo.Context(ss)
            cc.new_path(); f.glyph_path(cc, d['g'], d['x'], d['y'], size); cc.set_source_rgba(0, 0, 0, 1); cc.fill()
            ss.flush()
            m = np.ndarray((H, ss.get_stride()), np.uint8, ss.get_data())[:, :W]
            ys, xs = np.nonzero(m > 128)
            if len(xs):
                r = np.random.default_rng(d['i'])
                idx = r.choice(len(xs), min(len(xs), 260), replace=False)
                for x, y in zip(xs[idx], ys[idx]): pts.append((x, y, col))
        _TP['gl'] = list(zip(gl, cols)); _TP['pts'] = pts; _TP['size'] = size
        r = np.random.default_rng(9)
        _TP['vel'] = r.normal(0, 1, (len(pts), 2)) * np.array([260, 160])
    return _TP

def s_title(c, g, t):
    fill_bg(c, INK)
    fx = {}
    L = title_layout(); f = fonts()['monom']; size = L['size']
    tb = B(64)
    if t < tb:
        nvis = int((t - B(60)) / (P / 8)) + 1
        build = prog(t, B(62.3), tb)
        rnd = random.Random(int(t * 60))
        for d, col in L['gl'][:nvis]:
            jx = (rnd.random() - 0.5) * 6 * build ** 2; jy = (rnd.random() - 0.5) * 6 * build ** 2
            c.new_path(); f.glyph_path(c, d['g'], d['x'] + jx, d['y'] + jy, size); rgba(c, col, 1); c.fill()
            if build > 0:
                g.new_path(); f.glyph_path(g, d['g'], d['x'] + jx, d['y'] + jy, size); rgba(g, col, 0.5 * build); g.fill()
        # cursor
        last = L['gl'][min(nvis, len(L['gl'])) - 1][0]
        cxp = last['x'] + last['w'] + 8
        if nvis < len(L['gl']) or int((t - T0) / (P / 2)) % 2 == 0:
            rgba(c, CYAN, 0.9); c.rectangle(cxp, 590 - size * 0.72, size * 0.55, size * 0.84); c.fill()
        text(c, 'mono', 'ŌMETEŌTL  >', 960 - text_w('monom', 'world.execute(me);', size) / 2, 420, 26, BONE, 0.5, track=0.2)
        ul = eo_cubic(prog(t, B(62), tb))
        line(c, 480, 650, 480 + 960 * ul, 650, BONE, 0.3, 1.2)
        text(c, 'mono', 'press ENTER to execute', 960, 720, 20, BONE, 0.4 * ul, align='center', track=0.3)
    else:
        dt = t - tb
        sp = 1 - math.exp(-dt * 3.5)
        pts = L['pts']; vel = L['vel']
        for (x, y, col), (vx, vy) in zip(pts, vel):
            X = x + vx * sp * 0.9 + math.sin(y * 0.05 + t * 2) * 6 * sp
            Y = y + vy * sp * 0.9
            rgba(c, col, 0.95); c.rectangle(X - 1.6, Y - 1.6, 3.2, 3.2)
        c.fill()
        text(c, 'mono', 'set of points: ' + str(len(pts)), 960, 980, 20, BONE, 0.5 * prog(t, tb + 0.1, tb + 0.3), align='center', track=0.2)
    fx['flash'] = 0.7 * pulse(t, tb, 0.15)
    fx['ab'] = 8 * pulse(t, tb, 0.3)
    fx['glow'] = 1.0
    hud(c, t, True, a=0.6, log=False)
    if t > END_FADE: fx['flash'] = 0
    return fx
END_FADE = 99
