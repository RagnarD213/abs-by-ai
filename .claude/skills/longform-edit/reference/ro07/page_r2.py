"""RO-07 round 2 review page (standard layout; only what changed or is new). Writes round2/index.html.
Serve: python3 .claude/skills/_shared/review_server.py 8859 /Volumes/Extreme/_edit_work/ro07/round2"""
import json, os, html
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro07"; O = f"{W}/round2"
import sys; sys.path.insert(0, f"{W}/recipe")
from r2media import CTX, CHANGED_G, CHANGED_C, NEW_C
rows = {r["id"]: r for r in json.load(open(f"{O}/stills.json"))}
S = json.load(open(f"{W}/shots.json")); TOTAL = S[-1]["out_f1"]/(30000/1001)
have = {f.split("-context")[0] for f in os.listdir(f"{O}/context") if f.endswith("REVIEW 540p.mp4") and not f.startswith("._")}
CTXOF = {i: n for n, ids in CTX.items() for i in ids if n in have}
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
e = html.escape
os.makedirs(f"{O}/frames", exist_ok=True)
for src, dst in (("A3-start.png", "A3-start.jpg"), ("A3-end-r1b.png", "A3-end-new.jpg"), ("A3-end.png", "A3-end-old.jpg")):
    Image.open(f"{W}/aiframes/{src}").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{O}/frames/{dst}", quality=90)
DEC = [
 ("A3, the new end frame", "Approve the start frame with the new end frame", ["Approve: I make one 6 second take, about $0.60 (recommended)", "Change the end frame: say what", "Drop the clip"],
  "You kept the start frame and asked for a new end: a much larger cartoon glove on a spring comes in from outside the door and knocks him down. The new end frame is below, next to the start. Plays under \"life is going to punch you in the face\" (4:55). No motion is made until you approve."),
 ("The two picture sizes", "Approve as built", ["Approve as built (recommended)", "Use the tighter size less", "Use the tighter size more"],
  "Asked in round 1, no answer yet. Two fixed sizes, cut between at every join so no cut is a jump: the camera frame as shot (waist up) and a 1.3x punch-in (chest up). The punch-in is on screen about two thirds of the time. Both are in the first minute above."),
 ("Hair at the top edge", "Leave as shot", ["Leave as shot (recommended)", "Add headroom by extending the wall above your head (one extra round)"],
  "Asked in round 1, no answer yet. The camera left 20 to 45 pixels above your hair, and in six late shots your hair touches the edge for a moment. I never crop the top; there is simply no spare picture above your head."),
 ("Length", "About 16:50", ["Trim five more restatements, about 16:50 (recommended)", "Keep everything as cut, 18:07", "Also drop the best-time-of-day section, about 14:50"],
  "Asked in round 1, no answer yet. The 16:50 version removes: the detailed study explanation (23 s), the tail of reason 1 (17 s), the recap at the end of the night section (10 s), 'The key is you probably would be overtraining...' in the opening (19 s) and the closing recap before the outro (27 s). If you pick it, the first minute gets 19 s shorter and I show it again."),
 ("Gymboss on screen", "Send me a screen recording", ["I send a screen recording of my Gymboss timer set to 5 rounds of 30 seconds, 4 times (recommended)", "Lower thirds only, as built", "Show the App Store page and keep the settings as a lower third"],
  "Asked in round 1, no answer yet. At 13:26 and 13:35 you say 'we're showing it on screen right now'. There is no Gymboss picture in the footage or the library and I will not fake the app. Built for now: two lower thirds (G36, G37)."),
 ("'All that stuff for 50 bucks'", "Keep the line, no price on screen", ["Keep the line, no price on screen (recommended, as built)", "Cut the sentence"],
  "Asked in round 1, no answer yet. At 11:35 you say the kettlebell, mat, ab wheel, jump rope and push-up handles cost 50 bucks together. In the home workout video the four basics came to $58 and the kettlebell was $45 on top."),
 ("Music", "Add the quiet bed", ["Quiet bed under your voice, as in the home workout video (recommended)", "Voice only"],
  "Asked in round 1, no answer yet. The first minute above is voice only so you can judge voice 4 on its own. The bed goes in with the full film."),
 ("Timer in the workout section", "No timer", ["No timer: round numbers and move names only (recommended, as built)", "Also put a follow-along version with a running timer on the edit list as its own video"],
  "Asked in round 1, no answer yet. You describe the workout here, you do not run it in real time, so a running clock would match nothing."),
]
DECIDED = [
 "Colour D on both kitchen rolls and voice 4, as you locked them. The voice now runs through the shared voice tool with a new 'no expander' setting. On the same 31 seconds it is sample for sample identical to the audition you approved.",
 "Audio check, stated plainly: the automatic audio gate fails this first minute on one row of 13, tone (it reads less treble than the reference voice, 4.9 dB at the top band). That is the treble boost you rejected in round 1, left out on purpose. Your pick is the approval; no limit was changed. A blind listen heard this first minute and your approved audition as the same sound, well ahead of the round 1 sound.",
 "The round 1 first minute passed that same gate 12 of 12 with the sound you rejected. Recorded as a finding in the regression set, with your words. The gate was not tuned to fit.",
 "Opener (0:00 to 0:06): fast jump rope, then one full handstand push-up, then one full decline push-up on the handles. Each strength clip starts at the top of a rep. Kettlebell deadlifts are not in the opener: one rep takes 3 seconds and each opener piece is 2. They are in the equipment list at 11:20 instead. Say so if you want them in the opener and I will make it four pieces.",
 "Capital letters: your 16 changes are in exactly. I then took full caps off 16 more. Six of 47 lower thirds keep one full caps word: G01 DAILY (the video's whole claim), G06 NOT A Laboratory, G10 Then You SKIP, G12 The One You Actually DO, G14 If You Have To DECIDE, G27 NEVER At Night. Topic labels (the small blue line) stay in caps as the template has them.",
 "G43 is now two lower thirds under 'How many circuits?'. I wrote them in title case like every other lower third: 'Beginners: 2 Circuits, About 5 Minutes Total.' and 'Advanced: 3 Or 4 Rounds, 7.5 To 10 Minutes.'",
 "Every lower third was re-rendered with the missing-space fix, not only G02.",
 "C20: the posing clip is gone. In its place: single-arm curls, seated overhead press, lateral raises, all front on. None is used anywhere else in the film.",
 "C21: starts 0.3 seconds before your first squat. The standing around is cut.",
 "C22: push-ups with the handles, from the side, in low sun (8/28 shoot). Passed over: the 7/8 handle footage, because it is the same from-behind angle you disliked.",
 "C23: used the same from-behind angle, so I replaced it too: flat-body push-ups from the side, same spot and light as C22.",
 "C24: your real knee push-ups (8/28 shoot), not the AI clip. The footage existed all along: the library had it filed as plain push-ups. I corrected the library entry.",
 "No footage twice: the equipment list (C18) now uses a different jump rope cut and a different handles take than the opener and C22, and the second squat clip (C08) uses later reps than C21.",
 "A1 is removed, as you asked. A2: one take was made from the frames you approved ($0.80). I read it frame by frame and found no fault: hands, face and stairs hold. It is trimmed to open just before his first step. Play it below.",
 "10 new cutaways (C30 to C42), shown below. Eight are your own workout footage, picked for front-on or side-on angles and good light; two are library AI clips, labelled. I built 13 and cut three after seeing them on screen: a sofa clip with another video's text burned into it, and two of your clips shot from poor angles. The film was 20 % covered by cutaways and is now 26 %. The delivery check asks for 40 %; the home workout video was approved at 34 %. The library has nothing that fits the remaining lines (alarm clock, commute, the couch, tired at night). If you want more, I download new stock for those and show it next round.",
 "Not built this round, by design: the full film (items are still pending), subtitles, chapters, the music bed.",
 "Spend on this video so far: $0.80 of the $5 cap (the A2 take), plus about 5 cents of listening checks. Next: $0.60 for A3 if you approve it.",
]
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 420px 60px 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}.opt{color:#cfe2f7;margin:4px 0 0 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#14223a;border:1px solid #26354d;border-radius:10px;overflow:hidden}
.card img{width:100%;display:block}.card .b{padding:9px 11px;font-size:13px}.id{font-weight:700;color:#8fd0ff}.copy{color:#fff;margin:4px 0}.muted{color:#9fb2cc}
.multi{display:grid;grid-template-columns:repeat(auto-fit,minmax(30%,1fr));gap:2px}.new{background:#1f7a4d;color:#fff;border-radius:4px;padding:1px 6px;font-size:11px;margin-left:4px}
details{margin-top:5px}summary{cursor:pointer;color:#9fb2cc}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}a.btn{display:inline-block;background:#2b6cb0;color:#fff;border-radius:6px;padding:6px 10px;margin-top:6px;text-decoration:none}
#dock{position:fixed;right:14px;top:14px;width:384px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:10px}#dock video{width:100%;border-radius:6px;background:#000}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 2px}.pair img{width:100%;border-radius:6px}.pair div{font-size:12px;color:#9fb2cc;text-align:center}
textarea{width:100%;height:250px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li{margin:5px 0}a{color:#8fd0ff}
@media(max-width:1300px){main{margin-right:28px}#dock{position:static;width:auto;margin:14px 28px}}"""
KIND = {"lt": "lower third", "clip": "clip"}
def card(i):
    r = rows[i]; c = r["copy"]; lines = []
    if "topic" in c: lines.append(f"{e(c['topic'])}: {e(c['point'])}")
    if r["kind"] == "clip": lines.append(e(r.get("note") or ""))
    if c.get("label"): lines.append("Label on screen: " + e(c["label"]))
    name = CTXOF.get(i)
    btn = f"<a class='btn' href='context/{name}-context - REVIEW 540p.mp4' onclick=\"return play(this,'{name}')\">Play it moving, in context</a>" if name else ""
    imgs = "".join(f"<img loading='lazy' src='stills/{s}.jpg'>" for s in r["stills"])
    if len(r["stills"]) > 1: imgs = f"<div class='multi'>{imgs}</div>"
    tag = "<span class='new'>NEW</span>" if r["group"] == "new" else ""
    return (f"<div class='card' id='{i}'>{imgs}<div class='b'><span class='id'>{i}</span>{tag} <span class='muted'>{KIND[r['kind']]} &middot; {mmss(r['t0'])} to {mmss(r['t1'])} ({r['t1']-r['t0']:.1f} s)</span>"
            f"<div class='copy'>{'<br>'.join(lines)}</div>{btn}<details><summary>What you are saying</summary><span class='muted'>Before:</span> {e(r['before'])}<br><span class='muted'>During:</span> {e(r['during'])}<br><span class='muted'>After:</span> {e(r['after'])}</details></div></div>")
fm = "first-minute/DRAFT - RO-07 round 2 - first minute"
h = [f"<!doctype html><meta charset='utf-8'><title>RO-07 round 2</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play any item moving, in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>Why You MUST Work Out Every Day: round 2</h1>",
     f"<div class='sub'>Long-form content, 16:9. Your round 1 notes, built. This page shows the rebuilt first minute and only what changed or is new. The full film ({mmss(TOTAL)} as cut) is not rendered: it waits until nothing below is pending.</div>",
     "<p><b>Locked:</b> colour D (2026-10-10), voice 4 (2026-10-10), the opener idea, the A2 frames, the A3 start frame, Soft Blue Light graphics, the cut itself (no notes in round 1). <b>Removed:</b> A1.</p>",
     f"<h2>Your decisions ({len(DEC)})</h2><p class='muted'>Number 1 is new. Numbers 2 to 8 were on the round 1 page and never got an answer; I do not take silence as a yes.</p>"]
for i, (t, rec, opts, why) in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
h += ["<h2>The first minute, rebuilt</h2>", f"<video class='big' controls preload='none' poster='{fm}.jpg' src='{fm} - REVIEW 540p.mp4'></video>",
      f"<p class='muted'>Colour D, voice 4, voice only (no music yet). New opener, G02 with its space and without the capitals, G03 without the capitals. <a href='{fm}.mp4'>Full 1080p file</a> &nbsp; <a href='first-minute/AB_reference-vs-ours.mp4'>Audio A/B against the reference voice</a><br>Also in the project folder for VLC: <b>Videos to Review / Work Out Every Day LFC R2 - first minute.mp4</b></p>",
      "<h2>Decision 1: A3, start frame and the new end frame</h2>",
      "<div class='dec'><b>A3. Life punches you in the face.</b> He opens the front door with his gym bag; a giant cartoon boxing glove on a spring shoots in from outside and knocks him off his feet. Slot: 4.6 s. Cost if approved: about $0.60 for one 6 s take."
      "<div class='pair'><div><img loading='lazy' src='frames/A3-start.jpg'>START (you approved this one)</div><div><img loading='lazy' src='frames/A3-end-new.jpg'>NEW END (for your approval)</div></div>"
      "<details><summary>The end frame you rejected, for comparison</summary><img loading='lazy' style='width:50%;border-radius:6px' src='frames/A3-end-old.jpg'></details></div>",
      "<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += [f"<h2>Changed clips ({len(CHANGED_C)})</h2><div class='grid'>"] + [card(i) for i in CHANGED_C] + ["</div>"]
h += [f"<h2>New cutaways ({len(NEW_C)})</h2><div class='grid'>"] + [card(i) for i in sorted(NEW_C, key=lambda i: rows[i]['t0'])] + ["</div>"]
h += [f"<h2>Changed lower thirds ({len(CHANGED_G)})</h2><p class='muted'>Text only: the template and the way each part lands on your words are unchanged from round 1, so these are stills. G43A and G43B are new and have a moving clip.</p><div class='grid'>"] + [card(i) for i in CHANGED_G] + ["</div>"]
reply = "RO-07 round 2\n" + "\n".join(f"{i}. {t}: {rec}" for i, (t, rec, o, w) in enumerate(DEC, 1)) + "\nFirst minute, anything to change:\nClips or cutaways to change (ID and what):\nLower thirds to change (ID and what):\nAnything else:\n"
h += ["<h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(a,id){var v=document.getElementById('player');v.src=a.getAttribute('href');document.getElementById('docklabel').textContent=id+' in context';v.play();return false;}</script></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("page:", len(rows), "items,", len(have), "context clips,", "em dashes:", "\n".join(h).count(chr(8212)))
