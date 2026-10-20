from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'_production'/'round8';Q=R/'_qa'/'round8'
names=['peek_frozen.png','lishenna_wink.png','lishenna_wave_back.png','ralmia_frozen_34.png']
records=[];arrays=[]
for name in names:
    path=R/name; im=Image.open(path);im.verify();im=Image.open(path)
    assert im.size==(1672,941) and im.mode=='RGBA',(name,im.size,im.mode)
    arr=np.array(im);aa=arr[:,:,3];assert aa.min()==0 and aa.max()==255,name
    ys,xs=np.where(aa>32)
    row={'name':name,'size':list(im.size),'mode':im.mode,'bytes':path.stat().st_size,
         'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'bbox_alpha_gt32':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
         'visible_height_fraction':round((ys.max()-ys.min()+1)/941,6),
         'visible_width_fraction':round((xs.max()-xs.min()+1)/1672,6),
         'transparent_pixels':int((aa==0).sum()),'alpha_quantiles_nonzero':[float(x) for x in np.quantile(aa[aa>0],[.05,.5,.95])]}
    records.append(row);arrays.append(arr)
baseline=json.loads((P/'baseline.json').read_text(encoding='utf-8-sig'))
changed=[r['name'] for r in baseline if hashlib.sha256((R/r['name']).read_bytes()).hexdigest().upper()!=r['sha256']]
assert not changed,changed
details={k:json.loads((Q/(k+'_validation.json')).read_text(encoding='utf-8')) for k in ['peek','wink','wave','frozen']}
stats={'status':'complete','asset_count':4,'required_count':3,'optional_count':1,
       'files':records,'preexisting_count':len(baseline),'preexisting_changed':changed,'details':details}
(Q/'validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')

def display(arr,color=(48,52,62,255)):
    im=Image.fromarray(arr);bg=Image.new('RGBA',im.size,color);bg.alpha_composite(im);return bg.convert('RGB')
def edges(arr):
    alpha=arr[:,:,3].astype(float)/255;gray=np.mean(arr[:,:,:3].astype(float),axis=2)
    edge=np.maximum(np.abs(gray-np.roll(gray,1,1)),np.abs(gray-np.roll(gray,1,0)))
    interior=np.minimum.reduce([alpha,np.roll(alpha,1,0),np.roll(alpha,1,1)])
    outer=np.maximum(np.abs(alpha-np.roll(alpha,1,0)),np.abs(alpha-np.roll(alpha,1,1)))*255
    e=np.clip(np.maximum(np.maximum(edge*interior-10,0)*2.2,outer),0,255)/255
    bg=np.zeros((*e.shape,3));bg[:]=[14,19,28]
    return Image.fromarray(np.rint(bg*(1-e[:,:,None])+np.array([239,234,214])*e[:,:,None]).astype('uint8'))
def dots(arr):
    small=Image.fromarray(arr).resize((836,470),Image.Resampling.LANCZOS);sa=np.array(small)
    out=Image.new('RGB',small.size,(14,19,28));d=ImageDraw.Draw(out)
    for y in range(2,470,4):
        for x in range(2,836,4):
            if sa[y,x,3]<96:continue
            lum=float(np.mean(sa[y,x,:3]))/255
            radius=.45+1.25*(1-lum)
            d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(115,220,230))
    return out

for kind in ['contact_sheet','lineart_contact_sheet','dot_contact_sheet']:
    sheet=Image.new('RGB',(1672,996),(30,34,41));d=ImageDraw.Draw(sheet)
    for i,(name,arr) in enumerate(zip(names,arrays)):
        x=(i%2)*836;y=(i//2)*498
        if kind=='contact_sheet':im=display(arr).resize((836,470),Image.Resampling.LANCZOS)
        elif kind=='lineart_contact_sheet':im=edges(arr).resize((836,470),Image.Resampling.LANCZOS)
        else:im=dots(arr)
        sheet.paste(im,(x,y));d.text((x+10,y+478),name,fill='white')
    sheet.save(Q/(kind+'.jpg'),quality=95)
prompts=['peek_prompt.json','peek_detail_edit_prompt.json','peek_left_edge_prompt.json',
         'wink_prompt.json','wave_prompt.json','frozen_prompt.json']
# Include any wave sleeve-fix record without assuming the agent's chosen name.
for path in P.glob('*.json'):
    if 'sleeve' in path.name and path.name not in prompts:prompts.append(path.name)
manifest={'status':'complete','request':'request_v3a.md','generator':'built-in image_gen',
          'execution':'Four independent assets generated concurrently by root and three subagents; local repairs remained sequential per asset.',
          'assets':names,'prompt_records':prompts,'style_board':'style_references.png',
          'postprocessing':'Authorized alpha-edge cleanup, only downscale/translation for framing, local-edit pixel locking; no upscale.',
          'validation':'_qa/round8/validation.json'}
(P/'prompts.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'asset_count':4,'files':records,'old_count':len(baseline),'old_changed':changed},ensure_ascii=False))
