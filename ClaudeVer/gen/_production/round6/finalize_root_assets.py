from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib
from alpha_utils import clean,canvas
R=Path(__file__).resolve().parents[2];P=R/'_production'/'round6';Q=R/'_qa'/'round6'
stats={}
def arr(path,mode='RGBA'):return np.array(canvas(Image.open(path).convert(mode)))
def save(a,path):Image.fromarray(a).save(path)
def paired(a,b,mask,name,key):
    am=np.array(mask)>0
    wt=np.array(mask.filter(ImageFilter.GaussianBlur(2)),dtype=float)/255;wt[~am]=0
    out=np.rint(a*(1-wt[:,:,None])+b*wt[:,:,None]).astype('uint8')
    save(out,R/name);mask.save(Q/(key+'_edit_mask.png'))
    stats[key]={'A':key+'_together.png' if key=='cube' else 'lishenna_sit.png','B':name,'outside_edit_pixels':int((~am).sum()),'outside_changed_pixels':int(np.any(out!=a,axis=2)[~am].sum())}
    assert stats[key]['outside_changed_pixels']==0
    return out
# Sitting B: only lower legs and shoes, with above-knee and hair invariant.
a=arr(R/'lishenna_sit.png');b=np.array(clean(Image.open(P/'raw'/'lishenna_sit_b_ai.png')))
h,w=a.shape[:2];yy,xx=np.indices((h,w))
m=Image.new('L',(w,h),0);d=ImageDraw.Draw(m)
d.rectangle((470,585,1080,885),fill=255)
d.polygon([(694,522),(790,522),(828,602),(470,650),(470,585)],fill=255)
d.polygon([(789,540),(860,540),(944,630),(1060,650),(1080,815),(790,885)],fill=255)
ma=np.array(m)
hand_skin=(xx>640)&(xx<715)&(yy>505)&(yy<553)&(a[:,:,0]>180)&(a[:,:,1]>95)&(a[:,:,0]>a[:,:,1]*1.1)&(a[:,:,1]>a[:,:,2]*1.02)
ma[hand_skin]=0
ma[520:559,615:679]=0
pink=(a[:,:,0]>a[:,:,1]*1.15)&(a[:,:,1]>85)&(a[:,:,0]>150)&(yy<630)&(xx>895)
ma[pink]=0
out=paired(a,b,Image.fromarray(ma),'lishenna_sit_b.png','sit')
stats['sit']['above_y522_exact']=bool(np.array_equal(out[:522],a[:522]))
# Cube B: remove Lishenna/reveal previously hidden Ralmia, keep visible face/body and pose.
a=arr(R/'cube_together.png')
b=np.array(clean(Image.open(P/'raw'/'cube_alone_hand_repaired_ai.png')))
m=Image.new('L',(w,h),0);d=ImageDraw.Draw(m)
d.polygon([(824,0),(824,140),(831,169),(818,214),(840,254),(813,316),(806,359),(839,385),(870,400),(896,500),(919,568),(929,665),(875,665),(875,940),(1671,940),(1671,0)],fill=255)
d.rectangle((874,483,933,555),fill=255)
ma=np.array(m)
# Keep the already-visible face and cyan gem exactly.
face=Image.new('L',(w,h),0);fd=ImageDraw.Draw(face)
fd.polygon([(736,144),(792,137),(815,153),(817,179),(814,211),(795,236),(758,226),(737,206)],fill=255)
ma[np.array(face)>0]=0
# Preserve visible blonde hair while excluding Lishenna's small partly-hidden speaker.
gold=(a[:,:,0]>150)&(a[:,:,1]>110)&(a[:,:,1]>a[:,:,2]*1.17)&(a[:,:,0]>a[:,:,1]*1.02)&(xx<925)&(yy<430)&(a[:,:,3]>0)
gold[(xx>=820)&(yy<146)]=False
ma[gold]=0
out=paired(a,b,Image.fromarray(ma),'cube_alone.png','cube')
stats['cube']['face_exact']=bool(np.array_equal(out[np.array(face)>0],a[np.array(face)>0]))
# Mechanical layer: exact original RGB in opaque retained pixels; generated matte edge.
source=arr(R/'creation_inverse_v2.png','RGB')
mech=np.array(clean(Image.open(P/'raw'/'creation_hand_ralmia_ai.png')))
opaque=mech[:,:,3]>=250
mech[opaque,:3]=source[opaque]
save(mech,R/'creation_hand_ralmia.png')
stats['mechanical_layer']={'opaque_rgb_matches_source':bool(np.array_equal(mech[opaque,:3],source[opaque])),'opaque_pixels':int(opaque.sum())}
# Natural fingertip layer, keep repaired AI color throughout, register leading tip by integer translation.
human=clean(Image.open(P/'raw'/'creation_hand_lishenna_final_ai.png'))
ha=np.array(human);active=ha[:,:,3]>128
ys,xs=np.where(active)
tipx=int(xs.min());tiprows=np.where(active[:,tipx])[0];tipy=int(round(float(tiprows.mean())))
dx,dy=826-tipx,403-tipy
registered=Image.new('RGBA',(w,h));registered.alpha_composite(human,(dx,dy));registered.save(R/'creation_hand_lishenna.png')
stats['human_layer']={'AI_tip':[tipx,tipy],'registration_translation':[dx,dy],'final_tip':[826,403],'upscaled':False}
# Restore original background outside both original hand supports, complete occluded background with AI plate.
hm=np.maximum(mech[:,:,3],ha[:,:,3])
mask=Image.fromarray((hm>1).astype('uint8')*255).filter(ImageFilter.MaxFilter(35))
allow=np.array(mask)>0
plate=arr(P/'raw'/'creation_plate_ai.png','RGB')
plate[~allow]=source[~allow]
save(plate,R/'creation_plate.png');mask.save(Q/'creation_plate_edit_mask.png')
stats['plate']={'outside_changed_pixels':int(np.any(plate!=source,axis=2)[~allow].sum())}
# Layer reassembly and pair previews.
bg=Image.fromarray(plate).convert('RGBA');bg.alpha_composite(Image.fromarray(mech));bg.alpha_composite(registered)
bg.convert('RGB').save(Q/'creation_layers_composite.jpg',quality=95)
detail=bg.crop((735,340,925,480)).resize((760,560),Image.Resampling.NEAREST);detail.save(Q/'creation_fingertips_detail.png')
for key,A,B in [('sit','lishenna_sit.png','lishenna_sit_b.png'),('cube','cube_together.png','cube_alone.png')]:
    frames=[]
    for name in [A,B]:
        im=Image.open(R/name).convert('RGBA');back=Image.new('RGBA',im.size,(48,52,62,255));back.alpha_composite(im)
        frames.append(back.convert('RGB').resize((836,470),Image.Resampling.LANCZOS))
    joined=Image.new('RGB',(1672,470));joined.paste(frames[0],(0,0));joined.paste(frames[1],(836,0))
    joined.save(Q/(key+'_compare.jpg'),quality=95)
    pal=joined.quantize(colors=255);ff=[im.quantize(palette=pal) for im in frames]
    ff[0].save(Q/(key+'_switch.gif'),save_all=True,append_images=ff[1:],duration=600,loop=0,optimize=False)
(Q/'root_validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False))
# Preserve the latest foot-direction feedback when rebuilding this batch.
feedback_script=P/'apply_sit_depth_feedback.py'
if feedback_script.exists() and (P/'raw'/'sit_b_depth_knee_repair_ai6.png').exists():
    import runpy
    runpy.run_path(str(feedback_script),run_name='__main__')
