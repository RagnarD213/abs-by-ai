#!/usr/bin/env python3
"""RA-06 round 3 review page: the full 9:16 film, only what changed since round 1 (each with exact times, a watch range and a
context clip), the three AI clips moving, a short "What I decided" list, one reply box. No claim question.
  python3 round3/page_r3.py [--media]      (run from the work dir) -> round3/index.html"""
import json, os, subprocess, html, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
os.chdir("/Volumes/Extreme/_edit_work/ra06")
B = json.load(open("beats.json")); W = json.load(open("words_aligned.json"))["words"]
R = "round3"; SRC = "draft_9x16.mp4"; TOTAL = B["total"]
by = {c["name"]: c for c in B["cards"]}; lt = {l["id"]: l for l in B["lt"]}
hold = {round(p["beat"][0], 2): p for p in B["punch"]}
def say(a, b): return " ".join(w["w"].strip() for w in W if a - 0.05 <= w["t"] < b - 0.05)
def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"
NOTES = json.load(open(f"{R}/page_notes_r3.json"))
items = []
for it in NOTES["changes"]:
    a, b = it["span"] if "span" in it else by[it["key"]]["beat"]
    items.append(dict(it, a=a, b=b))
if "--media" in sys.argv:
    for it in items:
        mid = it["a"] + it.get("at", 0.5) * (it["b"] - it["a"])
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{mid:.3f}", "-i", SRC, "-frames:v", "1", "-vf", "scale=540:960", f"{R}/stills/{it['id']}.jpg"], check=True)
        s = max(0, it["a"] - 3); d = min(TOTAL, it["b"] + 3) - s
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "23",
                        "-preset", "fast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{R}/context/{it['id']}-context - REVIEW 540p.mp4"], check=True)
    for c in ("I3", "I1", "I4"):
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", f"cards_9x16/{c}.mp4", "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "22", "-preset", "fast",
                        "-movflags", "+faststart", f"{R}/clips/{c} - AI clip alone - 540p.mp4"], check=True)
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", SRC, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-c:a", "aac",
                    "-b:a", "128k", "-movflags", "+faststart", f"{R}/DRAFT - RA-06 round 3 - full ad - REVIEW 540p.mp4"], check=True)
def card(it):
    sp = f"<b>During:</b> {html.escape(say(it['a'], it['b']))}"
    return f"""<div class="card"><img loading="lazy" src="stills/{it['id']}.jpg" alt="{it['id']}">
<div class="meta"><div class="id">{html.escape(it['name'])}</div><div class="t">{tc(it['a'])} to {tc(it['b'])} · watch {tc(max(0, it['a'] - 2))} to {tc(min(TOTAL, it['b'] + 2))}</div>
<div class="copy">{it['copy']}</div>
<button onclick="play('context/{it['id']}-context - REVIEW 540p.mp4','{html.escape(it['name'])}')">Play it moving, in context</button>
<details><summary>What he says</summary><p>{sp}</p></details></div></div>"""
clips = "".join(f"""<div class="card"><video controls preload="metadata" playsinline src="clips/{c} - AI clip alone - 540p.mp4"></video>
<div class="meta"><div class="id">{html.escape(NOTES['clips'][c]['name'])}</div><div class="t">{tc(by[c]['beat'][0])} to {tc(by[c]['beat'][1])}</div>
<div class="copy">{NOTES['clips'][c]['copy']}</div></div></div>""" for c in ("I3", "I1", "I4"))
did = "".join(f"<li>{d}</li>" for d in NOTES["decided"])
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Best Ab Exercise AD R3</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;background:#0b1220;color:#e8eef7;font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 16px 120px}} @media(min-width:1500px){{main{{margin-right:400px}}}}
h1{{font-size:26px;margin:0 0 6px}} h2{{font-size:20px;margin:34px 0 10px;border-bottom:1px solid #24324a;padding-bottom:6px}}
.lock{{color:#9fb3cc;font-size:14px}} ol li,ul li{{margin:8px 0}} a{{color:#68c5ff}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}} @media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:#111b2e;border:1px solid #24324a;border-radius:12px;overflow:hidden}} .card img,.card video{{width:100%;display:block;background:#000}}
.meta{{padding:12px 14px}} .id{{font-weight:700}} .t{{color:#9fb3cc;font-size:14px}} .copy{{margin:8px 0;font-size:15px}}
button{{background:#1d6fb8;color:#fff;border:0;border-radius:8px;padding:8px 12px;font-size:14px;cursor:pointer}} details{{margin-top:8px;font-size:14px;color:#c6d3e4}}
.top{{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start}} .top video{{width:320px;max-width:100%;border-radius:12px;background:#000}}
#dock{{position:fixed;right:18px;top:18px;width:350px;background:#0f1930;border:1px solid #2b3d5c;border-radius:12px;padding:10px;z-index:5}}
#dock video{{width:100%;border-radius:8px;background:#000}} #dock .lab{{font-size:13px;color:#9fb3cc;margin-bottom:6px}}
@media(max-width:1499px){{#dock{{position:sticky;top:0;right:auto;width:auto;max-width:360px;margin:0 auto}}}}
textarea{{width:100%;box-sizing:border-box;height:170px;background:#0f1930;color:#e8eef7;border:1px solid #2b3d5c;border-radius:8px;padding:10px;font:15px/1.4 Menlo,monospace}}
</style></head><body>
<div id="dock"><div class="lab" id="docklab">Context player: press a "Play it moving, in context" button</div><video id="dv" controls preload="none" playsinline></video></div>
<main>
<h1>What's The Best Ab Exercise? · AD (RA-06) · round 3</h1>
<div class="lock">{NOTES['intro']}</div>
<h2>The whole ad ({TOTAL:.1f} s, 9:16)</h2>
<div class="top"><video controls preload="metadata" playsinline src="DRAFT - RA-06 round 3 - full ad - REVIEW 540p.mp4"></video>
<div><p>{NOTES['film']}</p></div></div>
<h2>What changed since round 1 ({len(items)}), in film order</h2>
<div class="grid">{''.join(card(i) for i in items)}</div>
<h2>Close shots: the first frame of each, centre line drawn</h2>
<p class="lock">Measured over every frame of each close: his head sits a median 0.8 to 1.2 % of the frame width off centre (round 1: 2.8 to 4.8 %).</p>
<img src="stills/close_holds.jpg" alt="close holds" style="width:100%;border-radius:10px">
<h2>The three AI clips alone</h2>
<div class="grid">{clips}</div>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Your reply</h2>
<p class="lock">Nothing needs a decision. Approve it, or write what to change (a time from the film is enough).</p>
<textarea id="reply">Approved / changes: </textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy my reply</button></p>
</main>
<script>function play(src,lab){{const v=document.getElementById('dv');v.src=src;document.getElementById('docklab').textContent=lab;v.play();}}</script>
</body></html>"""
open(f"{R}/index.html", "w").write(page); print("page ->", f"{R}/index.html", len(items), "changes")
