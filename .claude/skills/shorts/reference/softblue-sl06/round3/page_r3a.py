#!/usr/bin/env python3
"""SL-06 round 3, stage 1 review page: the six AI flex intro frame pairs (no motion yet) each playable in place as stills,
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
DECISIONS = ["The six intro frame pairs: approve them, or name what to change on any one. After your yes I make the motion on your Google Flow subscription, check every take, and build all six shorts.",
             "Short C's three YouTube thigh-injection clips and their credits (Nurse Scott and a clinical training video in the montage, then Karli Sine's pinch and inject)."]
DECIDED = [
 "One look for all six intros: you in your black tank and glasses, as in the film each one cuts into, in front of a plain light-grey wall with a white poster in big black letters.",
 "Posters say your exact words in the case you dictated them (\"Start at 1 mg, not 2.5 mg\"). They are props in the scene, not our graphics, so they are not title-cased.",
 "The flexing hand holds the vial and the other hand points at the poster, on all five one-arm shorts (your words for A; E and F follow it). On E and F the flexed arm is nearer the camera, as you said \"in the foreground\".",
 "Start frame: the finger is just short of the poster. End frame: the fingertip lands on the poster's margin and the flex tightens. D: the double biceps squeezes and the grin grows.",
 "The vial label says only \"Zepbound\", with no made-up logo. The calendar on D is a real 30-day month starting on a Sunday, with only the Thursdays (5, 12, 19, 26) circled.",
 "The title band comes off during the intro on all six and returns on the first film frame (your words for D, applied to all). Captions, the disclaimer and the AbsByAI.com mark stay.",
 "The AI-GENERATED label sits on the bare wall at the top right (D: top centre, between calendar and poster), clear of face, body and poster.",
 "C: the montage of two real thigh injections covers \"This takes about 10 seconds once you know what you are doing\" (replacing the vial-drawing clip); Karli Sine's pinch and inject covers \"Inject into your thigh on the outer front part, right around the middle\"; then you on camera with Step 1 as before.",
 "YouTube has almost no Zepbound-vial injections into the thigh with a needle: the vial tutorials inject the belly, and the thigh ones use the pen. These three are real thigh injections with an insulin syringe (Karli's is semaglutide, the other two are unlabelled); no drug name shows on screen.",
 "Two of C's clips sit in a card instead of filling the frame. The clinical clip: a full-frame crop shows only the gown and the glove, not the thigh. Karli's: her injection is low in her frame, under our captions, with her own captions on her chest, so the card is cropped to her thigh and hands.",
 "All three clips are colour matched to your footage (the clinical clip lifted; Karli's brought down a little). Each credit stays on for its whole clip.",
 "E keeps its staircase ending from round 2.",
 "Motion next: Veo 3.1 Fast on your Google Flow subscription (no API spend), about 3 to 4.6 s per intro to match each opening line. Every take gets the motion check and a fresh independent reviewer before you see it.",
]
CHECKS = ["Frame gate PASS on all six pairs, and a fresh independent reviewer PASS on each (B's first pair failed on fake-looking skin specks and was regenerated before you saw it).",
          "Every poster letter checked in both frames by the reviewers; the poster does not move between START and END.",
          "Likeness checked against four real close-ups of your face; body checked against a real photo (lean, not bulky).",
          "These are stills. The 'in place' players hold the start frame, then the end frame, over your real opening line, then cut into the round-2 film so you can judge the band coming back.",
          "Round 2's page stays up at http://127.0.0.1:8819/ until you finalize."]
REPLY = "1. Intro frames: approved / changes:\n   D:\n   A:\n   B:\n   C:\n   E:\n   F:\n2. C YouTube clips and credits: approved / changes:\n\nOther notes:\n"
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFL R3</title>
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
<main><h1>Top 5 Zepbound Tips shorts / Round 3, stage 1: AI flex intros and C's YouTube clips</h1>
<p>Your round 2 notes asked for an AI flex intro on all six and real thigh-injection clips in C. Here are the six intro start and end frames (no motion yet: frames come first) and C's new opening. Everything else in the six shorts is as you approved in round 2.</p>
<nav><a href="#decide">Your decisions (2)</a><a href="#intros">The six intros</a><a href="#c">C's new opening</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Pick any Play button: it plays here (at the right on a wide screen). Every player can be scrubbed.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="decide"><h2>Your decisions (2)</h2><ol>{"".join(f"<li>{E(x)}</li>" for x in DECISIONS)}</ol></section>
<section id="intros"><h2>The six AI flex intros: start and end frames</h2><p class="small">Click a frame to open it full size. "Play it in place" holds START, then END, over your real opening line, then cuts into the round-2 short so you see the title band come back on the first film frame.</p><div class="grid">{"".join(pairs)}</div></section>
<section id="c"><h2>C's new opening (0 to 13 s), then each YouTube clip</h2><p><button onclick="play('{copen}','Short C: new opening (intro as stills, montage, Karli Sine)',0)">Play C's new opening</button> 0 to 2.8 s the intro (stills here), 2.8 to 5.8 s the montage, 5.8 to 9.6 s Karli Sine, then you with Step 1. The Step 1 bar is left out of this preview; in the build it sits over the lower part of Karli's card, below the injection.</p><div class="grid">{"".join(clips)}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in DECIDED)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button></p></section></main>
<script>function play(src,id,t){{const v=document.getElementById('pv');const go=()=>{{try{{v.currentTime=t||0}}catch(e){{}};v.play()}};document.getElementById('nowp').textContent=id;
if(v.getAttribute('src')!==src){{v.src=src;v.addEventListener('loadedmetadata',go,{{once:true}});v.load()}}else go();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{PG}/index.html", "w").write(page); print("page ok", len(page))
