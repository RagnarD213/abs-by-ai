import sys,subprocess
import build as B
sys.path.insert(0,str(B.P/'.claude/skills/_shared'));import buildcap
buildcap.wait('Arms Shoulders R2 final exact-file gate')
rc=subprocess.run([sys.executable,'-u',str(B.P/'.claude/skills/_shared/deliver/gate.py'),str(B.W/'Arms Shoulders Workout LFC R2 - first minute.mp4'),'--format','longform','--plan',str(B.W/'qa/plan.json'),'--json',str(B.W/'qa/delivery-gate-result.json')]).returncode
raise SystemExit(rc)
