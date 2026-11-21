"""RO-11 round-1 review page, RO-16 layout (PRE-RENDER-APPROVAL "The review page"): header of locks, your decisions,
first minute on top, what I decided, every graphic and clip in order three per row on its real frame with the speech
before / during / after, one lazy player for the moving context clips, the checks, one reply box."""
import json, html, os
W = "/Volumes/Extreme/_edit_work/ro11/round1"
rows = json.load(open(f"{W}/stills.json"))
checks = json.load(open(f"{W}/checks/all.json")) if os.path.exists(f"{W}/checks/all.json") else {}
fid = json.load(open(f"{W}/first-minute/fidelity.json")) if os.path.exists(f"{W}/first-minute/fidelity.json") else {}
extra = json.load(open(f"{W}/page_extra.json"))
def mmss(t): return f"{int(t // 60)}:{t % 60:05.2f}"
E = html.escape
KIND = {"clip": "Clip", "scene": "Full-screen graphic", "fact": "Fact card (HyperFrames)", "title": "Section title", "ai": "AI opener (placeholder)", "lt": "Lower third (HyperFrames)",
        "l3": "3A side list (HyperFrames)", "cycle": "Cycle diagram (HyperFrames)", "phone": "App demo"}
cards = []
for r in rows:
    c = r["copy"]; lines = []
    for k in ("eyebrow", "topic", "title", "heading", "headline", "point", "detail", "label"):
        if k in c:
            v = c[k]
            if isinstance(v, list): v = " / ".join(x[0] if isinstance(x, list) else str(x) for x in v) if k != "eyebrow" and k != "detail" else v[0]
            lines.append(f"<b>{k}</b>: {E(str(v))}")
    for k in ("points", "items", "boxes"):
        if k in c: lines.append(f"<b>{k}</b>: " + " / ".join(E(x) for x in c[k]))
    if r.get("src"): lines.append("<b>source</b>: " + E(", ".join(s.split('/')[-1] for s in r["src"])))
    if r.get("note"): lines.append("<i>" + E(r["note"]) + "</i>")
    ck = checks.get(r["id"])
    if ck:
        it = ck["items"][0] if ck["items"] else {}
        bits = []
        if it.get("min_clear") is not None: bits.append(f"arms/hands clear of the card: {it['min_clear']} px minimum")
        if it.get("min_face_gap") is not None: bits.append(f"face ends {it['min_face_gap']} px above the strip")
        if it.get("fill"): bits.append("card fill " + ", ".join(str(tuple(f['rgb'])) for f in it['fill'][:1]) + " (spec 10,38,72)")
        bits.append("PASS" if not ck["failures"] else "FAIL: " + "; ".join(ck["failures"]))
        lines.append(f"<span class='ok'>{E(' · '.join(bits))}</span> <a href='checks/{r['id']}/{r['id']}_every10th.jpg'>every 10th frame</a>")
    beat = ""
    if r.get("beats"):
        beat = "<details><summary>Beat sheet (every move on a word)</summary><table>" + "".join(
            f"<tr><td>{mmss(b['t'])}</td><td>{E(b['word'])}</td><td>{E(b['beat'])}</td></tr>" for b in r["beats"]) + "</table></details>"
    play = f"<button onclick=\"play('context/{r['id']}-context - REVIEW 540p.mp4','{r['id']}')\">Play it moving, in context</button>" if r.get("template") else ""
    t1 = r["t1"] if r["t1"] else r["t0"]
    cards.append(f"""<article id="{r['id']}"><h3>{r['id']} <span class="tag">{KIND.get(r['kind'], r['kind'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(t1)}</span></h3>
<a href="stills/{r['id']}.jpg"><img loading="lazy" src="stills/{r['id']}.jpg"></a>{play}<div class="copy">{'<br>'.join(lines)}</div>{beat}
<details><summary>Speech before / during / after</summary><p class="small"><b>before</b>: {E(r['before'])}<br><b>during</b>: {E(r['during'])}<br><b>after</b>: {E(r['after'])}</p></details></article>""")
fm = extra["first_minute"]
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RO-11 round 1</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.tag{{color:#8ed7ff;font-size:14px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.ok{{color:#9be7b5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:190px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
table{{font-size:13px;color:#cfe0f0;border-collapse:collapse}}td{{padding:2px 8px 2px 0;vertical-align:top}}#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b;margin-bottom:16px}}#dock video{{max-height:52vh}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<main><h1>RO-11 / Round 1</h1><p>"When Calories Don't Matter For Fat Loss", cut from 9/23 roll C1705. Full film will run about {extra['film_len']}. Every lower third, fact card, side list and the cycle diagram come from the HyperFrames templates you approved on RO-10.</p>
<p class="notice"><b>Already locked, reused as is:</b> studio colour C, wide/tight framing W2/T2 and audio B (approved on the website video, RO-16 and RO-10, same set; C1705 is framed identically); Soft Blue Light; the four HyperFrames templates and their motion (approved on RO-10: "All the graphics look great. The motion looks great."); the full-screen section title and recap card styles; no music. Nothing here is rendered as a full film yet.</p>
<nav><a href="#decide">Your {len(extra['decisions'])} decisions</a><a href="#minute">First minute</a><a href="#ai">AI opener frames</a><a href="#decided">What I decided</a><a href="#all">All graphics and clips</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(extra['decisions'])})</h2><ol>{''.join('<li>' + d + '</li>' for d in extra['decisions'])}</ol></section>
<section id="minute"><h2>The first minute (0:00 to {mmss(fm['end'])})</h2><video controls preload="none" playsinline poster="first-minute/DRAFT - RO-11 round 1 - first minute.jpg" src="first-minute/DRAFT - RO-11 round 1 - first minute - REVIEW 540p.mp4"></video>
<p class="small"><a href="first-minute/DRAFT - RO-11 round 1 - first minute.mp4">1080p master</a> · <a href="first-minute/RO-11 round 1 - audio A-B vs Muhammad.mp4">audio A/B vs Muhammad</a> · {E(fm['note'])}</p></section>
<section id="ai"><h2>AI opener frames (decision 2)</h2><p class="small">START and END frame of each concept, same man as RO-10's junk-food clip so the two calories videos share a character. Motion is not generated until you pick. About 4.6 s, under your first line; AI-GENERATED chip on screen.</p>
<div class="grid" style="grid-template-columns:repeat(2,minmax(0,1fr))">
<article><h3>A START <span class="tag">the scale</span></h3><a href="aiframes/A-start.png"><img loading="lazy" src="aiframes/A-start.jpg"></a></article>
<article><h3>A END</h3><a href="aiframes/A-end.png"><img loading="lazy" src="aiframes/A-end.jpg"></a><div class="copy"><b>Action:</b> he has eaten clean (chicken and broccoli on the counter), steps on the scale hopeful, sees the number, his face drops and he grabs his belly with both hands. Both frames are the same room and camera, so the model only has to move him. Estimated $0.60 to $1.20 for the motion.</div></article>
<article><h3>B START <span class="tag">awake at 2 AM</span></h3><a href="aiframes/B-start.png"><img loading="lazy" src="aiframes/B-start.jpg"></a></article>
<article><h3>B END</h3><a href="aiframes/B-end.png"><img loading="lazy" src="aiframes/B-end.jpg"></a><div class="copy"><b>Action:</b> wide awake on his phone in the dark, two empty beers on the nightstand; he drops the phone on his chest and rubs his eyes, exhausted. Previews two of the seven factors (sleep, alcohol). Same cost.</div></article>
</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + d + '</li>' for d in extra['decided'])}</ul></section>
<section id="all"><h2>All graphics and clips, in order</h2><p class="small">Each is a still on its real graded frame at its real time, taken after every part of it has landed. HyperFrames graphics have a "Play it moving" button: it loads that graphic with 3 seconds of your speech either side into the one player below.</p>
<div id="dock"><div class="small" id="nowp">Pick a graphic below to play it here.</div><video id="pv" controls preload="none" playsinline></video></div><div class="grid">{''.join(cards)}</div></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + d + '</li>' for d in extra['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(extra['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id+' in context';v.play();document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
open(f"{W}/index.html", "w").write(page); print("page ok", len(rows), "items")
