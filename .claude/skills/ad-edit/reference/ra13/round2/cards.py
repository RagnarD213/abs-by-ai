"""One RA-13 layout adapter over the shared approved phone shell and Soft Blue photo card."""
from pathlib import Path
import sys,importlib.util,json
from PIL import Image,ImageDraw,ImageOps
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared'))
import softblue as B
sp=importlib.util.spec_from_file_location('approved_phone_shell',R/'.claude/skills/ad-edit/reference/ra14/s63_stills.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S)
GOAL=S.GOAL

def phone(t,screen,fmt,chip=None,room_for_label=False):
 wh=(1080,1920) if fmt=='9' else (1920,1080);im=B.field(t,*wh).convert('RGBA');body=S.phone_shell()
 scr=ImageOps.fit(screen,(518,982),Image.Resampling.LANCZOS,centering=(.5,0));mask=Image.new('L',(518,982));ImageDraw.Draw(mask).rounded_rectangle((0,-60,517,981),56,fill=255);body.paste(scr,(48,114),mask)
 if fmt=='9':
  if room_for_label:size=(550,1137);xy=(265,80);label_xy=(540,1240)
  else:size=(624,1290);xy=(228,72);label_xy=(540,1240)
 else:size=(366,756);xy=(777,40);label_xy=(960,815)
 body=body.resize(size,Image.Resampling.LANCZOS);im.alpha_composite(body,xy)
 box=None
 if chip:box=B.disclosure(im,chip,xy=label_xy,anchor='mt',size=20 if fmt=='16' else 22)
 return im.convert('RGB'),dict(phone=[*xy,xy[0]+size[0],xy[1]+size[1]],chip=box)

def goal(t,fmt):
 wh=(1080,1920) if fmt=='9' else (1920,1080);im=B.field(t,*wh).convert('RGBA')
 if fmt=='9':box=(127,100,825,1100);pos=(540,1240)
 else:box=(690,60,540,720);pos=(960,805)
 B.photo_card(im,GOAL,box,t,u=2);chip=B.disclosure(im,'AI-GENERATED',xy=pos,anchor='mt',size=22 if fmt=='9' else 20)
 return im.convert('RGB'),dict(photo=[box[0],box[1],box[0]+box[2],box[1]+box[3]],chip=chip)
