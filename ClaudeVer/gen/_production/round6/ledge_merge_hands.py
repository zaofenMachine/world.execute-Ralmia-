from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
R=Path(r"F:\Project\world.execute-Ralmia-\ClaudeVer\gen")
A=Image.open(R/"_production/round6/raw/ledge_a_framing.png").convert("RGB")
detail=Image.open(R/"_production/round6/raw/ledge_a_hands_detail.png").convert("RGB").resize((160,100),Image.Resampling.LANCZOS)
patch=A.copy(); patch.paste(detail,(740,570))
yy,xx=np.indices((A.height,A.width))
dist=np.minimum.reduce((xx-740,900-xx,yy-570,670-yy))
t=np.clip(dist/24,0,1); weight=t*t*(3-2*t)
mask=(weight*255).astype(np.uint8)
m=Image.fromarray((mask>0).astype(np.uint8)*255)
out=Image.composite(patch,A,Image.fromarray(mask));out.save(R/"ledge_together.png")
m.save(R/"_qa/round6/ledge_pinky_edit_mask.png")
out.crop((775,590,890,670)).resize((690,480)).save(R/"_qa/round6/ledge_hands_final.png")
