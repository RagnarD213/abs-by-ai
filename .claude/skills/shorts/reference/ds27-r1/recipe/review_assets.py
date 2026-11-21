from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageDraw
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];Q=W/'review';F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;shots=json.load(open(W/'shots.json'));edl=json.load(open(W/'edl.json'))
items=[('B0431','Opening',5.0,0),('G01','Opening',10.6,0),('G02','Opening',22.5,0),('E01','Equipment-context',29.6,round(24.2*FPS)/FPS),('E02','Equipment-context',31.8,round(24.2*FPS)/FPS),('E03','Equipment-context',33.7,round(24.2*FPS)/FPS),('E04','Equipment-context',37.2,round(24.2*FPS)/FPS),('A0157','Daily-workouts-context',55.6,next(s['n0'] for s in shots if s['id']=='T09')/FPS)]
for id,name,t,offset in items:
 subprocess.run([F,'-v','error','-nostdin','-y','-ss',str(t-offset),'-i',str(Q/(name+' - 1080p.mp4')),'-frames:v','1',str(Q/(id+'.jpg'))],check=True)
sheet=Image.new('RGB',(1440,1530),'#102136');d=ImageDraw.Draw(sheet)
for i,(id,*_) in enumerate(items):
 im=Image.open(Q/(id+'.jpg')).resize((360,640));x=i%4*360;y=i//4*760;sheet.paste(im,(x,y+30));d.text((x+15,y+8),id,fill='white')
sheet.save(W/'evidence/asset-composite-sheet.jpg',quality=95)
# Exact first/last six native frames of each excerpt, plus a hash binding.
rows=[]
for name in ['Opening','Equipment-context','Daily-workouts-context']:
 src=Q/(name+' - 1080p.mp4');probe=json.loads(subprocess.check_output([str(R/'Media/video_edit/bin/ffprobe'),'-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(src)]));n=int(probe['streams'][0]['nb_frames']);out=W/'evidence'/(name+'-endpoints.jpg')
 vf=f"select='lt(n,6)+gte(n,{n-6})',scale=180:320,tile=6x2";subprocess.run([F,'-v','error','-nostdin','-y','-i',str(src),'-vf',vf,'-frames:v','1',str(out)],check=True);rows.append(dict(file=str(src),sha256=hashlib.sha256(src.read_bytes()).hexdigest(),native_frames=n,endpoint_sheet=str(out)))
(W/'evidence/endpoint-manifest.json').write_text(json.dumps(rows,indent=2))
