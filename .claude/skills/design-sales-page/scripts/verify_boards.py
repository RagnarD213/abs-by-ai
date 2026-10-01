# Prove the boards carry Dan's doc word for word, and catch the usual build slips.
# Usage: python3 verify_boards.py <blocks.json> "<boards glob>" [--assets assets.json] [--allow allow.txt] [--forbid "Day 5" ...]
#   blocks.json : parse_doc.py output of the LATEST doc export
#   allow.txt   : one fragment per line that is intentionally not on the page (a heading colon split into an
#                 eyebrow, a removed timeline Dan asked to cut, a button marker lifted out of a bullet)
#   --forbid    : text that must not appear (a removed eyebrow, "Day 5", a rejected photo's blob id)
# Checks: every sentence fragment of every page-copy block is on the boards; no em or en dashes; no striped
# placeholders left; every asset url in assets.json is used; balanced tags; $preview height equals the root height.
import argparse, glob, html, json, re
from html.parser import HTMLParser

ap = argparse.ArgumentParser()
ap.add_argument('blocks'); ap.add_argument('boards')
ap.add_argument('--assets'); ap.add_argument('--allow'); ap.add_argument('--forbid', nargs='*', default=[])
a = ap.parse_args()

SKIP = ('[', 'S1 ·', 'S2 ·', 'S3 ·', 'S4 ·', 'S5 ·', 'S6 ·', 'S7 ·', 'S8 ·', 'S9 ·', 'S10 ·', 'S11 ·', 'S12 ·', 'S13 ·',
        'HEADLINE:', 'Draft v', 'Sticky top bar', 'Sticky bottom')
allow = set(l.strip() for l in open(a.allow)) if a.allow else set()
VOID = {'img', 'br', 'meta', 'link', 'hr', 'input', 'polyline', 'line', 'circle', 'path', 'polygon', 'rect'}

def norm(t):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t)).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', t).strip()

files = sorted(glob.glob(a.boards))
assert files, 'no boards matched'
page, raw, problems = '', '', []
for f in files:
    s = open(f, encoding='utf-8').read(); raw += s
    body = s[s.index('<x-dc>'):s.index('</x-dc>') + 7]
    stack, bad = [], []
    class P(HTMLParser):
        def handle_starttag(self, t, _):
            if t not in VOID: stack.append(t)
        def handle_endtag(self, t):
            if t in VOID: return
            if not stack or stack[-1] != t: bad.append(t)
            else: stack.pop()
    P().feed(body)
    if bad or stack: problems.append(f'{f}: unbalanced tags {bad[:3]} {stack[:3]}')
    root_h = re.search(r'<div style="width: \d+px; height: (\d+)px', s)
    prev_h = re.search(r'"\$preview":\{"width":\d+,"height":(\d+)\}', s)
    if not (root_h and prev_h and root_h.group(1) == prev_h.group(1)):
        problems.append(f'{f}: root height and $preview disagree')
    txt = re.sub(r'<style>.*?</style>|<script.*?</script>|<title>.*?</title>', ' ', s, flags=re.S).replace('<br>', ' ')
    page += ' ' + norm(txt)

missing = []
for i, b in enumerate(json.load(open(a.blocks))):
    t = norm(b['text'])
    if i == 0 or not t or t.startswith(SKIP) or t.startswith('[[IMG'):  # block 0 is the doc's own title
        continue
    t = t.replace('SUBHEADLINE: ', '').replace(' [face crop]', '')
    for frag in [x.strip() for x in re.split(r'(?<=[.?!…:”"])\s+|→', t) if len(x.strip()) > 2]:
        if frag not in page and frag not in allow:
            missing.append((i, frag))

dashes = page.count('\u2014') + page.count('\u2013')
placeholders = raw.count('class="ph')
forbidden = [f for f in a.forbid if f in raw]
unused = []
if a.assets:
    for k, v in json.load(open(a.assets)).items():
        url = v[0] if isinstance(v, list) else v
        if url not in raw: unused.append(k)

print(f'{len(files)} boards | missing copy: {len(missing)} | dashes: {dashes} | placeholders: {placeholders} | '
      f'forbidden present: {forbidden} | assets not placed: {unused}')
for m in missing: print('  MISSING', m)
for p in problems: print('  PROBLEM', p)
ok = not (missing or dashes or forbidden or unused or problems)
print('PASS' if ok else 'FAIL', '(placeholders are allowed only while an image is still coming)')
