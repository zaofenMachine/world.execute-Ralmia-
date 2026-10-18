from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,json
R=Path(__file__).resolve().parents[2];P=R/'_production'/'round6';Q=R/'_qa'/'round6'
def canvas(im):
    assert im.width in (1671,1672) and im.height==941,im.size
    if im.width==1671:
        dst=Image.new(im.mode,(1672,941),0);dst.paste(im,(0,0));return dst
    return im
def clean(im):
    im=canvas(im.convert('RGBA'));a=np.array(im)
    alpha=a[:,:,3];alpha[alpha<=2]=0
    near=np.array(Image.fromarray(alpha).filter(ImageFilter.MinFilter(9)))<32
    fringe=near&(a[:,:,0]>220)&(a[:,:,1]<90)&(a[:,:,2]<150)&(a[:,:,0].astype(int)-a[:,:,1].astype(int)>100)
    alpha[fringe]=0
    opaque=alpha>=245;edges=(alpha>0)&(alpha<245);done=~edges
    h,w=alpha.shape
    offsets=sorted([(dx,dy) for dx in range(-4,5) for dy in range(-4,5) if dx or dy],key=lambda v:v[0]**2+v[1]**2)
    for dx,dy in offsets:
        valid=np.roll(opaque,(-dy,-dx),(0,1))&~done
        if dy<0: valid[:-dy,:]=False
        if dy>0: valid[h-dy:,:]=False
        if dx<0: valid[:,:-dx]=False
        if dx>0: valid[:,w-dx:]=False
        if valid.any():
            shifted=np.roll(a[:,:,:3],(-dy,-dx),(0,1))
            a[valid,:3]=shifted[valid];done[valid]=True
    a[:,:,3]=alpha
    a[alpha==0,:3]=0
    return Image.fromarray(a)
def fit_height(im,fraction):
    im=clean(im);alpha=np.array(im.getchannel('A'));ys,xs=np.where(alpha>32)
    box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
    crop=im.crop(box);s=min(1.,941*fraction/crop.height)
    size=(round(crop.width*s),round(crop.height*s))
    crop=crop.resize(size,Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(1672,941));pos=((1672-size[0])//2,(941-size[1])//2)
    out.alpha_composite(crop,pos)
    return out,{'source_bbox':box,'scale':s,'target_bbox':[pos[0],pos[1],pos[0]+size[0],pos[1]+size[1]]}
if __name__=='__main__':
    im,stat=fit_height(Image.open(P/'raw'/'lishenna_sit_final_ai.png'),.8)
    im.save(R/'lishenna_sit.png')
    (Q/'sit_registration.json').write_text(json.dumps(stat,indent=2),encoding='utf-8')
    print(stat)
