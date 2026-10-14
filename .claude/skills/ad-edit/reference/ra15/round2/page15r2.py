#!/usr/bin/env python3
"""RA-15 round 2 review page: the three approved AI clips moving in the ad (3 s either side, V2 voice), the whole ad as it stands
(review copy), stills of what changed, "What I decided", one reply box. python3 page15r2.py [--media]  -> round2/index.html"""
import json, os, subprocess, html, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
B = json.load(open("beats.json")); W = json.load(open("words_aligned.json"))["words"]
R = "round2"; SRC = "draft_9x16.mp4"; TOTAL = B["total"]; by = {c["name"]: c for c in B["cards"]}
for d in ("stills", "context"): os.makedirs(f"{R}/{d}", exist_ok=True)
def say(a, b): return " ".join(w["w"].strip() for w in W if a - 0.05 <= w["t"] < b - 0.05)
def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"
N = json.load(open(f"{R}/page_notes.json"))
FULL = "DRAFT - RA-15 round 2 - whole ad.mp4"; FULL540 = "DRAFT - RA-15 round 2 - whole ad - REVIEW 540p.mp4"
def grab(t, out):
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", SRC, "-frames:v", "1", "-vf", "scale=540:960", out], check=True)
if "--media" in sys.argv:
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", SRC, "-c", "copy", "-movflags", "+faststart", f"{R}/{FULL}"], check=True)
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", SRC, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", f"{R}/{FULL540}"], check=True)
    grab(0.6, f"{R}/stills/full.jpg")
    for it in N["clips"] + N["changed"]:
        a, b = by[it["key"]]["beat"]
        for k, f in enumerate(it.get("at", [0.5])): grab(a + f * (b - a), f"{R}/stills/{it['id']}-{k}.jpg")
        if it in N["clips"]:
            s = max(0, a - 3); d = min(TOTAL, b + 3) - s
            subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "21",
                            "-preset", "fast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{R}/context/{it['id']}-context - REVIEW 540p.mp4"], check=True)
def clip(it):
    a, b = by[it["key"]]["beat"]
    sp = f"<b>Before:</b> {html.escape(say(a - 3, a))}<br><b>During:</b> {html.escape(say(a, b))}<br><b>After:</b> {html.escape(say(b, b + 3))}"
    imgs = "".join(f'<img loading="lazy" src="stills/{it["id"]}-{k}.jpg">' for k in range(len(it.get("at", [0.5]))))
    return f"""<div class="card"><div class="imgs">{imgs}</div><div class="meta"><div class="id">{it['id']} · {html.escape(it['name'])}</div>
<div class="t">{tc(a)} to {tc(b)} ({b - a:.2f} s) · plays over: "{html.escape(say(a, b))}"</div>
<button onclick="play('context/{it['id']}-context - REVIEW 540p.mp4','{it['id']} · {html.escape(it['name'])}')">Play it moving, in context</button>
<div class="copy">{it['body']}</div><details><summary>What he says around it</summary><p>{sp}</p></details></div></div>"""
def changed(it):
    a, b = by[it["key"]]["beat"]
    imgs = "".join(f'<img loading="lazy" src="stills/{it["id"]}-{k}.jpg">' for k in range(len(it.get("at", [0.5]))))
    return f'<div class="card"><div class="imgs">{imgs}</div><div class="meta"><div class="id">{html.escape(it["name"])}</div><div class="t">{tc(a)} to {tc(b)} ({b - a:.2f} s)</div><div class="copy">{it["body"]}</div></div></div>'
did = "".join(f"<li>{d}</li>" for d in N["decided"]); dec = "".join(f"<li><b>{html.escape(d['q'])}</b><br>{d['body']}</li>" for d in N["decisions"])
reply = "\n".join(f"{n + 1}. {d['short']}: " for n, d in enumerate(N["decisions"])) + ("\n" if N["decisions"] else "") + "Fridge: \nRestaurant: \nCardboard nutritionist: \nOther notes: "
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Never Pay Nutritionist R2</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;background:#0b1220;color:#e8eef7;font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 16px 120px}} @media(min-width:1500px){{main{{margin-right:400px}}}}
h1{{font-size:26px;margin:0 0 6px}} h2{{font-size:20px;margin:34px 0 10px;border-bottom:1px solid #24324a;padding-bottom:6px}}
.lock{{color:#9fb3cc;font-size:14px;margin:4px 0}} ol li,ul li{{margin:8px 0}} a{{color:#68c5ff}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}} @media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:#111b2e;border:1px solid #24324a;border-radius:12px;overflow:hidden}} .imgs{{display:flex}} .imgs img{{width:100%;min-width:0;flex:1;display:block}}
.meta{{padding:12px 14px}} .id{{font-weight:700}} .t{{color:#9fb3cc;font-size:14px;margin-bottom:8px}} .copy{{margin:8px 0;font-size:15px}}
button{{background:#1d6fb8;color:#fff;border:0;border-radius:8px;padding:8px 12px;font-size:14px;cursor:pointer}} details{{margin-top:8px;font-size:14px;color:#c6d3e4}}
.top{{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start}} .top video{{width:300px;max-width:100%;border-radius:12px;background:#000}}
#dock{{position:fixed;right:18px;top:18px;width:350px;background:#0f1930;border:1px solid #2b3d5c;border-radius:12px;padding:10px;z-index:5}}
#dock video{{width:100%;border-radius:8px;background:#000}} #dock .lab{{font-size:13px;color:#9fb3cc;margin-bottom:6px}}
@media(max-width:1499px){{#dock{{position:sticky;top:0;right:auto;width:auto;max-width:360px;margin:0 auto}}}}
textarea{{width:100%;height:170px;background:#0f1930;color:#e8eef7;border:1px solid #2b3d5c;border-radius:8px;padding:10px;font:15px/1.4 Menlo,monospace;box-sizing:border-box}}
</style></head><body>
<div id="dock"><div class="lab" id="docklab">Context player: press a "Play it moving, in context" button</div><video id="dv" controls preload="none" playsinline></video></div>
<main>
<h1>Never Pay A Nutritionist Again · AD (RA-15) · round 2</h1>
<div class="lock">{N['intro']}</div><div class="lock"><b>Locked from round 1:</b> {N['locked']}</div>
<h2>Your decisions ({len(N['decisions'])})</h2>{('<ol>' + dec + '</ol>') if N['decisions'] else '<p>' + N['no_questions'] + '</p>'}
<h2>The three AI clips, moving in the ad</h2><div class="grid">{''.join(clip(i) for i in N['clips'])}</div>
<h2>The whole ad as it stands (review copy)</h2>
<div class="top"><video controls preload="none" playsinline poster="stills/full.jpg" src="{FULL540}"></video>
<div><p><a href="{html.escape(FULL)}">Full quality 1080 x 1920 file</a></p><p>{N['full']}</p></div></div>
<h2>What else changed</h2><div class="grid">{''.join(changed(i) for i in N['changed'])}</div>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Your reply</h2><textarea id="rep">{html.escape(reply)}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value);this.textContent='Copied'">Copy</button>
</main><script>
function play(src,lab){{const v=document.getElementById('dv');v.src=encodeURI(src);document.getElementById('docklab').textContent=lab;v.play();}}
</script></body></html>"""
assert chr(0x2014) not in page, "em dash on the page"
open(f"{R}/index.html", "w").write(page); print("page written")
