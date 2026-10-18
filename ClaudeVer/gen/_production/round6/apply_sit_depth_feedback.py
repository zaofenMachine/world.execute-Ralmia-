from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, json
import numpy as np
from alpha_utils import clean

R=Path(__file__).resolve().parents[2]
P=R/'_production'/'round6'; Q=R/'_qa'/'round6'; raw=P/'raw'
a=np.array(Image.open(R/'lishenna_sit.png').convert('RGBA'))
candidate=np.array(clean(Image.open(raw/'sit_b_depth_knee_repair_ai6.png')))
assert a.shape==candidate.shape==(941,1672,4)
mask=Image.open(Q/'sit_edit_mask_before_foot_direction.png').convert('L')
allowed=np.array(mask)>0
yy,xx=np.indices(allowed.shape)
# The old horizontal cutoff intersected the far kneecap when it changed from
# kicking to hanging. Include that dark stocking contour; retain skin/hands.
knee_region=(xx>=704)&(xx<=815)&(yy>=490)&(yy<554)
old_dark=(a[:,:,0]<135)&(a[:,:,1]<130)&(a[:,:,2]<130)&(a[:,:,3]>0)
new_dark=(candidate[:,:,0]<135)&(candidate[:,:,1]<130)&(candidate[:,:,2]<130)&(candidate[:,:,3]>0)
allowed |= knee_region & (old_dark|new_dark)
hand_mask=Image.new('L',(1672,941)); hd=ImageDraw.Draw(hand_mask)
hd.rectangle((620,516,681,554),fill=255)
hd.polygon([(679,516),(703,513),(718,526),(714,539),(704,548),
            (690,553),(678,557),(665,551),(673,539)],fill=255)
hd.rectangle((962,532,1050,567),fill=255)
hands=np.array(hand_mask)>0
allowed[hands]=False
mask=Image.fromarray(allowed.astype('uint8')*255)
weight=np.array(mask.filter(ImageFilter.GaussianBlur(1.2)),dtype=float)/255
weight[~allowed]=0
out=np.rint(a*(1-weight[:,:,None])+candidate*weight[:,:,None]).astype('uint8')
out[~allowed]=a[~allowed]
assert np.array_equal(out[:490],a[:490])
assert np.array_equal(out[~allowed],a[~allowed])
assert np.array_equal(out[hands],a[hands])
Image.fromarray(out).save(R/'lishenna_sit_b.png')
mask.save(Q/'sit_edit_mask.png')
mask.save(Q/'sit_foot_direction_edit_mask.png')

feedback={'basis':'User blue/red depth diagram plus subsequent lower-kick request',
    'foreground_leg':'Anatomical left leg from viewer-right knee, kicking down-left',
    'background_leg':'Anatomical right leg from viewer-left knee, hanging behind foreground calf',
    'outside_edit_pixels':int((~allowed).sum()),'outside_changed_pixels':0,
    'above_y490_exact':True,'knee_contour_included_from_y490':True,
    'hands_and_microphone_locked_pixels':int(hands.sum()),
    'hands_and_microphone_changed_pixels':0,
    'AI_source_size':[1672,941],
    'translation':[0,0],'rescaled':False,'upscaled':False,
    'A_sha256':hashlib.sha256((R/'lishenna_sit.png').read_bytes()).hexdigest()}
baseline=json.loads((P/'sit_foot_direction_baseline.json').read_text(encoding='utf-8'))
changed=[n for n,h in baseline.items() if hashlib.sha256((R/n).read_bytes()).hexdigest()!=h]
assert changed==['lishenna_sit_b.png'],changed
feedback.update(root_png_count=len(baseline),changed_root_png=changed,
                unchanged_root_png_count=len(baseline)-len(changed))
stats=json.loads((Q/'root_validation.json').read_text(encoding='utf-8'))
stats['sit']={'A':'lishenna_sit.png','B':'lishenna_sit_b.png',
    'outside_edit_pixels':int((~allowed).sum()),'outside_changed_pixels':0,
    'above_y490_exact':True,'foot_direction_feedback':feedback}
(Q/'root_validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
(Q/'sit_foot_direction_validation.json').write_text(json.dumps(feedback,ensure_ascii=False,indent=2),encoding='utf-8')

def display(pixels):
    im=Image.fromarray(pixels).convert('RGBA')
    bg=Image.new('RGBA',im.size,(48,52,62,255));bg.alpha_composite(im)
    return bg.convert('RGB')

frames=[display(x).resize((836,470),Image.Resampling.LANCZOS) for x in [a,out]]
joined=Image.new('RGB',(1672,470));joined.paste(frames[0],(0,0));joined.paste(frames[1],(836,0))
joined.save(Q/'sit_compare.jpg',quality=95)
pal=joined.quantize(colors=255);ff=[im.quantize(palette=pal) for im in frames]
ff[0].save(Q/'sit_switch.gif',save_all=True,append_images=ff[1:],duration=600,loop=0,optimize=False)
display(out).crop((470,470,1000,880)).save(Q/'sit_corrected_leg_detail.jpg',quality=96)
before=np.array(Image.open(raw/'sit_b_superseded_separate_legs.png').convert('RGBA'))
comparison=Image.new('RGB',(1220,430),(48,52,62))
for i,source in enumerate([before,out]):
    comparison.paste(display(source).crop((470,470,1080,900)),(610*i,0))
ImageDraw.Draw(comparison).text((8,8),'Previous',fill='white')
ImageDraw.Draw(comparison).text((618,8),'User depth diagram',fill='white')
comparison.save(Q/'sit_foot_direction_compare.jpg',quality=96)
record=json.loads((P/'sit_foot_direction_feedback.json').read_text(encoding='utf-8'))
record.update(status='complete',raw_output='raw/sit_b_depth_knee_repair_ai6.png',
    output='lishenna_sit_b.png',accepted_prompt_record='sit_foot_direction_attempt6.json',
    pose_prompt_record='sit_foot_direction_attempt5.json',
    user_diagram='raw/sit_leg_depth_user_diagram.png',
    postprocessing='Direct local edit of A. Restore all pixels outside the two lower-leg edit region. No detached-limb compositing, translation, or rescaling.',
    rejected_previous_results=['raw/sit_b_rejected_crossed_legs.png','raw/sit_b_superseded_separate_legs.png'],
    validation='_qa/round6/sit_foot_direction_validation.json')
(P/'sit_foot_direction_feedback.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
attempt=json.loads((P/'sit_foot_direction_attempt6.json').read_text(encoding='utf-8'))
attempt.update(status='accepted_local_edit',raw_output='raw/sit_b_depth_knee_repair_ai6.png')
(P/'sit_foot_direction_attempt6.json').write_text(json.dumps(attempt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(feedback,ensure_ascii=False))
