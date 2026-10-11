"""RO-07 round 3 review page: the full film on top, then the three revisions with their timestamps and a short context clip
each, the three items Dan left blank (handoff defaults used), what I decided, the checks stated plainly, a reply box.
Facts that come from the checks are read from round3/page_facts.json. Writes round3/index.html.
Serve: python3 .claude/skills/_shared/review_server.py 8860 /Volumes/Extreme/_edit_work/ro07/round3"""
import json, html
W = "/Volumes/Extreme/_edit_work/ro07"; O = f"{W}/round3"; e = html.escape
F = json.load(open(f"{O}/page_facts.json"))
FILM = "RO-07 round 3 - full film"
REV = [
 ("1. Opener, the handstand push-ups", "0:02 to 0:04", "watch 0:00 to 0:08", "opener-handstand",
  "Before: the piece opened on you holding the handstand for two seconds. Now: you are already lowering on its first frame, you finish that rep and start the next one before the cut to the decline push-up.",
  "Re-cut from the camera roll (the same crop and colour as the library clip). I measured your height on every frame: you hold still until 15.9 s of the roll, so the piece now starts at 15.95 s. It plays at 1.2x so one whole rep and most of the next descent fit in its two seconds. The jump rope and the decline push-up are untouched."),
 ("2. C31, the AI deadlift before the stairs clip", "2:24 to 2:27", "watch 2:19 to 2:36", "C31-deadlift",
  "Before: he gripped the bar and the clip cut away before it moved. Now: the bar comes off the floor in the first half second, he pulls it up and stands tall with it, then the stairs clip.",
  "Same library clip, started 2.9 s in. That clip turns into a frozen picture at 6.25 s, with the red X drawn over the frozen picture later, so my cut is one frame before the freeze. Neither the freeze nor the X is in the film (checked frame by frame, twice)."),
 ("3. A3, life punches you in the face", "4:57 to 5:00", "watch 4:50 to 5:06", "A3-punch",
  "Before: a placeholder (the two frames you approved). Now: the moving clip. He pulls the front door open, the giant glove on the spring shoots in from outside and knocks him off his feet. The glove lands as you say \"punch\".",
  "One 6 second take from your approved frames ($0.60). I use its first 3.4 seconds: in the last 2 seconds he hangs in the air at the end frame, which reads as a freeze, so the clip cuts back to you while he is still falling. Because of that the clip now starts on \"once you start working out\" (4:57), not on \"And I guarantee you\" (4:55), and you are on camera for that first second and a half."),
]
EXTRA = [
 ("Push-up cutaway, a crew member in the picture", "10:08 to 10:15", "watch 10:05 to 10:19", "C37-pushups",
  "In the low-angle push-up clip under \"5 Minutes. Bodyweight. At Home.\" someone from the crew stood at the left edge looking into the camera, next to a gold reflector. The clip is the same one you saw in round 2; it is now cropped about 10 % so he and the reflector are out of the picture. You are whole in frame through every rep. Half a white bucket is still at the left edge."),
 ("Three mouth clicks in pauses, turned down", "11:01, 11:18, 13:58", "listen 11:15 to 11:21", None,
  "Before \"Well,\", before \"What I recommend\" and before \"One detail\". The one at 11:18 was as loud as your voice. Each is a 60 millisecond spot in a pause; no word is touched, and the rest of the sound is sample for sample the same as before."),
]
BLANK = [
 ("Length", "Kept 18:07 as cut. Nothing was trimmed. If you want the 16:50 version, say so and I apply the five trims and show you the first minute again."),
 ("Gymboss", "Lower thirds only (13:22 and 13:31), as built. No screen recording arrived, and I do not fake the app."),
 ("Music", f"Quiet bed added under your voice, the same track as the home workout video. {F['bed']}"),
]
DECIDED = [
 "Everything else in the film is exactly what you saw in round 2. Every shot is held at the same size and crop as the round 2 build, every lower third is the same render (the graphics file is byte for byte unchanged), and the voice is the round 2 voice apart from the three click spots.",
 "The handstand piece runs at 1.2x. At normal speed its two seconds would end on you holding at the top again.",
 "A3 is shorter than its old slot (3.4 s, was 4.6 s) so the freeze at the end of the take never appears. I did not buy a second take: nothing in the part I use shows at speed.",
 "The crew member crop and the three click spots were not in your notes. An independent review found them on the first render of this film and I fixed them in the same pass. Say so if you want either put back.",
 "Subtitles are a separate file (no burned captions), proofread against the finished sound, with 17 chapters for YouTube. Both are in the delivery folder.",
 f"Spend on this video: {F['spend']}",
]
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1100px;margin:0 auto 60px;padding:0 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}
.rev{display:grid;grid-template-columns:480px 1fr;gap:16px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:14px;margin:12px 0}.rev video{width:100%;border-radius:8px;background:#000}
.ts{display:inline-block;background:#1f7a4d;color:#fff;border-radius:5px;padding:1px 8px;font-weight:700;margin-right:6px}.muted{color:#9fb2cc}
textarea{width:100%;height:210px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li,ul li{margin:5px 0}a{color:#8fd0ff}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}
@media(max-width:900px){.rev{grid-template-columns:1fr}}"""
h = [f"<!doctype html><meta charset='utf-8'><title>RO-07 round 3: full film</title><style>{css}</style><main>",
     "<h1>Why You MUST Work Out Every Day: round 3, the full film</h1>",
     f"<div class='sub'>Long-form content, 16:9, {F['length']}. Your three round 2 changes are in. Nothing is pending: this is the finished film.</div>",
     "<h2>The full film</h2>", f"<video class='big' controls preload='none' poster='{FILM}.jpg' src='{FILM} - REVIEW 540p.mp4'></video>",
     f"<p class='muted'><a href='{FILM}.mp4'>Full 1080p file</a> &nbsp; <a href='RO07.srt'>Subtitles</a> &nbsp; <a href='RO07.chapters.txt'>Chapters</a> &nbsp; <a href='RO-07 audio AB (reference then ours).mp4'>Audio A/B against the reference voice</a><br>"
     "Also in the project folder for VLC: <b>Videos to Review / Work Out Every Day LFC R3 - full film.mp4</b></p>",
     "<h2>The three changes, with where to look</h2><p class='muted'>You do not need to watch the whole film again for these. Each has a short clip cut from the finished film.</p>"]
for t, ts, watch, clip, what, how in REV:
    h.append(f"<div class='rev'><video controls preload='metadata' src='context/{clip} - REVIEW 540p.mp4'></video><div><b>{e(t)}</b><br><span class='ts'>{ts}</span><span class='muted'>{watch}</span>"
             f"<p>{e(what)}</p><p class='muted'>{e(how)}</p></div></div>")
h.append("<h2>Two more fixes, found by the independent review</h2>")
for t, ts, watch, clip, what in EXTRA:
    v = f"<video controls preload='metadata' src='context/{clip} - REVIEW 540p.mp4'></video>" if clip else "<div class='muted' style='padding:20px'>Sound only: play the full film at the times shown.</div>"
    h.append(f"<div class='rev'>{v}<div><b>{e(t)}</b><br><span class='ts'>{ts}</span><span class='muted'>{watch}</span><p>{e(what)}</p></div></div>")
h.append("<h2>The three things you left blank: I used the handoff defaults</h2>")
for t, s in BLANK: h.append(f"<div class='dec'><b>{e(t)}.</b> {e(s)}</div>")
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += ["<h2>The checks, stated plainly</h2><ul>"] + [f"<li>{e(d)}</li>" for d in F["checks"]] + ["</ul>"]
if F.get("flags"): h += ["<h2>Existing flags, unchanged from round 2 (not new). One needs your word</h2><ul>"] + [f"<li>{e(d)}</li>" for d in F["flags"]] + ["</ul>"]
reply = "RO-07 round 3\nFinalize it (yes / no):\n1. Handstand piece (0:02):\n2. C31 deadlift (2:24):\n3. A3 punch (4:57):\nPush-up clip crop (10:08):\nLength (18:07 kept):\nGymboss (lower thirds kept):\nMusic (quiet bed added):\nHair at the top edge (leave as shot / add headroom):\nAnything else:\n"
h += ["<h2>Your reply</h2>", f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button></main>"]
s = "\n".join(h); assert chr(8212) not in s and chr(8211) not in s
open(f"{O}/index.html", "w").write(s); print("page written", len(s))
