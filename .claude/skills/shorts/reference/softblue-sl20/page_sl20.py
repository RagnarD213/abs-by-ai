#!/usr/bin/env python3
"""SL-20 review page (phone first): the three delivered 1080p Shorts on one page, players first, then per-Short notes, what I
decided, your calls, checks and one reply box. Serve with `_shared/review_server.py PORT /Volumes/Expansion/_edit_work/SL-20/review`."""
import html, json, os, shutil, subprocess, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
E = html.escape; R = "/Volumes/Expansion/_edit_work/SL-20/review"; FF = Bt.lib.FF
OUT = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content"
os.makedirs(f"{R}/media", exist_ok=True)
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
ORDER = [("C", 1), ("B", 2), ("G", 3)]
NOTES = {
 "C": ["Opens on \"Now, in today's dating environment\": \"Now\" runs straight into \"in\" with no gap, so it cannot be cut cleanly.",
       "Cut: the repeated \"such a\" (\"make such a, such a huge difference\" is now \"make such a huge difference\"); the couch clip covers the moment your head was down.",
       "Clips, all from the approved film: man swiping a dating app, woman swiping on her couch (twice), the AI dating-app phone, your winner-take-all diagram."],
 "B": ["Cut: the half-started \"or\" in \"if you're married, or- and you're...\"; the pause after \"right now\" is a little shorter.",
       "New closing clip: library stock of a family at dinner (used in two of your films), in place of the film's AI dinner clip, whose last half second glitches (greens appear on a plate). A clip is never slowed to fill a slot.",
       "Other clips from the approved film: wife serving dinner, the AI poolside cafe clip, the wedding ring."],
 "G": ["Cut: a half-started \"b-\" before \"just being slaves to their job\".",
       "New clip: library stock of hands passing hundred-dollar bills on \"pass it on to your heirs\" (used in My First Spray Tan), colour toned down to match you.",
       "Other clips from the approved film: a man slumped at his desk, the lawyers."],
}
DECIDED = [
 "The picture comes from the approved film itself, without its burned-in text bars, so the look, colour and sound match what you approved.",
 "Your titles are used word for word in title case, with your capital NOT kept.",
 "One key point per Short, each on a single steady shot: dating \"Only The Top 10% Get Seen / Looks First, Personality Later\", relationship \"Getting Fat Changes / How She Sees You\", money \"Money Can't Buy Health / Health Comes First\".",
 "The crop lands on your face at every cut and follows only if you drift (the standard vertical framing).",
 "The dating-app phone and your diagram show whole on the blue field, because their horizontal cards do not crop to vertical.",
 "Captions in the money Short read \"going to happen\" where you say \"gonna\"; the film's transcript has it that way. Say if you want it to read \"gonna\".",
]
CALLS = [
 "Relationship, 0:01 to 0:05: the film's own clip shows a slim husband while you say \"a little bit overweight\". The approved film uses the same clip on the same line. Keep it, or swap it?",
 "All three open on you talking to camera rather than on a clip. Keep the open on you?",
]
CHECKS = [
 "Three independent reviews per Short (round 1, 1b, 1c): all three now SHIP with 0 open defects.",
 "Sound: the film's own mix, untouched (the audio check passes on all three; loudness about -13.5 to -14.4 LUFS).",
 "One compliance check (no banned app screens) could not run on the final files: its reference recording was moved off this Mac this afternoon, apparently by the nightly footage offload. It passed on the relationship Short and on the dating Short before its last crop change, and none of the three contains an app screen recording.",
 "Final quality gate: the dating and money Shorts pass every other check except the two hair-at-the-top checks; the relationship Short passes 37 of 39, the same two. The camera cut off the top of your hair through this whole film (the approved film fails the same two), and the crop already starts at the camera's top row. Same as the spray-tan Shorts.",
 "AI clips: the three reused film AI clips were checked frame by frame by an independent reviewer; the dinner clip failed and was replaced.",
 "No covers made and nothing uploaded: that is the setup step after your approval. Kitchen Shorts air in February, after the parent film is public (Wed Dec 9).",
]
cards = []
for S, n in ORDER:
    d = Bt.D(S); T = json.load(open(f"{d}/timeline.json"))
    src = f"{OUT}/{P.NAME[S]}.mp4"; dst = f"{R}/media/short{n}.mp4"
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src): shutil.copyfile(src, dst)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "2.0", "-i", dst, "-frames:v", "1", "-vf", "scale=540:-1", "-q:v", "3", f"{R}/media/short{n}.jpg"], check=True)
    eb, hl = P.TITLE[S]; title = " ".join(hl)
    words = re.sub(r"\{[^}]*\}", "", P.TEXT[S]).replace(" | ", " ")
    cards.append(f"""<article id="s{n}"><h3>Short {n}: {E(title)} <span class="small">{mmss(T['total'])}</span></h3>
<video controls preload="metadata" playsinline poster="media/short{n}.jpg" src="media/short{n}.mp4"></video>
<div class="copy"><ul>{''.join('<li>' + E(x) + '</li>' for x in NOTES[S])}</ul>
<details><summary>Full transcript</summary><p>{E(words)}</p></details>
<p class="small">Full size: <code>Short-form video content/{E(P.NAME[S])}.mp4</code> (also in Videos to Review)</p></div></article>""")
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Invest In Your Health SFL R1</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:20px 16px}}h1{{font-size:30px;margin:0 0 8px}}h2{{font-size:24px}}
p,li{{color:#bdd0e4}}section{{margin:24px 0;padding:18px;background:#101f32;border:1px solid #29425b;border-radius:16px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
article{{min-width:0;background:#081626;padding:12px;border-radius:14px}}video{{width:100%;aspect-ratio:9/16;border-radius:10px;background:black}}.small{{font-size:14px;color:#9fb7cf}}.copy{{font-size:15px}}
textarea{{width:100%;box-sizing:border-box;min-height:180px;background:#071221;color:white;padding:12px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;font-size:15px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}video{{max-height:80vh}}}}</style>
<main><h1>Invest In Your Health Shorts, round 1</h1><p>Your three picks, cut from the approved film with your titles. Watch each on your phone size first. Nothing is uploaded; covers come in the setup step.</p>
<section id="shorts"><div class="grid">{''.join(cards)}</div></section>
<section id="calls"><h2>Your calls ({len(CALLS)})</h2><ol>{''.join('<li>' + E(x) + '</li>' for x in CALLS)}</ol></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in DECIDED)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in CHECKS)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">Short 1 (dating):
Short 2 (relationship):
Short 3 (money):
Calls: 1) 2) </textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash"
open(f"{R}/index.html", "w").write(page); print("page ok", len(page))
