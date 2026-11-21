"""RO-20 round 3 page (2026-10-13 update): the first minutes of videos 2 and 3 and video 1's ending with the re-recorded pickups, plus what
round 3 already showed. Writes round3/index.html (the earlier intro-ideas page is round3/intro-ideas.html).
Serve: _shared/review_server.py 8868 /Volumes/Extreme/_edit_work/ro20/round3"""
import os, html
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round3"; e = html.escape
css = open(f"{W}/recipe/page2_20.py").read().split('css = """')[1].split('"""')[0]
def vid(p, cap, full=None):
    if not os.path.exists(f"{O}/{p}"): return "<p class='muted'>(not built yet)</p>"
    return f"<video class='big' controls preload='none' src='{e(p)}' style='width:100%;max-width:960px;border-radius:8px;background:#000'></video><p class='muted'>{cap}" + (f" <a href='{e(full)}'>Full 1080p file</a>" if full else "") + "</p>"
FM = "first-minute/DRAFT - "
DEC = [
 ("Does the pickup voice sit with your kitchen voice", "The pickups were recorded on your desk mic, the film on the shoot's clip-on mic in the kitchen. I matched tone, level and room sound, and the measured rows pass (12 of 13; the 13th needs the full film). A blind listener still hears the change at each join: it calls the pickup closer, drier and fuller. Listen at 0:12 and 0:26 of video 2 and 0:17 of video 3. The finished films carry a quiet music bed, which hides some of it.", ["Good enough, build the films", "Not good enough: I re-record the four pickups standing in the kitchen doorway on the shoot's clip-on mic"]),
 ("Video 1 sign-off: one sentence I ended early", "You said \"you'll be filled with motivation to make you happen\" and then restarted. I ended the sentence on \"filled with motivation.\" Listen at 0:56 of the video 1 ending clip.", ["Keep it (recommended)", "Put the words back"]),
]
DECIDED = [
 "Pickups: the 10-13 recording is clean (166.20 seconds captured in 166.23, no dropped or doubled blocks). I used the second take of each. For P3 the first sentence is from take 1, because \"That's what to cut\" was slurred in take 2.",
 "You read P1 as \"And in the video after that\" and P2 as \"and it makes you more productive\": your wording is in.",
 "Video 2 opens on camera with your own \"You need to be spending more money on your health... no matter how little money you have\" (12 seconds, no graphics), then P2, then \"But I know at this point in the video...\".",
 "Video 3 opens straight on the three-levels graphic, as you asked (the shot of you standing by the pool is gone). Its title is alone on screen for about 3 seconds until \"dead broke\".",
 "P2's window shows the handshake part of the job interview clip under \"makes you more money\". The clip is 0.04 seconds shorter than its slot, so the window closes a hair early; nothing is slowed or frozen.",
 "Pickup voice treatment: low rumble removed, tone matched to the film voice in third-octave steps (mostly cuts), a little room sound added, level set 1 dB under the film's speech level, the kitchen's own room tone laid underneath, peaks held under the film's. Chosen from five versions by a blind listener; two more passes did not change its verdict on the joins.",
 "Still to fix in the full films: \"All right. So let me walk you through it\" starts very tightly after P4 (it was a cut in the long film); I will give it a short lead-in from the roll.",
 "Approved by you on 10-13 and unchanged: video 1's first 77 seconds (piggy bank intro, job interview clip) and the pickup screens.",
 "Not yet seen by you in motion: the partnership clip (video 1, 1:25), below.",
 "Audio rows on the two first minutes: 12 of 13 pass on each, tone included. The one that fails is \"do no harm: not measured\", because a joined review clip has no untreated baseline; the full films will.",
 "Spend unchanged: video 1 $7.39 of $12; videos 2 and 3 $0.60 each.",
]
h = [f"<!doctype html><meta charset='utf-8'><title>Invest In Your Health LFC R3</title><style>{css}</style><main style='margin-right:28px'>",
     "<h1>Invest In Your Health, round 3: the pickups are in</h1><div class='sub'>New since your last look: the first minute of videos 2 and 3, and video 1's ending. Everything else is locked and unchanged.</div>",
     f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, (t, why, opts) in enumerate(DEC, 1): h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
h += ["<h2>Video 2: the first minute</h2>", vid(FM + "RO-20B round 3 - video 2 first minute - REVIEW 540p.mp4", "On camera 0:00 to 0:12, pickup P2 0:12 to 0:26, then the film.", FM + "RO-20B round 3 - video 2 first minute.mp4"),
      "<h2>Video 3: the first minute</h2>", vid(FM + "RO-20C round 3 - video 3 first minute - REVIEW 540p.mp4", "Pickup P4 0:00 to 0:17, then the film.", FM + "RO-20C round 3 - video 3 first minute.mp4"),
      "<h2>Video 1: the ending</h2>", vid(FM + "RO-20 round 3 - video 1 ending - REVIEW 540p.mp4", "The film to 0:16, pickup P1 0:16 to 0:28, then the on-camera sign-off.", FM + "RO-20 round 3 - video 1 ending.mp4"),
      "<h2>Video 2's ending screens (pickup P3)</h2>", vid("pickups/P3 - REVIEW 540p.mp4", "Plays after \"once you're there in a couple months.\" It ends on the three-part card with room for YouTube's end screen.", "pickups/P3.mp4"),
      "<h2>Video 1: the partnership clip in context (1:17 to 1:39)</h2>", vid("context/J2-context - REVIEW 540p.mp4", "The clip is at 0:07 of this excerpt.", "context/J2-context.mp4"),
      "<h2>Approved on 10-13: video 1, the first 77 seconds</h2>", vid("first-minute/DRAFT - RO-20 round 3 - video 1 first minute - REVIEW 540p.mp4", "Unchanged.", "first-minute/DRAFT - RO-20 round 3 - video 1 first minute.mp4"),
      "<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>",
      "<p class='muted'>Earlier page with the three intro ideas: <a href='intro-ideas.html'>intro-ideas.html</a>. Round 2 page: port 8864.</p></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("wrote", f"{O}/index.html")
