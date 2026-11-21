#!/usr/bin/env python3
"""RA-07 round 4 review page: the whole 9:16 with two labelled placeholders, the revision list with watch ranges, the two new
frame pairs for Dan's yes, what I decided, the checks. Writes round4/page/index.html; reads round4/page/checks.json if present.
Serve: python3 .claude/skills/_shared/review_server.py 8856 /Volumes/Extreme/_edit_work/ra07/round4/page"""
import html, json, os, shutil, subprocess
E = html.escape
R = "/Volumes/Extreme/_edit_work/ra07/round4"
os.chdir(R + "/page")
CK = json.load(open("checks.json")) if os.path.exists("checks.json") else {}


def btn(src, poster, label, start=0, on=False):
    return f'<button class="{"on" if on else ""}" data-src="{src}" data-poster="{poster}" data-t="{start}">{E(label)}</button>'


def verdict(path):
    try:
        t = open(path).read()
        v = [l for l in t.splitlines() if l.startswith("VERDICT")][-1]
        return v
    except Exception:
        return "VERDICT: not recorded"


vA = verdict(R + "/clipcheck/A0179.f8-43.review.md"); vB = verdict(R + "/clipcheck/A0179.f102-128.review.md")
vG = verdict(R + "/frames/framecheck/GC-end_v3.review.md"); vL = verdict(R + "/frames/framecheck/LP-end_v4b.review.md")
vH = verdict(R + "/clipcheck/I4bW_v1.f28-66.review.md")

rev = [
 ("0:00 to 0:30.1", "Unchanged. Frame for frame the first 30 seconds you approved.", None),
 ("0:36.5 to 0:38.6", "CHANGED: the broken-arm clip (the one from the \"How AI Real Abs\" ad) replaces the tweaked shoulder. He walks into the gym toward the squat racks in his cast and sling, then he is on the leg press. Round 3's shoulder-fix slot is gone.", 33.5),
 ("0:38.6 to 0:39.8", "NEW, placeholder: the gym is closed. The picture is the clip's first frame with a PLACEHOLDER label; the frames are below for your yes.", 35.0),
 ("0:39.8 to 0:41.0", "Home curls, after the closed gym. Same clip as before, its AI label stays on the wall beside his head.", 36.0),
 ("0:41.0 to 0:42.4", "NEW, placeholder: the leg press is out of order. Same man as the hack squat, same label treatment.", 37.5),
 ("0:42.4 to 0:44.0", "The hack squat, straight after it. The same take you approved, trimmed to its towel, handle and step-on.", 38.5),
 ("0:44.0 to 0:47.0", "Back next week, then the ending: unchanged from round 3.", 40.0),
]
rows = "".join(f"<tr><th>{E(t)}</th><td>{E(d)}</td></tr>" for t, d, _ in rev)

decided = [
 "Each fix follows its problem, as you asked: broken arm, then he is on the leg press; gym closed, then home curls; leg press out of order, then the hack squat; back next week. The squat rack no longer appears twice.",
 "The broken-arm clip is the finished clip from the \"How AI Real Abs\" ad, which you approved there. I use its walk-in (the first 1.2 s, cast and sling in view) and then its leg press shot. It was already played faster than real time there, so I did not speed it further or hold a frame.",
 "The middle of that clip, where he stops at the rack, did not pass the new quality check: his head does not really shake, he never faces the rack, and his hand pulls a smeared phone out of his pocket. So I cut around it. You will not see him shake his head or stand at the rack in this slot; the injury still reads from the cast and sling.",
 "Both pieces went through the motion check and a fresh independent reviewer again (the clip was approved before that rule existed): "+vA.replace("VERDICT: ","")+" for the walk-in, "+vB.replace("VERDICT: ","")+" for the leg press shot.",
 "Slot times follow your words: the closed gym starts on \"or you can't make it to the gym\", the curls take \"one day,\" and the pause, the leg press starts as \"equipment you need is broken\" begins, and the hack squat takes over as \"AI adjusts your plan in seconds\" plays. Every clip is at least 1.2 s.",
 "The gym-closed man is dressed like the home-curls man (black t-shirt and shorts, grey hair, beard) so the cut to his living room reads as one story. The leg press man is the hack squat man, same shirt, shorts and towel, in the same gym.",
 "The leg press out of order uses the plate-loaded machine type from the broken-arm clip, in this gym's white-wall room, with the sign hung from the backrest. The machine never moves in this clip. In its end frame he glances back at the camera over his shoulder with a tired look and his shoulder lifts in a small shrug. My first two versions (palm up) failed the independent check: one twisted his chest about 90 degrees over still hips, the other bent his arm across his spine. This one keeps hips, legs and arms as they were and passed.",
 "The hack squat now plays 1.6 s from 1.17 s of the take (before: 1.9 s from 0.9 s) because its slot is shorter. It still ends before the take's baked camera cut.",
 "Your voice, music and every other picture are the approved ones; I did not re-render any shot of you. Budget: you gave $20; round 3 used $10. This round spent $0 (frames are free on the Codex subscription). Motion for the two new clips is about $1 each plus retakes, only after you say yes.",
 "Still open from round 3 and not in this round (they need new frames of their own): the hack squat lift and the same-sheet clip. Say if you want them next.",
]
dec = "".join(f"<li>{E(x)}</li>" for x in decided)
cks = "".join(f"<li>{E(x)}</li>" for x in CK.get("lines", ["Checks are still running; this page updates."]))
ask = CK.get("ask", "")
reply = "1. Gym closed frames (G1): yes / changes:\n2. Leg press out of order frames (O1): yes / changes:\n3. Anything in the film to change (give the time):\n"

def pair(a, b, ca, cb):
    return (f'<div class="pair"><figure><a href="{a}" target="_blank"><img src="{a}" alt="start"></a><figcaption>{E(ca)}</figcaption></figure>'
            f'<figure><a href="{b}" target="_blank"><img src="{b}" alt="end"></a><figcaption>{E(cb)}</figcaption></figure></div>')

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fire Your Trainer AD R4</title><style>
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
table{{border-collapse:collapse;width:100%;font-size:14.5px;margin-top:10px}}th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:6px 12px 6px 0;width:24%;white-space:nowrap}}td{{padding:6px 0;vertical-align:top}}
tr+tr th,tr+tr td{{border-top:1px solid var(--line)}}
.play{{background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:10px 0 0;font-size:14px;cursor:pointer}}
textarea{{width:100%;height:150px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
</style></head><body><main>
<h1>Fire Your Trainer! · ad · round 4</h1>
<p class="sub">RA-07, the whole 9:16, 52.7 seconds, with the two new clips shown as labelled placeholders so you can see the order. The first 30 seconds are the ones you approved, unchanged.</p>
{f'<div class="ask">{E(ask)}</div>' if ask else ''}
<div class="player"><video id="v" controls preload="none" poster="poster_full.jpg" src="full.mp4"></video>
<div class="btns">{btn("full.mp4","poster_full.jpg","Whole ad (540p)",0,True)}{btn("run.mp4","poster_run.jpg","The changed run: 0:33.0 to 0:50.0")}{btn("ctx_A1.mp4","poster_A1.jpg","Broken arm in context")}{btn("ctx_G1.mp4","poster_G1.jpg","Gym closed in context (placeholder)")}{btn("ctx_O1.mp4","poster_O1.jpg","Leg press out of order in context (placeholder)")}</div>
<p class="sub" style="font-size:13px">Full quality file: Videos to Review/Fire Your Trainer AD R4 - whole 9x16 with placeholders.mp4</p></div>
<h2>What changed since round 3 (watch these)</h2>
<table>{rows}</table>
<h2>Two sets of frames for your yes</h2>
<section class="newpair"><h3>Gym closed (0:38.6 to 0:39.8, under "or you can't make it to the gym")</h3>
{pair("GC_start.jpg","GC_end.jpg","START: he walks up to the gym door, the CLOSED sign hanging in the glass","END: he stops, reads it, shoulders drop, both palms up")}
<table><tr><th>In the clip</th><td>He walks up to the glass door of the gym, reads the CLOSED sign and shrugs with both palms up. Then it cuts to the living-room curls.</td></tr>
<tr><th>Checked</th><td>Frame gate: every row passes. Fresh independent reviewer: {E(vG.replace("VERDICT: ",""))}.</td></tr>
<tr><th>If yes</th><td>I make the clip next (about $1, a retake if it needs one) and check the motion before you see it.</td></tr></table>
<button class="play" data-src="ctx_G1.mp4" data-poster="poster_G1.jpg">Play it in context (placeholder in the film, about 3 s of speech either side)</button></section>
<section class="newpair"><h3>Leg press out of order (0:41.0 to 0:42.4, under "or when the equipment you need is broken")</h3>
{pair("LP_start.jpg","LP_end.jpg","START: he walks up to the leg press, the OUT OF ORDER sign hanging from its backrest","END: he stops, glances back at the camera and shrugs")}
<table><tr><th>In the clip</th><td>He walks up to a plate-loaded leg press, sees the yellow OUT OF ORDER sign, glances back at the camera and shrugs. The machine does not move. Then the hack squat.</td></tr>
<tr><th>Checked</th><td>Frame gate: every row passes. Fresh independent reviewer: {E(vL.replace("VERDICT: ",""))}.</td></tr>
<tr><th>If yes</th><td>Same: I make the clip next and check the motion before you see it.</td></tr></table>
<button class="play" data-src="ctx_O1.mp4" data-poster="poster_O1.jpg">Play it in context (placeholder in the film, about 3 s of speech either side)</button></section>
<h2>What I decided (overrule anything)</h2><ul>{dec}</ul>
<h2>Checks on the exact file</h2><ul>{cks}</ul>
<h2>Your reply</h2>
<textarea id="r">{E(reply)}</textarea><br><button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button>
</main><script>
const v=document.getElementById('v');v.muted=false;
function go(src,poster){{v.poster=poster;v.src=src;v.play();document.querySelectorAll('.btns button').forEach(x=>x.classList.toggle('on',x.dataset.src===src));if(window.innerWidth<1500)v.scrollIntoView({{behavior:'smooth',block:'center'}})}}
document.querySelectorAll('.btns button,.play').forEach(b=>b.onclick=()=>go(b.dataset.src,b.dataset.poster));
</script></body></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash on the page"
open("index.html", "w").write(page)
print("index.html", len(page))
