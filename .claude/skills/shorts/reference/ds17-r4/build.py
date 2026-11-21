"""Raw-short adapter of the Shorts full-bleed shot/concat/finish architecture.
No alternate audio processor or quality thresholds: use shared production modules.
"""
from pathlib import Path
import subprocess,json,hashlib,os,sys,shutil
import numpy as np
from scipy.io import wavfile
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];S=Path('/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera');F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH']
P=W/'recipe';B=W/'build';B.mkdir(exist_ok=True)
def ff(args):subprocess.run([F,'-nostdin','-v','error','-y']+list(map(str,args)),check=True)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load():return json.loads((W/'edit.json').read_text())
def audio():
 e=load();sr,x=wavfile.read(W/'source.wav');x=x.astype(np.float64)/2147483648;assert sr==48000 and x.ndim==1;ys=[]
 for p in e['pieces']:
  y=x[round(p['start']*sr):round(p['end']*sr)].copy();n=round(p['frames']/FPS*sr);y=np.pad(y,(0,max(0,n-len(y))))[:n];fade=round(.005*sr);y[:fade]*=np.linspace(0,1,fade);y[-fade:]*=np.linspace(1,0,fade);ys.append(y)
 wavfile.write(W/'untreated.wav',sr,np.concatenate(ys).astype(np.float32));print('untreated',len(np.concatenate(ys))/sr,flush=True)
 subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/voice_chain.py'),'--in',str(W/'untreated.wav'),'--out',str(W/'voice.wav'),'--no-dereverb','--work',str(W/'voice-work')],check=True)
def picture():
 e=load();outs=[]
 for i,s in enumerate(e['shots']):
  out=B/f'shot-{i:02d}.mp4';key=hashlib.sha256(json.dumps(s,sort_keys=True).encode()+Path(__file__).read_bytes()).hexdigest();receipt=out.with_suffix('.json')
  if out.exists() and receipt.exists() and json.loads(receipt.read_text()).get('key')==key and json.loads(receipt.read_text()).get('sha256')==digest(out):print('CACHE',i,flush=True);outs.append(out);continue
  x,y,cw,ch=s['crop'];ph=s['height']
  if s.get('tracking'):
   pts=s['tracking'];x=str(pts[0][1])+''.join(f'+({q[1]-p[1]:.4f})*clip((t-{p[0]:.4f})/{q[0]-p[0]:.4f},0,1)' for p,q in zip(pts,pts[1:]));x="'"+x+"'"
  vf=f'setpts=PTS-STARTPTS,crop={cw}:{ch}:{x}:{y},scale=1080:{ph}:flags=lanczos:in_color_matrix=bt709:in_range=tv,lut3d=file={W}/assets/source-grade.cube:interp=tetrahedral,eq=saturation=0.88,format=yuv420p,setsar=1'
  if s['kind']=='talk':vf+=f',pad=1080:1920:0:310:color=0x0D0E0B'
  else:vf+=f',pad=1080:1920:0:310:color=0x0D0E0B'
  ff(['-ss',s['source_start'],'-i',S/(s['source']+'.MP4'),'-map','0:v:0','-an','-vf',vf,'-frames:v',s['frames'],'-r','30000/1001','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-metadata:s:v:0','rotate=0','-movflags','+faststart',out]);receipt.write_text(json.dumps({'key':key,'sha256':digest(out),'shot':s},indent=2));print('BUILT',i,flush=True);outs.append(out)
 (B/'concat.txt').write_text(''.join("file '"+str(p)+"'\n" for p in outs));ff(['-f','concat','-safe','0','-i',B/'concat.txt','-c','copy',W/'picture.mp4'])
def caption():
 if (W/'caption-timing-ctc.json').exists():
  subprocess.run([sys.executable,str(P/'retime_captions.py')],check=True);return
 d=json.loads((W/'delivered-words.json').read_text());ws=[{'text':a['word'],'timestamp':[a['start'],a['end']]} for s in d['segments'] for a in s['words']];e=load();seg={'id':'DS17','slug':'how-to-jump-rope','pieces':[{'start':0,'end':e['duration'],'words':ws}]};(P/'segments.js').write_text('module.exports={SEGMENTS:'+json.dumps([seg])+',words:[]};\n');subprocess.run(['node',str(P/'captions.js')],check=True);shutil.copy(P/'build/DS17.ass',W/'captions.ass');(W/'words.json').write_text(json.dumps([{'w':x['text'].strip(),'t':x['timestamp'][0],'e':x['timestamp'][1]} for x in ws],indent=2))
def transcribe():
 import whisper,torch
 torch.set_num_threads(4);m=whisper.load_model('medium.en');d=m.transcribe(str(W/'voice.wav'),language='en',word_timestamps=True,fp16=False,verbose=False);(W/'delivered-words.json').write_text(json.dumps(d,indent=2));caption()
def finish():
 e=load();out=W/'ds-17_how-to-jump-rope.mp4';final_audio=Path('/Volumes/Extreme/_edit_work/ds-17/revisions/r3/ds-17_how-to-jump-rope.mp4');on='+'.join(f'gte(n,{round(x["out"]*FPS)})*lt(n,{round(x["out"]*FPS)+x["frames"]})' for x in e['shots'] if x['kind']=='demo');opening_frames=142;fc=f"[0:v][3:v]overlay=0:0:shortest=1:enable='{on}'[d];[d][1:v]overlay=0:0:shortest=1:enable='gte(n,{opening_frames})'[t];[t]ass={W}/captions.ass[v]"
 ff(['-i',W/'picture.mp4','-loop','1','-framerate','30000/1001','-i',W/'assets/title.png','-i',final_audio,'-loop','1','-framerate','30000/1001','-i',W/'assets/demo-frame.png','-filter_complex',fc,'-map','[v]','-map','2:a:0','-t',e['duration'],'-frames:v',e['frames'],'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','30000/1001','-c:a','copy','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-movflags','+faststart',out]);print('MASTER',digest(out),flush=True)
 if not (W/'assets/title.mov').exists():ff(['-loop','1','-framerate','30000/1001','-i',W/'assets/title.png','-t','1','-c:v','qtrle','-pix_fmt','argb',W/'assets/title.mov'])
if __name__=='__main__':globals()[sys.argv[1]]()
