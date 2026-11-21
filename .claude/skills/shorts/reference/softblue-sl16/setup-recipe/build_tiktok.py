from pathlib import Path
import json,sys,hashlib,subprocess
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(P/'scripts/blotato'));import tiktok_cover as tc
S=P/'Short-form video content';O=Path('/Volumes/Extreme/_edit_work/sl16-publish');C=S/'covers/approved-sl16';m=json.loads((S/'fasting-SHORTS-final-manifest.json').read_text())['shorts'];picks=json.loads((C/'picks.json').read_text())['covers'];rows=[]
def ah(path):
 r=subprocess.run([tc.FFMPEG,'-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','adts','-'],capture_output=True,check=True);return hashlib.sha256(r.stdout).hexdigest()
for v in m:
 src=S/v['file'];cov=Path(picks[src.stem]['instagram']);dst=O/f'{src.stem}_tiktok.mp4'
 res=tc.build(str(src),str(cov),str(dst));assert res.get('ok'),res
 a,b=ah(src),ah(dst);assert a==b
 fr=O/f'{src.stem}_frame0.png';subprocess.run([tc.FFMPEG,'-v','error','-y','-i',str(dst),'-frames:v','1',str(fr)],check=True)
 rows.append({'short':v['n'],'path':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'bytes':dst.stat().st_size,'firstFrame':str(fr),'audio_identical':True,'verification':res});(O/'tiktok-verification.json').write_text(json.dumps(rows,indent=2));print('TikTok verified',v['n'],flush=True)
