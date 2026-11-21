#!/usr/bin/env python3
"""Real source frames and approved keyed Dan, adapted from DS44 split-cover method."""
from pathlib import Path
import hashlib, json, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT/'Short-form video content/covers/review/ds37-dr-mike-dial-20261103'
OUT = BASE/'round2'
SRC = OUT/'sources'
PUBLIC = BASE/'blind-review'
PM = Path.home()/'.cache/absbyai/personmask/personmask'
SUP = Path('/System/Library/Fonts/Supplemental')
W,H = 1080,1920
COPY = ['Tirzepatide Is', 'An Appetite Dial']
BRIEF = "I don't like any of these. Make me a few designs similar to the Hormozi reaction short that we just published, where it shows the original video on top and me reacting to it on the bottom (or the original video could be on the bottom). Basically show me reacting and the original video on this design"
DESIGNS = {
 'A': dict(label='Dr. Mike Above, Your Reaction Below', mike='665.00', dan='0065', reverse=False, full=False, accent='#FFD60A', font='Impact.ttf'),
 'B': dict(label='Your Reaction Above, Dr. Mike Below', mike='668.00', dan='0430', reverse=True, full=False, accent='#FFD60A', font='Impact.ttf'),
 'C': dict(label='Full Original Video Above', mike='668.00', dan='0600', reverse=False, full=True, accent='#FFD60A', font='DIN Condensed Bold.ttf'),
 'D': dict(label='Your Reaction Above, Blue Headline', mike='679.00', dan='0008', reverse=True, full=False, accent='#65D9FF', font='DIN Condensed Bold.ttf'),
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def detector(p):
 dest = p.with_name(p.stem+'.mask.png')
 x = subprocess.run([str(PM),str(p),str(dest)],capture_output=True,text=True,check=True)
 return json.loads(x.stdout)['faces']

def face_box(path):
 f=detector(path)
 assert len(f)==1,(path,f)
 x0,y0,x1,y1=f[0];fw=x1-x0;fh=y1-y0
 # Include actual bald scalp / hair above the detected face with extra clearance.
 return [max(0,x0-fw*.12),max(0,y0-fh*.32),min(Image.open(path).width,x1+fw*.12),y1+fh*.04]

def mike_panel(spec,height,platform,tail=0):
 path=SRC/f"mike-{spec['mike']}s.png"; im=Image.open(path).convert('RGB')
 face=face_box(path)
 if spec['full']:
  assert height==540
  pic=im.resize((W,height),Image.Resampling.LANCZOS)
  return pic,[x*.5625 for x in face]
 scale=1.42 if platform=='instagram' else 1.53
 if spec['reverse']:scale=1.32 if platform=='instagram' else 1.45
 scale=min(scale,(height-75)/(face[3]-face[1]))
 big=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 cx=(face[0]+face[2])/2
 x0=max(0,min(big.width-W,round(cx*scale-W/2)))
 y0=max(0,min(big.height-height,round(face[1]*scale-35)))
 assert y0+height+tail<=big.height
 pic=big.crop((x0,y0,x0+W,y0+height+tail))
 ff=[face[0]*scale-x0,face[1]*scale-y0,face[2]*scale-x0,face[3]*scale-y0]
 assert ff[1]>=20 and ff[3]<height-12,(spec,height,ff)
 return ImageEnhance.Contrast(pic).enhance(1.04),ff

def dan_panel(spec,height,platform,tail=0):
 path=SRC/f"dan-O{spec['dan']}.png";im=Image.open(path).convert('RGBA');face=face_box(path)
 scale=.72 if platform=='instagram' else 1.12
 if spec['full']:scale=.74 if platform=='instagram' else 1.02
 # Subject remains a real approved-key frame; no regenerated face, pose or body.
 ys,xs=np.where(np.array(im.getchannel('A'))>200)
 hair=int(ys.min());top=35
 width,height2=round(im.width*scale),round(im.height*scale)
 layer=im.resize((width,height2),Image.Resampling.LANCZOS)
 cx=(face[0]+face[2])/2
 x0=round(W/2-cx*scale);y0=round(top-hair*scale)
 yy,xx=np.mgrid[:height+tail,:W];glow=np.exp(-(((xx-W*.5)/(W*.6))**2+((yy-height*.35)/(height*.8))**2))
 if spec['full'] or spec['reverse']: c0=np.array([8,17,25]);c1=np.array([29,54,72])
 else:c0=np.array([8,24,41]);c1=np.array([40,82,114])
 rgb=(c0+(c1-c0)*glow[...,None]).astype('uint8');bg=Image.fromarray(rgb).convert('RGBA');bg.alpha_composite(layer,(x0,y0))
 f=[face[0]*scale+x0,face[1]*scale+y0,face[2]*scale+x0,face[3]*scale+y0]
 assert f[1]>20 and f[3]<height-12,(spec,height,f)
 return bg.convert('RGB'),f

def text(im,words,y,spec,fill):
 name=spec['font'];font=ImageFont.truetype(str(SUP/name),125)
 while font.getlength(words)>980:font=ImageFont.truetype(str(SUP/name),font.size-1)
 d=ImageDraw.Draw(im);box=d.textbbox((0,0),words,font=font);x=(W-(box[2]-box[0]))//2
 d.text((x-box[0],y-box[1]),words,font=font,fill=fill)
 return [x,y,x+box[2]-box[0],y+box[3]-box[1]]

def build(k,platform):
 spec=DESIGNS[k];lo,hi=(240,1680) if platform=='instagram' else (0,H)
 band=290;span=hi-lo
 top_h=540 if spec['full'] else (580 if platform=='instagram' else 825)
 bottom_h=span-top_h-band
 first,ff=(dan_panel if spec['reverse'] else mike_panel)(spec,top_h,platform)
 second,sf=(mike_panel if spec['reverse'] else dan_panel)(spec,bottom_h,platform,tail=H-hi)
 im=Image.new('RGB',(W,H),'#090C10');im.paste(first,(0,lo));by=lo+top_h;sy=by+band;im.paste(second,(0,sy))
 if lo:im.paste(first.crop((0,0,W,35)).resize((W,lo)).filter(ImageFilter.GaussianBlur(22)),(0,0))
 draw=ImageDraw.Draw(im);bg=spec['accent'] if k=='C' else ('#071B2C' if k=='D' else '#090A0C')
 draw.rectangle((0,by,W,sy),fill=bg)
 draw.rectangle((0,by,W,by+9),fill=spec['accent']);draw.rectangle((0,sy-9,W,sy),fill=spec['accent'])
 colors=['#111111','#111111'] if k=='C' else [spec['accent'],'#FFFDF6']
 boxes=[text(im,line,by+40+i*128,spec,colors[i]) for i,line in enumerate(COPY)]
 faces=[[ff[0],ff[1]+lo,ff[2],ff[3]+lo],[sf[0],sf[1]+sy,sf[2],sf[3]+sy]]
 for b in boxes:
  assert 25<=b[0]<b[2]<=W-25 and lo+20<=b[1]<b[3]<=hi-20
  for f in faces:assert b[2]<f[0]-20 or b[0]>f[2]+20 or b[3]<f[1]-20 or b[1]>f[3]+20,(k,b,f)
 dest=OUT/platform/f'{k}.jpg';dest.parent.mkdir(exist_ok=True);im.save(dest,quality=94,subsampling=0)
 assert dest.stat().st_size<2_000_000
 actual_faces=detector(dest);assert len(actual_faces)==2,(k,platform,actual_faces)
 public=PUBLIC/f'r2-{k}-{platform}.jpg';shutil.copy2(dest,public)
 if platform=='instagram':im.crop((0,240,W,1680)).resize((540,720),Image.Resampling.LANCZOS).save(PUBLIC/f'r2-{k}-grid.jpg',quality=94)
 return {'option':k,'platform':platform,'path':str(dest.relative_to(ROOT)),'sha256':sha(dest),'bytes':dest.stat().st_size,'text_boxes':boxes,'measured_head_boxes':faces,'detected_faces':actual_faces,'passed':True}

def review():
 old=PUBLIC/'index.html'
 if not (PUBLIC/'round1.html').exists():shutil.copy2(old,PUBLIC/'round1.html')
 font=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),25)
 sheet=Image.new('RGB',(1200,1140),'#101823');d=ImageDraw.Draw(sheet)
 for j,k in enumerate(DESIGNS):
  for n,pf in enumerate(['instagram','youtube']):
   x=j*300;y=n*570;d.text((x+10,y+12),f'{k} / {"Instagram" if n==0 else "YouTube"}',font=font,fill='white')
   im=Image.open(PUBLIC/f'r2-{k}-{pf}.jpg');im.thumbnail((280,500));sheet.paste(im,(x+10,y+55))
 sheet.save(PUBLIC/'reaction-choices.jpg',quality=95)
 h=['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dr Mike Reaction Cover Choices</title><style>body{background:#101823;color:#f7f8fa;font:18px/1.5 -apple-system,Arial;margin:0}main{max-width:1200px;margin:auto;padding:28px 20px}a{color:#82daff}section{padding:22px;margin:25px 0;background:#1b2738;border-radius:12px}.pair{display:grid;grid-template-columns:1fr 1fr .75fr;gap:18px}img{width:100%;display:block}figure{margin:0}nav a{display:inline-block;padding:8px 24px;background:#273d54;margin:4px;border-radius:8px;text-decoration:none}figcaption{font-size:15px;color:#c6d2df;margin-bottom:8px}h1{font-size:32px}@media(max-width:700px){.pair{grid-template-columns:1fr 1fr}.grid{grid-column:1/3;max-width:240px}}</style></head><body><main><h1>Dr. Mike + Your Reaction</h1><p>Four new covers based on the Hormozi reaction layout. Each pairs actual Dr. Mike video frames with you reacting, with both platform layouts and the Instagram profile crop.</p><p>Choose A, B, C or D in this chat. Your film is already approved. These covers still need your pick before uploads or scheduling.</p><nav>']
 for k in DESIGNS:h.append(f'<a href="#{k}">{k}</a>')
 h.append('</nav><a href="reaction-choices.jpg"><img src="reaction-choices.jpg" alt="Four reaction covers in both platform layouts"></a>')
 for k,spec in DESIGNS.items():
  h.append(f'<section id="{k}"><h2>{k}: {spec["label"]}</h2><div class="pair">')
  for pf,title in [('instagram','Instagram'),('youtube','YouTube Shorts'),('grid','Instagram Profile Crop')]:h.append(f'<figure class="{"grid" if pf=="grid" else ""}"><figcaption>{title}</figcaption><a href="r2-{k}-{pf}.jpg"><img loading="lazy" src="r2-{k}-{pf}.jpg" alt="{k} {title}"></a></figure>')
  h.append('</div></section>')
 h.append('<p>Reply with A, B, C or D. The earlier eight choices are retired.</p></main></body></html>');old.write_text(''.join(h))

def prepare_sources():
 import sys
 cache=Path('/Volumes/Expansion/_edit_work/DS-37/round2')
 sys.path.insert(0,str(cache/'recipe'))
 from grade import grade
 from r5_post import r5_clean
 sources=[]
 for i in sorted({int(s['dan']) for s in DESIGNS.values()}):
  p=cache/'key/c2_O'/f'f{i:04d}.npy';fp,a=r5_clean(np.load(p))
  rgb=grade(np.clip(fp/np.maximum(a[...,None],.001),0,1),'warm')
  dest=SRC/f'dan-O{i:04d}.png';Image.fromarray((np.dstack([rgb,a])*255+.5).clip(0,255).astype('uint8')).save(dest)
  sources.append({'file':str(p),'sha256':sha(p),'key_frame':i,'roll_seconds':841.908+i*1001/30000,'output':str(dest),'output_sha256':sha(dest),'method':'existing R2 c2 key, r5_clean, approved Warm grade'})
 arr=np.load(cache/'src/clip661-695_24fps.npy',mmap_mode='r')
 for t in sorted({float(s['mike']) for s in DESIGNS.values()}):
  idx=round((t-661)*24);dest=SRC/f'mike-{t:.2f}s.png';Image.fromarray(arr[idx]).save(dest)
  sources.append({'file':str(cache/'src/clip661-695_24fps.npy'),'frame':idx,'source_seconds':t,'output':str(dest),'output_sha256':sha(dest),'method':'actual source video cache, no redraw'})
 (OUT/'source-provenance.json').write_text(json.dumps(sources,indent=2))

if __name__=='__main__':
 prepare_sources()
 rows=[build(k,p) for k in DESIGNS for p in ['instagram','youtube']]
 (OUT/'manifest.json').write_text(json.dumps({'job':'DS-37','round':2,'status':'awaiting-dan-pick','dan_words':BRIEF,'generation':'none, real source frames and reused approved key','copy':COPY,'designs':DESIGNS,'outputs':rows},indent=2))
 (BASE/'round1-rejection.json').write_text(json.dumps({'date':'2026-11-03','rejected_labels':[f'X{x}' for x in range(1,9)],'dan_words':BRIEF,'old_key_preserved':True},indent=2))
 review();print('Built 8 reaction covers; geometry, face clearance and JPEG checks passed.')
