from pathlib import Path
import sys,json
from PIL import Image,ImageDraw,ImageOps
P=Path(__file__).parent;W=P.parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');OLD=W.parent/'round3'
sys.path.insert(0,str(P));import lib
F=W/'frames';O=W/'review';(O/'frames').mkdir(parents=True,exist_ok=True)
def still(S,which,t,title=None):
 base=Image.new('RGB',(1080,1920));title=title or Image.open(OLD/'review'/f'title-{S}.png').convert('RGB');base.paste(title,(0,0))
 pic=ImageOps.fit(Image.open(F/f'{S}01-{which}.png').convert('RGB'),(1080,1610),centering=(.5,.1));base.paste(pic,(0,310))
 lib.B.disclosure(base,'AI-GENERATED',(32,335),1.25,anchor='lt',size=23)
 for c in json.loads((OLD/f'build/{S}/cues.json').read_text()):
  if c['a']<=t<c['b']:lib.caption(base,c['lines'],1640 if S=='A' else 1500)
 draw=ImageDraw.Draw(base);font=lib.B.font(24);txt='Frame Preview: Motion Not Generated';box=draw.textbbox((0,0),txt,font=font);x=(1080-(box[2]-box[0]))//2
 draw.rounded_rectangle((x-14,1840,1080-x+14,1885),8,fill=(7,19,34));draw.text((x,1846),txt,font=font,fill='white')
 return base
