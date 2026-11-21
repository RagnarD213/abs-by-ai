from pathlib import Path
import subprocess,sys,json
P=Path(__file__).parent;W=P.parent;R='/Users/danielrose/Documents/Claude/Projects/Abs By AI'
sys.path[:0]=[str(P),R+'/.claude/skills/_shared']
import buildcap,cap_local,plans
for S in (sys.argv[1:] or list('BCE')):
 buildcap.wait('Calories R3 full delivery gate '+S)
 d=W/'build'/S;v=d/(plans.NAME[S]+'.mp4');g=d/'gate';g.mkdir(exist_ok=True)
 r=subprocess.run(['python3',R+'/.claude/skills/_shared/deliver/gate.py',str(v),'--format','short','--plan',str(g/'plan.json')],stdout=open(g/'delivery-first.log','w'),stderr=subprocess.STDOUT)
 print('GATE FINISHED',S,r.returncode,flush=True)
