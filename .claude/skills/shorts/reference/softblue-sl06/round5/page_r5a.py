#!/usr/bin/env python3
"""SL-06 round 5 review page (A shorts, leaner D, Seattle-only C opening); was round 4 stage 1 review page (shirtless gym intros, new thigh clips): the six AI flex intro frame pairs (no motion yet) each playable in place as stills,
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
DECISIONS = ["A and D: approve the new start and end frames, or name what to change. (B, C, E and F you already approved.)",
             "C's opening: the Seattle Children's clip now covers \"This takes about 10 seconds once you know what you are doing\", then SynergenX's pinch and inject as before."]
DECIDED = [
 "D: about 20 % narrower through the chest and lats and thinner arms than round 4, the same width at the waist as B and C. The end frame keeps the arms the same size; only the fists curl in and the grin grows.",
 "A: the waistband now sits a little below the navel, level and worn normally, like B to F. Pose, poster, vial and pointing move are unchanged from round 4.",
 "C's opening: one continuous Seattle Children's shot (6:59.5 to 7:02.4 in their video): he pinches the front of his thigh and the insulin syringe goes in. It fills the frame, colour matched to your footage, credited the whole time.",
 "Motion: the four approved intros (B, C, E, F) were sent to Google Flow. Every try failed on Flow's own audio step (8 of 8, two prompt styles, credits refunded). Flow offers a setting that returns silent videos instead; our edit uses your voice, never Veo's sound.",
]
CHECKS = ["New A and D pairs: frame gate PASS and a fresh independent reviewer PASS each. Caught before you saw them: D's first end frame swelled the arms back up (8 %), and A's first fix pulled the shorts up to the belly button. Both were redone.",
          "B, C, E, F frames are byte-identical to the ones you approved (hashes saved).",
          "Round 2's page stays up at http://127.0.0.1:8819/ until you finalize."]
REPLY = "1. A and D frames: approved / changes:\n   A:\n   D:\n2. C opening: approved / changes:\n\nOther notes:\n"
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 5 Zepbound Tips SFL R5</title>
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
<main><h1>Top 5 Zepbound Tips shorts / Round 5: A and D redone, C's opening</h1>
<p>Your round 4 notes: D slightly less muscular, like the other bodies; A's shorts back up to a normal height, like B; C's opening uses the Seattle Children's clip. B, C, E and F are approved and unchanged. Only A, D and C's opening are new here.</p>
<nav><a href="#decide">Your decisions (2)</a><a href="#intros">The six intros</a><a href="#c">C's new opening</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Pick any Play button: it plays here (at the right on a wide screen). Every player can be scrubbed.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="decide"><h2>Your decisions (2)</h2><ol>{"".join(f"<li>{E(x)}</li>" for x in DECISIONS)}</ol></section>
<section id="intros"><h2>The six AI flex intros: A and D are new; B, C, E, F approved</h2><p class="small">Click a frame to open it full size. "Play it in place" holds START, then END, over your real opening line, then cuts into the round-2 short so you see the title band come back on the first film frame.</p><div class="grid">{"".join(pairs)}</div></section>
<section id="c"><h2>C's new opening (0 to 13 s), then each YouTube clip</h2><p><button onclick="play('{copen}','Short C: new opening (intro, Seattle clip, SynergenX)',0)">Play C's new opening</button> 0 to 2.8 s the intro (stills here), 2.8 to 5.8 s Seattle Children's, 5.8 to 9.6 s SynergenX's pinch and inject, then you with Step 1.</p><div class="grid">{"".join(clips)}</div></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in DECIDED)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(REPLY)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button></p></section></main>
<script>function play(src,id,t){{const v=document.getElementById('pv');const go=()=>{{try{{v.currentTime=t||0}}catch(e){{}};v.play()}};document.getElementById('nowp').textContent=id;
if(v.getAttribute('src')!==src){{v.src=src;v.addEventListener('loadedmetadata',go,{{once:true}});v.load()}}else go();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{PG}/index.html", "w").write(page); print("page ok", len(page))
