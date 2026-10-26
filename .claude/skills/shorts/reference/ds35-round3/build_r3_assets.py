"""Narrow R3 changes through maintained HyperFrames templates; no AI generation."""
from pathlib import Path
import sys,json,hashlib,shutil
from PIL import Image
W=Path(__file__).resolve().parents[1];O=W.parent/'round1';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');H=R/'.claude/skills/_shared/hyperframes'
sys.path.insert(0,str(H));import vertical as V
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=json.loads((W/'round-controller.json').read_text());assert j['productionOwner']=='01a17430-0acf-72c1-93fa-026651f4da47' and j['phase']=='complete'
photo=R/'photos/finalized social media photos/studio-blue-11_FINAL_PRIMARY.jpg'
original=R/'photos/studio shoot | 8-28-26 | dan | mindi/Portrait Shoot Thu Aug 27/ Snappr Daniel Studio Blue-11.JPG'
assert original.exists()
shutil.copyfile(photo,W/'assets/stronger-abs-studio-blue-11.jpg')
shutil.copyfile(O/'assets/Daniel-source-inset.png',W/'assets/Daniel-source-inset.png')
# Preserve G04 exact card geometry, disclosure, words, full field and accent motion.
c=json.loads((O/'scripted/hf/configs/G04_After.json').read_text())[0];c['id']='R3_After';c['dur']=85/(30000/1001)
V.build([(H/'before-card/before-card.template.htm',c,[(photo,'photo.jpg')])],W/'hf',render=True,snap=.8)
# Small native media-card supplies the same moving Soft Blue field/rim. Native compositor
# isolates its label and photo regions; everything outside them remains transparent.
c=dict(id='R3_Craig',dur=185/(30000/1001),canvas=[480,650],hole=[20,185,425,428],radius=12,kicker={'x':18,'y':24,'px':31,'s':'The Dad Bod she likes'},chip=None)
V.build([(H/'media-card/media-card.template.htm',c,[])],W/'hf',render=True,snap=1)
rec=dict(photo={'path':str(photo),'sha256':sha(photo),'original_camera_photo':str(original),'original_sha256':sha(original),'classification':'existing finalized retouched real studio photograph; new round makes no physique alteration','selected':'studio-blue-11; visible stronger definition than reviewed black-shorts card'},craig={'path':str(W/'assets/Daniel-source-inset.png'),'sha256':sha(W/'assets/Daniel-source-inset.png'),'source':'ManVsStreet original source inset, same approved R1 component; no download','film_frames':[284,469],'text':'The Dad Bod she likes','rect':[20,455,425,428]},new_assets_downloaded=[],metered_spend=0)
(W/'asset-provenance.json').write_text(json.dumps(rec,indent=2))
for v in ['scripted','off_the_cuff']:
 p=W/v/'graphics-manifest.json';m=json.loads(p.read_text())
 for x in m:
  if x['id']=='G04_After':x.update(id='R3_After',mov=str(W/'hf/renders/R3_After.mov'),photo=str(photo))
 p.write_text(json.dumps(m,indent=2))
print('R3_ASSETS_READY',flush=True)
