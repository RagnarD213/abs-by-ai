"""RO-07 round 1 review page (standard layout: decisions, first minute, AI frames, look, What I decided, every item three
per row, one docked player, one reply box). Writes round1/index.html. Serve with _shared/review_server.py PORT round1."""
import json, os, html, shutil
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro07"; O = f"{W}/round1"
rows = json.load(open(f"{O}/stills.json")); num = json.load(open(f"{O}/look/numbers.json"))
S = json.load(open(f"{W}/shots.json")); TOTAL = S[-1]["out_f1"]/(30000/1001)
ctx = {f.split("-context")[0] for f in os.listdir(f"{O}/context") if f.endswith("REVIEW 540p.mp4") and not f.startswith("._")} if os.path.isdir(f"{O}/context") else set()
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
e = html.escape
os.makedirs(f"{O}/frames", exist_ok=True)
for k in ("A1", "A2", "A3"):
    for se in ("start", "end"):
        Image.open(f"{W}/aiframes/{k}-{se}.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{O}/frames/{k}-{se}.jpg", quality=90)
AIC = [
 ("A1", "The gym bag by the door", "He looks over at the packed gym bag by the door, puffs out a sigh and sinks back into the couch. Plays under: \"I can't even get myself to work out twice per week. How could I get myself to work out every day?\" (0:26, in the first minute)", 4.9),
 ("A2", "The morning after", "He eases himself down the stairs one stiff step at a time, gripping the rail. Plays under: \"you are going to be sore the next day. And you're not used to being sore...\" (2:28)", 6.3),
 ("A3", "Life punches you in the face", "He reaches for the front door with his gym bag; a boxing glove on a spring pops out of the bag and bops him on \"punch you in the face\" (4:56). Slapstick, like the slap you liked in the home workout video.", 4.2),
]
DEC = [
 ("Colour", "C, rich and a little warmer (used in the first minute)", ["C: rich, warmer skin (recommended)", "A: rich, skin as the camera saw it", "B: brighter"],
  "These kitchen rolls were shot about a stop and a half dark, with blue window light in the shadows (your black tank top read navy). All three options lift you to the same range as your published videos and make the tank top black again. C also warms your skin slightly, which measures closest to the published Top 10 Tips video and Zeeshan's ab wheel video."),
 ("Framing", "Approve the two sizes as built", ["Approve", "Use the tighter size less", "Use the tighter size more"],
  "Two fixed sizes, cut between on every join so no cut is a jump: the camera frame as shot (waist up) and a 1.3x punch-in (chest up). The punch-in is on screen about two thirds of the time. No camera movement."),
 ("Hair at the top edge", "Leave as shot", ["Leave as shot (recommended)", "Add headroom by extending the wall above your head (one extra round)"],
  "The camera framed your hair close to the top: 20 to 45 pixels of room most of the time, and in six shots late in the roll your hair touches the edge for a moment when you straighten up. I never crop the top (both sizes keep the camera's own top row), but there is no spare picture above your head. One for Jeff on the next shoot."),
 ("Length", "B: about 16:50", ["B: trim five more restatements, about 16:50 (recommended)", "A: keep everything as cut, 18:07", "C: B plus drop the best-time-of-day section, about 14:50"],
  "Every retake, false start and plain repeat is already out (the two rolls ran 30:29). B also removes: the detailed study explanation (23 s; 'that's not what the research says, and you're right' stays), the tail of reason 1 ('This, in my experience, is what really builds the habit...', 17 s), the recap at the end of the night section (10 s), 'The key is you probably would be overtraining...' in the opening (19 s) and the closing recap before the outro (27 s; its last line 'better something short every day than something long inconsistently' stays). C also drops the 2-minute best time of day section, since reason 3 already covers mornings."),
 ("AI clips A1, A2, A3", "Approve all three frame pairs", ["Approve all three (recommended)", "Approve some: name them", "No new AI clips"],
  "Three short new AI clips of one fictional beginner, shown below as start and end frames. Motion is not generated until you approve the frames. Estimated cost for all three: about $2 (Veo 3.1 Fast, one take each, up to 8 s), inside the $5 per video cap. Spend so far: $0."),
 ("Opening", "Your own B-roll for the first 3.5 seconds", ["Your own B-roll, then you (recommended, as built)", "Open on camera", "An AI opener: I send two concepts as frames"],
  "The first 3.5 seconds show you doing push-ups and the towel row by the pool while your first line plays, then cut to you. It is real, it shows the result, and it previews the workout."),
 ("Gymboss on screen", "Send me a screen recording", ["I send a screen recording of my Gymboss timer set to 5 rounds of 30 seconds, 4 times (recommended)", "Use lower thirds only, as built", "Show the App Store page for 'go download it' and keep the settings as a lower third"],
  "You say 'we're showing it on screen right now' twice. There is no Gymboss picture in the footage or the library, and I will not fake the app. Built for now: two lower thirds (G36, G37)."),
 ("'All that stuff for 50 bucks'", "Keep the line, no price on screen", ["Keep the line, no price on screen (recommended, as built)", "Cut the sentence"],
  "At 11:26 you say the kettlebell, mat, ab wheel, jump rope and push-up handles cost 50 bucks all together. In the home workout video the four basics came to $58 and the kettlebell was $45 on top. Nothing on screen repeats the $50."),
 ("Knee push-ups", "Keep the labelled AI demo", ["Keep the app's AI demo of knee push-ups, labelled AI-GENERATED (recommended)", "No clip there, stay on you"],
  "There is no real footage of the knee version. C24 uses the app's own AI demo for 5 seconds."),
 ("Music", "Add the quiet bed", ["Quiet bed under your voice, as you chose for the home workout video (recommended)", "Voice only"],
  "The first minute below is voice only. The bed goes in with the full film."),
 ("Timer for the workout section", "No timer", ["No timer: round numbers and move names only (recommended, as built)", "Also add a follow-along version with a running timer to the edit list as its own video"],
  "The job note suggested an on-screen timer. You describe the workout here, you do not run it in real time, so a running clock would not match anything. The B-roll could become a separate follow-along workout later."),
]
DECIDED = [
 "Intro: your third and last take. It is the cleanest and has the most energy (take 1 trails off on 'twice per week', take 2 doubles a word).",
 "Opening section: the second full run (the first stopped for the plane).",
 "Removed as repeats of the sentence before them: 'So no, it will not be overtraining and yes, you can do it' (0:57), 'Okay, so let me explain why in the real world...' before reason 1, the second 'that sense of dread is going to be in your mind', and 'In addition to this, remember you're going to be tired and sore...' in reason 2 (19 s).",
 "Removed: 'So for all the reasons that I'm about to show you... and then driving to a commercial gym' (15 s). It repeats the opening promise and has a slip in it.",
 "Equipment list: your fourth run, the only one with the push-up handles you were trying to remember.",
 "Fourth month advice: your third, complete version.",
 "Timer setup: kept 'five 30 second rounds, repeat those rounds four times'. Left out the second pass at the same numbers ('So two and a half minutes through the circuit...').",
 "Left out three things said to the crew or to the editor: the plane question, 'we'll cut in B-roll at this point' and 'as I show you on screen a video of myself doing the exercise'.",
 "About a dozen hidden false starts found on a second listen are out (for example 'if you put out two', 'Counting reps can you...', 'Or for those...').",
 "The workout section is covered by the B-roll you shot for it that day: squats, push-ups, lunges, towel rows and the karate chop on the towel, each on the words that describe it.",
 "Other clips: your own equipment B-roll, 11 library clips (nine stock, two older AI clips, labelled), one new stock clip from Pexels (brushing teeth). No stock source and no stock actor is used twice.",
 "Graphics: Soft Blue Light, the approved lower third template, text landing on your words. Reasons are numbered 1 to 4, the plan runs Month 1 to Month 4, the workout runs Round 1 to 5. One fact card (45 minutes).",
 "No side list cards: you stand in the middle of a waist-up frame, so a card would sit on your arm. Lists come up as lower thirds, one part per item as you say it.",
 "No full-screen title cards (the home workout video did not use them either).",
 "Your poolside B-roll gets its own colour correction so it sits with the kitchen.",
 "Microphone: the lav on both rolls. The roll note for the intro clip had picked the far mic by mistake (a plane and the crew talking fooled it); checked on three clean stretches and corrected.",
 "The job note says these rolls match the published Top 10 Tips video. They do not: that video was filmed in the other kitchen. So there was no approved look for this set, which is why colour is decision 1.",
 "Ending: the approved sunglasses-to-pool phone demo, the same file as the home workout video. No AbsByAI.com mark at the end.",
 "Still to come with the full film: about 20 more cutaways (the delivery check wants 40 % of the film covered; this plan covers 21 %), shown to you next round; the music bed; subtitles; chapters.",
 "The lift from the dark original brings up a little grain in the wall behind you. It is mild at normal viewing size; a light noise clean-up is ready if you see it.",
 "Spend so far: $0. Seven Codex pictures on the subscription.",
 "No burned captions. The subtitle file comes with the finished film.",
]
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 420px 60px 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}.opt{color:#cfe2f7;margin:4px 0 0 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#14223a;border:1px solid #26354d;border-radius:10px;overflow:hidden}
.card img{width:100%;display:block}.card .b{padding:9px 11px;font-size:13px}.id{font-weight:700;color:#8fd0ff}.copy{color:#fff;margin:4px 0}.muted{color:#9fb2cc}
details{margin-top:5px}summary{cursor:pointer;color:#9fb2cc}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}a.btn{display:inline-block;background:#2b6cb0;color:#fff;border-radius:6px;padding:6px 10px;margin-top:6px;text-decoration:none}
#dock{position:fixed;right:14px;top:14px;width:384px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:10px}#dock video{width:100%;border-radius:6px;background:#000}
.look{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.look img{width:100%;border-radius:6px}.look div{font-size:12px;color:#9fb2cc;text-align:center}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 2px}.pair img{width:100%;border-radius:6px}.pair div{font-size:12px;color:#9fb2cc;text-align:center}
textarea{width:100%;height:270px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li{margin:5px 0}a{color:#8fd0ff}
@media(max-width:1300px){main{margin-right:28px}#dock{position:static;width:auto;margin:14px 28px}}"""
h = [f"<!doctype html><meta charset='utf-8'><title>RO-07 round 1</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play any item moving, in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>Why You MUST Work Out Every Day: round 1</h1>",
     f"<div class='sub'>Long-form content, 16:9, first cut from the 7/8 kitchen rolls (C1484 and C1485) with the poolside B-roll you shot for it. The full film runs {mmss(TOTAL)} as cut and is not rendered yet: this round locks the look, the graphics and the clips first.</div>",
     "<p><b>Already locked and reused:</b> Soft Blue Light graphics and the approved lower third and fact card templates; the shared voice chain; hard cuts, no swipe sounds, no camera movement.</p>",
     f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, (t, rec, opts, why) in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
fm = "first-minute/DRAFT - RO-07 round 1 - first minute"
h += ["<h2>The first minute, finished</h2>", f"<video class='big' controls preload='none' poster='{fm}.jpg' src='{fm} - REVIEW 540p.mp4'></video>",
      f"<p class='muted'>Colour C, voice only. The AI clip A1 shows as a labelled START / END placeholder until its frames are approved. <a href='{fm}.mp4'>Full 1080p file</a> &nbsp; <a href='first-minute/AB_reference-vs-ours.mp4'>Audio A/B against the reference voice</a><br>Also in the project folder for VLC: <b>Videos to Review / Work Out Every Day LFC R1 - first minute.mp4</b></p>",
      "<h2>Decision 5: new AI clips, start and end frames</h2>"]
for k, name, act, dur in AIC:
    h.append(f"<div class='dec'><b>{k}. {e(name)}.</b> {e(act)} Slot: {dur:.1f} s. Estimated cost: ${0.8:.2f} for one 8 s take."
             f"<div class='pair'><div><img loading='lazy' src='frames/{k}-start.jpg'>START</div><div><img loading='lazy' src='frames/{k}-end.jpg'>END</div></div></div>")
lab = {"raw": "camera original", "A": "A rich", "B": "B brighter", "C": "C rich, warmer"}
h += ["<h2>Decision 1: colour, on four moments</h2><div class='muted'>Left to right: camera original, A, B, C. Measured on these frames (picture brightness / saturation, then your skin brightness): "
      + "; ".join(f"{lab[k]} {v['luma']:.2f} / {v['sat']:.2f}, skin {v['skinY']:.2f}" for k, v in num.items())
      + ". For comparison, your skin reads 0.33 in the published Top 10 Tips video and 0.36 in Zeeshan's ab wheel video.</div><div class='look'>"]
PICK = ("hook.0r1", "r2a.0r1", "t3.0r1", "e2b.0r1")
for p in PICK:
    for k in ("raw", "A", "B", "C"): h.append(f"<div><img loading='lazy' src='look/{p}_{k}.jpg'>{lab[k]}</div>")
h += ["</div><h2>Decision 2: the tighter size (colour C)</h2><div class='look'>"] + [f"<div><img loading='lazy' src='look/{p}_T-C.jpg'>1.3x punch-in</div>" for p in PICK] + ["</div>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += [f"<h2>Every graphic and clip, in order ({len(rows)})</h2><div class='grid'>"]
KIND = {"lt": "lower third", "fact": "fact card", "l3": "side list", "clip": "clip"}
for r in rows:
    c = r["copy"]; lines = []
    if "topic" in c: lines.append(f"{e(c['topic'])}: {e(c['point'])}")
    if "eyebrow" in c: lines.append(e(c["eyebrow"][0]) + " / " + e(" ".join(x[0] for x in c["headline"])) + " / " + e(c["detail"][0]))
    if r["kind"] == "clip": lines.append(e(r.get("note") or ""))
    if c.get("label"): lines.append("Label on screen: " + e(c["label"]))
    if r.get("pending"): lines.append("<b>PLACEHOLDER: start frame shown. Motion is generated only after you approve the frames (decision 5).</b>")
    btn = f"<a class='btn' href='context/{r['id']}-context - REVIEW 540p.mp4' onclick=\"return play(this,'{r['id']}')\">Play it moving, in context</a>" if r["id"] in ctx else ""
    h.append(f"<div class='card' id='{r['id']}'><img loading='lazy' src='stills/{r['id']}.jpg'><div class='b'><span class='id'>{r['id']}</span> <span class='muted'>{KIND[r['kind']]} &middot; {mmss(r['t0'])} to {mmss(r['t1'])}</span>"
             f"<div class='copy'>{'<br>'.join(lines)}</div>{btn}<details><summary>What you are saying</summary><span class='muted'>Before:</span> {e(r['before'])}<br><span class='muted'>During:</span> {e(r['during'])}<br><span class='muted'>After:</span> {e(r['after'])}</details></div></div>")
reply = "RO-07 round 1\n" + "\n".join(f"{i}. {t}: {rec}" for i, (t, rec, o, w) in enumerate(DEC, 1)) + "\nGraphics or clips to change (ID and what):\nFirst minute, anything to change:\nAnything else:\n"
h += ["</div><h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(a,id){var v=document.getElementById('player');v.src=a.getAttribute('href');document.getElementById('docklabel').textContent=id+' in context';v.play();return false;}</script></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("page:", len(rows), "items,", len(ctx), "context clips,", "em dashes:", "\n".join(h).count(chr(8212)))
