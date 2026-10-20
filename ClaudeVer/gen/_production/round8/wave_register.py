from pathlib import Path
import importlib.util,json,hashlib
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[2]
P=R/"_production"/"round8";Q=R/"_qa"/"round8";Q.mkdir(exist_ok=True,parents=True)
spec=importlib.util.spec_from_file_location("round6_alpha_utils",R/"_production"/"round6"/"alpha_utils.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
raw=Image.open(P/"raw"/"lishenna_wave_back_ai.png").convert("RGBA")
im=mod.clean(raw)
a=np.array(im);ys,xs=np.where(a[:,:,3]>32)
box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
crop=im.crop(box);target_h=round(941*.85);scale=min(1.0,target_h/crop.height)
size=(round(crop.width*scale),round(crop.height*scale))
crop=crop.resize(size,Image.Resampling.LANCZOS) if size!=crop.size else crop
bottom=round(941*.92)
pos=((1672-size[0])//2,bottom-size[1])
out=Image.new("RGBA",(1672,941));out.alpha_composite(crop,pos);out=mod.clean(out)
out.save(R/"lishenna_wave_back.png")
arr=np.array(out);aa=arr[:,:,3];fy,fx=np.where(aa>32)
final_box=[int(fx.min()),int(fy.min()),int(fx.max()+1),int(fy.max()+1)]
report={
"file":"lishenna_wave_back.png","raw_size":list(raw.size),"final_size":list(out.size),"mode":out.mode,
"alpha_range":[int(aa.min()),int(aa.max())],"transparent_pixels":int((aa==0).sum()),"nonzero_alpha_pixels":int((aa>0).sum()),
"visible_bbox_alpha_gt_32":final_box,"visible_height_fraction":(final_box[3]-final_box[1])/941,
"visible_foot_bottom_fraction":final_box[3]/941,"source_bbox":list(box),"scale":scale,"translation":list(pos),
"no_enlargement":scale<=1.0,"sha256":hashlib.sha256((R/"lishenna_wave_back.png").read_bytes()).hexdigest(),
"visual_checks":{"left_shoulder":"Back visible; head turns over anatomical LEFT shoulder on image LEFT; face left of back hair.","wave":"Image-left free hand raised to shoulder height, open-palm casual wave.","microphone":"Image-right other hand holds microphone down beside body.","speaker_discs":2,"outfit":"White puffy jacket, pure black shorts, black thigh-highs, white sneakers with purple laces; checkered band and black loops.","background":"Transparent; no floor, shadow, text or effects."}}
(Q/"wave_validation.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
for name,color in [("slate",(39,49,64,255)),("cream",(235,229,214,255))]:
    bg=Image.new("RGBA",out.size,color);bg.alpha_composite(out);bg.convert("RGB").save(Q/f"wave_preview_{name}.jpg",quality=95)
print(json.dumps(report,ensure_ascii=False))
