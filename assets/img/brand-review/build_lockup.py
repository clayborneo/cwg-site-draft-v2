#!/usr/bin/env python3
"""Rebuild the CWG lockup in the badge's script (Ephesis, thickened to the badge's stroke weight),
reusing the sprig + gold sweep from the original v6 art. Also writes the white version and
the A-F colour variants for brand-review (lockup-*.png and badge-*.png)."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, pathlib
W='/private/tmp/claude-501/-Users-clayborneo-Desktop-claude-code-cwg/b14551e3-99d5-4ce5-8e03-76f8cf57ec28/scratchpad/'
ROOT=pathlib.Path('/Users/clayborneo/Desktop/claude-code/cwg/site-draft-v2')
FONT=W+'fonts/Ephesis-Regular.ttf'
PLUM=(94,45,94,255); TEAL=(47,93,86,255)
VARS=[('a','#5E2D5E','#2F5D56','#C7A65A'),('b','#1E2A44','#2F5D56','#C7A65A'),('c','#5E2D5E','#B48AB7','#C7A65A'),
      ('d','#1E2A44','#B48AB7','#C7A65A'),('e','#2F5D56','#5E2D5E','#C7A65A'),('f','#5E2D5E','#5E2D5E','#5E2D5E')]
src=Image.open(ROOT/'assets/img/brand-v6/lockup-v1-greatvibes.png').convert('RGBA'); a=np.asarray(src).astype(int)
H,Wd=a.shape[:2]; al=a[...,3]>10; r,g,b=a[...,0],a[...,1],a[...,2]
mx=np.maximum(np.maximum(r,g),b); mn=np.minimum(np.minimum(r,g),b); sat=(mx-mn)/np.maximum(mx,1)
yy,xx=np.mgrid[0:H,0:Wd]
plumhue=(b>=g)&(r>=g)&(sat>0.12)
sprig=al&(xx>=940)&(yy<=560)&~(plumhue&(yy>445))&~((xx<990)&(yy>380))
gold=(r>g)&(g>b)&(sat>0.22)
sweep=al&gold&(yy>=630)&(yy<=845)
def parts_img(white=False):
    parts=np.zeros_like(a); m=sprig|sweep; parts[m]=a[m]
    if white:
        pm=parts.astype(float); lum=(0.299*pm[...,0]+0.587*pm[...,1]+0.114*pm[...,2])/255
        isgold=gold&sprig; tint=np.clip(0.75+lum*0.35,0.7,1.0)
        for c in range(3): pm[...,c]=np.where(sprig&~isgold,255*tint,pm[...,c])
        parts=pm.astype(int)
    return Image.fromarray(parts.astype(np.uint8),'RGBA')
def render(text,target_w,color,stroke_frac=0.012):
    lo,hi=50,900
    for _ in range(30):
        s=(lo+hi)/2; f=ImageFont.truetype(FONT,int(s)); x0,y0,x1,y1=f.getbbox(text)
        if x1-x0<target_w: lo=s
        else: hi=s
    size=int(lo); f=ImageFont.truetype(FONT,size); sw=max(1,int(size*stroke_frac)); x0,y0,x1,y1=f.getbbox(text,stroke_width=sw)
    img=Image.new('RGBA',(x1-x0+40,y1-y0+40),(0,0,0,0)); ImageDraw.Draw(img).text((20-x0,20-y0),text,font=f,fill=color,stroke_width=sw,stroke_fill=color)
    return img
def place(canvas,img,left=None,right=None,top=None):
    bb=img.getbbox(); crop=img.crop(bb); x=left if left is not None else right-crop.width
    canvas.alpha_composite(crop,(int(x),int(top)))
def compose(plum,teal,white=False):
    c=Image.new('RGBA',(Wd,H),(0,0,0,0))
    place(c,render('Caring',790,plum),left=150,top=178)
    place(c,render('Grace',770,plum),right=1312,top=515)
    place(c,render('with',210,teal),left=266,top=505)
    c.alpha_composite(parts_img(white)); return c
compose(PLUM,TEAL).save(ROOT/'assets/img/brand-v6/lockup-v1.png')
compose((255,255,255,255),(255,255,255,235),white=True).save(ROOT/'assets/img/brand-v6/lockup-v1-white.png')
print('lockup written')
# ---- colour variants (lockup + badge) by hue remap
def hexrgb(h): return np.array([int(h[i:i+2],16) for i in (1,3,5)],dtype=np.float32)
def recolor(path,prim,sec,acc):
    im=Image.open(path).convert('RGBA'); arr=np.asarray(im).astype(np.float32); h,w=arr.shape[:2]
    flat=arr[...,:3].reshape(-1,3); fa=arr[...,3].reshape(-1); fo=flat.copy()
    mx=flat.max(1); mn=flat.min(1); sat=np.where(mx>0,(mx-mn)/np.maximum(mx,1),0)
    r,g,b=flat[:,0],flat[:,1],flat[:,2]; d=np.maximum(mx-mn,1e-6); hue=np.zeros(len(flat))
    m=(mx==r); hue[m]=((g-b)/d)[m]%6
    m=(mx==g)&~(mx==r); hue[m]=((b-r)/d)[m]+2
    m=(mx==b)&~(mx==r)&~(mx==g); hue[m]=((r-g)/d)[m]+4
    hue*=60; ok=(sat>=0.16)&(fa>30)
    cls=np.full(len(flat),'',dtype='<U1'); cls[ok&(hue>=250)&(hue<=335)]='p'; cls[ok&(hue>=130)&(hue<=200)]='s'; cls[ok&(hue>=15)&(hue<=60)]='a'
    luma=0.299*r+0.587*g+0.114*b
    refs={'p':hexrgb('#5E2D5E'),'s':hexrgb('#2F5D56'),'a':hexrgb('#C7A65A')}; tgt={'p':hexrgb(prim),'s':hexrgb(sec),'a':hexrgb(acc)}
    for k in 'psa':
        sel=cls==k
        if not sel.any(): continue
        ref=0.299*refs[k][0]+0.587*refs[k][1]+0.114*refs[k][2]; ratio=(luma[sel]/ref)[:,None]
        newc=np.clip(tgt[k][None,:]*ratio,0,255); over=np.clip(ratio-1,0,None); newc=newc+(255-newc)*np.clip(over*0.6,0,1)
        fo[sel]=np.clip(newc,0,255)
    return Image.fromarray(np.dstack([fo.reshape(h,w,3),arr[...,3]]).astype(np.uint8),'RGBA')
out=ROOT/'assets/img/brand-review'
for f in out.glob('lockup-*.png'): f.unlink()
for f in out.glob('badge-*.png'): f.unlink()
Image.open(ROOT/'assets/img/brand-v6/lockup-v1.png').save(out/'lockup-a.png')
Image.open(ROOT/'assets/img/brand-v6/badge-karen.png').save(out/'badge-a.png')
Image.open(ROOT/'assets/img/brand-v6/lockup-v1-white.png').save(out/'lockup-white.png')
for k,p,s,ac in VARS[1:]:
    recolor(ROOT/'assets/img/brand-v6/lockup-v1.png',p,s,ac).save(out/f'lockup-{k}.png',optimize=True)
    recolor(ROOT/'assets/img/brand-v6/badge-karen.png',p,s,ac).save(out/f'badge-{k}.png',optimize=True)
print('variants written', sorted(x.name for x in out.glob('*.png')))
