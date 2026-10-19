"""v3 (plan_v3.md): Ralmia's system -- ŌMETEŌTL OS -- around the scenes of v2.
render_v3(t, fr, scene, composite) draws the scene into its own buffers, then the panel, then puts the scene either full
frame or into the VIEWPORT (mode follows MODES), with the picture register (lib.REG) following REGS.
Phase 1 covers 0 .. B(64) (the boot, the speed of sound, Achilles, the title); later sections fall back to v2."""
from lib import *
import lib
import scenes as S
from codelog import CODE_LOG

V3_UNTIL = B(66)
VP = (360, 64, 1200, 675)                     # viewport x, y, w, h
LX, RX, COLW = 24, 1584, 312
TOP_H = 52

# ---------------------------------------------------------------- what the frame is, when
# (k0, mode) -- 'full' or 'panel'; switches land on the beat and take TR seconds
MODES = [(0, 'panel'), (40, 'full'), (48, 'panel'), (60, 'full'), (64, 'panel')]
TR = 0.16
# (k0, register) -- picture treatment, following the shot's own paper / ink
REGS = [(0, 'r'), (8, 'm'), (16, 'r'), (24, 'm'), (28, 'r'), (48, 'r'), (60, 'r')]
def mode_at(t):
    kk = (t - T0) / P; cur, k_on, prev = 'panel', -9, 'panel'
    for k, m in MODES:
        if kk >= k: prev, cur, k_on = cur, m, k
    u = eo_cubic(prog(t, B(k_on), B(k_on) + TR))
    a, b = (1.0 if prev == 'panel' else 0.0), (1.0 if cur == 'panel' else 0.0)
    return lerp(a, b, u)
def reg_at(t):
    kk = (t - T0) / P; r = None
    for k, v in REGS:
        if kk >= k: r = v
    return r

# ---------------------------------------------------------------- the boot: POWER and VOICE are there from the first
# beat, SHIELD comes with "protection"; the rest land one per 16th with the parts of "lay down your pieces" (k8.25..),
# the core last, with the core gem, on k11
LEFT = [('POWER', 84), ('SHIELD', 70), ('CORE  ŌMETEŌTL', 104), ('DRIVE', 150), ('SENSORS', 112), ('CLASS', 164),
        ('CLOCK', 84), ('MEMORY', 106)]
RIGHT = [('LINK', 214), ('TRANSMISSION', 214), ('TASKS', 544)]
LAND_ORDER = ['DRIVE', 'SENSORS', 'CLASS', 'CLOCK', 'MEMORY', 'LINK', 'TRANSMISSION', 'TASKS']
LAND = {n: B(8.25 + 0.25 * i) for i, n in enumerate(LAND_ORDER)}
LAND.update({'POWER': B(0), 'VOICE': B(0), 'SHIELD': B(4), 'CORE  ŌMETEŌTL': B(11)})
def rects():
    out = {}; y = VP[1]
    for n, h in LEFT: out[n] = (LX, y, COLW, h); y += h + 10
    y = VP[1]
    for n, h in RIGHT: out[n] = (RX, y, COLW, h); y += h + 10
    vy = VP[1] + VP[3] + 24
    out['VOICE'] = (VP[0], vy, VP[2], H - vy - 24)
    return out
RECTS = rects()

# active module (lit border) by beat
ACTIVE = [(0, 'POWER'), (4, 'SHIELD'), (8, None), (12, 'CLASS'), (16, 'MEMORY'), (21, 'SENSORS'), (24, 'CLOCK'),
          (28, 'TASKS'), (32, 'DRIVE'), (48, 'LINK'), (60, None)]
def active_at(kk):
    a = None
    for k, n in ACTIVE:
        if kk >= k: a = n
    return a

# ---------------------------------------------------------------- the voices
# OUT = her (the lyric, word times as in the scenes); IN = Lishenna (plan_v3.md section 3)
OUT = [[('Switch', B(0)), ('on', 0.58), ('the', 1.04), ('power', B(2)), ('line', B(2.5))],
       [('Remember', B(4)), ('to', 2.40), ('put', 2.78), ('on', 3.02), ('PROTECTION', B(6))],
       [('Lay', B(8)), ('down', 4.26), ('your', 4.70), ('PIECES', B(10))],
       [('and', 5.42), ("let's", 5.80), ('begin', 6.10), ('OBJECT', B(13)), ('CREATION', B(14))],
       [('Fill', B(16)), ('in', 7.94), ('my', 8.36), ('data', B(18)), ('PARAMETERS', B(18.7))],
       [('INITIALIZATION', B(22))],
       [('Set', B(24)), ('up', 11.60), ('our', 12.06), ('new', B(26)), ('WORLD', B(26.5))],
       [('and', B(28)), ("let's", 13.30), ('begin', 13.44), ('the', 13.84), ('SIMULATION', B(30))],
       [('world.execute(me);', B(60))]]
IN = [(16.80, 'Running? Cute. You can\'t outrun a song.'),
      (22.75, '…hey. Where\'d you go?'),
      (24.10, 'Catch me~')]
def voice_lines(t):
    ev = [(ws[0][1], 'OUT', ws) for ws in OUT] + [(t0, 'IN', s) for t0, s in IN]
    return sorted([e for e in ev if e[0] <= t], key=lambda e: e[0])[-5:]

# ---------------------------------------------------------------- module states (all from t)
def drive_state(t, kk):
    import scenes2 as S2
    if kk < 32: return 0.0, 0.0
    if kk < 36:
        v = 0.0
        for kb, val in [(32, 0.0), (33, 85.07), (34, 170.15), (35, 255.22), (35.5, 340.29)]:
            if t >= B(kb): v = lerp(v, val, eo_cubic(prog(t, B(kb), B(kb) + 0.12)))
        return v, v / 340.29
    if kk < 48:
        M = S2.mach_of(min(t, B(47.99))); return M * 340.29, M
    return 299792458.0, 881000.0

def achilles_d(t):
    kk = (t - T0) / P
    if kk < 49: return 1.0
    kr = kk - 49; frozen = 7.0 <= kr < 7.5
    kf = 7.0 if frozen else (7.0 + (kr - 7.5) * 2 if 7.5 <= kr < 8.0 else kr)
    n = math.floor(kf); ph = kf - n
    if kk >= 58: return 0.5 ** 9
    return 0.5 ** n * (1 - 0.5 * eo_cubic(clamp(ph / 0.45)))

def mem_fill(t):
    lv = math.floor(prog(t, B(17), B(18)) * 8) / 8
    return 1.0 if t >= B(18) else eo_cubic(lv)

# ---------------------------------------------------------------- drawing helpers
def _box(c, g, x, y, w, h, title, active, t):
    rgba(c, INK2, 0.97); c.rectangle(x, y, w, h); c.fill()
    kk = (t - T0) / P
    bl = pulse(t, B(math.floor(kk)), 0.35) if active else 0.0
    col = CYAN if active else GREY
    rgba(c, col, (0.75 + 0.25 * bl) if active else 0.4); c.set_line_width(1.4 if active else 1.0)
    c.rectangle(x + 0.5, y + 0.5, w - 1, h - 1); c.stroke()
    rgba(c, col, 1); c.rectangle(x, y, 4, 22); c.fill()
    if active and bl > 0.05:
        rgba(g, CYAN, 0.35 * bl); g.set_line_width(3); g.rectangle(x, y, w, h); g.stroke()
    text(c, 'monom', title, x + 14, y + 17, 14, BONE if active else GREY, 0.95, track=0.18)

def _light(c, x, y, on, col=CYAN):
    rgba(c, col if on else GREY, 1 if on else 0.35); c.arc(x, y, 4.5, 0, 6.283); c.fill()

def _row(c, x, y, w, label, value, on=True, vcol=BONE, dot=CYAN):
    _light(c, x + 6, y - 5, on, dot)
    text(c, 'mono', label, x + 18, y, 15, BONE if on else GREY, 0.85 if on else 0.6)
    if value: text(c, 'monom', value, x + w - 4, y, 15, vcol if on else GREY, 0.95, align='right')

def _bar(c, x, y, w, u, col=CYAN):
    rgba(c, GREY, 0.35); c.rectangle(x, y, w, 5); c.fill()
    if u > 0: rgba(c, col, 0.95); c.rectangle(x, y, w * clamp(u), 5); c.fill()

def _wave(c, g, x, y, w, amp, t, a=1.0, col=LISH):
    for cc, aa, lw in ((c, a, 1.6), (g, 0.4 * a, 3)):
        rgba(cc, col, aa); cc.set_line_width(lw); cc.new_path()
        for i in range(121):
            xx = x + w * i / 120; e = math.sin(math.pi * i / 120)
            yy = y - amp * e * math.sin(i * 0.19 - t * 9) * (0.6 + 0.4 * math.sin(i * 0.31 + t * 5))
            (cc.move_to if i == 0 else cc.line_to)(xx, yy)
        cc.stroke()

def _check(c, x, y, kind):
    """task marks drawn as vectors: done = tick, run = triangle, no = cross, todo = dot"""
    if kind == 'done':
        rgba(c, GREY, 1); c.set_line_width(1.6); c.move_to(x, y - 5); c.line_to(x + 4, y - 1); c.line_to(x + 11, y - 10); c.stroke()
    elif kind == 'run':
        rgba(c, CYAN, 1); c.move_to(x + 1, y - 11); c.line_to(x + 11, y - 5.5); c.line_to(x + 1, y); c.close_path(); c.fill()
    elif kind == 'no':
        rgba(c, BONE, 0.9); c.set_line_width(1.6)
        c.move_to(x + 1, y - 10); c.line_to(x + 10, y - 1); c.move_to(x + 10, y - 10); c.line_to(x + 1, y - 1); c.stroke()
    else:
        rgba(c, GREY, 0.8); c.arc(x + 5, y - 5, 2, 0, 6.283); c.fill()

# ---------------------------------------------------------------- module bodies
def body(c, g, name, x, y, w, h, t, kk):
    X = x + 14; W_ = w - 28; yy = y + 46
    if name == 'POWER':
        _row(c, X, yy, W_, 'line', 'ON' if kk >= 3 else 'OFF', kk >= 3); _row(c, X, yy + 24, W_, 'current', 'DC', kk >= 3)
    elif name == 'SHIELD':
        on = kk >= 7
        _row(c, X, yy, W_, 'protection', 'ON' if on else 'OFF', on)
    elif name.startswith('CORE'):
        out_ = 0.0 if kk < 11 else 0.34 + 0.66 * eo_cubic(prog(t, B(32), B(40)))
        _row(c, X, yy, W_, 'output', f'{int(round(out_ * 100))} %', kk >= 11)
        _bar(c, X, yy + 10, W_, out_)
        _row(c, X, yy + 40, W_, 'limiter', 'ON', kk >= 11)
    elif name == 'DRIVE':
        v, M = drive_state(t, kk)
        light_ = kk >= 44
        _row(c, X, yy, W_, 'velocity', ('c' if kk >= 48 else f'{v:,.2f} m/s'.replace(',', ' ')) if kk >= 32 else '0.00 m/s', kk >= 32)
        _row(c, X, yy + 24, W_, 'mach', ('—' if kk >= 48 else f'{M:.2f}') if kk >= 32 else '0.00', kk >= 32)
        _bar(c, X, yy + 34, W_, min(1, M / 1.2) if kk < 48 else 1.0)
        bx = X + W_ / 1.2; rgba(c, RED, 0.9 if kk < 48 else 0.35); c.rectangle(bx - 1, yy + 28, 2, 17); c.fill()
        text(c, 'mono', 'M 1', bx, yy + 60, 11, RED, 0.8 if kk < 48 else 0.3, align='center')
        _row(c, X, yy + 88, W_, 'optics', 'ENGAGED' if light_ else 'standby', light_)
    elif name == 'SENSORS':
        vis = kk >= 23; aud = kk >= 35.7
        _row(c, X, yy, W_, 'vision', 'ON' if vis else 'OFF', vis)
        _row(c, X, yy + 24, W_, 'audio in', 'song' if aud else '—', aud, BONE, LISH if aud else CYAN)
        _row(c, X, yy + 48, W_, 'gyro', 'stable', kk >= 11)
    elif name == 'CLASS':
        if kk < 12: _row(c, X, yy, W_, 'me', 'null', False)
        else:
            s = 'new Lovable("Me", 0, true, -1, false);'
            typed = type_on(s, t, B(12.25), 0.026)
            text(c, 'mono', 'me =', X + 18, yy, 15, BONE, 0.85); _light(c, X + 6, yy - 5, True)
            for i, part in enumerate((typed[:12], typed[12:])):
                if part: text(c, 'mono', part.strip(), X + 18, yy + 26 + i * 22, 16, CYAN, 0.95)
            if kk >= 15:
                ui = eo_cubic(prog(t, B(15), B(15) + 0.2))
                c.save(); c.translate(0, 8 * (1 - ui)); _row(c, X, yy + 84, W_, 'instanceof', 'Lovable', True, CYAN); c.restore()
    elif name == 'CLOCK':
        on = kk >= 24
        hh = 23 * 3600 + 40 * 60 + max(0.0, t - B(24))
        _row(c, X, yy, W_, 'A.D. 2026', f'{int(hh // 3600):02d}:{int(hh // 60 % 60):02d}:{int(hh % 60):02d}' if on else '--:--:--', on)
    elif name == 'MEMORY':
        f = mem_fill(t) if kk >= 16 else 0.0
        _row(c, X, yy, W_, 'data', f'{int(round(f * 100))} %', kk >= 16); _bar(c, X, yy + 10, W_, f)
    elif name == 'LINK':
        if kk < 35.7:
            _row(c, X, yy, W_, 'source', '—', False); _row(c, X, yy + 24, W_, 'signal', 'none', False)
            line(c, X, yy + 52, X + W_, yy + 52, GREY, 0.5, 1.2)
        elif kk < 48 or kk >= 60:
            _row(c, X, yy, W_, 'source', 'LISHENNA', True, BONE, LISH)
            db = -32 + 6 * math.sin(t * 3.1) + 4 * pulse(t, B(math.floor(kk)), 0.3)
            _row(c, X, yy + 24, W_, 'signal', f'{db:.0f} dB', True, BONE, LISH)
            _wave(c, g, X, yy + 52, W_, 9 + 6 * pulse(t, B(math.floor(kk)), 0.3), t)
        else:                                                   # 22.5-28 s: Achilles -- target lock, never achieved
            d = achilles_d(t)
            _row(c, X, yy, W_, 'target', 'LISHENNA', True, BONE, LISH)
            _row(c, X, yy + 24, W_, 'd', f'{d:.6f}', True, CYAN)
            blink = int(t * 4) % 2 == 0
            _row(c, X, yy + 48, W_, 'lock', 'FAILED' if blink else '', True, BONE, GREY)
        _row(c, X, yy + 96, W_, 'touch', 'null', False, RED, GREY)
    elif name == 'TRANSMISSION':
        cur = [e for e in IN if e[0] <= t]
        if not cur:
            text(c, 'mono', '— no signal —', X, yy + 4, 14, GREY, 0.7)
        else:
            t0, s = cur[-1]
            typed = type_on(s, t, t0, 0.035)
            fresh = t - t0 < 4.0
            ws, lines_, cur_l = s.split(' '), [], ''
            for wd in typed.split(' '):
                if text_w('serifr', (cur_l + ' ' + wd).strip(), 24) > W_ - 10: lines_.append(cur_l); cur_l = wd
                else: cur_l = (cur_l + ' ' + wd).strip()
            lines_.append(cur_l)
            for i, l_ in enumerate(lines_[:3]): text(c, 'serifr', ('"' if i == 0 else '') + l_ + ('"' if i == len(lines_) - 1 and len(typed) == len(s) else ''), X, yy + 2 + i * 28, 24, BONE, 0.95 if fresh else 0.55)
            speaking = prog(t, t0, t0 + 0.035 * len(s) + 0.4)
            if 0 < speaking < 1: _wave(c, g, X, y + h - 22, W_, 7, t)
            else: line(c, X, y + h - 22, X + W_, y + h - 22, GREY, 0.5, 1.2)
    elif name == 'TASKS':
        rows = [(3, 'power.on()', 'done'), (7, 'protect()', 'done'), (11, 'assemble()', 'done'), (15, 'me = new Lovable()', 'done'),
                (23, 'init()', 'done'), (30, 'world.startSimulation()', 'done'), (32, 'run()', 'run', ''),
                (35.7, 'worship(Lishenna)', 'no', 'unauthorized'), (48, 'touch(you)', 'run', 'd → 0')]
        i = 0
        for k_, lab, kind, *note in rows:
            if kk < k_: continue
            ua = eo_cubic(prog(t, B(k_), B(k_) + 0.15))
            yr = yy - 4 + i * 24
            _check(c, X + 2, yr, kind)
            text(c, 'mono', lab, X + 22, yr, 14, BONE if kind in ('run',) else GREY, ua)
            if note and note[0]: text(c, 'mono', note[0], X + W_, yr, 12, GREY, 0.9 * ua, align='right')
            i += 1
    elif name == 'VOICE':
        lines_ = voice_lines(t)
        for i, (t0, ch, data) in enumerate(lines_):
            yr = y + 52 + i * 38
            age = len(lines_) - 1 - i
            a_ = 1.0 if age == 0 else 0.55 if age == 1 else 0.35
            if ch == 'IN':
                rgba(c, LISH, a_); c.rectangle(x + 8, yr - 14, 3, 18); c.fill()
            text(c, 'monom', ch, x + 18, yr, 14, CYAN if ch == 'OUT' else BONE, a_, track=0.15)
            text(c, 'mono', f'{int(t0 // 60):02d}:{t0 % 60:05.2f}', x + 70, yr, 13, GREY, 0.9 * a_)
            if ch == 'OUT':
                cx = x + 170
                for wd, ton in data:
                    u = eo_cubic(prog(t, ton, ton + 0.12))
                    big = wd.isupper() and len(wd) > 2
                    if u > 0: text(c, 'serif', wd, cx, yr + 3 + 6 * (1 - u), 26, BONE if not big else CYAN, a_ * u)
                    cx += text_w('serif', wd + ' ', 26)
            else:
                text(c, 'serifr', '"' + type_on(data, t, t0, 0.035) + '"', x + 170, yr + 3, 25, BONE, a_)
        past = [(tt, s) for tt, s in CODE_LOG if tt <= t]
        if past:
            tt, s = past[-1]
            text(c, 'mono', type_on('> ' + s, t, tt, 0.018), x + 18, y + h - 16, 14, CYAN, 0.8)

def top_bar(c, g, t):
    kk = (t - T0) / P
    if kk < 3: return
    u = eo_cubic(prog(t, B(3), B(3) + 0.3))
    rgba(c, INK, 0.92 * u); c.rectangle(0, 0, W, TOP_H); c.fill()
    line(c, 0, TOP_H, W, TOP_H, GREY, 0.35 * u, 1)
    text(c, 'monom', type_on('ŌMETEŌTL OS', t, B(3), 0.03), LX, 36, 18, BONE, 0.95 * u, track=0.2)
    if kk >= 4: text(c, 'mono', 'RALMIA / MACHINA   ·   unit 0x7E3   ·   SONIC RACER', LX + 175, 36, 15, GREY, 0.9 * eo_cubic(prog(t, B(4), B(4) + 0.3)), track=0.08)
    tc = f'{int(t // 60):02d}:{t % 60:05.2f}'
    text(c, 'mono', tc, W - LX, 36, 15, BONE, 0.8 * u, align='right')
    kb = math.floor(kk); x0 = W - LX - text_w('mono', tc, 15) - 30 - 4 * 16
    for i in range(4):
        on = (kb % 4 == i)
        aa = 0.25 + 0.75 * (pulse(t, B(kb), 0.5) if on else 0)
        rgba(c, CYAN if (on and i == 0) else BONE, aa * u); c.rectangle(x0 + i * 16, 22, 10, 10)
        if on: c.fill()
        else: c.set_line_width(1.2); c.stroke()

def modules(c, g, t, pv):
    kk = (t - T0) / P
    act = active_at(kk)
    for name, (x, y, w, h) in RECTS.items():
        tl = LAND[name]
        if t < tl - 0.12: continue
        u = prog(t, tl - 0.12, tl)
        dy = (500 if name == 'VOICE' else -600) * (1 - ei_cubic(u))   # dropped in, like the parts of 5 s
        land = prog(t, tl, tl + 0.14)
        sq = math.sin(land * math.pi) * (1 - land) * 6 if t >= tl else 0
        side = -1 if x < VP[0] else 1 if x > VP[0] + VP[2] else 0
        ox = side * 420 * (1 - pv); oy = (0 if side else 460 * (1 - pv)) + dy + sq
        if pv <= 0.001: continue
        c.save(); c.translate(ox, oy); g.save(); g.translate(ox, oy)
        _box(c, g, x, y, w, h, name if name != 'VOICE' else 'VOICE  ·  OUT / IN', act == name, t)
        body(c, g, name, x, y, w, h, t, kk)
        if t >= tl:
            fl = pulse(t, tl, 0.25)
            if fl > 0.03: rgba(g, CYAN, 0.6 * fl); g.set_line_width(4); g.rectangle(x, y, w, h); g.stroke()
        c.restore(); g.restore()

def render_v3(t, fr, scene, composite):
    pv = mode_at(t)
    kk = (t - T0) / P
    # a panel module appears before the first full panel switch only from its landing time on
    lib.REG[0] = reg_at(t)
    S.HUD_OFF[0] = True
    S.LYRICS_OFF[0] = pv > 0.5
    s1 = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c1 = cairo.Context(s1)
    gs1 = cairo.ImageSurface(cairo.FORMAT_ARGB32, W // 2, H // 2); g1 = cairo.Context(gs1); g1.scale(0.5, 0.5)
    try:
        fx = scene(c1, g1, t) or {}
    finally:
        lib.REG[0] = None; S.HUD_OFF[0] = False; S.LYRICS_OFF[0] = False
    s1.flush(); gs1.flush()
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    gs = cairo.ImageSurface(cairo.FORMAT_ARGB32, W // 2, H // 2); g = cairo.Context(gs); g.scale(0.5, 0.5)
    fill_bg(c, INK)
    if pv > 0.001:                                              # the panel's own faint grid
        for i in range(0, W, 48): line(c, i, 0, i, H, BONE, 0.022 * pv, 1)
        for j in range(0, H, 48): line(c, 0, j, W, j, BONE, 0.022 * pv, 1)
    # the scene: full frame at pv = 0, the viewport at pv = 1
    vx, vy, vw, vh = lerp(0, VP[0], pv), lerp(0, VP[1], pv), lerp(W, VP[2], pv), lerp(H, VP[3], pv)
    k = vw / W
    c.save(); c.rectangle(vx, vy, vw, vh); c.clip(); c.translate(vx, vy); c.scale(k, k)
    c.set_source_surface(s1, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint(); c.restore()
    g.save(); g.rectangle(vx, vy, vw, vh); g.clip(); g.translate(vx, vy); g.scale(k * 2, k * 2)
    g.set_source_surface(gs1, 0, 0); g.paint(); g.restore()
    if pv > 0.001:
        ub = eo_cubic(prog(t, B(0), B(1)))                      # the frame draws itself, corners first
        if ub > 0:
            rgba(c, CYAN, 0.7 * pv); c.set_line_width(1.4)
            for (px_, py_, sx, sy) in ((vx, vy, 1, 1), (vx + vw, vy, -1, 1), (vx, vy + vh, 1, -1), (vx + vw, vy + vh, -1, -1)):
                c.move_to(px_ + sx * vw / 2 * ub, py_); c.line_to(px_, py_); c.line_to(px_, py_ + sy * vh / 2 * ub)
            c.stroke()
            text(c, 'mono', 'VIEWPORT', vx, vy + vh + 18, 13, GREY, 0.8 * pv * ub, track=0.12)
    modules(c, g, t, pv)
    top_bar(c, g, t)
    s.flush(); gs.flush()
    buf = np.ndarray((H, W, 4), np.uint8, s.get_data())
    gbuf = np.ndarray((H // 2, W // 2, 4), np.uint8, gs.get_data())
    if pv > 0.5: fx = dict(fx); fx['vig'] = min(fx.get('vig', 1.0), 0.35)
    return composite(buf, gbuf, fr, fx)
