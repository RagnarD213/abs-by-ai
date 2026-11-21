"""Export the exact libass glyph states used by the full R2 renderer, with delivered-pixel verification left to the shared gate."""
from pathlib import Path
import sys,json,subprocess,hashlib,os
from PIL import Image
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');FF=str(R/'Media/video_edit/bin/ffmpeg')
sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
renderq.hold_until_exit('DS35 actual libass caption state export '+','.join(sys.argv[1:]),pool='quick')
# Required corrected normal audio qualification runs as a sequential child of the held full-build slot.
for version in sys.argv[1:]:
 subprocess.run([sys.executable,str(W/'recipe/audio_exact_r2.py'),version],check=True)
 if version=='scripted':subprocess.run([sys.executable,str(W/'recipe/selected_voice_identity_r2.py')],check=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sec=lambda x:sum(float(y)*z for y,z in zip(x.split(':'),[3600,60,1]))
for iid in sys.argv[1:]:
 Q=W/'qa'/iid;plan=json.loads((Q/'plan.json').read_text());ass=Path(plan['captions_ass']);head=[];cues=[]
 for line in ass.read_text().splitlines():
  if line.startswith('Dialogue:'):cues.append(line)
  else:head.append(line)
 D=Q/'caption-states';D.mkdir(exist_ok=True);states=[];gaps=[]
 for i,line in enumerate(cues):
  f=line.split(',',9);a,b=sec(f[1]),sec(f[2]);f[1],f[2]='0:00:00.00','0:00:02.00';one=D/'one-cue.ass';one.write_text('\n'.join(head+[','.join(f)])+'\n');png=D/f'{i:03d}.png'
  subprocess.run([FF,'-v','error','-nostdin','-y','-threads','1','-f','lavfi','-i','color=c=black@0.0:s=1080x1920:r=30000/1001:d=0.2,format=rgba','-vf',f'ass={one}:alpha=1','-frames:v','1',str(png)],check=True)
  im=Image.open(png).convert('RGBA');alpha=im.getchannel('A');box=alpha.getbbox();assert box and alpha.getextrema()==(0,255),(iid,i,'No real transparent glyph alpha')
  states.append(dict(name=f'{iid} cue{i}',beat=[a,b],image=str(png),image_sha256=sha(png),pos=[0,0],word=f[9].split()[0],cue_text=f[9],measurement_scope='First-word onset of a whole J2 chunk; no per-word highlight is claimed',libass_source_sha256=sha(ass),ink_bbox=list(box)))
  for g in plan['graphic_regions']:
   if min(b,g['beat'][1])<=max(a,g['beat'][0]):continue
   x,y,w,h=g['rect'];x0,y0,x1,y1=box
   if x1<x or x0>x+w:continue
   gap=y-y1 if y1<y else y0-(y+h) if y0>y+h else -min(y1-y,y+h-y0)
   gaps.append(dict(cue=i,graphic=g['name'],gap=gap))
 # Re-read so a separate completed ASR update is preserved; the state source itself must be unchanged.
 current=json.loads((Q/'plan.json').read_text());assert current['video_sha256']==plan['video_sha256'] and current['caption_source']==plan['caption_source']
 (Q/'caption-states.json').write_text(json.dumps(dict(video_sha256=plan['video_sha256'],caption_source=plan['caption_source'],states=states),indent=1));current['caption_states']=states;temp=Q/'plan-caption-temp.json';temp.write_text(json.dumps(current,indent=1));temp.replace(Q/'plan.json')
 (Q/'caption-state-export.json').write_text(json.dumps(dict(video_sha256=plan['video_sha256'],ass_sha256=sha(ass),method='Same libass font/style/text rasterizer as render_ds35.py; exact glyph alpha exported on transparent field. Shared gate must independently verify states in delivered pixels.',states=len(states),bbox_gap_diagnostic=gaps,minimum_bbox_gap=min((x['gap'] for x in gaps),default=None),not_a_delivered_pixel_pass=True),indent=1))
 print('CAPTION_STATES_EXPORTED',iid,len(states),'minimum geometric gap',min((x['gap'] for x in gaps),default=None),flush=True)
