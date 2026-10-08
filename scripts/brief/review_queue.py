"""Evidence-bound read-only checks for the seven-day release review."""
import re
from datetime import timedelta
from master_queue import CT, stamp, longform_errors


def public_tile(record, evidence, now):
    """Different CDN bytes do not establish a visual mismatch after compression."""
    if not evidence:
        return {'status': 'unverified', 'reason': 'Public profile tile has not been observed'}
    valid = (evidence.get('placementId') == record['id'] and evidence.get('publicPostUrl') == record.get('publicPostUrl')
             and record.get('approvedCoverSHA256') and evidence.get('approvedCoverSHA256') == record['approvedCoverSHA256']
             and evidence.get('surface') == 'public_profile_tile' and evidence.get('observedAt'))
    if not valid:
        return {'status': 'unverified', 'reason': 'Tile evidence does not identify this approved cover and public post'}
    try:
        age = (now - stamp(evidence['observedAt'])).total_seconds()
        if not 0 <= age <= 86400:
            raise ValueError()
    except (ValueError, TypeError):
        return {'status': 'unverified', 'reason': 'Public tile evidence is stale or invalid'}
    if evidence.get('tileSHA256') == record['approvedCoverSHA256']:
        return {'status': 'verified', 'reason': 'Observed public tile bytes equal the approved cover'}
    if (evidence.get('reviewer') and evidence.get('cropNormalized') is True and evidence.get('tileSHA256')
            and evidence.get('assessment') in ('match', 'mismatch')):
        return {'status': 'mismatch' if evidence['assessment'] == 'mismatch' else 'verified', 'reason': evidence.get('reason', 'Recorded visual review')}
    return {'status': 'unverified', 'reason': 'Recompression or grid crop can change bytes; visual review is required'}


def review(records, live, now, checks=None, public_evidence=None):
    checks, public_evidence = checks or {}, public_evidence or {}
    start = now.astimezone(CT).replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)
    rules = longform_errors(records)
    rows = []
    counts = {}
    for item in live:
        key = (str(item['draft']['accountId']), stamp(item['scheduledAt']))
        counts[key] = counts.get(key, 0) + 1

    def url_state(url):
        evidence = checks.get(url)
        if not evidence or not evidence.get('checkedAt'):
            return 'unverified'
        try:
            age = (now - stamp(evidence['checkedAt'])).total_seconds()
            if not 0 <= age <= 12 * 3600:
                return 'unverified'
        except (ValueError, TypeError):
            return 'unverified'
        code = evidence.get('status')
        if code in (200, 206):
            return 'verified'
        # Auth/rate limits do not prove an asset is broken.
        return 'broken' if code in (404, 410) else 'unverified'

    for r in records:
        at = stamp(r['scheduledAt'])
        if not start <= at < end or not r.get('scheduleId'):
            continue
        cover = r.get('cover')
        video = next((u for u in r.get('media', []) if re.search(r'\.(mp4|mov|webm)(?:\?|$)', u, re.I)), None)
        links = [u.rstrip('.,!;') for u in re.findall(r'https://[^\s<>"\)]+', r['caption'])]
        link_states = [url_state(u) for u in links]
        media_states = [url_state(u) for u in r.get('media', [])]
        preflight = {'cover': url_state(cover) if cover else ('unverified' if r['platform'] in ('facebook', 'tiktok') else 'missing'),
                     'description': 'verified' if r['caption'].strip() else 'missing',
                     'links': 'not_applicable' if not links else ('broken' if 'broken' in link_states else 'verified' if all(s == 'verified' for s in link_states) else 'unverified'),
                     'duplicates': 'duplicate' if counts.get((r['account'], at), 0) > 1 else 'verified',
                     'assetMatch': 'broken' if 'broken' in media_states else 'unverified',
                     'cadence': 'mismatch' if any(n.startswith(('Long-form YouTube must','Other platforms must','More than one')) for n in rules.get(r['id'],[])) else 'unverified' if r['id'] in rules or r['kind'] == 'unknown' else 'verified',
                     'crop': 'verified' if r.get('cropVerified') is True else 'unverified'}
        notes = list(rules.get(r['id'], []))
        if r['kind'] == 'unknown':
            notes.append('Content type needs confirmation before cadence can be checked')
        if r['platform'] == 'tiktok':
            target = r['payload']['target']
            if target.get('videoCoverTimestamp') != 0:
                preflight['cover'] = 'missing'
                notes.append('TikTok needs the approved cover in frame zero and timestamp zero')
            elif r.get('tiktokCoverVerified') is not True:
                notes.append('TikTok timestamp is zero; approved frame-zero image and crop still need verification')
        rows.append({'id': r['id'], 'platform': r['platform'], 'account': r['account'], 'scheduledAt': r['scheduledAt'],
                     'title': r['title'][:220], 'caption': r['caption'][:1000], 'coverReviewUrl': cover,
                     'mediaUrl': video, 'reviewUrl': r.get('publicPostUrl') or 'https://my.blotato.com',
                     'preflight': preflight, 'notes': notes[:8]})
    released = [{'id': r['id'], 'platform': r['platform'], 'title': r['title'][:220], 'reviewUrl': r.get('publicPostUrl'),
                 **public_tile(r, public_evidence.get(r['id']), now)}
                for r in records if r.get('publicPostUrl') and now - timedelta(days=7) <= stamp(r['scheduledAt']) < now]
    return {'status': 'partial', 'checkedAt': now.isoformat(), 'windowFrom': start.isoformat(), 'windowTo': end.isoformat(),
            'sourceCoverage': {'blotato': 'ok', 'youtubeStudio': 'error'},
            'coverageNote': 'Native YouTube owner API has not been read by this normalizer. Native schedules remain unknown. Public grid tiles require separate observation.',
            'rows': sorted(rows, key=lambda r: r['scheduledAt']), 'released': released,
            'publicCoverage': {p: 'unverified' for p in ('youtube', 'tiktok', 'facebook', 'instagram')}}
