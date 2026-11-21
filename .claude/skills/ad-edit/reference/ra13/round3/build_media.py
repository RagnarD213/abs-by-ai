from pathlib import Path
import sys,json,subprocess,importlib.util,hashlib
import numpy as np
from PIL import Image
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');B=W/'round2';SH=R/'.claude/skills/_shared';sys.path[:0]=[str(O/'recipe'),str(SH),str(SH/'hyperframes')]
import cards,buildcap,vertical as V,hfbuild as H,composite as CP
FF=str(R/'Media/video_edit/bin/ffmpeg');F=30000/1001
rec=json.load(open(B/'build-record.json'));cfg=json.load(open(O/'analysis-config.json'))[0];src='/Volumes/Extreme/_edit_work/ra04/round5/gen_white_man_rec.mp4';spec=json.load(open(O/'phone-source.json'))
sp=importlib.util.spec_from_file_location('analysis_card',SH/'hyperframes/analysis-card/build.py');AC=importlib.util.module_from_spec(sp);sp.loader.exec_module(AC)
def enc(frames,path,wh):
 p=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{wh[0]}x{wh[1]}','-framerate','30000/1001','-i','-','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','16','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv',str(path)],stdin=subprocess.PIPE)
 for im in frames:p.stdin.write(np.asarray(im,dtype=np.uint8).tobytes())
 p.stdin.close();assert p.wait()==0
buildcap.wait('RA13 R3 analysis and phone assets')
subprocess.run([sys.executable,str(O/'recipe/head_measure.py')],check=True)
for fmt,wh in [('9',(1080,1920)),('16',(1920,1080))]:
 config,assets,layout=AC.layout(cfg,wh,bottom=1376 if fmt=='9' else 900)
 scenes=[(AC.TPL,config,assets)];V.build(scenes,O/f'hf{fmt}',render=True,check=True)
 (O/f'analysis-layout{fmt}.json').write_text(json.dumps(layout,indent=2))
 man=json.load(open(B/f'hf-manifest{fmt}.json'));man[0]['mov']=str(O/f'hf{fmt}/renders/A1.mov');(O/f'hf-manifest{fmt}.json').write_text(json.dumps(man,indent=2))
 s=next(x for x in rec['slots'] if x['name']=='P1');n=s['f1']-s['f0'];switch=round(spec['result_at']*F)-s['f0'];screens=[]
 for name,t,nn in [('loader',spec['loader_t0'],switch),('result',spec['result_t0'],n-switch)]:
  x,y,cw,ch=spec[name+'_crop'];vf=f'scale=in_color_matrix=bt709:in_range=tv,crop={cw}:{ch}:{x}:{y},fps=30000/1001,scale=518:982,format=rgb24'
  raw=subprocess.run([FF,'-v','error','-ss',str(t),'-i',src,'-vf',vf,'-frames:v',str(nn),'-f','rawvideo','-'],capture_output=True,check=True).stdout
  arr=np.frombuffer(raw,np.uint8).reshape(-1,982,518,3);assert len(arr)==nn,(name,len(arr),nn);screens.extend(Image.fromarray(f) for f in arr)
 def frames():
  for i,screen in enumerate(screens):yield cards.phone(s['a']+i/F,screen,fmt,'AI-GENERATED',room_for_label=True)[0]
 enc(frames(),O/f'media/P1-{fmt}.mp4',wh)
 # Native component stills and moving media prove content independently of final assembly.
 for name,frame in [('loader',0),('before-cut',switch-1),('result',switch),('last',n-1)]:
  im=cards.phone(s['a']+frame/F,screens[frame],fmt,'AI-GENERATED',room_for_label=True)[0];im.save(O/f'preflight/P1-{fmt}-{name}.jpg')
 (O/f'phone-layout{fmt}.json').write_text(json.dumps({'source':src,'screen_source':spec,'n':n,'switch_frame':switch,'switch_full_frame':s['f0']+switch,'geometry':cards.phone(0,screens[0],fmt,'AI-GENERATED',room_for_label=True)[1]},indent=2))
 print('ASSETS READY',fmt,flush=True)
print('ASSET PREFLIGHT REVIEW REQUIRED',flush=True)
