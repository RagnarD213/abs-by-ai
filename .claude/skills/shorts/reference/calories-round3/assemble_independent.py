from pathlib import Path
import sys
P=Path(__file__).parent
sys.path[:0]=[str(P),'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared']
import batch as B, buildcap, cap_local, cv2
B.cv2=cv2
for s in 'BCE':
 buildcap.wait('Calories Shorts R3 independent '+s)
 B.cmd_render(s)
print('Independent Shorts B C E assembled; final verification remains',flush=True)
