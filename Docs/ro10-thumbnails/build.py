#!/usr/bin/env python3
"""RO-10 "Calories: The Reason You're Not Losing Weight": five thumbnail options.
1 = real pool photo (photo-244) on a Codex-made scene   2 = real studio photo (studio-blue-6) on a Codex-made scene
3,4,5 = three Codex AI images, each its own design (concepts in prompts/codex-concepts.json).
All type is set here in code, never generated. Run from anywhere. Export of FINAL waits for Dan's pick.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
AS=HERE/'assets'; PH=ROOT/'photos/finalized social media photos'
W,H=1280,720
MANROPE='/Users/danielrose/Library/Fonts/Manrope.ttf'
WHITE=(255,255,250); DARK=(10,12,18); YEL=(255,212,59); LIME=(163,255,18); ORANGE=(255,106,0)

def font(size):
 f=ImageFont.truetype(MANROPE,size); f.set_variation_by_name('ExtraBold'); return f

def person(path,mask,bottom):
 im=Image.open(path).convert('RGBA')
 if mask:
  a=Image.open(mask).convert('L').resize(im.size).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.65)); im.putalpha(a)
 im=im.crop((0,0,im.width,int(im.height*bottom)))
 return im.crop(im.getchannel('A').point(lambda p:255 if p>127 else 0).getbbox())

def place(canvas,p,height,right_margin,outline):
 s=height/p.height; p=p.resize((round(p.width*s),round(p.height*s)),Image.Resampling.LANCZOS)
 x=W-right_margin-p.width; y=H-p.height
 layer=Image.new('RGBA',(W,H)); layer.alpha_composite(p,(x,y)); a=layer.getchannel('A')
 sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(14)).point(lambda z:int(z*.6))); canvas.alpha_composite(sh)
 if outline:
  e=Image.new('RGBA',(W,H),(*WHITE,0)); e.putalpha(a.filter(ImageFilter.MaxFilter(13))); canvas.alpha_composite(e)
 canvas.alpha_composite(layer); return a

def scrim_left(im,strength,reach=820,color=DARK):
 ar=np.asarray(im.convert('RGB'),dtype=float); x=np.arange(W)[None,:]
 a=np.broadcast_to(strength*np.maximum(0,1-x/reach)**1.25,(H,W)).copy(); a=np.clip(a,0,235)/255
 return Image.fromarray((ar*(1-a[:,:,None])+np.array(color)[None,None,:]*a[:,:,None]).astype('uint8')).convert('RGBA')

def type_lines(canvas,lines,x,y,maxw,gap=6,bar=None,plate=None,stroke=0,anchor='l'):
 """lines: [(text,size,color)]. Fits each line to maxw. Returns list of boxes."""
 d=ImageDraw.Draw(canvas); boxes=[]; cy=y
 for s,size,col in lines:
  f=font(size)
  while d.textbbox((0,0),s,font=f,stroke_width=stroke)[2]>maxw: size-=1; f=font(size)
  b=d.textbbox((0,0),s,font=f,stroke_width=stroke); tw,th=b[2]-b[0],b[3]-b[1]
  tx=x if anchor=='l' else x-tw//2
  if plate and plate.get(s): d.rounded_rectangle((tx-22,cy-14,tx+tw+22,cy+th+22),radius=16,fill=plate[s])
  d.text((tx-b[0]+3,cy-b[1]+5),s,font=f,fill=(0,0,0,110),stroke_width=stroke+2,stroke_fill=(0,0,0,110)) if not (plate and plate.get(s)) else None
  d.text((tx-b[0],cy-b[1]),s,font=f,fill=col,stroke_width=stroke,stroke_fill=DARK)
  boxes.append((tx-6,cy-6,tx+tw+8,cy+th+8)); cy+=th+gap
 if bar:
  d.rectangle((x-30,y-4,x-20,cy-gap+4),fill=bar)
  boxes.append((x-30,y-4,x-20,cy-gap+4))
 return boxes

def finish(n,name,canvas,boxes,mask,source,notes):
 out=HERE/f'ro10-{n}.jpg'; canvas.convert('RGB').save(out,quality=94,subsampling=0)
 rec=dict(id=n,name=name,file=out.name,source=source,bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),notes=notes)
 assert out.stat().st_size<2_000_000
 assert min(b[0] for b in boxes)>=0 and max(b[2] for b in boxes)<=W and max(b[3] for b in boxes)<=H
 if mask is not None:
  ma=np.asarray(mask)>127; ys,xs=np.where(ma)
  grown=np.asarray(Image.fromarray((ma*255).astype('uint8')).filter(ImageFilter.MaxFilter(51)))>127   # 25 px halo
  clear=[]
  for x0,y0,x1,y1 in boxes:
   hit=grown[max(0,y0):min(H,y1),max(0,x0):min(W,x1)].any()
   clear.append(0 if hit else 25)
  rec['text_clearance_px']=min(clear); rec['hair_headroom_px']=int(ys.min())
  assert min(clear)>=25,(out.name,'text within 25 px of person',clear)
  assert ys.min()>=14,(out.name,'hair headroom',int(ys.min()))
 Image.open(out).resize((320,180),Image.Resampling.LANCZOS).save(HERE/f'ro10-{n}-feed.jpg',quality=94)
 return rec

recs=[]
# 1  pool photo on the scale + donut scene
bg=ImageOps.fit(Image.open(AS/'bg1.png').convert('RGB'),(W,H))
# Codex rendered a hard panel seam at x=695; blend it away with a wide horizontal blur masked around the seam.
arr=np.asarray(bg,dtype=float); big=np.asarray(bg.filter(ImageFilter.BoxBlur(1)),dtype=float)
from scipy.ndimage import uniform_filter1d,gaussian_filter1d
blur=gaussian_filter1d(arr,sigma=48,axis=1,mode='nearest')
wx=np.exp(-((np.arange(W)-695)/62.0)**2)[None,:,None]
bg=Image.fromarray((arr*(1-wx)+blur*wx).astype('uint8'))
c=scrim_left(bg,60,700)
c=c.convert('RGBA')
p=person(PH/'photo-244_FINAL_PRIMARY.jpg',AS/'mask/photo-244_FINAL_PRIMARY.mask.png',.74)
m=place(c,p,704,24,False)
bx=type_lines(c,[("IT'S THE",96,WHITE),('CALORIES',150,YEL)],72,56,620,gap=8,bar=YEL)
recs.append(finish(1,'POOL PHOTO: scale + donuts',c,bx,m,'photo-244_FINAL_PRIMARY.jpg (real pool shoot, cropped at mid-thigh, normal teal shorts); Codex scene bg1','real photo; Codex made scene only'))

# 2  studio photo on the junk-food pile scene
bg=ImageOps.fit(Image.open(AS/'bg2.png').convert('RGB'),(W,H)); c=scrim_left(bg,40,640,(5,20,70)).convert('RGBA')
p=person(PH/'_cutouts/studio-blue-6_CUTOUT.png',None,.74)
m=place(c,p,700,26,True)
bx=type_lines(c,[("IT'S THE",96,WHITE),('CALORIES',150,DARK)],72,56,600,gap=14,plate={'CALORIES':YEL})
recs.append(finish(2,'STUDIO PHOTO: junk-food pile',c,bx,m,'studio-blue-6_CUTOUT.png (real studio shoot, cropped at the waistband, fists out of frame); Codex scene bg2','real photo; Codex made scene only'))

# 3  Codex concept 1: man holding snack cakes on orange (headline left zone)
c=Image.open(AS/'ai1.png').convert('RGBA').resize((W,H))
m=Image.open(AS/'mask/ai1.mask.png').convert('L').resize((W,H))
bx=type_lines(c,[("IT'S THE",118,DARK),('CALORIES',170,WHITE)],92,150,540,gap=16,bar=None,plate={'CALORIES':DARK})
# white word on orange needs weight: add dark outline pass
d=ImageDraw.Draw(c)
recs.append(finish(3,'AI: snack-cake plate (Codex concept 1)',c,bx,m,'Codex gpt-6.1-sol image ai1 (AI man from a real reference photo, AI-generated)','AI image'))

# 4  Codex concept 2: overhead salad bowl, turquoise, headline top-right
c=Image.open(AS/'ai2.png').convert('RGBA').resize((W,H))
bx=type_lines(c,[('HIDDEN',112,WHITE),('CALORIES',132,LIME)],690,80,560,gap=8,bar=LIME)
recs.append(finish(4,'AI: loaded salad bowl (Codex concept 2)',c,bx,None,'Codex gpt-6.1-sol image ai2 (no person)','AI image'))

# 5  Codex concept 3: balance scale, violet, headline top-centre
c=Image.open(AS/'ai3.png').convert('RGBA').resize((W,H))
bx=type_lines(c,[('CALORIES',150,WHITE),('BEAT DIETS',112,YEL)],W//2,50,900,gap=6,anchor='c')
recs.append(finish(5,'AI: balanced scale (Codex concept 3)',c,bx,None,'Codex gpt-6.1-sol image ai3 (no person)','AI image'))

(HERE/'manifest-QC.json').write_text(json.dumps(recs,indent=2)+'\n')

# review sheet: five labelled 1-5 + feed-size strip
tw,th=600,338; g=24; mg=30; SW=3*tw+2*g+2*mg
sheet=Image.new('RGB',(SW,2*(th+60)+330),'#eef0f4'); d=ImageDraw.Draw(sheet)
d.text((mg,16),"CALORIES: THE REASON YOU'RE NOT LOSING WEIGHT | THUMBNAIL REVIEW",font=font(30),fill=DARK)
for i,r in enumerate(recs):
 x=mg+(i%3)*(tw+g); y=70+(i//3)*(th+60)
 sheet.paste(Image.open(HERE/r['file']).resize((tw,th),Image.Resampling.LANCZOS),(x,y))
 d.text((x,y+th+8),f"{r['id']}.  {r['name']}",font=font(21),fill=DARK)
y=70+2*(th+60)
d.text((mg,y),'Phone-feed size (320 px wide):',font=font(21),fill=DARK)
for i,r in enumerate(recs):
 sheet.paste(Image.open(HERE/f"ro10-{r['id']}-feed.jpg"),(mg+i*(320+16),y+36))
 d.text((mg+i*(320+16),y+36+186),str(r['id']),font=font(21),fill=DARK)
sheet.save(HERE/'REVIEW_ro10_thumbnails.jpg',quality=94)
print('PASS',[(r['id'],r.get('text_clearance_px'),r.get('hair_headroom_px')) for r in recs])
