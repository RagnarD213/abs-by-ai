"""RO-07 round 1b: a short page to lock colour and voice sound (Dan rejected both on the round 1 first minute).
Writes round1b/index.html. Serve with _shared/review_server.py 8858 round1b."""
import json, os, html
W = "/Volumes/Extreme/_edit_work/ro07"; O = f"{W}/round1b"; e = html.escape
AUD = [
 ("4-warm-less-room", "4. Warm, less kitchen echo (recommended)", "A gentle tone shape (a little more body, less boxiness, the top end left alone) plus a light pass that takes some of the room echo off. Nothing gates between words. A blind listen scored this 8 of 10, the best of the five."),
 ("3-warm", "3. Warm", "The same gentle tone shape, no echo removal. Scored 6 of 10: fuller, but the kitchen is still audible."),
 ("2-natural", "2. Natural", "The lav exactly as recorded, only the rumble below your voice removed. Scored 5 of 10."),
 ("1-as-delivered", "1. What you heard in the first minute", "The automatic tone match added 5 dB of treble and a gate chopped the ends of words. Scored 4 of 10. This is what went wrong."),
 ("5-other-microphone", "5. The other microphone (for comparison only)", "The second channel on the camera file: distant, thin, hissy. Scored 2 of 10. The first minute did NOT use this one."),
]
COL = [("D", "D: bright and natural (recommended)", "Brighter on your face, clean neutral wall, black tank top, a light noise clean-up. Skin close to the camera's own tone with a touch of warmth."),
       ("E", "E: bright, more contrast", "The same brightness as D with deeper shadows, more colour and a little added crispness."),
       ("B", "B: brighter (from round 1)", "Brighter than what you saw, skin exactly as the camera saw it (pinker), no noise clean-up."),
       ("C", "C: what you saw in the first minute", "Darker and more orange. Rejected; here only so you can see the difference.")]
css = """body{font:15px/1.5 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1240px;margin:0 auto 60px;padding:0 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}.muted{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}video{width:100%;border-radius:10px;background:#000}audio{width:100%;margin-top:6px}
textarea{width:100%;height:120px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}a{color:#8fd0ff}"""
h = [f"<!doctype html><meta charset='utf-8'><title>RO-07 colour and sound</title><style>{css}</style><main>",
     "<h1>Why You MUST Work Out Every Day: lock the colour and the sound</h1>",
     "<p class='muted'>The first minute you watched used colour C and voice option 1. Both are replaced below. Pick one colour and one voice; everything else you asked for goes into the next build.</p>",
     "<h2>Colour: all four at once</h2><p class='muted'>The same 16 seconds (camera frame, then the punch-in). Top row: C (what you saw), B. Bottom row: D, E. Each one is labelled in its corner.</p>",
     "<video controls preload='none' poster='colour/option-D.jpg' src='colour/grid-all-four.mp4'></video>",
     "<p class='muted'>For VLC, full size, one after another (C, B, D, E): <b>Videos to Review / Work Out Every Day LFC R1 - colour options C B D E.mp4</b></p>",
     "<h2>Colour: each option full size</h2><div class='grid'>"]
for k, name, what in COL:
    h.append(f"<div class='dec'><b>{e(name)}</b><br><span class='muted'>{e(what)}</span><video controls preload='none' poster='colour/option-{k}.jpg' src='colour/option-{k} - REVIEW 720p.mp4'></video><a href='colour/option-{k}.mp4'>Full 1080p file</a></div>")
h += ["</div><h2>Voice: the same 31 seconds, five ways</h2><p class='muted'>All five are matched in loudness. The microphone: the first minute used the lav (channel 2 of the camera file). I checked it three ways after your note: it is 14 dB cleaner than the other channel on every clean stretch, seven of the nine rolls from that day were logged the same way, and a blind listen picked it as the lav. Option 5 is the other microphone so you can hear the difference. The bad sound came from my processing, not from the microphone.</p>"]
for k, name, what in AUD:
    h.append(f"<div class='dec'><b>{e(name)}</b><br><span class='muted'>{e(what)}</span><audio controls preload='none' src='audio/{k}.mp3'></audio></div>")
reply = "RO-07 colour and sound\nColour: D\nVoice: 4\nNotes:\n"
h += ["<h2>Your reply</h2>", f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("page 1b written; em dashes:", "\n".join(h).count(chr(8212)))
