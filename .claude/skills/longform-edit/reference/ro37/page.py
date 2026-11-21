"""RO-37 round 1 review page (PRE-RENDER-APPROVAL "The review page"): header of locks, your decisions, the first minute on
top, presentation / colour / voice options, the AI clip frames (named, in context), "What I decided", then every graphic and
clip in timeline order, three per row, each with its still and a "Play it moving, in context" button feeding ONE floating
player. Media start muted; review_server injects the shared silent-checks / owner-handoff helper (VIDEO-RULES 2026-10-28)."""
import json, html, os
W = "/Volumes/Expansion/_edit_work/RO-37/round1"; OUT = f"{W}/review"
R = json.load(open(f"{OUT}/context/items.json")); X = json.load(open(f"{OUT}/page_extra.json"))
WO = json.load(open(f"{W}/words_out.json")); E = html.escape
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
FIX = [("6packabs .com", "SixPackAbs.com"), ("6packabs", "SixPackAbs"), (" .com", ".com"), (" -", "-")]
def clean(t):
    for a, b in FIX: t = t.replace(a, b)
    return t
def speech(a, b): return clean(" ".join(w["w"] for w in WO if a <= w["t0"] < b))
KIND = {"clip": "Real gym B-roll", "ai": "AI clip slot (frames only)", "lt": "Lower third", "l3": "Side list"}
def vid(src, poster=""):
    return f'<video controls muted preload="none" playsinline {f"poster={chr(34)}{poster}{chr(34)}" if poster else ""} src="{src}"></video>'
ai_html = []
for a in X["ai"]:
    it = next((r for r in R if r["id"] == a["id"]), None)
    t0, t1 = (it["t0"], it["t1"]) if it else (0, 0)
    ai_html.append(f"""<div class="pair"><h3>{E(a['name'])} <span class="tag">{a['id']}</span> <span class="small">{mmss(t0)} to {mmss(t1)}</span></h3>
<div class="two"><figure><a href="{a['start']}"><img loading="lazy" src="{a['start']}"></a><figcaption>START</figcaption></figure>
<figure><a href="{a['end']}"><img loading="lazy" src="{a['end']}"></a><figcaption>END</figcaption></figure></div>
<table class="ctx"><tr><td>When it appears</td><td>{mmss(t0)} to {mmss(t1)} ({t1 - t0:.1f} s)</td></tr>
<tr><td>What you say just before</td><td>{E(speech(t0 - 6, t0))}</td></tr>
<tr><td>The line it plays under</td><td><b>{E(speech(t0, t1))}</b></td></tr>
<tr><td>What comes right after</td><td>{E(speech(t1, t1 + 5))}</td></tr>
<tr><td>What you see</td><td>{E(a['action'])}</td></tr>
<tr><td>If you say no</td><td>You stay on camera there.</td></tr>
<tr><td>Checks</td><td>{E(a['checks'])}</td></tr></table>
<button onclick="play('context/{a['id']}-context - REVIEW 540p.mp4','{E(a['name'])} ({a['id']}): where it goes (you on camera until its motion is approved)')">Play the spot in context</button></div>""")
cards = []
for r in R:
    if r["kind"] == "ai": continue
    lines = []
    if r["kind"] == "lt": lines.append(f"<b>{E(r['topic'])}</b> · {E(r['point'])}")
    if r["kind"] == "l3": lines.append(f"<b>{E(r['heading'])}</b>: " + " / ".join(E(p) for p in r["points"]))
    if r["kind"] == "clip": lines.append(f"<b>{E(r['src'].split('@')[0])}</b>" + (f", label “{E(r['chip'])}”" if r.get("chip") else ""))
    if r.get("note"): lines.append("<i>" + E(r["note"]) + "</i>")
    t1 = r["t1"] or r["t0"]
    cards.append(f"""<article><h3>{r['id']} <span class="tag">{KIND.get(r['kind'], r['kind'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(t1)}</span></h3>
<a href="context/{r['id']}.jpg"><img loading="lazy" src="context/{r['id']}.jpg"></a><button onclick="play('context/{r['id']}-context - REVIEW 540p.mp4','{r['id']}')">Play it moving, in context</button>
<div class="copy">{'<br>'.join(lines)}</div>
<details><summary>Speech under it</summary><p class="small">{E(speech(r['t0'] - 3, r['t0']))} <b>{E(speech(r['t0'], t1))}</b> {E(speech(t1, t1 + 3))}</p></details></article>""")
P = X["presentation"]; pres = "<div class='grid'>" + "".join(f"""<article><h3>{E(p['name'])} <span class='small'>{'recommended' if p['rec'] else ''}</span></h3><p class='small'>{E(p['what'])}</p>
<a href="options/presentation/presentation-{p['key']}.jpg"><img loading="lazy" src="options/presentation/presentation-{p['key']}.jpg"></a>
<button onclick="play('options/presentation/presentation-{p['key']} - REVIEW 540p.mp4','Presentation {p['key']}: {E(p['name'])}')">Play 8 s moving</button></article>""" for p in P) + "</div>"
CO = X["colour"]; col = "<div class='grid'>" + "".join(f"""<article><h3>Colour {k}: {E(v['name'])} <span class='small'>{'recommended' if v['rec'] else ''}</span></h3><p class='small'>{E(v['why'])}</p>
<a href="options/colour/colour-{k}-tight.jpg"><img loading="lazy" src="options/colour/colour-{k}-tight.jpg"></a><a href="options/colour/colour-{k}-wide.jpg"><img loading="lazy" src="options/colour/colour-{k}-wide.jpg" style="margin-top:6px"></a>
<button onclick="play('options/colour/colour-{k} - REVIEW 540p.mp4','Colour {k}: {E(v['name'])}')">Play 8 s moving</button></article>""" for k, v in CO.items()) + "</div>"
VO = X["voice"]; voice = "<ul>" + "".join(f"""<li><b>{k}: {E(v['name'])}</b>{' (recommended)' if v['rec'] else ''}. {E(v['why'])}<br><audio controls muted preload="none" src="options/voice/{k}.mp3"></audio></li>""" for k, v in VO.items()) + \
    """<li><b>Reference</b>: 30 s of How To Do Hamstring Curls (approved, same pool, same day).<br><audio controls muted preload="none" src="options/voice/_reference.mp3"></audio></li></ul>"""
fm = X["first_minute"]
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>First Time At The Gym R1</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1240px;margin:0 auto;padding:28px 16px}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:calc(62vw)}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
h1{{font-size:34px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px}}p,li{{color:var(--mute)}}section{{margin:30px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}article,.pair{{min-width:0;background:#081626;padding:14px;border-radius:14px}}.pair{{margin-bottom:18px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}figure{{margin:0}}figcaption{{font-size:13px;color:#9fb7cf}}
img,video{{width:100%;border-radius:10px;background:black}}audio{{width:100%}}a{{color:var(--acc)}}.tag{{color:#8ed7ff;font-size:13px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
table{{font-size:14px;color:#cfe0f0;border-collapse:collapse}}td{{padding:3px 10px 3px 0;vertical-align:top}}table.ctx td:first-child{{color:#8ed7ff;white-space:nowrap}}
textarea{{width:100%;box-sizing:border-box;min-height:220px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px}}#dock video{{max-height:60vh}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}.two{{grid-template-columns:1fr}}h1{{font-size:26px}}}}</style>
<div id="dock"><div class="small" id="nowp">Pick any option, graphic or clip below to play it here, with a few seconds of your speech either side.</div><video id="pv" controls muted preload="none" playsinline></video></div>
<main><h1>I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time <span class="small">LFC, round 1</span></h1>
<p>{X['intro']}</p>
<p class="notice"><b>Already locked, reused as is:</b> {X['locked']}</p>
<nav><a href="#decide">Your {len(X['decisions'])} decisions</a><a href="#minute">First minute</a><a href="#look">Presentation, colour, voice</a><a href="#ai">AI clip frames</a><a href="#decided">What I decided</a><a href="#all">All graphics and clips</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(X['decisions'])})</h2><ol>{''.join('<li>' + d + '</li>' for d in X['decisions'])}</ol></section>
<section id="minute"><h2>The first minute (0:00 to {mmss(fm['end'])})</h2>{vid('first-minute/DRAFT - First Time At The Gym R1 - first minute - REVIEW 540p.mp4', 'first-minute/poster.jpg')}
<p class="small"><a href="first-minute/DRAFT - First Time At The Gym R1 - first minute.mp4">1080p</a> · also in Videos to Review</p><p class="small">{fm['note']}</p></section>
<section id="look"><h2>Presentation, colour and voice</h2><p class="small">{X['look_intro']}</p><h3>How the upright footage sits in a widescreen video</h3>{pres}<h3>Colour</h3>{col}<h3>Voice</h3><p class="small">{X['voice_note']}</p>{voice}</section>
<section id="ai"><h2>AI clip frames ({len(X['ai'])} ideas)</h2><p class="small">{X['ai_intro']}</p>{''.join(ai_html)}</section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + d + '</li>' for d in X['decided'])}</ul></section>
<section id="all"><h2>All graphics and clips, in order ({len(cards)})</h2><p class="small">Each still is the real frame at its real time. Every item plays in place with your voice.</p><div class="grid">{''.join(cards)}</div></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + d + '</li>' for d in X['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
open(f"{OUT}/index.html", "w").write(page); print("page ok", len(cards), "items,", len(ai_html), "AI pairs")
