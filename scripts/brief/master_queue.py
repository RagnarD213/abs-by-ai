"""Private durable inventory and conservative, date-preserving Blotato planner.

SQLite is the unlimited local source of truth. Imports preserve source versions;
neither a draft nor a filename grants approval. This module never makes HTTP writes.
"""
import contextlib
import fcntl
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

CT = ZoneInfo('America/Chicago')
CAP = 200


def stamp(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('Date needs an explicit timezone')
    return dt.astimezone(timezone.utc)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def identity(payload, at):
    # A different platform/account/date is a separate placement, never collapsed.
    return digest({'post': payload, 'at': stamp(at).isoformat()})


@contextlib.contextmanager
def locked(directory):
    directory = Path(directory).expanduser().resolve()
    for parent in (directory, *directory.parents):
        if (parent / '.git').exists():
            raise ValueError('Runtime queue must stay outside Git')
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if directory.is_symlink() or directory.stat().st_mode & 0o077:
        raise ValueError('Runtime directory must be private')
    fd = os.open(directory / 'social.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield directory
    finally:
        os.close(fd)


class Inventory:
    def __init__(self, directory):
        self.directory = Path(directory)
        file = Path(directory) / 'social-master.sqlite'
        if file.is_symlink():
            raise ValueError('Symlinked database')
        self.db = sqlite3.connect(file)
        os.chmod(file, 0o600)
        self.db.execute('CREATE TABLE IF NOT EXISTS placements (id TEXT PRIMARY KEY, record TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS evidence (id TEXT, hash TEXT, source TEXT, PRIMARY KEY(id, hash))')
        self.db.execute('CREATE TABLE IF NOT EXISTS submissions (id TEXT PRIMARY KEY, state TEXT NOT NULL, receipt TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS aliases (id TEXT PRIMARY KEY, canonical TEXT NOT NULL)')

    def put(self, record, evidence):
        key = identity(record['payload'], record['scheduledAt'])
        record['id'] = key
        previous = self.db.execute('SELECT record FROM placements WHERE id=?', (key,)).fetchone()
        if previous:
            old = json.loads(previous[0])
            record['provenance'] = list({digest(p): p for p in old['provenance'] + record['provenance']}.values())
            # Explicit approval survives a read-only queue refresh.
            if old['approval']['status'] == 'approved' and record['approval']['status'] != 'approved':
                record['approval'] = old['approval']
            for field in ('kind', 'youtubeReleaseAt', 'youtubePublicVerifiedAt', 'cover', 'tiktokCoverVerified', 'cropVerified','approvedCoverSHA256','publicPostUrl'):
                if old.get(field) is not None and record.get(field) is None:
                    record[field] = old[field]
        self.db.execute('INSERT INTO placements VALUES (?,?) ON CONFLICT(id) DO UPDATE SET record=excluded.record', (key, json.dumps(record)))
        self.db.execute('INSERT OR IGNORE INTO evidence VALUES (?,?,?)', (key, digest(evidence), json.dumps(evidence)))
        self.db.commit()
        return key

    def records(self):
        return [json.loads(r[0]) for r in self.db.execute('SELECT record FROM placements WHERE id NOT IN (SELECT id FROM aliases) ORDER BY id')]

    def alias(self, old, canonical):
        if old != canonical:
            self.db.execute('INSERT INTO aliases VALUES (?,?) ON CONFLICT(id) DO UPDATE SET canonical=excluded.canonical', (old, canonical))
            self.db.commit()

    def submission(self, key):
        row = self.db.execute('SELECT state FROM submissions WHERE id=?', (key,)).fetchone()
        return row[0] if row else None

    def submitted(self, key, state, receipt=None):
        self.db.execute('INSERT INTO submissions VALUES (?,?,?) ON CONFLICT(id) DO UPDATE SET state=excluded.state, receipt=excluded.receipt', (key, state, json.dumps(receipt)))
        self.db.commit()


def from_live(item, checked_at):
    payload = {k: item['draft'][k] for k in ('accountId', 'content', 'target')}
    target, content = payload['target'], payload['content']
    return {'payload': payload, 'scheduledAt': stamp(item['scheduledAt']).isoformat(),
            'platform': content['platform'], 'account': str(payload['accountId']),
            'title': target.get('title') or content.get('text', '').split('\n')[0][:220] or 'Scheduled post',
            'caption': content.get('text', ''), 'media': content.get('mediaUrls', []),
            'cover': target.get('thumbnailUrl') or target.get('coverImageUrl'),
            'kind': 'photo' if content.get('mediaUrls') and all(Path(u.split('?')[0]).suffix.lower() in ('.jpg', '.jpeg', '.png') for u in content['mediaUrls']) else 'unknown',
            'approval': {'status': 'scheduled_observed', 'reference': 'blotato:' + str(item['id']), 'quote': 'Observed live schedule; original approval not inferred'},
            'provenance': [{'source': 'blotato', 'sourceId': str(item['id']), 'checkedAt': checked_at}],
            'scheduleId': str(item['id'])}


def import_studio(inventory, plan, manifest, checked_at, live=None, media_hashes=None):
    posts = {p['id']: p for p in manifest.get('posts', [])}
    # The original handoff is explicit approval of these 27 photo posts, not every draft.
    approved = bool(manifest.get('approved_on') and manifest.get('approval_quote') and manifest.get('status', '').startswith('Approved'))
    for slot in plan:
        post = posts.get(slot['post'])
        if not post:
            continue
        payload = {'accountId': str(slot['account']), 'content': {'platform': slot['platform'], 'text': post['caption'], 'mediaUrls': slot['media']},
                   'target': {'targetType': slot['platform'], **({'pageId': '1294282227094660'} if slot['platform'] == 'facebook' else {})}}
        record = {'payload': payload, 'scheduledAt': stamp(slot['scheduledTime']).isoformat(), 'platform': slot['platform'], 'account': str(slot['account']),
                  'title': post['title'], 'caption': post['caption'], 'media': slot['media'], 'cover': slot['media'][0] if slot['media'] else None, 'kind': 'photo',
                  'approval': {'status': 'approved' if approved else 'pending', 'reference': 'handoff-20261003-approved-studio-posts-27-blotato:' + slot['post'], 'quote': manifest.get('approval_quote', '')},
                  'provenance': [{'source': 'studio27_plan', 'sourceId': slot['post'], 'checkedAt': checked_at}]}
        if post.get('images') and post['images'][0].get('sha256'):
            record['approvedCoverSHA256'] = post['images'][0]['sha256']
        old_key = identity(payload, record['scheduledAt'])
        # Blotato re-hosts media per post. Exact caption/account/date alone is not
        # enough to declare equal assets. Join only with all approved byte hashes.
        expected = [i.get('sha256') for i in post.get('images', [])]
        for item in live or []:
            draft = item['draft']
            urls = draft['content'].get('mediaUrls', [])
            if (str(draft['accountId']) == record['account'] and stamp(item['scheduledAt']) == stamp(record['scheduledAt'])
                    and draft['content'].get('text') == record['caption'] and draft['content'].get('platform') == record['platform']
                    and expected and all(expected) and [(media_hashes or {}).get(u) for u in urls] == expected):
                record.update(payload={k: draft[k] for k in ('accountId','content','target')},media=urls,cover=urls[0],scheduleId=str(item['id']))
                record['provenance'].append({'source':'blotato','sourceId':str(item['id']),'checkedAt':checked_at})
                break
        key = inventory.put(record, {'slot': slot, 'post': post, 'approval': record['approval'], 'verifiedLiveMediaHashes': [(media_hashes or {}).get(u) for u in record['media']]})
        inventory.alias(old_key, key)


def longform_errors(records):
    errors = {}
    weeks = {}
    for r in records:
        if r.get('kind') != 'longform':
            continue
        at = stamp(r['scheduledAt']).astimezone(CT)
        problems = []
        if r['platform'] == 'youtube':
            if at.weekday() != 6 or (at.hour, at.minute, at.second) != (9, 0, 0):
                problems.append('Long-form YouTube must release Sunday at 9 AM Central')
            week = at.date() - timedelta(days=(at.weekday() + 1) % 7)
            weeks.setdefault(week, []).append(r['id'])
        else:
            first = r.get('youtubeReleaseAt')
            if not first:
                problems.append('YouTube first-release date is unknown')
            else:
                yt = stamp(first).astimezone(CT)
                monday = datetime.combine(yt.date() + timedelta(days=1), datetime.min.time(), CT).replace(hour=9)
                if yt.weekday() != 6 or at < monday:
                    problems.append('Other platforms must wait until Monday at 9 AM after Sunday YouTube')
                if not r.get('youtubePublicVerifiedAt'):
                    problems.append('Public YouTube release is not verified; other platforms remain held')
        if problems:
            errors[r['id']] = problems
    for ids in weeks.values():
        if len(ids) > 1:
            for key in ids:
                errors.setdefault(key, []).append('More than one YouTube long-form in this Sunday week')
    return errors


def plan_topup(inventory, live, now, guard, asset_checks=None):
    records = inventory.records()
    existing = {identity({k: i['draft'][k] for k in ('accountId', 'content', 'target')}, i['scheduledAt']) for i in live}
    occupied = {(str(i['draft']['accountId']), stamp(i['scheduledAt'])) for i in live}
    rules = longform_errors(records)
    result = {'checkedAt': now.isoformat(), 'scheduleChanged': False, 'activation': 'held_for_parent_review', 'cap': CAP,
              'existingCount': len(live), 'create': [], 'held': [], 'overflow': [], 'outsideWindow': [], 'alreadyScheduled': []}
    end = now + timedelta(days=30)
    for r in sorted(records, key=lambda r: r['scheduledAt']):
        key, at = r['id'], stamp(r['scheduledAt'])
        if key in existing or inventory.submission(key) == 'confirmed':
            result['alreadyScheduled'].append(key)
            continue
        reasons = []
        if inventory.submission(key):
            reasons.append('Prior submission is unresolved; reconcile before retry')
        if r['approval']['status'] != 'approved':
            reasons.append('Explicit approval is absent; a live schedule alone cannot authorize recreation')
        if at <= now + timedelta(hours=2):
            reasons.append('Authorized date has passed or is within two hours; no automatic reslotting')
        if at >= end:
            result['outsideWindow'].append(key)
            continue
        if r.get('kind') == 'unknown':
            reasons.append('Content kind is unknown; long-form rule cannot be checked')
        checks = asset_checks or r.get('assetChecks') or {}
        asset_ready = True
        for url in r.get('media', []):
            evidence = checks.get(url, {})
            try:
                age = (now - stamp(evidence['checkedAt'])).total_seconds()
                if not 0 <= age <= 12 * 3600 or evidence.get('status') not in (200,206):
                    asset_ready = False
            except (KeyError, ValueError, TypeError):
                asset_ready = False
        if not r.get('media') or not asset_ready:
            reasons.append('Media availability is missing, stale or inaccessible')
        reasons.extend(rules.get(key, []))
        if (r['account'], at) in occupied:
            reasons.append('Account already has a post at this exact time')
        if r['platform'] == 'tiktok' and (r['payload']['target'].get('videoCoverTimestamp') != 0 or r.get('tiktokCoverVerified') is not True):
            reasons.append('TikTok approved frame-zero cover build is not verified')
        try:
            guard({'content_type': 'organic'}, texts=[r['title'], r['caption']], sources=r.get('sourcePaths', []))
        except Exception:
            reasons.append('Organic ad guard did not pass')
        if reasons:
            result['held'].append({'id': key, 'reasons': reasons})
        elif len(live) + len(result['create']) >= CAP:
            result['overflow'].append(key)
        else:
            result['create'].append({'id': key, 'scheduledAt': r['scheduledAt'], 'platform': r['platform'], 'account': r['account'], 'title': r['title'], 'payload': r['payload']})
            occupied.add((r['account'], at))
    result['planDigest'] = digest({k: v for k, v in result.items() if k != 'checkedAt'})
    return result


def reconcile(inventory, fetch, create, now, guard, approved_digest, asset_checks=None):
    """Future activation only: lock across all reads, writes and readbacks."""
    with locked(inventory.directory):
        return _reconcile_locked(inventory, fetch, create, now, guard, approved_digest, asset_checks)


def _reconcile_locked(inventory, fetch, create, now, guard, approved_digest, asset_checks):
    """Reconcile only after the public entrypoint has acquired the private lock.

    Before each write re-count every platform entry. Persist uncertain attempts
    before sending, so timeout/crash cannot cause a repeat POST. No automatic HTTP
    retry is allowed. A stale reviewed diff is rejected rather than widened.
    """
    live = fetch()
    plan = plan_topup(inventory, live, now, guard, asset_checks)
    if plan['planDigest'] != approved_digest:
        raise ValueError('Reviewed plan has changed')
    for item in plan['create']:
        latest = fetch()
        if len(latest) >= CAP:
            break
        keys = {identity({k: i['draft'][k] for k in ('accountId', 'content', 'target')}, i['scheduledAt']) for i in latest}
        if item['id'] in keys:
            continue
        inventory.submitted(item['id'], 'uncertain')
        receipt = create({'post': item['payload'], 'scheduledTime': item['scheduledAt']})
        # Receipt alone does not verify saved date/media. Re-read exact schedule.
        latest = fetch()
        keys = {identity({k: i['draft'][k] for k in ('accountId', 'content', 'target')}, i['scheduledAt']) for i in latest}
        if item['id'] not in keys:
            raise ValueError('Created schedule could not be verified; attempt remains uncertain')
        inventory.submitted(item['id'], 'confirmed', receipt)
    return plan
