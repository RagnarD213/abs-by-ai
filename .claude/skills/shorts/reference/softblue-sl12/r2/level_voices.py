from pathlib import Path
import sys,json,subprocess,wave,hashlib
import numpy as np
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=Path('/Volumes/Extreme/_edit_work/SL-12/round2');D=R/'audio';SR=48000
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C
def wr(p,x):
 with wave.open(str(p),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
def active(x):
 f=C.frames(x,2048,1024);r=np.sqrt((f*f).mean(1)+1e-12);v=r[r>np.percentile(r,60)];return float(20*np.log10(np.sqrt((v*v).mean())))
ref=C.pcm(str(D/'qwen-reference.wav'));target=active(ref);rows=[]
for tag in ['parent-natural','parent-direct','prior-natural','qwen-parent','parent-natural-retake','parent-conversational']:
 src=D/(tag+'.wav');x=C.pcm(str(src));gain=target-active(x);peak=float(abs(x).max()*10**(gain/20));limited=peak>.78
 af=f'aresample=48000,volume={gain:.6f}dB'+(',alimiter=limit=0.78:attack=5:release=60:level=false:latency=true' if limited else '')
 z=C.pcm(str(src),af=af);z[:min(120,len(z))]*=np.linspace(0,1,min(120,len(z)));z[-min(120,len(z)):]*=np.linspace(1,0,min(120,len(z)));p=D/(tag+'-matched.wav');wr(p,np.repeat(z[:,None],2,axis=1))
 # A160ms quiet sentence boundary; original leading space remains. No time/pitch alteration.
 joined=np.concatenate([z,np.zeros(int(.16*SR)),ref[:6*SR]]);jp=D/(tag+'-context.wav');wr(jp,np.repeat(joined[:,None],2,axis=1));rows.append(dict(id=tag,solo=str(p),context=str(jp),seconds=len(z)/SR,seam_seconds=len(z)/SR+.16,gain_db=gain,limiter=limited,active_rms_dbfs=active(z),source_sha256=C.sha256(src),sha256=C.sha256(p)))
control=D/'real-control.wav';wr(control,np.repeat(ref[:10*SR,None],2,axis=1))
(D/'level-manifest.json').write_text(json.dumps(dict(reference=str(D/'qwen-reference.wav'),target_active_dbfs=target,candidates=rows,control=str(control),processing='Constant gain, optional true-peak safety limiter only, 2.5ms endpoint fades; no tone matching or time/pitch shift.'),indent=2)+'\n')
print('Level-matched',[(x['id'],round(x['seconds'],2)) for x in rows],flush=True)
