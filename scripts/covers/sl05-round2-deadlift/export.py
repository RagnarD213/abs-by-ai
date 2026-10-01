#!/usr/bin/env python3
"""Copy Dan's five approved round2 A choices unchanged into final delivery folders."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil
P=Path(__file__).resolve().parents[3];C=P/'Short-form video content/covers';R=C/'review/sl05-covers-20261001/round2-deadlift'
m=json.loads((R/'manifest.json').read_text());q=json.loads((R/'quality-checks.json').read_text());assert q['status']=='PASS'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
selected=[x for x in m['outputs'] if x['variant']=='A'];assert len(selected)==10
approved=C/'approved-sl05-for-Claude';approved.mkdir(parents=True,exist_ok=True)
rows=[]
for x in selected:
 src=Path(x['path']);assert sha(src)==x['sha256']
 qc=next(z for z in q['outputs'] if z['path']==str(src));assert qc['sha256']==x['sha256'] and all(qc['checks'].values())
 name=src.name.replace('_cover-R2A.png','_cover-A.png')
 out=C/'posted covers';out=out/'youtube' if x['platform']=='youtube' else out;out.mkdir(parents=True,exist_ok=True)
 dst=out/name;copy=approved/(x['platform'].title()+'_'+name)
 for p in [dst,copy]:
  if p.exists():assert sha(p)==x['sha256'],f'Existing different file:{p}'
  shutil.copy2(src,p);im=Image.open(p);assert im.mode=='RGB' and im.size==(1080,1920) and sha(p)==x['sha256']
 rows.append(dict(short=x['short'],platform=x['platform'],selected_variant='R2A',path=str(dst),finder_path=str(copy),review_path=str(src),sha256=x['sha256'],minimum_text_person_clearance_px=qc['minimum_text_person_clearance_px']))
receipt={'status':'finalized','approval':'Dan,2026-10-01: Okay let\'s use the ones with the dark backgrounds for everything.','no_upload_or_scheduling':True,'outputs':rows}
(R/'final-export-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
m['status']='finalized: Dan selected R2A for shorts1-5 on2026-10-01';m['picks']={str(n):'A' for n in range(1,6)};(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
d=['# SL-05 approved dark-background covers','',"Dan selected round2 option A for all five shorts on2026-10-01: \"Okay let's use the ones with the dark backgrounds for everything.\"",'', 'Ten exact approved PNGs: five Instagram/Facebook/TikTok layouts and five YouTube layouts. Dark gym backgrounds and red X. No upload or scheduling.','', 'All finals are RGB1080x1920 and byte-identical to the checked review files. Export and Finder copies verified with SHA256.','', 'Finder delivery folder:','',str(approved),'', 'The folder contains the ten chosen PNGs only, labeled Instagram or Youtube. Claude can use these identical copies or the canonical paths below.','', '## Final paths','']
for n in range(1,6):
 d.extend([f'### Short {n}',''])
 for x in [z for z in rows if z['short']==n]:d.extend([x['platform'].title()+':','',x['path'],''])
d.extend(['## Export verification','', '| Short | Platform | SHA256 | Text clearance |','|---|---|---|---|'])
for x in rows:d.append(f"| {x['short']} | {x['platform']} | `{x['sha256']}` | {x['minimum_text_person_clearance_px']}px |")
d.extend(['', 'Source review and receipt: `Short-form video content/covers/review/sl05-covers-20261001/round2-deadlift/`. Recipe: `scripts/covers/sl05-round2-deadlift/export.py`.',''])
text='\n'.join(d).replace('round2','round 2').replace('on2026','on 2026').replace('RGB1080','RGB 1080');assert '\u2014' not in text and '\u2013' not in text
(P/'Docs/SL05_COVER_FINALS_20261001.md').write_text(text)
assert len(list(approved.glob('*.png')))==10
print('Exported and verified ten chosen finals and ten identical Finder delivery copies.')
print(approved)
