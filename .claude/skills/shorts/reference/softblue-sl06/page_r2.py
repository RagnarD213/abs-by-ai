#!/usr/bin/env python3
"""SL-06 round 2 review page: Dan's FIRST review of the batch (he skipped round 1). Standard layout: header, your
decisions, the six finished shorts with one floating player, the pickup joins and the voice choice, the AI frame pairs,
what I decided, every title / crop / clip / graphic / key point of all six as stills (three per row, each plays in the
finished short with about 3 s either side), checks, one reply box.
  export_stills_r2.py A B C D E F ; page_r2.py      serve: review_server.py 8819 /Volumes/Extreme/_edit_work/sl06/round2"""
import html, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt, notes_r2 as N
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sl06_deliver", os.path.join(HERE, "deliver.py")); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
from gate import require_pass
E = html.escape; R = Bt.WORK + "/round2"; FF = Bt.lib.FF
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
os.makedirs(f"{R}/media", exist_ok=True); os.makedirs(f"{R}/ai", exist_ok=True)
def cp(src, dst):
    if not os.path.exists(f"{R}/{dst}") or os.path.getsize(f"{R}/{dst}") != os.path.getsize(src): shutil.copyfile(src, f"{R}/{dst}")
    return dst

# ---- the six finished shorts
cards, vids = [], {}
for S in N.ORDER:
    d = Bt.D(S); T = json.load(open(f"{d}/timeline.json")); man = json.load(open(f"{d}/hf/manifest.json"))
    base = os.path.basename(Dl.dname(S))[:-4]; name = " ".join(P.TITLE[S][1])
    rv = cp(f"{Dl.REV}/{base} - REVIEW 540p.mp4", f"media/{S} - REVIEW 540p.mp4"); vids[S] = rv
    full = cp(Dl.dname(S), f"media/{S} - 1080x1920.mp4")
    ab = f"{Dl.REV}/AB_film-vs-short_{base}.mp4"; ab = cp(ab, f"media/{S} - sound check.mp4") if os.path.exists(ab) else None
    poster = f"media/{S}.jpg"
    subprocess.run([FF, "-v", "error", "-y", "-ss", "4.5", "-i", f"{R}/{rv}", "-frames:v", "1", "-q:v", "3", f"{R}/{poster}"], check=True)
    bars = "".join(f"<li>{mmss(m['a'])}: <b>{E(m['topic'])}</b>: {E(' / '.join(p[0] for p in m['parts']))}</li>" for m in man)
    join = ""
    if S in P.PICKUP:
        j = cp(f"{R}/joins/{S}_join.mp4", f"media/{S} - pickup into film.mp4")
        join = f'<button onclick="play(\'{j}\',{E(json.dumps("Short " + S + ": your pickup into the film"))},0)">Pickup into film (6 s)</button>'
    gate = json.load(open(Dl.dname(S) + ".deliver_gate.json")) if os.path.exists(Dl.dname(S) + ".deliver_gate.json") else {}
    cards.append(f"""<article id="f{S}"><h3>{S}: {E(name)} <span class="small">{mmss(T['total'])}</span></h3>
<a href="{rv}" target="_blank"><img loading="lazy" src="{poster}"></a><button onclick="play('{rv}',{E(json.dumps('Short ' + S + ': ' + name))},0)">Play it</button> {join}
<div class="copy">{N.SHORT[S]}<br>Key points:<ul>{bars}</ul><a href="{full}">1080 x 1920 file</a>{f' · <a href="{ab}">sound check (the film, then the short)</a>' if ab else ''}</div></article>""")

# ---- AI frame pairs (only pairs that passed the frame gate AND an independent reviewer)
ai = []
for k, txt in N.AI:
    st, en = f"{Bt.WORK}/aiframes/{k}_start.jpg", f"{Bt.WORK}/aiframes/{k}_end.jpg"
    require_pass(st, en)
    a1, a2 = cp(st, f"ai/{k}_start.jpg"), cp(en, f"ai/{k}_end.jpg")
    ai.append(f'<div class="pair"><div><a href="{a1}" target="_blank"><img loading="lazy" src="{a1}"></a><span>{N.AI_LABEL[k][0]}</span></div>'
              f'<div><a href="{a2}" target="_blank"><img loading="lazy" src="{a2}"></a><span>{N.AI_LABEL[k][1]}</span></div><p>{txt}</p></div>')

# ---- every item as a still that plays in the finished short
def card(it, S):
    key = f"{S}.{it['id']}"; extra = N.ITEM.get(key, ""); tag = N.TAG.get(key, "")
    t = f' <span class="tag">{E(tag)}</span>' if tag else ""
    kind = dict(crop="Crop", clip="Clip", graphic="Graphic", bar="Key point", phone="Phone demo")[it["kind"]]
    a0 = max(0.0, it["a"] - 3.0)
    sp = (f'<details><summary>What you are saying</summary><b>before:</b> {E(it["before"] or "(start of the short)")}<br>'
          f'<b>during:</b> {E(it["during"])}<br><b>after:</b> {E(it["after"] or "(end of the short)")}</details>')
    return (f'<article><a href="stills/{it["img"]}.jpg" target="_blank"><img loading="lazy" src="stills/{it["img"]}_sm.jpg"></a>'
            f'<h3>{S}: {kind}: {E(it["id"])}{t}</h3><button onclick="play(\'{vids[S]}\',{E(json.dumps(S + ": " + it["id"] + " in context"))},{a0:.2f})">Play it in the short ({mmss(a0)})</button>'
            f'<div class="copy">{mmss(it["a"])} to {mmss(it["b"])}. {E(it["note"])}' + (f"<br>{extra}" if extra else "") + f'{sp}</div></article>')
def extra_card(img, title, text, tag=""):
    t = f' <span class="tag">{E(tag)}</span>' if tag else ""
    return f'<article><a href="stills/{img}.jpg" target="_blank"><img loading="lazy" src="stills/{img}_sm.jpg"></a><h3>{title}{t}</h3><div class="copy">{text}</div></article>'
secs = []
for S in N.ORDER:
    J = json.load(open(f"{R}/items_{S}.json")); cs = [card(it, S) for it in J["items"]] + [extra_card(*x) for x in N.EXTRA.get(S, [])]
    secs.append(f'<section id="s{S}"><h2>Short {S}, every item: {E(" ".join(J["title"][1]))} <span class="small">{J["total"]:.0f} s</span></h2><div class="grid">{"".join(cs)}</div></section>')

voice = "".join(f'<li><button onclick="play(\'{cp(src, dst)}\',{E(json.dumps(lab))},0)">{E(lab)}</button> {E(why)}</li>' for src, dst, lab, why in N.VOICE)
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFC R2</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--text:#edf5ff;--muted:#bdd0e4}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px system-ui,-apple-system,sans-serif;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}
h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px;margin-top:0}}h3{{font-size:17px;margin:10px 0 4px}}p,li{{color:var(--muted)}}li b,p b{{color:var(--text)}}
section{{margin:28px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}
article{{min-width:0;background:#081626;padding:12px;border-radius:12px}}img,video{{width:100%;border-radius:10px;background:#000;display:block}}a{{color:#8cd6ff}}.small{{font-size:14px;color:#9fb7cf;font-weight:400}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.copy li{{color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
.tag{{color:#fff;background:#1f6fb0;font-size:12px;font-weight:700;padding:2px 8px;border-radius:9px}}details{{margin-top:6px;font-size:13px}}summary{{cursor:pointer;color:#8cd6ff}}
.pairs{{display:grid;grid-template-columns:1fr 1fr;gap:26px}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.pair p{{grid-column:1/3;margin:4px 0;font-size:14px;color:#d7e6f5}}.pair div{{position:relative}}.pair span{{position:absolute;left:8px;top:8px;background:#000a;padding:2px 8px;border-radius:8px;font-size:12px;font-weight:700}}
textarea{{width:100%;box-sizing:border-box;min-height:520px;background:#071221;color:white;padding:14px;font:15px ui-monospace,monospace;border:1px solid #47607b;border-radius:10px}}
#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px;text-align:center}}#dock video{{max-height:60vh;width:auto;max-width:100%;margin:auto}}
@media(min-width:1500px){{body{{padding-right:min(30vw,520px)}}#dock{{position:fixed;top:16px;right:16px;width:calc(min(30vw,520px) - 40px);max-height:calc(100vh - 32px);box-sizing:border-box;margin:0;box-shadow:0 8px 40px #000a}}#dock video{{max-height:calc(100vh - 110px)}}}}
@media(max-width:1499px){{#dock video{{max-height:42vh}}}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:7px 11px;cursor:pointer;font-size:14px;margin:6px 4px 0 0}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}.pairs{{grid-template-columns:1fr}}}}@media(max-width:560px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<main><h1>Top 5 Zepbound Tips shorts / Round 2: all six, finished</h1><p>{N.INTRO}</p>
<p class="notice"><b>Already locked and reused:</b> {N.LOCKED}</p>
<p class="notice"><b>Full-quality copies for VLC</b> are in <b>Videos to Review</b>: {E(", ".join(N.VLC))}</p>
<nav><a href="#decide">Your decisions ({len(N.DECISIONS)})</a><a href="#shorts">The six shorts</a><a href="#voice">Pickup sound</a><a href="#ai">AI frames</a><a href="#decided">What I decided</a>{"".join(f'<a href="#s{S}">{S} items</a>' for S in N.ORDER)}<a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Pick any Play button: it plays here (at the right on a wide screen). Every player can be scrubbed.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="decide"><h2>Your decisions ({len(N.DECISIONS)})</h2><ol>{"".join(f"<li>{x}</li>" for x in N.DECISIONS)}</ol></section>
<section id="shorts"><h2>The six shorts, finished</h2><p class="small">{N.SHORTS_NOTE}</p><div class="grid">{"".join(cards)}</div></section>
<section id="voice"><h2>Pickup sound: two treatments of the same take (decision {N.VOICE_DECISION})</h2><p>{N.VOICE_INTRO}</p><ul>{voice}</ul></section>
<section id="ai"><h2>New AI clips: start and end frames (no motion made yet)</h2><p>{N.AI_INTRO}</p><div class="pairs">{"".join(ai)}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{"".join(f"<li>{x}</li>" for x in N.DECIDED)}</ul></section>
{"".join(secs)}
<section id="checks"><h2>Checks</h2><ul>{"".join(f"<li>{x}</li>" for x in N.CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(N.REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button></p></section></main>
<script>function play(src,id,t){{const v=document.getElementById('pv');const go=()=>{{try{{v.currentTime=t||0}}catch(e){{}};v.play()}};document.getElementById('nowp').textContent=id;
if(v.getAttribute('src')!==src){{v.src=src;v.addEventListener('loadedmetadata',go,{{once:true}});v.load()}}else go();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
