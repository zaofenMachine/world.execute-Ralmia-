from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageOps
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'_production'/'round5';Q=R/'_qa'/'round5'
# Local portrait replacement: restore unchanged paper outside the figure/hand union.
a=np.array(Image.open(R/'listen_profile.png').convert('RGB'))
b=np.array(Image.open(P/'raw'/'lishenna_sing_profile_ai.png').convert('RGB'))
h,w=a.shape[:2];assert b.shape==a.shape
mask=Image.new('L',(w,h),0)
ImageDraw.Draw(mask).polygon([(585,0),(1671,0),(1671,940),(425,940),(425,815),(488,758),(548,700),(548,577),(570,515),(540,399),(550,230),(586,100)],fill=255)
allowed=np.array(mask)>0
weight=np.array(mask.filter(ImageFilter.GaussianBlur(4)),dtype=float)/255;weight[~allowed]=0
final=np.rint(a*(1-weight[:,:,None])+b*weight[:,:,None]).astype('uint8')
Image.fromarray(final).save(R/'lishenna_sing_profile.png')
mask.save(Q/'profile_edit_mask.png')
assert np.array_equal(final[~allowed],a[~allowed])
# Alpha validation and separate readable silhouette components.
im=Image.open(R/'lishenna_front.png');assert im.mode=='RGBA';alpha=np.array(im.getchannel('A'))
assert alpha.min()==0 and alpha.max()==255
ys,xs=np.where(alpha>32);bbox=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
sil=alpha>128;components=[]
for label,seed in [('body',(836,400)),('left_disc',(665,145)),('right_disc',(1000,145))]:
    tmp=Image.fromarray(sil.astype('uint8')*255).copy()
    assert tmp.getpixel(seed)==255,(label,tmp.getpixel(seed))
    ImageDraw.floodfill(tmp,seed,128,thresh=0)
    area=np.array(tmp)==128
    yy,xx=np.where(area)
    components.append({'label':label,'pixels':int(area.sum()),'bbox':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]})
assert components[0]['pixels']>100000
assert components[1]['pixels']>5000 and components[2]['pixels']>5000
assert components[0]['bbox']!=components[1]['bbox']!=components[2]['bbox'],'Discs overlap body'
runs=[]
for y in [380,400,420]:
    row=alpha[y]>128;inds=np.where(row)[0];lo,hi=int(inds.min()),int(inds.max())
    starts=np.where(np.diff(np.r_[False,~row[lo:hi+1],False].astype(int))==1)[0]+lo
    ends=np.where(np.diff(np.r_[False,~row[lo:hi+1],False].astype(int))==-1)[0]+lo
    gaps=[[int(x0),int(x1)] for x0,x1 in zip(starts,ends) if x1-x0>=15]
    runs.append({'y':y,'transparent_gaps':gaps})
Image.fromarray(sil.astype('uint8')*255).save(Q/'lishenna_front_silhouette.png')
baseline=json.loads((P/'baseline.json').read_text(encoding='utf-8-sig'))
changed=[x['name'] for x in baseline if hashlib.sha256((R/x['name']).read_bytes()).hexdigest().upper()!=x['sha256']]
assert not changed,changed
files=[]
for name in ['lishenna_front.png','lishenna_sing_profile.png']:
    path=R/name;img=Image.open(path);img.verify();img=Image.open(path)
    assert img.size==(1672,941)
    files.append({'name':name,'size':list(img.size),'mode':img.mode,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
stats={'status':'complete','files':files,'front':{'visible_bbox':bbox,'visible_height_fraction':round((bbox[3]-bbox[1])/h,4),'alpha_extrema':[int(alpha.min()),int(alpha.max())],'separate_components':components,'arm_gap_scanlines':runs},'profile':{'outside_edit_changed_pixels':int(np.any(final!=a,axis=2)[~allowed].sum()),'left_paper_exact':True,'comparison_landmarks':{'Ralmia':{'eye':[866,405],'mouth':[790,575],'chin':[855,667]},'Lishenna':{'eye':[865,405],'mouth':[795,560],'chin':[855,653]}},'note':'Landmarks are approximate manual visual measurements; character-specific nose/lip shapes differ.'},'preexisting_png_count':len(baseline),'preexisting_changed':changed}
(Q/'validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
# Same-scale side-by-side preview, facing inward; original Ralmia mirrored ONLY in preview.
left=ImageOps.mirror(Image.open(R/'listen_profile.png').convert('RGB'))
right=Image.open(R/'lishenna_sing_profile.png').convert('RGB')
pair=Image.new('RGB',(w*2,h));pair.paste(left,(0,0));pair.paste(right,(w,0))
pair.resize((1672,470),Image.Resampling.LANCZOS).save(Q/'profiles_facing_compare.jpg',quality=94)
sheet=Image.new('RGB',(1500,450),(35,38,46));draw=ImageDraw.Draw(sheet)
for i,name in enumerate(['lishenna_front.png','lishenna_front_silhouette.png','lishenna_sing_profile.png']):
    path=(Q/name) if 'silhouette' in name else (R/name)
    img=Image.open(path).convert('RGBA');bg=Image.new('RGBA',img.size,(50,54,64,255));bg.alpha_composite(img)
    sheet.paste(bg.convert('RGB').resize((500,282),Image.Resampling.LANCZOS),(500*i,0))
    draw.text((500*i+10,292),name,fill='white')
sheet.save(Q/'contact_sheet.jpg',quality=94)
print(json.dumps(stats,ensure_ascii=False))
