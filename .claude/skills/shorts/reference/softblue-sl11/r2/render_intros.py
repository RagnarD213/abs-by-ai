from pathlib import Path
import json,subprocess,hashlib,sys,os
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path('/Volumes/Extreme/_edit_work/SL-11/round2'); OLD=R.parent/'round1'; ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');FF=str(ROOT/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
LIB=Path('/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed');ALT=next(LIB.glob('B0428*.mp4'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):Path(p).write_text(json.dumps(v,indent=2))
def reader(path,n,start=0,vf=None):
 args=[FF,'-v','error','-threads','1','-filter_threads','1','-ss',str(start),'-i',str(path),'-frames:v',str(n)]
 if vf:args+=['-vf',vf]
 args+=['-pix_fmt','rgb24','-f','rawvideo','-'];return subprocess.Popen(args,stdout=subprocess.PIPE)
def frame(p,w=1080,h=1920):
 b=p.stdout.read(w*h*3);assert len(b)==w*h*3,len(b);return np.frombuffer(b,np.uint8).reshape(h,w,3).copy()
(R/'review/media').mkdir(parents=True,exist_ok=True);(R/'build').mkdir(exist_ok=True);(R/'sources').mkdir(exist_ok=True)
# Both cache files are new. Do not mutate originals, LUTs or approved master.
manifest=[]
for S,N in [('A',271),('B',345),('C',151)]:
 d=OLD/'build'/S; intro=180 if S=='B' else 75
 for option in [1,2]:
  id=f'{S}{option}';out=R/'review/media'/f'{id}-intro-context.mp4';bd=R/'build'/id;bd.mkdir(exist_ok=True)
  if out.exists():raise RuntimeError('Resume must explicitly verify existing output before skipping: '+str(out))
  base=reader(d/f'Vacuum-{S}-R1.mp4',N)
  if option==1:src=reader(OLD/'build/A/source_picture.mp4',intro,660/FPS,'crop=1080:1610:0:310')
  else:src=reader(ALT,intro,54/FPS,'crop=724:1080:550:0,scale=1080:1610:flags=lanczos,eq=contrast=1.04:brightness=0.005:gamma=1.08:saturation=1.08')
  tmp=bd/'picture.mp4';args=[FF,'-v','error','-y','-threads','1','-filter_threads','1','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30000/1001','-i','-','-frames:v',str(N),'-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-crf','19','-preset','fast','-threads',os.environ.get('RENDERQ_CORES','4'),'-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(tmp)]
  enc=subprocess.Popen(args,stdin=subprocess.PIPE);cues=json.loads((d/'cues.json').read_text());caps={c['f0']:Image.open(c['png']).convert('RGBA') for c in cues if c['f0']<intro};font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30)
  # Excerpt B ends before the next So/you. Remove unheard next words from that excerpt's last cue only.
  lastcap=None
  if S=='B':
   lastcap=Image.new('RGBA',(1080,1920));dr=ImageDraw.Draw(lastcap);f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',86);s='unnecessarily.';dr.text(((1080-dr.textlength(s,font=f))/2,1412),s,font=f,fill='white',stroke_width=7,stroke_fill='black')
  for n in range(N):
   fr=frame(base)
   if n<intro:
    fr[310:]=frame(src,h=1610);im=Image.fromarray(fr);dr=ImageDraw.Draw(im);dr.text((64,1800),'AbsByAI.com',font=font,fill=(244,250,255),stroke_width=1,stroke_fill=(5,13,28))
    for c in cues:
     if c['f0']<=n<c['f1']:
      im.paste(caps[c['f0']],(0,0),caps[c['f0']]);break
    fr=np.array(im)
   if S=='B' and n>=318:
    # Original frame carries the old line, so reconstruct this last presenter section from the clean cache.
    # Filled separately below with a clean-cache reader rather than painted over source pixels.
    pass
   enc.stdin.write(fr.tobytes())
  for p in [base,src]:p.stdout.close();assert p.wait()==0
  enc.stdin.close();assert enc.wait()==0
  if S=='B':
   # Avoid changing a valid prior caption: shorten B context to just before its last grouped cue begins.
   # 318f=10.6106 ends before unnecessarily; instead complete phrase at345 needs excerpt-only text repair.
   clean=reader(d/'source_picture.mp4',N);base2=reader(tmp,N);fixed=bd/'picture-edge-fixed.mp4';args[-1]=str(fixed);enc2=subprocess.Popen(args,stdin=subprocess.PIPE)
   for n in range(N):
    fr=frame(base2);cl=frame(clean)
    if n>=318:
     im=Image.fromarray(cl);dr=ImageDraw.Draw(im);dr.text((64,1800),'AbsByAI.com',font=font,fill=(244,250,255),stroke_width=1,stroke_fill=(5,13,28));im.paste(lastcap,(0,0),lastcap);fr=np.array(im)
    enc2.stdin.write(fr.tobytes())
   for p in [base2,clean]:p.stdout.close();assert p.wait()==0
   enc2.stdin.close();assert enc2.wait()==0;tmp=fixed
  # Copy AAC packets from exact R1 reviewed mix. No voice chain or re-encoding.
  subprocess.run([FF,'-v','error','-y','-i',str(tmp),'-i',str(d/f'Vacuum-{S}-R1.mp4'),'-map','0:v','-map','1:a','-c','copy','-t',str(N/FPS),'-movflags','+faststart',str(out)],check=True)
  row=dict(id=id,short=S,option=option,file=str(out),sha256=sha(out),frames=N,seconds=N/FPS,intro_frames=intro,intro_end=intro/FPS,presenter_return=intro/FPS,source=str(OLD/'build/A/source_picture.mp4') if option==1 else str(ALT),source_start=660/FPS if option==1 else 54/FPS,source_end=(660+intro)/FPS if option==1 else(54+intro)/FPS,source_sha256=sha(OLD/'build/A/source_picture.mp4') if option==1 else sha(ALT),action='Existing clip: clear held contraction, no new draw-in' if option==1 else'Real B0428: exhale/bend, visible draw-in, hold',audio='AAC packet copy of R1 reviewed full export',caption_endpoint_repair='B last cue: unnecessarily. only; unheard So you removed' if S=='B' else None)
  manifest.append(row);dump(R/'intro-manifest.json',manifest);print('RENDERED',id,N,flush=True)
