#!/usr/bin/env python3
"""SL-21 review page (phone first): the three delivered 1080p Shorts on one page, players first, then per-Short notes, what I
decided, your calls, checks and one reply box. Serve with `_shared/review_server.py PORT /Users/danielrose/Projects/_edit_work/SL-21/review`."""
import html, json, os, shutil, subprocess, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
E = html.escape; R = "/Users/danielrose/Projects/_edit_work/SL-21/review"; FF = Bt.lib.FF
OUT = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content"
os.makedirs(f"{R}/media", exist_ok=True)
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
ORDER = [("A", 1), ("D", 2), ("E", 3)]
import page_text as PT
NOTES, DECIDED, CALLS, CHECKS = PT.NOTES, PT.DECIDED, PT.CALLS, PT.CHECKS
cards = []
for S, n in ORDER:
    d = Bt.D(S); T = json.load(open(f"{d}/timeline.json"))
    src = f"{OUT}/{P.NAME[S]}.mp4"; dst = f"{R}/media/short{n}.mp4"
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src): shutil.copyfile(src, dst)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "2.0", "-i", dst, "-frames:v", "1", "-vf", "scale=540:-1", "-q:v", "3", f"{R}/media/short{n}.jpg"], check=True)
    eb, hl = P.TITLE[S]; title = " ".join(hl)
    words = re.sub(r"\{[^}]*\}", "", P.TEXT[S]).replace(" | ", " ")
    cards.append(f"""<article id="s{n}"><h3>Short {n}: {E(title)} <span class="small">{mmss(T['total'])}</span></h3>
<video controls preload="metadata" playsinline poster="media/short{n}.jpg" src="media/short{n}.mp4"></video>
<div class="copy"><ul>{''.join('<li>' + E(x) + '</li>' for x in NOTES[S])}</ul>
<details><summary>Full transcript</summary><p>{E(words)}</p></details>
<p class="small">Full size: <code>Short-form video content/{E(P.NAME[S])}.mp4</code> (also in Videos to Review)</p></div></article>""")
CALLS_HTML = (f'<section id="calls"><h2>Your calls ({len(CALLS)})</h2><ol>' + ''.join('<li>' + E(x) + '</li>' for x in CALLS) + '</ol></section>') if CALLS else ""
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>What To Cut SFL R1</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:20px 16px}}h1{{font-size:30px;margin:0 0 8px}}h2{{font-size:24px}}
p,li{{color:#bdd0e4}}section{{margin:24px 0;padding:18px;background:#101f32;border:1px solid #29425b;border-radius:16px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
article{{min-width:0;background:#081626;padding:12px;border-radius:14px}}video{{width:100%;aspect-ratio:9/16;border-radius:10px;background:black}}.small{{font-size:14px;color:#9fb7cf}}.copy{{font-size:15px}}
textarea{{width:100%;box-sizing:border-box;min-height:180px;background:#071221;color:white;padding:12px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;font-size:15px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}video{{max-height:80vh}}}}</style>
<main><h1>What To Cut Shorts, round 1</h1><p>Your three picks (A, D, E), cut from the approved film. Each player is the full 1080p file. Nothing is uploaded; covers come in the setup step.</p>
<section id="shorts"><div class="grid">{''.join(cards)}</div></section>
{CALLS_HTML}
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in DECIDED)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">Short 1 (restaurants):
Short 2 (vacation):
Short 3 (therapy):
Calls: </textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
