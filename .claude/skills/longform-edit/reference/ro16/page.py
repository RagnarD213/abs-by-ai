"""Round-1 review page (Codex WV-01 layout: header of locks, what-I-decided list, one lazy player, sections per item, one reply box)."""
import json, html
W = "/Volumes/Extreme/_edit_work/ro16/round1"
rows = json.load(open(f"{W}/stills.json"))
def mmss(t): return f"{int(t//60)}:{t%60:05.2f}"
E = html.escape
KIND = {"ai": "AI clip", "clip": "Clip", "scene": "Full-screen graphic", "title": "Step title", "lt": "Lower third", "l3": "Side card (3A)", "phone": "App demo"}
cards = []
for r in rows:
    c = r["copy"]; lines = []
    for k in ("eyebrow", "topic", "heading", "headline", "point", "detail", "label"):
        if k in c: lines.append(f"<b>{k}</b>: {E(str(c[k]))}")
    for k in ("points", "items"):
        if k in c: lines.append(f"<b>{k}</b>: " + " / ".join(E(x) for x in c[k]))
    if r.get("src"): lines.append("<b>source</b>: " + E(", ".join(s.split('/')[-1] for s in r["src"])))
    if r.get("note"): lines.append("<i>" + E(r["note"]) + "</i>")
    t1 = r["t1"] if r["t1"] else r["t0"]
    cards.append(f"""<article id="{r['id']}"><h3>{r['id']} <span class="tag">{KIND.get(r['kind'], r['kind'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(t1)}</span></h3>
<a href="stills/{r['id']}.jpg"><img loading="lazy" src="stills/{r['id']}.jpg"></a><div class="copy">{'<br>'.join(lines)}</div>
<details><summary>Speech before / during / after</summary><p class="small"><b>before</b>: {E(r['before'])}<br><b>during</b>: {E(r['during'])}<br><b>after</b>: {E(r['after'])}</p></details></article>""")
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RO-16 round 1</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.tag{{color:#8ed7ff;font-size:14px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:190px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:10px 14px;cursor:pointer;font-size:15px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}.pair{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<main><h1>RO-16 / Round 1</h1><p>"If I Had Belly Fat, Here's How I'd Lose It In 90 Days", cut from 9/23 roll C1710. Full film will run about 12:10.</p>
<p class="notice"><b>Already locked, reused as is:</b> studio colour C, wide/tight framing W2/T2 and audio B, all three approved by you on the website video from this same set; Soft Blue Light graphics, the Motivation lower third and the 3A side card; no music (like the approved C1652 video). Nothing here is rendered as a full film yet.</p>
<nav><a href="#decide">Your 3 decisions</a><a href="#minute">First minute</a><a href="#opener">AI opener frames</a><a href="#decided">What I decided</a><a href="#all">All graphics and clips</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions (3)</h2><ol>
<li><b>AI opener.</b> A: heavier AI-you in the bathroom mirror, looking down at his belly, then grabbing a handful of it (the script's own idea, recommended). Or C: no AI clip, open on camera. Approving A lets me generate the motion (about $1 more; $1.50 of the $5 video budget spent so far on frames). A second concept (waking up heavier in bed) was dropped: its frames kept drifting away from your face.</li>
<li><b>The first minute</b> below: approve, or give notes by timestamp. It is final except the labelled placeholder in the first 7 seconds.</li>
<li><b>Step titles.</b> Each of the 8 steps opens on a 2.4 s full-screen card (see Step 1 at 1:08). Keep that, or switch to a lower-third step header so you stay on camera?</li></ol></section>
<section id="minute"><h2>The first minute (0:00 to 1:15)</h2><video controls preload="none" playsinline poster="first-minute/DRAFT - RO-16 round 1 - first minute - REVIEW 540p.jpg" src="first-minute/DRAFT - RO-16 round 1 - first minute - REVIEW 540p.mp4"></video>
<p class="small"><a href="first-minute/DRAFT - RO-16 round 1 - first minute.mp4">1080p master</a> · <a href="first-minute/RO-16 round 1 - audio A-B vs Muhammad.wav">audio A/B vs Muhammad</a> · audio gate PASS (-14.2 LUFS), hair clear of the top edge on every sampled frame (34 px minimum).</p></section>
<section id="opener"><h2>AI opener frames (no motion generated yet)</h2><h3>A: bathroom mirror</h3><div class="pair"><a href="frames/A-start.png"><img src="frames/A-start.jpg"></a><a href="frames/A-end.png"><img src="frames/A-end.jpg"></a></div>
<p class="small">Action, 6 s, locked camera: he stares at his belly in the mirror, then grabs a handful of belly fat, lowers his head and sighs. Runs under "If I woke up 30 pounds fatter tomorrow... within three months." AI-GENERATED label on screen.</p>
</section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>
<li>Takes: last clean take of every line. Three hidden restarts the first transcript missed were caught with a second, stronger transcription and cut (e.g. "Try ours out or use any other AI..." plus a throat clear; "let's say I stole that for a f-"). His corrected "192 to 175" take is used; "I take Zepbound myself" is kept.</li>
<li>Numbers on screen follow what you said, not the script: 175 lb today, 192 to 175.</li>
<li>No drug brand name in any graphic: Step 2 reads "Get A GLP-1 Prescription". You still say Zepbound.</li>
<li>An independent reviewer went through this packet first and did not pass it; everything it found is fixed: the mirror frames were redrawn (the reflection was physically impossible), three side cards that repeated your words became single KEY POINT lower thirds, a wrong-audience injection clip and a same-actor pair were replaced, an AI chef under "this is what I personally do" became a real meal-delivery clip, and two labels were moved or timed with their photos.</li>
<li>Two study cards with citations: SURMOUNT-1 body-composition result (about 1 in 4 pounds lost was lean mass) and Steinberg 2015 daily weighing (about 14 lb vs 1 lb in 6 months). Plus an animated 7-day-average chart.</li>
<li>Your real photos: the 200 lb sunglasses photo (already used in approved ads) and three studio portraits, all labelled "Real picture(s) of me. Not AI-generated."</li>
<li>Your workout footage: ab wheel by the pool and the V4 1-minute ab workout (finished masters). AI-you kettlebell deadlift (labelled) on "lift weights"; I rejected the 2010 archive deadlift (Mike Chang fills half the frame).</li>
<li>Stock: free Pexels plus the clip library; no glucose meters on the injection beat.</li>
<li>Ending: recap card of all 8 steps, then the Week 2 to Month 3 AI transformation clips on "Do all eight of these for 90 days".</li>
<li>The line "I made a whole separate video on this... link in the description" stays; the link goes in when the Zepbound tips video is published.</li></ul></section>
<section id="all"><h2>All graphics and clips, in order</h2><p class="small">Each is a still on its real graded frame at its real time. Checked by me for copy, placement, labels and clearance; shown so you can overrule, not as questions.</p><div class="grid">{''.join(cards)}</div></section>
<section id="reply"><h2>One reply</h2><textarea id="r">1. Opener: A / C
2. First minute: approved / notes:
3. Step titles: full-screen cards / lower-third headers
Other notes (ID or timestamp):</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main></html>"""
open(f"{W}/index.html", "w").write(page); print("page ok", len(rows), "items")
