#!/usr/bin/env python3
"""Daily private queue refresh and top-up dry run. No schedule mutations.

The parent reviews migration-plan.json before any later activation. No --apply
entrypoint exists while activation is held. The existing cloud morning routine
can run this before collection and again after creating its brief.
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

from master_queue import Inventory, locked, from_live, import_studio, plan_topup, identity
from review_queue import review
from public_tiles import published_posts, acquire, post_id
from native_youtube import native_records, add_native_rows


def private_json(file, data):
    temp = file.with_suffix('.tmp')
    with temp.open('w') as f:
        import os
        os.chmod(temp, 0o600)
        json.dump(data, f, indent=2)
    temp.replace(file)


def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def check(url, now):
    parsed = urlparse(url)
    # Exact provider domains only. Never fetch private IPs, credentials or arbitrary
    # caption destinations. Such links stay unknown for connected/browser review.
    hosts = {'database.blotato.io', 'i.ytimg.com', 'i9.ytimg.com', 'absbyai.com', 'sixpackabs.com', 'youtu.be', 'www.youtube.com'}
    if parsed.scheme != 'https' or parsed.hostname not in hosts or parsed.username or parsed.password or parsed.port not in (None, 443):
        return {'checkedAt': now.isoformat(), 'status': None}
    try:
        with build_opener(NoRedirect()).open(Request(url, method='HEAD'), timeout=10) as response:
            return {'checkedAt': now.isoformat(), 'status': response.status, 'mime': response.headers.get('Content-Type')}
    except HTTPError as exc:
        return {'checkedAt': now.isoformat(), 'status': exc.code}
    except Exception:
        return {'checkedAt': now.isoformat(), 'status': None}


def photo_hash(url):
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname != 'database.blotato.io' or parsed.username or parsed.password or parsed.port not in (None,443):
        return None
    try:
        with build_opener(NoRedirect()).open(Request(url), timeout=10) as response:
            if response.status != 200 or not (response.headers.get('Content-Type','').startswith('image/') or response.headers.get('Content-Type','').startswith('application/octet-stream')):
                return None
            data = response.read(8 * 1024 * 1024 + 1)
            is_image = data.startswith(b'\xff\xd8\xff') or data.startswith(b'\x89PNG\r\n\x1a\n')
            return hashlib.sha256(data).hexdigest() if is_image and len(data) <= 8 * 1024 * 1024 else None
    except Exception:
        return None


def public_profile_check(platform, url, now):
    # Read-only profile access is not a cover comparison. Keep that distinction
    # even when the platform returns a successful login wall or generic shell.
    result = {'platform': platform, 'profileUrl': url, 'checkedAt': now.isoformat(), 'status': 'unverified',
              'reason': 'No correlated public post tile with approved cover evidence is available'}
    try:
        with build_opener(NoRedirect()).open(Request(url, headers={'User-Agent':'AbsByAI private release review'}), timeout=10) as response:
            result['httpStatus'] = response.status
            response.read(512000)
    except HTTPError as exc:
        result['httpStatus'] = exc.code
        result['reason'] = 'Public profile read unavailable; no visual match inferred'
    except Exception:
        result['httpStatus'] = None
        result['reason'] = 'Public profile read unavailable; no visual match inferred'
    return result
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--state-dir', type=Path, required=True)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--snapshot', type=Path)
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    project = args.project_root.resolve()
    with locked(args.state_dir) as directory:
        inventory = Inventory(directory)
        if args.live:
            api = load_module('existing_blotato', project / 'scripts/blotato/danrosefit_migration.py')
            live = api.fetch_schedules(api.api_key())
            try: published=published_posts(api,api.api_key(),now)
            except Exception: published=None
        elif args.snapshot:
            live = json.loads(args.snapshot.read_text())
        else:
            parser.error('Use --live or a complete read-only --snapshot')
        for item in live:
            inventory.put(from_live(item, now.isoformat()), item)
        native={'status':'missing','reason':'Native YouTube owner API has not been read','checkedAt':now.isoformat()}
        if args.live:
            try:
                public_ids=[post_id('youtube',p.get('state',{}).get('postUrl','')) for p in published or [] if p['platform']=='youtube']
                process=subprocess.run(['node',str(Path(__file__).with_name('native_youtube.js'))],input=json.dumps([i for i in public_ids if i]),capture_output=True,text=True,timeout=180)
                native=json.loads(process.stdout)
            except Exception:
                native={'status':'error','reason':'Native YouTube read failed; schedules remain unknown','checkedAt':now.isoformat()}
            private_json(directory/'native-youtube-source.json',native)
        native_rows=native_records(native)
        for r in native_rows:inventory.put(r,{'source':'youtube_native','videoId':r['nativeVideoId'],'checkedAt':native['checkedAt']})
        manifest = json.loads((project / 'Handoffs/handoff-20261003-approved-studio-posts-27-blotato.json').read_text())
        studio_plan = json.loads((project / 'scripts/blotato/studio27_plan.json').read_text())
        # Restrict byte verification to exact approved photo caption/account/date twins.
        captions = {p['caption'] for p in manifest['posts']}
        photo_urls = sorted({u for i in live if i['draft']['content'].get('text') in captions for u in i['draft']['content'].get('mediaUrls',[])})
        with ThreadPoolExecutor(max_workers=8) as pool:
            hashes = dict(zip(photo_urls, pool.map(photo_hash, photo_urls)))
        import_studio(inventory, studio_plan, manifest, now.isoformat(), live, hashes)
        # Long-form queue declares its category explicitly in its campaign link.
        for r in inventory.records():
            body = json.dumps(r['payload'])
            if 'utm_campaign=longform' in body:
                r['kind'] = 'longform'
                groups = set(re.findall(r'utm_content=([A-Za-z0-9_-]+)',body))
                if len(groups) == 1:
                    r['releaseGroup'] = groups.pop()
                inventory.put(r, {'source': 'longform campaign marker', 'checkedAt': now.isoformat()})
        records = inventory.records()
        for r in records:
            if r.get('releaseGroup') and r['platform'] != 'youtube':
                youtube = [yt for yt in records if yt['platform'] == 'youtube' and yt.get('releaseGroup') == r['releaseGroup']]
                if len(youtube) == 1:
                    r['youtubeReleaseAt'] = youtube[0]['scheduledAt']
                    inventory.put(r, {'source':'unique explicit longform campaign group','youtubePlacementId':youtube[0]['id'],'checkedAt':now.isoformat()})
        guard = load_module('existing_ad_guard', project / 'scripts/blotato/ad_guard.py')
        records = inventory.records()
        live_ids = {identity({k:i['draft'][k] for k in ('accountId','content','target')},i['scheduledAt']) for i in live}
        # Disappearance may mean posted, deleted or failed. Never infer public release.
        current = [r for r in records if r['id'] in live_ids]
        preview_file=directory/'native-preview-sources.json'
        preview_sources=json.loads(preview_file.read_text()) if preview_file.exists() else {}
        preliminary = review(current, live, now)
        urls = {u for row in preliminary['rows'] for u in (row.get('mediaUrl'), row.get('coverReviewUrl')) if u}
        urls.update(u.rstrip('.,!;') for row in preliminary['rows'] for u in re.findall(r'https://[^\s<>"\)]+', row['caption']))
        from datetime import timedelta
        from master_queue import stamp
        urls.update(u for r in records if r['approval']['status'] == 'approved' and now < stamp(r['scheduledAt']) < now+timedelta(days=30) for u in r['media'])
        urls.update(v['sourceUrl'] for v in preview_sources.values() if v.get('sourceUrl'))
        urls.update(r['cover'] for r in native_rows if r['cover'])
        urls.update(u.rstrip('.,!;') for r in native_rows for u in re.findall(r'https://[^\s<>"\)]+',r['caption']))
        with ThreadPoolExecutor(max_workers=8) as pool:
            checks = dict(zip(sorted(urls), pool.map(lambda u: check(u, now), sorted(urls))))
        evidence_file = directory / 'public-tile-evidence.json'
        evidence = json.loads(evidence_file.read_text()) if evidence_file.exists() else {}
        queue = review(current, live, now, checks, evidence)
        queue['sourceCoverage']['youtubeStudio']=native['status']
        queue['coverageNote']=('Native YouTube owner API verified '+native['channel']['id']+'; '+str(native.get('uniqueUploads',native['uploadsEnumerated']))+' unique uploads checked, '+str(len(native_rows))+' native schedules observed. Approved-cover visual comparisons remain evidence-bound.' if native['status']=='ok' else native.get('reason','Native YouTube schedules remain unknown'))
        visibility_file=directory/'expected-youtube-visibility.json'
        visibility_exceptions=json.loads(visibility_file.read_text()) if visibility_file.exists() else {}
        conflicts={key:value for key,value in native.get('publicChecks',{}).items() if value!='public' and not (visibility_exceptions.get(key,{}).get('expectedStatus')==value and visibility_exceptions[key].get('reference') and visibility_exceptions[key].get('quote'))}
        if conflicts:queue['coverageNote']+=' Release alert: '+', '.join(key+' is '+value for key,value in conflicts.items())+' despite Blotato published status.'
        add_native_rows(queue,native_rows,checks,preview_sources)
        if args.live:
            try:
                if published is None: raise ValueError('Published source unavailable')
                private_json(directory / 'published-source.json', {'checkedAt':now.isoformat(),'items':published})
                observations_file = directory / 'public-grid-observations.json'
                observations = json.loads(observations_file.read_text()) if observations_file.exists() else []
                cover_file=directory/'approved-public-covers.json'
                approved_covers=json.loads(cover_file.read_text()) if cover_file.exists() else {}
                queue['released'], profile_checks = acquire(records,published,now,directory,private_json,observations,evidence,native,approved_covers,visibility_exceptions)
                queue['coverageNote'] += ' '+str(len(published))+' Blotato published URLs checked. '+ ' '.join(p['platform']+': HTTP '+str(p['httpStatus'])+', '+str(p['tileCount'])+' HTTP/'+str(p['browserTileCount'])+' browser tiles.' for p in profile_checks)
            except Exception:
                queue['coverageNote'] += ' Blotato published-post read failed; post-release coverage remains unknown.'
        plan = plan_topup(inventory, live, now, guard.assert_organic, checks)
        master = [{k: r[k] for k in ('id', 'platform', 'account', 'scheduledAt', 'title', 'caption', 'media', 'cover', 'kind', 'approval', 'provenance')} for r in records]
        private_json(directory / 'migration-plan.json', plan)
        private_json(directory / 'social-master-export.json', master)
        private_json(directory / 'social-queue.json', queue)
        private_json(directory / 'social-url-checks.json', checks)
        private_json(directory / 'blotato-source.json', {'checkedAt': now.isoformat(), 'items': live})
        print(json.dumps({'inventoryCount': len(master), 'liveCount': len(live), 'wouldCreate': len(plan['create']),
                          'held': len(plan['held']), 'overflow': len(plan['overflow']), 'sevenDayRows': len(queue['rows']),
                          'planDigest': plan['planDigest'], 'nativeYouTube': native['status'], 'scheduleChanged': False}))


if __name__ == '__main__':
    main()
