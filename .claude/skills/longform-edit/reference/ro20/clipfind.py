"""OR search over the clip library catalog (clip_library.py find needs every word): score = distinct query words found in
slug + description + tags. usage: clipfind.py "words ..." [n] [--169]"""
import json, sys, re
C = json.load(open("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/clip-library/catalog.json"))
C = C if isinstance(C, list) else C.get("clips", C)
def run(q, n=6, wide=False):
    qs = [w for w in re.findall(r"[a-z0-9]+", q.lower()) if len(w) > 2]; out = []
    for c in C:
        if c.get("status", "").startswith("reject"): continue
        if wide and c.get("aspect") != "16x9": continue
        hay = " ".join([c.get("slug", ""), c.get("description", ""), " ".join(c.get("tags") or [])]).lower()
        sc = sum(1 for w in qs if re.search(r"\b" + w, hay))
        if sc: out.append((sc, c))
    out.sort(key=lambda x: (-x[0], x[1]["id"]))
    for sc, c in out[:n]:
        u = c.get("used_in") or []
        print(f"  {sc} {c['id']} {c['kind']:5s} {c.get('aspect')} {c.get('duration', 0):.0f}s {c.get('people')} used:{len(u) if isinstance(u, list) else 1} | {c.get('description', '')[:150]}")
if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    for q in a[0].split(";"):
        print("##", q.strip()); run(q, int(a[1]) if len(a) > 1 else 6, "--169" in sys.argv)
