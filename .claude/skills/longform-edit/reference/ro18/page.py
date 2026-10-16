"""RO-18 round 1 review page (PRE-RENDER-APPROVAL "The review page", Dan 2026-09-30, 10-02, 10-13): header of locks, your
decisions, the first minute on top, the AI clip frames (each named, with its context), "What I decided", then every graphic and
clip in timeline order, three per row, each with a still on its real frame and a "Play it moving, in context" button feeding ONE
player that floats at the right on a wide screen. One reply box."""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W = "/Volumes/Extreme/_edit_work/RO-18/round1"; OUT = f"{W}/review"
rows = json.load(open(f"{OUT}/stills.json"))
checks = json.load(open(f"{OUT}/checks/all.json")) if os.path.exists(f"{OUT}/checks/all.json") else {}
X = json.load(open(f"{OUT}/page_extra.json"))
WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
E = html.escape
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
FIXES = [("apps by AI", "Abs By AI"), ("cloud plan", "Claude plan"), ("Kelly Blue", "Kelley Blue"), ("Robo Taxis", "robotaxis"), ("WhisperFlow", "Wispr Flow"),
         ("Whisper flow", "Wispr Flow"), ("whisper flow", "Wispr Flow"), ("chat GPT", "ChatGPT"), ("paid cloud", "paid Claude"), ("whisper", "Wispr"), ("absbyai .com", "AbsByAI.com"), (" ,000", ",000"), (" -", "-"), (" %", "%")]
def clean(t):
    for a, b in FIXES: t = t.replace(a, b)
    return t
def speech(a, b): return clean(" ".join(w["w"] for w in WO if a <= w["t0"] < b))
KIND = {"clip": "Clip", "scene": "Full-screen graphic", "fact": "Fact card", "title": "Section card", "ai": "AI clip slot (frames only)",
        "lt": "Lower third", "l3": "Side list (3A)", "phone": "Phone beside you"}
NAMES = {it["id"]: it.get("name") for it in json.load(open(f"{W}/plan_resolved.json"))}

# ---------------- AI frame pairs, each named and placed in context (Dan 2026-10-13: "give me ... the context")
ai_html = []
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
from gate import require_pass                       # framecheck rule (2026-10-14): no AI frames on a page without gate + reviewer PASS
for a in X["ai"]:
    require_pass(f"{W}/aiframes/{a['id']}-start.png", f"{W}/aiframes/{a['id']}-end.png")
    r = next(x for x in rows if x["id"] == a["id"])
    t0, t1 = r["t0"], r["t1"]
    ai_html.append(f"""<div class="pair" id="ai-{a['id']}"><h3>{E(a['name'])} <span class="tag">{a['id']}</span> <span class="small">{mmss(t0)} to {mmss(t1)}</span></h3>
<div class="two"><figure><a href="aiframes/{a['id']}-start.png"><img loading="lazy" src="aiframes/{a['id']}-start.jpg"></a><figcaption>START</figcaption></figure>
<figure><a href="aiframes/{a['id']}-end.png"><img loading="lazy" src="aiframes/{a['id']}-end.jpg"></a><figcaption>END</figcaption></figure></div>
<table class="ctx"><tr><td>When it appears</td><td>{mmss(t0)} to {mmss(t1)} ({t1 - t0:.1f} s)</td></tr>
<tr><td>What you say just before</td><td>{E(speech(t0 - 6, t0))}</td></tr>
<tr><td>The line it plays under</td><td><b>{E(speech(t0, t1))}</b></td></tr>
<tr><td>What comes right after</td><td>{E(speech(t1, t1 + 5))}</td></tr>
<tr><td>What you see</td><td>{E(a['action'])}</td></tr>
<tr><td>If you say no</td><td>{E(a['fallback'])}</td></tr>
<tr><td>Motion</td><td>{E(a['cost'])}</td></tr></table>
<button onclick="play('context/{a['id']}-context - REVIEW 540p.mp4','{E(a['name'])} ({a['id']}): the frames in place, in context')">Play the placeholder in context</button></div>""")

# ---------------- every item, in timeline order
cards = []
for r in rows:
    c = r["copy"]; lines = []
    for k in ("eyebrow", "topic", "heading", "headline", "point", "detail", "label"):
        if k in c:
            v = c[k]
            if isinstance(v, list): v = " / ".join(x[0] if isinstance(x, list) else str(x) for x in v) if k not in ("eyebrow", "detail") else v[0]
            lines.append(f"<b>{k}</b>: {E(str(v))}")
    for k in ("points", "items", "left", "right"):
        if k in c: lines.append(f"<b>{k}</b>: " + " / ".join(E(x) for x in c[k]))
    if r.get("src"): lines.append("<b>source</b>: " + E(", ".join(s.split('/')[-1] for s in r["src"])))
    if r.get("note"): lines.append("<i>" + E(r["note"]) + "</i>")
    ck = checks.get(r["id"])
    if ck:
        it = ck["items"][0] if ck["items"] else {}
        bits = []
        if it.get("min_clear") is not None: bits.append(f"arms clear of the card by {it['min_clear']} px")
        if it.get("min_face_gap") is not None: bits.append(f"face ends {it['min_face_gap']} px above the strip")
        bits.append("checks PASS" if not ck["failures"] else "checks FAIL: " + "; ".join(ck["failures"]))
        lines.append(f"<span class='ok'>{E(' · '.join(bits))}</span>")
    beat = ""
    if r.get("beats"):
        beat = "<details><summary>Beat sheet (what moves on which word)</summary><table>" + "".join(
            f"<tr><td>{mmss(b['t'])}</td><td>{E(clean(b['word']))}</td><td>{E(b['beat'])}</td></tr>" for b in r["beats"]) + "</table></details>"
    nm = NAMES.get(r["id"]); title = f"{E(nm)} <span class='tag'>{r['id']}</span>" if nm else r["id"]
    t1 = r["t1"] if r["t1"] else r["t0"]
    cards.append(f"""<article id="{r['id']}"><h3>{title} <span class="tag">{KIND.get(r['kind'], r['kind'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(t1)}</span></h3>
<a href="stills/{r['id']}.jpg"><img loading="lazy" src="stills/{r['id']}.jpg"></a><button onclick="play('context/{r['id']}-context - REVIEW 540p.mp4','{r['id']}')">Play it moving, in context</button>
<div class="copy">{'<br>'.join(lines)}</div>{beat}
<details><summary>Speech before / during / after</summary><p class="small"><b>before</b>: {E(clean(r['before']))}<br><b>during</b>: {E(clean(r['during']))}<br><b>after</b>: {E(clean(r['after']))}</p></details></article>""")

fm = X["first_minute"]
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Make Time, round 1</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1240px;margin:0 auto;padding:28px 16px}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:calc(62vw)}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px}}p,li{{color:var(--mute)}}section{{margin:30px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}article,.pair{{min-width:0;background:#081626;padding:14px;border-radius:14px}}.pair{{margin-bottom:18px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}figure{{margin:0}}figcaption{{font-size:13px;color:#9fb7cf}}
img,video{{width:100%;border-radius:10px;background:black}}a{{color:var(--acc)}}.tag{{color:#8ed7ff;font-size:13px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.ok{{color:#9be7b5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
table{{font-size:14px;color:#cfe0f0;border-collapse:collapse}}td{{padding:3px 10px 3px 0;vertical-align:top}}table.ctx td:first-child{{color:#8ed7ff;white-space:nowrap}}
textarea{{width:100%;box-sizing:border-box;min-height:220px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px}}#dock video{{max-height:60vh}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}.two{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<div id="dock"><div class="small" id="nowp">Pick any graphic or clip below to play it here, with 3 seconds of your speech either side.</div><video id="pv" controls preload="none" playsinline></video></div>
<main><h1>How To Make Time For Exercise &amp; Nutrition <span class="small">LFC, round 1</span></h1>
<p>Cut from 9/23 rolls C1714 and C1715. The film will run {X['film_len']}. This round is the first minute, the AI clip frames and every graphic and clip in place. No full film until you have picked.</p>
<p class="notice"><b>Already locked, reused as is:</b> {X['locked']}</p>
<nav><a href="#decide">Your {len(X['decisions'])} decisions</a><a href="#minute">First minute</a><a href="#ai">AI clip frames</a><a href="#decided">What I decided</a><a href="#all">All graphics and clips</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(X['decisions'])})</h2><ol>{''.join('<li>' + d + '</li>' for d in X['decisions'])}</ol></section>
<section id="minute"><h2>The first minute (0:00 to {mmss(fm['end'])})</h2><video controls preload="none" playsinline poster="first-minute/DRAFT - RO-18 round 1 - first minute.jpg" src="first-minute/DRAFT - RO-18 round 1 - first minute - REVIEW 540p.mp4"></video>
<p class="small"><a href="first-minute/DRAFT - RO-18 round 1 - first minute.mp4">1080p</a> · {fm['links']}</p><p class="small">{fm['note']}</p></section>
<section id="ai"><h2>AI clip frames ({len(X['ai'])} ideas)</h2><p class="small">{X['ai_intro']}</p>{''.join(ai_html)}</section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + d + '</li>' for d in X['decided'])}</ul></section>
<section id="all"><h2>All graphics and clips, in order ({len(rows)})</h2><p class="small">Each still is the real graded frame at its real time, taken after every part has landed. Every item has a "Play it moving, in context" button.</p><div class="grid">{''.join(cards)}</div></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + d + '</li>' for d in X['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
open(f"{OUT}/index.html", "w").write(page); print("page ok", len(rows), "items")
