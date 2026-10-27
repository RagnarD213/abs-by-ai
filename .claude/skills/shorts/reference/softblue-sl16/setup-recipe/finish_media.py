#!/usr/bin/env python3
"""SL-16: install Dan's approved covers (2026-10-27), record picks with hashes, write .srt sidecars from each build's
delivered cue map, and copy finals + covers to the Extreme 'Short-form video content' folder."""
from pathlib import Path
import json,shutil,hashlib
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');S=P/'Short-form video content';R=S/'covers/review/sl16-20261027';C=S/'covers/approved-sl16';C.mkdir(parents=True,exist_ok=True)
O=Path('/Volumes/Extreme/_edit_work/sl16-publish');O.mkdir(parents=True,exist_ok=True);X=Path('/Volumes/Extreme/Short-form video content/Intermittent Fasting Shorts - SL-16');X.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads((S/'fasting-SHORTS-final-manifest.json').read_text())['shorts'];r1=json.loads((R/'manifest.json').read_text())['outputs'];r2=json.loads((R/'manifest-r2.json').read_text())['outputs']
PICK={1:('F',r2,'How To Start Fasting: Just Skip Breakfast'),2:('A2',r2,'Why Carbs Destroy Your Productivity'),3:('A2',r2,'Never Break Your Fast With Alcohol'),4:('F',r2,'Why You Need A Simple Nutrition Plan')}
BUILD={1:'S1',2:'B',3:'C',4:'D'}
picks={'picked_by':'Dan','date':'2026-10-27','words':'Short 1F, dumping breakfast, is approved. Short 2A with the new title is approved. Short 3A revised is approved. Short 4F, eating a salad, is approved.','covers':{}}
def ts(t):
 n=round(t*1000);h,n=divmod(n,3600000);mi,n=divmod(n,60000);s,ms=divmod(n,1000);return f'{h:02d}:{mi:02d}:{s:02d},{ms:03d}'
for v in m:
 n=v['n'];src=S/v['file'];assert sha(src)==v['sha256'];var,man,title=PICK[n]
 ig=next(x for x in man if x['short']==f's{n}' and x['variant']==var and x['platform']=='instagram');yt=next(x for x in man if x['short']==f's{n}' and x['variant']==var and x['platform']=='youtube')
 ip=Path(ig['path']);yp=Path(yt['path']).with_suffix('.jpg');assert sha(ip)==ig['sha256'];assert yp.stat().st_size<2_000_000
 io=C/('Instagram_'+ip.name);yo=C/('YouTube_'+yp.name);shutil.copy2(ip,io);shutil.copy2(yp,yo)
 picks['covers'][src.stem]={'short':f's{n}','title':title,'pick':var,'instagram':str(io),'instagram_sha256':sha(io),'youtube':str(yo),'youtube_sha256':sha(yo),'youtube_bytes':yo.stat().st_size}
 cues=json.loads(Path(f'/Volumes/Extreme/_edit_work/SL-16/build/{BUILD[n]}/cues.json').read_text());assert max(x['b'] for x in cues)<=v['seconds']+0.05
 srt='\n\n'.join(f"{j}\n{ts(x['a'])} --> {ts(min(x['b'],v['seconds']))}\n{x['text']}" for j,x in enumerate(cues,1))+'\n';sp=src.with_suffix('.srt');sp.write_text(srt)
 xd=X/src.name
 if not xd.exists() or sha(xd)!=v['sha256']:shutil.copyfile(src,xd)
 assert sha(xd)==v['sha256'];shutil.copyfile(sp,X/sp.name);print('installed',n,var,title,flush=True)
(C/'picks.json').write_text(json.dumps(picks,indent=2)+'\n');(O/'picks.json').write_text(json.dumps(picks,indent=2)+'\n')
shutil.copytree(C,X/'approved covers',dirs_exist_ok=True,copy_function=shutil.copyfile);print('done')
