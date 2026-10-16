"""Round 2 delivery QA and authorized pixel locking of AI pair edits.

All new art comes from image_gen. Scripts only restore invariant pixels/alpha,
and create review previews; original first-batch source PNGs are never modified.
"""
from pathlib import Path
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/'_production'/'round2'/'raw'
QA=ROOT/'_qa'/'round2'
RAW.mkdir(parents=True,exist_ok=True)
QA.mkdir(parents=True,exist_ok=True)
NAMES=['creator_sheet.png','lab_desk.png','lab_desk_empty.png','pinky_alone.png','offer_pose.png',
       'spec_eggplant.png','spec_tomato.png','spec_tabbycat.png','creation_inverse.png',
       'world_L1_night.png','world_L2_city_night.png','eye_tear.png','sitting_alone.png',
       'back_reach.png','reach_camera.png','creator_walk.png','listen_profile.png',
       'run_front.png','blackboard.png','escape_leap.png','portrait_front_v2.png']

def raw_image(name):
    target=RAW/(Path(name).stem+'_ai.png')
    if not target.exists():
        shutil.copy2(ROOT/name,target)
    return Image.open(target)

def region_mask(size,polygons):
    im=Image.new('L',size,0)
    draw=ImageDraw.Draw(im)
    w,h=size
    for poly in polygons:
        draw.polygon([(round(x*w/1672),round(y*h/941)) for x,y in poly],fill=255)
    return np.array(im)

def lock_local(a_name,b_name,polygons,kind):
    a=np.array(Image.open(ROOT/a_name).convert('RGB'))
    b=np.array(raw_image(b_name).convert('RGB'))
    assert a.shape==b.shape,(a_name,b_name,a.shape,b.shape)
    h,w=a.shape[:2]
    mask=region_mask((w,h),polygons)
    weight=np.array(Image.fromarray(mask).filter(ImageFilter.GaussianBlur(4)),dtype=float)/255
    weight*=mask>0
    if kind=='pinky':
        # Preserve the intersecting mechanical black-finger pixels from A too.
        aa=a.astype(int); bb=b.astype(int)
        protect=(aa.max(axis=2)<180)&(bb.max(axis=2)<180)
        yy,xx=np.indices((h,w))
        protect&=(xx<842)&(yy<560)&(xx<832)
        # Thread pixels are the only red pixels permitted to change there.
        red=(aa[:,:,0]-aa[:,:,1]>40)|(bb[:,:,0]-bb[:,:,1]>40)
        protect&=~red
        weight[protect]=0
        mask[protect]=0
    out=np.rint(a*(1-weight[:,:,None])+b*weight[:,:,None]).clip(0,255).astype('uint8')
    Image.fromarray(out).save(ROOT/b_name)
    Image.fromarray(mask).save(QA/(kind+'_edit_mask.png'))
    changed=np.any(a!=out,axis=2)
    outside=mask==0
    assert not changed[outside].any()
    yy,xx=np.where(changed)
    record={'base':a_name,'edit':b_name,'generation':'image_gen local edit',
            'postprocess':'user-authorized original pixel restoration outside edit mask',
            'size':[w,h],'outside_mask_pixels':int(outside.sum()),'outside_mask_changed_pixels':0,
            'outside_mask_exact_match_percent':100.0,'changed_pixels':int(changed.sum()),
            'changed_bbox':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]}
    frames=[Image.fromarray(im).resize((836,470),Image.Resampling.LANCZOS) for im in (a,out)]
    frames[0].save(QA/(kind+'_blink.gif'),save_all=True,append_images=frames[1:],duration=800,loop=0)
    return record

pairs=[]
pairs.append(lock_local('lab_desk.png','lab_desk_empty.png',[
    [(690,20),(962,20),(968,188),(1036,235),(1083,308),(1110,328),(1110,482),
     (1105,772),(1080,838),(1080,929),(576,929),(576,788),(560,740),(571,550),
     (530,478),(530,322),(607,292),(640,214),(706,182)]
],'lab'))
pairs.append(lock_local('pinky_promise.png','pinky_alone.png',[
    [(746,232),(1671,232),(1671,811),(745,811),(745,520),(757,472),(747,407)]
],'pinky'))
pairs.append(lock_local('eye_open.png','eye_tear.png',[
    [(1207,540),(1305,535),(1327,554),(1316,591),(1302,612),(1310,758),
     (1302,790),(1247,790),(1242,737),(1260,607),(1240,592),(1207,583)]
],'tear'))

# Retain A's actual architectural alpha geometry outside the removed sun.
day=Image.open(ROOT/'world_L2_city.png').convert('RGBA')
night=raw_image('world_L2_city_night.png').convert('RGBA')
assert day.size==night.size
a=np.array(day); b=np.array(night)
h,w=a.shape[:2]
yy,xx=np.indices((h,w))
v=a.astype(int)
sun_box=(xx>1000)&(xx<1215)&(yy>437)&(yy<595)
sun_colour=(v[:,:,0]-v[:,:,2]>50)&(v[:,:,1]-v[:,:,2]>30)
sun=sun_box&sun_colour&(a[:,:,3]>2)&(b[:,:,3]<100)
alpha=a[:,:,3].copy()
alpha[sun]=0
waterline=594
alpha[waterline:]=255
b[:,:,3]=alpha
Image.fromarray(b).save(ROOT/'world_L2_city_night.png')
Image.fromarray((sun*255).astype('uint8')).save(QA/'city_removed_sun_mask.png')
above=(yy<waterline)&~sun
assert np.array_equal(alpha[above],a[:,:,3][above])
assert alpha[waterline:].min()==255
night_geometry={'base':'world_L2_city.png','edit':'world_L2_city_night.png',
                'method':'image_gen lighting edit; restored original architectural alpha outside removed sun',
                'removed_sun_pixels':int(sun.sum()),'above_water_outside_sun_alpha_changed_pixels':0,
                'opaque_water_below_y':waterline,'water_alpha_min':255,'canvas':list(day.size)}

sky_day=Image.open(ROOT/'world_L1_sky.png')
sky_night=Image.open(ROOT/'world_L1_night.png')
assert sky_day.size==sky_night.size==day.size
sky_pair={'base':'world_L1_sky.png','edit':'world_L1_night.png','method':'image_gen full-canvas lighting edit, original as edit target',
          'same_canvas':True,'note':'All colours change for night; cloud geometry checked visually, not claimed pixel-identical.'}

assets=[]
for name in NAMES:
    im=Image.open(ROOT/name)
    row={'file':name,'size':list(im.size),'mode':im.mode,'bytes':(ROOT/name).stat().st_size}
    if im.mode=='RGBA':
        alpha=np.array(im.getchannel('A'))
        assert alpha.min()==0 and alpha.max()==255,name
        row.update(alpha_range=[int(alpha.min()),int(alpha.max())],
                   transparent_percent=round(float((alpha==0).mean()*100),3),alpha_bbox=im.getchannel('A').getbbox())
    assets.append(row)

# Review images use slate grey behind transparent assets, never a fake checkerboard.
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
tw,th,label=418,235,30
sheet=Image.new('RGB',(tw*4,(th+label)*6),'#25272b')
draw=ImageDraw.Draw(sheet)
for idx,name in enumerate(NAMES):
    im=Image.open(ROOT/name).convert('RGBA')
    bg=Image.new('RGBA',im.size,'#55575d' if im.getextrema()[3][0]==0 else '#EFE6D2')
    bg.alpha_composite(im)
    bg.thumbnail((tw,th),Image.Resampling.LANCZOS)
    x=(idx%4)*tw; y=(idx//4)*(th+label)
    sheet.paste(bg.convert('RGB'),(x,y))
    draw.text((x+8,y+th+5),name,font=font,fill='#eeeeee')
sheet.save(QA/'contact_sheet.jpg',quality=94)
night_scene=sky_night.convert('RGBA')
night_scene.alpha_composite(Image.open(ROOT/'world_L2_city_night.png').convert('RGBA'))
night_scene.convert('RGB').save(QA/'night_L1_L2_composite.jpg',quality=95)
for name in ['world_L3_mid.png','world_L4_fore.png']:
    night_scene.alpha_composite(Image.open(ROOT/name).convert('RGBA'))
night_scene.convert('RGB').save(QA/'night_with_existing_foreground.jpg',quality=94)

report={'expected_count':21,'delivered_count':len(assets),'assets':assets,'local_pairs':pairs,
        'night_city_geometry':night_geometry,'night_sky_pair':sky_pair,
        'native_resolution_note':'Approximately 1672x941; exact native dimensions listed per asset, with occasional 1px differences. Not 2560x1440; no artificial upscaling.',
        'scope':'Images only; no MV code or timing/audio edits.'}
(QA/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'count':len(assets),'rgba_count':sum(x['mode']=='RGBA' for x in assets),
                  'local_pairs':pairs,'night_city':night_geometry},ensure_ascii=False,indent=2))
