#!/usr/bin/env python3
"""RA-07 round 6 stage 1 review page: the whole 9:16 with the gym-closed trim, the new home-curls clip and the phone clip as a labelled
placeholder; the phone START/END frames for Dan's yes; the timestamped revision list; what I decided; the checks.
Writes round6/page/index.html. Serve: python3 .claude/skills/_shared/review_server.py 8856 /Volumes/Extreme/_edit_work/ra07/round6/page"""
import html, json, os, shutil
from PIL import Image
E = html.escape
R = "/Volumes/Extreme/_edit_work/ra07/round6"
P = R + "/page"; os.makedirs(P, exist_ok=True)
cp = lambda s, d: shutil.copyfile(s, f"{P}/{d}")
cp(f"{R}/DRAFT - RA-07 round 6 - full film - REVIEW 540p.mp4", "full.mp4")
cp(f"{R}/run - REVIEW 540p.mp4", "run.mp4")
for k in ("G1", "M1", "O1"):
    cp(f"{R}/context/{k}-context - REVIEW 540p.mp4", f"ctx_{k}.mp4"); cp(f"{R}/context/{k}-context - REVIEW 540p.jpg", f"poster_{k}.jpg")
    cp(f"{R}/stills/{k}.jpg", f"still_{k}.jpg")
cp(f"{R}/context/G1-context - REVIEW 540p.jpg", "poster_full.jpg"); cp(f"{R}/context/M1-context - REVIEW 540p.jpg", "poster_run.jpg")
for src, dst in ((f"{R}/frames/PH-start.png", "ph_start.jpg"), (f"{R}/frames/PH-end_v1a.png", "ph_end.jpg")):
    Image.open(src).convert("RGB").save(f"{P}/{dst}", quality=92)
CK = json.load(open(f"{R}/page_checks.json"))
CB = json.load(open("/Volumes/Extreme/_edit_work/ra07/beats_r6.json"))
cards = {c["name"]: c["beat"] for c in CB["cards"]}
mmss = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"
G, M, O = cards["G1"], cards["M1"], cards["O1"]

rev = [
 (f"0:00 to {mmss(G[0])}", "Unchanged. The first 30 seconds are frame for frame the ones you approved, and the broken-arm clip is the same."),
 (f"{mmss(G[0])} to {mmss(G[1])}", f"CHANGED (your note): gym closed is trimmed from 1.27 s to {G[1]-G[0]:.2f} s. It now ends as soon as his arms have opened into the shrug; the standing and looking at the door is gone. Watch {mmss(G[0]-2)} to {mmss(M[1]+0.5)}."),
 (f"{mmss(M[0])} to {mmss(M[1])}", f"CHANGED: the home curls now start 0.8 s earlier and fill the freed time ({M[1]-M[0]:.1f} s). It is a different curls clip: the old one failed its quality review on the longer window (his hand melted into a see-through blob for a few frames, twice). The new one is a grey-haired man in his 40s curling in his home garage gym. Same watch range."),
 (f"{mmss(O[0])} to {mmss(O[1])}", "PLACEHOLDER (your note): the new phone clip goes here. For now it shows the new start frame with a label on the floor. Its start and end frames are below for your yes; the motion comes after it."),
 (f"{mmss(O[1])} to 0:52.7", "Unchanged: the hack squat, back next week, the ending and the button. The sound is the approved mix, sample for sample, and the ad is still 52.7 s."),
]
rows = "".join(f"<tr><th>{E(t)}</th><td>{E(d)}</td></tr>" for t, d in rev)
dec = "".join(f"<li>{E(x)}</li>" for x in CK["decided"])
cks = "".join(f"<li>{E(x)}</li>" for x in CK["lines"])
reply = "1. Phone clip frames: yes / change (what):\n2. Gym closed trim and the new home curls: OK / change (what):\n3. Anything else in the film (give the time):\n"

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fire Your Trainer AD R6</title><style>
:root{{--bg:#0d1420;--panel:#152033;--ink:#eef4fb;--mute:#9db0c7;--line:#27384f;--acc:#68c5ff;--warn:#ffcf6b}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:24px 16px 80px}}@media(min-width:1500px){{main{{margin-right:460px}}}}
h1{{font-size:28px;margin:0 0 6px}}h2{{font-size:21px;margin:34px 0 10px;border-top:1px solid var(--line);padding-top:22px}}h3{{font-size:17px;margin:0 0 10px}}
.sub{{color:var(--mute)}}ol,ul{{padding-left:22px}}li{{margin:6px 0}}a{{color:var(--acc)}}
.ask{{background:#2a2410;border:1px solid var(--warn);border-radius:12px;padding:12px 16px;margin:14px 0}}
.player{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}
@media(min-width:1500px){{.player{{position:fixed;right:18px;top:18px;width:420px}}}}
video{{width:100%;max-height:72vh;border-radius:10px;background:#000}}
.btns button{{display:block;width:100%;text-align:left;background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:6px 0 0;font-size:14px;cursor:pointer}}
.btns button.on{{border-color:var(--acc);color:var(--acc)}}
.newpair{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:18px}}.pair{{display:flex;gap:10px;max-width:760px}}.pair figure{{margin:0;flex:1;min-width:0}}.pair img{{width:100%;border-radius:8px}}
figcaption{{font-size:12.5px;color:var(--mute);text-align:center}}
table{{border-collapse:collapse;width:100%;font-size:14.5px;margin-top:10px}}th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:6px 12px 6px 0;width:22%;white-space:nowrap}}td{{padding:6px 0;vertical-align:top}}
tr+tr th,tr+tr td{{border-top:1px solid var(--line)}}
.play{{background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:10px 0 0;font-size:14px;cursor:pointer}}
textarea{{width:100%;height:120px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
@media(max-width:600px){{th{{white-space:normal;width:30%}}}}
</style></head><body><main>
<h1>Fire Your Trainer! · ad · round 6</h1>
<p class="sub">RA-07, the whole 9:16, 52.7 seconds, with the gym-closed trim in and the new phone clip as a labelled placeholder. A review copy: nothing is uploaded or running.</p>
<div class="ask">{E(CK['ask'])}</div>
<div class="player"><video id="v" controls preload="none" poster="poster_full.jpg" src="full.mp4"></video>
<div class="btns"><button class="on" data-src="full.mp4" data-poster="poster_full.jpg">Whole ad (540p)</button><button data-src="run.mp4" data-poster="poster_run.jpg">The changed run: 0:33.0 to 0:50.0</button><button data-src="ctx_G1.mp4" data-poster="poster_G1.jpg">Gym closed (trimmed) in context</button><button data-src="ctx_M1.mp4" data-poster="poster_M1.jpg">Home curls in context</button><button data-src="ctx_O1.mp4" data-poster="poster_O1.jpg">Phone clip slot (placeholder) in context</button></div>
<p class="sub" style="font-size:13px">Full quality file: Videos to Review/Fire Your Trainer AD R6 - whole 9x16 (phone placeholder).mp4</p></div>
<h2>What changed since round 5 (watch these)</h2>
<table>{rows}</table>
<h2>The new phone clip: start and end frames (your yes, then motion)</h2>
<section class="newpair"><h3>Out of order, phone out ({mmss(O[0])} to {mmss(O[1])}, 1.4 s, under "or when the equipment you need is broken.")</h3>
<div class="pair"><figure><img src="ph_start.jpg" alt="start frame"><figcaption>START: he stands beside the leg press, reading the OUT OF ORDER sign, hands empty</figcaption></figure>
<figure><img src="ph_end.jpg" alt="end frame"><figcaption>END: same spot, same feet; he has pulled his phone out and looks at it</figcaption></figure></div>
<table><tr><th>The motion</th><td>He reads the sign, his right hand goes into his right shorts pocket, comes out with the phone and lifts it in front of his chest; he looks down at it. His feet stay planted (no walking, so no sliding feet). Then the hack squat, as before.</td></tr>
<tr><th>Why this framing</th><td>He is turned three-quarters toward the camera so the phone and the hand are visible. The screen faces him, so only the plain back of the phone shows: no made-up screen text.</td></tr>
<tr><th>Checked</th><td>Frame gate: every row passed (feet 0 px, machine and sign 0 px, arm length the same, the phone fully in his hand). Fresh independent reviewer: {E(CK['ph_verdict'])}. One phone, straight edges, a thumb and four fingers.</td></tr>
<tr><th>Cost</th><td>Frames are free (Codex subscription). Motion is about $1 a take; I expect one to three takes. $12 of the $20 is spent so far.</td></tr></table>
<button class="play" data-src="ctx_O1.mp4" data-poster="poster_O1.jpg">See the slot in context</button></section>
<section class="newpair"><h3>Gym closed, trimmed ({mmss(G[0])} to {mmss(G[1])})</h3>
<div class="pair"><figure><img src="still_G1.jpg" alt="gym closed"><figcaption>The last part of the trimmed clip</figcaption></figure><figure><img src="still_M1.jpg" alt="home curls"><figcaption>The new home curls that follow it</figcaption></figure></div>
<table><tr><th>Gym closed</th><td>{E(CK['g1_note'])}</td></tr>
<tr><th>Home curls</th><td>{E(CK['m1_note'])}</td></tr></table>
<button class="play" data-src="ctx_G1.mp4" data-poster="poster_G1.jpg">Play both in context</button></section>
<h2>What I decided (overrule anything)</h2><ul>{dec}</ul>
<h2>Checks</h2><ul>{cks}</ul>
<h2>Your reply</h2>
<textarea id="r">{E(reply)}</textarea><br><button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button>
</main><script>
const v=document.getElementById('v');
function go(src,poster){{v.poster=poster;v.src=src;v.play();document.querySelectorAll('.btns button').forEach(x=>x.classList.toggle('on',x.dataset.src===src));if(window.innerWidth<1500)v.scrollIntoView({{behavior:'smooth',block:'center'}})}}
document.querySelectorAll('.btns button,.play').forEach(b=>b.onclick=()=>go(b.dataset.src,b.dataset.poster));
</script></body></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash on the page"
open(f"{P}/index.html", "w").write(page)
print("index.html", len(page))
