from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,hashlib
import numpy as np
B=Path(__file__).resolve().parent;OUT=B.parent/'option-3-text-variations';OUT.mkdir(exist_ok=True)
FONT='/System/Library/Fonts/Supplemental/Impact.ttf'
LABEL=Path.home()/'Library/Fonts/Manrope.ttf'
def font(s,label=False):
 f=ImageFont.truetype(str(LABEL) if label else FONT,int(s))
 if label:f.set_variation_by_name('ExtraBold')
 return f
VARIANTS={
'A':{'copy':'Why Most Guys Never Get Abs','horizontal':['WHY MOST','GUYS NEVER','GET ABS'],'vertical':['WHY MOST GUYS','NEVER GET ABS']},
'B':{'copy':'Stop Training Blind','horizontal':['STOP','TRAINING','BLIND'],'vertical':['STOP TRAINING','BLIND']},
'C':{'copy':'No Plan. No Abs.','horizontal':['NO PLAN.','NO ABS.'],'vertical':['NO PLAN.','NO ABS.']},
'D':{'copy':'Stop Guessing. Use AI.','horizontal':['STOP','GUESSING.','USE AI.'],'vertical':['STOP GUESSING.','USE AI.']}
}
def typeblock(c,rows,rect,color):
 x,y,w,h=rect;s=400
 while s>10:
  f=font(s);bs=[f.getbbox(t) for t in rows];ws=[b[2]-b[0] for b in bs];hs=[b[3]-b[1] for b in bs];gap=round(s*.12)
  if max(ws)<=w and sum(hs)+gap*(len(rows)-1)<=h:break
  s-=1
 yy=y+(h-sum(hs)-gap*(len(rows)-1))/2;d=ImageDraw.Draw(c);boxes=[]
 for t,b,ww,hh in zip(rows,bs,ws,hs):
  xx=x+(w-ww)/2 if c.height>c.width else x
  d.text((round(xx-b[0]),round(yy-b[1])),t,font=f,fill=color)
  boxes.append([round(xx),round(yy),round(xx+ww),round(yy+hh)]);yy+=hh+gap
 return boxes,s
asset=Image.open(B/'assets/option3.png').convert('RGB');source_hash=hashlib.sha256((B/'assets/option3.png').read_bytes()).hexdigest();checks=[]
for key,v in VARIANTS.items():
 for vertical in [False,True]:
  W,H=(1080,1920) if vertical else (1280,720)
  if vertical:
   band=round(H*.265);c=Image.new('RGB',(W,H),'#fff1cf');panel=ImageOps.fit(asset,(W,H-band),Image.Resampling.LANCZOS);c.paste(panel,(0,band));rect=(W*.05,H*.03,W*.90,band-H*.06);color='#06236d';rows=v['vertical']
  else:
   c=Image.new('RGB',(W,H),'#05216b');panel=ImageOps.fit(asset,(round(W*.51),H),Image.Resampling.LANCZOS);c.paste(panel,(round(W*.49),0));ImageDraw.Draw(c).line((W*.475,H*.08,W*.475,H*.92),fill='#99cfff',width=3);rect=(W*.045,H*.10,W*.39,H*.8);color='#fff1cf';rows=v['horizontal']
  before=np.array(c);boxes,size=typeblock(c,rows,rect,color);after=np.array(c)
  # Pixel check on the entire photographic region before JPEG export.
  photo_equal=bool(np.array_equal(before[band:,:,:],after[band:,:,:])) if vertical else bool(np.array_equal(before[:,round(W*.49):,:],after[:,round(W*.49):,:]))
  assert photo_equal
  aspect='9x16' if vertical else '16x9';name=f'{key}-{aspect}.jpg';c.save(OUT/name,quality=95,subsampling=0,optimize=True)
  checks.append({'variant':key,'copy':v['copy'],'format':aspect,'file':str((OUT/name).resolve()),'font':'Impact','font_size':size,'text_boxes':boxes,'photograph_pixels_unchanged_before_encoding':photo_equal,'bytes':(OUT/name).stat().st_size})
# One numbered sheet with both formats per text choice.
sheet=Image.new('RGB',(1680,2460),'#e9edf3');d=ImageDraw.Draw(sheet)
d.text((32,24),'Thumbnail 3: Bolder Text Options',font=font(40,True),fill='#142138')
d.text((32,78),'Same image, colors and layout. Only the headline and typography change.',font=font(22,True),fill='#526178')
for i,(key,v) in enumerate(VARIANTS.items()):
 y=122+i*576;d.rounded_rectangle((20,y,1660,y+558),radius=14,fill='white')
 d.text((36,y+14),f'{key}. {v["copy"]}',font=font(26,True),fill='#142138')
 h=Image.open(OUT/f'{key}-16x9.jpg');h.thumbnail((860,484));sheet.paste(h,(36,y+62))
 p=Image.open(OUT/f'{key}-9x16.jpg');p.thumbnail((272,484));sheet.paste(p,(960,y+62))
 d.text((1290,y+240),'16:9 + 9:16',font=font(25,True),fill='#526178')
sheet.save(OUT/'REVIEW-text-variations.jpg',quality=94)
record={'category':'AD','job':'RA-13','date':'2026-10-17','status':'Option 3 image and design selected; waiting for text pick A-D','dan_request':"Okay I like thumbnail 3 but I don't like the text. Make the text bolder and more attention-getting. Show me a few text variations while keeping the image and design the same",'source_image_sha256':source_hash,'additional_image_generation':0,'variants':VARIANTS,'checks':checks,'review_sheet':str((OUT/'REVIEW-text-variations.jpg').resolve()),'upload_or_ads_mutations':False}
(OUT/'text-variations.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'review_sheet':record['review_sheet'],'files':len(checks),'photo_unchanged':all(c['photograph_pixels_unchanged_before_encoding'] for c in checks),'all_under_2mb':all(c['bytes']<2000000 for c in checks)},indent=2))
