"""Parallel full-film render on one machine (the old sandbox could only do 2 chunks at a time).
usage:
  python render_all.py chunks I0 I1 [JOBS]   render chunks/c{I0..I1-1}.mp4, 5 s each (c{i} = [5i, 5i+5) clipped to END)
  python render_all.py dchunks [JOBS]        re-encode every chunks/c*.mp4 -> d*.mp4 at 18 Mbps (mux.py dchunk), in parallel
  python render_all.py n                     print the number of chunks for END
needs ffmpeg on PATH."""
import sys, os, math, subprocess, glob
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render import END
SEG = 5.0
N = math.ceil(END / SEG)

def run(args):
    r = subprocess.run([sys.executable, *args], cwd=HERE, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-2000:]); raise SystemExit(f'failed: {args}')
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else args, flush=True)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'n': print(N)
    elif mode == 'chunks':
        i0, i1 = int(sys.argv[2]), min(int(sys.argv[3]), N)
        jobs = int(sys.argv[4]) if len(sys.argv) > 4 else max(1, os.cpu_count() - 4)
        os.makedirs(os.path.join(HERE, 'chunks'), exist_ok=True)
        with ThreadPoolExecutor(jobs) as ex:
            list(ex.map(lambda i: run(['render.py', 'enc', str(i * SEG), str(min(END, (i + 1) * SEG)), os.path.join(HERE, 'chunks', f'c{i}.mp4')]),
                        range(i0, i1)))
    elif mode == 'dchunks':
        jobs = int(sys.argv[2]) if len(sys.argv) > 2 else max(1, os.cpu_count() // 4)
        cs = sorted(int(os.path.basename(p)[1:-4]) for p in glob.glob(os.path.join(HERE, 'chunks', 'c*.mp4')))
        with ThreadPoolExecutor(jobs) as ex:
            list(ex.map(lambda i: run(['mux.py', str(END), 'dchunk', str(i)]), cs))
