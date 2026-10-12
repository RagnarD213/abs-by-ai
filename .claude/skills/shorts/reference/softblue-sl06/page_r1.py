#!/usr/bin/env python3
"""SL-06 round 1 review page (PRE-RENDER-APPROVAL layout: decisions, the finished short, AI frames, what I decided, every
title / crop / clip / graphic / key point of all six as stills on real frames, three per row, one reply box).
  page_r1.py   -> round1/index.html      serve: review_server.py 8816 /Volumes/Extreme/_edit_work/sl06/round1"""
import html, json, os
E = html.escape; R = "/Volumes/Extreme/_edit_work/sl06/round1"
import notes_r1 as N
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def card(it, S):
    key = f"{S}.{it['id']}"; extra = N.ITEM.get(key, ""); tag = N.TAG.get(key, "")
    t = f' <span class="tag">{E(tag)}</span>' if tag else ""
    kind = dict(crop="Crop", clip="Clip", graphic="Graphic", bar="Key point", phone="Phone demo")[it["kind"]]
    sp = f'<details><summary>What you are saying</summary><b>before:</b> {E(it["before"] or "(start of the short)")}<br><b>during:</b> {E(it["during"])}<br><b>after:</b> {E(it["after"] or "(end of the short)")}</details>'
    return (f'<article><a href="stills/{it["img"]}.jpg" target="_blank"><img loading="lazy" src="stills/{it["img"]}_sm.jpg"></a>'
            f'<h3>{S}: {kind} · {E(it["id"])}{t}</h3><div class="copy">{mmss(it["a"])} to {mmss(it["b"])}. {E(it["note"])}' + (f"<br>{extra}" if extra else "") + f'{sp}</div></article>')
def extra_card(img, title, text, tag=""):
    t = f' <span class="tag">{E(tag)}</span>' if tag else ""
    return f'<article><a href="stills/{img}.jpg" target="_blank"><img loading="lazy" src="stills/{img}_sm.jpg"></a><h3>{title}{t}</h3><div class="copy">{text}</div></article>'
secs = []
for S in N.ORDER:
    J = json.load(open(f"{R}/items_{S}.json")); cards = [card(it, S) for it in J["items"]] + [extra_card(*x) for x in N.EXTRA.get(S, [])]
    secs.append(f'<section id="s{S}"><h2>Short {S}: {E(" ".join(J["title"][1]))} <span class="len">{J["total"]:.0f} s</span></h2><p>{N.SHORT[S]}</p><div class="grid">{"".join(cards)}</div></section>')
ai = "".join(f'<div class="pair"><div><img loading="lazy" src="ai/{k}_start.jpg"><span>START</span></div><div><img loading="lazy" src="ai/{k}_end.jpg"><span>END</span></div><p>{t}</p></div>' for k, t in N.AI)
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFC R1</title>
<style>:root{{--bg:#050d1c;--panel:#0b1a30;--line:#234a6e;--cy:#68c5ff;--text:#f4faff;--muted:#b4c6d8}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px system-ui,-apple-system,sans-serif;line-height:1.55}}main{{max-width:1500px;margin:auto;padding:28px 16px}}
h1{{font-size:36px;margin:0 0 6px}}h2{{font-size:25px;margin-top:0}}h3{{font-size:17px;margin:10px 0 4px}}p,li{{color:var(--muted)}}li b,p b{{color:var(--text)}}
section{{margin:26px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:16px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}
article{{min-width:0;background:#07142a;padding:12px;border-radius:12px}}img{{width:100%;border-radius:10px;background:#000;display:block}}
a{{color:#9bd6ff}}.tag{{color:#fff;background:#1f6fb0;font-size:12px;font-weight:700;padding:2px 8px;border-radius:9px}}.len{{font-size:15px;color:var(--muted);font-weight:400}}
.copy{{font-size:14px;color:#dfe9f2}}.notice{{border-left:4px solid var(--cy);padding:10px 16px;background:#0e2440}}
details{{margin-top:6px;font-size:13px;color:#b4c6d8}}summary{{cursor:pointer;color:#9bd6ff}}
.first{{display:grid;grid-template-columns:minmax(260px,400px) 1fr;gap:26px;align-items:start}}video{{width:100%;border-radius:12px;background:#000}}
.pairs{{display:grid;grid-template-columns:1fr 1fr;gap:26px}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.pair p{{grid-column:1/3;margin:4px 0;font-size:14px;color:#dfe9f2}}.pair div{{position:relative}}.pair span{{position:absolute;left:8px;top:8px;background:#000a;padding:2px 8px;border-radius:8px;font-size:12px;font-weight:700}}
textarea{{width:100%;box-sizing:border-box;min-height:460px;background:#030915;color:#fff;padding:14px;font:15px ui-monospace,monospace;border:1px solid #2c5d8a;border-radius:10px}}
button{{background:#1f6fb0;color:#fff;border:0;border-radius:9px;padding:10px 16px;cursor:pointer;font-size:15px}}nav{{display:flex;gap:14px;flex-wrap:wrap;font-size:15px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}.first,.pairs{{grid-template-columns:1fr}}}}@media(max-width:520px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<main><h1>Top 5 Zepbound Tips shorts / Round 1</h1>
<p>{N.INTRO}</p>
<p class="notice"><b>Already locked and reused:</b> {N.LOCKED}</p>
<nav><a href="#decide">Your decisions ({len(N.DECISIONS)})</a><a href="#first">Short D finished</a><a href="#ai">AI frames</a><a href="#decided">What I decided</a>{"".join(f'<a href="#s{S}">Short {S}</a>' for S in N.ORDER)}<a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(N.DECISIONS)})</h2><ol>{"".join(f"<li>{d}</li>" for d in N.DECISIONS)}</ol></section>
<section id="first"><h2>Short D, finished: Inject On Thursday Evening</h2><div class="first"><div><video controls preload="metadata" playsinline src="{E(N.D_REVIEW)}"></video></div><div>{N.D_TEXT}</div></div></section>
<section id="ai"><h2>New AI clips: start and end frames (no motion made yet)</h2><div class="pairs">{ai}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{"".join(f"<li>{d}</li>" for d in N.DECIDED)}</ul></section>
{"".join(secs)}
<section id="reply"><h2>Reply</h2><textarea id="r">{E(N.REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy</button></p></section>
</main></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
