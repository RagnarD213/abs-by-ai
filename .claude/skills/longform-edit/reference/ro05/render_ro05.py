"""RO-05 scene renderer (after Media/codex-video-trial/06-organic-r4/render_r3.py).
usage: render_ro05.py [start_s end_s]   -> PICTURE.mp4 (or review/sample-*.mp4)"""
import json,hashlib,subprocess,sys,os,time
from pathlib import Path
from PIL import Image
import ro05_gfx as G, muhammad_graphics as MG
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg";FPS=30000/1001
M="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/"
SCR="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4"
GRADE="colorchannelmixer=rr=0.984:gg=1.000:bb=1.017,curves=all='0/0 0.050/0.004 0.25/0.27 0.50/0.565 0.80/0.855 1/1'"
DEC="scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv"
BEATS=[(33.70,8.0),(48.96,24.0),(60.42,36.0),(66.32,41.0),(71.36,47.5),(74.60,53.0),(81.76,57.0),(86.94,63.0),(88.82,66.0),
       (100.86,78.0),(117.04,93.0),(146.50,121.0),(160.64,134.5),(172.58,138.0),(201.98,183.0),(237.96,214.5),(288.08,256.3),(299.58,270.0)]
def scr_t(cam):  # screen-recording time for a camera time: the 05 build's per-beat sync (longform-edit/reference/build_graded.py)
    cs,ss=max((b for b in BEATS if b[0]<=cam+0.3),key=lambda b:b[0]);return ss+(cam-cs)
TL=json.load(open('timeline.json'));P=TL['pieces'];FR=json.load(open('framing.json'));PLAN=json.load(open('gfx-plan.json'))
END_FR=round(4.0*FPS);TOTAL=P[-1]['out_f1']+END_FR
os.makedirs('cache',exist_ok=True);os.makedirs('layers',exist_ok=True);os.makedirs('logs',exist_ok=True);os.makedirs('review',exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
# ---- graphic layers -> immutable PNGs (content-addressed)
PLACE=json.load(open('placement.json')) if os.path.exists('placement.json') else {}
def build(g):
    k=g['kind'];pl=PLACE.get(g['key'])
    if pl and k in('keypoint','lower','number','solid','ingredient'):
        pos,ty=pl['pos'],pl['top_y']
        if k=='keypoint':return G.lower(g['text'],pos=pos,keypoint=True,top_y=ty)
        if k=='lower':return G.lower(g['text'],pos=pos,top_y=ty)
        if k=='number':return G.lower(g['text'],pos=pos,tab=g['num'],top_y=ty)
        if k=='solid':return G.solid(g['text'],pos=pos,top_y=ty)
        return G.ingredient(g['num'],g['text'],g.get('sub'),pos=pos,top_y=ty)
    if k=='keypoint':return G.lower(g['text'],pos=g.get('pos','bottom'),keypoint=True)
    if k=='lower':return G.lower(g['text'],pos=g.get('pos','bottom'))
    if k=='number':return G.lower(g['text'],pos=g.get('pos','bottom'),tab=g['num'])
    if k=='solid':return G.solid(g['text'])
    if k=='ingredient':return G.ingredient(g['num'],g['text'],g.get('sub'))
    if k=='speed':return G.speed(g['factor'])
    if k=='title':return G.title(g['text'])
    if k=='left-list':return G.left_list(g['text'],g['items'],[r-g['a'] for r in g['reveals']])
    raise ValueError(k)
LAY={}
def png(im):
    import io;b=io.BytesIO();im.save(b,'PNG');h=sha(b.getvalue())[:20];p=f'layers/{h}.png'
    if not os.path.exists(p):
        open(p+'.tmp','wb').write(b.getvalue());os.replace(p+'.tmp',p)
    return os.path.abspath(p)
for g in PLAN['graphics']:
    full,ls=build(g);LAY[g['key']]=dict(full=bool(full) and g['kind']=='title',layers=[dict(path=png(l['image']),start=g['a']+l['start'],motion=l['motion']) for l in ls])
bg_title=png(MG.gradient());grid=MG.grid();import numpy as np
from PIL import ImageDraw
mask=Image.new('L',grid.size,255);ImageDraw.Draw(mask).rounded_rectangle((160,150,1760,930),30,fill=0);grid.putalpha(mask);bg_frame=png(grid)
efull,el=G.endcard();end_png=png(el[0]['image'])
GPD="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/gopro 2/"
def gp_file(t):
    if t<1060.501333:return GPD+'GH010270.MP4',t
    if t<2121.002666:return GPD+'GH020270.MP4',t-1060.501333
    return GPD+'GH030270.MP4',t-2121.002666
_pb=MG.grid();_d=ImageDraw.Draw(_pb);_pw=round(1320*940/2500)
_d.rounded_rectangle(((1920-_pw)//2-16,54,(1920+_pw)//2+16,1026),34,fill=(8,9,10,255),outline=(142,150,121,255),width=3)
phone_bg=png(_pb)
# ---- scene boundaries
cuts={0,TOTAL}
for p in P:cuts|={p['out_f0'],p['out_f1']}
F=lambda t:round(t*FPS)
for g in PLAN['graphics']:cuts|={F(g['a']),F(g['b'])} if g['kind'] in('title',) else set()
for c in PLAN['cutaways']:cuts|={F(c['a']),F(c['b'])}
cuts=sorted(cuts);scenes=list(zip(cuts,cuts[1:]))
lim=None if len(sys.argv)<3 else (float(sys.argv[1]),float(sys.argv[2]))
receipt=[];t0=time.monotonic()
RENDER_VERSION='ro05-r1'   # bump when the encode settings change; inputs/filters are already in the key
NOG=bool(os.environ.get('NOGFX'))
for f0,f1 in scenes:
    ta,tb=f0/FPS,f1/FPS
    if lim and (tb<=lim[0] or ta>=lim[1]):continue
    n=f1-f0;inputs=[];filters=[];spec=dict(f0=f0,f1=f1)
    def add(path,still=False,ss=None):inputs.append(dict(path=path,still=still,ss=ss));return len(inputs)-1
    title=next((g for g in PLAN['graphics'] if g['kind']=='title' and F(g['a'])<=f0 and f1<=F(g['b'])),None)
    cutaway=next((c for c in PLAN['cutaways'] if F(c['a'])<=f0 and f1<=F(c['b'])),None)
    if f0>=P[-1]['out_f1']:
        add(end_png,True);filters.append('[0:v]format=rgba[v0]');spec['base']='endcard';active=[]
    elif title:
        dt=ta-title['a'];add(bg_title,True);add(bg_frame,True)
        filters.append(f"[0:v]scale=2016:1134,crop=1920:1080:x='48+42*sin((t+{dt:.4f})*.35)':y='27+23*cos((t+{dt:.4f})*.29)',format=rgba[vbg]")
        filters.append('[vbg][1:v]overlay=0:0:format=auto[v0]');spec['base']=('title',title['key']);active=[title]
    else:
        pi=next(i for i,p in enumerate(P) if p['out_f0']<=f0<p['out_f1']);p=P[pi];fr=FR[pi]
        if cutaway:
            sp=cutaway.get('speed',1);ss=cutaway['ss']+(ta-cutaway['a'])*sp
            spf=f"setpts=(PTS-STARTPTS)/{sp}" if sp!=1 else "setpts=PTS-STARTPTS"
            if cutaway['source']=='GP':
                gf,go=gp_file(ss);add(gf,ss=go)
                filters.append(f"[0:v]scale=in_color_matrix=bt601:in_range=pc:out_color_matrix=bt709:out_range=tv,crop=1280:720:320:0,scale=1920:1080:flags=lanczos,{GRADE},{spf},fps=30000/1001,format=rgba[v0]")
            elif cutaway['source']=='PHONE':
                add(phone_bg,True);sc=add(SCR,ss=scr_t(ss))
                dt=ta-cutaway['a'];L=cutaway['b']-cutaway['a']
                filters.append(f"[{sc}:v]crop=1320:2500:0:175,scale=-2:940:flags=lanczos,{spf},fps=30000/1001[ph];[0:v]format=rgba[bg];[bg][ph]overlay=(W-w)/2:70,scale=2016:1134,crop=1920:1080:x='48-40*(t+{dt:.4f})/{L:.4f}':y='27-22*(t+{dt:.4f})/{L:.4f}',format=rgba[v0]")
            else:
                add(M+cutaway['source']+'.MP4',ss=ss);cr=cutaway.get('crop')
                cc=f"crop={cr[2]}:{cr[3]}:{cr[0]}:{cr[1]},scale=1920:1080:flags=lanczos," if cr else ""
                filters.append(f"[0:v]{DEC},{cc}{GRADE},{spf},fps=30000/1001,format=rgba[v0]")
            spec['base']=('cut',cutaway['key'],round(ss,4))
        else:
            src_t=p['src_in']+(f0-p['out_f0'])/FPS*p['speed']
            crop=fr['crop']
            if p['source']=='C1541':
                cam=add(M+'C1541.MP4',ss=src_t);sc=add(SCR,ss=scr_t(src_t))
                cc=f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]},scale=1350:1080:flags=lanczos" if crop else "crop=1350:1080:375:0"
                filters.append(f"[{cam}:v]{DEC},{cc},{GRADE},setpts=PTS-STARTPTS,fps=30000/1001[d];[{sc}:v]crop=1320:2500:0:175,scale=570:1080:flags=lanczos,setpts=PTS-STARTPTS,fps=30000/1001[ph];[ph][d]hstack=inputs=2,format=rgba[v0]")
            else:
                add(M+p['source']+'.MP4',ss=src_t)
                cc=f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]},scale=1920:1080:flags=lanczos," if crop else ""
                sp=f"setpts=(PTS-STARTPTS)/{p['speed']}," if p['speed']!=1 else "setpts=PTS-STARTPTS,"
                filters.append(f"[0:v]{DEC},{cc}{GRADE},{sp}fps=30000/1001,format=rgba[v0]")
            spec['base']=('piece',pi,round(src_t,4),crop,p['speed'])
        active=[] if NOG else [g for g in PLAN['graphics'] if g['kind']!='title' and g['a']<tb and g['b']>ta]
    cur='v0';L=0
    for g in active:
        for l in LAY[g['key']]['layers']:
            idx=add(l['path'],True);st=l['start']-ta;mo=l['motion'];fac=[]
            endf=f"fade=t=out:st={max(0,g['b']-ta-.16):.4f}:d=0.16:alpha=1" if g['b']-ta<n/FPS+.05 else None
            if mo=='focus' and st>-.46:
                filters.append(f"[{idx}:v]format=rgba,split=2[l{L}b0][l{L}s0]")
                filters.append(f"[l{L}b0]gblur=sigma=12:steps=2,fade=t=in:st={max(0,st):.4f}:d=0.14:alpha=1,fade=t=out:st={max(0,st+.2):.4f}:d=0.28:alpha=1[l{L}b]")
                sh=[f"fade=t=in:st={max(0,st+.12):.4f}:d=0.34:alpha=1"]+([endf] if endf else [])
                filters.append(f"[l{L}s0]{','.join(sh)}[l{L}s]")
                filters.append(f"[{cur}][l{L}b]overlay=0:0:format=auto:enable='gte(t,{max(0,st):.4f})'[c{L}b]")
                filters.append(f"[c{L}b][l{L}s]overlay=0:0:format=auto:enable='gte(t,{max(0,st+.12):.4f})'[c{L}]");cur=f'c{L}';L+=1;continue
            if mo in('fade','slide'):
                fac=[f"fade=t=in:st={max(0,st):.4f}:d=0.3:alpha=1"] if st>=0 else ([f"fade=t=in:st=0:d={max(.001,.3+st):.4f}:alpha=1"] if st>-.3 else [])
            if mo=='wipe':fac=[f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='alpha(X,Y)*if(lte(X,60+1860*min(1,max(0,(T-({st:.4f})))/0.5)),1,0)'"]
            if mo=='wipe-wide':fac=[f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='alpha(X,Y)*if(lte(X,200+1600*min(1,max(0,(T-({st:.4f})))/0.55)),1,0)'"]
            if endf:fac.append(endf)
            filters.append(f"[{idx}:v]format=rgba"+(','+','.join(fac) if fac else '')+f"[l{L}]")
            filters.append(f"[{cur}][l{L}]overlay=0:0:format=auto:enable='gte(t,{max(0,st):.4f})'[c{L}]");cur=f'c{L}';L+=1
    filters.append(f"[{cur}]format=yuv420p[vout]")
    key=sha(json.dumps([spec,inputs,filters,RENDER_VERSION],sort_keys=True,default=str).encode())[:24]
    out=f'cache/{key}.mp4';ok=os.path.exists(out) and os.path.exists(out+'.ok')
    if not ok:
        cmd=[FF,'-nostdin','-y','-v','error']
        for q in inputs:
            cmd+=(['-loop','1','-framerate','30000/1001'] if q['still'] else ['-ss',f"{q['ss']:.5f}"])+['-i',q['path']]
        cmd+=['-filter_complex',';'.join(filters),'-map','[vout]','-an','-frames:v',str(n),'-c:v','libx264','-preset','fast','-crf','17','-threads','6',
              '-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-video_track_timescale','30000',out]
        json.dump(cmd,open(f'logs/{key}.cmd.json','w'))
        r=subprocess.run(cmd,capture_output=True,text=True)
        open(f'logs/{key}.log','w').write(r.stderr)
        if r.returncode or r.stderr.strip():
            print('SCENE ERROR',f0,f1,r.stderr[-600:]);
            if os.path.exists(out):os.remove(out)
            sys.exit(1)
        got=subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-count_packets','-select_streams','v','-show_entries','stream=nb_read_packets','-of','csv=p=0',out],capture_output=True,text=True).stdout.strip()
        if got!=str(n):
            print('SCENE ERROR frame count',f0,f1,'want',n,'got',got);os.remove(out);sys.exit(1)
        open(out+'.ok','w').write('ok')
    receipt.append(dict(f0=f0,f1=f1,path=os.path.abspath(out),base=spec['base']))
    print(f"{ta:8.2f}-{tb:8.2f} {'HIT ' if ok else 'BUILT'} {spec['base'] if isinstance(spec['base'],str) else spec['base'][0]}",flush=True)
tag=('PICTURE_NOGFX' if NOG else 'PICTURE') if not lim else f'review/sample-{lim[0]:g}-{lim[1]:g}'
open('cache/concat.txt','w').write(''.join(f"file '{r['path']}'\n" for r in receipt))
subprocess.run([FF,'-y','-v','error','-f','concat','-safe','0','-i','cache/concat.txt','-c','copy','-movflags','+faststart',tag+'.mp4'],check=True)
json.dump(dict(scenes=receipt,total_frames=TOTAL,elapsed=time.monotonic()-t0),open(tag+'.receipt.json','w'),indent=0)
print('WROTE',tag+'.mp4',len(receipt),'scenes',round(time.monotonic()-t0),'s')
