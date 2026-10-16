from pathlib import Path
import sys,json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
import mediapipe as mp
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');B=W/'round2';SH=R/'.claude/skills/_shared';sys.path[:0]=[str(SH),str(SH/'cut')];import buildcap,landing
FF=str(R/'Media/video_edit/bin/ffmpeg');F=30000/1001
rec=json.load(open(B/'build-record.json'));oc=json.load(open(W/'cut.json'));T=json.load(open(B/'track-all.json'));grade=json.load(open(W/'grade-options.json'))['B']['filter'];roll=json.load(open(W/'source/roll.json'))['identity']['current_path']
# Measure head in a face crop, so detection cannot confuse body pose with head center.
mesh=mp.solutions.face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,min_detection_confidence=.4)
def head(im):
 a=np.array(im);x0,y0,x1,y1=650,1220,1500,1800;roi=np.ascontiguousarray(a[y0:y1,x0:x1]);res=mesh.process(roi)
 if not res.multi_face_landmarks:raise RuntimeError('Exact head missing')
 lm=res.multi_face_landmarks[0].landmark;left=x0+lm[234].x*(x1-x0);right=x0+lm[454].x*(x1-x0)
 return (left+right)/2, dict(left=left,right=right,forehead=y0+lm[10].y*(y1-y0),chin=y0+lm[152].y*(y1-y0))
def expr(ni,x,cw):
 e=str(float(x[-1])-cw/2)
 for j in range(len(ni)-2,-1,-1):
  a,b=int(ni[j]),int(ni[j+1]);xa,xb=float(x[j])-cw/2,float(x[j+1])-cw/2;e=f'if(lt(n,{b}),{xa:.4f}+({xb-xa:.4f})*(n-{a})/{max(1,b-a)},{e})'
 return e
buildcap.wait('RA13 R3 vertical framing')
out=[]
for s in rec['slots']:
 if s['piece'] is None:continue
 old=next(x for x in rec['framing'] if x['format']=='9' and x['name']==s['name']);src0=old['src0'];n=old['n'];cw,ch=old['crop'];y=old['y'];img=O/f'preflight/{s["name"]}-source.png'
 if not img.exists():subprocess.run([FF,'-v','error','-y','-ss',str(src0),'-i',roll,'-vf',grade,'-frames:v','1',str(img)],check=True)
 face_cx,lm=head(Image.open(img).convert('RGB'));cx=next(q['whole_head_center'] for q in json.load(open(O/'head-silhouette-measurements.json')) if q['name']==s['name']);vals=[q for q in T if q['piece']==s['piece']];ns=np.array([q['frame']*6 for q in vals]);
 def full_head(q):
  mpth=B/f'track/p{s["piece"]}/mask/f{q["frame"]+1:04d}.mask.png';a=np.array(Image.open(mpth).convert('L'))>127;xc=q['cx']/2;x0,x1=round(xc-120),round(xc+120);y0,y1=round(q['hair']/2-10),round(q['chin']/2);reg=a[y0:y1,x0:x1];occupied=np.where(reg.sum(0)>4)[0];assert len(occupied),mpth;return (2*x0+int(occupied.min())+int(occupied.max()))
 rx=np.array([full_head(q) for q in vals]);off=round((src0-oc['pieces'][s['piece']]['src_in'])*F)
 use=np.arange(0,n,6);raw=np.interp(use+off,ns,rx);raw[0]=cx
 ni,x,info=landing.vertical_track(use,raw,[dict(n0=0,n1=n)],cw,F);info.update(landing.motion_stats(ni,np.interp(ni,use,raw),x,[dict(n0=0,n1=n)],cw,F))
 assert abs(x[0]-cx)<.001
 assert min(x-cw/2)>=0 and max(x+cw/2)<=2160
 vf=grade+f",crop={cw}:{ch}:'{expr(ni,x,cw)}':{y},scale=1080:1920:flags=lanczos,setsar=1"
 dst=O/f'seg9/{s["name"]}.mp4'
 subprocess.run([FF,'-v','error','-y','-ss',str(src0),'-i',roll,'-vf',vf,'-frames:v',str(n),'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv',str(dst)],check=True)
 q={**old,'motion':info,'path':str(dst),'exact_landing_head_x':cx,'face_mesh_center':face_cx,'centering_method':'Whole visible head silhouette, hair through chin including ears; dense mask centers, shared landing.vertical_track.','landmarks':lm,'track':{'n':ni.tolist(),'crop_center':x.tolist(),'head':np.interp(ni,use,raw).tolist()}};out.append(q)
 subprocess.run([FF,'-v','error','-y','-i',str(dst),'-frames:v','1',str(O/f'preflight/{s["name"]}-landing.png')],check=True)
 print(s['name'],'EXACT LANDING',round(cx,2),info,flush=True)
out.extend([{**x,'path':str(O/f'seg16/{x["name"]}.mp4'),'reuse':'byte-identical R2 horizontal segment'} for x in rec['framing'] if x['format']=='16'])
(O/'framing.json').write_text(json.dumps(out,indent=2));print('FRAMING READY',flush=True)
# Independent rendered components in moving narration context before full assembly.
for fmt in ['9','16']:
 for name,a,b in [('P1',14.3476666667,25.1584666667),('A1',28.3616666667,33.7670666667)]:
  src=O/f'media/P1-{fmt}.mp4' if name=='P1' else O/f'hf{fmt}/renders/A1.mov';baseline=next((B/'final').glob('[!._]*'+('9x16' if fmt=='9' else '16x9')+'*.mp4'));dst=O/f'preflight/{name}-{fmt}-narrated.mp4'
  vf='scale=in_color_matrix=bt709:in_range=tv' if name=='P1' else 'scale=in_color_matrix=bt601:in_range=tv'
  vf+=',scale=540:960' if fmt=='9' else ',scale=960:540'
  subprocess.run([FF,'-v','error','-y','-i',str(src),'-ss',str(a),'-i',str(baseline),'-map','0:v','-map','1:a:0','-vf',vf,'-t',str(b-a),'-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-movflags','+faststart',str(dst)],check=True)
  if name=='A1':
   for t in [1,3,5]:subprocess.run([FF,'-v','error','-y','-ss',str(t),'-i',str(src),'-vf','scale=in_color_matrix=bt601:in_range=tv','-frames:v','1',str(O/f'preflight/A1-{fmt}-{t}.jpg')],check=True)
print('NARRATED COMPONENT PREFLIGHTS READY',flush=True)
