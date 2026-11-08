from pathlib import Path
import json,subprocess,hashlib,shutil
root=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');w=Path('/Users/danielrose/Projects/_edit_work/sl13-setup-20261107')
rows=json.loads((w/'layout-manifest-private.json').read_text());meta=json.loads((w/'packaging/metadata.json').read_text());media=json.loads((w/'approved-media-check.json').read_text());dest=root/'Short-form video content/covers/approved-sl13';dest.mkdir(exist_ok=True)
words="Let's go with Protein X3, Eat Less X4, and Steps X3. Go ahead and finish the backups and setup, including verified waitlist placement if Blotato is still full."
out={'job':'SL-13','date':'2026-11-08','picked_by':'Dan','words':words,'covers':{}}
for idx,(k,label) in enumerate([('A','X3'),('B','X4'),('C','X3')]):
 sd=w/'blind-sets'/k;key=json.loads((sd/'.blind-key.json').read_text());choice=key['labels'][label];ident=choice['note'];assert len([r for r in rows if r['short']==k and r['id']==ident])==2
 old=dest/'picks.json'
 if not old.exists():subprocess.run(['python3',str(root/'.claude/skills/_shared/blind-image/blind.py'),'pick',str(sd),'--chose',label,'--words',words],check=True,capture_output=True)
 record={'short':k,'title':meta[idx]['title'],'pick':label,'slug':meta[idx]['slug'],'film_sha256':media[idx]['sha256']}
 for platform,ext in [('instagram','.png'),('youtube','.jpg')]:
  row=next(r for r in rows if r['short']==k and r['id']==ident and r['platform']==platform)
  src=Path(row['path']).with_suffix(ext)
  if platform=='instagram':assert hashlib.sha256(src.read_bytes()).hexdigest().startswith(choice['sha'])
  dst=dest/f'{platform.capitalize()}_{meta[idx]["slug"]}_cover-{label}{ext}';shutil.copy2(src,dst)
  record[platform]=str(dst);record[platform+'_sha256']=hashlib.sha256(dst.read_bytes()).hexdigest();record[platform+'_bytes']=dst.stat().st_size
 out['covers'][meta[idx]['slug']]=record
(dest/'picks.json').write_text(json.dumps(out,indent=2));print('Installed all3 exact picks,6 approved layouts. No creative changes.')
