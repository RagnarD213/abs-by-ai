#!/usr/bin/env python3
"""SL-09 R4 review page (Oura Ring Review SFL R4): a later round, so only what changed (VIDEO-RULES 2026-10-08 / 2026-10-10).
Header, what changed with exact times and watch ranges, shorts 4 and 5 whole, each new AI clip moving (alone and in context)
beside its start/end frames, "What I decided", one reply box. Shorts 1-3 are finalized and listed only.
Copy lives in r4_page.json (written by hand after the build); this file is layout.
  page_r4.py -> review/index.html     serve: review_server.py 8989 /Volumes/Extreme/_edit_work/sl09/round2/review"""
import html, json, os
E = html.escape; R = "/Volumes/Extreme/_edit_work/sl09/round2/review"; W9 = "/Volumes/Extreme/_edit_work/sl09/round2"
D = json.load(open(f"{W9}/r4_page.json"))
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
changes = "".join(
    f'<li><b>{E(c["short"])}, {E(c["what"])}</b><br>{c["detail"]}<br><span class="when">In the new file: {mmss(c["a"])} to {mmss(c["b"])}. '
    f'Watch {mmss(c["wa"])} to {mmss(c["wb"])}.</span> '
    + (f'<button class="play" data-src="{E(c["ctx"])}" data-label="{E(c["short"])}: {E(c["what"])}, {mmss(c["wa"])} to {mmss(c["wb"])}">Play this part</button>' if c.get("ctx") else "")
    + "</li>" for c in D["changes"])
shorts = "".join(
    f'<div class="sh"><h3>{E(s["name"])}</h3><p class="len">{E(s["len"])}</p>'
    f'<button class="play" data-src="{E(s["review"])}" data-label="{E(s["name"])} (whole short)">Play the whole short</button>'
    f'<p>{s["check"]}</p><p class="small">{s["vlc"]}<br>Sound check (Zeeshan\'s own cut of this passage, then the short): <a href="{E(s["ab"])}" target="_blank">A/B clip</a></p></div>'
    for s in D["shorts"])
def clip_card(c):
    fr = "".join(f'<div><a href="{E(f)}" target="_blank"><img loading="lazy" src="{E(f.replace(".jpg", "_sm.jpg"))}"></a><span>{lab}</span></div>'
                 for f, lab in ((c["start"], "START"), (c["end"], "END")))
    btns = (f'<button class="play" data-src="{E(c["alone"])}" data-label="{E(c["name"])}: the clip as it plays in the short">Play the clip</button> '
            f'<button class="play" data-src="{E(c["ctx"])}" data-label="{E(c["name"])}: in context, with about 3 s either side">Play it moving, in context</button>')
    return (f'<div class="pair"><h4>{E(c["name"])} <span class="tag">{E(c["id"])}</span></h4>{fr}<div class="info">{c["about"]}<br>{btns}</div></div>')
clips = "".join(clip_card(c) for c in D["clips"])
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Oura Ring Review SFL R4</title>
<style>:root{{--bg:#050d1c;--panel:#0b1a30;--line:#234a6e;--cy:#68c5ff;--text:#f4faff;--muted:#b4c6d8}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px system-ui,-apple-system,sans-serif;line-height:1.55}}
main{{max-width:1180px;margin:0;padding:28px 16px 28px 28px}}#dock{{position:fixed;right:18px;top:18px;width:min(420px,32vw);background:#030915;border:1px solid var(--line);border-radius:14px;padding:12px;z-index:5}}
#dock video{{width:100%;max-height:78vh;border-radius:10px;background:#000;display:block}}#dock p{{margin:6px 0 0;font-size:14px;color:var(--muted)}}
@media(min-width:1100px){{main{{margin-right:calc(min(420px,32vw) + 40px)}}}}@media(max-width:1099px){{#dock{{position:sticky;top:0;width:auto;margin:0 0 12px}}#dock video{{max-height:50vh}}}}
h1{{font-size:34px;margin:0 0 6px}}h2{{font-size:24px;margin-top:0}}h3{{font-size:17px;margin:10px 0 4px}}p,li{{color:var(--muted)}}li b,p b{{color:var(--text)}}
section{{margin:24px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:16px}}
img{{width:100%;border-radius:10px;background:#000;display:block}}a{{color:#9bd6ff}}.tag{{color:#fff;background:#1f6fb0;font-size:12px;font-weight:700;padding:2px 8px;border-radius:9px}}
.len{{font-size:15px;color:var(--muted);font-weight:400}}.small{{font-size:14px}}.notice{{border-left:4px solid var(--cy);padding:10px 16px;background:#0e2440}}.when{{color:#dfe9f2;font-size:15px}}
button{{background:#1f6fb0;color:#fff;border:0;border-radius:9px;padding:8px 14px;cursor:pointer;font-size:14px;margin-top:8px}}button.on{{background:#2a9d5c}}
ol li,ul li{{margin-bottom:12px}}.shorts{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.sh{{background:#07142a;padding:14px;border-radius:12px}}.sh h3{{margin-top:0}}
.pairs{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px;background:#07142a;padding:12px;border-radius:12px;align-content:start}}
.pair div{{position:relative}}.pair img{{aspect-ratio:9/16;object-fit:cover}}.pair h4{{grid-column:1/3;margin:0 0 2px;font-size:19px}}.pair .info{{grid-column:1/3;font-size:14px;color:#dfe9f2}}
.pair span{{position:absolute;left:8px;top:8px;background:#000a;padding:2px 8px;border-radius:8px;font-size:12px;font-weight:700}}
textarea{{width:100%;box-sizing:border-box;min-height:260px;background:#030915;color:#fff;padding:14px;font:15px ui-monospace,monospace;border:1px solid #2c5d8a;border-radius:10px}}
nav{{display:flex;gap:14px;flex-wrap:wrap;font-size:15px}}@media(max-width:900px){{.shorts,.pairs{{grid-template-columns:1fr}}}}@media(max-width:520px){{h1{{font-size:27px}}main{{padding:20px 16px}}}}</style>
<div id="dock"><video id="v" controls playsinline preload="none"></video><p id="vl">Press any "Play" button: it plays here.</p></div>
<main><h1>Oura Ring Review shorts / Round 4</h1>
<p>{D["intro"]}</p>
<p class="notice">{D["locked"]}</p>
<nav><a href="#changed">What changed</a><a href="#shorts">Shorts 4 and 5</a><a href="#clips">The AI clips</a><a href="#decided">What I decided</a><a href="#reply">Reply</a></nav>
<section id="changed"><h2>What changed (watch only these)</h2><ol>{changes}</ol><p>{D["unchanged"]}</p></section>
<section id="shorts"><h2>Shorts 4 and 5, finished</h2><div class="shorts">{shorts}</div></section>
<section id="clips"><h2>The AI clips, moving</h2><p>{D["clips_intro"]}</p><div class="pairs">{clips}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{"".join(f"<li>{d}</li>" for d in D["decided"])}</ul></section>
<section id="reply"><h2>Reply</h2><textarea id="r">{E(D["reply"])}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy</button></p></section>
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
