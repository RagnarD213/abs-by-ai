#!/usr/bin/env python3
"""SL-18 round 1 review page content: per-item context clips (every graphic and clip, 3 s either side) cut from the delivered
540p review copies, then extra.json for page_r1.py. Run after the final delivery; then page_r1.py; then review_server.py."""
import json, os, subprocess, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sl18_deliver", os.path.join(HERE, "deliver.py")); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
E = html.escape; FF = Bt.lib.FF; FPS = Bt.FPS
R = f"{HERE}/r1/review"; os.makedirs(f"{R}/media/ctx", exist_ok=True)
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
NAMES = {"desk": "AI clip: the film's pill-and-water desk clip (frames 0-111 only)", "graph": "Graph: the film's productivity sketch, rebuilt in motion for vertical",
         "curls": "Your real curls by the pool", "money": "Stock: hands counting money", "pool": "AI clip: a fit couple at a resort pool (shown as a wide card so both fit)",
         "app2": "AI screen mock: the lean dating profile", "app3": "AI screen mock: the full Matches list", "date": "AI clip: the film's dinner date, now shown whole and horizontal (round 2)",
         "squats": "Your real bodyweight squats on the lawn", "abwheel": "Your real ab wheel rollouts (the card approved in SL-07)"}
items = []
for S in ("B", "D"):
    d = Bt.D(S); sh = json.load(open(f"{d}/shots.json")); man = json.load(open(f"{d}/hf/manifest.json"))
    base = os.path.basename(Dl.dname(S))[:-4]; rv = f"{Dl.REV}/{base} - REVIEW 540p.mp4"
    T = json.load(open(f"{d}/timeline.json")); W = json.load(open(f"{d}/words.json"))
    ents = [(s["f0"] / FPS, s["f1"] / FPS, s["cover"]["id"], "clip") for s in sh if s["kind"] == "clip"]
    ents += [(m["a"], m["b"], m["id"], "bar") for m in man]
    ents.sort()
    for a, b, cid, kind in ents:
        lo, hi = max(0, a - 3), min(T["total"], b + 3); out = f"media/ctx/{S}_{cid}.mp4"; poster = f"media/ctx/{S}_{cid}.jpg"
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{lo:.3f}", "-i", rv, "-t", f"{hi - lo:.3f}", "-c:v", "libx264", "-crf", "23", "-preset", "veryfast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{R}/{out}"], check=True)
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{(a + b) / 2:.3f}", "-i", rv, "-frames:v", "1", "-q:v", "3", f"{R}/{poster}"], check=True)
        said = " ".join(w["w"] for w in W if a - 0.1 <= w["t"] < b)
        if kind == "bar":
            m = next(x for x in man if x["id"] == cid); title = f"Key point: {' / '.join(p[0] for p in m['parts'])}"
        else: title = NAMES.get(cid, cid)
        items.append(dict(S=S, title=title, a=a, b=b, clip=out, poster=poster, said=said))
SH = {"B": "Short 1 (Adderall)", "D": "Short 2 (dating)"}
cards = "".join(f"""<article><h3>{E(SH[i['S']])} · {mmss(i['a'])} to {mmss(i['b'])}</h3><img loading="lazy" src="{i['poster']}">
<button onclick="play('{i['clip']}',{json.dumps(i['title'])!r})">Play it moving, in context</button><div class="copy"><b>{E(i['title'])}</b><br>Over: “{E(i['said'][:220])}”</div></article>""" for i in items)
coverage = f"""<section id="coverage"><h2>Every graphic and clip, in order</h2><p class="small">Each button plays the item with 3 seconds before and after, in the player above.</p><div class="grid">{cards}</div></section>"""
X = json.load(open(f"{R}/extra.json")) if os.path.exists(f"{R}/extra.json") else {}
X["coverage"] = coverage
json.dump(X, open(f"{R}/extra.json", "w"), indent=1)
print(len(items), "items")
