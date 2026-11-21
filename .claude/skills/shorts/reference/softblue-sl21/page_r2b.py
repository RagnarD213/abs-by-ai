#!/usr/bin/env python3
"""SL-21 round 2 review page (phone first): Short 1 with the restaurant excuse guy, and Short 2 twice (beach pair X1 and pair X2,
Dan picks one). Players first, each with a button that jumps to the new clip; then the change list with timestamps, his pick,
what I decided, checks, one reply. The frames page is kept as index-r2-frames.html and round 1 as index-r1.html.
Serve: `_shared/review_server.py 9621 /Users/danielrose/Projects/_edit_work/SL-21/review` (run it again after every rebuild)."""
import html, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
import page_text_r2 as PT
E = html.escape; R = "/Users/danielrose/Projects/_edit_work/SL-21/review"; FF = Bt.lib.FF
OUT = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content"
os.makedirs(f"{R}/media", exist_ok=True)
if os.path.exists(f"{R}/index.html") and "round 2: the two excuse clips" in open(f"{R}/index.html").read():
    shutil.copy(f"{R}/index.html", f"{R}/index-r2-frames.html")
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
CARDS = [("A2", "s1", "Short 1: Restaurants Don't Care About Your Fitness Goals", "The restaurant excuse guy", 1.53, 5.67, None),
         ("D1", "s2x1", "Short 2, pair X1: You Don't Deserve A Vacation Until You're Ripped", "Beach excuse guy, pair X1", 2.85, 5.94, "X1"),
         ("D2", "s2x2", "Short 2, pair X2: You Don't Deserve A Vacation Until You're Ripped", "Beach excuse guy, pair X2", 2.85, 5.94, "X2")]
cards = []
for S, vid, title, clipname, t0, t1, label in CARDS:
    d = Bt.D(S); T = json.load(open(f"{d}/timeline.json")); src = f"{OUT}/{P.NAME[S]}.mp4"; dst = f"{R}/media/{vid}.mp4"
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src): shutil.copyfile(src, dst)
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{(t0 + t1) / 2:.2f}", "-i", dst, "-frames:v", "1", "-vf", "scale=540:-1", "-q:v", "3", f"{R}/media/{vid}.jpg"], check=True)
    pick = f'<button class="pick" data-label="{label}" onclick="pick(this)">Pick {label}</button>' if label else ""
    cards.append(f"""<article id="{vid}"{' data-label="' + label + '"' if label else ''}><h3>{E(title)} <span class="small">{mmss(T['total'])}</span></h3>
<video controls preload="metadata" playsinline poster="media/{vid}.jpg" src="media/{vid}.mp4"></video>
<p><button onclick="jump('{vid}',{max(0, t0 - 1.0):.2f})">Jump to the new clip ({mmss(t0)})</button> {pick}</p>
<div class="copy"><p><b>{E(clipname)}:</b> {mmss(t0)} to {mmss(t1)}.</p><ul>{''.join('<li>' + E(x) + '</li>' for x in PT.NOTES[S])}</ul>
<p class="small">Full size: <code>Short-form video content/{E(P.NAME[S])}.mp4</code> (also in Videos to Review)</p></div></article>""")
sec = lambda i, h, items, tag="ul": f'<section id="{i}"><h2>{h}</h2><{tag}>' + ''.join('<li>' + E(x) + '</li>' for x in items) + f'</{tag}></section>'
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>What To Cut SFL R2</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:20px 16px}}h1{{font-size:30px;margin:0 0 8px}}h2{{font-size:24px}}
p,li{{color:#bdd0e4}}section{{margin:24px 0;padding:18px;background:#101f32;border:1px solid #29425b;border-radius:16px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
article{{min-width:0;background:#081626;padding:12px;border-radius:14px;border:2px solid transparent}}article.on{{border-color:#35c26b;background:#0c2319}}video{{width:100%;aspect-ratio:9/16;border-radius:10px;background:black}}.small{{font-size:14px;color:#9fb7cf}}.copy{{font-size:15px}}
textarea{{width:100%;box-sizing:border-box;min-height:150px;background:#071221;color:white;padding:12px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:9px 13px;font-size:15px;margin:2px 4px 2px 0}}
article.on .pick{{background:#35c26b;color:#04210f;border-color:#35c26b}}a{{color:#8fd0ff}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}video{{max-height:80vh}}}}</style>
<main><h1>What To Cut Shorts, round 2</h1><p>Short 3 is final. Shorts 1 and 2 are the versions you approved with one new clip each: the excuse guy, lips synced to your own recording. Short 2 is here twice so you can pick the beach guy. Each player is the full 1080p file. Nothing is uploaded. <a href="index-r2-frames.html">The frames page</a> · <a href="index-r1.html">Round 1 page</a></p>
<section id="shorts"><div class="grid">{''.join(cards)}</div></section>
{sec("changes", "What changed (" + str(len(PT.CHANGES)) + ")", PT.CHANGES, "ol")}
{sec("calls", "Your calls (" + str(len(PT.CALLS)) + ")", PT.CALLS, "ol")}
{sec("decided", "What I decided (overrule anything)", PT.DECIDED)}
{sec("checks", "Checks", PT.CHECKS)}
<section id="reply"><h2>One reply</h2><textarea id="n" placeholder="Anything to change (optional)" oninput="upd()"></textarea><pre id="r" style="white-space:pre-wrap;background:#071221;border:1px solid #47607b;border-radius:10px;padding:12px"></pre>
<p><button onclick="navigator.clipboard.writeText(document.getElementById('r').textContent)">Copy reply</button></p></section></main>
<script>
function jump(id,t){{const v=document.querySelector('#'+id+' video');v.currentTime=t;v.scrollIntoView({{block:'center'}})}}
function pick(b){{const a=b.closest('article'),was=a.classList.contains('on');
 document.querySelectorAll('article[data-label]').forEach(x=>{{x.classList.remove('on');x.querySelector('.pick').textContent='Pick '+x.dataset.label}});
 if(!was){{a.classList.add('on');b.textContent='Picked '+a.dataset.label}}upd()}}
function upd(){{const a=document.querySelector('article.on');let t=['Short 1 (restaurant excuse guy): ','Short 2 beach guy: '+(a?'pair '+a.dataset.label:'')];
 const n=document.getElementById('n').value.trim();if(n)t.push('Notes: '+n);document.getElementById('r').textContent=t.join('\\n')}}
upd();</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
