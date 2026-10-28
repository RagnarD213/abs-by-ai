from pathlib import Path
import sys,os,json,hashlib,subprocess
import numpy as np
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');F=R/'Media/video_edit/bin/ffmpeg';os.environ['PATH']=str(F.parent)+':'+os.environ['PATH'];sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as A
v=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p.mp4';a=A.pcm(str(v),ac=1);b=A.pcm(str(W/'audio/voice-selected.wav'),ac=1);N=min(len(a),len(b));a=a[:N];b=b[:N];corr=[]
for i in range(0,N-48000,48000):corr.append(float(np.corrcoef(a[i:i+48000],b[i:i+48000])[0,1]))
gain=float(np.dot(a,b)/np.dot(b,b));res=a-b*gain
rec=dict(video_sha256=hashlib.sha256(v.read_bytes()).hexdigest(),selected_voice_sha256=hashlib.sha256((W/'audio/voice-selected.wav').read_bytes()).hexdigest(),compared_samples=N,seconds=N/48000,per_second_corr=corr,median_corr=float(np.median(corr)),minimum_corr=float(min(corr)),constant_gain_db=float(20*np.log10(abs(gain))),residual_rms=float(np.sqrt(np.mean(res**2))),note='Sample-aligned decoded AAC versus exact approved full Voice A PCM. This proves preservation/encoding similarity, not a new perceptual listen. R1 independent full selected-audio listen is retained as existing evidence. No paid QA called.')
assert rec['minimum_corr']>.98;assert abs(rec['constant_gain_db'])<.2
(W/'evidence/checks/audio-preservation.json').write_text(json.dumps(rec,indent=2))
# New extended moving field: compare adjacent seconds across entire title, including former40.04s endpoint.
def rgb(path,t,rect=None):
 vf='scale=in_color_matrix=bt709:in_range=tv'
 if rect:vf+=','+rect
 z=subprocess.check_output([str(F),'-nostdin','-v','error','-ss',str(t),'-i',str(path),'-an','-frames:v','1','-vf',vf,'-pix_fmt','rgb24','-f','rawvideo','pipe:1']);return np.frombuffer(z,'uint8').astype(float)
ms=[]
for t in [1,5,10,15,20,25,30,35,39,40,41,45,50,55,60,62]:
 p=rgb(v,t,'crop=1080:310:0:0');q=rgb(v,t+1,'crop=1080:310:0:0');ms.append(dict(t=t,adjacent_second_mean_change=float(abs(q-p).mean())))
assert all(x['adjacent_second_mean_change']>0 for x in ms)
(W/'evidence/checks/title-motion.json').write_text(json.dumps(dict(video_sha256=rec['video_sha256'],method='Native rendered title ROI adjacent-second decoded-pixel change; independently inspect visible continuous field motion.',samples=ms),indent=2))
print('AUDIO_PRESERVED',rec['minimum_corr'],rec['constant_gain_db']);print('TITLE_MOVING',min(x['adjacent_second_mean_change'] for x in ms))
