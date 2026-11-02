# Adapted from DS28's reviewed per-shot builder and shared RGB HyperFrames compositor.
from pathlib import Path
import subprocess,json,sys,os,importlib.util,hashlib
import numpy as np
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];Q=W/'review';B=W/'build';F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH'];os.environ['GATE_GROUP']='DS-27'
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap;buildcap.wait('DS-27 R2 full Short')
def mod(path,name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
HG=mod(R/'scripts/video/hyperframes_graphics.py','hg');C=HG.module('composite');G=HG.load_compositor(W/'hf',wh=(1080,1920))
S=json.load(open(W/'source.json'))['path'];shots=json.load(open(W/'shots.json'));grades=json.load(open(W/'grades.json'));plates=json.load(open(W/'media-plates.json'));grade=grades['B'];bp=json.load(open(W/'broll-plan.json'));ES=Path(bp['source']);eg=bp['grade']
KB='/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed/B0431_dan-kettlebell-swings-poolside_16x9_9s.mp4'
AI='/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/concepts-and-gags/A0157_client-pushups-on-handles-trainer-whistle-fist-pump_16x9_6s.mp4'
kg="curves=all='0/0 0.08/0.06 0.25/0.32 0.5/0.59 0.8/0.87 1/1',eq=saturation=1.02"
def ff(a):subprocess.run([F,'-nostdin','-v','error','-y']+list(map(str,a)),check=True)
def cached(name,src,start,n,vf,wh):
 out=B/(name+'.mp4');data=dict(src=src,source_size=Path(src).stat().st_size,start=start,n=n,vf=vf,wh=list(wh));stamp=B/(name+'.inputs.json')
 if not out.exists() or not stamp.exists() or json.load(open(stamp))!=data:
  ff(['-ss',start,'-i',src,'-an','-vf',vf+',setsar=1,format=yuv420p','-frames:v',n,'-r','30000/1001','-c:v','libx264','-threads',os.environ.get('RENDERQ_CORES','4'),'-preset','fast','-crf','18','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv',out]);stamp.write_text(json.dumps(data))
 return out
# Equipment overview, then close-up dumbbells, then overview including each named item, then all-six setup.
equip0=next(s['n0'] for s in shots if s['kind']=='equipment');equip1=next(s['n1'] for s in shots if s['kind']=='equipment')
events=json.load(open(W/'asset-events.json'))
(W/'asset-events.json').write_text(json.dumps(events,indent=2))
sections=[('Home Workouts SFC R2',0,1841)]
def make(name,g0,g1):
 # Each base part is a sequential decode with verified dimensions. No mixed-resolution concatenation.
 edges=sorted(set([g0,g1]+[max(g0,min(g1,v)) for s in shots for v in (s['n0'],s['n1'])]+[max(g0,min(g1,v)) for e in events for v in (e['a'],e['b'])]));parts=[]
 for a,b in zip(edges,edges[1:]):
  if b<=a:continue
  e=next((e for e in events if e['a']<=a<e['b']),None)
  if e:
   src=e['src'];ss=e['ss']+(a-e['a'])/FPS;vf=e['vf'];wh=e['wh'];mode=e['mode'];id=e['id']
  else:
   s=next(s for s in shots if s['n0']<=a<s['n1']);assert s['kind']!='equipment';cw,ch,cy=s['crop'];values=[v for n,v in s['tracking'] if n>=a];x=values[0]
   # Shared landing supplies the centres. Transport the dense changes as a flat frame expression.
   track=[(n-a,v) for n,v in s['tracking'] if a<=n<b];expr=str(track[0][1])+''.join(f'+({v-prev:.4f})*gte(n,{n})' for (n,v),(_,prev) in zip(track[1:],track[:-1]) if abs(v-prev)>.005)
   src=S;ss=s['src']+(a-s['n0'])/FPS;vf=f"setpts=PTS-STARTPTS,crop={cw}:{ch}:'{expr}':{cy},scale=1080:1920:in_color_matrix=bt709:in_range=tv,"+grade;wh=(1080,1920);mode='full';id=s['id']
  p=cached(f'{name}-{id}-{a}-{b}',src,ss,b-a,vf,wh);parts.append((a,b,p,wh,mode))
 # Timeline captions are shifted only for the excerpt; heard neighboring words excluded.
 ass=W/'captions.ass';text=ass.read_text();lines=[]
 def at(t):return f'{int(t//3600)}:{int(t//60)%60:02d}:{t%60:05.2f}'
 header=text[:text.index('Dialogue:')];chunks=json.load(open(W/'caption-chunks.json'))
 override=W/'caption-overrides'/(name+'.json')
 if override.exists():
  chunks=json.load(open(override))['chunks']
  chunks=[[dict(w=v['w'],t0=v['t0']+g0/FPS,t1=v['t1']+g0/FPS) for v in c] for c in chunks]
 for ci,c in enumerate(chunks):
  if c[0]['t0']>=g0/FPS and c[-1]['t1']<=g1/FPS+.02:
   start=max(0,c[0]['t0']-g0/FPS);end=min((g1-g0)/FPS,c[-1]['t1']+.03-g0/FPS, chunks[ci+1][0]['t0']-g0/FPS if ci+1<len(chunks) else (g1-g0)/FPS);lines.append(f"Dialogue: 0,{at(start)},{at(end)},Default,,0,0,0,,"+' '.join(x['w'] for x in c))
 sub=B/(name+'.ass');sub.write_text(header+'\n'.join(lines)+'\n');audio=B/(name+'.wav');ff(['-ss',g0/FPS,'-i',W/'voice.wav','-t',(g1-g0)/FPS,'-c:a','pcm_s16le',audio])
 out=Q/(name+' - 1080p.mp4');cmd=[F,'-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate','30000/1001','-i','-','-i',str(audio),'-map','0:v','-map','1:a','-vf',f"ass='{sub}',scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",'-frames:v',str(g1-g0),'-c:v','libx264','-threads',os.environ.get('RENDERQ_CORES','4'),'-preset','fast','-crf','18','-c:a','aac','-b:a','256k','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv','-movflags','+faststart',str(out)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);plateit={};count=0
 for a,b,path,wh,mode in parts:
  frames=C.reader(str(path),wh=wh)
  for g in range(a,b):
   frame=next(frames)
   if mode!='full':
    if mode not in plateit:
     start=(a-equip0) if mode=='EQUIPMENT' else a-next(e['a'] for e in events if e['mode']=='CLIENT');plateit[mode]=C.reader(plates[mode]['mov'],start=max(0,start),rgba=True,wh=(1080,1920))
    plate=next(plateit[mode]);base=np.zeros((1920,1080,3),np.uint8);x0,y0,x1,y1=plates[mode]['hole'];base[y0:y1,x0:x1]=frame[:y1-y0,:x1-x0];frame=C.over(base,plate)
   frame=G.apply(frame,g);proc.stdin.write(np.ascontiguousarray(frame).tobytes());count+=1
  frames.close()
 proc.stdin.close();assert proc.wait()==0;assert count==g1-g0
 ff(['-i',out,'-vf','scale=540:960','-c:v','libx264','-threads',2,'-preset','fast','-crf',21,'-c:a','copy','-movflags','+faststart',Q/(name+' - REVIEW 540p.mp4')]);ff(['-ss',min(2,(g1-g0)/FPS/2),'-i',out,'-frames:v',1,Q/(name+'.jpg')]);print('RENDERED',name,(g1-g0)/FPS,flush=True)
 for v in plateit.values():v.close()
for section in sections:
 if len(sys.argv)<2 or sys.argv[1]==section[0] or sys.argv[1]=='all':make(*section)
if len(sys.argv)>1 and sys.argv[1] not in ['all','colors']:sys.exit(0)
