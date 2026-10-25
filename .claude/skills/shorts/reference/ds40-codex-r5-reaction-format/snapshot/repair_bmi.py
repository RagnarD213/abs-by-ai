import os
for v in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ.setdefault(v,'1')
import subprocess,json,hashlib,cv2,numpy as np
from pathlib import Path
from PIL import Image
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');D=W/'review/media';src=W/'internal-pre-bmi-repair/review/media/bill-maher-fat-90-year-old-r5.mp4';out=D/'bmi-repaired-picture.mp4';cv2.setNumThreads(1)
a=json.loads((W/'assembly.json').read_text());t=np.array(Image.open(W.parent/'round4/bmi-table.png').convert('RGB'));small=cv2.resize(t[:900],(1008,810),interpolation=cv2.INTER_AREA)
r=subprocess.Popen([F,'-v','error','-i',str(src),'-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
e=subprocess.Popen([F,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30000/1001','-i','-','-an','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','14','-threads',os.environ.get('RENDERQ_CORES','4'),'-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
for g in range(1944):
 b=r.stdout.read(1080*1920*3);assert len(b)==1080*1920*3;f=np.frombuffer(b,np.uint8).reshape(1920,1080,3).copy()
 if 1530<=g<1818:
  f[240:1360,36:1044]=t[0,0];f[240:1050,36:1044]=small;j=2 if g<1671 else 3;x=24+j*246;f[1068:1334,248:832]=cv2.resize(t[925:1029,x:x+228],(584,266),interpolation=cv2.INTER_CUBIC)
 e.stdin.write(f.tobytes())
 if g in [1529,1530,1531,1670,1671,1672,1817,1818]:Image.fromarray(f).save(W/'independent'/('repaired-%04d.png'%g))
 if g%300==0:print('BMI repair assembly',g,flush=True)
e.stdin.close();assert e.wait()==0;assert r.wait()==0
master=D/'bill-maher-fat-90-year-old-r5.mp4'
subprocess.run([F,'-y','-v','error','-i',str(out),'-i',str(src),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(master)],check=True)
a['previousCandidateSha256']=a['sha256'];a['sha256']=hashlib.sha256(master.read_bytes()).hexdigest();a['internalRepair']='BMI focus frames1530–1817 cleared table interior, removing residual duplicate row/legend before relayout; original evidence retained. Whole video encoded CRF14 from previous candidate; AAC stream copied.';(W/'assembly.json').write_text(json.dumps(a,indent=2));print('REPAIRED',a['sha256'],flush=True)
