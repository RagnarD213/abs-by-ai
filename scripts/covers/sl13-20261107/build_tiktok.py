from pathlib import Path
import json,sys,hashlib,subprocess
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');w=Path('/Users/danielrose/Projects/_edit_work/sl13-setup-20261107');sys.path.insert(0,str(P/'scripts/blotato'));import tiktok_cover as tc
media=json.loads((w/'approved-media-check.json').read_text());picks=json.loads((P/'Short-form video content/covers/approved-sl13/picks.json').read_text())['covers'];rows=[]
for m,x in zip(media,picks.values()):
 src=Path(m['file']);assert hashlib.sha256(src.read_bytes()).hexdigest()==m['sha256'];cov=Path(x['instagram']);dst=w/f'{src.stem}_tiktok.mp4'
 res=tc.verify(str(src),str(dst),1,str(cov)) if dst.exists() else tc.build(str(src),str(cov),str(dst));assert res['ok'],res
 def ah(p):return hashlib.sha256(subprocess.check_output([tc.FFMPEG,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'])).hexdigest()
 a,b=ah(src),ah(dst);assert a==b
 fr=w/f'{src.stem}_frame0.png';subprocess.run([tc.FFMPEG,'-v','error','-y','-i',str(dst),'-frames:v','1',str(fr)],check=True)
 rows.append({'short':x['short'],'slug':x['slug'],'title':x['title'],'path':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'bytes':dst.stat().st_size,'firstFrame':str(fr),'audio_payload_sha256':a,'audio_identical':True,'verification':res});(w/'tiktok-verification.json').write_text(json.dumps(rows,indent=2));print('TikTok build/packet/first-frame verified:',x['title'],flush=True)
