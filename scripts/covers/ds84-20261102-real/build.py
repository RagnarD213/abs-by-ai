#!/usr/bin/env python3
"""Four real screenshot covers; paired layouts; source and photo-retouch comparison."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'Short-form video content/covers/review/ds84-hamstring-curls-20261102-real'
SRC=OUT/'sources'; W,H=1080,1920
SUP=Path('/System/Library/Fonts/Supplemental')
FONTS={'condensed':SUP/'DIN Condensed Bold.ttf','impact':SUP/'Impact.ttf','bold':Path('/System/Library/Fonts/Avenir Next Condensed.ttc'),'sans':SUP/'Arial Bold.ttf'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(style,n):return ImageFont.truetype(str(FONTS[style]),n,index=8 if style=='bold' else 0)
def title(im,tm,lines,ys,style,sizes,colors,width=960,align='center',x=540):
 boxes=[];d=ImageDraw.Draw(im);md=ImageDraw.Draw(tm)
 for text,y,size,col in zip(lines,ys,sizes,colors):
  while font(style,size).getbbox(text)[2]-font(style,size).getbbox(text)[0]>width:size-=1
  f=font(style,size);a='mt' if align=='center' else 'lt';b=d.textbbox((x,y),text,font=f,anchor=a)
  d.text((x,y),text,font=f,anchor=a,fill=col);md.text((x,y),text,font=f,anchor=a,fill=255);boxes.append(list(b))
 return boxes

def photo(im,key,box,records,contain=True):
 p=SRC/(key+'-retouched.png');src=Image.open(p).convert('RGB');x0,y0,x1,y1=map(int,box);bw=x1-x0;bh=y1-y0
 scale=min(bw/src.width,bh/src.height) if contain else max(bw/src.width,bh/src.height)
 nw,nh=round(src.width*scale),round(src.height*scale);res=src.resize((nw,nh),Image.Resampling.LANCZOS)
 dx=(bw-nw)//2;dy=(bh-nh)//2
 if contain:im.paste(res,(x0+dx,y0+dy))
 else:im.paste(res.crop((-dx,-dy,-dx+bw,-dy+bh)),(x0,y0))
 # Manually checked, conservative native rectangle around full hair and face.
 face=[780,350,1120,745]
 f=[round(x0+dx+face[0]*scale),round(y0+dy+face[1]*scale),round(x0+dx+face[2]*scale),round(y0+dy+face[3]*scale)]
 records.append({'source':str(p.relative_to(ROOT)),'sha256':sha(p),'photo_box':list(box),'face_hair_box':f,'scale':scale,'contain':contain})

def build(k,platform):
 ig=platform=='instagram';top=240 if ig else 70;bottom=1680 if ig else 1850
 im=Image.new('RGB',(W,H),'#10141c');tm=Image.new('L',(W,H),0);d=ImageDraw.Draw(im);photos=[];bounds=[]
 if k=='1':
  im.paste('#f7f6f2',(0,0,W,H));d=ImageDraw.Draw(im)
  bounds+=title(im,tm,['How To Do','Hamstring Curls'],[top+48,top+182],'condensed',[154,166],['#152634','#152634'])
  d.rectangle((66,top+352,1014,top+365),fill='#d42a28')
  py=top+425;ph=bottom-py-14
  
  if ig:
   d.rectangle((40,py-12,1040,bottom+4),fill='#152634');photo(im,'curled',(52,py,1028,bottom-8),photos)
  else:
   d.rectangle((12,518,1068,1812),fill='#152634');photo(im,'curled',(24,530,1056,1800),photos,contain=False)
 elif k=='2':
  im.paste('#ffd72e',(0,0,W,H));d=ImageDraw.Draw(im)
  ph_end=bottom-400;photo(im,'curled',(0,top,W,ph_end),photos)
  d.polygon([(0,ph_end-38),(W,ph_end),(W,bottom+60),(0,bottom+60)],fill='#ffd72e')
  bounds+=title(im,tm,['How To Do','Hamstring','Curls'],[ph_end+22,ph_end+132,ph_end+240],'impact',[125,148,156],['#101319']*3,width=976)
 elif k=='3':
  # Two full real positions offset diagonally; the central title avoids both heads.
  span=bottom-top
  size=650 if ig else 760;h=round(size*1288/1221)
  b1=(30,top+22,30+size,top+22+h);b2=(W-size-30,bottom-h-8,W-30,bottom-8)
  d.rectangle((b1[0]-8,b1[1]-8,b1[2]+8,b1[3]+8),fill='#d9f5fa');photo(im,'extended',b1,photos)
  d.rectangle((b2[0]-8,b2[1]-8,b2[2]+8,b2[3]+8),fill='#45dce9');photo(im,'curled',b2,photos)
  yy=top+round(span*.405)
  d.polygon([(0,yy-30),(W,yy+5),(W,yy+280),(0,yy+245)],fill='#082a39')
  bounds+=title(im,tm,['How To Do','Hamstring Curls'],[yy+20,yy+145],'bold',[148,144],['white','#4ce2ee'],width=1000)
 elif k=='4':
  photo(im,'extended',(0,650 if ig else 550,W,bottom),photos,contain=False)
  # A broad top cap, with the real action filling the lower frame.
  d=ImageDraw.Draw(im);d.polygon([(0,0),(W,0),(W,top+410),(0,top+330)],fill='#17171a')
  bounds+=title(im,tm,['How To Do','Hamstring','Curls'],[top+25,top+122,top+264],'bold',[108,160,168],['#f5f0e7','#f5f0e7','#f3493e'],width=920,align='left',x=68)
  d.rectangle((0,top+445,16,bottom),fill='#e6352a')
 else:raise ValueError(k)
 folder=OUT/platform;folder.mkdir(exist_ok=True);p=folder/f'ds84-real-design-{k}.png';im.save(p);tm.save(folder/f'ds84-real-design-{k}.text-mask.png')
 collisions=[]
 for q in photos:
  a,b,c,e=q['face_hair_box'];a,b,c,e=max(0,a-10),max(0,b-10),min(W,c+10),min(H,e+10)
  collisions.append(tm.crop((a,b,c,e)).getbbox() is not None)
 assert all(20<=b[0]<b[2]<=1060 and top<=b[1]<b[3]<=bottom for b in bounds),(k,platform,bounds)
 row={'design':k,'platform':platform,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'text_bounds':bounds,'photos':photos,'text_hits_face_hair':collisions,'source_type':'real video screenshot with photographic touch-up','review_status':'awaiting Dan pick'}
 if not ig:
  jp=p.with_suffix('.jpg');im.save(jp,quality=94,subsampling=0);assert jp.stat().st_size<2_000_000
  row.update({'jpeg_path':str(jp.relative_to(ROOT)),'jpeg_sha256':sha(jp),'jpeg_bytes':jp.stat().st_size})
 else:
  gr=OUT/'grid';gr.mkdir(exist_ok=True);im.crop((0,240,1080,1680)).resize((360,480),Image.Resampling.LANCZOS).save(gr/f'{k}.jpg',quality=95)
 ph=OUT/'phone'/platform;ph.mkdir(parents=True,exist_ok=True);im.resize((270,480),Image.Resampling.LANCZOS).save(ph/f'{k}.jpg',quality=95)
 return row

def main():
 rows=[build(k,p) for p in ['instagram','youtube'] for k in '1234']
 sh=Image.new('RGB',(4*360,2*680),'#111923');d=ImageDraw.Draw(sh)
 for row in rows:
  i=int(row['design'])-1;j=0 if row['platform']=='instagram' else 1;im=Image.open(ROOT/row['path']).resize((342,608),Image.Resampling.LANCZOS);x=i*360+9;y=j*680+46
  sh.paste(im,(x,y));d.text((x,y-34),row['design']+' / '+row['platform'].title(),font=font('sans',22),fill='white')
 sh.save(OUT/'four-cover-choices.jpg',quality=95)
 g=Image.new('RGB',(4*380,540),'#111923');d=ImageDraw.Draw(g)
 for i,k in enumerate('1234'):g.paste(Image.open(OUT/'grid'/f'{k}.jpg'),(i*380+10,45));d.text((i*380+12,8),'Design '+k,font=font('sans',23),fill='white')
 g.save(OUT/'profile-grid-choices.jpg',quality=95)
 comp=Image.new('RGB',(4*400,480),'#111923');d=ImageDraw.Draw(comp)
 for i,(name,label) in enumerate([('curled-original','Original: curled'),('curled-retouched','Touched up: curled'),('extended-original','Original: extended'),('extended-retouched','Touched up: extended')]):
  pic=Image.open(SRC/(name+'.png'));pic.thumbnail((390,420));comp.paste(pic,(i*400+(400-pic.width)//2,45));d.text((i*400+10,8),label,font=font('sans',20),fill='white')
 comp.save(OUT/'source-comparison.jpg',quality=95)
 manifest={'job':'DS-84','date':'2026-11-02','round':'Cover revision 2','status':'awaiting Dan pick 1-4','master_sha256':'de0e83f5e69bd000d83beb1f22ed0593510b670fe5db2bfe85e5983bca73d0c9','outputs':rows,'retouch_prompts':['scripts/covers/ds84-20261102-real/curled-prompt.txt','scripts/covers/ds84-20261102-real/extended-prompt.txt'],'source_frames':json.loads((SRC/'source-frames.json').read_text()),'note':'Real photographic sources, touched up with Codex subscription. Original frames shown for comparison. No pick, upload, or schedule.'}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps([(r['design'],r['platform'],r['text_hits_face_hair']) for r in rows]))
if __name__=='__main__':main()
