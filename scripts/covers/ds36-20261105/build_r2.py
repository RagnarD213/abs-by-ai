#!/usr/bin/env python3
"""Four explicitly requested heavier-Dan mirror covers, paired platform layouts."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib, json, os, subprocess, tempfile
import numpy as np
ROOT=Path(os.environ.get('ABS_PROJECT_ROOT') or Path(__file__).resolve().parents[3])
BASE=ROOT/'Short-form video content/covers/review/ds36-20261105'
OUT=BASE/'round2'; SRC=OUT/'sources'; W,H=1080,1920
PM=Path.home()/'.cache/absbyai/personmask/personmask'
SUP=Path('/System/Library/Fonts/Supplemental')
FONTS={'1':(SUP/'DIN Condensed Bold.ttf',0),'2':(SUP/'Impact.ttf',0),'3':(Path('/System/Library/Fonts/Avenir Next Condensed.ttc'),8),'4':(SUP/'Georgia Bold.ttf',0)}
LABELS={k:f'M{k}' for k in '1234'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ft(k,n):
 p,i=FONTS[k];return ImageFont.truetype(str(p),n,index=i)
def fit(k,text,size,width):
 for n in range(size,40,-1):
  f=ft(k,n);b=f.getbbox(text,anchor='mt')
  if b[2]-b[0]<=width:return f
 raise ValueError(text)
def segment(im):
 with tempfile.TemporaryDirectory(prefix='ds36-r2-') as t:
  a=Path(t)/'pic.png';b=Path(t)/'mask.png';im.convert('RGB').save(a)
  r=subprocess.run([str(PM),str(a),str(b)],capture_output=True,text=True,check=True)
  return np.array(Image.open(b))>127,json.loads(r.stdout)['faces']
def title_spec(k,pf):
 top=280 if pf=='instagram' else 90
 if k=='1':return ['Why Fat Shaming','Is Good'],[180,190],[top,top+155],['#111318','#B51E19'],None
 if k=='2':return ['Why Fat','Shaming','Is Good'],[142,160,142],[top,top+132,top+278],['white','white','#4BDDE8'],None
 if k=='3':
  lines=['Why Fat','Shaming','Is Good'];sizes=([130,145,138] if pf=='instagram' else [170,190,180]);fonts=[fit(k,x,n,960) for x,n in zip(lines,sizes)];heights=[f.getbbox(x,anchor='mt',stroke_width=3)[3] for x,f in zip(lines,fonts)];y=(1660 if pf=='instagram' else 1800)-sum(heights)-28;ys=[]
  for h in heights:ys.append(y);y+=h+14
  return lines,sizes,ys,['white','#ED4545','white'],ys[0]-24
 return ['Why Fat Shaming','Is Good'],[116,132],[top,top+148],['#181C22','#875D2A'],None

def build_one(k,pf):
 raw=Image.open(SRC/f'{k}.png').convert('RGB');im=ImageOps.fit(raw,(W,H),Image.Resampling.LANCZOS).convert('RGBA')
 person,faces=segment(im);ys=np.where(person.any(axis=1))[0];assert len(ys),k
 if pf=='youtube' and k!='3':
  z=1.18;target_top=550 if k=='2' else 465;cw=W/z;ch=H/z;offset=min(H-ch,max(0,int(ys.min())-target_top/z));left=(W-cw)/2
  im=im.crop((round(left),round(offset),round(left+cw),round(offset+ch))).resize((W,H),Image.Resampling.LANCZOS)
  person,faces=segment(im);ys=np.where(person.any(axis=1))[0];assert len(ys),k
 lines,sizes,positions,colors,picture_bottom=title_spec(k,pf)
 target=(260 if pf=='instagram' else 100) if k=='3' else ((740 if pf=='instagram' else 550) if k=='2' else (650 if pf=='instagram' else 465))
 delta=(target-int(ys.min())) if k=='3' else max(0,target-int(ys.min()))
 color=tuple(np.array(im.convert('RGB'))[:40].reshape(-1,3).mean(axis=0).astype(int));placed=Image.new('RGBA',(W,H),color+(255,))
 src_y=max(0,-delta);dest_y=max(0,delta);bottom=H if picture_bottom is None else picture_bottom
 height=min(H-src_y,bottom-dest_y);assert height>0
 placed.alpha_composite(im.crop((0,src_y,W,src_y+height)),(0,dest_y));im=placed
 if k=='3':ImageDraw.Draw(im).rectangle((0,picture_bottom,W,H),fill='#080B10')
 if k=='2':
  overlay=np.zeros((H,W,4),np.uint8);overlay[:,:,:3]=[5,14,28];end=min(target-30,900)
  for y in range(end):overlay[y,:,3]=round(235*(1 if y<end-130 else (end-y)/130))
  im.alpha_composite(Image.fromarray(overlay))
 if k=='4':
  d=ImageDraw.Draw(im);d.rectangle((0,0,W,(610 if pf=='instagram' else 425)),fill='#F2E6D1');d.line((70,250 if pf=='instagram' else 60,W-70,250 if pf=='instagram' else 60),fill='#A47C40',width=4)
 picture=im.convert('RGB');mask=Image.new('L',(W,H));draw=ImageDraw.Draw(im);md=ImageDraw.Draw(mask);bounds=[]
 if k=='1':draw.rectangle((0,240 if pf=='instagram' else 50,W,610 if pf=='instagram' else 420),fill='#FFD423')
 if k=='2':draw.rectangle((42,positions[0]-8,54,positions[-1]+125),fill='#D52E36')
 for i,(line,size,y,c) in enumerate(zip(lines,sizes,positions,colors)):
  f=fit(k,line,size,938 if k=='2' else 960);stroke=3 if k=='3' else 0;b=f.getbbox(line,anchor='lt' if k=='2' else 'mt',stroke_width=stroke);x=86 if k=='2' else W//2;anchor='lt' if k=='2' else 'mt'
  draw.text((x,y),line,font=f,anchor=anchor,fill=c,stroke_width=stroke,stroke_fill='#080B10');md.text((x,y),line,font=f,anchor=anchor,fill=255,stroke_width=stroke);bounds.append([x+b[0],y+b[1],x+b[2],y+b[3]])
 if k=='4':draw.line((70,positions[-1]+130,W-70,positions[-1]+130),fill='#A47C40',width=4)
 target_dir=OUT/pf;target_dir.mkdir(parents=True,exist_ok=True);p=target_dir/f'{LABELS[k]}.png';im.convert('RGB').save(p);picture.save(target_dir/f'{LABELS[k]}.picture.png');mask.save(target_dir/f'{LABELS[k]}.text-mask.png')
 if pf=='youtube':im.convert('RGB').save(p.with_suffix('.jpg'),quality=92);assert p.with_suffix('.jpg').stat().st_size<2000000
 person,faces=segment(picture);text=np.array(mask)>0;collisions=[];face_proofs=[]
 for face in faces:
  x0,y0,x1,y1=map(int,face);fw=x1-x0;fh=y1-y0;b=[max(0,x0-fw//4),max(0,y0-fh//2),min(W,x1+fw//4),min(H,y1+fh//5)];a,c,d,e=b;collisions.append(int(text[c:e,a:d].sum()));face_proofs.append((LABELS[k],pf,im.convert('RGB').crop(b)))
 safe=all(28<=b[0]<b[2]<=W-28 and (240 if pf=='instagram' else 50)<=b[1]<b[3]<=(1680 if pf=='instagram' else 1850) for b in bounds)
 row={'label':LABELS[k],'platform':pf,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'size':[W,H],'mode':'RGB','text_bounds':bounds,'text_bounds_safe':safe,'faces':faces,'expanded_face_hair_collisions':collisions,'picture_shift':delta,'source_sha256':sha(SRC/f'{k}.png'),'passed':safe and 1<=len(faces)<=2 and not any(collisions)}
 if pf=='youtube':row.update(jpeg_path=str(p.with_suffix('.jpg').relative_to(ROOT)),jpeg_sha256=sha(p.with_suffix('.jpg')),jpeg_bytes=p.with_suffix('.jpg').stat().st_size)
 return row,face_proofs

def main():
 rows=[];proofs=[]
 for k in '1234':
  for pf in ['instagram','youtube']:
   row,faces=build_one(k,pf);rows.append(row);proofs+=faces
 (OUT/'cover-checks.json').write_text(json.dumps({'all_passed':all(x['passed'] for x in rows),'checks':rows,'visual_review_required':True},indent=2))
 sheet=Image.new('RGB',(240*len(proofs),310),'#203045');d=ImageDraw.Draw(sheet)
 for i,(label,pf,im) in enumerate(proofs):
  im=ImageOps.contain(im,(220,260));sheet.paste(im,(240*i+10,40));d.text((240*i+10,12),label+' / '+pf,fill='white')
 sheet.save(OUT/'face-check.jpg',quality=95)
 print('Built',len(rows),'paired covers;',sum(x['passed'] for x in rows),'automatic passes',flush=True)
 if not all(x['passed'] for x in rows):raise SystemExit('A cover needs correction before review')
if __name__=='__main__':main()
