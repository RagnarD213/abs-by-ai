"""Hair top for the corner-layout runs of an assemble_r3 build (the main measure scans rows 0-420; in the corner his hair sits
at about 420-455): his placed matte on screen, first row from the top with at least 3 pixels over alpha 0.5, every frame."""
import json, sys, numpy as np
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/worktrees/agitated-pike-89e952/.claude/skills/_shared/greenscreen-bg'); import gsbg as G
B = json.load(open(sys.argv[1])); out = []
for r in B['runs']:
    if r.get('placement') != 'corner': continue
    meta = json.load(open(r['key'] + '.json')); k, ox, oy = r['affine']
    pr = G.Presenter(r['key'], r['src0'] - meta['f0'], r['o1'] - r['o0'], k, ox, oy)
    for q in range(r['o0'], r['o1']):
        F, A = pr.read(); rows = np.where((A > 0.5).sum(1) >= 3)[0]
        out.append((q, int(rows[0]) + pr.rect[1] if len(rows) else None, r['framing']))
    pr.close()
v = [o[1] for o in out if o[1] is not None]
rep = dict(frames=len(out), none=sum(o[1] is None for o in out), min_top=min(v), median=float(np.median(v)), verdict='PASS' if v and min(v) >= 20 and len(v) == len(out) else 'CHECK')
json.dump(dict(rep, frames_list=out), open(sys.argv[2], 'w')); print(rep)
