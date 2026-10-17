import sys, subprocess, time
from lib import *
import scenes as S
import scenes2 as S2
import scenes3 as S3
import scenes4 as S4
import scenes5 as S5
import scenes6 as S6

TIMELINE = [
    (0.0,   B(4),  S.s_power),
    (B(4),  B(8),  S.s_protect),
    (B(8),  B(12), S.s_pieces),
    (B(12), B(16), S.s_object),
    (B(16), B(21), S2.s_data),
    (B(21), B(24), S2.s_init),
    (B(24), B(28), S2.s_world),
    (B(28), B(32), S2.s_sim),
    (B(32), B(36), S2.s_velocity),
    (B(36), B(40), S2.s_doppler),
    (B(40), B(48), S2.s_mach),
    (B(48), B(52), S2.s_gap),
    (B(52), B(58), S2.s_zeno),
    (B(58), B(60), S2.s_near),
    (B(60), B(64), S2.s_title),
    (B(64),  B(68),  S3.s_points),
    (B(68),  B(72),  S3.s_dimension),
    (B(72),  B(76),  S3.s_circle),
    (B(76),  B(80),  S3.s_circum),
    (B(80),  B(88),  S3.s_sine),
    (B(88),  B(95),  S3.s_infinity),
    (B(95),  B(103), S3.s_scope),
    (B(103), B(106.5), S3.s_blind),
    (B(106.5), B(111.5), S3.s_dizzy),
    (B(111.5), B(119), S3.s_spacetime),
    (B(119), B(123), S3.s_unite),
    (B(123), B(128), S3.s_deeply),
    (B(128), B(160), S4.s_chorus1),
    (B(160), B(192), S4.s_verse2),
    (B(192), B(224), S4.s_switch),
    (B(224), B(256), S5.s_chorus2),
    (B(256), B(288), S5.s_bridge),
    (B(288), B(320), S6.s_executions),
    (B(320), B(342), S6.s_doors),
    (B(342), 999.0, S6.s_pending),     # the count / 13th / launch: waiting for the user's ears (HANDOFF 2.3)
]
END = B(352)

def render_frame(t, fr):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    gs = cairo.ImageSurface(cairo.FORMAT_ARGB32, W // 2, H // 2); g = cairo.Context(gs); g.scale(0.5, 0.5)
    fx = {}
    for a, b, fn in TIMELINE:
        if a <= t < b:
            fx = fn(c, g, t) or {}
            break
    s.flush(); gs.flush()
    buf = np.ndarray((H, W, 4), np.uint8, s.get_data())
    gbuf = np.ndarray((H // 2, W // 2, 4), np.uint8, gs.get_data())
    return composite(buf, gbuf, fr, fx)

def composite(buf, gbuf, fr, fx):
    img = buf[..., :3].astype(np.float32)
    gl = gbuf[..., :3].astype(np.float32)
    if gl.max() > 0:
        k = fx.get('glow', 1.0)
        b1 = cv2.GaussianBlur(gl, (0, 0), 4); b2 = cv2.GaussianBlur(cv2.resize(gl, (W // 8, H // 8), interpolation=cv2.INTER_AREA), (0, 0), 4)
        glow = cv2.resize(b1, (W, H)) * 0.9 + cv2.resize(b2, (W, H)) * 1.1
        img += glow * k
    ab = fx.get('ab', 0)
    if ab > 0.5:
        sft = int(round(ab))
        img[..., 2] = np.roll(img[..., 2], sft, 1); img[..., 0] = np.roll(img[..., 0], -sft, 1)
    fl = fx.get('flash', 0)
    if fl > 0: img = img * (1 - fl) + 255 * fl
    vk = fx.get('vig', 1.0)
    if vk > 0: img *= (1 - (1 - VIG) * vk)
    gr = fx.get('grain', 0.035)
    if gr > 0:
        gn = cv2.resize(GRAIN[fr % len(GRAIN)], (W, H), interpolation=cv2.INTER_NEAREST)
        img += (gn * 255 * gr)[..., None]
    return np.clip(img, 0, 255).astype(np.uint8)

def encode(t0, t1, out):
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    st = time.time()
    for fr in range(f0, f1):
        p.stdin.write(render_frame(fr / FPS, fr).tobytes())
    p.stdin.close(); p.wait()
    print(out, f1 - f0, 'frames', round(time.time() - st, 1), 's')

def stills(times, out, cols=4, scale=0.25):
    ims = []
    for tt in times:
        im = render_frame(tt, int(tt * FPS))
        im = cv2.resize(im, (int(W * scale), int(H * scale)), interpolation=cv2.INTER_AREA)
        cv2.rectangle(im, (0, 0), (70, 18), (0, 0, 0), -1)
        cv2.putText(im, f'{tt:.2f}', (3, 14), 0, 0.45, (0, 255, 255), 1)
        ims.append(im)
    while len(ims) % cols: ims.append(np.zeros_like(ims[0]))
    cv2.imwrite(out, np.vstack([np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 88])

if __name__ == '__main__':
    if sys.argv[1] == 'enc':
        encode(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    elif sys.argv[1] == 'still':
        ts = [float(x) for x in sys.argv[3].split(',')]
        sc = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
        cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
        stills(ts, sys.argv[2], cols, sc)
