from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json
R=Path(__file__).resolve().parents[2];P=R/'_production'/'round4';Q=R/'_qa'/'round4'
a=np.array(Image.open(P/'raw'/'pinky_before_proportion_feedback.png').convert('RGB'))
b=np.array(Image.open(P/'raw'/'pinky_proportion_feedback_ai.png').convert('RGB'))
assert a.shape==b.shape
h,w=a.shape[:2];m=Image.new('L',(w,h),0);d=ImageDraw.Draw(m)
d.rectangle((0,300,434,700),fill=255)
d.rectangle((1141,230,1671,924),fill=255)
yy,xx=np.indices((h,w))
core=(xx-486)**2+(yy-514)**2<92**2
protected=np.array(m)
protected[core]=0
m=Image.fromarray(protected)
mask=np.array(m)>0
weight=np.array(m.filter(ImageFilter.GaussianBlur(3)),dtype=float)/255
weight[~mask]=0
out=np.rint(a*(1-weight[:,:,None])+b*weight[:,:,None]).astype('uint8')
Image.fromarray(out).save(R/'pinky_promise_v2.png')
m.save(Q/'pinky_proportion_edit_mask.png')
assert np.array_equal(a[:,435:1141],out[:,435:1141])
assert np.array_equal(a[core],out[core])
stats={'status':'complete','asset':'pinky_promise_v2.png','outside_changed_pixels':int(np.any(a!=out,axis=2)[~mask].sum()),'fingers_palm_core_and_thread_exact':True,'fixed_central_columns':[435,1141],'palm_core_roi':{'center':[486,514],'radius':92}}
(Q/'pinky_proportion_validation.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
print(stats)
# Matching alone B is derived by AI local edit on corrected A, then lock non-edit pixels.
pair_a=out.copy()
pair_b=np.array(Image.open(P/'raw'/'pinky_alone_v2_ai.png').convert('RGB'))
bm=Image.new('L',(w,h),0);bd=ImageDraw.Draw(bm);bd.rectangle((750,235,1671,924),fill=255)
bmask=np.array(bm)
pinkym=Image.new('L',(w,h),0)
ImageDraw.Draw(pinkym).polygon([(774,414),(789,366),(804,359),(816,361),(829,369),(833,381),(826,406),(815,429),(800,450),(778,467),(758,474),(754,457)],fill=255)
robot=(np.array(pinkym)>0)&(np.max(pair_a,axis=2)<150)&(np.abs(pair_a[:,:,0].astype(int)-pair_a[:,:,1].astype(int))<16)
bmask[robot]=0
bm=Image.fromarray(bmask);editable=bmask>0
bw=np.array(bm.filter(ImageFilter.GaussianBlur(2)),dtype=float)/255;bw[~editable]=0
alone=np.rint(pair_a*(1-bw[:,:,None])+pair_b*bw[:,:,None]).astype('uint8')
Image.fromarray(alone).save(R/'pinky_alone_v2.png')
bm.save(Q/'pinky_alone_v2_edit_mask.png')
stats['alone_pair']={'asset':'pinky_alone_v2.png','outside_changed_pixels':int(np.any(alone!=pair_a,axis=2)[~editable].sum()),'mechanical_forearm_exact':bool(np.array_equal(alone[:,:750],pair_a[:,:750]))}
assert stats['alone_pair']['outside_changed_pixels']==0
assert stats['alone_pair']['mechanical_forearm_exact']
import hashlib
old_hashes=json.loads((P/'before_proportion_feedback_hashes.json').read_text(encoding='utf-8-sig'))
changed=[x['name'] for x in old_hashes if hashlib.sha256((R/x['name']).read_bytes()).hexdigest().upper()!=x['sha256']]
assert changed==['pinky_promise_v2.png'],changed
stats['existing_files_changed']=changed
(Q/'pinky_proportion_validation.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
# Refresh final file hashes and contact previews.
v=json.loads((Q/'validation.json').read_text(encoding='utf-8'))
v['pinky_promise_v2.png']=stats
v['pinky_alone_v2.png']=stats['alone_pair']
v['proportion_feedback']='Left-arm invariance versus old v1 no longer applies: user requested a slimmer forearm. Use the new matching pinky_alone_v2.'
for name in ['pinky_promise_v2.png','pinky_alone_v2.png']:
    p=R/name
    row={'name':name,'size':[w,h],'mode':'RGB','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    v['files']=[x for x in v['files'] if x['name']!=name]+[row]
(Q/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
names=['lishenna_ref_sheet.png','pinky_promise_v2.png','creation_inverse_v2.png','stage.png','stage_empty.png','lishenna_walk.png','lishenna_stand.png','lishenna_float.png','pinky_alone_v2.png']
tw,th=500,282
sheet=Image.new('RGB',(1500,930),(35,38,46));draw=ImageDraw.Draw(sheet)
for i,name in enumerate(names):
    im=Image.open(R/name).convert('RGBA');bg=Image.new('RGBA',im.size,(50,54,64,255));bg.alpha_composite(im)
    x=(i%3)*tw;y=(i//3)*(th+28)
    sheet.paste(bg.convert('RGB').resize((tw,th),Image.Resampling.LANCZOS),(x,y))
    draw.text((x+10,y+th+7),name,fill='white')
sheet.save(Q/'contact_sheet.jpg',quality=92)
for stem,aa,bb in [('pinky_proportion_before_after',P/'raw'/'pinky_before_proportion_feedback.png',R/'pinky_promise_v2.png'),('pinky_v2_pair',R/'pinky_promise_v2.png',R/'pinky_alone_v2.png')]:
    ims=[Image.open(p).convert('RGB').resize((836,470),Image.Resampling.LANCZOS) for p in [aa,bb]]
    join=Image.new('RGB',(1672,470));join.paste(ims[0],(0,0));join.paste(ims[1],(836,0));palette=join.quantize(colors=255)
    frames=[im.quantize(palette=palette) for im in ims]
    frames[0].save(Q/(stem+'.gif'),save_all=True,append_images=frames[1:],duration=650,loop=0,optimize=False)
    if stem=='pinky_proportion_before_after':
        compare=Image.new('RGB',(1672,500),(35,38,46));compare.paste(ims[0],(0,0));compare.paste(ims[1],(836,0))
        dd=ImageDraw.Draw(compare);dd.text((10,478),'Before',fill='white');dd.text((846,478),'After',fill='white')
        compare.save(Q/'pinky_proportion_before_after.jpg',quality=94)
print(json.dumps(stats))
