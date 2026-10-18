from pathlib import Path
import sys,subprocess,json
import numpy as np
from PIL import Image,ImageDraw
import build as B
sys.path.insert(0,str(B.P/'.claude/skills/_shared'));import buildcap
buildcap.wait('Arms Shoulders R2 full-action crop audit')
W=B.W;D=W/'qa/crop-dense';D.mkdir(exist_ok=True)
# Internal sampled QA frames only, no full-film assembly.
if not (D/'f0383.jpg').exists():subprocess.run([B.FF,'-v','error','-ss',str(B.START),'-i',B.RAW,'-t',str(B.REST),'-vf','fps=4,crop=1776:1000:100:0,scale=960:540','-q:v','2','-y',str(D/'f%04d.jpg')],check=True)
files=sorted(D.glob('f*.jpg'));M=D/'masks';tool=B.P/'.claude/skills/shorts/reference/recentre/personmask'
for i in range(0,len(files),120):
 if not all((M/(p.stem+'.mask.png')).exists() for p in files[i:i+120]):subprocess.run([str(tool),str(M)]+list(map(str,files[i:i+120])),check=True,stdout=subprocess.DEVNULL)
rows=[];invalid=[]
for i,p in enumerate(files):
 m=np.asarray(Image.open(M/(p.stem+'.mask.png')).convert('L'))>128
 # Any subject silhouette includes raised hands and dumbbells when recognized.
 ys,xs=np.where(m)
 if not len(ys): invalid.append({'t':i/4,'file':str(p),'reason':'Vision returned an empty silhouette; requires visual review'});continue
 rows.append({'t':i/4,'top_before1080':int(ys.min()*2),'top_after1080':round(ys.min()*2-19.44,2),'left1080':int(xs.min()*2),'right1080':int(xs.max()*2),'bottom1080':int(ys.max()*2)})
v={'method':'Apple Vision full-body masks, every 0.25 s across all 95.8497 s of source action. Before is x100 y0 1776x1000; after y18, unchanged scale. Mask top is any foreground, including weights, not a hairline detector. Native edge samples and matching stills additionally inspected.','total_frames':len(files),'invalid_samples':invalid,'samples':len(rows),'fixed_shift1080':19.44,'min_foreground_top_before':min(x['top_before1080'] for x in rows),'min_foreground_top_after':min(x['top_after1080'] for x in rows),'standing_median_top_before':float(np.median([x['top_before1080'] for x in rows if 6<=x['t']<35])),'rows':rows}
v['standing_median_top_after']=v['standing_median_top_before']-19.44
v['standing_headroom_reduction_percent']=19.44/v['standing_median_top_before']*100
(W/'qa/crop-audit.json').write_text(json.dumps(v,indent=2))
worst=sorted(rows,key=lambda x:x['top_after1080'])[:6];samples=[(int(x['t']*4),x['t']) for x in worst]+[(i/0.25,int(i)) for i in []]
# Contact sheets every second across complete action; shifted edges overlaid for review.
for z in range(0,len(files),100):
 subset=files[z:z+100:4];sheet=Image.new('RGB',(1600,25//5*195),(8,16,24))
 for k,p in enumerate(subset):
  im=Image.open(p).resize((320,180));draw=ImageDraw.Draw(im);draw.line((0,3.24,320,3.24),fill='red',width=2);draw.text((6,8),f'{(int(p.stem[1:])-1)/4:.2f}s',fill='white',stroke_fill='black',stroke_width=1);sheet.paste(im,((k%5)*320,(k//5)*195))
 sheet.save(W/f'qa/crop-contact-{z//100}.jpg',quality=92)
print({k:v for k,v in v.items() if k!='rows'},flush=True)
