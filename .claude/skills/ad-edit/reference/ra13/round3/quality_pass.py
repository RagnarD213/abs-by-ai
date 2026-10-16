"""Measured per-format checks and native watch evidence. Human dispositions remain separate."""
from pathlib import Path
import sys,os,json,subprocess,importlib.util
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');fmt=sys.argv[1];D=O/f'checks{fmt}';D.mkdir(exist_ok=True)
SH=R/'.claude/skills/_shared';sys.path[:0]=[str(SH),str(SH/'cut')];import buildcap
FF=str(R/'Media/video_edit/bin/ffmpeg');video=O/f'final/why do most guys never get abs | codex | {"9x16" if fmt=="9" else "16x9"} | RA-13 R3.mp4'
def run(cmd,log):
 with open(D/log,'w') as f:return subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT).returncode
buildcap.wait('RA-13 exact candidate quality '+fmt)
subprocess.run([sys.executable,str(O/'recipe/prepare_checks.py')],check=True)
run([FF,'-nostdin','-v','error','-y','-i',str(video),'-map','0:a:0','-c:a','pcm_s16le',str(D/'delivered-audio.wav')],'audio-extract.log')
assert json.load(open(O/'preservation.json'))['videos'][0]['audio_bit_identical']
assert (D/'speech.json').exists() and (D/'transcript.json').exists()
rc=run([sys.executable,str(SH/'audio/audio_gate.py'),str(video),'--untreated',str(O/'audio/mix.wav.audio_untreated.json'),'--ab',str(D/'Audio AB - reference then RA13.m4a')],'audio-gate.log')
print('AUDIO GATE',fmt,rc,flush=True)
subprocess.run([sys.executable,str(O/'recipe/prepare_checks.py')],check=True)
rc=run([sys.executable,str(SH/'deliver/watch.py'),str(video),'--plan',str(D/'watch-plan.json'),'--out',str(D/'watch-final'),'--log',str(D/'watch-final/logs/watch_pass.json')],'native-watch.log');assert rc==0
# Use the exact shared checks, normalizing only its decoder's canvas for a vertical.
man=json.load(open(O/f'hf-manifest{fmt}.json'))
for m in man:m['template']='analysis-card' if m['id']=='A1' else 'cta'
(D/'hf-manifest.json').write_text(json.dumps(man,indent=1))
code="import sys;sys.path.insert(0,sys.argv[1]);import checks;checks.C.WH=(1080,1920) if sys.argv[2]=='9' else (1920,1080);sys.argv=[sys.argv[0]]+sys.argv[3:];checks.main()"
rc=run([sys.executable,'-c',code,str(SH/'hyperframes'),fmt,str(D/'hf-manifest.json'),'--film',str(video),'--out',str(D/'hyperframes')],'hyperframes.log')
print('SHARED GRAPHICS CHECK',fmt,rc,'(generic template sampling; CTA face and analysis layout require actual inspection)',flush=True)
(D/'automatic-stage.json').write_text(json.dumps(dict(format=fmt,status='native evidence ready for human dispositions; delivery gate pending',audio_gate_rc=json.load(open(str(video)+'.audio_gate.json'))['verdict'],shared_graphics_rc=rc),indent=2))
print('QUALITY EVIDENCE READY',fmt,flush=True)
