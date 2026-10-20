from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,sys
R=Path(__file__).resolve().parents[2];P=R/'_production'/'round8';Q=R/'_qa'/'round8'
sys.path.insert(0,str(R/'_production'/'round6'))
from alpha_utils import clean
source=P/'raw'/'peek_frozen_detail_ai.png'
im=clean(Image.open(source)); arr=np.array(im)
ys,xs=np.where(arr[:,:,3]>32)
box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
scale=min(1.,800/(box[3]-box[1]))
crop=im.crop(box);size=(round(crop.width*scale),round(crop.height*scale))
if crop.size!=size:crop=crop.resize(size,Image.Resampling.LANCZOS)
pos=((1672-size[0])//2,(941-size[1])//2)
final=Image.new('RGBA',(1672,941));final.alpha_composite(crop,pos)
edge_source=P/'raw'/'peek_left_edge_ai.png'
if edge_source.exists():
    # The AI completed the truncated left boundary in native canvas coordinates.
    # Retain the intended chest-up bottom and remove generation spill below it.
    final=clean(Image.open(edge_source))
    edge_arr=np.array(final);edge_arr[870:]=0
    final=Image.fromarray(edge_arr)
final.save(R/'peek_frozen.png')
out=np.array(final);ys,xs=np.where(out[:,:,3]>32)
def point(x,y):return (round((x-box[0])*scale+pos[0]),round((y-box[1])*scale+pos[1]))
# Separate connected components provide a numerical check that the two bodies
# are not touching. The individual speaker discs can remain separate too.
binary=Image.fromarray((out[:,:,3]>128).astype('uint8')*255)
ralmia_seed=point(780,430);lishenna_seed=point(1130,445)
assert binary.getpixel(ralmia_seed)==255
assert binary.getpixel(lishenna_seed)==255
ImageDraw.floodfill(binary,ralmia_seed,128)
separate=binary.getpixel(lishenna_seed)==255
assert separate,'Character silhouettes merged'
stats={'filename':'peek_frozen.png','canvas':[1672,941],'mode':'RGBA',
 'source':str(source),'source_bbox':list(box),'scale':scale,'upscaled':False,'placement':list(pos),
 'native_edge_completion_source':str(edge_source) if edge_source.exists() else None,
 'final_bottom_crop_y':870 if edge_source.exists() else None,
 'final_bbox_alpha_gt32':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],
 'height_fraction':round((ys.max()-ys.min()+1)/941,6),
 'alpha_min':int(out[:,:,3].min()),'alpha_max':int(out[:,:,3].max()),
 'separate_character_components_alpha_gt128':separate,
 'component_check_seeds':{'ralmia':list(ralmia_seed),'lishenna':list(lishenna_seed)},
 'visual_check':'Ralmia at left faces right with visible right-temple gem, fixed gaze, hair and red bow streaming left; Lishenna at right leans forward, arms behind, hair down. Visible face and lower arm-to-hair gaps. No contact/effects.'}
(Q/'peek_validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
for name,color in [('dark',(48,52,62,255)),('light',(238,235,226,255))]:
    bg=Image.new('RGBA',final.size,color);bg.alpha_composite(final)
    bg.convert('RGB').save(Q/('peek_preview_'+name+'.jpg'),quality=95)
record=json.loads((P/'peek_detail_edit_prompt.json').read_text(encoding='utf-8'))
record.update(status='complete',raw_output='raw/peek_frozen_detail_ai.png',output='peek_frozen.png')
(P/'peek_detail_edit_prompt.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
if edge_source.exists():
    edge_record=json.loads((P/'peek_left_edge_prompt.json').read_text(encoding='utf-8'))
    edge_record.update(status='complete',raw_output='raw/peek_left_edge_ai.png',output='peek_frozen.png',
        postprocessing='Native canvas output; alpha cleanup and retain intended chest-up bottom crop at y=870. Visual invariants rechecked; no pairwise pixel-lock claim.')
    (P/'peek_left_edge_prompt.json').write_text(json.dumps(edge_record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False))
