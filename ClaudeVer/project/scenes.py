"""world.execute(me); x Ralmia — first 30 seconds. Scene definitions."""
from lib import *

# ---------------------------------------------------------------- shared bits
def words(c, key, items, t, x, y, size, col, a=1.0, rise=10, dur=0.12, gap=0.28):
    """items: [(word, t_on)]. Words laid out in a row; each fades/rises in at its time."""
    cx = x
    sp = text_w(key, ' ', size)
    for w, ton in items:
        ww = text_w(key, w, size)
        u = eo_cubic(prog(t, ton, ton + dur))
        if u > 0:
            text(c, key, w, cx, y + rise * (1 - u), size, col, a * u)
        cx += ww + sp
    return cx

LOG = [(B(0), 'sys.power(ON)'), (B(4), 'shield.enable()'), (B(8), 'pieces.lay(grid)'),
       (B(12), 'obj = new Object()'), (B(16), 'obj.fill(data, params)'), (B(21), 'obj.init()'),
       (B(24), 'world = new World()'), (B(28), 'world.simulate()'), (B(32), 'run'),
       (B(36), 'v -> 340.29 m/s'), (B(40), 'mach > 1'), (B(44), 'v -> c'),
       (B(48), 'touch(target)'), (B(52), 'd /= 2'), (B(58), 'err: d != 0'), ]

def hud(c, t, dark=True, a=1.0, log=True, log_a=1.0):
    """log_a: extra opacity for the boot log only. Scenes pass < 1 while big type sits in the top-left."""
    col = BONE if dark else SEPIA
    m = 56; L = 20
    for (x, y, sx, sy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        line(c, x, y, x + sx * L, y, col, 0.45 * a, 1.4); line(c, x, y, x, y + sy * L, col, 0.45 * a, 1.4)
    text(c, 'monom', 'ŌMETEŌTL', m + 34, m + 24, 17, col, 0.75 * a, track=0.18)
    text(c, 'mono', 'RALMIA / MACHINA', m + 34 + text_w('monom', 'ŌMETEŌTL', 17, 0.18) + 22, m + 24, 17, col, 0.4 * a, track=0.08)
    # top right: timecode + beat squares
    tc = f'{int(t // 60):02d}:{t % 60:05.2f}'
    text(c, 'mono', tc, W - m - 34, m + 24, 17, col, 0.6 * a, align='right', track=0.06)
    kb = math.floor((t - T0) / P)
    x0 = W - m - 34 - text_w('mono', tc, 17, 0.06) - 30 - 4 * 16
    for i in range(4):
        on = (kb % 4 == i) and t >= T0
        k_t = B(kb) if on else -9
        aa = 0.25 + 0.75 * (pulse(t, k_t, 0.5) if on else 0)
        rgba(c, CYAN if (on and i == 0) else col, aa * a)
        c.rectangle(x0 + i * 16, m + 12, 10, 10)
        c.fill() if on else (c.set_line_width(1.2), c.stroke())
    if not log or log_a <= 0.01: return
    a = a * log_a
    # boot log (last 3 lines) under the id
    past = [(tt, s) for tt, s in LOG if tt <= t][-3:]
    for j, (tt, s) in enumerate(past):
        age = len(past) - 1 - j
        shown = type_on('> ' + s, t, tt, 0.018)
        y = m + 58 + j * 24
        text(c, 'mono', shown, m + 34, y, 16, CYAN if (age == 0 and dark) else col, (0.85 if age == 0 else 0.35) * a)
        if t > tt + 0.35 and age > 0:
            text(c, 'mono', 'ok', m + 34 + text_w('mono', '> ' + s + '  ', 16), y, 16, col, 0.35 * a)

def ruler(c, y, x0, x1, col, a, t0, t, step=40):
    """ticks along a horizontal line, revealed from center outward."""
    u = eo_expo(prog(t, t0, t0 + 0.35))
    half = u * (x1 - x0) / 2; cx = (x0 + x1) / 2
    for i in range(int((x1 - x0) / step) + 1):
        x = x0 + i * step
        if abs(x - cx) > half: continue
        big = (i % 5 == 0)
        line(c, x, y + 6, x, y + (22 if big else 12), col, a * (0.6 if big else 0.3), 1.2)
        if big and i % 10 == 0:
            text(c, 'mono', f'{x:04d}', x + 4, y + 36, 12, col, a * 0.35)

# ================================================================ S1 POWER  [0, B4)
def s_power(c, g, t):
    fill_bg(c, INK)
    fx = {}
    LY = 640
    # cursor before the line
    if t < B(0):
        if int(t * 6) % 2 == 0:
            rgba(c, BONE, 0.9); c.rectangle(950, LY - 30, 16, 30); c.fill()
    # the power line
    u = eo_expo(prog(t, B(0), B(0) + 0.32))
    if u > 0:
        half = u * W / 2
        line(c, W / 2 - half, LY, W / 2 + half, LY, BONE, 0.9, 2.2)
        ruler(c, LY, 40, W - 40, BONE, 0.9, B(0), t)
    # current pulses
    for k, dur in ((1, 0.42), (2, 0.34), (3, 0.26), (3.5, 0.2)):
        p_ = prog(t, B(k), B(k) + dur)
        if 0 < p_ < 1:
            x = lerp(-300, W + 300, ei_cubic(p_) * 0.35 + p_ * 0.65)
            for cc in (c, g):
                grd = cairo.LinearGradient(x - 320, 0, x, 0)
                grd.add_color_stop_rgba(0, *CYAN, 0); grd.add_color_stop_rgba(1, *CYAN, 1)
                cc.set_source(grd); cc.set_line_width(5); cc.move_to(x - 320, LY); cc.line_to(x, LY); cc.stroke()
                rgba(cc, BONE, 1); cc.arc(x, LY, 5, 0, 2 * math.pi); cc.fill()
    # Switch on the
    um = eio_cubic(prog(t, B(2) - 0.12, B(2) + 0.1))
    ssz = lerp(150, 76, um); sy_ = lerp(LY - 60, 236, um)
    words(c, 'serif', [('Switch', B(0)), ('on', 0.58), ('the', 1.04)], t, 150, sy_, ssz, BONE, 0.95, rise=20)
    # POWER letters drop in on 16ths starting at "power"
    f = fonts()['heavy']; size = 440
    gl = f.glyphs('POWER', 140, LY - 18, size, track=0.0)
    pulse_x = lambda tt: lerp(-300, W + 300, ei_cubic(prog(tt, B(2), B(2) + 0.34)) * 0.35 + prog(tt, B(2), B(2) + 0.34) * 0.65)
    for d in gl:
        ti = B(2) + d['i'] * P / 8
        uu = prog(t, ti, ti + 0.16)
        if uu <= 0: continue
        dy = -90 * (1 - eo_back(uu, 2.2))
        cx_ = d['x'] + d['w'] / 2
        # charged when the current passes
        t_charge = B(2) + 0.34 * clamp((cx_ + 300) / (W + 600)) * 1.2
        ch = prog(t, t_charge, t_charge + 0.06)
        c.new_path(); f.glyph_path(c, d['g'], d['x'], d['y'] + dy, size)
        if ch < 1:
            rgba(c, BONE, 0.9 * min(1, uu * 4)); c.set_line_width(2.2); c.stroke_preserve()
        rgba(c, BONE, ch); c.fill()
        fl = pulse(t, t_charge, 0.35)
        if fl > 0.01:
            g.new_path(); f.glyph_path(g, d['g'], d['x'], d['y'] + dy, size); rgba(g, CYAN, 0.9 * fl); g.fill()
    # power symbol, right side
    cx, cy, R = 1585, 395, 118
    ua = eo_cubic(prog(t, B(2.5), B(2.5) + 0.22))
    on = prog(t, B(3), B(3) + 0.02)
    col = CYAN if on > 0 else BONE
    if ua > 0:
        a0 = -math.pi / 2 + 0.62; a1 = -math.pi / 2 - 0.62 + 2 * math.pi
        for cc, aa in ((c, 1), (g, on)):
            if aa <= 0: continue
            cc.new_path(); cc.arc(cx, cy, R, a0, a0 + (a1 - a0) * ua)
            rgba(cc, col, aa); cc.set_line_width(17); cc.set_line_cap(cairo.LINE_CAP_ROUND); cc.stroke()
        ub = eo_back(prog(t, B(3) - 0.06, B(3) + 0.1))
        if ub > 0:
            for cc, aa in ((c, 1), (g, on)):
                if aa <= 0: continue
                rgba(cc, col, aa); cc.set_line_width(17); cc.set_line_cap(cairo.LINE_CAP_ROUND)
                cc.move_to(cx, cy - R - 26 + 60 * (1 - ub)); cc.line_to(cx, cy - 10 + 60 * (1 - ub) * 0.2); cc.stroke()
        c.set_line_cap(cairo.LINE_CAP_BUTT); g.set_line_cap(cairo.LINE_CAP_BUTT)
    # shock ring
    if t >= B(3):
        r = eo_expo(prog(t, B(3), B(3) + 0.6))
        for cc in (c, g):
            rgba(cc, CYAN, 0.7 * (1 - r)); cc.set_line_width(3); cc.arc(cx, cy, R + 700 * r, 0, 2 * math.pi); cc.stroke()
    # L I N E spaced along the power line
    for i, ch in enumerate('LINE'):
        ti = B(2.5) + i * P / 8
        uu = eo_cubic(prog(t, ti, ti + 0.1))
        if uu > 0:
            text(c, 'monom', ch, 1350 + i * 135, LY + 92 + 12 * (1 - uu), 64, BONE, uu)
    fx['ab'] = 7 * pulse(t, B(3), 0.25)
    fx['flash'] = 0.18 * pulse(t, B(3), 0.12)
    hud(c, t, True, a=eo_cubic(prog(t, B(0), B(0) + 0.3)))
    return fx

# ================================================================ S2 PROTECTION  [B4, B8)
_HEX = None
def hex_cells():
    global _HEX
    if _HEX is None:
        R = 46; cells = []
        for q in range(-16, 17):
            for r in range(-16, 17):
                x = 960 + R * 1.5 * q; y = 560 + R * math.sqrt(3) * (r + q / 2)
                if -60 < x < W + 60 and -60 < y < H + 60:
                    d = (abs(q) + abs(r) + abs(q + r)) // 2
                    cells.append((x, y, d, random.Random(q * 99 + r).random()))
        _HEX = (R, cells)
    return _HEX

def hexpath(c, x, y, R):
    for i in range(6):
        a = math.pi / 3 * i
        (c.move_to if i == 0 else c.line_to)(x + R * math.cos(a), y + R * math.sin(a))
    c.close_path()

def s_protect(c, g, t):
    fill_bg(c, INK)
    fx = {}
    R, cells = hex_cells()
    tp = B(6)  # "protection"
    for (x, y, d, rr) in cells:
        ta = B(4) + d * 0.035 + rr * 0.05
        u = eo_cubic(prog(t, ta, ta + 0.14))
        if u <= 0: continue
        rad = R * 0.92 * (0.5 + 0.5 * u)
        inside = d <= 6
        wave = 0.0
        if t >= tp:
            front = (t - tp) / 0.032
            wave = math.exp(-((front - d) ** 2) / 2.5)
        hit = pulse(t, B(7), 0.4) * (1 if inside else 0.35)
        a_st = 0.34 + 0.5 * wave + 0.5 * hit
        c.new_path(); hexpath(c, x, y, rad)
        if inside and t >= tp + d * 0.032:
            rgba(c, CYAN, 0.06 + 0.12 * hit + 0.15 * wave); c.fill_preserve()
        rgba(c, CYAN, a_st); c.set_line_width(1.3); c.stroke()
        if wave > 0.2 or hit > 0.2:
            g.new_path(); hexpath(g, x, y, rad); rgba(g, CYAN, 0.6 * max(wave, hit)); g.set_line_width(2); g.stroke()
    # shield rim
    if t >= tp:
        u = eo_expo(prog(t, tp, tp + 0.3))
        rim = 6.4 * R * 1.5
        for cc, aa in ((c, 0.8), (g, 0.7)):
            rgba(cc, CYAN, aa); cc.set_line_width(2.5)
            cc.new_path(); cc.arc(960, 560, rim, -math.pi / 2, -math.pi / 2 + 2 * math.pi * u); cc.stroke()
    words(c, 'serif', [('Remember', B(4)), ('to', 2.40), ('put', 2.78), ('on', 3.02)], t, 150, 268, 76, BONE, 0.9)
    # PROTECTION, letters appear from the center outward
    f = fonts()['heavy']; size = 250
    gl = f.glyphs('PROTECTION', 960, 650, size, align='center', track=0.01)
    n = len(gl)
    for d in gl:
        dc = abs(d['i'] - (n - 1) / 2)
        ti = tp + dc * 0.035
        u = eo_cubic(prog(t, ti, ti + 0.12))
        if u <= 0: continue
        c.save()
        cx_ = d['x'] + d['w'] / 2
        c.translate(cx_, 650); c.scale(1, 0.4 + 0.6 * u); c.translate(-cx_, -650)
        c.new_path(); f.glyph_path(c, d['g'], d['x'], d['y'], size)
        rgba(c, BONE, u); c.fill()
        c.restore()
    # brackets slam on beat 7
    ub = eo_expo(prog(t, B(7), B(7) + 0.18))
    if t >= B(7) - 0.01:
        wtot = f.width('PROTECTION', size, 0.01)
        for sgn in (-1, 1):
            x = 960 + sgn * (wtot / 2 + 50 + 600 * (1 - ub))
            for cc, aa in ((c, 1.0), (g, 0.6 * pulse(t, B(7), 0.5))):
                rgba(cc, BONE if cc is c else CYAN, aa); cc.set_line_width(7)
                cc.move_to(x - sgn * 34, 650 - size * f.cap - 30); cc.line_to(x, 650 - size * f.cap - 30)
                cc.line_to(x, 690); cc.line_to(x - sgn * 34, 690); cc.stroke()
        text(c, 'mono', 'INTEGRITY  100%', 960, 760, 22, CYAN, 0.8 * ub, align='center', track=0.3)
    fx['ab'] = 6 * pulse(t, B(7), 0.2)
    hud(c, t, True)
    return fx

# ================================================================ S3 PIECES  [B8, B12)
def dotgrid(c, col, a, step=48, ox=0, oy=0):
    rgba(c, col, a)
    for x in range(int(ox) % step, W, step):
        for y in range(int(oy) % step, H, step):
            c.rectangle(x - 1, y - 1, 2, 2)
    c.fill()

PART_ORDER = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 6]          # n_parts_<i>; the core gem (6) lands last
PART_NAME = ['phalanx', 'phalanx', 'phalanx', 'tip', 'knuckle', 'palm ring', 'bearing', 'wrist cuff',
             'plate A', 'plate B', 'screw', 'CORE']
def s_pieces(c, g, t):
    """'Lay down your pieces': letters land on the 8ths, her mechanical parts on the 16ths in between; the core lands on k11."""
    paper_bg(c)
    fx = {}
    zoom = 1 + 0.025 * prog(t, B(8), B(12))
    c.save(); c.translate(960, 560); c.scale(zoom, zoom); c.translate(-960, -560)
    dotgrid(c, SEPIA, 0.16)
    words(c, 'serif', [('Lay', B(8)), ('down', 4.26), ('your', 4.70)], t, 150, 248, 76, SEPIA, 0.95)
    f = fonts()['heavy']; size = 270
    sw, gap = 230, 24
    x0 = (W - (6 * sw + 5 * gap)) / 2; top, bot = 320, 620
    us = eo_expo(prog(t, B(8), B(8) + 0.3))
    for i in range(6):
        x = x0 + i * (sw + gap)
        c.set_dash([8, 6]); rgba(c, SEPIA, 0.35 * us); c.set_line_width(1.4)
        c.rectangle(x, top + (1 - us) * 30, sw, bot - top); c.stroke(); c.set_dash([])
        text(c, 'mono', f'p{i}', x + 6, bot + 24, 15, SEPIA, 0.5 * us)
    settle = 8 * pulse(t, B(11), 0.25)
    for i, ch in enumerate('PIECES'):
        x = x0 + i * (sw + gap)
        tl = B(8) + i * P / 2 + 0.17       # landing time
        u = prog(t, tl - 0.17, tl)
        if u <= 0: continue
        rr = random.Random(i * 7)
        rot0 = (rr.random() - 0.5) * 0.9
        cw = f.width(ch, size)
        bx = x + sw / 2; by = bot - 30
        fall = ei_cubic(u)
        dy = -520 * (1 - fall); rot = rot0 * (1 - fall)
        land = prog(t, tl, tl + 0.16)
        sq = 0
        if t >= tl: sq = math.sin(land * math.pi) * (1 - land) * 0.9
        c.save(); c.translate(bx, by + dy + settle); c.rotate(rot); c.scale(1 + 0.08 * sq, 1 - 0.1 * sq)
        c.new_path(); f.glyph_path(c, f.glyphs(ch, 0, 0, size)[0]['g'], -cw / 2 + 10, 12, size)
        rgba(c, SEPIA, 0.18 * min(1, u * 2)); c.fill()
        c.new_path(); f.glyph_path(c, f.glyphs(ch, 0, 0, size)[0]['g'], -cw / 2, 0, size)
        rgba(c, INK, min(1, u * 3)); c.fill()
        c.restore()
        if t >= tl:
            v = eo_cubic(prog(t, tl, tl + 0.22))
            for sx in (-1, 1):
                line(c, bx + sx * (cw / 2 + 6 + 30 * v), by + 4, bx + sx * (cw / 2 + 22 + 50 * v), by + 4, SEPIA, 0.7 * (1 - v), 2.5)
            rgba(c, SEPIA, 0.05 * eo_cubic(prog(t, tl, tl + 0.1))); c.rectangle(x, top, sw, bot - top); c.fill()
    # parts tray: 12 cells, one part per 16th note
    n = len(PART_ORDER); cw_, ch_, gp = 118, 150, 14
    px0 = (W - (n * cw_ + (n - 1) * gp)) / 2; ptop = 690
    ut = eo_expo(prog(t, B(8.1), B(8.1) + 0.3))
    for j, pi in enumerate(PART_ORDER):
        x = px0 + j * (cw_ + gp)
        c.set_dash([4, 5]); rgba(c, SEPIA, 0.3 * ut); c.set_line_width(1.1)
        c.rectangle(x, ptop, cw_, ch_); c.stroke(); c.set_dash([])
        tl = B(8.25 + j * 0.25)
        u = prog(t, tl - 0.12, tl)
        if u > 0:
            s_ = surf(f'n_parts_{pi}')
            iw, ih = s_.get_width(), s_.get_height()
            sc = min((cw_ - 14) / iw, (ch_ - 34) / ih) * (1.25 if pi == 6 else 1.0)
            rot = (random.Random(pi).random() - 0.5) * 1.2 * (1 - ei_cubic(u))
            dy = -360 * (1 - ei_cubic(u))
            land = prog(t, tl, tl + 0.14)
            sq = math.sin(land * math.pi) * (1 - land) * 0.8 if t >= tl else 0
            cx_, cy_ = x + cw_ / 2, ptop + (ch_ - 24) / 2
            c.save(); c.translate(cx_, cy_ + dy + settle * 0.6); c.rotate(rot); c.scale(sc * (1 + 0.08 * sq), sc * (1 - 0.1 * sq))
            c.set_source_surface(s_, -iw / 2, -ih / 2); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(min(1, u * 3))
            c.restore()
            if t >= tl:
                text(c, 'mono', PART_NAME[j], x + 6, ptop + ch_ - 8, 12, CYAN if pi == 6 else SEPIA, 0.75)
                rgba(c, SEPIA, 0.06 * eo_cubic(prog(t, tl, tl + 0.1))); c.rectangle(x, ptop, cw_, ch_); c.fill()
            if pi == 6:
                gl_ = pulse(t, tl, 0.5)
                if gl_ > 0.02:
                    rg = cairo.RadialGradient(cx_, cy_, 0, cx_, cy_, 90)
                    rg.add_color_stop_rgba(0, *CYAN, 0.9 * gl_); rg.add_color_stop_rgba(1, *CYAN, 0)
                    g.set_source(rg); g.arc(cx_, cy_, 90, 0, 6.283); g.fill()
    text(c, 'mono', f'parts  {sum(1 for j in range(n) if t >= B(8.25 + j * 0.25)):02d} / {n}', px0, ptop - 14, 15, SEPIA, 0.6 * ut)
    c.restore()
    hud(c, t, False)
    fx['grain'] = 0.03; fx['vig'] = 0.4
    fx['ab'] = 3 * pulse(t, B(11), 0.2)
    return fx

# ================================================================ S4 OBJECT CREATION  [B12, B16)
_PTS = {}
def line_points(name, n, box, seed=1):
    key = (name, n)
    if key not in _PTS:
        m = cv2.imread(f'{WORK}/assets/{name}_line.png', 0)
        x0, y0, x1, y1 = box
        ys, xs = np.nonzero(m[y0:y1, x0:x1] < 120)
        r = np.random.default_rng(seed); idx = r.choice(len(xs), n, replace=False)
        _PTS[key] = (xs[idx] + x0, ys[idx] + y0, r.random(n))
    return _PTS[key]

def s_object(c, g, t):
    paper_bg(c)
    fx = {}
    gx, gy = 1228, 562      # palm core in n_hand_palm
    # stage 1 guides
    ug = eo_cubic(prog(t, B(12), B(12) + 0.3))
    c.set_line_width(1.2)
    rgba(c, SEPIA, 0.28 * ug)
    c.move_to(gx - 1500 * ug, gy); c.line_to(gx + 1500 * ug, gy); c.stroke()
    c.move_to(gx, gy - 900 * ug); c.line_to(gx, gy + 900 * ug); c.stroke()
    c.set_dash([6, 6]); c.new_path(); c.arc(gx, gy, 430, math.pi, math.pi + 2 * math.pi * ug); c.stroke(); c.set_dash([])
    rgba(c, CYAN, 0.7 * ug); c.set_line_width(1.6); c.new_path(); c.arc(gx, gy, 92, 0, 2 * math.pi * ug); c.stroke()   # v2: red is only touch / the barrier
    # points pop in
    xs, ys, rr = line_points('n_hand_palm', 1700, (640, 0, 1920, 1080))
    pa = 1 - prog(t, B(14), B(14) + 0.3)
    if pa > 0:
        vis = rr < prog(t, B(12), B(13))
        rgba(c, SEPIA, 0.85 * pa)
        for x, y in zip(xs[vis], ys[vis]): c.rectangle(x - 1.5, y - 1.5, 3, 3)
        c.fill()
    # stage 2: line art revealed by scanline
    sx = lerp(680, 1920, eo_cubic(prog(t, B(13), B(13) + 0.36)))
    if t >= B(13):
        c.save(); c.rectangle(0, 0, sx, H); c.clip()
        c.set_operator(cairo.OPERATOR_MULTIPLY); draw_img(c, 'n_hand_palm_line', 1.0); c.set_operator(cairo.OPERATOR_OVER)
        c.restore()
        if sx < 1915:
            for cc in (c, g):
                line(cc, sx, 0, sx, H, CYAN, 0.9, 2)
            text(c, 'mono', f'x={int(sx)}', sx + 8, 1030, 14, CYAN, 0.9)
    # stage 3: colour bursts out of the core
    if t >= B(14):
        u = eo_cubic(prog(t, B(14), B(14) + 0.42))
        rad = 1500 * u
        c.save(); c.new_path(); c.arc(gx, gy, rad, 0, 2 * math.pi); c.clip()
        draw_img(c, 'n_hand_palm_hd', 1.0)
        c.restore()
        if u < 1:
            for cc in (c, g):
                rgba(cc, CYAN, 0.9 * (1 - u)); cc.set_line_width(3); cc.new_path(); cc.arc(gx, gy, rad, 0, 2 * math.pi); cc.stroke()
    # core glow on beat 15 and 15.5
    for k in (14, 15, 15.5):
        p_ = pulse(t, B(k), 0.45)
        if p_ > 0.01:
            rg = cairo.RadialGradient(gx, gy, 0, gx, gy, 120)
            rg.add_color_stop_rgba(0, *CYAN, 0.9 * p_); rg.add_color_stop_rgba(1, *CYAN, 0)
            g.set_source(rg); g.arc(gx, gy, 120, 0, 2 * math.pi); g.fill()
    # annotation
    ua = eo_cubic(prog(t, B(14.5), B(14.5) + 0.25))
    if ua > 0:
        ex, ey = gx + 380 * ua, gy - 230 * ua
        line(c, gx + 40, gy - 24, ex, ey, INK, 0.8, 1.4)
        line(c, ex, ey, ex + 300 * ua, ey, INK, 0.8, 1.4)
        text(c, 'mono', type_on('core', t, B(14.5), 0.03), ex + 4, ey - 34, 16, INK, 0.6)
        text(c, 'monom', type_on('ŌMETEŌTL', t, B(14.6), 0.03), ex + 4, ey - 10, 24, INK, 0.9, track=0.12)
    # text block
    words(c, 'serif', [('and', 5.42), ("let's", 5.80), ('begin', 6.10)], t, 130, 640, 70, SEPIA, 0.95)
    fo = fonts()['thin']
    for d in fo.glyphs('OBJECT', 124, 815, 190, track=0.04):
        ti = B(13) + d['i'] * P / 8
        u = eo_cubic(prog(t, ti, ti + 0.08))
        if u > 0:
            c.new_path(); fo.glyph_path(c, d['g'], d['x'], d['y'] - 14 * (1 - u), 190); rgba(c, INK, u); c.fill()
    fh = fonts()['heavy']
    gl = fh.glyphs('CREATION', 120, 1010, 210, track=0.0)
    us = prog(t, B(14), B(14) + 0.3)
    uf = eo_cubic(prog(t, B(15), B(15) + 0.06))
    if us > 0:
        c.new_path()
        for d in gl: fh.glyph_path(c, d['g'], d['x'], d['y'], 210)
        if uf < 1:
            path = c.copy_path(); rgba(c, INK, 1); c.set_line_width(2.2); partial_stroke(c, eo_cubic(us))
            c.append_path(path)
        rgba(c, INK, uf); c.fill()
    fx['flash'] = 0.0
    fx['ab'] = 4 * pulse(t, B(15), 0.2); fx['vig'] = 0.4
    hud(c, t, False)
    return fx
