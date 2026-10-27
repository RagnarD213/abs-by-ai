#!/usr/bin/env python3
"""Round 2 (Dan, 2026-10-27). B picked for Getting Abs, Top 3 Ways AI and Weigh Daily, with his changes, which are now
the standard for this layout: picture slightly larger, no eyebrow pill, bottom headline significantly larger.
Supplements: new concept (he in the background, three unlabeled supplements in the foreground), yellow band on top."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build as B
from build import W,H,Image,ImageDraw,ImageOps,font,common,text,ramp,plate,sha,AVENIR,WHITE,CYAN,COPY,R
SCALE=1.12
# Three lines so the type can be much larger than the two-line version (width-limited by the long second line).
BIG={'ds02':['How Getting Abs','Looksmaxxes','Your Face'],'ds07':['Top 3 Ways','To Use AI','To Get Abs'],'ds11':['Why You Must','Weigh Yourself','Daily']}
def lay_big_bottom(canvas,mask,k,ig):
 """Bottom headline, no pill, significantly larger (Avenir Heavy up to 240 px, full width)."""
 lines=BIG[k];limit=1608 if ig else 1740
 cap=round(min(300,1.15*common(lines,AVENIR,330,1020,6).size)*(0.88 if ig else 1))
 fs=[B.fit(ln,AVENIR,cap,1020,6) for ln in lines];y=limit;ys=[]
 for ln,f in zip(reversed(lines),reversed(fs)):
  y-=f.getbbox(ln,stroke_width=6,anchor='ma')[3];ys.insert(0,y);y-=round(f.size*0.04)
 for i,(ln,f,yy) in enumerate(zip(lines,fs,ys)):text(canvas,mask,(W//2,yy),ln,f,CYAN if i==len(lines)-1 else WHITE,6,anchor='ma')
 return ys[0]
def bigger(im):
 """Picture 12% larger, centred horizontally, top kept (his hair stays in frame)."""
 big=im.resize((round(W*SCALE),round(H*SCALE)),Image.Resampling.LANCZOS);x=(big.width-W)//2;return big.crop((x,0,x+W,H))
def build_b(k):
 out=[]
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';im,gp=plate(k,'b');im=bigger(im)
  top=lay_big_bottom(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig)
  ramp(im,top-170,top+30,245,top_dark=False);tm=Image.new('L',(W,H));lay_big_bottom(im,tm,k,ig)
  out.append(save(im,tm,k,'B2',platform))
 return out
def build_supp(tag):
 k='ds03';out=[]
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';src=R/'assets/gen'/f'ds03-{tag}.png'
  im=ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
  bb=B.lay_C(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig);im,_=B.drop_below(im,bb+40)
  tm=Image.new('L',(W,H));B.lay_C(im,tm,k,ig);out.append(save(im,tm,k,'S'+tag[-1].upper(),platform))
 return out
def save(im,tm,k,v,platform):
 d=R/'round2'/platform;d.mkdir(parents=True,exist_ok=True);p=d/f'{COPY[k][1]}_cover-{v}.png'
 im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
 if platform=='youtube':im.convert('RGB').save(p.with_suffix('.jpg'),quality=92)
 return dict(short=k,variant=v,platform=platform,path=str(p),sha256=sha(p))
if __name__=='__main__':
 recs=[]
 for a in sys.argv[1:]:recs+=build_b(a) if a!='supp' else build_supp('r2a')+build_supp('r2b')
 mp=R/'round2/manifest.json';old=json.loads(mp.read_text()) if mp.exists() else []
 keep=[r for r in old if (r['short'],r['variant'],r['platform']) not in {(x['short'],x['variant'],x['platform']) for x in recs}]
 mp.write_text(json.dumps(keep+recs,indent=1));print('built',len(recs))
