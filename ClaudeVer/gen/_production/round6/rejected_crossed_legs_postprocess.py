from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib, json
import numpy as np
from alpha_utils import clean

R = Path(__file__).resolve().parents[2]
P = R / '_production' / 'round6'
Q = R / '_qa' / 'round6'
raw = P / 'raw'
before = np.array(Image.open(raw / 'lishenna_sit_b_before_foot_direction.png').convert('RGBA'))
a = np.array(Image.open(R / 'lishenna_sit.png').convert('RGBA'))
# Keep only the AI-drawn leftward lower leg. Register it to the far knee;
# the tool also altered the other leg, which is deliberately discarded.
crop = Image.open(raw / 'sit_b_leg_foot_direction_ai2.png').convert('RGBA')
assert crop.width >= 610 and crop.height >= 380
crop = crop.resize((610,380),Image.Resampling.LANCZOS)
leg_mask=Image.new('L',crop.size)
ImageDraw.Draw(leg_mask).polygon([(270,0),(336,0),(334,22),(308,58),
    (296,76),(266,99),(226,126),(231,162),(228,233),(150,237),
    (70,200),(65,145),(160,113),(213,77)],fill=255)
ca=np.array(crop);ca[:,:,3][np.array(leg_mask)==0]=0
layer=Image.new('RGBA',(1672,941))
layer.alpha_composite(Image.fromarray(ca),(560,505))
candidate = np.array(clean(layer))
assert candidate.shape == before.shape == a.shape

# Only the raised lower leg and shoe may change. Preserve the hanging leg
# even where the revised swinging leg passes behind it.
mask = Image.new('L', (1672, 941))
d = ImageDraw.Draw(mask)
d.rectangle((630,523,1080,812),fill=255)
hang = Image.new('L', mask.size)
ImageDraw.Draw(hang).polygon([(700,480),(805,480),(819,506),(813,526),
                             (786,552),(779,580),(776,630),(766,713),
                             (773,779),(770,878),(645,878),(645,756),
                             (682,712),(682,607)], fill=255)
hang_pixels = (np.array(hang)>0) & (before[:,:,3]>0)
allowed = np.array(mask)>0
allowed[hang_pixels] = False
yy,xx=np.indices(allowed.shape)
# The crop contains skin, pink hair and the supporting hand next to the
# black knee. Retain those source pixels rather than clearing them.
colored=(before[:,:,0]>120)&(before[:,:,3]>0)&(yy<630)
allowed[colored]=False
allowed[(xx<715)&(yy<562)]=False
mask = Image.fromarray(allowed.astype('uint8')*255)
weight = np.array(mask.filter(ImageFilter.GaussianBlur(1.2)), dtype=float)/255
weight[~allowed] = 0
out = np.rint(before*(1-weight[:,:,None])+candidate*weight[:,:,None]).astype('uint8')
out[~allowed] = before[~allowed]
assert np.array_equal(out[hang_pixels], before[hang_pixels])
assert np.array_equal(out[:523], before[:523])
Image.fromarray(out).save(R / 'lishenna_sit_b.png')
mask.save(Q / 'sit_foot_direction_edit_mask.png')

original_pair = np.array(Image.open(Q / 'sit_edit_mask_before_foot_direction.png').convert('L'))>0
pair_allowed = original_pair | allowed
Image.fromarray(pair_allowed.astype('uint8')*255).save(Q / 'sit_edit_mask.png')
assert np.array_equal(out[~pair_allowed], a[~pair_allowed])
stats = json.loads((Q / 'root_validation.json').read_text(encoding='utf-8'))
stats['sit'] = {'A':'lishenna_sit.png', 'B':'lishenna_sit_b.png',
    'outside_edit_pixels':int((~pair_allowed).sum()),
    'outside_changed_pixels':int(np.any(out!=a,axis=2)[~pair_allowed].sum()),
    'above_y522_exact':bool(np.array_equal(out[:522],a[:522]))}
feedback = {'outside_correction_pixels':int((~allowed).sum()),
    'outside_correction_changed_pixels':int(np.any(out!=before,axis=2)[~allowed].sum()),
    'hanging_leg_locked_pixels':int(hang_pixels.sum()),
    'hanging_leg_changed_pixels':int(np.any(out!=before,axis=2)[hang_pixels].sum()),
    'above_y523_exact_to_previous_B':bool(np.array_equal(out[:523],before[:523])),
    'AI_crop_source_size':list(Image.open(raw/'sit_b_leg_foot_direction_ai2.png').size),
    'crop_registered_size':[610,380], 'crop_origin':[470,505],
    'AI_leg_translation':[90,0], 'upscaled':False,
    'A_sha256':hashlib.sha256((R/'lishenna_sit.png').read_bytes()).hexdigest()}
stats['sit']['foot_direction_feedback'] = feedback
(Q/'root_validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
(Q/'sit_foot_direction_validation.json').write_text(json.dumps(feedback,ensure_ascii=False,indent=2),encoding='utf-8')

def display(image):
    im=Image.fromarray(image).convert('RGBA')
    bg=Image.new('RGBA', im.size, (48,52,62,255));bg.alpha_composite(im)
    return bg.convert('RGB')

frames=[display(a).resize((836,470),Image.Resampling.LANCZOS),
        display(out).resize((836,470),Image.Resampling.LANCZOS)]
joined=Image.new('RGB',(1672,470));joined.paste(frames[0],(0,0));joined.paste(frames[1],(836,0))
joined.save(Q/'sit_compare.jpg',quality=95)
pal=joined.quantize(colors=255)
ff=[im.quantize(palette=pal) for im in frames]
ff[0].save(Q/'sit_switch.gif',save_all=True,append_images=ff[1:],duration=600,loop=0,optimize=False)
comparison=Image.new('RGB',(1220,430),(48,52,62))
for i,source in enumerate([before,out]):
    comparison.paste(display(source).crop((470,470,1080,900)),(610*i,0))
ImageDraw.Draw(comparison).text((8,8),'Before',fill='white')
ImageDraw.Draw(comparison).text((618,8),'After',fill='white')
comparison.save(Q/'sit_foot_direction_compare.jpg',quality=96)
record=json.loads((P/'sit_foot_direction_feedback.json').read_text(encoding='utf-8'))
record.update(status='complete',raw_output='raw/sit_b_leg_foot_direction_ai2.png',
              output='lishenna_sit_b.png',validation='_qa/round6/sit_foot_direction_validation.json',
              accepted_prompt_record='sit_foot_direction_attempt2.json',
              postprocessing='Retain the AI-drawn leftward calf/shoe only, downscale the crop and translate it to the original far knee. Restore the original hanging leg and everything outside the correction mask pixel for pixel.')
(P/'sit_foot_direction_feedback.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
attempt=json.loads((P/'sit_foot_direction_attempt2.json').read_text(encoding='utf-8'))
attempt.update(status='accepted_partial_leg_only',raw_output='raw/sit_b_leg_foot_direction_ai2.png',
               discarded_changes='Tool also moved the hanging leg; that portion was not used.')
(P/'sit_foot_direction_attempt2.json').write_text(json.dumps(attempt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(feedback,ensure_ascii=False))
