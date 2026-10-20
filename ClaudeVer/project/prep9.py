"""v3: the chorus-3 rewind (scenes_v3.s_rewind) shows the film itself, running back from 160 s to the pinky promise.
Grabs those frames out of the rendered chunks (chunks_v3/c*.mp4) into assets/rewind3_NN.jpg (960 x 540).
Run after chunks 11-32 are rendered, then re-render chunks 33-34.   usage: python prep9.py"""
import os, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
from scenes_v3 import REWIND_SRC

def grab(t):
    i = int(t // 5); cap = cv2.VideoCapture(os.path.join(HERE, 'chunks_v3', f'c{i}.mp4'))
    cap.set(cv2.CAP_PROP_POS_FRAMES, round((t - 5 * i) * 60)); ok, f = cap.read(); cap.release()
    if not ok: raise SystemExit(f'no frame at {t}')
    return cv2.resize(f, (960, 540), interpolation=cv2.INTER_AREA)

if __name__ == '__main__':
    for n, t in enumerate(REWIND_SRC):
        cv2.imwrite(os.path.join(HERE, 'assets', f'rewind3_{n:02d}.jpg'), grab(t), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(len(REWIND_SRC), 'rewind frames')
