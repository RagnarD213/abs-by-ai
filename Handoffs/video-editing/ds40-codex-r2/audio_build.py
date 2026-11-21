from pathlib import Path
import subprocess,sys,shutil,json
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');P=W.parent/'round1';A=R/'.claude/skills/_shared/audio'
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R2 audio auditions')
subprocess.run(['zsh',str(A/'selftest.sh')],stdout=open(W/'audio-selftest.log','w'),stderr=subprocess.STDOUT,check=True)
shutil.copy2(P/'voice-open.wav',W/'voice-baseline.wav');shutil.copy2(P/'voice-open.wav.audio_untreated.json',W/'voice-baseline.wav.audio_untreated.json')
options={
 'clearer':'highpass=f=75,equalizer=f=180:t=q:w=0.8:g=-1.5,equalizer=f=450:t=q:w=0.8:g=-1.5,equalizer=f=2500:t=q:w=0.8:g=1',
 'fuller':'highpass=f=65,equalizer=f=120:t=q:w=0.8:g=2.5,equalizer=f=400:t=q:w=0.9:g=-1.5,equalizer=f=4000:t=q:w=0.8:g=-0.7',
 'balanced':'highpass=f=70,equalizer=f=120:t=q:w=0.8:g=0.8,equalizer=f=300:t=q:w=0.8:g=-2,equalizer=f=1800:t=q:w=0.8:g=0.5,equalizer=f=6000:t=q:w=0.8:g=-1.2'}
for name,eq in options.items():
 cmd=[sys.executable,str(A/'voice_chain.py'),'--in',str(P/'lav.wav'),'--out',str(W/f'voice-{name}.wav'),'--work',str(W/f'audio-{name}'),'--eq',eq,'--no-expander-because','R1 listening found chopped word tails with expansion; Dan found the open baseline fairly decent. Preserve natural word endings.','--target','-14.1','--tp','-2.5']
 subprocess.run(cmd,stdout=open(W/f'voice-{name}.log','w'),stderr=subprocess.STDOUT,check=True)
 print(name,'done',flush=True)
(W/'audio-options.json').write_text(json.dumps(options,indent=2))
print('AUDIO DONE',flush=True)
