# first: ffmpeg -i "../../Audio/Mili - world.execute (me) ;.mp3" -ac 1 -ar 44100 song.wav
from beat_this.inference import File2Beats
import json, numpy as np
f2b = File2Beats(checkpoint_path="final0", device="cpu", dbn=False)
b, d = f2b("song.wav")
json.dump({"beats":[float(x) for x in b],"downbeats":[float(x) for x in d]}, open("beats.json","w"))
print(60/np.median(np.diff(b))); print([round(float(x),3) for x in d[:20]]); print([round(float(x),3) for x in b[:70]])
