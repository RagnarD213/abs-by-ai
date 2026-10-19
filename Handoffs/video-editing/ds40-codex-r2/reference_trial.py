from pathlib import Path
import subprocess,sys
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R2 natural reference trial')
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/voice_chain.py'),'--in',str(W.parent/'round1/lav.wav'),'--out',str(W/'voice-focused.wav'),'--work',str(W/'audio-focused'),'--no-expander-because','R1 listening found chopped word tails with expansion; user wants natural processing and thinks the open baseline decent.','--target','-14.1','--tp','-1.5','--oversample','4'],stdout=open(W/'voice-focused.log','w'),stderr=subprocess.STDOUT,check=True)
print('DONE',flush=True)
