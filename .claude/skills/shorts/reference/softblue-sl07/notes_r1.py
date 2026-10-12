"""SL-07 round 1 page copy (plain language for Dan; no em dashes)."""
import json, os
ORDER = "BADEF"
PK = "/Volumes/Extreme/_edit_work/sl07/pickups"
rep = json.load(open(PK + "/B.report.json")) if os.path.exists(PK + "/B.report.json") else None
HAVE_PICKUP = rep is not None and not os.path.exists(PK + "/B.PLACEHOLDER")
INTRO = ("Five shorts from the approved long-form \"If I Had Belly Fat, Here's How I'd Lose It In 90 Days\" (your picks A, B, D, E, F). "
         "This round: short B finished, start and end frames for 12 AI clip ideas (stills only, no motion made), and every title, crop, "
         "clip, graphic and key point of all five as stills on real frames. The other four are planned to the frame but not rendered. "
         "No covers, no upload.")
LOCKED = ("the Soft Blue shorts look you approved on the salad shorts (title band on top for the whole short, two steady picture sizes, "
          "two-line key-point bar, captions under it, clips filling the picture); the film's colour (same camera roll, same grade) and its "
          "approved sound, cut only; your five segment picks from 10-12; AI-GENERATED chips on AI clips.")
FIRST_H = "Short B, finished: Weigh Yourself Every Morning"
FIRST_REVIEW = "review/If I Had Belly Fat SFC R1 - short B - Weigh Yourself Every Morning - REVIEW 540p.mp4"
if HAVE_PICKUP:
    _pk = (f"<p><b>How your pickup was treated:</b> recorded on the desk Yeti, tone matched to your voice in the film (average difference "
           f"{rep['tone_err_mean']:.1f} dB across ten bands, largest {rep['tone_err_max']:.1f} dB), level matched to the film line that follows it "
           f"({rep['gain_db']:+.1f} dB), a 15 ms fade at the join. Nothing else was done to it: no echo removal, no noise removal. The film has no "
           f"music, so nothing runs under it. The room measures {rep['edt_ms_pickup']:.0f} ms on the desk mic against {rep['edt_ms_film']:.0f} ms "
           f"on the studio lav, so listen for whether the first line sounds like a different room from the second.</p>")
    _open = "the first 5 seconds (your new opening line over the scale clip, then the cut to you on \"Weigh yourself every morning\")"
else:
    _pk = ("<p><b>Your opening line is not in this copy yet.</b> The mic did not catch you reading it during this session, so this copy "
           "starts on \"Weigh yourself every morning\" with the scale clip held for its first seconds. Everything after that is as it will ship. "
           "The line goes in the moment you record it (see the first decision).</p>")
    _open = "the opening (the scale clip, then the cut to you)"
_o = 3 if HAVE_PICKUP else 0
FIRST_TEXT = (f"<p><b>What to check:</b> {_open}, the study card at 0:{14 + _o}, the weight chart at 0:{21 + _o} (the dots arrive as you say the weight "
              f"bounces, the blue line draws on \"7 day moving average\"), the two weekly-check key points from 0:{34 + _o}, and the last line.</p>"
              + _pk +
              "<p>Full quality copy for VLC: <b>Videos to Review / If I Had Belly Fat SFC R1 - short B - Weigh Yourself Every Morning.mp4</b></p>"
              "<p>Sound check clip (the film's own cut of this passage, then the short): <a href=\"review/AB_film-vs-short_B.mp4\">AB_film-vs-short_B.mp4</a></p>")
AI_INTRO = ("Twelve ideas, more than feel safe, so turn down the ones you do not like (you said about a third). Every short works without its "
            "AI clips: the plain version is what the stills below show. Frames were made on the ChatGPT subscription ($0). Motion is about "
            "$1 to $2 a clip and is only made for the ones you approve. Your limit is $5 a short, so if you approve all three in short A "
            "I will make the opener and one more unless you say to go to about $6 there.")
AI = [
 ("A1", "<b>A1. Short A opener (0:00 to 0:05), under \"make small, sustainable changes and lose 1 pound a week.\"</b> A snail crawls across a bathroom scale and the needle barely twitches. If no: A opens on you, close."),
 ("A2", "<b>A2. Short A, \"That is going to take you seven months.\"</b> A man plods on a treadmill while the calendar pages fly off and his stubble grows. Note: he reads as walking slowly, not jogging. If no: you on camera with the key point."),
 ("A3", "<b>A3. Short A, \"Most people are trying to squeeze fat loss into their life.\"</b> A man tries to cram a kettlebell into an overstuffed briefcase. Note: the bottom of the briefcase sits under the captions; the kettlebell and the flying papers are clear. If no: you on camera."),
 ("B1", "<b>B1. Short B, \"your weight is going to bounce around 2 or 3 pounds.\"</b> The scale needle swings like a metronome while he stares, deadpan. Note: the dial is small in the frame, so this is the weakest of the twelve. If no: the weight chart starts there, as in the finished short above."),
 ("B2", "<b>B2. Short B last line, \"hope the scale is going to move.\"</b> He kneels and prays to his scale; candles appear. If no: the short ends on you, as in the finished short above."),
 ("D1", "<b>D1. Short D, \"is today a gym day or not?\"</b> He flips a coin in bed and it lands on its edge. Note: the coin is small. If no: you on camera."),
 ("D2", "<b>D2. Short D, \"something comes up at work and they miss a day.\"</b> A phone buzzes itself off a gym bench in an empty gym. Note: a quiet picture. If no: the tired man in the gym (film's stock clip) covers the whole line."),
 ("E1", "<b>E1. Short E opener, \"Maintaining your weight is far, far easier than losing weight.\"</b> He pulls a dusty, cobwebbed scale out from under the bed and blows the dust off. The strongest gag of the set. If no: E opens on you, close."),
 ("E2", "<b>E2. Short E, \"gain 5 pounds, gain 10 pounds, gain 20 pounds before you even realize it.\"</b> A shirt button pops off and knocks his coffee over. Framed chest up, no stomach in shot. If no: you on camera with the key point."),
 ("E3", "<b>E3. Short E, \"you can have a drink on the weekend.\"</b> Played straight: a lean man raises one beer on a patio. If no: the film's stock clip of friends clinking beers (shown in short E below)."),
 ("F1", "<b>F1. Short F opener, \"If you never look at your bank account, you're probably going to be poor.\"</b> A moth flies out of an empty wallet. If no: F opens on you, close."),
 ("F2", "<b>F2. Short F, \"weigh your food on a scale and look up every ingredient.\"</b> A man buried in measuring cups, a food scale and a thick binder gives up and drops his forehead on the binder. If no: the film's food-scale clip (shown in short F below)."),
]
_d1 = ("<b>Your pickup's sound (short B).</b> Play the first 6 seconds. A: it sits fine, use the desk mic for both pickups (recommended if you cannot hear the join). B: re-record them on the lav at the next shoot."
       if HAVE_PICKUP else
       "<b>Record the two pickup lines.</b> They are not recorded yet. B: \"Here's how to know if your fat loss plan is working.\" D: \"Here's why you should work out every single morning.\" Say \"record now\" in the chat and read each three times, or drop a Voice Memo in the chat.")
DECISIONS = [
 _d1,
 "<b>The 12 AI clip ideas.</b> For each: yes, yes with a change, or no. My picks if you want a default: yes to A1, A2, B2, E1, E2, F1, F2; no to B1, D1 and D2 (small or quiet pictures); A3 and E3 are your taste.",
 "<b>Title copy</b> for all five (in the reply box). Title case, two lines each. The small line above each is LOSE YOUR BELLY FAT.",
 "<b>Key-point copy.</b> Every bar is listed in the reply box. Edit any line; two lines each, about 26 letters a line.",
]
DECIDED = [
 "<b>B opens on your pickup over the film's own scale clip</b>, then cuts to you on \"Weigh yourself every morning\"" + ("" if HAVE_PICKUP else " (in this copy, with no pickup yet, the clip sits under those first words instead)") + ". That clip is a square, not full screen: the scale is the subject and it is 1,000 px wide, and a full-screen crop put the caption on it. The scale shot later in B (\"let's say it stalled out\") is a different clip.",
 "<b>All five endings are whole.</b> The handoff warned that A (\"...fit around that.\") and F (\"...losing fat.\") end on one of the film's audio cuts. I measured each last word against the raw lav: every one finishes before the film cuts away, so no ending was moved.",
 "<b>E is one continuous passage.</b> The plan cut the 0.6 s pause before \"So how does somebody end up 30 pounds overweight\". It is a natural pause, so I left it and changed the picture size there instead. E runs 43 s.",
 "<b>The film's graphics are rebuilt for the tall frame, not cropped:</b> the study card and the 7-day average chart in B fill the picture area; the weekly check list in B became two key-point bars (one per rule) so nothing sits on your face; the 7-months point (A) and the 3-pound rule (E) are key-point bars.",
 "<b>Capital letters:</b> full caps on three key points only (7 MONTHS, NOTHING, DAILY) and on \"13 lb MORE\" in the study card. Everything else is title case.",
 "<b>D opens on your fast jump rope, not the ab wheel</b> (the handoff said ab wheel). The jump rope fills the whole screen with you facing the camera, which is a stronger first frame; the ab wheel has to sit in a card. The ab wheel stays where the film had it (\"You just get up and you do it, even on weekends, even on vacation\"), and D ends on the medicine-ball toe touch. Three exercises, no clip twice.",
 "<b>D's ab wheel and toe touch are cards, not full screen.</b> Reason: you travel about 1,400 px sideways in both (the rollout, and lying flat on the mat), so a full-screen crop cuts off your hands or feet. Each card is as tall as that allows and nothing is cropped off the height.",
 "<b>E shows your real abs on \"once you have your abs\"</b>: your vertical pool clip (B0435), not stock.",
 "<b>Two stock clips were brightened</b> to sit with you beside them: the tired man in the gym and the morning kitchen (both in D).",
 "<b>F has two phone demos beside you, two different recordings:</b> taking the meal photo and getting the numbers (B0035) on \"you just take a picture of your food\", then the day's log (the film's own, B0038) on \"it adds up your day for you\".",
 "<b>A keeps the film's two clips</b> on \"they work all day, they drive home, then they take care of their family\": the traffic stock and the AI busy dad (chip on). So A gets the AI flag at upload either way.",
 "<b>Every cut between two pieces of you on camera changes the picture size</b> or goes through a clip, so no cut reads as a jump. Long takes are stepped between the two sizes in a pause.",
 "<b>Cut from the 4K camera file</b> through the film's own edit and colour, so the vertical picture is sharper than a crop of the finished film.",
 "<b>Captions were checked against a transcript of each short's cut audio.</b> No first or last word is clipped on any of the five. Captions print \"abs\" in lower case, \"AI\" in capitals, and keep your swearing.",
 "<b>The recording tool was dropping audio.</b> The command the handoff gave lost 11 percent of the Yeti's sound (a tiny skip every tenth of a second) and nothing reported it. I built a replacement, tested it clean, wrote it into the rules, and told the Zepbound shorts session, which was recording you with the faulty command at the same time.",
 "<b>Spend so far: $0.</b> The 24 AI frames were made on the ChatGPT subscription.",
 "<b>Posting order to suggest at setup:</b> F, B, A, D, E, with B and E (both about weighing) at least a week apart. Nothing posts before the long-form is public on Nov 1.",
]
SHORT = dict(
 A="52 s, opens on the film line \"Most fitness channels tell you to make small, sustainable changes...\" Two pieces of the film; the cut between them changes the picture size. AI ideas A1, A2 and A3 would go in this one.",
 B="49 s plus your pickup (about 3 s). One continuous passage. The finished copy is at the top of the page." + ("" if HAVE_PICKUP else " These stills are from that copy, so the scale clip sits under the first film words; with your pickup it sits under the pickup."),
 D="57 s with the pickup \"Here's why you should work out every single morning.\" over your jump rope. One continuous passage. AI ideas D1 and D2 would go in this one.",
 E="43 s, opens on the film line \"Maintaining your weight is far, far easier than losing weight.\" You picked it knowing it is under 45 s; it is not padded. AI ideas E1, E2 and E3 would go in this one.",
 F="48 s, opens on the film line \"If you never look at your bank account, you're probably going to be poor.\" AI ideas F1 and F2 would go in this one.",
)
ITEM = {
 "A.crop-mid": "The opening of A if you turn down the snail (A1).",
 "A.dad": "The film's AI clip (A0063), AI-GENERATED chip top left.",
 "B.scale": "Under your pickup line. The film used this clip at the same place. Square so the whole scale shows.",
 "B.study": "Rebuilt from the film's card. The first bar grows on \"weighed themselves every day\", the second on \"the people who didn't\".",
 "B.chart": "Rebuilt from the film's chart, same data. AI idea B1 would replace its first 5 seconds.",
 "D.jumprope": "Under your pickup line: the fast skip (the correct jump rope clip), full screen.",
 "D.abwheel": "A card, because the rollout runs about 1,400 px sideways.",
 "D.toetouch": "The last picture of D. A card, because lying flat you are about 1,400 px long.",
 "D.sore": "Brightened. AI idea D2 would replace its middle (\"something comes up at work\").",
 "D.morning": "Brightened a little.",
 "E.abs": "Your real pool clip, native vertical.",
 "E.cheers": "The film's stock clip. AI idea E3 would replace it.",
 "F.foodscale": "The film's clip. AI idea F2 would replace it.",
 "F.photo": "The phone beside you: camera on the plate, Analyze Meal, the calorie and macro breakdown.",
 "F.log": "The film's phone demo: the itemised meal, then today's total.",
}
TAG = {"A.dad": "AI", "B.study": "rebuilt", "B.chart": "rebuilt"}
EXTRA = {}
_T = {"A": "Stop Trying To Lose / 1 Pound A Week", "B": "Weigh Yourself / Every Morning", "D": "Work Out Every Morning, / Not 3 Times A Week",
      "E": "The 3-Pound Rule That / Keeps Belly Fat Off", "F": "Track Your Calories / With A Photo"}
def _bars():
    import plans as P
    out = []
    for S in ORDER:
        for b in P.BARS[S]: out.append(f"  {S} {b['id']}  {b['topic']}: {b['parts'][0][0]} / {b['parts'][1][0]}")
    return "\n".join(out)
REPLY = ("1. " + ("Pickup sound: A (desk mic is fine) / B (re-record on the lav)" if HAVE_PICKUP else "Pickups: I will record them now / Voice Memo") + "\n"
         "2. AI clips (yes / change / no):\n"
         + "".join(f"   {k}: \n" for k, _ in AI) +
         "3. Titles (edit any):\n" + "".join(f"   {S}: {_T[S]}\n" for S in ORDER) +
         "4. Key points (edit any):\n" + _bars() + "\n"
         "5. Anything else:\n")
