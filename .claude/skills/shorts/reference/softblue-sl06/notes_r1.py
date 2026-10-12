"""SL-06 round 1 page copy (plain language for Dan; no em dashes)."""
import json, os
ORDER = "DABCEF"
PK = "/Volumes/Extreme/_edit_work/sl06/pickups"
rep = json.load(open(PK + "/D.report.json")) if os.path.exists(PK + "/D.report.json") else None
INTRO = ("Six shorts from the approved \"Top 5 Zepbound Tips\" long-form (your picks A to F; G is out). This round: short D "
         "finished with your recorded opening line, start and end frames for two new AI clips, and every title, crop, clip, graphic and "
         "key point of all six as stills on real frames. The other five are planned to the frame but not rendered. No covers, no upload.")
LOCKED = ("the Soft Blue shorts look you approved on the salad shorts (title band on top for the whole short, two steady picture sizes, "
          "two-line key-point bar, captions under it, clips filling the picture); the film's colour (same camera roll, same grade) and its "
          "approved sound, cut only; your segment picks and changes from 10-11; \"Not medical advice. Talk to your doctor.\" small in the "
          "corner of every short; AI-GENERATED chips on the AI clips.")
D_REVIEW = "review/Top 5 Zepbound Tips SFC R1 - short D - Inject On Thursday Evening - REVIEW 540p.mp4"
_pk = ("<p><b>Known fault in this copy:</b> your opening line (0:00 to 0:03) carries dropouts from the recording tool and will be replaced "
       "with a clean re-read. The film's own sound from 0:03 on is untouched. When the clean take is in, it gets the same treatment as planned: "
       "tone and level matched to your voice in the film, the film's music under it, no echo or noise removal.</p>")
D_TEXT = ("<p><b>What to check:</b> the first 4 seconds (your recorded opening line over the calendar clip, then the cut to you on "
          "\"The medication is strongest...\"), the weekly chart at 0:07, the four weekend clips from 0:21, and the key point at 0:32.</p>"
          + _pk +
          "<p>Full quality copy for VLC: <b>Videos to Review / Top 5 Zepbound Tips SFC R1 - short D - Inject On Thursday Evening.mp4</b></p>"
          "<p>Sound check clip (the film's own cut of this passage, then the short): <a href=\"review/AB_film-vs-short_D.mp4\">AB_film-vs-short_D.mp4</a></p>")
AI = [("C", "<b>Short C opener (0:00 to about 0:04), under your pickup \"Here's how to inject Zepbound with a needle, step by step.\"</b> "
            "A seated man brings a small insulin syringe to the outer front of his thigh, midway down. No pinch, no stomach in frame. "
            "About 4 seconds of motion, about $1 to $2. The title band covers the top of the frame and captions sit low, so the syringe is placed mid-frame. "
            "If you turn it down, C opens on the syringe close-up shown in short C below."),
      ("E", "<b>Short E last line: \"Walk down the stairs instead of jumping off the roof.\"</b> A gag on purpose (your 10-10 rule for lines with no "
            "literal picture): he winds up to hop off a low garage roof with the stairs right beside him, then hard cut to him strolling down the stairs. "
            "Two short clips, about $2 to $3 together. If you turn it down, E ends on the plain staircase clip shown in short E below.")]
DECISIONS = [
 "<b>Your pickups need one more read (2 minutes).</b> The recording tool dropped tiny slices of sound on every take from 10-12 (about 11 % of the audio, a 10 ms slice missing every 90 ms). You will hear it in short D's first 3 seconds as a rough, slightly hurried stutter. It cannot be repaired, so none of these takes ship. The recorder is replaced and tested clean. Say \"go\" in the task and read the five lines once more; short D's opening is then rebuilt. Judge D's picture, timing and everything after 0:03 as it is.",
 "<b>Drug name in the title band.</b> A: <b>ZEPBOUND TIPS</b> as shown on every still (recommended: the film says Zepbound in every sentence and the captions spell it). B: <b>GLP-1 TIPS</b> (the two versions are side by side at the top of short D). With B, short F's headline becomes \"How Much Protein You Need On A GLP-1\".",
 "<b>Title copy</b> for all six (in the reply box). Title case, two lines each.",
 "<b>Steps in shorts C and E.</b> A (recommended): one step at a time in the key-point bar, with a counter (STEP 1 OF 5), each landing on your words. B: the film's whole list as a card at the bottom. I planned B, then built it: with the title band on top the card pushes the captions onto your face (the still is in short C). Your call.",
 "<b>AI clip for short C's opening.</b> Approve the two frames for motion, ask for changes, or use the syringe close-up.",
 "<b>AI gag for short E's last line.</b> Approve the two frames for motion, ask for changes, or use the staircase clip.",
 "<b>Key-point copy.</b> Every bar is listed in the reply box. Edit any line; two lines each, about 24 letters a line.",
]
DECIDED = [
 "<b>Pickup takes: the rule is your last clean take of each line.</b> The 10-12 takes all carry recorder dropouts, so they are placeholders until the re-read (decision 1). Take 3 of the Thursday line also hit the mic's limit: stay about a hand's width from the mic and keep the same distance for all five lines.",
 "<b>B uses the wording you settled on while recording:</b> \"Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead.\" It runs 4.3 s. Say it that way again on the re-read, or go back to the short version.",
 "<b>You recorded A's pickup, so A opens on it</b> (\"Here's why you should start Zepbound at 1 milligram to avoid the side effects.\") over the vials clip, then you on camera at \"And for most of you watching this channel...\"",
 "<b>D opens on your pickup over the calendar clip</b> (turned the right way up so the dates read), then cuts to you on \"The medication is strongest in the first few days after your shot\", so your face is on screen by 0:04. The weekly chart comes in on \"and it fades\".",
 "<b>\"Again,\" is not in D's captions.</b> The film's subtitle has \"Again, Monday through Thursday\". Two speech models, four listens: you say \"Monday through Thursday, I am dialed in.\" Captions print what you say.",
 "<b>D's couch clip was replaced.</b> The film used a man on the floor looking at his phone for \"eat out of boredom\". Your 10-11 rule says a person looking at a phone is not a picture, so the short shows a hand grabbing chips (library B0490).",
 "<b>No pen-injection stock in B.</b> Every pen clip we have frames a bare stomach, so you stay on camera for \"the problem with the pen\".",
 "<b>A keeps its leading \"And\".</b> It is 0.08 s long and joined to \"for\"; it cannot be cut without clipping the word.",
 "<b>The dark syringe close-up (B0352) is out of A.</b> It reads far darker than you beside it, so you stay on camera for \"1 milligram. That is less than half...\"",
 "<b>F's AI split screen is stacked</b>, strong man on top and weak man under him, so both fill the width (side by side would be a thin strip).",
 "<b>F's ab-wheel clip is a square, not full screen.</b> Reason: the rollout runs the whole width of the frame.",
 "<b>F's weight-training clip is your own footage</b> (dumbbell curls by the pool, B0458) in place of the film's dark gym stock.",
 "<b>F opens on the sliced chicken, and the later chicken shot is a different clip</b> (no clip repeats inside a short).",
 "<b>C ends on \"you pushed the plunger too fast.\"</b> The last word is whole: there is a tenth of a second of silence before the film's own cut.",
 "<b>Every cut between two pieces of you on camera changes the picture size</b> or goes through a clip, so no cut reads as a jump.",
 "<b>Cut from the 4K camera file</b> through the film's own edit and colour, so the vertical picture is sharper than a crop of the finished film.",
 "<b>Captions were checked against a transcript of each short's cut audio.</b> No first or last word is clipped on any of the six.",
 "<b>Spend so far: $0.</b> The four AI frames were made on the ChatGPT subscription. Motion for both clips would be about $3 to $5 in total, inside the $5 per video limit.",
 "<b>Posting order to suggest at setup:</b> D, A, F, C, B, E, with A and B at least a week apart. Nothing posts before the long-form is public on Oct 25.",
]
SHORT = dict(
 D="Finished above. One continuous passage plus your pickup. 50 s.",
 A="Dose only, as you asked: the pen talk moved to B and the 1.5 mg maintenance lines were added. Opens on your pickup over the vials clip. 46 s.",
 B="Pen versus needle only. Opens on your pickup over the vial and syringe clip. Five pieces of the film, each join covered by a size change or a clip. 54 s with the pickup.",
 C="One continuous passage after your pickup. Five step bars and one key point. 54 s with the pickup. The opener still below is the fallback; the AI frames are above.",
 E="Opens on your pickup over the scale clip, then you on \"Coming off is where I see people destroy everything they built.\" 57 s with the pickup, so nothing more can be added.",
 F="Good as is, per your note. Opens on the sliced chicken for 2.5 s under your first line. 55 s.")
ITEM = {
 "D.calendar": "The film's calendar clip, turned upright, under your pickup.", "D.week": "The film's seven-day chart, redrawn for the tall frame. Same copy.",
 "D.chips": "Replaces the film's man-on-his-phone clip.", "A.ramp": "The film's 1 mg, 2 mg, 2.5 mg ramp, redrawn for the tall frame. Each step lands on its number.",
 "A.nausea": "Our AI clip from the film (A0137). This short gets the AI flag at setup.", "F.split": "Our AI clip from the film (A0058), stacked. This short gets the AI flag at setup.",
 "F.abwheel": "Square, not full screen: the rollout runs the whole width.", "F.curls": "Your own footage, in place of the film's gym stock.",
 "F.app": "The phone-beside-you layout you approved on the salad shorts.", "C.plunger": "FALLBACK opener, only if you turn down the AI frames above. Lifted because it is dark.",
 "E.stairs": "FALLBACK ending, only if you turn down the AI gag above.", "B.vialhand": "The film's 2:02 clip, under your pickup.",
 "B.draw": "A different clip from the film's here, because the film's is B's opening.",
}
TAG = {"C.plunger": "fallback", "E.stairs": "fallback"}
EXTRA = {
 "D": [("D_title_glp1", "D: Title band, option B", "The same frame with <b>GLP-1 TIPS</b> in the band (decision 2). Everything else identical.", "option B")],
 "C": [("C_optB_listcard", "C: Steps, option B (the film's list card)", "The whole list as a bottom card (decision 4). With the title band on top there is no room: the captions land on your mouth and chin, and the card reaches your chest. Shown with four of the five steps up.", "option B")],
}
def _bars():
    import plans as P
    out = []
    for S in ORDER:
        for b in P.BARS.get(S, []): out.append(f"   {S} {b['id']}: {b['topic']}: " + " / ".join(p[0] for p in b["parts"]))
    return "\n".join(out)
def _titles():
    import plans as P
    return "\n".join(f"   Short {S}: {P.TITLE[S][0]} / {' / '.join(P.TITLE[S][1])}" for S in ORDER)
REPLY = f"""1. Pickups: I will re-read the five lines (say "go" in the task)
2. Title band: A ZEPBOUND TIPS / B GLP-1 TIPS
3. Title copy: approved / edits:
{_titles()}
4. Steps in C and E: A one step at a time in the bar / B the list card
5. AI clip, short C opening: approve frames for motion / changes: / use the syringe close-up
6. AI gag, short E last line: approve frames for motion / changes: / use the staircase clip
7. Key-point copy: approved / edits:
{_bars()}
Short D notes:
Other notes (anything in "What I decided", any clip or crop):"""
