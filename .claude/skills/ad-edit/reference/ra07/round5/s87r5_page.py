#!/usr/bin/env python3
"""RA-07 round 5 review page: the whole 9:16 with both new clips moving, the timestamped revision list, what I decided, the checks.
Writes round5/page/index.html (and copies the review videos and stills in). Serve: python3 .claude/skills/_shared/review_server.py 8856 /Volumes/Extreme/_edit_work/ra07/round5/page"""
import html, json, os, re, shutil
E = html.escape
R = "/Volumes/Extreme/_edit_work/ra07/round5"
P = R + "/page"; os.makedirs(P, exist_ok=True)
cp = lambda s, d: shutil.copyfile(s, f"{P}/{d}")
cp(f"{R}/DRAFT - RA-07 round 5 - full film - REVIEW 540p.mp4", "full.mp4")
cp(f"{R}/run - REVIEW 540p.mp4", "run.mp4")
for k in ("G1", "O1"):
    cp(f"{R}/context/{k}-context - REVIEW 540p.mp4", f"ctx_{k}.mp4"); cp(f"{R}/context/{k}-context - REVIEW 540p.jpg", f"poster_{k}.jpg")
    cp(f"{R}/stills/{k}.jpg", f"still_{k}.jpg")
cp(f"{R}/context/G1-context - REVIEW 540p.jpg", "poster_full.jpg"); cp(f"{R}/context/O1-context - REVIEW 540p.jpg", "poster_run.jpg")
CK = json.load(open(f"{R}/page_checks.json"))


def verdict(path):
    try:
        return [l for l in open(path).read().splitlines() if l.startswith("VERDICT")][-1].replace("VERDICT: ", "").replace("VERDICT ", "")
    except Exception:
        return "not recorded"


MC = R + "/motion/clipcheck"
vG = verdict(MC + "/G1_v1.f59-96.review.md"); vO = verdict(MC + "/O1_v1.f55-96.review.md")
vR = verdict(R + "/deliver/ROUND-5-REVIEW.md")

rev = [
 ("0:00 to 0:37.7", "Unchanged. The first 30 seconds are the ones you approved, frame for frame, and everything after them up to 0:37.7 is the same as the round 4 film."),
 ("0:38.5 to 0:39.8", "CHANGED: gym closed is now a real clip, no longer a placeholder. He is at the glass door under the CLOSED sign, opens both hands palm up and shrugs. Watch 0:37.5 to 0:41.0 to see it between the broken-arm clip and the home curls."),
 ("0:39.8 to 0:41.0", "Unchanged: the home curls."),
 ("0:41.0 to 0:42.4", "CHANGED: leg press out of order is now a real clip. He stands at the leg press with the OUT OF ORDER sign, turns his head and glances back over his shoulder with a tired look. Watch 0:40.0 to 0:43.5 to see it between the curls and the hack squat."),
 ("0:42.4 to 0:52.7", "Unchanged: the hack squat, back next week, the ending and the button. The sound is the approved mix, sample for sample."),
]
rows = "".join(f"<tr><th>{E(t)}</th><td>{E(d)}</td></tr>" for t, d in rev)
dec = "".join(f"<li>{E(x)}</li>" for x in CK["decided"])
cks = "".join(f"<li>{E(x)}</li>" for x in CK["lines"])
reply = "1. Anything in the film to change (give the time):\n2. Next for the 16:9 after you approve this 9:16: yes / hold:\n3. Hack squat lift and the same-sheet clip next round? yes / no:\n"

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fire Your Trainer AD R5</title><style>
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
.newpair{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:18px}}.pair{{display:flex;gap:10px;max-width:720px}}.pair figure{{margin:0;flex:1}}.pair img{{width:100%;border-radius:8px}}
figcaption{{font-size:12.5px;color:var(--mute);text-align:center}}
table{{border-collapse:collapse;width:100%;font-size:14.5px;margin-top:10px}}th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:6px 12px 6px 0;width:22%;white-space:nowrap}}td{{padding:6px 0;vertical-align:top}}
tr+tr th,tr+tr td{{border-top:1px solid var(--line)}}
.play{{background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:10px 0 0;font-size:14px;cursor:pointer}}
textarea{{width:100%;height:130px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
</style></head><body><main>
<h1>Fire Your Trainer! · ad · round 5</h1>
<p class="sub">RA-07, the whole 9:16, 52.7 seconds, with both new clips moving. This is a review copy: nothing is uploaded or running until you approve it.</p>
<div class="ask">{E(CK['ask'])}</div>
<div class="player"><video id="v" controls preload="none" poster="poster_full.jpg" src="full.mp4"></video>
<div class="btns"><button class="on" data-src="full.mp4" data-poster="poster_full.jpg">Whole ad (540p)</button><button data-src="run.mp4" data-poster="poster_run.jpg">The changed run: 0:33.0 to 0:50.0</button><button data-src="ctx_G1.mp4" data-poster="poster_G1.jpg">Gym closed in context (0:35.5 to 0:42.8)</button><button data-src="ctx_O1.mp4" data-poster="poster_O1.jpg">Leg press out of order in context (0:38.0 to 0:45.4)</button></div>
<p class="sub" style="font-size:13px">Full quality file: Videos to Review/Fire Your Trainer AD R5 - whole 9x16.mp4</p></div>
<h2>What changed since round 4 (watch these)</h2>
<table>{rows}</table>
<h2>The two new clips</h2>
<section class="newpair"><h3>Gym closed (0:38.5 to 0:39.8, under "or you can't make it to the gym")</h3>
<div class="pair"><figure><img src="still_G1.jpg" alt="gym closed"><figcaption>A frame from the clip, with its AI label</figcaption></figure></div>
<table><tr><th>In the clip</th><td>He is at the glass door of the gym, the red and white CLOSED sign hanging in the glass. Both palms open and up, shoulders drop, head tilts, a resigned look. Then the home curls.</td></tr>
<tr><th>Checked</th><td>Motion tracker on the frames used: pass. Fresh independent reviewer: {E(vG)}. Both feet stay planted (largest drift of any part of a shoe 2.8 px on a 720 px wide take), hands checked on 11 frames, no baked cut.</td></tr></table>
<button class="play" data-src="ctx_G1.mp4" data-poster="poster_G1.jpg">Play it in context</button></section>
<section class="newpair"><h3>Leg press out of order (0:41.0 to 0:42.4, under "or when the equipment you need is broken")</h3>
<div class="pair"><figure><img src="still_O1.jpg" alt="leg press out of order"><figcaption>A frame from the clip, with its AI label</figcaption></figure></div>
<table><tr><th>In the clip</th><td>He stands at the plate-loaded leg press with the yellow OUT OF ORDER sign on its backrest, turns his head and glances back over his shoulder with a tired look while his shoulder lifts. The machine does not move. Then the hack squat.</td></tr>
<tr><th>Checked</th><td>Motion tracker on the frames used: pass. Fresh independent reviewer: {E(vO)}. Both shoes stay on the floor (largest drift 1.0 px), the towel and the sign hold still, the face is the same man throughout.</td></tr></table>
<button class="play" data-src="ctx_O1.mp4" data-poster="poster_O1.jpg">Play it in context</button></section>
<h2>What I decided (overrule anything)</h2><ul>{dec}</ul>
<h2>Checks on the exact file</h2><ul>{cks}<li>Independent review of the finished film (fresh reviewer, never shown my notes): {E(vR)}.</li></ul>
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
