"""RO-19 round 2 review page (later round: only what changed or is new). Order: decisions, the first minute, the voice options,
the two new photo pairs, new AI clip frames (doctor + four gag ideas), the four finished AI clips in context, the headroom
question, What I decided, one reply box. Writes round2/index.html. Serve with _shared/review_server.py 8865 round2."""
import json, os, html, shutil
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro19"; O = f"{W}/round2"; e = html.escape
R = {r["id"]: r for r in json.load(open(f"{W}/plan_resolved.json"))}
V = json.load(open(f"{W}/audio/opts2/options.json")); S = json.load(open(f"{W}/shots.json")); TOTAL = S[-1]["out_f1"]/(30000/1001)
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
def at(i): return mmss(R[i]["t0"])
def dur(i): return R[i]["t1"]-R[i]["t0"]
for d in ("frames", "audio", "stills", "motion-takes", "headroom"): os.makedirs(f"{O}/{d}", exist_ok=True)
NEW = ["D1", "G1", "G2", "G3", "G4"]
for i in NEW:
    for se in ("start", "end"): Image.open(f"{W}/aiframes/{i}-{se}.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{O}/frames/{i}-{se}.jpg", quality=90)
for k in V: shutil.copy(f"{W}/audio/opts2/{k}.mp3", f"{O}/audio/{k}.mp3")
for i in ("A4", "A3", "A2", "A1"): shutil.copy(f"{W}/round2/motion/{i}-t1.mp4", f"{O}/motion-takes/{i}-take1.mp4")
VOICES = [("W1-light", "W1: warm, light echo removal", "The exact voice you picked on Work Out Every Day."),
          ("W2-lightest", "W2: warm, lightest echo removal", "Closest to the microphone as recorded. The least processing of the four."),
          ("W3-more", "W3: warm, a step more echo removed", "The driest I can go without the voice starting to sound processed."),
          ("W4-less-boxy", "W4: warm, less boxy (in the first minute)", "W1 with more of the boxy kitchen tone taken out. Best numbers of the four."),
          ("B1-W4-bass+1.5", "B1: W4 with a little more bass", "A 1.5 dB lift around 120 Hz."),
          ("B2-W4-bass+3.0", "B2: W4 with more bass (my pick)", "A 3 dB lift. Its low end measures the same as the reference voice."),
          ("B3-W4-bass+4.5", "B3: W4 with the most bass", "A 4.5 dB lift. The deepest of the three, close to boomy."),
          ("0-untreated", "For comparison: the microphone as recorded", "Only the rumble below your voice removed.")]
IDEAS = [
 dict(id="D1", name="Talk to your doctor (reusable)", line=f"Replaces the stock doctor at {at('A5')}, under 'Researchers coming out showing that sun damage really increases your risk for many different health conditions.'",
      act="An ordinary man of about 45 in a polo and jeans sits talking with a male doctor in a plain exam room. The doctor explains with an open hand, then holds up a clipboard and points at it; the man leans in and nods. Nothing in the room names a condition, so it fits any 'talk to your doctor' line. When you approve the finished motion it goes in the clip library as the default for those lines.", slot=dur("A5"), cost="$0.60 for one 6 s take"),
 dict(id="G1", name="The eight hour wait", line="5:49, under 'I needed to wait eight hours before taking the shower.'",
      act="A freshly tanned man in a bathrobe sits on a stool in front of a shower sealed off with barrier tape, staring at the clock. The clock hands spin from nine to five, the light swings from morning to evening, and he slumps lower and lower with boredom.", slot=3.7, cost="$0.60 for one 6 s take"),
 dict(id="G2", name="One wipe of a washcloth", line="7:09, under 'No washcloths for the duration of the tan. The washcloth is gonna exfoliate and powerfully remove the tan.'",
      act="A proudly tanned man gives his forearm one wipe with a white washcloth. It leaves a clean pale stripe down his arm, the cloth comes away brown, and he stares at it in horror.", slot=4.5, cost="$0.60 for one 6 s take"),
 dict(id="G3", name="The spot he could not reach", line="13:39, under 'If you don't have a partner and you can't reach your whole body, it's going to be less even than a professional tan.'",
      act="A man by his pool shows off his do-it-yourself tan with a thumbs up, tanning mitt still on his hand. He turns to walk to the pool and the middle of his back is one big pale patch his mitt never reached.", slot=4.3, cost="$0.60 for one 6 s take"),
 dict(id="G4", name="She has seen it all", line="5:28, under 'Keep in mind though, these people are professionals. They see dudes in thongs all the time.'",
      act="A pale man stands in the tanning tent rigid with embarrassment, arms crossed, eyes shut. The specialist yawns into her coffee and sprays him without looking. He ends up tanned and surprised it is over; she is checking her watch.", slot=4.8, cost="$0.60 for one 6 s take"),
]
MOTION = [
 dict(id="A4", name="The appointment", note="The first 4.0 s of the 6 s take: she sprays, the tan comes up, she lowers the gun and he looks down. I left off the last 2 s, where he rubs his arm."),
 dict(id="A3", name="Destroy your sheets", note="Cut in two on purpose. In the full take the brown print fades in on a bare white sheet about half a second after he pulls the duvet back, which looks like a magic trick. So the film shows 1.4 s of him asleep in clean sheets, then a hard cut on the word 'sheets' to the print already there and his hand going to his head."),
 dict(id="A2", name="Too much tan", note="From 0.9 s of the take. The orange cloud hits on 'full Donald Trump color'. Small thing you may not catch at speed: a tiny made-up logo shows on her shirt for about a second."),
 dict(id="A1", name="Vampires", note="From 0.9 s of the take. The change from cowering to tanned happens as a half second dissolve inside the mist, which reads as part of the gag."),
]
DEC = [
 dict(t="Voice", rec="B2 (W4 with more bass)", opts=["B2: W4 with 3 dB more bass (recommended)", "Any other letter below: W1, W2, W3, W4, B1, B3", "A mix, for example 'W1 with B2's bass'"],
      why="Four warm versions with less room echo, then three with more bass, all on the same 31 seconds that start on your first word ('If you guys want to look good in photos'). You pick by ear. The first minute above is rendered with W4, the best measuring of the warm four, with no added bass yet."),
 dict(t="The two new photo pairs", rec="approve both", opts=["Approve both (recommended)", "Change one: say which and what you want instead"],
      why="Same pose in both halves, neither a double biceps. Pair 1: standing front on, arms down, the same teal shorts. Pair 2: side on, hands clasped at your hip. The pale side is from your 1 April shoot (I found 96 pictures of you from that day in your photo library, not just the four the old edit had). Both halves are cropped so your body is the same size."),
 dict(t="Doctor clip frames", rec="approve", opts=["Approve the frames (recommended): I generate the motion", "Change: say what (older or younger man, different room, different ending)"],
      why="The reusable 'man talking to his male doctor' clip you asked for. Start and end frames below."),
 dict(t="Which extra funny clips get made", rec="G1 and G3", opts=["G1 and G3 (recommended)", "Any two of G1, G2, G3, G4", "Three or all four: that goes over the $5 per video limit, so say 'go over' and I will"],
      why="Four more gag ideas with frames, for lines that have no good picture today. Frames cost nothing. Motion is $0.60 each. Spent so far: $3.00. The doctor clip takes it to $3.60, which leaves room for two more inside the $5 limit ($4.80 total). Turn down as many as you like."),
 dict(t="Headroom above your hair", rec="apply it to the whole film", opts=["Apply it to the whole film (recommended, after I fix the two flaws; you see it in round 3)", "Leave the camera's framing as shot"],
      why="The camera put the top of your hair on the top edge of the picture for the whole roll, so there is nothing above it to crop to. The proof below adds a strip above your head: the wall and door frame are continued upward and the cut part of your hair is rounded off from your own hair. Left is the camera, right is with headroom. Two flaws I can see and would fix first: on the wide shot the top of your hair is a little flat on some frames, and on a few frames a thin dark line runs from your hair up to the top edge. If the fixed version is not clean on every shot, I keep the camera's framing and tell you."),
]
DECIDED = [
 "The film now opens on the camera's wide shot, as you asked. After the before and after pictures it comes back wide as well and goes to the closer size at 0:26.",
 "Colour is F everywhere, both sizes. Everything graded is re-rendered in F from here on.",
 "Your before and after at 0:03 is untouched.",
 "The single pale photo at 0:48 is now a different picture from the 1 April shoot (grey shorts, hands at your waist), because the old one would have repeated the arms down pose of pair 1.",
 "In the three portraits at 3:00, photo 247 moved into pair 1, so photo 17 (towel on your shoulder) takes its place. No photo appears twice in the film.",
 "The clip of you on your phone by the pool at 2:11 is out (you ruled on 10-11 that it is never used). You stay on camera there with the lower third.",
 "Sheets clip: cut in two as described beside it, at no extra cost. If you would rather see the duvet pulled back in one move, a second take is $0.80.",
 "A third pair (hands on hips) did not make it: the pale shoot has no true hands on hips picture, so it would not have been the same pose.",
 "Voice options: one stronger echo setting measured past the processing limit on the audition clip, so I backed it off to the W3 you hear.",
 "Honest sound check on the first minute (voice W4): the delivery check passes 10 of 12 rows. It fails the tone match to the reference voice (expected with any fixed warm tone, the same as your Work Out Every Day pick) and the processing row by a hair (0.083 against a limit of 0.080; the untreated microphone already reads 0.079 on that minute). A listener heard no processing faults and no chopped words, but still heard the room and called the voice thin beside the reference. That points the same way you did: more bass (B1 to B3), and W3 if you want it drier.",
 "I ran five blind listening trials as a cross-check. They did not separate the options: five different winners in five trials, averages between 3.2 and 5.2 out of 10, W4 highest. That is noise, so the pick is yours by ear.",
 "The close: you did not answer in round 1, so I am building the app tour beside you (the Work Out At Home ending) into the full film. Say so if you want the two lower thirds instead.",
 "Not rendered, uploaded or queued: the full film. It is built in round 3, after your voice pick, the pairs and the doctor frames are locked.",
 "Spend: $3.00 of the $5.00 motion limit (four clips, one take each). Ten frame images on the Codex subscription. Six listening calls on Gemini, a few cents.",
]
css = open(f"{W}/recipe/page20.py").read().split('css = """')[1].split('"""')[0] + ".three{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.aud{grid-template-columns:290px 1fr 1.2fr}.rec{color:#7be08f;font-weight:700}"
fm = "first-minute/DRAFT - RO-19 round 2 - first minute"
h = [f"<!doctype html><meta charset='utf-8'><title>RO-19 round 2</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play any clip in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     "<h1>My First Spray Tan: round 2</h1>",
     f"<div class='sub'>Long-form content, 16:9. This round shows only what changed after your round 1 notes. The cut is locked at {mmss(TOTAL)} and the full film is not rendered yet.</div>",
     "<p><b>Already locked:</b> the cut and your take picks; the before and after at 0:03; every lower third, stock clip and other graphic from round 1 ('the rest of these are looking good'); the four AI clip frame pairs; Soft Blue Light graphics; no burned captions, no end mark.</p>",
     f"<h2>Your decisions ({len(DEC)})</h2>"]
for i, d in enumerate(DEC, 1):
    h.append(f"<div class='dec'><b>{i}. {e(d['t'])}.</b> {e(d['why'])}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in d['opts'])}</div></div>")
h += ["<h2>The first minute again</h2>", f"<video class='big' controls preload='none' poster='{fm}.jpg' src='{fm} - REVIEW 540p.mp4'></video>",
      f"<p class='muted'>Opens on the wide shot, colour F, voice W4, no music yet. What changed: 0:00 to 0:03 is the wide shot (was the closer size); 0:48 to 0:55 is a different pale photo. <a href='{fm}.mp4'>Full 1080p file</a><br>Also in the project folder for VLC: <b>Videos to Review / My First Spray Tan LFC R2 - first minute.mp4</b></p>",
      "<h2>Voice options</h2><div class='muted'>The same 31 seconds of the film, starting on your first word, all at the same loudness. Room echo is measured as the time your voice takes to die away after a word: 72 thousandths of a second as recorded, 44 to 53 in these, 40 on the reference voice.</div><div class='aud'>"]
for k, lab, what in VOICES:
    m = V[k]; h.append(f"<div>{e(lab)}</div><audio controls preload='none' src='audio/{k}.mp3'></audio><div class='muted'>{e(what)} Echo {m['edt']:.0f}.</div>")
h += ["</div>", "<h2>The two new photo pairs</h2><div class='three'>"]
for i, lab in (("P04", "Pair 1: arms down, front on"), ("P05", "Pair 2: side pose")):
    h.append(f"<div class='card'><img loading='lazy' src='stills/{i}.jpg'><div class='b'><span class='id'>{i}</span> <span class='muted'>{at(i)} to {mmss(R[i]['t1'])}</span><div class='copy'>{e(lab)}</div>"
             f"<a class='btn' href='context/{i}-context - REVIEW 540p.mp4' onclick=\"return play(this,'{i}')\">Play it moving, in context</a></div></div>")
h += ["</div><h3>Two photos swapped so nothing repeats</h3><div class='three'>"]
for i, lab in (("P02", "0:48, the single pale photo (new picture; it plays in the first minute above)"), ("P03", "3:00, the three portraits (third one is new)")):
    btn = f"<a class='btn' href='context/{i}-context - REVIEW 540p.mp4' onclick=\"return play(this,'{i}')\">Play it moving, in context</a>" if i == "P03" else ""
    h.append(f"<div class='card'><img loading='lazy' src='stills/{i}.jpg'><div class='b'><span class='id'>{i}</span><div class='copy'>{e(lab)}</div>{btn}</div></div>")
h += ["</div><h2>New AI clips: start and end frames</h2>"]
for a in IDEAS:
    h.append(f"<div class='dec'><b>{a['id']}. {e(a['name'])}.</b> {e(a['act'])}<br><span class='muted'>{e(a['line'])} Slot: {a['slot']:.1f} s. Motion: {e(a['cost'])}.</span>"
             f"<div class='pair'><div><img loading='lazy' src='frames/{a['id']}-start.jpg'>START</div><div><img loading='lazy' src='frames/{a['id']}-end.jpg'>END</div></div></div>")
h += ["<h2>The four approved AI clips, finished</h2><p class='muted'>One take each, shown in the film with a few seconds of your speech either side. Each carries the AI-GENERATED label.</p><div class='three'>"]
for m in MOTION:
    i = m["id"]
    h.append(f"<div class='card'><img loading='lazy' src='context/{i}-context.jpg'><div class='b'><span class='id'>{i}</span> <span class='muted'>{e(m['name'])} &middot; {at(i)} to {mmss(R[i]['t1'])}</span><div class='copy'>{e(m['note'])}</div>"
             f"<a class='btn' href='context/{i}-context - REVIEW 540p.mp4' onclick=\"return play(this,'{i}')\">Play it in context</a> &nbsp; <a class='btn' href='motion-takes/{i}-take1.mp4' onclick=\"return play(this,'{i} whole take')\">Play the whole take</a></div></div>")
h += ["</div><h2>Headroom above your hair: camera on the left, with headroom on the right</h2><div class='three'>"]
for f, lab in (("intro_W", "The opening, wide shot"), ("photos_T", "The closer size")):
    h.append(f"<div class='card'><video controls preload='none' poster='headroom/{f}.jpg' src='headroom/{f}.mp4' style='width:100%'></video><div class='b'><div class='copy'>{e(lab)}</div></div></div>")
h += ["</div><h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in DECIDED] + ["</ol>"]
reply = "RO-19 round 2\n" + "\n".join(f"{i}. {d['t']}: {d['rec']}" for i, d in enumerate(DEC, 1)) + "\nFinished AI clips (A4, A3, A2, A1), anything to change:\nFirst minute, anything to change:\nAnything else:\n"
h += ["<h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(a,id){var v=document.getElementById('player');v.src=a.getAttribute('href');document.getElementById('docklabel').textContent=id+' in context';v.play();return false;}</script></main>"]
txt = "\n".join(h); open(f"{O}/index.html", "w").write(txt); print("page written; em dashes:", txt.count(chr(8212)), "en dashes:", txt.count(chr(8211)))
