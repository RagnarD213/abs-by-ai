"""RO-03 round-2 review page: the full film first, then "What I decided", what is new since round 1, the independent
review, the checks as they read, one reply box. A later round shows only what changed or is new (VIDEO-RULES 2026-10-08):
every graphic was approved in round 1, so the page links those stills and does not show them again.
Content comes from round2/page_extra.json. Served from round2/ on the same port as round 1."""
import json, html
W = "/Volumes/Extreme/_edit_work/ro03/round2"; X = json.load(open(f"{W}/page_extra.json")); E = html.escape
FILM = "RO-03 round 2 - full film"
li = lambda xs: "".join("<li>" + d + "</li>" for d in xs)
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RO-03 round 2</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1180px;margin:0 auto;padding:28px 24px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px;margin-top:0}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.small{{font-size:14px;color:#9fb7cf}}.ok{{color:#9be7b5}}.warn{{color:#ffd28a}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
textarea{{width:100%;box-sizing:border-box;min-height:160px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
table.map td{{padding:4px 14px 4px 0;font-size:15px;color:#cfe0f0;vertical-align:top}}button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin:8px 8px 0 0}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:800px){{h1{{font-size:30px}}}}</style>
<main><h1>RO-03 / Round 2: the full film</h1><p>{X['intro']}</p>
<p class="notice"><b>Locked in round 1 and built exactly that way:</b> {X['locked']}</p>
<nav><a href="#film">The full film</a><a href="#decided">What I decided</a><a href="#new">New since round 1</a><a href="#review">Independent review</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="film"><h2>The full film ({X['film_len']})</h2><video id="pv" controls preload="metadata" playsinline src="{FILM} - REVIEW 540p.mp4"></video>
<p>{''.join(f'<button onclick="go({t})">{E(n)}</button>' for t, n in X['jumps'])}</p>
<p class="small">For VLC: <b>{E(X['vlc'])}</b> in the project folder <b>Videos to Review</b> (the full-quality file). · <a href="RO03_MASTER.mp4">1080p file</a> · <a href="RO-03 audio AB (reference then ours).mp4">audio A/B: Muhammad's mix, then this one</a> · <a href="RO03.srt">subtitle file</a> · <a href="RO03.chapters.txt">chapters</a></p>
<table class="map">{''.join(f"<tr><td>{a}</td><td><b>{E(b)}</b></td><td>{E(c)}</td></tr>" for a, b, c in X['map'])}</table></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{li(X['decided'])}</ul></section>
<section id="new"><h2>New since round 1</h2><ul>{li(X['new'])}</ul><p class="small">Every graphic is the one you approved in round 1. Those stills are still on the round 1 list in the delivery notes; nothing about them changed, so they are not shown again.</p></section>
<section id="review"><h2>Independent review</h2><p><b>{X['verdict']}</b></p><ul>{li(X['review'])}</ul><p class="small"><a href="ROUND-2-REVIEW.md">The reviewer's full file</a></p></section>
<section id="checks"><h2>Checks, as they read</h2><ul>{li(X['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function go(t){{const v=document.getElementById('pv');v.currentTime=t;v.play();}}</script></html>"""
assert page.count("—") == 0 and page.count("–") == 0, "an em or en dash is on the page"
open(f"{W}/index.html", "w").write(page); print("page ok")
