"""RO-03 round-1 review page (PRE-RENDER-APPROVAL "The review page"): what is locked, your decisions, the first minute,
what I decided, every graphic and clip in order three per row on its real frame with the speech before / during / after,
one shared floating player, the checks, one reply box. Content comes from round1/page_extra.json."""
import json, html, os
W = "/Volumes/Extreme/_edit_work/ro03/round1"
rows = json.load(open(f"{W}/stills.json")); X = json.load(open(f"{W}/page_extra.json"))
E = html.escape
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
KIND = {"clip": "Opening clip", "title": "Title chip (new)", "work": "Set and rest countdown (new)", "flash": "Flash transition", "lt": "Lower third (HyperFrames)"}
FM = "first-minute/DRAFT - RO-03 round 1 - first minute"
def card(r):
    c = r["copy"]; lines = [f"<b>{k}</b>: {E(str(c[k]))}" for k in ("eyebrow", "headline", "detail", "topic", "point") if k in c]
    if r.get("state"): lines.append("<b>shown</b>: " + E(r["state"]))
    lines.append(f"<b>framing</b>: {'far' if r['framing'] == 'F' else 'near'}")
    if r.get("src"): lines.append("<b>source</b>: " + E(", ".join(s.split('/')[-1] for s in r["src"])))
    if r.get("note"): lines.append("<i>" + E(r["note"]) + "</i>")
    if X.get("item_notes", {}).get(r["item"]): lines.append("<span class='ok'>" + X["item_notes"][r["item"]] + "</span>")
    beat = ""
    if r.get("beats"):
        beat = "<details><summary>Beat sheet (what moves, and when)</summary><table>" + "".join(f"<tr><td>{mmss(b['t'])}</td><td>{E(b['word'])}</td><td>{E(b['beat'])}</td></tr>" for b in r["beats"]) + "</table></details>"
    play = ""
    if r.get("moving") and r.get("ctx"):
        if r["ctx"] == "first": play = f"<button onclick=\"play('{FM} - REVIEW 540p.mp4','First minute',{max(0, r['t0'] - 2):.1f})\">Play it moving (first minute, from {mmss(max(0, r['t0'] - 2))})</button>"
        elif not os.path.exists(f"{W}/context/{r['ctx']}-context - REVIEW 540p.mp4") and r["t0"] < X["first_end"]: play = f"<button onclick=\"play('{FM} - REVIEW 540p.mp4','First minute',{max(0, min(r['still_t'], r['t0'] + 30) - 4):.1f})\">Play it moving (first minute, from {mmss(max(0, min(r['still_t'], r['t0'] + 30) - 4))})</button>"
        elif os.path.exists(f"{W}/context/{r['ctx']}-context - REVIEW 540p.mp4"): play = f"<button onclick=\"play('context/{r['ctx']}-context - REVIEW 540p.mp4','{r['id']} in context',0)\">Play it moving, in context</button>"
    return f"""<article id="{r['id']}"><h3>{r['id']} <span class="tag">{KIND.get(r['kind'], r['kind'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(r['t1'])}</span></h3>
<a href="stills/{r['id']}.jpg"><img loading="lazy" src="stills/{r['id']}.jpg"></a>{play}<div class="copy">{'<br>'.join(lines)}</div>{beat}
<details><summary>Speech before / during / after</summary><p class="small"><b>before</b>: {E(r['before'])}<br><b>during</b>: {E(r['during'])}<br><b>after</b>: {E(r['after'])}</p></details></article>"""
li = lambda xs: "".join("<li>" + d + "</li>" for d in xs)
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RO-03 round 1</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1180px;margin:0;padding:28px 24px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}h3{{font-size:17px;margin:0 0 8px}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.tag{{color:#8ed7ff;font-size:14px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.ok{{color:#9be7b5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:200px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
table{{font-size:13px;color:#cfe0f0;border-collapse:collapse}}td{{padding:2px 8px 2px 0;vertical-align:top}}table.map td{{padding:4px 14px 4px 0;font-size:15px}}
#dock{{position:fixed;right:18px;top:18px;width:min(36vw,640px);z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(min-width:1500px){{main{{margin-right:calc(min(36vw,640px) + 40px);max-width:none}}}}@media(max-width:1499px){{#dock{{position:sticky;top:0;width:auto;right:auto}}}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<div id="dock"><div class="small" id="nowp">Player. The first minute is loaded; the buttons on the page load other clips here.</div><video id="pv" controls preload="none" playsinline poster="{FM}.jpg" src="{FM} - REVIEW 540p.mp4"></video></div>
<main><h1>RO-03 / Round 1: the plan, every graphic, the first minute</h1><p>{X['intro']}</p>
<p class="notice"><b>Locked already, reused from RO-02 (same shoot, same day):</b> {X['locked']}</p>
<nav><a href="#decide">Your {len(X['decisions'])} decisions</a><a href="#minute">First minute</a><a href="#map">The whole video on one screen</a><a href="#decided">What I decided</a><a href="#all">All graphics and clips</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(X['decisions'])})</h2><ol>{li(X['decisions'])}</ol></section>
<section id="minute"><h2>The first minute (0:00 to {mmss(X['first_end'])})</h2><p><button onclick="play('{FM} - REVIEW 540p.mp4','First minute',0)">Play the first minute</button></p>
<p class="small"><a href="{FM}.mp4">1080p file</a> · <a href="first-minute/RO-03 round 1 - audio A-B vs Muhammad.mp4">audio A/B: Muhammad's ab wheel mix, then this one</a> · {X['first_note']}</p></section>
<section id="map"><h2>The whole video on one screen ({X['film_len']})</h2><table class="map">{''.join(f"<tr><td>{a}</td><td><b>{E(b)}</b></td><td>{E(c)}</td></tr>" for a, b, c in X['map'])}</table></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{li(X['decided'])}</ul></section>
<section id="all"><h2>All graphics and clips, in order ({len(rows)})</h2><p class="small">Each is a still on its real graded frame at its real time. Everything moves, so each has a play button: it loads that moment into the player. There is no stock and no AI clip in this video.</p><div class="grid">{''.join(card(r) for r in rows)}</div></section>
<section id="checks"><h2>Checks</h2><ul>{li(X['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id,t){{const v=document.getElementById('pv');const go=()=>{{v.currentTime=t||0;v.play();}};if(v.getAttribute('src')!==src){{v.src=src;v.addEventListener('loadedmetadata',go,{{once:true}});v.load();}}else go();document.getElementById('nowp').textContent=id;}}</script></html>"""
open(f"{W}/index.html", "w").write(page); print("page ok;", len(rows), "items;", page.count("—"), "em dashes;", page.count("–"), "en dashes")
