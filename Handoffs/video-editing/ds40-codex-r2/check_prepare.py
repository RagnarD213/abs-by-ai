from pathlib import Path
import subprocess,sys,time,hashlib,json
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');D=W/'review/media';V=D/'sample.mp4';A=W/'audit';A.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
for i in range(1000):
 if 'PACKAGE DONE' in (W/'package.log').read_text():break
 time.sleep(2)
else:raise RuntimeError('package wait timed out')
buildcap.wait('Bill Maher R2 watch preparation')
sha=hashlib.sha256(V.read_bytes()).hexdigest();(W/'sha256.txt').write_text(sha+'\n')
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),str(V),'--plan',str(W/'plan.json'),'--out',str(W/'watch'),'--log',str(W/'watch/watch_pass.json')],stdout=open(W/'watch.log','w'),stderr=subprocess.STDOUT,check=True)
subprocess.run([F,'-y','-v','error','-i',str(V),'-vf','fps=2.4,scale=180:320,tile=8x3','-frames:v','1',str(A/'scan-24.jpg')],check=True)
for n,t in enumerate([1,2,5,8]):
 subprocess.run([F,'-y','-v','error','-ss',str(t),'-i',str(D/'hair.mp4'),'-frames:v','1','-vf','select=not(mod(n\\,2)),scale=324:360,tile=5x1',str(A/f'hair-motion-{n}.jpg')],check=True)
(W/'check-ready.json').write_text(json.dumps({'sha256':sha,'video':str(V),'duration':10.01}));print('CHECK PREP DONE',flush=True)
