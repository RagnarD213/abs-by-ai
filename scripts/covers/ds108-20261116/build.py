"""DS108 paired covers; adapts DS30 layout and preserves the approved film."""
from pathlib import Path
import hashlib,json,sys,uuid
import cv2
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageFilter

ROOT=Path(__file__).resolve().parents[3]
P=Path(sys.argv[1] if len(sys.argv)>1 else '/Volumes/Extreme/_edit_work/DS-108-setup')
OUT=P/'designed';OUT.mkdir(exist_ok=True)
W,H=1080,1920
FONT='/System/Library/Fonts/Supplemental/Impact.ttf'
SERIF='/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
SANS='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
styles={
 'a':{'bg':'#ffd51a','ink':'#111923','accent':'#b6271d','speaker':359,'side':'left','style':'top'},
 'b':{'bg':'#102d47','ink':'#ffffff','accent':'#72e6f4','style':'meal'},
 'c':{'bg':'#122c40','ink':'#ffffff','accent':'#f0ca72','speaker':377,'side':'right','style':'real'},
 'd':{'bg':'#111923','ink':'#ffffff','accent':'#7de7fa','speaker':359,'side':'left','style':'bottom'},
 'e':{'bg':'#361823','ink':'#fff6e6','accent':'#ffc873','speaker':377,'side':'right','style':'top'},
 'f':{'bg':'#f1eadb','ink':'#172b2d','accent':'#9d432e','speaker':359,'side':'full','style':'top'},
 'g':{'bg':'#f5e6d1','ink':'#263328','accent':'#91652c','style':'meal'},
 'h':{'bg':'#153746','ink':'#ffffff','accent':'#bdedff','speaker':377,'side':'left','style':'bottom'},
}

def save(im,path,**kwargs):
 path=Path(path);tmp=path.with_name(path.stem+'.'+uuid.uuid4().hex+path.suffix)
 im.save(tmp,**kwargs);tmp.replace(path)

def write_json(path,data):
 path=Path(path);tmp=path.with_name(path.name+'.'+uuid.uuid4().hex)
 tmp.write_text(json.dumps(data,indent=2)+'\n');tmp.replace(path)

def text(im,word,y,size,color,font=FONT,width=960):
 d=ImageDraw.Draw(im)
 while size>25:
  f=ImageFont.truetype(font,size)
  if d.textlength(word,font=f)<=width:break
  size-=1
 box=d.textbbox((0,0),word,font=f)
 x=round((W-d.textlength(word,font=f))/2);xy=(x,round(y-box[1]));d.text(xy,word,font=f,fill=color)
 box=d.textbbox(xy,word,font=f)
 assert box[0]>=45 and box[2]<=1035,(word,box)
 return {'text':word,'box':list(box),'font_size':size}

def keyed(path):
 im=Image.open(path).convert('RGB');a=np.asarray(im).astype(np.float32)
 r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
 excess=g-np.maximum(r,b)
 alpha=1-np.clip((excess-12)/65,0,1)
 # Keep dark hair/clothing and skin opaque; only chroma background is removed.
 alpha=np.where((g>60)&(g>np.maximum(r,b)*1.18),alpha,1)
 binary=(alpha>.15).astype(np.uint8)
 n,labels,stats,_=cv2.connectedComponentsWithStats(binary,8)
 keep=1+int(np.argmax(stats[1:,cv2.CC_STAT_AREA]))
 component=(labels==keep).astype(np.uint8)
 component=cv2.dilate(component,np.ones((3,3),np.uint8))
 alpha*=component
 # Remove chroma spill only along partial-alpha edges.
 edge=(alpha>0)&(alpha<.99)
 a[:,:,1]=np.where(edge,np.minimum(g,np.maximum(r,b)+12),g)
 rgba=np.dstack([a,np.round(alpha*255)]).clip(0,255).astype(np.uint8)
 out=Image.fromarray(rgba,'RGBA');box=out.getchannel('A').getbbox();assert box
 return out.crop(box)

def speaker(im,t,top,bottom):
 src=Image.open(P/'refs'/f'mike-{t}.jpg').convert('RGB')
 # Genuine camera pixels, source head near x640. Crop the surrounding stage.
 cropw=round(src.height*W/(bottom-top));cx=445 if t==377 else 640
 src=src.crop((cx-cropw//2,0,cx+(cropw-cropw//2),src.height))
 src=src.resize((W,bottom-top),Image.Resampling.LANCZOS)
 im.paste(src,(0,top))

def foreground(im,fg,side,bottom,kind):
 if kind=='real':
  # Original RGBA photograph, no generated person pixels or retouch.
  fg=fg.crop(fg.getbbox());fg=fg.crop((0,0,fg.width,round(fg.height*.70)))
 else:
  # Editorial waist/bust crop, hiding shorts. Cut side edges stay at canvas edges.
  frac={'d':.58,'e':.57,'a':.78,'f':.58,'h':.68}.get(kind,.65)
  fg=fg.crop((0,0,fg.width,round(fg.height*frac)))
 target_h=880 if bottom>1500 else 690
 if side=='full':
  width=W;height=round(fg.height*W/fg.width)
 else:
  height=target_h;width=round(fg.width*height/fg.height)
  if width>720:
   width=720;height=round(fg.height*width/fg.width)
 fg=fg.resize((width,height),Image.Resampling.LANCZOS)
 x=0 if side in ('left','full') else W-width
 y=bottom-height
 alpha=fg.getchannel('A')
 line=alpha.filter(ImageFilter.MaxFilter(9));white=Image.new('RGBA',fg.size,'white');white.putalpha(line)
 im.paste(white,(x,y),white);im.paste(fg,(x,y),fg)
 return [x,y,x+width,y+height]

records=[]
for k,cfg in styles.items():
 src=P/('google/'+('g2' if k=='g' else k)+'.jpg' if k in 'fgh' else 'plates/'+k+'.png')
 fg=None
 if k in 'adefh':fg=keyed(src);save(fg,P/'plates'/f'{k}-cutout.png')
 if k=='c':fg=Image.open(ROOT/'photos/finalized social media photos/_cutouts/studio-white-23_CUTOUT.png').convert('RGBA')
 for platform in ['Instagram','YouTube']:
  ig=platform=='Instagram';style=cfg['style'];im=Image.new('RGB',(W,H),cfg['bg']);boxes=[];person=None
  if style=='bottom':
   top=240 if ig else 96;end=1245 if ig else 1400
   speaker(im,cfg['speaker'],top,end)
   person=foreground(im,fg,cfg['side'],end,k)
   y=1290 if ig else 1450
   boxes.append(text(im,'Use Smaller',y,150,cfg['ink']))
   boxes.append(text(im,'Plates',y+162,166,cfg['accent']))
  elif style=='meal':
   top=420 if ig else 230
   source=Image.open(src).convert('RGB')
   # Keep actual plates, hands and hair in the Instagram profile crop.
   # Narrow solid side rails are intentional; no repeated blurred food behind it.
   crop=source.crop((0,round(source.height*(.21 if ig and k=='b' else .12)),source.width,source.height))
   if k=='b' or not ig:
    fitted=ImageOps.fit(crop,(W,H-top),Image.Resampling.LANCZOS,centering=(.5,0))
   else:
    fitted=ImageOps.contain(crop,(W,H-top),Image.Resampling.LANCZOS)
   ImageDraw.Draw(im).rectangle((0,top,W,H),fill='#d0b486' if k=='g' else '#e5e2dd')
   im.paste(fitted,((W-fitted.width)//2,top))
   d=ImageDraw.Draw(im);start=280 if ig else 108
   d.line((76,start-28,1004,start-28),fill=cfg['accent'],width=6)
   boxes.append(text(im,'Use Smaller Plates',start,130,cfg['ink'],SERIF if k=='g' else FONT))
  else:
   top=650 if ig else 480
   speaker(im,cfg['speaker'],top,H)
   person=foreground(im,fg,cfg['side'],H,'real' if k=='c' else k)
   start=280 if ig else 108
   if k=='c':ImageDraw.Draw(im).line((75,start-25,1005,start-25),fill=cfg['accent'],width=5)
   font=SERIF if k=='f' else FONT
   boxes.append(text(im,'Use Smaller',start,144,cfg['ink'],font))
   boxes.append(text(im,'Plates',start+170,175,cfg['accent'],font))
  assert min(x['box'][1] for x in boxes)>=(240 if ig else 90)
  assert max(x['box'][3] for x in boxes)<=(1620 if ig else 1850)
  f=OUT/f'{k}-{platform}.png';save(im,f)
  jpg=f.with_suffix('.jpg');save(im,jpg,quality=94,subsampling=0);assert jpg.stat().st_size<2_000_000
  save(im.crop((0,240,W,1680)).resize((270,360)),OUT/f'{k}-{platform}-grid.jpg',quality=94)
  records.append({'concept':k,'platform':platform,'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'jpg':str(jpg),'jpg_bytes':jpg.stat().st_size,'text':boxes,'person_box':person,'real_person_pixels_preserved':k=='c','source_plate':str(src) if k!='c' else 'original studio-white-23 RGBA','reaction_scene':k in 'adefh'})
write_json(P/'layout-manifest.json',records)
sheet=Image.new('RGB',(2160,1580),'#101b29');d=ImageDraw.Draw(sheet)
for i,k in enumerate(styles):
 for j,platform in enumerate(['Instagram','YouTube']):
  x=(i%4)*540+j*240;y=(i//4)*790+45
  im=Image.open(OUT/f'{k}-{platform}.png').resize((215,382));sheet.paste(im,(x,y));d.text((x,y-23),k+' '+platform,fill='white')
 sheet.paste(Image.open(OUT/f'{k}-Instagram-grid.jpg'),((i%4)*540,(i//4)*790+440))
save(sheet,P/'layout-sheet.jpg',quality=96)
print('Built 16 paired exports and actual Instagram grid crops; five reaction designs.')
