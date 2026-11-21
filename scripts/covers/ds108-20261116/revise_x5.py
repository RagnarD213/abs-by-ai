"""Build Dan's selected X5 revision in both layouts; preserve the film."""
from pathlib import Path
import hashlib,json,sys,uuid
from PIL import Image,ImageDraw,ImageFont,ImageOps

P=Path('/Volumes/Extreme/_edit_work/DS-108-setup')
Q=P/'cover-r2';Q.mkdir(exist_ok=True)
SRC=Path(sys.argv[1])
OUT=Q/'designed';OUT.mkdir(exist_ok=True)
FONT='/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
W,H=1080,1920

def save(im,path,**kwargs):
 tmp=path.with_name(path.stem+'.'+uuid.uuid4().hex+path.suffix)
 im.save(tmp,**kwargs);tmp.replace(path)

def text(im,words,y,size,color):
 d=ImageDraw.Draw(im)
 while size>20:
  font=ImageFont.truetype(FONT,size)
  if d.textlength(words,font=font)<=970:break
  size-=1
 box=d.textbbox((0,0),words,font=font);x=round((W-d.textlength(words,font=font))/2)
 xy=(x,round(y-box[1]));d.text(xy,words,font=font,fill=color)
 box=d.textbbox(xy,words,font=font)
 assert box[0]>=50 and box[2]<=1030
 return {'text':words,'box':list(box),'font_size':size}

rows=[]
for platform in ['Instagram','YouTube']:
 ig=platform=='Instagram';im=Image.new('RGB',(W,H),'#f5e6d1')
 photo=Image.open(SRC).convert('RGB');photo=photo.crop((0,round(photo.height*.12),photo.width,photo.height))
 top=480 if ig else 340
 if ig:
  fitted=ImageOps.contain(photo,(W,H-top),Image.Resampling.LANCZOS)
 else:
  fitted=ImageOps.fit(photo,(W,H-top),Image.Resampling.LANCZOS,centering=(.5,0))
 ImageDraw.Draw(im).rectangle((0,top,W,H),fill='#d0b486')
 im.paste(fitted,((W-fitted.width)//2,top))
 start=268 if ig else 108
 ImageDraw.Draw(im).line((76,start-23,1004,start-23),fill='#91652c',width=5)
 boxes=[text(im,'Use Smaller Plates',start,99,'#263328'),text(im,'To Lose Fat.',start+109,109,'#91652c')]
 assert min(b['box'][1] for b in boxes)>=(240 if ig else 90)
 assert max(b['box'][3] for b in boxes)<top-20
 dst=OUT/f'X5-R2-{platform}.png';save(im,dst)
 jpg=dst.with_suffix('.jpg');save(im,jpg,quality=94,subsampling=0)
 assert jpg.stat().st_size<2_000_000
 grid=OUT/f'X5-R2-{platform}-grid.jpg';save(im.crop((0,240,W,1680)),grid,quality=94)
 rows.append({'platform':platform,'png':str(dst),'png_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'jpg':str(jpg),'jpg_sha256':hashlib.sha256(jpg.read_bytes()).hexdigest(),'bytes':jpg.stat().st_size,'text':boxes,'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest()})
temp=Q/'layout-manifest.tmp';temp.write_text(json.dumps(rows,indent=2)+'\n');temp.replace(Q/'layout-manifest.json')
sheet=Image.new('RGB',(1160,1170),'#102335');d=ImageDraw.Draw(sheet)
for i,platform in enumerate(['Instagram','YouTube']):
 im=Image.open(OUT/f'X5-R2-{platform}.jpg');im.thumbnail((540,960));sheet.paste(im,(i*580+10,45));d.text((i*580+15,15),platform,fill='white')
save(sheet,OUT/'X5-R2-pair.jpg',quality=95)
print('Built selected X5 R2 pair and manifest.')
