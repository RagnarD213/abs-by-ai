from pathlib import Path
import json,hashlib,shutil
root=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');w=Path('/Users/danielrose/Projects/_edit_work/sl13-setup-20261107');here=root/'scripts/blotato';live=Path.home()/'.absbyai/fb-reel-covers';(live/'covers').mkdir(parents=True,exist_ok=True)
meta=json.loads((w/'packaging/metadata.json').read_text());picks=list(json.loads((root/'Short-form video content/covers/approved-sl13/picks.json').read_text())['covers'].values());slots=json.loads((w/'planned-slots-final.json').read_text())['slots'];new=[]
rp=here/'fb_reel_covers.json';lp=live/'fb_reel_covers.json';reg=json.loads(rp.read_text());installed=json.loads(lp.read_text())
(w/'facebook-source-before.json').write_text(json.dumps(reg,indent=2));(w/'facebook-live-before.json').write_text(json.dumps(installed,indent=2))
for m,p,s in zip(meta,picks,slots):
 dst=here/'fb_covers'/f'{m["slug"]}-approved.png';shutil.copy2(p['instagram'],dst);ld=live/'covers'/dst.name;shutil.copy2(dst,ld)
 h=hashlib.sha256(dst.read_bytes()).hexdigest();assert h==p['instagram_sha256']==hashlib.sha256(ld.read_bytes()).hexdigest()
 line=m['caption_overrides']['facebook'].strip().split('\n')[0];r={'job':'SL-13 '+p['short'],'slug':m['slug'],'match':line,'cover':str(dst),'w':1080,'h':1920,'approved':'Dan selected '+p['pick']+' on2026-11-08; both exact platform layouts approved.','sha256':h,'when':s['main']}
 hit=[x for x in reg if x['match'].strip().split('\n')[0]==line];assert not hit or all(x.get('slug')==m['slug'] for x in hit),'caption conflict'
 reg=[x for x in reg if x.get('slug')!=m['slug']]+[r]
 lr=dict(r,cover=str(ld));installed=[x for x in installed if x.get('slug')!=m['slug']]+[lr];new.append(r)
for path,rows in [(rp,reg),(lp,installed)]:
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(rows,indent=2));tmp.replace(path)
(w/'facebook-owned-rows.json').write_text(json.dumps(new,indent=2));print('Registered3 approved covers in repo and live installer; all pixels/hash identities match; preserved existing entries.')
