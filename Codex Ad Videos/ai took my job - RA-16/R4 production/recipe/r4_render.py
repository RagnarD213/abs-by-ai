#!/usr/bin/env python3
"""AD. Isolated RA16 R4 assembly of hash-locked R3 components, no publishing."""
import os,sys,json,hashlib,subprocess,time,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
W=Path('/Volumes/Extreme/_edit_work/ra16'); O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra16/round4')
SH=R/'.claude/skills/_shared';sys.path[:0]=[str(SH),str(SH/'cut'),str(R/'scripts/video')]
import buildcap,landing,hyperframes_graphics as HG
from motionlib import font as caption_font
FF=str(R/'Media/video_edit/bin/ffmpeg');FP=FF.replace('ffmpeg','ffprobe');FPS=30000/1001;N=1765;D=N/FPS
CUT=json.load(open(W/'round2/cut.json'));WORDS=json.load(open(W/'round2/words_out.json'));PLAN=json.load(open(W/'round2/plan_resolved.json'))
SRC=json.load(open(W/'source/roll.json'))['identity']['current_path'];SPEED=CUT['speed']
GRADE='scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709,lut3d=file=/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.45.cube:interp=tetrahedral,eq=saturation=1.12:gamma=1.03'
for d in ['measure','plates','audio','masters','review','evidence','logs','hf9','hf16','captions']:(O/d).mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,indent=2))
def run(cmd,**kw):return subprocess.run(list(map(str,cmd)),check=True,**kw)
def probe(p):return json.loads(subprocess.check_output([FP,'-v','error','-show_streams','-show_format','-of','json',str(p)]))
def segments():
 out=[]
 for p in CUT['pieces']:
  a=round(p['t_in']*FPS);b=round(p['t_out']*FPS)
  if p['id']=='P03':b=581
  spans=[(a,b)]
  for q0,q1 in [(578,725),(757,983)]:
   # P03's 578-580 picture continues from its own original source.
   if p['id']=='P03' and q0==578:q0=581
   nxt=[]
   for x,y in spans:
    if x<q0:nxt.append((x,min(y,q0)))
    if y>q1:nxt.append((max(x,q1),y))
   spans=[(x,y) for x,y in nxt if y>x]
  for a,b in spans:
   if b>a:out.append(dict(id=p['id'],n0=a,n1=min(N,b),framing=p['framing'],src0=p['src_in']+(a/FPS-p['t_in'])*SPEED))
 return out
SEGS=segments()
def preflight():
 a=json.load(open(W/'round3/round4-plan/decisions.json'));assert a['full_assembly_authorized'] and not a['remaining_asset_approvals']
 checks=[]
 for x in a['protected_inputs']:
  h=sha(x['path']);assert h==x['sha256'],x['path'];checks.append(dict(x,actual=h))
 assert Path(SRC).stat().st_size==json.load(open(W/'source/roll.json'))['identity']['size_bytes']
 for aspect,folder,wh in [('9x16','hf9',[1080,1920]),('16x9','hf16',[1920,1080])]:
  mf=json.load(open(W/'round2'/folder/'manifest.json'))
  mf.append(dict(id='D01',template='app-demo',a=19.402,b=24.193,mov=str(W/'round3'/f'DEMO-{aspect}-CLEAN.mp4'),kind='opaque'))
  for m in mf:
   for k in ['mov','mask']:
    if k not in m:continue
    meta=probe(m[k]);v=next(x for x in meta['streams'] if x['codec_type']=='video');assert [v['width'],v['height']]==wh,(m['id'],wh,v)
    assert int(v['nb_frames'])>=round(m['b']*FPS)-round(m['a']*FPS)
    checks.append({'path':m[k],'sha256':sha(m[k]),'role':m['id']+' '+k,'dimensions':wh,'frames':v['nb_frames']})
  write(O/folder/'manifest.json',mf)
 words=[dict(w,frame0=math.ceil(w['t0']*FPS-1e-8),frame1=math.ceil(w['t1']*FPS-1e-8)) for w in WORDS]
 assert max(w['t1'] for w in words)<D
 write(O/'words-native.json',words);write(O/'picture-segments.json',SEGS)
 write(O/'preflight.json',{'passed':True,'checks':checks,'frames':N,'fps':'30000/1001','duration':D,'last_word_end':max(w['t1'] for w in WORDS),'native_segments':SEGS,'new_asset_selection':False,'source':'C1668 original read-only; approved R3 components unchanged'})
 print('PREFLIGHT PASS',len(checks),'inputs',flush=True)
def measure():
 import mediapipe as mp
 fd=mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=.4)
 segmodel=mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)
 PM=SH.parent/'shorts/reference/recentre/personmask';reports=[]
 for s in SEGS:
  d=O/'measure'/f"{s['id']}-{s['n0']}";d.mkdir(exist_ok=True)
  nf=s['n1']-s['n0'];indices=sorted(set(list(range(0,nf,6))+[nf-1]));expr='+'.join(f'eq(n,{n})' for n in indices)
  if not (d/'measure.json').exists():
   vf=GRADE+f',setpts=(PTS-STARTPTS)/{SPEED},fps=30000/1001,trim=end_frame={nf},select=\'{expr}\',scale=540:960'
   run([FF,'-v','error','-y','-ss',s['src0'],'-i',SRC,'-t',((nf/FPS)+.15)*SPEED,'-vf',vf,'-vsync','0',d/'f%04d.png'])
   files=sorted(d.glob('f*.png'));assert len(files)==len(indices),(s,len(files),len(indices));vals=[]
   for n,f in zip(indices,files):
    ar=np.array(Image.open(f).convert('RGB'));det=fd.process(ar);assert det.detections,(s,n)
    b=max(det.detections,key=lambda x:x.score[0]).location_data.relative_bounding_box
    cx=(b.xmin+b.width/2)*540;fore=b.ymin*960;fh=b.height*960
    # Use actual silhouette, not an estimated hair offset from a face box.
    x0=max(0,int(cx-1.1*fh));x1=min(540,int(cx+1.1*fh));y1=min(960,int(fore+1.25*fh))
    crop=ar[:y1,x0:x1];cpath=d/f'head{n:04}.png';Image.fromarray(crop).save(cpath)
    m=segmodel.process(crop).segmentation_mask;b0=max(0,int(cx-.32*b.width*540-x0));b1=min(x1-x0,int(cx+.32*b.width*540-x0))
    z=np.where((m[:,b0:b1]>.65).mean(1)>=.20)[0]
    vals.append(dict(n=n,g=s['n0']+n,cx=cx*4,fore=fore*4,face_h=fh*4,head_crop=str(cpath),b0=b0,b1=b1,hair_mp=(float(z[0])*4 if len(z) else None)))
   run([PM,d/'masks']+[x['head_crop'] for x in vals],stdout=subprocess.DEVNULL)
   for v in vals:
    path=d/'masks'/(Path(v['head_crop']).stem+'.mask.png');m=np.array(Image.open(path).convert('L'))/255
    z=np.where((m[:,v['b0']:v['b1']]>.65).mean(1)>=.20)[0];assert len(z),(s,v['n'])
    v['hair_vision']=float(z[0])*4
   write(d/'measure.json',vals)
  vals=json.load(open(d/'measure.json'));ns=np.array([x['n'] for x in vals]);cx=np.array([x['cx'] for x in vals]);hair=min(min(x['hair_mp'],x['hair_vision']) for x in vals if x['hair_mp'] is not None)
  # Same crop dimensions and approved vertical placement recipe, now using measured silhouettes.
  crops={}
  for aspect in ['9x16','16x9']:
   near=s['framing']=='near';cw,ch=((612,1088) if near else (800,1422)) if aspect=='9x16' else ((1728,972) if near else (2160,1216))
   prior=json.load(open(W/'round2/track.json'))[s['id']]
   approved_y=max(0,int(min(v['hair'] for v in prior)-ch*.06)//2*2)
   # Preserve approved placement unless actual silhouettes prove hair needs more clearance.
   y=min(approved_y,max(0,int(hair-ch*.04)//2*2))
   if aspect=='9x16':
    dn,dx,heads,info=landing.vertical_dense(ns,cx,[{'n0':0,'n1':nf}],cw,FPS)
    info.update(landing.motion_stats(dn,np.interp(dn,ns,cx),dx,[{'n0':0,'n1':nf}],cw,FPS))
    assert abs(dx[0]-cx[0])<1e-6
   else:dn=np.arange(nf);dx=np.full(nf,(1080 if cw==2160 else int(np.median([v['cx'] for v in prior])-cw/2)//2*2+cw/2));info={'method':'Fixed within shot'}
   assert min(dx-cw/2)>=0 and max(dx+cw/2)<=2160,(s,aspect,'crop outside source')
   crops[aspect]={'cw':cw,'ch':ch,'y':y,'approved_y':approved_y,'hair_correction_px':approved_y-y,'n':dn.tolist(),'cx':dx.tolist(),'motion':info,'minimum_hair_clearance_output_px':(hair-y)*(1920 if aspect=='9x16' else 1080)/ch}
  reports.append(dict(s,measurements=str(d/'measure.json'),hair_min_source_px=hair,crops=crops));write(O/'framing.json',reports)
  print('MEASURED',s['id'],s['n0'],len(vals),flush=True)
 fd.close();segmodel.close()
def captions(aspect):
 wh=(1080,1920) if aspect=='9x16' else (1920,1080);cues=[]
 for p in CUT['pieces']:
  sentences=[];sen=[]
  for w in [w for w in WORDS if w['piece']==p['id']]:
   sen.append(w)
   if w['w'].endswith(('.','?','!')):sentences.append(sen);sen=[]
  if sen:sentences.append(sen)
  for sen in sentences:
   cnt=(len(sen)+3)//4;q,r=divmod(len(sen),cnt);start=0
   for j in range(cnt):
    size=q+(j>=cnt-r if r else 0);group=sen[start:start+size];start+=size;cues.append({'text':' '.join(x['w'] for x in group),'t0':group[0]['t0'],'t1':group[-1]['t1']+.06})
 states=[];frames={};lastkey=None;active=None;cache={}
 for g in range(N):
  t=g/FPS;hits=[c for c in cues if c['t0']<=t<c['t1']];c=hits[-1] if hits else None
  if c is None:key=None
  else:
   text=c['text'];sz=64
   while caption_font(sz,'ExtraBold').getlength(text)>wh[0]-120:sz-=2
   f=caption_font(sz,'ExtraBold');x=(wh[0]-f.getlength(text))/2;y=1400 if aspect=='9x16' else 930
   if aspect=='16x9' and 581<=g<725:y=970
   if aspect=='16x9' and 757<=g<983:x=1370.5-f.getlength(text)/2;y=930
   if aspect=='16x9' and any(m['kind']=='lt' and m['t0']<=t<m['t1'] for m in PLAN):y=700
   key=(text,sz,round(x,3),y)
  if key!=lastkey:
   if active:active['beat'][1]=g/FPS;active['frame1']=g
   if key:
    if key not in cache:
     text,sz,x,y=key;f=caption_font(sz,'ExtraBold');full=Image.new('RGBA',wh);d=ImageDraw.Draw(full);d.text((x,y),text,font=f,fill='white',stroke_width=3,stroke_fill='black');box=full.getbbox();im=full.crop(box);dest=O/'captions'/f'{aspect}-{len(cache):03}.png';im.save(dest);cache[key]=(dest,box,im)
    dest,box,im=cache[key];active={'beat':[g/FPS,D],'frame0':g,'frame1':N,'image':str(dest),'image_sha256':sha(dest),'pos':list(box[:2]),'rect':list(box),'word':text};states.append(active)
   else:active=None
   lastkey=key
  if key:frames[g]=cache[key]
 write(O/f'caption-states-{aspect}.json',states)
 return frames
def render():
 framing=json.load(open(O/'framing.json'))
 # Encode the approved common sound once. Only the unused 27 ms tail is shortened.
 au=O/'audio/common.m4a'
 if not au.exists():run([FF,'-v','error','-y','-i',W/'round2/audio/warm-bass-final-timing.wav','-t',D,'-c:a','aac','-b:a','192k','-movflags','+faststart',au])
 for aspect,folder,wh in [('9x16','hf9',(1080,1920)),('16x9','hf16',(1920,1080))]:
  for s in framing:
   out=O/'plates'/f"{s['id']}-{s['n0']}-{aspect}.mp4";nf=s['n1']-s['n0'];c=s['crops'][aspect]
   if out.exists() and int(next(x for x in probe(out)['streams'] if x['codec_type']=='video')['nb_frames'])==nf:continue
   # ffmpeg crop evaluates at delivered-frame indices, after pitch-independent picture acceleration.
   dn=c['n'];xs=np.array(c['cx'])-c['cw']/2
   # Compact interpolation knots preserve native dense shared tracker without a per-frame parser chain.
   knots=sorted(set(list(range(0,nf,3))+[nf-1]));expr=f'{xs[-1]:.3f}'
   for a,b in reversed(list(zip(knots[:-1],knots[1:]))):expr=f'if(lt(n,{b}),{xs[a]:.3f}+({xs[b]-xs[a]:.3f})*(n-{a})/{b-a},{expr})'
   if aspect=='16x9':expr=f'{xs[0]:.3f}'
   vf=GRADE+f",setpts=(PTS-STARTPTS)/{SPEED},fps=30000/1001,crop={c['cw']}:{c['ch']}:'{expr}':{c['y']},scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1"
   run([FF,'-v','error','-y','-ss',s['src0'],'-i',SRC,'-an','-vf',vf,'-frames:v',nf,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',out]);assert int(next(x for x in probe(out)['streams'] if x['codec_type']=='video')['nb_frames'])==nf
   print('PLATE',out.name,flush=True)
  comp=HG.load_compositor(O/folder,wh=wh);C=HG.module('composite');caps=captions(aspect)
  out=O/'masters'/f'AI Took Job AD R4 - {aspect}.mp4';picture=O/'masters'/f'picture-{aspect}.mp4'
  cmd=[FF,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{wh[0]}x{wh[1]}','-framerate','30000/1001','-i','-','-an','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','18','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(picture)]
  e=subprocess.Popen(cmd,stdin=subprocess.PIPE);it=None;curr=None
  try:
   for g in range(N):
    if not comp.opaque(g):
     s=next(x for x in framing if x['n0']<=g<x['n1'])
     if curr!=s['n0']:
      if it:it.close()
      it=C.reader(str(O/'plates'/f"{s['id']}-{s['n0']}-{aspect}.mp4"),n=s['n1']-s['n0'],wh=wh);curr=s['n0']
     fr=next(it)
    else:fr=None
    fr=comp.apply(fr,g)
    if g in caps:
     _,box,cap=caps[g];im=Image.fromarray(fr).convert('RGBA');im.alpha_composite(cap,box[:2]);fr=np.array(im.convert('RGB'))
    e.stdin.write(np.ascontiguousarray(fr).tobytes())
    if g%150==0:print('COMPOSITE',aspect,g,'/',N,flush=True)
  finally:
   if it:it.close()
   e.stdin.close()
  assert e.wait()==0
  run([FF,'-v','error','-y','-i',picture,'-i',au,'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',out])
  v=next(x for x in probe(out)['streams'] if x['codec_type']=='video');assert int(v['nb_frames'])==N;assert float(probe(out)['format']['duration'])<59
  run([FF,'-v','error','-y','-i',out,'-vf','scale=540:960' if aspect=='9x16' else 'scale=960:540','-c:v','libx264','-preset','fast','-crf','23','-c:a','copy','-movflags','+faststart',O/'review'/f'AI Took Job AD R4 - {aspect} - REVIEW.mp4'])
  write(O/f'master-{aspect}.json',{'path':str(out),'sha256':sha(out),'probe':probe(out),'common_audio':str(au),'common_audio_sha256':sha(au)})
  print('MASTER READY',aspect,sha(out),flush=True)
def main():
 preflight()
 if '--preflight' in sys.argv:return
 since=float((O/'build-wait-start.txt').read_text()) if (O/'build-wait-start.txt').exists() else time.time();os.environ['RA16_BUILD_WAIT_SINCE']=str(since)
 (O/'build-wait-start.txt').write_text(str(since))
 old=buildcap.builds
 buildcap.builds=lambda table=None,me=None,since=None:old(table=table,me=me,since=float(os.environ['RA16_BUILD_WAIT_SINCE']))
 write(O/'BUILD_STATE.json',{'status':'waiting-for-build-slot','wait_since':since,'pid':os.getpid()})
 buildcap.wait('AI Took Job AD R4 full film build')
 write(O/'BUILD_STATE.json',{'status':'building','started':time.time(),'pid':os.getpid()})
 run(['zsh',SH/'audio/selftest.sh'],stdout=open(O/'logs/audio-selftest.log','w'),stderr=subprocess.STDOUT)
 measure();render();write(O/'BUILD_STATE.json',{'status':'complete-candidates-awaiting-QC','finished':time.time()})
 print('R4 COMPLETE CANDIDATES READY FOR EDITOR QA',flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as exc:
  write(O/'BUILD_STATE.json',{'status':'failed','reason':str(exc),'at':time.time()})
  raise
