from pathlib import Path
import json
import math
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def components(mask):
    parent=[]
    runs=[]
    previous=[]
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i
    for y,row in enumerate(mask):
        padded=np.pad(row.astype('int8'),(1,1))
        starts=np.where(np.diff(padded)==1)[0]
        ends=np.where(np.diff(padded)==-1)[0]
        current=[]
        for start,end in zip(starts,ends):
            tag=len(parent); parent.append(tag)
            for ps,pe,pt in previous:
                if start<=pe and end>=ps:
                    parent[find(tag)]=find(pt)
            current.append((int(start),int(end),tag))
            runs.append((y,int(start),int(end),tag))
        previous=current
    groups={}
    for y,start,end,tag in runs:
        groups.setdefault(find(tag),[]).append((y,start,end))
    result=[]
    for group in groups.values():
        area=sum(end-start for y,start,end in group)
        if area>200:
            bbox=[min(s for y,s,e in group),min(y for y,s,e in group),max(e for y,s,e in group),max(y for y,s,e in group)+1]
            result.append({'area':area,'bbox':bbox,'runs':group})
    return sorted(result,key=lambda g:(g['bbox'][1]//200,g['bbox'][0]))

im=Image.open(ROOT/'parts_exploded.png')
mask=np.array(im.getchannel('A'))>128
parts=components(mask)
boundaries=[]
for part in parts:
    x0,y0,x1,y1=part['bbox']
    local=np.zeros((y1-y0,x1-x0),bool)
    for y,start,end in part['runs']:
        local[y-y0,start-x0:end-x0]=True
    p=np.pad(local,1)
    interior=p[1:-1,1:-1] & p[:-2,1:-1] & p[2:,1:-1] & p[1:-1,:-2] & p[1:-1,2:]
    yy,xx=np.where(local & ~interior)
    boundaries.append(np.column_stack((xx+x0,yy+y0)).astype('int32'))
min_gap=math.inf
for i,a in enumerate(boundaries):
    for j,b in enumerate(boundaries[:i]):
        ab=parts[i]['bbox']; bb=parts[j]['bbox']
        bound=math.hypot(max(0,ab[0]-bb[2],bb[0]-ab[2]),max(0,ab[1]-bb[3],bb[1]-ab[3]))
        if bound>=min_gap:
            continue
        for block in np.array_split(a,max(1,len(a)//256)):
            dist=((block[:,None,:]-b[None,:,:]).astype('float32')**2).sum(axis=2)
            min_gap=min(min_gap,math.sqrt(float(dist.min())))
assert len(parts)==14,len(parts)
assert min_gap>=60,min_gap

hand=np.array(Image.open(ROOT/'hand_palm.png').convert('RGBA'))
cyan=(hand[:,:,1].astype(int)-hand[:,:,0].astype(int)>40)&(hand[:,:,2].astype(int)-hand[:,:,0].astype(int)>40)&(hand[:,:,3]>128)
core=max(components(cyan),key=lambda p:p['area'])
cb=core['bbox']; center=[round((cb[0]+cb[2])/2,1),round((cb[1]+cb[3])/2,1)]
floating=Image.open(ROOT/'floating.png')
alpha=np.array(floating.getchannel('A'))
yy,xx=np.where(alpha>128)
radius=float(np.hypot(xx-floating.width/2,yy-floating.height/2).max())
assert radius<floating.height/2,radius
anchors={'parts_count':len(parts),'parts_min_gap_at_alpha_gt_128_px':round(min_gap,2),
         'parts_bounds':[p['bbox'] for p in parts],
         'hand_palm_core_center_px':center,'hand_palm_core_center_normalized':[round(center[0]/hand.shape[1],4),round(center[1]/hand.shape[0],4)],
         'hand_gap_fingertip_approx_px':[1144,165],'hand_gap_thread_endpoint_approx_px':[1190,146],
         'world_waterline_approx_y_px':594,'world_waterline_approx_normalized_y':round(594/941,4),
         'world_foreground_figure_approx_bounds_px':[518,540,610,728],
         'floating_max_opaque_radius_from_canvas_center_px':round(radius,2),'floating_rotation_safe_radius_px':floating.height/2,
         'notes':'Anchors are measured or visually estimated on native outputs for compositing. Some positions differ from the plan approximate guides.'}
(ROOT/'_qa'/'anchors.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(anchors,ensure_ascii=False,indent=2))
