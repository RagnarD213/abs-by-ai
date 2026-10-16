from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');mask=R/'.claude/skills/shorts/reference/recentre/personmask';rows=json.load(open(O/'framing.json'));dest=O/'preflight/head-mask';dest.mkdir(exist_ok=True)
paths=[O/f'preflight/{s["name"]}-source.png' for s in rows if s['format']=='9']
subprocess.run([str(mask),str(dest)]+[str(p) for p in paths],stdout=subprocess.DEVNULL,check=True)
out=[]
for s in rows:
 if s['format']!='9':continue
 p=O/f'preflight/{s["name"]}-source.png';a=np.array(Image.open(dest/(p.stem+'.mask.png')).convert('L'))>127;cx=s['exact_landing_head_x'];x0,x1=round(cx-240),round(cx+240);y0,y1=round(s['min_hair']-20),round(s['landmarks']['chin']);reg=a[y0:y1,x0:x1];ys,xs=np.where(reg);counts=reg.sum(0);occupied=np.where(counts>4)[0];left,right=x0+int(occupied.min()),x0+int(occupied.max());center=(left+right)/2;cw,ch=s['crop'];im=Image.open(p).convert('RGB');im.crop((round(center-cw/2),s['y'],round(center+cw/2),s['y']+ch)).resize((1080,1920)).save(O/f'preflight/{s["name"]}-head-silhouette-preview.jpg')
 out.append(dict(name=s['name'],face_mesh_center=cx,whole_head_center=center,head_box=[left,y0,right,y1],correction_source_px=round(center-cx,2),method='Shared Vision person mask: whole head silhouette from hair through chin, including ears. First delivered source frame; visible-head centering separate from pose-dependent cheek landmarks.'))
(O/'head-silhouette-measurements.json').write_text(json.dumps(out,indent=2));print('WHOLE HEAD MEASUREMENTS',out,flush=True)
