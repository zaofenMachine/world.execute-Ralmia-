from pathlib import Path
from PIL import Image
import json
from alpha_utils import fit_height
P=Path(__file__).resolve().parent
R=P.parents[1];Q=R/'_qa'/'round6';Q.mkdir(exist_ok=True,parents=True)
meta=json.loads((P/'cat_generation.json').read_text(encoding='utf-8'))
meta['assets'].append({"filename":"cat_ralmia_v2.png","step":"A framing correction","prompt":"Use case: precise-object-edit. Image 1 is the edit target, image 2 the canonical character identity. Produce the EXACT same waist-up Ralmia cat-paw illustration, same wink, cute omega mouth, black mechanical fists, tabby cat ears, gem on viewer-left, red bow and white armor. Only adjust framing: zoom the entire figure OUT uniformly about 10%, centered, leaving transparent breathing space at top and bottom. Complete the very top of the ahoge hair loop so it is fully inside the frame and has a smooth uncut curve. Keep lower edge at waist and NO legs/tail. Same 16:9 canvas, true transparent background. Keep all outfit, face, ears, hair, hands, pose and style otherwise unchanged. No words or watermark.","references":["_production/round6/cat_a_initial.png","ref_sheet.png"],"source":"C:\\Users\\zaofenMachine\\.codex\\generated_images\\01a14edb-d956-7ae2-b8c5-5d4d3f241d21\\exec-fbbdca44-86cb-49d3-b139-1d1f1d88f6fa.png"})
im,stat=fit_height(Image.open(P/'cat_a_final_ai.png'),.9)
im.save(R/'cat_ralmia_v2.png')
meta['A_registration']=stat
(P/'cat_generation.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
bg=Image.new('RGBA',im.size,(58,60,66,255));bg.alpha_composite(im);bg.convert('RGB').save(Q/'cat_a_preview.jpg')
print(stat)
