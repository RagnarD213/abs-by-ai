from pathlib import Path
import json,subprocess,shutil,hashlib
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');D=R/'Codex Ad Videos/why do most guys never get abs - RA-13';P=O/'review';V=R/'Videos to Review';FF=str(R/'Media/video_edit/bin/ffmpeg')
import sys;sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
for fmt,label in [('9x16','vertical'),('16x9','horizontal')]:
 src=next((O/'final').glob('[!._]*'+fmt+'*.mp4'));shutil.copy2(src,D/src.name);shutil.copy2(src,V/f'Most Guys Abs AD R3 - {label}.mp4');shutil.copy2(src,P/f'Most Guys Abs AD R3 - {fmt}.mp4')
 buildcap.wait('RA13 R3 review copies '+fmt)
 def encode(out,a=None,b=None):
  cmd=[FF,'-nostdin','-v','error','-y','-i',str(src)]
  if a is not None:cmd+=['-ss',str(a),'-t',str(b-a)]
  subprocess.run(cmd+['-vf','scale=540:960' if fmt=='9x16' else 'scale=960:540','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],check=True)
 out=P/f'Most Guys Abs AD R3 - {fmt} - REVIEW540p.mp4';encode(out);shutil.copy2(out,D/out.name)
 for name,a,b in [('P1',13,27),('A1',27,35),('centering',0,6),('CTA',49,53.920533)]:encode(P/f'{name}-{fmt}-context.mp4',a,b)
print('REVIEW COPIES PACKAGED',flush=True)
