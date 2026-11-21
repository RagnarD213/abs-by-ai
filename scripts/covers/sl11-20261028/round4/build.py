"""SL-11 R4: revise header 1 exactly as requested; retain every photograph pixel."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
P=Path(__file__).resolve().parents[4];B=P/'Short-form video content/covers/review/sl11-vacuum-20261028';R=B/'round4';R.mkdir(exist_ok=True)
F={'manrope':(str(Path.home()/'Library/Fonts/Manrope.ttf'),0),'condensed':('/System/Library/Fonts/Avenir Next Condensed.ttc',8),'medium':('/System/Library/Fonts/Avenir Next.ttc',5)}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(kind,size):
 p,i=F[kind];f=ImageFont.truetype(p,size,index=i)
 if kind=='manrope':f.set_variation_by_name('ExtraBold')
 return f
def bbox(text,f):return f.getbbox(text,anchor='lt')
def fit(text,kind,start,width):
 for n in range(start,20,-1):
  f=font(kind,n);b=bbox(text,f)
  if b[2]-b[0]<=width:return f
 raise ValueError(text)
def gradient(end):
 a=np.zeros((end,1080,3),np.uint8)
 for y in range(end):
  t=y/max(1,end-1);a[y,:,:]=[round(v*(1-t)+w*t) for v,w in zip((5,14,29),(14,37,59))]
 return Image.fromarray(a)
def ink(text,f,width=None):
 # Expand letter spacing only when vertical room limits the top line's font size.
 natural=sum(f.getlength(c) for c in text);tracking=max(0,((width or natural)-natural)/max(1,len(text)-1))
 layer=Image.new('L',(1500,500));d=ImageDraw.Draw(layer);x=8
 if not width:
  d.text((x,350),text,font=f,fill=255,anchor='ls')
 else:
  for c in text:
   d.text((x,350),c,font=f,fill=255,anchor='ls');x+=f.getlength(c)+tracking
 bb=layer.getbbox();out=layer.crop(bb)
 if width and out.width!=width:out=out.resize((width,out.height),Image.Resampling.LANCZOS)
 return out,tracking
m=json.loads((B/'round3/manifest.json').read_text());rows=[]
for old in [r for r in m['outputs'] if r['design']==1]:
 key=old['short'];plat=old['platform'];prior=Image.open(P/old['path']).convert('RGB');end=old['photo_start_y'];im=prior.copy();im.paste(gradient(end),(0,0));mask=Image.new('L',(1080,1920));text=old['text'];gap=12 if len(text)==2 else 8;topmin=250 if plat=='instagram' else 66;limit=end-10
 lower=[]
 for t in text[1:]:
  f=fit(t['text'],t['font'],round(t['size']*1.05),1020);layer,tracking=ink(t['text'],f);lower.append((t,f,layer,tracking))
 # Largest top font that fits available width and all lines' vertical room.
 for n in range(240,20,-1):
  f=font('manrope',n);bb=bbox(text[0]['text'],f)
  if bb[2]-bb[0]>1020:continue
  topink,tr=ink(text[0]['text'],f,1020)
  total=topink.height+sum(k[2].height for k in lower)+gap*(len(text)-1)
  if total<=limit-topmin:break
 else:raise ValueError('No header fit')
 y=topmin+(limit-topmin-total)//2;blocks=[]
 for i,(t,ff,layer,tracking) in enumerate([(text[0],f,topink,tr)]+lower):
  x=(1080-layer.width)//2;color='#D8C18B' if i==0 or i==len(text)-1 and len(text)==3 else '#FFFFFF'
  im.paste(Image.new('RGB',layer.size,color),(x,y),layer);mask.paste(layer,(x,y))
  blocks.append(dict(text=t['text'],font=t['font'],old_size=t['size'],size=ff.size,letter_spacing=round(tracking,3),bbox=[x,y,x+layer.width,y+layer.height]));y+=layer.height+gap
 assert np.array_equal(np.array(im)[end:],np.array(prior)[end:])
 assert blocks[0]['bbox'][2]-blocks[0]['bbox'][0]==1020
 assert all(25<=b['bbox'][0]<b['bbox'][2]<=1055 and (240 if plat=='instagram' else 50)<=b['bbox'][1]<b['bbox'][3]<=end-10 for b in blocks)
 p=R/key/plat/f'sl11-{key}-header-1-r4.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);j=p.with_suffix('.jpg');im.save(j,quality=94);mask.save(p.with_name(p.stem+'-text-mask.png'));assert j.stat().st_size<2_000_000
 gr=R/key/'grid';gr.mkdir(parents=True,exist_ok=True)
 if plat=='instagram':im.crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS).save(gr/'revised.jpg',quality=96)
 rows.append(dict(short=key,platform=plat,path=str(p.relative_to(P)),sha256=sha(p),jpeg_path=str(j.relative_to(P)),jpeg_sha256=sha(j),jpeg_bytes=j.stat().st_size,text=blocks,base_path=old['path'],base_sha256=old['sha256'],photo_start_y=end,all_photo_pixels_identical=True,horizontal_lines=False))
for key in 'abc':
 sh=Image.new('RGB',(1100,760),'#152435');d=ImageDraw.Draw(sh);lf=font('manrope',24)
 for i,plat in enumerate(['instagram','youtube']):
  row=next(x for x in rows if x['short']==key and x['platform']==plat);d.text((15+i*400,14),plat.title(),font=lf,fill='white');sh.paste(Image.open(P/row['path']).resize((378,672),Image.Resampling.LANCZOS),(10+i*400,65))
 d.text((815,14),'Profile Crop',font=lf,fill='white');sh.paste(Image.open(R/key/'grid/revised.jpg'),(815,65));sh.save(R/key/'revised-header-pair.jpg',quality=96)
(R/'manifest.json').write_text(json.dumps({'round':4,'status':'awaiting exact revised approval','scope':'Header 1 only. All horizontal rules removed; top line maximized to 1020 pixels wide within available height; lower lines approximately 5% larger. Photo pixels identical.','outputs':rows},indent=2));print('Built six revised layouts')
for x in rows:
 if x['platform']=='instagram':print(x['short'],[(t['text'],t['old_size'],t['size'],t['bbox']) for t in x['text']])
