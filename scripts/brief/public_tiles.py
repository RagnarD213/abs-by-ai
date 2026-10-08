"""Acquire public profile tile evidence, without credentials or write actions."""
import hashlib
import json
import re
from datetime import timedelta
from urllib.parse import urlencode, urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

from master_queue import stamp
from review_queue import public_tile

PROFILES = {'youtube': 'https://www.youtube.com/channel/UC236gjadarHAhEhOMYNGJ9g/shorts',
            'tiktok': 'https://www.tiktok.com/@absbyai',
            'facebook': 'https://www.facebook.com/1294282227094660',
            'instagram': 'https://www.instagram.com/danrosefit/'}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def read_public(url, image=False):
    p = urlparse(url)
    hosts = ('youtube.com','ytimg.com','tiktok.com','tiktokcdn.com','tiktokcdn-us.com',
             'instagram.com','cdninstagram.com','facebook.com','fbcdn.net','blotato.io')
    if (p.scheme != 'https' or p.username or p.password or p.port not in (None,443)
            or not any(p.hostname == h or p.hostname.endswith('.'+h) for h in hosts)):
        raise ValueError('Unsupported public provider')
    with build_opener(NoRedirect()).open(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=12) as r:
        data = r.read(8*1024*1024+1)
        if len(data) > 8*1024*1024:
            raise ValueError('Public response too large')
        if image and not (data.startswith(b'\xff\xd8\xff') or data.startswith(b'\x89PNG\r\n\x1a\n')
                          or (data.startswith(b'RIFF') and data[8:12] == b'WEBP')
                          or (data[4:8] == b'ftyp' and data[8:12] in (b'avif',b'avis'))):
            raise ValueError('Not an observed tile image')
        return data


def extract_tiles(platform, html):
    """Only profile-grid renderer data qualifies. OG/watch thumbnails do not."""
    tiles = []
    def visit(value):
        if isinstance(value, list):
            for v in value: visit(v)
        elif isinstance(value, dict):
            for name in ('reelItemRenderer','videoRenderer','shortsLockupViewModel'):
                r = value.get(name)
                if not isinstance(r, dict): continue
                video = r.get('videoId')
                if not video:
                    video = r.get('onTap',{}).get('innertubeCommand',{}).get('reelWatchEndpoint',{}).get('videoId')
                thumb = r.get('thumbnail',{}).get('thumbnails',[]) or r.get('thumbnail',{}).get('sources',[])
                if video and thumb:
                    tiles.append({'postId':video,'publicPostUrl':'https://www.youtube.com/shorts/'+video,'tileUrl':thumb[-1]['url']})
            for v in value.values(): visit(v)
    if platform == 'youtube':
        match = re.search(r'(?:var\s+)?ytInitialData\s*=\s*',html)
        if match:
            try: visit(json.JSONDecoder().raw_decode(html[match.end():])[0])
            except (ValueError,KeyError): pass
    elif platform == 'tiktok':
        for match in re.finditer(r'<script[^>]+id="(?:SIGI_STATE|__UNIVERSAL_DATA_FOR_REHYDRATION__)"[^>]*>(.*?)</script>',html,re.S):
            try:
                root = json.loads(match.group(1))
                # SIGI profile ItemModule is distinct from a video detail page.
                for key,item in root.get('ItemModule',{}).items():
                    if item.get('author') == 'absbyai' and item.get('video',{}).get('cover'):
                        tiles.append({'postId':key,'publicPostUrl':'https://www.tiktok.com/@absbyai/video/'+key,'tileUrl':item['video']['cover']})
            except ValueError: pass
    return list({t['postId']:t for t in tiles}.values())


def published_posts(api, key, now):
    items, cursor, seen = [], None, set()
    while True:
        query = {'since':(now-timedelta(days=7)).isoformat(),'until':now.isoformat(),'status':'published','limit':100}
        if cursor: query['cursor'] = cursor
        page = api.call('GET','/posts?'+urlencode(query),key,retries=1)
        items.extend(page.get('items',[]))
        cursor = page.get('cursor')
        if not cursor: return items
        if cursor in seen: raise ValueError('Repeated published cursor')
        seen.add(cursor)


def post_id(platform, url):
    if platform == 'youtube':
        match = re.search(r'(?:[?&]v=|/shorts/|youtu.be/)([A-Za-z0-9_-]{11})',url)
    elif platform == 'tiktok': match = re.search(r'/video/(\d+)',url)
    elif platform == 'instagram': match = re.search(r'/(?:p|reel)/([^/?]+)',url)
    else: match = re.search(r'/(?:reel|videos)/(\d+)',url)
    return match.group(1) if match else None


def acquire(records, published, now, directory, private_json, observations=None, reviewed=None):
    profiles, tiles = [], {}
    for platform,url in PROFILES.items():
        result = {'platform':platform,'profileUrl':url,'checkedAt':now.isoformat(),'status':'unverified'}
        try:
            body = read_public(url).decode('utf-8',errors='replace')
            candidates = extract_tiles(platform,body)
            result.update(httpStatus=200,tileCount=len(candidates),reason='Profile grid tiles acquired' if candidates else 'Profile returned a shell/login wall or unsupported grid markup; no observable tile evidence')
            for tile in candidates:
                tiles[(platform,tile['postId'])] = {**tile,'observedAt':now.isoformat(),'profileUrl':url}
        except Exception as exc:
            result.update(httpStatus=getattr(exc,'code',None),tileCount=0,reason='Public profile unavailable; redirects and authentication walls are not bypassed')
        profiles.append(result)
    # Browser acquisition can supply exact grid tile URLs after inspecting the
    # same profile in an existing session. No cookies or credentials are exported.
    for o in observations or []:
        platform = o.get('platform')
        if (o.get('surface') == 'public_profile_tile' and o.get('profileUrl') == PROFILES.get(platform)
                and o.get('observedAt') and 0 <= (now-stamp(o['observedAt'])).total_seconds() <= 86400):
            pid = post_id(platform,o.get('publicPostUrl',''))
            if pid: tiles[(platform,pid)] = o
    for profile in profiles:
        profile['browserTileCount'] = sum(1 for (platform,_),tile in tiles.items() if platform==profile['platform'] and tile.get('surface')=='public_profile_tile')
    released, evidence = [], {}
    for post in published:
        platform, url = post['platform'], post.get('state',{}).get('postUrl')
        if not url: continue
        candidates = [r for r in records if r['platform'] == platform and r['account'] == str((post.get('account') or {}).get('id'))
                      and r['caption'] == post['text'] and abs((stamp(r['scheduledAt'])-stamp(post['postTime'])).total_seconds()) <= 600]
        record = candidates[0] if len(candidates)==1 else None
        row = {'id': record['id'] if record else 'published:'+str(post['id']), 'platform':platform,
               'title':post['text'].split('\n')[0][:220], 'reviewUrl':url,'status':'unverified'}
        tile = tiles.get((platform,post_id(platform,url)))
        data = None
        if tile:
            try:
                data = read_public(tile['tileUrl'],image=True)
                tile['tileSHA256'] = hashlib.sha256(data).hexdigest()
                # Published IDs come from Blotato; never use an external filename.
                name = hashlib.sha256((platform+':'+str(post['id'])).encode()).hexdigest()
                tile_file = directory / ('published-tile-'+name+'.image')
                tile_file.write_bytes(data); tile_file.chmod(0o600)
            except Exception as exc:
                tile['acquisitionError'] = {'httpStatus':getattr(exc,'code',None),'reason':type(exc).__name__}
                data = None
        if not record or record['approval']['status'] != 'approved' or not record.get('approvedCoverSHA256'):
            row['reason'] = ('Public grid tile acquired; ' if data else 'Published URL verified by Blotato; ') + 'no unique approved placement and cover hash available'
        elif not tile:
            row['reason'] = 'Approved placement identified; public profile tile unavailable on this surface'
        else:
            try:
                if data is None: raise ValueError('Tile acquisition unavailable')
                cover_hash = record['approvedCoverSHA256']
                record = {**record,'publicPostUrl':url}
                ev = {**tile,'placementId':record['id'],'publicPostUrl':url,'approvedCoverSHA256':cover_hash,
                      'tileSHA256':hashlib.sha256(data).hexdigest(),'surface':'public_profile_tile'}
                supplied = (reviewed or {}).get(record['id'],{})
                if supplied.get('tileSHA256') == ev['tileSHA256']:
                    # public_tile rechecks identity, timestamp and approved hash.
                    assessed = public_tile(record,supplied,now)
                else:
                    assessed = public_tile(record,ev,now)
                evidence[record['id']] = ev
                tile_file = directory / ('public-tile-'+record['id']+'.image')
                tile_file.write_bytes(data); tile_file.chmod(0o600)
                row.update(assessed)
            except Exception:
                row['reason'] = 'Observed tile image could not be acquired; visual comparison remains unknown'
        released.append(row)
    private_json(directory/'public-profile-checks.json',profiles)
    private_json(directory/'acquired-public-tile-evidence.json',evidence)
    private_json(directory/'public-tile-candidates.json',list(tiles.values()))
    private_json(directory/'public-release-review.json',released)
    return released, profiles
