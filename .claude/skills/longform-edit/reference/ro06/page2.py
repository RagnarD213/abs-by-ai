"""RO-06 round 2 review page (first minute rebuilt to Dan's round 1 notes). Short page: the first minute on top, what
changed, the stills that changed pulled from the rendered file, the still-open decisions in one list, one reply box.
Writes round2/index.html. Serve with _shared/review_server.py PORT round2.  usage: page2.py"""
import json, os, html, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro06"; O = f"{W}/round2"; FM = "first-minute/DRAFT - RO-06 round 2 - first minute"
M = f"{O}/{FM}.mp4"; e = html.escape; os.makedirs(f"{O}/stills", exist_ok=True)
def grab(t, name, crop=None):
    p = subprocess.run([Bd.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", M, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    im = Image.frombytes("RGB", (1920, 1080), p)
    if crop: im = im.crop(crop)
    im.save(f"{O}/stills/{name}.jpg", quality=92); return name
OPEN = [(1.6, "open-1", "0:00 to 0:03.7", "Tight: just above your hair to just below your shorts", "Today, I'm going to show you how to create a great home workout setup."),
        (4.9, "open-2", "0:03.7 to 0:06.1", "Clip 1: ab wheel (the one you liked)", "This is a setup I personally use to not only maintain my abs"),
        (7.2, "open-3", "0:06.1 to 0:08.4", "Clip 2: jump rope", "during COVID, but to actually"),
        (9.6, "open-4", "0:08.4 to 0:10.8", "Clip 3: kettlebell", "make gains during that time."),
        (11.8, "open-5", "0:10.8 to 0:12.8", "The wide: you and everything on the floor", "You can get it for just fifty eight dollars."),
        (15.0, "open-6", "0:12.8 to 0:20.2", "Back to tight, with the $58 lower third", "So this is great for you guys who are on a limited budget. And if you have limited time to work out..."),
        (21.5, "open-7", "0:20.2 to 0:23.1", "The equipment up close (unchanged)", "then you need something like this so you can work out at home."),
        (30.5, "open-8", "0:28.9 to 0:35.8", "Medium: hair to mid-thigh, used between two tight shots", "but you got all kinds of excuses like Dan I don't have time to go to the gym..."),
        (50.0, "open-9", "0:46.7 to 0:54.9", "The wide again, because you say 'the stuff in front of me right here'", "You can do it with just the stuff in front of me right here just cost $58"),
        (57.2, "open-10", "0:54.9 to 0:59.0", "Tight, with the lower third", "Super cheap, super easy, there's no excuse for not doing this."),
        (61.4, "open-11", "0:59.0 to 1:03", "Medium, because you lean over and point at the equipment", "Even if you do have a gym membership, I still recommend this stuff.")]
for t, n, *_ in OPEN: grab(t, n)
grab(1.6, "sharp-tight", (560, 40, 1520, 580)); grab(30.5, "sharp-medium", (560, 40, 1520, 580)); grab(11.8, "sharp-wide", (300, 0, 1260, 540))
DEC = [
 ("Tight shot sharpness", "Keep the tight shot as built", ["Keep as built (recommended)", "Make it a little less tight (hair to upper thigh), a bit sharper"],
  "The camera filmed you small in a 1080p frame, so the tight shot is that picture enlarged about 2 times. It is softer than the wide. I added sharpening to offset it. Three same-size crops are below so you can judge. A less tight shot would be a bit sharper but would not end at your shorts."),
 ("Hair at the top edge", "Leave as shot for this cut", ["Leave as shot", "Add headroom by extending the background above your head (one extra round)"],
  "Not in this first minute (your hair has 26 pixels or more of room on every frame here). Later, on 9 of the 20 rolls (jump rope through the second medicine ball clip, and the closing), the camera framed your hair 5 to 15 pixels from the top edge. I crop nothing off, but there is no spare picture above your head."),
 ("Length", "A: trim three pure repeats, about 16:30", ["A: trim three repeats, about 16:30 (recommended)", "B: keep everything, 17:39", "C: deeper trim to about 15:00"],
  "A cuts only places where you restate a point you already made: the 'I don't care how poor you are' run after the $58 total (26 s), the second explanation of why you don't need the rubber coating (14 s), and the closing restatements of 'this is a great way to get started' (25 s). C also trims the medicine ball form detail and the full dumbbell rack advice."),
 ("Product pictures", "Keep the AI-made pictures (labelled)", ["Keep AI pictures (recommended)", "Use real product photos you send me", "No pictures, prices as lower thirds only"],
  "You say 'the one you're seeing on your screen right now' six times, so each price card needs a picture. Codex made six plain product pictures, each carrying the AI-GENERATED label. They are on the round 1 page."),
 ("Jump rope price", "Keep as built", ["Keep as built", "Cut the words 'for just $10'"],
  "You say '$10' in the jump rope section and '$9' in the total (which is what adds up to $58). Built: no price on screen in the jump rope section, $9 in the total list."),
 ("Music", "Add a quiet music bed", ["Add a quiet bed under your voice (recommended)", "Voice only"],
  "The first minute is voice only, exactly the audio you approved. Zeeshan's ab wheel videos carry a soft bed; our last two long-forms (Calories, Belly Fat) did not."),
 ("App demo at the end", "Rebuild it in the blue phone card", ["Same approved demo, in the Soft Blue phone card (recommended)", "Exactly as approved, olive background"],
  "For 'upload your current picture, make a picture of your goal' I use your approved sunglasses-to-pool demo. It was built on the old olive background. The steps and the AI label stay identical either way."),
 ("Opening", "Keep the on-camera open", ["Keep the on-camera open as rebuilt here (recommended)", "Also show me two AI opener ideas as start and end frames"],
  "Your round 1 notes kept the on-camera open, so that is what is built. This line only confirms you do not also want an AI opener."),
]
CHANGED = [
 "The video now opens on the tight shot of you: just above your hair to just below the bottom of your shorts.",
 "Three different B-roll clips at the start, about 2.4 seconds each: the ab wheel clip you liked, then jump rope, then kettlebell. The push-up clip is out of the opening.",
 "After the clips comes the wide shot with all the equipment on the floor, on 'You can get it for just fifty eight dollars'. Then back to tight.",
 "Tight is now the normal shot. In this first minute you are tight for 30 seconds, medium for 13, wide for 10, and the B-roll and equipment clips take 10.",
 "The wide shot comes back once more in this minute, at 0:47, because you say 'the stuff in front of me right here'.",
 "The $58 lower third now comes in one sentence later ('So this is great for you guys...'), on the tight shot. On the wide shot it would have covered the equipment.",
 "Audio and colour are exactly what you approved. I checked the audio sample by sample against the round 1 file: identical.",
]
DECIDED = [
 "A third size, medium (hair to mid-thigh, the tighter size from round 1), is used where one take is cut to another and I do not want to go wide. Two shots of the same size back to back would look like a jump cut. Say so if you would rather I use the wide there.",
 "The wide shot holds for 2 seconds after the opening clips (just the '$58' sentence). If you want it longer, it can run through 'limited budget' (5 seconds), and the $58 lower third then goes away or moves later.",
 "On the tight shot the lower third sits over your shorts. Your face, chest and abs stay clear.",
 "At 0:59 ('I still recommend this stuff') you lean over and point at the equipment. That is too big a move for the tight shot, so that sentence is medium.",
 "Kettlebell clip: I used the one on the lawn (B0439). The poolside kettlebell swings stay where they are, later in the kettlebell section, so no clip is used twice.",
 "Jump rope and kettlebell each appear again later in their own sections, with different clips. The opening is a quick preview of three exercises.",
 "No camera movement was added. Every shot is a fixed frame and every change of size is a hard cut.",
 "Spend this round: $0. No AI clips, no new images.",
]
css = open(f"{W}/recipe/page.py").read().split('css = """')[1].split('"""')[0]
css += ".three{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.three img{width:100%;border-radius:6px}.three div{font-size:13px;color:#9fb2cc;text-align:center}ul li{margin:5px 0}"
h = [f"<!doctype html><meta charset='utf-8'><title>RO-06 round 2</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>The first minute. Press any 'Play from here' button below.</div><video id='player' controls preload='none' poster='first-minute/poster.jpg' src='" + FM + " - REVIEW 540p.mp4'></video></div><main>",
     "<h1>How To Work Out At Home On A Budget: round 2, the first minute rebuilt</h1>",
     "<div class='sub'>Long-form content, 16:9. Only the first minute was rebuilt, to your round 1 notes. The full film is not rendered yet.</div>",
     "<p><b>Locked by you in round 1 and not touched:</b> the audio ('The audio is sounding good') and the colour ('Color correction is looking good').</p>",
     "<h2>The first minute</h2>", f"<video class='big' controls preload='none' poster='first-minute/poster.jpg' src='{FM} - REVIEW 540p.mp4'></video>",
     f"<p class='muted'>Also in the project folder for VLC: <b>Videos to Review / Work Out At Home LFC R2 - first minute.mp4</b>. <a href='{FM}.mp4'>Full 1080p file</a> &nbsp; <a href='first-minute/AB_reference-vs-ours.mp4'>Audio A/B against the reference voice</a></p>",
     "<h2>What changed</h2><ul>"] + [f"<li>{e(c)}</li>" for c in CHANGED] + ["</ul>",
     f"<h2>Your decisions ({len(DEC)})</h2><p class='muted'>Number 1 is new. The other seven are still open from round 1; I have not assumed an answer to any of them.</p>"]
for i, (t, rec, opts, why) in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
h += ["<h2>Decision 1: how sharp each size is</h2><div class='muted'>A piece of the picture at full size (not shrunk), straight from the finished file. Left to right: tight (enlarged about 2 times), medium (enlarged 1.5 times), wide (as filmed).</div><div class='three'>"]
h += [f"<div><img loading='lazy' src='stills/sharp-{k}.jpg'>{k}</div>" for k in ("tight", "medium", "wide")] + ["</div>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += [f"<h2>The new first minute, shot by shot ({len(OPEN)})</h2><div class='grid'>"]
for t, n, when, what, said in OPEN:
    h.append(f"<div class='card'><img loading='lazy' src='stills/{n}.jpg'><div class='b'><span class='id'>{e(when)}</span><div class='copy'>{e(what)}</div>"
             f"<span class='muted'>You are saying: {e(said)}</span><br><button onclick=\"seek({max(0, t-3.0):.1f})\">Play from here</button></div></div>")
reply = "RO-06 round 2\n" + "\n".join(f"{i}. {t}: {rec}" for i, (t, rec, o, w) in enumerate(DEC, 1)) + "\nFirst minute, anything to change (time and what):\nAnything else:\n"
h += ["</div><h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function seek(t){var v=document.getElementById('player');var go=function(){v.currentTime=t;v.play();};if(v.readyState>=1){go();}else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}}</script></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("page written;", len(OPEN), "stills; em dashes:", "\n".join(h).count(chr(8212)))
