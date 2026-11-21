from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[4];W=Path('/Volumes/Expansion/_edit_work/ds16-publish');pre=json.load(open(W/'preflight.json'));assert pre['ok'];v=json.load(open(R/'scripts/blotato/configs/ds16-last-ten-pounds.json'))
p=R/'scripts/blotato/video_waitlist.json';raw=p.read_text();before=json.loads(raw);match=[x for x in before if x['job']=='DS-16'];assert len(match)<=1
entry={'config':'scripts/blotato/configs/ds16-last-ten-pounds.json','kind':'short','job':'DS-16','label':'How To Lose The Last Ten Pounds Of Fat','added':'2026-11-04','kitchen':False,'gym':False,'note':'HQ V3 verified and approved by Dan; X2 unchanged approved. All media and covers uploaded, full-download SHA256 verified. Planned Jan2 2027 at6PM Central. Ready for existing shared daily top-up; no release hold.'}
if not match:
 (W/'waitlist-before.json').write_text(raw);assert p.read_text()==raw
 block='\n'.join(' '+line for line in json.dumps(entry,indent=1,ensure_ascii=False).splitlines())
 p.write_text(raw.rstrip()[:-1].rstrip()+',\n'+block+'\n]\n')
after=json.loads(p.read_text());assert len([x for x in after if x['job']=='DS-16'])==1;assert [x for x in after if x['job']!='DS-16']==[x for x in before if x['job']!='DS-16']
# The dated calendar now records this completed Short's slot.
p=R/'Docs/SHORTS_RELEASE_CALENDAR.md';s=p.read_text();old='| Sat Jan 2 | 3 | 6 PM | OPEN | Not booked |';new='| Sat Jan 2 | 3 | 6 PM | How To Lose The Last Ten Pounds Of Fat (DS-16) | Waitlist |'
if old in s:s=s.replace(old,new)
else:assert new in s
s=s.replace('Still unedited, no date: Lose The Last 10 Pounds (DS-16) and other Aug 28 Shorts','Still unedited, no date: other Aug 28 Shorts');p.write_text(s)
# Refresh only DS-16 in the two existing Facebook registries.
for p in [R/'scripts/blotato/fb_reel_covers.json',Path.home()/'.absbyai/fb-reel-covers/fb_reel_covers.json']:
 d=json.load(open(p));row=next(x for x in d if x.get('job')=='DS-16');row.update(when=v['main'],note='X2 approved unchanged2026-11-03. HQ verified; waitlistedJan2 2027 at6PM Central, not a live schedule.');p.write_text(json.dumps(d,indent=1,ensure_ascii=False)+'\n')
A=R/'Short-form video content/covers/approved-ds16';pick=json.load(open(A/'picks.json'));pick.update(master_status='HQ verified and media uploaded; shared waitlist, not scheduled',film_sha256=v['master_sha256'],planned_release=v['main'],config='scripts/blotato/configs/ds16-last-ten-pounds.json')
D=Path(v['source']).parent;E=Path('/Volumes/Extreme/Short-form video content/How To Lose The Last Ten Pounds Of Fat - DS-16')
for folder in [A,D/'Approved covers',E/'Approved covers']:(folder/'picks.json').write_text(json.dumps(pick,indent=2,ensure_ascii=False)+'\n')
# Durable exact-file evidence beside the delivered master, on both local drives.
for folder in [D/'Setup records',E/'Setup records']:
 folder.mkdir(parents=True,exist_ok=True)
 for name in ['hq-verification.json','tiktok-verification.json','master.json','uploads.json','preflight.json','slot.json','drive-backup.json']:
  shutil.copy2(W/name,folder/name)
 shutil.copy2(R/'scripts/blotato/configs/ds16-last-ten-pounds.json',folder/'release-config.json')
(W/'waiting-list-receipt.json').write_text(json.dumps({'entry':next(x for x in after if x['job']=='DS-16'),'main':v['main'],'local':'2027-01-02 18:00 America/Chicago','queue_capacity':200,'live_posts_for_DS16':0,'other_waitlist_entries_unchanged':True,'config_sha256':hashlib.sha256((R/'scripts/blotato/configs/ds16-last-ten-pounds.json').read_bytes()).hexdigest()},indent=2))
# Add only this verified HQ delivery to the editor's dedupe ledger.
p=R/'.claude/skills/editor-deliveries/state.json';d=json.load(open(p));id='1-GGtoEbTEtjn433cZbpc7N4TAP_-9goh'
if not any(x.get('drive_id')==id for x in d.get('filed',[])):
 d.setdefault('filed',[]).append({'drive_id':id,'editor':'Muhammad','title':v['title'],'kind':'content','number':'DS-16','path':str(Path(v['source']).relative_to(R)),'size':69460867,'filed_on':'2026-11-04','sha256':v['master_sha256'],'note':'V3 HD directly delivered by Muhammad; Dan approved HQ in Upwork. Matches V3 timeline.'});p.write_text(json.dumps(d,indent=1,ensure_ascii=False)+'\n')
print('Shared waiting list read-back verified; Jan2 2027 at6PM Central. No other entry changed.')
