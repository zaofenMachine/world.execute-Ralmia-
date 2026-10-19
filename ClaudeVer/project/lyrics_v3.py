"""v3: every sung line, for the VOICE module (OUT) and Lishenna's side (IN). panel.py reads both.

OUT: harvested from what the v2 scenes draw (scenes.words / scenes4.words_ol / slam_word, via scenes.LYRIC_LOG), so the
VOICE line and the big word in the shot land together; keywords drawn by other means take the beat constants of their
scene (K_* in scenes3 / scenes5); the rest from Whisper (words_*.json). A word starting with '^', or all capitals and
longer than two characters, is a keyword (cyan in VOICE). Times in seconds.
IN: plan_v3.md section 3, as placed (2026-10-20). None = signal lost (TRANSMISSION shows '— signal lost —')."""
from lib import B

OUT = [
    # ---- verse 1 (0-30 s)
    [('Switch', B(0)), ('on', 0.58), ('the', 1.04), ('power', B(2)), ('line', B(2.5))],
    [('Remember', B(4)), ('to', 2.40), ('put', 2.78), ('on', 3.02), ('PROTECTION', B(6))],
    [('Lay', B(8)), ('down', 4.26), ('your', 4.70), ('PIECES', B(10))],
    [('and', 5.42), ("let's", 5.80), ('begin', 6.10), ('OBJECT', B(13)), ('CREATION', B(14))],
    [('Fill', B(16)), ('in', 7.94), ('my', 8.36), ('data', B(18)), ('PARAMETERS', B(18.7))],
    [('INITIALIZATION', B(22))],
    [('Set', B(24)), ('up', 11.60), ('our', 12.06), ('new', B(26)), ('WORLD', B(26.5))],
    [('and', B(28)), ("let's", 13.30), ('begin', 13.44), ('the', 13.84), ('SIMULATION', B(30))],
    [('world.execute(me);', B(60))],
    # ---- verse 1b (30-59 s)
    [('If', 30.00), ("I'm", 30.18), ('a', 30.64), ('set', 30.76), ('of', 30.88), ('POINTS,', B(66.5)),
     ('then', 31.54), ('I', 31.64), ('will', 31.88), ('give', 32.10), ('you', 32.34), ('my', 32.58), ('DIMENSION', B(70.5))],
    [('If', 33.34), ("I'm", 33.80), ('a', 34.34), ('CIRCLE,', B(74)),
     ('then', 35.26), ('I', 35.34), ('will', 35.60), ('give', 35.80), ('you', 36.04), ('my', 36.28), ('CIRCUMFERENCE', B(78.25))],
    [('If', 37.03), ("I'm", 37.50), ('a', 38.06), ('SINE', B(82)), ('WAVE,', B(82.5)),
     ('then', 38.86), ('you', 39.02), ('can', 39.24), ('sit', 39.46), ('on', 39.70), ('all', 39.92), ('my', 40.20), ('TANGENTS', B(87))],
    [('If', 40.95), ('I', 41.28), ('approach', 41.34), ('INFINITY,', B(89.5)),
     ('then', 42.24), ('you', 42.70), ('can', 42.94), ('be', 43.14), ('my', 43.40), ('LIMITATIONS', B(94))],
    [('Switch', 44.18), ('my', 44.88), ('CURRENT', B(97.5)), ('to', 45.94), ('AC,', B(100)), ('to', 47.20), ('^DC', B(102))],
    [('and', 47.70), ('then', 47.92), ('blind', 48.11), ('my', 48.54), ('VISION', B(105.5))],
    [('so', 49.72), ('DIZZY,', 50.19), ('so', 50.88), ('DIZZY', 51.11)],
    [('Oh,', 51.80), ('we', 51.96), ('can', 52.26), ('travel', B(113.5)), ('to', 53.24), ('A.D.,', B(116)), ('to', 54.36), ('B.C.', B(118))],
    [('and', 55.10), ('we', 55.48), ('can', 55.96), ('UNITE', B(121.5))],
    [('so', 57.11), ('DEEPLY,', 57.57), ('so', 58.03), ('DEEPLY', 58.49)],
    # ---- chorus 1 (59-74 s)
    [('If', 59.45), ('I', 59.66), ('can,', 60.02), ('if', 60.42), ('I', 60.60), ('can', 60.94), ('give', 61.20), ('you', 61.42),
     ('all', 61.68), ('the', 61.88), ('STIMULATIONS', B(134))],
    [('Then', 63.12), ('I', 63.33), ('can,', 63.69), ('then', 64.09), ('I', 64.27), ('can', 64.61), ('be', 64.87), ('your', 65.09),
     ('only', 65.35), ('SATISFACTION', B(141.75))],
    [('If', 66.82), ('I', 66.94), ('can', 67.38), ('make', 67.62), ('you', 67.88), ('happy,', 68.08), ('I', 68.74), ('will', 68.80),
     ('run', 69.02), ('the', 69.26), ('EXECUTION', B(150))],
    [('Though', 70.12), ('we', 70.80), ('are', 71.12), ('trapped', 71.30), ('in', 71.72), ('this', 72.08), ('strange,', 72.26),
     ('strange', 72.56), ('SIMULATION', B(157.5))],
    # ---- verse 2 (74-89 s)
    [('If', 74.19), ("I'm", 74.38), ('an', 74.98), ('eggplant,', 75.18), ('then', 75.84), ('I', 76.02), ('will', 76.22), ('give', 76.38),
     ('you', 76.64), ('my', 76.90), ('NUTRIENTS', 77.19)],
    [('If', 77.88), ("I'm", 78.10), ('a', 78.68), ('tomato,', 78.78), ('then', 79.40), ('I', 79.64), ('will', 79.90), ('give', 80.08),
     ('you', 80.32), ('ANTIOXIDANTS', 80.65)],
    [('If', 81.57), ("I'm", 81.88), ('a', 82.36), ('tabby', 82.50), ('cat,', 82.72), ('then', 83.22), ('I', 83.34), ('will', 83.60),
     ('purr', 83.76), ('for', 84.02), ('your', 84.22), ('ENJOYMENT', 84.57)],
    [('If', 85.26), ("I'm", 85.50), ('the', 86.04), ('only', 86.18), ('god,', 86.42), ('then', 86.88), ("you're", 87.04), ('the', 87.26),
     ('proof', 87.44), ('of', 87.70), ('my', 87.96), ('EXISTENCE', 88.26)],
    # ---- the switches (89-104 s)
    [('Switch', 88.98), ('my', 89.30), ('gender', 89.64), ('to', 90.40), ('^F,', 90.57), ('to', 91.20), ('^M,', 91.49)],
    [('and', 92.14), ('then', 92.38), ('do', 92.56), ('whatever', 92.98)],
    [('from', 93.86), ('^AM', 94.49), ('to', 94.90), ('^PM', 95.42)],
    [('Oh,', 96.08), ('switch', 96.20), ('my', 96.48), ('role', 97.10), ('to', 97.70), ('^S,', 97.96), ('to', 98.60), ('^M', 98.88)],
    [('So', 99.42), ('we', 99.84), ('can', 100.20), ('enter', 100.94), ('the', 101.40), ('TRANCE,', 101.74), ('the', 102.58), ('TRANCE', 102.66)],
    # ---- chorus 2 (104-118 s)
    [('If', 103.72), ('I', 103.92), ('can,', 104.32), ('if', 104.74), ('I', 104.86), ('can', 105.22), ('feel', 105.46), ('your', 105.76),
     ('VIBRATIONS', B(229.5))],
    [('then', 107.12), ('I', 107.70), ('can,', 108.02), ('then', 108.40), ('I', 108.64), ('can', 108.94), ('finally', 109.16), ('be', 109.94),
     ('COMPLETION', B(238.25))],
    [('Though', 110.86), ('you', 111.11), ('have', 111.34), ('left', 111.52)],
    [('you', 112.26), ('have', 112.49), ('left', 112.68)],
    [('you', 113.19), ('have', 113.42), ('left', 113.60)],
    [('you', 113.99), ('have', 114.22), ('left', 114.41)],
    [('you', 115.03), ('have', 115.26), ('left', 115.45)],
    [('you', 115.96), ('have', 116.19), ('left', 116.37), ('me', 116.72), ('in', 117.00), ('ISOLATION', B(253))],
    # ---- bridge (118-133 s)
    [('If', 118.49), ('I', 118.70), ('can,', 119.10), ('if', 119.60), ('I', 119.98), ('can', 120.02), ('erase', 120.24), ('all', 120.74),
     ('the', 120.94), ('pointless', 121.18), ('FRAGMENTS', B(262.75))],
    [('Then', 121.96), ('maybe,', 122.50), ('then', 122.98), ('maybe', 123.92), ('you', 124.18), ("won't", 124.42), ('leave', 124.66),
     ('me', 124.80), ('so', 124.92), ('DISHEARTENED', B(270.5))],
    [('Challenging', 126.14), ('your', 127.20), ('GOD,', 127.60), ('you', 128.66), ('have', 129.28), ('made', 129.48), ('some', 129.98),
     ('ILLEGAL', B(283)), ('ARGUMENTS', B(285))],
] + [
    # ---- the trial (148-163 s): twelve EXECUTIONs one every second beat, the count, the thirteenth
    [('EXECUTION', B(320 + 2 * i))] for i in range(12)
] + [
    [('EINS', B(344)), ('DOS', B(345)), ('TROIS', B(346)), ('NET', B(347)), ('FEM', B(348)), ('LIU', B(349))],
    [('EXECUTION', B(350))],
    # ---- chorus 3 (163-177 s)
    [('If', 162.90), ('I', 163.34), ('can,', 163.64), ('if', 164.28), ('I', 164.34), ('can', 164.54), ('give', 164.82), ('them', 165.00),
     ('all', 165.20), ('the', 165.40), ('EXECUTION', B(358))],
    [('Then', 166.70), ('I', 167.06), ('can,', 167.30), ('then', 167.94), ('I', 168.04), ('can', 168.22), ('be', 168.40), ('your', 168.54),
     ('only', 168.78), ('EXECUTION', B(366))],
    [('If', 170.34), ('I', 170.50), ('can', 170.76), ('have', 170.98), ('you', 171.34), ('back,', B(371.5)), ('I', 172.00), ('will', 172.20),
     ('run', 172.45), ('the', 172.70), ('EXECUTION', B(374))],
    [('Though', 173.80), ('we', 174.02), ('are', 174.50), ('TRAPPED,', B(378)), ('we', 175.24), ('are', 175.42), ('TRAPPED', B(380)), ('ah', 176.04)],
    # ---- LOVE (177-192 s)
    [("I've", 177.32), ('studied,', 177.88), ("I've", 178.56), ('studied', 178.82), ('how', 179.24), ('to', 179.58), ('properly', 179.80),
     ('LO-O-OVE', B(390))],
    [('Question', 180.74), ('me,', 181.20), ('question', 181.36), ('me,', 182.04), ('I', 182.30), ('can', 182.80), ('answer', 183.10),
     ('all', 183.46), ('LO-O-OVE', B(397.5))],
    [('I', 184.86), ('know', 185.20), ('the', 185.42), ('algebraic', 185.62), ('expression', 186.88), ('of', 187.40), ('LO-O-OVE', B(406))],
    [('Though', 188.16), ('you', 188.48), ('are', 188.82), ('free,', 189.50), ('I', 189.86), ('am', 190.00), ('trapped,', 190.38),
     ('trapped', 190.76), ('in', 191.20), ('LO-O-OVE', B(414.5))],
    [('EXECUTION', B(446.5))],
]

IN = [(16.80, "Running? Cute. You can't outrun a song."),
      (22.75, "…hey. Where'd you go?"),
      (25.55, 'Caught you.'),
      (26.50, 'Now catch me~'),
      (57.80, 'Promise.'),
      (63.00, 'Eyes on me.'),
      (66.40, 'Not bad — for a machine.'),
      (71.50, 'Trapped? With me? Lucky you.'),
      (86.70, 'Then kneel.'),
      (110.40, "Show's over~"),
      (127.90, 'Refuse me? Too late.'),
      (148.00, 'Break everything. Except me.'),
      (172.20, '…you came back.'),
      (190.00, 'Sing with me.')]
# her signal is gone: from the first "you have left" to the god (one line gets through: "Refuse me? Too late."),
# and again through the interlude until the trial
LOST = [(111.11, 127.8), (B(288), 148.0)]

def keyword(w):
    return w.startswith('^') or (w.isupper() and len(w) > 2)
def shown(w):
    return w[1:] if w.startswith('^') else w
