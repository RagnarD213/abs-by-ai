from pathlib import Path
import time,json,sys,subprocess
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');A=json.loads((W/'assembly.json').read_text());sha=A['sha256']
while True:
 try:
  r=json.loads((W/'audit/report.json').read_text());f=json.loads((W/'audit/findings.json').read_text())
  if (r.get('sha256') or r.get('master_sha256') or r.get('video_sha256'))==sha:break
 except (FileNotFoundError,json.JSONDecodeError):pass
 time.sleep(3)
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap;buildcap.wait('Bill Maher R4 final exact-file gate')
p=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),'--judge',str(W/'watch/watch_pass.json'),'--findings',str(W/'audit/findings.json'),'--by','Independent GPT-6 Sol high, full-candidate and repair review'],capture_output=True,text=True);(W/'watch-judgment.log').write_text(p.stdout+p.stderr);print(p.stdout,flush=True)
g=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),A['master'],'--format','organic9x16','--plan',str(W/'delivery-plan.json')],stdout=open(W/'delivery-gate-final.log','w'),stderr=subprocess.STDOUT);print('FINAL GATE ACTUAL EXIT',g.returncode,flush=True)
(W/'final-gate-complete.json').write_text(json.dumps({'sha256':sha,'watch_judge_exit':p.returncode,'delivery_gate_exit':g.returncode,'independent_verdict':r.get('verdict')},indent=2))
