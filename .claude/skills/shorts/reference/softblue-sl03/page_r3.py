#!/usr/bin/env python3
"""SL-03 round 3 review page: the two revised shorts (2 and 4); the four approved ones are a record line. Same layout as round 2: (standard layout: header, your decisions, what I
decided, every short three per row with one floating player, checks, one reply box). Serve with
`_shared/review_server.py 8831 /Volumes/Extreme/_edit_work/sl03/r3/review`.
  page_r3.py   (reads r3/review/extra.json for the decisions, decided and checks lists)"""
import html, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
import importlib.util as _iu                      # `deliver` on sys.path is _shared/deliver (the gate); load ours by path
_sp = _iu.spec_from_file_location("sl03_deliver", os.path.join(HERE, "deliver.py")); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
E = html.escape; R = "/Volumes/Extreme/_edit_work/sl03/r3/review"; FF = Bt.lib.FF
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
os.makedirs(f"{R}/media", exist_ok=True)
X = json.load(open(f"{R}/extra.json"))
cards = []
for S in ("S2", "S4"):
    d = Bt.D(S); T = json.load(open(f"{d}/timeline.json")); man = json.load(open(f"{d}/hf/manifest.json")) if os.path.exists(f"{d}/hf/manifest.json") else []
    n = S[1]; base = f"daily-salad-{P.NAME[S]}"
    rv = f"{Dl.REV}/{base} - REVIEW 540p.mp4"; ab = f"{Dl.REV}/AB_source-vs-short_{base}.mp4"
    for src, dst in ((rv, f"media/{base} - REVIEW 540p.mp4"), (ab, f"media/AB {base}.mp4"), (Dl.dname(S), f"media/{base}.mp4")):
        if os.path.exists(src) and (not os.path.exists(f"{R}/{dst}") or os.path.getsize(f"{R}/{dst}") != os.path.getsize(src)): shutil.copyfile(src, f"{R}/{dst}")
    poster = f"media/{base}.jpg"
    subprocess.run([FF, "-v", "error", "-y", "-ss", "3.5", "-i", f"{R}/media/{base} - REVIEW 540p.mp4", "-frames:v", "1", "-q:v", "3", f"{R}/{poster}"], check=True)
    eb, hl = P.TITLE[S]
    bars = "".join(f"<li>{mmss(m['a'])} to {mmss(m['b'])}: <b>{E(m['topic'])}</b>: {E(' / '.join(p[0] for p in m['parts']))}</li>" for m in man) or "<li>none</li>"
    gate = json.load(open(Dl.dname(S) + ".deliver_gate.json")) if os.path.exists(Dl.dname(S) + ".deliver_gate.json") else {}
    verdict = gate.get("verdict", "not run")
    cards.append(f"""<article id="{S}"><h3>Short {n}: {E(hl[0].title() + ' ' + hl[1].title())} <span class="small">{mmss(T['total'])}</span></h3>
<a href="media/{base} - REVIEW 540p.mp4"><img loading="lazy" src="{poster}"></a><button onclick="play('media/{base} - REVIEW 540p.mp4','Short {n}')">Play short {n}</button>
<div class="copy"><b>{E(eb)}</b> / {E(' '.join(hl))}<br>Key points:<ul>{bars}</ul>{X['notes'].get(S, '')}<br><a href="media/{base}.mp4">1080 x 1920 file</a> · <a href="media/AB {base}.mp4">sound check (long-form, then short)</a> · gate: {E(verdict)}</div></article>""")
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Daily Salad SFC R3</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}p,li{{color:#bdd0e4}}li b{{color:#edf5ff}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.copy li{{color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:200px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b;margin-bottom:16px;text-align:center}}#dock video{{max-height:60vh;width:auto;max-width:100%}}
@media(min-width:1500px){{body{{padding-right:min(30vw,520px)}}#dock{{position:fixed;top:16px;right:16px;width:calc(min(30vw,520px) - 40px);max-height:calc(100vh - 32px);box-sizing:border-box;margin:0;box-shadow:0 8px 40px #000a}}#dock video{{max-height:calc(100vh - 110px)}}}}
@media(max-width:1499px){{#dock video{{max-height:42vh}}}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<main><h1>Daily Salad shorts / Round 3: shorts 2 and 4</h1><p>{X['intro']}</p>
<p class="notice"><b>Already locked, reused as is:</b> {X['locked']}</p>
<nav><a href="#decide">Your {len(X['decisions'])} decision{'s' if len(X['decisions']) != 1 else ''}</a><a href="#shorts">The two shorts</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(X['decisions'])})</h2><ol>{''.join('<li>' + x + '</li>' for x in X['decisions'])}</ol></section>
<section id="shorts"><h2>The two revised shorts</h2><p class="small">Each button plays that short in the one player (at the right on a wide screen). The players can be scrubbed.</p>
<div id="dock"><div class="small" id="nowp">Pick a short below to play it here.</div><video id="pv" controls preload="none" playsinline></video></div><div class="grid">{''.join(cards)}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + x + '</li>' for x in X['decided'])}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + x + '</li>' for x in X['checks'])}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(X['reply'])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
open(f"{R}/index.html", "w").write(page); print("page ok", page.count("—"), "em dashes")
