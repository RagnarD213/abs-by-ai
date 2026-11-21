#!/usr/bin/env python3
"""RA-07 round 2 review page (PRE-RENDER-APPROVAL "The review page"): header + decisions, the finished first 30 seconds in the one
docked player, the NEW AI frames (I3b, I4a, I4b) with their context rows, the three approved clips moving, "What I decided",
then every graphic and clip in timeline order three per row, each with "Play it moving, in context". One reply box.
Writes round2/index.html. Serve: python3 .claude/skills/_shared/review_server.py 8817 /Volumes/Extreme/_edit_work/ra07/round2
"""
import html, json, os
from urllib.parse import quote
E = html.escape
os.chdir("/Volumes/Extreme/_edit_work/ra07")
PL = json.load(open("beats_r2.json")); CU = json.load(open("round2/cuts.json"))
NOTES = json.load(open("round2/notes_r2.json"))
W = json.load(open("words_aligned.json"))["words"]
CB = {c["name"]: c for c in PL["cards"]}


def speech(a, b):
    return " ".join(w["w"].strip() for w in W if a - 0.02 <= w["t"] < b - 0.02)


def mmss(t): return f"0:{t:04.1f}"


def btn(i, label="Play it moving, in context"):
    c = CU["items"][i]
    return (f'<button class="ctx" data-src="{quote(c["clip"].replace("round2/", ""))}" '
            f'data-poster="{quote(c["clip"].replace("round2/", "").replace(".mp4", ".jpg"))}">{E(label)}</button>')


# ---- new frames
frames = []
for f in NOTES["new_frames"]:
    c = CB[f["id"]]; a, b = c["beat"]
    frames.append(f"""<section class="newpair"><h3>{f['id']} · {E(f['name'])}</h3>
<div class="pair"><figure><a href="frames/{f['id']}-start.jpg" target="_blank"><img src="frames/{f['id']}-start.jpg" alt="{f['id']} start"></a><figcaption>START</figcaption></figure>
<figure><a href="frames/{f['id']}-end.jpg" target="_blank"><img src="frames/{f['id']}-end.jpg" alt="{f['id']} end"></a><figcaption>END</figcaption></figure></div>
<table><tr><th>When it appears</th><td>{mmss(a)} to {mmss(b)} ({b-a:.1f} s)</td></tr>
<tr><th>What you say just before</th><td>"{E(speech(a - 2.6, a))}"</td></tr>
<tr><th>The line it plays under</th><td><b>"{E(speech(a, b))}"</b></td></tr>
<tr><th>What comes right after</th><td>{E(f['after'])}</td></tr>
<tr><th>What you see</th><td>{E(f['see'])}</td></tr>
<tr><th>How it will move</th><td>{E(f['move'])}</td></tr>
<tr><th>Cost</th><td>{E(f['cost'])}</td></tr>
<tr><th>If you say no</th><td>{E(f['no'])}</td></tr></table></section>""")

# ---- the three approved clips moving
moving = []
for m in NOTES["moving"]:
    c = CU["items"][m["id"]]
    moving.append(f"""<section class="card"><h3>{m['id']} · {E(m['name'])}</h3>
<a href="{quote(c['still'].replace('round2/', ''))}" target="_blank"><img loading="lazy" src="{quote(c['still'].replace('round2/', ''))}" alt="{E(m['name'])}"></a>
{btn(m['id'])}
<table><tr><th>On screen</th><td>{mmss(c['a'])} to {mmss(c['b'])}</td></tr><tr><th>Line</th><td><b>"{E(speech(c['a'], c['b']))}"</b></td></tr>
<tr><th>Take used</th><td>{E(m['take'])}</td></tr><tr><th>Checked</th><td>{E(m['checked'])}</td></tr></table></section>""")

# ---- every graphic and clip in order
cards = []
for it in NOTES["items"]:
    c = CU["items"][it["id"]]; a, b = c["a"], c["b"]
    sp = (f'<details><summary>Speech before / during / after</summary><p><b>Before:</b> {E(speech(a - 3, a))}</p>'
          f'<p><b>During:</b> {E(speech(a, b))}</p><p><b>After:</b> {E(speech(b, b + 3))}</p></details>')
    cards.append(f"""<section class="card"><h3>{it['id']} · {E(it['name'])}</h3>
<a href="{quote(c['still'].replace('round2/', ''))}" target="_blank"><img loading="lazy" src="{quote(c['still'].replace('round2/', ''))}" alt="{E(it['name'])}"></a>
{btn(it['id'])}
<table><tr><th>On screen</th><td>{mmss(a)} to {mmss(b)}</td></tr><tr><th>What it is</th><td>{E(it['kind'])}</td></tr>
<tr><th>Status</th><td>{E(it['status'])}</td></tr><tr><th>Copy</th><td>{E(it['copy'])}</td></tr><tr><th>Source</th><td>{E(it['src'])}</td></tr></table>
{sp}</section>""")

D = NOTES["decisions"]
first = CU["first30"]; F30 = os.path.basename(first["file"])
dec = "".join(f"<li><b>{E(d['q'])}</b><br>{E(d['opts'])}</li>" for d in D)
decided = "".join(f"<li>{E(x)}</li>" for x in NOTES["decided"])
locked = "".join(f"<li>{E(x)}</li>" for x in NOTES["locked"])
reply = "\n".join(f"{i+1}. {d['short']}: " for i, d in enumerate(D)) + "\nAnything else to change: "
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fire Your Trainer AD R2</title><style>
:root{{--bg:#0d1420;--panel:#152033;--ink:#eef4fb;--mute:#9db0c7;--line:#27384f;--acc:#68c5ff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:24px 16px 80px}}@media(min-width:1500px){{main{{margin-right:460px}}}}
h1{{font-size:28px;margin:0 0 6px}}h2{{font-size:21px;margin:34px 0 10px;border-top:1px solid var(--line);padding-top:22px}}h3{{font-size:17px;margin:0 0 10px}}
.sub{{color:var(--mute)}}ol,ul{{padding-left:22px}}li{{margin:6px 0}}a{{color:var(--acc)}}
.player{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}
@media(min-width:1500px){{.player{{position:fixed;right:18px;top:18px;width:420px}}}}
video{{width:100%;max-height:72vh;border-radius:10px;background:#000}}
.btns button,.ctx{{display:block;width:100%;text-align:left;background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:6px 0 0;font-size:14px;cursor:pointer}}
.btns button.on,.ctx.on{{border-color:var(--acc);color:var(--acc)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}@media(max-width:1000px){{.grid{{grid-template-columns:1fr}}}}
.card,.newpair{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}.card img{{width:100%;border-radius:8px;display:block}}
.newpair{{margin-bottom:18px}}.pair{{display:flex;gap:10px;max-width:640px}}.pair figure{{margin:0;flex:1}}.pair img{{width:100%;border-radius:8px}}
figcaption{{font-size:12.5px;color:var(--mute);text-align:center}}
table{{border-collapse:collapse;width:100%;font-size:14px;margin-top:10px}}th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:5px 10px 5px 0;width:30%}}td{{padding:5px 0;vertical-align:top}}
tr+tr th,tr+tr td{{border-top:1px solid var(--line)}}details{{font-size:13.5px;color:var(--mute);margin-top:8px}}summary{{cursor:pointer}}
textarea{{width:100%;height:200px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
</style></head><body><main>
<h1>Fire Your Trainer! · ad · round 2</h1>
<p class="sub">RA-07, vertical 9:16 first, {PL['total']:.1f} seconds. This round: the Cheat Code framing, colour and voice on this ad, the fired-trainer clip first, the new frames for the three fixes, your three approved clips moving, every graphic and clip moving in context, and the finished first {first['dur']:.1f} seconds. AI spend so far: {E(NOTES['spend'])} of $10.</p>
<p class="sub"><b>Locked from round 1:</b></p><ul class="sub">{locked}</ul>
<h2>Your decisions ({len(D)})</h2><ol>{dec}</ol>
<h2>The finished first {first['dur']:.1f} seconds</h2>
<div class="player"><video id="v" controls preload="none" poster="stills/first30.jpg" src="{quote(F30.replace('.mp4', ' - REVIEW 540p.mp4'))}"></video>
<div class="btns"><button class="on" data-src="{quote(F30.replace('.mp4', ' - REVIEW 540p.mp4'))}" data-poster="stills/first30.jpg">First {first['dur']:.0f} seconds (540p)</button>
<button data-src="{quote(F30)}" data-poster="stills/first30.jpg">First {first['dur']:.0f} seconds, full 1080x1920</button></div>
<p class="sub" style="font-size:13px">Every "Play it moving, in context" button below loads into this one player.</p></div>
<p>{E(NOTES['first30_note'])}</p>
<h2>New frames: the problem solved (motion only after you approve)</h2>
<p class="sub">{E(NOTES['frames_note'])}</p>
{''.join(frames)}
<h2>Your three approved clips, now moving</h2>
<div class="grid">{''.join(moving)}</div>
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>Every graphic and clip, in order, moving in context</h2>
<p class="sub">Each still is the settled moment on its real frame, with its caption. The button plays it with about 3 seconds of speech either side. Where a neighbour is one of the three new clips, a labelled placeholder (its START frame) stands in for it.</p>
<div class="grid">{''.join(cards)}</div>
<p class="sub">Round 1 page: <a href="http://127.0.0.1:8807/" target="_blank">http://127.0.0.1:8807/</a></p>
<h2>Your reply</h2>
<textarea id="r">{E(reply)}</textarea><br><button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button>
</main><script>
const v=document.getElementById('v');
function play(b){{v.poster=b.dataset.poster;v.src=b.dataset.src;v.play();document.querySelectorAll('.btns button,.ctx').forEach(x=>x.classList.toggle('on',x===b));
if(b.classList.contains('ctx')&&window.innerWidth<1500)v.scrollIntoView({{behavior:'smooth',block:'center'}})}}
document.querySelectorAll('.btns button,.ctx').forEach(b=>b.onclick=()=>play(b));
</script></body></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash on the page"
open("round2/index.html", "w").write(page)
print("round2/index.html", len(page), "bytes")
