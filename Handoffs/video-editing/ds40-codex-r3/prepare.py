import sys,subprocess,json,cv2,numpy as np,time
from pathlib import Path
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');SRC='/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R3 hair cache');cv2.setNumThreads(2)
(W/'native').mkdir(exist_ok=True)
dec=subprocess.Popen([F,'-v','error','-ss','1413.0116','-i',SRC,'-frames:v','300','-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,format=rgb48le','-f','rawvideo','-'],stdout=subprocess.PIPE)
coefs=[]; t=time.time()
for i in range(300):
 raw=dec.stdout.read(2160*3840*6);assert len(raw)==2160*3840*6
 im=np.frombuffer(raw,'<u2').reshape(3840,2160,3)
 np.save(W/'native'/f'{i:03}.npy',im[400:1300,350:1850])
 if i%15==0:
  s=im[::16,::16].astype(np.float32)/65535;h,w=s.shape[:2]; y,x=np.mgrid[:h,:w].astype(np.float32);x=x*16/2160;y=y*16/3840
  r,g,b=s.transpose(2,0,1);sel=(g-r>.14)&(g-b>.14);X=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],-1)
  coef=np.linalg.lstsq(X[sel],s[sel],rcond=None)[0]
  for it in range(3):
   res=np.linalg.norm(s-X@coef,axis=2);keep=sel&(res<np.percentile(res[sel],85));coef=np.linalg.lstsq(X[keep],s[keep],rcond=None)[0]
  coefs.append(coef)
 if i%60==0:print(i,round(time.time()-t,1),flush=True)
assert dec.wait()==0
np.save(W/'screen-coefs.npy',np.array(coefs));coef=np.median(coefs,axis=0)
y,x=np.mgrid[400:1300,350:1850].astype(np.float32);x/=2160;y/=3840;X=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],-1)
np.save(W/'screen.npy',X@coef)
print('CACHE DONE',flush=True)
