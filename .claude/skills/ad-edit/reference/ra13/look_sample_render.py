import os,sys,json,subprocess,math
from pathlib import Path
import numpy as np
W=Path(__file__).resolve().parents[1];os.chdir(W)
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');SH=R/'.claude/skills/_shared'
sys.path.insert(0,str(SH));import buildcap
buildcap.wait('RA-13 moving look samples')
sys.path.insert(0,str(SH/'cut'));import landing
FF=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
C=json.load(open('cut.json'));T=json.load(open('track-look.json'));G=json.load(open('grade-options.json'));roll=json.load(open('source/roll.json'))['identity']['current_path']
O=W/'round1/context';O.mkdir(exist_ok=True,parents=True);meta={}
# Same short section for the three grades. These are isolated look auditions, not an opening approval.
for code,aspect in [('A','9x16'),('B','9x16'),('C','9x16'),('B','16x9')]:
 ins=[];vf=[];stats=[];total=0
 for i,p in enumerate(C['pieces'][:2]):
  dur=p['src_out']-p['src_in'];nf=round(dur*FPS);total+=nf
  vals=[q for q in T if q['piece']==i];assert vals and vals[0]['frame']==0,'Missing first cut frame'
  n=np.array([q['frame']*6 for q in vals]);raw=np.array([q['cx'] for q in vals]);cw,ch=(738,1312) if aspect=='9x16' else (2144,1206)
  ni,x,info=landing.vertical_track(n,raw,[{'n0':0,'n1':nf}],cw,FPS) if aspect=='9x16' else (n,np.full(len(n),1080.),{})
  if aspect=='9x16':
   info.update(landing.motion_stats(ni,np.interp(ni,n,raw),x,[{'n0':0,'n1':nf}],cw,FPS))
  # Crop expressions interpolate only within this source piece.
  expr=str(round(float(x[-1])-cw/2,3))
  for j in range(len(ni)-2,-1,-1):
   a,b=int(ni[j]),int(ni[j+1]);xa,xb=float(x[j])-cw/2,float(x[j+1])-cw/2
   part=f'{xa:.3f}+({xb-xa:.3f})*(n-{a})/{max(1,b-a)}'
   expr=f'if(lt(n,{b}),{part},{expr})'
  y=int(min(v['hair'] for v in vals)-ch*.05)//2*2;y=max(0,y)
  stats.append({'piece':i,'crop':[cw,ch],'y':y,'first_head':float(raw[0]),'raw_range':float(np.ptp(raw)),'motion':info})
  ins+=['-ss',str(p['src_in']),'-t',str(dur+.1),'-i',roll]
  wh='1080:1920' if aspect=='9x16' else '1920:1080'
  vf.append(f'[{i}:v]{G[code]["filter"]},trim=end_frame={nf},setpts=PTS-STARTPTS,crop={cw}:{ch}:\'{expr}\':{y},scale={wh}:flags=lanczos,setsar=1[v{i}]')
 vf.append('[v0][v1]concat=n=2:v=1:a=0[v]')
 out=O/f'look-{code}-{aspect}.mp4'
 subprocess.run([FF,'-v','error','-y']+ins+['-i',str(W/'audio-options/lighter-bass.wav'),'-filter_complex',';'.join(vf),'-map','[v]','-map','2:a','-t',str(total/FPS),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
 subprocess.run([FF,'-v','error','-y','-ss','1','-i',str(out),'-frames:v','1',str(O/f'look-{code}-{aspect}.jpg')],check=True)
 meta[f'{code}-{aspect}']={'frames':total,'duration':total/FPS,'framing':stats,'stage':'look audition only'}
 print('READY',out.name,flush=True)
json.dump(meta,open('round1/look-sample-metrics.json','w'),indent=2)
# Native reference frame checks beside this source.
for path,t,name in [(Path('/Volumes/Extreme/_edit_work/ra01/master_9x16.mp4'),2.5,'reference-ra01')]:
 subprocess.run([FF,'-v','error','-y','-ss',str(t),'-i',str(path),'-frames:v','1',str(W/f'round1/stills/{name}.jpg')],check=True)
print('LOOK SAMPLES READY',flush=True)
lib=Path('/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library')
assets=[('L1',lib/'04 AI-Generated Clips/ai-dan/A0074_hand-holds-phone-lockscreen-ai-goal-pool_9x16_5s.mp4',.5,3.15),('P3',lib/'03 B-Roll - Real Footage/screen-recordings/B0037_app-workout-swap-goblet-squat-card_16x9_8s.mp4',0,7.5)]
for name,path,t,d in assets:
 subprocess.run([FF,'-v','error','-y','-ss',str(t),'-i',str(path),'-t',str(d),'-an','-vf','scale=-2:540','-c:v','libx264','-preset','fast','-crf','20','-movflags','+faststart',str(O/f'{name}-source.mp4')],check=True)
 subprocess.run([FF,'-v','error','-y','-ss',str(t+1),'-i',str(path),'-frames:v','1',str(W/f'round1/stills/{name}.jpg')],check=True)
print('ASSET SOURCES READY',flush=True)
