"""world.execute(me); x Ralmia — Act IV "execution" (133.26–162.80 s).
EXECUTION x12 on every second beat k288..310 (needs an ears-on check: the chant is too dense for Whisper);
the count EIN DOS TROIS NE FEM LIU on a dotted-8th grid k325.5 .. 329.25, EXECUTION k330; then the thread pulls (k340)
and she crouches to launch (k344-352) into the third chorus."""
from scenes5 import *

EXE = [288 + 2 * i for i in range(12)]
COUNT = [325.5 + 0.75 * i for i in range(6)]
K_EX13, K_PULL, K_LAUNCH = 330.0, 340.0, 344.0

# ================================================================ S26 TWELVE EXECUTIONS  [B288, B320)
WIN_W, WIN_H, WIN_SP = 470, 264, 540
RUN_X, TOP_Y = 560, 640
VEL = WIN_SP / (2 * P)
def win_cx(i, t): return 20 + WIN_SP * i - VEL * (t - B(288))
def win_src(i):
    if i == 12: return ('n_pinky_hd', None, 'sim #0001  ·  you & me')
    name, bg = POOL[(i * 5 + 2) % len(POOL)]
    return (name, bg, f'sim #{2 + i * 37:04d}')

def platform(c, g, i, t):
    cx = win_cx(i, t)
    if cx < -WIN_W or cx > W + WIN_W: return
    name, bg, lab = win_src(i)
    x, y = cx - WIN_W / 2, TOP_Y
    tc = B(EXE[i]) if i < 12 else B(312)
    dt = t - tc
    if dt < 0.12:
        win(c, x, y, WIN_W, WIN_H, name, bg, lab, 1.0, pan=0)
        if dt >= 0:
            rgba(c, BONE, 1 - dt / 0.12); c.rectangle(x, y, WIN_W, WIN_H); c.fill()
        return
    # executed: a stamp, then six slats fall away
    rr = random.Random(i * 17)
    for k in range(6):
        d0 = 0.12 + rr.random() * 0.12
        u = max(0.0, dt - d0)
        dy = 0.5 * 3200 * u * u; rot = (rr.random() - 0.5) * 2.4 * u
        if dy > H: continue
        sx = x + k * WIN_W / 6
        c.save(); c.translate(sx + WIN_W / 12, y + WIN_H / 2 + dy); c.rotate(rot); c.translate(-(sx + WIN_W / 12), -(y + WIN_H / 2))
        c.rectangle(sx, y, WIN_W / 6 + 0.5, WIN_H); c.clip()
        win(c, x, y, WIN_W, WIN_H, name, bg, 'EXECUTED', 1.0)
        rgba(c, INK, min(0.7, u * 3)); c.rectangle(x, y, WIN_W, WIN_H); c.fill()
        c.restore()
    if dt < 0.6:
        a_ = 1 - prog(t, tc + 0.35, tc + 0.6)
        c.save(); c.translate(cx, y + WIN_H / 2); c.rotate(-0.12)
        c.new_path(); fonts()['heavy'].text_path(c, 'EXECUTED', 0, 26, 76, 'center')
        rgba(c, INK, 0.9 * a_); c.set_line_width(8); c.stroke_preserve(); rgba(c, BONE, a_); c.fill()
        c.restore()

def runner(c, g, t, x, top):
    """her bounding run: one stride per beat, airborne in the first half"""
    ph = ((t - T0) / P) % 1.0
    if ph < 0.55:
        bob = -120 * math.sin(math.pi * ph / 0.55)
        name, ax, ay, sc = 'n_dash_full_hd', 986, 976, 0.33
    else:
        bob = 0; name, ax, ay, sc = 'n_dash_launch_hd', 980, 943, 0.36
    img(c, name, x, top - 6 + bob, sc, 1, ax, ay)
    rgba(g, CYAN, 0.10 if ph < 0.55 else 0.05); g.save(); g.translate(x, top - 6 + bob); g.scale(sc, sc); g.translate(-ax, -ay); g.mask_surface(surf(name), 0, 0); g.restore()
    return top - 6 + bob

# ---- the corridor: she runs straight at us down an avenue of worlds; each EXECUTION kills the one she is passing
VPX, VPY, KZ = 960, 430, 1150
VZ = 3.0 / (2 * P)                       # depth units per second: one main window every two beats
def zpos(tc, t): return 3.2 + (tc - t) * VZ
DEAD = [(288 - 8 + j * 0.5, (-1 if j % 2 else 1), -0.75 + 1.0 * random.Random(j * 13).random(), j) for j in range(66)]

def cwin(c, g, t, tc, side, Y, name, bg, lab, size=1.0, dim=1.0, executed_at=None, key=0):
    z = zpos(tc, t)
    if z < 0.3 or z > 15: return
    s = KZ / z; w = size * s; h = w * 9 / 16
    cx = VPX + side * 1.45 * s; cy = VPY + Y * s
    x, y = cx - w / 2, cy - h / 2
    fog = clamp((15 - z) / 6) * dim
    ex = executed_at
    if ex == -1:                                         # long dead: a dark pane with its stamp
        win(c, x, y, w, h, name, bg, lab, fog)
        rgba(c, INK, 0.55 * fog); c.rectangle(x, y, w, h); c.fill()
        c.save(); c.translate(cx, cy); c.rotate(-0.12)
        text(c, 'heavy', 'EXECUTED', 0, w * 0.05, w * 0.14, BONE, 0.6 * fog, align='center'); c.restore()
        return
    if ex is None or t < ex:
        win(c, x, y, w, h, name, bg, lab, fog)
        return
    dt = t - ex
    if dt < 0.12:
        win(c, x, y, w, h, name, bg, lab, fog)
        rgba(c, BONE, fog * (1 - dt / 0.12)); c.rectangle(x, y, w, h); c.fill()
        rgba(g, BONE, 0.6 * (1 - dt / 0.12)); g.rectangle(x, y, w, h); g.fill()
        return
    rr = random.Random(key * 17)
    for k in range(6):                                  # six slats fall away
        u = max(0.0, dt - 0.12 - rr.random() * 0.12)
        dy = 0.5 * 2600 * u * u * (s / 480); rot = (rr.random() - 0.5) * 2.4 * u
        if y + dy > H + 50: continue
        sx = x + k * w / 6
        c.save(); c.translate(sx + w / 12, y + h / 2 + dy); c.rotate(rot); c.translate(-(sx + w / 12), -(y + h / 2))
        c.rectangle(sx, y, w / 6 + 0.5, h); c.clip()
        win(c, x, y, w, h, name, bg, 'EXECUTED', fog)
        rgba(c, INK, min(0.7, u * 3) * fog); c.rectangle(x, y, w, h); c.fill()
        c.restore()
    if dt < 0.6:
        a_ = (1 - prog(t, ex + 0.35, ex + 0.6)) * fog
        c.save(); c.translate(cx, cy); c.rotate(-0.12)
        c.new_path(); fonts()['heavy'].text_path(c, 'EXECUTED', 0, w * 0.06, w * 0.16, 'center')
        rgba(c, INK, 0.9 * a_); c.set_line_width(w * 0.016); c.stroke_preserve(); rgba(c, BONE, a_); c.fill()
        c.restore()

def her_run(c, g, t, a=1.0):
    ph = ((t - T0) / P) % 1.0
    bob = -22 * abs(math.sin(math.pi * ph)); sway = 16 * math.sin(math.pi * (t - T0) / P); rot = 0.025 * math.sin(math.pi * (t - T0) / P)
    for k, (ss, aa) in enumerate(((0.80, 0.07), (0.88, 0.14))):     # after-images, trailing back toward the vanishing point
        img(c, 'n_run_front_hd', lerp(960 + sway, VPX, 1 - ss) , lerp(1110 + bob, VPY + 300, 1 - ss), 0.62 * ss, aa * a, 957, 1061, rot)
    img(c, 'n_run_front_hd', 960 + sway, 1110 + bob, 0.62, a, 957, 1061, rot)
    g.save(); g.translate(960 + sway, 1110 + bob); g.rotate(rot); g.scale(0.62, 0.62); g.translate(-957, -1061)
    rgba(g, CYAN, 0.07 * a); g.mask_surface(surf('n_run_front_hd'), 0, 0); g.restore()

def s_executions(c, g, t):
    fill_bg(c, INK)
    fx = {}
    kk = (t - T0) / P
    if t < B(312):
        # floor lines rushing at us, rails to the vanishing point, radial speed streaks
        off = (t * VZ) % 1.0
        for n_ in range(1, 15):
            z = n_ - off
            if z < 0.4: continue
            y = VPY + 0.62 * KZ / z
            line(c, 0, y, W, y, BONE, 0.16 * (1 - z / 15), 1 + 1.5 / z)
        for sx in (-1, 1):
            line(c, VPX, VPY, VPX + sx * 2200, VPY + 0.62 * KZ / 0.5, BONE, 0.18, 1.2)
        rnd = np.random.default_rng(12); ang = rnd.random(110) * 6.283; ph = rnd.random(110)
        for a_, p_ in zip(ang, ph):
            f = (t * 0.9 + p_) % 1.0
            r0, r1 = 120 + 1500 * f ** 2, 120 + 1500 * min(1, f + 0.12) ** 2
            rgba(c, BONE, 0.10 + 0.25 * f); c.set_line_width(1 + 2 * f)
            c.move_to(VPX + math.cos(a_) * r0, VPY + math.sin(a_) * r0 * 0.7); c.line_to(VPX + math.cos(a_) * r1, VPY + math.sin(a_) * r1 * 0.7); c.stroke()
        for k in EXE[3::4]:                        # every 4th call: a huge backdrop word at the far end
            if B(k) <= t < B(k + 2):
                u = eo_expo(prog(t, B(k), B(k) + 0.2)); a_ = 1 - prog(t, B(k + 1), B(k + 2))
                text(c, 'heavy', 'EXECUTION', VPX, VPY + 120, 360 * (1.1 - 0.1 * u), BONE, 0.14 * a_, align='center')
                text(g, 'heavy', 'EXECUTION', VPX, VPY + 120, 360, CYAN, 0.3 * pulse(t, B(k), 0.5), align='center')
        items = []
        for (kb, side, Y, j) in DEAD:                       # worlds already dead, lining the avenue
            tc = B(kb); z = zpos(tc, t)
            name, bg = POOL[(j * 3 + 1) % len(POOL)]
            items.append((z, ('d', tc, side, Y, name, bg, j)))
        for i in range(13):                                  # the twelve, and then the first one: you & me
            tc = B(EXE[i]) if i < 12 else B(312)
            name, bg, lab = win_src(i)
            side = 0 if i == 12 else (-1 if i % 2 == 0 else 1)
            items.append((zpos(tc, t), ('m', tc, side, -0.12 if i < 12 else -0.2, name, bg, i, lab)))
        items.sort(key=lambda it: -it[0])
        def draw(it):
            kind = it[1]
            if kind[0] == 'd':
                _, tc, side, Y, name, bg, j = kind
                cwin(c, g, t, tc, side * (1.2 + 0.5 * random.Random(j).random()), Y, name, bg, 'EXECUTED', 0.75, 0.5, executed_at=-1, key=100 + j)
            else:
                _, tc, side, Y, name, bg, i, lab = kind
                cwin(c, g, t, tc, side, Y, name, bg, lab, 1.15 if i == 12 else 1.0, 1.0, executed_at=tc, key=i)
        for it in items:
            if it[0] >= 1.0: draw(it)
        her_run(c, g, t)
        for it in items:
            if it[0] < 1.0: draw(it)
        n = sum(1 for k in EXE if kk >= k)
        for k in EXE:
            if kk >= k and kk < k + 2:
                slam_word(c, g, 'EXECUTION', t, B(k), 1300, 190, 100, until=B(k + 2), glow=0.3)
        text(c, 'monom', f'world.runExecution();   x {n:2d} / 12', W - 130, 1000, 24, CYAN, 0.9, align='right', track=0.05)
        text(c, 'mono', f'MACH {1.2 + 0.15 * n:4.2f}', 130, 1000, 26, BONE, 0.7, track=0.15)
        fx['ab'] = sum(5 * pulse(t, B(k), 0.25) for k in EXE) + 2 * pulse(t, B(math.floor(kk)), 0.15)
        fx['flash'] = sum((0.3 if EXE.index(k) % 4 == 3 else 0.1) * pulse(t, B(k), 0.08) for k in EXE)
        hud(c, t, True, a=0.6, log_a=0.85)
        return fx
    n = 12
    if True:
        # the last world -- the first one, the two of them -- goes under her, and she falls
        dt = t - B(312)
        # behind her: the twelve executed worlds, a wall of dead windows receding
        uw = eo_cubic(prog(t, B(312.5), B(314)))
        zs = lerp(1.25, 0.8, eio_cubic(prog(t, B(312.5), B(320))))
        aw = uw * (1 - prog(t, B(319), B(320)))
        if aw > 0:
            ww, wh, gp = 380 * zs, 214 * zs, 22 * zs
            for i in range(12):
                r_, c_ = divmod(i, 4)
                x = 960 + (c_ - 1.5) * (ww + gp) - ww / 2; y = 520 + (r_ - 1) * (wh + gp) - wh / 2
                name, bg, lab = win_src(i)
                win(c, x, y, ww, wh, name, bg, lab, 0.35 * aw)
                rgba(c, INK, 0.55 * aw); c.rectangle(x, y, ww, wh); c.fill()
                c.save(); c.translate(x + ww / 2, y + wh / 2); c.rotate(-0.12)
                text(c, 'heavy', 'EXECUTED', 0, 18 * zs, 54 * zs, BONE, 0.55 * aw, align='center'); c.restore()
            text(c, 'thin', '12 / 12', 960, 990, 90, BONE, 0.8 * aw, align='center', track=0.3)
        if dt < 0.45:                                          # the last window, you & me, coming apart in front of her
            name, bg, lab = win_src(12)
            cwin(c, g, t, B(312), 0, -0.2, name, bg, lab, 1.15, 1.0, executed_at=B(312), key=12)
        drop = eo_cubic(prog(t, B(312), B(313.5)))             # she stops dead, lifts off, and hangs there turning in front of the dead wall
        y = lerp(860, 640, drop) + 40 * max(0, dt - 0.7)
        x = 960
        a_ = 1 - prog(t, B(318.5), B(320))
        img(c, 'n_floating_hd', x, y, lerp(0.42, 0.55, prog(t, B(312), B(320))), a_, 961, 552, rot=0.9 * dt + 0.6)
    # readouts
    for k in EXE:
        if kk >= k and kk < k + 2:
            slam_word(c, g, 'EXECUTION', t, B(k), 1300, 190, 100, until=B(k + 2), glow=0.3)
    text(c, 'monom', f'world.runExecution();   x {n:2d} / 12', W - 130, 1000, 24, CYAN, 0.9, align='right', track=0.05)
    m = 1.2 + 0.15 * n
    text(c, 'mono', f'MACH {m:4.2f}', 130, 1000, 26, BONE, 0.7, track=0.15)
    fx['ab'] = sum(5 * pulse(t, B(k), 0.25) for k in EXE) + 6 * pulse(t, B(312), 0.3)
    fx['flash'] = sum((0.35 if EXE.index(k) % 4 == 3 else 0.12) * pulse(t, B(k), 0.08) for k in EXE)
    hud(c, t, True, a=0.6, log_a=0.85)
    return fx

# ================================================================ S27 THE COUNT + THE PULL + THE LAUNCH  [B320, B352)
HEX_C = (960, 560); HEX_R = 360
WORDS = [('EINS', 'bold', 'de'), ('DOS', 'bold', 'es'), ('TROIS', 'bold', 'fr'), ('넷', 'cjk', 'kr'), ('FEM', 'bold', 'se'), ('六', 'cjk', 'cn')]
def hexv(i, r=HEX_R):
    a = math.radians(60 * i)
    return HEX_C[0] + r * math.sin(a), HEX_C[1] - r * math.cos(a)

def thread_tail(t, origin, hang_len, sway_ph, taut=0.0, target=(W + 60, 300)):
    """polyline of a loose thread end hanging from origin; taut 0..1 pulls it straight towards target"""
    pts = []
    for s in np.linspace(0, 1, 40):
        sw = math.sin(t * 1.7 + sway_ph + s * 2.2) * 10 * s
        hx, hy = origin[0] + 40 * s * s + sw, origin[1] + hang_len * s
        tx, ty = lerp(origin[0], target[0], s), lerp(origin[1], target[1], s)
        pts.append((lerp(hx, tx, taut), lerp(hy, ty, taut)))
    return pts

def s_count(c, g, t):
    fx = {}
    kk = (t - T0) / P
    if t < B(332):
        fill_bg(c, INK)
        dotgrid(c, BONE, 0.04)
        close = eio_cubic(prog(t, B(330.5), B(331.75)))
        R = HEX_R * lerp(1, 0.55, close)
        # her, adrift in the dark after the fall
        dy = lerp(160, 0, eo_cubic(prog(t, B(320), B(325))))
        img(c, 'n_floating_hd', HEX_C[0], HEX_C[1] + dy, 0.36, eo_cubic(prog(t, B(320), B(321.5))), 961, 552,
            rot=0.15 * (t - B(320)) + 2.0)
        # faint vertices waiting
        ua = eo_cubic(prog(t, B(321), B(323)))
        for i in range(6):
            x, y = hexv(i, R); rgba(c, BONE, 0.25 * ua); c.arc(x, y, 4, 0, 6.283); c.fill()
        # edges, card by card
        for i in range(6):
            if t < B(COUNT[i]): continue
            if i > 0:
                ue = eo_cubic(prog(t, B(COUNT[i]), B(COUNT[i]) + 0.18))
                (xa, ya), (xb, yb) = hexv(i - 1, R), hexv(i, R)
                for cc, aa in ((c, 0.9), (g, 0.5)): line(cc, xa, ya, lerp(xa, xb, ue), lerp(ya, yb, ue), CYAN, aa, 2.5)
        if t >= B(K_EX13):
            (xa, ya), (xb, yb) = hexv(5, R), hexv(0, R)
            ue = eo_cubic(prog(t, B(K_EX13), B(K_EX13) + 0.12))
            for cc, aa in ((c, 0.9), (g, 0.5)): line(cc, xa, ya, lerp(xa, xb, ue), lerp(ya, yb, ue), CYAN, aa, 2.5)
            # the hexagon fills with the shield cells from 2.3 s: this time a cage
            c.save(); c.new_path()
            for i in range(6): (c.move_to if i == 0 else c.line_to)(*hexv(i, R))
            c.close_path(); c.clip()
            Rc, cells = hex_cells()
            fl = pulse(t, B(K_EX13), 0.6)
            for (x, y, d, rr) in cells:
                X, Y = HEX_C[0] + (x - 960) * lerp(1, 0.55, close), HEX_C[1] + (y - 560) * lerp(1, 0.55, close)
                c.new_path(); hexpath(c, X, Y, Rc * 0.92 * lerp(1, 0.55, close))
                rgba(c, CYAN, 0.10 + 0.3 * fl); c.fill_preserve(); rgba(c, CYAN, 0.5); c.set_line_width(1.2); c.stroke()
            c.restore()
            slam_word(c, g, 'EXECUTION', t, B(K_EX13), 960, 600, 220, glow=0.8)
        # the six cards
        for i, kb in enumerate(COUNT):
            if t < B(kb): continue
            u = eo_expo(prog(t, B(kb), B(kb) + 0.14))
            x, y = hexv(i, lerp(HEX_R + 40, R + 40 * (1 - close), 1))
            wd, key, code = WORDS[i]
            c.save(); c.translate(x, y); s_ = (1.25 - 0.25 * u) * lerp(1, 0.6, close); c.scale(s_, s_)
            text(c, 'heavy', str(i + 1), 0, 10, 130, BONE, u, align='center')
            text(c, key, wd, 0, 76, 52 if key == 'bold' else 46, BONE, u, align='center', track=0.1 if key == 'bold' else 0)
            text(c, 'mono', code, 0, 112, 20, CYAN, 0.9 * u, align='center', track=0.3)
            c.restore()
            p_ = pulse(t, B(kb), 0.4)
            if p_ > 0.02: text(g, 'heavy', str(i + 1), x, y + 10, 130, CYAN, 0.6 * p_, align='center')
        fx['ab'] = sum(4 * pulse(t, B(k), 0.2) for k in COUNT) + 7 * pulse(t, B(K_EX13), 0.3)
        fx['flash'] = 0.3 * pulse(t, B(K_EX13), 0.1) + 0.7 * ei_cubic(prog(t, B(331.6), B(332)))
        hud(c, t, True, a=0.55, log_a=0.85)
        return fx
    if t < B(K_LAUNCH):
        # the loose end of the red thread, still on her little finger. at k340 it is pulled taut -- towards him
        paper_bg(c)
        KN = (957, 510)
        s_ = 1.0 + 0.22 * eio_cubic(prog(t, B(332), B(K_PULL))) + 0.04 * prog(t, B(K_PULL), B(K_LAUNCH))
        T = lambda p: (KN[0] + (p[0] - KN[0]) * s_ + 40 * (1 - s_), KN[1] + (p[1] - KN[1]) * s_)
        smear = prog(t, B(343.5), B(K_LAUNCH))
        for k in range(1 if smear <= 0 else 6):
            img(c, 'n_pinky_alone_clean', T((960, 540))[0] + k * 70 * smear, T((960, 540))[1], s_, 1 if k == 0 else 0.25)
        tr = (B(338) <= t < B(K_PULL)) * prog(t, B(338), B(K_PULL))
        taut = eo_back(prog(t, B(K_PULL), B(K_PULL) + 0.25), 1.2)
        twang = 14 * math.exp(-max(0, t - B(K_PULL) - 0.2) * 4) * (t > B(K_PULL) + 0.2)
        for idx, (ln_, ph) in enumerate(((110, 0.0), (190, 1.3))):
            pts = thread_tail(t, (960, 522), ln_, ph, taut if idx == 1 else 0.0)
            for cc, aa, lw in ((c, 1, 4.2), (g, 0.25 + 0.6 * taut * (idx == 1), 7)):
                rgba(cc, RED, aa); cc.set_line_width(lw * s_); cc.set_line_cap(cairo.LINE_CAP_ROUND); cc.new_path()
                for n_, p in enumerate(pts):
                    x, y = T(p)
                    if idx == 1:
                        x += (random.Random(int(t * 60) + n_).random() - 0.5) * 6 * tr
                        y += twang * math.sin(n_ / 39 * math.pi * 3) * math.sin(t * 70)
                    (cc.move_to if n_ == 0 else cc.line_to)(x, y)
                cc.stroke()
            c.set_line_cap(cairo.LINE_CAP_BUTT); g.set_line_cap(cairo.LINE_CAP_BUTT)
            if idx == 1 and t < B(K_PULL):              # a heartbeat runs down the loose end on every beat: something is still on the line
                kb_ = math.floor((t - T0) / P)
                if kb_ >= 333:
                    u = prog(t, B(kb_), B(kb_) + 0.45)
                    if u < 1:
                        n_ = int(u * 39); x, y = T(pts[n_])
                        for cc, aa, r in ((c, 0.9, 6), (g, 0.8, 14)):
                            rgba(cc, RED if cc is g else BONE, aa * (1 - u)); cc.arc(x, y, r * s_, 0, 6.283); cc.fill()
        if t >= B(K_PULL):
            u = eo_cubic(prog(t, B(K_PULL) + 0.1, B(K_PULL) + 0.35))
            text(c, 'monom', 'you.setExecution(me.toExecution());', 1840, 980, 26, SEPIA, u, align='right')
            text(c, 'mono', '// he is still out there', 1840, 1020, 20, SEPIA, 0.7 * u, align='right')
        fx['ab'] = 6 * pulse(t, B(K_PULL), 0.3) + 8 * smear
        fx['flash'] = 0.4 * (1 - prog(t, B(332), B(332) + 0.2)) ** 2
        fx['vig'] = 0.4; fx['grain'] = 0.03
        hud(c, t, False, a=0.5, log_a=0.85)
        return fx
    # the launch: eight beats of charge
    fill_bg(c, INK)
    gy = 860
    line(c, 0, gy, W, gy, BONE, 0.6, 2)
    ruler(c, gy, 40, W - 40, BONE, 0.8, B(K_LAUNCH), t)
    beats_in = kk - K_LAUNCH
    sc = lerp(0.6, 0.68, eio_cubic(prog(t, B(K_LAUNCH), B(352))))
    sx = 760
    shake = 2 * prog(t, B(348), B(352)) * math.sin(t * 80)
    img(c, 'n_dash_launch_hd', sx + shake, gy, sc, 1, 980, 943)
    ch = clamp(beats_in / 8)
    g.save(); g.translate(sx + shake, gy); g.scale(sc, sc); g.translate(-980, -943)
    rgba(g, CYAN, 0.05 + 0.18 * ch + 0.12 * pulse(t, B(math.floor(kk)), 0.3)); g.mask_surface(surf('n_dash_launch_hd'), 0, 0); g.restore()
    # particles drawn into her thrusters
    th = (sx + (700 - 980) * sc, gy + (560 - 943) * sc)
    rnd = np.random.default_rng(21); ang = rnd.random(260) * 6.283; ph = rnd.random(260)
    f = ((t * (0.8 + 1.6 * ch) + ph) % 1.0)
    r = (1 - f) * 900
    X, Y = th[0] + np.cos(ang) * r, th[1] + np.sin(ang) * r * 0.6
    draw_points(c, X, Y, CYAN, 0.6 * ch + 0.2, 3)
    # the thread from her hand, out to the right edge: still taut
    hx, hy = sx + (1460 - 980) * sc, gy + (450 - 943) * sc
    for cc, aa, lw in ((c, 1, 4), (g, 0.6, 7)):
        rgba(cc, RED, aa); cc.set_line_width(lw); cc.move_to(hx, hy); cc.line_to(W + 40, hy - 160); cc.stroke()
    # countdown squares
    for i in range(8):
        on = beats_in >= i
        x = 960 - 4 * 46 + i * 46
        rgba(c, CYAN if on else BONE, 1 if on else 0.3); c.set_line_width(1.5)
        c.rectangle(x, 960, 30, 30); c.fill() if on else c.stroke()
    text(c, 'mono', f'ignition   t - {max(0, 8 - math.floor(beats_in)):d}', 960, 1030, 22, BONE, 0.8, align='center', track=0.2)
    if t >= B(350):
        u = prog(t, B(350), B(352))
        rnd = np.random.default_rng(4); ys = rnd.random(120) * H; sp_ = rnd.random(120)
        for y, s_ in zip(ys, sp_):
            xx = W - ((t * (2000 + 4000 * s_) * u + s_ * 3000) % (W + 800))
            rgba(c, BONE, 0.3 * u); c.set_line_width(1 + 2 * s_); c.move_to(xx, y); c.line_to(xx + 300 + 900 * s_ * u, y); c.stroke()
    fx['ab'] = 2 * pulse(t, B(math.floor(kk)), 0.2) + 6 * prog(t, B(350), B(352))
    fx['flash'] = 0.25 * pulse(t, B(K_LAUNCH), 0.1) + 0.95 * ei_cubic(prog(t, B(351.25), B(352)))
    fx['glow'] = 1.0
    hud(c, t, True, a=0.6, log_a=0.85)
    return fx
