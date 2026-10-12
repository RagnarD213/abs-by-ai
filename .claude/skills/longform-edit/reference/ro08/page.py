"""RO-08 round 1 review page (standard layout: decisions, first minute, AI frames, voice options, What I decided, every item
three per row, one docked player, one reply box). Writes round1/index.html.
Serve: python3 .claude/skills/_shared/review_server.py 8869 /Volumes/Extreme/_edit_work/ro08/round1"""
import json, os, html
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro08"; O = f"{W}/round1"
rows = json.load(open(f"{O}/stills.json")); R = json.load(open(f"{W}/plan_resolved.json"))
S = json.load(open(f"{W}/shots.json")); TOTAL = S[-1]["out_f1"]/(30000/1001)
ctx = {f.split("-context")[0] for f in os.listdir(f"{O}/context") if f.endswith("REVIEW 540p.mp4") and not f.startswith("._")} if os.path.isdir(f"{O}/context") else set()
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
e = html.escape
T = {r["id"]: r for r in R}
cover = sum(r["t1"]-r["t0"] for r in R if r["kind"] == "clip")/TOTAL
nlt = sum(r["kind"] == "lt" for r in R); nclip = sum(r["kind"] == "clip" for r in R)
_src = [x.split("@")[0] for r in R if r["kind"] == "clip" for x in r.get("src", [])]
npx = len({x for x in _src if "/px_" in x}); nlib = len({x for x in _src if not x.startswith("/") and x not in ("B0542", "B0438", "B0427", "B0431", "B0453")})
os.makedirs(f"{O}/frames", exist_ok=True)
AIC = [
 ("A1", "\"This is just too hard\" (your excuse voice, lip-synced)", "7 AM, a man whines at his empty breakfast plate, then slumps back in his chair and groans. His lips are synced to your own recording of \"oh, this is just too hard. I could never do intermittent fasting. This just isn't for me. I'm not cut out for it.\"", True),
 ("A2", "\"I could never do this\" (your excuse voice, lip-synced)", "A beginner flat on his back on the gym floor beside one tiny pink dumbbell whines at the camera, then drags himself toward the exit. Lips synced to your \"oh, I could never do this. I'm always gonna be this sore and tired... I might as well just quit.\"", True),
 ("A3", "Their body really lets them know", "A quiet office meeting. His empty stomach rumbles so loudly the water in the glasses ripples and everyone turns to stare. Framed chest up; his stomach is never shown. Plays under: \"They've done this for the past 40 years and all of a sudden there's no breakfast. Their body really lets them know.\"", False),
 ("A4", "Entire days without eating", "An office worker who has not eaten all day stares at a coworker's sandwich. By the end he has a napkin tucked in his collar and a knife and fork in his fists, like a cartoon wolf. Plays under: \"Some people even go entire days without eating.\"", False),
 ("A5", "The food coma", "9 o'clock: a cheerful office worker bites into a donut beside a full bakery box. 10 o'clock: the box is empty and he is asleep face down on his keyboard. Plays under: \"your body has to consume energy to digest. And that's what gives you that food coma, lethargic type of feeling.\"", False),
 ("A6", "The late night binge", "He tiptoes through a dark kitchen. The fridge light catches him frozen like a raccoon, arms full of ice cream, pizza and cake, a spoon in his mouth. Plays under: \"If you do binge on junk food in the later part of the day, intermittent fasting is not going to work for you.\"", False),
 ("A7", "One beer on an empty stomach", "Lunchtime at a bar, his plate still empty. One sip of beer and he slides off the stool, hugging the counter while the bartender stares. Plays under: \"It's going to hit you faster, you're going to feel more drunk and the health effects are going to be a lot worse.\"", False),
 ("A8", "Autophagy (a cartoon, because there is no real picture of it)", "Inside a cell, a tiny clean-up crew in hard hats wheels the broken old parts into a furnace and the whole cell glows brighter. Plays under: \"This process of breaking down the old diseased damaged parts of your cells for fuel renews your cells.\"", False),
]
for k, *_ in AIC:
    for se in ("start", "end"):
        Image.open(f"{W}/aiframes/{k}-{se}.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{O}/frames/{k}-{se}.jpg", quality=90)
VOICES = [("voice-1 - warm, less echo, a little more bass (used in the first minute).mp3", "1: warm, less echo, a little more bass (recommended, used in the first minute)"),
          ("voice-2 - warm, less echo, no bass added (exactly the Work Out Every Day voice).mp3", "2: warm, less echo, no bass added (exactly the voice you picked on Work Out Every Day)"),
          ("voice-3 - warm, less echo, more bass.mp3", "3: warm, less echo, more bass (the amount you picked on the spray tan video)")]
DEC = [
 ("AI clips A1 to A8", "Approve the ones you like; name any to drop", ["Approve all eight and raise this video's AI budget from $5 to $7", "Approve up to six (inside the $5 cap): name the ones to drop", "No new AI clips"],
  "Eight new AI clip ideas of one fictional beginner (the same man as the sore-on-the-stairs clip you approved on Work Out Every Day), shown below as start and end frames. Most are meant to be funny; I brought more than I expect you to keep. Nothing moves until you approve its frames. Cost: $0.60 to $0.80 a clip, plus about $0.50 each for the lip sync on A1 and A2. All eight come to about $6.20, which is over the $5 per video cap, so either drop two or say the word and I use up to $7. Spend so far: $0."),
 ("Opening", "Your own footage, then you (as built)", ["Your own footage for the first sentence, then you on camera (recommended, as built)", "Open on camera"],
  "The first 7 seconds show your fast jump rope and then your front pose by the pool on the words \"six-pack abs\", with your first sentence playing underneath. It shows the result before you explain how. I did not offer an AI gag opener: you turned those down on the Invest In Your Health video and asked for a camera scene."),
 ("Voice", "1", ["1: a little more bass (recommended)", "2: no bass added", "3: more bass"],
  "Same room and microphones as Work Out Every Day, so I started from the voice you picked there (warm, less kitchen echo) and added your new standing bass lift. This microphone already reads fuller than the reference voice, so I used a smaller lift (1 dB) than on the spray tan video (3 dB). Three 31 second clips of the same sentence are below, level matched. One blind listen ranked option 1 first and above the untreated microphone; I would not trust it to separate three versions this close, so your ear decides."),
 ("Length", "Keep 14:41", ["Keep 14:41 as cut (recommended)", "Trim about a minute more: the other kinds of fasting (20 s), the 15 hour sum (14 s), the game plan recap (15 s) and 'avoid alcohol while you're working' (6 s)"],
  "The roll runs 23:06. Every retake, false start and plain repeat is out. What is left is all new information, so I would keep it."),
 ("Hair at the top edge", "Leave as shot", ["Leave as shot (recommended, as on Work Out Every Day)", "Add headroom by extending the wall above your head (one extra round)"],
  "On this roll the camera framed your hair right at the top of the picture: about 14 pixels of room on average, and it touches the edge for a moment in most shots. I never crop the top (both sizes keep the camera's own top row), but there is no spare picture above your head. Same shoot as Work Out Every Day, which you approved as shot."),
 ("The app at the end", "Lower third, as built", ["Lower third naming the three tools (as built, same as Work Out Every Day)", "The phone tour beside you (calorie tracking, then workouts) that you approved on the home workout video: I build it for round 2"],
  "You list the macro tracker, the trainer and the nutritionist in the close. Built now: one lower third that brings each name up as you say it, after the sunglasses-to-pool phone demo."),
]
DECIDED = [
 "This is long-form content (it ends 'go to absbyai.com' and 'let me know in the comments'), so it gets Shorts later and nothing else.",
 "Intro: your third and last take. It is the cleanest (take 1 goes flat on 'so much easier', take 2 restarts 'In today's video'). A blind listen scored the three 8, 5 and 10.",
 "Removed from the intro: 'It's really changed so much for me and I'm excited to share it with you today.' It repeats 'totally changed my life' four seconds earlier.",
 "Removed: the second 'In today's video I'm going to show you...' promise at 4:36 of the roll (25 s, with a false start in it). The intro already makes that promise.",
 "Removed as repeats: 'So just make sure to keep everything else in the latter part of the day the same' (the third time in 20 seconds) and 'All right, so that's your simple game plan to get started' (it came right after 'So that's your game plan').",
 "Eighteen retakes and false starts are out. In each case I kept your retake, for example 'how you lose your belly fat' over 'how your belly fat loses', 'not consuming anything' over 'not consuming energy', and 'fasting five hours' over 'about five to six hours'.",
 "One abandoned sentence was hiding where the transcript showed nothing ('With that being said though, you do have...' before the clean run). I found it on the sound itself and it is out.",
 "The close: your second run, the one you asked for on the roll ('Do that close one more time').",
 "Colour: the look you picked on Work Out Every Day (bright and natural). This roll measures the same as that one (your skin reads 0.254 here, 0.256 there), so it is reused, not reopened.",
 "Microphone: the lav. The roll's note had the far microphone by mistake; three clean stretches all say the lav is the other channel, the same as the Work Out Every Day rolls. Corrected.",
 "Music: the same quiet bed, at the same level, as Work Out Every Day. It is in the first minute.",
 f"Graphics: {nlt} lower thirds in Soft Blue Light, the approved template, each part landing on the word you say. Title capitalisation throughout; no word in full capitals. Reasons are numbered 1 to 4 plus 'The Most Important Reason', the plan runs Month 1 onward, the mistakes run 1 to 3.",
 "On-screen wording for the health section uses your own words and nothing stronger ('Your Cells Run Out Of Fuel', 'They Break Down Their Old, Damaged Parts'). You name the drugs out loud; on screen it says GLP-1 only.",
 "No side list cards and no full-screen title cards: you stand in the middle of a waist-up frame, so a card would sit on your arm. Work Out Every Day did not use title cards either. Lists come up as lower thirds.",
 f"Clips: {nclip} cutaways. Your own footage first: the opener, three shots of your daily salad lifted from the approved salad film (already colour corrected, no graphics), the ab wheel, and kettlebell deadlifts and decline push-ups under the close. Then {nlib} library clips, {npx} new stock clips from Pexels, and the eight AI ideas. No stock source and no stock actor is used twice.",
 "The boxing glove gag you approved on Work Out Every Day is reused on 'life is going to punch you in the face', with the glove landing on 'punch'.",
 "C22 (a stock man asleep at his desk) is a stand-in. If you approve A5, the donut food coma, C22 comes out so the film does not show two men asleep at desks.",
 "When you say 'cold brew', the clip is cold brew over ice. When you say 'spaghetti or a piece of pizza', it is spaghetti, then pizza. Milkshakes and a sundae on 'no milkshakes, no jumbo ice cream sundaes'.",
 "For the GLP-1 line I used the vial and syringe clip, not the pen with a glucose meter beside it.",
 "Framing: two fixed sizes (the camera frame and a 1.3x punch-in), cut between on every join so no cut is a jump. The punch-in is on screen two thirds of the time. No camera movement. The longest stretch with nothing changing is 22 seconds.",
 f"Cutaways cover {cover*100:.0f} % of the film (the delivery check asks for 40 %; Work Out Every Day was approved at 27 %). If you want more, say so and I add stock in round 2.",
 "Ending: the approved sunglasses-to-pool phone demo, the same file as the last two videos. No AbsByAI.com mark at the end.",
 "Still to come with the full film: subtitles, chapters (worded so they do not repeat the fasting tips in your Top 10 Tips video), the independent review and the delivery checks.",
 "Spend so far: $0 on generation. Sixteen Codex pictures on the subscription. Two short Gemini listens (take choice and voice), a few cents.",
 "No burned captions. The subtitle file comes with the finished film.",
]
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 420px 60px 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}.opt{color:#cfe2f7;margin:4px 0 0 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#14223a;border:1px solid #26354d;border-radius:10px;overflow:hidden}
.card img{width:100%;display:block}.card .b{padding:9px 11px;font-size:13px}.id{font-weight:700;color:#8fd0ff}.copy{color:#fff;margin:4px 0}.muted{color:#9fb2cc}
details{margin-top:5px}summary{cursor:pointer;color:#9fb2cc}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}a.btn{display:inline-block;background:#2b6cb0;color:#fff;border-radius:6px;padding:6px 10px;margin-top:6px;text-decoration:none}
#dock{position:fixed;right:14px;top:14px;width:384px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:10px}#dock video{width:100%;border-radius:6px;background:#000}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 2px}.pair img{width:100%;border-radius:6px}.pair div{font-size:12px;color:#9fb2cc;text-align:center}
textarea{width:100%;height:300px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li{margin:5px 0}a{color:#8fd0ff}audio{width:100%;margin:4px 0 10px}
@media(max-width:1300px){main{margin-right:28px}#dock{position:static;width:auto;margin:14px 28px}}"""
h = [f"<!doctype html><meta charset='utf-8'><title>RO-08 round 1</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play any item moving, in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>Intermittent Fasting: The Best Way To Get Abs: round 1</h1>",
     f"<div class='sub'>Long-form content, 16:9, first cut from the 7/8 kitchen roll C1486. The full film runs {mmss(round(TOTAL))} as cut and is not rendered yet: this round shows you the first minute, every graphic and every clip first.</div>",
     "<p><b>Already locked and reused:</b> the colour you picked on Work Out Every Day (same set, same shoot); Soft Blue Light graphics and the approved lower third template; the quiet music bed; hard cuts, no swipe sounds, no camera movement; the boxing glove gag; the sunglasses-to-pool phone demo.</p>",
     f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, (t, rec, opts, why) in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
fm = "first-minute/DRAFT - RO-08 round 1 - first minute"
h += ["<h2>The first minute, finished</h2>", f"<video class='big' controls preload='none' poster='{fm}.jpg' src='{fm} - REVIEW 540p.mp4'></video>",
      f"<p class='muted'>Voice 1. The music bed is in, and it is quiet (the same level as Work Out Every Day); say so if you want it louder. No AI clip falls inside the first minute. Audio check: 12 of 13 rows pass; the tone row fails because this is a fixed voice shape you chose, not a matched one. <a href='{fm}.mp4'>Full 1080p file</a> &nbsp; <a href='first-minute/AB_reference-vs-ours.mp4'>Audio A/B against the reference voice</a><br>Also in the project folder for VLC: <b>Videos to Review / Intermittent Fasting LFC R1 - first minute.mp4</b></p>",
      "<h2>Decision 1: new AI clips, start and end frames</h2>"]
for k, name, act, lip in AIC:
    r = T[k]; cost = ("$0.80" if r["t1"]-r["t0"] > 6.0 else "$0.60") + " for one take" + (" plus about $0.50 for the lip sync" if lip else "")
    h.append(f"<div class='dec'><b>{k}. {e(name)}.</b> {e(act)} At {mmss(r['t0'])}, {r['t1']-r['t0']:.1f} s. Estimated cost: {cost}."
             f"<div class='pair'><div><img loading='lazy' src='frames/{k}-start.jpg'>START</div><div><img loading='lazy' src='frames/{k}-end.jpg'>END</div></div></div>")
h += ["<h2>Decision 3: your voice, three options on the same 31 seconds</h2><div class='muted'>Each starts on \"Alright so let's talk about why intermittent fasting is superior...\" and is speech all the way through.</div>"]
for f, lab in VOICES: h.append(f"<div>{e(lab)}<audio controls preload='none' src='audio/{e(f)}'></audio></div>")
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += [f"<h2>Every graphic and clip, in order ({len(rows)})</h2><div class='grid'>"]
KIND = {"lt": "lower third", "fact": "fact card", "l3": "side list", "clip": "clip"}
for r in rows:
    c = r["copy"]; lines = []
    if "topic" in c: lines.append(f"{e(c['topic'])}: {e(c['point'])}")
    if r["kind"] == "clip": lines.append(e(r.get("note") or ""))
    if c.get("label"): lines.append("Label on screen: " + e(c["label"]))
    if r.get("pending"): lines.append("<b>PLACEHOLDER: start frame shown. Motion is generated only after you approve the frames (decision 1).</b>")
    btn = f"<a class='btn' href='context/{r['id']}-context - REVIEW 540p.mp4' onclick=\"return play(this,'{r['id']}')\">Play it moving, in context</a>" if r["id"] in ctx else ""
    h.append(f"<div class='card' id='{r['id']}'><img loading='lazy' src='stills/{r['id']}.jpg'><div class='b'><span class='id'>{r['id']}</span> <span class='muted'>{KIND[r['kind']]} &middot; {mmss(r['t0'])} to {mmss(r['t1'])}</span>"
             f"<div class='copy'>{'<br>'.join(lines)}</div>{btn}<details><summary>What you are saying</summary><span class='muted'>Before:</span> {e(r['before'])}<br><span class='muted'>During:</span> {e(r['during'])}<br><span class='muted'>After:</span> {e(r['after'])}</details></div></div>")
reply = ("RO-08 round 1\n" + "\n".join(f"{i}. {t}: {rec}" for i, (t, rec, o, w) in enumerate(DEC, 1))
         + "\nAI clips, one line each (approve / change / drop): A1  A2  A3  A4  A5  A6  A7  A8\nGraphics or clips to change (ID and what):\nFirst minute, anything to change:\nAnything else:\n")
h += ["</div><h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(a,id){var v=document.getElementById('player');v.src=a.getAttribute('href');document.getElementById('docklabel').textContent=id+' in context';v.play();return false;}</script></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("page:", len(rows), "items,", len(ctx), "context clips,", "em dashes:", "\n".join(h).count(chr(8212)), "cover", round(cover*100, 1))
