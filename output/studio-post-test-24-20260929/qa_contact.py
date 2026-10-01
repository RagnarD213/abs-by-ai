from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parent
posts=json.loads((R/'posts.json').read_text())
for st in range(1,9):
 out=Image.new('RGB',(1080,485),'white');d=ImageDraw.Draw(out)
 for j,v in enumerate('ABC'):
  im=Image.open(R/'images'/f'S{st:02}-{v}-01.jpg');im.thumbnail((360,450));out.paste(im,(j*360,35));d.text((j*360+10,8),f'S{st:02}-{v}',fill='black',font_size=20)
 out.save(R/'qa'/f'style-{st:02}.jpg')
for st in [7,8]:
 for v in 'ABC':
  out=Image.new('RGB',(1800,485),'white');d=ImageDraw.Draw(out)
  for j in range(5):
   im=Image.open(R/'images'/f'S{st:02}-{v}-{j+1:02}.jpg');im.thumbnail((360,450));out.paste(im,(j*360,35));d.text((j*360+10,8),f'S{st:02}-{v} / {j+1}',fill='black',font_size=20)
  out.save(R/'qa'/f'carousel-{st:02}-{v}.jpg')
out=Image.new('RGB',(1440,3104),'#f6f4ed');d=ImageDraw.Draw(out)
d.text((25,20),'DAN ROSE / 24 POSTS / REVIEW BATCH',fill='#10243c',font_size=38)
for i,p in enumerate(posts):
 x=(i%4)*360;y=80+(i//4)*504
 im=Image.open(R/'images'/f'{p["id"]}-01.jpg');im.thumbnail((344,430));out.paste(im,(x+8,y));d.text((x+12,y+440),f'{p["number"]:02} / {p["id"]} / '+('5 slides' if p['slides']==5 else '1 image'),fill='#10243c',font_size=20)
out.save(R/'overview.jpg',quality=93)
# Full-width bottom strips allow both hips to be inspected for the three tight crops.
ims=[]
for id in ['S01-C','S06-C','S08-C']:
 im=Image.open(R/'images'/f'{id}-01.jpg');im=im.crop((0,1050,1080,1350));ims.append((id,im))
out=Image.new('RGB',(1080,990),'white');d=ImageDraw.Draw(out)
for j,(id,im) in enumerate(ims):d.text((15,j*330+5),id,fill='black',font_size=22);out.paste(im,(0,j*330+30))
out.save(R/'qa/waistband-check.jpg',quality=95)
