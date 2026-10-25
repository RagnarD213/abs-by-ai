import os
for v in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ.setdefault(v,'1')
import sys,json,subprocess,numpy as np,cv2
from pathlib import Path
from layer import clean,place
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');name=sys.argv[1];p=next(x for x in json.loads((W/'plan.json').read_text())['pieces'] if x['id']==name);D=W/'key-check'/name;D.mkdir(parents=True,exist_ok=True);cv2.setNumThreads(1)
fields={'pale':[.86,.89,.93],'navy':[.025,.055,.10],'pink':[.95,.25,.62]};encs={}
for k in fields:
 encs[k]=subprocess.Popen([F,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30000/1001','-i','-','-an','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','16','-threads','1','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(D/f'{k}.mp4')],stdin=subprocess.PIPE)
for i in range(p['n']):
 fp,a=clean(np.load(W/'key'/name/'c15'/f'f{i:04d}.npy'))
 for k,col in fields.items():
  bg=np.ones((1920,1080,3),np.float32)*np.array(col,np.float32);out=place(bg,fp,a);encs[k].stdin.write((out*255+.5).astype(np.uint8).tobytes())
 if i%120==0:print('keycheck',name,i,flush=True)
for k,e in encs.items():e.stdin.close();assert e.wait()==0
# Same approved R2 measurement formulas, adapted only for the full-height origin and actual hair/watch regions.
for mod in ['mcflicker','measure_r2']:
 s=(W/'recipe'/f'{mod}.py').read_text().replace('import numpy as np, subprocess, json, sys, os, cv2','import numpy as np, subprocess, json, sys, os, cv2\ncv2.setNumThreads(1)').replace('OY = 176','OY = 0').replace('slice(470, 680), slice(300, 700)','slice(240, 650), slice(230, 850)').replace('see[:1650] = False','see[:1200] = False')
 q=D/f'{mod}.py';q.write_text(s);env=dict(os.environ,T0=str(p['t0']),DUR=str(p['n']/(30000/1001)))
 args=[sys.executable,str(q),str(D/'pale.mp4')]
 if mod=='measure_r2':args.append(str(D/'navy.mp4'))
 args.append(str(D/f'{mod}.json'));subprocess.run(args,env=env,check=True)
(D/'complete.json').write_text(json.dumps({'piece':p,'checks':['mcflicker','measure_r2'],'origin':0,'hair_roi':[230,240,850,650],'see_through_region':'below y1200 includes moving watch; three-field visual check retained'},indent=2))
