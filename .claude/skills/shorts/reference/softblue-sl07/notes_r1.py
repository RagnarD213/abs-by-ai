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
FIRST_H = "Finished short: Weigh Yourself Every Morning"
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
NAMES = {"A": "Stop Trying To Lose 1 Pound A Week", "B": "Weigh Yourself Every Morning", "D": "Work Out Every Morning, Not 3 Times A Week",
         "E": "The 3-Pound Rule That Keeps Belly Fat Off", "F": "Track Your Calories With A Photo"}
ABOUT = {"A": "52 seconds. You say the \"lose 1 pound a week\" advice is why people stay fat, and that it is easier to go all-in for 90 days and make fat loss the number one priority.",
         "B": "About 52 seconds with your pickup. Weigh in every morning, ignore the daily bounce, judge the plan on the 7-day average, and cut 200 calories if it stalls for a week.",
         "D": "About 57 seconds with your pickup. Short workouts every morning beat long ones two or three times a week, because nobody needs you at 8 in the morning.",
         "E": "43 seconds. Staying lean is easier than getting lean, as long as you keep weighing in and cut back the moment you are 3 pounds over.",
         "F": "48 seconds. Tracking calories used to be too much work; now you take a picture of your food. Ends on the free tracker at AbsByAI.com."}
AI_INTRO = ("Twelve ideas, more than feel safe, so turn down the ones you do not like (you said about a third). They are grouped by the short "
            "they would go in, in the order they would appear. Under each pair: when it appears, what you say just before it, the line it plays "
            "under, and what comes right after. Every short works without its AI clips: \"If you say no\" is what plays there instead, and it is "
            "what the stills further down show. Frames were made on the ChatGPT subscription ($0). Motion is about $1 to $2 a clip and is only "
            "made for the ones you approve. Your limit is $5 a short, so if you approve all three in \"Stop Trying To Lose 1 Pound A Week\" I "
            "will make the opener and one more unless you say to go to about $6 there.")
# id, short, name of the idea, when, before, under, after, what you see, if no, note
AI_ITEMS = [
 ("A1", "A", "Snail on the scale", "The very first picture, 0:00 to 0:05.", "Nothing. This opens the short.",
  "Most fitness channels tell you to make small, sustainable changes and to lose 1 pound a week.",
  "Cut to you on camera: \"In my opinion, that advice is bullshit, and that is the reason why most of the people following it are still fat.\"",
  "A snail crawls across a bathroom scale and the needle barely twitches.", "The short opens on you, close up, saying the line.", ""),
 ("A2", "A", "Seven months on the treadmill", "About 0:16 to 0:20.", "You on camera: \"Let's say you have 30 pounds to lose and you are losing 1 pound a week.\"",
  "That is going to take you seven months,",
  "Back to you: \"and in my opinion, almost nobody can stay motivated for that long. It's far, far easier to go all-in for 90 days and get it over with.\"",
  "A man plods on a treadmill while the calendar pages tear off and fly past and his stubble grows. The key point \"30 lb At 1 lb A Week Takes 7 MONTHS\" sits over it.",
  "You stay on camera with the same key point.", "He reads as walking slowly, not jogging."),
 ("A3", "A", "Kettlebell in the briefcase", "About 0:27 to 0:30, the start of the second half.", "You on camera, end of the first half: \"...go all-in for 90 days and get it over with.\"",
  "Most people are trying to squeeze fat loss into their life.",
  "The film's own clips: traffic on \"They work all day, they drive home\", then the AI busy dad in the kitchen on \"then they take care of their family\".",
  "A man in a shirt and tie tries to cram a kettlebell into an overstuffed briefcase; papers squirt out.", "You stay on camera for that line.",
  "The bottom of the briefcase sits under the captions; the kettlebell and the flying papers are clear."),
 ("B1", "B", "The metronome needle", "About 0:24 to 0:29 (with your pickup in).", "The study card: \"...lost about 13 pounds more over six months than the people who didn't.\"",
  "Now, your weight is going to bounce around 2 or 3 pounds from day to day, just from water and salt.",
  "The weight chart: \"So don't freak out about any one day. What you want to look at is your 7 day moving average...\"",
  "A man stands on a scale, deadpan, while the needle swings left and right like a metronome.", "The weight chart starts on that line, as in the finished short at the top of this page.",
  "The dial is small in the frame. The weakest of the twelve."),
 ("B2", "B", "Praying to the scale", "The last 4 seconds of the short.", "You on camera: \"Most guys never adjust anything.\"",
  "They just keep doing the same thing for months and hope the scale is going to move.",
  "Nothing. The short ends on it.",
  "A man kneels on the bathroom floor and prays to his scale; candles appear beside it.", "The short ends on you saying the line, as in the finished short at the top of this page.", ""),
 ("D2", "D", "Phone buzzes off the bench", "About 0:10 to 0:12.", "\"They go to the gym two or three times a week for an hour and a half. They get really sore,\" (the tired man in the gym comes in on \"really sore\").",
  "then something comes up at work and they miss a day,",
  "\"and within a month they're not going at all.\" Then you on camera with the key point \"Short DAILY Workouts Beat Long Occasional Ones\".",
  "An empty gym. A phone face down on a weight bench buzzes its way to the edge and drops off.", "The tired man in the gym (the film's stock clip) covers the whole sentence.",
  "A quiet picture next to the others."),
 ("D1", "D", "The coin lands on its edge", "About 0:23 to 0:25.", "You on camera: \"...when you're working out every day, you don't have to think about it. You're not waking up and asking yourself,\"",
  "is today a gym day or not?",
  "Your ab wheel clip: \"You just get up and you do it, even on weekends, even on vacation.\"",
  "A man in bed flips a coin to decide and it lands balanced on its edge.", "You stay on camera for that line.", "The coin is small in the frame."),
 ("E1", "E", "The dusty scale", "The very first picture, 0:00 to 0:04.", "Nothing. This opens the short.",
  "Maintaining your weight is far, far easier than losing weight.",
  "Your real pool clip: \"And once you have your abs, you can eat more,\"",
  "A man pulls an old scale thick with dust and cobwebs out from under the bed and blows the dust off.", "The short opens on you, close up, saying the line.",
  "The strongest gag of the set."),
 ("E3", "E", "One beer on the patio", "About 0:06 to 0:10.", "Your real pool clip: \"And once you have your abs, you can eat more,\"",
  "you can have a drink on the weekend, and you can relax a little bit.",
  "You on camera: \"You can't do that when you're trying to lose two and a half pounds a week.\"",
  "Played straight, not a gag: a lean man at a sunny patio table raises one beer.", "The film's stock clip of friends clinking beer mugs in a bar (shown in this short's stills below).", ""),
 ("E2", "E", "The button pops", "About 0:20 to 0:25.", "You on camera: \"So how does somebody end up 30 pounds overweight in the first place? It's because they're not weighing themselves. If you're not weighing yourself,\"",
  "you're going to gain 5 pounds, gain 10 pounds, gain 20 pounds before you even realize it.",
  "The scale clip: \"So here's what I would do. I would keep weighing myself every day.\"",
  "A man at breakfast in a too-tight shirt; a button shoots off and knocks his coffee over. Framed chest up, no stomach in shot.",
  "You stay on camera with the key point \"Stop Weighing Yourself And 5 lb Quietly Becomes 20\".", ""),
 ("F1", "F", "Moth in the wallet", "The very first picture, 0:00 to 0:04.", "Nothing. This opens the short.",
  "If you never look at your bank account, you're probably going to be poor.",
  "Cut to you on camera: \"Same thing applies to your calories.\"",
  "A man opens a worn wallet. It is empty, and a moth flies out.", "The short opens on you, close up, saying the line.", ""),
 ("F2", "F", "Buried in measuring cups", "About 0:09 to 0:13.", "You on camera: \"Now, before AI, I was always against tracking calories.\"",
  "The old way where you weigh your food on a scale and look up every ingredient,",
  "You on camera: \"that was way too much work for normal people like me and you. But with AI, everything has changed.\" Then the phone demo.",
  "A man at a kitchen counter buried in a food scale, measuring cups and a thick binder gives up and drops his forehead on the binder.",
  "The film's clip of fruit going into a bowl on a kitchen scale (shown in this short's stills below).", ""),
]
AI = [(i[0], "") for i in AI_ITEMS]
_d1 = ("<b>Your pickup's sound (short B).</b> Play the first 6 seconds. A: it sits fine, use the desk mic for both pickups (recommended if you cannot hear the join). B: re-record them on the lav at the next shoot."
       if HAVE_PICKUP else
       "<b>Record the two pickup lines.</b> They are not recorded yet. B: \"Here's how to know if your fat loss plan is working.\" D: \"Here's why you should work out every single morning.\" Say \"record now\" in the chat and read each three times, or drop a Voice Memo in the chat.")
DECISIONS = [
 _d1,
 "<b>The 12 AI clip ideas.</b> For each: yes, yes with a change, or no. My picks if you want a default: <b>yes</b> to the snail on the scale (A1), seven months on the treadmill (A2), praying to the scale (B2), the dusty scale (E1), the button pops (E2), the moth in the wallet (F1) and buried in measuring cups (F2); <b>no</b> to the metronome needle (B1), the coin on its edge (D1) and the phone off the bench (D2), which are small or quiet pictures; the kettlebell in the briefcase (A3) and the beer on the patio (E3) are your taste.",
 "<b>Title copy</b> for all five (in the reply box). Title case, two lines each. The small line above each is LOSE YOUR BELLY FAT.",
 "<b>Key-point copy.</b> Every bar is listed in the reply box. Edit any line; two lines each, about 26 letters a line.",
]
DECIDED = [
 "<b>\"Weigh Yourself Every Morning\" opens on your pickup over the film's own scale clip</b>, then cuts to you on \"Weigh yourself every morning\"" + ("" if HAVE_PICKUP else " (in this copy, with no pickup yet, the clip sits under those first words instead)") + ". That clip is a square, not full screen: the scale is the subject and it is 1,000 px wide, and a full-screen crop put the caption on it. The scale shot later in that short (\"let's say it stalled out\") is a different clip.",
 "<b>All five endings are whole.</b> The handoff warned that \"Stop Trying To Lose 1 Pound A Week\" (\"...fit around that.\") and \"Track Your Calories With A Photo\" (\"...losing fat.\") end on one of the film's audio cuts. I measured each last word against the raw lav: every one finishes before the film cuts away, so no ending was moved.",
 "<b>\"The 3-Pound Rule That Keeps Belly Fat Off\" is one continuous passage.</b> The plan cut the 0.6 s pause before \"So how does somebody end up 30 pounds overweight\". It is a natural pause, so I left it and changed the picture size there instead. It runs 43 s.",
 "<b>The film's graphics are rebuilt for the tall frame, not cropped:</b> the study card and the 7-day average chart in \"Weigh Yourself Every Morning\" fill the picture area; its weekly check list became two key-point bars (one per rule) so nothing sits on your face; the 7-months point (in \"Stop Trying To Lose 1 Pound A Week\") and the 3-pound rule are key-point bars.",
 "<b>Capital letters:</b> full caps on three key points only (7 MONTHS, NOTHING, DAILY) and on \"13 lb MORE\" in the study card. Everything else is title case.",
 "<b>\"Work Out Every Morning, Not 3 Times A Week\" opens on your fast jump rope, not the ab wheel</b> (the handoff said ab wheel). The jump rope fills the whole screen with you facing the camera, which is a stronger first frame; the ab wheel has to sit in a card. The ab wheel stays where the film had it (\"You just get up and you do it, even on weekends, even on vacation\"), and the short ends on the medicine-ball toe touch. Three exercises, no clip twice.",
 "<b>The ab wheel and the toe touch in that short are cards, not full screen.</b> Reason: you travel about 1,400 px sideways in both (the rollout, and lying flat on the mat), so a full-screen crop cuts off your hands or feet. Each card is as tall as that allows and nothing is cropped off the height.",
 "<b>\"The 3-Pound Rule That Keeps Belly Fat Off\" shows your real abs on \"once you have your abs\"</b>: your vertical pool clip (B0435), not stock.",
 "<b>Two stock clips were brightened</b> to sit with you beside them: the tired man in the gym and the morning kitchen (both in \"Work Out Every Morning, Not 3 Times A Week\").",
 "<b>\"Track Your Calories With A Photo\" has two phone demos beside you, two different recordings:</b> taking the meal photo and getting the numbers (B0035) on \"you just take a picture of your food\", then the day's log (the film's own, B0038) on \"it adds up your day for you\".",
 "<b>\"Stop Trying To Lose 1 Pound A Week\" keeps the film's two clips</b> on \"they work all day, they drive home, then they take care of their family\": the traffic stock and the AI busy dad (chip on). So that short gets the AI flag at upload either way.",
 "<b>Every cut between two pieces of you on camera changes the picture size</b> or goes through a clip, so no cut reads as a jump. Long takes are stepped between the two sizes in a pause.",
 "<b>Cut from the 4K camera file</b> through the film's own edit and colour, so the vertical picture is sharper than a crop of the finished film.",
 "<b>Captions were checked against a transcript of each short's cut audio.</b> No first or last word is clipped on any of the five. Captions print \"abs\" in lower case, \"AI\" in capitals, and keep your swearing.",
 "<b>The recording tool was dropping audio.</b> The command the handoff gave lost 11 percent of the Yeti's sound (a tiny skip every tenth of a second) and nothing reported it. I built a replacement, tested it clean, wrote it into the rules, and told the Zepbound shorts session, which was recording you with the faulty command at the same time.",
 "<b>Spend so far: $0.</b> The 24 AI frames were made on the ChatGPT subscription.",
 "<b>Posting order to suggest at setup:</b> Track Your Calories With A Photo; Weigh Yourself Every Morning; Stop Trying To Lose 1 Pound A Week; Work Out Every Morning, Not 3 Times A Week; The 3-Pound Rule That Keeps Belly Fat Off. The two about weighing go at least a week apart. Nothing posts before the long-form is public on Nov 1.",
]
SHORT = dict(
 A="52 s, opens on the film line \"Most fitness channels tell you to make small, sustainable changes...\" Two pieces of the film; the cut between them changes the picture size. Three AI ideas would go in this one: the snail on the scale, seven months on the treadmill, the kettlebell in the briefcase.",
 B="49 s plus your pickup (about 3 s). One continuous passage. The finished copy is at the top of the page." + ("" if HAVE_PICKUP else " These stills are from that copy, so the scale clip sits under the first film words; with your pickup it sits under the pickup."),
 D="57 s with the pickup \"Here's why you should work out every single morning.\" over your jump rope. One continuous passage. Two AI ideas would go in this one: the phone off the bench and the coin on its edge.",
 E="43 s, opens on the film line \"Maintaining your weight is far, far easier than losing weight.\" You picked it knowing it is under 45 s; it is not padded. Three AI ideas would go in this one: the dusty scale, one beer on the patio, the button pops.",
 F="48 s, opens on the film line \"If you never look at your bank account, you're probably going to be poor.\" Two AI ideas would go in this one: the moth in the wallet and buried in measuring cups.",
)
ITEM = {
 "A.crop-mid": "How this short opens if you turn down the snail on the scale.",
 "A.dad": "The film's AI clip (A0063), AI-GENERATED chip top left.",
 "B.scale": "Under your pickup line. The film used this clip at the same place. Square so the whole scale shows.",
 "B.study": "Rebuilt from the film's card. The first bar grows on \"weighed themselves every day\", the second on \"the people who didn't\".",
 "B.chart": "Rebuilt from the film's chart, same data. The AI idea \"the metronome needle\" would replace its first 5 seconds.",
 "D.jumprope": "Under your pickup line: the fast skip (the correct jump rope clip), full screen.",
 "D.abwheel": "A card, because the rollout runs about 1,400 px sideways.",
 "D.toetouch": "The last picture of D. A card, because lying flat you are about 1,400 px long.",
 "D.sore": "Brightened. The AI idea \"phone off the bench\" would replace its middle (\"something comes up at work\").",
 "D.morning": "Brightened a little.",
 "E.abs": "Your real pool clip, native vertical.",
 "E.cheers": "The film's stock clip. The AI idea \"one beer on the patio\" would replace it.",
 "F.foodscale": "The film's clip. The AI idea \"buried in measuring cups\" would replace it.",
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
        out.append(f"  In \"{NAMES[S]}\":")
        for b in P.BARS[S]: out.append(f"    {b['topic']}: {b['parts'][0][0]} / {b['parts'][1][0]}")
    return "\n".join(out)
REPLY = ("1. " + ("Pickup sound: A (desk mic is fine) / B (re-record on the lav)" if HAVE_PICKUP else "Pickups: I will record them now / Voice Memo") + "\n"
         "2. AI clips (yes / change / no):\n"
         + "".join(f"   {i[0]} {i[2]} (in \"{NAMES[i[1]]}\"): \n" for i in AI_ITEMS) +
         "3. Titles (edit any):\n" + "".join(f"   {_T[S]}\n" for S in ORDER) +
         "4. Key points (edit any):\n" + _bars() + "\n"
         "5. Anything else:\n")
