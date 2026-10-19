from pathlib import Path
import subprocess,sys,json
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');A=R/'.claude/skills/_shared/audio';P=W.parent/'round1'
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R2 voice headroom')
options=json.loads((W/'audio-options.json').read_text());options['balanced']='highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7'
for name,eq in options.items():
 cmd=[sys.executable,str(A/'voice_chain.py'),'--in',str(P/'lav.wav'),'--out',str(W/f'voice-{name}.wav'),'--work',str(W/f'audio-{name}'),'--eq',eq,'--no-expander-because','R1 listening found chopped word tails with expansion; Dan found the open baseline fairly decent. Preserve natural word endings.','--target','-14.1','--tp','-1.5','--oversample','4']
 subprocess.run(cmd,stdout=open(W/f'voice-{name}.log','w'),stderr=subprocess.STDOUT,check=True);print(name,'done',flush=True)
(W/'audio-options.json').write_text(json.dumps(options,indent=2));print('DONE',flush=True)
