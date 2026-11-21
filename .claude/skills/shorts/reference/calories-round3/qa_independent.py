from pathlib import Path
import sys,subprocess
P=Path(__file__).parent;W=P.parent
R='/Users/danielrose/Documents/Claude/Projects/Abs By AI'
sys.path[:0]=[str(P),R+'/.claude/skills/_shared']
import buildcap,cap_local,deliver as D,plans
# Every exact MP4 gets a fresh audio stamp, delivered-audio transcript, native watch evidence, and full gate.
buildcap.wait('Calories R3 audio selftest')
r=subprocess.run(['zsh',R+'/.claude/skills/_shared/audio/selftest.sh'],stdout=open(W/'audit/audio-selftest.log','w'),stderr=subprocess.STDOUT)
assert r.returncode==0, 'audio selftest failed; retain report'
for s in 'BCE':
 buildcap.wait('Calories R3 QA '+s)
 d=Path(D.Bt.D(s));v=d/(plans.NAME[s]+'.mp4');g=d/'gate';g.mkdir(exist_ok=True)
 subprocess.run(['python3',R+'/.claude/skills/_shared/audio/audio_gate.py',str(v),'--reference-mix',str(d/'his_mix.wav'),'--verbatim','--ab',str(W/'review'/f'{s}-audio-AB.mp4')],check=True)
 D.transcript(s,str(v));D.plan(s)
 subprocess.run(['python3',R+'/.claude/skills/_shared/deliver/watch.py',str(v),'--plan',str(g/'plan.json'),'--out',str(g/'watch'),'--log',str(g/'logs/watch_pass.json')],check=True)
 print('WATCH READY',s,flush=True)
print('QA evidence ready for independent judgement',flush=True)
