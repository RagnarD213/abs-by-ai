"""RO-20 round 3 mini page (Dan's reply to round 2, 2026-10-12): the title-intro concepts as START and END frames, the working
A1, and the open choices. Writes round3/index.html. Serve: _shared/review_server.py 8865 /Volumes/Extreme/_edit_work/ro20/round3"""
import os, html
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round3"; e = html.escape; os.makedirs(f"{O}/frames", exist_ok=True)
for j in ("T1", "T2", "T3"):
    for se in ("start", "end"): Image.open(f"{W}/aiframes/{j}-{se}.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{O}/frames/{j}-{se}.jpg", quality=90)
css = open(f"{W}/recipe/page2_20.py").read().split('css = """')[1].split('"""')[0]
DEC = [
 ("The intro graphic for video 1", "Three ideas for a full-screen title made as an AI video, each as a START and END frame below. It plays under your first sentence (0:00 to 0:06), then you are on camera for \"The first reason is the halo effect\". Motion is one 8 second take, $0.80, made only for the one you pick.", ["T1 the vault (recommended)", "T2 the health chart", "T3 the piggy bank", "None, stay with the camera open"], "T1"),
 ("The fat guy who has money (0:20)", "You were right: I measured the mouth against your recording and the lips did not follow your words. I tried three fixes and the sync tool will not drive this character's mouth (details under What I decided). The working version on this page has no mismatch because his mouth stays shut: he smirks, pats the cash and shrugs while your voice does the line, the way the brokie clip works. Or I try a different lip-sync tool, which needs the budget in decision 3.", ["Try one different lip-sync tool, fall back to the silent version (recommended)", "Keep the silent version"], "try one different tool"),
 ("Budget for video 1", "Video 1 has used $4.99 of its $5.00. Still to make: retakes of the two job clips ($1.20, the first takes got the story wrong), the intro you pick ($0.80), one more lip-sync try (up to $1.50) and one spare retake ($0.80). That takes video 1 to about $9.30. Videos 2 and 3 have used $0.60 each.", ["Raise video 1's cap to $10 (recommended)", "Hold at $5: no intro motion, no job clip retakes, silent version stays"], "raise to $10"),
]
IDEAS = [
 ("T1", "The vault", "A bank vault door swings open. Inside, where the gold would be, the shelves are stacked with chrome dumbbells and kettlebells, and the title glows in the middle. The door hides the title until it opens, so no letters have to form on screen: the cleanest of the three for AI video."),
 ("T2", "The health chart", "A red stock line crashes beside a cracked heart. It turns into a green line with a heartbeat spike that rockets up, the heart heals, and the title lands. The most graphic of the three. The title would be laid in by me so the letters stay sharp."),
 ("T3", "The piggy bank", "A coin drops into a plain piggy bank on a gym bench. It stands up jacked, flexes, coins burst out, and the title lands beside it. The funniest of the three; a ceramic pig changing shape is also the hardest for the AI to do without it looking like it is melting."),
]
DECIDED = [
 "Job clips: both first takes are rejected, not shown. In the boardroom take the interviewer shakes the heavy man's hand for three seconds before the fit man's, which tells the opposite story. In the golf terrace take the heavy man joins the handshake. Your approved frames stand; the retakes get tighter direction (the heavy man never stands, never reaches). They wait on decision 3.",
 "Lip sync, what I tried ($1.53): (1) the same take with the face sent to the tool twice as large: no better. (2) A new take where he keeps his mouth shut, on the idea that the tool works best from a still mouth: the tool was set to find the active speaker, found none and did nothing. (3) The same with that setting off, on the 2.5 seconds around 0:26: his mouth still stayed shut. A different tool is the next thing to try.",
 "The round 2 lip sync I sent you had not been judged at speed by anyone, and I said so; I now measure every synced clip against the audio before it goes on a page (mouth opening against the speech, frame by frame).",
 "The new silent take is made from your approved START frame only. He ends in the same shrug as your approved END frame, but smirking with his mouth shut instead of laughing.",
 "The intro title wording is yours: Why You Need To Invest More In Your Health.",
 "Round 2, decision 3: you did not overrule it, so video 2 opens on camera with your own take of the hook.",
 "Everything else you approved on the round 2 page is locked: the pickup scripts, the two dating graphics, the three-part card, the three-levels card, the brokie and cardboard box clips, and the B-roll colour.",
 "Spend, all three videos: $6.19 (video 1 $4.99, video 2 $0.60, video 3 $0.60).",
]
h = [f"<!doctype html><meta charset='utf-8'><title>Invest In Your Health LFC R3</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Press a button to play</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>Invest In Your Health, round 3: your round 2 notes</h1><div class='sub'>Only what is new: three intro ideas, the fat guy clip, and where the job clips stand.</div>",
     "<p><b>Already locked and reused:</b> everything on the round 2 page you did not flag.</p>", f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, (t, why, opts, rec) in enumerate(DEC, 1): h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
h.append("<h2>The intro: three ideas, START and END frames</h2>")
for j, name, act in IDEAS:
    h.append(f"<div class='dec'><b>{j}. {e(name)}.</b> {e(act)} 8 second take, $0.80. Label: AI-GENERATED.<div class='pair'><div><img loading='lazy' src='frames/{j}-start.jpg'>START</div><div><img loading='lazy' src='frames/{j}-end.jpg'>END</div></div></div>")
p = "context/A1-context - REVIEW 540p.mp4"
h += ["<h2>The fat guy who has money: the working version</h2>",
      (f"<video class='big' controls preload='none' src='{p}'></video><p class='muted'>0:15 to 0:31 of video 1. He keeps his mouth shut and your voice does the excuse. <a href='context/A1-context.mp4'>Full 1080p clip</a></p>" if os.path.exists(f"{O}/{p}") else "<p class='muted'>(still rendering)</p>"),
      "<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += ["<h2>Recording the pickups: the easy way</h2><ol>",
      "<li>On your iPhone, open <b>Voice Memos</b>. One time only: Settings, Voice Memos, Audio Quality, choose Lossless.</li>",
      "<li>Stand in a closet with clothes in it, or any quiet soft room. Hold the phone about a hand's width from your mouth, a little to the side.</li>",
      "<li>Make <b>one recording</b> for all four. Say \"P1\", read it, read it a second time, then \"P2\", and so on. No need to stop between them or name files: I cut it up and pick the best take of each.</li>",
      "<li>Getting it to me: <b>AirDrop the recording to this Mac</b> (Share, AirDrop, your Mac). It lands in Downloads and I pick it up from there. If your Voice Memos sync to this Mac through iCloud it will also just appear here, and I can read that folder already, but its newest recording is from January, so AirDrop is the sure way.</li>",
      "<li>Tell me \"pickups are in\" in the round 3 session.</li></ol>",
      "<p class='muted'>The phone is fine. I match the level and tone to the kitchen voice, and each pickup plays over pictures and a quiet music bed, which hides a small difference in the room.</p>"]
reply = "Invest In Your Health LFC R3\n" + "\n".join(f"{i}. {t}: {rec}" for i, (t, why, opts, rec) in enumerate(DEC, 1)) + "\nAnything to change:\n"
h += ["<h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, then copy and paste it to me.</p>",
      f"<textarea id='reply' style='height:170px'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button></main>"]
txt = "\n".join(h); open(f"{O}/index.html", "w").write(txt); print("page written; em dashes:", txt.count(chr(8212)), "en dashes:", txt.count(chr(8211)))
