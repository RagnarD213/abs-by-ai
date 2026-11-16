from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,hashlib
W=Path('/Volumes/Extreme/_edit_work/DS-109');D=W/'setup/r3';V=D/'review';F='/System/Library/Fonts/Supplemental/Impact.ttf';TITLE="Hormozi: You're Not Hungry, You're Bored.";sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
bg=Image.open(W/'setup/r2/assets/hormozi-2.png').convert('RGB');src=D/'assets/dan-pointing-enhanced.png';dan=Image.open(src).convert('RGBA');bbox=dan.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox();dan=dan.crop(bbox)
oldsource=Image.open(W/'setup/r2/assets/dan-pointing.png').convert('RGBA').crop((140,330,990,1500));oldbox=oldsource.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox();oldwidth=(oldbox[2]-oldbox[0])*900/850;newwidth=round(oldwidth*.5);dan=dan.resize((newwidth,round(dan.height*newwidth/dan.width)),Image.Resampling.LANCZOS)
def font(text,size):
 while True:
  f=ImageFont.truetype(F,size);b=f.getbbox(text,anchor='lt')
  if b[2]-b[0]<=960:return f,b
  size-=1
rows=[]
for platform in ['instagram','youtube']:
 ig=platform=='instagram';im=Image.new('RGBA',(1080,1920),'#08283d');d=ImageDraw.Draw(im);yy=250 if ig else 90;boxes=[]
 for j,(txt,size)in enumerate(zip(['Hormozi:',"You're Not Hungry,","You're Bored."],[96,116,156])):
  f,b=font(txt,size);xx=(1080-(b[2]-b[0]))//2;d.text((xx,yy),txt,font=f,fill='#7be2ff'if j==2 else'#ffffff',anchor='lt');bb=d.textbbox((xx,yy),txt,font=f,anchor='lt');boxes.append(list(bb));yy=bb[3]+14
 photo_y=yy-14+36;texture=ImageOps.fit(bg.crop((1040,0,1310,1080)),(1080,1920-photo_y));im.paste(texture,(0,photo_y));pic=bg.crop((0,20,800,1080));pic=pic.resize((810,round(pic.height*810/pic.width)),Image.Resampling.LANCZOS);ImageDraw.Draw(im).rounded_rectangle((243,photo_y-7,1067,photo_y+pic.height+7),radius=22,fill='#7be2ff');im.paste(pic,(250,photo_y));ImageDraw.Draw(im).rectangle((0,photo_y+pic.height+8,1080,1920),fill='#08283d')
 foreground_y=1130 if ig else 1370;old=Image.open(W/'setup/r2/review/images'/f'R2-B-{platform}.png').convert('RGB');im.paste(old.crop((0,0,1080,photo_y-8)),(0,0));im.alpha_composite(dan,(12,foreground_y));assert im.convert('RGB').crop((0,0,1080,photo_y-8)).tobytes()==old.crop((0,0,1080,photo_y-8)).tobytes()
 p=V/'images'/f'R3-B-{platform}.png';im.convert('RGB').save(p);im.convert('RGB').save(p.with_suffix('.jpg'),quality=94,optimize=True);assert p.with_suffix('.jpg').stat().st_size<2000000
 rows.append({'platform':platform,'path':str(p),'sha256':sha(p),'jpeg_sha256':sha(p.with_suffix('.jpg')),'size':[1080,1920],'title':TITLE,'text_boxes':boxes,'photo_y':photo_y,'foreground_xy':[12,foreground_y],'foreground_size':list(dan.size),'old_visible_width':oldwidth,'new_visible_width':newwidth,'linear_scale_ratio':newwidth/oldwidth,'enhanced_source':str(src),'enhanced_source_sha256':sha(src),'enhanced_crop':list(bbox),'hormozi_source_sha256':sha(W/'setup/r2/assets/hormozi-2.png'),'header_pixels_identical_to_B':True,'hormozi_face_unobstructed':True})
m={'round':3,'label':'B revised','title':TITLE,'cover_approved':False,'design_selected':'B','count':1,'url':'http://127.0.0.1:9920/?round=3','film_sha256_unchanged':'ce7c496e037ae91d1a74495f120e1d4c214c629df05c7493d7de88280941ca54','layouts':rows};(D/'layout-manifest.json').write_text(json.dumps(m,indent=2));(V/'manifest.json').write_text(json.dumps(m,indent=2))
sheet=Image.new('RGB',(810,720),'#eef3f6');ds=ImageDraw.Draw(sheet)
for k,(platform,crop)in enumerate([('instagram',True),('youtube',False)]):
 p=Image.open(rows[k]['path']);p=p.crop((0,240,1080,1680))if crop else p;p.thumbnail((405,685));sheet.paste(p,(k*405,30));ds.text((k*405+12,8),'Revised B: '+platform,fill='#102c41')
sheet.save(D/'qa/B-revised-pair.jpg',quality=95);print('REVISED_B_BUILT',newwidth,'OLD_WIDTH',oldwidth,'RATIO',newwidth/oldwidth,flush=True)
