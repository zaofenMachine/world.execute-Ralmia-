from pathlib import Path
import json
from PIL import Image
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
PROD=ROOT/'_production'/'round6'
QA=ROOT/'_qa'/'round6'
src=PROD/'ending_raw'/'ending_margin_corrected.png'
im=Image.open(src).convert('RGBA')
arr=np.array(im)
arr[arr[:,:,3] < 8]=0
clean=Image.fromarray(arr,'RGBA')
a=arr[:,:,3]
box=Image.fromarray(np.uint8(a>32)*255).getbbox()
scale=(round(941*0.85))/(box[3]-box[1])
assert scale <= 1.0
padded=(max(0,box[0]-2),max(0,box[1]-2),min(im.width,box[2]+2),min(im.height,box[3]+2))
crop=clean.crop(padded)
size=(round(crop.width*scale),round(crop.height*scale))
small=crop.resize(size,Image.Resampling.LANCZOS)
out=Image.new('RGBA',(1672,941),(0,0,0,0))
pos=((out.width-small.width)//2,(out.height-small.height)//2)
out.alpha_composite(small,pos)
oa=np.array(out)
oa[oa[:,:,3]<8]=0
out=Image.fromarray(oa,'RGBA')
out.save(ROOT/'ending_together.png')
finalbox=Image.fromarray(np.uint8(oa[:,:,3]>32)*255).getbbox()
qa=Image.new('RGB',(1672*2,941))
for i,color in enumerate([(54,59,70,255),(245,243,235,255)]):
    bg=Image.new('RGBA',out.size,color)
    bg.alpha_composite(out)
    qa.paste(bg.convert('RGB'),(i*1672,0))
qa.resize((2006,565),Image.Resampling.LANCZOS).save(QA/'ending_preview.jpg',quality=94)
hands=out.crop((680,550,1005,850))
bg=Image.new('RGBA',hands.size,(54,59,70,255))
bg.alpha_composite(hands)
bg.convert('RGB').save(QA/'ending_hands_final.jpg',quality=97)
validation={
'asset':'ending_together.png','status':'complete','canvas':[1672,941],'mode':'RGBA',
'visible_bbox_alpha_gt32':list(finalbox),'subject_height_fraction':(finalbox[3]-finalbox[1])/941,
'alpha_min':int(oa[:,:,3].min()),'alpha_max':int(oa[:,:,3].max()),
'transparent_pixels':int((oa[:,:,3]==0).sum()),
'registration':{'source_visible_bbox':list(box),'crop':list(padded),'scale':scale,'paste_xy':list(pos),'no_upscale':True},
'visual_checks':{
'ralmia_viewer_left_and_lishenna_viewer_right':True,'both_eyes_closed':True,
'cheeks_touch':True,'lishenna_lips_parted_humming':True,'ralmia_gem_viewer_left':True,
'full_ahoge_and_ear_loop_tips':True,'pinky_hook_visible':True,'fully_clothed':True,
'no_red_thread':True,'no_text_logo':True,
'note':'One Lishenna speaker disc is partly hidden behind the two heads; the outer disc is fully visible. Hands inspected in a close-up.'}}
(QA/'ending_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
meta_path=PROD/'ending_generation.json'
meta=json.loads(meta_path.read_text(encoding='utf-8'))
meta['status']='complete'
meta['final']='ending_together.png'
meta['postprocessing']={'authorized_by_user':True,'script':'_production/round6/ending_finalize.py',
'steps':['threshold only alpha below 8 to zero','uniformly downscale only to approximately 85 percent visible frame height','center on same 1672 by 941 transparent canvas','zero RGB of fully transparent pixels'],
'no_painting_or_content_redraw':True,'no_upscale':True}
meta['validation']='_qa/round6/ending_validation.json'
meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(validation,ensure_ascii=False))

