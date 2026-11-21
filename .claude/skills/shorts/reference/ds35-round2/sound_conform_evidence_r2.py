"""Actual decoded AAC vs selected owned voice and audible source segment.
Evidence of identity and source routing; not a perceptual PASS or a reference-mode gate.
"""
from pathlib import Path
import sys,json,numpy as np
from scipy.signal import correlate,correlation_lags
W=Path(__file__).resolve().parents[1];O=W.parent/'round1';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
renderq.hold_until_exit('Dad Bod actual AAC selected sound conform',pool='light')
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
from qa_full_r2 import sha

def compare(a,b):
 n=min(len(a),len(b));a=a[:n];b=b[:n];co=correlate(b,a,method='fft');la=correlation_lags(len(b),len(a));mask=abs(la)<4800;lag=int(la[mask][co[mask].argmax()])
 if lag>0:b=b[lag:];a=a[:len(b)]
 elif lag<0:a=a[-lag:];b=b[:len(a)]
 n=min(len(a),len(b));a=a[:n];b=b[:n];g=float(np.dot(a,b)/np.dot(a,a));return dict(seconds=n/48000,lag_samples=lag,correlation=float(np.corrcoef(a,b)[0,1]),gain_db=float(20*np.log10(abs(g))),residual_vs_signal_db=float(20*np.log10(np.sqrt(np.mean((b-a*g)**2))/np.sqrt(np.mean(b*b)))))
for v in sys.argv[1:]:
 q=W/'qa'/v;vid=W/'review/media'/('dad-bod-r2-'+v+'.mp4');stem=W/v/'audio/voice-C_Balanced.wav';final=q/'Dan-exact-stereo-final-AAC.wav'
 a=C.pcm(str(stem),ac=1);b=C.pcm(str(final),ac=1);whole=compare(a,b);windows=[]
 for i in range(0,min(len(a),len(b)),5*48000):
  aa=a[i:i+5*48000];bb=b[i:i+5*48000]
  if len(aa)<48000:continue
  windows.append(dict(start=i/48000,**compare(aa,bb)))
 old=O/('options/C_Balanced.wav' if v=='scripted' else 'options/off_the_cuff/C_Balanced.wav')
 oa=C.pcm(str(old),ac=1);fb=C.pcm(str(final),ss=16/(30000/1001)+.02,dur=30,ac=1) if v=='scripted' else b
 oldmatch=compare(oa,fb)
 audio=json.loads((q/'Dan-exact-stereo-final-AAC.wav.audio_gate.json').read_text());r=dict(video_sha256=sha(vid),owned_normal_gate=str(q/'Dan-exact-stereo-final-AAC.wav.audio_gate.json'),selected_stem=dict(path=str(stem),sha256=sha(stem)),actual_decoded_AAC=dict(path=str(final),sha256=sha(final)),whole_selected_stem_conform=whole,windows=windows,approved_original_C_audition=dict(path=str(old),sha256=sha(old),comparison=oldmatch),routing=dict(approved_source_clip=str(O/'scripted/audio/clip-finished-candidate3.wav'),source_ends_at=469/(30000/1001),response_begins_at=485/(30000/1001),description='Concatenated source clip then selected owned voice. No interview voice/audio overlay exists in response. Quiet room/breath is present before Dan first speaks.'),normal_owned_rows=[x for x in audio['rows']],interpretation='Measured identity only. All normal owned-mix tests preserved. Tone difference from Muhammad reference is explicit selected C choice; no added NR, dereverb or expander.')
 (q/'sound-conform-evidence.json').write_text(json.dumps(r,indent=2));print(v,whole,oldmatch,flush=True)
