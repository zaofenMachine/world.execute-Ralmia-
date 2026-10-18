"""Concatenate chunks_v2/c*.mp4 (v2; v1 used chunks/), add the original song, fade out.
usage:
  python mux.py END            master + delivery in one go (fine on a normal PC)
  python mux.py END master     out_v2.mp4 only (crf14 master, stream copy -> fast)
  python mux.py END dchunk N   re-encode chunks_v2/cN.mp4 -> chunks_v2/dN.mp4 at 18 Mbps (run several in parallel)
  python mux.py END deliver    concat chunks_v2/d*.mp4 + audio -> out_v2_delivery.mp4 (stream copy)
"""
import os, sys, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SONG = os.path.join(HERE, '..', '..', 'Audio', 'Mili - world.execute (me) ;.mp3')
END = float(sys.argv[1]) if len(sys.argv) > 1 else 30.45
MODE = sys.argv[2] if len(sys.argv) > 2 else 'all'
run = lambda *a: subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
num = lambda p: int(os.path.basename(p)[1:-4])
CH = 'chunks_v2'                 # v2 (v1's chunks stay in chunks/)

def concat_with_audio(prefix, out, vcodec_args):
    chunks = sorted(glob.glob(os.path.join(HERE, CH, prefix + '*.mp4')), key=num)
    lst = os.path.join(HERE, f'list_v2_{prefix}.txt')
    with open(lst, 'w') as f:
        for c in chunks: f.write(f"file '{c}'\n")
    run('-f', 'concat', '-safe', '0', '-i', lst, '-t', str(END), '-i', SONG, '-map', '0:v', '-map', '1:a', *vcodec_args,
        '-c:a', 'aac', '-b:a', '256k', '-af', f'afade=t=out:st={END - 0.4}:d=0.4', '-shortest', '-movflags', '+faststart', out)
    print(out, len(chunks), 'chunks')

def dchunk(i):
    src = os.path.join(HERE, CH, f'c{i}.mp4')
    run('-i', src, '-c:v', 'libx264', '-preset', 'medium', '-b:v', '18M', '-maxrate', '24M', '-bufsize', '36M',
        '-pix_fmt', 'yuv420p', '-g', '60', os.path.join(HERE, CH, f'd{i}.mp4'))

if MODE in ('all', 'master'):
    concat_with_audio('c', os.path.join(HERE, 'out_v2.mp4'), ['-c:v', 'copy'])
if MODE == 'dchunk':
    dchunk(int(sys.argv[3]))
if MODE == 'all':
    for c in glob.glob(os.path.join(HERE, CH, 'c*.mp4')): dchunk(num(c))
if MODE in ('all', 'deliver'):
    concat_with_audio('d', os.path.join(HERE, 'out_v2_delivery.mp4'), ['-c:v', 'copy'])
