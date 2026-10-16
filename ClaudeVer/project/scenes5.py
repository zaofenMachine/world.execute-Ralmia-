"""world.execute(me); x Ralmia — Act III "losing" (103.72–133.26 s): chorus 2 + bridge.
Lyric beats (small.en + prompt, then snapped; marked ~ in plan_full.md):
VIBRATIONS k229.5 · COMPLETION k238.25 · "you have left" x6 k240 242.5 244.5 246.25 248.5 250.5 · ISOLATION k253
FRAGMENTS k262.75 · DISHEARTENED k270.5 · "Challenging your God" k272.5 · "you have made some" k278 · ILLEGAL k283 · ARGUMENTS k285"""
from scenes4 import *

K_VIB, K_COMP, K_ISO = 229.5, 238.25, 253.0
LEFT = [240.0, 242.5, 244.5, 246.25, 248.5, 250.5]
K_FRAG, K_DISH, K_GOD, K_SOME, K_ILL, K_ARG = 262.75, 270.5, 272.5, 278.0, 283.0, 285.0

def img(c, name, x, y, sc=1.0, a=1.0, ax=960, ay=540, rot=0.0):
    """draw assets/<name> with its point (ax, ay) placed at (x, y), scaled by sc"""
    if a <= 0.003: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc); c.translate(-ax, -ay)
    c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(min(1, a)); c.restore()

_AP = {}
def alpha_points(name, n=2600, seed=8):
    """random points inside an RGBA asset (canvas coords) + their colours"""
    if name not in _AP:
        im = cv2.imread(f'{WORK}/assets/{name}.png', cv2.IMREAD_UNCHANGED)
        ys, xs = np.nonzero(im[..., 3] > 160); r = np.random.default_rng(seed); idx = r.choice(len(xs), n, replace=False)
        col = im[ys[idx], xs[idx], :3][:, ::-1] / 255.0
        _AP[name] = (xs[idx].astype(np.float32), ys[idx].astype(np.float32), col, r.random(n), r.normal(0, 1, (n, 2)))
    return _AP[name]

# where things stand in the finished 12 s world (L4 parallax at t_ref = end of that shot)
WREF = B(28) - 0.01
def wxf(x, y, push=1.0):
    pan = 34 * (WREF - B(24.5)); zoom = (1.035 + 0.02) * push
    return 960 - pan + (x - 960) * zoom, 540 + (y - 540) * zoom, zoom
HIM_AT = (515, 842)            # beside her on the ledge (L4 coords); she stands at ~ (648, 836)
WALK_FEET = (985, 1050); WALK_H = 1022     # n_creator_walk canvas: feet, figure height
WALK_PINKY = (800, 560)

def him_in_world(c, push, a=1.0, h=250):
    X, Y, z = wxf(*HIM_AT, push)
    img(c, 'n_creator_walk_hd', X, Y, h / WALK_H * z, a, *WALK_FEET)
    return X, Y, h / WALK_H * z

def ecg(tt):
    """his heartbeat: lub on the beat, dub on the 16th after"""
    if tt < B(224): return 0.0
    f = ((tt - T0) / P) % 1.0
    return (70 * math.exp(-((f - 0.02) / 0.012) ** 2) - 24 * math.exp(-((f - 0.055) / 0.016) ** 2)
            + 34 * math.exp(-((f - 0.27) / 0.014) ** 2) - 10 * math.exp(-((f - 0.30) / 0.016) ** 2))

# ================================================================ S24 CHORUS 2  [B224, B256)
def s_chorus2(c, g, t):
    fx = {}
    kk = (t - T0) / P
    if t < B(232):
        # A — VIBRATIONS: she listens; his heartbeat and her wave converge into one line
        paper_bg(c)
        img(c, 'n_listen_hd', 960, 540, 1.0 + 0.05 * eio_cubic(prog(t, B(224), B(232))))
        rgba(c, PAPER, 0.8); c.rectangle(0, 880, W, 160); c.fill()
        merge = eio_cubic(prog(t, B(227.5), B(K_VIB)))
        pen = 1560; spd = 760
        for who in (0, 1):
            base = 960 + (36 if who == 0 else -36) * (1 - merge)
            for cc, aa, lw in ((c, 1, 2.6), (g, 0.55 if who else 0.0, 4)):
                if aa <= 0: continue
                rgba(cc, SEPIA if who == 0 else CYAN, aa); cc.set_line_width(lw); cc.new_path()
                for s in range(0, 241):
                    x = pen * s / 240; tt = t - (pen - x) / spd
                    v = ecg(tt) if who == 0 else 16 * math.sin(2 * math.pi * 4.33 * tt) * (0.5 + 0.5 * prog(tt, B(224), B(K_VIB)))
                    if who == 1 and tt >= B(K_VIB): v = ecg(tt) + 22 * math.sin(2 * math.pi * 4.33 * tt)
                    (cc.move_to if s == 0 else cc.line_to)(x, base - v)
                cc.stroke()
            if t < B(K_VIB):
                text(c, 'mono', 'you' if who == 0 else 'me', pen + 18, base + 6, 20, SEPIA if who == 0 else CYAN, 0.8)
        rgba(c, SEPIA, 1); c.arc(pen, 960 - ecg(t), 6, 0, 6.283); c.fill()
        words(c, 'serif', [('If', 103.72), ('I', 103.92), ('can,', 104.32), ('if', 104.74), ('I', 104.86), ('can', 105.22),
                           ('feel', 105.46), ('your', 105.76)], t, 1180, 380, 64, SEPIA, 0.95)
        if t >= B(K_VIB):
            slam_word(c, g, 'VIBRATIONS', t, B(K_VIB), 1180, 560, fit_size('bold', 'VIBRATIONS', 640, 170), key='bold',
                      col=INK, align='left', ol=PAPER, glow=0.5)
        fx['ab'] = 5 * pulse(t, B(K_VIB), 0.25) + 1.5 * pulse(t, B(math.floor(kk)), 0.12)
        fx['vig'] = 0.4; fx['grain'] = 0.03
        hud(c, t, False, a=0.6, log_a=0.85)
    elif t < B(240):
        # B — COMPLETION: the warm world from 12 s, the two of them on the ledge. the fullest bar of the film
        push = 1 + 0.05 * eio_cubic(prog(t, B(232), B(240)))
        world_at(c, g, WREF, 0.0, push)
        him_in_world(c, push)
        sun = 0.35 + 0.65 * pulse(t, B(K_COMP), 1.2)
        sx, sy, _ = wxf(1246, 574, push)
        rg = cairo.RadialGradient(sx, sy, 0, sx, sy, 420)
        rg.add_color_stop_rgba(0, 1, 0.9, 0.65, 0.7 * sun); rg.add_color_stop_rgba(1, 1, 0.9, 0.65, 0)
        g.set_source(rg); g.arc(sx, sy, 420, 0, 6.283); g.fill()
        lv = 0.0
        for kb, v in ((232, 0.25), (234, 0.5), (236, 0.75), (K_COMP, 1.0)):
            if t >= B(kb): lv = lerp(lv, v, eo_expo(prog(t, B(kb), B(kb) + 0.15)))
        x0, x1, y = 1180, 1780, 1000
        rgba(c, INK, 0.55); c.rectangle(x0 - 24, y - 52, x1 - x0 + 48, 84); c.fill()
        text(c, 'mono', 'me.feeling', x0, y - 18, 20, BONE, 0.8, track=0.15)
        text(c, 'monom', 'complete' if lv >= 1 else f'{int(lv * 100):3d} %', x1, y - 18, 22, CYAN, 0.95, align='right')
        line(c, x0, y + 10, x1, y + 10, BONE, 0.3, 6)
        for cc, aa in ((c, 1), (g, 0.7)): line(cc, x0, y + 10, lerp(x0, x1, lv), y + 10, CYAN, aa, 6)
        words_ol(c, [('then', 107.12), ('I', 107.70), ('can,', 108.02), ('then', 108.40), ('I', 108.64), ('can', 108.94),
                     ('finally', 109.16), ('be', 109.94)], t, 150, 248, 66, col=BONE, ol=SEPIA)
        if t >= B(K_COMP):
            slam_word(c, g, 'COMPLETION', t, B(K_COMP), 960, 380, 170, key='bold', col=BONE, ol=SEPIA, glow=0.4)
        fx['ab'] = 4 * pulse(t, B(K_COMP), 0.25); fx['vig'] = 0.4; fx['grain'] = 0.03
        fx['flash'] = 0.25 * pulse(t, B(K_COMP), 0.15)
        hud(c, t, False, a=0.6, log_a=0.85)
    elif t < B(252):
        # C — "you have left" x6: six places he used to be
        j = max(i for i, k in enumerate(LEFT) if t >= B(k))
        k0 = LEFT[j]; k1 = LEFT[j + 1] if j < 5 else 252.0
        u = eio_cubic(prog(t, B(k0) + P * 0.5, B(k0) + P * 1.0))         # the moment he is gone
        lp = prog(t, B(k0), B(k1))
        dark = True
        if j == 0:
            paper_bg(c); s_ = 1 + 0.03 * lp; dark = False
            img(c, 'n_pinky_hd', 960, 540, s_); img(c, 'n_pinky_alone_hd', 960, 540, s_, u)
        elif j == 1:
            s_ = 1.04 + 0.03 * lp
            img(c, 'n_lab_hd', 960, 540, s_); img(c, 'n_lab_empty_hd', 960, 540, s_, u)
        elif j == 2:
            push = 1.05 + 0.03 * lp
            world_at(c, g, WREF, 0.0, push); dark = False
            X, Y, sc = him_in_world(c, push, 1 - u)
            if u > 0:                                   # he comes apart into points that drift up and away
                xs, ys, col, rr, nz = alpha_points('n_creator_walk_hd')
                px = X + (xs - WALK_FEET[0]) * sc + nz[:, 0] * 40 * u + 60 * u * rr
                py = Y + (ys - WALK_FEET[1]) * sc - 260 * u * (0.4 + rr) + nz[:, 1] * 12 * u
                a_ = (1 - u) ** 0.7 * min(1, u * 6)
                draw_points(c, px, py, SEPIA, 0.8 * a_, 2.2)
        elif j == 3:
            fill_bg(c, INK); dotgrid(c, BONE, 0.05)
            rx, ry = -0.3, 0.5 + 0.12 * (t - B(246))
            s = 300
            V = [(x, y, z) for x in (-s, s) for y in (-s, s) for z in (-s, s)]
            Pp = [proj(*rot3(x, y, z, rx, ry), cx=960, cy=520) for (x, y, z) in V]
            edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count('1') == 1]
            for a, b in edges: line(c, Pp[a][0], Pp[a][1], Pp[b][0], Pp[b][1], BONE, 0.7, 2)
            img(c, 'n_offer_hd', 860, 770, 0.4, 1, 960, 1034)
            # the select-and-delete of world.removeThing(you)
            hx, hy = 1080, 770
            if u < 1:
                img(c, 'n_creator_walk_hd', hx, hy, 0.4 * 0.92, 1 - u, *WALK_FEET)
            sel = prog(t, B(k0) + P * 0.25, B(k0) + P * 0.5)
            if 0 < sel and u < 1:
                c.set_dash([6, 5]); rgba(c, CYAN, 0.9); c.set_line_width(2)
                c.rectangle(hx - 100, hy - 400, 200, 410); c.stroke(); c.set_dash([])
                text(c, 'mono', 'you', hx - 100, hy - 412, 18, CYAN, 0.9)
            if u > 0:
                text(c, 'mono', 'removed', hx, hy - 180, 20, GREY, 0.8 * (1 - prog(t, B(k1) - 0.2, B(k1))), align='center')
            for vi in (0, 7):
                px, py = Pp[vi][:2]
                padlock(c, g, px, py, 40, 1 - u if vi == 7 else 1)
        elif j == 4:
            # he walks away into the light; the thread between them goes slack and falls
            fill_bg(c, BONE)
            rg = cairo.RadialGradient(1180, 380, 40, 1180, 380, 1100)
            rg.add_color_stop_rgba(0, 1, 1, 1, 1); rg.add_color_stop_rgba(1, *PAPER, 1)
            c.set_source(rg); c.paint()
            w_ = eio_cubic(lp)
            sc = lerp(0.62, 0.22, w_); X, Y = lerp(980, 1180, w_), lerp(1090, 760, w_)
            img(c, 'n_creator_walk_hd', X, Y, sc, 1 - 0.7 * prog(t, B(k1) - 0.3, B(k1)), *WALK_FEET)
            hx, hy = X + (WALK_PINKY[0] - WALK_FEET[0]) * sc, Y + (WALK_PINKY[1] - WALK_FEET[1]) * sc
            for cc, aa, lw in ((c, 1, 4), (g, 0.5, 7)):
                rgba(cc, RED, aa); cc.set_line_width(lw); cc.new_path()
                if u < 0.5:                         # taut, from his little finger to her, off-frame bottom-left
                    cc.move_to(hx, hy); cc.curve_to(hx - 200, hy + 60, -100, 900, -40, 1100)
                else:                               # let go: the end falls
                    d = eo_cubic((u - 0.5) * 2)
                    ex, ey = lerp(hx, 380, d), lerp(hy, 1120, d)
                    cc.move_to(ex, ey); cc.curve_to(lerp(hx - 200, 200, d), lerp(hy + 60, 1100, d), -100, 1000, -40, 1100)
                cc.stroke()
            dark = False
        else:
            img(c, 'n_eye_open_hd', 960, 540, 1.06 + 0.02 * lp); img(c, 'n_eye_tear_hd', 960, 540, 1.06 + 0.02 * lp, u)
            gl = u * (0.5 + 0.5 * math.sin(t * 7) ** 2)
            tx, ty = 960 + (1392 - 960) * (1.06 + 0.02 * lp), 540 + (858 - 540) * (1.06 + 0.02 * lp)
            rg = cairo.RadialGradient(tx, ty, 0, tx, ty, 60)
            rg.add_color_stop_rgba(0, *BONE, 0.7 * gl); rg.add_color_stop_rgba(1, *BONE, 0)
            g.set_source(rg); g.arc(tx, ty, 60, 0, 6.283); g.fill()
            dark = False
        # code + lyric
        code = 'world.removeThing(you);' if j == 0 else 'me.lookFor(you, world);'
        rgba(c, INK, 0.7); c.rectangle(110, 930, 640, 96); c.fill()
        text(c, 'monom', code, 130, 968, 26, BONE, 0.95)
        if u > 0.2: text(c, 'mono', '// you == null' if j else '// you: gone', 130, 1006, 22, CYAN, min(1, u * 2))
        ly = [('Though', 110.86)] if j == 0 else []
        ly += [('you', B(k0)), ('have', B(k0) + P * 0.5), ('left', B(k0) + P * 0.9)]
        words_ol(c, ly, t, 150, 248, 76, col=BONE, ol=INK)
        fx['ab'] = 6 * pulse(t, B(k0), 0.25) + 2 * pulse(t, B(k0) + P * 0.5, 0.2)
        fx['flash'] = 0.2 * pulse(t, B(k0), 0.08)
        fx['vig'] = 0.6; fx['grain'] = 0.035
        hud(c, t, dark, a=0.55, log_a=0.9)
    else:
        # D — ISOLATION: a white void, a cage, her
        paper_bg(c)
        fl = 1 - prog(t, B(252), B(252) + 0.25)
        s = 250
        rx, ry = -0.28, 0.6 + 0.35 * (t - B(252))
        V = [(x, y, z) for x in (-s, s) for y in (-s, s) for z in (-s, s)]
        Pp = [proj(*rot3(x, y, z, rx, ry), cx=960, cy=560) for (x, y, z) in V]
        Zs = [rot3(x, y, z, rx, ry)[2] for (x, y, z) in V]
        edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count('1') == 1]
        ue = eo_expo(prog(t, B(252), B(252) + 0.4))
        for front in (False, True):
            if front: img(c, 'n_sitting_hd', 960, 720, 0.48, 1, 996, 841)
            for a, b in edges:
                if ((Zs[a] + Zs[b]) / 2 < 0) != front: continue
                xa, ya = Pp[a][:2]; xb, yb = Pp[b][:2]
                line(c, xa, ya, lerp(xa, xb, ue), lerp(ya, yb, ue), SEPIA, 0.85 if front else 0.35, 2 if front else 1.2)
        words(c, 'serif', [('me', 116.72), ('in', 117.0)], t, 150, 248, 76, SEPIA, 0.95)
        if t >= B(K_ISO):
            glyph_pop(c, 'thin', 'ISOLATION', 960, 1000, 120, SEPIA, t, B(K_ISO), P / 4, align='center', track=0.6, drop=0, dur=0.4)
        fx['flash'] = 0.9 * fl ** 2; fx['vig'] = 0.3; fx['grain'] = 0.03
        hud(c, t, False, a=0.4, log_a=0.8)
    return fx

# ================================================================ S25 BRIDGE  [B256, B288)
FRAG = None
def frag_layout():
    global FRAG
    if FRAG is None:
        meta = json.load(open(f'{WORK}/assets/frag.json'))
        tw, th, gp = 150, 84, 6; x0 = (W - (12 * tw + 11 * gp)) / 2; y0 = 300
        r = random.Random(3)
        dels = [m['i'] for m in meta if not m['keep']]; r.shuffle(dels)
        when = {i: 258 + (n // 4) * 0.25 for n, i in enumerate(dels)}      # 4 deletions per 16th from k258, all gone by FRAGMENTS
        FRAG = dict(meta=meta, tw=tw, th=th, gp=gp, x0=x0, y0=y0, when=when,
                    tries=[m['i'] for m in meta if m['keep']][::5][:4])
    return FRAG

def s_bridge(c, g, t):
    fx = {}
    kk = (t - T0) / P
    if t < B(272):
        fill_bg(c, INK)
        L = frag_layout(); tw, th, gp, x0, y0 = L['tw'], L['th'], L['gp'], L['x0'], L['y0']
        cur = None
        for m in L['meta']:
            i = m['i']; r_, c_ = divmod(i, 12)
            x, y = x0 + c_ * (tw + gp), y0 + r_ * (th + gp)
            ua = eo_cubic(prog(t, B(256) + (r_ + c_) * 0.02, B(256) + (r_ + c_) * 0.02 + 0.2))
            if ua <= 0: continue
            kd = L['when'].get(i)
            gone = kd is not None and kk >= kd
            if gone:
                rgba(c, BONE, 0.12); c.set_line_width(1); c.rectangle(x, y, tw, th); c.stroke()
                c.move_to(x, y); c.line_to(x + tw, y + th); c.move_to(x + tw, y); c.line_to(x, y + th); c.stroke()
                continue
            bright = 1.0
            if t >= B(264) and m['keep']: bright = 1.0
            elif t >= B(264): bright = 0.5
            c.save(); c.rectangle(x, y, tw, th); c.clip()
            c.set_source_surface(surf(f'frag_{i:02d}'), x, y); c.paint_with_alpha(ua * bright); c.restore()
            rgba(c, BONE, 0.35 * ua * bright); c.set_line_width(1); c.rectangle(x + 0.5, y + 0.5, tw - 1, th - 1); c.stroke()
            if kd is not None and kd - 0.25 <= kk < kd:          # selected, about to go
                rgba(c, CYAN, 0.9); c.set_line_width(3); c.rectangle(x - 2, y - 2, tw + 4, th + 4); c.stroke()
                rgba(c, CYAN, 0.25); c.rectangle(x, y, tw, th); c.fill()
                cur = (x + tw * 0.7, y + th * 0.7)
            if t >= B(K_DISH) - 0.1 and m['keep']:
                rgba(g, BONE, 0.25 * pulse(t, B(K_DISH), 0.8)); g.rectangle(x, y, tw, th); g.fill()
        ndel = sum(1 for i, kd in L['when'].items() if kk >= kd)
        text(c, 'mono', f'memory  {96 - ndel:2d} / 96 frames', x0, y0 - 16, 18, BONE, 0.6, track=0.15)
        # failed deletes on the frames that have him in them
        for n, i in enumerate(L['tries']):
            kt = 265 + n * 1.25
            if not (B(kt) - 0.2 <= t < B(kt) + 0.9): continue
            r_, c_ = divmod(i, 12); x, y = x0 + c_ * (tw + gp), y0 + r_ * (th + gp)
            cur = (x + tw * 0.7, y + th * 0.7)
            if t >= B(kt):
                sh = 6 * pulse(t, B(kt), 0.2) * math.sin(t * 90)
                bx, by = min(x + tw * 0.5, W - 520), y + th + 10
                rgba(c, INK, 0.92); c.rectangle(bx + sh, by, 500, 82); c.fill()
                rgba(c, BONE, 0.9); c.set_line_width(1.5); c.rectangle(bx + sh, by, 500, 82); c.stroke()
                text(c, 'monom', 'Permission denied', bx + 18 + sh, by + 34, 24, BONE, 1)
                text(c, 'mono', 'me.getMemory().isErasable() == false', bx + 18 + sh, by + 64, 17, CYAN, 0.9)
                rgba(c, BONE, 0.9); c.set_line_width(2.5); c.rectangle(x - 2, y - 2, tw + 4, th + 4); c.stroke()
        if cur:                                                   # the cursor
            x, y = cur
            rgba(c, CYAN, 1); c.move_to(x, y); c.line_to(x, y + 30); c.line_to(x + 8, y + 23); c.line_to(x + 14, y + 36)
            c.line_to(x + 19, y + 33); c.line_to(x + 13, y + 21); c.line_to(x + 23, y + 21); c.close_path(); c.fill()
        if t < B(264):
            words_ol(c, [('If', 118.49), ('I', 118.70), ('can,', 119.10), ('if', 119.60), ('I', 119.98), ('can', 120.02),
                         ('erase', 120.24), ('all', 120.74), ('the', 120.94), ('pointless', 121.18)], t, 150, 248, 66)
            if t >= B(K_FRAG):
                slam_word(c, g, 'FRAGMENTS', t, B(K_FRAG), 960, 720, 230)
        else:
            words_ol(c, [('Then', 121.96), ('maybe,', 122.50), ('then', 122.98), ('maybe', 123.92), ('you', 124.18),
                         ("won't", 124.42), ('leave', 124.66), ('me', 124.80), ('so', 124.92)], t, 150, 248, 66)
            if t >= B(K_DISH) - 0.25:
                s = scramble('DISHEARTENED', t, B(K_DISH), 0.03, seed=11)
                c.new_path(); fonts()['bold'].text_path(c, s, 960, 720, 200, 'center', 0.04)
                rgba(c, INK, 0.9); c.set_line_width(12); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
                rgba(c, BONE, 1); c.fill()
        fx['ab'] = 5 * pulse(t, B(K_FRAG), 0.25) + 4 * pulse(t, B(K_DISH), 0.25) + sum(3 * pulse(t, B(265 + n * 1.25), 0.15) for n in range(4))
        fx['flash'] = 0.25 * pulse(t, B(256), 0.1)
        hud(c, t, True, a=0.6, log_a=0.85)
        return fx
    # C — Challenging your God: she pushes against the wall of her own source code
    fill_bg(c, INK)
    lines_ = [s for _, s in CODE_LOG if not s.startswith('//')] * 3
    lh = 48; scroll = (t - B(272)) * 70
    first = int(scroll // lh)
    hot = t >= B(K_GOD)
    for n in range(first, first + 26):
        s = lines_[n % len(lines_)]; y = 80 + n * lh - scroll
        god = ('God' in s or 'god' in s)
        a_ = 0.22 if not (god and hot) else 0.9
        text(c, 'mono', s, 120 + 40 * (n % 3), y, 30, CYAN if (god and hot) else BONE, a_)
        if god and hot: text(g, 'mono', s, 120 + 40 * (n % 3), y, 30, CYAN, 0.5 * pulse(t, B(math.floor(kk)), 0.4) + 0.2)
    # her, back to us, hand on the wall
    sc = 0.95; bx, by = 1300, 1120
    img(c, 'n_back_reach_hd', bx, by, sc, 1, 979, 1045)
    px, py = bx + (1125 - 979) * sc, by + (195 - 1045) * sc
    for kb in range(272, 288):
        p_ = prog(t, B(kb), B(kb) + 0.6)
        if 0 < p_ < 1:
            for cc, aa in ((c, 0.6), (g, 0.5)):
                rgba(cc, CYAN, aa * (1 - p_)); cc.set_line_width(2); cc.new_path(); cc.arc(px, py, 20 + 260 * p_, 0, 6.283); cc.stroke()
    if t >= B(K_ILL):                                    # the wall cracks from her palm
        uc = eo_expo(prog(t, B(K_ILL), B(K_ILL) + 0.5))
        rr = random.Random(5)
        rgba(c, BONE, 0.85); c.set_line_width(2)
        for k in range(14):
            a = rr.random() * 6.283; L = (200 + rr.random() * 700) * uc
            x, y = px, py; c.move_to(x, y)
            for s in range(5):
                a += (rr.random() - 0.5) * 0.9; x += math.cos(a) * L / 5; y += math.sin(a) * L / 5; c.line_to(x, y)
        c.stroke()
        st = ['Exception in thread "main"', '  java.lang.IllegalArgumentException', '    at Thing.setOpinion(Thing.java:617)',
              '    at GodDrinksJava.main(GodDrinksJava.java:3691)']
        rgba(c, BONE, 0.95); c.rectangle(640, 110, 760, 40 + 38 * 4); c.fill()
        for n, s in enumerate(st):
            text(c, 'monom' if n < 2 else 'mono', type_on(s, t, B(K_ILL) + n * 0.12, 0.008), 660, 150 + n * 38, 22, INK, 1)
    words_ol(c, [('Challenging', 126.14), ('your', 127.20), ('God,', 127.60)] if t < B(277.6) else
             [('you', 128.66), ('have', 129.28), ('made', 129.48), ('some', 129.98)], t, 150, 248 if t < B(K_ILL) else 1040, 66)
    slam_word(c, g, 'ILLEGAL', t, B(K_ILL), 120, 560, 220, align='left')
    slam_word(c, g, 'ARGUMENTS', t, B(K_ARG), 120, 780, 220, align='left')
    if t >= B(285.75):
        u = eo_cubic(prog(t, B(285.75), B(285.75) + 0.2))
        c.new_path(); fonts()['serif'].text_path(c, 'God is always true.', 960, 980, 96, 'center')
        rgba(c, INK, 0.9 * u); c.set_line_width(10); c.stroke_preserve(); rgba(c, BONE, u); c.fill()
    # the end of the bridge: the picture inverts on the 16ths, then shatters
    if t >= B(286.5):
        n16 = int((t - B(286.5)) / (P / 4))
        if n16 % 2 == 0:
            c.set_operator(cairo.OPERATOR_DIFFERENCE); rgba(c, (1, 1, 1), 1); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
        fx['ab'] = 10
    else:
        fx['ab'] = 6 * pulse(t, B(K_ILL), 0.3) + 6 * pulse(t, B(K_ARG), 0.3) + 2 * pulse(t, B(math.floor(kk)), 0.15)
    fx['flash'] = 0.3 * pulse(t, B(K_ILL), 0.1) + 0.3 * pulse(t, B(K_ARG), 0.1) + 0.9 * ei_cubic(prog(t, B(287.6), B(288)))
    hud(c, t, True, a=0.6, log_a=0.85)
    return fx
