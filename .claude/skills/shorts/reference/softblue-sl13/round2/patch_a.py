from pathlib import Path
import sys,json,subprocess,numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent));import batch as B
W=Path(B.WORK);OLD=W.parent/'round1';d=W/'build/A'
S=B.Short('A');sh=next(s for s in S.shots if s['roll']=='study');n0,n1=sh['f0'],sh['f1']
scene=B.Seq(str(d/'hf/renders/protein-study-r2.mov'),'scale=in_color_matrix=bt601:in_range=tv,format=rgb24',(1080,1610),B.FPS)
def decode(p):return subprocess.Popen([B.lib.FF,'-nostdin','-v','error','-i',str(p),'-vf','scale=in_color_matrix=bt709:in_range=tv,format=rgb24','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
def encode(p,audio=False):
 args=[B.lib.FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate',B.FPSS,'-i','-']
 if audio:args+=['-i',str(OLD/'review'/(B.P.NAME['A']+'.mp4')),'-map','0:v','-map','1:a','-c:a','copy']
 args+=['-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-crf','16' if audio else '20','-preset','medium','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(p)]
 return subprocess.Popen(args,stdin=subprocess.PIPE)
if sys.argv[-1]=='proof':
 base=B.Seq(str(OLD/'review'/(B.P.NAME['A']+'.mp4')),'scale=in_color_matrix=bt709:in_range=tv,format=rgb24',(1080,1920),B.FPS)
 (d/'proof').mkdir(exist_ok=True)
 for t in [34.5,35.8,38,39.4,41.5,43,44.8]:
  i=B.fr(t);f=base.get(i).copy();f[310:]=scene.get(i-n0);f=S.finish(f,sh,i);Image.fromarray(f).save(d/'proof'/('study-%04d.jpg'%i),quality=95)
 print('Study proof ready');base.close();scene.close();S.close();sys.exit()
p1=decode(OLD/'review'/(B.P.NAME['A']+'.mp4'));p2=decode(OLD/'build/A/source_picture.mp4')
e1=encode(d/(B.P.NAME['A']+'.mp4'),True);e2=encode(d/'source_picture.mp4');size=1080*1920*3
for i in range(S.N):
 bs=p1.stdout.read(size);cs=p2.stdout.read(size);assert len(bs)==len(cs)==size
 f=np.frombuffer(bs,np.uint8).reshape(1920,1080,3).copy();c=np.frombuffer(cs,np.uint8).reshape(1920,1080,3).copy()
 if n0<=i<n1:
  pic=scene.get(i-n0);f[310:]=pic;c[310:]=pic;f=S.finish(f,sh,i)
 e1.stdin.write(f.tobytes());e2.stdin.write(c.tobytes())
 if i%300==0:print('A patch',i,'/',S.N,flush=True)
for e in [e1,e2]:e.stdin.close();assert e.wait()==0
for p in [p1,p2]:p.stdout.close();assert p.wait()==0
scene.close();S.close()
(W/'a-preservation-method.json').write_text(json.dumps(dict(original=str(OLD/'review'/(B.P.NAME['A']+'.mp4')),changedFrames=[n0,n1],outsideFrames='R1 decoded frame carried without alteration before H264 encode',audio='AAC packets stream-copied from R1',header='R1 decoded pixels retained on every frame',captions='R1 cue data and alpha renderer reused only inside study'),indent=2))
print('A PATCH COMPLETE',flush=True)
