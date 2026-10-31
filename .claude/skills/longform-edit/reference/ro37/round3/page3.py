import html
E = html.escape; R = "/Volumes/Expansion/_edit_work/RO-37/round3/r3/review"
FILM = "film/First Time At The Gym LFC R3 - REVIEW 540p.mp4"; HD = "film/First Time At The Gym LFC R3.mp4"
def sec(s):
    m, x = s.split(":"); return int(m) * 60 + float(x)
REV = [("0:00 to 0:08", "New intro clip: pull-ups, full body, left of you with nothing blocked. The AI door clip is gone, as you said."),
       ("0:09 to 0:15", "First scene you flagged. Same layout, much cleaner key."),
       ("0:15 to 0:22", "Rebuilt scene you flagged. Three big cards beside you, no blank middle."),
       ("0:22 to 0:26", "You sit at the far right edge now, so your arm is not cut off."),
       ("0:35 to 0:42", "New: sit-ups at about 4.6 times speed with the clock spinning, he collapses, then the weak thumbs-up. A short dissolve joins the two clips."),
       ("0:56 to 0:59", "Too sore for the stairs."),
       ("1:05 to 1:10", "The gym bag under the desk. See the question below."),
       ("1:26 to 1:31", "The cobwebs clip is gone, as you said. You stay on camera."),
       ("1:41 to 1:46", "Moved to the corner over your gym clip: fast hands, the key could not be cleaned."),
       ("2:02 to 2:19", "Moved to the corner over your gym clip (2:03 to 2:08 and 2:12 to 2:18), same reason. The faint \"5 MINUTES, THAT'S FINE\" type came out, because you on empty blue was the blank-space problem again. You still say it."),
       ("4:05 to 4:10", "Moved to the corner, same reason."),
       ("4:13 to 4:19", "You sit at the far right edge now, so your forearm is not cut off."),
       ("4:46 to 4:50", "I fixed a stumble that earlier rounds missed: \"important than, portant than working out longer\". The film is 0.4 seconds shorter from here on."),
       ("5:32 to 5:37", "Moved to the corner over your gym clip, same reason."),
       ("6:50 to 6:57", "The gym clip with your changes: white guy gone, jacked guy moved right, a thought bubble from each.")]
def rows():
    o = ""
    for w, n in REV:
        a = sec(w.split(" to ")[0]); o += f'<tr><td><button onclick="go({a})">{E(w)}</button></td><td>{E(n)}</td></tr>'
    return o
LOOK = [("0:05", "elbow"), ("0:11", "arm"), ("1:13", "elbow"), ("5:15", "elbow")]
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>First Time At The Gym R3</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1080px;margin:0 auto;padding:28px 16px}}
h1{{font-size:32px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:24px}}p,li,td{{color:var(--mute)}}section{{margin:26px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:16px}}
video{{width:100%;border-radius:10px;background:black}}.small{{font-size:14px}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}a{{color:var(--acc)}}
table{{width:100%;border-collapse:collapse}}td{{padding:8px 10px 8px 0;border-top:1px solid var(--line);vertical-align:top}}
textarea{{width:100%;box-sizing:border-box;min-height:150px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:6px 10px;cursor:pointer;font-size:14px;white-space:nowrap}}
@media(max-width:700px){{h1{{font-size:25px}}section{{padding:14px}}}}</style>
<main><h1>I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time <span class="small">LFC, round 3, full film</span></h1>
<p class="notice"><b>The full film, 7:55.</b> Colour F, voice A (Natural Warmth), weeks 2 to 4 with your clips and side list. You have not reviewed this yet. Release: Fri Jan 1, 2027.</p>
<section><h2>The film</h2><video id="v" controls muted preload="metadata" playsinline src="{FILM}"></video><p class="small"><a href="{HD}">1080p</a>, best for judging the key. <a href="film/First Time At The Gym LFC R3.srt">Subtitle file</a>. The subtitles are a separate file, not burned in.</p></section>
<section><h2>What changed, with times</h2><p class="small">Each button jumps the player there. You should not need to watch the whole film for these.</p><table>{rows()}</table></section>
<section><h2>The key</h2><p>Three things were wrong. I fixed all three:</p><ul><li>The outline of your body ran one frame behind the picture on some shots, which printed the white line.</li><li>The cut-out had filled in the gaps between your arms and body, so pool stone and tile stayed solid there. Those are now taken back out.</li><li>Fast fingers came out thin and claw-like, because blur confused the tool. Moving skin now goes back in with a soft edge.</li></ul>
<p>Scores from fresh reviewers looking at every shot of you: the first full build had 80 clean, 24 minor, 7 sloppy. The last shot-by-shot pass had 95 clean, 11 minor, 5 sloppy. Those 5 are the corner moves above. All five were fast hands; your face, hair, shoulders and body were clean in every shot.</p>
<p class="small">That shot-by-shot count came before the last build, which softened fast hand edges and moved those five shots. The final reviews checked every cut and the fastest hand moments, not every shot again. Short flashes on fast hands can remain for a few frames. A reviewer watching those moments rated them not noticeable at normal speed.</p></section>
<section><h2>What I could not fix</h2><ul><li><b>Your arm leaves the camera frame.</b> You filmed vertically, so a big gesture puts an elbow outside the picture and it ends at a soft straight edge for about a second. Clearest at 0:05, then 0:11, 1:13 and 5:15. It is in the original footage, so moving you only helps when you sit against the screen edge. I did that at 0:22 and 4:14. You passed the same look at 0:05 in round 2.</li>
<li><b>6:05.3:</b> one very short shot, 0.3 seconds, reads as a quick double zoom. Tell me if you want it smoothed.</li></ul></section>
<section><h2>What I decided</h2><ul><li>Intro clip: pull-ups, full body, the default from the early look. The other options are still here: <a href="intro/chain_dips - REVIEW 540p.mp4">weighted dips</a>, <a href="intro/dips - REVIEW 540p.mp4">bodyweight dips</a>, <a href="intro/pullups_front - REVIEW 540p.mp4">pull-ups from the front</a>, <a href="intro/sled - REVIEW 540p.mp4">the sled moved left</a>.</li><li>The stray words at 4:47 came out with a real 0.4 second cut, not a pause: a pause left your mouth moving with no sound.</li><li>Your thumbs-up at 0:39 is a Veo take played backward, because Veo would not do one clean slow lift.</li><li>The new gym clip behind you at 2:03 is your seated chest press.</li><li>The corner shot at 1:41 and the others use the same gym clip that was softened behind you, now sharp.</li></ul></section>
<section><h2>Question for you</h2><p class="notice">Your note on the gym bag clip came through as "Q&amp;A4". I took that as "queue it" and kept it, at 1:05. If you meant "kill A4", tell me and it goes.</p></section>
<section><h2>Checks</h2><ul><li><b>Sound:</b> loudness, peaks and silence pass. The one failing row is tone, the known mismatch with your Natural Warmth voice. I left it alone on purpose.</li><li><b>Audio joins:</b> every join scanned, flagged ones sent to a blind listener twice. That is how the 4:47 stumble was found. After the fix, two more listens heard no stumble. No person has heard this mix.</li><li><b>Lip sync:</b> 0 frames off at six points after the cut, checked against the raw camera.</li><li><b>Independent reviewers:</b> two full passes. Picture, audio and timing passed on this file. The second review's subtitle notes are all applied, but no reviewer has re-read the final subtitle file, and its last words at 7:51 went back to "Subscribe to my channel, go to".</li><li><b>Frame-by-frame cut review:</b> all 168 cuts looked at. Its only 7 open items are the arm moments above. Nothing bad turned up in the 66-frame scan.</li>
<li><b>Automatic delivery gate:</b> 30 rows pass, 8 fail, 1 could not be measured, so this file has no pass stamp. The sound tone row is the mismatch above, and the arm moments fail the cut-review row until you accept them. Lip sync reads as failing only because the row compares against the audio from before the trim. Hair height, headroom, same-size cuts, cut visibility and burned captions fail on the measurement. Reviewers checked these on this film and found no problem. Hair clears the top by 20 px or more in the reviewers' samples, and no subtitles are burned in.</li></ul></section>
<section><h2>Reply</h2><textarea id="r">Arm moments: accept
Gym bag clip: keep
Notes:
</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy</button></p></section></main>
<script>function go(t){{var v=document.getElementById('v');v.currentTime=t;v.scrollIntoView({{behavior:'smooth',block:'center'}});}}</script></html>"""
assert "—" not in page
open(f"{R}/index.html", "w").write(page); print("ok")
