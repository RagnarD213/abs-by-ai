from pathlib import Path
import json,sys,subprocess,hashlib,math
from PIL import Image,ImageDraw
import numpy as np,cv2
W=Path('/Volumes/Expansion/_edit_work/DS-35/round3');v=sys.argv[1];q=W/'qa'/v;out=W/'independent'/v;FPS=30000/1001;s=json.loads((q/'caption-states.json').read_text());states=s['states'];picks={round(sum(x['beat'])/2*FPS):i for i,x in enumerate(states)};N=json.loads((q/'plan.json').read_text())['target_frames'];F='/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg';vid=W/'review/media'/('dad-bod-r3-'+v+'.mp4');proc=subprocess.Popen([F,'-v','error','-i',str(vid),'-an','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE);rows=[];cells=[];onsetrows=[];onsets={math.ceil(x['beat'][0]*FPS-1e-7):i for i,x in enumerate(states)}
for g in range(N):
 b=proc.stdout.read(1080*1920*3);assert len(b)==1080*1920*3
 if g not in picks and g not in onsets:continue
 i=picks.get(g,onsets.get(g));st=states[i];im=np.frombuffer(b,np.uint8).reshape(1920,1080,3);exp=np.asarray(Image.open(st['image']).convert('RGBA'));x0,y0,x1,y1=st['ink_bbox'];x0=max(0,x0-8);x1=min(1080,x1+8);y0=max(0,y0-8);y1=min(1920,y1+8)
 a=exp[y0:y1,x0:x1];r=im[y0:y1,x0:x1];ink=(a[:,:,:3].mean(2)>200)&(a[:,:,3]>220);actual=r[ink];white=np.mean((actual.min(1)>170)&(actual.max(1)-actual.min(1)<65)) if len(actual) else 0
 if g in onsets:onsetrows.append(dict(cue=i,g=g,t=g/FPS,text=st['cue_text'],white_ink_fraction=float(white)))
 if g not in picks:continue
 rows.append(dict(cue=i,g=g,t=g/FPS,text=st['cue_text'],image=st['image'],hash_valid=hashlib.sha256(Path(st['image']).read_bytes()).hexdigest()==st['image_sha256'],white_ink_fraction=float(white),bbox=st['ink_bbox']))
 cell=Image.new('RGB',(540,145),(30,36,45));d=ImageDraw.Draw(cell);d.text((4,2),f'{i}: {g/FPS:.3f} {st["cue_text"]}',fill='white');rr=Image.fromarray(r).resize((min(532,round(r.shape[1]*.55)),round(r.shape[0]*.55)));cell.paste(rr,(4,25));ee=Image.fromarray(a);ee.thumbnail((532,50));cell.paste(ee,(4,90),ee);cells.append(cell)
assert proc.wait()==0
for a in range(0,len(cells),24):
 seq=cells[a:a+24];sheet=Image.new('RGB',(3*540,8*145))
 for i,c in enumerate(seq):sheet.paste(c,(i%3*540,i//3*145))
 sheet.save(out/f'caption-contact-{a//24:02d}.jpg')
(out/'caption-independent.json').write_text(json.dumps(dict(video_sha256=hashlib.sha256(vid.read_bytes()).hexdigest(),scope='Every exact libass cue raster hash checked and actual native decoded midpoint white-ink pixels measured; contact sheets show actual upper crop and exact raster below. Whole chunk display not per-word highlight.',required=len(states),checked=len(rows),native_onsets_checked=len(onsetrows),onset_rows=onsetrows,min_onset_white_ink=min(r['white_ink_fraction'] for r in onsetrows),min_white_ink=min(r['white_ink_fraction'] for r in rows),rows=rows),indent=1));print('CAPTIONS',len(rows),min(r['white_ink_fraction'] for r in rows))
