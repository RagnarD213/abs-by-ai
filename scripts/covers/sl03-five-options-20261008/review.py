#!/usr/bin/env python3
"""One review sheet with all 30 SL-03 cover choices (Instagram + YouTube layout each), plus a paired sheet per short with grid crops."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/sl03-covers-20261008'
F='/System/Library/Fonts/Supplemental/Arial Bold.ttf';font=lambda s:ImageFont.truetype(F,s)
m=json.loads((R/'manifest.json').read_text())['outputs']
get=lambda n,v,pl:Image.open(next(a['path'] for a in m if a['short']==n and a['variant']==v and a['platform']==pl))
kinds={'A':'A: Pool shoot photo','B':'B: Studio shoot photo','C':'C: Screenshot from the video','D':'D: Codex design 1','E':'E: Codex design 2'}
titles={1:'Break Your Fast With This',2:'The $20 Salad You Can Make For $4',3:'Keep Your Salads Fresh For 7 Days',4:'Stop Buying Salad Dressing',5:'Track A Week Of Meals From 1 Photo',6:'The One Line That Makes It Accurate'}
cw,ch=236,420;colw=2*cw+14+28;rowh=ch+86
im=Image.new('RGB',(5*colw+40,150+6*rowh),(18,23,31));d=ImageDraw.Draw(im)
d.text((24,16),'SL-03 DAILY SALAD: FIVE COVER CHOICES PER SHORT (30 total)',font=font(40),fill='white')
d.text((24,70),'Each choice shown twice: Instagram / TikTok / Facebook layout (left), YouTube layout (right). Tell me one letter for each short.',font=font(26),fill=(185,198,209))
for r,n in enumerate(range(1,7)):
 y=130+r*rowh;d.text((24,y),f'SHORT {n}: {titles[n]}',font=font(32),fill=(255,214,0))
 for c,v in enumerate('ABCDE'):
  x=24+c*colw;d.text((x,y+44),kinds[v],font=font(23),fill=(213,228,238))
  for j,pl in enumerate(['instagram','youtube']):im.paste(get(n,v,pl).resize((cw,ch),Image.Resampling.LANCZOS),(x+j*(cw+14),y+78))
im.save(R/'REVIEW_sl03_all-30-choices.jpg',quality=92)
for n in range(1,7):
 s=Image.new('RGB',(2870,1090),(18,23,31));d=ImageDraw.Draw(s);d.text((24,14),f'SHORT {n}: {titles[n]}. INSTAGRAM + YOUTUBE PER OPTION',font=font(36),fill='white')
 for i,v in enumerate('ABCDE'):
  x=24+i*568;d.text((x,66),kinds[v],font=font(25),fill='white')
  for j,pl in enumerate(['instagram','youtube']):
   xx=x+j*278;d.text((xx,107),'Instagram' if j==0 else 'YouTube',font=font(21),fill=(180,195,211));s.paste(get(n,v,pl).resize((270,480),Image.Resampling.LANCZOS),(xx,140))
   if j==0:s.paste(get(n,v,pl).crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS),(xx,686));d.text((xx,646),'Instagram grid crop',font=font(20),fill=(180,195,211))
 s.save(R/f'REVIEW_short{n}_paired.jpg',quality=92)
print('review built')
