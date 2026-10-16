from pathlib import Path
import sys,json,subprocess,hashlib
import numpy as np
from PIL import Image
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');B=W/'round2';SH=R/'.claude/skills/_shared';sys.path[:0]=[str(SH),str(SH/'hyperframes')];import buildcap,composite as CP
FF=str(R/'Media/video_edit/bin/ffmpeg');F=30000/1001
assert json.load(open(O/'asset-preflight-review.json'))['verdict']=='PASS','Review actual component pictures and moving phone before assembly'
rec=json.load(open(B/'build-record.json'));rec['framing']=json.load(open(O/'framing.json'));rec['manifests']={f:json.load(open(O/f'hf-manifest{f}.json')) for f in ['9','16']};rec['revision']=3;rec['phone_spec']=json.load(open(O/'phone-source.json'))
(O/'build-record.json').write_text(json.dumps(rec,indent=2))
buildcap.wait('RA13 R3 full composite, both formats')
for fmt,wh in [('9',(1080,1920)),('16',(1920,1080))]:
 man=rec['manifests'][fmt];C=CP.Compositor(man,wh=wh);states=json.load(open(O/f'cap{fmt}/caption_states.json'))['states'];ci=0;last=None;cache=None;g=0
 pic=O/f'final/picture{fmt}.mp4'
 enc=subprocess.Popen([FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{wh[0]}x{wh[1]}','-framerate','30000/1001','-i','-','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv',str(pic)],stdin=subprocess.PIPE)
 for s in rec['slots']:
  n=s['f1']-s['f0'];p=O/f'seg{fmt}/{s["name"]}.mp4' if s['piece'] is not None else (None if s['name']=='A1' else O/f'media/{s["name"]}-{fmt}.mp4');rd=CP.reader(str(p),wh=wh) if p else None
  for i in range(n):
   base=next(rd,None) if rd else np.zeros((wh[1],wh[0],3),np.uint8);assert base is not None,(s['name'],i);fr=C.apply(base,g)
   while ci<len(states) and g>=states[ci]['f1']:ci+=1
   if ci<len(states) and states[ci]['f0']<=g<states[ci]['f1']:
    if ci!=last:cache=np.array(Image.open(states[ci]['image']).convert('RGBA'));last=ci
    fr=CP.over(fr,cache)
   enc.stdin.write(np.asarray(fr,np.uint8).tobytes());g+=1
  if rd:rd.close()
  print('COMPOSITED',fmt,s['name'],g,flush=True)
 enc.stdin.close();assert enc.wait()==0 and g==rec['frames']
 old=next((B/'final').glob('[!._]*'+('9x16' if fmt=='9' else '16x9')+'*.mp4'));target=O/f'final/why do most guys never get abs | codex | {"9x16" if fmt=="9" else "16x9"} | RA-13 R3.mp4'
 subprocess.run([FF,'-nostdin','-v','error','-y','-i',str(pic),'-i',str(old),'-map','0:v','-map','1:a:0','-c','copy','-movflags','+faststart',str(target)],check=True)
 print('CANDIDATE COMPLETE',target,flush=True)
print('BOTH CANDIDATES COMPLETE',flush=True)
