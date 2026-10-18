#!/usr/bin/env python3
"""SL-09 round 1 review page (Oura Ring Review SFL R2). PRE-RENDER-APPROVAL layout: header, decisions, the five finished shorts,
the AI frame ideas, "What I decided", then every title / crop / clip / phone screen / scene / key point of each short as a still
on its real frame, three per row, each with "Play it moving, in context" feeding ONE floating player at the right; one reply box.
  page_r1.py  -> review/index.html     serve: review_server.py 8987 /Volumes/Extreme/_edit_work/sl09/round2/review"""
import html, json, os, shutil
E = html.escape; R = "/Volumes/Extreme/_edit_work/sl09/round2/review"
import notes_r1 as N
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
KIND = dict(title="Title", crop="Crop", clip="Clip", graphic="Moving scene", bar="Key point", phone="Phone screen")
def card(it, S):
    key = f"{S}.{it['id']}"; extra = N.ITEM.get(key, "")
    sp = (f'<details><summary>What you are saying</summary><b>before:</b> {E(it["before"] or "(start of the short)")}<br>'
          f'<b>during:</b> {E(it["during"])}<br><b>after:</b> {E(it["after"] or "(end of the short)")}</details>') if it["kind"] != "title" else ""
    btn = (f'<button class="play" data-src="{E(it["ctx"])}" data-label="{E(N.NAMES[S])}: {E(KIND[it["kind"]])} {E(it["id"])}, '
           f'{mmss(it["a"])} to {mmss(it["b"])} (with about 3 s either side)">Play it moving, in context</button>') if it.get("ctx") else ""
    return (f'<article><a href="stills/{it["img"]}.jpg" target="_blank"><img loading="lazy" src="stills/{it["img"]}_sm.jpg"></a>'
            f'<h3>{KIND[it["kind"]]} · {E(it["id"])}</h3><div class="copy">{mmss(it["a"])} to {mmss(it["b"])}. {E(it["note"])}'
            + (f"<br>{extra}" if extra else "") + f'</div>{btn}{sp}</article>')
secs = []
for S in N.ORDER:
    J = json.load(open(f"{R}/items_{S}.json")); n = N.NUM[S]
    cards = "".join(card(it, S) for it in J["items"])
    secs.append(f'<section id="s{S}"><h2>Short {n}: {E(N.NAMES[S])} <span class="len">{J["total"]:.0f} s</span></h2><p>{N.ABOUT[S]}</p><div class="grid">{cards}</div></section>')
shorts = "".join(
    f'<div class="sh"><h3>Short {N.NUM[S]}: {E(N.NAMES[S])}</h3><p class="len">{N.LEN[S]}</p>'
    f'<button class="play" data-src="{E(N.REVIEW[S])}" data-label="Short {N.NUM[S]}: {E(N.NAMES[S])} (whole short)">Play the whole short</button>'
    f'<p>{N.CHECK[S]}</p><p class="small">VLC copy: <b>Videos to Review / {E(N.VLC[S])}</b><br>Sound check (Zeeshan\'s own cut of this passage, then the short): '
    f'<a href="{E(N.AB[S])}" target="_blank">A/B clip</a></p></div>' for S in N.ORDER)
def ai_card(i):
    k, S, name, when, before, under, after, see, ifno, note = i
    rows = [("When", when), ("Just before", before), ("It plays under", f"<b>\"{E(under)}\"</b>"), ("Right after", after), ("What you see", see), ("If you say no", ifno)] + ([("Note", note)] if note else [])
    dl = "".join("<dt>%s</dt><dd>%s</dd>" % (a, b if a == "It plays under" else E(b)) for a, b in rows)
    return (f'<div class="pair"><h4>{E(name)} <span class="tag">{k}</span></h4><div><a href="ai/{k}_start.jpg" target="_blank"><img loading="lazy" src="ai/{k}_start_sm.jpg"></a><span>START</span></div>'
            f'<div><a href="ai/{k}_end.jpg" target="_blank"><img loading="lazy" src="ai/{k}_end_sm.jpg"></a><span>END</span></div><dl>{dl}</dl></div>')
ai = "".join(f'<div class="aigroup"><h3>In short {N.NUM[S]}, "{E(N.NAMES[S])}"</h3><p>{E(N.ABOUT_AI[S])}</p><div class="pairs">{"".join(ai_card(i) for i in N.AI_ITEMS if i[1] == S)}</div></div>'
             for S in N.ORDER if any(i[1] == S for i in N.AI_ITEMS))
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Oura Ring Review SFL R2</title>
<style>:root{{--bg:#050d1c;--panel:#0b1a30;--line:#234a6e;--cy:#68c5ff;--text:#f4faff;--muted:#b4c6d8}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px system-ui,-apple-system,sans-serif;line-height:1.55}}
main{{max-width:1180px;margin:0;padding:28px 16px 28px 28px}}#dock{{position:fixed;right:18px;top:18px;width:min(420px,32vw);background:#030915;border:1px solid var(--line);border-radius:14px;padding:12px;z-index:5}}
#dock video{{width:100%;max-height:78vh;border-radius:10px;background:#000;display:block}}#dock p{{margin:6px 0 0;font-size:14px;color:var(--muted)}}
@media(min-width:1100px){{main{{margin-right:calc(min(420px,32vw) + 40px)}}}}@media(max-width:1099px){{#dock{{position:sticky;top:0;width:auto;margin:0 0 12px}}#dock video{{max-height:50vh}}}}
h1{{font-size:34px;margin:0 0 6px}}h2{{font-size:24px;margin-top:0}}h3{{font-size:17px;margin:10px 0 4px}}p,li{{color:var(--muted)}}li b,p b{{color:var(--text)}}
section{{margin:24px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:16px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
article{{min-width:0;background:#07142a;padding:12px;border-radius:12px}}img{{width:100%;border-radius:10px;background:#000;display:block}}article img{{aspect-ratio:9/16;object-fit:cover}}
a{{color:#9bd6ff}}.tag{{color:#fff;background:#1f6fb0;font-size:12px;font-weight:700;padding:2px 8px;border-radius:9px}}.len{{font-size:15px;color:var(--muted);font-weight:400}}
.copy{{font-size:14px;color:#dfe9f2}}.small{{font-size:14px}}.notice{{border-left:4px solid var(--cy);padding:10px 16px;background:#0e2440}}
details{{margin-top:6px;font-size:13px;color:#b4c6d8}}summary{{cursor:pointer;color:#9bd6ff}}
button{{background:#1f6fb0;color:#fff;border:0;border-radius:9px;padding:8px 14px;cursor:pointer;font-size:14px;margin-top:8px}}button.on{{background:#2a9d5c}}
.shorts{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.sh{{background:#07142a;padding:14px;border-radius:12px}}.sh h3{{margin-top:0}}
.pairs{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px;background:#07142a;padding:12px;border-radius:12px;align-content:start}}
.pair div{{position:relative}}.pair img{{aspect-ratio:9/16;object-fit:cover}}.pair h4{{grid-column:1/3;margin:0 0 2px;font-size:19px}}
.pair dl{{grid-column:1/3;margin:6px 0 0;font-size:14px;color:#dfe9f2;display:grid;grid-template-columns:104px 1fr;gap:5px 10px}}.pair dt{{color:var(--cy);font-weight:700}}.pair dd{{margin:0}}
.pair span{{position:absolute;left:8px;top:8px;background:#000a;padding:2px 8px;border-radius:8px;font-size:12px;font-weight:700}}.aigroup{{margin:22px 0 0;padding-top:16px;border-top:1px solid var(--line)}}.aigroup h3{{font-size:21px}}
textarea{{width:100%;box-sizing:border-box;min-height:380px;background:#030915;color:#fff;padding:14px;font:15px ui-monospace,monospace;border:1px solid #2c5d8a;border-radius:10px}}
nav{{display:flex;gap:14px;flex-wrap:wrap;font-size:15px}}@media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}.shorts,.pairs{{grid-template-columns:1fr}}}}@media(max-width:520px){{.grid{{grid-template-columns:1fr}}h1{{font-size:27px}}}}</style>
<div id="dock"><video id="v" controls playsinline preload="none"></video><p id="vl">Press any "Play" button: it plays here.</p></div>
<main><h1>Oura Ring Review shorts / Round 1</h1>
<p>{N.INTRO}</p>
<p class="notice"><b>Already locked and reused:</b> {N.LOCKED}</p>
<nav><a href="#decide">Your decisions ({len(N.DECISIONS)})</a><a href="#shorts">The five shorts</a><a href="#ai">AI frames</a><a href="#decided">What I decided</a>{"".join(f'<a href="#s{S}">{N.NUM[S]}. {E(N.NAMES[S])}</a>' for S in N.ORDER)}<a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(N.DECISIONS)})</h2><ol>{"".join(f"<li>{d}</li>" for d in N.DECISIONS)}</ol></section>
<section id="shorts"><h2>The five shorts, finished</h2><p>{N.SHORTS_INTRO}</p><div class="shorts">{shorts}</div></section>
<section id="ai"><h2>Two AI opener ideas: start and end frames (no motion made yet)</h2><p>{N.AI_INTRO}</p>{ai}</section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{"".join(f"<li>{d}</li>" for d in N.DECIDED)}</ul></section>
{"".join(secs)}
<section id="reply"><h2>Reply</h2><textarea id="r">{E(N.REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy</button></p></section>
</main>
<script>
const v=document.getElementById('v'), vl=document.getElementById('vl');
document.querySelectorAll('button.play').forEach(b=>b.addEventListener('click',()=>{{
  document.querySelectorAll('button.play.on').forEach(x=>x.classList.remove('on')); b.classList.add('on');
  v.src=b.dataset.src; vl.textContent=b.dataset.label; v.load(); v.play().catch(()=>{{}});
}}));
</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
