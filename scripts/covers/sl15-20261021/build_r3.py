#!/usr/bin/env python3
"""SL-15 covers round 3 (Dan, 2026-10-22): "Let's go with F. Let's change the text to 'How a spray tan makes you look more ripped.'
I like these images in F, but I want a few different designs. Maybe one where it's diagonally divided. I feel like this has a
little bit too much blank space. Give me a few different designs with the same images in F and that text."
Same two real photos as F (film P01: pale_intro / tan_125), new copy, four designs with no empty field:
  H  diagonal split, pale upper left / tan lower right, Impact headline on a dark band on top
  I  diagonal split the other way, pale upper right / tan lower left, Avenir Heavy headline on black at the bottom
  J  two straight full-height halves with a white divider, DIN headline on a yellow band on top (C's band)
  K  the tan photo full bleed as the hero, the pale photo as a tilted white-framed inset, Futura headline with a marker box
Each region is filled by a blurred, darkened enlargement of its own photo behind the sharp photo, so nothing is blank. The
diagonal is chosen by search: the line that leaves every person pixel of each photo on its own side (person masks, Apple Vision).
Real photos only, never redrawn; type set in code. Records go into manifest.json beside rounds 1 and 2 for qc.py."""
import json,sys,os,subprocess,tempfile
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageEnhance
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build as b
from build import R,W,H,WHITE,INK,YEL,IMPACT,DIN,ARIAL,FUTURA,AVENIR,font,common,text,box
PH=Path('/Volumes/Extreme/_edit_work/ro19/photos')
AMBER=(255,170,60);GREY=(196,204,214)
LINES=['How A Spray Tan Makes','You Look More Ripped'];TITLE=' '.join(LINES);BADGE='SPRAY TANNING'
SLUG='spraytan-short1_why-you-look-less-ripped-in-photos'
SRC={'pale':('pale_intro.jpg',(179,100,2829,3633)),'tan':('tan_125.jpg',(147,0,2722,3433))}   # F's crops (build_r2.py)
CHIPS={'pale':('Before The Tan',GREY),'tan':('After The Tan',AMBER)}
PM=os.path.expanduser('~/.cache/absbyai/personmask/personmask')
def pmask(im):
 with tempfile.TemporaryDirectory() as t:
  a,m=os.path.join(t,'i.png'),os.path.join(t,'m.png');im.convert('RGB').save(a);subprocess.run([PM,a,m],capture_output=True,check=True)
  return np.array(Image.open(m).convert('L').resize(im.size))>127
_cache={}
def sharp(side,w):
 """F's crop of one photo at width w, with its person mask."""
 if (side,w) in _cache:return _cache[(side,w)]
 name,c=SRC[side];src=Image.open(PH/name).convert('RGB');cr=src.crop(c);h=round(w*cr.height/cr.width);im=cr.resize((w,h),Image.Resampling.LANCZOS)
 _cache[(side,w)]=(im,pmask(im),dict(source=str(PH/name),source_sha256=b.sha(PH/name),source_crop=list(c)));return _cache[(side,w)]
def backdrop(side,size):
 name,_=SRC[side];im=Image.open(PH/name).convert('RGB');sw,sh=im.size;k=max(size[0]/sw,size[1]/sh)*1.15
 im=im.resize((round(sw*k),round(sh*k)));x=(im.width-size[0])//2;y=(im.height-size[1])//2
 im=im.crop((x,y,x+size[0],y+size[1])).filter(ImageFilter.GaussianBlur(28));return ImageEnhance.Brightness(im).enhance(0.55)
def feather(size,f=46):
 m=np.ones((size[1],size[0]),np.float32);r=np.linspace(0,1,f)
 m[:f]*=r[:,None];m[-f:]*=r[::-1][:,None];m[:,:f]*=r[None,:];m[:,-f:]*=r[::-1][None,:];return m
def layer(side,w,xy,keep_edges=()):
 """Full-canvas RGBA of one photo: blurred backdrop everywhere, sharp photo at xy with feathered edges (edges named in keep_edges
 stay hard, for a photo that meets the canvas edge), plus that photo's person mask on the canvas."""
 im,pm,info=sharp(side,w);bg=backdrop(side,(W,H)).convert('RGBA');f=feather(im.size)
 if 'left' in keep_edges:f[:,:46]=np.maximum(f[:,:46],1)
 if 'right' in keep_edges:f[:,-46:]=np.maximum(f[:,-46:],1)
 if 'bottom' in keep_edges:f[-46:]=np.maximum(f[-46:],1)
 s=im.convert('RGBA');s.putalpha(Image.fromarray((np.clip(f,0,1)*255).astype(np.uint8)));bg.alpha_composite(s,xy)
 cm=np.zeros((H,W),bool);x,y=xy;x0,y0=max(0,x),max(0,y);x1,y1=min(W,x+im.width),min(H,y+im.height)
 cm[y0:y1,x0:x1]=pm[y0-y:y1-y,x0-x:x1-x];return bg,cm,info
def fit_pair(top,bottom,upper,lower,upper_left=True,gap=14):
 """Largest width at which the two people, staggered (upper photo against the top-left or top-right, lower photo against the
 opposite bottom corner), do not touch: person masks dilated by `gap` px must not intersect."""
 from scipy.ndimage import binary_dilation
 for w in range(720,460,-20):
  hu=sharp(upper,w)[0].height;hl=sharp(lower,w)[0].height
  if hu>bottom-top or hl>bottom-top:continue
  pu=(0 if upper_left else W-w,top);pl=(W-w if upper_left else 0,bottom-hl)
  mu=canvas_mask(upper,w,pu);ml=canvas_mask(lower,w,pl)
  if not (binary_dilation(mu,iterations=gap)&ml).any():return w,pu,pl,mu,ml
 raise ValueError('no clean stagger')
def canvas_mask(side,w,xy):
 im,pm,_=sharp(side,w);cm=np.zeros((H,W),bool);x,y=xy;x0,y0=max(0,x),max(0,y);x1,y1=min(W,x+im.width),min(H,y+im.height)
 cm[y0:y1,x0:x1]=pm[y0-y:y1-y,x0-x:x1-x];return cm
def mid_line(mu,ml,upper_left):
 """The diagonal for the backgrounds: through the midpoint between the two people's centres, at the steepest angle that keeps
 each person's centre on its own side."""
 cu=np.argwhere(mu).mean(axis=0);cl=np.argwhere(ml).mean(axis=0);my,mx=(cu+cl)/2
 d=420 if upper_left else -420   # y drop across the canvas: rises to the right for upper-left/lower-right, else to the left
 y0=my+d*mx/W;y1=y0-d;return int(y0),int(y1)
def split(la,lb,y0,y1,ma=None,mb=None):
 """Backgrounds divided by the diagonal (A above); each person then laid back on top whole, so the line runs behind them."""
 X=np.arange(W)[None,:];Y=np.arange(H)[:,None];above=(Y<y0+(y1-y0)*X/W)
 out=lb.copy();a=la.copy();a.putalpha(Image.fromarray((above*255).astype(np.uint8)));out.alpha_composite(a)
 g=Image.new('RGBA',(W,H));d=ImageDraw.Draw(g);d.line((0,y0,W,y1),fill=AMBER+(255,),width=26);g=g.filter(ImageFilter.GaussianBlur(10))
 out.alpha_composite(g);ImageDraw.Draw(out).line((0,y0,W,y1),fill=WHITE,width=10)
 for lay,m in ((la,ma),(lb,mb)):
  if m is None:continue
  p=lay.copy();p.putalpha(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)));out.alpha_composite(p)
 return out
def cutout(side,w,xy,fade=0):
 """The person alone from F's crop (Apple Vision mask), white keyline and soft shadow, on a transparent canvas. fade: rows at the
 bottom of the crop faded out so a figure that ends mid-thigh does not stop on a hard edge."""
 im,pm,info=sharp(side,w);a=Image.fromarray((pm*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
 if fade:
  f=np.ones(im.size[::-1],np.float32);f[-fade:]=np.linspace(1,0,fade)[:,None];a=Image.fromarray((np.asarray(a)*f).astype(np.uint8))
 pad=30;big=Image.new('L',(im.width+2*pad,im.height+2*pad));big.paste(a,(pad,pad))
 out=Image.new('RGBA',(W,H));x,y=xy
 sh=Image.new('RGBA',big.size,(0,0,0,0));sh.putalpha(big.filter(ImageFilter.GaussianBlur(16)).point(lambda v:int(v*0.6)));out.alpha_composite(sh,(x-pad+10,y-pad+14))
 kl=Image.new('RGBA',big.size,WHITE+(255,));kl.putalpha(big.filter(ImageFilter.MaxFilter(15)));out.alpha_composite(kl,(x-pad,y-pad))
 p=im.convert('RGBA');p.putalpha(a);out.alpha_composite(p,(x,y));return out,info
def duo_bg(y0,y1,upper_left):
 """Two-tone field: cool slate on the pale side (above the line), warm bronze on the tan side, white line with an amber glow."""
 yy,xx=np.mgrid[0:H,0:W];above=yy<y0+(y1-y0)*xx/W;t=yy/H
 cool=np.stack([34+40*t,42+46*t,54+52*t],-1);warm=np.stack([92+110*(1-t),44+50*(1-t),12+18*(1-t)],-1)
 im=Image.fromarray(np.where(above[...,None],cool,warm).astype(np.uint8)).convert('RGBA')
 g=Image.new('RGBA',(W,H));ImageDraw.Draw(g).line((0,y0,W,y1),fill=AMBER+(255,),width=30);im.alpha_composite(g.filter(ImageFilter.GaussianBlur(12)))
 ImageDraw.Draw(im).line((0,y0,W,y1),fill=WHITE,width=10);return im
def chip(canvas,mask,cx,y,side,size=34):
 label,fill=CHIPS[side];f=font(ARIAL,size);bb=f.getbbox(label);w=bb[2]-bb[0]+52
 box(canvas,mask,(cx-w//2,y,cx+w//2,y+size+26),fill,30);text(canvas,mask,(cx,y+12),label,f,INK,anchor='ma')
def band_top(im,tm,ig,f_spec,col1,col2,band=(8,10,14),stroke=0,y_start=None):
 top=236 if ig else 48;y=y_start or top+28;f=common(LINES,f_spec,150,990,stroke);step=round(f.size*1.0)
 fb=font(ARIAL,36);bot=y+52+2*step+18
 ImageDraw.Draw(im).rectangle((0,0,W,bot),fill=band);ImageDraw.Draw(im).rectangle((0,bot,W,bot+8),fill=AMBER)
 text(im,tm,(W//2,y),BADGE,fb,AMBER,anchor='ma')
 for i,ln in enumerate(LINES):text(im,tm,(W//2,y+52+i*step),ln,f,col1 if i==0 else col2,stroke,anchor='ma')
 return bot+8
def make_H(ig):
 tm=Image.new('L',(W,H));bot=band_top(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),ig,IMPACT,WHITE,AMBER,stroke=5)
 B=H;w,pu,pl,mu,ml=fit_pair(bot+20,B,'pale','tan',True,gap=34)   # the tan figure stands on the bottom edge
 y0,y1=mid_line(mu,ml,True);im=duo_bg(y0,y1,True)
 cu,ia=cutout('pale',w,pu,fade=90);cl,ib=cutout('tan',w,pl);im.alpha_composite(cu);im.alpha_composite(cl);pic=im.copy()
 band_top(im,tm,ig,IMPACT,WHITE,AMBER,stroke=5)
 chip(im,tm,W-200,bot+50,'pale');chip(im,tm,200,(1540 if ig else 1660),'tan')
 return im,tm,pic,dict(line=[y0,y1],width=w,pale=ia,tan=ib)
def make_I(ig):
 B=1620 if ig else 1740;f=common(LINES,AVENIR,160,1000,4);step=round(f.size*0.98)
 ty=B-2*step-10;fb=font(ARIAL,36);band=ty-70;T=250 if ig else 60
 w,pu,pl,mu,ml=fit_pair(T,band-50,'pale','tan',False,gap=34)
 y0,y1=mid_line(mu,ml,False);im=duo_bg(y0,y1,False)
 cu,ia=cutout('pale',w,pu,fade=90);cl,ib=cutout('tan',w,pl,fade=90);im.alpha_composite(cu);im.alpha_composite(cl)
 ImageDraw.Draw(im).rectangle((0,band,W,H),fill=(6,7,9));ImageDraw.Draw(im).rectangle((0,band,W,band+8),fill=AMBER);pic=im.copy();tm=Image.new('L',(W,H))
 text(im,tm,(W//2,band+8),BADGE,fb,AMBER,anchor='ma')
 for i,ln in enumerate(LINES):text(im,tm,(W//2,ty+i*step-24),ln,f,WHITE if i==0 else AMBER,4,anchor='ma')
 chip(im,tm,210,T+40,'pale');chip(im,tm,W-210,band-84,'tan')
 return im,tm,pic,dict(line=[y0,y1],width=w,pale=ia,tan=ib)
def make_J(ig):
 tm=Image.new('L',(W,H));top=236 if ig else 48;f=common(LINES,DIN,170,980);step=round(f.size*0.92);fb=font(ARIAL,36)
 bw=fb.getbbox(BADGE)[2];bh=24+60+12+2*step+18;yb=top+bh;B=1680 if ig else H;w=540
 halves=[]
 for j,side in enumerate(['pale','tan']):
  im_,pm,info=sharp(side,w);col=backdrop(side,(w,B-yb)).convert('RGBA');y=max(0,((B-yb)-im_.height)//2-60)
  ff=feather(im_.size,40);ff[:,:40]=1;ff[:,-40:]=1;s=im_.convert('RGBA');s.putalpha(Image.fromarray((ff*255).astype(np.uint8)));col.alpha_composite(s,(0,y));halves.append((col,info,y,im_.height))
 im=Image.new('RGBA',(W,H),(6,7,9,255))
 for j,(col,info,y,hh) in enumerate(halves):im.alpha_composite(col,(j*w,yb))
 ImageDraw.Draw(im).rectangle((W//2-5,yb,W//2+5,B),fill=WHITE);pic=im.copy()
 box(im,tm,(0,top,W,yb),YEL);ImageDraw.Draw(im).rectangle((54,top+24,54+bw+40,top+82),fill=INK);text(im,tm,(74,top+33),BADGE,fb,YEL)
 for i,ln in enumerate(LINES):text(im,tm,(54,top+100+i*step),ln,f,INK if i==0 else (196,24,24))
 for j,side in enumerate(['pale','tan']):
  col,info,y,hh=halves[j];chip(im,tm,j*w+w//2,min(B-90,yb+y+hh+10),side)
 return im,tm,pic,dict(pale=halves[0][1],tan=halves[1][1])
def hero_tan(s):
 """The whole tan_125 frame at scale s, with its person mask (Apple Vision)."""
 if ('hero',s) in _cache:return _cache[('hero',s)]
 src=Image.open(PH/SRC['tan'][0]).convert('RGB');im=src.resize((round(src.width*s),round(src.height*s)),Image.Resampling.LANCZOS)
 _cache[('hero',s)]=(im,pmask(im));return _cache[('hero',s)]
def inset(w):
 pi,ppm,ip=sharp('pale',w);fr=Image.new('RGBA',(pi.width+24,pi.height+80),WHITE+(255,));fr.alpha_composite(pi.convert('RGBA'),(12,12))
 fc=font(ARIAL,27);ImageDraw.Draw(fr).text((fr.width//2,pi.height+26),'Before The Tan',font=fc,fill=INK,anchor='ma')
 return fr.rotate(7,expand=True,resample=Image.Resampling.BICUBIC),ip
def make_K(ig):
 """Round 4 (Dan, 2026-10-22): "move my body slightly to the right and up, the picture slightly to the left and down, and make the
 picture slightly smaller... so that the photo isn't blocking my body." The hero is the whole tan_125 frame, scaled so his right
 fist stays inside the frame with his centre further right, raised 40 px; the inset is smaller, in the bottom-left corner. The
 inset's position is searched until it does not touch his person mask (overlap reported in the manifest)."""
 tm=Image.new('L',(W,H));top=250 if ig else 64;f1=b.fit(LINES[0],FUTURA,118,980,5);f2=b.fit(LINES[1],FUTURA,118,920)
 y2=top+56+f1.size+22;b2=f2.getbbox(LINES[1],anchor='ma');hb=y2+b2[3]+40;B=1700 if ig else H+26   # YouTube: the print may run just past the bottom edge (its caption stays inside)
 # Round 5 (Dan, 2026-10-22): "For the Instagram crop, make the photo slightly larger. For the YouTube crop, make my photo extend to the
 # bottom and also make the photo slightly larger... make the YouTube one look a little bit more like the Instagram and move the photo
 # down." YouTube: the hero is larger and stands on the bottom edge, its top just under the headline; the fist limit sets its centre.
 FIST,MID,RIGHT=1070,1492,2685   # his right fist's outer edge and his centre in the source (measured)
 from scipy.ndimage import binary_dilation
 def try_scale(sc,CX,ty_fn):
  hi,hm=hero_tan(sc);hx=round(CX-MID*sc);ty=ty_fn(hi)
  cm=np.zeros((H,W),bool);x0,y0=max(0,hx),max(0,ty);x1,y1=min(W,hx+hi.width),min(H,ty+hi.height);cm[y0:y1,x0:x1]=hm[y0-ty:y1-ty,x0-hx:x1-hx]
  cmd=binary_dilation(cm,iterations=10);best=None
  for w in (330,320,310,300,290):   # round 5: larger than round 4's 290 where it still clears him
   fr,ip=inset(w)
   for ix in (8,0,-8,-16):
    iy=B-fr.height;a=np.zeros((H,W),bool);ys,xs=np.where(np.asarray(fr.getchannel('A'))>20)
    ys=ys+iy;xs=xs+ix;k=(xs>=0)&(xs<W)&(ys>=0)&(ys<H);a[ys[k],xs[k]]=True;ov=int((a&cmd).sum())
    if best is None or (ov,-w)<(best[0],-best[1]):best=(ov,w,ix,iy,fr,ip)
    if ov==0:break
   if best[0]==0:break
  return hi,hx,ty,best
 # Round 6 (Dan, 2026-10-22): "Move the photo up in the YouTube one to the same position as the Instagram... and move the 'after the
 # tan' to the upper right, the same as the Instagram." YouTube is now the Instagram composition (same hero size and centre, same
 # print size and place relative to him, same chip place) moved down by SHIFT so his photo stands on the bottom edge.
 IG_TY=571-50;IG_B=1700;sc=0.40
 if ig:SHIFT=0;hi,hx,ty,best=try_scale(sc,610,lambda h:hb-50)
 else:
  SHIFT=(H-hero_tan(sc)[0].height)-IG_TY;B=IG_B+SHIFT;hi,hx,ty,best=try_scale(sc,610,lambda h:H-h.height)
 if not ig:   # YouTube: the headline block moves down to sit on the hero's top edge, as on Instagram (no blurred band between)
  sh_=ty+50-hb;top+=sh_;y2+=sh_;hb+=sh_
 im=backdrop('tan',(W,H)).convert('RGBA');ff=feather(hi.size,60);ff[:,-60:]=1;ff[-60:]=1;ff[:60]=1
 s_=hi.convert('RGBA');s_.putalpha(Image.fromarray((ff*255).astype(np.uint8)));im.alpha_composite(s_,(hx,ty))
 ov,w,ix,iy,fr,ip=best
 b.ramp(im,0,hb+120,240)
 sh=Image.new('RGBA',fr.size,(0,0,0,0));sh.putalpha(fr.getchannel('A').point(lambda v:int(v*0.55)))
 im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)),(ix+10,iy+12));im.alpha_composite(fr,(ix,iy))
 pic=im.copy()
 fb=font(ARIAL,38);text(im,tm,(W//2,top),BADGE,fb,YEL,3,anchor='ma');text(im,tm,(W//2,top+56),LINES[0],f1,WHITE,5,anchor='ma')
 box(im,tm,(W//2+b2[0]-20,y2+b2[1]-14,W//2+b2[2]+20,y2+b2[3]+14),AMBER,8);text(im,tm,(W//2,y2),LINES[1],f2,INK,anchor='ma')
 from scipy.ndimage import distance_transform_edt
 dist=distance_transform_edt(~pmask(pic));cw=270;chh=60;spot=None
 for y in range(1540+SHIFT,hb+20,-20):
  for cx in (W-150,W-170):   # right side only: the pale inset holds the bottom left
   if dist[y:y+chh,cx-cw//2:cx+cw//2].min()>=40:spot=(cx,y);break
  if spot:break
 chip(im,tm,spot[0],spot[1],'tan')
 name=PH/SRC['tan'][0]
 return im,tm,pic,dict(hero=dict(source=str(name),source_sha256=b.sha(name),scale=sc,xy=[hx,ty]),inset=ip,inset_width=w,
  inset_box=[ix,iy,ix+fr.width,iy+fr.height],inset_overlap_px=ov)
ROUND3=['H','I','K']   # J (two halves with blurred fill bands) dropped before review: the fill read as empty
KIND3={'H':'Pale vs tan cutouts on a diagonal two-tone split, headline on top','I':'Pale vs tan cutouts on a diagonal two-tone split, headline at the bottom',
 'J':'Pale vs tan pair, two halves under a yellow band','K':'Tan photo full bleed, pale photo as a tilted inset'}
if __name__=='__main__':
 only=sys.argv[1:] or ROUND3;mp=R/'manifest.json';m=json.loads(mp.read_text());rec=[r for r in m['outputs'] if not (r['short']=='s1' and r['variant'] in only)]
 for v in only:
  for platform in ['instagram','youtube']:
   ig=platform=='instagram';im,tm,pic,info={'H':make_H,'I':make_I,'J':make_J,'K':make_K}[v](ig);slug=f'{SLUG}_cover-{v}';p=R/platform/(slug+'.png')
   im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'));pic.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
   ph=R/'phone'/platform;Image.open(p).resize((270,480),Image.Resampling.LANCZOS).save(ph/(slug+'.jpg'),quality=95)
   rec.append(dict(short='s1',variant=v,platform=platform,path=str(p),sha256=b.sha(p),kind=KIND3[v],round=3,has_person=True,
    copy={'badge':BADGE,'headline':LINES,'chips':['Before The Tan','After The Tan']},**info));print(v,platform,{k:info[k] for k in info if k in('line','width','inset_overlap_px','inset_width','inset_box')})
 m['outputs']=rec;m['status']='round 3: short 1 H/I/K awaiting Dan pick; short 2 C picked';mp.write_text(json.dumps(m,indent=1)+'\n')
