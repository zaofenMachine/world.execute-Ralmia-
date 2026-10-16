from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(r'F:\Project\world.execute-Ralmia-\ClaudeVer\gen')
source=Path(r'C:\Users\zaofenMachine\.codex\generated_images\01a1408d-5dd4-7781-ab21-3edd8fac2f3c\exec-7efbb7cb-6ddc-4b72-b123-b76e244c21ed.png')
raw=root/'_production'/'round2'/'raw'
qa=root/'_qa'/'round2'
raw.mkdir(parents=True,exist_ok=True)
qa.mkdir(parents=True,exist_ok=True)
target=root/'back_reach.png'
backup=raw/'back_reach_before_feedback_round2.png'
assert not backup.exists(), 'Backup already exists; choose a fresh version'
others={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.glob('*.png') if p.name!='back_reach.png'}
im=Image.open(source)
assert im.mode=='RGBA',im.mode
alpha=np.array(im.getchannel('A'))
assert alpha.min()==0 and alpha.max()==255
shutil.copy2(target,backup)
shutil.copy2(source,target)
for name,digest in others.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
def record(path):
    v=Image.open(path)
    a=np.array(v.getchannel('A'))
    return {'file':path.name,'size':list(v.size),'mode':v.mode,'bytes':path.stat().st_size,
            'alpha_range':[int(a.min()),int(a.max())],
            'transparent_percent':round(float((a==0).mean()*100),3),
            'alpha_bbox':v.getchannel('A').getbbox()}
entry=record(target)
meta_path=root/'_production'/'round2'/'back_reach_feedback_round2.json'
meta=json.loads(meta_path.read_text(encoding='utf-8'))
meta.update(status='complete',backup=str(backup.relative_to(root)),output=entry,other_final_pngs_verified_unchanged=len(others))
meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
manifest_path=root/'_production'/'round2'/'prompts.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
asset=next(a for a in manifest['assets'] if a['file']=='back_reach.png')
asset.setdefault('feedback_revisions',[]).append({'feedback':'feedback_round2.md','prompt':meta['prompt'],'inputs':meta['inputs'],'source':str(source),'backup':str(backup.relative_to(root))})
asset['current_source']=str(source)
asset['feedback_status']='Replaced after feedback_round2: bowed head, pressed closed-finger hand, tense posture'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report_path=qa/'validation.json'
report=json.loads(report_path.read_text(encoding='utf-8'))
idx=next(i for i,a in enumerate(report['assets']) if a['file']=='back_reach.png')
report['assets'][idx]=entry
report['feedback_round2']={'replaced':['back_reach.png'],'other_final_pngs_verified_unchanged':len(others),'visual_review':meta['review']}
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
tw,th,label=418,235,30
sheet=Image.new('RGB',(tw*4,(th+label)*6),'#25272b')
draw=ImageDraw.Draw(sheet)
for idx,asset in enumerate(manifest['assets']):
    name=asset['file']
    v=Image.open(root/name).convert('RGBA')
    bg=Image.new('RGBA',v.size,'#55575d' if v.getextrema()[3][0]==0 else '#EFE6D2')
    bg.alpha_composite(v)
    bg.thumbnail((tw,th),Image.Resampling.LANCZOS)
    x=(idx%4)*tw;y=(idx//4)*(th+label)
    sheet.paste(bg.convert('RGB'),(x,y))
    draw.text((x+8,y+th+5),name,font=font,fill='#eeeeee')
sheet.save(qa/'contact_sheet.jpg',quality=94)
comparison=Image.new('RGB',(1004,600),'#181b21')
draw=ImageDraw.Draw(comparison)
for idx,(path,title) in enumerate([(backup,'BEFORE'),(target,'AFTER: feedback_round2')]):
    v=Image.open(path).convert('RGBA')
    v.thumbnail((490,550),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(500,550),'#30353e')
    canvas.alpha_composite(v,((500-v.width)//2,(550-v.height)//2))
    comparison.paste(canvas.convert('RGB'),(idx*504,35))
    draw.text((idx*504+12,10),title,font=font,fill='#eeeeee')
comparison.save(qa/'back_reach_feedback_compare.jpg',quality=95)
readme=root/'README_round2.md'
with readme.open('a',encoding='utf-8') as f:
    f.write('\n\n## feedback_round2 修订\n\n仅重做并替换 back_reach.png：低头、收紧肩膀、右手五指并拢贴向前方隐形墙，背向镜头的机械手背不显示掌心核心，左拳下垂。已查看实际生成图及新旧对照。旧版备份在 _production/round2/raw/back_reach_before_feedback_round2.png；对照图在 _qa/round2/back_reach_feedback_compare.jpg。其他 36 张最终 PNG 的 SHA-256 校验一致。反馈注明由成片代码翻转的 listen_profile 和 reach_camera 保持原文件。完整提示词与修订来源见 _production/round2/back_reach_feedback_round2.json。\n')
print(json.dumps({'replaced':str(target),'backup':str(backup),'output':entry,'other_pngs_unchanged':len(others),'comparison':str(qa/'back_reach_feedback_compare.jpg')},ensure_ascii=False,indent=2))
