#!/usr/bin/env python3
"""RA-15 round 1 review page (PRE-RENDER-APPROVAL.md layout): decisions, first 30 s, what I decided, every graphic
and clip in timeline order with a shared docked context player, one reply box. Writes round1/index.html + media."""
import json, os, subprocess, html, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
B = json.load(open("beats.json")); W = json.load(open("words_aligned.json"))["words"]
R = "round1"; os.makedirs(f"{R}/stills", exist_ok=True); os.makedirs(f"{R}/context", exist_ok=True)
SRC = "draft_9x16.mp4"; TOTAL = B["total"]
by = {c["name"]: c for c in B["cards"]}; lt = {l["id"]: l for l in B["lt"]}
def say(a, b): return " ".join(w["w"].strip() for w in W if a - 0.05 <= w["t"] < b - 0.05)
def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"
NOTES = json.load(open("page_notes.json"))
items = []
for i in NOTES["items"]:
    a, b = (by[i["key"]]["beat"] if i["key"] in by else ([lt[i["key"]]["a"], lt[i["key"]]["b"]] if i["key"] in lt else B["cta"][0]))
    items.append(dict(i, a=a, b=b))
if "--media" in sys.argv:
    for it in items:
        mid = it["a"] + (it.get("at", 0.6)) * (it["b"] - it["a"])
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{mid:.3f}", "-i", SRC, "-frames:v", "1", "-vf", "scale=540:960", f"{R}/stills/{it['id']}.jpg"], check=True)
        s = max(0, it["a"] - 3); d = min(TOTAL, it["b"] + 3) - s
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "23",
                        "-preset", "fast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{R}/context/{it['id']}-context - REVIEW 540p.mp4"], check=True)
    pass
def fig(n, cap): return f'<figure><img loading="lazy" src="stills/{n}.jpg"><figcaption>{cap}</figcaption></figure>'
def idea(i): return f'''<div class="idea"><div class="pair">{fig_f(i['id']+'-start','START')}{fig_f(i['id']+'-end','END')}</div><div><b>{i['id']} · {html.escape(i['name'])}</b><br><span class="t">{html.escape(i['slot'])}</span><p>{html.escape(i['body'])}</p></div></div>'''
def fig_f(n, cap): return f'<figure><img loading="lazy" src="frames/{n}.jpg"><figcaption>{cap}</figcaption></figure>'
def card(it):
    sp = f"<b>Before:</b> {html.escape(say(it['a'] - 3, it['a']))}<br><b>During:</b> {html.escape(say(it['a'], it['b']))}<br><b>After:</b> {html.escape(say(it['b'], it['b'] + 3))}"
    return f"""<div class="card"><img loading="lazy" src="stills/{it['id']}.jpg" alt="{it['id']}">
<div class="meta"><div class="id">{it['id']} · {html.escape(it['name'])}</div><div class="t">{tc(it['a'])} to {tc(it['b'])} ({it['b'] - it['a']:.1f} s)</div>
<div class="copy">{it['copy']}</div><div class="src">{html.escape(it['source'])}</div>
<button onclick="play('context/{it['id']}-context - REVIEW 540p.mp4','{it['id']} · {html.escape(it['name'])}')">Play it moving, in context</button>
<details><summary>What he says</summary><p>{sp}</p></details></div></div>"""
dec = "".join(f"<li><b>{html.escape(d['q'])}</b><br>{d['body']}</li>" for d in NOTES["decisions"])
did = "".join(f"<li>{d}</li>" for d in NOTES["decided"])
reply = "\n".join(f"{n + 1}. {d['short']}: " for n, d in enumerate(NOTES["decisions"])) + "\nOther notes: "
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>RA-15 Never Pay Nutritionist AD R1</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;background:#0b1220;color:#e8eef7;font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 24px 120px}} @media(min-width:1500px){{main{{margin-right:400px}}}}
h1{{font-size:26px;margin:0 0 6px}} h2{{font-size:20px;margin:34px 0 10px;border-bottom:1px solid #24324a;padding-bottom:6px}}
.lock{{color:#9fb3cc;font-size:14px}} ol li,ul li{{margin:8px 0}} a{{color:#68c5ff}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}} @media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:#111b2e;border:1px solid #24324a;border-radius:12px;overflow:hidden}} .card img{{width:100%;display:block}}
.meta{{padding:12px 14px}} .id{{font-weight:700}} .t{{color:#9fb3cc;font-size:14px}} .copy{{margin:8px 0;font-size:15px}} .src{{color:#9fb3cc;font-size:13px;margin-bottom:8px}}
button{{background:#1d6fb8;color:#fff;border:0;border-radius:8px;padding:8px 12px;font-size:14px;cursor:pointer}} details{{margin-top:8px;font-size:14px;color:#c6d3e4}}
.top{{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start}} .top video{{width:300px;border-radius:12px;background:#000}}
#dock{{position:fixed;right:18px;top:18px;width:350px;background:#0f1930;border:1px solid #2b3d5c;border-radius:12px;padding:10px;z-index:5}}
#dock video{{width:100%;border-radius:8px;background:#000}} #dock .lab{{font-size:13px;color:#9fb3cc;margin-bottom:6px}}
@media(max-width:1499px){{#dock{{position:sticky;top:0;right:auto;width:auto;max-width:360px;margin:0 auto}}}}
textarea{{width:100%;height:190px;background:#0f1930;color:#e8eef7;border:1px solid #2b3d5c;border-radius:8px;padding:10px;font:15px/1.4 Menlo,monospace}}
.pair{{display:flex;gap:14px;flex-wrap:wrap}} .pair figure{{margin:0;width:240px}} .idea{{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start;margin:14px 0;padding:12px;background:#111b2e;border:1px solid #24324a;border-radius:12px}} .idea .pair figure{{width:200px}} .aud{{display:flex;gap:20px;flex-wrap:wrap}} .pair img{{width:100%;border-radius:10px}} figcaption{{font-size:13px;color:#9fb3cc}}
</style></head><body>
<div id="dock"><div class="lab" id="docklab">Context player: press a "Play it moving, in context" button</div><video id="dv" controls preload="none" playsinline></video></div>
<main>
<h1>Never Pay A Nutritionist Again · AD (RA-15) · round 1</h1>
<div class="lock">{NOTES['intro']}</div>
<div class="lock"><b>Already locked, reused:</b> {NOTES['locked']}</div>
<h2>Your decisions ({len(NOTES['decisions'])})</h2><ol>{dec}</ol>
<h2>The first 31 seconds, finished</h2>
<div class="top"><video controls preload="none" playsinline poster="stills/first30.jpg" src="DRAFT - RA-15 round 1 - first 31 seconds - REVIEW 540p.mp4"></video>
<div><p><a href="DRAFT - RA-15 round 1 - first 31 seconds.mp4">Full quality 1080 x 1920 file</a></p>
<p>{NOTES['first30']}</p></div></div>
<h2>AI clip ideas, start and end frames ({len(NOTES['ideas'])})</h2>
{''.join(idea(i) for i in NOTES['ideas'])}
<h2>Colour (on this roll, recommended framing)</h2>
<div class="pair">{fig('K-C2_brighter_gold-close','<b>C2 (in the cut):</b> brighter, golden skin, your RA-14 pick re-made for this roll')}{fig('K-C1_approved_level-close','C1: RA-01 brightness level')}{fig('K-C3_brighter_cool-close','C3: brighter, cooler background')}{fig('ref-ra14-approved-close','For comparison: the C2 frame you approved on Cheat Code (RA-14)')}</div>
<div class="pair">{fig('K-C2_brighter_gold-wide','<b>C2</b>, wide shot')}{fig('K-C1_approved_level-wide','C1, wide')}{fig('K-C3_brighter_cool-wide','C3, wide')}{fig('ref-ra14-approved-wide','Cheat Code C2, wide')}</div>
<h2>Shot size (golden colour)</h2>
<div class="pair">{fig('F1-close','F1 close: a little tighter')}{fig('F2-close','<b>F2 close (in the cut):</b> your RA-14 pick')}{fig('F3-close','F3 close: wider still')}</div>
<div class="pair">{fig('F1-wide','F1 wide')}{fig('F2-wide','<b>F2 wide (in the cut)</b>')}{fig('F3-wide','F3 wide')}</div>
<h2>Voice (the same 10 seconds, level matched)</h2>
<div class="aud">{''.join(f'<div><b>{html.escape(n)}</b><br><audio controls preload="none" src="audio/{html.escape(n)}.m4a"></audio></div>' for n in ("V1 - subtle bass lift, recommended","V2 - bass lift as on Cheat Code","V3 - no bass lift"))}</div>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Every graphic and clip, in order</h2><div class="grid">{''.join(card(i) for i in items)}</div>
<h2>Your reply</h2><textarea id="rep">{html.escape(reply)}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value);this.textContent='Copied'">Copy</button>
</main><script>
function play(src,lab){{const v=document.getElementById('dv');v.src=encodeURI(src);document.getElementById('docklab').textContent=lab;v.play();}}
</script></body></html>"""
open(f"{R}/index.html", "w").write(page); print("page written", len(items), "items")
