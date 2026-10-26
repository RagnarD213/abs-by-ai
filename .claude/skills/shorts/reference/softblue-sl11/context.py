import sys,json,subprocess,os,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/hyperframes'))
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/renderq'))
import composite as HC,renderq
FF=str(ROOT/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;N=180
MASTER=str(ROOT/'claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.mp4')
WORDS=json.loads(Path('/Volumes/Extreme/_edit_work/ro02/words_out.json').read_text())
FONT=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',86)
ITEMS=json.loads((R/'items.json').read_text())
previous={z['id']:z for z in json.loads((R/'items-context.json').read_text())} if (R/'items-context.json').exists() else {}
for z in ITEMS:
    for k in ['context','context_parent_start','context_frames']:
        if k in previous.get(z['id'],{}):z[k]=previous[z['id']][k]
for it in ITEMS:
    if os.environ.get('ONLY') and it['id'] not in os.environ['ONLY'].split(','):continue
    out=R/'review/context'/f"{it['id']}-context.mp4"
    if out.exists():print('EXISTS',out.name,flush=True);continue
    with renderq.slot('Vacuum asset context '+it['id'],pool='quick',group='SL-11'):
        N={'A-step2':114,'B-recover':150}.get(it['id'],180)
        s=it['source'];sh=s['shot'];a=max(sh['out_f0']/FPS,min(it['t']-2,sh['out_f1']/FPS-N/FPS));a=round(a*FPS)/FPS
        a=round({'A-step2':455.088,'B-recover':579.012}.get(it['id'],a)*FPS)/FPS
        raw=(sh['src_f0']+round(a*FPS)-sh['out_f0'])/FPS
        x,y,w,h=it['crop'];vf=s['vf']+f',crop={w}:{h}:{x}:{y},scale=1080:1610:flags=lanczos,format=rgb24'
        cp=subprocess.Popen([FF,'-nostdin','-v','error','-ss',str(raw),'-i',s['source'],'-frames:v',str(N),'-vf',vf,'-f','rawvideo','-'],stdout=subprocess.PIPE)
        tp=HC.reader(str(R/'hf/renders'/f"TITLE-{it['short']}.mov"),n=N,rgba=False,wh=(1080,310))
        ov=HC.reader(str(R/'hf/renders'/f"{it['id']}.mov"),n=N,rgba=True,wh=(1080,1920)) if it['topic'] else None
        mk=HC.reader(str(R/'hf/renders'/f"{it['id']}_mask.mov"),n=N,rgba=True,wh=(1080,1920)) if it['topic'] else None
        enc=subprocess.Popen([FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate','30000/1001','-i','-','-ss',str(a),'-i',MASTER,'-map','0:v:0','-map','1:a:0','-frames:v',str(N),'-t',str(N/FPS),'-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','320k','-ar','48000','-ac','2','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
        ws=[dict(w=z['w'],a=z['t0']-a,b=(z.get('t1') or z['t0']+.12)-a) for z in WORDS if z.get('t0') is not None and a<=z['t0']<a+N/FPS]
        cues=[]
        j=0
        while j<len(ws):
            take=2 if it.get('cap_top',1412)>=1650 else 3
            ss=ws[j:j+take]
            # Lower captions remain one line, above y1750; long two-word pairs split naturally.
            while it.get('cap_top',1412)>=1650 and len(ss)>1 and ImageDraw.Draw(Image.new('RGB',(1,1))).textlength(' '.join(z['w'] for z in ss),font=FONT)>950:ss=ss[:-1]
            cues.append((ss[0]['a'],ss[-1]['b'],' '.join(z['w'] for z in ss)));j+=len(ss)
        proof=R/'qa'/it['id'];proof.mkdir(parents=True,exist_ok=True);edges=[]
        try:
            for n in range(N):
                b=cp.stdout.read(1080*1610*3)
                if len(b)!=1080*1610*3:raise RuntimeError((it['id'],'camera short read',n))
                frame=np.empty((1920,1080,3),np.uint8);frame[:310]=next(tp);frame[310:]=np.frombuffer(b,np.uint8).reshape(1610,1080,3)
                # Independent of the person mask: record possible dark hair at the picture's top edge on every frame.
                roi=frame[310:330,390:690];edges.append(float((roi.mean(2)<65).mean()))
                if ov is not None:
                    frame=HC.glass(frame,next(mk),[it['graphic']['band'][0],it['graphic']['band'][1]]);frame=HC.over(frame,next(ov))
                im=Image.fromarray(frame);d=ImageDraw.Draw(im)
                text=next((s for ca,cb,s in cues if ca<=n/FPS<cb),'')
                if text:
                    tw=d.textlength(text,font=FONT)
                    if tw>950:
                        zz=text.split();ls=[' '.join(zz[:-1]),zz[-1]]
                    else:ls=[text]
                    for k,ln in enumerate(ls):d.text(((1080-d.textlength(ln,font=FONT))/2,it.get('cap_top',1412)+k*96),ln,font=FONT,fill='white',stroke_width=7,stroke_fill='black')
                if n%7==0:im.save(proof/f'f{n:04d}.png')
                enc.stdin.write(im.tobytes())
        finally:
            cp.stdout.close();cp.wait();enc.stdin.close();rc=enc.wait()
            tp.close()
            if ov is not None:ov.close();mk.close()
        if rc:raise RuntimeError(('encode failed',rc))
        it['context']='context/'+out.name;it['context_parent_start']=a;it['context_frames']=N
        (proof/'edge.json').write_text(json.dumps(dict(all_frames=N,max_dark_share=max(edges),values=edges),indent=1))
        (R/'items-context.json').write_text(json.dumps(ITEMS,indent=2))
        print('CONTEXT',it['id'],a,flush=True)
