from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import numpy as np,json,hashlib,re
R=Path(__file__).resolve().parents[2];P=R/'_production'/'round6';Q=R/'_qa'/'round6'
calls=json.loads((P/'prior_generation_tool_calls.json').read_text(encoding='utf-8'))
constants={}
for item in calls:
    code=item['payload'].get('input','')
    for key,value in re.findall(r'store\("(r6_(?:style|lish|ral))","((?:\\.|[^"])*)"\)',code):
        constants[key]=json.loads('"'+value+'"')
recovered=[]
for item in calls:
    code=item['payload'].get('input','');m=re.search(r'const prompt=\x60(.*?)\x60(.*?);',code,re.S)
    if not m:continue
    prompt=m.group(1)
    for k in re.findall(r'load\("(r6_[^"]+)"\)',m.group(2)):prompt+=' '+constants.get(k,k)
    rm=re.search(r'const refs=\[(.*?)\];',code,re.S)
    refs=[]
    if rm:
        for value in re.findall(r'root\+"((?:\\.|[^"])*)"',rm.group(1)):
            refs.append(json.loads('"'+value+'"').lstrip('\\').replace('\\','/'))
    am=re.search(r'asset(?::|===)"([^"]+)"',code)
    dest=re.findall(r'\\+raw\\+([^\'"]+\.png)',code)
    recovered.append({'call_id':item['payload'].get('call_id'),'asset':am.group(1) if am else None,'prompt':prompt,'references':refs,'raw_destinations':dest,'status':'not_executed_reference_limit' if len(refs)>5 else 'generated'})
(P/'recovered_generation_records.json').write_text(json.dumps(recovered,ensure_ascii=False,indent=2),encoding='utf-8')
names=['creation_plate.png','creation_hand_ralmia.png','creation_hand_lishenna.png','cube_together.png','cube_alone.png','ledge_together.png','ledge_alone.png','cat_ralmia_v2.png','cat_ralmia_v2b.png','lishenna_sit.png','lishenna_sit_b.png','ending_together.png']
files=[]
for name in names:
    p=R/name;im=Image.open(p);im.verify();im=Image.open(p)
    assert im.size==(1672,941),(name,im.size)
    transparent=name not in ['creation_plate.png','ledge_together.png','ledge_alone.png']
    row={'name':name,'size':list(im.size),'mode':im.mode,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    if transparent:
        assert im.mode=='RGBA',name
        aa=np.array(im.getchannel('A'));assert aa.min()==0 and aa.max()==255,name
        ys,xs=np.where(aa>32);row['visible_bbox']=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
        if name.startswith('lishenna_sit'):
            row['max_rotation_radius']=round(float(np.sqrt((xs-835.5)**2+(ys-470)**2).max()),2)
            assert row['max_rotation_radius']<470, 'Insufficient rotation margin'
    files.append(row)
pairs=[]
for key,an,bn,mn in [('cube','cube_together.png','cube_alone.png','cube_edit_mask.png'),('ledge','ledge_together.png','ledge_alone.png','ledge_edit_mask.png'),('cat','cat_ralmia_v2.png','cat_ralmia_v2b.png','cat_face_edit_mask.png'),('sit','lishenna_sit.png','lishenna_sit_b.png','sit_edit_mask.png')]:
    a=np.array(Image.open(R/an).convert('RGBA'));b=np.array(Image.open(R/bn).convert('RGBA'));m=np.array(Image.open(Q/mn).convert('L'))>0
    count=int(np.any(a!=b,axis=2)[~m].sum());assert count==0,(key,count)
    pairs.append({'group':key,'A':an,'B':bn,'edit_mask':mn,'outside_pixels':int((~m).sum()),'outside_changed_pixels':count})
baseline=json.loads((P/'baseline.json').read_text(encoding='utf-8-sig'))
changed=[x['name'] for x in baseline if hashlib.sha256((R/x['name']).read_bytes()).hexdigest().upper()!=x['sha256']]
assert not changed,changed
stats={'status':'complete','delivered_count':len(names),'transparent_count':9,'files':files,'pairs':pairs,'preexisting_count':len(baseline),'preexisting_changed':changed,'root':json.loads((Q/'root_validation.json').read_text(encoding='utf-8')),'cat':json.loads((Q/'cat_validation.json').read_text(encoding='utf-8')),'ledge':json.loads((Q/'ledge_validation.json').read_text(encoding='utf-8')),'ending':json.loads((Q/'ending_validation.json').read_text(encoding='utf-8'))}
(Q/'validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
manifest={'status':'complete','request':'request_v2c.md','generator':'built-in image_gen','execution':'Independent ledge, cat and ending generation ran concurrently in subagents; dependent B edits followed each A.','user_postprocessing_authorization':'Pixel restore, only downscale/translation registration, alpha-edge cleanup; no upscale.','assets':names,'generation_records':['recovered_generation_records.json','cube_hand_repair_prompt.json','ledge_generation.json','cat_generation.json','ending_generation.json'],'recovered_calls':recovered,'validation':'_qa/round6/validation.json'}
(P/'prompts.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
if (P/'sit_foot_direction_feedback.json').exists():
    manifest['generation_records'] += ['sit_foot_direction_feedback.json','sit_foot_direction_attempt2.json','sit_foot_direction_attempt3.json','sit_foot_direction_attempt4.json','sit_foot_direction_attempt5.json','sit_foot_direction_attempt6.json']
    (P/'prompts.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
# Twelve deliverables, same panel size, all transparent layers shown on neutral gray.
tw,th=500,282
sheet=Image.new('RGB',(tw*3,(th+28)*4),(34,38,45));draw=ImageDraw.Draw(sheet)
for i,name in enumerate(names):
    im=Image.open(R/name).convert('RGBA');bg=Image.new('RGBA',im.size,(54,58,68,255));bg.alpha_composite(im)
    x=(i%3)*tw;y=(i//3)*(th+28)
    sheet.paste(bg.convert('RGB').resize((tw,th),Image.Resampling.LANCZOS),(x,y));draw.text((x+10,y+th+7),name,fill='white')
sheet.save(Q/'contact_sheet.jpg',quality=94)
Image.open(R/'lishenna_sit.png').crop((625,470,1045,585)).resize((1260,345)).save(Q/'sit_support_detail.png')
print(json.dumps({'status':'complete','images':len(files),'pairs':pairs,'old_images':len(baseline),'old_changed':changed},ensure_ascii=False))
