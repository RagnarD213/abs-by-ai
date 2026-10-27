"""All-frame preservation comparison, not independent scene-content approval."""
from pathlib import Path
import sys,json,hashlib,os
import numpy as np
W=Path(__file__).resolve().parents[1];B=W.parent/'round2';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import composite as C
v=sys.argv[1];src=B/'review/media'/f'dad-bod-r2-{v}.mp4';out=W/'review/media'/f'dad-bod-r3-{v}.mp4';rows=[];means=[]
for g,(a,b) in enumerate(zip(C.reader(str(src),wh=(1080,1920)),C.reader(str(out),wh=(1080,1920)))):
 if 284<=g<485 or (v=='scripted' and 973<=g<1058):continue
 x=a[::4,::4].astype(np.float32)-b[::4,::4].astype(np.float32);m=float(np.mean(x*x));psnr=99 if not m else float(10*np.log10(255**2/m));means.append(float(np.mean(np.abs(x))));rows.append((g,psnr))
n=json.loads((W/v/'edl.json').read_text())['total_frames'];assert g+1==n
rec=dict(video_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),baseline_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),scope='Preservation proof ONLY: all unchanged timeline frames compared to locked reviewed R2. Independent R1 components and fresh exact-file scene review still required.',decoded_frames=g+1,unchanged_frames_compared=len(rows),minimum_psnr_db=min(x[1] for x in rows),median_psnr_db=float(np.median([x[1] for x in rows])),mean_absolute_rgb_delta=float(np.mean(means)),worst_frames=sorted(rows,key=lambda x:x[1])[:12],changed_intervals_frames=[[284,485]]+([[973,1058]] if v=='scripted' else []))
p=W/'qa'/v/'preservation.json';p.write_text(json.dumps(rec,indent=1));print(v,'UNCHANGED_PICTURE_PRESERVATION',rec['minimum_psnr_db'],rec['mean_absolute_rgb_delta'],flush=True)
