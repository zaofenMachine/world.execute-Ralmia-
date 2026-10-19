"""world.execute(me); x Ralmia — Act II "giving" (59.41–103.72 s): chorus 1, verse 2 (specimen cards), the switches.
Placeholders until the 2nd GPT batch: her = n_her_front (cut from ref_sheet) for #13; the creator is a vector silhouette
(#11a/#24); objects #14a-c are vector drawings; #15 = n_hand_gap flipped + a vector human hand; #16a/b = n_w*_night (prep4)."""
from scenes3 import *

# ---------------------------------------------------------------- helpers
_TH = {}
def thumb(name, w, bg=None):
    """Downscaled cairo surface of an asset (cached). Alpha assets are flattened onto bg (rgb tuple)."""
    for bw in (120, 240, 480, 960, 1920):
        if bw >= w: break
    name = variant(name)                         # v3: the treated picture under the current register
    key = (name, bw, bg)
    if key not in _TH:
        im = cv2.imread(f'{WORK}/assets/{name}.png', cv2.IMREAD_UNCHANGED)
        if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        if im.shape[2] == 4:
            a = im[..., 3:4].astype(np.float32) / 255
            b = np.array((bg or INK2)[::-1], np.float32) * 255
            im = (im[..., :3] * a + b * (1 - a)).astype(np.uint8)
        im = cv2.resize(im, (bw, int(bw * 9 / 16)), interpolation=cv2.INTER_AREA)
        im = np.ascontiguousarray(np.dstack([im, np.full(im.shape[:2], 255, np.uint8)]))
        _TH[key] = (cairo.ImageSurface.create_for_data(im, cairo.FORMAT_ARGB32, im.shape[1], im.shape[0], im.strides[0]), im)
    return _TH[key][0]

def win(c, x, y, w, h, name, bg=None, label='', a=1.0, pan=0.0):
    """A simulation window: thumbnail + title bar + frame. pan (-1..1) slides the picture a little inside."""
    if w < 2 or a <= 0: return
    s_ = thumb(name, w, bg)
    sc = w / s_.get_width() * 1.06
    c.save(); c.rectangle(x, y, w, h); c.clip()
    c.translate(x + w / 2 + pan * w * 0.03, y + h / 2); c.scale(sc, sc)
    c.set_source_surface(s_, -s_.get_width() / 2, -s_.get_height() / 2); c.paint_with_alpha(a)
    c.restore()
    bar = clamp(h * 0.09, 4, 26)
    rgba(c, INK, 0.85 * a); c.rectangle(x, y, w, bar); c.fill()
    if label and bar > 10: text(c, 'mono', label, x + 6, y + bar * 0.74, bar * 0.6, BONE, 0.8 * a)
    rgba(c, BONE, 0.55 * a); c.set_line_width(1.1); c.rectangle(x, y, w, h); c.stroke()

POOL = [('n_pinky2_hd', None), ('n_world_hd', None), ('n_eye_open_hd', None), ('n_hand_palm_hd', PAPER),
        ('n_portrait_hd', None), ('n_dash_full_hd', INK2), ('n_hand_tied_s_hd', None), ('n_world_line', None),
        ('n_floating_hd', INK2), ('n_her_front_hd', PAPER), ('n_wL1_night_hd', None), ('n_eye_closed_hd', None),
        ('n_dash_launch_hd', INK2), ('n_hand_gap_s_hd', None), ('n_portrait_line', None), ('n_wL1_hd', None)]
LINE_OF = {'n_pinky2_hd': 'n_pinky2_line', 'n_world_hd': 'n_world_line', 'n_eye_open_hd': 'n_eye_open_line',
           'n_portrait_hd': 'n_portrait_line', 'n_hand_tied_s_hd': 'n_hand_tied_line', 'n_eye_closed_hd': 'n_eye_closed_line',
           'n_hand_gap_s_hd': 'n_hand_gap_line', 'n_wL1_hd': 'n_wL1_line'}

def words_ol(c, items, t, x, y, size, col=BONE, ol=INK, olw=9, key='serif'):
    """lyric words with an ink outline so they read over busy pictures"""
    if LYRIC_LOG[0] is not None: LYRIC_LOG[0].add(('w', tuple(items)))
    if LYRICS_OFF[0]: return
    f = fonts()[key]; cx = x; sp = text_w(key, ' ', size)
    for w_, ton in items:
        u = eo_cubic(prog(t, ton, ton + 0.12))
        if u > 0:
            c.new_path(); f.text_path(c, w_, cx, y + 10 * (1 - u), size)
            rgba(c, ol, 0.85 * u); c.set_line_width(olw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
            rgba(c, col, u); c.fill()
        cx += text_w(key, w_, size) + sp

def slam_word(c, g, word, t, t0, x, y, size, key='heavy', col=BONE, align='center', ol=INK, until=None, glow=0.6):
    if LYRIC_LOG[0] is not None: LYRIC_LOG[0].add(('s', word, t0))
    if t < t0 or (until and t >= until): return
    u = eo_expo(prog(t, t0, t0 + 0.14))
    c.save(); c.translate(x, y); s_ = 1.22 - 0.22 * u; c.scale(s_, s_)
    f = fonts()[key]
    c.new_path(); f.text_path(c, word, 0, 0, size, align)
    if ol is not None:
        rgba(c, ol, 0.9 * min(1, u * 2)); c.set_line_width(size * 0.05); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    rgba(c, col, min(1, u * 2)); c.fill()
    c.restore()
    p_ = pulse(t, t0, 0.5) * glow
    if p_ > 0.02:
        text(g, key, word, x, y, size, CYAN, p_, align=align)

# ---- her (placeholder: front view cut from the reference sheet; canvas figure spans y 90..1050, centred on x 960)
def her(c, cx, bottom, sc, a=1.0, name='n_her_front_hd'):
    c.save(); c.translate(cx, bottom); c.scale(sc, sc); c.translate(-960, -1050)
    c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(a)
    c.restore()
HER_HANDS = [(760, 530), (1170, 530)]    # gloved palms in n_her_front (canvas px)
OFFER_PALMS = [(644, 386), (1276, 385)]  # palm cores in n_offer (feet at (960, 1035))
def figure(c, name, x, feet_y, sc, a=1.0, feet=(960, 1050), rot=0.0):
    """a standing cut-out, placed by its feet"""
    if a <= 0.003: return
    c.save(); c.translate(x, feet_y); c.rotate(rot); c.scale(sc, sc); c.translate(-feet[0], -feet[1])
    c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(min(1, a)); c.restore()

# ---- the creator ("you"): never a face. vector silhouette until #11a / #24 arrive
def creator(c, x, y, h, pose='stand', col=SEPIA, a=1.0, rot=0.0):
    """x, y = bottom centre; h = height of the drawn figure."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(h, h)
    rgba(c, col, a)
    if pose == 'sit':                     # seen from behind, seated: head, shoulders, chair back
        c.arc(0, -0.80, 0.105, 0, 6.283); c.fill()
        c.move_to(-0.115, -0.84); c.curve_to(-0.12, -0.95, 0.12, -0.95, 0.115, -0.84); c.close_path(); c.fill()   # hair
        c.rectangle(-0.045, -0.71, 0.09, 0.08); c.fill()
        c.move_to(-0.06, -0.64); c.curve_to(-0.22, -0.64, -0.29, -0.6, -0.3, -0.45)
        c.line_to(-0.33, 0.0); c.line_to(0.33, 0.0); c.line_to(0.3, -0.45)
        c.curve_to(0.29, -0.6, 0.22, -0.64, 0.06, -0.64); c.close_path(); c.fill()
        rgba(c, GREY if col is not GREY else INK2, a)
        c.move_to(-0.25, -0.42); c.line_to(0.25, -0.42); c.line_to(0.27, 0.0); c.line_to(-0.27, 0.0); c.close_path(); c.fill()
        rgba(c, col, a); c.rectangle(-0.03, 0.0, 0.06, 0.12); c.fill()
    else:                                 # standing: head, long lab coat, legs
        c.arc(0, -0.925, 0.062, 0, 6.283); c.fill()
        c.move_to(-0.066, -0.94); c.curve_to(-0.07, -1.0, 0.07, -1.0, 0.066, -0.94); c.close_path(); c.fill()
        c.rectangle(-0.025, -0.87, 0.05, 0.04); c.fill()
        c.move_to(-0.03, -0.835); c.curve_to(-0.10, -0.835, -0.128, -0.82, -0.132, -0.77)
        c.curve_to(-0.135, -0.6, -0.13, -0.45, -0.155, -0.28); c.line_to(0.155, -0.28)
        c.curve_to(0.13, -0.45, 0.135, -0.6, 0.132, -0.77); c.curve_to(0.128, -0.82, 0.10, -0.835, 0.03, -0.835); c.close_path(); c.fill()
        for sx in (-1, 1):                 # arms hanging close to the coat
            c.save(); c.translate(sx * 0.142, -0.79); c.rotate(-sx * 0.05)
            c.move_to(-0.026, 0); c.curve_to(-0.03, 0.15, -0.024, 0.3, -0.02, 0.36); c.line_to(0.02, 0.36)
            c.curve_to(0.024, 0.3, 0.03, 0.15, 0.026, 0); c.close_path(); c.fill()
            c.arc(0, 0.375, 0.025, 0, 6.283); c.fill(); c.restore()
            c.move_to(sx * 0.03, -0.29); c.line_to(sx * 0.085, -0.29); c.line_to(sx * 0.075, -0.02); c.line_to(sx * 0.035, -0.02)
            c.close_path(); c.fill()
            c.rectangle(sx * 0.035 - (0.0 if sx > 0 else 0.05), -0.025, 0.09 if sx > 0 else 0.09, 0.025); c.fill()
    c.restore()

def padlock(c, g, x, y, s, u, col=BONE):
    """u: 0 open -> 1 shut."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rgba(c, col, 1); c.set_line_width(0.12)
    c.new_path(); c.arc(0, -0.55 - 0.35 * (1 - u), 0.32, math.pi, 0); c.line_to(0.32, -0.25 - 0.35 * (1 - u)); c.stroke()
    c.move_to(-0.32, -0.55 - 0.35 * (1 - u)); c.line_to(-0.32, -0.3); c.stroke()
    c.rectangle(-0.5, -0.3, 1.0, 0.8); c.fill()
    rgba(c, INK, 1); c.arc(0, 0.02, 0.1, 0, 6.283); c.fill(); c.rectangle(-0.035, 0.02, 0.07, 0.25); c.fill()
    c.restore()

STICK_COLS = [hexc('#f4a7c4'), hexc('#fff1e0'), hexc('#e9a3d8')]       # the crowd's light sticks: pink, warm white (never cyan/red)
_SW = np.random.default_rng(5)
SWAY = [(float(_SW.random() * 1920), float(905 + _SW.random() * 165), float(22 + _SW.random() * 18), float(_SW.random()),
         int(_SW.integers(0, 3))) for _ in range(84)]
def sway_sticks(c, g, t, a=1.0, lift=0.0):
    """the crowd's light sticks swinging in time (one swing per two beats, the house more or less together); call
    inside the stage camera. lift 0..1: everyone raises them (SATISFACTION)"""
    ph = 2 * math.pi * (t - T0) / (2 * P)
    for x, y, L, o, k in SWAY:
        an = 0.42 * math.sin(ph + 0.6 * o) - 0.1 + 0.25 * lift * (o - 0.5)
        L_ = L * (1 + 0.6 * lift); y_ = y - 30 * lift * (0.5 + o)
        x1, y1 = x + math.sin(an) * L_, y_ - math.cos(an) * L_
        for cc, aa, lw in ((c, 0.85 * a, 5), (g, 0.5 * a, 9)):
            rgba(cc, STICK_COLS[k], aa); cc.set_line_width(lw); cc.set_line_cap(cairo.LINE_CAP_ROUND)
            cc.move_to(x, y_); cc.line_to(x1, y1); cc.stroke(); cc.set_line_cap(cairo.LINE_CAP_BUTT)

def creation_layers(c, d, push=1.0, tp=(948, 463), ax=(0.82, 0.57)):
    """the god card from its three layers: Ralmia's hand moved back by d up the axis, Lishenna's down it"""
    for nm, sg in (('n_cr_plate_hd', 0), ('n_cr_hand_r_hd', -1), ('n_cr_hand_l_hd', 1)):
        c.save(); c.translate(*tp); c.scale(push, push); c.translate(-tp[0], -tp[1])
        c.translate(sg * ax[0] * d, sg * ax[1] * d)
        c.set_source_surface(surf(nm), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
        c.restore()

# ================================================================ S21 CHORUS 1  [B128, B160)
STAGE_SCREENS = [(63, 149, 510, 434), (601, 103, 1318, 439), (1409, 149, 1856, 434)]   # n_stage (gen/_qa/round4/anchors_v2.json)
GRID_LV = [(128, 1), (130, 2), (132, 4), (133, 8)]
def grid_rects(n, u, cx=960, cy=600, tot=1500):
    gap = 6 if n >= 8 else 12
    w = (tot - gap * (n - 1)) / n; h = w * 9 / 16
    tw, th = n * w + (n - 1) * gap, n * h + (n - 1) * gap
    out = []
    for i in range(n):
        for j in range(n):
            x = cx - tw / 2 + j * (w + gap); y = cy - th / 2 + i * (h + gap)
            x = lerp(cx - w / 2, x, u); y = lerp(cy - h / 2, y, u)
            out.append((x, y, w, h, i * n + j))
    return out

def wall(c, g, t, dim=1.0, flash=0.0, cy=600, tot=1500, labels=True):
    n = 1; t0 = B(128)
    for kb, nn in GRID_LV:
        if t >= B(kb): n, t0 = nn, B(kb)
    u = eo_expo(prog(t, t0, t0 + 0.22)) if n > 1 else 1.0
    if n == 1:
        s = lerp(1.0, 0.62, eio_cubic(prog(t, B(128), B(129))))
        w, h = W * s, H * s
        win(c, 960 - w / 2, cy - h / 2 * (1 if s < 1 else 1) + (540 - cy) * (1 - prog(t, B(128), B(129))), w, h,
            'n_pinky2_hd', None, 'sim #0001  ·  you & me' if labels else '', dim)
        return
    for (x, y, w, h, k) in grid_rects(n, u, cy=cy, tot=tot):
        name, bg = POOL[(k * 7 + n) % len(POOL)] if k else POOL[0]
        win(c, x, y, w, h, name, bg, f'sim #{k + 1:04d}' if labels else '', dim, pan=math.sin(t * 1.3 + k))
        if flash > 0.02:
            rgba(c, CYAN, 0.35 * flash); c.rectangle(x, y, w, h); c.fill()
            rgba(g, CYAN, 0.5 * flash); g.rectangle(x, y, w, h); g.fill()

def s_chorus1(c, g, t):
    fill_bg(c, INK)
    fx = {}
    dotgrid(c, BONE, 0.05)
    kk = (t - T0) / P
    if t < B(136):
        # A: the pinky promise was one window; she makes more of them for you, doubling on the beat
        wall(c, g, t, 1.0, pulse(t, B(134), 0.5))
        if t >= B(134):
            slam_word(c, g, 'STIMULATIONS', t, B(134), 960, 660, 230)
        words_ol(c, [('If', 59.45), ('I', 59.66), ('can,', 60.02), ('if', 60.42), ('I', 60.60), ('can', 60.94), ('give', 61.20),
                     ('you', 61.42), ('all', 61.68), ('the', 61.88)], t, 150, 248, 70)
        fx['ab'] = 3 * sum(pulse(t, B(kb), 0.2) for kb, _ in GRID_LV[1:]) + 6 * pulse(t, B(134), 0.25)
        fx['flash'] = 0.3 * pulse(t, B(134), 0.1) + 0.8 * (1 - prog(t, B(128), B(128) + 0.18)) ** 2
    elif t < B(144):
        # B (v2): Lishenna on her stage; behind her, three giant screens play the simulations Ralmia made, re-rendering on
        # every beat; the sea of light sticks breathes with the beat and goes up on SATISFACTION
        s_ = 1.0 + 0.06 * eio_cubic(prog(t, B(136), B(144))) + 0.16 * eo_expo(prog(t, B(141.75), B(141.75) + 0.3))
        def cam(cc):
            cc.translate(960, 520); cc.scale(s_, s_); cc.translate(-960, -520)
        c.save(); cam(c)
        c.set_source_surface(surf('n_stage_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
        c.push_group()
        beat = math.floor(kk)
        live = t >= B(141.75)                         # v2 round 6: the big screen goes to the live camera on SATISFACTION
        for si, (x0, y0, x1, y1) in enumerate(STAGE_SCREENS):
            if si == 1 and live:
                lz = 1.0 + 0.04 * prog(t, B(141.75), B(144))
                c.save(); c.rectangle(x0, y0, x1 - x0, y1 - y0); c.clip()
                fs = (x1 - x0) / 1920 * 0.98 * lz
                c.translate((x0 + x1) / 2, (y0 + y1) / 2); c.scale(fs, fs); c.translate(-960, -560)
                c.set_source_surface(surf('n_lish_face_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
                c.restore()
                for yy in range(int(y0), int(y1), 5): line(c, x0, yy, x1, yy, INK, 0.10, 1)       # the LED screen's lines
                rgba(c, BONE, 0.5 * pulse(t, B(141.75), 0.25)); c.rectangle(x0, y0, x1 - x0, y1 - y0); c.fill()
                continue
            cols = 6 if si == 1 else 4; gp = 3
            cw = (x1 - x0 - gp * (cols - 1)) / cols; ch = cw * 9 / 16
            for r_ in range(int((y1 - y0) / (ch + gp)) + 1):
                for k_ in range(cols):
                    x = x0 + k_ * (cw + gp); y = y0 + r_ * (ch + gp)
                    name, bg = POOL[(k_ * 7 + r_ * 3 + si * 11 + beat * 5) % len(POOL)]
                    win(c, x, y, cw, ch, name, bg, '', 1.0, pan=math.sin(t * 2 + k_))
                    fl = pulse(t, B(beat), 0.25) * (((k_ + r_ + si + beat) % 3) == 0)
                    if fl > 0.02: rgba(c, CYAN, 0.4 * fl); c.rectangle(x, y, cw, ch); c.fill()
        pat = c.pop_group(); c.set_source(pat); c.mask_surface(surf('n_stage_screens'), 0, 0)
        c.restore()
        g.save(); cam(g); rgba(g, (1, 0.92, 0.8), 0.22 + 0.2 * pulse(t, B(beat), 0.3)); g.mask_surface(surf('n_stage_screens'), 0, 0); g.restore()
        sat = pulse(t, B(141.75), 1.4)
        g.save(); cam(g); rgba(g, (1, 0.78, 0.9), 0.35 + 0.45 * pulse(t, B(beat), 0.35) + 0.9 * sat); g.mask_surface(surf('n_stage_sticks'), 0, 0); g.restore()
        c.save(); cam(c); g.save(); cam(g)
        sway_sticks(c, g, t, 1.0, eo_cubic(prog(t, B(141.5), B(141.75))))
        c.restore(); g.restore()
        levels = [(137, 0.15), (138, 0.30), (139, 0.45), (140, 0.60), (141, 0.80), (141.75, 1.0)]
        lv = 0.0
        for kb, v in levels:
            if t >= B(kb): lv = lerp(lv, v, eo_expo(prog(t, B(kb), B(kb) + 0.1)))
        gx0, gx1, gy = 1180, 1780, 1000
        rgba(c, INK, 0.75); c.rectangle(gx0 - 24, gy - 52, gx1 - gx0 + 48, 84); c.fill()
        text(c, 'mono', 'you.satisfaction', gx0, gy - 18, 20, BONE, 0.8, track=0.15)
        text(c, 'monom', f'{int(round(lv * 100)):3d} %', gx1, gy - 18, 22, CYAN, 0.95, align='right')
        line(c, gx0, gy + 10, gx1, gy + 10, BONE, 0.25, 6)
        for cc, aa in ((c, 1), (g, 0.7)): line(cc, gx0, gy + 10, lerp(gx0, gx1, lv), gy + 10, CYAN, aa, 6)
        slam_word(c, g, 'SATISFACTION', t, B(141.75), 150, 958, 158, key='bold', align='left')   # over the crowd, clear of her
        words_ol(c, [('Then', 63.12), ('I', 63.33), ('can,', 63.69), ('then', 64.09), ('I', 64.27), ('can', 64.61), ('be', 64.87),
                     ('your', 65.09), ('only', 65.35)], t, 150, 1040, 62)
        fx['ab'] = 5 * pulse(t, B(141.75), 0.25) + 2 * pulse(t, B(136), 0.2)
        fx['flash'] = 0.25 * pulse(t, B(141.75), 0.1) + 0.6 * (1 - prog(t, B(136), B(136) + 0.15)) ** 2
        fx['vig'] = 0.7
    elif t < B(152):
        # C: her, arms open; she floats up out of line art, and on "execution" the colour floods out of her palms
        run = t >= B(150)
        th0 = 0.35 * (t - B(144)) + 1.6 * eo_cubic(prog(t, B(150), B(152))) + (t - B(150)) * 0.9 * run
        items = []
        for i in range(12):
            a = th0 + 2 * math.pi * i / 12
            z = math.sin(a)
            items.append((z, 960 + 720 * math.cos(a), 600 + 170 * z, i))
        items.sort()
        def draw_item(z, x, y, i):
            s = 0.75 + 0.3 * z; w, h = 300 * s, 169 * s
            name, bg = POOL[(i * 5 + 3) % len(POOL)]
            if not run and name in LINE_OF: name = LINE_OF[name]
            a_ = 0.55 + 0.45 * (z + 1) / 2
            if z > 0: a_ *= 0.3 + 0.7 * clamp(abs(x - 960) / 360)          # don't bury her
            win(c, x - w / 2, y - h / 2, w, h, name, bg, '', a_, pan=math.sin(t * 2 + i) * run)
        for it in items:
            if it[0] < 0: draw_item(*it)
        sc = 0.6 + 0.03 * prog(t, B(144), B(152))
        rise = 40 * eio_cubic(prog(t, B(144), B(150))) + 10 * math.sin(math.pi * (t - B(144)) / P)   # floating, breathing with the beat
        fx_, fy_ = 960, 1010 - rise
        T = lambda p: (fx_ + (p[0] - 960) * sc, fy_ + (p[1] - 1035) * sc)
        # line art first (bone lines), colour from the palms on RUN
        c.save(); c.translate(fx_, fy_); c.scale(sc, sc); c.translate(-960, -1035)
        rgba(c, BONE, 0.95 * (1 - prog(t, B(150) + 0.35, B(150) + 0.6))); c.mask_surface(surf('n_offer_line'), 0, 0)
        if run:
            rr_ = 1400 * eo_cubic(prog(t, B(150), B(150) + 0.45))
            c.new_path()
            for hx, hy in OFFER_PALMS: c.new_sub_path(); c.arc(hx, hy, rr_, 0, 6.283)
            c.clip()
            c.set_source_surface(surf('n_offer_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
        c.restore()
        for hx, hy in OFFER_PALMS:                     # the cores in her palms
            px, py = T((hx, hy))
            gl_ = 0.35 + 0.65 * pulse(t, B(150), 0.8) + 0.25 * pulse(t, B(math.floor(kk)), 0.4)
            rg = cairo.RadialGradient(px, py, 0, px, py, 70)
            rg.add_color_stop_rgba(0, *CYAN, gl_); rg.add_color_stop_rgba(1, *CYAN, 0)
            g.set_source(rg); g.arc(px, py, 70, 0, 6.283); g.fill()
            if run:
                p_ = prog(t, B(150), B(150) + 0.6)
                for cc in (c, g):
                    rgba(cc, CYAN, 0.8 * (1 - p_)); cc.set_line_width(3); cc.new_path(); cc.arc(px, py, 20 + 500 * p_, 0, 6.283); cc.stroke()
        for it in items:
            if it[0] >= 0: draw_item(*it)
        # the RUN key
        ua = eo_back(prog(t, B(148.5), B(148.5) + 0.2))
        if ua > 0:
            kx, ky = 1600, 920; press = eo_cubic(prog(t, B(150) - 0.04, B(150))) * (1 - eo_cubic(prog(t, B(150) + 0.08, B(150) + 0.3)))
            c.save(); c.translate(kx, ky + 8 * press); c.scale(ua, ua)
            rgba(c, CYAN if run else INK2, 1); c.rectangle(-110, -44, 220, 88); c.fill()
            rgba(c, BONE, 0.9); c.set_line_width(2); c.rectangle(-110, -44, 220, 88); c.stroke()
            rgba(c, INK if run else BONE, 1); c.move_to(-70, -20); c.line_to(-70, 20); c.line_to(-38, 0); c.close_path(); c.fill()
            text(c, 'monom', 'RUN', 10, 13, 38, INK if run else BONE, 1, track=0.2)
            c.restore()
            if run:
                p_ = pulse(t, B(150), 0.6)
                rgba(g, CYAN, p_); g.rectangle(kx - 110, ky - 44, 220, 88); g.fill()
        slam_word(c, g, 'EXECUTION', t, B(150), 960, 250, 200)
        words_ol(c, [('If', 66.82), ('I', 66.94), ('can', 67.38), ('make', 67.62), ('you', 67.88), ('happy,', 68.08), ('I', 68.74),
                     ('will', 68.80), ('run', 69.02), ('the', 69.26)], t, 150, 1040, 62)
        fx['ab'] = 6 * pulse(t, B(150), 0.3) + 2 * pulse(t, B(math.floor(kk)), 0.15) * run
        fx['flash'] = 0.35 * pulse(t, B(150), 0.12)
    else:
        # D: trapped -- the windows fold into a cage around the two of them (v2: her and Lishenna); two locks
        uc = eo_cubic(prog(t, B(152), B(152) + 0.6))
        rx, ry = -0.3, 0.5 + 0.25 * (t - B(152))
        s = 300
        V = [(x, y, z) for x in (-s, s) for y in (-s, s) for z in (-s, s)]
        Pp = [proj(*rot3(x, y, z, rx, ry), cx=960, cy=520) for (x, y, z) in V]
        Zs = [rot3(x, y, z, rx, ry)[2] for (x, y, z) in V]
        # windows flying in to the vertices
        if uc < 1:
            for i, (px, py, sp) in enumerate(Pp):
                a = 2 * math.pi * i / 8 + 0.35 * (t - B(144))
                ox, oy = 960 + 700 * math.cos(a), 560 + 170 * math.sin(a)
                x, y = lerp(ox, px, uc), lerp(oy, py, uc)
                w, h = 300 * (1 - uc) + 2, 169 * (1 - uc) + 1
                name, bg = POOL[(i * 5 + 3) % len(POOL)]
                win(c, x - w / 2, y - h / 2, w, h, name, bg, '', 1)
        edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count('1') == 1]
        faces = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5)]
        for f_ in faces:
            rgba(c, BONE, 0.035 * uc); c.move_to(*Pp[f_[0]][:2])
            for v in f_[1:]: c.line_to(*Pp[v][:2])
            c.close_path(); c.fill()
        def edges_draw(front):
            for a, b in edges:
                zf = (Zs[a] + Zs[b]) / 2 < 0
                if zf != front: continue
                for cc, aa, lw in ((c, 0.9 if front else 0.4, 2.4 if front else 1.4), (g, 0.4, 3)):
                    rgba(cc, BONE if cc is c else CYAN, aa * uc); cc.set_line_width(lw)
                    cc.move_to(*Pp[a][:2]); cc.line_to(*Pp[b][:2]); cc.stroke()
        edges_draw(False)
        bob = 5 * abs(math.sin(math.pi * (t - T0) / P)) + 8 * sum(pulse(t, B(k), 0.25) for k in (155, 156))   # a little bounce on the beat
        figure(c, 'n_cube_together_hd', 975, 778 - bob, 0.43, uc, (959, 1036))    # v2 round 2: the two of them, cheek to cheek
        edges_draw(True)
        for kb, vi, lab in ((155, 0, 'world.lockThing(me);'), (156, 7, 'world.lockThing(you);')):
            if t >= B(kb) - 0.15:
                u = eo_back(prog(t, B(kb) - 0.15, B(kb)), 2.0)
                px, py = Pp[vi][:2]
                padlock(c, g, px, py, 48 * u + 1, prog(t, B(kb) - 0.05, B(kb)))
                p_ = pulse(t, B(kb), 0.5)
                if p_ > 0.02:
                    rgba(g, CYAN, 0.5 * p_); g.arc(px, py, 50, 0, 6.283); g.fill()
                text(c, 'mono', lab, px + (40 if px > 960 else -40), py + 70, 18, CYAN, 0.85 * u, align='left' if px > 960 else 'right')
        if t >= B(157.5):
            glyph_pop(c, 'heavy', 'SIMULATION', 960, 1010, 150, BONE, t, B(157.5), P / 8, align='center', track=0.06, drop=30)
        words_ol(c, [('Though', 70.12), ('we', 70.80), ('are', 71.12), ('trapped', 71.30), ('in', 71.72), ('this', 72.08),
                     ('strange,', 72.26), ('strange', 72.56)], t, 150, 248, 66)
        fx['ab'] = 5 * pulse(t, B(155), 0.2) + 5 * pulse(t, B(156), 0.2) + 3 * pulse(t, B(157.5), 0.2)
        fx['flash'] = 0.08 * pulse(t, B(155), 0.1) + 0.08 * pulse(t, B(156), 0.1)
    hud(c, t, True, a=0.65, log_a=0.85)
    return fx

# ================================================================ S22 VERSE 2 — specimen cards  [B160, B192)
# -- vector specimens (placeholders for #14a-c), unit coords: height ~1, centred on 0
def path_eggplant(c):
    c.move_to(0.02, -0.30); c.curve_to(0.22, -0.30, 0.38, -0.05, 0.36, 0.18); c.curve_to(0.34, 0.42, 0.12, 0.52, -0.04, 0.50)
    c.curve_to(-0.24, 0.48, -0.32, 0.30, -0.26, 0.12); c.curve_to(-0.20, -0.05, -0.16, -0.28, 0.02, -0.30); c.close_path()
def path_eggplant_calyx(c):
    pts = [(-0.15, -0.25), (-0.08, -0.19), (-0.04, -0.29), (0.02, -0.20), (0.07, -0.30), (0.12, -0.20), (0.18, -0.26), (0.09, -0.36), (-0.05, -0.36)]
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path()
    c.move_to(0.02, -0.36); c.curve_to(0.02, -0.44, -0.02, -0.48, -0.06, -0.52)
def path_tomato(c):
    for i in range(121):
        a = 2 * math.pi * i / 120
        r = 0.38 * (1 + 0.035 * math.cos(5 * a))
        (c.move_to if i == 0 else c.line_to)(r * math.cos(a), 0.06 + 0.86 * r * math.sin(a))
    c.close_path()
def path_tomato_calyx(c):
    for i in range(5):
        a = -math.pi / 2 + 2 * math.pi * i / 5 + 0.3
        tip = (0.2 * math.cos(a), -0.26 + 0.09 * math.sin(a))
        l = (0.03 * math.cos(a + 1.6), -0.26 + 0.03 * math.sin(a + 1.6)); r = (0.03 * math.cos(a - 1.6), -0.26 + 0.03 * math.sin(a - 1.6))
        c.move_to(*l); c.line_to(*tip); c.line_to(*r)
    c.move_to(0, -0.27); c.line_to(0.02, -0.38)
def path_cat(c):
    c.move_to(-0.12, -0.18); c.curve_to(0.10, -0.30, 0.40, -0.20, 0.38, 0.06); c.curve_to(0.36, 0.30, 0.10, 0.36, -0.10, 0.30)
    c.curve_to(-0.24, 0.26, -0.36, 0.16, -0.36, 0.04); c.close_path()                       # body
    c.new_sub_path(); c.arc(-0.26, -0.06, 0.135, 0, 6.283)                                     # head
    c.move_to(-0.37, -0.12); c.line_to(-0.36, -0.27); c.line_to(-0.27, -0.18)                 # ears
    c.move_to(-0.22, -0.19); c.line_to(-0.14, -0.27); c.line_to(-0.14, -0.12)
def path_cat_details(c):
    c.move_to(0.36, 0.12); c.curve_to(0.34, 0.40, -0.02, 0.44, -0.20, 0.24)                   # tail wrapped round
    for (x, y) in ((-0.31, -0.05), (-0.21, -0.05)):                                            # closed eyes
        c.move_to(x - 0.03, y); c.curve_to(x - 0.01, y + 0.025, x + 0.01, y + 0.025, x + 0.03, y)
    for i in range(6):                                                                          # tabby stripes
        x = -0.02 + i * 0.065
        c.move_to(x, -0.22 + abs(i - 2.5) * 0.02); c.curve_to(x + 0.04, -0.1, x + 0.03, 0.05, x - 0.01, 0.16)

SPEC = [  # (path, details, beat of the object word, fill on paper?, label, latin)
    dict(body=path_eggplant, det=path_eggplant_calyx, k=162.0, t_obj=75.18, paper=True, name='EGGPLANT', latin='Solanum melongena',
         gem=(0.06, 0.20, 0.05), fill=INK2),
    dict(body=path_tomato, det=path_tomato_calyx, k=170.0, t_obj=78.78, paper=False, name='TOMATO', latin='Solanum lycopersicum',
         gem=(0.13, 0.14, 0.045), fill=INK2),
    dict(body=path_cat, det=path_cat_details, k=178.0, t_obj=82.50, paper=True, name='TABBY CAT', latin='Felis catus  var. Ralmia',
         gem=None, fill=BONE),
]

def unit_points(builder, n=1400, seed=3, w=3):
    ss = cairo.ImageSurface(cairo.FORMAT_A8, 1000, 1000); cc = cairo.Context(ss)
    cc.translate(500, 500); cc.scale(800, 800); builder(cc); cc.set_line_width(w / 800); cc.set_source_rgba(0, 0, 0, 1); cc.stroke()
    ss.flush(); m = np.ndarray((1000, ss.get_stride()), np.uint8, ss.get_data())[:, :1000]
    ys, xs = np.nonzero(m > 100); r = np.random.default_rng(seed)
    idx = r.choice(len(xs), n, replace=len(xs) < n)
    return (xs[idx] - 500) / 800.0, (ys[idx] - 500) / 800.0

_HP = {}
def her_points(n=1400):
    if 'x' not in _HP:
        im = cv2.imread(f'{WORK}/assets/n_her_front_hd.png', cv2.IMREAD_UNCHANGED)
        e = cv2.Canny(im[..., 3], 50, 150) | (cv2.Canny(cv2.cvtColor(im[..., :3], cv2.COLOR_BGR2GRAY), 60, 160) & (im[..., 3] > 200))
        ys, xs = np.nonzero(e); r = np.random.default_rng(4); idx = r.choice(len(xs), n, replace=False)
        _HP['x'] = (xs[idx] - 960) / 960.0; _HP['y'] = (ys[idx] - 570) / 960.0
    return _HP['x'], _HP['y']

SPEC_IMG = ['n_spec_egg', 'n_spec_tomato', 'n_cat2']          # v2 round 2: the cat is her, waist up, paws up (cat_ralmia_v2)
SPEC_CORE = [(1006, 784), (524, 695), (815, 315)]          # where the colour starts: the gems (on the cat, her own temple gem)
_SM = {}
def spec_morph(i, cx=560, cy=610, H_=620):
    if i not in _SM:
        im = cv2.imread(f'{WORK}/assets/{SPEC_IMG[i]}_hd.png', cv2.IMREAD_UNCHANGED)
        a = im[..., 3]; ys, xs = np.nonzero(a > 128)
        bx, by = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
        sc = min(H_ / (ys.max() - ys.min()), 760 / (xs.max() - xs.min()))
        e = cv2.Canny(a, 50, 150) | (cv2.Canny(cv2.cvtColor(im[..., :3], cv2.COLOR_BGR2GRAY), 80, 180) & (a > 200))
        ey, ex = np.nonzero(e); hx, hy = her_points()
        r = np.random.default_rng(10 + i); idx = r.choice(len(ex), len(hx), replace=len(ex) < len(hx))
        ox = cx + (ex[idx] - bx) * sc; oy = cy + (ey[idx] - by) * sc
        ha = np.argsort(np.arctan2(hy - hy.mean(), hx - hx.mean())); oa = np.argsort(np.arctan2(oy - oy.mean(), ox - ox.mean()))
        _SM[i] = (hx[ha], hy[ha], ox[oa], oy[oa], sc, (bx, by), SPEC_CORE[i])
    return _SM[i]

_OP = {}
def morph_pairs(i):
    if i not in _OP:
        hx, hy = her_points(); sp = SPEC[i]
        def b(cc): sp['body'](cc); sp['det'](cc)
        ox, oy = unit_points(b, len(hx), seed=10 + i)
        ha = np.argsort(np.arctan2(hy - hy.mean(), hx - hx.mean())); oa = np.argsort(np.arctan2(oy - oy.mean(), ox - ox.mean()))
        _OP[i] = (hx[ha], hy[ha], ox[oa], oy[oa])
    return _OP[i]

def draw_spec(c, g, sp, cx, cy, S, grow, fill_a, ink):
    c.save(); c.translate(cx, cy); c.scale(S, S); c.rotate(-0.35 if sp['body'] is path_eggplant else 0)
    if fill_a > 0:
        c.new_path(); sp['body'](c); rgba(c, sp['fill'], fill_a * (0.9 if sp['fill'] is INK2 else 0.85)); c.fill()
    c.new_path(); sp['body'](c); c.set_line_width(3.2 / S); rgba(c, ink, 1); partial_stroke(c, grow)
    c.new_path(); sp['det'](c); c.set_line_width(2.4 / S); rgba(c, ink, 1); partial_stroke(c, clamp(grow * 1.3 - 0.3))
    if sp['gem'] and fill_a > 0:            # her core, set into the specimen (and a riveted plate on the eggplant)
        gx, gy, gr = sp['gem']
        if sp['body'] is path_eggplant:
            c.new_path(); c.move_to(-0.24, 0.02); c.curve_to(-0.05, -0.04, 0.2, -0.02, 0.34, 0.06); c.line_to(0.35, 0.14)
            c.curve_to(0.2, 0.06, -0.05, 0.04, -0.25, 0.1); c.close_path(); rgba(c, BONE, fill_a); c.fill_preserve()
            rgba(c, ink, fill_a); c.set_line_width(1.6 / S); c.stroke()
            for k in range(5):
                rgba(c, ink, fill_a); c.arc(-0.16 + k * 0.11, 0.05 - 0.005 * k + (0.01 if k > 2 else 0), 0.008, 0, 6.283); c.fill()
        rgba(c, INK, fill_a); c.arc(gx, gy, gr * 1.35, 0, 6.283); c.fill()
        rgba(c, CYAN, fill_a); c.arc(gx, gy, gr, 0, 6.283); c.fill()
    c.restore()
    if sp['gem'] and fill_a > 0:
        gx, gy, gr = sp['gem']; a_ = -0.35 if sp['body'] is path_eggplant else 0
        px = cx + S * (gx * math.cos(a_) - gy * math.sin(a_)); py = cy + S * (gx * math.sin(a_) + gy * math.cos(a_))
        rg = cairo.RadialGradient(px, py, 0, px, py, S * gr * 3)
        rg.add_color_stop_rgba(0, *CYAN, 0.8 * fill_a); rg.add_color_stop_rgba(1, *CYAN, 0)
        g.set_source(rg); g.arc(px, py, S * gr * 3, 0, 6.283); g.fill()

def fit_size(key, s, width, mx):
    return min(mx, width / max(1e-6, fonts()[key].shape(s, 0.02)[1]))

def lycopene(c, g, x0, y0, w, frac, glow, ink=BONE):
    """the lycopene chain as a skeletal formula, bond by bond"""
    n = 22; dx = w / n; amp = 20
    pts = [(x0 + i * dx, y0 + (amp if i % 2 else -amp)) for i in range(n + 1)]
    nb = int(frac * n)
    for i in range(nb):
        a, b = pts[i], pts[i + 1]
        for cc, aa in ((c, 1), (g, glow)):
            if aa <= 0: continue
            col = ink if cc is c else CYAN
            line(cc, a[0], a[1], b[0], b[1], col, aa, 2.2)
            if 2 <= i <= n - 3 and i % 2 == 1:                      # conjugated double bonds (inner parallel)
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                nx, ny = -(b[1] - a[1]), (b[0] - a[0]); L = math.hypot(nx, ny); nx, ny = nx / L * 8, ny / L * 8
                if (my + ny - y0) * (my - y0) > 0 or True:
                    sgn = 1 if ny * (y0 - my) > 0 else -1
                    line(cc, lerp(a[0], b[0], 0.2) + sgn * nx, lerp(a[1], b[1], 0.2) + sgn * ny,
                         lerp(a[0], b[0], 0.8) + sgn * nx, lerp(a[1], b[1], 0.8) + sgn * ny, col, aa * 0.9, 1.6)
            if i % 4 == 2:                                        # methyl branches
                line(cc, b[0], b[1], b[0], b[1] + (30 if b[1] > y0 else -30), col, aa, 2.2)

HAND_POLY = [(0, -9), (30, -13), (70, -15), (118, -17), (160, -24), (205, -26), (250, -18), (300, -8),
             (300, 98), (250, 104), (205, 102), (170, 92), (150, 78), (128, 66), (122, 54), (138, 44), (128, 34),
             (118, 22), (90, 15), (50, 12), (14, 10), (0, 6)]
def human_hand(c, x, y, s, ang, fill=INK2, ink=BONE):
    """placeholder for the creator's reaching hand (#15): fingertip at (x, y), wrist along ang; relaxed, index extended."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.new_path(); c.rectangle(296, -16, 900, 132); rgba(c, BONE, 1); c.fill_preserve()           # lab-coat sleeve
    rgba(c, SEPIA, 0.6); c.set_line_width(2 / s); c.stroke()
    line(c, 340, -16, 340, 116, SEPIA, 0.5, 2 / s)
    c.new_path(); c.move_to(*HAND_POLY[0])
    for i in range(1, len(HAND_POLY)):
        x0, y0 = HAND_POLY[i - 1]; x1, y1 = HAND_POLY[i]
        c.curve_to(x0 + (x1 - x0) * 0.4, y0 + (y1 - y0) * 0.4, x0 + (x1 - x0) * 0.6, y0 + (y1 - y0) * 0.6, x1, y1)
    c.curve_to(-6, 4, -6, -6, 0, -9); c.close_path()
    rgba(c, fill, 1); c.fill_preserve(); rgba(c, ink, 0.95); c.set_line_width(2.6 / s); c.stroke()
    for (px, py, L) in ((150, 58, 30), (165, 76, 26), (200, 34, 40)):                              # curled finger creases
        c.move_to(px, py); c.line_to(px + L, py + 4); rgba(c, ink, 0.5); c.set_line_width(1.6 / s); c.stroke()
    c.restore()

def s_verse2(c, g, t):
    fx = {}
    kk = (t - T0) / P
    i = int(clamp(math.floor((kk - 160) / 8), 0, 3))
    k0 = 160 + 8 * i
    paper = i < 3                                  # the three specimens share one notebook; god is a different page
    if paper: paper_bg(c); dotgrid(c, SEPIA, 0.10)
    else: fill_bg(c, INK); dotgrid(c, BONE, 0.05)
    ink = SEPIA if paper else BONE
    # specimen tag
    text(c, 'mono', f'SPECIMEN  {i + 1:02d} / 04', 1060, 330, 18, ink, 0.6, track=0.3)
    line(c, 1060, 344, 1800, 344, ink, 0.4, 1.2)
    LY_ = [[('If', 74.19), ("I'm", 74.38), ('an', 74.98), ('eggplant,', 75.18), ('then', 75.84), ('I', 76.02), ('will', 76.22),
            ('give', 76.38), ('you', 76.64), ('my', 76.90)],
           [('If', 77.88), ("I'm", 78.10), ('a', 78.68), ('tomato,', 78.78), ('then', 79.40), ('I', 79.64), ('will', 79.90),
            ('give', 80.08), ('you', 80.32)],
           [('If', 81.57), ("I'm", 81.88), ('a', 82.36), ('tabby', 82.50), ('cat,', 82.72), ('then', 83.22), ('I', 83.34), ('will', 83.60),
            ('purr', 83.76), ('for', 84.02), ('your', 84.22)],
           [('If', 85.26), ("I'm", 85.50), ('the', 86.04), ('only', 86.18), ('god,', 86.42), ('then', 86.88), ("you're", 87.04),
            ('the', 87.26), ('proof', 87.44), ('of', 87.70), ('my', 87.96)]]
    words(c, 'serif', LY_[i], t, 150, 248, 64, ink, 0.95)
    KEY = [('NUTRIENTS', 166.5), ('ANTIOXIDANTS', 174.0), ('ENJOYMENT', 182.5), ('EXISTENCE', 190.5)]
    kw, kb = KEY[i]
    if i < 3:
        sp = SPEC[i]
        cx, cy, S = 560, 610, 620
        hx, hy, ox, oy, sc_, (bx, by), core = spec_morph(i)
        tm = sp['t_obj']
        um = eo_cubic(prog(t, tm, tm + 0.35))
        pa = 1 - prog(t, tm + 0.4, tm + 0.65)
        if pa > 0:
            ua = eo_cubic(prog(t, B(k0), B(k0) + 0.25))
            X = lerp(cx + S * hx, ox, um) + np.sin(t * 3 + hy * 9) * 2 * (1 - um)
            Y = lerp(cy + S * hy, oy, um)
            draw_points(c, X, Y, ink, 0.9 * pa * ua, 2.6)
        ul_ = prog(t, tm + 0.3, tm + 0.45)
        if ul_ > 0:                                   # line art, then colour from her core outwards
            c.save(); c.translate(cx, cy)
            img_ = SPEC_IMG[i]
            if i == 2 and kk >= 182.5: img_ = 'n_cat2b'   # winking, then eyes shut, content, on "purr" -- that's all
            c.scale(sc_, sc_); c.translate(-bx, -by)
            rgba(c, SEPIA, ul_); c.mask_surface(surf(SPEC_IMG[i] + '_line'), 0, 0)
            rr_ = 1500 * eo_cubic(prog(t, tm + 0.42, tm + 0.8))
            if rr_ > 0:
                c.new_path(); c.arc(core[0], core[1], rr_, 0, 6.283); c.clip()
                c.set_source_surface(surf(img_ + '_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
            c.restore()
            gp_ = (cx + (core[0] - bx) * sc_, cy + (core[1] - by) * sc_)
            p_ = pulse(t, tm + 0.42, 0.6)
            if p_ > 0.02:
                rg = cairo.RadialGradient(*gp_, 0, *gp_, 90); rg.add_color_stop_rgba(0, *CYAN, 0.9 * p_); rg.add_color_stop_rgba(1, *CYAN, 0)
                g.set_source(rg); g.arc(*gp_, 90, 0, 6.283); g.fill()
        # museum label
        ul = eo_cubic(prog(t, tm + 0.3, tm + 0.5))
        text(c, 'thin', sp['name'], cx - 260, 1000, 64, ink, ul, track=0.2)
        text(c, 'serif', sp['latin'], cx - 260, 1040, 30, ink, 0.7 * ul)
        # data panel
        if i == 0:
            rows = [('Serving size', '1 Ralmia'), ('Speed', '340.29 m/s'), ('Core', '1  ŌMETEŌTL'), ('Armour', '12 plates'), ('Touch', '0 %')]
            px0, py0 = 1060, 400
            up = eo_cubic(prog(t, B(163), B(163) + 0.2))
            text(c, 'heavy', 'Nutrition Facts', px0, py0 + 40, 58, ink, up)
            line(c, px0, py0 + 60, px0 + 740 * up, py0 + 60, ink, 1, 6)
            reset = t >= B(167.25)
            for r_, (k_, v_) in enumerate(rows):
                tr = B(163.5 + r_ * 0.5)
                u = eo_cubic(prog(t, tr, tr + 0.12))
                if u <= 0: continue
                y = py0 + 110 + r_ * 52
                text(c, 'monom', k_, px0, y, 26, ink, u)
                vv = scramble('0', t, B(167.25), 0.02, seed=r_) if reset else v_
                text(c, 'mono', vv, px0 + 740, y, 26, ink, u, align='right')
                line(c, px0, y + 14, px0 + 740 * u, y + 14, ink, 0.5, 1.2)
            if reset:
                ua = eo_cubic(prog(t, B(167.25), B(167.25) + 0.2))
                text(c, 'mono', '→ you.addAttribute(...)', px0, py0 + 420, 22, CYAN, ua)
        elif i == 1:
            fr = prog(t, B(170.5), B(173.75))
            gl_ = pulse(t, B(174), 0.8)
            lycopene(c, g, 1080, 560, 700, fr, gl_, ink)
            ul = eo_cubic(prog(t, B(173.5), B(173.5) + 0.2))
            text(c, 'monom', 'C40H56', 1080, 470, 30, ink, ul)
            text(c, 'mono', 'lycopene  ·  antioxidant', 1080, 660, 22, ink, 0.7 * ul)
            if t >= B(174.5):
                text(c, 'mono', '→ you.addAttribute(...)', 1080, 720, 22, CYAN, eo_cubic(prog(t, B(174.5), B(174.5) + 0.2)))
        else:
            # purr: a 25 Hz rumble on a strip chart, breathing every two beats
            x0_, y0_, w_, h_ = 1060, 420, 740, 260
            ua = eo_cubic(prog(t, B(178.5), B(178.5) + 0.3))
            rgba(c, ink, 0.35 * ua); c.set_line_width(1); c.rectangle(x0_, y0_, w_, h_); c.stroke()
            for k_ in range(1, 8): line(c, x0_ + w_ * k_ / 8, y0_, x0_ + w_ * k_ / 8, y0_ + h_, ink, 0.12 * ua, 1)
            line(c, x0_, y0_ + h_ / 2, x0_ + w_, y0_ + h_ / 2, ink, 0.3 * ua, 1)
            beat = math.floor(kk)
            for cc, aa, lw in ((c, ua, 2.2), (g, 0.25 * ua + 0.5 * pulse(t, B(182.5), 0.6), 3)):
                rgba(cc, ink if cc is c else CYAN, aa); cc.set_line_width(lw); cc.new_path()
                for s_ in range(0, 371):
                    xx = x0_ + w_ * s_ / 370
                    tt = t - (1 - s_ / 370) * 1.2
                    env = 0.35 + 0.65 * abs(math.sin(math.pi * ((tt - T0) / P) / 2)) + 0.6 * pulse(tt, B(math.floor((tt - T0) / P)), 0.25)
                    yy = y0_ + h_ / 2 - (h_ * 0.38) * env * math.sin(2 * math.pi * 25 * tt * 0.12 + s_ * 0.35)
                    (cc.move_to if s_ == 0 else cc.line_to)(xx, yy)
                cc.stroke()
            text(c, 'monom', 'me.purr();', x0_, y0_ - 20, 26, ink, ua)
            text(c, 'mono', '25 Hz', x0_ + w_, y0_ - 20, 22, ink, 0.7 * ua, align='right')
    else:
        # god: her hand from above, Lishenna's from below -- three layers (gen/request_v2c.md L13): the plate, and each hand
        # pulled back along the axis by d; they close and touch on k189
        TP = (948, 463); AX = (0.82, 0.57)
        d = 150 * (1 - eio_cubic(prog(t, B(184), B(189)))) - 1.2
        push = 1.0 + 0.05 * prog(t, B(184), B(192))
        creation_layers(c, d, push)
        touch = t >= B(189)
        ft = TP; hf = TP
        if touch:
            p_ = pulse(t, B(189), 0.7)
            rg = cairo.RadialGradient(*TP, 0, *TP, 180)
            rg.add_color_stop_rgba(0, *CYAN, 0.4 + 0.6 * p_); rg.add_color_stop_rgba(1, *CYAN, 0)
            g.set_source(rg); g.arc(*TP, 180, 0, 6.283); g.fill()
        else:
            text(c, 'monom', f'd = {(d + 1.2) / 400:.6f}', 1400, 470 + 0 * 0, 26, CYAN, 0.85 * eo_cubic(prog(t, B(184.5), B(185))))
        # the proof
        x0_ = 1400
        for j, (s_, kb_, key_) in enumerate((('Theorem.  me exists.', 186.5, 'serif'), ('Proof.  you.', 188.0, 'serif'))):
            u = eo_cubic(prog(t, B(kb_), B(kb_) + 0.15))
            if u > 0: text(c, key_, s_, x0_, 300 + j * 60, 44, BONE, u)
        if t >= B(190.5):
            u = eo_back(prog(t, B(190.5), B(190.5) + 0.18), 2)
            rgba(c, BONE, 1); c.rectangle(x0_ + 300 - 14 * u, 400 - 28 * u, 28 * u, 28 * u); c.fill()
        words_ol(c, LY_[3], t, 150, 248, 64)
    # keyword
    if t >= B(kb):
        size = fit_size('bold', kw, 760, 150)
        slam_word(c, g, kw, t, B(kb), 150 if i == 3 else 1060, 1010, size, key='bold', col=ink, align='left', ol=None, glow=0.5)
    fx['ab'] = 3 * pulse(t, B(k0), 0.2) + 5 * pulse(t, B(kb), 0.25)
    fx['flash'] = 0.3 * pulse(t, B(k0), 0.08) + 0.2 * pulse(t, B(kb), 0.1)
    if paper: fx['vig'] = 0.4; fx['grain'] = 0.03
    hud(c, t, not paper, a=0.6, log_a=0.85)
    return fx

# ================================================================ S23 THE SWITCHES  [B192, B224)
def world_at(c, g, t_ref, night, push=1.0):
    """The finished world from 11-13 s (four layers at their parallax position for t_ref), with night blended in."""
    pan = 34 * max(0.0, t_ref - B(24.5)); zoom = (1.035 + 0.02 * prog(t_ref, B(26), B(28))) * push
    for name, kb, entry, depth, _ in LAYERS:
        c.save(); c.translate(960 - pan * depth, 540); c.scale(zoom, zoom); c.translate(-960, -540)
        c.set_source_surface(surf(name), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD)
        c.paint_with_alpha(1 - night if name == 'n_wL2_hd' else 1)     # (the night city has no sun: don't let the day one show through)
        if night > 0:
            if name in ('n_wL1_hd', 'n_wL2_hd'):
                c.set_source_surface(surf({'n_wL1_hd': 'n_wL1n_hd', 'n_wL2_hd': 'n_wL2n_hd'}[name]), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD)
                c.paint_with_alpha(night)
            else:
                c.set_source_rgba(0.04, 0.06, 0.12, 0.62 * night); c.mask_surface(surf(name), 0, 0)
        c.restore()

def clock(c, g, x, y, r, hours, label, a=1.0):
    rgba(c, INK, 0.45 * a); c.arc(x, y, r + 14, 0, 6.283); c.fill()
    rgba(c, BONE, 0.9 * a); c.set_line_width(2.4); c.new_path(); c.arc(x, y, r, 0, 6.283); c.stroke()
    for i in range(12):
        an = i * math.pi / 6; L = 16 if i % 3 == 0 else 8
        line(c, x + math.cos(an) * (r - L), y + math.sin(an) * (r - L), x + math.cos(an) * r, y + math.sin(an) * r, BONE, 0.8 * a, 2)
    ha = (hours % 12) / 12 * 2 * math.pi - math.pi / 2; ma = (hours % 1) * 2 * math.pi - math.pi / 2
    line(c, x, y, x + math.cos(ha) * r * 0.55, y + math.sin(ha) * r * 0.55, BONE, a, 5)
    for cc, aa in ((c, a), (g, 0.6 * a)): line(cc, x, y, x + math.cos(ma) * r * 0.85, y + math.sin(ma) * r * 0.85, CYAN, aa, 2.5)
    text(c, 'monom', label, x, y + r * 0.5, 24, BONE, 0.85 * a, align='center', track=0.2)

def s_switch(c, g, t):
    fx = {}
    kk = (t - T0) / P
    if t < B(202):
        # F / M: a toggle that will not stay put
        fill_bg(c, INK); dotgrid(c, BONE, 0.05)
        p = 0.07 * math.sin(t * 11) * (1 - prog(t, B(195.5), B(195.5) + 0.05))     # undecided: the knob trembles
        if t >= B(195.5): p = lerp(0, -1, eo_back(prog(t, B(195.5), B(195.5) + 0.16), 2))
        if t >= B(197.5): p = lerp(-1, 1, eo_back(prog(t, B(197.5), B(197.5) + 0.16), 2))
        glitch = B(199.5) <= t
        if glitch:
            n16 = int((t - B(199.5)) / (P / 4))
            p = random.Random(n16 * 31).choice((-1, 1)) * (0.6 + 0.4 * random.Random(n16 * 7).random())
        ua = eo_back(prog(t, B(192), B(192) + 0.3), 1.4)
        cx, cy = 960, 600
        c.save(); c.translate(cx, cy); c.scale(ua, ua)
        rgba(c, INK2, 1); c.new_path(); c.arc(-200, 0, 110, math.pi / 2, 3 * math.pi / 2); c.arc(200, 0, 110, -math.pi / 2, math.pi / 2); c.close_path()
        c.fill_preserve(); rgba(c, BONE, 0.8); c.set_line_width(3); c.stroke()
        for cc, aa in ((c, 1), (g, 0.5)):
            rgba(cc, BONE if cc is c else CYAN, aa); cc.arc(p * 200, 0, 88, 0, 6.283); cc.fill()
        rgba(c, INK, 0.5); c.arc(p * 200, 0, 30, 0, 6.283); c.fill()
        c.restore()
        state = 'F' if p < -0.5 else 'M' if p > 0.5 else 'undefined'
        for lab, sx, on in (('F', -1, p < -0.5), ('M', 1, p > 0.5)):
            text(c, 'heavy', lab, cx + sx * 540, cy + 86, 250, BONE if on else GREY, (1.0 if on else 0.3) * ua, align='center')
        text(c, 'mono', f'me.gender = {state}', cx, cy + 230, 24, CYAN if state != 'undefined' else BONE, 0.85 * ua, align='center', track=0.15)
        if glitch:
            rr = random.Random(int(t * 60))
            for _ in range(5):
                y0 = 380 + rr.random() * 440; hh = 8 + rr.random() * 40; dx = (rr.random() - 0.5) * 160
                c.save(); c.rectangle(0, y0, W, hh); c.clip()
                c.translate(dx, 0); text(c, 'heavy', 'F' if rr.random() > 0.5 else 'M', cx + dx * 2, cy + 86, 250, BONE, 0.8, align='center')
                c.restore()
            fx['ab'] = 6 + 4 * rr.random()
        else:
            fx['ab'] = 5 * pulse(t, B(195.5), 0.2) + 5 * pulse(t, B(197.5), 0.2)
        lyric(c, [('Switch', 88.98), ('my', 89.30), ('gender', 89.64), ('to', 90.40), ('F,', B(195.5)), ('to', 91.20), ('M,', B(197.5))]
              if t < B(199.3) else [('and', 92.14), ('then', 92.38), ('do', 92.56), ('whatever', 92.98)], t)
        hud(c, t, True, a=0.6)
    elif t < B(208):
        # AM -> PM: the world from 12 s runs through a day
        night = eio_cubic(prog(t, B(204), B(206)))
        world_at(c, g, B(28) - 0.01, night, push=1 + 0.03 * prog(t, B(202), B(208)))
        if night < 1:                               # the sun, sinking during the day
            sy_ = lerp(574, 700, night); sun = 1 - night
            rg = cairo.RadialGradient(1246, sy_, 0, 1246, sy_, 300)
            rg.add_color_stop_rgba(0, 1, 0.9, 0.65, 0.6 * sun); rg.add_color_stop_rgba(1, 1, 0.9, 0.65, 0)
            g.set_source(rg); g.arc(1246, sy_, 300, 0, 6.283); g.fill()
        hrs = 6 + 12 * eio_cubic(prog(t, B(204), B(206))) + 0.5 * prog(t, B(202), B(204))
        clock(c, g, 1660, 300, 110, hrs, 'AM' if hrs < 12 else 'PM', eo_cubic(prog(t, B(202), B(202) + 0.25)))
        for word, kb in (('AM', 204), ('PM', 206)):
            if t >= B(kb) and (word == 'PM' or t < B(206)):
                u = eo_expo(prog(t, B(kb), B(kb) + 0.14))
                if word == 'AM':
                    c.set_operator(cairo.OPERATOR_MULTIPLY)
                    text(c, 'heavy', word, 1800, 1000, 300 * (1.15 - 0.15 * u), INK, 0.9 * u, align='right'); c.set_operator(cairo.OPERATOR_OVER)
                else:
                    text(c, 'heavy', word, 1800, 1000, 300 * (1.15 - 0.15 * u), BONE, 0.95 * u, align='right')
                    p_ = pulse(t, B(kb), 0.5)
                    if p_ > 0.02: text(g, 'heavy', word, 1800, 1000, 300, CYAN, 0.5 * p_, align='right')
        lyric(c, [('from', 93.86), ('AM', B(204)), ('to', 94.90), ('PM', B(206))], t, col=SEPIA if night < 0.5 else BONE, x=760, y=200, size=72)
        fx['ab'] = 4 * pulse(t, B(204), 0.2) + 4 * pulse(t, B(206), 0.2)
        fx['vig'] = 0.4 + 0.6 * night; fx['grain'] = 0.03
        hud(c, t, night > 0.5, a=0.6)
    elif t < B(216):
        # S <-> M: her own two personalities on the F/M toggle (role_s / role_m, a pixel-aligned pair).
        # a character joke only -- faces and hands, framed above the chest, no props
        fill_bg(c, INK); dotgrid(c, BONE, 0.05)
        K_S, K_M, K_FL = 211.5, 213.5, 214.5
        if t < B(K_S): p = 0.07 * math.sin(t * 11)                                  # undecided: the knob trembles
        elif t < B(K_M): p = lerp(0, -1, eo_back(prog(t, B(K_S), B(K_S) + 0.16), 2))
        elif t < B(K_FL): p = lerp(-1, 1, eo_back(prog(t, B(K_M), B(K_M) + 0.16), 2))
        else: p = -1 if int((t - B(K_FL)) / (P / 4)) % 2 == 0 else 1                 # then it flips on every 16th
        cuts = [K_S, K_M] + [K_FL + 0.25 * j for j in range(6)]
        kc = max([k for k in cuts if kk >= k], default=None)
        # the portrait, in a frame: line art (both faces dissolving into each other) until she is set, then colour
        FX0, FY0, FW, FH = 520, 140, 880, 660
        pop = 1.0 + (0.06 * (1 - eo_expo(prog(t, B(kc), B(kc) + 0.16))) if kc is not None else 0)
        c.save(); c.rectangle(FX0, FY0, FW, FH); c.clip()
        c.translate(960, FY0 + FH / 2); c.scale(pop, pop); c.translate(-960, -380)
        if kc is None:
            ua = eo_cubic(prog(t, B(208), B(208) + 0.4))
            mx = 0.5 + 0.5 * math.sin(math.pi * (kk - 208))
            for nm, aa in (('n_role_s_line', 1 - mx), ('n_role_m_line', mx)):
                rgba(c, BONE, 0.85 * ua * aa); c.mask_surface(surf(nm), 0, 0)
        else:
            cur = 'n_role_s_hd' if p < 0 else 'n_role_m_hd'
            c.set_source_surface(surf(cur), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
            if kk >= K_FL:                                                            # torn: slices of the other one
                oth = 'n_role_m_hd' if p < 0 else 'n_role_s_hd'
                rr = random.Random(int(t * 60))
                for _ in range(4):
                    y0 = 120 + rr.random() * 560; hh = 10 + rr.random() * 50; dx = (rr.random() - 0.5) * 120
                    c.save(); c.rectangle(0, y0, W, hh); c.clip(); c.translate(dx, 0)
                    c.set_source_surface(surf(oth), 0, 0); c.paint(); c.restore()
        c.restore()
        rgba(c, BONE, 0.5); c.set_line_width(1.5); c.rectangle(FX0, FY0, FW, FH); c.stroke()
        text(c, 'mono', 'me.portrait', FX0, FY0 - 14, 18, BONE, 0.6, track=0.3)
        # the toggle, smaller this time, under her; S and M as its two marks
        cx, cy, ts = 960, 890, 0.5
        c.save(); c.translate(cx, cy); c.scale(ts, ts)
        rgba(c, INK2, 1); c.new_path(); c.arc(-200, 0, 110, math.pi / 2, 3 * math.pi / 2); c.arc(200, 0, 110, -math.pi / 2, math.pi / 2); c.close_path()
        c.fill_preserve(); rgba(c, BONE, 0.8); c.set_line_width(3); c.stroke()
        for cc, aa in ((c, 1), (g, 0.5)):
            rgba(cc, BONE if cc is c else CYAN, aa); cc.arc(p * 200, 0, 88, 0, 6.283); cc.fill()
        rgba(c, INK, 0.5); c.arc(p * 200, 0, 30, 0, 6.283); c.fill()
        c.restore()
        state = 'S' if p < -0.5 else 'M' if p > 0.5 else 'undefined'
        for lab, sx, on in (('S', -1, p < -0.5), ('M', 1, p > 0.5)):
            u = eo_expo(prog(t, B(kc), B(kc) + 0.14)) if (on and kc is not None) else 1.0
            text(c, 'heavy', lab, 960 + sx * 680, 560, 250 * (1.15 - 0.15 * u), BONE if on else GREY, 1.0 if on else 0.3, align='center')
            if on and kc is not None:
                p_ = pulse(t, B(kc), 0.4)
                if p_ > 0.02: text(g, 'heavy', lab, 960 + sx * 680, 560, 250, CYAN, 0.6 * p_, align='center')
        text(c, 'mono', f'me.role = {state}', cx, cy + 80, 22, CYAN if state != 'undefined' else BONE, 0.85, align='center', track=0.15)
        lyric(c, [('Oh,', 96.08), ('my', 96.20), ('switch', 96.48), ('role', 97.10), ('to', 97.70), ('S,', B(211.5)), ('to', 98.60),
                  ('M', B(213.5))], t, y=1050)
        fx['ab'] = sum(5 * pulse(t, B(k), 0.2) for k in cuts[:2]) + (4 + 3 * random.Random(int(t * 60)).random() if kk >= K_FL else 0)
        hud(c, t, True, a=0.6)
    else:
        # the trance: the two of them adrift around one centre; the rings are Lishenna's humming, going out from her (v2)
        fill_bg(c, INK)
        tt = t - B(216)
        a_ = 0.38 * tt + 0.6
        pos = lambda ta, who: (960 + 300 * math.cos(0.38 * ta + 0.6 + who * math.pi), 540 + 120 * math.sin(0.38 * ta + 0.6 + who * math.pi))
        for n_ in range(int(tt / (P / 2)) + 1):
            te = n_ * P / 2; r = (tt - te) * 260
            if r > 1500: continue
            ex, ey = pos(te, 1)
            aa = 0.8 * (1 - r / 1500) * min(1, r / 80) * (1.0 if n_ % 2 == 0 else 0.6)
            for cc, k_, lw in ((c, 1.0, 2.2 + r / 500), (g, 0.6, 4)):
                rgba(cc, LISH, aa * k_); cc.set_line_width(lw); cc.new_path(); cc.arc(ex, ey, r, 0, 6.283); cc.stroke()
        for who in (0, 1):
            x, y = pos(tt, who)
            c.save(); c.translate(x, y); c.rotate(0.25 * tt if who == 0 else -0.22 * tt + 0.7)
            if who == 0:
                c.scale(0.5, 0.5); c.translate(-961, -552)
                c.set_source_surface(surf('n_floating_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(0.95)
            else:
                c.scale(0.44, 0.44); c.translate(-966, -551)
                c.set_source_surface(surf('n_lish_float_hd'), 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint_with_alpha(0.95)
            c.restore()
        # bleach: on the first "trance" a breath of light, on the second the whole dream whitens into paper
        # (never a grey mix: the light floods in, the paper is swapped in under full white, then the white recedes)
        wash = 0.28 * pulse(t, B(219.5), 0.9) + ei_cubic(prog(t, B(221.5), B(222.9))) * (1 - eo_cubic(prog(t, B(222.9), B(224))))
        inv = 1.0 if t >= B(222.9) else 0.0
        if inv > 0:
            c.set_source_surface(paper_tex(), 0, 0); c.paint()
        tc = SEPIA if inv > 0.5 else BONE
        for word, kb, y in (('trance,', 219.5, 900), ('trance', 221.5, 1010)):
            u = eo_cubic(prog(t, B(kb), B(kb) + 0.3))
            if u > 0: text(c, 'serif', word, 960, y, 120, tc, u, align='center')
        lyric(c, [('So', 99.42), ('we', 99.84), ('can', 100.20), ('enter', 100.94), ('the', 101.40)], t, col=tc)
        fx['ab'] = 2 + 3 * pulse(t, B(219.5), 0.3) + 5 * pulse(t, B(221.5), 0.3)
        fx['glow'] = 0.8; fx['vig'] = 1 - 0.6 * inv; fx['flash'] = clamp(wash) * 0.92
        hud(c, t, inv < 0.5, a=0.5)
    return fx
