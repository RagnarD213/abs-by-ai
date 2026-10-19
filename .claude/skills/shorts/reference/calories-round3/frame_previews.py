from pathlib import Path
import sys,json,subprocess
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np
P=Path(__file__).parent;W=P.parent;R='/Users/danielrose/Documents/Claude/Projects/Abs By AI'
sys.path[:0]=[str(P),R+'/.claude/skills/_shared']
import batch as B,lib,buildcap,cap_local
F=W/'frames';O=W/'review';(O/'frames').mkdir(parents=True,exist_ok=True)
def still(S,which,t):
 d=Path(B.D(S));base=lib.canvas(t);title=Image.open(O/f'title-{S}.png').convert('RGB');base.paste(title,(0,0))
 p=F/f'{S}01-{which}.png'
 if S=='D' and which=='start':p=F/'D01-start-fit.png'
 pic=ImageOps.fit(Image.open(p).convert('RGB'),(1080,1610),centering=(.5,.1));base.paste(pic,(0,310))
 lib.B.disclosure(base,'AI-GENERATED',(32,335),1.25,anchor='lt',size=23)
 cues=json.load(open(d/'cues.json'))
 for c in cues:
  if c['a']<=t<c['b']:lib.caption(base,c['lines'],1640 if S=='A' else 1500)
 draw=ImageDraw.Draw(base);font=lib.B.font(24);txt='Frame Preview: Motion Not Generated'
 box=draw.textbbox((0,0),txt,font=font);x=(1080-(box[2]-box[0]))//2
 draw.rounded_rectangle((x-14,1840,1080-x+14,1885),8,fill=(7,19,34));draw.text((x,1846),txt,font=font,fill='white')
 return base
for S in 'AD':
 buildcap.wait('Calories R3 frame preview '+S)
 d=Path(B.D(S));subprocess.run([lib.FF,'-v','error','-y','-ss','1.2','-i',str(d/'hf/title.mov'),'-frames:v','1',str(O/f'title-{S}.png')],check=True)
 for which,t in [('start',.5),('end',4.1 if S=='A' else 1.7)]:still(S,which,t).save(O/'frames'/f'{S}01-{which}-composed.jpg',quality=94)
 N=B.fr(6.2368333333) if S=='A' else B.fr(2.3004666667);dest=O/f'{S}01-frame-context.mp4'
 e=subprocess.Popen([lib.FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate',B.FPSS,'-i','-','-i',str(d/'audio.wav'),'-t',str(N/B.FPS),'-map','0:v','-map','1:a','-vf','scale=540:960','-c:v','h264_videotoolbox','-b:v','1800k','-c:a','aac','-b:a','160k','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE)
 for i in range(N):
  t=i/B.FPS;which='start' if t<(2.86 if S=='A' else 1.15) else 'end';e.stdin.write(np.asarray(still(S,which,t)).tobytes())
 e.stdin.close();assert e.wait()==0;print('FRAME CONTEXT READY',S,flush=True)
