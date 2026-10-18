"""RO-04 source-specific preview recipe. Full assembly awaits Dan's opening/graphics approval."""
from pathlib import Path
import sys,subprocess,json,math
import numpy as np
from PIL import Image,ImageDraw
P=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=P/'Media/video-edits/RO-04/round2'
sys.path.insert(0,str(P/'.claude/skills/_shared'));import softblue as B
FF=str(P/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
RAW='/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1586.MP4'
REF=str(next((P/'Zeeshan Content Videos/arms and shoulders home workout - video 2').glob('*.mp4')))
START=66.6003; OFFSET=431.36425
# The first confirmed beep anchors real-time 30-second blocks; see qa/timing-proof.json.
SET0=5.8497; SETS=[SET0,SET0+30,SET0+60]; REST=SET0+90; TOTAL=REST+30
CROP={'OLD':(100,0,1776,1000),'B':(100,18,1776,1000)}
CAL=json.loads((W/'qa/calibration.json').read_text())
GRADES={'OLD':(1.0,1.0), 'A':(1.30,1.035), 'B':(1.48,1.075), 'C':(1.68,1.105)}
def vf(grade='B',crop='B'):
 c=CAL['rgb_polynomial'];ex=[]
 for i,(a,b,d) in enumerate(c):
  s=f'({a}*val+({b})*val*val/255+({d})*255)*{[1.012,1.,.99][i]}'
  ex.append('rgb'[i]+"='clip("+s+",0,255)'")
 x,y,w,h=CROP[crop];sat,con=GRADES[grade]
 base=f'crop={w}:{h}:{x}:{y},scale=1920:1080:in_color_matrix=bt709:in_range=tv,format=rgb24,lutrgb='+':'.join(ex)
 # Camera-only saturation and restrained contrast around the mids. Graphic paint follows this filter.
 if grade!='OLD':base+=f',format=yuv444p,eq=saturation={sat}:contrast={con}:brightness={(1-con)*0.04},format=rgb24'
 return base
def state(t):
 if t<SET0:return {'label':'Get ready','exercise':'Arms & Shoulders','next':'Curls, then shoulders, then triceps','left':SET0-t,'length':SET0}
 for i,s in enumerate(SETS):
  if t<s+30:return {'label':f'Exercise {i+1} of 3','exercise':['Bicep Curls','Side Lateral Raises','Overhead Triceps Extensions'][i],'next':['Next: side lateral raises','Next: overhead triceps extensions','Next: 30 seconds of rest'][i],'left':s+30-t,'length':30}
 return {'label':'Round complete','exercise':'Rest','next':'For more: replay the round after this rest','left':TOTAL-t,'length':30}
def paint(im,t):
 s=state(t);x,y,w,h=64,690,520,260
 if s['exercise']=='Overhead Triceps Extensions':y=646;h=304
 if t>=REST:
  im=B.field(t);x,y,w,h=540,260,840,500
 B.glass(im,(x,y,x+w,y+h),t,2,22)
 B.rr(im,(x+26,y+28,x+32,y+60),B.CYAN,3)
 B.text(im,(x+48,y+24),s['label'],26,B.CYAN)
 lines=B.wrap(s['exercise'],B.font(39),w-54)
 for i,l in enumerate(lines):B.text(im,(x+26,y+66+i*44),l,39)
 yy=y+124 if len(lines)==1 else y+160
 n=min(math.ceil(s['length']),max(1,math.ceil(s['left']-1e-7)))
 B.text(im,(x+26,yy),f'{n:02d}',70)
 B.text(im,(x+142,yy+36),'seconds',25,(205,226,244),False)
 if len(lines)>1:
  # Extra line increases the card naturally rather than covering the action with a wider panel.
  pass
 by=y+h-24;B.rr(im,(x+26,by,x+w-26,by+5),(22,51,81),2)
 q=max(0,min(1,s['left']/s['length']));B.rr(im,(x+26,by,x+26+(w-52)*q,by+5),B.CYAN,2)
 if t<REST:
  B.glass(im,(64,970,714,1030),t,2,14);B.text(im,(85,983),s['next'],25)
 else:
  B.text(im,(x+26,y+360),'One real-time round complete.',33)
  B.text(im,(x+26,y+412),'Replay for another round when ready.',30,B.CYAN)
 return im

def frame(t,grade='B',crop='B',graphics=True):
 if t>=REST:im=B.field(t)
 else:
  b=subprocess.check_output([FF,'-v','error','-ss',str(START+t),'-i',RAW,'-frames:v','1','-vf',vf(grade,crop),'-f','rawvideo','-pix_fmt','rgb24','-'])
  im=Image.frombytes('RGB',(1920,1080),b)
 return paint(im,t) if graphics else im

def render(name,a,b,grade='B',crop='B',graphics=True):
 out=W/name;out.parent.mkdir(parents=True,exist_ok=True);n=round((b-a)*FPS);dur=n/FPS
 if a>=REST:dec=None
 else:dec=subprocess.Popen([FF,'-v','error','-ss',str(START+a),'-i',RAW,'-frames:v',str(n),'-vf',vf(grade,crop),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 # Editor mix is cut only: no gain, limiter, mono sum, EQ or new music treatment.
 args=[FF,'-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30000/1001','-i','-']
 if a<REST:args+=['-ss',str(START+a+OFFSET),'-i',REF]
 else:args+=['-ss',str(START+a+OFFSET-510+8.7325),'-i','/Volumes/Extreme/_edit_work/music-check-20260922/knox-gym-energy-gym-thunder-538872.mp3']
 if a>=REST:args+=['-af','volume=0.07449345290660858']
 args+=['-map','0:v:0','-map','1:a:0','-t',str(dur),'-c:v','h264_videotoolbox','-b:v','12M','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a',('copy' if a<REST else 'aac'),'-movflags','+faststart','-y',str(out)]
 enc=subprocess.Popen(args,stdin=subprocess.PIPE)
 for j in range(n):
  t=a+j/FPS
  if dec:
   data=dec.stdout.read(1920*1080*3)
   if len(data)!=1920*1080*3:raise RuntimeError(f'short source frame {j}')
   im=Image.frombytes('RGB',(1920,1080),data)
  else:im=B.field(t)
  if graphics:im=paint(im,t)
  enc.stdin.write(im.tobytes())
 enc.stdin.close();rc=enc.wait()
 if dec:dec.stdout.close();assert dec.wait()==0
 assert rc==0
 subprocess.run([FF,'-v','error','-i',str(out),'-vf','scale=960:540','-c:v','h264_videotoolbox','-b:v','1600k','-c:a','copy','-movflags','+faststart','-y',str(out.with_name(out.stem+' - REVIEW 540p.mp4'))],check=True)
 print(out,flush=True)
