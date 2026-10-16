from pathlib import Path
import sys,json,subprocess
from PIL import Image,ImageDraw
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('RA13 R3 source preview')
FF=str(R/'Media/video_edit/bin/ffmpeg');src='/Volumes/Extreme/_edit_work/ra04/round5/gen_white_man_rec.mp4'
imgs=[]
for t in [3.4,4.5,5.75,36.6,38,41.8]:
 p=O/f'probe-{t}.png';subprocess.run([FF,'-v','error','-y','-ss',str(t),'-i',src,'-frames:v','1',str(p)],check=True);im=Image.open(p);im.thumbnail((330,717));imgs.append((t,im.copy()))
out=Image.new('RGB',(990,1494),'#cdddeb');d=ImageDraw.Draw(out)
for i,(t,im) in enumerate(imgs):x=i%3*330;y=i//3*747;out.paste(im,(x,y+30));d.text((x+8,y+8),str(t),fill='black')
out.save(O/'source-probe.jpg');print('SOURCE PROBE READY',flush=True)
