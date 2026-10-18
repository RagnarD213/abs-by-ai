#!/usr/bin/env python3
"""SL-06 round 4, stage 1 review page (shirtless gym intros, new thigh clips): the six AI flex intro frame pairs (no motion yet) each playable in place as stills,
and short C's new opening with the three credited YouTube thigh-injection clips. Refuses any pair without gate + reviewer PASS.
  python3 page_r3a.py ; review_server.py 8821 /Volumes/Extreme/_edit_work/sl06/round3/page"""
import html, json, os, shutil, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
from gate import require_pass
E = html.escape; R = "/Volumes/Extreme/_edit_work/sl06/round3"; PG = R + "/page"; AI = R + "/aiframes"
for d in ("ai", "media"): os.makedirs(f"{PG}/{d}", exist_ok=True)
def cp(src, dst):
    if not os.path.exists(f"{PG}/{dst}") or os.path.getsize(f"{PG}/{dst}") != os.path.getsize(src): shutil.copyfile(src, f"{PG}/{dst}")
    return dst
SH = [  # short, title, the line the intro covers, poster, the motion
 ("D", "Inject On Thursday Evening", "Here's why Thursday evening is the best time to inject Zepbound. (0 to 3.3 s)", "Inject Zepbound Thursday evening", "Front double biceps, a tiny Zepbound vial pinched in each hand; the calendar with every Thursday circled on one side, the poster on the other. Motion: he squeezes the pose a little harder and grins."),
 ("A", "Start At 1 mg, Not 2.5 mg", "Here's why you should start Zepbound at 1 milligram to avoid the side effects. (0 to 4.1 s)", "Start at 1 mg, not 2.5 mg", "One arm flexed holding the vial between thumb and forefinger; the other hand points, then its fingertip lands on the poster as the flex tightens."),
 ("B", "Use A Needle And Vial, Not The Pen", "Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead. (0 to 4.6 s)", "Use a needle, not a KwikPen", "Same as A: flex with the vial, the other hand moves to the poster."),
 ("C", "How To Inject In 10 Seconds", "Here's how to inject Zepbound with a needle, step by step. (0 to 2.8 s)", "How to inject Zepbound", "Same as A. The YouTube injection clips follow it (below)."),
 ("E", "How To Come Off Without Regaining It", "Here's how to come off Zepbound without gaining the fat back. (0 to 3.2 s)", "Come off Zepbound without regaining fat", "The flexed arm is in the foreground, nearer the camera; the other hand reaches back and lands on the poster."),
 ("F", "How Much Protein You Need", "Zepbound reduces your appetite, so eating less calories is easier. (0 to 2.5 s, replaces the sliced-chicken clip)", "How much protein do you need on a GLP-1?", "Same as E: foreground flex with the vial, the other hand lands on the poster."),
]
pairs = []
for S, title, line, poster, motion in SH:
    st, en = f"{AI}/{S}_start.jpg", f"{AI}/{S}_end.jpg"; require_pass(st, en)
    a1, a2 = cp(st, f"ai/{S}_start.jpg"), cp(en, f"ai/{S}_end.jpg"); ctx = cp(f"{R}/preview/{S}_intro_context.mp4", f"media/{S}_intro_in_place.mp4")
    pairs.append(f"""<article id="p{S}"><h3>{S}: {E(title)}</h3><div class="pair"><div><a href="{a1}" target="_blank"><img loading="lazy" src="{a1}"></a><span>START</span></div>
<div><a href="{a2}" target="_blank"><img loading="lazy" src="{a2}"></a><span>END</span></div></div>
<button onclick="play('{ctx}',{E(json.dumps('Short ' + S + ': intro in place (stills), then the film'))},0)">Play it in place (stills, your real audio)</button>
<div class="copy"><b>Covers:</b> {E(line)}<br><b>Poster:</b> {E(poster)}<br><b>Motion after your yes:</b> {E(motion)}</div></article>""")
src = json.load(open(f"{R}/clips/youtube_sources.json"))
copen = cp(f"{R}/preview/C_open_context.mp4", "media/C_new_opening.mp4")
clips = []
for c in src:
    v = cp(f"{R}/{c['file']}", f"media/{c['id']}.mp4")
    clips.append(f"""<article><video src="{v}" controls muted playsinline preload="metadata"></video><h3>{E(c['credit'].replace('Video: ', ''))}</h3>
<div class="copy">C {c['output_s'][0]:.2f} to {c['output_s'][1]:.2f} s. {E(c['what'])}.<br>Source: <a href="{E(c['url'])}" target="_blank">{E(c['title'])}</a>, {E(c['channel'])}, {E(c['t0'])} to {E(c['t1'])}.<br>Credit shown the whole clip, lower right: <b>{E(c['credit'])}</b></div></article>""")
DECISIONS = ["The six intro frame pairs (shirtless, real gym, printed gym poster): approve them, or name what to change on any one. After your yes I make the motion on your Google Flow subscription, check every take, and build all six shorts.",
             "Short C's three new YouTube thigh-injection clips and their credits: a University of Iowa nurse and a Seattle Children's self-injection in the montage, then SynergenX's pinch and inject."]
DECIDED = [
 "One look for all six intros: you shirtless in black gym shorts and your glasses, in the same real gym (power rack, cable machine, dumbbell rack, rubber floor), lit brighter than the room so you read well on a phone.",
 "The posters are one printed series: navy with a yellow band and border, your exact words in white, a small dumbbell icon, no other writing. Your dictated wording and case are kept (\"Start at 1 mg, not 2.5 mg\").",
 "Poses, the tiny vial, the pointing hand and the timing are kept from round 3. D keeps the double biceps with the Thursday calendar (a real 30-day month, only 5, 12, 19 and 26 circled).",
 "In a real gym the poster is on the wall behind you, so the finger cannot touch it for real. Start: the finger points from below the poster. End: the hand has lifted so the fingertip sits in front of the poster's bottom corner. The motion will be made as \"he points at the poster\".",
 "Your body matches your real shirtless studio photos (lean and shredded, not bulked up); the reviewers checked it against three of them, and your face against four close-ups.",
 "The image model gives skin a wormy texture up close. I smoothed only that fine texture on every frame, so the skin reads natural; shape, abs and shading are untouched.",
 "The title band comes off during the intro on all six and returns on the first film frame. Captions, the disclaimer and the AbsByAI.com mark stay.",
 "The AI-GENERATED label sits on the wall at the top right (D: top centre, above the calendar and poster), clear of face, body and poster.",
 "C: the montage covers \"This takes about 10 seconds once you know what you are doing\": a gloved nurse injecting the front of a patient's thigh (the doctor-style shot you asked for), then a man pinching the front of his own thigh with an insulin syringe. SynergenX's pinch and inject covers \"Inject into your thigh on the outer front part, right around the middle\".",
 "All three C clips fill the frame (no cards this time), each placed on the needle and the pinch. All three are colour matched to your footage (the nurse clip toned down, the SynergenX clip a little less saturated). Each credit stays on for its whole clip. No drug name shows on screen (two are hormone shots; same syringe and technique).",
 "E keeps its staircase ending from round 2.",
]
CHECKS = ["Frame gate PASS on all six pairs, and a fresh independent reviewer PASS on each. Caught and fixed before you saw them: F's first pair (the pointing hand barely moved, and its thumb melted), and E's end frame twice (a leftover fingertip beside the vial, then a small step in the poster border where the background was matched).",
          "Every poster letter checked in both frames by the reviewers; the poster and the gym do not move between START and END.",
          "C's clips: each one checked on a timestamped sheet in HD for what it really shows (front of the thigh, needle visible, no burned captions). The rejected round 3 clips and the belly-only and pen videos were left out.",
          "These are stills. The 'in place' players hold the start frame, then the end frame, over your real opening line, then cut into the round-2 film so you can judge the band coming back.",
          "Round 2's page stays up at http://127.0.0.1:8819/ until you finalize."]
REPLY = "1. Intro frames: approved / changes:\n   D:\n   A:\n   B:\n   C:\n   E:\n   F:\n2. C YouTube clips and credits: approved / changes:\n\nOther notes:\n"
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFL R4</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--text:#edf5ff;--muted:#bdd0e4}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px system-ui,-apple-system,sans-serif;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}
h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px;margin-top:0}}h3{{font-size:17px;margin:10px 0 4px}}p,li{{color:var(--muted)}}li b,p b{{color:var(--text)}}
section{{margin:28px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}
article{{min-width:0;background:#081626;padding:12px;border-radius:12px}}img,video{{width:100%;border-radius:10px;background:#000;display:block}}a{{color:#8cd6ff}}.small{{font-size:14px;color:#9fb7cf;font-weight:400}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.pair div{{position:relative}}.pair span{{position:absolute;left:8px;top:8px;background:#000a;padding:2px 8px;border-radius:8px;font-size:12px;font-weight:700}}
textarea{{width:100%;box-sizing:border-box;min-height:320px;background:#071221;color:white;padding:14px;font:15px ui-monospace,monospace;border:1px solid #47607b;border-radius:10px}}
#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px;text-align:center}}#dock video{{max-height:60vh;width:auto;max-width:100%;margin:auto}}
@media(min-width:1500px){{body{{padding-right:min(30vw,520px)}}#dock{{position:fixed;top:16px;right:16px;width:calc(min(30vw,520px) - 40px);max-height:calc(100vh - 32px);box-sizing:border-box;margin:0;box-shadow:0 8px 40px #000a}}#dock video{{max-height:calc(100vh - 110px)}}}}
@media(max-width:1499px){{#dock video{{max-height:42vh}}}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:7px 11px;cursor:pointer;font-size:14px;margin:6px 4px 0 0}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}}}@media(max-width:560px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<main><h1>Top 5 Zepbound Tips shorts / Round 4: shirtless gym intros and new thigh clips</h1>
<p>Your round 3 notes: all six intros regenerated with you shirtless in a real gym and a real-looking poster, and better thigh-injection clips for C (a clinician, or the front of the thigh). Frames come first (no motion yet). Everything else in the six shorts is as you approved in round 2.</p>
<nav><a href="#decide">Your decisions (2)</a><a href="#intros">The six intros</a><a href="#c">C's new opening</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Pick any Play button: it plays here (at the right on a wide screen). Every player can be scrubbed.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="decide"><h2>Your decisions (2)</h2><ol>{"".join(f"<li>{E(x)}</li>" for x in DECISIONS)}</ol></section>
<section id="intros"><h2>The six AI flex intros: start and end frames</h2><p class="small">Click a frame to open it full size. "Play it in place" holds START, then END, over your real opening line, then cuts into the round-2 short so you see the title band come back on the first film frame.</p><div class="grid">{"".join(pairs)}</div></section>
<section id="c"><h2>C's new opening (0 to 13 s), then each YouTube clip</h2><p><button onclick="play('{copen}','Short C: new opening (intro as stills, montage, SynergenX)',0)">Play C's new opening</button> 0 to 2.8 s the intro (stills here), 2.8 to 5.8 s the montage (nurse, then self-injection), 5.8 to 9.6 s SynergenX's pinch and inject, then you with Step 1.</p><div class="grid">{"".join(clips)}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in DECIDED)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button></p></section></main>
<script>function play(src,id,t){{const v=document.getElementById('pv');const go=()=>{{try{{v.currentTime=t||0}}catch(e){{}};v.play()}};document.getElementById('nowp').textContent=id;
if(v.getAttribute('src')!==src){{v.src=src;v.addEventListener('loadedmetadata',go,{{once:true}});v.load()}}else go();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{PG}/index.html", "w").write(page); print("page ok", len(page))
