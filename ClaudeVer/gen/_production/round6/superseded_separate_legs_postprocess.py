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
# Direct local edit in the original full-frame coordinates. No leg cutouts,
# translation, scaling, or swapping between knees.
candidate = np.array(clean(Image.open(raw / 'sit_b_foot_direction_ai3.png')))
assert candidate.shape == before.shape == a.shape

# Only the raised lower leg and shoe may change. Both legs remain separate.
mask = Image.new('L', (1672, 941))
d = ImageDraw.Draw(mask)
d.polygon([(780,552),(900,552),(970,625),(1080,640),
           (1080,815),(775,815),(775,620)],fill=255)
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
assert np.array_equal(out[:552], before[:552])
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
    'above_y552_exact_to_original_B':bool(np.array_equal(out[:552],before[:552])),
    'AI_source_size':list(Image.open(raw/'sit_b_foot_direction_ai3.png').size),
    'translation':[0,0], 'rescaled':False, 'upscaled':False,
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
record.update(status='complete',raw_output='raw/sit_b_foot_direction_ai3.png',
              output='lishenna_sit_b.png',validation='_qa/round6/sit_foot_direction_validation.json',
              accepted_prompt_record='sit_foot_direction_attempt3.json',
              postprocessing='Direct full-frame local edit of original B. Preserve AI leg placement; no leg cutout, translation or rescaling. Clean alpha edge colors and restore all pixels outside the calf/shoe edit mask from original B.',
              rejected_previous_result='raw/sit_b_rejected_crossed_legs.png')
(P/'sit_foot_direction_feedback.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
attempt=json.loads((P/'sit_foot_direction_attempt3.json').read_text(encoding='utf-8'))
attempt.update(status='accepted_local_edit',raw_output='raw/sit_b_foot_direction_ai3.png')
(P/'sit_foot_direction_attempt3.json').write_text(json.dumps(attempt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(feedback,ensure_ascii=False))
