# Prove the live page (public/start.html) carries Dan's doc word for word. Same fragment check as
# ../../scripts/verify_boards.py, adapted to one plain HTML page instead of canvas boards.
# Usage: python3 verify_live.py <blocks.json of the LATEST doc export> <start.html or URL-saved copy> --allow allow_live.txt [--forbid ...]
import argparse, html, json, re
ap = argparse.ArgumentParser()
ap.add_argument('blocks'); ap.add_argument('page')
ap.add_argument('--allow'); ap.add_argument('--forbid', nargs='*', default=[])
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
print('PASS' if not (missing or dashes or forbidden) else 'FAIL')
