from pathlib import Path
from PIL import Image
import json,hashlib,sys
ROOT=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI');w=Path(__file__).parent
CANON='/Users/danielrose/Projects/Claude/Projects/Abs By AI'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
dates=['2027-02-08T15:00:00.000Z','2027-02-10T15:00:00.000Z','2027-02-12T15:00:00.000Z']
names=['restaurants-dont-care-about-your-fitness-goals','you-dont-deserve-a-vacation-until-youre-ripped','if-you-cant-afford-a-gym-you-cant-afford-therapy']
meta=json.loads((w/'metadata-draft.json').read_text());media=json.loads((w/'approved-media.json').read_text())
uploads=json.loads((w/'uploads.json').read_text());tt={r['short']:r for r in json.loads((w/'tiktok-verification.json').read_text())}
assert len(uploads)==12 and all(r.get('remote_hash_verified') for r in uploads.values())
configs=[];registry_entries=[]
for m,r,name,day in zip(meta,media,names,dates):
 n=m['short'];slug=f'sl21-short{n}';tags=['#Fitness #FatLoss #FitnessOnABudget #Shorts','#Fitness #Vacation #FitnessHabits #Shorts','#Fitness #GymMembership #PhysicalHealth #Shorts'][n-1]
 base='\n\n'.join(m[k] for k in ['hook','body','close'])
 def link(source):return f'https://absbyai.com/?utm_source={source}&utm_medium=short&utm_campaign=what-to-cut&utm_content={slug}'
 disclosure='\n\nSome footage in this video is AI-generated and labeled on screen.' if n<3 else ''
 description=base+'\n\nTry Abs By AI:\n'+link('youtube')+'\n\nFull video on this channel: What To Cut To Afford Getting In Shape'+disclosure+'\n\n'+tags
 v={'content_type':'organic','source':str(Path(r['source']).relative_to(ROOT)),'slug':slug,'campaign':'what-to-cut','title':m['title'],'video_url':uploads[f'short{n}-master']['url'],'tiktok_video_url':uploads[f'short{n}-tiktok']['url'],'instagram_cover_url':uploads[f'short{n}-instagram']['url'],'youtube_cover_url':uploads[f'short{n}-youtube']['url'],'main':day,'keyword':['FOOD','COACH','COACH'][n-1],'ai_generated':n<3,'hook':m['hook'],'body':m['body'],'close':m['close'],'tags':tags,'youtube_tags':m['tags'],'youtube_description':description,'pinned_comment':m['pinned_comment'],'instagram_first_comment':'Try Abs By AI: '+link('instagram'),'parent_config':'scripts/blotato/configs/ro20b-what-to-cut.json','kitchen':True,'gym':False,'filming_set':'kitchen (Aug 3)','approved_cover':['Restaurant R4 X2','Vacation original X7','Therapy X3, large bubble R4'][n-1],'approval_date':'2026-11-15','media_sha256':{'master':r['master_sha256'],'tiktok':tt[n]['sha256'],'ig':uploads[f'short{n}-instagram']['sha256'],'yt':uploads[f'short{n}-youtube']['sha256']},'caption_overrides':{}}
 v['caption_overrides']['facebook']=base+'\n\nTry Abs By AI:\n'+link('facebook')+disclosure+'\n\n'+tags
 v['caption_overrides']['instagram']=base+f'\n\nComment {v["keyword"]} and I\'ll send you the Abs By AI link.'+disclosure+'\n\n'+tags
 v['caption_overrides']['tiktok']=base+'\n\nAbs By AI, link in bio.\n'+link('tiktok')+disclosure+'\n\n'+tags
 assert not any(c in json.dumps(v,ensure_ascii=False) for c in ['\u2013','\u2014'])
 file=ROOT/'scripts/blotato/configs'/f'{slug}-{name}.json'
 file.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n');configs.append(str(file.relative_to(ROOT)))
 # The canonical M2 username is an existing symlink on M6, so this checked
 # source path works on both production Macs. The live installer has its own copy.
 cover=ROOT/'scripts/blotato/fb_covers'/f'{slug}-approved.png';cover.write_bytes(Path(r['covers']['instagram']['file']).read_bytes())
 assert sha(cover)==r['covers']['instagram']['sha256']
 registry_entries.append({'job':'SL-21','slug':slug,'schedule':'pending-'+slug,'when':day,'match':m['hook'],'cover':CANON+'/scripts/blotato/fb_covers/'+cover.name,'w':1080,'h':1920,'approved':v['approved_cover']+', Dan approved 2026-11-15','sha256':sha(cover)})
reg=ROOT/'scripts/blotato/fb_reel_covers.json';rows=json.loads(reg.read_text());slugs={e['slug'] for e in registry_entries};rows=[e for e in rows if e.get('slug') not in slugs]+registry_entries;reg.write_text(json.dumps(rows,indent=2)+'\n')
live=Path.home()/'.absbyai/fb-reel-covers';(live/'covers').mkdir(parents=True,exist_ok=True)
installed=json.loads((live/'fb_reel_covers.json').read_text())
installed=[e for e in installed if e.get('slug') not in slugs]
for e in registry_entries:
 source=Path(e['cover']);dst=live/'covers'/source.name;dst.write_bytes(source.read_bytes());assert sha(dst)==e['sha256'];installed.append({**e,'cover':str(dst)})
(live/'fb_reel_covers.json').write_text(json.dumps(installed,indent=2)+'\n')
(w/'config-paths.json').write_text(json.dumps(configs,indent=2))
(w/'facebook-entries.json').write_text(json.dumps(registry_entries,indent=2))
print('Three complete configs and M6 Facebook installer entries saved.',flush=True)
