"""List Wikimedia Commons photos of a person with date, size, licence and URL (no key needed).  commons_find.py "Name" [N]"""
import sys, json, urllib.request, urllib.parse, re
UA = {'User-Agent': 'AbsByAI-video-research/1.0 (danroseconsulting@gmail.com)'}
def api(**q):
    q.update(format='json'); u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(q)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
name = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 50
r = api(action='query', generator='search', gsrsearch=f'"{name}" filetype:bitmap', gsrnamespace=6, gsrlimit=n,
        prop='imageinfo', iiprop='url|size|extmetadata', iiurlwidth=1600)
rows = []
for p in (r.get('query', {}).get('pages', {}) or {}).values():
    ii = p['imageinfo'][0]; md = ii.get('extmetadata', {})
    date = re.sub('<[^>]+>', '', md.get('DateTimeOriginal', {}).get('value', '') or md.get('DateTime', {}).get('value', ''))[:10]
    rows.append((date, ii['width'], ii['height'], md.get('LicenseShortName', {}).get('value', ''), p['title'], ii.get('thumburl') or ii['url'],
                 re.sub('<[^>]+>', '', md.get('Artist', {}).get('value', ''))[:40]))
for row in sorted(rows):
    if row[1] >= 1000: print(' | '.join(str(x) for x in row))
