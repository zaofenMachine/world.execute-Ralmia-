"""QA for a rendered video: contact sheets (every 0.25 s) + hard-cut alignment to the 8th-note grid + frozen spans.
usage: python qa.py out.mp4"""
import sys, os, cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
QA = sys.argv[2] if len(sys.argv) > 2 else 'qa_v3'      # v3; qa_v2/ and qa/ keep v2's and v1's sheets
P, T0 = 60 / 130, 0.34
cap = cv2.VideoCapture(sys.argv[1]); fps = cap.get(5)
os.makedirs(os.path.join(HERE, QA), exist_ok=True)
fr, d, prev, i = [], [], None, 0
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.cvtColor(cv2.resize(f, (160, 90)), cv2.COLOR_BGR2GRAY).astype(np.float32)
    d.append(0 if prev is None else float(np.abs(g - prev).mean())); prev = g
    if i % int(round(fps / 4)) == 0:
        im = cv2.resize(f, (400, 225), interpolation=cv2.INTER_AREA)
        cv2.rectangle(im, (0, 0), (52, 16), (0, 0, 0), -1); cv2.putText(im, f'{i / fps:.2f}', (2, 12), 0, 0.4, (0, 255, 255), 1)
        fr.append(im)
    i += 1
for s in range(0, len(fr), 32):
    ch = fr[s:s + 32]
    while len(ch) % 4: ch.append(np.zeros_like(fr[0]))
    cv2.imwrite(os.path.join(HERE, QA, f'q{s // 32}.jpg'), np.vstack([np.hstack(ch[j:j + 4]) for j in range(0, len(ch), 4)]))
d = np.array(d); grid = T0 + np.arange(0, 2000) * P / 2
ev = np.array([k for k in range(1, len(d) - 1) if d[k] > 12 and d[k] >= d[k - 1] and d[k] >= d[k + 1]]) / fps
off = np.array([e - grid[np.argmin(abs(grid - e))] for e in ev]) * 1000
print(f'{len(ev)} hard events, median |offset| {np.median(abs(off)):.1f} ms, within 35 ms: {np.mean(abs(off) <= 35):.0%}')
runs, s = [], None
for k, x in enumerate(d):
    if x < 0.3: s = k if s is None else s
    else:
        if s is not None and k - s >= int(1.3 * fps): runs.append((round(s / fps, 2), round(k / fps, 2)))
        s = None
print('frozen >= 1.3 s:', runs or 'none')
