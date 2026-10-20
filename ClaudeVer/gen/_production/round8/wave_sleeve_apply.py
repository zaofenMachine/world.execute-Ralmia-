from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];P=R/"_production"/"round8";Q=R/"_qa"/"round8"
A=Image.open(P/"raw"/"wave_before_sleeve_fix.png").convert("RGBA")
B=Image.open(P/"raw"/"wave_sleeve_fix_ai.png").convert("RGBA")
assert A.size==B.size==(1672,941)
m=Image.new("L",A.size);ImageDraw.Draw(m).polygon([(663,356),(684,353),(698,360),(704,375),(695,390),(681,402),(659,402),(655,382)],fill=255)
soft=m.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(1.5))
weight=np.array(soft);weight[:353,:]=0
mask=weight>0
a=np.array(A);b=np.array(B)
out=(b.astype(float)*(weight[:,:,None]/255)+a.astype(float)*(1-weight[:,:,None]/255)).round().astype("uint8")
out[:,:,3]=a[:,:,3]
out[~mask]=a[~mask]
final=Image.fromarray(out);final.save(R/"lishenna_wave_back.png")
Image.fromarray(mask.astype("uint8")*255).save(Q/"wave_sleeve_edit_mask.png")
Image.fromarray(weight).save(Q/"wave_sleeve_edit_blend.png")
changed=np.any(out!=a,axis=2)
aa=out[:,:,3];fy,fx=np.where(aa>32);box=[int(fx.min()),int(fy.min()),int(fx.max()+1),int(fy.max()+1)]
report=json.loads((Q/"wave_validation.json").read_text(encoding="utf-8"))
report["sha256"]=hashlib.sha256((R/"lishenna_wave_back.png").read_bytes()).hexdigest()
report["sleeve_correction"]={"mask":"_qa/round8/wave_sleeve_edit_mask.png","outside_edit_pixels":int((~mask).sum()),"outside_changed_pixels":int(changed[~mask].sum()),"changed_pixels":int(changed.sum()),"alpha_changed_pixels":int((out[:,:,3]!=a[:,:,3]).sum()),"canvas_position_and_bbox_unchanged":box==report["visible_bbox_alpha_gt_32"],"actual_shoulder_patch_roi":[675,318,725,353],"shoulder_patch_changed_pixels":int(changed[318:353,675:725].sum()),"back_strip_roi":[784,349,811,426],"back_strip_changed_pixels":int(changed[349:426,784:811].sum()),"notes":"Removed invented cyan bow only; no resize, shift or registration applied."}
roi=out[354:402,658:705,:3]
report["sleeve_correction"]["cyan_pixels_remaining_in_bow_roi"]=int(((roi[:,:,0]<130)&(roi[:,:,1]>130)&(roi[:,:,2]>130)).sum())
assert report["sleeve_correction"]["outside_changed_pixels"]==0
assert report["sleeve_correction"]["alpha_changed_pixels"]==0
assert report["sleeve_correction"]["shoulder_patch_changed_pixels"]==0
assert report["sleeve_correction"]["back_strip_changed_pixels"]==0
assert report["sleeve_correction"]["canvas_position_and_bbox_unchanged"]
(Q/"wave_validation.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
for name,color in [("slate",(39,49,64,255)),("cream",(235,229,214,255))]:
    bg=Image.new("RGBA",final.size,color);bg.alpha_composite(final);bg.convert("RGB").save(Q/f"wave_preview_{name}.jpg",quality=95)
sheet=Image.new("RGB",(720,460),(39,49,64))
for im,x in [(A,0),(final,360)]:
    part=im.crop((640,310,730,425)).resize((360,460),Image.Resampling.NEAREST)
    bg=Image.new("RGBA",part.size,(39,49,64,255));bg.alpha_composite(part);sheet.paste(bg.convert("RGB"),(x,0))
sheet.save(Q/"wave_sleeve_before_after.png")
print(json.dumps(report["sleeve_correction"],ensure_ascii=False))
