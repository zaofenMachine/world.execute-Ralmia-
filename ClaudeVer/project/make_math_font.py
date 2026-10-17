"""Blackboard formulas need Greek and maths symbols, which Plex Mono / Instrument Serif lack.
Instance the system Noto Sans SC variable font (OFL) at a light weight and subset it to Latin + Greek + maths.
usage: python make_math_font.py [path to NotoSansSC-VF.ttf]   -> fonts/NotoSansSC-Light-math-subset.ttf"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset
src = sys.argv[1] if len(sys.argv) > 1 else r'C:\Windows\Fonts\NotoSansSC-VF.ttf'
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'NotoSansSC-Light-math-subset.ttf')
f = instancer.instantiateVariableFont(TTFont(src), {'wght': 350})
chars = ''.join(chr(c) for c in range(0x20, 0x7f)) + 'πθγλΔΣ√∞²³¹⁻ⁿ½→≠≈±·×÷∫∂′−∈∀ħ∇ψερμνΩ≥≤ĤΨ⋅∙' + 'ΩωΦφμ'
opt = subset.Options(); opt.layout_features = ['kern', 'liga']; opt.notdef_outline = True
ss = subset.Subsetter(opt); ss.populate(text=chars); ss.subset(f)
f.save(out); print(out, os.path.getsize(out))
