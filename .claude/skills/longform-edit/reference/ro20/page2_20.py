"""RO-20 round 2 review page: only what changed or is new (PRE-RENDER-APPROVAL.md, later rounds). Writes round2/index.html.
Serve with _shared/review_server.py 8864 /Volumes/Extreme/_edit_work/ro20/round2"""
import json, os, html
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round2"; e = html.escape
DOC = "https://docs.google.com/document/d/1NI41W27Ipq3yukQ9HX-pLQYxbFEo849Na4Q95UzsGwA/edit"
os.makedirs(f"{O}/frames", exist_ok=True); os.makedirs(f"{O}/img", exist_ok=True)
for j in ("J1", "J2"):
    for se in ("start", "end"): Image.open(f"{W}/aiframes/{j}-{se}.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{O}/frames/{j}-{se}.jpg", quality=90)
for f in sorted(os.listdir(f"{O}/stills")):
    if f.endswith(".png") and not f.startswith("._"): Image.open(f"{O}/stills/{f}").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{O}/img/{f[:-4]}.jpg", quality=90)
GJ = json.load(open(f"{O}/broll_grades.json")); REP = json.load(open(f"{O}/broll/report.json")); OV = json.load(open(f"{O}/broll/overrides.json"))
def has(p): return os.path.exists(f"{O}/{p}")
def btn(name, label="Play it moving, in context"):
    p = f"context/{name}-context - REVIEW 540p.mp4"
    return f"<a class='btn' href='{p}' onclick=\"return play(this,'{name}')\">{label}</a>" if has(p) else "<span class='muted'>(context clip still rendering)</span>"
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 420px 60px 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}h3{font-size:15px;margin:22px 0 8px;color:#8fd0ff}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}.opt{color:#cfe2f7;margin:4px 0 0 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.card{background:#14223a;border:1px solid #26354d;border-radius:10px;overflow:hidden}
.card img{width:100%;display:block}.card .b{padding:9px 11px;font-size:13px}.id{font-weight:700;color:#8fd0ff}.copy{color:#fff;margin:4px 0}.muted{color:#9fb2cc}
details{margin-top:5px}summary{cursor:pointer;color:#9fb2cc}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}a.btn{display:inline-block;background:#2b6cb0;color:#fff;border-radius:6px;padding:6px 10px;margin-top:6px;text-decoration:none}
#dock{position:fixed;right:14px;top:14px;width:384px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:10px}#dock video{width:100%;border-radius:6px;background:#000}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 2px}.pair img{width:100%;border-radius:6px}.pair div{font-size:12px;color:#9fb2cc;text-align:center}
.say{font-size:17px;line-height:1.5;color:#fff;background:#0b1320;border-left:3px solid #8fd0ff;padding:10px 14px;margin:8px 0;border-radius:0 8px 8px 0}.ctx{color:#9fb2cc;font-style:italic;margin:4px 0}
table{border-collapse:collapse;width:100%}td,th{padding:5px 12px 5px 0;vertical-align:top;text-align:left;border-bottom:1px solid #1d2b44;font-size:13.5px}th{color:#8fd0ff}
.tri img{width:100%;display:block;border-radius:8px;margin:6px 0 2px}textarea{width:100%;height:300px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li{margin:5px 0}a{color:#8fd0ff}
@media(max-width:1300px){main{margin-right:28px}#dock{position:static;width:auto;margin:14px 28px}}"""
DEC = [
 dict(t="New AI clip J1, the job interview (replaces the stock handshake under the lower third at 1:01)", why="Your note: a guy in great shape getting a job while the fat guy looks on in envy, maybe in a boardroom. Frames below. Motion is 8 seconds, $0.80, made only when you approve.", opts=["Approve the frames (recommended)", "Change (say what)"], rec="approve"),
 dict(t="New AI clip J2, the partnership (replaces the old office handshake clip at 1:25)", why="The second of your two similar clips, a different scene: a deal signed on a golf clubhouse terrace, because the line it sits under is about getting the partnership. Motion is 4 seconds, $0.40.", opts=["Approve the frames (recommended)", "Change (say what)", "Make this one a second job scene instead"], rec="approve"),
 dict(t="How video 2 opens", why="You already said the hook on camera, word for word, at the end of the roll (\"You are being too cheap with your health...\"). Video 2 can open on that take for its first 12 seconds, then your pickup P2 continues over pictures from \"In the last video\". Or the whole opening is your pickup voice over pictures. You record P2 the same either way. Preview button below.", opts=["Open on camera with that take (recommended)", "Pickup voice over pictures for the whole opening"], rec="open on camera"),
 dict(t="The pickup scripts", why="Four short recordings, about 80 seconds in total. Read them as written, or change any wording in the doc before you record.", opts=["Record as written", "I edited the doc, use my wording"], rec="record as written"),
]
PICK = [
 ("P1", "End of video 1", "You just said on camera: \"All right, so hopefully now I've got you convinced. You need to be spending more money on your health.\"",
  ["In the next video, I'm going to tell you what you should cut to find that money, even if you're a brokie right now.", "In the video after that, I'll walk you through exactly what to buy for your health at every level, from dead broke to mega baller."],
  "Then on camera: \"Alright guys, that's today's video. If you wanna take the first step to getting in shape, go to AbsByAI.com...\" (the roll's other closing take)", "about 15 s",
  [("\"In the next video\"", "The three-part card. Row 1 ticked, row 2 lights up with a Next Video tag."), ("\"what you should cut to find that money\"", "In the card's picture window: three showy cocktails on a bar (stock from video 2)."),
   ("\"even if you're a brokie right now\"", "In the window: the brokie turning out his pockets (AI clip A2, labelled)."), ("\"In the video after that\"", "Row 3 lights up."),
   ("\"from dead broke\"", "In the window: the cardboard box house guy (AI clip A3, labelled)."), ("\"to mega baller\"", "In the window: a home gym (library AI clip A0037, labelled).")],
  ["SC-P1-next-is-2", "SC-P1-then-3"]),
 ("P2", "Start of video 2", "",
  ["You are being too cheap with your health, and your cheapness and wasting money on bullshit is literally killing you.", "In the last video, I told you why you need to spend more. Being in shape makes you more money and more productive, and bad health is ludicrously expensive.", "In this video, I'll tell you exactly what to cut, so you can spend more money on your health."],
  "Then on camera: \"But I know at this point in the video a lot of y'all guys are thinking, oh well damn that's easy for you to say, you have money. But I am a brokie...\"", "about 21 s",
  [("\"You are being too cheap with your health\" (first 5 seconds)", "Your own footage, colour corrected: front-on dumbbell lateral raises beside the pool (B0450). Or you on camera saying it (decision 3)."),
   ("\"wasting money on bullshit\"", "New stock: cash left on a bar."), ("\"is literally killing you\"", "Library stock: a heart monitor printing its strip (B0275)."),
   ("\"In the last video, I told you why\"", "The three-part card, row 1 lit with a Last Video tag."), ("\"more money\" / \"more productive\" / \"ludicrously expensive\"", "In the window: the fit guy getting the job (J1), your push-ups by the pool (B0032), the ambulance (stock from video 1)."),
   ("\"In this video, I'll tell you exactly what to cut\"", "Row 2 lights up with a This Video tag. In the window: going through a stack of receipts (new stock)."), ("\"so you can spend more money on your health\"", "In the window: your kneeling ab wheel rollouts by the pool (B0427).")],
  ["SC-P2-last-was-1", "SC-P2-this-is-2"]),
 ("P3", "End of video 2 (this video has no on-camera sign-off)", "You just said on camera: \"Again, sacrifices temporarily. It'll just be for a few months, and you'll be so glad you did once you're there in a couple months.\"",
  ["That's what to cut. Now you have the money.", "In the next video, I'll walk you through exactly what to buy for your health at every income level, from dead broke to baller.", "To take the first step to getting in shape, go to AbsByAI.com.", "Upload a picture of yourself, and AI makes a picture of you with ripped six-pack abs, for free.", "Thanks for watching guys, I'll see you in the next video."],
  "", "about 23 s",
  [("\"That's what to cut. Now you have the money.\"", "The three-part card, row 2 ticked. In the window: hands counting dollar bills (library stock B0207)."), ("\"In the next video ... from dead broke to baller\"", "Row 3 lights up with a Next Video tag. In the window: the cardboard box guy (A3), then the home gym (A0037), both labelled."),
   ("\"go to AbsByAI.com. Upload a picture of yourself ... for free.\"", "Full screen: your approved app demo (sunglasses photo to pool goal, 11 seconds, its AI-GENERATED label as approved)."), ("\"Thanks for watching guys...\"", "The demo finishes, then the three-part card with row 3 lit, with room for YouTube's end screen.")],
  ["SC-P3-next-is-3"]),
 ("P4", "Start of video 3", "",
  ["Here's exactly what you should be buying for your health, whether you're dead broke, middle class, or making over $10,000 a month.", "You need to be spending more money on your health no matter how little you have right now. Because money does you no good if you're dead or if you're sick.", "The last video covered what to cut to find the money. Now let's spend it."],
  "Then on camera: \"All right. So let me walk you through it. I'll walk you through every level...\"", "about 22 s",
  [("\"Here's exactly what you should be buying for your health\" (first 3 seconds)", "Your own footage, colour corrected: standing front-on beside the pool, hands on hips (B0429)."), ("\"dead broke, middle class, or making over $10,000 a month\"", "The three levels card. Its three tiles land one at a time on your words."),
   ("\"spending more money on your health no matter how little you have\"", "Your own footage, colour corrected: walking lunges by the pool (B0462)."), ("\"dead or if you're sick\"", "Library stock: a heart monitor printing its strip (B0275)."),
   ("\"The last video covered what to cut\"", "The three-part card, row 2 lit with a Last Video tag, cocktails in the window."), ("\"Now let's spend it.\"", "Row 3 lights up with a This Video tag, then cut to you on camera.")],
  ["LV-P4-three-levels", "SC-P4-this-is-3"]),
]
DECIDED = [
 "The three videos: video 1 is 0:00 to 15:00 of the round 1 cut plus P1 and the roll's other sign-off take; video 2 is P2, then 15:04 to 23:40, then P3; video 3 is P4, then 23:40 to the end. The cut itself is untouched: no pause was tightened again.",
 "Two sentences come out because the split makes them untrue: \"And I'll go more into that in a minute\" (video 1, 9:00, about therapy) and \"So, I'll be telling you exactly what you should be spending that money on in a minute\" (15:00).",
 "Video 1 now opens on camera at the closer size, the same shot and crop you approved from 0:06 on. The vending machine opener is gone. Every other shot in the film holds the size and crop it had on the round 1 page (checked: 499 of 499).",
 "A1, A2 and A3: the first take of each worked. I read every frame for melting hands and morphing objects and found none. A1's lips are synced to your own recording with the method you approved on the home workout video. A3 uses the last 4.6 seconds of its take (out of the box, onto the mat, the swing).",
 "The lawyer clip (A4) is removed. You stay on camera there.",
 "The job clip slot (old Ca02) is trimmed from 9.2 to 7.4 seconds: it ends on \"if you look better\" and you are back on camera for \"compared to if you look worse\". I read your note as: the lower third stays, the picture under it changes. Say if you meant the lower third to go too.",
 "One thing to know about J1: the stock clip just before it (0:52, three executives across a table) is also a boardroom, so two boardroom pictures run back to back. I kept both because they read as one scene, the panel sizing him up and then the handshake. Say if you want the stock clip swapped.",
 "The dating-app clip starts on \"and I know this because\" so all four of its screens fit without speeding anything up: heavier profile, no matches, lean profile on \"I got in really good shape\", the matches list on \"10x my matches\". The old lower third's words moved beside the phone, so that lower third is gone.",
 "Your diagram is now the full-screen graphic, with \"10 Women\" and \"10 Men\" over its two columns. The text beside it is from your own sentence. That lower third is gone too, since the card says it.",
 "B-roll colour: all 35 clips of your own footage were measured against the presenter look and each one looked at beside a presenter frame. 24 are graded, 11 are left alone (already bright in full sun, or gloved hands with no skin to match). The three you flagged (B0455, B0456, B0434) are lifted 1.6 to 1.9 times. My first two passes flattened the sunlit clips, so the rule now uses both your shaded and your sunlit skin and never darkens a highlight.",
 "The clip of you on your phone (B0437) is out of the film and marked never-use in the library.",
 "Pickup pictures: a planned squat clip (B0460) was too dark even graded, so it is swapped for the walking lunges. Pexels had no clean shot of a card being cut up, so that beat shows receipts instead.",
 "The three-part card names each part by what it covers, not by a working title, so a title change at upload time cannot make the graphic wrong.",
 "Spend so far: $2.66 (three motion takes $2.00, lip sync $0.66). By video: video 1 $1.46, video 2 $0.60, video 3 $0.60. Still planned: J1 $0.80 and J2 $0.40, both in video 1. Cap is $5.00 per video.",
 "Not built yet, on purpose: the first minute of videos 2 and 3 (both open on your pickup audio) and the three full films. The lower third over the job clip gets re-rendered once that clip's motion exists.",
]
h = [f"<!doctype html><meta charset='utf-8'><title>Invest In Your Health LFC R2</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play any item moving, in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>Invest In Your Health, round 2: three videos (LFC, content)</h1>",
     "<div class='sub'>Only what changed or is new since round 1. Nothing is fully rendered yet except video 1's first minute.</div>",
     "<p><b>Already locked and reused:</b> colour D for both sizes, voice 4, the chapters, frames A1, A2 and A3, and every graphic and clip you did not flag in round 1.</p>",
     f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, d in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(d['t'])}.</b> {e(d['why'])}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in d['opts'])}</div></div>")
fm = "first-minute/DRAFT - RO-20 round 2 - video 1 first minute"
h += ["<h2>Video 1: the first minute, finished</h2>"]
if has(fm + " - REVIEW 540p.mp4"):
    h += [f"<video class='big' controls preload='none' poster='{fm}.jpg' src='{fm} - REVIEW 540p.mp4'></video>",
          f"<p class='muted'>Opens on camera (no AI opener). The fat guy who has money is at 0:20 with his lips on your words. It stops at 1:01, where the new job clip starts. <a href='{fm}.mp4'>Full 1080p file</a><br>Also in the project folder for VLC: <b>Videos to Review/Invest In Your Health LFC R2 - video 1 first minute.mp4</b></p>"]
else: h.append("<p class='muted'>(still rendering)</p>")
h += ["<h2>New AI clips: start and end frames</h2>"]
for j, name, act, dur, cost in (("J1", "The job interview", "A hiring panel in a boardroom smiles at the fit candidate; the lead interviewer stands and shakes his hand across the table while the heavy candidate beside him, still holding his folder, looks on in envy. Sits under \"So let's say you're applying for a new job. Your odds of getting the job are drastically, drastically increased if you look better\", with the lower third \"Better Looking Candidates Get Hired More.\"", 7.4, "$0.80 (8 s take)"),
                                 ("J2", "The partnership", "On a golf clubhouse terrace the senior partner holds the contract out to the fit man, then they shake on it over the signed contract while the heavy man looks sideways at them. Sits under \"they're gonna judge you based on that and you're less likely to get the partnership.\"", 3.6, "$0.40 (4 s take)")):
    h.append(f"<div class='dec'><b>{j}. {e(name)}.</b> {e(act)} Slot: {dur:.1f} s. Cost: {e(cost)}. Label: AI-GENERATED. Framed from the chest up, the table hides both men below the chest."
             f"<div class='pair'><div><img loading='lazy' src='frames/{j}-start.jpg'>START</div><div><img loading='lazy' src='frames/{j}-end.jpg'>END</div></div></div>")
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += [f"<h2>Your audio pickups: the scripts and what is on screen</h2><p>The doc to read from: <a href='{DOC}'>Invest In Your Health R2: audio pickups to record (P1 to P4)</a>. Same lav as the shoot if you have it, otherwise your phone a hand's width from your mouth in a quiet soft room. One file per pickup named P1 to P4, two takes each, dropped in <b>Media/longform-raw/ro20-pickups/</b>. The seconds below are estimates; every picture is re-timed to your real recording.</p>"]
for pid, where, before, say, after, dur, rows, stills in PICK:
    h.append(f"<h3>{pid}: {e(where)} ({dur})</h3>")
    if before: h.append(f"<div class='ctx'>{e(before)}</div>")
    h.append("<div class='say'>" + "<br>".join(e(s) for s in say) + "</div>")
    if after: h.append(f"<div class='ctx'>{e(after)}</div>")
    h.append("<table><tr><th style='width:38%'>You are saying</th><th>On screen</th></tr>" + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in rows) + "</table>")
    h.append("<div class='grid2' style='margin-top:10px'>" + "".join(f"<div class='card'><img loading='lazy' src='img/{s}.jpg'><div class='b'><span class='id'>{'The three levels card' if s.startswith('LV') else 'The three-part card'}</span> <span class='muted'>new Soft Blue Light graphic, still</span></div></div>" for s in stills) + "</div>")
    if pid == "P2": h.append(f"<p>Decision 3, the camera option: your own take of the hook, from the end of the roll, as video 2's first 12 seconds. {btn('V2-camera-open', 'Play the on-camera opening')}</p>")
h += ["<h2>Changed and new, in film order</h2><div class='grid'>"]
ITEMS = [
 ("A1", "img/A1.jpg", "AI clip, finished", "0:20 to 0:28, video 1", "The fat guy who has money, lips synced to your own recording. AI-GENERATED label.", "<span class='muted'>It plays in the first minute at the top of this page.</span>"),
 ("Ca02 (J1)", "frames/J1-start.jpg", "new AI clip, frames only", "1:01 to 1:08, video 1", "Placeholder: start frame shown. Decision 1.", ""),
 ("Ca03 (J2)", "frames/J2-start.jpg", "new AI clip, frames only", "1:25 to 1:28, video 1", "Placeholder: start frame shown. Decision 2.", ""),
 ("Cb11", "img/Cb11-d.jpg", "full screen card", "4:17 to 4:25, video 1", "Your earlier AI dating-app clip in the phone shell. Text: DAN'S RESULT / Decent Shape To Great Shape: / 10x The Matches. Label: AI-GENERATED. Replaces the clip of you on your phone.", btn("dating")),
 ("Cb12", "img/Cb12-diagram.jpg", "full screen card", "4:28 to 4:34, video 1", "Your diagram. Text: ONLINE DATING / Winner Take All / The Top Guys Take Everything. / The Bottom 80% Get NOTHING. Replaces the stock man scrolling his phone.", btn("dating")),
 ("A2", "img/A2.jpg", "AI clip, finished", "0:06 after your pickup, video 2 (15:11 on the round 1 cut)", "The brokie turns out his pockets and shrugs. He does not speak; your voice does the excuse. AI-GENERATED label.", btn("A2")),
 ("A3", "img/A3.jpg", "AI clip, finished", "0:10 after your pickup, video 3 (23:51 on the round 1 cut)", "The cardboard box house guy climbs out and swings the kettlebell. AI-GENERATED label.", btn("A3")),
]
for iid, img, kind, when, copy, b in ITEMS:
    h.append(f"<div class='card'><img loading='lazy' src='{img}'><div class='b'><span class='id'>{e(iid)}</span> <span class='muted'>{e(kind)} &middot; {e(when)}</span><div class='copy'>{e(copy)}</div>{b}</div></div>")
h += ["</div>", f"<h2>B-roll colour: before and after ({len(GJ)} graded, {len(REP) - len(GJ)} left alone)</h2><p class='muted'>Each strip: a presenter frame in look D, the clip as it was, the clip graded. The three you called excessively dark come first.</p><div class='tri'>"]
first = ["B0455", "B0456", "B0434"]
for cid in first + [c for c in sorted(GJ) if c not in first]:
    h.append(f"<div class='muted'><b style='color:#8fd0ff'>{cid}</b>{' (you flagged this one)' if cid in first else ''}: lifted {REP[cid]['gain']}x{', colour up ' + str(round((REP[cid]['sat'] - 1)*100)) + '%' if REP[cid]['sat'] > 1.02 else ''}</div><img loading='lazy' src='broll/{cid}.jpg'>")
h.append("</div><details><summary>The clips left alone, and why</summary><ul>" + "".join(f"<li>{c}: {e(OV.get(c, {}).get('skip', 'already sits with the presenter (within 10%)'))}</li>" for c in sorted(REP) if c not in GJ) + "</ul></details>")
reply = "Invest In Your Health LFC R2\n" + "\n".join(f"{i}. {d['t'].split(',')[0].split(' (')[0]}: {d['rec']}" for i, d in enumerate(DEC, 1)) + "\nPickups recorded and dropped in Media/longform-raw/ro20-pickups/: yes / not yet\nAnything on this page to change (name it and say what):\nVideo 1 first minute, anything to change:\nAnything else:\n"
h += ["<h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(a,id){var v=document.getElementById('player');v.src=a.getAttribute('href');document.getElementById('docklabel').textContent=id+' in context';v.play();return false;}</script></main>"]
txt = "\n".join(h); open(f"{O}/index.html", "w").write(txt); print("page written; em dashes:", txt.count(chr(8212)), "en dashes:", txt.count(chr(8211)))
