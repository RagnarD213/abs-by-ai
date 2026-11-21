#!/usr/bin/env python3
"""RA-15 round 3 review page: both finished masters, a short clip around every change, the change list with timestamps, What I decided,
one reply box.  python3 round3/page15r3.py [--media]  -> round3/page/index.html"""
import html, json, os, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
D = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/never pay a nutritionist again - RA-15"
M = {k: f"{D}/never pay a nutritionist again | claude | {k} | RA-15.mp4" for k in ("9x16", "16x9")}
R = "round3/page"; N = json.load(open("round3/page_notes_r3.json"))
def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"
if "--media" in sys.argv:
    for k in M:
        sc = "540:960" if k == "9x16" else "960:540"
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", M[k], "-vf", f"scale={sc}", "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
                        "-movflags", "+faststart", f"{R}/RA-15 R3 {k} - REVIEW 540p.mp4"], check=True)
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", "3.0", "-i", M[k], "-frames:v", "1", "-vf", f"scale={sc}", f"{R}/stills/full_{k}.jpg"], check=True)
    for c in N["changes"]:
        a, b = c["watch"]
        for k in M:
            sc = "540:960" if k == "9x16" else "960:540"
            subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", "-i", M[k], "-vf", f"scale={sc}", "-c:v", "libx264", "-crf", "21",
                            "-preset", "fast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{R}/context/{c['id']}-{k}.mp4"], check=True)
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{c['still']:.2f}", "-i", M["9x16"], "-frames:v", "1", "-vf", "scale=360:640", f"{R}/stills/{c['id']}.jpg"], check=True)
def card(c):
    a, b = c["watch"]
    return f"""<div class="card"><img loading="lazy" src="stills/{c['id']}.jpg"><div class="meta"><div class="id">{html.escape(c['name'])}</div>
<div class="t">At {html.escape(c['at'])} in the new film · watch {tc(a)} to {tc(b)}</div>
<button onclick="play('context/{c['id']}-9x16.mp4','{html.escape(c['name'])} (9:16)')">Play 9:16</button>
<button onclick="play('context/{c['id']}-16x9.mp4','{html.escape(c['name'])} (16:9)')">Play 16:9</button>
<div class="copy"><b>Before:</b> {c['before']}<br><b>Now:</b> {c['now']}</div></div></div>"""
did = "".join(f"<li>{d}</li>" for d in N["decided"]); eye = "".join(f"<li>{d}</li>" for d in N["eye"])
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Never Pay Nutritionist R3</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;background:#0b1220;color:#e8eef7;font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 16px 120px}} @media(min-width:1500px){{main{{margin-right:400px}}}}
h1{{font-size:26px;margin:0 0 6px}} h2{{font-size:20px;margin:34px 0 10px;border-bottom:1px solid #24324a;padding-bottom:6px}}
.lock{{color:#9fb3cc;font-size:14px;margin:4px 0}} ul li{{margin:8px 0}} a{{color:#68c5ff}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}} @media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:#111b2e;border:1px solid #24324a;border-radius:12px;overflow:hidden}} .card img{{width:100%;display:block}}
.meta{{padding:12px 14px}} .id{{font-weight:700}} .t{{color:#9fb3cc;font-size:14px;margin-bottom:8px}} .copy{{margin:8px 0;font-size:15px}}
button{{background:#1d6fb8;color:#fff;border:0;border-radius:8px;padding:8px 12px;font-size:14px;cursor:pointer;margin:2px 4px 2px 0}}
.top{{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start}} .top video{{max-width:100%;border-radius:12px;background:#000}}
#dock{{position:fixed;right:18px;top:18px;width:350px;background:#0f1930;border:1px solid #2b3d5c;border-radius:12px;padding:10px;z-index:5}}
#dock video{{width:100%;border-radius:8px;background:#000}} #dock .lab{{font-size:13px;color:#9fb3cc;margin-bottom:6px}}
@media(max-width:1499px){{#dock{{position:sticky;top:0;right:auto;width:auto;max-width:360px;margin:0 auto}}}}
textarea{{width:100%;height:150px;background:#0f1930;color:#e8eef7;border:1px solid #2b3d5c;border-radius:8px;padding:10px;font:15px/1.4 Menlo,monospace;box-sizing:border-box}}
</style></head><body>
<div id="dock"><div class="lab" id="docklab">Clip player: press a Play button</div><video id="dv" controls preload="none" playsinline></video></div>
<main>
<h1>Never Pay A Nutritionist Again · AD (RA-15) · round 3: the finished film</h1>
<div class="lock">{N['intro']}</div>
<h2>The finished ad, both shapes</h2>
<div class="top"><video style="width:300px" controls preload="none" playsinline poster="stills/full_9x16.jpg" src="RA-15 R3 9x16 - REVIEW 540p.mp4"></video>
<video style="width:560px" controls preload="none" playsinline poster="stills/full_16x9.jpg" src="RA-15 R3 16x9 - REVIEW 540p.mp4"></video></div>
<p>{N['files']}</p>
<h2>What changed since round 2 (timestamps in the new film)</h2><div class="grid">{''.join(card(c) for c in N['changes'])}</div>
<h2>Worth your eye</h2><ul>{eye}</ul>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Your reply</h2><textarea id="rep">{html.escape(N['reply'])}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value);this.textContent='Copied'">Copy</button>
</main><script>
function play(src,lab){{const v=document.getElementById('dv');v.src=encodeURI(src);document.getElementById('docklab').textContent=lab;v.play();}}
</script></body></html>"""
assert chr(0x2014) not in page and chr(0x2013) not in page, "em or en dash on the page"
open(f"{R}/index.html", "w").write(page); print("page written")
