"""R2 requested layout, comparison and owned Balanced conform. Never writes R1."""
from pathlib import Path
import json,sys,subprocess,os,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parents[1];O=W.parent/'round1';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
FPS=30000/1001;F=str(R/'Media/video_edit/bin/ffmpeg');sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import vertical as V
os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH'];os.environ['GATE_GROUP']='DS-35'
PANEL=284
def write(p,x):p.write_text(json.dumps(x,indent=2))
def graphics():
 out=W/'hf';out.mkdir(exist_ok=True)
 # Use the maintained moving media-card plate around authentic source-inset photos.
 im=Image.new('RGB',(960,1000),(7,22,40));dr=ImageDraw.Draw(im)
 font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
 for i,(name,file,col) in enumerate([('Seth Rogen','Seth-source-inset.png',(239,69,72)),('Daniel Craig','Daniel-source-inset.png',(49,214,148))]):
  ph=Image.open(O/'assets'/file).convert('RGB');scale=min(436/ph.width,650/ph.height);ph=ph.resize((round(ph.width*scale),round(ph.height*scale)),Image.Resampling.LANCZOS)
  x=i*480+(480-ph.width)//2;im.paste(ph,(x,24+(650-ph.height)//2));cx=240+i*480
  dr.text((cx,730),name,font=ImageFont.truetype(font,47),fill='white',anchor='mt')
  cy=875
  if i==0:
   dr.line([(cx-48,cy-48),(cx+48,cy+48)],fill=col,width=19);dr.line([(cx+48,cy-48),(cx-48,cy+48)],fill=col,width=19)
  else:dr.line([(cx-58,cy),(cx-10,cy+44),(cx+65,cy-54)],fill=col,width=19)
 im.save(W/'comparison-real-source-photos.png')
 scenes=[]
 # The source/title is a concise single line ABOVE the full-height horizontal panel.
 sc,_=V.media_card_scene('R2_SourcePanel',24.0907333334-PANEL/FPS,16/9,kicker='Girls Like The Dad Bod | ManVsStreet',caps=False)
 tpl,cfg,assets=sc;cfg.update(hole=[0,92,1080,608],radius=0);cfg['kicker']={'x':36,'y':24,'px':32,'s':'Girls Like The Dad Bod | ManVsStreet'};scenes.append((tpl,cfg,assets))
 for v,a,b in [('scripted',641/FPS,755/FPS),('off_the_cuff',722/FPS,863/FPS)]:
  sid='R2_Compare_'+v;sc,_=V.media_card_scene(sid,b-a,.96,kicker='Her Definition Of Dad Bod',caps=False)
  tpl,cfg,assets=sc;cfg.update(hole=[60,230,960,1000],radius=24);cfg['kicker']={'x':60,'y':118,'px':52,'s':'Her Definition Of Dad Bod'};scenes.append((tpl,cfg,assets))
 V.build(scenes,out,render=True,snap=1)
 for v in ['scripted','off_the_cuff']:
  d=W/v;e=json.loads((d/'edl.json').read_text());m=json.loads((d/'graphics-manifest.json').read_text());m=[x for x in m if x['id']!='G01_Source']
  a,b=(641/FPS,755/FPS) if v=='scripted' else (722/FPS,863/FPS)
  # Same panel source animation reused, trimmed to each take's definition line.
  m.insert(0,dict(id='R2_SourcePanel',a=PANEL/FPS,b=a,kind='overlay',mov=str(out/'renders/R2_SourcePanel.mov'),hole=[0,92,1080,608],words='Girls Like The Dad Bod | ManVsStreet'))
  m.insert(1,dict(id='R2_Compare_'+v,a=a,b=b,kind='overlay',mov=str(out/'renders'/('R2_Compare_'+v+'.mov')),hole=[60,230,960,1000],photo=str(W/'comparison-real-source-photos.png'),words='Seth Rogen red X; Daniel Craig green check',template='media-card'))
  write(d/'graphics-manifest.json',m)
  write(d/'r2-layout.json',dict(panel_start=PANEL,panel_end=round(a*FPS),comparison=[round(a*FPS),round(b*FPS)],audible_horizontal=[PANEL,469],silent_horizontal=[469,round(a*FPS)],talk_start=485,source='ManVsStreet / Girls Like The Dad Bod Until We Showed Them This',selected_look='B_warmvivid',selected_voice='C_Balanced'))
  # Preserve exact reviewed chunk text/timings, move source captions below the now-large watching head.
  ass=(d/'captions.ass').read_text();head,events=ass.split('[Events]');rows=[]
  for line in events.splitlines():
   if not line.startswith('Dialogue:'):rows.append(line);continue
   z=line.split(',',9);sec=lambda s:sum(float(x)*k for x,k in zip(s.split(':'),[3600,60,1]));t=sec(z[1])
   if PANEL/FPS<=t<485/FPS:z[3]='Default'
   rows.append(','.join(z))
  (d/'captions.ass').write_text(head+'[Events]'+ '\n'.join(rows))
  cs=json.loads((d/'caption-cues.json').read_text())
  for c in cs:
   if PANEL/FPS<=c['t0']<485/FPS:c['style']='Default'
  write(d/'caption-cues.json',cs)
 print('R2_GRAPHICS_READY',flush=True)
def audio():
 eq=json.loads((O/'options/audio-configs.json').read_text())['C_Balanced']['eq']
 for v in ['scripted','off_the_cuff']:
  d=W/v;voice=d/'audio/voice-C_Balanced.wav';e=json.loads((d/'edl.json').read_text())
  if not voice.exists():subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/voice_chain.py'),'--in',str(d/'audio/lav.wav'),'--out',str(voice),'--target','-14.1','--tp','-1.5','--oversample','4','--eq',eq,'--no-expander-because',"Dan selected C_Balanced. Preserve natural tails using its audition's maintained no-expander chain.",'--work',str(d/'audio/chain-C_Balanced')],check=True)
  mix=d/'mix-C_Balanced.wav'
  subprocess.run([F,'-v','error','-nostdin','-y','-i',str(O/'scripted/audio/clip-finished-candidate3.wav'),'-i',str(voice),'-filter_complex','[0:a][1:a]concat=n=2:v=0:a=1,apad[a]','-map','[a]','-t',str(e['total_seconds']),'-ar','48000','-c:a','pcm_s24le',str(mix)],check=True)
  shutil.copy2(O/v/'mix-untreated.wav',d/'mix-untreated.wav')
  write(d/'audio/selected-voice-provenance.json',dict(selected='C_Balanced',eq=eq,source=str(d/'audio/lav.wav'),built_full=True,old_audition_is_30s=True,source_voice_unreplaced=True,gate_status='exact final AAC pending'))
  print('FULL_BALANCED_MIX_READY',v,flush=True)
if __name__=='__main__':
 {'graphics':graphics,'audio':audio}[sys.argv[1]]()
