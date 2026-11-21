from pathlib import Path
import subprocess,json,sys,math,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];E=W/'evidence';F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;V=W/'review/Home Workouts SFC R2 - 1080p.mp4'
p=json.load(open(E/'plan.json'));h=hashlib.sha256(V.read_bytes()).hexdigest();assert h==p['evidence_contract']['video_sha256']
sys.path.insert(0,str(R/'.claude/skills/_shared'));from deliver.checks.captions import read_cues
cues=read_cues(p['captions_ass']);mids=[math.ceil((a+b)*.5*FPS) for a,b,t in cues];ids=sorted(set(mids+[0,1,2,1838,1839,1840]+[max(0,min(1840,round(t*FPS)+d)) for t in p['joins'] for d in [-2,-1,0,1,2]]+[round(t*FPS) for t in np.arange(0,61.4,1)]));select='+'.join(f'eq(n,{n})' for n in ids)
proc=subprocess.Popen([F,'-v','error','-nostdin','-i',str(V),'-vf',f"select='{select}',scale=540:960:in_color_matrix=bt709:in_range=tv",'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE);frames={}
for n in ids:
 data=proc.stdout.read(540*960*3);assert len(data)==540*960*3,n;frames[n]=Image.frombytes('RGB',(540,960),data)
assert proc.wait()==0
for batch in range(math.ceil(len(cues)/24)):
 out=Image.new('RGB',(1620,8*195),'#172638');draw=ImageDraw.Draw(out)
 for i,(a,b,t) in enumerate(cues[batch*24:(batch+1)*24]):
  k=batch*24+i;n=mids[k];x=i%3*540;y=i//3*195;out.paste(frames[n].crop((0,610,540,785)),(x,y+20));draw.text((x+5,y+3),f'C{k+1:03} f{n} {a:.2f}-{b:.2f} {t}',fill='white')
 out.save(E/f'captions-all-{batch+1}.jpg',quality=95)
for n in [0,1,2,1838,1839,1840]:frames[n].save(E/f'endpoint-{n}.jpg',quality=96)
chron=Image.new('RGB',(6*270,11*500),'#172638');draw=ImageDraw.Draw(chron)
for i,n in enumerate([round(t*FPS) for t in np.arange(0,61.4,1)]):
 x=i%6*270;y=i//6*500;chron.paste(frames[n].resize((270,480)),(x,y+20));draw.text((x+5,y+3),f'{n/FPS:.2f}s / f{n}',fill='white')
chron.save(E/'whole-film-chronology.jpg',quality=95)
# Independent every-native-frame top-edge diagnostic. No sample/threshold is called a gate PASS.
proc=subprocess.Popen([F,'-v','error','-nostdin','-i',str(V),'-vf','crop=480:24:300:0','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE);rows=[];n=0
while True:
 data=proc.stdout.read(480*24*3)
 if len(data)<480*24*3:break
 if any(a['beat'][0]<=n/FPS<a['beat'][1] for a in p['talking_head_windows']):
  im=np.frombuffer(data,np.uint8).reshape(24,480,3);lum=im@np.array([.2126,.7152,.0722]);rows.append(dict(n=n,t=n/FPS,dark_pixels=int((lum<45).sum()),minimum_luma=float(lum.min())))
 n+=1
assert proc.wait()==0 and n==1841
(E/'native-top-edge-diagnostic.json').write_text(json.dumps(dict(sha256=h,frames_decoded=n,presenter_frames=len(rows),method='Native every-frame central 480x24 top band; raw luma diagnostic for visual reconciliation; source-specific threshold45, no independent delivery gate or segmentation PASS implied.',rows=rows),indent=2))
print('SELF_QA_EVIDENCE',h,len(cues),'caption images;',n,'native frames;',len(rows),'presenter edges',flush=True)
