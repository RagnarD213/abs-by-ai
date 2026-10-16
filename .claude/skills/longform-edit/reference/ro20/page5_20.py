"""RO-20 round 3b page (2026-10-16): the four pickups re-recorded on the shoot lav (roll C1722) in video 2's and video 3's first minutes and video 1's
ending, an A/B of the two pickup treatments on the three joins, and the sign-off question again. Writes round3/index.html (the 10-13 page is kept as
round3/index-r3-desk.html). Serve: _shared/review_server.py 8868 /Volumes/Extreme/_edit_work/ro20/round3"""
import os, html, json
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round3"; e = html.escape
css = open(f"{W}/recipe/page2_20.py").read().split('css = """')[1].split('"""')[0]
G = json.load(open(f"{W}/round3b/gate_summary.json"))
def vid(p, cap, full=None):
    if not os.path.exists(f"{O}/{p}"): return "<p class='muted'>(not built yet)</p>"
    return f"<video class='big' controls preload='none' src='{e(p)}' style='width:100%;max-width:960px;border-radius:8px;background:#000'></video><p class='muted'>{cap}" + (f" <a href='{e(full)}'>Full 1080p file</a>" if full else "") + "</p>"
def aud(p): return f"<audio controls preload='none' src='{e(p)}' style='width:100%;max-width:460px'></audio>"
FM = "first-minute-3b/DRAFT - "
DEC = [
 ("Do the studio pickups sit with your kitchen voice", "Your four pickups are now from the shoot's clip-on mic (10/15 shoot, green screen set), the same mic as the film. Listen at 0:12 and 0:26 of video 2, 0:18 of video 3, and 0:16 and 0:29 of video 1's ending. Below the clips there is an A/B of the two treatments I tried on the same three joins.",
  ["Good, build the films with A (recommended)", "Use B", "Still noticeable: tell me where"]),
 ("Video 1 sign-off: one sentence I ended early", "You said \"you'll be filled with motivation to make you happen\" and then restarted. I ended the sentence on \"filled with motivation.\" Listen at 0:56 of the video 1 ending clip.", ["Keep it (recommended)", "Put the words back"]),
]
DECIDED = [
 "Takes, all from roll C1722 and all checked word for word against the scripts you approved: P1 the second take, P2 the FIRST take (the second drops \"makes you more money\" and stumbles), P3 the second take (the first restarts), P4 the second take. Every word you read is in; P3 says \"Thank you for watching\", your wording.",
 "A (used in the clips above): the lav with a gentle tone match to the film voice, cuts only (less low rumble around 100 Hz and less brightness around 5 kHz, because the mic sat closer on this shoot than in the kitchen), no added room sound, level matched to the film's speech. B: the film's own voice chain on the lav with no tone match.",
 f"Why A: a blind listener could not tell A and B apart (21 listens each: B {G['listen']['chain']}, A {G['listen']['match']} out of 10 for how noticeable the join is; the old desk mic scored 8 every time), so the measurements decided. With B, two clips fail the tone check (peaks of 2.9 dB) and both first minutes fail the processing check. With A: {G['summary']}.",
 "The room on the green screen set measures about as dry as your treated kitchen voice (56 ms against 52), so no echo removal was added to the pickups.",
 "Two words touch the mic's ceiling for a fraction of a millisecond (\"more\" in P2 and the first \"That's\" in P3). Not audible; left as is.",
 "Video 2 opens on camera with your own \"You need to be spending more money on your health...\" (12 seconds), then P2, then the film. Video 3 opens on the three-levels graphic and P4. Unchanged from 10-13.",
 "In the full films I will give \"All right. So let me walk you through it\" (right after P4) a short lead-in from the roll; it starts tightly here because it was a cut in the long film.",
 "Still not seen by you with sound: the partnership clip in video 1 and video 2's ending screens (P3, now with the new pickup). Both are below.",
 "Spend unchanged: video 1 $7.39 of $12; videos 2 and 3 $0.60 each. The blind listens cost under $1 of Gemini review.",
]
h = [f"<!doctype html><meta charset='utf-8'><title>Invest In Your Health LFC R3b</title><style>{css}</style><main style='margin-right:28px'>",
     "<h1>Invest In Your Health, round 3b: the studio pickups are in</h1><div class='sub'>New since your last look: all four pickups re-recorded on the shoot's clip-on mic, in the first minute of videos 2 and 3 and video 1's ending. Everything else is locked and unchanged.</div>",
     f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, (t, why, opts) in enumerate(DEC, 1): h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
h += ["<h2>Video 2: the first minute</h2>", vid(FM + "RO-20B round 3b - video 2 first minute - REVIEW 540p.mp4", "On camera 0:00 to 0:12, pickup P2 0:12 to 0:26, then the film.", FM + "RO-20B round 3b - video 2 first minute.mp4"),
      "<h2>Video 3: the first minute</h2>", vid(FM + "RO-20C round 3b - video 3 first minute - REVIEW 540p.mp4", "Pickup P4 0:00 to 0:18, then the film.", FM + "RO-20C round 3b - video 3 first minute.mp4"),
      "<h2>Video 1: the ending</h2>", vid(FM + "RO-20 round 3b - video 1 ending - REVIEW 540p.mp4", "The film to 0:16, pickup P1 0:16 to 0:29, then the on-camera sign-off (the sentence in decision 2 at 0:56).", FM + "RO-20 round 3b - video 1 ending.mp4"),
      "<h2>A/B: the two pickup treatments on the same joins (sound only)</h2><table><tr><th></th><th>A: tone matched (recommended, used above)</th><th>B: film chain only</th></tr>"]
for j, t in (("v2open", "Video 2 open: film, P2, film"), ("v3open", "Video 3 open: end of P4, film"), ("v1end", "Video 1 end: film, P1, sign-off")):
    h.append(f"<tr><td>{t}</td><td>{aud(f'listen-3b/match_{j}.mp3')}</td><td>{aud(f'listen-3b/chain_{j}.mp3')}</td></tr>")
h += ["</table>",
      "<h2>Video 2's ending screens (pickup P3)</h2>", vid("pickups/P3 - REVIEW 540p.mp4", "Plays after \"once you're there in a couple months.\" It ends on the three-part card with room for YouTube's end screen.", "pickups/P3.mp4"),
      "<h2>Video 1: the partnership clip in context (1:17 to 1:39)</h2>", vid("context/J2-context - REVIEW 540p.mp4", "The clip is at 0:07 of this excerpt.", "context/J2-context.mp4"),
      "<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>",
      "<p class='muted'>Approved on 10-13 and unchanged: video 1's first 77 seconds (<a href='first-minute/DRAFT - RO-20 round 3 - video 1 first minute.mp4'>file</a>). The 10-13 desk-mic page: <a href='index-r3-desk.html'>index-r3-desk.html</a>. Intro ideas: <a href='intro-ideas.html'>intro-ideas.html</a>.</p></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("wrote", f"{O}/index.html")
