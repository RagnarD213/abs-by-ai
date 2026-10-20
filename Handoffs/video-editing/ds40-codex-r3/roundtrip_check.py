import subprocess,numpy as np,json
from pathlib import Path
W=Path(__file__).parent;F='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg';src=str(W.parent/'round2/review/media/balanced.mp4')
base='scale=in_color_matrix=bt709:in_range=tv:out_range=pc'
def read(src,flags):
 return subprocess.check_output([F,'-v','error','-i',src,'-vf',base+flags+',format=rgb24','-frames:v','1','-f','rawvideo','-'])
a=np.frombuffer(read(src,':flags=accurate_rnd+full_chroma_int'),'uint8').reshape(1920,1080,3);rows=[]
for mode,flags in [('fast',''),('accurate',':flags=accurate_rnd+full_chroma_int')]:
 path=str(W/f'roundtrip-{mode}.mp4');data=read(src,flags)
 subprocess.run([F,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30000/1001','-i','-','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-crf','16','-preset','fast','-threads','1','-colorspace','bt709',path],input=data,check=True)
 b=np.frombuffer(read(path,':flags=accurate_rnd+full_chroma_int'),'uint8').reshape(1920,1080,3)
 rows.append({'mode':mode,'before_field':a[100,100].tolist(),'after_field':b[100,100].tolist(),'body_mae':float(np.mean(abs(b[700:].astype(float)-a[700:]))),'field_mae':float(np.mean(abs(b[:200].astype(float)-a[:200])))})
print(json.dumps(rows));(W/'color-roundtrip.json').write_text(json.dumps(rows,indent=2))
