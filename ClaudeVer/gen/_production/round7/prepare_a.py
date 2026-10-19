from pathlib import Path
from PIL import Image
import numpy as np,json,sys
R=Path(__file__).resolve().parents[2]; P=R/'_production'/'round7'; Q=R/'_qa'/'round7'
sys.path.insert(0,str(R/'_production'/'round6'))
from alpha_utils import clean
source=P/'raw'/'lishenna_stroll_a_profile_ai.png'
im=clean(Image.open(source)); aa=np.array(im.getchannel('A'))
ys,xs=np.where(aa>32)
box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
scale=min(1.,800/(box[3]-box[1]))
crop=im.crop(box)
if scale<1:
    crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
ys,xs=np.where(np.array(crop.getchannel('A'))>128)
dx=round(835.5-(int(xs.min())+int(xs.max()))/2)
dy=847-int(ys.max())
out=Image.new('RGBA',(1672,941));out.alpha_composite(crop,(dx,dy))
# Integer-register the trailing shoe's ground contact. Blend only the tiny
# proximal ankle transition; keep all generated shoe pixels at native scale.
arr=np.array(out); yy,xx=np.indices(arr.shape[:2])
rear=(arr[:,:,3]>128)&(xx<850)&(yy>700)
rear_y=int(np.where(rear)[0].max()); foot_dy=847-rear_y
assert 0<=foot_dy<=12,foot_dy
if foot_dy:
    moved=np.roll(arr,foot_dy,axis=0);moved[:foot_dy]=0
    wt=np.clip((yy-700)/24,0,1)*((xx<850)&(yy<885))
    arr=np.rint(arr*(1-wt[:,:,None])+moved*wt[:,:,None]).astype('uint8')
    out=Image.fromarray(arr)
out.save(R/'lishenna_stroll_a.png')
stat={'source':source.name,'source_canvas':list(im.size),'source_visible_bbox':box,
      'scale':scale,'crop_placement':[dx,dy],'upscaled':False,
      'ground_contact_y_alpha_gt128':847,'rear_foot_integer_translation':[0,foot_dy],
      'target_canvas':[1672,941]}
(Q/'a_registration.json').write_text(json.dumps(stat,indent=2),encoding='utf-8')
record=json.loads((P/'prompt_a_profile_fix.json').read_text(encoding='utf-8'))
record.update(status='complete',raw_output='raw/'+source.name,output='lishenna_stroll_a.png')
(P/'prompt_a_profile_fix.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stat))
