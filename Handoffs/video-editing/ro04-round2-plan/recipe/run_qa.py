from pathlib import Path
import sys,subprocess
import build as B
sys.path.insert(0,str(B.P/'.claude/skills/_shared'));import buildcap
buildcap.wait('Arms Shoulders R2 QA')
def run(args,log):
 with (B.W/'qa'/log).open('w') as f:
  r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
 print(log,'exit',r.returncode,flush=True)
 return r.returncode
py=sys.executable;m=B.W/'Arms Shoulders Workout LFC R2 - first minute.mp4'
assert run([py,str(B.W/'recipe/qa_prepare.py')],'prepare.log')==0
assert run([py,str(B.W/'recipe/preservation.py')],'preservation.log')==0
assert run([py,str(B.W/'recipe/crop_audit.py')],'crop-audit.log')==0
assert run(['zsh',str(B.P/'.claude/skills/_shared/audio/selftest.sh')],'audio-selftest.log')==0
assert run([py,str(B.P/'.claude/skills/_shared/audio/audio_gate.py'),str(m),'--reference-mix',str(B.W/'audio/reference-Arms Shoulders Workout LFC R2 - first minute.m4a'),'--verbatim','--ab',str(B.W/'audio/round2-audio-AB.mp4')],'audio-gate.log')==0
assert run([py,str(B.P/'.claude/skills/_shared/deliver/watch.py'),str(m),'--plan',str(B.W/'qa/plan.json'),'--out',str(B.W/'qa/watch'),'--log',str(B.W/'qa/watch/watch_pass.json'),'--clips'],'watch.log')==0
run([py,str(B.P/'.claude/skills/_shared/deliver/gate.py'),str(m),'--format','longform','--plan',str(B.W/'qa/plan.json'),'--json',str(B.W/'qa/delivery-gate-initial.json')],'delivery-initial.log')
print('QA evidence ready for independent review',flush=True)
