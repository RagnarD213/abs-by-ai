import sys,os,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import mediapipe as mp
W=Path(__file__).resolve().parents[1];os.chdir(W);R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('RA-13 source framing measurements')
FF=str(R/'Media/video_edit/bin/ffmpeg');roll=json.load(open('source/roll.json'))['identity']['current_path']
grade=json.load(open('grade-options.json'))['B']['filter']
C=json.load(open('cut.json'));out=[]
fd=mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=.4)
fm=mp.solutions.face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,min_detection_confidence=.4)
mask=str(R/'.claude/skills/shorts/reference/recentre/personmask')
for pi,p in enumerate(C['pieces'][:2]):
 d=W/f'track/p{pi}';d.mkdir(parents=True,exist_ok=True)
 subprocess.run([FF,'-v','error','-y','-ss',str(p['src_in']),'-i',roll,'-t',str(p['src_out']-p['src_in']),'-vf',grade+",select='not(mod(n,6))',scale=1080:1920",'-vsync','0',str(d/'f%04d.png')],check=True)
 paths=sorted(d.glob('f*.png'));md=d/'mask';md.mkdir(exist_ok=True)
 subprocess.run([mask,str(md)]+[str(x) for x in paths],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 for k,path in enumerate(paths):
  a=np.asarray(Image.open(path).convert('RGB'));fr=fm.process(a);P=None
  if fr.multi_face_landmarks:
   lm=fr.multi_face_landmarks[0].landmark;P={i:(lm[i].x*1080,lm[i].y*1920) for i in [10,152,234,454]}
  if P is None:
   r=fd.process(a)
   if r.detections:
    b=r.detections[0].location_data.relative_bounding_box;cx=(b.xmin+b.width/2)*1080;cy=(b.ymin+b.height/2)*1920;s=max(b.width*1080,b.height*1920)*2.2;x0,y0=int(max(0,cx-s/2)),int(max(0,cy-s/2));x1,y1=int(min(1080,cx+s/2)),int(min(1920,cy+s/2));fr=fm.process(np.ascontiguousarray(a[y0:y1,x0:x1]));
    if fr.multi_face_landmarks:
     lm=fr.multi_face_landmarks[0].landmark;P={i:(lm[i].x*(x1-x0)+x0,lm[i].y*(y1-y0)+y0) for i in [10,152,234,454]}
  if P is None:continue
  cx=(P[234][0]+P[454][0])/2;fw=abs(P[234][0]-P[454][0]);m=np.asarray(Image.open(md/(path.stem+'.mask.png')).convert('L'))>127
  cols=m[:,int(cx-.4*fw):int(cx+.4*fw)].mean(1);ids=np.where(cols>.2)[0]
  if not len(ids):continue
  hair=float(ids[0]);chin=P[152][1];climb=(P[10][1]-hair)/(chin-P[10][1])
  if not .10<=climb<=.60:continue
  out.append(dict(piece=pi,t=p['t_in']+k*6/(30000/1001),src=p['src_in']+k*6/(30000/1001),cx=cx*2,hair=hair*2,chin=chin*2,frame=k))
 print('piece',pi,'measured',sum(x['piece']==pi for x in out),'of',len(paths),flush=True)
json.dump(out,open('track-look.json','w'),indent=1)
print('TRACK READY',len(out),flush=True)

subprocess.run([sys.executable,str(W/"recipe/look_sample_render.py")],check=True)
