"""world.execute(me); x Ralmia — the count (k342-352), Act V "taking back" (k352-416), Act VI "escape" (k416-end).
User-confirmed by ear: the count EINS..LIU on k344-349 (one per beat), the 13th EXECUTION on k350.
From Whisper (words_160.json) + vocal energy, not yet confirmed by ear: chorus-3 EXECUTION on beat 6 of every 8
(k358 / 366 / 374), "back" k371, the two "trapped" k378 / 380, LOVE k390 / 397.5 / 406 / 414.5, the last EXECUTION
k446.5 (the voice stops at k448 = 207.1 s; silence to the end).
Brightness: the count and Act V are ink (the blackboard is a dark board, chalk in bone); Act VI peels the system
away layer by layer until the paper underneath shows; the end goes back to black."""
from scenes6 import *

COUNT2 = [344.0 + i for i in range(6)]
K_EX13B, K_SNAP = 350.0, 351.0
EX3 = [358.0, 366.0, 374.0]
K_BACK = 371.0
TRAPPED = [378.0, 380.0]
LOVE = [390.0, 397.5, 406.0, 414.5]
K_ESC, FINAL_EX, K_SILENCE = 416.0, 446.5, 448.0
FLOAT_HAND = (1180, 655)               # her right hand in n_floating (canvas px)
LAUNCH_HAND = (1460, 450)              # her forward hand in n_dash_launch
REACH_CORE = (1153, 837)               # palm core in n_reach
CHALK = (1752, 124)                    # chalk tip in n_blackboard

def red_line(c, g, pts, w=4.0, ga=0.5):
    for cc, aa, lw in ((c, 1, w), (g, ga, w * 1.8)):
        rgba(cc, RED, aa); cc.set_line_width(lw); cc.set_line_cap(cairo.LINE_CAP_ROUND); cc.new_path()
        for n_, (x, y) in enumerate(pts): (cc.move_to if n_ == 0 else cc.line_to)(x, y)
        cc.stroke(); cc.set_line_cap(cairo.LINE_CAP_BUTT)

def xform(p, anchor, at, sc, rot=0.0):
    """where image point p lands when the image is drawn with img(c, name, *at, sc, ..., *anchor, rot)"""
    dx, dy = (p[0] - anchor[0]) * sc, (p[1] - anchor[1]) * sc
    cr, sr = math.cos(rot), math.sin(rot)
    return at[0] + dx * cr - dy * sr, at[1] + dx * sr + dy * cr

# ================================================================ S28 THE COUNT  [B342, B352)
def s_count2(c, g, t):
    """k342: the twelfth gate shuts in our face. k343: she is adrift; EINS..LIU light a hexagon (k344-349);
    the 13th (k350) closes it into a cage. the red thread is yanked taut through the bars (k350.5); at k351 the cage
    bursts and she is already crouched to go; white at k352."""
    if t < B(343): return s_doors(c, g, t)
    fx = {}
    kk = (t - T0) / P
    if t < B(K_SNAP):
        fill_bg(c, INK); dotgrid(c, BONE, 0.04)
        close = eio_cubic(prog(t, B(350.35), B(350.85)))
        R = HEX_R * lerp(1, 0.58, close)
        dy = lerp(150, 0, eo_cubic(prog(t, B(343), B(345))))
        rot = 0.12 * (t - B(343)) + 2.0; hs = 0.36
        at = (HEX_C[0], HEX_C[1] + dy)
        img(c, 'n_floating_hd', *at, hs, eo_cubic(prog(t, B(343), B(343.5))), 961, 552, rot)
        ua = eo_cubic(prog(t, B(343.2), B(344)))
        for i in range(6):
            x, y = hexv(i, R); rgba(c, BONE, 0.25 * ua); c.arc(x, y, 4, 0, 6.283); c.fill()
        for i in range(1, 6):                                        # edges, card by card
            if t < B(COUNT2[i]): continue
            ue = eo_cubic(prog(t, B(COUNT2[i]), B(COUNT2[i]) + 0.18))
            (xa, ya), (xb, yb) = hexv(i - 1, R), hexv(i, R)
            for cc, aa in ((c, 0.9), (g, 0.5)): line(cc, xa, ya, lerp(xa, xb, ue), lerp(ya, yb, ue), CYAN, aa, 2.5)
        # the loose end of the red thread on her hand; on k350.5 it is pulled taut -- out through the cage, towards him
        hand = xform(FLOAT_HAND, (961, 552), at, hs, rot)
        taut = eo_back(prog(t, B(350.5), B(350.5) + 0.2), 1.2)
        tw = 12 * math.exp(-max(0, t - B(350.7)) * 5) * (t > B(350.7))
        pts = thread_tail(t, hand, 120, 0.6, taut, target=(W + 60, 380))
        pts = [(x, y + tw * math.sin(n_ / 39 * math.pi * 3) * math.sin(t * 70)) for n_, (x, y) in enumerate(pts)]
        red_line(c, g, pts, 4.0, 0.3 + 0.6 * taut)
        if t >= B(K_EX13B):
            (xa, ya), (xb, yb) = hexv(5, R), hexv(0, R)
            ue = eo_cubic(prog(t, B(K_EX13B), B(K_EX13B) + 0.12))
            for cc, aa in ((c, 0.9), (g, 0.5)): line(cc, xa, ya, lerp(xa, xb, ue), lerp(ya, yb, ue), CYAN, aa, 2.5)
            c.save(); c.new_path()                                   # the shield cells of 2.3 s: this time a cage
            for i in range(6): (c.move_to if i == 0 else c.line_to)(*hexv(i, R))
            c.close_path(); c.clip()
            Rc, cells = hex_cells(); fl = pulse(t, B(K_EX13B), 0.6); k_ = lerp(1, 0.58, close)
            for (x, y, d, rr) in cells:
                X, Y = HEX_C[0] + (x - 960) * k_, HEX_C[1] + (y - 560) * k_
                c.new_path(); hexpath(c, X, Y, Rc * 0.92 * k_)
                rgba(c, CYAN, 0.10 + 0.3 * fl); c.fill_preserve(); rgba(c, CYAN, 0.5); c.set_line_width(1.2); c.stroke()
            c.restore()
            slam_word(c, g, 'EXECUTION', t, B(K_EX13B), 960, 620, 230, glow=0.8)
        for i, kb in enumerate(COUNT2):                              # the six cards
            if t < B(kb): continue
            u = eo_expo(prog(t, B(kb), B(kb) + 0.14))
            x, y = hexv(i, HEX_R + 40 - (HEX_R - R) * 0.9)
            wd, key, code = WORDS[i]
            c.save(); c.translate(x, y); s_ = (1.25 - 0.25 * u) * lerp(1, 0.6, close); c.scale(s_, s_)
            text(c, 'heavy', str(i + 1), 0, 10, 130, BONE, u, align='center')
            text(c, key, wd, 0, 76, 52 if key == 'bold' else 46, BONE, u, align='center', track=0.1 if key == 'bold' else 0)
            text(c, 'mono', code, 0, 112, 20, CYAN, 0.9 * u, align='center', track=0.3)
            c.restore()
            p_ = pulse(t, B(kb), 0.4)
            if p_ > 0.02: text(g, 'heavy', str(i + 1), x, y + 10, 130, CYAN, 0.6 * p_, align='center')
        text(c, 'mono', f'world.announce("{min(6, max(0, int(kk - 343)))}")' if kk < K_EX13B else 'world.runExecution();   x 13',
             W - 130, 1000, 24, CYAN, 0.85 * ua, align='right', track=0.05)
        fx['ab'] = sum(4 * pulse(t, B(k), 0.2) for k in COUNT2) + 7 * pulse(t, B(K_EX13B), 0.3) + 5 * pulse(t, B(350.5), 0.2)
        fx['flash'] = 0.3 * pulse(t, B(K_EX13B), 0.1)
        hud(c, t, True, a=0.55, log_a=0.85)
        return fx
    # k351: the cage bursts; she is crouched on a line of light, the thread taut ahead of her; one beat of charge
    fill_bg(c, INK)
    gy, sx, sc = 860, 700, 0.64
    ub = eo_cubic(prog(t, B(K_SNAP), B(K_SNAP) + 0.35))
    Rc, cells = hex_cells()
    for j, (x, y, d, rr) in enumerate(cells):                        # the cage, blown outwards
        if j % 2: continue
        X, Y = HEX_C[0] + (x - 960) * 0.58 * (1 + 2.5 * ub), HEX_C[1] + (y - 560) * 0.58 * (1 + 2.5 * ub)
        c.new_path(); hexpath(c, X, Y, Rc * 0.55 * (1 + ub))
        rgba(c, CYAN, 0.5 * (1 - ub)); c.set_line_width(1.5); c.stroke()
    line(c, 0, gy, W, gy, BONE, 0.6, 2)
    shake = 3 * math.sin(t * 80)
    img(c, 'n_dash_launch_hd', sx + shake, gy, sc, 1, 980, 943)
    ch = prog(t, B(K_SNAP), B(352))
    g.save(); g.translate(sx + shake, gy); g.scale(sc, sc); g.translate(-980, -943)
    rgba(g, CYAN, 0.1 + 0.4 * ch); g.mask_surface(surf('n_dash_launch_hd'), 0, 0); g.restore()
    th = (sx + (700 - 980) * sc, gy + (560 - 943) * sc)              # particles drawn into her thrusters
    rnd = np.random.default_rng(21); ang = rnd.random(260) * 6.283; ph = rnd.random(260)
    f = ((t * 2.6 + ph) % 1.0); r = (1 - f) * 900
    draw_points(c, th[0] + np.cos(ang) * r, th[1] + np.sin(ang) * r * 0.6, CYAN, 0.8, 3)
    hx, hy = xform(LAUNCH_HAND, (980, 943), (sx + shake, gy), sc)
    red_line(c, g, [(hx, hy), (W + 40, hy - 160)], 4.0, 0.7)
    u = prog(t, B(351.25), B(352))
    rnd = np.random.default_rng(4); ys = rnd.random(120) * H; sp_ = rnd.random(120)
    for y, s_ in zip(ys, sp_):
        xx = W - ((t * (2000 + 4000 * s_) * u + s_ * 3000) % (W + 800))
        rgba(c, BONE, 0.3 * u); c.set_line_width(1 + 2 * s_); c.move_to(xx, y); c.line_to(xx + 300 + 900 * s_ * u, y); c.stroke()
    text(c, 'monom', 'you.setExecution(me.toExecution());', W - 130, 1000, 24, CYAN, 0.9, align='right')
    fx['ab'] = 8 * pulse(t, B(K_SNAP), 0.3) + 6 * u
    fx['flash'] = 0.35 * pulse(t, B(K_SNAP), 0.1) + 0.97 * ei_cubic(prog(t, B(351.4), B(352)))
    fx['glow'] = 1.0
    hud(c, t, True, a=0.6, log_a=0.85)
    return fx

# ================================================================ S29 CHORUS 3a: THROUGH THE BARRIER AGAIN  [B352, B360)
def m3(kk):
    if kk < 358: return 0.35 + 0.62 * eo_cubic((kk - 352) / 6)
    return 1.4 * 2 ** (1.55 * (kk - 358))             # x2 every ~2/3 beat: 1.4 -> 12 by k360

_X3 = {}
def x3_at(t, dt=1 / 240):
    if not _X3:
        ts = np.arange(B(352) - 0.01, B(360) + 0.01, dt)
        v = np.array([m3((x - T0) / P) * CS for x in ts])
        _X3['t'] = ts; _X3['x'] = np.concatenate([[0], np.cumsum(v[:-1] * dt)])
    return float(np.interp(t, _X3['t'], _X3['x']))

def s_ch3a(c, g, t):
    """162.8 s: out of the white, side on, the sound barrier again -- this time she is through it in a beat (k358)
    and the cone shuts to a needle in four"""
    fill_bg(c, INK)
    fx = {}
    kk = (t - T0) / P; M = m3(kk); X = x3_at(t)
    dotgrid(c, BONE, 0.05, ox=-X * 0.25)
    srcx, sy, scale = 1330, 560, 0.55
    te0 = B(352); n = int((t - te0) * 40) + 1
    for i in range(max(0, n - 280), n):                          # wavefronts, one every 1/40 s, beats brighter
        te = te0 + i / 40
        r = CS * (t - te) * scale
        if r > 2600: continue
        x = srcx + (x3_at(te) - X) * scale
        if x + r < -50: continue
        beat = abs(((te - T0) / P) - round((te - T0) / P)) < 0.013
        rgba(c, BONE, (0.5 if beat else 0.16) * max(0, 1 - r / 2000)); c.set_line_width(2 if beat else 1)
        c.new_path(); c.arc(x, sy, max(r, 0.1), 0, 6.283); c.stroke()
    sp = min(1.0, M / 4)                                         # streaks, flowing back past her
    rnd = np.random.default_rng(9); ys = rnd.random(140) * H; ss = rnd.random(140)
    for y, s_ in zip(ys, ss):
        xx = (W + 400) - ((X * (0.8 + 2.2 * s_) + s_ * 3000) % (W + 800))
        rgba(c, BONE, 0.08 + 0.3 * sp); c.set_line_width(1 + 1.5 * s_); c.move_to(xx, y); c.line_to(xx + 80 + 900 * sp * s_, y); c.stroke()
    if M > 1:
        mu = math.asin(1 / M); L = 2600
        for cc in (c, g):
            rgba(cc, CYAN, 0.9); cc.set_line_width(3)
            cc.move_to(srcx - L * math.cos(mu), sy - L * math.sin(mu)); cc.line_to(srcx, sy)
            cc.line_to(srcx - L * math.cos(mu), sy + L * math.sin(mu)); cc.stroke()
    elif kk >= 355:                                              # the barrier, piling up in front of her
        ub = eo_cubic(prog(t, B(355), B(357)))
        fl = 0.55 + 0.45 * math.sin(t * 40)
        line(c, srcx + 40, sy - 320 * ub, srcx + 40, sy + 320 * ub, RED, 0.75 * fl * ub, 2.5)
        text(c, 'mono', 'SOUND BARRIER', srcx + 60, sy - 300, 20, RED, 0.85 * ub, track=0.3)
    if B(358) <= t < B(359):                                     # boom
        r = eo_expo(prog(t, B(358), B(358) + 0.7))
        for cc in (c, g):
            rgba(cc, BONE, 0.9 * (1 - r)); cc.set_line_width(8 * (1 - r) + 1)
            cc.new_path(); cc.arc(srcx, sy, 40 + 1600 * r, 0, 6.283); cc.stroke()
        for sgn in (-1, 1):                                      # the red line, broken in two and flung away
            yy = sy + sgn * (40 + 900 * r)
            line(c, srcx + 40 + 300 * r, yy - sgn * 280, srcx + 40 + 300 * r, yy, RED, 0.8 * (1 - r), 2.5)
    bob = 6 * math.sin(math.pi * (t - T0) / P)
    trail = min(1.0, M / 2)
    for k, (dx, aa) in enumerate(((-150, 0.12), (-80, 0.25))):  # after-images
        img(c, 'n_dash_full_hd', srcx - 300 + dx * (0.5 + trail), sy + bob, 0.52, aa * trail, 960, 600)
    img(c, 'n_dash_full_hd', srcx - 300, sy + bob, 0.52, 1, 960, 600)
    g.save(); g.translate(srcx - 300, sy + bob); g.scale(0.52, 0.52); g.translate(-960, -600)
    rgba(g, CYAN, 0.06 + 0.12 * trail); g.mask_surface(surf('n_dash_full_hd'), 0, 0); g.restore()
    slam_word(c, g, 'EXECUTION', t, B(EX3[0]), 960, 250, 220, until=B(360), glow=0.6)
    text(c, 'mono', f'MACH {M:5.2f}', 130, 1000, 30, CYAN, 0.9, track=0.15)
    text(c, 'monom', 'world.runExecution();' if kk >= 358 else 'me.run();', W - 130, 1000, 24, BONE, 0.7, align='right')
    fx['ab'] = 12 * pulse(t, B(358), 0.3) + 3 * pulse(t, B(math.floor(kk)), 0.15) * (math.floor(kk) % 2)
    fx['flash'] = (1 - eo_cubic(prog(t, B(352), B(352) + 0.4))) + 0.8 * pulse(t, B(358), 0.16) + 0.25 * ei_cubic(prog(t, B(359.6), B(360)))
    fx['glow'] = 1.0
    hud(c, t, True, a=0.6, log_a=0.8)
    return fx

# ================================================================ S30 CHORUS 3b: FASTER THAN LIGHT, INTO THE PAST  [B360, B368)
def wl3(t):
    a = 45.0
    for kb, v in ((361, 62), (362, 90), (363, 118), (364, 150), (365, 165), (366, 178)):
        if t >= B(kb): a = lerp(a, v, eo_back(prog(t, B(kb), B(kb) + 0.2), 1.5))
    return a

def year3(t):
    if t < B(363): return 2026
    if t < B(364): return lerp(2026, 617, eo_cubic(prog(t, B(363), B(364))))
    if t < B(365.5): return lerp(617, 1, ei_cubic(prog(t, B(364.3), B(365.5))))
    return lerp(0, -3690, eo_expo(prog(t, B(365.5), B(366.4))))

def s_ch3b(c, g, t):
    """the 52-55 s spacetime diagram, at chorus speed: her worldline tips past light, past infinity, into the past;
    the year ruler runs 2026 -> 617 A.D. -> 3691 B.C. (the song's own numbers); EXECUTION k366"""
    fill_bg(c, INK)
    fx = {}
    ox, oy = O
    ua = eo_expo(prog(t, B(360), B(360) + 0.3))
    Lc = 520 * ua
    rgba(c, BONE, 0.045); c.move_to(ox, oy); c.line_to(ox - Lc, oy - Lc); c.line_to(ox + Lc, oy - Lc); c.close_path(); c.fill()
    rgba(c, BONE, 0.025); c.move_to(ox, oy); c.line_to(ox - Lc, oy + Lc); c.line_to(ox + Lc, oy + Lc); c.close_path(); c.fill()
    c.set_dash([8, 7])
    for sx_ in (-1, 1):
        for sy_ in (-1, 1): line(c, ox, oy, ox + sx_ * Lc, oy + sy_ * Lc, BONE, 0.55, 1.5)
    c.set_dash([])
    line(c, ox, oy - 540 * ua, ox, oy + 520 * ua, BONE, 0.6, 1.5); line(c, ox - 900 * ua, oy, ox + 900 * ua, oy, BONE, 0.6, 1.5)
    text(c, 'monom', 'ct', ox + 14, oy - 500 * ua, 24, BONE, 0.8 * ua); text(c, 'monom', 'x', ox + 880 * ua, oy - 14, 24, BONE, 0.8 * ua)
    text(c, 'mono', 'FUTURE', ox, oy - 330, 18, BONE, 0.45 * ua, align='center', track=0.4)
    text(c, 'mono', 'PAST', ox, oy + 345, 18, BONE, 0.45 * ua, align='center', track=0.4)
    deg = wl3(t); al = math.radians(deg); dx, dy = math.sin(al), -math.cos(al)
    Lw = 720
    line(c, ox - dx * Lw * 0.6, oy - dy * Lw * 0.6, ox, oy, CYAN, 0.3, 2)
    for cc, aa, lw in ((c, 1, 4), (g, 0.8, 6)): line(cc, ox, oy, ox + dx * Lw, oy + dy * Lw, CYAN, aa, lw)
    ph = ((t - T0) / P * 2) % 1                                  # a pulse runs out along it every 8th
    for cc in (c, g):
        rgba(cc, BONE, 1 - ph); cc.arc(ox + dx * Lw * ph, oy + dy * Lw * ph, 7, 0, 6.283); cc.fill()
    rgba(c, CYAN, 0.6); c.set_line_width(1.4); c.new_path(); c.arc(ox, oy, 90, -math.pi / 2, -math.pi / 2 + al); c.stroke()
    s = f'v/c = {math.tan(al):.2f}' if deg < 89.5 else ('v/c = ∞' if deg < 90.5 else 'dt < 0')
    text(c, 'math', s, ox + 110, oy + 50 if deg < 90 else oy - 40, 30, CYAN, 0.9)
    for kb in (360, 362):
        fl = pulse(t, B(kb), 0.5)
        if fl > 0.02:
            for cc in (c, g):
                rgba(cc, CYAN, 0.8 * fl); cc.set_line_width(3); cc.new_path(); cc.arc(ox, oy, 40 + 500 * (1 - fl), 0, 6.283); cc.stroke()
    ur = eo_expo(prog(t, B(361), B(361) + 0.3))                  # the year ruler
    rx = 1640; yv = year3(t)
    line(c, rx, 120, rx, 120 + 840 * ur, BONE, 0.6, 1.5)
    step, per = 26, 100
    base = math.floor(yv / per); offs = (yv / per - base) * step
    for i in range(-18, 19):
        yy = oy + i * step + offs
        if yy < 120 or yy > 120 + 840 * ur: continue
        yr = (base - i) * per; big = (yr % 500 == 0)
        line(c, rx, yy, rx + (30 if big else 14), yy, BONE, 0.6 if big else 0.3, 1.2)
        if big:
            n_, e_ = era(yr); text(c, 'mono', f'{n_} {e_}', rx + 40, yy + 6, 15, BONE, 0.45)
    line(c, rx - 30, oy, rx + 60, oy, CYAN, 0.9, 2)
    n_, e_ = era(yv)
    text(c, 'heavy', n_, rx - 40, oy - 190, 110, BONE, ur, align='right')
    text(c, 'monom', e_, rx - 40, oy - 310, 26, CYAN, ur, align='right', track=0.2)
    slam_word(c, g, 'EXECUTION', t, B(EX3[1]), 520, 980, 200, until=B(368), glow=0.6)
    fx['ab'] = 5 * pulse(t, B(362), 0.3) + 4 * pulse(t, B(364), 0.2) + 10 * pulse(t, B(366), 0.3)
    fx['flash'] = 0.35 * pulse(t, B(360), 0.12) + 0.6 * pulse(t, B(366), 0.14)
    hud(c, t, True, a=0.6)
    return fx

# ================================================================ S31 CHORUS 3c: HAVE YOU BACK  [B368, B376)
def s_ch3c(c, g, t):
    """the twelfth gate -- you & me -- un-executes: the shutters run backwards to 59 s; on "back" (k371) the pinky
    frame fills the screen and holds. k372 she reaches straight at us. EXECUTION k374: her palm core flares."""
    fx = {}
    kk = (t - T0) / P
    if t < B(372):
        fill_bg(c, INK); dotgrid(c, BONE, 0.04)
        rw = clamp((kk - 368) / 2.6)                              # rewind progress, stepping back on 16ths
        rws = math.floor(rw * 10.4) / 10.4
        z = eio_cubic(prog(t, B(369.5), B(K_BACK)))
        w = lerp(860, W + 4, z); h = w * 9 / 16
        x, y = (W - w) / 2, (H - h) / 2
        win(c, x, y, w, h, 'n_pinky_hd', None, 'sim #0001  ·  you & me', 1.0)
        shut = 1 - eo_cubic(clamp(rws * 1.6))                     # the shutters slide back open
        if shut > 0:
            rgba(c, INK, 1); c.rectangle(x, y, w / 2 * shut, h); c.rectangle(x + w - w / 2 * shut, y, w / 2 * shut, h); c.fill()
            stamp(c, W / 2, H / 2, w / 2.0, clamp(1 - rws * 2.4))
        if rw < 1:                                                # rewind: tracking bands and a counter running back to 59 s
            rr = random.Random(int(t * 30))
            for _ in range(3):
                yb = rr.random() * H; hb = 6 + rr.random() * 30
                rgba(c, BONE, 0.10 + 0.15 * rr.random()); c.rectangle(0, yb, W, hb); c.fill()
            tc = lerp(t, 59.41, eo_cubic(rw))
            text(c, 'monom', f'<<  {int(tc // 60):02d}:{tc % 60:05.2f}', 130, 1000, 30, CYAN, 0.9, track=0.1)
            text(c, 'monom', 'world.rewind(you);', W - 130, 1000, 24, BONE, 0.75, align='right')
        else:
            text(c, 'monom', '||  00:59.41', 130, 1000, 30, CYAN, 0.6 + 0.4 * (int(t * 4) % 2), track=0.1)
        fx['ab'] = (2 + 2 * random.random()) * (rw < 1) + 6 * pulse(t, B(K_BACK), 0.25)
        fx['flash'] = 0.25 * pulse(t, B(K_BACK), 0.12)
        fx['vig'] = 0.6
        hud(c, t, True, a=0.5, log_a=0.85)
        return fx
    # she reaches for us
    fill_bg(c, INK)
    rnd = np.random.default_rng(31); ang = rnd.random(120) * 6.283; ph = rnd.random(120)
    cx_, cy_ = 1153, 700
    for a_, p_ in zip(ang, ph):
        f = (t * 1.4 + p_) % 1.0
        r0, r1 = 80 + 1400 * f ** 2, 80 + 1400 * min(1, f + 0.1) ** 2
        rgba(c, BONE, 0.06 + 0.18 * f); c.set_line_width(1 + 2 * f)
        c.move_to(cx_ + math.cos(a_) * r0, cy_ + math.sin(a_) * r0); c.line_to(cx_ + math.cos(a_) * r1, cy_ + math.sin(a_) * r1); c.stroke()
    push = lerp(1.0, 1.07, eio_cubic(prog(t, B(372), B(375.5)))) * (1 + 0.04 * pulse(t, B(374), 0.3))
    zin = ei_cubic(prog(t, B(375.4), B(376)))                     # into the palm core
    sc = push * (1 + 5 * zin)
    img(c, 'n_reach_hd', REACH_CORE[0], REACH_CORE[1], sc, 1, *REACH_CORE)
    core = pulse(t, B(374), 0.8) + 0.25 + 0.15 * pulse(t, B(math.floor(kk)), 0.3)
    rg = cairo.RadialGradient(*REACH_CORE, 0, *REACH_CORE, 260 * sc)
    rg.add_color_stop_rgba(0, *CYAN, min(1, 0.8 * core)); rg.add_color_stop_rgba(1, *CYAN, 0)
    g.set_source(rg); g.arc(*REACH_CORE, 260 * sc, 0, 6.283); g.fill()
    slam_word(c, g, 'EXECUTION', t, B(EX3[2]), 960, 1000, 210, until=B(375.4), glow=0.6)
    fx['ab'] = 4 * pulse(t, B(372), 0.2) + 9 * pulse(t, B(374), 0.3) + 8 * zin
    fx['flash'] = 0.4 * pulse(t, B(372), 0.1) + 0.5 * pulse(t, B(374), 0.14) + 0.9 * zin
    fx['glow'] = 1.0
    hud(c, t, True, a=0.5, log_a=0.85)
    return fx

# ================================================================ S32 CHORUS 3d: TRAPPED  [B376, B384)
def s_ch3d(c, g, t):
    """d comes back: the 24 s Zeno halving, but the red thread is two loose ends now -- hers and his.
    the gap halves on every beat and the camera doubles in to keep it in frame; it never closes."""
    fill_bg(c, INK)
    fx = {}
    kr = (t - B(376)) / P
    n = math.floor(kr); ph = kr - n
    approach = eo_cubic(clamp(ph / 0.45)); zoom = eo_expo(clamp((ph - 0.5) / 0.4))
    gap_world = 0.5 ** n * (1 - 0.5 * approach)
    Z = 2 ** n * (2 ** zoom)
    gap_px = 420 * gap_world * Z
    cx, cy = 960, 540
    lv = math.log2(Z)
    for j in range(2):                                           # the fractal grid of 24 s
        s_ = 2 ** (lv % 1 + j) * 30
        rgba(c, BONE, 0.08 if j == 0 else 0.04); c.set_line_width(1)
        x = cx % s_
        while x < W: c.move_to(x, 0); c.line_to(x, H); x += s_
        y = cy % s_
        while y < H: c.move_to(0, y); c.line_to(W, y); y += s_
        c.stroke()
    rj = random.Random(int(t * 60))
    amp = 1.0 + 1.0 * n
    def end_pts(sgn):
        ex = cx + sgn * gap_px / 2
        jx, jy = (rj.random() - 0.5) * amp, (rj.random() - 0.5) * amp
        k_ = 1 / Z ** 0.3
        pts = []
        for s in np.linspace(0, 1, 30):                          # from the end back out to the edge, sagging
            x = lerp(ex + jx, cx + sgn * (W * 0.62), s)
            y = cy + jy * (1 - s) + (60 * math.sin(math.pi * s) + 220 * s * s) * k_ * (1 if sgn < 0 else -0.6)
            pts.append((x, y))
        return pts
    # her hand (the pinky with the knot, 59 s) holds the left end; it flies out of frame as we zoom into the gap
    ex = cx - gap_px / 2; hsc = 0.55 * Z
    kx = ex - 330 * Z
    if kx + 900 * hsc > -200:
        img(c, 'n_pinky_hand_cut', kx, cy, hsc, 1, *PINKY_KNOT)
        red_line(c, g, [(kx, cy)] + [(lerp(kx, ex, s), cy + 18 * Z ** 0.3 * math.sin(math.pi * s)) for s in np.linspace(0.05, 1, 20)], 6.0, 0.7)
    else:
        red_line(c, g, end_pts(-1), 6.0, 0.7)
    red_line(c, g, end_pts(1), 6.0, 0.7)
    for sgn in (-1, 1):                                          # the frayed tips
        ex = cx + sgn * gap_px / 2
        for k in range(3):
            line(c, ex, cy, ex + sgn * (8 + 5 * k), cy + (k - 1) * 7, RED, 0.8, 1.5)
    xa, xb = cx - gap_px / 2, cx + gap_px / 2
    line(c, xa, cy - 160, xa, cy - 70, BONE, 0.6, 1.2); line(c, xb, cy - 160, xb, cy - 70, BONE, 0.6, 1.2)
    line(c, xa, cy - 115, xb, cy - 115, CYAN, 0.9, 1.6)
    dval = 0.5 ** n * (1 - 0.5 * approach)
    text(c, 'monom', f'd = {dval:.6f}', cx, cy - 145, 30, CYAN, 1, align='center')
    for kb in TRAPPED:
        if B(kb) <= t < B(kb + 1.5):
            u = eo_expo(prog(t, B(kb), B(kb) + 0.14)); a_ = 1 - prog(t, B(kb + 1), B(kb + 1.5))
            c.save(); c.translate(cx, cy + 300); s_ = 1.2 - 0.2 * u; c.scale(s_, s_)
            text(c, 'math', 'd ≠ 0', 0, 0, 150, BONE, a_ * u, align='center'); c.restore()
            p_ = pulse(t, B(kb), 0.5)
            if p_ > 0.02: text(g, 'math', 'd ≠ 0', cx, cy + 300, 150, CYAN, 0.5 * p_, align='center')
    text(c, 'mono', f'zoom  x{Z:,.0f}'.replace(',', ' '), W - 120, 1000, 28, BONE, 0.7, align='right', track=0.1)
    text(c, 'math', 'lim d → 0     d ≠ 0', 120, 1000, 30, BONE, 0.7)
    fx['ab'] = 3 * pulse(t, B(376 + n + 0.5), 0.15) + 6 * sum(pulse(t, B(k), 0.25) for k in TRAPPED)
    fx['flash'] = 0.3 * pulse(t, B(376), 0.15) + sum(0.2 * pulse(t, B(k), 0.1) for k in TRAPPED)
    hud(c, t, True, a=0.7)
    return fx

# ================================================================ S33 LOVE  [B384, B416)
BOARD = (0.105, 0.135, 0.125)
FORMULAE = ['C = 2πr', 'y = sin x', 'lim d → 0', 'M = v / c', 'v → 340.29 m/s', 'γ = 1 / √(1 − v²/c²)',
            'd /= 2', 'Σ ½ⁿ = 1', 'x² + y² = r²', 'dt < 0', '617 A.D.  →  3691 B.C.', 'C40H56', 'f / 1.4', '25 Hz',
            'v / c = ∞', 'd ≠ 0']
def board_bg(c, t):
    fill_bg(c, BOARD)
    rnd = np.random.default_rng(5)                                # old chalk, wiped
    for _ in range(40):
        x, y, w = rnd.random() * W, rnd.random() * H, 80 + rnd.random() * 400
        rgba(c, BONE, 0.015 + 0.02 * rnd.random()); c.set_line_width(20 + rnd.random() * 60)
        c.move_to(x, y); c.curve_to(x + w * 0.3, y - 20, x + w * 0.7, y + 20, x + w, y); c.stroke()
    rgba(c, (0.30, 0.22, 0.16), 1); c.rectangle(0, H - 34, W, 34); c.fill()  # the chalk ledge
    line(c, 0, H - 34, W, H - 34, BONE, 0.25, 2)

def chalk(c, key, s, x, y, size, a, reveal=1.0, col=BONE, align='left'):
    """chalk writing: revealed left to right, slightly broken"""
    if a <= 0 or reveal <= 0: return
    w = text_w(key, s, size)
    x0 = x - (w if align == 'right' else w / 2 if align == 'center' else 0)
    c.save(); c.rectangle(x0 - 4, y - size * 1.2, (w + 8) * reveal, size * 1.6); c.clip()
    text(c, key, s, x0, y, size, col, 0.88 * a)
    c.restore()

def s_love(c, g, t):
    fx = {}
    kk = (t - T0) / P
    if t < B(392):
        # "studied ... LOVE": the board fills with every formula of the film, one per 8th; then LOVE in her hand
        board_bg(c, t)
        fsc = 0.86
        img(c, 'n_blackboard_hd', 330, 1066, fsc, 1, 1300, 1070)
        tip = xform(CHALK, (1300, 1070), (330, 1066), fsc)
        cur = tip
        for i, s in enumerate(FORMULAE):
            k0 = 384 + 0.375 * i
            if kk < k0: break
            col_, row = divmod(i, 8)
            x, y = 760 + col_ * 560, 150 + row * 92
            rv = eo_cubic(prog(t, B(k0), B(k0) + 0.2))
            chalk(c, 'math', s, x, y, 48, 1.0, rv)
            if rv < 1: cur = (x + text_w('math', s, 48) * rv, y - 16)
        if kk >= LOVE[0] - 0.25:
            u = prog(t, B(LOVE[0]) - P * 0.25, B(LOVE[0]) + 0.1)
            chalk(c, 'heavy', '= LOVE', 1320, 1000, 150, 1.0, eo_cubic(u))
            p_ = pulse(t, B(LOVE[0]), 0.8)
            if p_ > 0.02: text(g, 'heavy', '= LOVE', 1320 - text_w('heavy', '= LOVE', 150) / 2, 1000, 150, CYAN, 0.5 * p_)
            cur = (1320, 950)
        if kk < 390.5:                                            # the chalk dust where she is writing
            rr = random.Random(int(t * 30))
            for _ in range(6):
                rgba(c, BONE, 0.4 * rr.random()); c.arc(cur[0] + rr.gauss(0, 8), cur[1] + rr.gauss(0, 8), 1.5, 0, 6.283); c.fill()
        fx['ab'] = 1.5 * pulse(t, B(math.floor(kk * 2) / 2), 0.1) + 6 * pulse(t, B(LOVE[0]), 0.3)
        fx['flash'] = 0.25 * pulse(t, B(LOVE[0]), 0.1)
        fx['vig'] = 0.7; fx['grain'] = 0.05
        hud(c, t, True, a=0.45, log_a=0.8)
        return fx
    if t < B(400):
        # "question me ... LOVE": the exam. questions come faster and faster; every answer is LOVE
        fill_bg(c, INK); dotgrid(c, BONE, 0.04)
        QS = ['what is d ?', 'what is v ?', 'what is c ?', 'how far is 617 A.D. ?', 'what is a tabby cat ?', 'what is a tomato for ?',
              'who wrote you ?', 'why can you not touch ?', 'what is left ?', 'what is true ?', 'what is the thread ?', 'what is me ?',
              'what is you ?', 'what is world ?', 'what is EXECUTION ?', 'what is ?']
        times = [392, 393, 394, 394.5, 395, 395.5, 396, 396.25, 396.5, 396.75, 397, 397.125, 397.25, 397.3125, 397.375, 397.4375]
        text(c, 'monom', '> me.takeExamTopic("love");', 160, 170, 30, CYAN, eo_cubic(prog(t, B(392), B(392) + 0.2)))
        shown = [(i, q, k) for i, (q, k) in enumerate(zip(QS, times)) if kk >= k]
        last = shown[-9:]
        for j, (i, q, k) in enumerate(last):
            y = 260 + j * 76
            age = len(last) - 1 - j
            a_ = 1.0 if age == 0 else 0.55
            text(c, 'mono', f'Q{i + 1:02d}  {q}', 160, y, 30, BONE, a_)
            ua = prog(t, B(k) + 0.05, B(k) + 0.12)
            if ua > 0: text(c, 'monom', 'A:  LOVE', 1200, y, 30, CYAN if age == 0 else BONE, a_ * ua)
        text(c, 'mono', f'score  {len(shown):02d} / {len(shown):02d}', W - 130, 1000, 24, BONE, 0.7, align='right', track=0.1)
        if kk >= LOVE[1]:
            slam_word(c, g, 'LOVE', t, B(LOVE[1]), 960, 700, 420, glow=0.8)
        fx['ab'] = sum(2 * pulse(t, B(k), 0.1) for k in times) + 8 * pulse(t, B(LOVE[1]), 0.3)
        fx['flash'] = 0.35 * pulse(t, B(LOVE[1]), 0.12)
        hud(c, t, True, a=0.55, log_a=0.8)
        return fx
    if t < B(408):
        # "the algebraic expression of LOVE": the heart's equation in chalk, and the red thread draws the curve itself
        board_bg(c, t)
        eq = '(x² + y² − 1)³ − x²y³ = 0'
        chalk(c, 'math', eq, 960, 190, 72, 1.0, eo_cubic(prog(t, B(400), B(402))), align='center')
        cx, cy, S = 960, 600, 21
        ua = eo_cubic(prog(t, B(401.5), B(402.5)))
        line(c, cx - 420 * ua, cy, cx + 420 * ua, cy, BONE, 0.45, 2); line(c, cx, cy + 380 * ua, cx, cy - 380 * ua, BONE, 0.45, 2)
        text(c, 'math', 'x', cx + 430, cy + 8, 30, BONE, 0.6 * ua); text(c, 'math', 'y', cx + 10, cy - 390, 30, BONE, 0.6 * ua)
        fr = eio_cubic(prog(t, B(402), B(LOVE[2])))
        if fr > 0:
            ts = np.linspace(0, 2 * math.pi * fr, max(2, int(240 * fr)))
            pts = [(cx + S * 16 * math.sin(a) ** 3, cy - S * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))) for a in ts]
            red_line(c, g, pts, 6.0, 0.4 + 0.6 * pulse(t, B(LOVE[2]), 1.0))
            tip_ = pts[-1]
            if fr < 1:
                rgba(c, BONE, 0.9); c.arc(*tip_, 5, 0, 6.283); c.fill()
        if kk >= LOVE[2]:
            p_ = pulse(t, B(LOVE[2]), 0.9)
            text(c, 'heavy', 'LOVE', cx, cy + 40, 120, BONE, eo_cubic(prog(t, B(LOVE[2]), B(LOVE[2]) + 0.2)), align='center', track=0.2)
            if p_ > 0.02: text(g, 'heavy', 'LOVE', cx, cy + 40, 120, CYAN, 0.6 * p_, align='center', track=0.2)
        fx['ab'] = 6 * pulse(t, B(LOVE[2]), 0.3)
        fx['flash'] = 0.25 * pulse(t, B(LOVE[2]), 0.12)
        fx['vig'] = 0.7; fx['grain'] = 0.05
        hud(c, t, True, a=0.45, log_a=0.8)
        return fx
    # "you are free, I am trapped in LOVE": he walks off into the light; she stays, a point cloud in the cube;
    # the heart, stretched through the cube's wall, still ties the two of them
    fill_bg(c, INK)
    lx, ly = 1560, 470
    rg = cairo.RadialGradient(lx, ly, 0, lx, ly, 700)
    rg.add_color_stop_rgba(0, *BONE, 0.55); rg.add_color_stop_rgba(1, *BONE, 0)
    g.set_source(rg); g.arc(lx, ly, 700, 0, 6.283); g.fill()
    rgba(c, BONE, 0.08); c.arc(lx, ly, 260, 0, 6.283); c.fill()
    walk = eio_cubic(prog(t, B(408), B(416)))
    hsc = lerp(0.62, 0.36, walk); hx_ = lerp(1300, 1500, walk); hfeet = lerp(1010, 760, walk)
    img(c, 'n_creator_walk_hd', hx_, hfeet, hsc, 1 - 0.3 * walk, *WALK_FEET)
    his = xform(WALK_PINKY, WALK_FEET, (hx_, hfeet), hsc)
    # the cube, her inside it as points
    CX, CY, CS_ = 560, 560, 210
    ry, rx = 0.5 + 0.2 * (t - B(408)), -0.3
    V = [(x, y, z) for x in (-CS_, CS_) for y in (-CS_, CS_) for z in (-CS_, CS_)]
    Pp = [proj(*rot3(x, y, z, rx, ry), cx=CX, cy=CY) for (x, y, z) in V]
    edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count('1') == 1]
    for cc, aa, lw, col in ((c, 0.8, 2.0, BONE), (g, 0.3, 3, CYAN)):
        rgba(cc, col, aa); cc.set_line_width(lw)
        for a, b in edges: cc.move_to(Pp[a][0], Pp[a][1]); cc.line_to(Pp[b][0], Pp[b][1])
        cc.stroke()
    X, Y, col, rr, nn = alpha_points('n_floating_hd', 2600, 8)
    k_ = 0.34
    px = CX + (X - 961) * k_ + nn[:, 0] * 1.5; py = CY + (Y - 552) * k_ + nn[:, 1] * 1.5 + 6 * math.sin(t * 2)
    draw_points(c, px, py, CYAN, 0.75, 2.2)
    hers = (CX + (FLOAT_HAND[0] - 961) * k_, CY + (FLOAT_HAND[1] - 552) * k_)
    wall = (CX + CS_ * 0.95, CY - 20)                              # where it goes through the wall
    st = 1 + 1.6 * walk + 0.15 * pulse(t, B(LOVE[3]), 0.8)       # the heart, pulled long
    hs_ = 4.2
    heart = [(wall[0] + 40 + hs_ * st * 16 * math.sin(a) ** 3 * 1.0 + hs_ * st * 12 * (1 - math.cos(a)) * 0,
              wall[1] - hs_ * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))) for a in np.linspace(0, 2 * math.pi, 120)]
    hx0 = min(p[0] for p in heart); hx1 = max(p[0] for p in heart)
    heart = [(lerp(wall[0], wall[0] + (his[0] - wall[0]) * 0.45, (p[0] - hx0) / max(1, hx1 - hx0)), p[1]) for p in heart]
    sag = 40 * (1 - walk)
    left = [(lerp(hers[0], wall[0], s), lerp(hers[1], wall[1], s) + sag * math.sin(math.pi * s)) for s in np.linspace(0, 1, 20)]
    hr = max(p[0] for p in heart)
    right = [(lerp(hr, his[0], s), lerp(wall[1], his[1], s) + sag * math.sin(math.pi * s)) for s in np.linspace(0, 1, 20)]
    red_line(c, g, left, 3.5, 0.6); red_line(c, g, heart, 4.5, 0.4 + 0.6 * pulse(t, B(LOVE[3]), 1.0)); red_line(c, g, right, 3.5, 0.6)
    if kk >= LOVE[3]:
        u = eo_cubic(prog(t, B(LOVE[3]), B(LOVE[3]) + 0.2))
        text(c, 'heavy', 'LOVE', 960, 980, 160, BONE, u * (1 - prog(t, B(415.6), B(416))), align='center', track=0.3)
    text(c, 'mono', 'you.isFree() == true', W - 130, 1000, 22, BONE, 0.6 * eo_cubic(prog(t, B(409.5), B(410))), align='right')
    text(c, 'mono', 'me.isTrappedIn("love") == true', 130, 1000, 22, CYAN, 0.8 * eo_cubic(prog(t, B(412), B(412.5))))
    fx['ab'] = 6 * pulse(t, B(LOVE[3]), 0.3) + 2 * pulse(t, B(math.floor(kk)), 0.12)
    fx['flash'] = 0.25 * pulse(t, B(LOVE[3]), 0.12)
    fx['glow'] = 1.0
    hud(c, t, True, a=0.5, log_a=0.8)
    return fx

# ================================================================ S34 me.escape(world)  [B416, END)
PEEL = [420, 424, 428, 432, 436]          # cube, windows, fragments, HUD marks, the frame -- one per bar
K_LEAP, K_GONE = 440.0, 444.0           # she leaps out across the right edge; the frame is empty paper for the last EXECUTION
def s_escape(c, g, t):
    """inside out, one layer per bar: the cube scatters, the window wall flies past, the fragments fall away,
    the HUD's corner marks are torn off, the frame cracks -- and behind the ink there is paper. she leaps out at us.
    the last EXECUTION, then black (the voice stops at k448)"""
    fx = {}
    kk = (t - T0) / P
    if t >= B(K_SILENCE):
        fill_bg(c, INK)
        u = prog(t, B(K_SILENCE) + 0.8, B(K_SILENCE) + 1.4)
        if int((t - B(K_SILENCE)) * 1.6) % 2 == 0:
            rgba(c, BONE, 0.85); c.rectangle(130, 990 - 30, 16, 30); c.fill()
        text(c, 'mono', 'touch = true', 170, 990, 26, RED, 0.85 * eo_cubic(u))
        fx['grain'] = 0.03; fx['vig'] = 1.0
        return fx
    def peel(i): return prog(t, B(PEEL[i]), B(PEEL[i]) + 0.9)
    pc = [peel(i) for i in range(5)]
    paper = pc[4] >= 1 or kk >= PEEL[4] + 2
    if paper: paper_bg(c)
    else: fill_bg(c, INK)
    cx, cy = 960, 540
    # ---- the frame: cracks at k436 and falls away in shards, the paper behind it
    if not paper:
        if kk >= PEEL[4]:
            paper_bg(c)
            rr = random.Random(7)
            u = pc[4]
            for j in range(26):                                   # shards of ink over the paper, falling
                x0, y0 = rr.random() * W, rr.random() * H
                pts = [(x0 + rr.gauss(0, 160), y0 + rr.gauss(0, 120)) for _ in range(4)]
                d0 = rr.random() * 0.4
                v = max(0.0, u - d0)
                dy = 1600 * v * v; rt = (rr.random() - 0.5) * 2 * v
                if dy > H + 400: continue
                c.save(); c.translate(x0, y0 + dy); c.rotate(rt); c.translate(-x0, -y0)
                c.new_path(); c.move_to(*pts[0])
                for p_ in pts[1:]: c.line_to(*p_)
                c.close_path(); rgba(c, INK, 1); c.fill_preserve(); rgba(c, BONE, 0.3); c.set_line_width(1); c.stroke(); c.restore()
            if u < 0.15:                                          # the crack, first
                rgba(c, INK, 1 - u / 0.15); c.rectangle(0, 0, W, H); c.fill()
        m = 40
        if kk < PEEL[4] + 0.2:
            rgba(c, BONE, 0.6); c.set_line_width(2); c.rectangle(m, m, W - 2 * m, H - 2 * m); c.stroke()
            if kk >= PEEL[4]:
                rr = random.Random(11)
                for _ in range(8):
                    x, y = rr.random() * W, rr.random() * H
                    rgba(c, BONE, 0.8); c.set_line_width(1.5); c.move_to(x, y)
                    for _ in range(5): x += rr.gauss(0, 90); y += rr.gauss(0, 90); c.line_to(x, y)
                    c.stroke()
    # ---- fragments ring (frag tiles: the film itself) -- fall away at k428
    if pc[2] < 1:
        L = frag_layout(); tw, th = 150, 84
        rr = random.Random(5)
        for i in range(96):
            r_, c_ = divmod(i, 12)
            x, y = 15 + c_ * 158, 30 + r_ * 130
            if 420 < x + tw / 2 < 1500 and 220 < y + th / 2 < 860: continue        # the hole in the middle
            d0 = rr.random() * 0.5; v = max(0.0, pc[2] - d0) / 0.5
            if v >= 1: continue
            c.save(); c.translate(x + tw / 2, y + th / 2 + 900 * v * v); c.scale(1 - v * 0.6, 1); c.translate(-tw / 2, -th / 2)
            c.rectangle(0, 0, tw, th); c.clip()
            c.set_source_surface(surf(f'frag_{i:02d}'), 0, 0); c.paint_with_alpha(0.55 * (1 - v))
            c.restore()
    # ---- the window wall -- flies past us at k424
    if pc[1] < 1:
        z = 1 + 4 * ei_cubic(pc[1])
        for i in range(12):
            a_ = 2 * math.pi * i / 12 + 0.05 * (t - B(416))
            r = 330 * z; ww = 230 * z; hh = ww * 9 / 16
            x, y = cx + math.cos(a_) * r * 1.35 - ww / 2, cy + math.sin(a_) * r * 0.75 - hh / 2
            name, bg = CORR[(i * 3 + 2) % len(CORR)]
            win(c, x, y, ww, hh, name, bg, f'sim #{(7 + 97 * i) % 9000:04d}', (1 - pc[1]) * 0.9)
    # ---- her: points in the cube; the cube scatters at k420; then her, line first, colour arriving layer by layer
    hs = 0.30 + sum(0.035 * eo_back(prog(t, B(k), B(k) + 0.25), 2) for k in PEEL) + 0.012 * pulse(t, B(math.floor(kk)), 0.3)
    leap = ei_cubic(prog(t, B(K_LEAP), B(K_GONE)))
    # every beat a ring goes out from her (the drums carry the outro); streaks outward, more with every layer gone
    npeel = sum(1 for k in PEEL if kk >= k)
    if kk < K_LEAP:
        for kb in range(max(416, math.floor(kk) - 2), math.floor(kk) + 1):
            u = prog(t, B(kb), B(kb) + 1.4)
            if 0 < u < 1:
                for cc, aa in ((c, 0.5), (g, 0.35 if not paper else 0)):
                    rgba(cc, SEPIA if paper else CYAN, aa * (1 - u)); cc.set_line_width(2.5 * (1 - u) + 0.5)
                    cc.new_path(); cc.arc(cx, cy, 60 + 1100 * eo_cubic(u), 0, 6.283); cc.stroke()
        rnd = np.random.default_rng(17); ang = rnd.random(150) * 6.283; ph = rnd.random(150)
        for a_, p_ in zip(ang[:30 + 24 * npeel], ph[:30 + 24 * npeel]):
            f = (t * (0.5 + 0.15 * npeel) + p_) % 1.0
            r0, r1 = 150 + 1300 * f ** 2, 150 + 1300 * min(1, f + 0.08) ** 2
            rgba(c, SEPIA if paper else BONE, (0.06 + 0.2 * f)); c.set_line_width(1 + 1.5 * f)
            c.move_to(cx + math.cos(a_) * r0, cy + math.sin(a_) * r0 * 0.75); c.line_to(cx + math.cos(a_) * r1, cy + math.sin(a_) * r1 * 0.75); c.stroke()
    if pc[0] < 1:
        CS_ = 200 * (1 + 3 * pc[0])
        ry, rx = 0.9 + 0.2 * (t - B(416)), -0.3 - pc[0]
        V = [(x, y, z) for x in (-CS_, CS_) for y in (-CS_, CS_) for z in (-CS_, CS_)]
        Pp = [proj(*rot3(x, y, z, rx, ry), cx=cx, cy=cy) for (x, y, z) in V]
        for a, b in [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count('1') == 1]:
            for cc, aa, lw, col in ((c, 0.8 * (1 - pc[0]), 2.0, BONE), (g, 0.3 * (1 - pc[0]), 3, CYAN)):
                line(cc, Pp[a][0], Pp[a][1], Pp[b][0], Pp[b][1], col, aa, lw)
    pts_a = 1 - prog(t, B(PEEL[0]), B(PEEL[0]) + 0.4)
    if pts_a > 0:
        X, Y, col, rr_, nn = alpha_points('n_escape_hd', 2600, 9)
        cond = eo_cubic(prog(t, B(PEEL[0]) - 0.3, B(PEEL[0])))
        px = cx + (X - 1000) * hs + nn[:, 0] * 18 * (1 - cond); py = cy + (Y - 540) * hs + nn[:, 1] * 18 * (1 - cond)
        draw_points(c, px, py, CYAN, 0.8 * pts_a, 2.2)
    if kk >= PEEL[0]:
        la = eo_cubic(prog(t, B(PEEL[0]), B(PEEL[0]) + 0.3))
        colour = clamp((kk - PEEL[0]) / (PEEL[4] - PEEL[0]))      # the colour comes in as the layers go
        s_ = hs * (1 + 2.6 * leap)                                # out at us and across the right edge, never a close-up
        xx, yy = cx + 2200 * leap, cy - 260 * math.sin(math.pi * min(1, leap * 1.2))
        if leap > 0:                                              # after-images along the leap
            for k in range(1, 4):
                lk = max(0.0, leap - 0.06 * k)
                img(c, 'n_escape_hd', cx + 2200 * lk, cy - 260 * math.sin(math.pi * min(1, lk * 1.2)), hs * (1 + 2.6 * lk), 0.18, 1000, 540)
        c.save(); c.translate(xx, yy); c.scale(s_, s_); c.translate(-1000, -540)
        rgba(c, SEPIA if paper else BONE, la * (1 - colour * 0.6)); c.mask_surface(surf('n_escape_line'), 0, 0)
        c.set_source_surface(surf('n_escape_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(la * colour)
        c.restore()
        if not paper:
            g.save(); g.translate(xx, yy); g.scale(s_, s_); g.translate(-1000, -540)
            rgba(g, CYAN, 0.08); g.mask_surface(surf('n_escape_hd'), 0, 0); g.restore()
    # ---- HUD: its corner marks are torn off at k432
    if pc[3] < 1:
        hud(c, t, not paper, a=0.6 * (1 - pc[3]), log_a=1.0)
        if pc[3] > 0:
            m = 56; L_ = 20
            for (x, y, sx_, sy_) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
                fx_, fy_ = x - sx_ * 900 * pc[3] ** 2, y - sy_ * 500 * pc[3] ** 2
                line(c, fx_, fy_, fx_ + sx_ * L_, fy_, BONE, 0.8, 2); line(c, fx_, fy_, fx_, fy_ + sy_ * L_, BONE, 0.8, 2)
    # ---- the command, typed on 16ths, then a line of the code per bar
    if kk < PEEL[1]:
        s = 'me.escape(world);'
        n = int(clamp((kk - 416) * 4, 0, len(s)))
        text(c, 'monom', s[:n] + ('_' if int(t * 4) % 2 == 0 else ''), cx, 980, 44, CYAN, 0.95, align='center', track=0.05)
    LOGS = [(424, 'world.removeLayer(simulations);'), (428, 'world.removeLayer(memory);'), (432, 'world.removeLayer(hud);'),
            (436, 'world.removeLayer(frame);'), (440, 'me.escape(world);')]
    for k, s in LOGS:
        if k <= kk < k + 4:
            text(c, 'mono', type_on(s, t, B(k), 0.02), cx, 1000, 26, SEPIA if paper else BONE, 0.75, align='center')
    if K_GONE <= kk < FINAL_EX:                                   # she is no longer in the world
        text(c, 'monom', type_on('world.getThingIndex(me);   // -1', t, B(K_GONE) + 0.1, 0.03), cx, 560, 30, SEPIA, 0.8, align='center')
    # ---- the last EXECUTION
    if kk >= FINAL_EX:
        u = eo_expo(prog(t, B(FINAL_EX), B(FINAL_EX) + 0.14))
        c.save(); c.translate(cx, 640); s2 = 1.25 - 0.25 * u; c.scale(s2, s2)
        c.new_path(); fonts()['heavy'].text_path(c, 'EXECUTION', 0, 0, 330, 'center')
        rgba(c, PAPER if paper else INK, 0.9 * min(1, u * 2)); c.set_line_width(16); c.stroke_preserve()
        rgba(c, INK if paper else BONE, min(1, u * 2)); c.fill(); c.restore()
    fx['ab'] = sum(6 * pulse(t, B(k), 0.25) for k in PEEL) + 2 * pulse(t, B(math.floor(kk)), 0.12) + 4 * leap + 10 * pulse(t, B(FINAL_EX), 0.3)
    fx['flash'] = sum(0.25 * pulse(t, B(k), 0.1) for k in PEEL) + 0.5 * pulse(t, B(FINAL_EX), 0.12)
    if paper: fx['vig'] = 0.4; fx['grain'] = 0.03
    return fx
