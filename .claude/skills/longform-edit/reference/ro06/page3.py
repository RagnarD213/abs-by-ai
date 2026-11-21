"""RO-06 round 3 review page: the rebuilt first minute (jump rope swap, panning equipment shot), START and END frames for
four new AI clips sitting in their slots as labelled placeholders, What changed, What I decided, the open decisions, one
reply box. Writes round3/index.html. Serve with _shared/review_server.py PORT round3.  usage: page3.py"""
import json, os, html, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro06"; O = f"{W}/round3"; FM = "first-minute/DRAFT - RO-06 round 3 - first minute"
M = f"{O}/{FM}.mp4"; e = html.escape; os.makedirs(f"{O}/stills", exist_ok=True)
def grab(t, name):
    p = subprocess.run([Bd.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", M, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    Image.frombytes("RGB", (1920, 1080), p).save(f"{O}/stills/{name}.jpg", quality=92); return name
for k in ("A1", "A2", "A3", "A4"):
    for s in ("start", "end"): Image.open(f"{O}/frames/{k}-{s}.png").convert("RGB").save(f"{O}/frames/{k}-{s}.jpg", quality=92)
CH = [(7.25, "jump-rope", "0:06.1 to 0:08.4", "New jump rope clip: fast and smooth", "during COVID, but to actually"),
      (20.35, "pan-1", "0:20.2", "Equipment shot, start: on the kettlebell", "then you need something like this"),
      (21.65, "pan-2", "0:21.6", "Equipment shot, middle: moving right", "so you can work out"),
      (23.0, "pan-3", "0:23.1", "Equipment shot, end: on the dumbbells", "at home."),
      (36.9, "tight-between", "0:35.8 to 0:38.6", "You, tight, between the AI clips (unchanged from round 2)", "You know I'm hearing your excuses and in this video")]
for t, n, *_ in CH: grab(t, n)
AI = [("A1", "0:31.1 to 0:33.5", 2.4, 4, "Dan I don't have time to go to the gym",
       "He whines the excuse and taps his bare wrist where a watch would be. You stand beside him with your arms crossed and roll your eyes. His lips move to your impression."),
      ("A2", "0:33.5 to 0:35.8", 2.3, 4, "or Dan I don't have the money for a gym membership.",
       "Closer shot. He opens his wallet, turns it upside down and it is empty, still whining. You put your hand on your forehead. His lips move to your impression."),
      ("A3", "0:38.6 to 0:41.2", 2.6, 4, "I'm about to destroy all those excuses,",
       "He is mid-whine with his eyes shut. You swing and slap him across the cheek. The hit lands on the word 'destroy' (0:39.4). His head whips round, shocked."),
      ("A4", "0:41.2 to 0:46.7", 5.5, 6, "show you why they're all a crock of shit and explain to you why those excuses are not valid in any way whatsoever.",
       "He does push-ups on your push-up handles on the blue mat, red in the face. You kneel beside him, blow the whistle, then pump your fist and shout him on. The ab wheel and jump rope are on the mat.")]
START = {"A1": 31.12, "A2": 33.54, "A3": 38.56, "A4": 41.16}
DEC = [
 ("AI clips A1 and A2, the two excuses", "Approve the frames", ["Approve the frames (recommended)", "Changes (say what)"],
  "Start and end frames are below. If you approve, I generate the motion and sync his lips to your impression. No new voice is made and the film's audio does not change."),
 ("AI clip A3, the slap", "Approve the frames", ["Approve the frames (recommended)", "Changes (say what)"],
  "Played as slapstick: no blood, no mark. The slap lands on 'destroy'."),
 ("AI clip A4, the home workout", "Approve as one clip of push-ups", ["One clip of push-ups on the handles (recommended)", "Two shorter clips: push-ups, then the ab wheel (one more pair of frames first)", "Changes (say what)"],
  "The slot is 5.5 seconds. One exercise fits it comfortably as a single clip. Two exercises means two clips of under 3 seconds each."),
 ("Hair at the top edge", "Leave as shot for this cut", ["Leave as shot", "Add headroom by extending the background above your head (one extra round)"],
  "Not in this first minute. Later, on 9 of the 20 rolls (jump rope through the second medicine ball clip, and the closing), the camera framed your hair 5 to 15 pixels from the top edge. I crop nothing off, but there is no spare picture above your head."),
 ("Length", "A: trim three pure repeats, about 16:30", ["A: trim three repeats, about 16:30 (recommended)", "B: keep everything, 17:39", "C: deeper trim to about 15:00"],
  "A cuts only places where you restate a point you already made: the 'I don't care how poor you are' run after the $58 total (26 s), the second explanation of why you don't need the rubber coating (14 s), and the closing restatements of 'this is a great way to get started' (25 s). C also trims the medicine ball form detail and the full dumbbell rack advice."),
 ("Product pictures", "Keep the AI-made pictures (labelled)", ["Keep AI pictures (recommended)", "Use real product photos you send me", "No pictures, prices as lower thirds only"],
  "You say 'the one you're seeing on your screen right now' six times, so each price card needs a picture. Codex made six plain product pictures, each carrying the AI-GENERATED label. They are on the round 1 page."),
 ("Jump rope price", "Keep as built", ["Keep as built", "Cut the words 'for just $10'"],
  "You say '$10' in the jump rope section and '$9' in the total (which is what adds up to $58). Built: no price on screen in the jump rope section, $9 in the total list."),
 ("Music", "Add a quiet music bed", ["Add a quiet bed under your voice (recommended)", "Voice only"],
  "The first minute is voice only, exactly the audio you approved."),
 ("App demo at the end", "Rebuild it in the blue phone card", ["Same approved demo, in the Soft Blue phone card (recommended)", "Exactly as approved, olive background"],
  "For 'upload your current picture, make a picture of your goal' I use your approved sunglasses-to-pool demo. It was built on the old olive background. The steps and the AI label stay identical either way."),
 ("Opening", "Keep the on-camera open", ["Keep the on-camera open (recommended)", "Also show me two AI opener ideas as start and end frames"],
  "You approved the tight open and the three clips. This line only confirms you do not also want an AI opener."),
]
CHANGED = [
 "Jump rope clip in the opening (0:06) swapped for you jumping fast and smooth. The old one was your beginner demo.",
 "Equipment shot at 0:20 is now a much closer shot that starts on the kettlebell and moves right across everything to the dumbbells by the end of the clip.",
 "Four AI clips have their start and end frames sitting in place as labelled placeholders: 0:31 and 0:33.5 (the two excuses), 0:38.6 (the slap), 0:41.2 (the workout). Each placeholder shows the start frame for the first half of its time and the end frame for the second half. No AI motion has been made yet.",
 "Nothing else was touched. Cropping, colour and audio are exactly what you approved: every frame of you that is still on screen uses the same crop as round 2, and the audio is identical to the round 2 file, checked sample by sample.",
]
DECIDED = [
 "Jump rope: I used the fast high-knee stretch from your pool jump rope roll (about 155 steps a minute, measured, steady rhythm, no trip). The both-feet clip from that roll is slower (about 95 jumps a minute with a pause on each landing). The driveway clip in sunglasses is fast, but its picture only fills half the frame, so it would need a 3 times enlargement and would cut your feet off. If you meant a different clip, tell me which.",
 "The jump rope section later in the film keeps its own clip (both feet), so no clip appears twice.",
 "Equipment shot: about 2.25 times closer than before. It moves at a steady speed with a soft start and stop, and has slight natural blur while moving, like a real camera pan. The kettlebell cannot sit dead centre at the start because it is near the left edge of what the camera filmed.",
 "Equipment shot sharpness: you said to upscale if needed, so I ran the 3 seconds through the Topaz video upscaler ($0.24). It is clearly sharper than a plain enlargement. Same-size comparison is below. Colour is the same correction as before.",
 "Your trainer outfit: the black Abs By AI tank top and black shorts from the app's AI trainer, plus a coach's whistle round your neck.",
 "The other man: heavyset, messy hair, baggy grey T-shirt, sweatpants. He is always fully clothed and no shot is framed on his stomach, because A1 and A2 sit at the 30 second mark that ad review looks at.",
 "One room for all four clips: a garage home gym with your real equipment copied from the equipment shot (kettlebell, ab wheel, jump rope, medicine ball, push-up handles, dumbbells, blue mat).",
 "Lip sync plan: Veo 3.1 Fast makes the motion from the start and end frames, then Sync Labs lipsync drives his mouth from your own recorded impression. I trim each clip to its slot, never slow or hold it.",
 "Two frames I rejected and redid before showing you: the first slap end frame had your arm finishing on the wrong side, and the first wallet frame gave you a different haircut.",
 "For Shorts later: the two men stand close together near the middle, but two people do not fit in the middle third. A vertical crop will follow whoever is talking.",
 "At upload this video gets the AI flag turned on, because it will contain realistic AI footage.",
 "Spend on this video so far: $0.24 (the upscale). The 12 AI pictures (2 reference pictures, 8 frames, 2 redone) were made by Codex on your subscription at no charge.",
 "Motion estimate for all four clips with the lip sync: about $2.20 if each works first time (18 seconds of Veo 3.1 Fast at $0.10 a second, plus about $0.40 of lip sync). With one redo of every clip, about $4.40. That stays inside the $5 per video limit, so approving the frames is all I need.",
]
css = open(f"{W}/recipe/page.py").read().split('css = """')[1].split('"""')[0]
css += (".three{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pair img,.wide img{width:100%;border-radius:6px;display:block}"
        ".pair div{font-size:13px;color:#9fb2cc;text-align:center}.ai{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:14px 0}ul li{margin:5px 0}")
h = [f"<!doctype html><meta charset='utf-8'><title>RO-06 round 3</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>The first minute. Press any 'Play from here' button.</div><video id='player' controls preload='none' poster='first-minute/poster.jpg' src='" + FM + " - REVIEW 540p.mp4'></video></div><main>",
     "<h1>How To Work Out At Home On A Budget: round 3, first minute and AI clip frames</h1>",
     "<div class='sub'>Long-form content, 16:9. Only the first minute was rebuilt. The full film is not rendered yet, and no AI motion has been generated.</div>",
     "<p><b>Locked by you and not touched:</b> cropping, colour and audio ('All the cropping, color correction, and audio look good'), the tight open ('I like the tight shot at the beginning'), the three clips at the start with the ab wheel and kettlebell clips ('I like how you added three clips in').</p>",
     f"<h2>Your decisions ({len(DEC)})</h2><p class='muted'>1 to 3 are new. 4 to 10 are still open from earlier rounds; I have not assumed an answer to any of them.</p>"]
for i, (t, rec, opts, why) in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
h += ["<h2>The first minute</h2>", f"<video class='big' controls preload='none' poster='first-minute/poster.jpg' src='{FM} - REVIEW 540p.mp4'></video>",
      f"<p class='muted'>Also in the project folder for VLC: <b>Videos to Review / Work Out At Home LFC R3 - first minute.mp4</b>. <a href='{FM}.mp4'>Full 1080p file</a> &nbsp; <a href='first-minute/AB_reference-vs-ours.mp4'>Audio A/B against the reference voice</a></p>",
      "<h2>The four AI clips: start and end frames</h2><p class='muted'>Every clip carries the AI-GENERATED label. Left is the first frame, right is the last frame. Motion is generated only after you approve.</p>"]
for k, when, slot, gen, said, act in AI:
    h.append(f"<div class='ai'><span class='id'>{k}</span> &nbsp; {e(when)} &nbsp; <span class='muted'>You are saying: {e(said)}</span>"
             f"<div class='pair' style='margin-top:8px'><div><img loading='lazy' src='frames/{k}-start.jpg'>START</div><div><img loading='lazy' src='frames/{k}-end.jpg'>END</div></div>"
             f"<div class='copy'><b>Action:</b> {e(act)}</div><span class='muted'>On screen for {slot} seconds. Generated as a {gen} second clip and trimmed (${gen*0.10:.2f}" + (", plus about $0.20 of lip sync" if k in ("A1", "A2") else "") + ").</span>"
             f"<br><button onclick=\"seek({max(0, START[k]-3.0):.1f})\">Play it in place, from 3 seconds before</button></div>")
h += ["<h2>What changed</h2><ul>"] + [f"<li>{e(c)}</li>" for c in CHANGED] + ["</ul>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += [f"<h2>The changed shots ({len(CH)})</h2><div class='grid'>"]
for t, n, when, what, said in CH:
    h.append(f"<div class='card'><img loading='lazy' src='stills/{n}.jpg'><div class='b'><span class='id'>{e(when)}</span><div class='copy'>{e(what)}</div>"
             f"<span class='muted'>You are saying: {e(said)}</span><br><button onclick=\"seek({max(0, t-3.0):.1f})\">Play from here</button></div></div>")
h += ["</div><h2>Equipment shot: plain enlargement (left) against the upscaler (right)</h2><div class='muted'>Pieces of the picture at full size, before colour correction. Top: the start. Middle: the end. Bottom: mid-move, where both are softened by the movement.</div>",
      "<div class='wide'><img loading='lazy' src='c02/compare-lanczos-vs-topaz.jpg'></div>"]
reply = "RO-06 round 3\n" + "\n".join(f"{i}. {t}: {rec}" for i, (t, rec, o, w) in enumerate(DEC, 1)) + "\nFirst minute, anything to change (time and what):\nAnything else:\n"
h += ["<h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function seek(t){var v=document.getElementById('player');var go=function(){v.currentTime=t;v.play();};if(v.readyState>=1){go();}else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}}</script></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("page written;", len(CH), "stills; em dashes:", "\n".join(h).count(chr(8212)))
