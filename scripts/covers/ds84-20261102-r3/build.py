#!/usr/bin/env python3
"""Four richer design-1 variations. Selected photo patches stay pixel-identical."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np,json,hashlib
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'Short-form video content/covers/review/ds84-hamstring-curls-20261102-real'
OUT=ROOT/'Short-form video content/covers/review/ds84-hamstring-curls-20261102-r3'
W,H=1080,1920;SUP=Path('/System/Library/Fonts/Supplemental')
FONT={'impact':SUP/'Impact.ttf','din':SUP/'DIN Condensed Bold.ttf','heavy':Path('/System/Library/Fonts/Avenir Next Condensed.ttc'),'arial':SUP/'Arial Bold.ttf'}
STYLES={
 'A':{'name':'Midnight And Ice','bg0':'#143750','bg1':'#050f20','accent':'#59d9f2','color1':'#f7f8fa','color2':'#67e4f4','font':'impact'},
 'B':{'name':'Racing Red And Ivory','bg0':'#faf4e8','bg1':'#dfd6c6','accent':'#d7272d','color1':'#fff8eb','color2':'#fff8eb','font':'heavy'},
 'C':{'name':'Charcoal And Gold','bg0':'#28292a','bg1':'#0c1013','accent':'#c9a96a','color1':'#f9f2e5','color2':'#e7c57e','font':'din'},
 'D':{'name':'Electric Lime And Graphite','bg0':'#252c30','bg1':'#080f14','accent':'#d4f534','color1':'#102026','color2':'#102026','font':'impact'},
}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(style,n):return ImageFont.truetype(str(FONT[style]),n,index=8 if style=='heavy' else 0)
def rgb(h):return np.array(tuple(bytes.fromhex(h.lstrip('#'))),dtype=np.float32)
def gradient(a,b):
 t=np.linspace(0,1,H)[:,None,None];row=rgb(a)[None,None,:]*(1-t)+rgb(b)[None,None,:]*t
 return Image.fromarray(np.repeat(row,W,axis=1).astype('uint8'),'RGB')
def text(im,mask,s,y,style,size,color,width=980):
 while f(style,size).getbbox(s)[2]-f(style,size).getbbox(s)[0]>width:size-=1
 ft=f(style,size);d=ImageDraw.Draw(im);md=ImageDraw.Draw(mask);xy=(540,y);box=d.textbbox(xy,s,font=ft,anchor='mt')
 d.text(xy,s,font=ft,anchor='mt',fill=color);md.text(xy,s,font=ft,anchor='mt',fill=255);return list(box)
def build(k,platform):
 st=STYLES[k];ig=platform=='instagram';top=240 if ig else 70
 im=gradient(st['bg0'],st['bg1']);d=ImageDraw.Draw(im);tm=Image.new('L',(W,H),0)
 box=(52,665,1028,1672) if ig else (24,530,1056,1800)
 x0,y0,x1,y1=box
 if k=='A':
  d.polygon([(0,0),(W,0),(W,top+240),(0,top+520)],fill='#15364a')
  for off in range(-400,1400,110):d.line((off,0,off-500,top+450),fill='#214758',width=2)
  d.rectangle((48,top+386,1032,top+398),fill=st['accent'])
  # Deliberate offset border, with a thin bright inner rule.
  d.rectangle((x0-14,y0-14,x1+14,y1+14),fill='#3c7c91')
  d.rectangle((x0-7,y0-7,x1+7,y1+7),fill='#95e4ed')
 elif k=='B':
  d.polygon([(0,0),(W,0),(W,top+370),(0,top+425)],fill='#b62129')
  d.polygon([(0,0),(W,0),(W,top+100),(0,top+230)],fill='#ca2630')
  d.rectangle((55,top+445,1025,top+456),fill='#152730')
  d.rectangle((x0-16,y0-16,x1+16,y1+16),fill='#162c34')
  for xx,yy,sx,sy in [(x0-22,y0-22,1,1),(x1+22,y1+22,-1,-1)]:
   d.line((xx,yy,xx+155*sx,yy),fill='#d62b31',width=16);d.line((xx,yy,xx,yy+140*sy),fill='#d62b31',width=16)
 elif k=='C':
  for x in range(0,W,60):d.line((x,0,x,H),fill='#2b2e30',width=1)
  d.rectangle((36,top-8,1044,top+414),outline='#6c5d3e',width=2)
  d.line((72,top+400,1008,top+400),fill='#d7bb7e',width=6)
  d.rectangle((x0-16,y0-16,x1+16,y1+16),fill='#82704d')
  d.rectangle((x0-10,y0-10,x1+10,y1+10),fill='#edcf91')
  d.rectangle((x0-5,y0-5,x1+5,y1+5),fill='#070c10')
 elif k=='D':
  d.polygon([(0,top-25),(W,top-25),(W,top+360),(0,top+423)],fill=st['accent'])
  d.polygon([(0,top+415),(W,top+352),(W,top+380),(0,top+445)],fill='#788b2b')
  d.rectangle((x0-5,y0-5,x1+15,y1+15),fill='#d4f534')
  d.rectangle((x0-15,y0-15,x1+5,y1+5),fill='#050c12')
  d.rectangle((x0-15,y0-15,x0-4,y0+175),fill='#d4f534')
 # Stronger type over the selected two-line header, never over the photo.
 ys=[top+41,top+205];sizes=[148,173]
 if k=='C':ys=[top+57,top+223];sizes=[155,180]
 bounds=[text(im,tm,s,y,st['font'],n,c) for s,y,n,c in zip(['How To Do','Hamstring Curls'],ys,sizes,[st['color1'],st['color2']])]
 # Paste EXACT pixels of Dan's chosen design, retaining its approved image/crop.
 ref=BASE/platform/'ds84-real-design-1.png';patch=Image.open(ref).convert('RGB').crop(box);im.paste(patch,box[:2]);assert np.array_equal(np.array(im.crop(box)),np.array(patch))
 assert all(25<=b[0]<b[2]<=1055 and top<=b[1]<b[3]<y0-10 for b in bounds),(k,platform,bounds)
 assert tm.crop(box).getbbox() is None
 p=OUT/platform/f'ds84-design1-{k}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
 row={'variation':k,'name':st['name'],'platform':platform,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'text_bounds':bounds,'selected_image_reference':str(ref.relative_to(ROOT)),'photo_box':list(box),'photo_patch_pixel_sha256':hashlib.sha256(patch.tobytes()).hexdigest(),'selected_photo_pixels_identical':True,'text_outside_photo':True}
 if platform=='youtube':
  jp=p.with_suffix('.jpg');im.save(jp,quality=94,subsampling=0);assert jp.stat().st_size<2_000_000;row.update(jpeg_path=str(jp.relative_to(ROOT)),jpeg_sha256=sha(jp),jpeg_bytes=jp.stat().st_size)
 else:
  gp=OUT/'grid'/f'{k}.jpg';gp.parent.mkdir(exist_ok=True);im.crop((0,240,1080,1680)).resize((360,480),Image.Resampling.LANCZOS).save(gp,quality=95)
 return row

def main():
 rows=[build(k,p) for p in ['instagram','youtube'] for k in STYLES]
 sheet=Image.new('RGB',(1440,1360),'#111923');d=ImageDraw.Draw(sheet)
 for row in rows:
  i='ABCD'.index(row['variation']);j=0 if row['platform']=='instagram' else 1;x=i*360+9;y=j*680+46
  sheet.paste(Image.open(ROOT/row['path']).resize((342,608),Image.Resampling.LANCZOS),(x,y));d.text((x,y-34),row['variation']+' / '+row['platform'].title(),font=f('arial',22),fill='white')
 sheet.save(OUT/'four-variations.jpg',quality=95)
 grid=Image.new('RGB',(1520,540),'#111923');d=ImageDraw.Draw(grid)
 for i,k in enumerate(STYLES):grid.paste(Image.open(OUT/'grid'/f'{k}.jpg'),(i*380+10,45));d.text((i*380+10,8),k+' / '+STYLES[k]['name'],font=f('arial',17),fill='white')
 grid.save(OUT/'profile-grid-variations.jpg',quality=95)
 m={'job':'DS-84','round':'Cover revision 3','date':'2026-11-02','status':'awaiting final variation pick A-D','base_selected':'Revision 2 Design 1, chosen for variation only, not installation approval','image_change':'None. Exact selected photo patch/crop preserved per platform, proven by pixel equality.','outputs':rows,'master_sha256':'de0e83f5e69bd000d83beb1f22ed0593510b670fe5db2bfe85e5983bca73d0c9'}
 (OUT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Four variations built in both layouts; selected photo patch equality verified on all eight PNGs.')
if __name__=='__main__':main()
