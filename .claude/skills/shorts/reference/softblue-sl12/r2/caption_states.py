"""Export genuine transparent libass caption states; video pixels/audio remain untouched."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=Path('/Volumes/Extreme/_edit_work/SL-12/round2');G=R/'qa/B';P=G/'plan.json';j=json.loads(P.read_text());D=G/'caption-states-alpha';D.mkdir(exist_ok=True);FPS=30000/1001
states=j['caption_states'];frames=[round(sum(x['beat'])/2*FPS) for x in states];select='+'.join(f'eq(n,{n})' for n in frames)
vf=f"format=rgba,colorchannelmixer=aa=0,select='{select}',ass='{j['captions_ass']}':alpha=1"
subprocess.run([str(ROOT/'Media/video_edit/bin/ffmpeg'),'-v','error','-y','-f','lavfi','-i',f'color=black@0:s=1080x1920:r=30000/1001:d={j["target_seconds"]}','-vf',vf,'-vsync','0',str(D/'cap%03d.png')],check=True)
paths=sorted(D.glob('cap*.png'));assert len(paths)==len(states);proof=[]
for s,p in zip(states,paths):
 im=Image.open(p);a=im.getchannel('A');assert a.getextrema()==(0,255),(p,a.getextrema());box=a.getbbox();assert box and box[1]>=1380 and box[3]<1700,(p,box)
 s['image']=str(p);s['image_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();proof.append(dict(image=str(p),sha256=s['image_sha256'],alpha_extrema=[0,255],ink_bbox=list(box),beat=s['beat']))
P.write_text(json.dumps(j,indent=2)+'\n');(G/'caption-alpha-evidence.json').write_text(json.dumps(dict(video_sha256=j['evidence_contract']['video_sha256'],method='Same actual libass ASS; explicit zero alpha before subtitle render; selected original PTS states. Old opaque-alpha diagnostic images retained separately.',states=proof),indent=2)+'\n');print('TRANSPARENT_CAPTION_STATES',len(proof),flush=True)
