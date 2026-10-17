from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json, shutil
root=Path(r'F:\Project\world.execute-Ralmia-\ClaudeVer\gen')
raw=Path(r'C:\Users\zaofenMachine\.codex\generated_images\01a1408d-5dd4-7781-ab21-3edd8fac2f3c\exec-dbb2773e-3e19-4921-92d5-504ff90ab7a9.png')
a=Image.open(root/'lishenna_ref_sheet_v2.png').convert('RGB')
b=Image.open(raw).convert('RGB')
assert a.size==b.size
mask=Image.new('L',a.size,0)
d=ImageDraw.Draw(mask)
regions=[(118,337,293,482),(441,338,519,477),(1227,816,1324,918)]
for box in regions: d.rectangle(box,fill=255)
m=np.array(mask)
w=np.array(mask.filter(ImageFilter.GaussianBlur(2)),dtype=float)/255
w[m==0]=0
out=np.round(np.array(a)*(1-w[:,:,None])+np.array(b)*w[:,:,None]).astype('uint8')
target=root/'lishenna_ref_sheet_v3.png'
assert not target.exists(),str(target)
Image.fromarray(out).save(target)
prod=root/'_production'/'round4'
shutil.copy2(raw,prod/'L0_outfit_revision_ai.png')
shutil.copy2(Path(r'C:\Users\zaofenMachine\AppData\Local\Temp\codex-clipboard-17e36f50-36a7-42b1-8712-ac50e62cf64c.png'),root/'_references'/'lishenna_waist_detail_user.png')
qa={'asset':target.name,'size':a.size,'edit_regions':regions,'outside_changed_pixels':int(np.any(out!=np.array(a),axis=2)[m==0].sum()),'status':'awaiting_user_confirmation'}
(prod/'L0_outfit_validation.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(qa))
