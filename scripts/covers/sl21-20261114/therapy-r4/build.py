from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops,ImageFont
import json,sys,numpy as np
w=Path(__file__).parent;old=w.parent/'therapy-r2'
root=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI')
sys.path.insert(0,str(root/'scripts/covers/sl08-20261025'))
import build as B
W,H=1080,1920
lines=[]
raw=Image.open(old/'sources/B.png').convert('RGBA')
raw=raw.resize((W,round(raw.height*W/raw.width)),Image.Resampling.LANCZOS)
_,rf=B.person_mask(raw)
central=min(rf,key=lambda a:abs((a[0]+a[2])/2-W/2))
a,b,c,d=central;hair=b-round(.62*(d-b))-20
wall=tuple(int(i) for i in np.array(raw.convert('RGB'))[:70].reshape(-1,3).mean(axis=0))
records=[];(w/'qa').mkdir(parents=True,exist_ok=True)
for platform in ['instagram','youtube']:
 ig=platform=='instagram';target=850 if ig else 700;shift=target-hair
 im=Image.new('RGBA',(W,H),wall+(255,));im.alpha_composite(raw,(0,shift))
 tm=Image.new('L',(W,H));bg=(8,24,42)
 # One union mask defines the entire bubble. The border is generated from
 # that silhouette, so no rectangular edge can cross the triangular tail.
 by=target-570;box=(350,by,1045,by+480)
 a,b,c,d=central;b+=shift;d+=shift
 tip=(c+34,round(b+.70*(d-b)))
 tail=[(765,box[3]-25),(825,box[3]-5),tip]
 bm=Image.new('L',(W,H));bd=ImageDraw.Draw(bm)
 bd.rounded_rectangle(box,radius=38,fill=255);bd.polygon(tail,fill=255)
 outline=bm.filter(ImageFilter.MaxFilter(7))
 shadow=outline.filter(ImageFilter.GaussianBlur(6))
 sh=Image.new('RGBA',(W,H),(0,0,0,0));sh.putalpha(shadow.point(lambda x:round(x*.30)));im.alpha_composite(sh,(0,5))
 im.paste(bg+(255,),(0,0,W,H),outline)
 im.paste((255,255,255,255),(0,0,W,H),bm)
 speech="Therapy makes you fat and depressed."
 copy_lines=['Therapy makes','you fat and','depressed.']
 sf=B.common(copy_lines,B.DIN,136,631)
 line_step=round(sf.size*1.02)
 text_height=sf.getbbox(copy_lines[-1],anchor='mt')[3]+line_step*2
 text_y=box[1]+(box[3]-box[1]-text_height)/2
 for i,t in enumerate(copy_lines):
  B.text(im,tm,((box[0]+box[2])/2,text_y+i*line_step),t,sf,(0,0,0),anchor='mt')
 _,faces=B.person_mask(im);assert len(faces)==3
 guards=[];ta=np.array(tm)>0;ba=np.array(outline)>0
 for a,b,c,d in faces:
  fh=d-b;guards.append([max(0,a-20),max(0,b-round(.62*fh)-20),min(W,c+20),min(H,d+20)])
 overlap=sum(int(ta[b:d,a:c].sum()) for a,b,c,d in guards)
 bubble_overlap=sum(int(ba[b:d,a:c].sum()) for a,b,c,d in guards)
 assert overlap==0 and bubble_overlap==0,(platform,overlap,bubble_overlap)
 bounds=tm.getbbox();assert bounds[0]>=20 and bounds[2]<=1060
 assert bounds[1]>=(240 if ig else 50) and bounds[3]<=(1620 if ig else 1840)
 previous=Image.open(w.parent/'therapy-r3/layouts'/platform/'X3-revised.png').convert('RGB')
 oldmask=Image.open(w.parent/'therapy-r3/qa'/f'{platform}-bubble.png').convert('L')
 ImageDraw.Draw(oldmask).rectangle((0,0,W,556 if ig else 400),fill=255)
 allowed=ImageChops.lighter(oldmask,bm).filter(ImageFilter.MaxFilter(121))
 changed=np.any(np.array(previous)!=np.array(im.convert('RGB')),axis=2)
 outside=int(np.logical_and(changed,np.array(allowed)==0).sum())
 assert outside==0,(platform,'changed outside bubble',outside)

 out=w/'layouts'/platform;out.mkdir(parents=True,exist_ok=True)
 p=out/'X3-revised.png';im.convert('RGB').save(p)
 if not ig:im.convert('RGB').save(p.with_suffix('.jpg'),quality=92);assert p.with_suffix('.jpg').stat().st_size<2_000_000
 tm.save(w/'qa'/f'{platform}-type.png');bm.save(w/'qa'/f'{platform}-bubble.png')
 records.append({'platform':platform,'path':str(p),'sha256':B.sha(p),'size':list(im.size),'selected':'therapy-r2 X3','previous_sha256':B.sha(w.parent/'therapy-r3/layouts'/platform/'X3-revised.png'),'source_sha256':B.sha(old/'sources/B.png'),'bubble_text':speech,'bubble_lines':len(copy_lines),'copy_lines':copy_lines,'bubble_text_rgb':[0,0,0],'bubble_box':box,'tail':tail,'bubble_font_size':sf.size,'one_continuous_silhouette':True,'face_hair_text_pixels':overlap,'face_hair_bubble_pixels':bubble_overlap,'changed_pixels_outside_bubble_and_removed_headline':outside,'headline_removed':True,'text_bounds':bounds,'faces':faces,'hair_guards':guards})
 print(platform,'PASS',flush=True)
(w/'layout-manifest-private.json').write_text(json.dumps(records,indent=2))
sheet=Image.new('RGB',(1080,1020),'#111b28');d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',26)
for i,platform in enumerate(['instagram','youtube']):
 d.text((i*540+16,10),'X3 Revised · '+platform.title(),font=font,fill='white')
 im=Image.open(w/'layouts'/platform/'X3-revised.png').resize((540,960),Image.Resampling.LANCZOS);sheet.paste(im,(i*540,60))
sheet.save(w/'X3-revised-both-layouts.jpg',quality=95)
