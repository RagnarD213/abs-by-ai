"""RO-19 round 3: the words on the review page (round3/page_notes.json), with every time taken from the plan the film was rendered from.
CHECKS and REVIEW are filled in from the gates and the independent review after they have run. usage: pagenotes19r3.py"""
import json
W = "/Volumes/Extreme/_edit_work/ro19"; FPS = 30000/1001
R = {r["id"]: r for r in json.load(open(f"{W}/plan_resolved.json"))}; S = json.load(open(f"{W}/shots.json")); TOTAL = S[-1]["out_f1"]/FPS
SH = json.load(open(f"{W}/round3-plan/timeline_shift.json")); AT = SH["at_out_frame"]/FPS; DT = SH["frames"]/FPS
X = json.load(open(f"{W}/round3/page_checks.json"))          # written by hand from the logs: {"checks": [...], "review": "...", "extra_decided": [...], "extra_revisions": [...]}
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
def at(i): return mmss(R[i]["t0"])
def rg(i): return f"{mmss(R[i]['t0'])} to {mmss(R[i]['t1'])}"
SB = {x["id"]: x for x in S}
def st(k): return SB[k]["out_f0"]/FPS
def en(k): return SB[k]["out_f1"]/FPS
def half(i): return (R[i]["t0"] + R[i]["t1"])/2
N = dict(
 locked="the cut and your take picks; the before and after at 0:03; pair 2 at " + at("P05") + " and the three portraits at " + at("P03") + "; every lower third, stock clip and graphic you saw in round 1; the four AI clips you approved in round 2 (appointment, sheets, too much tan, vampires); the wide opening; colour F; Soft Blue Light graphics; no burned captions, no end mark.",
 vlc_film="My First Spray Tan LFC R3 - full film.mp4", vlc_first="My First Spray Tan LFC R3 - first minute.mp4",
 decisions=[
  dict(t="The film", rec="approved", opts=["Approved (recommended): I write the upload and setup handoff", "Changes: give me the time and what you want"],
       why=f"The whole film, {mmss(TOTAL)}, with your round 2 notes in. The list below takes you straight to each change."),
  dict(t="The doctor clip", rec="approve, save it as the default for 'talk to your doctor' lines", opts=["Approve and save it to the clip library as the default (recommended)", "Use it here but do not make it the default", "Change it: say what"],
       why=f"The reusable man-and-his-doctor clip you asked for, now moving, at {rg('A5')}. If you approve it I register it in the clip library as the default for every 'talk to your doctor' line."),
 ],
 revisions=[
  dict(whole=True, t0=26.0, t1=57.0, pad=0, was="Voice W4, warm with light echo removal", now="Voice B2 on the whole film: the same voice plus the 3 dB bass lift you picked. Listen anywhere; 0:26 to 0:57 is a good stretch."),
  dict(id="P02", clip=True, was="A soft-looking pale photo (grey shorts, hands at the waist)", now="The driveway photo from the same 1 April shoot: pale, arms down, abs clearly defined"),
  dict(id="G1", clip=True, was="You on camera with the lower third", now="New funny AI clip: the eight hour wait. A man in a bathrobe stares at the clock by a taped-off shower while the hands spin from nine to five"),
  dict(id="P04", clip=True, was="Pair 1 with a tan-filtered copy as the pale half", now="Pair 1 with the untinted original of the same frame. Same pose, same crop, clearly paler"),
  dict(t0=AT - 6.4, t1=AT + DT, pad=4, was="The Bryan Johnson sentence stopped half way: 'that's the reason why he only goes out in the sun' and straight into the next line",
       now="The rest of your sentence is back: '...during off-peak hours, not in the bright sun in the noontime, and why he takes an umbrella out with him when he goes out in the sun.' The film is 7 seconds longer for it"),
  dict(id="A5", clip=True, was="Two still frames as a placeholder (round 2)", now="The doctor clip, moving: he explains, lifts the clipboard and points, the man leans in and nods"),
  dict(id="G3", clip=True, was="You on camera with the lower third", now="New funny AI clip: the spot he could not reach. Proud thumbs up, he turns, and the middle of his back is one pale patch"),
  dict(id="P07", clip=True, was="Two feature lower thirds over you on camera", now="The app tour beside you (the Work Out At Home ending): workout demo videos on the trainer line, calorie tracking from a meal photo on the nutritionist line"),
  dict(whole=True, t0=0.0, t1=12.0, pad=0, was="No music", now="A very quiet music bed under the whole film, the same track and setting as Work Out Every Day. You will only notice it in the pauses"),
  # fixes from the independent reviews: each changes something you saw in round 1 or 2
  dict(t0=st("visit.0r1"), t1=en("visit.0r1"), pad=3, was="The wide shot ran 54 seconds without a change from 4:21 to 5:15", now="Two size changes break it up: the closer size here and again at " + mmss(st("visit.0r4")) + " to " + mmss(en("visit.0r4")) + ". Same take, nothing cut"),
  dict(t0=R["Cc07"]["t0"], t1=half("Cc07"), pad=3, was="The stock swimmer had sunk low in the frame and the lower third lay across his face", now="The same clip from its start: he is at the pool edge and his face is clear of the lower third"),
  dict(id="A3", pad=3, was="AI-GENERATED label top right, on the side of the man's head", now="The label is top left, off him. Same clip. Also on the orange tan clip at " + rg("A2")),
  dict(id="Cc20", pad=3, was="Two stock portraits (a red-haired man, then a red-haired woman whose chin sat under the lower third)", now="The red-haired man holds the whole line; the woman's portrait is out"),
  dict(t0=R["Cd10"]["t0"], t1=half("Cd10"), pad=3, was="The stock fashion model shot started inside the clip's own glitch effect: the picture rolled and tore for about a second", now="The same clip from its clean start: the model walks toward the camera"),
 ] + X.get("extra_revisions", []),
 unchanged="Everything else is as you approved it in rounds 1 and 2: same takes, same lower thirds and copy, same stock and AI clips, same sizes and colour. Because of the restored sentence, everything after 10:23 now sits 7 seconds later than the times on the round 2 page.",
 first_note="The first minute, cut from the film above. What changed in it: the photo at 0:48, the voice, and the music bed.",
 motion=[
  dict(id="A5", name="Talk to your doctor", still=3.0, note="From 0.2 s of the 6 s take to its end. No faults I can see at speed or frame by frame."),
  dict(id="G1", name="The eight hour wait", still=3.3, note="3.9 s of the take, from 0.6 s. The change from morning to evening light happens in one frame while the clock hands are spinning, so it reads as a time-lapse jump. The lower third 'Rapid Tan: 8 Hours.' builds over it."),
  dict(id="G3", name="The spot he could not reach", still=3.2, note="4.3 s of the take, from 0.7 s. The pale patch is on screen as you say 'you can't reach your whole body'. Small thing you may not catch at speed: as he turns, the mitt ends up on his other hand (it changes over about a quarter of a second, low in the frame)."),
 ],
 p02="The driveway set you pointed me to has 18 frames. This is the one with the clearest abs and your eyes open (14:50:13). The one with the very sharpest abs has your eyes shut.",
 p04="The pale half you approved was a filtered copy of a frame in your library. I found the full-size original taken the same second, confirmed it is the same picture without the tint, and cut it to the identical crop. Old and new side by side below.",
 decided=[
  "A cut that went wrong, fixed: proofreading the captions I found the Bryan Johnson sentence cut off in the middle. The cut list ended that piece on 'goes out in the sun', which you say twice in that sentence, and it stopped at the first one. That was in the cut since round 1 and neither of us had seen that stretch. I restored the rest of the sentence. I then checked all 38 pieces of the cut the same way: no other piece ends early.",
  f"The app tour follows your words. In Work Out At Home you said calorie tracking first; here you say trainer, then nutritionist, so the phone shows the workout videos first and calorie tracking second. You sit 270 pixels to the right for those 15 seconds; your hands stay inside the frame and clear of the phone the whole time (measured on every third frame).",
  "The pale photo: I picked the driveway frame myself rather than send you 18 to choose from. Say so if you want a different one from that set.",
  "The two extra funny clips are G1 and G3, as you chose. G2 (washcloth) and G4 (bored specialist) were not made.",
  "No headroom was added. The camera put the top of your hair on the top edge for this whole roll, and you said to leave it.",
  "B-roll brightness: I checked every clip beside your kitchen picture. Five of your own clips were clearly darker than you on camera (the ab wheel and dumbbells at " + at("Cb12") + ", the push-up at " + at("Cd17") + ", the two poolside poses at " + at("Cd07") + " and " + at("Cd20") + ") and four stock clips read dark (the gym at " + at("Cd01") + ", the two photo studios at " + at("Cc08") + " and " + at("Cd11") + ", the handshake at " + at("Cd09") + "). All are lifted to sit with the kitchen footage. After the independent review I lifted six more a little (the AI desk at " + at("Cb04") + ", the bills at " + at("Cb07") + ", the spray can at " + at("Cb08") + ", the lotion at " + at("Cb11") + ", the indoor pool at " + at("Cd04") + ", the fire escape at " + at("Cd14") + ") and the poolside poses further. The dating app shot at 0:28 is as you approved it in the first minute. The meal prep clip at " + at("Cd06") + " got a little more colour.",
  "The two poolside posing clips (" + at("Cd07") + ", side on, and " + at("Cd20") + ", front on) come from the same roll two minutes apart in the film. Different poses, same pool and shorts. I kept both because each sits on a line about showing your body or posing, and the library has no other horizontal posing clip of you.",
  "One long stretch on the wide shot: 4:21 to 5:15 is 54 seconds at the wide size with five lower thirds over it. Your hands move a lot there and the closer size would cut them off. You turned down the gag clip that would have broken it up (G4).",
  "Music: the acoustic bed from your last finished films, at the Work Out Every Day setting. Be aware it is very quiet: it sits about 35 dB under your voice and you will only notice it in the pauses, if at all. That is as loud as the sound check allows on this recording (one row of the check measures how clean the gaps between your words are, and a louder bed fails it). Say 'louder music' if you want it up anyway. I transcribed five minutes of it to make sure it carries no words.",
  "Two more long holds I looked at: " + mmss(st("last.0r0")) + " to " + mmss(en("last.0r2")) + " stays 26 seconds on the wide shot. Its middle is where you lift your shirt to show the tan on your abs, which the closer size would cut off, and the shots either side cannot change size without a same-size join.",
  "Things the reviewers noted that I left for you: at 2:53 there is a small false start in your speech ('on the abs and the... to enhance'), you are on camera and it reads as natural speech; nine lower thirds come on with their heading a second or two before the main line lands on your words (the approved word-timed build); the dumbbell curls clip at " + mmss(half("Cb12")) + " has a light stand at the left edge of frame; the red-haired man's portrait at " + at("Cc20") + " holds for 6 seconds; the AI clip of the man at his monitors at " + at("Cb04") + " is a night scene and stays darker than the kitchen. None of these changed this round.",
  "Captions file: proofread against the sound. I corrected about 25 misheard words and missing full stops ('ads by AI', 'GOP1', 'face clubs', 'a Sprite tan', 'Brian Johnson' and so on). Captions are a separate file, never burned in.",
  "Chapters: the 17 chapter titles from round 1, each now starting on the first sentence of its section (the round 1 times sat a few seconds late).",
 ] + X.get("extra_decided", []) + [
  "Spend: $4.80 of the $5.00 motion limit for this video (seven AI clips, one take each). No new images were needed this round. Gemini: nothing new.",
  "Not done: nothing is uploaded or queued. Upload and setup is its own task once you approve the film.",
 ],
 checks=X["checks"],
)
json.dump(N, open(f"{W}/round3/page_notes.json", "w"), indent=1); txt = json.dumps(N, ensure_ascii=False); print("notes written; em dashes:", txt.count(chr(8212)), "en dashes:", txt.count(chr(8211)))
