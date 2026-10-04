"""RO-02 round-2 review page (PRE-RENDER-APPROVAL "The review page"): locks, your decisions, the first minute, the AI
opener frames + the opener graphic, what I decided, every graphic and clip in order three per row on its real frame with
the speech before / during / after, one shared floating player, the checks, one reply box."""
import json, html, os
W = "/Volumes/Extreme/_edit_work/ro02/round2"
rows = json.load(open(f"{W}/stills.json")); X = json.load(open(f"{W}/page_extra.json"))
checks = json.load(open(f"{W}/checks/all.json")) if os.path.exists(f"{W}/checks/all.json") else {}
E = html.escape
def mmss(t): return f"{int(t // 60)}:{t % 60:05.2f}"
KIND = {"clip": "Clip", "recap": "Recap card", "fact": "Fact card (HyperFrames)", "title": "Section title", "opener": "The opener graphic", "lt": "Lower third (HyperFrames)",
        "l3": "3A side list (HyperFrames)", "anat": "Anatomy card (new)", "count": "Countdown (new)", "url": "URL chip"}
FM = "first-minute/DRAFT - RO-02 round 2 - first minute"
def card(r):
    c = r["copy"]; lines = []
    for k in ("eyebrow", "topic", "title", "heading", "headline", "point", "detail", "label"):
        if k in c:
            v = c[k]
            if isinstance(v, list): v = v[0] if k in ("eyebrow", "detail") else " / ".join(x[0] if isinstance(x, list) else str(x) for x in v)
            lines.append(f"<b>{k}</b>: {E(str(v))}")
    for k in ("points", "items"):
        if k in c: lines.append(f"<b>{k}</b>: " + " / ".join(E(x) for x in c[k]))
    if "rows" in c: lines.append("<b>rows</b>: " + " / ".join(E(a + ": " + b) for a, b in c["rows"]))
    if r.get("state"): lines.append("<b>shown</b>: " + E(r["state"]))
    if r.get("src"): lines.append("<b>source</b>: " + E(", ".join(s.split('/')[-1] for s in r["src"])))
    if r.get("note"): lines.append("<i>" + E(r["note"]) + "</i>")
    ck = checks.get(r["item"])
    if ck:
        it = ck["items"][0] if ck["items"] else {}; bits = []
        if it.get("min_clear") is not None: bits.append(f"arms and hands clear of the card: {it['min_clear']} px minimum")
        if it.get("min_face_gap") is not None: bits.append(f"face ends {it['min_face_gap']} px above the strip")
        bits.append("PASS" if not ck["failures"] else "FLAGGED: " + "; ".join(ck["failures"]))
        lines.append(f"<span class='ok'>{E(' · '.join(bits))}</span>")
    if X.get("item_notes", {}).get(r["item"]): lines.append("<span class='ok'>" + X["item_notes"][r["item"]] + "</span>")
    beat = ""
    if r.get("beats"):
        beat = "<details><summary>Beat sheet (every move on a word)</summary><table>" + "".join(f"<tr><td>{mmss(b['t'])}</td><td>{E(b['word'])}</td><td>{E(b['beat'])}</td></tr>" for b in r["beats"]) + "</table></details>"
    play = f"<button onclick=\"play('context/{r['item']}-context - REVIEW 540p.mp4','{r['item']} in context')\">Play it moving, in context</button>" if r.get("moving") and os.path.exists(f"{W}/context/{r['item']}-context - REVIEW 540p.mp4") else ""
    t1 = r["t1"] if r["t1"] else r["t0"]
    return f"""<article id="{r['id']}"><h3>{r['id']} <span class="tag">{KIND.get(r['kind'], r['kind'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(t1)}</span></h3>
<a href="stills/{r['id']}.jpg"><img loading="lazy" src="stills/{r['id']}.jpg"></a>{play}<div class="copy">{'<br>'.join(lines)}</div>{beat}
<details><summary>Speech before / during / after</summary><p class="small"><b>before</b>: {E(r['before'])}<br><b>during</b>: {E(r['during'])}<br><b>after</b>: {E(r['after'])}</p></details></article>"""
op = [r for r in rows if r["kind"] == "opener"]; rest = [r for r in rows if r["kind"] != "opener"]
li = lambda xs: "".join("<li>" + d + "</li>" for d in xs)
A = X["ai"]
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RO-02 round 2</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1180px;margin:0;padding:28px 24px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}h3{{font-size:17px;margin:0 0 8px}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}.two{{grid-template-columns:repeat(2,minmax(0,1fr))}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.tag{{color:#8ed7ff;font-size:14px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.ok{{color:#9be7b5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:230px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
table{{font-size:13px;color:#cfe0f0;border-collapse:collapse}}td{{padding:2px 8px 2px 0;vertical-align:top}}
#dock{{position:fixed;right:18px;top:18px;width:min(36vw,640px);z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(min-width:1500px){{main{{margin-right:calc(min(36vw,640px) + 40px);max-width:none}}}}@media(max-width:1499px){{#dock{{position:sticky;top:0;width:auto;right:auto}}}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<div id="dock"><div class="small" id="nowp">Player. The first minute is loaded; the buttons on the page load other clips here.</div><video id="pv" controls preload="none" playsinline poster="{FM}.jpg" src="{FM} - REVIEW 540p.mp4"></video></div>
<main><h1>RO-02 / Round 2: the opener, every graphic and clip, the first minute</h1><p>"The Vacuum: The Best Ab Exercise For Belly Fat", content long-form, {X['film_len']}. Nothing here is a full film yet and no AI motion has been generated.</p>
<p class="notice"><b>Locked from round 1, not up for review:</b> colour A on every shot; the cut ({X['film_len']}, 66 shots); Soft Blue Light graphics; the HyperFrames lower third, fact card and side list templates and their motion (approved on RO-10); the section title and recap card styles; the approved demo of you generating your goal picture; no music; no burned captions; no AbsByAI.com end mark. <b>Applied from your round 1 answers:</b> half the space above your head on both sizes, with the bottom edge of each frame where it was.</p>
<nav><a href="#decide">Your {len(X['decisions'])} decisions</a><a href="#minute">First minute</a><a href="#ai">Opener frames and graphic</a><a href="#decided">What I decided</a><a href="#all">All graphics and clips</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(X['decisions'])})</h2><ol>{li(X['decisions'])}</ol></section>
<section id="minute"><h2>The first minute (0:00 to {mmss(X['first_minute']['end'])})</h2><p><button onclick="play('{FM} - REVIEW 540p.mp4','First minute')">Play the first minute</button></p>
<p class="small"><a href="{FM}.mp4">1080p master</a> · <a href="first-minute/RO-02 round 2 - audio A-B vs Muhammad.mp4">audio A/B: Muhammad's ab wheel mix, then this one</a> · {X['first_minute']['note']}</p></section>
<section id="ai"><h2>The opener: AI frames (decisions 1 and 2) and the graphic (decision 3)</h2><p class="small">START and END frame of each clip. Motion is generated only for frames you approve. Two different men, both clothed, whole body in frame, nobody touching his stomach. Click any picture for full size.</p>
<div class="grid two">
<article><h3>A START <span class="tag">crunches, left panel</span></h3><a href="aiframes/A-start.png"><img loading="lazy" src="aiframes/A-start.jpg"></a></article>
<article><h3>A END</h3><a href="aiframes/A-end.png"><img loading="lazy" src="aiframes/A-end.jpg"></a><div class="copy">{A['A']}</div></article>
<article><h3>B START <span class="tag">sit-ups, right panel</span></h3><a href="aiframes/B-start.png"><img loading="lazy" src="aiframes/B-start.jpg"></a></article>
<article><h3>B END</h3><a href="aiframes/B-end.png"><img loading="lazy" src="aiframes/B-end.jpg"></a><div class="copy">{A['B']}</div></article></div>
<h2>The graphic at three moments</h2><p class="small">{A['graphic']}</p><div class="grid">{''.join(card(r) for r in op)}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{li(X['decided'])}</ul></section>
<section id="all"><h2>All graphics and clips, in order ({len(rest)})</h2><p class="small">Each is a still on its real graded frame at its real time, taken after every part of it has landed. Anything that moves has a "Play it moving, in context" button: it loads that item with 3 seconds of your speech either side into the player.</p><div class="grid">{''.join(card(r) for r in rest)}</div></section>
<section id="checks"><h2>Checks</h2><ul>{li(X['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();}}</script></html>"""
open(f"{W}/index.html", "w").write(page); print("page ok;", len(rows), "items;", page.count("—"), "em dashes")
