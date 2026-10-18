"""world.execute(me); x Ralmia — Act IV "execution" (133.26–162.80 s).
k288-320 is the instrumental interlude: she is not on screen, we are her -- her cyan aperture reticle, an avenue of every
world of the film rushing at us, one gear up every 8 beats; no EXECUTION words (nobody sings yet).
k320-342: EXECUTION x12, one every second beat (user: first ~148 s, twelfth ~158 s): each call slams a gate shut ahead of
us and we smash through it on the next beat; the twelfth slams in our face and we stop dead.
k342-352 (the count, the 13th, the pull, the launch) is waiting for the user's ears -- see HANDOFF.md 2.3.
v2 (plan_v2b.md): the interlude is Lishenna's "song stopped" -- the worship grows in the silence: every gear, more of
the windows rushing at us are her, and Ralmia logs it as corrupted data. the twelve calls are her Trial of Destruction:
a lavender shock with each call, and the stamp does not take on anything with her in it (can't be destroyed by effects)."""
from scenes5 import *

EXE = [320 + 2 * i for i in range(12)]
COUNT = [325.5 + 0.75 * i for i in range(6)]
K_EX13, K_PULL, K_LAUNCH = 330.0, 340.0, 344.0

# ================================================================ S26 TWELVE EXECUTIONS  [B288, B320)
WIN_W, WIN_H, WIN_SP = 470, 264, 540
RUN_X, TOP_Y = 560, 640
VEL = WIN_SP / (2 * P)
def win_cx(i, t): return 20 + WIN_SP * i - VEL * (t - B(288))
def win_src(i):
    if i == 12: return ('n_pinky2_hd', None, 'sim #0001  ·  you & me')
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

# ---- the corridor, first person. depth is driven by distance travelled, so a gear change kicks the speed, never the picture
VPX, VPY, KZ = 960, 430, 1150
U = 1.5                                   # depth units per beat in first gear: one side window passes every beat
GEARS = [(288, 296, 1), (296, 304, 2), (304, 312, 2), (312, 342, 4)]
def dist(kk):
    d = 0.0
    for a, b, gr in GEARS: d += U * gr * clamp(kk - a, 0, b - a)
    return d
def gear(kk): return next((gr for a, b, gr in GEARS if a <= kk < b), 0)
D_EXE = [dist(k) for k in EXE]
GATE_W, Z_STOP = 2.0, 1.6                 # gates are bigger than the side windows; the twelfth stops us 1.6 ahead
Z_SLAM = 6.3                              # gates 1-11 slam this far ahead; at 4th gear we reach them one beat later (z 0.3)
CORR = POOL + [('n_stage_empty_hd', None), ('n_creation2_hd', None), ('n_eye_tear_hd', None), ('n_listen_hd', None), ('n_wL2n_hd', INK2),
               ('n_offer_hd', PAPER), ('n_cat2_hd', PAPER), ('n_role_s_hd', INK2), ('n_sitting_hd', PAPER), ('n_back_reach_hd', PAPER),
               ('n_spec_egg_hd', PAPER), ('n_spec_tomato_hd', INK2), ('n_pinky2_alone_hd', None), ('n_portrait2_hd', None)]
# v2: the frames with Lishenna in them
LISH_POOL = [('n_lish_face_hd', None), ('n_stage_hd', None), ('n_pinky2_hd', None), ('n_lish_walk_hd', PAPER), ('n_lish_float_hd', INK2),
             ('n_creation2_hd', None), ('n_lish_stand_hd', PAPER), ('n_lish_sheet_hd', None), ('n_ledge2_hd', None),
             ('n_cube_together_hd', INK2), ('n_lish_sit_hd', PAPER)]
LISH_SET = {n for n, _ in LISH_POOL}
NON = [it for it in CORR if it[0] not in LISH_SET]
def lish_share(d):
    """how much of what rushes past is her, by distance travelled: one step per gear (= one me.update())"""
    return 0.12 if d < dist(296) + 2 else 0.33 if d < dist(304) + 2 else 0.6 if d < dist(312) + 2 else 0.88
SP = U / 2                                # side windows: one each side per beat in first gear
N_SIDE = int(dist(342) / SP) + 24
SIDE = [((-1 if j % 2 else 1) * (1.3 + 0.6 * random.Random(j * 7).random()), -0.85 + 1.15 * random.Random(j * 13).random(),
         LISH_POOL[(j * 5 + 1) % len(LISH_POOL)] if random.Random(j * 31).random() < lish_share(j * SP) else NON[(j * 7 + 3) % len(NON)])
        for j in range(N_SIDE)]
GATE_SRC = [NON[(i * 5 + 1) % len(NON)] for i in range(12)]
for i_, it in ((2, ('n_lish_face_hd', None)), (5, ('n_stage_hd', None)), (8, ('n_lish_float_hd', INK2)), (11, ('n_pinky2_hd', None))):
    GATE_SRC[i_] = it                     # every third gate is her; the twelfth is the two of them
D_DEAD = dist(320) + 1.0                  # side windows we pass after the first call are already dead when we first see them

def stamp(c, cx, cy, w, a):
    if a <= 0: return
    c.save(); c.translate(cx, cy); c.rotate(-0.12)
    c.new_path(); fonts()['heavy'].text_path(c, 'EXECUTED', 0, w * 0.06, w * 0.16, 'center')
    rgba(c, INK, 0.9 * a); c.set_line_width(w * 0.016); c.stroke_preserve(); rgba(c, BONE, a); c.fill()
    c.restore()

def reflect(c, s, x, y, w, h, name, bg, a):
    """the window again, upside down in the glossy floor under it"""
    yf = VPY + 0.62 * s
    if y + h > yf or a <= 0.01: return
    c.save(); c.rectangle(0, yf, W, H); c.clip(); c.translate(0, 2 * yf); c.scale(1, -1)
    win(c, x, y, w, h, name, bg, '', a); c.restore()

def cwin(c, g, z, side, Y, name, bg, lab, size=1.0, dead=False, flash=0.0):
    if z < 0.3 or z > 15: return
    s = KZ / z; w = size * s; h = w * 9 / 16
    cx = VPX + side * s; cy = VPY + Y * s
    x, y = cx - w / 2, cy - h / 2
    fog = clamp((15 - z) / 6)
    reflect(c, s, x, y, w, h, name, bg, fog * (0.06 if dead else 0.16))
    win(c, x, y, w, h, name, bg, 'EXECUTED' if dead else lab, fog)
    if dead:
        rgba(c, INK, 0.6 * fog); c.rectangle(x, y, w, h); c.fill()
        c.save(); c.translate(cx, cy); c.rotate(-0.12)
        text(c, 'heavy', 'EXECUTED', 0, w * 0.05, w * 0.14, BONE, 0.5 * fog, align='center'); c.restore()
    elif flash > 0.01:
        rgba(c, BONE, 0.7 * flash * fog); c.rectangle(x, y, w, h); c.fill()
        rgba(g, BONE, 0.5 * flash * fog); g.rectangle(x, y, w, h); g.fill()

def gate(c, g, t, z, i):
    """gate i: a world framed dead ahead. it slams on its EXECUTION (two shutters meet); on the next beat we go through it"""
    if z < 0.3 or z > 15: return
    tc = B(EXE[i])
    s = KZ / z; w = GATE_W * s; h = w * 9 / 16
    cx, cy = VPX, VPY + 0.05 * s
    x, y = cx - w / 2, cy - h / 2
    fog = clamp((15 - z) / 6)
    name, bg = GATE_SRC[i]                                                                # the last one: the two of them
    immune = name in LISH_SET
    reflect(c, s, x, y, w, h, name, bg, fog * (0.16 if t < tc else 0.05))
    win(c, x, y, w, h, name, bg, 'sim #0001  ·  you & me' if i == 11 else f'sim #{3 + 41 * i:04d}', fog)
    rgba(g, CYAN, 0.25 * fog); g.set_line_width(4); g.rectangle(x, y, w, h); g.stroke()
    if t < tc: return
    u = eo_expo(prog(t, tc, tc + 0.07))                                                   # the shutters: bang
    if immune: u *= 1 - eo_cubic(prog(t, tc + 0.10, tc + 0.30))                           # ...and they spring open again
    rgba(c, INK, fog); c.rectangle(x, y, w / 2 * u, h); c.rectangle(x + w - w / 2 * u, y, w / 2 * u, h); c.fill()
    line(c, cx, y, cx, y + h, BONE, 0.5 * u * fog, max(1, w * 0.004))
    fl = 1 - prog(t, tc + 0.05, tc + 0.2)
    if fl > 0:
        rgba(g, BONE, 0.8 * fl); g.set_line_width(max(2, w * 0.01)); g.rectangle(x, y, w, h); g.stroke()
    rgba(c, BONE, 0.7 * fog); c.set_line_width(max(1.2, w * 0.004)); c.rectangle(x, y, w, h); c.stroke()
    if immune:                                                                            # the stamp does not take: it slides off
        v = ei_cubic(prog(t, tc + 0.11, tc + 0.38))                                     # gone before we pass through
        c.save(); c.translate(cx + 120 * v * w / 1000, cy + 900 * v * v * w / 1000); c.rotate(0.9 * v); c.translate(-cx, -cy)
        stamp(c, cx, cy, w, eo_expo(prog(t, tc + 0.04, tc + 0.12)) * fog * (1 - v)); c.restore()
        return
    ts = tc + (0.6 if i == 11 else 0.04)                                                 # the last: the word first, then the stamp
    stamp(c, cx, cy, w, eo_expo(prog(t, ts, ts + 0.08)) * fog)

def reticle(c, g, t, R, a=1.0, kick=0.0):
    """her aperture (the iris rings of 10 s and the blades of 48 s), now the centre of our view"""
    if a <= 0: return
    x, y = VPX, VPY
    R *= 1 + 0.12 * kick
    for cc, aa, lw in ((c, 0.8 * a, 1.8), (g, 0.5 * a, 3)):
        rgba(cc, CYAN, aa); cc.set_line_width(lw); cc.new_path(); cc.arc(x, y, R, 0, 6.283); cc.stroke()
        for k in range(8):
            an = k * math.pi / 4 + 0.15 * t
            cc.move_to(x + math.cos(an) * R, y + math.sin(an) * R); cc.line_to(x + math.cos(an) * (R + 16), y + math.sin(an) * (R + 16))
        cc.stroke()
        rgba(cc, CYAN, 0.6 * aa); cc.set_line_width(lw * 0.8)
        for k in range(8):                                                                # blades, open
            a0 = 2 * math.pi * k / 8 - 0.1 * t
            px, py = x + math.cos(a0) * R * 0.55, y + math.sin(a0) * R * 0.55
            tx_, ty_ = -math.sin(a0), math.cos(a0)
            cc.move_to(px, py); cc.line_to(px + tx_ * R * 0.42, py + ty_ * R * 0.42)
        cc.stroke()
    line(c, x - 6, y, x + 6, y, CYAN, 0.9 * a, 1.5); line(c, x, y - 6, x, y + 6, CYAN, 0.9 * a, 1.5)

def corridor(c, g, t, D, gr):
    off = D % 1.0
    for n_ in range(1, 15):                                  # floor lines rushing at us, rails to the vanishing point
        z = n_ - off
        if z < 0.4: continue
        y = VPY + 0.62 * KZ / z
        line(c, 0, y, W, y, BONE, 0.16 * (1 - z / 15), 1 + 1.5 / z)
    for sx in (-1, 1):
        line(c, VPX, VPY, VPX + sx * 2200, VPY + 0.62 * KZ / 0.5, BONE, 0.18, 1.2)
    rnd = np.random.default_rng(12); n_st = 40 + 30 * gr; ang = rnd.random(160) * 6.283; ph = rnd.random(160)
    for a_, p_ in zip(ang[:n_st], ph[:n_st]):                # radial streaks, denser and longer with each gear
        f = (D * 0.22 + p_) % 1.0
        r0, r1 = 120 + 1500 * f ** 2, 120 + 1500 * min(1, f + 0.06 + 0.03 * gr) ** 2
        rgba(c, BONE, 0.10 + 0.25 * f); c.set_line_width(1 + 2 * f)
        c.move_to(VPX + math.cos(a_) * r0, VPY + math.sin(a_) * r0 * 0.7); c.line_to(VPX + math.cos(a_) * r1, VPY + math.sin(a_) * r1 * 0.7); c.stroke()

def side_items(D, sparse=False):
    items = []
    j0 = max(0, int((D - 1) / SP) - 1)
    for j in range(j0, min(N_SIDE, j0 + 40)):
        if sparse and j * SP >= D_DEAD and j % 4 > 1: continue
        z = 1 + j * SP - D
        if 0.3 <= z <= 15:
            side, Y, (name, bg) = SIDE[j]
            items.append((z, ('s', side, Y, name, bg, j, j * SP >= D_DEAD and name not in LISH_SET)))
    return items

def draw_items(c, g, t, items, lab=True, flash=0.0):
    items.sort(key=lambda it: -it[0])
    for z, it in items:
        if it[0] == 's':
            _, side, Y, name, bg, j, dead = it
            cwin(c, g, z, side, Y, name, bg, f'sim #{(2 + j * 37) % 9000:04d}' if lab else '', 1.0, dead, flash)
        else:
            gate(c, g, t, z, it[1])

def s_executions(c, g, t):
    """k288-320: the interlude, first person. nobody sings: only speed"""
    fill_bg(c, INK)
    fx = {}
    kk = (t - T0) / P; D = dist(kk); gr = gear(kk)
    blk = int((kk - 288) // 8)
    kick = pulse(t, B(288 + 8 * blk), 0.35) if blk > 0 else 0.0                        # gear change on the downbeat
    sh = 6 * kick * math.sin(t * 90)
    c.save(); c.translate(sh, 0); g.save(); g.translate(sh / 2, 0)
    corridor(c, g, t, D, gr)
    if kk >= 314:                                                                         # the vanishing point lights up: a door
        u = eo_cubic(prog(t, B(314), B(320)))
        dw, dh = 30 + 70 * u, (30 + 70 * u) * 9 / 16
        rg = cairo.RadialGradient(VPX, VPY, 0, VPX, VPY, 40 + 120 * u)
        rg.add_color_stop_rgba(0, *BONE, 0.35 * u); rg.add_color_stop_rgba(1, *BONE, 0)
        g.set_source(rg); g.arc(VPX, VPY, 40 + 120 * u, 0, 6.283); g.fill()
        rgba(c, BONE, 0.9 * u); c.rectangle(VPX - dw / 2, VPY - dh / 2, dw, dh); c.fill()
        rgba(g, BONE, 0.5 * u); g.rectangle(VPX - dw / 2, VPY - dh / 2, dw, dh); g.fill()
    fl = pulse(t, B(304), 0.45)                                                           # k304: every window flashes at once
    items = side_items(D)
    for i in range(12):
        z = Z_SLAM + D_EXE[i] - D
        if z <= 15: items.append((z, ('g', i)))
    draw_items(c, g, t, items, True, fl)
    c.restore(); g.restore()
    RS = [170, 140, 112, 88]
    R = RS[min(blk, 3)]
    if blk > 0: R = lerp(RS[min(blk, 3) - 1], R, eo_back(prog(t, B(288 + 8 * blk), B(288 + 8 * blk) + 0.2), 2))
    reticle(c, g, t, R, eo_cubic(prog(t, B(288), B(288) + 0.3)), pulse(t, B(math.floor(kk)), 0.18))
    text(c, 'mono', f'MACH {1.2 + 0.035 * D:5.2f}', 130, 1000, 26, BONE, 0.75, track=0.15)
    text(c, 'monom', f'me.velocity  x{gr}', W - 130, 1000, 24, CYAN, 0.85, align='right', track=0.05)
    song_line(c, g, t, 0.0)
    pc = 0.0
    for kb, v in CORRUPT:
        if kk >= kb: pc = lerp(pc, v, eo_expo(prog(t, B(kb), B(kb) + 0.25)))
    text(c, 'mono', f'data.corrupted  {int(round(pc)):3d} %', 960, 1000, 22, BONE, 0.7, align='center', track=0.1)
    fx['ab'] = 5 * kick + 2 * pulse(t, B(math.floor(kk)), 0.12) + 3 * fl + 0.6 * gr
    fx['flash'] = 0.12 * fl + 0.15 * pulse(t, B(288), 0.15)
    fx['glow'] = 0.9
    hud(c, t, True, a=0.6, log_a=0.85)
    return fx

SONG_Y = 952
def song_line(c, g, t, amp=0.0):
    """v2: her song along the bottom -- flat while nobody sings, a burst on every call"""
    text(c, 'mono', 'song', 130, SONG_Y - 14, 16, BONE, 0.45, track=0.2)
    for cc, aa, lw in ((c, 0.55, 1.6), (g, 0.35, 3)):
        rgba(cc, LISH, aa); cc.set_line_width(lw); cc.new_path()
        for n_ in range(0, 241):
            x = 200 + (W - 400) * n_ / 240
            v = amp * math.sin(n_ * 0.9 - t * 30) * math.sin(math.pi * n_ / 240) * (0.6 + 0.4 * math.sin(n_ * 0.21 + t * 7))
            (cc.move_to if n_ == 0 else cc.line_to)(x, SONG_Y - v)
        cc.stroke()

def shock(c, g, t, kb, x=VPX, y=VPY):
    u = prog(t, B(kb), B(kb) + 0.7)
    if not (0 < u < 1): return
    r = 40 + 1500 * eo_cubic(u)
    for cc, k_, lw in ((c, 0.7, 4 * (1 - u) + 1), (g, 0.5, 6)):
        rgba(cc, LISH, k_ * (1 - u)); cc.set_line_width(lw); cc.new_path(); cc.arc(x, y, r, 0, 6.283); cc.stroke()

CORRUPT = [(288, 12), (296, 33), (304, 60), (312, 88)]
EX_AT = [(0.27, 0.30, 150), (0.74, 0.78, 190), (0.30, 0.82, 130), (0.72, 0.24, 170), (0.50, 0.16, 120), (0.22, 0.58, 200),
         (0.80, 0.52, 140), (0.50, 0.88, 160), (0.24, 0.20, 180), (0.76, 0.66, 210), (0.36, 0.48, 230), (0.50, 0.50, 300)]
def s_doors(c, g, t):
    """k320-342: twelve calls, twelve gates. slam on the call, through it on the next beat; the twelfth stops us dead"""
    fill_bg(c, INK)
    fx = {}
    kk = (t - T0) / P; D = dist(min(kk, 342)); gr = gear(kk)
    n = sum(1 for k in EXE if kk >= k)
    kick = sum(pulse(t, B(k + 1), 0.3) for k in EXE[:11])                               # through the gate
    crash = pulse(t, B(342), 0.5)
    sh = 7 * kick * math.sin(t * 90) + 22 * crash * math.sin(t * 70)
    c.save(); c.translate(sh, 0.4 * sh); g.save(); g.translate(sh / 2, 0.2 * sh)
    corridor(c, g, t, D, gr)
    items = side_items(D, sparse=True)
    for i in range(12):
        z = (Z_STOP if i == 11 else Z_SLAM) + D_EXE[i] - D
        if 0.3 <= z <= 15: items.append((z, ('g', i)))
    draw_items(c, g, t, items, False)
    c.restore(); g.restore()
    reticle(c, g, t, 76 * (1 - 0.6 * eo_cubic(prog(t, B(342), B(342) + 0.3))), 1 - prog(t, B(342.5), B(343.5)),
            sum(pulse(t, B(k), 0.25) for k in EXE))
    for i, k in enumerate(EXE):                              # EXECUTION strobes once per call, somewhere new each time
        xr, yr, sz = EX_AT[i]
        slam_word(c, g, 'EXECUTION', t, B(k), xr * W, yr * H + sz * 0.35, sz, until=B(k) + (0.6 if i == 11 else 0.32), glow=0.5)
    for k in EXE: shock(c, g, t, k)                         # v2: each call is her song coming back -- the trial
    song_line(c, g, t, sum(46 * pulse(t, B(k), 0.45) for k in EXE))
    text(c, 'monom', f'world.runExecution();   x {n:2d} / 12', W - 130, 1000, 24, CYAN, 0.9, align='right', track=0.05)
    text(c, 'mono', f'MACH {1.2 + 0.035 * D:5.2f}' if kk < 342 else 'MACH  0.00', 130, 1000, 26, BONE, 0.75, track=0.15)
    fx['ab'] = sum(5 * pulse(t, B(k), 0.25) for k in EXE) + 4 * kick + 10 * crash
    fx['flash'] = sum(0.18 * pulse(t, B(k), 0.08) for k in EXE) + 0.12 * kick + 0.5 * pulse(t, B(342), 0.12)
    fx['glow'] = 0.9
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
