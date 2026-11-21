import html
E = html.escape; R = "/Volumes/Expansion/_edit_work/RO-37/round4/r4/review"
FILM = "film/First Time At The Gym LFC R4 - REVIEW 540p.mp4"; HD = "film/First Time At The Gym LFC R4.mp4"
def sec(s):
    m, x = s.split(":"); return int(m) * 60 + float(x)
REV = [("0:08 to 0:20", "The picture cards are gone. Your captain's chair leg raises run behind you the whole way, sharp and on the left. That clip is not used anywhere else in the film."),
       ("0:10 to 0:13", "Hands-on-hips pause cut: 0.8 seconds out after \"more than 20 years\", so it goes straight into \"So why should you listen to me?\""),
       ("0:20 to 0:29", "The background you liked moved forward: it now starts at 0:20 instead of 0:21."),
       ("0:58 to 1:05", "The picture cards are gone. Your high cable work plays behind you instead, also not used elsewhere. The two AI clips on either side are unchanged."),
       ("2:42 to 2:45", "Pause cut: 0.6 seconds of silence out before \"On every rep\", leaving a natural beat between the sentences. The film is 1.4 seconds shorter from here on.")]
def rows():
    o = ""
    for w, n in REV:
        a = sec(w.split(" to ")[0]); o += f'<tr><td><button onclick="go({a})">{E(w)}</button></td><td>{E(n)}</td></tr>'
    return o
CHECKS = open(f"{R}/../../checks/page_checks.html").read()
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>First Time At The Gym R4</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1080px;margin:0 auto;padding:28px 16px}}
h1{{font-size:32px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:24px}}p,li,td{{color:var(--mute)}}section{{margin:26px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:16px}}
video{{width:100%;border-radius:10px;background:black}}.small{{font-size:14px}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}a{{color:var(--acc)}}
table{{width:100%;border-collapse:collapse}}td{{padding:8px 10px 8px 0;border-top:1px solid var(--line);vertical-align:top}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:6px 10px;cursor:pointer;font-size:14px;white-space:nowrap}}
@media(max-width:700px){{h1{{font-size:25px}}section{{padding:14px}}td{{display:block;border:0;padding:4px 0}}tr{{display:block;border-top:1px solid var(--line);padding:8px 0}}}}</style>
<main><h1>I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time <span class="small">LFC, round 4</span></h1>
<p class="notice"><b>The full film, 7:54.</b> Only the five spots below changed. You have not reviewed this round yet. Release: Fri Jan 1, 2027.</p>
<section><h2>The film</h2><video id="v" controls muted preload="metadata" playsinline src="{FILM}"></video><p class="small"><a href="{HD}">1080p</a></p></section>
<section><h2>What changed, with times</h2><p class="small">Each button jumps the player there. You do not need to watch the whole film.</p><table>{rows()}</table></section>
<section><h2>What I decided</h2><ul><li>Both new clips are machine or cable work, not barbells or dumbbells, so the opening matches what the film teaches. I passed on the rear delt fly because a stranger in a red hat filled the left side.</li>
<li>You stand on the right from 0:08 to 0:20 and from 0:58 to 1:05, so the footage is not hidden behind you.</li>
<li>You said everything else looks good, so I kept the gym bag clip at 1:04 and took the arm moments as accepted. They now sit at 0:05, 1:12 and 5:14.</li>
<li>Subtitles keep the same words, retimed to the new cuts.</li></ul></section>
<section><h2>Checks</h2><ul>{CHECKS}</ul></section></main>
<script>function go(t){{var v=document.getElementById('v');v.currentTime=t;v.scrollIntoView({{behavior:'smooth',block:'center'}});}}</script></html>"""
assert "—" not in page
open(f"{R}/index.html", "w").write(page); print("ok")
