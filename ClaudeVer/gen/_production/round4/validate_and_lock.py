from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json, hashlib
R=Path(__file__).resolve().parents[2]
P=R/'_production'/'round4'; Q=R/'_qa'/'round4'; Q.mkdir(exist_ok=True)
stats={}
def rgb(p): return np.array(Image.open(p).convert('RGB'))
def save(a,p): Image.fromarray(a).save(p)
def lock(a,b,mask,name):
    assert a.shape==b.shape
    m=np.array(mask)>0
    w=np.array(mask.filter(ImageFilter.GaussianBlur(2)),dtype=float)/255
    w[~m]=0
    out=np.rint(a*(1-w[:,:,None])+b*w[:,:,None]).astype('uint8')
    save(out,R/name)
    mask.save(Q/(Path(name).stem+'_edit_mask.png'))
    stats[name]={'outside_edit_pixels':int((~m).sum()),'outside_changed_pixels':int(np.any(out!=a,axis=2)[~m].sum())}
    assert stats[name]['outside_changed_pixels']==0
    return out
# Pinky: AI local edit on original; exact left half and red thread restored.
a=rgb(R/'pinky_promise.png'); b=rgb(P/'raw'/'pinky_promise_v2_ai.png'); h,w=a.shape[:2]
m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rectangle((w//2,230,w-1,924),fill=255)
arr=np.array(m)
yy,xx=np.indices((h,w))
red=(a[:,:,0]>100)&(a[:,:,0]>a[:,:,1]*1.4)&(a[:,:,0]>a[:,:,2]*1.3)&(xx>755)&(xx<892)&(yy>385)&(yy<565)
red=np.array(Image.fromarray(red.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0
arr[red]=0
out=lock(a,b,Image.fromarray(arr),'pinky_promise_v2.png')
assert np.array_equal(out[:,:w//2],a[:,:w//2])
assert np.array_equal(out[red],a[red])
stats['pinky_promise_v2.png'].update(left_half_exact=True,red_thread_exact=True)
# Creation: original fingertip anchor and entire mechanical hand unchanged.
a=rgb(R/'creation_inverse.png'); b=rgb(P/'raw'/'creation_inverse_v2_ai.png'); h,w=a.shape[:2]
m=Image.new('L',(w,h),0); d=ImageDraw.Draw(m)
d.rectangle((838,389,1671,940),fill=255)
d.polygon([(819,389),(838,389),(838,440),(819,420)],fill=255)
d.rectangle((795,378,837,419),fill=0)
out=lock(a,b,m,'creation_inverse_v2.png')
assert np.array_equal(out[378:420,795:838],a[378:420,795:838])
stats['creation_inverse_v2.png'].update(fingertip_anchor_roi=[795,378,838,420],fingertip_anchor_exact=True)
# Pure screen interiors, same three masks in A/B. AI-created base screenshots retained.
a=rgb(P/'raw'/'stage_final_ai.png'); b=rgb(P/'raw'/'stage_empty_ai.png')
h,w=a.shape[:2]
white=np.all(a>180,axis=2)
combined=np.zeros((h,w),bool); screens=[]
for i,seed in enumerate([(250,220),(835,230),(1400,220)],1):
    flood=Image.fromarray(white.astype('uint8')*255).copy()
    ImageDraw.floodfill(flood,seed,128,thresh=0)
    area=np.array(flood)==128
    assert area.sum()>50000
    sy,sx=np.where(area); box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)]
    area[:]=False
    area[box[1]:box[3],box[0]:box[2]]=True
    combined|=area
    Image.fromarray(area.astype('uint8')*255).save(Q/f'stage_screen_{i}_mask.png')
    screens.append({'index':i,'bbox':box,'pixels':int(area.sum())})
a[combined]=255
save(a,R/'stage.png')
Image.fromarray(combined.astype('uint8')*255).save(Q/'stage_screens_mask.png')
# Protect full screen frames and dark structure linework. Lighting, people and venue floor are edit areas.
inside=Image.fromarray(combined.astype('uint8')*255)
ring=(np.array(inside.filter(ImageFilter.MaxFilter(35)))>0)&~combined
region=np.zeros((h,w),bool)
for x0,x1 in [(0,43),(458,520),(1149,1226),(1618,w)]:
    region[:780,x0:x1]=True
region[650:780,:]=True
dark=(np.max(a,axis=2)<48)&(np.max(np.abs(a.astype(int)-b.astype(int)),axis=2)<15)
protected=ring|(region&dark)
protected[430:780,710:965]=False
protected[:82,790:880]=False
# Remove mask fragments intersecting former audience or actual lights.
protected[780:,:]=False
edit=~protected
out=b.copy(); out[protected]=a[protected]; out[combined]=0
save(out,R/'stage_empty.png')
Image.fromarray(edit.astype('uint8')*255).save(Q/'stage_empty_edit_mask.png')
assert np.array_equal(out[protected],a[protected])
assert np.all(a[combined]==255) and np.all(out[combined]==0)
stats['stage_empty.png']={'outside_edit_pixels':int(protected.sum()),'outside_changed_pixels':0,'screen_frames_and_structure_linework_exact':True,'note':'Stage shading changes in lighting edit areas; fixed screen frames and protected structural linework retain A pixels.'}
stats['screens']={'items':screens,'A_RGB':[255,255,255],'B_RGB':[0,0,0],'pure_fill_exact':True}
# File validity, alpha envelopes, immutable baseline check.
names=['pinky_promise_v2.png','creation_inverse_v2.png','stage.png','stage_empty.png','lishenna_walk.png','lishenna_stand.png','lishenna_float.png']
files=[]
for name in names:
    p=R/name; im=Image.open(p); im.verify(); im=Image.open(p)
    row={'name':name,'size':list(im.size),'mode':im.mode,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    assert im.size==(1672,941)
    if name.startswith('lishenna_'):
        assert im.mode=='RGBA'
        alpha=np.array(im.getchannel('A')); assert alpha.min()==0 and alpha.max()==255
        ys,xs=np.where(alpha>32)
        row['visible_bbox']=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
        row['height_fraction']=round((ys.max()+1-ys.min())/im.height,4)
        row['transparent_pixel_fraction']=round(float((alpha==0).mean()),4)
    files.append(row)
baseline=json.loads((P/'baseline_before_batch.json').read_text(encoding='utf-8-sig'))
changes=[]
for item in baseline:
    p=R/item['name']; digest=hashlib.sha256(p.read_bytes()).hexdigest().upper()
    if digest!=item['sha256']: changes.append(item['name'])
assert changes==['lishenna_ref_sheet.png'],changes
stats.update(files=files,baseline_changes=changes,canonical_ref_equals_approved_v3=(R/'lishenna_ref_sheet.png').read_bytes()==(R/'lishenna_ref_sheet_v3.png').read_bytes(),status='complete')
(Q/'validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
# QA contact sheet and paired previews, common palettes prevent palette jitter.
thumbw,thumbh=500,282
sheet=Image.new('RGB',(thumbw*3,(thumbh+28)*3),(35,38,46))
draw=ImageDraw.Draw(sheet)
for i,name in enumerate(['lishenna_ref_sheet.png']+names):
    im=Image.open(R/name).convert('RGBA')
    bg=Image.new('RGBA',im.size,(50,54,64,255)); bg.alpha_composite(im)
    tile=bg.convert('RGB').resize((thumbw,thumbh),Image.Resampling.LANCZOS)
    x=(i%3)*thumbw;y=(i//3)*(thumbh+28)
    sheet.paste(tile,(x,y));draw.text((x+10,y+thumbh+7),name,fill='white')
sheet.save(Q/'contact_sheet.jpg',quality=92)
for stem,aa,bb in [('stage_switch','stage.png','stage_empty.png'),('pinky_switch','pinky_promise.png','pinky_promise_v2.png'),('creation_switch','creation_inverse.png','creation_inverse_v2.png')]:
    ims=[Image.open(R/n).convert('RGB').resize((836,470),Image.Resampling.LANCZOS) for n in [aa,bb]]
    joined=Image.new('RGB',(1672,470));joined.paste(ims[0],(0,0));joined.paste(ims[1],(836,0))
    palette=joined.quantize(colors=255)
    frames=[im.quantize(palette=palette) for im in ims]
    frames[0].save(Q/(stem+'.gif'),save_all=True,append_images=frames[1:],duration=650,loop=0,optimize=False)
print(json.dumps({'status':stats['status'],'delivered':names,'baseline_changes':changes,'pair_stats':{k:v for k,v in stats.items() if isinstance(v,dict) and 'outside_changed_pixels' in v}},ensure_ascii=False))
if (P/'raw'/'pinky_proportion_feedback_ai.png').exists():
    import runpy
    runpy.run_path(str(P/'lock_pinky_proportion_feedback.py'),run_name='__main__')
