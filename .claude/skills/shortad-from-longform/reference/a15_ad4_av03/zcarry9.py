#!/usr/bin/env python3
"""CARRY A JUDGED WATCH PASS FORWARD ONLY WHERE THE PICTURE DID NOT CHANGE (the kit's carry_verdicts.py rule, for this
build's four files). For every image in the new watch dir: when an image of the same name exists in the previous round's
watch dir, is pixel-near-identical (mean < 1 grey level, worst 16x16 block < 12) and every previous entry for it was
clean or expected, its entries are carried (note prefixed). Everything else goes to rejudge.json for a fresh judge, who
writes findings_part2.json for exactly those images. zcarry9.py --merge joins the two into the findings file.
  python3 zcarry9.py <key: v|vc|s|sc>            python3 zcarry9.py <key> --merge"""
import glob, json, os, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shortad-from-longform/reference/kit9x16")
from carry_verdicts import same
K = dict(v=('watch', 'logs/findings.json', 'review_round4/watch_v', 'review_round4/findings_v.json'),
         vc=('cut/watch', 'cut/logs/findings.json', 'review_round4/watch_vc', 'review_round4/findings_vc.json'),
         s=('watch_sq', 'logs/findings_sq.json', 'review_round4/watch_s', 'review_round4/findings_s.json'),
         sc=('cut_sq/watch_sq', 'cut_sq/logs/findings_sq.json', 'review_round4/watch_sc', 'review_round4/findings_sc.json'))
new, fout, prev, fprev = K[sys.argv[1]]
p1 = fout.replace('.json', '_part1.json'); p2 = fout.replace('.json', '_part2.json'); rj = fout.replace('findings', 'rejudge')
if '--merge' in sys.argv:
    a = json.load(open(p1))['entries']; b = json.load(open(p2))['entries']
    need = set(json.load(open(rj))['images']); got = {os.path.basename(e['image']) for e in b}
    assert need <= got, f'not judged: {sorted(need - got)[:6]}'
    json.dump(dict(entries=a + b), open(fout, 'w'), indent=1); print(fout, len(a), 'carried +', len(b), 'fresh'); sys.exit(0)
old = {}
for e in json.load(open(fprev))['entries']: old.setdefault(os.path.basename(e['image']), []).append(e)
carried, rejudge = [], []
for f in sorted(glob.glob(f'{new}/sheets/*') + glob.glob(f'{new}/strips/*')):
    if not f.lower().endswith(('.jpg', '.png')): continue
    b = os.path.basename(f); sub = os.path.basename(os.path.dirname(f)); pf = os.path.join(prev, sub, b)
    es = old.get(b)
    if es and os.path.exists(pf) and all(e['verdict'] in ('clean', 'expected') for e in es) and same(f, pf, 1.0):
        carried += [dict(e, note='carried: pixel-identical to the judged round 4 image. ' + str(e.get('note', ''))) for e in es]
    else: rejudge.append(b)
json.dump(dict(entries=carried), open(p1, 'w'), indent=1); json.dump(dict(images=rejudge, dir=os.path.abspath(new)), open(rj, 'w'), indent=1)
print(f'{sys.argv[1]}: {len(carried)} entries carried, {len(rejudge)} images to judge fresh -> {rj}')
