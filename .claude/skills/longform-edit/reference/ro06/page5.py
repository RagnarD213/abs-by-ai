"""RO-06 round 5 review page: the FULL FILM on top, What changed, What I decided (the seven older decisions as Dan answered
them, then the editor's own), the two app demos in their new form (stills + play in place), the six closing cover clips,
the checks as they came out (round5/checks_summary.json, written by hand from the logs), one reply box.
Writes round5/index.html. Serve with _shared/review_server.py PORT round5.  usage: page5.py"""
import json, os, html, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro06"; O = f"{W}/round5"; NAME = "RO-06 round 5 - full film"
M = f"{O}/{NAME}.mp4"; e = html.escape; os.makedirs(f"{O}/stills", exist_ok=True)
R = {r["id"]: r for r in json.load(open(f"{W}/plan_resolved.json"))}; FPS = Bd.FPS
TOTAL = json.load(open(M + ".build.json"))["frames"]/FPS
def mmss(t): return f"{int(t//60)}:{t % 60:04.1f}"
def grab(t, name):
    p = subprocess.run([Bd.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", M, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    Image.frombytes("RGB", (1920, 1080), p).save(f"{O}/stills/{name}.jpg", quality=90); return name
def item(k, said, what, fr_list):
    r = R[k]; st = []
    for j, (dt, cap) in enumerate(fr_list):
        t = r["t0"] + dt if dt >= 0 else r["t1"] + dt; st.append((grab(t, f"{k}-{j}"), f"{mmss(t)}, {cap}"))
    return dict(id=k, when=f"{mmss(r['t0'])} to {mmss(r['t1'])}", t0=r["t0"], said=said, what=what, stills=st)
DEMOS = [
 item("P01", "With Abs By AI, you're going to upload your current picture, you're going to make a picture of your goal ...",
      "Your approved sunglasses-to-pool demo: the same screens, the same steps, the same timing and the same AI-GENERATED label on the result. What is new is around it: the blue background and card in place of the olive one, and the phone body we use in the website video. Your real before picture carries the 'Real picture of me' label while the phone is up.",
      [(0.4, "your before picture"), (2.0, "the options"), (3.3, "generating"), (5.5, "the result, labelled")]),
 item("P02", "If you don't have a certain piece of equipment, we'll work around that ... using the equipment that you have in place.",
      "A real recording of the app: the workout list (each exercise has a 'Swap' link), a tap on 'How to do it', then the exercise sheet with its demo video. Upright phone with a visible tap, the format you approved for the website video. The demo inside the phone is AI footage of you, so it carries the AI-GENERATED label on the video. It is full screen because the closing shot is too close to fit a phone beside you.",
      [(0.5, "the workout list"), (1.2, "the tap"), (3.0, "the exercise sheet"), (-0.6, "the demo playing")]),
]
COVER = [
 item("C16", "So that's why eventually I want you to get a gym membership", "Stock clip from our library: a man bench pressing in a gym.", [(0.4, "start"), (-0.5, "end")]),
 item("C17", "You could also build a full gym at your house.", "Stock clip from our library: a man lifting in a home gym.", [(0.4, "start"), (-0.5, "end")]),
 item("C18", "Most important is going to be the barbells. I don't have any barbells in this setup", "Stock clip from our library: a plate goes onto a barbell.", [(0.4, "start"), (-0.5, "end")]),
 item("C19", "Leg press machine, that's another really important one.", "The app's own leg press demo (AI footage of you, labelled).", [(0.4, "start"), (-0.5, "end")]),
 item("C20", "The leg curl machine is another really important one.", "The app's own leg curl demo (AI footage of you, labelled).", [(0.4, "start"), (-0.5, "end")]),
 item("C21", "having access to bumper plates and a powerlifting platform, that will make it a lot better for you", "An AI clip we already own (labelled): a lifter loads a bar on a lifting platform.", [(0.4, "start"), (-0.5, "end")]),
]
BROLL = [
 item("C24", "So don't do your workouts prison style. Do it on a yoga mat.", "Your B-roll: plank up-downs on the blue mat.", [(0.4, "start"), (-0.5, "end")]),
 item("C23", "This will make it challenging again, so you build muscle even when you're athletic.", "Your B-roll: push-ups on the handles with your feet up on a chair.", [(0.4, "start"), (-0.5, "end")]),
 item("C27", "This comes in handy for many, many home workout exercises.", "Your B-roll: seated twists with the medicine ball.", [(0.4, "start"), (-0.5, "end")]),
 item("C25", "very useful for doing your curls, essential arm exercise.", "Your B-roll: standing dumbbell curls.", [(0.4, "start"), (-0.5, "end")]),
 item("C26", "variety of different arm exercises that you can do with these.", "Your B-roll: seated dumbbell overhead press.", [(0.4, "start"), (-0.5, "end")]),
 item("C30", "OK, guys, so that's how you build a basic home workout setup", "The real equipment, locked off and wide (same roll as the panning shot in the opening, a later part of it). It covers a nose wipe at the start of that take.", [(0.4, "start"), (-0.5, "end")]),
 item("C29", "we're also going to use AI to design a custom workout plan just for you.", "Your B-roll: you on your phone by the pool after a workout.", [(0.4, "start"), (-0.5, "end")]),
]
S = json.load(open(f"{O}/page_text.json"))        # CHANGED, DECIDED, CHECKS, OPEN written by the editor after the checks ran
grab(8.0, "poster")
css = open(f"{W}/recipe/page.py").read().split('css = """')[1].split('"""')[0]
css += (".three{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.three img{width:100%;border-radius:6px;display:block}"
        ".three div{font-size:13px;color:#9fb2cc;text-align:center}.ai{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:14px 0}ul li{margin:5px 0}"
        "table.ck{border-collapse:collapse;width:100%}table.ck td{border-bottom:1px solid #26354d;padding:6px 8px;vertical-align:top;font-size:14px}.ok{color:#7fd69a}.no{color:#ff9a8a}")
V = f"{NAME} - REVIEW 540p.mp4"
h = [f"<!doctype html><meta charset='utf-8'><title>RO-06 round 5</title><style>{css}</style>",
     f"<div id='dock'><div class='muted' id='docklabel'>The full film. Press any 'Play it in place' button.</div><video id='player' controls preload='none' poster='stills/poster.jpg' src='{V}'></video></div><main>",
     "<h1>How To Work Out At Home On A Budget: round 5, the full film</h1>",
     f"<div class='sub'>Long-form content, 16:9, {mmss(TOTAL)}. Built with your seven answers. Nothing is uploaded or scheduled.</div>",
     "<p><b>Locked by you and not touched:</b> the round 4 first minute (cropping, colour, voice, the tight open, the three opening clips, the fast jump rope, the panning equipment shot) and the four AI clips exactly as placed.</p>",
     "<h2>The full film</h2>", f"<video class='big' controls preload='none' poster='stills/poster.jpg' src='{V}'></video>",
     f"<p class='muted'>Also in the project folder for VLC: <b>Videos to Review / Work Out At Home LFC R5 - full film.mp4</b>. <a href='{NAME}.mp4'>Full 1080p file</a> &nbsp; <a href='RO-06 audio AB (reference then ours).mp4'>Audio A/B against the reference voice</a> &nbsp; <a href='RO06.srt'>Subtitles file</a> &nbsp; <a href='RO06.chapters.txt'>Chapters</a></p>",
     "<h2>What changed since the first minute you approved</h2><ul>"] + [f"<li>{e(c)}</li>" for c in S["CHANGED"]] + ["</ul>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in S["DECIDED"]] + ["</ol>"]
def block(it):
    n = len(it["stills"])
    return (f"<div class='ai'><span class='id'>{it['id']}</span> &nbsp; {e(it['when'])} &nbsp; <span class='muted'>You are saying: {e(it['said'])}</span><div class='three' style='margin-top:8px;grid-template-columns:repeat({n},1fr)'>"
            + "".join(f"<div><img loading='lazy' src='stills/{s}.jpg'>{e(c)}</div>" for s, c in it["stills"])
            + f"</div><div class='copy'><b>What it is:</b> {e(it['what'])}</div><button onclick=\"seek({max(0, it['t0']-3.0):.1f})\">Play it in place, from 3 seconds before</button></div>")
h.append("<h2>The two app demos (new to you in this form)</h2>"); h += [block(i) for i in DEMOS]
h.append("<h2>Six new clips over the closing section</h2><p class='muted'>The last two minutes had no cutaways. These are all from our own clip library: nothing was generated and nothing was bought. Strike any you do not want.</p>"); h += [block(i) for i in COVER]
h.append("<h2>Seven more cutaways through the middle (your own footage)</h2><p class='muted'>The delivery check wants at least 40% of a long video to be something other than you talking; the first full render read 33%. These are all footage you shot. (C30 is a later part of the same equipment roll as the panning shot in the opening.) Strike any you do not want.</p>"); h += [block(i) for i in BROLL]
h.append("<h2>One choice about the voice tone (15 seconds to hear)</h2><p>The automatic audio check passes every row except one: it reads your voice as too bright (around 5.5 kHz) in the stretch it measures, 0:20 to 2:20. The voice settings are the ones you approved on the first minute, so I left them alone. Here is the same 14 seconds both ways. If you prefer B, say so and I swap the sound for the whole film; the picture does not change.</p>"
         "<div class='three' style='grid-template-columns:repeat(2,1fr)'><div><video controls preload='none' src='tone_A_as_approved.mp4' style='width:100%'></video>A: as you approved it (in the film now)</div><div><video controls preload='none' src='tone_B_treble_trimmed.mp4' style='width:100%'></video>B: treble trimmed 4 dB (passes the check)</div></div>")
h.append("<h2>The checks, as they came out</h2><table class='ck'>" + "".join(f"<tr><td class='{'ok' if ok else 'no'}'>{'PASS' if ok else 'NOT PASSED'}</td><td><b>{e(n)}</b></td><td>{e(t)}</td></tr>" for ok, n, t in S["CHECKS"]) + "</table>")
if S.get("OPEN"): h += ["<h2>Things I want you to know before you approve</h2><ul>"] + [f"<li>{e(c)}</li>" for c in S["OPEN"]] + ["</ul>"]
reply = "RO-06 round 5, the full film\nApproved as is, or changes (time and what):\nApp demos P01 and P02:\nNew cutaways C16 to C30 (strike any):\nVoice tone: A (as approved)\nMusic bed (keep, quieter, louder, off): keep\nHair at the top edge in the last three minutes: leave as shot\nAnything else:\n"
h += ["<h2>Your reply</h2><p class='muted'>Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function seek(t){var v=document.getElementById('player');var go=function(){v.currentTime=t;v.play();};if(v.readyState>=1){go();}else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}}</script></main>"]
txt = "\n".join(h); open(f"{O}/index.html", "w").write(txt); print("page written; em dashes:", txt.count(chr(8212)) + txt.count(chr(8211)))
