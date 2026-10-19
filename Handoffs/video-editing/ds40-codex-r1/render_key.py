import sys,subprocess,time,json
from pathlib import Path
import numpy as np,cv2
from refine_key import key
W=Path(__file__).parent
F='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC='/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
width,height=1656,2944
cmd=[F,'-hide_banner','-loglevel','error','-ss','1413.0116','-i',SRC,'-an','-frames:v','300','-vf','crop=1656:2944:252:500,scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,format=rgb48le','-f','rawvideo','-']
dec=subprocess.Popen(cmd,stdout=subprocess.PIPE)
enc=subprocess.Popen([F,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgba64le','-video_size','1080x1920','-framerate','30000/1001','-i','-','-an','-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-alpha_bits','16','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(W/'keyed-master.mov')],stdin=subprocess.PIPE)
t=time.time();stats=[]
for i in range(300):
 raw=dec.stdout.read(width*height*6)
 if len(raw)!=width*height*6:raise RuntimeError(f'short frame {i}')
 im=np.frombuffer(raw,np.uint16).reshape(height,width,3).astype(np.float32)/65535
 fg,a=key(im)
 # Resize premultiplied color and alpha together, avoiding colored resize fringes.
 fg=cv2.resize(fg,(1080,1920),interpolation=cv2.INTER_AREA);a=cv2.resize(a,(1080,1920),interpolation=cv2.INTER_AREA)
 straight=np.clip(fg/np.maximum(a[:,:,None],.00001),0,1)
 out=np.concatenate([straight,a[:,:,None]],axis=2)
 enc.stdin.write((out*65535).astype('<u2').tobytes())
 if i%30==0:
  stats.append({'frame':i,'background_alpha_p99':float(np.percentile(a[:50,:100],99))})
  comp=fg+(1-a[:,:,None])*np.array([.84,.87,.89]);cv2.imwrite(str(W/f'frame-{i:03}.png'),(np.clip(comp,0,1)[:,:,::-1]*255).astype('uint8'))
  print(i,round(time.time()-t,1),flush=True)
enc.stdin.close();assert enc.wait()==0;assert dec.wait()==0
(W/'key-measurements.json').write_text(json.dumps(stats,indent=2))
print('DONE',time.time()-t,flush=True)
