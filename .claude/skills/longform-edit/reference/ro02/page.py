"""RO-02 round-1 review page (cut + look). Layout per _shared/PRE-RENDER-APPROVAL.md "The review page": header of what is
reused, your decisions, the first minute, what I decided, the look items three per row with one shared floating player,
the cut (take list, listen-only audio, transcript), what is planned for round 2, one reply box."""
import json, html, os
W = "/Volumes/Extreme/_edit_work/ro02"; R = f"{W}/round1"; FPS = 30000/1001
P = json.load(open(f"{W}/edl.json")); S = json.load(open(f"{W}/shots.json")); X = json.load(open(f"{W}/page_extra.json"))
WD = json.load(open(f"{W}/words_out.json")); hair = json.load(open(f"{R}/first-minute/hair.json"))
E = html.escape
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
start = {}; end = {}
for s in S:
    start.setdefault(s["piece"], s["out_f0"]/FPS); end[s["piece"]] = s["out_f1"]/FPS
total = S[-1]["out_f1"]/FPS
keep = {p["id"]: (p["in"], p["out"]) for p in P}; pid_of = {"cta2": "cta"}
txt = {}
for w in WD:
    for pid, (a, b) in keep.items():
        if P[[q["id"] for q in P].index(pid)]["roll"] == w["roll"] and a-0.05 <= w["src0"] <= b+0.05: txt.setdefault(pid, []).append(w["w"]); break
rows = "".join(f"<tr><td>{mmss(start[p['id']])}</td><td>{p['roll']}</td><td>{E(p['text'])}</td><td class='small'>{E(p['why'])}</td></tr>" for p in P)
script = "".join(f"<p class='small'><b>{mmss(start[p['id']])}</b> {E(' '.join(txt.get(p['id'], [])))}</p>" for p in P)
def card(title, tag, img, body="", play=None):
    b = f"<button onclick=\"play('{play[0]}','{E(play[1])}')\">{E(play[2])}</button>" if play else ""
    return f"<article><h3>{E(title)} <span class='tag'>{E(tag)}</span></h3><a href='{img}'><img loading='lazy' src='{img}'></a>{b}<div class='copy'>{body}</div></article>"
look = []
for name, label in (("hook", "Hook, full sun (0:03)"), ("cloud", "Three types, under cloud (4:56)"), ("demo", "The slump, step 1 (7:33)")):
    look.append(card(f"{label}: camera original", "untouched", f"look/{name}-raw-N.jpg"))
    look.append(card(f"{label}: colour A", "recommended", f"look/{name}-A-N.jpg", X["look_notes"]["A"]))
    look.append(card(f"{label}: colour B", "alternative", f"look/{name}-B-N.jpg", X["look_notes"]["B"]))
frm = []
for name, label in (("hook", "Hook"), ("demo", "The slump")):
    frm.append(card(f"{label}: FAR", "x1.45, hair to mid-thigh", f"look/{name}-A-F.jpg"))
    frm.append(card(f"{label}: NEAR", "x1.80, hair to waistband", f"look/{name}-A-N.jpg"))
frm.append(card("Moving sample: colour A", "0:00 to 0:23", "look/hook-A-F.jpg", "Same 23 seconds in each colour. Loads into the player.", ("look/sample-A - REVIEW 540p.mp4", "Colour A, 0:00 to 0:23", "Play colour A")))
frm.append(card("Moving sample: colour B", "0:00 to 0:23", "look/hook-B-F.jpg", "", ("look/sample-B - REVIEW 540p.mp4", "Colour B, 0:00 to 0:23", "Play colour B")))
li = lambda xs: "".join("<li>"+d+"</li>" for d in xs)
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RO-02 round 1</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1180px;margin:0;padding:28px 24px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.tag{{color:#8ed7ff;font-size:14px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:210px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
table{{font-size:14px;color:#cfe0f0;border-collapse:collapse;width:100%}}td{{padding:6px 10px 6px 0;vertical-align:top;border-top:1px solid #1d3248}}
#dock{{position:fixed;right:18px;top:18px;width:min(36vw,640px);z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(min-width:1500px){{main{{margin-right:calc(min(36vw,640px) + 40px);max-width:none}}}}@media(max-width:1499px){{#dock{{position:sticky;top:0;width:auto;right:auto}}}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<div id="dock"><div class="small" id="nowp">Player. The first minute is loaded; the buttons below load other clips here.</div><video id="pv" controls preload="none" playsinline poster="first-minute/DRAFT - RO-02 round 1 - first minute.jpg" src="first-minute/DRAFT - RO-02 round 1 - first minute - REVIEW 540p.mp4"></video></div>
<main><h1>RO-02 / Round 1: the cut and the look</h1><p>"The Vacuum: The Best Ab Exercise For Belly Fat", cut from the 8/14 poolside rolls C1614 to C1629. The cut runs {mmss(total)}. This round locks the cut, the colour, the framing and the sound. No graphics or B-roll are on it yet: those come next round as stills, then the finished first minute, then the full film.</p>
<p class="notice"><b>Reused, not up for review:</b> the poolside colour you approved on the ab wheel video (same day, same spot, same camera); the shared voice chain; Soft Blue Light graphics and the HyperFrames templates (next round); no burned captions, SRT sidecar; no AbsByAI.com end mark.</p>
<nav><a href="#decide">Your {len(X['decisions'])} decisions</a><a href="#minute">First minute</a><a href="#decided">What I decided</a><a href="#look">Colour and framing</a><a href="#cut">The cut</a><a href="#next">Planned for round 2</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(X['decisions'])})</h2><ol>{li(X['decisions'])}</ol></section>
<section id="minute"><h2>The first minute (0:00 to 1:02), cut and look only</h2><p><button onclick="play('first-minute/DRAFT - RO-02 round 1 - first minute - REVIEW 540p.mp4','First minute')">Play the first minute</button></p>
<p class="small"><a href="first-minute/DRAFT - RO-02 round 1 - first minute.mp4">1080p master</a> · <a href="first-minute/RO-02 round 1 - audio A-B vs Muhammad.mp4">audio A/B: Muhammad's ab wheel mix, then this one</a> · {E(X['first_minute_note'])} Hair clearance, measured every quarter second: {hair['hair_min_px']} px minimum, {hair['hair_median_px']} px median.</p></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{li(X['decided'])}</ul></section>
<section id="look"><h2>Colour and framing (decisions 1 and 2)</h2><p class="small">Each still is the real frame at its real time. Click a still for full size.</p><div class="grid">{''.join(look)}</div><h2>Framing</h2><div class="grid">{''.join(frm)}</div></section>
<section id="cut"><h2>The cut</h2><p><a href="cut/RO-02 full cut - listen only (rough mix).mp3">Listen to the whole {mmss(total)} cut (audio only, rough mix)</a>. It is the exact cut below, so you can check the content before any picture is built.</p>
<details open><summary>Every piece, in order: where it is in the film, which roll, what you say, why this take</summary><table>{rows}</table></details>
<details><summary>The full transcript of the cut</summary>{script}</details></section>
<section id="next"><h2>Planned for round 2 (stills first, nothing built yet)</h2><ul>{li(X['planned'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();}}</script></html>"""
open(f"{R}/index.html", "w").write(page); print("page ok;", page.count("—"), "em dashes")
