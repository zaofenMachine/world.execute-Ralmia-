from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json
from alpha_utils import canvas
P=Path(__file__).resolve().parent
R=P.parents[1];Q=R/'_qa'/'round6';Q.mkdir(parents=True,exist_ok=True)
a=canvas(Image.open(R/'cat_ralmia_v2.png').convert('RGBA'))
b=canvas(Image.open(P/'cat_b_ai.png').convert('RGBA'))
aa=np.array(a);bb=np.array(b)
mask=Image.new('L',a.size);d=ImageDraw.Draw(mask)
d.polygon([(749,391),(773,370),(813,372),(841,402),(828,437),(778,450),(751,431)],fill=255)
d.polygon([(870,330),(924,316),(950,336),(948,389),(924,411),(877,400),(864,374)],fill=255)
d.polygon([(825,420),(856,413),(900,426),(906,466),(876,487),(834,474),(820,450)],fill=255)
raw=np.array(mask)>0
weight=np.array(mask.filter(ImageFilter.GaussianBlur(3)),dtype=float)/255.
weight[~raw]=0
r,g,bl=aa[:,:,0].astype(int),aa[:,:,1].astype(int),aa[:,:,2].astype(int)
gold=(g>bl+32)&(r>g+12)
weight[gold]=0
mask_final=(weight>0)
out=aa.copy()
f=weight[:,:,None]
out[:,:,:3]=np.round(aa[:,:,:3]*(1-f)+bb[:,:,:3]*f).astype(np.uint8)
out[:,:,3]=aa[:,:,3]
out[~mask_final]=aa[~mask_final]
Image.fromarray(out).save(R/'cat_ralmia_v2b.png')
Image.fromarray((mask_final.astype(np.uint8)*255),'L').save(Q/'cat_face_edit_mask.png')
diff=np.any(out!=aa,axis=2)
ys,xs=np.where(np.array(a.getchannel('A'))>32)
stat={'canvas':list(a.size),'A_alpha_min':int(aa[:,:,3].min()),'A_alpha_max':int(aa[:,:,3].max()),
 'bbox_alpha_gt32':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
 'subject_height_fraction':float((ys.max()-ys.min()+1)/941),
 'edit_mask_pixels':int(mask_final.sum()),'outside_mask_pixels':int((~mask_final).sum()),
 'outside_mask_changed_pixels':int((diff&~mask_final).sum()),'inside_mask_changed_pixels':int((diff&mask_final).sum()),
 'alpha_identical':bool(np.array_equal(aa[:,:,3],out[:,:,3])),
 'pixel_lock':'Only facial feature regions from the built-in local edit were composited; hair, ears, hands, torso, gem and all alpha are from A.'}
assert stat['outside_mask_changed_pixels']==0
(Q/'cat_validation.json').write_text(json.dumps(stat,indent=2),encoding='utf-8')
frames=[]
for im in (a,Image.fromarray(out)):
 bg=Image.new('RGBA',im.size,(58,60,66,255));bg.alpha_composite(im);frames.append(bg.convert('RGB'))
combined=Image.new('RGB',(1672*2,941));combined.paste(frames[0],(0,0));combined.paste(frames[1],(1672,0))
combined.resize((1672,470),Image.Resampling.LANCZOS).save(Q/'cat_pair_preview.jpg',quality=94)
palette=combined.resize((1000,282)).quantize(colors=255)
gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
gif[0].save(Q/'cat_switch.gif',save_all=True,append_images=gif[1:],duration=450,loop=0,disposal=2)
print(json.dumps(stat,indent=2))
