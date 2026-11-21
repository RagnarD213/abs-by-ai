"""RO-06 visual plan. Round 6: capitals follow Dan's 2026-10-09 rule (title case by default; FULL CAPS kept on five punch words: G06 NO, G17 LOWER, G21 HEAVY, G26 EVERYTHING, G29 UPGRADE; the approved first minute's G02 untouched).
 Every item is anchored to the words Dan says (phrase -> output time via words_out.json).
HyperFrames templates (from_plan.py): lt (Motivation lower third), scene/fact (photo + glass price card), l3 (3A side list).
clip = full-frame cutaway, hard cuts. Order of preference kept: Dan's own B-roll (B####), existing library AI (A####),
stock, new AI last (none needed; the six product pictures are Codex stills, labelled). No clip source is used twice."""
AS = "/Volumes/Extreme/_edit_work/ro06/assets"
SHOOT = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera"
R3 = "/Volumes/Extreme/_edit_work/ro06/round3"
R4 = "/Volumes/Extreme/_edit_work/ro06/round4/motion"
R5 = "/Volumes/Extreme/_edit_work/ro06/round5"
PLAN = [
 # ---------------- hook
 dict(id="C01", kind="clip", start="This is a setup I personally", end="during that time", tail=0.14, src=["B0436@2.0", "B0448@4.0", "B0439@0.5"],
      note="Dan's own B-roll, three different exercises with this setup: ab wheel rollout, jump rope at full speed (round 3: B0448 from 4.0 s, the fast smooth stretch of roll C1674; B0447 was the beginner demo), kettlebell (lawn)"),
 dict(id="G01", kind="lt", start="So this is great", end="limited time to work out", topic="HOME WORKOUT ON A BUDGET",
      point="A Full Home Setup For $58.", parts=[["A Full Home Setup", "So this is great"], ["For $58.", "for you guys"]]),
 dict(id="C02", kind="clip", start="then you need something like this", end="work out at home", tail=0.2, src=[f"{R3}/c02/C02-pan-topaz.mp4@0.0"], grade="C1559", people="none", physique=False,
      note="the real equipment (C1557 from 3.0 s, locked off), round 3: a 2.25x window that pans from the kettlebell to the dumbbells over the whole clip (c02_pan.py), built from a Topaz 4K upscale of the same 88 frames"),
 # ---------------- round 4: the four AI clips with their motion (Dan approved every frame pair 2026-10-08). Veo 3.1 Fast from the approved
 # START and END frames (gen_motion.py), each trimmed to its slot on its best-flowing part, never slowed or held. Picture only; the voice track does not change.
 dict(id="A1", kind="clip", start="Dan I don't have time", end="go to the gym", tail=0.28, src=[f"{R4}/A1-final.mp4@0.0"], label="AI-GENERATED",
      people="dan", physique=False, note="AI clip (take A1-t1 from 1.50 s): the client whines the first excuse and taps his bare wrist; the trainer rolls his eyes. The client's lips are synced to Dan's own impression (lipsync.py), kept on the client's face only (syncfix.py)"),
 dict(id="A2", kind="clip", start="Dan I don't have the money", end="gym membership", tail=0.12, src=[f"{R4}/A2-final.mp4@0.0"], label="AI-GENERATED",
      people="dan", physique=False, note="AI clip (take A2-t1 from 1.70 s): closer two-shot; the client opens his empty wallet on 'money' and the trainer facepalms. Lips synced to Dan's impression, client's face only"),
 dict(id="A3", kind="clip", start="I'm about to destroy", end="all those excuses", tail=0.1, late=0.312, src=[f"{R4}/A3-t1.mp4@1.341"], label="AI-GENERATED",
      people="dan", physique=False, note="AI clip (take A3-t1 from 1.34 s, made from the ROUND 4 left-hand frame pair): wind-up, the left hand lands on 'destroy' (39.40, clip frame 45), the hand carries on past, his head whips round. "
      "The take holds two slaps; this is the second, harder one, so the clip starts 0.31 s after 'I'm' (late=) and Dan stays on screen for those 9 frames"),
 dict(id="A4", kind="clip", start="show you why", end="any way whatsoever", tail=0.2, src=[f"{R4}/A4-t1.mp4@0.30"], label="AI-GENERATED",
      people="dan", physique=False, note="AI clip (take A4-t1 from 0.30 s): two push-ups on the push-up handles on the blue mat; the trainer kneels with the whistle, then pumps his fist"),
 # ---------------- excuses
 dict(id="G02", kind="lt", start="Super cheap, super easy", end="not doing this", tail=0.25, topic="NO MORE EXCUSES",
      point="No Gym Membership. No COMMUTE.", parts=[["No Gym Membership.", "Super cheap"], ["No COMMUTE.", "super easy"]]),
 dict(id="G03", kind="lt", start="you have an emergency", end="whenever you want", topic="ALREADY HAVE A GYM?",
      point="This Is Your Backup Setup.", parts=[["This Is Your Backup Setup.", "emergency"]]),
 dict(id="G04", kind="lt", start="in the description below", end="recommended items", topic="LINKS IN THE DESCRIPTION",
      point="Every Item I Recommend Is Linked Below.", parts=[["Every Item I Recommend", "in the description"], ["Is Linked Below.", "Amazon Associates"]]),   # round 6: two parts again (the template now spaces them). round 5: one part. The template sets a later part too close to the one before ('RecommendIs'), which only reads wrong mid-sentence; template fault reported separately
 # ---------------- 1 yoga mat
 dict(id="G05", kind="lt", start="yoga mat like this", end="most important thing to buy", tail=0.0, topic="BASIC SETUP: ITEM 1 OF 4",   # round 5: comes up once he is standing again (it sat over his head while he bent to the equipment)
      point="A Basic Yoga Mat.", parts=[["A Basic Yoga Mat.", "yoga mat"]]),
 dict(id="C03", kind="clip", start="a lot of these exercises", end="doing on the floor", tail=0.3, src=["B0461@1.0"], note="Dan's B-roll: push-ups on a mat by the pool"),
 dict(id="C24", kind="clip", start="So don't do your workouts prison style", end="Do it on a yoga mat", tail=0.1, src=["B0455@1.0"], people="dan", physique=False, 
      note="Dan's B-roll: plank up-downs on the blue mat by the pool. round 5 (the delivery gate read 33 % cutaway cover against its 40 % floor): Dan's own unused B-roll, placed on the words that name it"),
 dict(id="F01", kind="scene", scene="fact", people="none", physique=False, start="I'm linking you to my recommended", end="one for $22", tail=2.2, photo=f"{AS}/card_mat.png", label="AI-GENERATED",
      eyebrow=["BASIC YOGA MAT", "I'm linking"], headline=[["$22", "22"]],
      detail=["Thin, basic, cheap.", "cheap basic"], push=1.05, drift=-8),
 dict(id="G06", kind="lt", start="but I still regret", end="cheap basic ones", topic="MY MISTAKE",
      point="The Thick Mat Cost $10 More. NO Difference.", parts=[["The Thick Mat Cost $10 More.", "but I still regret"], ["NO Difference.", "doesn't make any difference"]]),
 dict(id="C04", kind="clip", start="lunges a little bit harder", end="a little bit more", tail=0.2, src=["B0462@1.0"], note="Dan's B-roll: walking lunges on a yoga mat"),
 # ---------------- 2 push-up handles
 dict(id="G07", kind="lt", start="handles like these", end="rotate for about", tail=0.6, topic="BASIC SETUP: ITEM 2 OF 4",   # round 5: comes up once he is standing again (it sat over his head while he bent to the equipment)
      point="Push-Up Handles.", parts=[["Push-Up Handles.", "handles"]]),
 dict(id="F02", kind="scene", scene="fact", people="none", physique=False, start="I would buy these cheap ones", end="right now for $10", tail=2.0, photo=f"{AS}/card_handles.png", label="AI-GENERATED",
      eyebrow=["PUSH-UP HANDLES", "I would buy"], headline=[["$10", "10"]],
      detail=["Not the $40 rotating ones.", "right now"], push=1.05, drift=-8),
 dict(id="C05", kind="clip", start="But this is gonna give you extra range", end="much more effective contraction", tail=0.2, src=["B0452@0.5"],
      note="Dan's B-roll: push-ups on the handles, side on (the extra depth he is describing)"),
 dict(id="G08", kind="lt", start="It's gonna make the push", end="30, 40 reps", topic="WHY HANDLES",
      point="Deeper Range Of Motion. Harder Push-Ups.", parts=[["Deeper Range Of Motion.", "It's gonna make"], ["Harder Push-Ups.", "Especially once"]]),
 # ---------------- 3 jump rope
 dict(id="C23", kind="clip", start="This will make it challenging again", end="even when you're athletic", tail=0.2, src=["B0453@0.5"], people="dan", physique=False, 
      note="Dan's B-roll: push-ups on the handles with his feet up on a chair. round 5 (the delivery gate read 33 % cutaway cover against its 40 % floor): Dan's own unused B-roll, placed on the words that name it"),
 dict(id="G09", kind="lt", start="jump rope", end="essential because", topic="BASIC SETUP: ITEM 3 OF 4",   # round 5: comes up once he is standing again (it sat over his head while he bent to the equipment)
      point="A Jump Rope.", parts=[["A Jump Rope.", "jump rope"]]),
 dict(id="C06", kind="clip", start="excellent cardio", end="few dollars to get it", tail=0.2, src=["/Volumes/Extreme/_edit_work/ro06/round6/c06/C06-fastskip-C1674-101.8.mp4@0.0"], people="dan", physique=False,
      note="round 6 (Dan: 'the clip where I'm quickly skipping over the rope with correct form'): the fast boxer skip, roll C1674 from 101.8 s, cut and graded exactly as library clip B0448 "
           "(the same stretch, about 160 steps a minute). The opening uses roll 99.1 to 101.5 s, so no frame appears twice. B0430 (both feet) was a mistake demo"),
 dict(id="G10", kind="lt", start="I bought all kinds of expensive", end="get the job done", topic="KEY POINT",
      point="Skip The Speed Ropes. Cheap And Basic Works.", parts=[["Skip The Speed Ropes.", "I bought all kinds"], ["Cheap And Basic Works.", "cheap and basic"]]),
 # ---------------- 4 ab wheel
 dict(id="G11", kind="lt", start="favorite infomercial gimmick", end="underestimate the ab wheel", topic="BASIC SETUP: ITEM 4 OF 4",   # round 5: comes up once he is standing again (it sat over his head while he bent to the equipment)
      point="The Ab Wheel.", parts=[["The Ab Wheel.", "the ab wheel"]]),
 dict(id="C07", kind="clip", start="but this is one of the best devices", end="exercise your abs", tail=0.3, src=["B0427@0.5"], note="Dan's B-roll: ab wheel rollout by the pool"),
 dict(id="G12", kind="lt", start="It's very simple and it's continuous", end="you get no breaks", tail=1.9, topic="WHY IT WORKS",   # round 5 tail: the last part had 0.7 s on screen
      point="Continuous Tension. No Breaks.", parts=[["Continuous Tension.", "continuous tension"], ["No Breaks.", "no breaks"]]),
 dict(id="F03", kind="scene", scene="fact", people="none", physique=False, start="The ab wheel costs about", end="on screen right now", tail=0.6, photo=f"{AS}/card_wheel.png", label="AI-GENERATED",
      eyebrow=["BASIC AB WHEEL", "The ab wheel costs"], headline=[["$17", "17"]],
      detail=["No need for a fancy one.", "recommended one"], push=1.05, drift=-8),
 # ---------------- basic total
 dict(id="L01", kind="l3", start="Yoga mat, $22", end="get the job done", heading="Basic Setup: $58",
      points=["Yoga mat: $22", "Push-up handles: $10", "Jump rope: $9", "Ab wheel: $17"], reveal=["Yoga mat", "Push", "Jump rope", "ab wheel"]),
 # C08 (B0460, bodyweight squats) left the film in round 5: its line ("Even if you only have five minutes a day") is inside the length trim
 # ---------------- 5 kettlebell
 dict(id="G13", kind="lt", start="But I know most of you guys", end="good home setup", topic="GOT A LITTLE MORE MONEY?",
      point="The Intermediate Setup: 3 More Items.", parts=[["The Intermediate Setup:", "But I know most"], ["3 More Items.", "couple hundred"]]),
 dict(id="G14", kind="lt", start="kettlebell", end="my kettlebell here", tail=0.35, topic="INTERMEDIATE: ITEM 5",   # round 5: off before the deadlift demo (the strip hid the kettlebell in his hands)
      point="A Kettlebell.", parts=[["A Kettlebell.", "kettlebell"]]),
 dict(id="F04", kind="scene", scene="fact", people="none", physique=False, start="So, this kettlebell, you can pick up", end="about $45", tail=0.4, cover_shot=True, extend=1.4, photo=f"{AS}/card_kettlebell.png", label="AI-GENERATED",
      eyebrow=["35 LB KETTLEBELL", "this kettlebell"], headline=[["$45", "45"]],
      detail=["Right for most beginners.", "most beginners"], push=1.05, drift=-8),
 dict(id="G15", kind="lt", start="that you can do about", end="using the kettlebell for", topic="WHICH WEIGHT?",
      point="30 Seconds Of Deadlifts Should Exhaust You.", parts=[["30 Seconds Of Deadlifts", "30 seconds of kettlebell"], ["Should Exhaust You.", "exhausts"]]),   # round 6: two parts again
 dict(id="G16", kind="lt", start="it uses your entire body", end="just like the regular deadlift", topic="KETTLEBELL DEADLIFT",
      point="Back, Legs, Arms, Abs: Your Whole Body.", parts=[["Back, Legs, Arms, Abs:", "your back"], ["Your Whole Body.", "everything will be"]]),
 dict(id="G17", kind="lt", start="But I do these kettlebell deadlifts", end="do things wrong", topic="KEY POINT",
      point="Kettlebell Deadlifts: Much LOWER Risk.", parts=[["Kettlebell Deadlifts:", "But I do these"], ["Much LOWER Risk.", "lower risk"]]),
 dict(id="G18", kind="lt", start="barbells from home", end="heavier kettlebell", topic="THE PRICE GAP",
      point="Barbell Set: $500 To $1,000. Kettlebell: $45.", parts=[["Barbell Set: $500 To $1,000.", "five hundred"], ["Kettlebell: $45.", "but this will just"]]),
 dict(id="C10", kind="clip", start="you can progress to this kettlebell swings", end="for that weight", tail=0.2, src=["B0431@1.0"], note="Dan's B-roll: kettlebell swings by the pool"),
 dict(id="G19", kind="lt", start="you should buy basic prison", end="rubber coating", topic="KEY POINT",
      point="Skip The $100 Coated One. Buy Basic Iron.", parts=[["Skip The $100 Coated One.", "you should buy"], ["Buy Basic Iron.", "black iron"]]),
 # ---------------- 6 medicine ball
 dict(id="G20", kind="lt", start="medicine ball", end="workout exercises", topic="INTERMEDIATE: ITEM 6",   # round 5: comes up once he is standing again (it sat over his head while he bent to the equipment)
      point="A Medicine Ball.", parts=[["A Medicine Ball.", "medicine"]]),
 dict(id="C27", kind="clip", start="This comes in handy for many", end="home workout exercises", tail=0.3, src=["B0463@1.0"], people="dan", physique=False, 
      note="Dan's B-roll: seated twists with the medicine ball by the pool. round 5 (the delivery gate read 33 % cutaway cover against its 40 % floor): Dan's own unused B-roll, placed on the words that name it"),
 dict(id="C11", kind="clip", start="is toe touches", end="that exercise yet", tail=0.2, src=["B0434@0.5"], people="dan", physique=False, note="Dan's B-roll: medicine ball toe touches by the pool"),
 dict(id="G21", kind="lt", start="Now the mistake that most people make", end="only four pounds", topic="THE COMMON MISTAKE",
      point="Buying One That's Too HEAVY. Mine Is 4 lb.", parts=[["Buying One That's Too HEAVY.", "Now the mistake"], ["Mine Is 4 lb.", "the one that I have"]]),
 dict(id="F05", kind="scene", scene="fact", people="none", physique=False, start="So what you're seeing on screen right now", end="most people", tail=1.0, photo=f"{AS}/card_medball.png", label="AI-GENERATED",
      eyebrow=["MEDICINE BALL", "So what you're seeing"], headline=[["6 lb", "six"]],
      detail=["About $20.", "right for"], push=1.05, drift=-8),
 dict(id="C12", kind="clip", start="because it's a little bit more ergonomic", end="in that repetition", tail=0.2, src=["B0467@1.0"], people="dan", physique=False,
      note="Dan's B-roll: lying toe-touch crunches (the ball coming back to the ground). round 6: starts 1.9 s earlier, on 'because it's a little bit more ergonomic', "
           "so it is up before he throws both arms overhead (9:32.5): his hands leave the CAMERA frame there and no crop can bring them back. Same clip from the same point, played longer, not slowed"),
 dict(id="G22", kind="lt", start="but if you want to save money", end="dumbbell instead", topic="SAVE MONEY HERE",
      point="A 5 lb Plate Or Dumbbell Works Too.", parts=[["A 5 lb Plate Or Dumbbell", "but if you want"], ["Works Too.", "Just use"]]),   # round 6: two parts again
 # ---------------- 7 dumbbells
 dict(id="G23", kind="lt", start="Like we see right here", end="essential arm exercise", topic="INTERMEDIATE: ITEM 7",   # round 5: up after he has picked the dumbbells up (the strip sat on the equipment row in the wide)
      point="Dumbbells.", parts=[["Dumbbells.", "Like we see"]]),
 dict(id="C25", kind="clip", start="very useful for doing your curls", end="essential arm exercise", tail=0.1, src=["B0432@1.0"], people="dan", physique=False, 
      note="Dan's B-roll: standing dumbbell curls by the pool. round 5 (the delivery gate read 33 % cutaway cover against its 40 % floor): Dan's own unused B-roll, placed on the words that name it"),
 dict(id="C26", kind="clip", start="variety of different arm exercises", end="do with these", tail=0.1, src=["B0449@1.0"], people="dan", physique=False, 
      note="Dan's B-roll: seated dumbbell overhead press by the pool. round 5 (the delivery gate read 33 % cutaway cover against its 40 % floor): Dan's own unused B-roll, placed on the words that name it"),
 dict(id="F06", kind="scene", scene="fact", people="none", physique=False, start="it's going to run you about $29", end="scale with the weight", tail=0.3, photo=f"{AS}/card_dumbbells.png", label="AI-GENERATED",
      eyebrow=["25 LB DUMBBELLS", "it's going to run"], headline=[["$29", "29"]],
      detail=["Heavier costs more.", "like with the kettlebell"], push=1.05, drift=-8),
 dict(id="G24", kind="lt", start="So if you can only afford one pair", end="showed you on screen", topic="ONLY BUYING ONE PAIR?",
      point="Pick Your Curl Weight: About 25 lb.", parts=[["Pick Your Curl Weight:", "So if you can only"], ["About 25 lb.", "25 pounds"]]),
 dict(id="G25", kind="lt", start="30 seconds of curls and then", end="30 seconds of side laterals", tail=1.5, topic="BUYING TWO PAIRS?",
      point="Add A Light Pair For Side Laterals.", parts=[["Add A Light Pair", "lighter weight"], ["For Side Laterals.", "side laterals"]]),   # round 6: two parts again
 dict(id="C13", kind="clip", start="These side laterals are important", end="best way to build your deltoids", tail=0.1, src=["B0450@0.3"],   # round 5: the clip is 8.0 s long and the old slot was 8.4 s (never hold a clip): out on "deltoids"
      note="Dan's B-roll: dumbbell side laterals by the pool"),
 dict(id="G31", kind="lt", start="In that case, I recommend a heavy pair", end="40 or 45 pounds", tail=1.1, topic="BUYING THREE PAIRS?",
      point="Add A Heavy Pair For Triceps: 40 To 45 lb.", parts=[["Add A Heavy Pair For Triceps:", "heavy pair"], ["40 To 45 lb.", "40 or 45"]]),
 dict(id="G32", kind="lt", start="most important dumbbells", end="light for your side laterals", tail=0.9, topic="THE 3 PAIRS TO BUY",
      point="Heavy: Triceps. Medium: Curls. Light: Laterals.", parts=[["Heavy: Triceps.", "heavy for triceps"], ["Medium: Curls.", "medium for curls"], ["Light: Laterals.", "light for your"]]),
 # ---------------- intermediate recap
 dict(id="G33", kind="lt", start="the kettlebell good for", end="weight that you're using", topic="INTERMEDIATE SETUP",
      point="Kettlebell $45. Ball $20. Dumbbells $29.", parts=[["Kettlebell $45.", "the kettlebell good"], ["Ball $20.", "Your medicine ball"], ["Dumbbells $29.", "your dumbbells"]]),
 dict(id="G26", kind="lt", start="only going to cost you", end="about $150", tail=1.9, topic="THE FULL SETUP",
      point="$58 + $94 = About $150 For EVERYTHING.", parts=[["$58 + $94", "94"], ["= About $150 For EVERYTHING.", "150"]]),
 dict(id="C14", kind="clip", start="This stuff will make a huge difference", end="in your life", tail=0.1, src=["B0473@0.5", "B0474@0.5"], note="Dan's B-roll: his dumbbell, then his kettlebell and ab wheel, low angle"),
 # ---------------- towel
 dict(id="G27", kind="lt", start="You will also need a towel", end="hand towels like this", topic="ONE MORE THING",
      point="A Few Strong Hand Towels.", parts=[["A Few Strong Hand Towels.", "towel"]]),
 dict(id="C15", kind="clip", start="we're going to be doing things like these towel rows", end="with the towel", tail=0.3, src=["B0465@1.0"], note="Dan's B-roll: towel pull-aparts"),
 # ---------------- caveats
 dict(id="C30", kind="clip", start="OK guys", end="basic home workout set", tail=0.3, src=[f"{SHOOT}/C1557.MP4@7.0"], grade="C1559", people="none", physique=False,
      note="round 5 (watch judge): he wipes his nose with the back of his hand for the first second of this take, over 'OK, guys, so that's'. Covered with the real equipment, "
           "locked off and wide (roll C1557 from 7.0 s; the opening's panning shot C02 is a tight moving window of the first seconds of the same roll)"),
 dict(id="G28", kind="lt", start="50 and a great", end="around 150", topic="RECAP",   # round 5, fourth render: up as the equipment cutaway C30 ends (it sat across the equipment in that shot)
      point="Basic Setup: $58. Full Setup: About $150.", parts=[["Basic Setup: $58.", "50 and a great"], ["Full Setup: About $150.", "great set up"]]),
 dict(id="G29", kind="lt", start="However, I don't want you to stay", end="get a gym membership", topic="KEY POINT",
      point="Start At Home. Then UPGRADE To A Gym.", parts=[["Start At Home.", "However"], ["Then UPGRADE To A Gym.", "more sophisticated"]]),
 dict(id="C16", kind="clip", start="So that's why eventually I want you to get a gym", end="gym membership", tail=0.1, src=["B0290@1.0"], people="other", physique=False,
      note="stock (Pexels, library B0290, unused before): a man bench pressing in a modern gym. round 5 cover for the closing section, from our clip library (nothing generated, nothing bought)"),
 dict(id="C17", kind="clip", start="You could also build a full gym", end="at your house", tail=0.15, src=["B0298@2.0"], people="other", physique=False,
      note="stock (Pexels, library B0298, unused before): a man deadlifting in a home gym. round 5 cover for the closing section, from our clip library (nothing generated, nothing bought)"),
 dict(id="G34", kind="lt", start="Most important is going to be the barbells", end="that type of thing", topic="WHAT A GYM ADDS",
      point="Barbells. Leg Press. Leg Curl. Bumper Plates.", parts=[["Barbells.", "the barbells"], ["Leg Press.", "Leg press"], ["Leg Curl.", "leg curl"], ["Bumper Plates.", "bumper plates"]]),
 dict(id="C18", kind="clip", start="Most important is going to be the barbells", end="in this setup", tail=0.1, src=["B0327@3.6"], people="other", physique=False,
      note="stock (Pexels, library B0327, unused before): a plate goes onto a barbell at a squat rack. round 5 cover for the closing section, from our clip library (nothing generated, nothing bought)"),
 dict(id="C19", kind="clip", start="Leg press machine", end="really important one", tail=0.2, src=["A0110@1.0"], label="AI-GENERATED", people="dan", physique=False,
      note="existing AI clip (library A0110, the app's own leg press demo of AI-Dan), picture only. round 5 cover for the closing section, from our clip library (nothing generated, nothing bought)"),
 dict(id="C20", kind="clip", start="The leg curl machine", end="really important one", tail=0.2, src=["A0106@1.0"], label="AI-GENERATED", people="dan", physique=False,
      note="existing AI clip (library A0106, the app's own leg curl demo of AI-Dan), picture only. round 5 cover for the closing section, from our clip library (nothing generated, nothing bought)"),
 dict(id="C21", kind="clip", start="having access to bumper plates", end="a lot better for you", tail=0.1, src=["A0019@0.2"], label="AI-GENERATED", people="other", physique=False,
      note="existing AI clip (library A0019, first 5 s only: the part before its red X): a lifter loads a bar on a lifting platform. round 5 cover for the closing section, from our clip library (nothing generated, nothing bought)"),
 dict(id="G30", kind="lt", start="Eventually, once you're ready", end="at your house", topic="ACTION STEP",     # round 5: "So I want you guys to get started" is in the length trim; same text, anchored on the sentence that stays
      point="Buy The Basics Now. Upgrade When You're Ready.", parts=[["Buy The Basics Now.", "Eventually"], ["Upgrade When You're Ready.", "once you're ready"]]),
 # ---------------- CTA
 # round 6 (Dan, 15:49: "I don't like that. It's just me looking at my phone. I want to replace this with the camera scene with a graphic of the Abs By AI home
 # screen next to me, and then click into it, seeing the calorie tracking functionality, seeing some of the AI-generated workout videos ... in a left-third graphic
 # within a phone frame next to me"). C29 (B0437) is out. P03 = Dan on camera, shifted right in one fixed composition, the approved phone shell on the left third
 # (phone_side.py). It runs for the whole sentence (shot cta.0r1), because a home screen, two taps, a meal analysis and two exercise videos do not fit in 4.6 s.
 dict(id="P03", kind="clip", start="On absbyai", end="just for you", tail=0.1, src=["/Volumes/Extreme/_edit_work/ro06/round6/phone/P03-side.mp4@0.0"],
      people="dan", physique=False, label="AI-GENERATED", label_in_picture=True,
      note="round 6: Dan on camera (the same take, same frames, moved 290 px right, never animated) with the app in the approved iPhone shell on the left third. Screens in order: the app's own home screen "
           "(captured at phone size from a local copy of the app, appcap6.py), a visible tap on Macro Tracker, the real meal-photo recording B0038 (salmon plate to the itemised 775 calories), "
           "home again with a visible tap on AI Trainer, then the app's own Push-Up and Reverse Lunge exercise sheets with their demo videos playing at natural speed. "
           "The two demos are AI-made footage of Dan and carry the app's AI-GENERATED chip on the video"),
 dict(id="P01", kind="clip", start="you're going to upload your current picture", end="where you want to get to", tail=0.1,
      src=[f"{R5}/phone/P01-softblue.mp4@0.0"], people="dan", physique=True, label="AI-GENERATED", label_in_picture=True,
      note="Dan's approved self-generation demo (Ad 14 R3 g17: sunglasses before to pool goal, simulated/composited provenance), same screen content, steps and timing, "
           "rebuilt in the Soft Blue phone card (phone_demo.py): the approved iPhone shell on the field, 'Real picture of me' on the before picture, the result's AI-GENERATED chip exactly as approved (inside the picture)"),
 dict(id="P02", kind="clip", start="If you don't have a certain piece of equipment", end="have in place", tail=0.1, src=[f"{R5}/phone/P02-softblue.mp4@0.0"],
      people="dan", physique=False, label="AI-GENERATED", label_in_picture=True,
      note="real app screen recording B0034 from 2.5 s (the workout list, a visible tap on 'How to do it', the Goblet Squat sheet) in the approved upright-phone format; the sheet's player is paused in the recording, so the app's own demo file plays in its rectangle, "
           "full screen in the Soft Blue phone card because the closing roll is shot too close for a phone beside Dan; the AI exercise demo carries AI-GENERATED on the video; key point beside the phone"),
]
