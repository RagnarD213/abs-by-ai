import subprocess,time,sys
from pathlib import Path
W=Path(__file__).parent;ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(ROOT/'.claude/skills/_shared'));import buildcap
for i in range(300):
 if 'DONE' in (W/'key-render.log').read_text():break
 time.sleep(2)
else:raise RuntimeError('key did not complete')
buildcap.wait("Codex green screen sample")
for args in [('natural',),('warm',),('bright',),('natural','dark')]:
 subprocess.run([sys.executable,str(W/'finish.py'),*args],check=True)
print('FINISH DONE',flush=True)
