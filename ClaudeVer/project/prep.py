import cv2, numpy as np, glob, os
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'..','..','AstraVer','Images')
def xdog(gray, sigma, k=1.6, p=30, eps=-0.01, phi=15):
    g=gray.astype(np.float32)/255
    a=cv2.GaussianBlur(g,(0,0),sigma); b=cv2.GaussianBlur(g,(0,0),sigma*k)
    d=(1+p)*a-p*b
    return np.clip(np.where(d>=eps,1.0,1+np.tanh(phi*(d-eps))),0,1)
for f in sorted(glob.glob(SRC+'/*/*.png')):
    n=os.path.basename(f)[:-4]
    im=cv2.imread(f)
    im=cv2.resize(im,(1920,int(round(941*1920/1672))),interpolation=cv2.INTER_LANCZOS4)[:1080]
    sm=cv2.bilateralFilter(im,9,30,7); sm=cv2.bilateralFilter(sm,9,30,7)
    gray=cv2.cvtColor(sm,cv2.COLOR_BGR2GRAY)
    line=xdog(gray,1.1)
    # clean specks
    inv=((1-line)>0.5).astype(np.uint8)
    nlab,lab,st,_=cv2.connectedComponentsWithStats(inv,8)
    keep=np.zeros(nlab,bool); keep[1:]=st[1:,cv2.CC_STAT_AREA]>=40
    mask=keep[lab]
    line=np.where(mask,line,1.0)
    flat=cv2.pyrMeanShiftFiltering(cv2.resize(im,(960,540)),8,16)
    flat=cv2.resize(flat,(1920,1080),interpolation=cv2.INTER_CUBIC)
    flat=cv2.bilateralFilter(flat,9,40,9)
    hd=(flat.astype(np.float32)*(0.12+0.88*line[...,None])).clip(0,255).astype(np.uint8)
    cv2.imwrite(f'{HERE}/assets/{n}_full.png',im)
    cv2.imwrite(f'{HERE}/assets/{n}_line.png',(line*255).astype(np.uint8))
    cv2.imwrite(f'{HERE}/assets/{n}_hd.png',hd)
