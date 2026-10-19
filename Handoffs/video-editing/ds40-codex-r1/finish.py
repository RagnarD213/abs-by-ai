import sys,subprocess,cv2,numpy as np,json
from pathlib import Path
from grade import grade
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg')
mode=sys.argv[1];back=sys.argv[2] if len(sys.argv)>2 else 'light';name=mode if back=='light' else 'edge-dark'
(W/'review/media').mkdir(parents=True,exist_ok=True)
dec=subprocess.Popen([F,'-hide_banner','-loglevel','error','-i',str(W/'keyed-master.mov'),'-f','rawvideo','-pix_fmt','rgba64le','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen([F,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1080x1920','-framerate','30000/1001','-i','-','-an','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','medium','-crf','17','-threads','3','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(W/f'{name}-picture.mp4')],stdin=subprocess.PIPE)
col=np.array([.84,.87,.89] if back=='light' else [.08,.10,.13],np.float32)
for i in range(300):
 data=dec.stdout.read(1080*1920*8)
 if len(data)!=1080*1920*8:raise RuntimeError(i)
 im=np.frombuffer(data,'<u2').reshape(1920,1080,4).astype(np.float32)/65535
 im=cv2.resize(im,(1100,1956),interpolation=cv2.INTER_CUBIC)[36:1956,10:1090];a=np.clip(im[:,:,3:4],0,1)
 x=grade(im[:,:,:3],mode)*a+col*(1-a);o=(np.clip(x,0,1)*255+.5).astype('uint8')
 enc.stdin.write(o.tobytes())
 if i in [30,150,240]:cv2.imwrite(str(W/f'review/media/{name}-{i}.jpg'),o[:,:,::-1],[cv2.IMWRITE_JPEG_QUALITY,97])
enc.stdin.close();assert enc.wait()==0;assert dec.wait()==0
print(name,'done',flush=True)
