"""RO-08 round 2 review page: the two openers side by side at the head of the first minute, the full film, every AI clip moving in
context with its timestamp in the full film, the list of every change since round 1 with watch ranges, what I decided, the checks
stated plainly, one reply box. Facts that come from the checks are read from round2/page_facts.json (page_facts_r2.py).
Writes round2/index.html. Serve: python3 .claude/skills/_shared/review_server.py 8871 /Volumes/Extreme/_edit_work/ro08/round2"""
import json, html
W = "/Volumes/Extreme/_edit_work/ro08"; O = f"{W}/round2"; e = html.escape
F = json.load(open(f"{O}/page_facts.json")); R = {r["id"]: r for r in json.load(open(f"{W}/plan_resolved.json"))}
FILM = "RO-08 round 2 - full film"
FA = "first-minute/DRAFT - RO-08 round 2 - first minute - opener A time-lapse"; FB = "first-minute/DRAFT - RO-08 round 2 - first minute - opener B split screen"
def mmss(t): return f"{int(t//60)}:{int(t % 60):02d}"
def rng(i, pre=3, post=3): return f"{mmss(R[i]['t0'])} to {mmss(R[i]['t1'])}", f"watch {mmss(max(0, R[i]['t0']-pre))} to {mmss(R[i]['t1']+post)}"
AI = [  # id, context clip, title, what happens, editor's note
 ("A4", "A4", "A4. The man who has not eaten all day", "He stares at a coworker's sandwich, tucks a napkin in his collar, plants a knife and fork on the desk and leans in with his tongue out while the sandwich is pulled away.",
  "One 6 second take, used whole. The napkin, knife and fork come up from below the desk."),
 ("A8", "A8", "A8. The clean-up crew inside the cell", "The five workers shovel the broken parts into wheelbarrows, wheel them to the furnace and tip them in. The cell turns bright and clean as you say \"renews your cells\".",
  "One 8 second take, its first 7.4 seconds. It is a cartoon: around the fifth second the junk clears in one quick sweep rather than piece by piece."),
 ("A5", "A5", "A5. The donut and the food coma", "He bites a donut at normal speed, the box empties in a one second fast-forward while the clock runs from nine to ten, then his head sinks onto the keyboard on \"food coma\".",
  "One 6 second take, used whole. The AI label sits top left here so it does not cover the clock. The stock clip of a man asleep at his desk (6:47) is out, as planned, so the film does not show two of them."),
 ("A3", "A3-A1", "A3. The stomach rumble in the meeting", "The water jumps in the glasses on \"all of a sudden\", then everyone turns to stare and the woman hides a laugh on \"really lets them know\".",
  "One 6 second take. The rumble reads as water splashing up out of three glasses: bigger than a ripple, on purpose a gag."),
 ("A1", "A3-A1", "A1. \"This is just too hard\" (lip sync)", "He whines the line at his empty plate with your voice, then slumps back and groans on \"I'm not cut out for it\".",
  F["a1_sync"]),
 ("A2", "A2", "A2. \"I could never do this\" (no lip sync)", "Flat on his back beside the tiny pink dumbbell, eyes shut and panting, while your voice does the line; then he heaves himself over and starts to crawl off on \"I might as well just quit\".",
  F["a2_sync"]),
 ("A6", "A6", "A6. The midnight fridge raid", "He pulls the fridge open, his arms fill with ice cream, pizza and cake, he turns away from the fridge, freezes at the camera with the spoon in his mouth, then tiptoes off.",
  "One 8 second take, from 1.6 seconds in (the walk up to the fridge is left out so the raid fits your sentence). He is walking away from the open fridge, as you asked."),
 ("A7", "A7", "A7. One sip on an empty stomach", "The end of his first sip, the glass goes down, he sways on \"feel more drunk\", slides off the stool and hugs the bar while the bartender stares.",
  "One 6 second take, from 0.6 seconds in."),
]
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 auto 60px;padding:0 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}.two video{width:100%;border-radius:10px;background:#000}
.rev{display:grid;grid-template-columns:480px 1fr;gap:16px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:14px;margin:12px 0}.rev video{width:100%;border-radius:8px;background:#000}
.ts{display:inline-block;background:#1f7a4d;color:#fff;border-radius:5px;padding:1px 8px;font-weight:700;margin-right:6px}.muted{color:#9fb2cc}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #26354d;padding:7px 8px;text-align:left;vertical-align:top}th{color:#9fb2cc;font-weight:600}
textarea{width:100%;height:230px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li,ul li{margin:5px 0}a{color:#8fd0ff}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}
@media(max-width:900px){.rev,.two{grid-template-columns:1fr}}"""
h = [f"<!doctype html><meta charset='utf-8'><title>RO-08 round 2: full film, two openers</title><style>{css}</style><main>",
     "<h1>Intermittent Fasting: The Best Way To Get Abs. Round 2, the full film</h1>",
     f"<div class='sub'>Long-form content, 16:9, {F['length']}. Every AI clip you approved as frames is now moving, both openers are built, and the film is finished from start to end. Nothing is a placeholder.</div>",
     "<div class='dec'><b>Already locked, not reopened:</b> the cut, colour D, voice 1a, the two sizes, the 48 lower thirds, every cutaway you did not name, the brightened B-roll, the AI frames.</div>",
     "<h2>Your decisions (2)</h2>",
     "<div class='dec'><b>1. Which opener?</b> A, the time-lapse (your idea: 8 AM to 2 PM at his laptop, then the salad). It is the one in the full film below. Or B, the split screen (idea 6). "
     f"My recommendation: {e(F['opener_rec'])} If you pick B, the first 8 seconds of the film are swapped and everything after them stays as it is.</div>",
     "<div class='dec'><b>2. Finalize the film?</b> Yes, or your notes with a time. Each AI clip is below with its time in the film, so you do not have to hunt for them. The one to look at hardest is A2 (7:45): it is a new take with no lip sync that you have not seen.</div>",
     "<h2>The two openers, each at the head of the first minute</h2><div class='two'>",
     f"<div><b>Opener A: the time-lapse</b> (in the full film)<video controls preload='none' poster='{FA}.jpg' src='{FA} - REVIEW 540p.mp4'></video><p class='muted'>{e(F['ot_note'])}</p></div>",
     f"<div><b>Opener B: the split screen</b><video controls preload='none' poster='{FB}.jpg' src='{FB} - REVIEW 540p.mp4'></video><p class='muted'>{e(F['o6_note'])}</p></div></div>",
     f"<p class='muted'>1080p files: <a href='{FA}.mp4'>first minute with A</a> &nbsp; <a href='{FB}.mp4'>first minute with B</a>. Both are also in the project folder for VLC (names at the bottom).</p>",
     "<h2>The full film</h2>", f"<video class='big' controls preload='none' poster='{FILM}.jpg' src='{FILM} - REVIEW 540p.mp4'></video>",
     f"<p class='muted'><a href='{FILM}.mp4'>Full 1080p file</a> &nbsp; <a href='RO08.srt'>Subtitles</a> &nbsp; <a href='RO08.chapters.txt'>Chapters</a> &nbsp; <a href='RO-08 audio AB (reference then ours).mp4'>Audio A/B against the reference voice</a></p>",
     "<h2>The eight AI clips, moving, in the film</h2><p class='muted'>Each clip below is cut from the finished film with about 3 seconds of you either side. The green time is where it sits in the full film.</p>"]
for i, clip, title, what, note in AI:
    ts, watch = rng(i)
    h.append(f"<div class='rev'><video controls preload='none' poster='context/{clip}-context.jpg' src='context/{clip}-context - REVIEW 540p.mp4'></video><div><b>{e(title)}</b><br><span class='ts'>{ts}</span><span class='muted'>{watch}</span>"
             f"<p>{e(what)}</p><p class='muted'>{e(note)}</p></div></div>")
h.append("<h2>Every change since the round 1 page, with where to look</h2><table><tr><th>Time in the film</th><th>Watch</th><th>What changed</th></tr>")
CH = [("OT", "The opener. Before: your workout B-roll (you cut it). Now: AI opener A, with B as the alternative above."),
      ("A4", "A4 is moving (was two still frames)."), ("C08", "Salad lid clip, brightened to sit with the kitchen footage (you approved the colour)."),
      ("A8", "A8 is moving."), ("A5", "A5 is moving."), (None, None), ("A3", "A3 is moving."), ("A1", "A1 is moving, lips synced to your recording."),
      ("A2", "A2 is moving, with no lip sync (your rule from 10-12)."), ("C38", "Ab wheel clip swapped to the bright daylight one (your colour note)."),
      ("C30", "Salad push-in, brightened."), ("A6", "A6 is moving, with the new end: he walks away from the fridge."), ("A7", "A7 is moving."),
      ("C35", "Kettlebell deadlifts and decline push-ups, brightened.")]
G20 = (R["G20"]["t0"], R["G20"]["t1"])
for i, what in CH:
    if i is None:
        a, b = F["c22_slot"]; h.append(f"<tr><td><span class='ts'>{mmss(a)} to {mmss(b)}</span></td><td class='muted'>watch {mmss(a-3)} to {mmss(b+3)}</td><td>The stock clip of a man asleep at his desk is out (A5 is in). You are on camera here now.</td></tr>"); continue
    ts, watch = rng(i); h.append(f"<tr><td><span class='ts'>{ts}</span></td><td class='muted'>{watch}</td><td>{e(what)}</td></tr>")
h.append(f"<tr><td><span class='ts'>{mmss(G20[0])} to {mmss(G20[1])}</span></td><td class='muted'>watch 6:00 to 6:13</td><td>The lower third \"Digesting A Heavy Meal Takes Energy.\" comes up a second and a half earlier, so it is off before the donut box empties.</td></tr>")
h.append("<tr><td><span class='ts'>whole film</span></td><td class='muted'>any 20 seconds</td><td>Voice 1a (your pick: a little less echo, same warmth and bass) and the quiet music bed under it.</td></tr></table>"
         "<p class='muted'>Everything else is the round 1 build you approved: every shot is held at the same size and crop, and the 48 lower thirds are the same renders (the graphics file is byte for byte unchanged).</p>")
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in F["decided"]] + ["</ol>"]
h += ["<h2>The checks, stated plainly</h2><ul>"] + [f"<li>{e(d)}</li>" for d in F["checks"]] + ["</ul>"]
if F.get("flags"): h += ["<h2>Existing flags, unchanged from round 1 (not new)</h2><ul>"] + [f"<li>{e(d)}</li>" for d in F["flags"]] + ["</ul>"]
h += ["<h2>For VLC</h2><p>In the project folder <b>Videos to Review</b>:</p><ul>"] + [f"<li>{e(n)}</li>" for n in F["vlc"]] + ["</ul>"]
reply = ("RO-08 round 2\n1. Opener (A time-lapse / B split screen):\n2. Finalize it (yes / no):\nA1 lip sync (7:24):\nA2 lip sync (7:45):\nA3 (7:17):\nA4 (1:59):\nA5 (6:06):\nA6 (12:11):\nA7 (13:35):\nA8 (4:55):\nAnything else (with a time):\n")
h += ["<h2>Your reply</h2>", f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button></main>"]
s = "\n".join(h); assert chr(8212) not in s and chr(8211) not in s
open(f"{O}/index.html", "w").write(s); print("page written", len(s))
