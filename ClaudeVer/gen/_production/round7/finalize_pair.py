from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib,sys
R=Path(__file__).resolve().parents[2];P=R/'_production'/'round7';Q=R/'_qa'/'round7'
sys.path.insert(0,str(R/'_production'/'round6'))
from alpha_utils import clean
a=np.array(Image.open(R/'lishenna_stroll_a.png').convert('RGBA'))
b=np.array(clean(Image.open(P/'raw'/'lishenna_stroll_b_leg_phase_ai.png')))
assert a.shape==b.shape==(941,1672,4)
yy,xx=np.indices(a.shape[:2]); ground=[]
for side,region in [('rear',xx<850),('front',xx>=850)]:
    contact=(b[:,:,3]>128)&region&(yy>700)
    old_y=int(np.where(contact)[0].max());dy=847-old_y
    assert abs(dy)<=16,(side,dy)
    if dy:
        moved=np.roll(b,dy,axis=0)
        if dy>0:moved[:dy]=0
        else:moved[dy:]=0
        wt=np.clip((yy-690)/30,0,1)*(region&(yy<885))
        b=np.rint(b*(1-wt[:,:,None])+moved*wt[:,:,None]).astype('uint8')
    ground.append({'side':side,'source_contact_y':old_y,'integer_translation':[0,dy]})

def poly(points):
    im=Image.new('L',(1672,941));ImageDraw.Draw(im).polygon(points,fill=255);return np.array(im)>0

old_arm=poly([(773,321),(829,313),(874,355),(878,395),(854,416),
 (817,463),(769,497),(752,505),(744,533),(728,550),(707,566),
 (689,561),(682,548),(696,518),(716,492),(708,473),(706,443),
 (718,405),(745,375),(761,349)])
new_arm=poly([(831,313),(879,313),(912,349),(916,379),(951,407),
 (975,436),(982,460),(1017,477),(1035,507),(1030,548),(999,553),
 (982,533),(957,511),(944,490),(898,486),(873,472),(853,444),
 (844,412),(841,385),(821,368),(821,339)])
legs=poly([(831,481),(853,480),(867,469),(916,462),(938,474),
 (946,509),(984,607),(1155,790),(1155,875),(620,875),
 (620,742),(756,609),(811,531)])
hair_patch=poly([(712,321),(771,305),(816,301),(834,313),(829,340),
 (827,375),(833,396),(828,417),(818,444),(780,466),(723,462),
 (700,430),(700,380)])
hair_path=P/'raw'/'lishenna_stroll_b_hair_repair_ai.png'
if hair_path.exists():
    repaired=np.array(clean(Image.open(hair_path)))
    patch_path=P/'raw'/'hair_patch_repaired_ai.png'
    if patch_path.exists():
        patch=Image.open(patch_path).convert('RGBA')
        assert patch.width>=138 and patch.height>=162
        patch=np.array(patch.resize((138,162),Image.Resampling.LANCZOS))
        py,px=np.indices((162,138))
        edge=np.minimum.reduce([px,137-px,py,161-py])
        blend=np.clip(edge/24,0,1)[:,:,None]
        original=b[305:467,700:838].copy()
        patch[:,:,3]=original[:,:,3]
        repaired[305:467,700:838]=np.rint(original*(1-blend)+patch*blend).astype('uint8')
    b[hair_patch]=repaired[hair_patch]
else:
    hair_patch[:]=False
allowed=old_arm|new_arm|legs|hair_patch
# Visible shorts remain the original A, except where the forward sleeve covers them.
shorts=(xx>820)&(xx<947)&(yy>380)&(yy<491)&(a[:,:,0]<135)&(a[:,:,1]<135)&(a[:,:,2]<135)&(a[:,:,3]>0)
allowed[shorts&~new_arm&~old_arm&~hair_patch]=False
mic=poly([(940,204),(1010,204),(1065,231),(1065,275),(1017,283),
 (1035,313),(1044,338),(1024,381),(1004,402),(977,408),
 (951,393),(940,369),(947,337),(965,309),(961,281),(945,261)])
allowed[mic]=False
allowed[yy<300]=False
# Preserve cyan tie pixels where the moving sleeve does not occlude them.
cyan_a=(a[:,:,1]>a[:,:,0]*1.25)&(a[:,:,2]>a[:,:,0]*1.2)
cyan_b=(b[:,:,1]>b[:,:,0]*1.25)&(b[:,:,2]>b[:,:,0]*1.2)
allowed[cyan_a&cyan_b&(xx>880)&(xx<957)&(yy<402)]=False
mask=Image.fromarray(allowed.astype('uint8')*255)
weight=np.array(mask.filter(ImageFilter.GaussianBlur(1.2)),dtype=float)/255
weight[~allowed]=0
out=np.rint(a*(1-weight[:,:,None])+b*weight[:,:,None]).astype('uint8')
out[~allowed]=a[~allowed]
Image.fromarray(out).save(R/'lishenna_stroll_b.png')
mask.save(Q/'stroll_edit_mask.png')

assert np.array_equal(out[~allowed],a[~allowed])
assert np.array_equal(out[:300],a[:300])
assert np.array_equal(out[mic],a[mic])
files=[]
for name,arr in [('lishenna_stroll_a.png',a),('lishenna_stroll_b.png',out)]:
    ys,xs=np.where(arr[:,:,3]>128)
    feet={side:int(np.where((arr[:,:,3]>128)&region&(yy>700))[0].max())
          for side,region in [('rear',xx<850),('front',xx>=850)]}
    assert feet=={'rear':847,'front':847},(name,feet)
    im=Image.open(R/name);im.verify()
    files.append({'name':name,'canvas':[1672,941],'mode':'RGBA',
      'bbox_alpha_gt128':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
      'height_fraction':round((ys.max()-ys.min()+1)/941,5),'foot_contacts_y':feet,
      'sha256':hashlib.sha256((R/name).read_bytes()).hexdigest()})
baseline=json.loads((P/'baseline.json').read_text(encoding='utf-8-sig'))
changed=[r['name'] for r in baseline if hashlib.sha256((R/r['name']).read_bytes()).hexdigest().upper()!=r['sha256']]
assert not changed,changed
stats={'status':'complete','files':files,'outside_edit_pixels':int((~allowed).sum()),
 'outside_changed_pixels':0,'head_and_upper_y_lt300_exact':True,
 'microphone_arm_locked_pixels':int(mic.sum()),'microphone_arm_changed_pixels':0,
 'b_foot_registration':ground,'preexisting_count':len(baseline),'preexisting_changed':changed,
 'a_registration':json.loads((Q/'a_registration.json').read_text()),
 'mask':'stroll_edit_mask.png'}
(Q/'validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')

def display(arr):
    im=Image.fromarray(arr);bg=Image.new('RGBA',im.size,(48,52,62,255));bg.alpha_composite(im);return bg.convert('RGB')

frames=[display(x).resize((836,470),Image.Resampling.LANCZOS) for x in [a,out]]
joined=Image.new('RGB',(1672,498),(32,35,42))
d=ImageDraw.Draw(joined)
for i,im in enumerate(frames):joined.paste(im,(i*836,0));d.text((i*836+12,478),['A - left foot forward','B - right foot forward'][i],fill='white')
joined.save(Q/'stroll_compare.jpg',quality=95)
pal=joined.quantize(colors=255);ff=[im.quantize(palette=pal) for im in frames]
ff[0].save(Q/'stroll_switch.gif',save_all=True,append_images=ff[1:],duration=500,loop=0,optimize=False)
# Inspection only: monochrome main-edge extraction on a dark field.
def edges(arr):
    alpha=arr[:,:,3].astype(float)/255
    gray=np.mean(arr[:,:,:3].astype(float),axis=2)
    gx=np.abs(gray-np.roll(gray,1,1));gy=np.abs(gray-np.roll(gray,1,0))
    interior=np.minimum.reduce([alpha,np.roll(alpha,1,0),np.roll(alpha,1,1)])
    detail=np.maximum(gx,gy)*interior
    outer=np.maximum(np.abs(alpha-np.roll(alpha,1,0)),np.abs(alpha-np.roll(alpha,1,1)))*255
    e=np.clip(np.maximum(np.maximum(detail-12,0)*2.2,outer),0,255)/255
    bg=np.zeros((*e.shape,3),dtype='uint8');bg[:]=[14,19,28]
    tint=np.array([239,234,214])
    return Image.fromarray(np.rint(bg*(1-e[:,:,None])+tint*e[:,:,None]).astype('uint8'))
line=Image.new('RGB',(1672,470))
for i,arr in enumerate([a,out]):line.paste(edges(arr).resize((836,470),Image.Resampling.LANCZOS),(836*i,0))
line.save(Q/'lineart_preview.jpg',quality=96)
feet_preview=Image.new('RGB',(1140,210),(48,52,62))
for i,arr in enumerate([a,out]):
    feet_preview.paste(display(arr).crop((600,680,1170,890)),(570*i,0))
ImageDraw.Draw(feet_preview).line((0,167,1139,167),fill=(90,210,180),width=1)
feet_preview.save(Q/'groundline_preview.jpg',quality=95)
rec=json.loads((P/'prompt_b_leg_phase.json').read_text(encoding='utf-8'))
rec.update(status='complete',raw_output='raw/lishenna_stroll_b_leg_phase_ai.png',output='lishenna_stroll_b.png')
(P/'prompt_b_leg_phase.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={'status':'complete','request':'request_v2d.md','generator':'built-in image_gen',
 'assets':['lishenna_stroll_a.png','lishenna_stroll_b.png'],
 'prompt_records':['prompt_a.json','prompt_a_profile_fix.json','prompt_b.json','prompt_b_leg_phase.json','prompt_b_hair_repair.json','prompt_b_hair_patch.json'],
 'pair_method':'B locally edited from A; second leg-only edit corrected near/far walking phase; restore A outside arm/leg mask.',
 'postprocessing':'Authorized downscale/integer positioning, tiny ankle transition blend for groundline registration, alpha edge cleanup, pixel restore.',
 'validation':'_qa/round7/validation.json'}
(P/'prompts.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False))
