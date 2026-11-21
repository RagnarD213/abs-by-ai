"""SL-06 round 2 page copy (plain language for Dan; no em dashes). Dan skipped round 1, so this is his first review of
everything: the finished shorts, every graphic and clip, the AI frames and the open decisions."""
import os
import plans as P
ORDER = "DABCEF"
INTRO = ("All six shorts from the \"Top 5 Zepbound Tips\" long-form, finished, with your lav pickups from the 10/15 shoot laid in "
         "(A to E open on your pickup; F opens on a film line, as you approved). You skipped round 1, so everything is here for the "
         "first time: the six shorts, a 6-second clip of every pickup going into the film, the AI frames, what I decided, and every "
         "title, crop, clip, graphic and key point as stills. Each still has a button that plays that moment inside the finished short. "
         "No covers, no upload.")
LOCKED = ("the Soft Blue shorts look you approved on the salad shorts (title band on top for the whole short, two steady picture sizes, "
          "the two-line key-point bar, captions under it, clips filling the picture); the film's colour (same camera roll, same grade) and "
          "its approved sound, cut only; your segment picks and changes from 10-11; \"Not medical advice. Talk to your doctor.\" small at "
          "the bottom of every short; the AI-GENERATED chip on the film's AI clip in A.")
VLC = [f"Top 5 Zepbound Tips SFC R2 - short {S} - {t}.mp4" for S, t in [("D", "Inject On Thursday Evening"), ("A", "Start At 1 mg Not 2.5 mg"), ("B", "Use A Needle And Vial Not The Pen"), ("C", "How To Inject In 10 Seconds"), ("E", "How To Come Off Without Regaining It"), ("F", "How Much Protein You Need On A GLP-1")]]
SHORTS_NOTE = ("Play it plays the short in the one player (at the right on a wide screen). Pickup into film plays your recorded "
               "opening line and the first 3 seconds of the film after it.")
SHORT = dict(
 D="Your pickup over the calendar clip, then one continuous passage of the film. The restaurant clip is lifted to your brightness.",
 A="Dose only, as you asked. Your pickup over hands preparing an insulin syringe, then you on \"And for most of you watching this channel\".",
 B="Pen versus needle only. Your pickup (the long wording) over the vial and syringe clip, then five pieces of the film. Insulin syringes now on \"the tiny ones\" and \"units on the side of the barrel\".",
 C="Your pickup over a hand drawing a dose with an insulin syringe (the AI clip goes here if you approve its frames), then one continuous passage with the five steps.",
 E="Your pickup over the scale clip, then you on \"Coming off is where I see people destroy everything they built\". The staircase clip ends it (the AI gag goes here if you approve its frames).",
 F="Good as is, per your note. The sliced chicken under your first line, then you. The film's AI split screen is out (see What I decided).")
VOICE_DECISION = 7
VOICE_INTRO = ("Same take of short D's opening line, same picture, same loudness. A is built into all five shorts: an EQ fitted on your "
               "twelve lav takes toward the film's finished voice (same mic as the film, so the change is small), level matched to the next "
               "film line, the film's music under it. B uses the film's own voice settings instead (the EQ the film itself used, plus a "
               "little bass). By the numbers A is closer to the film; pick the one where you cannot hear the join.")
VOICE = [("/Volumes/Extreme/_edit_work/sl06/round2/joins/D_voiceA.mp4", "media/D voice A.mp4", "A: fitted EQ (built)", "an EQ fitted on your twelve lav takes toward the film's finished voice."),
         ("/Volumes/Extreme/_edit_work/sl06/round2/joins/D_voiceB.mp4", "media/D voice B.mp4", "B: the film's own voice settings", "the EQ the film used, plus a little bass. Same take, same loudness.")]
AI_INTRO = ("Stills only. Each pair passed the frame checks and an independent reviewer before it reached this page. Motion is made "
            "only after you approve the frames.")
AI = [("C", "<b>Short C opener (0:00 to 0:03), under your pickup \"Here's how to inject Zepbound with a needle, step by step.\"</b> "
            "A seated man brings a small insulin syringe down to the outer front of his thigh, midway down, and the short needle "
            "goes in. No pinch, stomach covered. About 3 to 4 seconds of motion, about $1 to $2. If you turn it down, C keeps the clip of a hand drawing a dose that it opens on now."),
      ("E", "<b>Short E's last line: \"Walk down the stairs instead of jumping off the roof.\"</b> A gag on purpose (your rule for lines "
            "with no literal picture): he winds up to hop off a low garage roof with the stairs right beside him, then a hard cut to him "
            "strolling down the stairs. Two short clips, about $2 to $3 together. If you turn it down, E keeps the staircase clip it ends on now.")]
AI_LABEL = {"C": ("START", "END"), "E": ("CLIP 1 START", "CLIP 2 START (after the cut)")}
DECISIONS = [
 "<b>Title band.</b> Built: <b>GLP-1 Tips</b>, because your standing note says brand names stay out of on-screen graphics until you rule on it, and short F's headline reads \"How Much Protein / You Need On A GLP-1\". The other way is <b>Zepbound Tips</b> (the still is in D's items): the film says Zepbound in every sentence and the captions spell it. This answer sets the rule for organic graphics going forward.",
 "<b>Title copy</b> for all six (in the reply box). Title case, two lines each.",
 "<b>Steps in shorts C and E.</b> Built: one step at a time in the key-point bar, with a counter (Step 1 Of 5). The other way, the film's whole list as a card, is the still at the end of C's items: with the title band on top it pushes the captions onto your mouth.",
 "<b>AI clip, short C opening.</b> Approve the frames for motion, ask for changes, or keep the clip of a hand drawing a dose.",
 "<b>AI gag, short E ending.</b> Approve the frames for motion, ask for changes, or keep the staircase clip.",
 "<b>Short B's opening line.</b> Built: the long wording you settled on while recording (\"...and why you should use a needle instead.\"). The short wording (\"Here's why you should stop using the pen to inject Zepbound.\") is on the roll if you prefer it.",
 "<b>Pickup sound.</b> A (built) or B, on short D's opening (section \"Pickup sound\").",
 "<b>Key-point copy</b> (every bar is in the reply box). Edit any line; two lines each.",
]
DECIDED = [
 "<b>Your lav pickups are laid in on all five</b> (A to E): your last clean take of each line from the 10/15 shoot (roll C1722). Treatment: a small EQ fitted toward the film's finished voice (same mic, so the change is small), level matched to the next film line, the film's music under it. No noise reduction, no dereverb. The desk-mic placeholders are gone.",
 "<b>A blind listening check of the five joins</b> (Gemini, with two of the film's own edits mixed in as controls): A, B, D and E were not heard at all. C was heard as \"slightly\" thinner at the join, milder than one of the film's own edits, which it heard \"clearly\". Listen to C's and B's \"Pickup into film\" buttons; the other treatment (decision 7) is the fallback.",
 "<b>How \"Zepbound\" sounds.</b> Speech software hears the last word of D's pickup as \"Zep out\", on the raw lav too, so it is how the line was said, not the cut. The film has the same spread. Judge it by ear on D's pickup clip; D's first take (heard as \"Z-Bound\") is on the roll if you want it.",
 "<b>B uses the long wording</b> you settled on while recording.",
 "<b>Graphic text is title case</b> (your 10-16 rule): bar labels read \"Key Point\", \"Step 1 Of 5\" and so on; the film charts read \"The Starting Ramp\" and \"How One Weekly Shot Works\". Capitals for emphasis kept on three words only: BELOW (A), YOU (B), SLOWLY (C).",
 "<b>The independent reviewers sent all six back once, and these were fixed</b> (re-rendered, gated and judged again): A's opening vials were labelled as a COVID vaccine, so A now opens on hands preparing an insulin syringe; B and C showed long hospital needles and a nurse injecting an arm, so they now use real insulin syringes (a hand drawing a dose, a syringe held up, a thumb on the plunger) and the arm injection is gone; C's man staring at a syringe is gone; B's first bar repeated your sentence, so it is out, and B's last bar now distills (\"Know Your Units, Then Draw To That Line\"); A's \"My Dose\" bar no longer prints a number you do not say in that short; D's restaurant clip is lifted to your brightness; D's chart headline now uses your words (\"Strongest In The First Few Days\"); A's ramp shows its three steps as outlines from the first frame instead of an empty screen; captions now end on every picture cut; short bars stay up longer; the small disclaimer has a soft shadow so it reads over white clips.",
 "<b>Also caught by the frame-by-frame checks:</b> you look up at the ceiling just before A's chart (the chart now comes in 0.4 s earlier); a smeared hand in the last second of A's AI clip (the clip now ends before it); a size step in E too small to read as a deliberate cut (now covered by the calendar clip); F's ab wheel cut your head off at full rollout (now a card as wide as the rollout); E opened on an empty scale for most of a second (now opens on the step).",
 "<b>More clips in C and E.</b> Both were mostly you on camera, which fails the 30% clip share the delivery check requires. Now C 34% and E 38%. E adds hands grabbing pizza (\"go off it again, and then regain\"), a calendar (\"per week\") and your fast jump rope by the pool (\"hold your new body the entire time\").",
 "<b>F: the film's AI split screen is out.</b> Both men's bodies change inside one take (soft to ripped), which fails your 10-13 rule, and it showed the gain on the \"loses muscle\" line. You stay on camera there. Only A now has an AI clip, so only A gets the AI flag at setup.",
 "<b>Rejected along the way:</b> a man massaging his knee (you say \"not down by your knee\"), a man eating on his phone (your phone rule), a shirtless heavy man on a scale (belly framing in the first 30 seconds), and a burger shot centred on a stomach. F's weight-training clip is now your real dumbbell curls (B0031); the clip the library called curls (B0458) is you holding the ab roller, so it is out and its library entry is corrected.",
 "<b>The AI frames were fixed before you saw them.</b> C's end frame took four regenerations and three hand fixes to pass the independent reviewer (the needle vanished, then the syringe changed shape, then a ghost needle, then the syringe read as empty). E's end frame had a leftover shoe on the roof, painted out.",
 "<b>D's couch clip was replaced</b> (a man on his phone) by a hand grabbing chips. <b>No pen-injection stock in B</b>: every pen clip frames a bare stomach.",
 "<b>Spend: about $0.10</b> (the Gemini listens). Frames were made on the ChatGPT subscription; the new stock is free Pexels footage. Motion for both AI clips, if you approve them: about $3 to $5, inside the $5 per video limit.",
 "<b>Not touched this round:</b> covers (a separate task), upload, queue. Posting order to suggest at setup: D, A, F, C, B, E, with A and B at least a week apart. Nothing posts before the long-form is public on Oct 25.",
]
CHECKS = [
 "<b>Delivery gate</b> (the one quality check every video passes, 39 rows: format, framing, captions in sync, sound, labels, banned screens, jump cuts, B-roll share): PASS on all six final files.",
 "<b>Sound:</b> the film's approved mix is cut only, never processed (checked sample for sample against the film); each short measures about -14.5 LUFS. Your pickups are level matched to the next film line within 0.7 dB.",
 "<b>Watch pass:</b> every frame of every short scanned for freezes, black frames and jump cuts, then a fresh judge looked at every cut frame by frame. No open defects.",
 "<b>Independent review:</b> two fresh reviewers watched all six without the editor's notes and sent every short back once; every item was fixed (see What I decided). A third fresh reviewer then re-checked all six: A to E ship; its one remaining item on F (the curls clip) was fixed, and F was judged and gated again.",
 "<b>AI frames:</b> both pairs passed the frame gate and a fresh independent reviewer before reaching this page.",
 "<b>Lengths:</b> A 47 s, B 54 s, C 54 s, D 51 s, E 58 s, F 55 s. All under 60 s.",
]
ITEM = {
 "D.calendar": "The film's calendar clip, turned upright, under your pickup.", "D.week": "The film's seven-day chart, redrawn for the tall frame. Same copy.",
 "D.chips": "Replaces the film's man-on-his-phone clip (your rule: a person looking at a phone is not a picture).",
 "A.ramp": "The film's 1 mg, 2 mg, 2.5 mg ramp, redrawn for the tall frame. Each step lands on its number.",
 "A.nausea": "Our AI clip from the film (A0137). This short gets the AI flag at setup.",
 "F.abwheel": "A card as wide as the rollout (full height): a full-screen or square crop cuts you off at full extension.", "F.curls": "Your real dumbbell curls by the pool (B0031), lifted for the overcast light.",
 "F.app": "The phone-beside-you layout you approved on the salad shorts.", "C.draw": "Stays only if you turn down the AI frames.", "C.plunger": "Lifted to your brightness (a black-background product shot).", "C.blood": "For \"draw blood out of your arm\".",
 "E.stairs": "Stays only if you turn down the AI gag.", "B.vialhand": "The film's 2:02 clip, under your pickup.",
 "B.draw": "A different clip from the film's here, because the film's is B's opening.",
 "B.supplies": "Vial and insulin syringes on a table.", "B.barrel": "An insulin syringe held up, barrel in view.", "A.vials": "Replaces a clip whose vials were labelled as a vaccine.",
 "C.needle": "The tiny insulin needle, for \"This is a tiny short needle\".",
 "E.regain": "New this round: hands on pizza for \"go off it again, and then regain almost all of it\".",
 "E.jumprope": "New this round: your fast jump rope by the pool (B0448) for \"hold your new body the entire time\".", "E.week": "Covers a size step that was too small to read as a deliberate cut.",
}
TAG = {"C.draw": "if no AI", "E.stairs": "if no AI", "C.needle": "new", "C.blood": "new", "C.plunger": "new", "B.supplies": "new", "B.barrel": "new", "A.vials": "new", "E.regain": "new", "E.jumprope": "new", "E.week": "new"}
EXTRA = {
 "F": [("F_split_option", "F: the film's AI split screen, taken out", "The film used this AI clip at \"studies have shown the average person loses a catastrophic amount of muscle\". Both men's bodies change inside one take, which your 10-13 rule says fails (a time jump needs a cut). You stay on camera instead. Say so if you want it back.", "removed")],
 "D": [("D_title_zepbound", "D: Title band, the Zepbound option", "The same frame with <b>Zepbound Tips</b> in the band (decision 1). Everything else identical.", "option")],
 "C": [("C_optB_listcard", "C: Steps, the list-card option", "The film's whole list as a bottom card (decision 3). With the title band on top there is no room: the captions land on your mouth and chin.", "option")],
}
def _bars():
    out = []
    for S in ORDER:
        for b in P.BARS.get(S, []): out.append(f"   {S} {b['id']}: {b['topic']}: " + " / ".join(p[0] for p in b["parts"]))
    return "\n".join(out)
def _titles():
    return "\n".join(f"   Short {S}: {P.TITLE[S][0]} / {' / '.join(P.TITLE[S][1])}" for S in ORDER)
REPLY = f"""1. Title band: GLP-1 Tips (built) / Zepbound Tips
2. Title copy: approved / edits:
{_titles()}
3. Steps in C and E: one step at a time in the bar / the list card
4. AI clip, short C opening: approve frames for motion / changes: / keep the syringe close-up
5. AI gag, short E ending: approve frames for motion / changes: / keep the staircase clip
6. Short B's opening line: long (built) / short
7. Pickup sound: A (built) / B
8. Key-point copy: approved / edits:
{_bars()}
Notes on any short (D, A, B, C, E, F):
Other notes (anything in "What I decided", any clip or crop):"""
