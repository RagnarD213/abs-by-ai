"""Writes review/page_extra.json: the words on the RO-37 round 1 page. AI pairs come from ai/frames_report.json."""
import json, os
W = "/Volumes/Expansion/_edit_work/RO-37/round1"
S = json.load(open(f"{W}/shots.json")); L = S[-1]["out_f1"] / (30000/1001)
hair = json.load(open(f"{W}/review/first-minute/hair.json")) if os.path.exists(f"{W}/review/first-minute/hair.json") else {}
VS = {}
for f in ("trials_100.json", "trials_200.json"):
    p = f"{W}/options/voice/{f}"
    if os.path.exists(p):
        for k, v in json.load(open(p)).items(): VS.setdefault(k, []).extend(s for s, _, _ in v)
vm = {k: sum(v)/len(v) for k, v in VS.items() if v}
G = json.load(open(f"{W}/broll/grade.json"))
AIR = json.load(open(f"{W}/ai/frames_report_page.json"))
X = dict(
 intro=f"Cut from the four 10/23 pool rolls (C1893 to C1897, filmed upright on the phone-shaped camera setting). The film runs {int(L//60)}:{L%60:04.1f}. "
       "This round: the first minute, how the upright footage sits in a widescreen video, colour and voice options, seven AI clip ideas as frames, and every graphic and gym clip playing in place. "
       "No full film until you have picked. Release: Fri Jan 1, 2027 (finished and set up by Dec 18).",
 locked="this pool set's colour and voice from your approved Shorts as the recommendation (How To Do Hamstring Curls, How To Do Pull-Ups) as the starting point; Soft Blue Light graphics; the October 23 gym B-roll names and Color C.",
 decisions=[
  "<b>Presentation</b> (the footage is upright, the video is widescreen): <b>(a) your full upright picture in a rounded panel on the moving blue background, cutting to a widescreen close-up</b> (recommended: shows your physique, the blue matches the graphics, side lists sit beside you), (b) the same panel on a blurred copy of the pool, (c) close-up only (never shows below your chest).",
  "<b>Colour</b>: <b>F Deep And Vivid</b> (recommended, your pick on Hamstring Curls and Pull-Ups, same pool, same day), E Vivid Softer, or B Richer Contrast.",
  f"<b>Voice</b>: <b>A Natural Warmth</b> (recommended, your pick on three Shorts from this pool) or C Original Mic. In 10 blind listens the listener preferred C (average {vm.get('C', 0):.1f} vs A {vm.get('A', 0):.1f}), but its scores swung 3 to 9 on the same clip, so your own earlier ear decides unless you hear it differently. B and D are there too.",
  "<b>Opening</b>: open on the AI clip <b>“Frozen at the gym door”</b> (A1) under “If I walked into a gym for the first time today...” (recommended), or stay on you there. Either way, “Here's exactly what I'd do instead” cuts to three quick gym clips (bike, leg press, chest press).",
  "<b>AI clips</b>: which of the six ideas to animate (about five). Frames below; motion is free on your Flow subscription.",
  "<b>Weeks 2 to 4</b>: the script asked for a full-screen A/B card with a week strip. I used real clips of the three Workout B machines on their words, then an “Alternate” side list (Day 1: Workout A, Day 2: Workout B...). Keep, or build the full-screen card?",
 ],
 decided=[
  "Takes: the last clean take of every line (36 pieces from 4 rolls). Hook: the second take (C1894), with its “Alright,” lead-in trimmed.",
  "Cut ad-libs and restarts: “I know you're probably surprised like that”, the first “Most guys walking into a gym...”, “No matter how bad your day was, always do five minutes” (first try), both doubled “On every rep”, the abandoned first Workout A list, the restart “working out every day is far more important than”, “The guy who does a crazy two hour workout... three days a week” (you corrected to three weeks), the first “And that's the guy... in my experience”.",
  "Kept as filmed: “my first day on the gym”, “I'm just keeping it real with you guys”, your 80% line (spoken only; no number on any graphic).",
  "Gym B-roll: your own October 23 clips for every machine you name (bike B0566, leg press B0621, chest press B0678, seated cable row B0648, lat pulldown B0688, shoulder press B0682 and B0693, cable crunch B0574 and B0583, seat adjust B0691), each with its exercise name as a small label. The gym footage reads darker than the sunny pool, so each clip got a midtone lift that keeps the blacks (DS-76 method): median brightness " + ", ".join(f"{k.split('@')[0]} {v['before'][0]:.0f}→{v['after'][0]:.0f}" for k, v in list(G.items())[:4]) + "...",
  "Not filmed, so you stay on camera there: walking into the gym, the empty barbell area, walking between sets, stretching on the mats, walking out. Added to the next shoot list.",
  "No phone shot for “look up how to do an exercise on your phone” (a person looking at a phone shows nothing).",
  "Lower thirds distil the point instead of repeating it; eyebrows in capitals (RULE 1, REASON 2, KEY POINT), points in title capitals. The “Why listen to me” card names the dozens of beginners, not the 20 years you just said.",
  "Side lists push your panel to the right; it slides over smoothly as each list comes on and back when it goes.",
  "AI clip ideas: seven drafted, six passed the frame checks. “300 pounds on day one” (a beginner under an absurdly loaded bar) failed five times on the shoes and the body changing between frames, so it is left out and you stay on camera there; say if you want another try.",
  "Spend so far: $0 (frames on the Codex subscription; listening tests on Gemini, a few cents).",
 ],
 checks=[
  "Every join re-transcribed from the assembled voice (medium.en): no clipped or doubled words after four fixes (a clipped “tomorrow” and “Second”, a doubled “working”, a repeated “in my experience”).",
  ("Hair clearance on the first minute, every 0.25 s of you on camera: " + (f"closest {hair.get('min_px')} px (needs 20), {hair.get('verdict')}" if hair else "pending")),
  "Opening montage: bike B0575, leg press B0623 and chest press B0681 are different angles from the clips used again at 2:28, so nothing repeats.",
  "Graphics: all 24 built in Soft Blue Light HyperFrames, moving the whole time; every lower third and list fit-checked before rendering.",
  "Not run yet (they run on the full film after you lock the choices): the delivery gate, the audio gate stamp, the full jump-cut and junk pass, the independent reviewer.",
 ],
 first_minute=dict(end=round(S[[s['id'] for s in S].index('most.3')]['out_f1'] / (30000/1001), 2) if any(s['id'] == 'most.3' for s in S) else 61.09,
   note="Built with the recommended choices: presentation (a), colour F, voice A. The AI slots (the opener, “Done at hour two”, “Too sore for the stairs”) show you on camera until their motion is approved."),
 look_intro="The same moment each way. Pick one of each (decisions 1 to 3).",
 voice_note="The same first 30 seconds of the film, four ways, level matched.",
 presentation=[dict(key="a", name="Upright panel on the blue background + close-ups", what="Your full upright picture, hair to waistband, in a rounded panel on the moving Soft Blue field; cuts to a widescreen close-up keep it moving.", rec=True),
               dict(key="b", name="Upright panel on blurred pool + close-ups", what="The same panel over a blurred, darkened copy of the pool picture (the background treatment you locked for green-screen films).", rec=False),
               dict(key="c", name="Close-up only", what="A widescreen window of the upright picture: head and shoulders all the way through. Never shows your physique.", rec=False)],
 colour=dict(F=dict(name="Deep And Vivid", why="Your pick on Hamstring Curls and Pull-Ups (same pool, same day).", rec=True),
             E=dict(name="Vivid, Softer", why="A touch less contrast and saturation than F.", rec=False),
             B=dict(name="Richer Contrast", why="Your pick on the V-Taper Short; you called it a little washed out on Hamstring Curls.", rec=False)),
 voice=dict(A=dict(name="Natural Warmth", why="Your pick on Hamstring Curls, V-Taper and Pull-Ups: warm tone, subtle bass lift.", rec=True),
            C=dict(name="Original Mic, Matched Volume", why="The lav as recorded, only level matched. The blind listener's favourite here.", rec=False),
            B=dict(name="Fuller Bass", why="A with the standard +3 dB bass lift.", rec=False),
            D=dict(name="Automatic Reference Match", why="The shared chain's automatic tone match.", rec=False)),
 ai_intro="Six ideas, each a START and END frame, checked by the frame gate and an independent reviewer before this page. Approve the ones to animate; the rest leave you on camera. Motion runs on your Google Flow subscription.",
 ai=AIR.get("pairs", []),
 reply="Presentation: a\nColour: F\nVoice: A\nOpening: A1 Frozen at the gym door\nAI clips to animate: A1, A2, A3, A4, A6, A7\nWeeks 2 to 4: keep the clips and side list\nFirst minute notes:\nGraphics and clips notes:\n",
)
json.dump(X, open(f"{W}/review/page_extra.json", "w"), indent=1); print("page_extra ok;", len(X["ai"]), "AI pairs")
