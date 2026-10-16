"""Lock AI local edits to their A frames. Authorized by user on 2026-10-16.

Artwork within changed regions comes from image_gen edits, never drawn by this script.
"""
from pathlib import Path
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / '_production' / 'raw'
QA = ROOT / '_qa'
RAW.mkdir(parents=True, exist_ok=True)
QA.mkdir(exist_ok=True)

def rgb(name):
    return np.array(Image.open(ROOT / name).convert('RGB'))

def retain_raw(name):
    target = RAW / (Path(name).stem + '_ai.png')
    if not target.exists():
        shutil.copy2(ROOT / name, target)
    return np.array(Image.open(target).convert('RGB'))

def feather_inside(mask, radius=5):
    # A finite region of support guarantees zero modifications outside it.
    blurred = np.array(Image.fromarray(mask).filter(ImageFilter.GaussianBlur(radius)), dtype=float) / 255
    return blurred * (mask > 0)

def lock(a_name, b_name, kind):
    a, b = rgb(a_name), retain_raw(b_name)
    assert a.shape == b.shape, (a_name, b_name, a.shape, b.shape)
    h, w = a.shape[:2]
    if kind == 'eyes':
        mask_image = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask_image)
        # Native 1672x941 coordinates. Eyebrows, nose, fringe and cheeks stay in A.
        for poly in [
            [(195,265),(675,265),(705,545),(653,613),(350,630),(205,567)],
            [(1000,265),(1517,265),(1525,526),(1445,615),(1110,630),(1005,558)],
        ]:
            draw.polygon([(round(x*w/1672),round(y*h/941)) for x,y in poly], fill=255)
        mask = np.array(mask_image)
        # Preserve crossing blonde strands and their nearby ink contours exactly.
        aa = a.astype(int)
        hair = ((aa[:,:,0]-aa[:,:,2] > 95) & (aa[:,:,1]-aa[:,:,2] > 55) & (aa[:,:,1] > 105) & (aa[:,:,2] < 145))
        weight = feather_inside(mask, 6)
        mask[hair] = 0
        weight[hair] = 0
    else:
        # Only the union of the old and new red thread, plus a 3px antialias margin.
        def red(im):
            v = im.astype(int)
            return (v[:,:,0] > 105) & (v[:,:,0]-v[:,:,1] > 42) & (v[:,:,0]-v[:,:,2] > 38)
        union = red(a) | red(b)
        region = np.zeros((h,w),bool)
        region[:round(h*.33),round(w*.60):] = True
        union &= region
        mask = np.array(Image.fromarray((union*255).astype('uint8')).filter(ImageFilter.MaxFilter(9)))
        weight = feather_inside(mask, 1)
        weight[union] = 1
    out = np.rint(a*(1-weight[:,:,None])+b*weight[:,:,None]).clip(0,255).astype('uint8')
    Image.fromarray(out).save(ROOT / b_name)
    Image.fromarray(mask).save(QA / (kind+'_edit_mask.png'))
    changed = np.any(a != out, axis=2)
    outside = mask == 0
    assert not changed[outside].any(), 'Pixels outside authorized edit region changed'
    ys,xs = np.where(changed)
    info = {'a':a_name,'b':b_name,'method':'image_gen local edit followed by authorized original-pixel restoration',
            'canvas':[w,h], 'outside_mask_pixels':int(outside.sum()), 'outside_mask_changed_pixels':int(changed[outside].sum()),
            'outside_mask_exact_match_percent':100.0,'changed_pixels':int(changed.sum()),
            'changed_bbox':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]}
    # A/B diagnostic animation, not a production asset.
    frames=[Image.fromarray(v).resize((836,470),Image.Resampling.LANCZOS) for v in (a,out)]
    frames[0].save(QA/(kind+'_blink.gif'),save_all=True,append_images=frames[1:],duration=650,loop=0)
    return info

pair_results=[lock('eye_open.png','eye_closed.png','eyes'),lock('hand_gap.png','hand_tied.png','thread')]

names=['ref_sheet.png','hand_palm.png','parts_exploded.png','eye_open.png','eye_closed.png',
       'world_L1_sky.png','world_L2_city.png','world_L3_mid.png','world_L4_fore.png',
       'dash_launch.png','dash_full.png','hand_gap.png','hand_tied.png','portrait_front.png','floating.png','pinky_promise.png']
assets=[]
for name in names:
    im=Image.open(ROOT/name)
    row={'file':name,'size':list(im.size),'mode':im.mode,'bytes':(ROOT/name).stat().st_size}
    if im.mode=='RGBA':
        alpha=np.asarray(im.getchannel('A'))
        row.update(alpha_range=[int(alpha.min()),int(alpha.max())],transparent_percent=round(float((alpha==0).mean()*100),3),
                   opaque_percent=round(float((alpha==255).mean()*100),3),alpha_bbox=im.getchannel('A').getbbox())
    assets.append(row)

world_names=names[5:9]
world_sizes=[Image.open(ROOT/name).size for name in world_names]
assert len(set(world_sizes)) == 1, world_sizes
world=Image.open(ROOT/world_names[0]).convert('RGBA')
for name in world_names[1:]:
    world=Image.alpha_composite(world,Image.open(ROOT/name).convert('RGBA'))
world.convert('RGB').save(QA/'world_composite.jpg',quality=94)

# Review-only contact sheet; final source PNGs are not rescaled or repainted.
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
thumb_w,thumb_h=418,235
sheet=Image.new('RGB',(thumb_w*4,(thumb_h+32)*4),'#25272b')
d=ImageDraw.Draw(sheet)
for index,name in enumerate(names):
    im=Image.open(ROOT/name).convert('RGBA')
    bg=Image.new('RGBA',im.size,'#EFE6D2')
    if im.getextrema()[-1][0] == 0:
        bg=Image.new('RGBA',im.size,'#55575d')
    bg.alpha_composite(im)
    bg.thumbnail((thumb_w,thumb_h),Image.Resampling.LANCZOS)
    x=(index%4)*thumb_w; y=(index//4)*(thumb_h+32)
    sheet.paste(bg.convert('RGB'),(x,y))
    d.text((x+8,y+thumb_h+5),name,font=font,fill='#eeeeee')
sheet.save(QA/'contact_sheet.jpg',quality=93)
report={'asset_count':len(assets),'assets':assets,'paired_edits':pair_results,'world_layer_sizes_match':True,
        'native_resolution_note':'Built-in generator returned approximately 1672x941, not requested 2560x1440. Native files retained without artificial upscaling.'}
(QA/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'count':len(assets),'pairs':pair_results,'world_sizes':world_sizes},ensure_ascii=False,indent=2))
