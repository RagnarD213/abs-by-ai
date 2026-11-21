"""Create the DS-30 organic package and reserve one shared-waitlist entry on M2."""
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo
import fcntl
import hashlib
import json
import re
import shutil
import sys

from finish_setup import ROOT, WORK, FILM, APPROVED, MASTER, EXPECTED, sha, save, copy_verified
sys.path.insert(0, str(ROOT / 'scripts/blotato'))
import release_phases as rp
from organic_short_queue import post_plan
from ad_guard import assert_organic
from cover_guard import assert_video_cover
from danrosefit_migration import api_key, fetch_schedules

CONFIG = ROOT / 'scripts/blotato/configs/ds30-fitness-self-driving-car.json'
CT = ZoneInfo('America/Chicago')
SLUG = 'ds30-fitness-self-driving-car'


def link(platform):
    return f'https://sixpackabs.com/?utm_source={platform}&utm_medium=short&utm_campaign=fitness-self-driving-car&utm_content={SLUG}'


def local_slot(iso):
    d = datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(CT)
    return d.date(), d.strftime('%H:%M')


def reserve_slot(live, entries):
    taken = {local_slot(i['scheduledAt']) for i in live if i.get('scheduledAt')}
    for e in entries:
        p = ROOT / e['config']
        if p.exists() and e.get('job') != 'DS-30':
            v = json.loads(p.read_text())
            if v.get('main'):
                taken.add(local_slot(v['main']))
    # Include the other Mac's current reservations, which can lead the git mirror.
    extra = json.loads((WORK / 'm6-release-reservations.json').read_text())
    taken.update(local_slot(stamp) for stamp in extra['mains'])
    # The approved calendars reserve unfinished work as well as live/waiting posts.
    calendar = (ROOT / 'Docs/SHORTS_RELEASE_CALENDAR.md').read_text() + '\n' + extra['calendar']
    for line in calendar.splitlines():
        fields = [f.strip() for f in line.split('|')]
        if len(fields) != 7 or fields[-2] == 'Not booked':
            continue
        try:
            month = fields[1].split()[1]
            year = 2027 if month == 'Jan' else 2026
            when = datetime.strptime(f'{fields[1]} {year} {fields[3]}', '%a %b %d %Y %I %p')
            taken.add((when.date(), when.strftime('%H:%M')))
        except (ValueError, IndexError):
            pass
    # The approved Dec 10 5 PM Short occupies that day's evening slot.
    # Preserve other explicitly moved afternoon/evening releases in the same way.
    taken.update((day, '18:00') for day, hhmm in list(taken)
                 if hhmm not in ('09:00', '12:00', '18:00') and hhmm >= '15:00'
                 and '18:00' in rp.short_times(day))
    today = date(2026, 11, 16)
    day, hhmm = rp.next_short_slot(today, taken, {'kitchen': False, 'gym': False}, SLUG)
    when = datetime.combine(day, datetime.strptime(hhmm, '%H:%M').time(), CT)
    stamp = when.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    save(WORK / 'slot-verification.json', dict(main=stamp, local=when.isoformat(),
         kitchen=False, gym=False, phase=rp.phase_for(day).name,
         checked_against=['fresh live queue', 'M2 and M6 shared waitlists', 'M2 and M6 approved release calendars'],
         occupied_slots=len(taken), live_count=len(live), waiting_count=sum(not e.get('queued') for e in entries)))
    return stamp


def package():
    assert sha(MASTER) == EXPECTED
    assert json.loads((APPROVED / 'picks.json').read_text())['final_cover_approved']
    assert json.loads((WORK / 'backup-verification.json').read_text())['complete']
    uploads = json.loads((WORK / 'uploads.json').read_text())
    assert len(uploads) == 4 and all(v['remote_hash_verified'] for v in uploads.values())
    copy = json.loads((WORK / 'setup-copy.json').read_text())
    assert len(copy['pinned_comment']) < 180 and copy['pinned_comment'].endswith('?')
    caption = '\n\n'.join(copy[k] for k in ('hook', 'body', 'close'))
    tags = '#Fitness #SelfDrivingCar #Tesla #AI #Shorts'
    live = fetch_schedules(api_key())
    save(WORK / 'live-queue-package.json', live)
    waitpath = ROOT / 'scripts/blotato/video_waitlist.json'
    with open(str(waitpath) + '.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        entries = json.loads(waitpath.read_text())
        prior = [e for e in entries if e.get('job') == 'DS-30']
        assert len(prior) <= 1
        main = json.loads(CONFIG.read_text())['main'] if prior else reserve_slot(live, entries)
        config = dict(content_type='organic', source=str(MASTER.relative_to(ROOT)), source_sha256=EXPECTED,
                      slug=SLUG, campaign='fitness-self-driving-car',
                      title='Make Time for Fitness with a Self-Driving Car.',
                      video_url=uploads['master']['url'], tiktok_video_url=uploads['tiktok']['url'],
                      instagram_cover_url=uploads['instagram']['url'], youtube_cover_url=uploads['youtube']['url'],
                      main=main, keyword='AI', ai_generated=False, cover_ai_generated=True,
                      hook=copy['hook'], body=copy['body'], close=copy['close'], tags=tags,
                      youtube_description=caption+'\n\nWatch all my newest videos:\n'+link('youtube')+'\n\n'+tags,
                      youtube_tags=['self driving car', 'make time for fitness', 'Tesla', 'Tesla Model 3',
                                    'robotaxi', 'fitness', 'busy schedule', 'AI fitness', 'workout motivation',
                                    'time management', 'Dan Rose Fitness', 'Shorts'],
                      pinned_comment=copy['pinned_comment'],
                      pinned_comment_status='prepared; shared daily routine posts and pins after public release',
                      instagram_first_comment='Watch all my newest videos: '+link('instagram'),
                      caption_overrides={p: caption+'\n\nWatch all my newest videos:\n'+link(p)+'\n\n'+tags
                                         for p in ('facebook', 'instagram', 'tiktok')},
                      setup_status='waitlisted', approved_cover='R2-X4, car correction and final With A copy',
                      approved_cover_record=str((APPROVED / 'picks.json').relative_to(ROOT)),
                      kitchen=False, gym=False)
        public = json.dumps({k: config[k] for k in ['title','hook','body','close','youtube_description','pinned_comment','caption_overrides']},ensure_ascii=False)
        assert '—' not in public and '–' not in public
        assert_organic(config, texts=[config['title'], caption, config['youtube_description']], sources=[config['source']])
        # Register only this video's Facebook cover without replacing any other entries.
        repo_registry = ROOT / 'scripts/blotato/fb_reel_covers.json'
        cover = APPROVED / 'R2-X4-Car-Fixed-Instagram.jpg'
        record = dict(match=copy['hook'], cover=str(cover), w=1080, h=1920, job='DS-30', when=main)
        with open(str(repo_registry)+'.lock', 'a') as reglock:
            fcntl.flock(reglock, fcntl.LOCK_EX)
            records = json.loads(repo_registry.read_text())
            same = [r for r in records if r.get('match') == copy['hook']]
            if same:
                assert len(same) == 1 and same[0]['cover'] == str(cover)
            else:
                records.append(record)
            save(repo_registry, records)
        live_dir = Path.home() / '.absbyai/fb-reel-covers'
        livecover = live_dir / 'covers/DS30-R2-X4-Instagram.jpg'
        copy_verified(cover, livecover)
        live_registry = live_dir / 'fb_reel_covers.json'
        with open(str(live_registry)+'.lock','a') as reglock:
            fcntl.flock(reglock, fcntl.LOCK_EX)
            records = json.loads(live_registry.read_text())
            records = [r for r in records if r.get('match') != copy['hook']]
            records.append(dict(record, cover=str(livecover)))
            save(live_registry, records)
        plan = post_plan(config)
        for p in plan:
            assert_video_cover({'post':dict(accountId=p['account'], content=dict(platform=p['platform'],text=p['text'],mediaUrls=[p['media']]), target=p['target'])})
        save(CONFIG, config)
        save(WORK / 'platform-preflight.json', dict(ok=True, plans=plan,
             all_media_uploads_download_hash_verified=True, actual_tiktok_first_frame_checked=True,
             film_synthetic_flag=False, film_unchanged=True,
             reason_for_waitlist='Existing shared backlog has priority over the six currently free posts. No queue line jumping.'))
        if not prior:
            entries.append(dict(config=str(CONFIG.relative_to(ROOT)),kind='short',job='DS-30',
                                label=config['title'],added='2026-11-16',kitchen=False,gym=False))
            save(waitpath, entries)
        assert len([e for e in json.loads(waitpath.read_text()) if e.get('job')=='DS-30']) == 1
        save(WORK / 'waitlist-readback.json', dict(entry=next(e for e in entries if e.get('job')=='DS-30'),
             main=main, platforms=[dict(platform=p['platform'],account=p['account'],when=p['when'],target=p['target']) for p in plan],
             live_ds30_schedules=[i for i in live if 'utm_content='+SLUG in json.dumps(i)],
             state='waitlisted; reserved plan, not live scheduled'))
        (FILM / 'youtube-description.md').write_text(config['youtube_description']+'\n')
        save(FILM / 'youtube-tags.json',config['youtube_tags'])
        (FILM / 'pinned-question.txt').write_text(config['pinned_comment']+'\n')
        save(FILM / 'setup-config.json', config)
        print('Package and one shared-waitlist entry read back:',main,flush=True)


if __name__ == '__main__':
    package()
