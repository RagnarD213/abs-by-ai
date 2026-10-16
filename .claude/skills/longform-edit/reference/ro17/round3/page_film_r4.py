"""RO-17 round 4 film page: the full film (540p review copy) in one player, the revision list with jump buttons and watch ranges,
"What I decided", the AI clips with their reviews, the gate results. One reply box (local copy only). Dan 2026-09-30, 10-10."""
import json, html, os, sys
W = "/Volumes/Extreme/_edit_work/RO-17/round3"; OUT = f"{W}/review_r4"; E = html.escape
X = json.load(open(f"{OUT}/page_r4.json"))
def mmss(t): return f"{int(t // 60)}:{int(t % 60):02d}"
rev = "".join(f"""<li><b>{E(r['what'])}</b> <span class="small">at {mmss(r['t'])}</span><br>{E(r['detail'])}<br>
<button onclick="go({max(0, r['w0'])})">Watch {mmss(max(0, r['w0']))} to {mmss(r['w1'])}</button></li>""" for r in X["revisions"])
dec = "".join(f"<li>{E(d)}</li>" for d in X["decided"])
ai = "".join(f"""<tr><td>{E(a['name'])} <span class="tag">{a['id']}</span></td><td><button onclick="go({a['t0']})">{mmss(a['t0'])}</button></td>
<td>{a['secs']:.1f} s</td><td>{E(a['take'])}</td><td>{E(a['review'])}</td></tr>""" for a in X["ai"])
gates = "".join(f"<li>{E(g)}</li>" for g in X["gates"])
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>3 Healthy Foods R4</title><style>
:root{{--bg:#f6f7f9;--fg:#15181d;--muted:#5b6370;--card:#fff;--line:#dde1e7;--acc:#2a6fdb}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111418;--fg:#e8ebef;--muted:#9aa3ae;--card:#1a1f25;--line:#2b323b;--acc:#6aa1ff}}}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 -apple-system,system-ui,sans-serif;margin:0;padding:16px}}
main{{max-width:1100px;margin:0 auto}} .card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:14px 0}}
video{{width:100%;border-radius:8px;background:#000}} .small{{color:var(--muted);font-size:14px}} .tag{{font-size:12px;color:var(--muted)}}
button{{background:var(--acc);color:#fff;border:0;border-radius:6px;padding:5px 10px;margin:4px 0;cursor:pointer;font-size:14px}}
li{{margin:8px 0}} table{{border-collapse:collapse;width:100%}} td{{border-top:1px solid var(--line);padding:6px;vertical-align:top;font-size:14px}}
textarea{{width:100%;min-height:120px;background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:8px;box-sizing:border-box}}
@media (min-width:1500px){{main{{max-width:1500px;display:grid;grid-template-columns:1fr 760px;gap:20px}} #pl{{position:sticky;top:12px;align-self:start;grid-column:2;grid-row:1/9}}}}
</style></head><body><main>
<div class="card" id="pl"><video id="v" controls preload="metadata" src="{E(X['film'])}"></video>
<div class="small">Full film, {E(X['length'])}, 540p review copy. Full quality for VLC: Videos to Review/{E(X['vlc'])}</div></div>
<div class="card"><h1>3 Healthy Foods That Made Me Fat, round 4: the full film</h1>
<p>{E(X['summary'])}</p><p class="small">Nothing is waiting on you except watching the changed parts below. Your decisions: none.</p></div>
<div class="card"><h2>What changed since round 2 (watch only these)</h2><ol>{rev}</ol>
<p class="small">Everything else is the round 2 edit you approved, unchanged: same cuts, graphics, colour and sound.</p></div>
<div class="card"><h2>What I decided</h2><ul>{dec}</ul></div>
<div class="card"><h2>The AI clips (all passed the motion check and a fresh reviewer)</h2><table>{ai}</table></div>
<div class="card"><h2>Checks run on this exact file</h2><ul>{gates}</ul></div>
<div class="card"><h2>Your notes</h2><textarea id="n" placeholder="Notes for round 5, with times"></textarea>
<button onclick="navigator.clipboard.writeText(document.getElementById('n').value)">Copy my notes</button></div>
</main><script>
function go(t){{const v=document.getElementById('v');v.currentTime=t;v.play();v.scrollIntoView({{behavior:'smooth',block:'nearest'}})}}
try{{const n=document.getElementById('n');n.value=localStorage.getItem('ro17r4')||'';n.oninput=()=>{{try{{localStorage.setItem('ro17r4',n.value)}}catch(e){{}}}}}}catch(e){{}}
</script></body></html>"""
open(f"{OUT}/index.html", "w").write(page); print("page", f"{OUT}/index.html")
