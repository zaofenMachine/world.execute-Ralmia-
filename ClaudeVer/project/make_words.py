"""Word-level lyric timestamps with faster-whisper (CPU). usage: python make_words.py START DUR  -> words_START.json"""
import sys, json, os, librosa
from faster_whisper import WhisperModel
HERE = os.path.dirname(os.path.abspath(__file__))
a, dur = float(sys.argv[1]), float(sys.argv[2])
y, _ = librosa.load(os.path.join(HERE, '..', '..', 'Audio', 'Mili - world.execute (me) ;.mp3'), sr=16000, offset=a, duration=dur)
m = WhisperModel('small.en', device='cpu', compute_type='int8')
segs, _ = m.transcribe(y, word_timestamps=True, beam_size=3, condition_on_previous_text=False)
out = [(w.start + a, w.end + a, w.word) for s in segs for w in s.words]
for w in out: print(f'{w[0]:7.2f} {w[1]:7.2f} {w[2]}')
json.dump(out, open(os.path.join(HERE, f'words_{int(a)}.json'), 'w'))
