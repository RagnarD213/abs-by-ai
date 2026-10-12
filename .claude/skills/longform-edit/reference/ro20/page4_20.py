"""RO-20 round 3 page (2026-10-12, execution session): only what is new. Video 1's opening with the T3 intro and the J1 take, J2 in context,
video 1's sign-off, the pickup screens on placeholder timing, and the pickup re-record. Writes round3/index.html (the earlier intro-ideas
page is kept as round3/intro-ideas.html). Serve: _shared/review_server.py 8868 /Volumes/Extreme/_edit_work/ro20/round3"""
import os, html
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round3"; e = html.escape
css = open(f"{W}/recipe/page2_20.py").read().split('css = """')[1].split('"""')[0]
def vid(p, cap, full=None):
    if not os.path.exists(f"{O}/{p}"): return "<p class='muted'>(not built yet)</p>"
    return f"<video class='big' controls preload='none' src='{e(p)}' style='width:100%;max-width:960px;border-radius:8px;background:#000'></video><p class='muted'>{cap}" + (f" <a href='{e(full)}'>Full 1080p file</a>" if full else "") + "</p>"
DEC = [
 ("Re-record the four pickups", "The recording from this morning cannot be used: the program that captured it dropped about 1 in every 7 slices of sound. A blind listener scored the best repair 2 out of 10 against 9 for your kitchen voice. The lines are below. Tell me \"record\" and I start the mic with the recorder that does not drop audio (proved today: 45 minutes recorded with nothing lost); read each pickup twice.", ["Say \"record\" in the chat, then read P1 to P4 twice each"]),
 ("Video 1 sign-off: one sentence I ended early", "You said \"Once you see how amazing you look with six-pack abs, you'll be filled with motivation to make you happen\" and then restarted. I ended the sentence on \"filled with motivation.\" so the slip is gone, and the next sentence is your restart: \"Once you're motivated to make it happen, we have a variety of AI tools...\". Listen at 0:26 of the sign-off clip.", ["Keep it (recommended)", "Put the words back"]),
 ("Pickup screens: one swap", "No free stock clip of scissors cutting a credit card exists. Under \"In this video, I'll tell you exactly what to cut\" the window shows hands going through receipts and cash with a planner, the same picture as on the still you approved.", ["Keep the receipts clip (recommended)", "Make an AI clip of scissors cutting a card (needs frames first, video 2 budget)"]),
]
LINES = [
 ("P1, end of video 1", "In the next video, I'm going to tell you what you should cut to find that money, even if you're a brokie right now. In the video after that, I'll walk you through exactly what to buy for your health at every level, from dead broke to mega baller."),
 ("P2, start of video 2 (after your on-camera \"too cheap with your health\" line)", "In the last video, I told you why you need to spend more on your health. Being in shape makes you more money and more productive, and bad health is ludicrously expensive. In this video, I'll tell you exactly what to cut, so you can spend more money on your health."),
 ("P3, end of video 2", "That's what to cut. Now you have the money. In the next video, I'll walk you through exactly what to buy for your health at every income level, from dead broke to baller. To take the first step to getting in shape, go to AbsByAI.com. Upload a picture of yourself, and AI makes a picture of you with ripped six-pack abs, for free. Thanks for watching guys, I'll see you in the next video."),
 ("P4, start of video 3", "Here's exactly what you should be buying for your health, whether you're dead broke, middle class, or making over $10,000 a month. You need to be spending more money on your health no matter how little you have right now. Because money does you no good if you're dead or if you're sick. The last video covered what to cut to find the money. Now let's spend it."),
]
DECIDED = [
 "Piggy bank intro: one take, used from its first quarter second and played 12 percent faster so the finished title holds on screen for about 2.4 seconds before you appear. The letters are the AI's own and are spelled right in every frame I read; nothing was laid in by me. The pig keeps its shape (no melting). Label: AI-GENERATED, top right, clear of the title.",
 "Job interview clip: take 3. In take 1 the interviewer shook the heavy man's hand first; one prompt was refused by the provider's filter (no charge). In this take the heavy man stays seated with his hands on the table the whole time and only the fit man gets the handshake.",
 "Partnership clip: take 3. In takes 1 and 2 the heavy man joined the handshake. This take starts on your approved END frame (the handshake already happening) so he has no turn: he looks over, then down at his coffee. The contract being handed over is no longer seen.",
 "The fat guy who has money is the silent version you approved. Nothing else in video 1's first minute changed.",
 "Voice: the new standing rule adds a subtle bass lift to your voice, less when a voice already measures full. This roll's voice 4 already reads slightly above the reference voice in the lowest band (5.9 against 5.4), so I added nothing: voice 4 is exactly as you locked it.",
 "Video 1 sign-off: the roll's other closing take, 60 seconds. Three restarts came out (the stray \"Not,\", the \"variety of AI tools with you\" restart, the \"custom meal print\" restart). Each join is hidden by a change of framing size or by the app demo. It carries the same kind of lower thirds and the same approved app demo as video 3's ending. Nothing in the existing 53 minutes moved (checked shot by shot and word by word).",
 "Pickup screens: built from your approved picture lists and driven by the words of the recording, so they re-time themselves to the new takes. The versions on this page are silent and use the old recording's timing. In P2's window the boardroom clip will show the handshake part of the take. On P1, row 3 lights with no tag while you say \"the video after that\".",
 "Not on this page yet, because they need the pickups: the first minute of video 2 (your on-camera line, then P2) and of video 3 (P4, then \"All right. So let me walk you through it\").",
 "Audio check on video 1's opening: 12 of 13 rows pass. The tone row fails (1.52 against 1.2), the known result of the fixed warm voice you chose by ear; I did not tune it.",
 "Spend: video 1 $7.39 of $12 (this round: intro $0.80, job interview $0.80, partnership $0.40 twice). Videos 2 and 3: $0.60 each.",
]
h = [f"<!doctype html><meta charset='utf-8'><title>Invest In Your Health LFC R3</title><style>{css}</style><main style='margin-right:28px'>",
     "<h1>Invest In Your Health, round 3: what is new</h1><div class='sub'>Video 1's new opening, the two job clips, video 1's ending, and the pickup screens. Everything else is locked and unchanged.</div>",
     f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, (t, why, opts) in enumerate(DEC, 1): h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
h.append("<h2>The pickup lines to read (each one twice)</h2>")
for t, l in LINES: h.append(f"<div class='dec'><b>{e(t)}</b><div class='copy' style='font-size:17px;line-height:1.5'>{e(l)}</div></div>")
h += ["<h2>Video 1: the first 77 seconds</h2>",
      vid("first-minute/DRAFT - RO-20 round 3 - video 1 first minute - REVIEW 540p.mp4", "New: the piggy bank intro (0:00 to 0:07) and the job interview clip (1:01 to 1:08). The fat guy at 0:20 is the version you approved.", "first-minute/DRAFT - RO-20 round 3 - video 1 first minute.mp4"),
      "<h2>Video 1: the partnership clip in context (1:17 to 1:39)</h2>", vid("context/J2-context - REVIEW 540p.mp4", "The clip is at 0:07 of this excerpt.", "context/J2-context.mp4"),
      "<h2>Video 1: the ending</h2>", vid("context/v1-signoff - REVIEW 540p.mp4", "The on-camera sign-off, 60 seconds. Pickup P1 (\"In the next video...\") plays right before it once it is recorded.", "context/v1-signoff.mp4"),
      "<h2>The pickup screens (silent, placeholder timing)</h2><div class='grid2'>"]
for p, cap in (("P1", "End of video 1"), ("P2", "Start of video 2, after your on-camera line"), ("P3", "End of video 2"), ("P4", "Start of video 3")):
    f = f"pickups/placeholder_{p} - REVIEW 540p.mp4"
    h.append(f"<div class='card'><video controls preload='none' src='{e(f)}' style='width:100%;display:block;background:#000'></video><div class='b'><span class='id'>{p}</span> {e(cap)}</div></div>")
h += ["</div><h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>",
      "<p class='muted'>Earlier page with the three intro ideas: <a href='intro-ideas.html'>intro-ideas.html</a>. Round 2 page: port 8864.</p></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("wrote", f"{O}/index.html")
