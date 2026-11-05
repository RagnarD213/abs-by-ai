#!/usr/bin/env python3
"""Write the four approved release targets and register their verified cover."""
from pathlib import Path
import json,sys,shutil,hashlib,subprocess
R=Path(__file__).resolve().parents[4]
A=R/'Short-form video content/covers/approved-ds37'
WORK=Path('/Volumes/Expansion/_edit_work/DS-37-publish')
sys.path.insert(0,str(R/'scripts/blotato'))
from organic_short_queue import post_plan
from cover_guard import assert_video_cover
from ad_guard import assert_organic

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 copy=json.loads((Path(__file__).parent/'copy.json').read_text())
 uploads=json.loads((A/'uploads.json').read_text());picks=json.loads((A/'picks.json').read_text());slot=json.loads((A/'slot-plan.json').read_text())
 slug='ds37-dr-mike-dial';campaign='dr-mike-dial'
 link=lambda pf:f'https://absbyai.com/?utm_source={pf}&utm_medium=short&utm_campaign={campaign}&utm_content={slug}'
 tags='#Tirzepatide #WeightLoss #DrMikeIsraetel #Fitness #AbsByAI'
 lede=copy['hook']+'\n\n'+copy['body']+'\n\n'+copy['close']
 desc=copy['description_paragraph']+'\n\n'+copy['close']+'\n\nClip: Dr. Mike Israetel / Renaissance Periodization.\n\n'+link('youtube')+'\n\n'+tags+' #Shorts'
 cfg=dict(content_type='organic',source=uploads['video']['path'],title="Dr. Mike Says Tirzepatide Is A Dial For Your Body Weight. He's Right.",slug=slug,campaign=campaign,
 video_url=uploads['video']['url'],tiktok_video_url=uploads['tiktok']['url'],instagram_cover_url=uploads['instagram']['url'],youtube_cover_url=uploads['youtube']['url'],
 main=slot['main'],keyword='FOOD',ai_generated=False,hook=copy['hook'],body=copy['body'],close=copy['close'],tags=tags,youtube_description=desc,pinned_comment=copy['pinned_comment'],
 instagram_first_comment='Abs By AI: '+link('instagram'),cover_pick='B revised, round3 approved 2026-11-04',cover_ig_sha256=picks['files']['instagram']['sha256'],cover_yt_sha256=picks['files']['youtube']['sha256'],
 version='Exact approved R4 shortened off-the-cuff, 5% faster already baked in; no AI video footage',source_sha256=picks['film_sha256'],kitchen=False,
 youtube_tags=['tirzepatide','Dr Mike Israetel','appetite control','food noise','weight loss','weight maintenance','protein','GLP-1','fitness over 40','Dan Rose Fitness'],
 caption_overrides={
 'facebook':lede+'\n\nAbs By AI: '+link('facebook')+'\n\n'+tags,
 'instagram':lede+'\n\nMore at AbsByAI.com. Link in bio.\n\n'+tags,
 'tiktok':lede+'\n\nAbs By AI: '+link('tiktok')+'\n\n'+tags})
 for field in ['title','hook','body','close','youtube_description','pinned_comment']:
  assert '\u2014' not in cfg[field] and '\u2013' not in cfg[field]
 assert len(cfg['pinned_comment'])<180 and cfg['pinned_comment'].endswith('?')
 # Add only DS37's record to each independent registry, preserving all existing rows.
 src=Path(picks['files']['instagram']['path'])
 for reg,folder in [(R/'scripts/blotato/fb_reel_covers.json',R/'scripts/blotato/fb_covers'),(Path.home()/'.absbyai/fb-reel-covers/fb_reel_covers.json',Path.home()/'.absbyai/fb-reel-covers/covers')]:
  folder.mkdir(exist_ok=True,parents=True);dest=folder/'ds37-dr-mike-dial-approved-B-revised.jpg'
  if dest.exists():assert sha(dest)==sha(src)
  else:shutil.copy2(src,dest)
  before=reg.read_text();rows=json.loads(before);hits=[x for x in rows if x.get('job')=='DS-37' or x.get('match')==cfg['hook']];assert len(hits)<=1
  row=dict(job='DS-37',match=cfg['hook'],cover=str(dest),w=1080,h=1920,approved='Dan approved exact revised B, November 4 2026',when=cfg['main'])
  if hits:rows[rows.index(hits[0])]={**hits[0],**row}
  else:rows.append(row)
  assert reg.read_text()==before,'Registry changed concurrently; re-read before retry'
  reg.write_text(json.dumps(rows,indent=1)+'\n');saved=next(x for x in json.loads(reg.read_text()) if x.get('job')=='DS-37');assert sha(saved['cover'])==picks['files']['instagram']['sha256']
 assert_organic(cfg,texts=[cfg[x] for x in ['title','hook','body','close','youtube_description']],sources=[cfg['source']])
 plans=post_plan(cfg);assert len(plans)==4
 for p in plans:
  assert_video_cover({'post':{'accountId':p['account'],'content':{'platform':p['platform'],'text':p['text'],'mediaUrls':[p['media']]},'target':p['target']}})
 cp=R/'scripts/blotato/configs/ds37-dr-mike-dial.json'
 if cp.exists():assert json.loads(cp.read_text())==cfg,'Unexpected existing config differs'
 else:cp.write_text(json.dumps(cfg,indent=2)+'\n')
 (WORK/'planned-targets.json').write_text(json.dumps(plans,indent=2));(WORK/'preflight.json').write_text(json.dumps({'four_targets_pass':True,'ad_guard_pass':True,'cover_guard_pass':True,'config':str(cp),'when':cfg['main'],'no_posts_created':True},indent=2))
 # File owner-readable packaging with the exact config metadata and caption sidecar.
 delivery=R/'Short-form video content/Dr Mike Dial SFC R4/Setup';delivery.mkdir(exist_ok=True)
 (delivery/'youtube-description.txt').write_text(cfg['youtube_description']+'\n')
 (delivery/'metadata.json').write_text(json.dumps(cfg,indent=2)+'\n')
 for name in ['picks.json','uploads.json']:shutil.copy2(A/name,delivery/name)
 print('Four targets and cover/ad guards pass. Config saved; no posts created.',flush=True)
if __name__=='__main__':main()
