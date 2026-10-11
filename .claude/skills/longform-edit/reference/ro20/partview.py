"""Compact view of one resolved plan part: time, id, lower third copy or clip source + note."""
import json, sys, os
for p in sys.argv[1:]:
    R = json.load(open(p))
    for r in R:
        t = f"{int(r['t0']//60)}:{r['t0']%60:04.1f}"
        if r["kind"] == "lt": print(f"{t} {r['id']} [{r['topic']}] {r['point']}  <{r['t1']-r['t0']:.0f}s>")
        else: print(f"{t} {r['id']} CLIP {r['t1']-r['t0']:.1f}s {'+'.join(os.path.basename(s)[:34] for s in r.get('src', ['AI frames']))} | {(r.get('note') or '')[:95]}")
