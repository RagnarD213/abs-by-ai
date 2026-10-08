"""RO-06 round 4 review page: the first minute with the four AI clips MOVING (Veo from Dan's approved frame pairs, the two
excuse clips lip-synced to his own impression), each clip with stills from the finished file and a 'Play it in place'
button, What changed, What I decided, the one new decision and the seven still open, one reply box.
Writes round4/index.html. Serve with _shared/review_server.py 8849 round4.  usage: page4.py"""
import json, os, html, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro06"; O = f"{W}/round4"; FM = "first-minute/DRAFT - RO-06 round 4 - first minute"
M = f"{O}/{FM}.mp4"; e = html.escape; os.makedirs(f"{O}/stills", exist_ok=True)
SPENT = round(0.24 + sum(x["usd"] for x in json.load(open(f"{O}/motion/ledger.json"))), 2)
def grab(t, name):
    p = subprocess.run([Bd.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", M, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    Image.frombytes("RGB", (1920, 1080), p).save(f"{O}/stills/{name}.jpg", quality=92); return name
# id, when, play-from, "you are saying", what happens, stills [(time, name, caption)]
AI = [("A1", "0:31.1 to 0:33.5", 31.13, "Dan I don't have time to go to the gym",
       "He whines the excuse, brings his arms up and taps his bare wrist. You stand with your arms crossed and roll your eyes on 'go to the gym'. His lips move to your impression.",
       [(31.35, "A1-a", "0:31.3, he starts whining"), (32.35, "A1-b", "0:32.3, tapping his wrist on 'time'"), (33.0, "A1-c", "0:33.0, you roll your eyes")]),
      ("A2", "0:33.5 to 0:35.8", 33.54, "or Dan I don't have the money for a gym membership.",
       "Closer shot. He fumbles the wallet open and it is empty, right on 'money'. You put your hand over your face at the same moment. His lips move to your impression.",
       [(33.75, "A2-a", "0:33.7, wallet still closed"), (34.6, "A2-b", "0:34.6, empty wallet and facepalm on 'money'"), (35.5, "A2-c", "0:35.5, 'membership'")]),
      ("A3", "0:38.9 to 0:41.2", 38.87, "(I'm) about to destroy all those excuses,",
       "You wind up with your left hand, it lands on 'destroy' (0:39.4), carries on down past his face, and his head whips round toward the camera. He comes back up reeling as the clip ends.",
       [(39.2, "A3-a", "0:39.2, the wind-up, left hand"), (39.5, "A3-b", "0:39.5, the hit, on 'destroy'"), (40.2, "A3-c", "0:40.2, your hand has gone past, his head whips round"), (41.0, "A3-d", "0:41.0, he comes back up")]),
      ("A4", "0:41.2 to 0:46.7", 41.17, "show you why they're all a crock of shit and explain to you why those excuses are not valid in any way whatsoever.",
       "He does two shaky push-ups on your push-up handles on the blue mat. You kneel beside him with the whistle in your mouth and point, then drop the whistle, pump your fist and shout him on.",
       [(41.6, "A4-a", "0:41.6, whistle and pointing"), (43.6, "A4-b", "0:43.6, down on the first push-up"), (45.6, "A4-c", "0:45.6, fist pump, second push-up")])]
for *_, st in AI:
    for t, n, _c in st: grab(t, n)
DEC = [
 ("The four AI clips, now moving", "Approve all four", ["Approve all four (recommended)", "Changes (say which clip and what)"],
  "Watch the first minute, or press 'Play it in place' under each clip below. If a clip needs another try, say which one and what is wrong. A new take of one clip costs $0.40 to $0.60, plus $0.20 where the lips are synced."),
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
 "The four placeholders are gone. A1, A2, A3 and A4 are now real moving clips, made from the start and end frames you approved (A3 from the new left-hand pair).",
 "In A1 and A2 the client's lips are synced to your own recorded impression. No new voice was made.",
 "A3 now starts a third of a second later than its placeholder did (0:38.9, not 0:38.6), so the clip opens on your wind-up. You stay on screen for those 9 extra frames, in the same shot and the same crop.",
 "Nothing else was touched. The audio is identical to the file you approved, checked sample by sample, and every frame of you that was on screen in round 3 uses the same crop and the same source frame (1,204 frames compared, 0 differences).",
]
DECIDED = [
 "A1: I used the last 2.4 seconds of the 4 second clip. That is the part where his arms come up and he taps his wrist, and your eye roll lands on 'go to the gym'.",
 "A2: I used the last 2.3 seconds. The wallet opening and your facepalm both land on the word 'money'.",
 "A3: the generated clip came out with two slaps, a light one and then a hard one. I used the hard one only: wind-up, hit on 'destroy', your hand carrying on past his face, his head whipping round, then him coming back up. That is why the clip starts a little later. If you would rather see both slaps (the first on 'destroy', the second on 'those'), tell me. It needs no new generation.",
 "A3, how the hit looks: your left hand lands flat on the side of his face and pushes through, then sweeps down across your body. It is a full-hand slap more than a glancing one across the cheek. Another take costs $0.40 if you want me to try for a different hit.",
 "A4: I used 5.5 of the 6 seconds, from just after the start. Two push-ups fit, with the whistle first and the fist pump second.",
 "No clip is slowed, held or sped up. Each one plays at the speed it was generated and is only trimmed.",
 "Lip sync: the sync tool also opened YOUR mouth for the last second of A1, as if you were talking. I kept the synced picture on his face only and the original picture everywhere else, so your mouth stays shut. I checked the finished file frame by frame: his lips close on the M in 'time', 'money' and 'membership'. The M at the end of 'gym' is loose.",
 "Your tank top shows the shield only in A1 and A2, and the shield with 'Abs by AI' under it in A3 and A4. That is how the frames you approved were drawn. Tell me if you want it matched.",
 "Each clip was checked at full size, frame by frame, for hands, fingers, the wallet, the whistle and the tank top. I found nothing a viewer would catch at normal speed. He is fully clothed throughout and no shot is framed on his stomach.",
 "I also had Gemini watch this stretch at normal speed. It agreed the slap reads as a slap and lands on 'destroy'. It called the lip sync unconvincing, but it only looks at one frame a second, so it cannot really judge lips. Your eye decides that one.",
 "One take of each clip was enough. No redos were bought.",
 f"Spend on this video so far: ${SPENT:.2f} of the $5 limit ($0.24 for the round 3 upscale, $1.80 for 18 seconds of Veo 3.1 Fast, $0.39 for the two lip syncs).",
 "At upload this video gets the AI flag turned on, because it now contains realistic AI footage.",
]
css = open(f"{W}/recipe/page.py").read().split('css = """')[1].split('"""')[0]
css += (".three{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.three img{width:100%;border-radius:6px;display:block}"
        ".three div{font-size:13px;color:#9fb2cc;text-align:center}.ai{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:14px 0}ul li{margin:5px 0}")
h = [f"<!doctype html><meta charset='utf-8'><title>RO-06 round 4</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>The first minute. Press any 'Play it in place' button.</div><video id='player' controls preload='none' poster='first-minute/poster.jpg' src='" + FM + " - REVIEW 540p.mp4'></video></div><main>",
     "<h1>How To Work Out At Home On A Budget: round 4, the first minute with the four AI clips moving</h1>",
     "<div class='sub'>Long-form content, 16:9. Only the first minute was rebuilt. The full film is not rendered yet: it waits for decisions 2 to 8 below.</div>",
     "<p><b>Locked by you and not touched:</b> cropping, colour and audio, the tight open, the three clips at the start, the fast jump rope clip and the panning equipment shot ('everything is looking good except A3'), and the start and end frames of all four AI clips ('A3 is approved').</p>",
     "<h2>The first minute</h2>", f"<video class='big' controls preload='none' poster='first-minute/poster.jpg' src='{FM} - REVIEW 540p.mp4'></video>",
     f"<p class='muted'>Also in the project folder for VLC: <b>Videos to Review / Work Out At Home LFC R4 - first minute.mp4</b>. <a href='{FM}.mp4'>Full 1080p file</a> &nbsp; <a href='first-minute/AB_reference-vs-ours.mp4'>Audio A/B against the reference voice</a></p>",
     "<h2>The four AI clips</h2><p class='muted'>Stills are pulled from the finished file. Every clip carries the AI-GENERATED label.</p>"]
for k, when, t0, said, act, st in AI:
    h.append(f"<div class='ai'><span class='id'>{k}</span> &nbsp; {e(when)} &nbsp; <span class='muted'>You are saying: {e(said)}</span><div class='three' style='margin-top:8px;grid-template-columns:repeat({len(st)},1fr)'>"
             + "".join(f"<div><img loading='lazy' src='stills/{n}.jpg'>{e(c)}</div>" for _t, n, c in st)
             + f"</div><div class='copy'><b>What happens:</b> {e(act)}</div><button onclick=\"seek({max(0, t0-3.0):.1f})\">Play it in place, from 3 seconds before</button></div>")
h += ["<h2>What changed</h2><ul>"] + [f"<li>{e(c)}</li>" for c in CHANGED] + ["</ul>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h.append(f"<h2>Your decisions ({len(DEC)})</h2><p class='muted'>1 is new. 2 to 8 are still open from earlier rounds; I have not assumed an answer to any of them. The full film gets built once these are answered.</p>")
for i, (t, rec, opts, why) in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
reply = "RO-06 round 4\n" + "\n".join(f"{i}. {t}: {rec}" for i, (t, rec, o, w) in enumerate(DEC, 1)) + "\nFirst minute, anything to change (time and what):\nAnything else:\n"
h += ["<h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function seek(t){var v=document.getElementById('player');var go=function(){v.currentTime=t;v.play();};if(v.readyState>=1){go();}else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}}</script></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("page written;", sum(len(a[5]) for a in AI), "stills; spent", SPENT, "; em dashes:", "\n".join(h).count(chr(8212)) + "\n".join(h).count(chr(8211)))
