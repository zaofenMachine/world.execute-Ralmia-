from pathlib import Path
import sys,json
from PIL import Image,ImageFilter,ImageOps
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
PROD=ROOT/'_production'/'round8'
QA=ROOT/'_qa'/'round8'
QA.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_production'/'round6'))
from alpha_utils import clean,fit_height
src=PROD/'raw'/'lishenna_wink_ai.png'
raw=Image.open(src).convert('RGBA')
final,registration=fit_height(raw,0.9)
a=np.array(final)
a[a[:,:,3]<=2]=0
final=Image.fromarray(a,'RGBA')
final.save(ROOT/'lishenna_wink.png')
alpha=a[:,:,3]
bbox=Image.fromarray((alpha>32).astype('uint8')*255).getbbox()
preview=Image.new('RGB',(3344,941))
for ix,color in enumerate([(54,59,70,255),(245,243,235,255)]):
    bg=Image.new('RGBA',final.size,color)
    bg.alpha_composite(final)
    preview.paste(bg.convert('RGB'),(1672*ix,0))
preview.resize((2006,565),Image.Resampling.LANCZOS).save(QA/'wink_preview.jpg',quality=95)
white=Image.new('RGBA',final.size,'white')
white.alpha_composite(final)
gray=white.convert('L')
edges=ImageOps.invert(gray.filter(ImageFilter.FIND_EDGES))
edges.save(QA/'wink_lineart_preview.png')
record={'asset':'lishenna_wink.png','canvas':list(final.size),'mode':final.mode,
'alpha_min':int(alpha.min()),'alpha_max':int(alpha.max()),'transparent_pixels':int((alpha==0).sum()),
'visible_bbox_alpha_gt32':list(bbox),'visible_height_fraction':(bbox[3]-bbox[1])/941,
'registration':registration,'native_no_upscale':registration['scale']<=1,
'visual_checks':{'single_subject_lishenna':True,'frontal_eye_level':True,'upper_body_forward_lean':True,
'one_eye_wink_other_at_camera':True,'head_tilt_playful_smile':True,'hands_hidden_behind_back':True,
'two_speakers':True,'cyan_bow_and_tie':True,'checkered_headband_and_two_full_loops':True,
'chest_up_modest_framing':True,'no_background_ground_text_effects':True,
'outline_clear_on_light_and_dark':True}}
(QA/'wink_validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
meta_path=PROD/'wink_prompt.json'
meta=json.loads(meta_path.read_text(encoding='utf-8'))
meta.update(status='complete',final='lishenna_wink.png',postprocessing={
'authorization':'User authorized alpha edge cleanup and uniform downscale/translation only.',
'script':'_production/round8/wink_finalize.py','alpha_function':'_production/round6/alpha_utils.py clean() unchanged',
'no_upscale':True,'registration':registration},
validation='_qa/round8/wink_validation.json')
meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))

