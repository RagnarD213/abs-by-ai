from pathlib import Path
import sys,subprocess
P=Path(__file__).parent;W=P.parent;R='/Users/danielrose/Documents/Claude/Projects/Abs By AI';sys.path[:0]=[str(P),R+'/.claude/skills/_shared']
import buildcap,cap_local,lib,plans
O=W/'review/candidates';O.mkdir(exist_ok=True,parents=True)
for S in 'BCE':
 buildcap.wait('Calories R3 review encode '+S)
 v=W/f'build/{S}'/(plans.NAME[S]+'.mp4')
 subprocess.run([lib.FF,'-nostdin','-v','error','-y','-i',str(v),'-vf','scale=540:960','-c:v','h264_videotoolbox','-b:v','1800k','-c:a','copy','-movflags','+faststart',str(O/f'{S}-review.mp4')],check=True)
print('REVIEW ENCODES READY',flush=True)
