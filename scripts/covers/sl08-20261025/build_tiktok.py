from pathlib import Path
import json,sys,hashlib,subprocess
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(P/'scripts/blotato'));import tiktok_cover as tc
D=P/'Short-form video content/Calories Not Losing Weight - Shorts R6';O=Path('/Volumes/Extreme/_edit_work/sl08-publish');C=P/'Short-form video content/covers/approved-sl08';m=json.loads((D/'finalization-manifest.json').read_text());picks=json.loads((C/'picks.json').read_text())['covers'];rows=[]
for i,v in enumerate(m['files'],1):
 src=Path(v['file']);pick=picks[src.stem];cov=Path(pick['instagram']);dst=O/f'{src.stem}_tiktok.mp4'
 res=tc.build(str(src),str(cov),str(dst));assert res.get('ok'),res
 # Verify complete AAC packet payloads, independent of timestamp/container changes.
 def ah(path):
  r=subprocess.run([tc.FFMPEG,'-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','adts','-'],capture_output=True,check=True);return hashlib.sha256(r.stdout).hexdigest()
 a,b=ah(src),ah(dst);assert a==b
 fr=O/f'{src.stem}_frame0.png';subprocess.run([tc.FFMPEG,'-v','error','-y','-i',str(dst),'-frames:v','1',str(fr)],check=True)
 rows.append({'short':i,'title':v['title'],'path':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'bytes':dst.stat().st_size,'firstFrame':str(fr),'audio_payload_sha256':a,'audio_identical':True,'verification':res});(O/'tiktok-verification.json').write_text(json.dumps(rows,indent=2));print('TikTok verified:',v['title'],flush=True)
