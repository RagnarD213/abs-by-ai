from pathlib import Path
import json,shutil,hashlib,sys
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=P/'Short-form video content/covers/review/sl08-20261025';D=P/'Short-form video content/Calories Not Losing Weight - Shorts R6';C=P/'Short-form video content/covers/approved-sl08';C.mkdir(parents=True,exist_ok=True);O=Path('/Volumes/Extreme/_edit_work/sl08-publish');O.mkdir(parents=True,exist_ok=True)
m=json.loads((D/'finalization-manifest.json').read_text());covers=json.loads((R/'manifest.json').read_text())['outputs'];sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();picks={'picked_by':'Dan','date':'2026-10-25','words':"Let's go with C for all five Shorts. Go ahead and complete setup for January 4, 5, 8, 9 and 11 at 9 AM Central.",'covers':{}}
def ts(t):
 n=round(t*1000);h,n=divmod(n,3600000);mi,n=divmod(n,60000);sec,ms=divmod(n,1000);return f'{h:02d}:{mi:02d}:{sec:02d},{ms:03d}'
for i,v in enumerate(m['files'],1):
 k=f's{i}';src=Path(v['file']);assert sha(src)==v['sha256'];assert sha(v['extremeBackup'])==v['sha256']
 ig=next(x for x in covers if x['short']==k and x['variant']=='C' and x['platform']=='instagram');yt=next(x for x in covers if x['short']==k and x['variant']=='C' and x['platform']=='youtube')
 ip=Path(ig['path']);yp=Path(yt['jpeg_path']);assert sha(ip)==ig['sha256'];assert sha(yp)==yt['jpeg_sha256']
 io=C/('Instagram_'+ip.name);yo=C/('YouTube_'+yp.name);shutil.copy2(ip,io);shutil.copy2(yp,yo);assert sha(io)==ig['sha256'] and sha(yo)==yt['jpeg_sha256']
 slug=src.stem;picks['covers'][slug]={'short':k,'title':v['title'],'pick':'C','instagram':str(io),'instagram_sha256':sha(io),'youtube':str(yo),'youtube_sha256':sha(yo),'youtube_bytes':yo.stat().st_size}
 cues=json.loads((Path(v['workMaster']).parent/'cues.json').read_text());assert max(x['b'] for x in cues)<=v['duration']+0.04
 srt='\n\n'.join(f"{j}\n{ts(x['a'])} --> {ts(min(x['b'],v['duration']))}\n{x['text']}" for j,x in enumerate(cues,1))+'\n';sp=src.with_suffix('.srt');sp.write_text(srt)
 shutil.copy2(sp,Path(v['extremeBackup']).with_suffix('.srt'));print('Approved exact pair exported; master and Extreme match:',v['title'],flush=True)
(C/'picks.json').write_text(json.dumps(picks,indent=2));(O/'picks.json').write_text(json.dumps(picks,indent=2))
# Approved covers accompany the finals on all three storage locations.
shutil.copytree(C,D/'approved covers',dirs_exist_ok=True);shutil.copytree(C,Path('/Volumes/Extreme/Short-form video content/Calories Not Losing Weight - Shorts R6/approved covers'),dirs_exist_ok=True)
print('All five picks saved, subtitle sidecars exported from each exact delivered cue map',flush=True)
