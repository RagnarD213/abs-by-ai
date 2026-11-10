"""DS-78 R1 review page: decisions on top, the whole Short in a floating scrubbable player, look options, What I decided,
every clip and graphic in timeline order with a play-in-context button (about 3 s either side, same shared player)."""
from pathlib import Path
import json, html
W = Path(__file__).resolve().parents[1]; O = W/'review'; esc = html.escape
m = json.load(open(W/'records/assembly.json')); look = json.load(open(W/'look-options.json')); VP = json.load(open(W/'records/visual-plan.json'))
words = json.load(open(W/'records/words.json')); dur = m['duration']
NAME = "How To Do Chest Flies On SFC R1"; movie = f'{NAME} - 1080p.mp4'; native = f'{NAME} - 1080p.mp4'; srt = f'{NAME}.srt'
def said(a, b): return ' '.join(w['w'] for w in words if a <= w['t0'] < b)
def mmss(t): return f"{int(t//60)}:{t%60:04.1f}"
qa = (W/'records/qa-status.html').read_text() if (W/'records/qa-status.html').exists() else '<p>Checks in progress.</p>'
decided = (W/'records/decided.html').read_text()
css = """:root{--bg:#0b1524;--card:#13223a;--ink:#e8eef8;--mut:#9fb0c8;--acc:#4da3ff}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,sans-serif}
main{max-width:1100px;padding:20px 16px 80px;margin-right:440px}h1{margin:0 0 4px;font-size:28px}h2{margin:34px 0 10px;font-size:21px;border-top:1px solid #24344f;padding-top:18px}h3{margin:6px 0;font-size:16px}
.intro{background:var(--card);border-radius:12px;padding:14px 16px}.muted{color:var(--mut);font-size:14px}ol.dec li{margin:8px 0}
button,.button{background:var(--acc);color:#04111f;border:0;border-radius:8px;padding:8px 12px;font-weight:700;cursor:pointer;margin:4px 6px 4px 0;text-decoration:none;display:inline-block;font-size:14px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:var(--card);border-radius:12px;padding:10px}.card img{width:100%;border-radius:8px;display:block}
.card .copy{font-size:13px;color:var(--mut)}details{margin-top:6px}summary{cursor:pointer;color:var(--acc);font-size:13px}.opt{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.opt img,.opt video{width:100%;border-radius:8px}.rec{outline:3px solid var(--acc)}audio{width:100%}textarea{width:100%;height:150px;background:#0e1b2f;color:var(--ink);border:1px solid #2b3f60;border-radius:8px;padding:10px;font:14px/1.4 monospace}
#dock{position:fixed;right:16px;top:16px;width:410px;background:var(--card);border-radius:14px;padding:12px;box-shadow:0 8px 30px #0008}#dock video{width:100%;max-height:72vh;background:#000;border-radius:8px}
@media(max-width:1100px){main{margin-right:0}#dock{position:sticky;top:0;width:100%;right:auto;z-index:5}.grid,.opt{grid-template-columns:1fr 1fr}}@media(max-width:600px){.grid,.opt{grid-template-columns:1fr}#dock{position:static}#dock video{max-height:62vh}}"""
H = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chest Flies SFC R1</title><style>{css}</style></head><body>',
     f'<aside id="dock"><div id="dockTitle"><b>Whole Short</b></div><video id="player" muted controls playsinline preload="metadata" src="{esc(movie)}" poster="media/P0.jpg"></video>'
     f'<div class="muted">Drag the timeline to seek. <a href="{esc(native)}" download style="color:var(--acc)">1080p</a> · <a href="{esc(srt)}" download style="color:var(--acc)">Subtitles</a></div></aside><main>',
     "<h1>How To Do Chest Flies On The Machine</h1>",
     f'<div class="intro"><b>Round 1 · whole Short, {dur:.1f} seconds · content (dedicated Short)</b><p>Built straight to the whole Short because everything in it is a kind you already approved on How To Do T-Bar Rows and Pull-Ups, filmed on the same camera roll minutes earlier: their look and voice, the large-title exercise windows, the small header, blue glass key-point bars and the sets-and-reps list card. One change: the intro is a window under the big title, not full screen, because a phone-shaped crop cuts your hands off at the stretch of a fly. If you pick a different colour, voice or crop below, only the picture or sound is re-rendered.</p>'
     '<p><b>Your decisions (4)</b></p><ol class="dec"><li><b>Colour:</b> F Deep And Vivid (recommended, your T-Bar Rows and Pull-Ups pick on this same roll) · E Vivid · B Richer Contrast</li>'
     '<li><b>Voice:</b> B Fuller Bass (recommended, your T-Bar Rows pick) · A Natural Warmth (your Pull-Ups pick) · C Original Mic · D Automatic Match</li>'
     '<li><b>Crop on you:</b> 1 Original Portrait (recommended, your T-Bar Rows and Pull-Ups pick) · 2 Slightly Closer · 3 Closer Still</li><li><b>"Set the seat" picture:</b> no close-up of setting this machine&#39;s seat was filmed. Keep the wide side view of you on the machine, showing the seat and handle height (recommended, B02 at 0:09) · or stay on you for that line.</li></ol>'
     f'<button onclick="play(0,{dur:.3f},\'Whole Short\')">Play the whole Short</button></div>',
     '<h2>1 · Colour</h2><p class="muted">Same 12 seconds of you in each. The gym clips keep the colour you approved for the library (C).</p><div class="opt">']
for k in ['F', 'E', 'B']:
    g = look['colours'][k]
    H.append(f'<div class="{"rec" if k == "F" else ""}"><h3>{k} · {esc(g["name"])}{" (recommended)" if k == "F" else ""}</h3><video muted controls playsinline preload="none" poster="media/colour-{k}-276.0.jpg" src="media/colour-{k}.mp4"></video><p class="muted">{esc(g["note"])}</p></div>')
H.append('</div><h2>2 · Voice</h2><p class="muted">The first 30 seconds of the Short, level matched. Each starts on your first word.</p><div class="opt">')
vo = json.load(open(W/'audio/options.json'))['options']
for k in 'ABCD':
    H.append(f'<div class="{"rec" if k == "B" else ""}"><h3>{k} · {esc(vo[k]["name"])}{" (recommended)" if k == "B" else ""}</h3><audio muted controls preload="none" src="media/voice-{k}.mp3"></audio></div>')
H.append('</div><h2>3 · Crop on you</h2><div class="opt">')
for k in '123':
    c = look['crops'][k]
    H.append(f'<div class="{"rec" if k == "1" else ""}"><h3>{k} · {esc(c["name"])}{" (recommended)" if k == "1" else ""}</h3><img src="media/crop-{k}-276.0.jpg"><img src="media/crop-{k}-331.0.jpg" style="margin-top:6px"></div>')
H.append('</div><h2>What I decided (overrule anything)</h2>'+decided)
H.append('<h2>Every clip and graphic, in order</h2><p class="muted">Each button plays that moment in the floating player with about 3 seconds either side. All gym footage is your real October 23 footage from the approved library, colour C.</p><div class="grid">')
items = [(u['film'][0], u['film'][1], u['id'], u['name'], f"Library {u['lib']}, from {u['start']:.1f}s, full height kept", u['id']) for u in m['assets']]
gp = {g['id']: g for g in VP['graphics']}
for g in m['graphics']:
    s = gp[g['id']]
    copy = f"{s['topic']} · {s['point']}" if g['kind'] == 'glass' else f"{s['eyebrow']} · {s['headline']} · " + ' / '.join(r[0] for r in s['rows'])
    items.append((g['a'], g['b'], g['id'], 'Key-Point Bar' if g['kind'] == 'glass' else 'Full-Screen List Card', copy, g['id']))
items.sort()
for a, b, gid, name, copy, img in items:
    H.append(f'<article class="card"><h3>{gid} · {esc(name)}</h3><img loading="lazy" src="media/{img}.jpg"><p class="copy">{mmss(a)}–{mmss(b)} · {esc(copy)}</p>'
             f'<button onclick="play({max(0, a-3):.2f},{min(dur, b+3):.2f},\'{gid} in context\')">Play it moving, in context</button>'
             f'<details><summary>What you say</summary><p class="copy"><b>Before:</b> {esc(said(a-4, a))}<br><b>Under it:</b> {esc(said(a, b))}<br><b>After:</b> {esc(said(b, b+4))}</p></details></article>')
H.append('</div><h2>Checks</h2>'+qa)
H.append('<h2>Reply once</h2><textarea id="reply">1 Colour: F\n2 Voice: B\n3 Crop: 1\n4 Set the seat picture: keep side view\nChanges, if any:\n</textarea><button onclick="copyReply()">Copy reply</button><span id="cs" class="muted"></span></main>'
         f'<script>const player=document.getElementById("player");let end={dur:.3f};function play(a,b,t){{player.pause();end=b;document.getElementById("dockTitle").innerHTML="<b>"+t+"</b>";'
         'const go=()=>{player.currentTime=a;player.play().catch(()=>{})};if(player.readyState>=1)go();else{player.addEventListener("loadedmetadata",go,{once:true});player.load()}}'
         'player.addEventListener("timeupdate",()=>{if(player.currentTime>=end)player.pause()});async function copyReply(){await navigator.clipboard.writeText(document.getElementById("reply").value);document.getElementById("cs").textContent=" Copied"}</script></body></html>')
(O/'index.html').write_text(''.join(H)); print('PAGE_READY')
