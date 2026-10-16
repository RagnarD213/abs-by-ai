from pathlib import Path
import subprocess,sys
O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3')
for n in ['framing.py','build_media.py']:
 print('STAGE',n,flush=True)
 subprocess.run([sys.executable,str(O/'recipe'/n)],check=True)
print('PREFLIGHT COMPONENTS COMPLETE. EDITOR VISUAL REVIEW BEFORE ASSEMBLY.',flush=True)
