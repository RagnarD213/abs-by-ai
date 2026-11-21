from pathlib import Path
import os,sys,json,hashlib,shutil,subprocess
import numpy as np
from PIL import Image
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Extreme/_edit_work/ra13/round2');SH=R/'.claude/skills/_shared';sys.path[:0]=[str(SH),str(SH/'hyperframes')];import buildcap,vertical as V,composite as CP,hfbuild as H
FF=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;r=json.load(open(O/'build-record.json'));old=O/'before-cta-repair';old.mkdir(exist_ok=True);proof=[]
for fmt,wh,box in [('9',(1080,1920),(68,1530,944,180)),('16',(1920,1080),(68,740,590,140))]:
 buildcap.wait('RA13 CTA clearance repair '+fmt)
 v=next((O/'final').glob('*'+('9x16' if fmt=='9' else'16x9')+'*.mp4'));dst=old/v.name
 if not dst.exists():shutil.copy2(v,dst)
 cta=r['manifests'][fmt][1];scenes,_=V.cta_scenes('CTA',cta['b']-cta['a'],'Tap The Button Below','Get Started',hold_out=True)
 x,y,w,h=box;toppx,bigpx=(30,64) if fmt=='9' else(24,46);topy=y+20;bigy=y+65 if fmt=='9' else y+58
 bx=x+(w-H.text_w('Get Started',bigpx)-56)/2
 for _,c,_ in scenes:
  c['canvas']=list(wh);c['btn']=list(box);c['radius']=36 if fmt=='9' else 28;c['top']=dict(x=round(x+(w-H.text_w('Tap The Button Below',toppx))/2),y=topy,px=toppx,s='Tap The Button Below');c['big']=dict(x=round(bx),y=bigy,px=bigpx,s='Get Started');c['arrow']=dict(x=round(bx+H.text_w('Get Started',bigpx)+22),y=bigy,px=bigpx)
 out=O/f'cta-clear{fmt}';V.build(scenes,out,render=True)
 cta.update(mov=str(out/'renders/CTA.mov'),mask=str(out/'renders/CTA_mask.mov'),box=[x,y,x+w,y+h],band=[y-12,y+h+12]);json.dump(r['manifests'][fmt],open(O/f'hf-manifest{fmt}.json','w'),indent=2)
 states=json.load(open(O/f'cap{fmt}/caption_states.json'))['states'];C=CP.Compositor(r['manifests'][fmt],wh=wh);ci=0;g=0;cache=None;last=None
 pic=O/f'final/picture{fmt}-clear.mp4';enc=subprocess.Popen([FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{wh[0]}x{wh[1]}','-framerate','30000/1001','-i','-','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv',str(pic)],stdin=subprocess.PIPE)
 for s in r['slots']:
  n=s['f1']-s['f0'];path=O/f'seg{fmt}/{s["name"]}.mp4' if s['piece'] is not None else (O/f'media/{s["name"]}-{fmt}.mp4' if s['name']!='A1' else None);rd=CP.reader(str(path),wh=wh) if path else None
  for i in range(n):
   base=next(rd,None) if rd else np.zeros((wh[1],wh[0],3),np.uint8);assert base is not None
   fr=C.apply(base,g)
   while ci<len(states) and g>=states[ci]['f1']:ci+=1
   if ci<len(states) and states[ci]['f0']<=g<states[ci]['f1']:
    if ci!=last:cache=np.array(Image.open(states[ci]['image']).convert('RGBA'));last=ci
    fr=CP.over(fr,cache)
   enc.stdin.write(np.asarray(fr,np.uint8).tobytes());g+=1
  if rd:rd.close()
 enc.stdin.close();assert enc.wait()==0 and g==r['frames']
 subprocess.run([FF,'-nostdin','-v','error','-y','-i',str(pic),'-i',str(dst),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(v)],check=True)
 # Packet-level audio identity, so the chosen voice remains exactly intact.
 def audiohash(p):
  a=subprocess.run([FF,'-nostdin','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'],capture_output=True,check=True).stdout;return hashlib.sha256(a).hexdigest()
 h0,h1=audiohash(dst),audiohash(v);assert h0==h1;proof.append(dict(format=fmt,before=str(dst),after=str(v),audio_sha256=h1,audio_bit_identical=True,box=cta['box']))
 json.dump(r,open(O/'build-record.json','w'),indent=2);json.dump(proof,open(O/'cta-repair.json','w'),indent=2)
 print('REPAIRED',fmt,flush=True)
print('CTA REPAIR BOTH COMPLETE',flush=True)
