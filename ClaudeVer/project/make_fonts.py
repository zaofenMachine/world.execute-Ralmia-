"""Instance the Big Shoulders Display variable font into static weights with overlaps removed (needs skia-pathops)."""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
for w in (900, 700, 300):
    f = TTFont(os.path.join(d, 'BigShouldersDisplay[wght].ttf'))
    instancer.instantiateVariableFont(f, {"wght": w}, overlap=instancer.OverlapMode.REMOVE).save(os.path.join(d, f'BSD-{w}.ttf'))
print('ok')
