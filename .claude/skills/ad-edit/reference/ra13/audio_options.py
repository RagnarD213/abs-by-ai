import os,sys,json,subprocess,wave
from pathlib import Path
import numpy as np
W=Path(__file__).resolve().parents[1];os.chdir(W)
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');SH=R/'.claude/skills/_shared/audio'
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('RA-13 voice auditions')
FF=str(R/'Media/video_edit/bin/ffmpeg');(W/'audio-options').mkdir(exist_ok=True)
# Verify the audition begins in speech and contains no long empty stretch before any paid listen.
f=wave.open('source/audition.wav');sr=f.getframerate();x=np.frombuffer(f.readframes(f.getnframes()),np.int16)/32768.;f.close()
levels=[float(20*np.log10(max(1e-9,np.sqrt(np.mean(x[i:i+sr]**2))))) for i in range(0,len(x),sr)]
json.dump(levels,open('audio-options/speech-levels.json','w'),indent=1)
assert max(levels[:1])>-40,levels[:2]
assert not any(a<-45 and b<-45 for a,b in zip(levels,levels[1:])),levels
warm='highpass=f=70,equalizer=f=140:t=q:w=0.8:g=1.5,equalizer=f=450:t=q:w=1:g=-1.5,equalizer=f=3200:t=q:w=0.8:g=-1,equalizer=f=120:t=q:w=0.8:g=3'
variants=[('untreated',['--finish-only']),('default',[]),('warm-bass',['--eq',warm]),('lighter-bass',['--eq',warm.replace('g=3','g=1.5')])]
for name,extra in variants:
 cmd=[sys.executable,str(SH/'voice_chain.py'),'--in','source/audition.wav','--out',f'audio-options/{name}.wav','--work',f'audio-options/work-{name}']+extra
 with open(f'logs/voice-{name}.log','w') as log:p=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 print(name,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
print('AUDIO OPTIONS READY',flush=True)
