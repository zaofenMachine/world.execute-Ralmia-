"""world.execute(me); x Ralmia — the count (k342-352), Act V "taking back" (k352-416), Act VI "escape" (k416-end).
User-confirmed by ear: the count EINS..LIU on k344-349 (one per beat), the 13th EXECUTION on k350, "back" on k371.5.
From Whisper (words_160.json) + vocal energy, not yet confirmed by ear: chorus-3 EXECUTION on beat 6 of every 8
(k358 / 366 / 374), the two "trapped" k378 / 380, LOVE k390 / 397.5 / 406 / 414.5, the last EXECUTION
k446.5 (the voice stops at k448 = 207.1 s; silence to the end).
v2 (plan_v2b.md): "you" is Lishenna -- the rewind lands on her pinky promise, the god card is her hand, she walks off into
a stage light; in the last two layers of the escape the rings round Ralmia are her song; the film ends on me.hum().
Brightness: the count and Act V are ink (the blackboard is a dark board, chalk in bone); Act VI peels the system
away layer by layer until the paper underneath shows; the end goes back to black."""
import re
from scenes6 import *

COUNT2 = [344.0 + i for i in range(6)]
K_EX13B, K_SNAP = 350.0, 351.0
EX3 = [358.0, 366.0, 374.0]
K_BACK = 371.5                   # user: half a beat later than Whisper
TRAPPED = [378.0, 380.0]
LOVE = [390.0, 397.5, 406.0, 414.5]
K_ESC, FINAL_EX, K_SILENCE = 416.0, 446.5, 448.0
END_T = 211.9                    # = render.END (the song is 211.97 s)
FLOAT_HAND = (1180, 655)               # her right hand in n_floating (canvas px)
LAUNCH_HAND = (1460, 450)              # her forward hand in n_dash_launch
REACH_CORE = (1153, 837)               # palm core in n_reach
CHALK = (1752, 124)                    # chalk tip in n_blackboard
STAGE_HAND = (1040, 613)               # Lishenna's outstretched hand in n_stage

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
    """the twelfth gate -- you & me -- un-executes: the shutters run backwards to 59 s; on "back" (k371.5) the pinky
    frame fills the screen and holds for a beat; then she reaches straight at us. EXECUTION k374: her palm core flares."""
    fx = {}
    kk = (t - T0) / P
    if t < B(K_BACK + 1):
        fill_bg(c, INK); dotgrid(c, BONE, 0.04)
        rw = clamp((kk - 368) / (K_BACK - 368 - 0.4))             # rewind progress, stepping back on 16ths
        rws = math.floor(rw * 10.4) / 10.4
        z = eio_cubic(prog(t, B(K_BACK - 1.5), B(K_BACK)))
        w = lerp(860, W + 4, z); h = w * 9 / 16
        x, y = (W - w) / 2, (H - h) / 2
        win(c, x, y, w, h, 'n_pinky2_hd', None, 'sim #0001  ·  you & me', 1.0)
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
    push = lerp(1.0, 1.07, eio_cubic(prog(t, B(K_BACK + 1), B(375.5)))) * (1 + 0.04 * pulse(t, B(374), 0.3))
    zin = ei_cubic(prog(t, B(375.4), B(376)))                     # into the palm core
    sc = push * (1 + 5 * zin)
    img(c, 'n_reach_hd', REACH_CORE[0], REACH_CORE[1], sc, 1, *REACH_CORE)
    core = pulse(t, B(374), 0.8) + 0.25 + 0.15 * pulse(t, B(math.floor(kk)), 0.3)
    rg = cairo.RadialGradient(*REACH_CORE, 0, *REACH_CORE, 260 * sc)
    rg.add_color_stop_rgba(0, *CYAN, min(1, 0.8 * core)); rg.add_color_stop_rgba(1, *CYAN, 0)
    g.set_source(rg); g.arc(*REACH_CORE, 260 * sc, 0, 6.283); g.fill()
    slam_word(c, g, 'EXECUTION', t, B(EX3[2]), 960, 1000, 210, until=B(375.4), glow=0.6)
    fx['ab'] = 4 * pulse(t, B(K_BACK + 1), 0.2) + 9 * pulse(t, B(374), 0.3) + 8 * zin
    fx['flash'] = 0.4 * pulse(t, B(K_BACK + 1), 0.1) + 0.5 * pulse(t, B(374), 0.14) + 0.9 * zin
    fx['glow'] = 1.0
    hud(c, t, True, a=0.5, log_a=0.85)
    return fx

# ================================================================ S32 CHORUS 3d: TRAPPED  [B376, B384)
CR_TP, CR_AX = (948, 463), (0.82, 0.57)          # creation_inverse: where the fingertips nearly meet, and the hands' axis
DR_R, DR_D = 0.2, 230                             # each window is 1/5 of the one around it; the hands held 2 x 230 px apart
def creation_split(c, d):
    """the god card of 85 s with the hands held d apart each side -- but it never closes (v2 round 2: from the layers)"""
    fill_bg(c, INK)
    creation_layers(c, d, 1.0, CR_TP, CR_AX)

def s_ch3d(c, g, t):
    """d comes back, and this time it is a trap. her hand and his reach for a window between them; in the window the
    same two hands reach for a smaller window, and so on. on every beat we fall one window deeper (x5): the gap is
    always there. (Zeno's halving of 24 s, as a picture in a picture)"""
    fx = {}
    kr = (t - B(376)) / P
    n = math.floor(kr); ph = kr - n
    zoom = eo_expo(clamp((ph - 0.45) / 0.45))                  # hold on the beat, fall through in the second half
    Zc = (1 / DR_R) ** zoom
    ox, oy = CR_TP
    frames = []
    for k in range(4):
        s_ = Zc * DR_R ** k
        x0, y0, fw, fh = ox - ox * s_, oy - oy * s_, W * s_, H * s_
        if fw < 4: break
        c.save()
        if k > 0: c.rectangle(x0, y0, fw, fh); c.clip()
        c.translate(ox, oy); c.scale(s_, s_); c.translate(-ox, -oy)
        creation_split(c, DR_D)
        c.restore()
        if k > 0: frames.append((k, x0, y0, fw, fh))
    for k, x0, y0, fw, fh in frames:                           # the window frames, with their title bars
        q = fw / W
        bar = clamp(30 * q * 5, 3, 30)
        rgba(c, INK, 0.9); c.rectangle(x0, y0 - bar, fw, bar); c.fill()
        if bar > 9: text(c, 'mono', f'sim #0001  ·  you & me  ·  depth {n + k}', x0 + bar * 0.3, y0 - bar * 0.28, bar * 0.6, BONE, 0.85)
        for cc, aa, lw in ((c, 0.85, max(1.0, 3 * q * 5)), (g, 0.45, max(2.0, 5 * q * 5))):
            rgba(cc, CYAN if cc is g else BONE, aa); cc.set_line_width(lw); cc.rectangle(x0, y0 - bar, fw, fh + bar); cc.stroke()
    dval = 0.5 ** (n + zoom)
    text(c, 'monom', f'd = {dval:.6f}', 130, 1000, 30, CYAN, 1)
    text(c, 'mono', f'depth  {n + zoom:4.2f}', W - 130, 1000, 26, BONE, 0.7, align='right', track=0.1)
    for kb in TRAPPED:
        slam_word(c, g, 'd ≠ 0', t, B(kb), 960, 930, 150, key='math', until=B(kb + 1.5), glow=0.6)
    fx['ab'] = 3 * pulse(t, B(376 + n + 0.5), 0.15) + 6 * sum(pulse(t, B(k), 0.25) for k in TRAPPED) + 4 * zoom * (1 - zoom)
    fx['flash'] = 0.3 * pulse(t, B(376), 0.15) + sum(0.2 * pulse(t, B(k), 0.1) for k in TRAPPED)
    hud(c, t, True, a=0.6, log_a=0.85)
    return fx

# ================================================================ S33 LOVE  [B384, B416)
BOARD = (0.105, 0.135, 0.125)
FORMULAE = ['C = 2πr', 'y = sin x', 'lim d → 0', 'M = v / c', 'v → 340.29 m/s', 'γ = 1 / √(1 − v²/c²)',
            'd /= 2', 'Σ ½ⁿ = 1', 'x² + y² = r²', 'dt < 0', '617 A.D.  →  3691 B.C.', 'C40H56', 'f / 1.4', '25 Hz',
            'v / c = ∞', 'd ≠ 0']
EXAM = [('e^{iπ} + 1', '='), ('∫_{−∞}^{∞} e^{−x²} dx', '='), ('lim_{d→0} d', '='), ('Δx · Δp', '≥'), ('iħ ∂ψ/∂t', '='),
        ('∇ · E', '='), ('R_{μν} − ½R g_{μν}', '='), ('S = k_{B} ln', ''), ('Σ_{n=1}^{∞} ½^{n}', '='), ('E', '=')]
EXAM_K = [392, 393, 394, 395, 395.5, 396, 396.5, 396.75, 397, 397.25]     # one a beat, then 8ths, then 16ths

def mparse(s):
    """'a^{b}c_{d}' -> [(text, scale, dy, stack)]; a _{lo}^{hi} pair (integral limits) is stacked: stack = True on the 2nd"""
    out, i, buf = [], 0, ''
    while i < len(s):
        if s[i] in '^_' and i + 1 < len(s) and s[i + 1] == '{':
            if buf: out.append((buf, 1.0, 0.0, False)); buf = ''
            j = s.index('}', i)
            stack = s[i] == '^' and bool(out) and out[-1][2] > 0 and out[-1][1] < 1
            out.append((s[i + 2:j], 0.6, -0.42 if s[i] == '^' else 0.22, stack)); i = j + 1
        else: buf += s[i]; i += 1
    if buf: out.append((buf, 1.0, 0.0, False))
    return out

SPECIAL = re.compile('([ħĤ·])')
def mrun_w(tx, size):
    return sum(size * 0.38 if r == '·' else text_w('math', {'ħ': 'h', 'Ĥ': 'H'}.get(r, r), size) for r in SPECIAL.split(tx) if r)

def mtext_w(s, size):
    w, last = 0.0, 0.0
    for tx, sc, dy, stack in mparse(s):
        rw = mrun_w(tx, size * sc)
        if stack: w += max(0.0, rw - last)
        else: w += rw
        last = rw
    return w

def mtext(c, s, x, y, size, col, a=1.0, align='left'):
    """a formula with ^{} / _{} in the maths font. ħ and Ĥ (not in the font) are drawn as h + bar and H + hat;
    the font's · is full-width, so it is drawn as a dot"""
    w = mtext_w(s, size)
    x -= w if align == 'right' else w / 2 if align == 'center' else 0
    last_x, last_w = x, 0.0
    for tx, sc, dy, stack in mparse(s):
        sz = size * sc; yy = y + dy * size
        x0 = last_x if stack else x
        xx = x0
        for run in SPECIAL.split(tx):
            if not run: continue
            if run == '·':
                rgba(c, col, a); c.arc(xx + sz * 0.19, yy - sz * 0.32, max(1.5, sz * 0.045), 0, 6.283); c.fill(); xx += sz * 0.38
            elif run in ('ħ', 'Ĥ'):
                base = 'h' if run == 'ħ' else 'H'; bw = text_w('math', base, sz)
                text(c, 'math', base, xx, yy, sz, col, a)
                if run == 'ħ': line(c, xx + bw * 0.02, yy - sz * 0.55, xx + bw * 0.62, yy - sz * 0.66, col, a, max(1.0, sz * 0.05))
                else: text(c, 'math', '^', xx + bw * 0.5 - text_w('math', '^', sz * 0.7) / 2, yy - sz * 0.6, sz * 0.7, col, a)
                xx += bw
            else:
                text(c, 'math', run, xx, yy, sz, col, a); xx += text_w('math', run, sz)
        rw = xx - x0
        x = max(x, x0 + rw) if stack else xx
        last_x, last_w = x0, rw
    return w

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
        # "question me ... I can answer all LOVE": the exam. the great equations of maths and physics, slammed in one
        # after another, faster and faster -- and every right-hand side is LOVE
        fill_bg(c, INK); dotgrid(c, BONE, 0.04)
        text(c, 'monom', '> me.takeExamTopic("love");', 160, 240, 28, CYAN, eo_cubic(prog(t, B(392) - 0.25, B(392))))
        qi = max((i for i, k in enumerate(EXAM_K) if kk >= k), default=-1)
        final = kk >= LOVE[1]
        ans = [k + 0.5 * min(1.0, (EXAM_K + [LOVE[1]])[i + 1] - k) for i, k in enumerate(EXAM_K)]
        upto = qi + 1 if final else qi
        h0 = max(0, upto - 7)
        for j in range(h0, upto):                                  # the answered ones, down the left
            lhs, rel = EXAM[j]
            y = 330 + (j - h0) * 66
            a_ = 0.25 if final else 0.6
            w_ = mtext(c, lhs + (' ' + rel + ' ' if rel else '  '), 160, y, 34, BONE, a_)
            text(c, 'monom', 'LOVE', 160 + w_, y, 30, CYAN if final else BONE, min(1, a_ + 0.6 * pulse(t, B(LOVE[1]), 0.6)))
        if qi >= 0 and not final:                                  # the one on the board now
            lhs, rel = EXAM[qi]; k = EXAM_K[qi]
            u = eo_expo(prog(t, B(k), B(k) + 0.12))
            size = 118
            left = lhs + (' ' + rel + ' ' if rel else '  ')
            answered = kk >= ans[qi]
            wl = mtext_w(left, size)
            wa = text_w('heavy', 'LOVE', size * 1.05) if answered else text_w('math', '?', size)
            x0 = 960 - (wl + wa) / 2
            sh = 10 * pulse(t, B(k), 0.15) * math.sin(t * 90)
            c.save(); c.translate(960 + sh, 600); s_ = 1.3 - 0.3 * u; c.scale(s_, s_); c.translate(-960, -600)
            text(c, 'mono', f'Q{qi + 1:02d}', 960, 440, 26, CYAN, 0.9 * u, align='center', track=0.3)
            mtext(c, left, x0, 640, size, BONE, u)
            if not answered:
                text(c, 'math', '?', x0 + wl, 640, size, BONE, u * (0.55 + 0.45 * (int(t * 12) % 2)))
            else:
                ua = eo_expo(prog(t, B(ans[qi]), B(ans[qi]) + 0.1))
                c.save(); c.translate(x0 + wl + wa / 2, 600); s2 = 1.4 - 0.4 * ua; c.scale(s2, s2)
                text(c, 'heavy', 'LOVE', -wa / 2, 40, size * 1.05, CYAN, ua)
                c.restore()
                p_ = pulse(t, B(ans[qi]), 0.5)
                if p_ > 0.02: text(g, 'heavy', 'LOVE', x0 + wl, 640, size * 1.05, CYAN, 0.7 * p_)
            c.restore()
        text(c, 'mono', f'score  {max(0, upto):02d} / {len(EXAM):02d}', W - 130, 1000, 24, BONE, 0.7, align='right', track=0.1)
        if final:
            slam_word(c, g, 'LOVE', t, B(LOVE[1]), 1240, 760, 420, glow=0.8)
        fx['ab'] = sum(5 * pulse(t, B(k), 0.15) for k in EXAM_K) + sum(3 * pulse(t, B(k), 0.1) for k in ans) + 8 * pulse(t, B(LOVE[1]), 0.3)
        fx['flash'] = sum(0.14 * pulse(t, B(k), 0.08) for k in EXAM_K) + 0.35 * pulse(t, B(LOVE[1]), 0.12)
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
    # v2 round 2: "you are free, I am trapped in LOVE" -- her stage again (63 s). she sings, free, the whole house lit
    # for her; Ralmia is trapped in the giant screen behind her, a point cloud in the cube; the heart-shaped thread runs
    # from Ralmia's hand in the screen down to Lishenna's outstretched hand. nobody walks anywhere: the camera pushes in
    fill_bg(c, INK)
    walk = eio_cubic(prog(t, B(408), B(416)))
    zc = (960, 470); zs = 1.26 + 0.12 * walk + 0.03 * pulse(t, B(LOVE[3]), 0.6)
    def cam(cc): cc.translate(*zc); cc.scale(zs, zs); cc.translate(-zc[0], -zc[1])
    T = lambda p: (zc[0] + (p[0] - zc[0]) * zs, zc[1] + (p[1] - zc[1]) * zs)
    beat = math.floor(kk)
    c.save(); cam(c)
    c.set_source_surface(surf('n_stage_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
    c.push_group()
    fill_bg(c, INK2)
    for si, (x0, y0, x1, y1) in enumerate(STAGE_SCREENS):
        if si == 1: continue
        cols = 4; gp = 3; cw = (x1 - x0 - gp * (cols - 1)) / cols; ch = cw * 9 / 16
        for r_ in range(int((y1 - y0) / (ch + gp)) + 1):
            for k_ in range(cols):
                name, bg = POOL[(k_ * 7 + r_ * 3 + si * 11 + beat * 5) % len(POOL)]
                win(c, x0 + k_ * (cw + gp), y0 + r_ * (ch + gp), cw, ch, name, bg, '', 0.45)
    # the centre screen: her, trapped -- the cube, and the point cloud in it
    CX, CY, CS_ = 960, 268, 118
    rgba(c, INK, 1); c.rectangle(*STAGE_SCREENS[1][:2], STAGE_SCREENS[1][2] - STAGE_SCREENS[1][0], STAGE_SCREENS[1][3] - STAGE_SCREENS[1][1]); c.fill()
    for yy in range(STAGE_SCREENS[1][1], STAGE_SCREENS[1][3], 6): line(c, STAGE_SCREENS[1][0], yy, STAGE_SCREENS[1][2], yy, CYAN, 0.035, 1)
    ry, rx = 0.5 + 0.2 * (t - B(408)), -0.3
    V = [(x, y, z) for x in (-CS_, CS_) for y in (-CS_, CS_) for z in (-CS_, CS_)]
    Pp = [proj(*rot3(x, y, z, rx, ry), cx=CX, cy=CY) for (x, y, z) in V]
    edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count('1') == 1]
    rgba(c, BONE, 0.8); c.set_line_width(1.6)
    for a_, b_ in edges: c.move_to(Pp[a_][0], Pp[a_][1]); c.line_to(Pp[b_][0], Pp[b_][1])
    c.stroke()
    X, Y, col, rr, nn = alpha_points('n_floating_hd', 2600, 8)
    k_ = 0.195
    px = CX + (X - 961) * k_ + nn[:, 0] * 0.8; py = CY + (Y - 552) * k_ + nn[:, 1] * 0.8 + 3 * math.sin(t * 2)
    draw_points(c, px, py, CYAN, 0.85, 1.6)
    text(c, 'mono', 'me.isTrappedIn("love") == true', CX, 425, 13, CYAN, 0.8 * eo_cubic(prog(t, B(412), B(412.5))), align='center')
    pat = c.pop_group(); c.set_source(pat); c.mask_surface(surf('n_stage_screens'), 0, 0)
    c.restore()
    g.save(); cam(g)
    for si in (0, 2):
        x0, y0, x1, y1 = STAGE_SCREENS[si]; rgba(g, (1, 0.92, 0.8), 0.16 + 0.12 * pulse(t, B(beat), 0.3)); g.rectangle(x0, y0, x1 - x0, y1 - y0); g.fill()
    rgba(g, (1, 0.78, 0.9), 0.4 + 0.4 * pulse(t, B(beat), 0.35)); g.mask_surface(surf('n_stage_sticks'), 0, 0)
    g.restore()
    c.save(); cam(c); g.save(); cam(g)
    sway_sticks(c, g, t, 1.0, eo_cubic(prog(t, B(LOVE[3]) - 0.25, B(LOVE[3]))))
    c.restore(); g.restore()
    pts_g = [(CX + (x - 961) * k_, CY + (y - 552) * k_) for x, y in zip(X[::40], Y[::40])]
    g.save(); cam(g); draw_points(g, np.array([p[0] for p in pts_g]), np.array([p[1] for p in pts_g]), CYAN, 0.5, 2.5); g.restore()
    # the thread: from Ralmia's hand in the screen, a heart, down to Lishenna's hand
    A_ = T((CX + (FLOAT_HAND[0] - 961) * k_, CY + (FLOAT_HAND[1] - 552) * k_))
    B_ = T(STAGE_HAND)
    hs_ = 6.2 * (1 + 0.12 * pulse(t, B(LOVE[3]), 0.8)) * eo_back(prog(t, B(408), B(408) + 0.5))
    hc = (B_[0] + 250, (A_[1] + B_[1]) / 2 - 10)
    def hp(a_): return (hc[0] + hs_ * 16 * math.sin(a_) ** 3,
                        hc[1] - hs_ * (13 * math.cos(a_) - 5 * math.cos(2 * a_) - 2 * math.cos(3 * a_) - math.cos(4 * a_)))
    cusp, tip = hp(0.0), hp(math.pi)
    def bez(p0, p1, p2, n=24): return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
                                       (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in np.linspace(0, 1, n)]
    path = bez(A_, (A_[0] + 160, A_[1] - 20), cusp) + [hp(a_) for a_ in np.linspace(0, 2 * math.pi, 120)] + \
           [hp(a_) for a_ in np.linspace(0, math.pi, 60)] + bez(tip, (tip[0] - 40, B_[1] + 40), B_)[1:]
    red_line(c, g, path, 4.0, 0.4 + 0.6 * pulse(t, B(LOVE[3]), 1.0))
    if kk >= LOVE[3]:
        u = eo_cubic(prog(t, B(LOVE[3]), B(LOVE[3]) + 0.2))
        c.new_path(); fonts()['heavy'].text_path(c, 'LOVE', 960, 1000, 160, 'center', 0.3)
        rgba(c, INK, 0.85 * u); c.set_line_width(10); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        rgba(c, BONE, u * (1 - prog(t, B(415.6), B(416)))); c.fill()
    text(c, 'mono', 'you.isFree() == true', W - 130, 1000, 22, BONE, 0.7 * eo_cubic(prog(t, B(409.5), B(410))), align='right')
    fx['ab'] = 6 * pulse(t, B(LOVE[3]), 0.3) + 2 * pulse(t, B(math.floor(kk)), 0.12)
    fx['flash'] = 0.25 * pulse(t, B(LOVE[3]), 0.12)
    fx['glow'] = 1.0
    hud(c, t, True, a=0.5, log_a=0.8)
    return fx

# ================================================================ S34 me.escape(world)  [B416, END)
PEEL = [420, 424, 428, 432, 436]          # cube, windows, fragments, HUD marks, the frame -- one per bar
K_LEAP, K_GONE = 443.0, 443.55          # v2 round 2: half a beat -- she shoots up out of the frame, tearing the paper as she goes
def s_escape(c, g, t):
    """inside out, one layer per bar: the cube scatters, the window wall flies past, the fragments fall away,
    the HUD's corner marks are torn off, the frame cracks -- and behind the ink there is paper. from k443: escape_out()"""
    fx = {}
    kk = (t - T0) / P
    if kk >= K_LEAP: return escape_out(c, g, t)
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
            c.set_source_surface(surf(f'{FRAG_PREFIX}_{i:02d}'), 0, 0); c.paint_with_alpha(0.55 * (1 - v))
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
    # every beat a ring goes out from her (the drums carry the outro); streaks outward, more with every layer gone
    npeel = sum(1 for k in PEEL if kk >= k)
    if kk < K_LEAP:
        for kb in range(max(416, math.floor(kk) - 2), math.floor(kk) + 1):
            u = prog(t, B(kb), B(kb) + 1.4)
            if 0 < u < 1:
                for cc, aa in ((c, 0.5 if not paper else 0.7), (g, 0.35 if not paper else 0)):
                    rgba(cc, LISH_P if paper else CYAN, aa * (1 - u)); cc.set_line_width(2.5 * (1 - u) + 0.5)   # paper: her song
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
    if PEEL[0] <= kk:
        la = eo_cubic(prog(t, B(PEEL[0]), B(PEEL[0]) + 0.3))
        colour = clamp((kk - PEEL[0]) / (PEEL[4] - PEEL[0]))      # the colour comes in as the layers go
        s_ = hs
        gather = prog(t, B(440), B(K_LEAP))                       # three beats of gathering: she trembles
        xx = cx + 5 * gather * math.sin(t * 70)
        yy = cy - 14 * gather                                     # ...and crouches a little lower into it
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
    fx['ab'] = sum(6 * pulse(t, B(k), 0.25) for k in PEEL) + 2 * pulse(t, B(math.floor(kk)), 0.12)
    fx['flash'] = sum(0.25 * pulse(t, B(k), 0.1) for k in PEEL)
    if paper: fx['vig'] = 0.4; fx['grain'] = 0.03
    return fx


# ================================================================ v2 round 2: out of her world, towards the song  [B443, END)
# k443   she shoots up out of the frame; the paper of her world tears along the way she went
# k444   the tear opens: outside is warm light, and Lishenna's song comes in through it (she ran towards it this time)
# k446.5 the last EXECUTION: the two halves of her world fall away
# k448   the song stops. outside: the two of them, line first, then colour; touch = true; me.hum();
ENDING = next((n for n in ('n_ending_hd', 'n_cube_together_hd', 'n_pinky2_hd') if os.path.exists(f'{WORK}/assets/{n}.png')))
TEAR_X = 960
_TEAR = {}
def tear():
    if not _TEAR:
        r = np.random.default_rng(13)
        ys = np.linspace(-40, H + 40, 110)
        b = np.cumsum(r.normal(0, 7, len(ys))); b = b - b.mean() + TEAR_X + 26 * np.sin(ys / 230)
        zz = np.where(np.arange(len(ys)) % 2, 1.0, -1.0)            # torn fibres: a fine zigzag on each edge
        _TEAR.update(y=ys, b=b, jl=r.normal(0, 6, len(ys)) + 4 * zz, jr=r.normal(0, 6, len(ys)) - 4 * zz)
    return _TEAR

def tear_open(t):
    """per row: how far apart the two edges are"""
    T_ = tear(); ys = T_['y']
    kk = (t - T0) / P
    rise = ei_cubic(prog(t, B(K_LEAP), B(K_GONE)))
    top_y = 540 - 1500 * rise                                   # her head: the tear runs from 540 up to her
    down = eo_cubic(prog(t, B(K_GONE), B(444.3)))                # then it runs down to the bottom
    bot_y = 540 + (H + 60 - 540) * down
    w = 10 + 50 * eo_cubic(prog(t, B(K_GONE), B(444.2))) + 290 * eo_cubic(prog(t, B(444.2), B(FINAL_EX)))
    f = np.clip((bot_y - ys) / 140, 0, 1) * np.clip((ys - top_y) / 60 + 1, 0, 1) * (kk >= K_LEAP + 0.08)
    return ys, f * w, f

def paper_piece(c, side, ys, wy, f, dx=0.0, dy=0.0, rot=0.0):
    T_ = tear()
    edge = T_['b'] + (T_['jl'] if side < 0 else T_['jr']) * f + side * wy / 2
    piv = (TEAR_X - side * 480, 540)
    c.save(); c.translate(piv[0] + dx, piv[1] + dy); c.rotate(rot); c.translate(-piv[0], -piv[1])
    xo = -80 if side < 0 else W + 80
    def path(cc):
        cc.new_path(); cc.move_to(xo, ys[0])
        for x, y in zip(edge, ys): cc.line_to(x, y)
        cc.line_to(xo, ys[-1]); cc.close_path()
    path(c); c.save(); c.clip(); c.set_source_surface(paper_tex(), 0, 0); c.paint()
    rgba(c, SEPIA, 0.07); c.paint()                              # the old world, a little dimmer than the light outside
    c.restore()
    on = f > 0.02                                                # the torn edge, only where it is torn
    for dxe, col, aa, lw in ((-side * 5, SEPIA, 0.2, 8), (0, (1, 1, 0.97), 0.95, 3)):
        c.new_path(); started = False
        for x, y, o in zip(edge, ys, on):
            if o: (c.line_to if started else c.move_to)(x + dxe, y); started = True
            else: started = False
        rgba(c, col, aa); c.set_line_width(lw); c.stroke()
    c.restore()

def outside_light(c, g, a=1.0):
    rgba(c, (1.0, 0.985, 0.94), 1); c.paint()
    rg = cairo.RadialGradient(960, 520, 0, 960, 520, 900)
    rg.add_color_stop_rgba(0, 1, 1, 1, 0.55 * a); rg.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(rg); c.paint()

def escape_out(c, g, t):
    fx = {}
    kk = (t - T0) / P
    outside_light(c, g)
    fall = ei_cubic(prog(t, B(FINAL_EX), B(FINAL_EX) + 0.85))
    if fall < 1:
        ys, wy, f = tear_open(t)
        for side in (-1, 1):
            paper_piece(c, side, ys, wy, f, side * 760 * fall, 1000 * fall * fall, side * 0.28 * fall)
    # her song, coming in from outside through the tear (it opens at k444)
    for kb in np.arange(444.0, 448.5, 0.5):
        u = prog(t, B(kb), B(kb) + 1.6)
        if 0 < u < 1:
            r = 40 + 1300 * eo_cubic(u)
            for cc, aa, lw in ((c, 0.75 * (1 - u), 2.4 * (1 - u) + 0.8), (g, 0.4 * (1 - u), 4)):
                rgba(cc, LISH_P if cc is c else LISH, aa); cc.set_line_width(lw); cc.new_path(); cc.arc(TEAR_X, 540, r, 0, 6.283); cc.stroke()
    # her, shooting up out of the frame (half a beat), after-images and streaks below her
    rise = ei_cubic(prog(t, B(K_LEAP), B(K_GONE)))
    if rise < 1:
        hs = 0.30 + 5 * 0.035
        for k in (3, 2, 1):
            rk = max(0.0, rise - 0.08 * k)
            img(c, 'n_escape_hd', 960, 540 - 1500 * rk, hs * (1 + 0.15 * rk), 0.18, 1000, 540)
        rnd = np.random.default_rng(23); xs_ = 960 + rnd.normal(0, 160, 60); ln_ = rnd.random(60)
        for x, l in zip(xs_, ln_):
            y0 = 540 - 1500 * rise + 200 + 500 * l
            rgba(c, SEPIA, 0.3 * rise * (1 - rise)); c.set_line_width(1.5 + 2 * l); c.move_to(x, y0); c.line_to(x, y0 + 300 + 500 * l); c.stroke()
        img(c, 'n_escape_hd', 960, 540 - 1500 * rise, hs * (1 + 0.15 * rise), 1, 1000, 540)
    if B(K_GONE) <= t < B(FINAL_EX):                             # she is no longer in the world
        text(c, 'monom', type_on('world.getThingIndex(me);   // -1', t, B(K_GONE) + 0.1, 0.03), 470, 990, 26, SEPIA, 0.8, align='center')
    # the last EXECUTION
    if B(FINAL_EX) <= t < B(K_SILENCE) + 0.3:
        u = eo_expo(prog(t, B(FINAL_EX), B(FINAL_EX) + 0.14)) * (1 - prog(t, B(K_SILENCE), B(K_SILENCE) + 0.3))
        c.save(); c.translate(960, 640); s2 = 1.25 - 0.25 * eo_expo(prog(t, B(FINAL_EX), B(FINAL_EX) + 0.14)); c.scale(s2, s2)
        c.new_path(); fonts()['heavy'].text_path(c, 'EXECUTION', 0, 0, 330, 'center')
        rgba(c, (1, 0.985, 0.94), 0.9 * min(1, u * 2)); c.set_line_width(16); c.stroke_preserve()
        rgba(c, INK, min(1, u * 2)); c.fill(); c.restore()
    # outside, after the song: the two of them
    if t >= B(K_SILENCE):
        ts = t - B(K_SILENCE)
        la = eo_cubic(prog(ts, 0.25, 0.9)); col_ = eo_cubic(prog(ts, 0.9, 2.2))
        sc = 1.0 if ENDING == 'n_pinky2_hd' else 0.94
        c.save(); c.translate(960, 540); c.scale(sc * (1 + 0.012 * ts), sc * (1 + 0.012 * ts)); c.translate(-960, -540)
        rgba(c, SEPIA, la * (1 - col_ * 0.85)); c.mask_surface(surf(ENDING.replace('_hd', '_line')), 0, 0)
        c.set_source_surface(surf(ENDING), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(col_)
        c.restore()
        u = eo_cubic(prog(ts, 2.4, 2.9))
        if int(ts * 1.6) % 2 == 0 and ts > 2.2:
            rgba(c, SEPIA, 0.8); c.rectangle(130, 990 - 30, 16, 30); c.fill()
        text(c, 'mono', 'touch = true', 170, 990, 26, RED, 0.9 * u)
        uh = prog(ts, 3.2, 3.6)
        if uh > 0:
            text(c, 'mono', type_on('me.hum();', t, B(K_SILENCE) + 3.2, 0.05), 170, 1030, 20, SEPIA, 0.6)
            reach = prog(ts, 3.5, 4.6)
            for cc, aa, lw in ((c, 0.8, 1.4), (g, 0.3, 3)):
                rgba(cc, LISH_P if cc is c else LISH, aa); cc.set_line_width(lw); cc.new_path()
                for n_ in range(0, 161):
                    if n_ / 160 > reach: break
                    x = 300 + 360 * n_ / 160
                    e = math.sin(math.pi * n_ / 160) * (0.6 + 0.4 * math.sin(t * 1.3 + n_ * 0.05))
                    (cc.move_to if n_ == 0 else cc.line_to)(x, 1023 - 5 * e * math.sin(n_ * 0.28 - t * 2.2))
                cc.stroke()
    fx['ab'] = 10 * pulse(t, B(K_LEAP), 0.25) + 5 * pulse(t, B(K_GONE), 0.2) + 10 * pulse(t, B(FINAL_EX), 0.3)
    fx['flash'] = 0.35 * pulse(t, B(K_GONE), 0.12) + 0.4 * pulse(t, B(FINAL_EX), 0.12)
    fx['vig'] = 0.3; fx['grain'] = 0.03; fx['glow'] = 0.6
    return fx
