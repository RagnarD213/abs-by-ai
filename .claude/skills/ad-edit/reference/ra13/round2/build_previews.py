from pathlib import Path
import sys,os,json,subprocess,importlib.util,hashlib,shutil
import numpy as np
from PIL import Image
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W=Path('/Volumes/Extreme/_edit_work/ra13'); O=W/'round2';os.chdir(O)
sys.path.insert(0,str(O/'recipe'));import cards
SH=R/'.claude/skills/_shared';sys.path[:0]=[str(SH),str(SH/'hyperframes')];import buildcap,softblue as B,hyperframes.composite as CP
FF=str(R/'Media/video_edit/bin/ffmpeg'); FPS=30000/1001
for d in ('context','stills','audio','media','logs'): (O/d).mkdir(exist_ok=True)
def run(cmd):subprocess.run(cmd,check=True)
def wait(name):buildcap.wait('RA-13 R2 '+name)
def encode(frames,path,wh):
 p=subprocess.Popen([FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{wh[0]}x{wh[1]}','-r','30000/1001','-i','-','-vf','scale=out_color_matrix=bt709:out_range=tv','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',str(path)],stdin=subprocess.PIPE)
 for im in frames:p.stdin.write(np.asarray(im,dtype=np.uint8).tobytes())
 p.stdin.close();assert p.wait()==0
spec=importlib.util.spec_from_file_location('phone_helpers',R/'.claude/skills/ad-edit/reference/ra14/s63_stills.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
cut=json.load(open(W/'cut.json'));eq=json.load(open(W/'audio-options/lighter-bass.wav.voice_chain.json'))['eq']
wait('approved voice chain');run([sys.executable,str(SH/'audio/voice_chain.py'),'--in',str(W/'cut_audio.wav'),'--out',str(O/'audio/voice.wav'),'--eq',eq,'--work',str(O/'audio/work')])
# Align without changing the recorded cut's spelling or word content.
sp=(W/'recipe/align.py').read_text().replace('CUT = json.load(open("cut.json"))',f'CUT = json.load(open({str(W/"cut.json")!r}))')
(O/'recipe/align.py').write_text(sp);wait('cut alignment');run([sys.executable,str(O/'recipe/align.py'),str(O/'audio/voice.wav'),str(O/'words_aligned.json')])
ws=json.load(open(O/'words_aligned.json'))['words']
def cap(im,t,wh):
 # Maintain the accepted caption font, highlight and shadow treatment, with phrase-sized lines.
 g=[];groups=[]
 for w in ws:
  if g and (len(' '.join(q['w'] for q in g+[w]))>22 or g[-1]['w'].endswith(('.', '?','!'))):groups.append(g);g=[]
  g.append(w)
 if g:groups.append(g)
 for i,g in enumerate(groups):
  end=min(g[-1]['e']+.7,groups[i+1][0]['t'] if i+1<len(groups) else cut['dur']+.6)
  if g[0]['t']<=t<end:
   k=max(j for j,q in enumerate(g) if q['t']<=t);line=' '.join(q['w'] for q in g)
   return S.caption(im,line,k,y=1400 if wh[0]<wh[1] else 930)
 return im

def mux(pic,gid,a,b,wh):
 out=O/f'context/{gid}-context - REVIEW 540p.mp4';scale='540:960' if wh[0]<wh[1] else '960:540'
 run([FF,'-nostdin','-v','error','-y','-i',str(pic),'-ss',str(a),'-i',str(O/'audio/voice.wav'),'-t',str(b-a),'-vf',f'scale={scale}','-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','160k','-movflags','+faststart',str(out)])
 run([FF,'-nostdin','-v','error','-y','-ss',str(min(2,(b-a)/2)),'-i',str(out),'-frames:v','1',str(O/f'stills/{gid}.jpg')]);return out

def decode(path,t,n,wh,crop=None):
 vf='scale=in_color_matrix=bt709:in_range=tv,'+(f'crop={crop},' if crop else '')+f'fps=30000/1001,scale={wh[0]}:{wh[1]},format=rgb24'
 b=subprocess.run([FF,'-nostdin','-v','error','-ss',str(t),'-i',str(path),'-frames:v',str(n),'-vf',vf,'-f','rawvideo','-'],capture_output=True,check=True).stdout
 return np.frombuffer(b,np.uint8).reshape(-1,wh[1],wh[0],3)
# Reference hair was 36 px in the approved 540-high still: 64.8 source px. Shift 20 px, leave 69.1%.
newtop=json.load(open(O/'headroom.json'))['new_top'];grade=json.load(open(W/'grade-options.json'))['B']['filter'];roll=json.load(open(W/'source/roll.json'))['identity']['current_path']
wait('horizontal correction');p=cut['pieces'][1];n=round((p['src_out']-p['src_in'])*FPS)
for label,top in [('before',1240),('after',newtop)]:
 pic=O/f'media/headroom-{label}.mp4';run([FF,'-nostdin','-v','error','-y','-ss',str(p['src_in']),'-i',roll,'-frames:v',str(n),'-vf',grade+f',crop=1728:972:216:{top},scale=1920:1080,setsar=1','-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',str(pic)]);mux(pic,'headroom-'+label,p['t_in'],p['t_out'],(1920,1080))
# Every card is an isolated contextual preview; no complete placeholder film is assembled.
wait('analysis card motion');import hfbuild as H,vertical as V
cfg=json.load(open(O/'analysis-config.json'))[0]
scenes,meta=V.analysis_scenes(cfg);V.build(scenes,O/'hf9',render=True,check=True)
H.render(O/'hf16/A1',O/'hf16/A1.mov')
for fmt,wh,path in [('9x16',(1080,1920),O/'hf9/renders/A1.mov'),('16x9',(1920,1080),O/'hf16/A1.mov')]:
 a,b=cfg['a'],cfg['b'];frames=CP.reader(str(path),wh=wh);pic=O/f'media/A1-{fmt}.mp4';encode((cap(Image.fromarray(fr),a+i/FPS,wh) for i,fr in enumerate(frames)),pic,wh);mux(pic,'A1-'+fmt,a,b,wh)
wait('phone contexts')
DEMO=Path(S.DEMO);TOUR=Path(S.TOUR)
# This 9:16 shell and scene-photo layout are approved reusable shared components.
a,b=16.711,25.759;n=round(b*FPS)-round(a*FPS);phone_n=round(1.57*FPS)
scr=decode(DEMO,2.0,phone_n,(434,940),'434:940:741:68')
def p1frames():
 for i in range(n):
  t=a+i/FPS
  if i<phone_n:
   chip='Real picture of me. Not AI-generated.' if 2.0+i/FPS>=2.60 else None
   im,_=cards.phone(t,Image.fromarray(S.square_corners(scr[i])),'9',chip,room_for_label=True)
  else:im,_=cards.goal((i-phone_n)/FPS+1,'9')
  yield cap(im,t,(1080,1920))
pic=O/'media/P1.mp4';encode(p1frames(),pic,(1080,1920));mux(pic,'P1',a,b,(1080,1920))
a,b=34.311,39.431;n=round(b*FPS)-round(a*FPS);first=round(2*FPS);w1=decode(TOUR,6,first,(432,920));w2=decode(TOUR,2.05,n-first,(432,920))
def p2frames():
 for i in range(n):
  im,_=cards.phone(a+i/FPS,Image.fromarray(w1[i] if i<first else w2[i-first]),'9');yield cap(im,a+i/FPS,(1080,1920))
pic=O/'media/P2.mp4';encode(p2frames(),pic,(1080,1920));mux(pic,'P2',a,b,(1080,1920))

(O/'asset-dispositions.json').write_text(json.dumps({'P3':{'status':'removed','source':'B0037','reason':'Stick-figure exercise demo visible','replacement':'Presenter'},'L1':{'status':'removed','source':'A0074','reason':'Motion distortion in long range; short range is a photo viewer rather than a lockscreen','replacement':'Presenter'}},indent=2))
print('PREVIEWS READY',flush=True)
