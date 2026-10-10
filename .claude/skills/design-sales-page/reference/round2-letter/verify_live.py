# Prove the live page (public/start.html) carries Dan's doc word for word. Same fragment check as
# ../../scripts/verify_boards.py, adapted to one plain HTML page instead of canvas boards.
# Usage: python3 verify_live.py <blocks.json of the LATEST doc export> <start.html or URL-saved copy> --allow allow_live.txt [--forbid ...]
#
# Since 2026-10-10 it also proves the video test: both arms are complete, every film file is in public/ (whole, or in
# numbered parts each under GitHub's 100 MB limit), no markup names a film (so a browser can only ask for the arm it
# was given), and the split, the events and the checkout tag are on the page. --public <dir> names the public folder
# when the page is a saved copy somewhere else; --no-files skips the file check for a copy saved from the live URL.
import argparse, html, json, os, re
ap = argparse.ArgumentParser()
ap.add_argument('blocks'); ap.add_argument('page')
ap.add_argument('--allow'); ap.add_argument('--forbid', nargs='*', default=[])
ap.add_argument('--public'); ap.add_argument('--no-files', action='store_true')
a = ap.parse_args()
SKIP = ('[', 'S1 ·', 'S2 ·', 'S3 ·', 'S4 ·', 'S5 ·', 'S6 ·', 'S7 ·', 'S8 ·', 'S9 ·', 'S10 ·', 'S11 ·', 'S12 ·', 'S13 ·',
        'HEADLINE:', 'Draft v', 'Sticky top bar', 'Sticky bottom')
allow = set(l.strip() for l in open(a.allow) if l.strip()) if a.allow else set()
def norm(t):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t)).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', t).strip()
raw = open(a.page, encoding='utf-8').read()
body = raw[raw.index('<body'):]
page = norm(re.sub(r'<style>.*?</style>|<script.*?</script>', ' ', body, flags=re.S).replace('<br>', ' '))
missing = []
for i, b in enumerate(json.load(open(a.blocks))):
    t = norm(b['text'])
    if i == 0 or not t or t.startswith(SKIP) or t.startswith('[[IMG'):
        continue
    t = t.replace('SUBHEADLINE: ', '').replace(' [face crop]', '')
    for frag in [x.strip() for x in re.split(r'(?<=[.?!…:”"])\s+|→', t) if len(x.strip()) > 2]:
        if frag not in page and frag not in allow:
            missing.append((i, frag))
dashes = raw.count('\u2014') + raw.count('\u2013')
forbidden = [f for f in a.forbid if f in raw]
print(f'missing copy: {len(missing)} | dashes: {dashes} | forbidden present: {forbidden}')
for m in missing: print('  MISSING', m)

# ---- The video test: two arms, one film per browser ----
LIMIT = 95 * 1000 * 1000  # bytes per committed file; GitHub refuses 100 MB
bad = []
head = raw[:raw.index('<body')]
m = re.search(r'var VIDEOS = (\{.*?\}\}), B_SHARE = ([\d.]+), STORE = \'([\w-]+)\';', head)
if not m:
    bad.append('the arm picker (VIDEOS, B_SHARE, STORE) is not in <head>')
    videos, share = {}, None
else:
    videos, share = json.loads(m.group(1)), float(m.group(2))
    if sorted(videos) != ['a', 'b']: bad.append(f'arms are {sorted(videos)}, expected a and b')
    if not 0 <= share <= 1: bad.append(f'B_SHARE {share} is outside 0 to 1')
    meaning = 'everyone gets A' if share <= 0 else 'everyone gets B' if share >= 1 else f'{share:.0%} of visitors get B'
    print(f'video test: B_SHARE = {share} ({meaning}), arm stored in localStorage.{m.group(3)}')
pub = a.public or os.path.dirname(os.path.abspath(a.page))
def pieces(url):
    """A film is one whole file, or <name>.part1, .part2, ... joined by server.js."""
    p = os.path.join(pub, url.lstrip('/'))
    if os.path.isfile(p): return [p]
    out, n = [], 1
    while os.path.isfile(f'{p}.part{n}'):
        out.append(f'{p}.part{n}'); n += 1
    return out
for arm, f in sorted(videos.items()):
    for k in ('phone', 'desk', 'poster', 'opening'):
        if not f.get(k): bad.append(f'arm {arm} has no {k}')
    if not (isinstance(f.get('opening'), (int, float)) and f['opening'] > 0): bad.append(f'arm {arm}: opening must be seconds above 0')
    if a.no_files:
        continue
    for k in ('phone', 'desk', 'poster'):
        got = pieces(f.get(k, ''))
        sizes = [os.path.getsize(p) for p in got]
        if not got: bad.append(f'arm {arm} {k}: {f.get(k)} is not in {pub}')
        if any(s > LIMIT for s in sizes): bad.append(f'arm {arm} {k}: a piece is over {LIMIT // 1000000} MB')
        print(f'  arm {arm} {k:6} {f.get(k)}: {len(got)} file(s), ' + ' + '.join(f'{s / 1e6:.1f}' for s in sizes) + ' MB')
if a.no_files: print('  film files: NOT CHECKED (--no-files)')
names = set(re.findall(r'/video/[\w-]+\.mp4', raw))
listed = {f[k] for f in videos.values() for k in ('phone', 'desk') if f.get(k)}
if names != listed: bad.append(f'films named on the page {sorted(names)} are not the arms\' films {sorted(listed)}')
outside = re.sub(r'var VIDEOS = .*?;\n', '', raw, count=1, flags=re.S)
if re.search(r'/video/[\w-]+\.mp4', outside): bad.append('a film is named outside the arm picker')
if re.search(r'<source\b', raw) or re.search(r'<video[^>]*\b(poster|src)=', raw): bad.append('the video tag carries a fixed source or poster')
if 'rel="preload" as="image"' in raw: bad.append('a fixed poster preload is in <head>; it must follow the arm')
NEED = {'the arm on every event': "video_variant: VSL.video", 'the arm registered for later events': "posthog.register({ video_variant: VSL.video",
        'the exposure event': "$feature_flag: 'vsl-video-variant'", 'watch seconds': "ph('vsl_video_watch'",
        'opening done': "ph('vsl_opening_done'", 'the arm on the checkout link': "out.set('vid', VSL.video)",
        'the page variant unchanged': "landing_variant: 'letter-v1'"}
for what, text in NEED.items():
    if text not in raw: bad.append(f'missing: {what}')
print(f'video test problems: {len(bad)}')
for b in bad: print('  PROBLEM', b)
print('PASS' if not (missing or dashes or forbidden or bad) else 'FAIL')
