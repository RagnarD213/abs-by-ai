from pathlib import Path
import os,sys,json,shutil,subprocess
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Extreme/_edit_work/ra13/round2');sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
D=R/'Codex Ad Videos/why do most guys never get abs - RA-13';V=R/'Videos to Review';P=O/'review';D.mkdir(exist_ok=True,parents=True);P.mkdir(exist_ok=True);V.mkdir(exist_ok=True);FF=str(R/'Media/video_edit/bin/ffmpeg')
for fmt,label in [('9x16','vertical'),('16x9','horizontal')]:
 src=next((O/'final').glob('*'+fmt+'*.mp4'));dst=D/src.name;shutil.copy2(src,dst);shutil.copy2(src,V/f'Most Guys Abs AD R2 - {label}.mp4');shutil.copy2(src,P/f'Most Guys Abs AD R2 - {fmt}.mp4')
 buildcap.wait('RA13 '+fmt+' review exports')
 out=P/f'Most Guys Abs AD R2 - {fmt} - REVIEW540p.mp4';subprocess.run([FF,'-nostdin','-v','error','-y','-i',str(src),'-vf','scale=540:960' if fmt=='9x16' else'scale=960:540','-c:v','libx264','-preset','fast','-crf','23','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],check=True);shutil.copy2(out,D/out.name)
 for name,a,b in [('P1',13,27),('A1',27,35),('P2',32.5,40),('CTA',49,53.920533)]+([('headroom',1,7)] if fmt=='16x9' else[]):
  out=P/f'{name}-{fmt}-context.mp4';subprocess.run([FF,'-nostdin','-v','error','-y','-i',str(src),'-ss',str(a),'-t',str(b-a),'-vf','scale=540:960' if fmt=='9x16' else'scale=960:540','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],check=True)
print('REVIEW EXPORTS COMPLETE',flush=True)
