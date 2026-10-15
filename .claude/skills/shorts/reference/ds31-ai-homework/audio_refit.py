"""Refit the voice tone to THIS recording with the shared fitter (the method behind DS-28's approved 'fitted tone + bass'),
then the standard +3 dB at 120 Hz, no expander, no dereverb. Writes voice-fit.wav for comparison against voice.wav."""
from pathlib import Path
import sys, subprocess, json, os
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; A = R/'.claude/skills/_shared/audio'
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
sys.path.insert(0, str(A)); import voice_chain as V; import reference as Ref
ref_audio, ref = Ref.resolve(); work = W/'voice-refit'; work.mkdir(exist_ok=True)
lav, x, how = V.pull(str(W/'untreated.wav'), None, 'pan=mono|c0=0.5*c0+0.5*c1', str(work))
eq, gains, step = V.fit_eq(lav, ref, str(work)); eq += ',equalizer=f=120:t=q:w=0.8:g=3.0'
(W/'fit-voice-eq.json').write_text(json.dumps(dict(eq=eq, gains=gains), indent=1))
subprocess.run([sys.executable, str(A/'voice_chain.py'), '--in', str(W/'untreated.wav'), '--out', str(W/'voice-fit.wav'), '--pull', 'pan=mono|c0=0.5*c0+0.5*c1', '--eq', eq,
                '--no-expander-because', 'Same roll and mic as DS-28 (fitted tone + bass, no expander, approved); preserve word tails.', '--work', str(W/'voice-fit-work')], check=True)
print(eq)
