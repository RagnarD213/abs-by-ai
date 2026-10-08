"""RO-06 round 1 review page (standard layout: decisions, first minute, pictures, What I decided, every item three per row,
one docked player, one reply box). Writes round1/index.html. Serve with _shared/review_server.py PORT round1."""
import json, os, html
W = "/Volumes/Extreme/_edit_work/ro06"; O = f"{W}/round1"
rows = json.load(open(f"{O}/stills.json")); num = json.load(open(f"{O}/look/numbers.json"))
ctx = {f.split("-context")[0] for f in os.listdir(f"{O}/context") if f.endswith("REVIEW 540p.mp4")}
def mmss(t): return f"{int(t//60)}:{t%60:04.1f}"
e = html.escape
DEC = [
 ("Colour", "B, Rich (used in the first minute)", ["A, Natural", "B, Rich (recommended)", "C, Bright"],
  "The sun was going down during the shoot, so every roll gets its own correction to keep your skin the same brightness from start to finish. Three strengths are shown below on four moments."),
 ("Framing", "Approve the two sizes as built", ["Approve", "Make the tighter size less tight"],
  "Two fixed sizes, cut between on every join: the camera frame as shot (you plus the equipment), and a 1.5x punch-in (hair to mid-thigh). Same approach as Zeeshan's ab wheel videos. No camera movement."),
 ("Hair at the top edge", "Leave as shot for this cut", ["Leave as shot", "Add headroom by extending the background above your head (one extra round)"],
  "On 9 of the 20 rolls (jump rope through the second medicine ball clip, and the closing section) the camera framed your hair 5 to 15 pixels from the top edge. Nothing is cropped off by me, but there is no spare picture above your head to add. This one is for Jeff on the next shoot too."),
 ("Length", "A: trim three pure repeats, about 16:30", ["A: trim three repeats, about 16:30 (recommended)", "B: keep everything, 17:39", "C: deeper trim to about 15:00"],
  "A cuts only places where you restate a point you already made: the 'I don't care how poor you are' run after the $58 total (26 s), the second explanation of why you don't need the rubber coating (14 s), and the closing restatements of 'this is a great way to get started' (25 s). C also trims the medicine ball form detail and the full dumbbell rack advice."),
 ("Product pictures", "Keep the AI-made pictures (labelled)", ["Keep AI pictures (recommended)", "Use real product photos you send me", "No pictures, prices as lower thirds only"],
  "You say 'the one you're seeing on your screen right now' six times, so each price card needs a picture. No Amazon screenshots per the job rule, so Codex made six plain product pictures, each carrying the AI-GENERATED label."),
 ("Jump rope price", "Keep as built", ["Keep as built", "Cut the words 'for just $10'"],
  "You say '$10' in the jump rope section and '$9' in the total (which is what adds up to $58). Built: no price on screen in the jump rope section, $9 in the total list."),
 ("Music", "Add a quiet music bed", ["Add a quiet bed under your voice (recommended)", "Voice only"],
  "The first minute below is voice only. Zeeshan's ab wheel videos carry a soft bed; our last two long-forms (Calories, Belly Fat) did not."),
 ("App demo at the end", "Rebuild it in the blue phone card", ["Same approved demo, in the Soft Blue phone card (recommended)", "Exactly as approved, olive background"],
  "For 'upload your current picture, make a picture of your goal' I use your approved sunglasses-to-pool demo. It was built on the old olive background. The steps and the AI label stay identical either way."),
 ("Opening", "Keep the on-camera open", ["Keep the on-camera open with your own B-roll (recommended)", "AI opener 1: man in a small apartment unrolls a mat beside a kettlebell and ignores a gym sign-up flyer", "AI opener 2: man in gym clothes stuck in traffic checks the clock, then is doing push-ups at home"],
  "The video opens on you with the real equipment at your feet, then your own push-up and ab wheel clips. If you want an AI opener I will send start and end frames first."),
]
DECIDED = [
 "Intro: your last take (the fourth), complete and clean. Take 1 lacks the COVID line; takes 2 and 3 you stopped yourself.",
 "Excuses: your second take says 'you want to lose in shape', so that sentence comes from the first take and the rest from the second.",
 "Kettlebell price: the main take says '$45 for a $35 kettlebell'. The same line said right in the earlier clip replaces it, hidden under the kettlebell price card.",
 "Closing: take 2 of 3. It is the latest take with no restart inside it (take 3 restarts twice).",
 "Gym membership line: a hidden false start ('That means you're going to have to drive a few minutes...') removed.",
 "Left out as repetition, easy to restore: the last 52 s of dumbbell advice (up to 100 lb, your own rack) and the 37 s recap of one, two and three pairs.",
 "Amazon link request stays where you filmed it (1:16), in its one clean take.",
 "Swearing kept. No AbsByAI.com mark at the end.",
 "Graphics: Soft Blue Light throughout, built from the approved templates. Each item gets a numbered lower third, a price card, and one key point.",
 "Side lists: only the $58 total uses the left card. On the dumbbell, recap and gym sections your arms would cross it, so those are lower thirds whose parts land as you name them.",
 "B-roll: your own filmed clips only (push-ups, handles, jump rope, ab wheel, lunges, squats, swings, toe touches, laterals, towel). They are from other days (green shorts), no clip used twice.",
 "Removed: the library's AI powerlifter deadlift clip, because it has another video's caption burned into it.",
 "No AI video clips. Spend so far: $0 (six Codex product stills on the subscription).",
 "Audio: lav only, shared voice chain, no echo removal. The first minute passes the audio gate (12 of 12).",
 "No burned captions. The subtitle file comes with the finished film.",
]
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 420px 60px 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}.opt{color:#cfe2f7;margin:4px 0 0 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#14223a;border:1px solid #26354d;border-radius:10px;overflow:hidden}
.card img{width:100%;display:block}.card .b{padding:9px 11px;font-size:13px}.id{font-weight:700;color:#8fd0ff}.copy{color:#fff;margin:4px 0}.muted{color:#9fb2cc}
details{margin-top:5px}summary{cursor:pointer;color:#9fb2cc}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}
#dock{position:fixed;right:14px;top:14px;width:384px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:10px}#dock video{width:100%;border-radius:6px;background:#000}
.look{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.look img{width:100%;border-radius:6px}.look div{font-size:12px;color:#9fb2cc;text-align:center}
textarea{width:100%;height:230px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li{margin:5px 0}a{color:#8fd0ff}
@media(max-width:1300px){main{margin-right:28px}#dock{position:static;width:auto;margin:14px 28px}}"""
h = [f"<!doctype html><meta charset='utf-8'><title>RO-06 round 1</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play any item moving, in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>How To Work Out At Home On A Budget: round 1</h1>",
     "<div class='sub'>Long-form content, 16:9, first cut from the 8/3 pool rolls (C1557 to C1581). The full film runs 17:39 as cut and is not rendered yet: this page locks the look, the graphics and the clips first.</div>",
     "<p><b>Already locked and reused:</b> Soft Blue Light graphics and the approved lower third, price card and side list templates; the shared voice chain; hard cuts, no swipe sounds, no camera movement.</p>",
     f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, (t, rec, opts, why) in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(t)}.</b> {e(why)}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in opts)}</div></div>")
fm = "first-minute/DRAFT - RO-06 round 1 - first minute"
h += ["<h2>The first minute, finished</h2>", f"<video class='big' controls preload='none' poster='first-minute/poster.jpg' src='{fm} - REVIEW 540p.mp4'></video>",
      f"<p class='muted'>Colour B, voice only. <a href='{fm}.mp4'>Full 1080p file</a> &nbsp; <a href='first-minute/AB_reference-vs-ours.mp4'>Audio A/B against the reference voice</a></p>",
      "<h2>Decision 1: colour, on four moments</h2><div class='muted'>Left to right: camera original, A Natural, B Rich, C Bright. Measured on these frames (brightness / saturation): "
      + ", ".join(f"{k if k != 'raw' else 'original'} {v['luma']:.2f} / {v['sat']:.2f}" for k, v in num.items()) + ". Approved Belly Fat film for comparison: 0.24 / 0.35 (indoors).</div><div class='look'>"]
for p in ("hook.0r0", "wheel.0r1", "db3.0r2", "cav2.0r3"):
    for k in ("raw", "A", "B", "C"): h.append(f"<div><img loading='lazy' src='look/{p}_{k}.jpg'>{'original' if k == 'raw' else k}</div>")
h += ["</div><h2>Decision 2: the tighter framing (colour B)</h2><div class='look'>"] + [f"<div><img loading='lazy' src='look/{p}_T-B.jpg'>tighter size</div>" for p in ("hook.0r0", "wheel.0r1", "db3.0r2", "cav2.0r3")] + ["</div>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
h += [f"<h2>Every graphic and clip, in order ({len(rows)})</h2><div class='grid'>"]
KIND = {"lt": "lower third", "fact": "price card", "l3": "side list", "clip": "clip"}
for r in rows:
    c = r["copy"]; lines = []
    if "topic" in c: lines.append(f"{e(c['topic'])}: {e(c['point'])}")
    if "heading" in c: lines.append(e(c["heading"]) + ": " + e("; ".join(c["points"])))
    if "eyebrow" in c: lines.append(e(c["eyebrow"][0]) + " / " + e(" ".join(x[0] for x in c["headline"])) + " / " + e(c["detail"][0]))
    if r["kind"] == "clip": lines.append(e(r.get("note") or ""))
    if c.get("label"): lines.append("Label on screen: " + e(c["label"]))
    if r.get("pending"): lines.append("<b>PLACEHOLDER still: this goes inside the phone card in the full build (decision 8)</b>")
    btn = f"<button onclick=\"play('{r['id']}')\">Play it moving, in context</button>" if r["id"] in ctx else ""
    h.append(f"<div class='card' id='{r['id']}'><img loading='lazy' src='stills/{r['id']}.jpg'><div class='b'><span class='id'>{r['id']}</span> <span class='muted'>{KIND[r['kind']]} &middot; {mmss(r['t0'])} to {mmss(r['t1'])}</span>"
             f"<div class='copy'>{'<br>'.join(lines)}</div>{btn}<details><summary>What you are saying</summary><span class='muted'>Before:</span> {e(r['before'])}<br><span class='muted'>During:</span> {e(r['during'])}<br><span class='muted'>After:</span> {e(r['after'])}</details></div></div>")
reply = "RO-06 round 1\n" + "\n".join(f"{i}. {t}: {rec}" for i, (t, rec, o, w) in enumerate(DEC, 1)) + "\nGraphics or clips to change (ID and what):\nAnything else:\n"
h += ["</div><h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(id){var v=document.getElementById('player');v.src='context/'+id+'-context - REVIEW 540p.mp4';document.getElementById('docklabel').textContent=id+' in context';v.play();}</script></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("page:", len(rows), "items,", len(ctx), "context clips,", "em dashes:", "\n".join(h).count("—"))
