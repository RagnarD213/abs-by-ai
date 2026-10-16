from pathlib import Path
import sys,json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
import mediapipe as mp
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
FF=str(R/'Media/video_edit/bin/ffmpeg');F=30000/1001;r=json.load(open(O/'build-record.json'));P=O/'native-proof';P.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
buildcap.wait('RA13 R3 native scene and landing proof')
mesh=mp.solutions.face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,min_detection_confidence=.4)
report={}
for fmt,wh in [('9',(1080,1920)),('16',(1920,1080))]:
 v=next((O/'final').glob('[!._]*'+('9x16' if fmt=='9' else '16x9')+'*.mp4'));land={s['f0']:s['name'] for s in r['slots'] if s['piece'] is not None};sw=json.load(open(O/f'phone-layout{fmt}.json'))['switch_full_frame'];targets={0,67,68,429,430,sw-2,sw-1,sw,sw+1,sw+2,753,754,849,850,932,1011,1012,1071,1072,1167,1168,1276,1277,1395,1396,1540,1558,1611,1612,1613,1614,1615};targets|=set(land)
 rd=subprocess.Popen([FF,'-v','error','-i',str(v),'-vf','scale=in_color_matrix=bt709:in_range=tv,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE);n=0;imgs={};positions=[];unit=wh[0]*wh[1]*3
 while True:
  raw=rd.stdout.read(unit)
  if not raw:break
  assert len(raw)==unit
  if n in targets:
   im=Image.frombytes('RGB',wh,raw);im.save(P/f'{fmt}-f{n}.jpg');imgs[n]=im
   if fmt=='9' and n in land:
    a=np.array(im);roi=a[0:720,150:930];res=mesh.process(np.ascontiguousarray(roi));assert res.multi_face_landmarks,(n,'no face mesh');lm=res.multi_face_landmarks[0].landmark;cx=150+(lm[234].x+lm[454].x)/2*780
    positions.append(dict(name=land[n],frame=n,t=n/F,rendered_head_center=round(cx,2),error_px=round(cx-540,2),chin_y=lm[152].y*720,image=str(P/f'{fmt}-f{n}.jpg')))
  n+=1
 rd.stdout.close();assert rd.wait()==0 and n==1616
 
 if fmt=='9':
  md=P/'head-mask';md.mkdir(exist_ok=True);subprocess.run([str(R/'.claude/skills/shorts/reference/recentre/personmask'),str(md)]+[q['image'] for q in positions],stdout=subprocess.DEVNULL,check=True)
  for q in positions:
   a=np.array(Image.open(md/(Path(q['image']).stem+'.mask.png')).convert('L'))>127;region=a[:round(q['chin_y']),100:980];occupied=np.where(region.sum(0)>4)[0];left,right=100+int(occupied.min()),100+int(occupied.max());q.update(whole_head_bounds=[left,right],whole_head_center=(left+right)/2,whole_head_error_px=(left+right)/2-540)
 report[fmt]=dict(path=str(v),sha256=sha(v),frames_sequentially_decoded=n,geometry=wh,landings=positions)
 for name,ns in [('opening',[0,67,68]),('phone-cut',[sw-2,sw-1,sw,sw+1,sw+2]),('scene-check',[430,753,850,932,1011,1012,1072,1167]),('returns',[754,1168,1277,1396]),('ending',[1540,1558,1611,1612,1613,1614,1615])]:
  width=360;h=round(wh[1]*width/wh[0]);sheet=Image.new('RGB',(width*len(ns),h+30));d=ImageDraw.Draw(sheet)
  for i,k in enumerate(ns):sheet.paste(imgs[k].resize((width,h)),(i*width,30));d.text((i*width+5,5),f'f{k} {k/F:.3f}s',fill='white')
  sheet.save(P/f'{fmt}-{name}.jpg')
(P/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:dict(frames=v['frames_sequentially_decoded'],landings=v['landings']) for k,v in report.items()},indent=2),flush=True)
