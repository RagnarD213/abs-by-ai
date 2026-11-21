#!/usr/bin/env python3
"""RA-14 round 1 review page (PRE-RENDER-APPROVAL "The review page": header + decisions, the sample player on top, what I
decided, every graphic and clip in timeline order three per row, one reply box). Writes round1/index.html.
Serve with: python3 .claude/skills/_shared/review_server.py 8814 /Volumes/Extreme/_edit_work/ra14/round1
"""
import html, json, os
B = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
W = json.load(open("words_aligned.json"))["words"]
META = json.load(open("round1/stills/meta.json"))
NOTES = json.load(open("round1/notes_r1.json"))
E = html.escape
mmss = lambda t: f"{int(t//60)}:{t%60:04.1f}"


def speech(a, b):
    w = lambda lo, hi: " ".join(x["w"].strip() for x in W if lo <= x["t"] < hi)
    return w(a - 3.0, a), w(a, b), w(b, b + 3.0)


items = []
for c in B["cards"]:
    items.append(dict(id=c["name"], a=c["beat"][0], b=c["beat"][1], kind="clip or picture (replaces the camera)"))
for o in B["overlays"]:
    items.append(dict(id=o["id"], a=o["t0"], b=o["t1"], kind="graphic over the camera"))
items.sort(key=lambda x: x["a"])
STILLS = {"G1": ["G1"], "P1": ["P1a", "P1a2", "P1b"], "A1": ["A1"], "T1": ["T1a", "T1b"]}
cards = []
for it in items:
    n = NOTES["items"][it["id"]]
    pre, dur, post = speech(it["a"], it["b"])
    imgs = "".join(f'<a href="stills/{s}.jpg" target="_blank"><img loading="lazy" src="stills/{s}.jpg" alt="{s}"></a>' for s in STILLS.get(it["id"], [it["id"]]))
    cards.append(f"""<section class="card"><div class="imgs n{len(STILLS.get(it['id'], [1]))}">{imgs}</div>
<h3>{E(it['id'])} · {E(n['name'])}</h3>
<p class="meta">{mmss(it['a'])} to {mmss(it['b'])} ({it['b']-it['a']:.1f} s) · {E(it['kind'])}</p>
<p><b>On screen:</b> {E(n['copy'])}</p>
<p><b>Source:</b> {E(n['source'])}</p>
<p class="why">{E(n['why'])}</p>
<details><summary>What he says before, during, after</summary><p><i>Before:</i> {E(pre)}</p><p><b>During:</b> {E(dur)}</p><p><i>After:</i> {E(post)}</p></details>
</section>""")
dec = "".join(f"<li><b>{E(d['q'])}</b><br>{E(d['opts'])}</li>" for d in NOTES["decisions"])
decided = "".join(f"<li>{E(x)}</li>" for x in NOTES["decided"])
locked = "".join(f"<li>{E(x)}</li>" for x in NOTES["locked"])
claims = "".join(f"<li>{E(x)}</li>" for x in NOTES["claims"])
reply = "\n".join(f"{i+1}. {d['short']}: " for i, d in enumerate(NOTES["decisions"])) + "\nAnything else to change: "
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cheat Code Six Pack AD R1</title><style>
:root{{--bg:#0d1420;--panel:#152033;--ink:#eef4fb;--mute:#9db0c7;--line:#27384f;--acc:#68c5ff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 16px 80px}}@media(min-width:1500px){{main{{margin-right:460px}}}}
h1{{font-size:28px;margin:0 0 6px}}h2{{font-size:21px;margin:34px 0 10px;border-top:1px solid var(--line);padding-top:22px}}h3{{font-size:17px;margin:12px 0 2px}}
.sub{{color:var(--mute)}}ol,ul{{padding-left:22px}}li{{margin:6px 0}}
.player{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}
@media(min-width:1500px){{.player{{position:fixed;right:18px;top:18px;width:420px}}}}
video{{width:100%;max-height:78vh;border-radius:10px;background:#000}}
.btns button{{background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:6px 6px 0 0;font-size:14px;cursor:pointer}}
.btns button.on{{border-color:var(--acc);color:var(--acc)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}.card p{{margin:6px 0;font-size:14.5px}}
.imgs{{display:flex;gap:6px}}.imgs img{{width:100%;border-radius:8px;display:block}}.imgs a{{flex:1}}
.meta{{color:var(--mute);font-size:13.5px}}.why{{color:var(--mute)}}details{{font-size:14px;color:var(--mute)}}summary{{cursor:pointer;color:var(--acc)}}
textarea{{width:100%;height:210px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
img.wide{{width:100%;border-radius:10px;border:1px solid var(--line)}}
</style></head><body><main>
<h1>The Cheat Code For Six Pack Abs · ad · round 1</h1>
<p class="sub">RA-14, vertical 9:16 first. This round shows the look, the cut I chose and every graphic and clip as a still. Nothing is rendered in full until you have been through these. The ad runs {B['total']:.1f} s ({59-B['total']:.1f} s under the 0:59 limit), no line cut.</p>
<h2>Already locked (reused, not a question)</h2><ul>{locked}</ul>
<h2>Your decisions ({len(NOTES['decisions'])})</h2><ol>{dec}</ol>
<h2>The opening, finished: look and sound</h2>
<div class="player"><video id="v" controls preload="none" poster="stills/sample_poster.jpg" src="{E(NOTES['sample'])}"></video>
<div class="btns"><button class="on" data-src="{E(NOTES['sample'])}">Voice as approved on RA-01</button><button data-src="{E(NOTES['sample_bass'])}">Same, with more bass</button></div>
<p class="sub" style="font-size:13.5px">{E(NOTES['sample_note'])}</p></div>
<p>{E(NOTES['look_note'])}</p>
<a href="look/side_by_side.jpg" target="_blank"><img class="wide" loading="lazy" src="look/side_by_side.jpg" alt="this ad beside the approved RA-01"></a>
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>Spoken claims, kept as filmed (your call if any should come out)</h2><ul>{claims}</ul>
<h2>Every graphic and clip, in order</h2>
<div class="grid">{''.join(cards)}</div>
<h2>Your reply</h2>
<textarea id="r">{E(reply)}</textarea><br><button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button>
</main><script>
document.querySelectorAll('.btns button').forEach(b=>b.onclick=()=>{{const v=document.getElementById('v');const t=v.currentTime;v.src=b.dataset.src;v.currentTime=t;v.play();document.querySelectorAll('.btns button').forEach(x=>x.classList.toggle('on',x===b))}});
</script></body></html>"""
open("round1/index.html", "w").write(page)
assert chr(8212) not in page, "long dash on the page"
print("round1/index.html", len(page), "bytes,", len(cards), "items")
