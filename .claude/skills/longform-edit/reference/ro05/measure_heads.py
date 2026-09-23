"""Per camera piece: face centre + hair top (Vision person mask in the head band), 3 samples."""
import sys,json,subprocess,os,numpy as np
sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
from deliver.checks import framing as F
from PIL import Image
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg";M="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/"
PM="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
P=json.load(open('timeline.json'))['pieces'];fm,fd=F._facemesh(),F._facefinder()
os.makedirs('heads',exist_ok=True);out={};jobs=[]
for i,p in enumerate(P):
    if p['source']=='C1541':continue
    ts=[p['src_in']+f*p['src_dur'] for f in (0.05,0.25,0.5,0.75,0.95)]
    for k,t in enumerate(ts):
        fn=f"heads/{p['source']}_{t:.2f}.png"
        if not os.path.exists(fn):subprocess.run([FF,'-nostdin','-v','error','-y','-ss',f'{t:.3f}','-i',M+p['source']+'.MP4','-frames:v','1',fn])
        jobs.append((f"{p['source']}@{round(p['src_in'],2)}",k,fn))
todo=[j[2] for j in jobs if not os.path.exists('heads/m/'+os.path.basename(j[2])[:-4]+'.mask.png')]
for q in range(0,len(todo),150):subprocess.run([PM,'heads/m']+todo[q:q+150],capture_output=True)
for i,k,fn in jobs:
    fr=np.asarray(Image.open(fn).convert('RGB'))
    Pp=F._find_face(fm,fd,fr,1920,1080)
    mp='heads/m/'+os.path.basename(fn)[:-4]+'.mask.png'
    rec=dict(face=Pp is not None)
    if Pp is not None:
        cx=(Pp[234][0]+Pp[454][0])/2;fw=abs(Pp[454][0]-Pp[234][0]);fore,chin=Pp[10][1],Pp[152][1]
        rec.update(cx=float(cx),fw=float(fw),fore=float(fore),chin=float(chin))
        if os.path.exists(mp):
            m=np.asarray(Image.open(mp).convert('L'),np.float32)/255
            b0,b1=int(max(0,cx-0.35*fw)),int(min(1920,cx+0.35*fw))
            rows=np.where((m[:,b0:b1]>0.5).mean(1)>0.3)[0]
            rows=rows[rows<chin]
            rec['top']=int(rows[0]) if len(rows) else None
    out.setdefault(i,[]).append(rec)
json.dump(out,open('heads_by_src.json','w'),indent=0)
n=sum(1 for v in out.values() if any(r.get('face') for r in v));print(len(out),'pieces measured,',n,'with a face')
