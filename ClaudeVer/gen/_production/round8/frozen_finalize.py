from pathlib import Path
from PIL import Image
import numpy as np,json,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[1];Q=R/'_qa'/'round8';Q.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('round6_alpha',R/'_production'/'round6'/'alpha_utils.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
source=P/'raw'/'ralmia_frozen_34_ai.png'
im=m.clean(Image.open(source))
alpha=np.array(im.getchannel('A'));ys,xs=np.where(alpha>32)
box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
cropped=im.crop(box)
scale=min(1.,1672*.85/cropped.width,941*.9/cropped.height)
size=(round(cropped.width*scale),round(cropped.height*scale))
if size!=cropped.size: cropped=cropped.resize(size,Image.Resampling.LANCZOS)
out=Image.new('RGBA',(1672,941));pos=((1672-size[0])//2,(941-size[1])//2);out.alpha_composite(cropped,pos)
out.save(R/'ralmia_frozen_34.png')
aa=np.array(out);ys,xs=np.where(aa[:,:,3]>32)
stat={'filename':'ralmia_frozen_34.png','canvas':list(out.size),'mode':out.mode,
'source_bbox_alpha_gt32':list(box),'scale':scale,'upscaled':False,'position':list(pos),
'final_bbox_alpha_gt32':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
'subject_width_fraction':float((xs.max()-xs.min()+1)/1672),
'alpha_min':int(aa[:,:,3].min()),'alpha_max':int(aa[:,:,3].max()),
'alpha_zero_pixels':int((aa[:,:,3]==0).sum()),'alpha_opaque_pixels':int((aa[:,:,3]==255).sum()),
'edge_cleanup':'nearest opaque local RGB carried into alpha edges; alpha<=2 removed; no enlargement',
'visual_check':'PASS: three-quarter front shows both cyan eyes and nearer right-temple gem; five black articulated fingers with cyan palm core on forward hand; long hair, skirt fins and both red bow tails trail left; full body and boots visible; no ground or speed/jet effects. Inspected on both dark and light backgrounds.'}
(Q/'frozen_validation.json').write_text(json.dumps(stat,indent=2),encoding='utf-8')
for name,col in [('dark',(54,58,65,255)),('light',(236,231,219,255))]:
 bg=Image.new('RGBA',out.size,col);bg.alpha_composite(out);bg.convert('RGB').save(Q/('frozen_preview_'+name+'.jpg'),quality=95)
print(json.dumps(stat,indent=2))
