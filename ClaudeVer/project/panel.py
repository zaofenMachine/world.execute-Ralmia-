"""v3 (plan_v3.md): Ralmia's system -- ŌMETEŌTL OS -- around the scenes of v2.
render_v3(t, fr, scene, composite) draws the scene into its own buffers, then the panel, then puts the scene either full
frame or into the VIEWPORT (mode follows MODES), with the picture register (lib.REG) following REGS.
The sung lines and Lishenna's lines are in lyrics_v3.py; every module's state is a function of t (section 4 of the plan).
Phase 3 (plan_v3.md sections 5-6): the trial executes the modules one per call (LINK and TRANSMISSION do not take the
stamp), the 13th call overflows the counter and cages the core, releaseCoreLimit() crashes the system, it reboots as
ASTROWING (a module per 8th, k352-356); the outro shuts it down one bar at a time, protection OFF last (k440).
The chorus-3 rewind and the four-step colour ending are shots, in scenes_v3.py."""
from lib import *
import lib
import scenes as S
from codelog import CODE_LOG
from lyrics_v3 import OUT, IN, LOST, keyword, shown
import scenes3 as S3
import scenes5 as S5
import scenes7 as S7

V3_UNTIL = 999.0
VP = (360, 64, 1200, 675)                     # viewport x, y, w, h
LX, RX, COLW = 24, 1584, 312
TOP_H = 52
def kt(t): return (t - T0) / P               # seconds -> beats

# ---------------------------------------------------------------- what the frame is, when
# (k0, mode) -- 'full' or 'panel'; switches land on bar lines and take TR seconds. Panel for the verses and everything
# about the system; full for the choruses and the shots that are about the two of them (plan_v3.md section 2)
MODES = [(0, 'panel'), (40, 'full'), (48, 'panel'), (60, 'full'), (64, 'panel'),
         (128, 'full'),                       # chorus 1
         (160, 'panel'),                      # verse 2: eggplant .. god, the switches, the trance
         (224, 'full'),                       # chorus 2: VIBRATIONS, COMPLETION
         (240, 'panel'),                      # "you have left" x6, FRAGMENTS
         (272, 'full'),                       # "Challenging your god"
         (288, 'panel'),                      # the interlude, the trial (the viewport itself is executed at k342)
         (352, 'full'),                       # white -> the reboot, a module per 8th (reboot_montage)
         (356, 'panel'),                      # ASTROWING: the panel, rebuilt
         (358, 'full'),                       # the barrier again, chorus 3, the rewind, LOVE
         (416, 'panel'),                      # me.escape(world): the shutdown, one bar at a time
         (442, 'full')]                       # she leaps out of it
TR = 0.16
# (k0, register): 'auto' = each frame by its own ground (paper -> manga, ink -> raster); None = the pictures as they are
REGS = [(0, 'auto')]                  # full colour only at the very end (scenes_v3.escape_out_v3)
def mode_at(t):
    kk = kt(t); cur, k_on, prev = 'panel', -9, 'panel'
    for k, m in MODES:
        if kk >= k: prev, cur, k_on = cur, m, k
    u = eo_cubic(prog(t, B(k_on), B(k_on) + TR))
    a, b = (1.0 if prev == 'panel' else 0.0), (1.0 if cur == 'panel' else 0.0)
    return lerp(a, b, u)
def reg_at(t):
    kk = kt(t); r = None
    for k, v in REGS:
        if kk >= k: r = v
    return r

# ---------------------------------------------------------------- the boot: POWER and VOICE are there from the first
# beat, SHIELD comes with "protection"; the rest land one per 16th with the parts of "lay down your pieces" (k8.25..),
# the core last, with the core gem, on k11
LEFT = [('POWER', 84), ('SHIELD', 70), ('CORE  ŌMETEŌTL', 128), ('DRIVE', 150), ('SENSORS', 112), ('CLASS', 184),
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

# the module the current words are about is lit; the others step back
ACTIVE = [(0, 'POWER'), (4, 'SHIELD'), (8, None), (12, 'CLASS'), (16, 'MEMORY'), (21, 'SENSORS'), (24, 'CLOCK'),
          (28, 'TASKS'), (32, 'DRIVE'), (48, 'LINK'), (60, None),
          (64, 'CLASS'), (95, 'POWER'), (103, 'SENSORS'), (111.5, 'CLOCK'), (119, 'LINK'), (123, 'CORE  ŌMETEŌTL'), (128, None),
          (160, 'CLASS'), (202, 'CLOCK'), (207, 'CLASS'), (214.5, 'SENSORS'), (224, None),
          (240, 'LINK'), (256, 'MEMORY'), (272, None), (288, 'MEMORY'), (320, None)]
def active_at(kk):
    a = None
    for k, n in ACTIVE:
        if kk >= k: a = n
    return a

# ---------------------------------------------------------------- the keyword times the modules answer to
T_AC, T_DC = B(S3.K_AC), B(S3.K_DC)
T_BLIND, T_SEE = B(S3.K_BLIND), B(111.5)
DIZZY = (B(106.5), B(111.5))
T_TRAVEL, T_AD, T_BC = B(S3.K_TRAVEL), B(S3.K_AD), B(S3.K_BC)
T_UNITE, T_DEEP = B(S3.K_UNITE), B(S3.K_SO3)
T_LEFT = [B(k) for k in S5.LEFT]
T_FRAG, T_ILL = B(S5.K_FRAG), B(S5.K_ILL)
TRANCE = (99.42, 103.72)
T_TWELVE = B(192)                             # the clock goes to 12 hours for "from AM to PM"
T_AM, T_PM = 94.49, 95.42
CLASSES = [(B(66.5), 'PointSet', B(70.5), 'you.receive(dimension)'), (B(74), 'Circle', B(78.25), 'you.receive(circumference)'),
           (B(82), 'SineWave', B(87), 'you.sitOn(tangents)'), (B(89.5), 'Sequence', B(94), 'limit = you'),
           (75.18, 'Eggplant', 77.19, 'you.receive(nutrients)'), (78.78, 'Tomato', 80.65, 'you.receive(antioxidants)'),
           (82.50, 'TabbyCat', 84.57, 'me.purr(you)'), (86.42, 'God', 88.26, 'you == proof(me)')]
GENDER = [(90.57, 'F'), (91.49, 'M')]
ROLE = [(97.96, 'S'), (98.88, 'M')]
PACKET = ['3 s', '1 min', '1 h', '1 day', '1 month', '1 year']
# the interlude: her song seeps into the system, one module border every 2.5 beats (LINK is hers from the start)
SEEP = ['TASKS', 'CLOCK', 'DRIVE', 'SENSORS', 'CLASS', 'POWER', 'SHIELD', 'MEMORY', 'VOICE', 'TRANSMISSION', 'CORE  ŌMETEŌTL']
def seeped(name, t):
    if name == 'LINK': return t >= B(288)
    return name in SEEP and t >= B(288 + 2.5 * SEEP.index(name))

# ---- the trial (k320-342): one module per call. LINK and TRANSMISSION are hers -- the stamp slides off. the 12th
# call executes the viewport itself: its frame falls away and the count plays bare, round what is left (CORE, LINK)
EXE = [B(320 + 2 * i) for i in range(12)]
EXEC_ORDER = ['POWER', 'SHIELD', 'DRIVE', 'SENSORS', 'CLASS', 'CLOCK', 'MEMORY', 'TASKS', 'VOICE', 'LINK', 'TRANSMISSION', 'VIEWPORT']
IMMUNE = ('LINK', 'TRANSMISSION')
T_EX13, T_SNAP, T_CRASH, T_REBOOT = B(350), B(351), B(351.5), B(352)
COUNT_T = [B(344 + i) for i in range(6)]
def exe_t(name): return EXE[EXEC_ORDER.index(name)] if name in EXEC_ORDER else None
def trial_n(t): return sum(1 for e in EXE if t >= e)
def executed(name, t):
    """0 alive; (0, 1] stamped and falling; > 1 gone. None for the ones that can't be executed"""
    te = exe_t(name)
    if te is None or name in IMMUNE or not (te <= t < T_REBOOT): return 0.0
    return 1e-3 + prog(t, te + P, te + P + 0.55) * 1.001      # the stamp, a beat of it, then down it goes
def astro(t): return t >= T_REBOOT

# ---- the reboot (k352-356): white, then a restored module per 8th note
MONTAGE = ['CORE  ŌMETEŌTL', 'POWER', 'SHIELD', 'DRIVE', 'SENSORS', 'CLASS', 'LINK', 'TOPBAR']

# ---- the shutdown (k416-443), the boot backwards: one bar at a time the system folds away; protection OFF last
SHUT = {'SENSORS': B(420), 'DRIVE': B(420), 'CLASS': B(424), 'CLOCK': B(424), 'MEMORY': B(424),
        'VOICE': B(428), 'TRANSMISSION': B(428), 'POWER': B(432), 'CORE  ŌMETEŌTL': B(432), 'SHIELD': B(440.75),
        'LINK': B(441.5), 'TASKS': B(441.5)}
T_FRAME = B(436)                               # the frame cracks (v2's PEEL[4]): the shot goes bare
T_PROT_OFF = B(440)                            # 203.4 s: "Remember to put on PROTECTION" -- she turns it off herself
def folded(name, t):
    ts = SHUT.get(name)
    return 0.0 if ts is None or t < ts else prog(t, ts, ts + 0.45)

def last(table, t, default=None):
    v = default
    for t0, x in table:
        if t >= t0: v = x
    return v
def lost(t): return any(a <= t < b for a, b in LOST)

# ---------------------------------------------------------------- 22.5-28 s (plan_v3_chase.md, A): at c her own clock
# stops. Her modules hold the instant she reached it; only what is Lishenna's -- LINK, TRANSMISSION and her lines in
# VOICE -- goes on in the world's time. The panel comes back live after the title (k64).
FREEZE = (B(48), B(60))
FREEZE_T = B(48) + 0.16
LIVE = ('LINK', 'TRANSMISSION', 'VOICE')
def frozen(t): return FREEZE[0] <= t < FREEZE[1]
def own_t(t, name=None):
    return FREEZE_T if frozen(t) and name not in LIVE else t
def voice_lines(t):
    ev = [(ws[0][1], 'OUT', ws) for ws in OUT] + [(t0, 'IN', s) for t0, s in IN]
    return sorted([e for e in ev if e[0] <= t], key=lambda e: e[0])[-5:]

# ---------------------------------------------------------------- module states (all from t)
def drive_state(t, kk):
    import scenes2 as S2
    if 352 <= kk < 368:                        # ASTROWING: the barrier again (k358), then past light
        if kk < 360: M = lerp(0.9, 1.0, eo_cubic(prog(t, B(352), B(358)))) if kk < 358 else S7.m3(kk)
        else: M = S7.beta3(kk) * 881000.0
        return M * 340.29, M
    if kk >= 368 and kk < 416: return 299792458.0, 881000.0
    if kk < 32 or kk >= 64: return 0.0, 0.0
    if kk < 36:
        v = 0.0
        for kb, val in [(32, 0.0), (33, 85.07), (34, 170.15), (35, 255.22), (35.5, 340.29)]:
            if t >= B(kb): v = lerp(v, val, eo_cubic(prog(t, B(kb), B(kb) + 0.12)))
        return v, v / 340.29
    if kk < 48:
        M = S2.mach_of(min(t, B(47.99))); return M * 340.29, M
    return 299792458.0, 881000.0

def mem_fill(t):
    lv = math.floor(prog(t, B(17), B(18)) * 8) / 8
    return 1.0 if t >= B(18) else eo_cubic(lv)

def year_of(t):
    if t < T_TRAVEL: return 'A.D. 2026'
    if t < T_AD: return f'A.D. {int(round(lerp(2026, 617, eio_cubic(prog(t, T_TRAVEL, T_AD)))))}'
    if t < T_BC:
        v = int(round(lerp(617, -3691, eio_cubic(prog(t, T_AD + 0.12, T_BC)))))
        return f'A.D. {v}' if v > 0 else f'B.C. {max(1, -v)}'
    return 'B.C. 3691'

def clock_of(t):
    s_ = 23 * 3600 + 40 * 60 + max(0.0, t - B(24))
    h_, m_, sec = int(s_ // 3600) % 24, int(s_ // 60 % 60), int(s_ % 60)
    if t < T_TWELVE: return f'{h_:02d}:{m_:02d}:{sec:02d}'
    ampm = 'AM' if T_AM <= t < T_PM else 'PM'
    return f'{(h_ - 1) % 12 + 1:02d}:{m_:02d}:{sec:02d} {ampm}'

# ---------------------------------------------------------------- drawing helpers
def _box(c, g, x, y, w, h, title, active, t, name=''):
    rgba(c, INK2, 0.97); c.rectangle(x, y, w, h); c.fill()
    kk = kt(t)
    bl = pulse(t, B(math.floor(kk)), 0.35) if active else 0.0
    sp = seeped(name, t) and not astro(t)
    col = CYAN if active else LISH if (sp or astro(t)) else GREY
    rgba(c, col, (0.75 + 0.25 * bl) if active else 0.65 if sp else 0.5 if astro(t) else 0.4)
    c.set_line_width(1.4 if (active or sp or astro(t)) else 1.0)
    c.rectangle(x + 0.5, y + 0.5, w - 1, h - 1); c.stroke()
    rgba(c, LISH if astro(t) else col, 1); c.rectangle(x, y, 4, 22); c.fill()
    if astro(t): rgba(c, CYAN, 1); c.rectangle(x, y + 22, 4, 10); c.fill()
    if (active and bl > 0.05):
        rgba(g, col, 0.35 * bl); g.set_line_width(3); g.rectangle(x, y, w, h); g.stroke()
    if sp and name != 'LINK' and t < B(288 + 2.5 * SEEP.index(name)) + 0.3:   # the moment it turns
        f_ = 1 - prog(t, B(288 + 2.5 * SEEP.index(name)), B(288 + 2.5 * SEEP.index(name)) + 0.3)
        rgba(g, LISH, 0.7 * f_); g.set_line_width(5); g.rectangle(x, y, w, h); g.stroke()
    text(c, 'monom', title, x + 14, y + 17, 15, BONE if active else GREY, 0.95, track=0.18)

def _stamp(c, cx, cy, w, a, rot=-0.12):
    """the trial's EXECUTED, as on the gates (scenes6.stamp)"""
    if a <= 0: return
    c.save(); c.translate(cx, cy); c.rotate(rot)
    c.new_path(); fonts()['heavy'].text_path(c, 'EXECUTED', 0, w * 0.06, w * 0.16, 'center')
    rgba(c, INK, 0.9 * a); c.set_line_width(max(2, w * 0.016)); c.stroke_preserve(); rgba(c, BONE, a); c.fill()
    c.restore()

def _light(c, x, y, on, col=CYAN):
    rgba(c, col if on else GREY, 1 if on else 0.35); c.arc(x, y, 4.5, 0, 6.283); c.fill()

def _row(c, x, y, w, label, value, on=True, vcol=BONE, dot=CYAN, key='monom'):
    _light(c, x + 6, y - 5, on, dot)
    text(c, 'mono', label, x + 18, y, 16, BONE if on else GREY, 0.85 if on else 0.6)
    if value: text(c, key, value, x + w - 4, y, 16, vcol if on else GREY, 0.95, align='right')

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

# the task list: (shown from, label, [(from, mark, note), ...])
TASKS = [(B(3), 'power.on()', [(0, 'done', '')]), (B(7), 'protect()', [(0, 'done', '')]), (B(11), 'assemble()', [(0, 'done', '')]),
         (B(15), 'me = new Lovable()', [(0, 'done', '')]), (B(23), 'init()', [(0, 'done', '')]),
         (B(30), 'world.startSimulation()', [(0, 'done', '')]), (B(32), 'run()', [(0, 'run', '')]),
         (B(35.7), 'worship(Lishenna)', [(0, 'no', 'unauthorized')]),
         (B(48), 'touch(you)', [(0, 'no', 'Δτ = 0'), (T_UNITE, 'done', 'true'), (LOST[0][0], 'no', 'signal lost')]),
         (120.24, 'erase(fragments)', [(0, 'run', ''), (T_FRAG, 'no', 'denied')]),
         (T_ILL, 'argue(god)', [(0, 'no', 'illegal')]),
         (147.9, 'trial.destruction', [(0, 'no', 'not listed')])]
TASKS_A = [(B(352.1), 'reboot("ASTROWING")', [(0, 'done', '')]), (B(352.1), 'releaseCoreLimit()', [(0, 'done', '')]),
           (B(352.1), 'run()', [(0, 'run', '')]), (B(352.1), 'worship(Lishenna)', [(0, 'no', 'unauthorized')]),
           (B(352.1), 'touch(you)', [(0, 'todo', 'd → 0')]), (B(371.5), 'bring(you).back()', [(0, 'done', '')]),
           (B(390), 'receive(song)', [(0, 'done', '')]), (B(416), 'escape(world)', [(0, 'run', '')])]

# ---------------------------------------------------------------- module bodies
def body(c, g, name, x, y, w, h, t, kk):
    X = x + 14; W_ = w - 28; yy = y + 46
    if name == 'POWER':
        ac = T_AC <= t < T_DC
        _row(c, X, yy, W_, 'line', 'ON' if kk >= 3 else 'OFF', kk >= 3)
        _row(c, X, yy + 24, W_, 'current', 'AC' if ac else 'DC', kk >= 3, CYAN if T_AC <= t < T_DC + 0.6 else BONE)
        if ac:
            rgba(c, CYAN, 0.9); c.set_line_width(1.5); c.new_path()
            for i in range(41): (c.move_to if i == 0 else c.line_to)(X + 150 + i * 2.2, yy + 19 - 6 * math.sin(i * 0.45 - t * 14))
            c.stroke()
    elif name == 'SHIELD':
        on = kk >= 7 and t < T_PROT_OFF
        _row(c, X, yy, W_, 'protection', 'ON' if on else 'OFF', on, CYAN if T_PROT_OFF <= t < T_PROT_OFF + 1.2 else BONE)
    elif name.startswith('CORE') and (t >= T_SNAP):            # releaseCoreLimit(): no ceiling any more
        if t < T_REBOOT:
            text(c, 'monom', type_on('me.releaseCoreLimit();', t, T_SNAP, 0.02), X + 4, yy, 16, CYAN, 0.95)
            _row(c, X, yy + 40, W_, 'limiter', 'OFF', True, CYAN)
        else:
            _row(c, X, yy, W_, 'output', 'unbound', True, CYAN)
            _bar(c, X, yy + 10, W_, 0.82 + 0.18 * pulse(t, B(math.floor(kk)), 0.4), CYAN)
            _row(c, X, yy + 40, W_, 'limiter', 'OFF', True, CYAN)
            _row(c, X, yy + 64, W_, 'tuned to', 'song', True, BONE, LISH)
    elif name.startswith('CORE'):
        out_ = 0.0 if kk < 11 else 0.34 + 0.66 * eo_cubic(prog(t, B(32), B(40)))
        _row(c, X, yy, W_, 'output', f'{int(round(out_ * 100))} %', kk >= 11)
        _bar(c, X, yy + 10, W_, out_)
        _row(c, X, yy + 40, W_, 'limiter', 'ON', kk >= 11)
        if t >= T_DEEP:                                         # "so deeply": her song, into the core
            _row(c, X, yy + 64, W_, 'tuned to', 'song', True, BONE, LISH)
    elif name == 'DRIVE':
        v, M = drive_state(t, kk)
        light_ = 44 <= kk < 64
        going = 32 <= kk < 64 or 352 <= kk < 416
        at_c = 48 <= kk < 64 or 360 <= kk < 416
        if 360 <= kk < 368: vs, ms = f'{S7.beta3(kk):.5f} c', '—'
        else: vs, ms = ('c' if at_c else f'{v:,.2f} m/s'.replace(',', ' ')), ('—' if at_c else f'{M:.2f}')
        _row(c, X, yy, W_, 'velocity', vs, going)
        _row(c, X, yy + 24, W_, 'mach', ms, going)
        _bar(c, X, yy + 34, W_, 1.0 if at_c else min(1, M / 1.2))
        before = kk < 48 or 352 <= kk < 358
        bx = X + W_ / 1.2; rgba(c, RED, 0.9 if before else 0.35); c.rectangle(bx - 1, yy + 28, 2, 17); c.fill()
        text(c, 'mono', 'M 1', bx, yy + 60, 12, RED, 0.8 if before else 0.3, align='center')
        if astro(t): _row(c, X, yy + 88, W_, 'optics', 'sublimated', True, CYAN)
        else: _row(c, X, yy + 88, W_, 'optics', 'ENGAGED' if light_ else 'standby', light_)
    elif name == 'SENSORS':
        vis = kk >= 23 and not (T_BLIND <= t < T_SEE)
        aud = kk >= 35.7 and not lost(t)
        trance = TRANCE[0] <= t < TRANCE[1]
        _row(c, X, yy, W_, 'vision', 'ON' if vis else 'OFF', vis)
        _row(c, X, yy + 24, W_, 'audio in', ('hum  100 %' if trance else 'song') if aud else '—', aud, BONE, LISH if aud else CYAN)
        if trance: _bar(c, X + 18, yy + 32, W_ - 18, 0.6 + 0.4 * pulse(t, B(math.floor(kk)), 0.4), LISH)
        if DIZZY[0] <= t < DIZZY[1]:
            ang = 37 * math.sin((t - DIZZY[0]) * 7.3) * math.sin(math.pi * prog(t, *DIZZY))
            _row(c, X, yy + 52, W_, 'gyro', f'drift {ang:+05.1f}°', True, CYAN)
        else:
            _row(c, X, yy + 52, W_, 'gyro', 'stable', kk >= 11)
    elif name == 'CLASS':
        if kk < 12: _row(c, X, yy, W_, 'me', 'null', False)
        elif kk < 64.5 or t < CLASSES[0][0]:
            s = 'new Lovable("Me", 0, true, -1, false);'
            typed = type_on(s, t, B(12.25), 0.026)
            text(c, 'mono', 'me =', X + 18, yy, 15, BONE, 0.85); _light(c, X + 6, yy - 5, True)
            for i, part in enumerate((typed[:12], typed[12:])):
                if part: text(c, 'mono', part.strip(), X + 18, yy + 26 + i * 22, 16, CYAN, 0.95)
            if kk >= 15:
                ui = eo_cubic(prog(t, B(15), B(15) + 0.2))
                c.save(); c.translate(0, 8 * (1 - ui)); _row(c, X, yy + 84, W_, 'instanceof', 'Lovable', True, CYAN); c.restore()
        elif astro(t):                                          # the card she evolves into
            _row(c, X, yy, W_, 'me instanceof', scramble('Astrowing', t, T_REBOOT + 0.05, 0.03), True, CYAN)
            text(c, 'mono', type_on('me.evolve();  // the trial survived', t, T_REBOOT + 0.3, 0.02), X + 18, yy + 28, 15, CYAN, 0.75)
        else:                                                   # what she is now: the song's own `me instanceof ...`
            cur = [e for e in CLASSES if t >= e[0]]
            t0, typ, t1, code = cur[-1]
            _row(c, X, yy, W_, 'me instanceof', scramble(typ, t, t0, 0.025), True, CYAN)
            if t >= t1: text(c, 'mono', type_on(code, t, t1, 0.02), X + 18, yy + 28, 15, CYAN, 0.75)
            if t >= 88.98:
                _row(c, X, yy + 64, W_, 'gender', last(GENDER, t, '—'), True, CYAN if 90.57 <= t < 92.1 else BONE)
            if t >= 96.08:
                _row(c, X, yy + 88, W_, 'role', last(ROLE, t, '—'), True, CYAN if 97.96 <= t < 99.4 else BONE)
    elif name == 'CLOCK':
        on = kk >= 24
        yr = year_of(t) if not astro(t) else 'A.D. 2026'
        spinning = T_TRAVEL <= t < T_BC + 0.3
        _row(c, X, yy, W_, yr, clock_of(t) if on else '--:--:--', on, CYAN if (T_AM <= t < T_PM + 0.6) else BONE)
        if spinning: rgba(c, CYAN, 0.6); c.rectangle(X + 18, yy + 8, text_w('mono', yr, 16), 2); c.fill()
    elif name == 'MEMORY':
        f = mem_fill(t) if kk >= 16 else 0.0
        _row(c, X, yy, W_, 'data', f'{int(round(f * 100))} %', kk >= 16); _bar(c, X, yy + 10, W_, f)
        if astro(t):                                              # the song is part of her now
            _row(c, X, yy + 40, W_, 'song', '100 %', True, BONE, LISH); _bar(c, X, yy + 50, W_, 1.0, LISH)
        elif 120.24 <= t < B(288):                               # FRAGMENTS: she cannot delete them
            n = 1 + max(0, math.floor((kt(t) - S5.K_FRAG) / 2)) if t >= T_FRAG else 0
            blink = t >= T_FRAG and (int(t * 6) % 2 == 0 or t >= B(272))
            _row(c, X, yy + 40, W_, 'erase(fragments)', (f'denied ×{min(n, 5)}' if n else '...') if (blink or not n) else '', True,
                 BONE, CYAN)
        elif t >= B(288):                                         # the interlude: her song corrupts the data
            pc = 12 + 76 * min(1.0, math.floor((kt(t) - 288) / 2) / 15)
            _row(c, X, yy + 40, W_, 'corrupted', f'{int(pc)} %', True, BONE, LISH); _bar(c, X, yy + 50, W_, pc / 100, LISH)
    elif name == 'LINK':
        if kk < 35.7:
            _row(c, X, yy, W_, 'source', '—', False); _row(c, X, yy + 24, W_, 'signal', 'none', False)
            line(c, X, yy + 52, X + W_, yy + 52, GREY, 0.5, 1.2)
        elif lost(t):                                             # "you have left": the last packet gets older
            i = sum(1 for tl in T_LEFT if t >= tl) - 1
            _row(c, X, yy, W_, 'source', '—', False)
            _row(c, X, yy + 24, W_, 'signal', 'lost', True, BONE, GREY)
            line(c, X, yy + 52, X + W_, yy + 52, GREY, 0.6, 1.2)
            if i >= 0:
                fl = pulse(t, T_LEFT[i], 0.3)
                _row(c, X, yy + 86, W_, 'last packet', PACKET[i] + ' ago', True, BONE if fl < 0.1 else CYAN, GREY)
        else:
            _row(c, X, yy, W_, 'source', 'LISHENNA', True, BONE, LISH)
            db = -32 + 6 * math.sin(t * 3.1) + 4 * pulse(t, B(math.floor(kk)), 0.3)
            _row(c, X, yy + 24, W_, 'signal', f'{db:.0f} dB', True, BONE, LISH)
            _wave(c, g, X, yy + 52, W_, 9 + 6 * pulse(t, B(math.floor(kk)), 0.3), t)
            if frozen(t):                                       # the one module still running
                text(c, 'mono', 'live  ·', X + 18, yy + 86, 15, BONE, 0.7); text(c, 'math', 'Δt ≠ 0', X + 86, yy + 87, 17, BONE, 0.7)
        te = exe_t('LINK')
        if te <= t < te + 2 * P:                                  # the stamp would not take
            text(c, 'mono', 'immune', X + 18, yy + 86, 15, BONE, 0.9); text(c, 'mono', 'not destroyed by effects', X + W_, yy + 86, 12, GREY, 0.9, align='right')
        touch = T_UNITE <= t < LOST[0][0]
        _row(c, X, yy + 130, W_, 'touch', 'true' if touch else 'null', touch, RED, RED if touch else GREY)
        if touch and t < T_UNITE + 0.5:
            fl = 1 - prog(t, T_UNITE, T_UNITE + 0.5); rgba(g, RED, 0.6 * fl); g.set_line_width(4); g.rectangle(x, y + 110, w, 40); g.stroke()
    elif name == 'TRANSMISSION':
        cur = [e for e in IN if e[0] <= t]
        if lost(t):
            text(c, 'mono', '— signal lost —', X, yy + 4, 15, GREY, 0.7)
            line(c, X, y + h - 22, X + W_, y + h - 22, GREY, 0.5, 1.2)
        elif not cur:
            text(c, 'mono', '— no signal —', X, yy + 4, 15, GREY, 0.7)
        else:
            t0, s = cur[-1]
            typed = type_on(s, t, t0, 0.035)
            fresh = t - t0 < 4.0
            lines_, cur_l = [], ''
            for wd in typed.split(' '):
                if text_w('serifr', (cur_l + ' ' + wd).strip(), 24) > W_ - 10: lines_.append(cur_l); cur_l = wd
                else: cur_l = (cur_l + ' ' + wd).strip()
            lines_.append(cur_l)
            for i, l_ in enumerate(lines_[:3]): text(c, 'serifr', ('"' if i == 0 else '') + l_ + ('"' if i == len(lines_) - 1 and len(typed) == len(s) else ''), X, yy + 2 + i * 28, 24, BONE, 0.95 if fresh else 0.55)
            speaking = prog(t, t0, t0 + 0.035 * len(s) + 0.4)
            if 0 < speaking < 1: _wave(c, g, X, y + h - 22, W_, 7, t)
            else: line(c, X, y + h - 22, X + W_, y + h - 22, GREY, 0.5, 1.2)
    elif name == 'TASKS':
        i = 0
        rows = [r for r in (TASKS_A if astro(t) else TASKS) if t >= r[0]][-21:]
        if t >= B(428):                                           # the shutdown: everything goes but one
            keep = 'touch(you)'
            rows = [r for j, r in enumerate(rows) if r[1] == keep or t < B(428) + 0.12 * (len(rows) - j)]
        for t_on, lab, states in rows:
            kind, note = 'todo', ''
            for t_s, k_, n_ in states:
                if t >= t_s: kind, note = k_, n_
            if lab == 'trial.destruction' and t >= EXE[0]:
                kind, note = 'run', f'{min(trial_n(t), 12):02d} / 12'
            t_ch = max(t_s for t_s, _, _ in states if t >= t_s)
            ua = eo_cubic(prog(t, t_on, t_on + 0.15))
            fl = pulse(t, t_ch, 0.4) if t_ch > 0 else 0
            yr = yy - 4 + i * 24
            _check(c, X + 2, yr, kind)
            text(c, 'mono', lab, X + 22, yr, 15, BONE if (kind == 'run' or fl > 0.1) else GREY, ua)
            if note:
                ncol = RED if note == 'true' else BONE if fl > 0.1 else GREY
                text(c, 'math' if 'τ' in note else 'mono', note, X + W_, yr, 15 if 'τ' in note else 13, ncol, 0.9 * ua, align='right')
            i += 1
    elif name == 'VOICE':
        lines_ = voice_lines(t)
        for i, (t0, ch, data) in enumerate(lines_):
            yr = y + 52 + i * 38
            age = len(lines_) - 1 - i
            a_ = 1.0 if age == 0 else 0.55 if age == 1 else 0.35
            if ch == 'IN':
                rgba(c, LISH, a_); c.rectangle(x + 8, yr - 14, 3, 18); c.fill()
            text(c, 'monom', ch, x + 18, yr, 15, CYAN if ch == 'OUT' else BONE, a_, track=0.15)
            text(c, 'mono', f'{int(t0 // 60):02d}:{t0 % 60:05.2f}', x + 70, yr, 14, GREY, 0.9 * a_)
            if ch == 'OUT':
                cx = x + 170
                for wd, ton in data:
                    u = eo_cubic(prog(t, ton, ton + 0.12)); ws_ = shown(wd)
                    if u > 0: text(c, 'serif', ws_, cx, yr + 3 + 6 * (1 - u), 26, CYAN if keyword(wd) else BONE, a_ * u)
                    cx += text_w('serif', ws_ + ' ', 26)
            else:
                text(c, 'serifr', '"' + type_on(data, t, t0, 0.035) + '"', x + 170, yr + 3, 25, BONE, a_)
        tc_ = own_t(t)                                          # her code line holds with her
        past = [(tt, s) for tt, s in CODE_LOG if tt <= tc_]
        if past:
            tt, s = past[-1]
            text(c, 'mono', type_on('> ' + s, tc_, tt, 0.018), x + 18, y + h - 16, 15, CYAN, 0.8)

def top_bar(c, g, t, pv):
    hold = frozen(t); t = own_t(t)
    kk = kt(t)
    if kk < 3 or pv <= 0.001: return
    u = eo_cubic(prog(t, B(3), B(3) + 0.3))
    c.save(); c.translate(0, -(TOP_H + 4) * (1 - pv))
    rgba(c, INK, 0.92 * u); c.rectangle(0, 0, W, TOP_H); c.fill()
    line(c, 0, TOP_H, W, TOP_H, GREY, 0.35 * u, 1)
    text(c, 'monom', type_on('ŌMETEŌTL OS', t, B(3), 0.03), LX, 36, 18, BONE, 0.95 * u, track=0.2)
    if kk >= 4:
        form = 'ASTROWING' if astro(t) else 'SONIC RACER'
        text(c, 'mono', f'RALMIA / MACHINA   ·   unit 0x7E3   ·   {form}', LX + 175, 36, 15, BONE if astro(t) and t < T_REBOOT + 3 else GREY,
             0.9 * eo_cubic(prog(t, B(4), B(4) + 0.3)), track=0.08)
        if astro(t): rgba(c, LISH, 0.9); c.rectangle(LX + 175 + text_w('mono', 'RALMIA / MACHINA   ·   unit 0x7E3   ·   ', 15, 0.08), 42, text_w('mono', form, 15, 0.08), 2); c.fill()
    trial_bar(c, g, t)
    tc = f'{int(t // 60):02d}:{t % 60:05.2f}'
    text(c, 'mono', tc, W - LX, 36, 15, BONE, 0.8 * u, align='right')
    kb = math.floor(kk); x0 = W - LX - text_w('mono', tc, 15) - 30 - 4 * 16
    for i in range(4):
        on = (kb % 4 == i)
        aa = 0.25 + 0.75 * (pulse(t, B(kb), 0.5) if on else 0)
        rgba(c, CYAN if (on and i == 0) else BONE, aa * u); c.rectangle(x0 + i * 16, 22, 10, 10)
        if on: c.fill()
        else: c.set_line_width(1.2); c.stroke()
    if hold:
        x1 = x0 - 24
        text(c, 'math', 'Δτ = 0', x1, 37, 19, CYAN, 0.95, align='right')
        text(c, 'monom', 'HOLD', x1 - text_w('math', 'Δτ = 0', 19) - 14, 36, 15, CYAN, 0.95, align='right', track=0.2)
    c.restore()

def trial_bar(c, g, t):
    """k320-352: TRIAL nn / 12, twelve cells; the 13th call has no cell -- it overflows"""
    if not (EXE[0] - 0.05 <= t < T_REBOOT): return
    n = trial_n(t); over = t >= T_EX13
    cw, gap = 26, 6; x0 = 960 - (12 * cw + 11 * gap) / 2; y0 = 18
    for i in range(12):
        x = x0 + i * (cw + gap)
        if i < n:
            fl = pulse(t, EXE[i], 0.3)
            rgba(c, BONE, 0.85 + 0.15 * fl); c.rectangle(x, y0, cw, 16); c.fill()
            if fl > 0.05: rgba(g, BONE, 0.6 * fl); g.rectangle(x, y0, cw, 16); g.fill()
        else:
            rgba(c, BONE, 0.4); c.set_line_width(1.2); c.rectangle(x + 0.5, y0 + 0.5, cw - 1, 15); c.stroke()
    if over:                                                     # a thirteenth cell, outside the bar, glitching
        jit = 3 * math.sin(t * 97); x = x0 + 12 * (cw + gap) + jit
        if int(t * 20) % 3: rgba(c, BONE, 0.95); c.rectangle(x, y0, cw, 16); c.fill()
        text(c, 'monom', '13 > 12   OVERFLOW', x0 - 24, 32, 17, BONE, 0.95, align='right', track=0.12)
    else:
        text(c, 'monom', f'TRIAL  {min(n, 12):02d} / 12', x0 - 24, 32, 17, BONE, 0.95, align='right', track=0.12)

def in_toast(c, g, t, pv):
    """full frame: Lishenna's line still comes in, small, top right -- the v2 lyrics sit left and low in these shots
    (the panel's TRANSMISSION is off screen)"""
    a = 1 - pv * 2
    if a <= 0: return
    cur = [e for e in IN if e[0] <= t < e[0] + 3.6]
    if not cur or lost(t): return
    t0, s = cur[-1]
    u = eo_cubic(prog(t, t0, t0 + 0.2)) * (1 - prog(t, t0 + 3.2, t0 + 3.6)) * a
    y = 96; x = W - 64 - 50 - text_w('serifr', '"' + s + '"', 32)
    rgba(c, LISH, u); c.rectangle(x, y - 22, 3, 28); c.fill()
    text(c, 'monom', 'IN', x + 14, y - 1, 15, BONE, 0.9 * u, track=0.15)
    f = fonts()['serifr']; typed = '"' + type_on(s, t, t0, 0.035) + '"'
    c.new_path(); f.text_path(c, typed, x + 50, y + 2, 32)
    rgba(c, INK, 0.8 * u); c.set_line_width(6); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    rgba(c, BONE, u); c.fill()
    if prog(t, t0, t0 + 0.035 * len(s) + 0.4) < 1: _wave(c, g, x + 50, y + 22, 260, 5, t, u)

BOOT = [(0.5, 'ŌMETEŌTL BIOS 3.0'), (0.75, 'unit .............. 0x7E3'), (1.0, 'memory ............ 0 / 4096 KB'),
        (1.5, 'core .............. found'), (2.0, 'power line ........ '), (2.5, 'parts ............. 0 / 12'),
        (3.0, 'shield ............ standby'), (3.25, 'optics ............ standby'), (3.5, 'link .............. no signal')]
def boot_log(c, t, pv):
    if t >= B(4.5) or pv < 0.5: return
    a = 1 - eo_cubic(prog(t, B(4), B(4.5)))
    x, y = VP[0] + 28, VP[1] + 446          # under the power line, where the shot is empty
    for i, (k, s_) in enumerate(BOOT):
        if t < B(k): break
        if s_.startswith('power line'): s_ += 'OK' if t >= B(3) else '...'
        text(c, 'mono', type_on(s_, t, B(k), 0.012), x, y + i * 24, 15, BONE if i == 0 else GREY, 0.85 * a)
    if int(t * 4) % 2 == 0 and t < B(4): rgba(c, BONE, 0.7 * a); c.rectangle(x, y + min(len(BOOT), sum(1 for k, _ in BOOT if t >= B(k))) * 24 - 13, 9, 15); c.fill()

def dimmed(name, act, t, kk):
    """the modules the current keyword is not about step back, so the eye goes to the lit one"""
    if act is None or name == act or name == 'VOICE': return False
    if name == 'TRANSMISSION' and any(t0 <= t < t0 + 4.0 for t0, _ in IN): return False
    if name == 'LINK' and (35.7 <= kk < 38 or T_UNITE <= t < T_UNITE + 2): return False
    if name == 'TASKS' and any(abs(t - t_s) < 1.0 for r in TASKS for t_s, _, _ in r[2] if t_s > 0): return False
    return True

def modules(c, g, t, pv):
    act = active_at(kt(own_t(t)))
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
        ex = executed(name, t); fo = folded(name, t)
        if ex > 1 or fo >= 1: continue
        if ex > 0:                                              # down it goes, turning a little
            fu = ei_cubic(min(1, ex)); ox += (-1 if x < W / 2 else 1) * 60 * fu; oy += 1300 * fu
        c.save(); c.translate(ox, oy); g.save(); g.translate(ox, oy)
        if ex > 0:
            for cc in (c, g): cc.translate(x + w / 2, y + h / 2); cc.rotate((0.25 if x < W / 2 else -0.25) * ei_cubic(min(1, ex))); cc.translate(-x - w / 2, -y - h / 2)
        if fo > 0:                                              # the shutdown: folded flat into its title line
            for cc in (c, g): cc.translate(0, y); cc.scale(1, 1 - ei_cubic(fo)); cc.translate(0, -y)
        tm = own_t(t, name); kk = kt(tm)
        if name == 'TASKS' and t >= B(429):                     # one task left: the list shrinks to it
            h = lerp(h, 84, eio_cubic(prog(t, B(429), B(430))))
        _box(c, g, x, y, w, h, name if name != 'VOICE' else 'VOICE  ·  OUT / IN', act == name, tm, name)
        body(c, g, name, x, y, w, h, tm, kk)
        if dimmed(name, act, t, kk): rgba(c, INK, 0.42); c.rectangle(x, y, w, h); c.fill()
        te = exe_t(name)
        if te is not None and te <= t < T_REBOOT and name != 'VIEWPORT':
            if name in IMMUNE:                                  # her: the stamp lands -- and slides off
                v = ei_cubic(prog(t, te + 0.11, te + 0.45))
                c.save(); c.translate(x + w / 2 + 80 * v, y + h / 2 + 700 * v * v); c.rotate(0.9 * v); c.translate(-x - w / 2, -y - h / 2)
                _stamp(c, x + w / 2, y + h / 2, w * 0.95, eo_expo(prog(t, te, te + 0.08)) * (1 - v)); c.restore()
                rp = prog(t, te, te + 0.8)
                if 0 < rp < 1:
                    for cc, aa, lw in ((c, 0.8, 2), (g, 0.5, 5)):
                        rgba(cc, LISH, aa * (1 - rp)); cc.set_line_width(lw); cc.rectangle(x - 40 * rp, y - 40 * rp, w + 80 * rp, h + 80 * rp); cc.stroke()
            else:
                rgba(c, INK, 0.55 * eo_cubic(prog(t, te, te + 0.15))); c.rectangle(x, y, w, h); c.fill()
                _stamp(c, x + w / 2, y + h / 2, w * 0.95, eo_expo(prog(t, te, te + 0.08)))
        if t >= tl:
            fl = pulse(t, tl, 0.25)
            if fl > 0.03: rgba(g, CYAN, 0.6 * fl); g.set_line_width(4); g.rectangle(x, y, w, h); g.stroke()
        c.restore(); g.restore()
    core_cage(c, g, t)

def core_cage(c, g, t, ox=0.0, oy=0.0):
    """the count lights a hexagon round her core, an edge a beat (EINS..LIU); the 13th shuts it -- bars; then it bursts"""
    if not (COUNT_T[0] <= t < T_REBOOT): return
    x, y, w, h = RECTS['CORE  ŌMETEŌTL']; cx, cy = x + w / 2 + ox, y + h / 2 + oy
    R = 190 * (1 - 0.18 * eo_cubic(prog(t, T_EX13, T_EX13 + 0.2)))
    burst = eo_cubic(prog(t, T_SNAP + 0.25, T_SNAP + 0.6))
    V = [(cx + R * math.cos(math.radians(60 * i + 30)), cy + R * 0.62 * math.sin(math.radians(60 * i + 30))) for i in range(6)]
    for i in range(6):
        if t < COUNT_T[i]: continue
        fl = pulse(t, COUNT_T[i], 0.3)
        a_, b_ = V[i], V[(i + 1) % 6]
        mx, my = (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2
        dx, dy = (mx - cx) * burst * 3, (my - cy) * burst * 3
        for cc, aa, lw in ((c, 0.9, 2.2), (g, 0.5 + 0.4 * fl, 5)):
            line(cc, a_[0] + dx, a_[1] + dy, b_[0] + dx, b_[1] + dy, BONE, aa * (1 - burst), lw)
    if t >= T_EX13:                                              # the thirteenth: bars across it, LOCKED
        u = eo_expo(prog(t, T_EX13, T_EX13 + 0.12))
        for j in range(7):
            bx = x + 20 + j * (w - 40) / 6 + ox
            line(c, bx, y + oy - 10 + (1 - u) * -300 - burst * 600, bx, y + h + oy + 10 + (1 - u) * -300 - burst * 600, BONE, 0.9 * (1 - burst), 3)
        if t < T_SNAP:
            text(c, 'monom', 'LOCKED', cx, y + h + oy + 34, 18, BONE, 0.95 * u, align='center', track=0.3)

def crash(img_, t):
    """k351.5-352: the system falls over -- the picture slips in bands, faster and faster, into the white of k352"""
    u = prog(t, T_CRASH, T_REBOOT)
    if u <= 0 or u >= 1: return img_
    r = random.Random(int(t * 60))
    out = img_.copy(); hh = img_.shape[0]
    for _ in range(int(6 + 30 * u)):
        y0 = r.randrange(0, hh - 8); bh = r.randrange(4, int(12 + 90 * u))
        out[y0:y0 + bh] = np.roll(img_[y0:y0 + bh], int(r.gauss(0, 30 + 260 * u)), axis=1)
    return out

def reboot_montage(c, g, t):
    """k352-356: out of the white, a restored module per 8th note, close up, in its ASTROWING colours"""
    fill_bg(c, INK)
    for i in range(0, W, 48): line(c, i, 0, i, H, BONE, 0.03, 1)
    for j in range(0, H, 48): line(c, 0, j, W, j, BONE, 0.03, 1)
    kk = kt(t); k = min(7, int((kk - 352) * 2)); name = MONTAGE[k]; t0 = B(352 + k / 2)
    zoom = 1 + 0.04 * prog(t, t0, t0 + P / 2)
    text(c, 'monom', 'ŌMETEŌTL OS  ·  REBOOT', 96, 110, 22, BONE, 0.85, track=0.3)
    rgba(c, LISH, 0.9); c.rectangle(96, 124, 260, 3); c.fill(); rgba(c, CYAN, 0.9); c.rectangle(356, 124, 80, 3); c.fill()
    text(c, 'mono', f'{k + 1} / 8   restored', W - 96, 110, 20, BONE, 0.7, align='right', track=0.15)
    if name == 'TOPBAR':
        c.save(); c.translate(W / 2, H / 2); c.scale(2.2 * zoom, 2.2 * zoom); c.translate(-W / 2, -36)
        top_bar(c, g, t, 1.0); c.restore()
        text(c, 'heavy', 'ASTROWING', W / 2, 760, 150, BONE, 0.95 * eo_expo(prog(t, t0, t0 + 0.14)), align='center')
        return
    x, y, w, h = RECTS[name]
    S_ = min(2.6, 640 / h) * zoom
    for cc in (c, g):
        cc.save(); cc.translate(W / 2, H / 2 + 20); cc.scale(S_, S_); cc.translate(-(x + w / 2), -(y + h / 2))
    _box(c, g, x, y, w, h, name, True, t, name)
    body(c, g, name, x, y, w, h, t, kk)
    for cc in (c, g): cc.restore()
    u = eo_expo(prog(t, t0 + 0.05, t0 + 0.15))
    c.save(); c.translate(W / 2 + w * S_ / 2 - 40, H / 2 - h * S_ / 2 + 20); c.rotate(-0.08)
    c.new_path(); fonts()['heavy'].text_path(c, 'RESTORED', 0, 0, 54, 'right')
    rgba(c, CYAN, 0.95 * u); c.set_line_width(2); c.stroke(); c.restore()

def hex_shield_off(c, g, t):
    """k440: protection OFF -- the hexagon shield of 2.5 s over the whole frame, one last time, coming apart"""
    u = prog(t, T_PROT_OFF, T_PROT_OFF + 0.9)
    if u <= 0 or u >= 1: return
    R = 46; hw = R * math.sqrt(3)
    for j in range(-1, int(H / (1.5 * R)) + 2):
        for i in range(-1, int(W / hw) + 2):
            cx = i * hw + (hw / 2 if j % 2 else 0); cy = j * 1.5 * R
            d = math.hypot(cx - 960, cy - 540) / 1100
            a = clamp(1 - (u * 1.6 - d) * 3) * (1 - u) * 0.55
            if a <= 0.01: continue
            dr = 12 * u * (1 + d)
            pts = [(cx + R * math.cos(math.radians(60 * k + 30)), cy + R * math.sin(math.radians(60 * k + 30)) + dr * dr) for k in range(6)]
            for cc, aa, lw in ((c, a, 1.4), (g, a * 0.6, 3)):
                rgba(cc, CYAN, aa); cc.set_line_width(lw); cc.move_to(*pts[0])
                for q in pts[1:]: cc.line_to(*q)
                cc.close_path(); cc.stroke()

def tilt(t):
    """"so dizzy": the whole system sways, one swing every two beats"""
    if not DIZZY[0] <= t < DIZZY[1]: return 0.0
    return math.radians(1.6) * math.sin(math.pi * prog(t, *DIZZY)) * math.sin(math.pi * (kt(t) - 106.5))

def scene_pv(t, pv):
    """where the shot goes: the viewport, unless the viewport itself is gone (executed k342-352; cracked k436-443)"""
    te = exe_t('VIEWPORT')
    if te + P <= t < T_REBOOT: return pv * (1 - eo_cubic(prog(t, te + P, te + P + 0.3)))
    if T_FRAME <= t < B(443): return pv * (1 - eo_cubic(prog(t, T_FRAME + 0.15, T_FRAME + 0.5)))
    return pv

def render_v3(t, fr, scene, composite):
    pv = mode_at(t)
    if T_REBOOT <= t < B(356):                                  # the reboot: no shot, the system rebuilding itself
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
        gs = cairo.ImageSurface(cairo.FORMAT_ARGB32, W // 2, H // 2); g = cairo.Context(gs); g.scale(0.5, 0.5)
        reboot_montage(c, g, t); s.flush(); gs.flush()
        buf = np.ndarray((H, W, 4), np.uint8, s.get_data()); gbuf = np.ndarray((H // 2, W // 2, 4), np.uint8, gs.get_data())
        fx = {'flash': 1.0 - eo_cubic(prog(t, T_REBOOT, T_REBOOT + 0.3)), 'ab': 3 * pulse(t, B(352 + 0.5 * math.floor((kt(t) - 352) * 2)), 0.12),
              'vig': 0.35, 'glow': 0.8}
        return composite(buf, gbuf, fr, fx)
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
    a_ = tilt(t)
    if a_:
        for cc in (c, g): cc.translate(W / 2, H / 2); cc.rotate(a_); cc.translate(-W / 2, -H / 2)
    if pv > 0.001:                                              # the panel's own faint grid
        for i in range(0, W, 48): line(c, i, 0, i, H, BONE, 0.022 * pv, 1)
        for j in range(0, H, 48): line(c, 0, j, W, j, BONE, 0.022 * pv, 1)
    # the scene: full frame at pv = 0, the viewport at pv = 1
    ps = scene_pv(t, pv)
    vx, vy, vw, vh = lerp(0, VP[0], ps), lerp(0, VP[1], ps), lerp(W, VP[2], ps), lerp(H, VP[3], ps)
    k = vw / W
    c.save(); c.rectangle(vx, vy, vw, vh); c.clip(); c.translate(vx, vy); c.scale(k, k)
    c.set_source_surface(s1, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint(); c.restore()
    g.save(); g.rectangle(vx, vy, vw, vh); g.clip(); g.translate(vx, vy); g.scale(k * 2, k * 2)
    g.set_source_surface(gs1, 0, 0); g.paint(); g.restore()
    te = exe_t('VIEWPORT')
    if te <= t < te + P:                                        # the twelfth call: the viewport itself
        rgba(c, INK, 0.5 * eo_cubic(prog(t, te, te + 0.15))); c.rectangle(vx, vy, vw, vh); c.fill()
        _stamp(c, vx + vw / 2, vy + vh / 2, vw * 0.9, eo_expo(prog(t, te + 0.6, te + 0.68)))
    if ps > 0.001:
        ub = eo_cubic(prog(t, B(0), B(1)))                      # the frame draws itself, corners first
        if ub > 0:
            rgba(c, LISH if t >= B(288) else CYAN, 0.7 * ps); c.set_line_width(1.4)
            for (px_, py_, sx, sy) in ((vx, vy, 1, 1), (vx + vw, vy, -1, 1), (vx, vy + vh, 1, -1), (vx + vw, vy + vh, -1, -1)):
                c.move_to(px_ + sx * vw / 2 * ub, py_); c.line_to(px_, py_); c.line_to(px_, py_ + sy * vh / 2 * ub)
            c.stroke()
            text(c, 'mono', 'VIEWPORT', vx, vy + vh + 18, 14, GREY, 0.8 * ps * ub, track=0.12)
    boot_log(c, t, pv)
    modules(c, g, t, pv)
    top_bar(c, g, t, pv)
    in_toast(c, g, t, pv)
    hex_shield_off(c, g, t)
    s.flush(); gs.flush()
    buf = np.ndarray((H, W, 4), np.uint8, s.get_data())
    gbuf = np.ndarray((H // 2, W // 2, 4), np.uint8, gs.get_data())
    fx = dict(fx)
    if pv > 0.5: fx['vig'] = min(fx.get('vig', 1.0), 0.35)
    kk = kt(t)
    if 288 <= kk < 320:                                         # the interlude holds its breath: no strobing, the gear changes only
        fx['flash'] = 0.3 * fx.get('flash', 0); fx['ab'] = 0.5 * fx.get('ab', 0)
    elif 320 <= kk < 352:
        fx['flash'] = 0.6 * fx.get('flash', 0)
        fx['ab'] = fx.get('ab', 0) + 4 * sum(pulse(t, e, 0.2) for e in EXE)
    if T_PROT_OFF <= t < T_PROT_OFF + 0.3: fx['flash'] = max(fx.get('flash', 0), 0.35 * (1 - prog(t, T_PROT_OFF, T_PROT_OFF + 0.3)))
    out = composite(buf, gbuf, fr, fx)
    return crash(out, t)
