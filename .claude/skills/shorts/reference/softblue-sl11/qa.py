import sys,json,subprocess,hashlib,os
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
R=Path(__file__).resolve().parents[1];ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(ROOT/'.claude/skills/_shared'))
import softblue_titlecheck as TC
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/renderq'));import renderq
PM=str(ROOT/'.claude/skills/shorts/reference/recentre/personmask');FB=str(Path.home()/'.cache/absbyai/facebox');FF=str(ROOT/'Media/video_edit/bin/ffmpeg')
items=[x for x in json.loads((R/'items-context.json').read_text()) if x.get('context')];cached={x['id']:x for x in json.loads((R/'context-qa.json').read_text()).get('items',[])} if (R/'context-qa.json').exists() else {};report={'stage':'asset contexts only; not final delivery gates','items':[]}
for it in items:
    if os.environ.get('ONLY') and it['id'] not in os.environ['ONLY'].split(','):continue
    video=R/'review'/it['context'];sha=hashlib.sha256(video.read_bytes()).hexdigest()
    if cached.get(it['id'],{}).get('sha256')==sha:
        report['items'].append(cached[it['id']]);print('CACHED',it['id'],flush=True);continue
    d=R/'qa-exact'/it['id'];d.mkdir(parents=True,exist_ok=True)
    for old_sample in d.glob('f*.png'):old_sample.unlink()
    with renderq.slot('Vacuum exact context QA '+it['id'],pool='quick',group='SL-11'):
        # Decode this exact single-resolution export, at 29.97 native rate, then sample every seventh frame (<0.25 s).
        cp=subprocess.Popen([FF,'-nostdin','-v','error','-i',str(video),'-vf','scale=in_color_matrix=bt709:in_range=tv,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
        edges=[];paths=[];n=0
        while True:
            b=cp.stdout.read(1080*1920*3)
            if not b:break
            assert len(b)==1080*1920*3
            frame=np.frombuffer(b,np.uint8).reshape(1920,1080,3)
            edges.append(int((frame[310:330,390:690].mean(2)<65).sum()))
            if n%7==0:
                p=d/f'f{n:04d}.png';Image.fromarray(frame).save(p);paths.append(p)
            n+=1
        cp.stdout.close();assert cp.wait()==0;assert n==it['context_frames'],(it['id'],n)
        subprocess.run([PM,str(d/'m')]+list(map(str,paths)),check=True,capture_output=True)
        fbs={}
        for line in subprocess.run([FB]+list(map(str,paths)),check=True,capture_output=True,text=True).stdout.splitlines():
            p,b=line.split('\t');fbs[p]=b
        rows=[]
        for p in paths:
            m=np.asarray(Image.open(d/'m'/f'{p.stem}.mask.png'))>127;m[:310]=False
            lab,num=ndimage.label(m)
            if not num:raise RuntimeError(('unresolved person detection',p))
            labid=1+np.argmax(ndimage.sum(m,lab,range(1,num+1)));mask=lab==labid
            rr=np.where(mask.sum(1)>=20)[0]
            if not len(rr):raise RuntimeError(('unresolved hair sample',p))
            hair=int(rr[0]);face=fbs[str(p)];bottom=int(face.split()[3]) if face not in ['none','error'] else None
            rows.append(dict(frame=int(p.stem[1:]),hair_y=hair,clearance=hair-310,face_bottom=bottom))
        low=min(x['clearance'] for x in rows)
        if low<20:raise RuntimeError(('hair clearance',it['id'],low))
        if it['topic']:
            bad=[x for x in rows if x['face_bottom'] is None or x['face_bottom']>=1110]
            if bad:raise RuntimeError(('unresolved face/graphic clearance',it['id'],bad))
        title=TC.frame_report(str(video))
        # Full template text lives above the picture and has a real two-pixel separator.
        if title.get('verdict') not in ['OK']:raise RuntimeError(('title band unresolved',title))
        row=dict(id=it['id'],file=str(video),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),frames=n,hair_samples=rows,min_hair_clearance=low,top_edge_every_frame_dark_pixels=edges,title=title)
        report['items'].append(row);(R/'context-qa.json').write_text(json.dumps(report,indent=2))
        print(it['id'],'hair min',low,'title',title.get('verdict'),'edge max',max(edges),flush=True)
(R/'context-qa.json').write_text(json.dumps(report,indent=2))
print('EXACT CONTEXT CHECKS COMPLETE',flush=True)
