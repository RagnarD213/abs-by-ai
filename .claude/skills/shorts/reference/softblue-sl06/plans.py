"""SL-06: six Shorts from RO-12 "Top 5 Zepbound Tips" as data. Film seconds are on the RO-12 master (9:11.42, sha 7f6766c5).
seg     audio pieces kept (film in, out); every edge sits in measured silence on the film's dry voice (snap.py)
pickup  Dan's recorded opening line (VIDEO-RULES 2026-10-11): text + the treated wav (pickup.py); it plays before piece 0
covers  picture that replaces the talking shot: dict(id, a, b = film times, or "o1.2" output time, or "head" = the pickup's end,
        src + t (clip in-point) + fx/fy (where the fill crop sits) + fit (fill|square|whole) + eq (colour correction) + ai (chip xy),
        or scene=<name in scenes.py> for a film graphic rebuilt for the vertical picture area)
shots   per talking shot (index in `batch.py plan` order): win full|mid, cx, auto (steady holds that alternate the two sizes)
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets
text    the captions as spoken: `shown{spoken}` for numbers, ` | ` at each audio piece join (the pickup is piece 0)"""
STOCK = "/Volumes/Extreme/_edit_work/sl06/clips/"          # copies; never read from another session's build folder at render time
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
DISC = "Not medical advice. Talk to your doctor."
Y0 = {"full": 0, "mid": 78}        # source top row of each window (1920-space): mid is hair-anchored (hair top 120 - 4 % of 900)
KEEP = 0.90
TRIM = {}
SEG = {
 "A": [[60.42, 67.50], [80.95, 116.72]],
 "B": [[40.62, 49.12], [55.20, 60.25], [67.65, 72.08], [117.08, 126.98], [140.75, 162.12]],
 "C": [[164.70, 216.08]],
 "D": [[258.15, 305.40]],
 "E": [[341.03, 350.95], [362.35, 407.30]],
 "F": [[410.55, 465.25]],
}
PICKUP = {
 "A": dict(text="Here's why you should start Zepbound at 1 milligram to avoid the side effects.", wav="pickups/A.wav"),
 "B": dict(text="Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead.", wav="pickups/B.wav"),
 "C": dict(text="Here's how to inject Zepbound with a needle, step by step.", wav="pickups/C.wav"),
 "E": dict(text="Here's how to come off Zepbound without gaining the fat back.", wav="pickups/E.wav"),
 "D": dict(text="Here's why Thursday evening is the best time to inject Zepbound.", wav="pickups/D.wav"),
}
NAME = {"A": "short1_start-at-1-mg-not-2-5", "B": "short2_use-a-needle-and-vial-not-the-pen", "C": "short3_how-to-inject-in-10-seconds",
        "D": "short4_inject-on-thursday-evening", "E": "short5_how-to-come-off-without-regaining-it", "F": "short6_how-much-protein-you-need"}
TITLE = {"A": ("GLP-1 Tips", ["Start At 1 mg,", "Not 2.5 mg"]), "B": ("GLP-1 Tips", ["Use A Needle And", "Vial, Not The Pen"]),
         "C": ("GLP-1 Tips", ["How To Inject", "In 10 Seconds"]), "D": ("GLP-1 Tips", ["Inject On", "Thursday Evening"]),
         "E": ("GLP-1 Tips", ["How To Come Off", "Without Regaining It"]), "F": ("GLP-1 Tips", ["How Much Protein", "You Need On A GLP-1"])}
COVERS = {
 "A": [dict(id="vials", a="o0.0", b="head", src=STOCK + "cand/px6824057.mp4", t=6.0, fy=0.45),      # r2: drawing a measured dose with an insulin syringe (B0329 read "COVID-19 vaccine"; the green-background syringes have long needles)
       dict(id="tray", a=80.95, b=87.19, src=STOCK + "px8413544.mp4", t=0.2, fx=0.34),
       dict(id="ramp", a=90.58, b=101.97, scene="ramp", steps=[["1 mg", 2.42], ["2 mg", 4.12], ["2.5 mg", 5.52]]),     # r2: in 0.41 s earlier, over his look up (judge A 20.9)
       dict(id="nausea", a=101.97, b=104.29, src=STOCK + "A0137.mp4", t=0.0, fx=0.66, ai=(40, 340, 1.6))],              # r2: ends before the clip's smeared hand (judge A 34.1)
 "B": [dict(id="vialhand", a="o0.0", b="head", src=STOCK + "px6824226.mp4", t=1.0, fx=0.69),
       dict(id="tray", a=67.65, b=72.08, src=STOCK + "px8413544.mp4", t=0.2, fx=0.34),
       dict(id="supplies", a="o34.27", b="o38.10", src=STOCK + "cand/px8670956.mp4", t=0.0, fy=0.5),      # r2: vial and insulin syringes on a table (reviewer B: the long needle contradicted "tiny ones")
       dict(id="barrel", a="o38.10", b="o41.47", src=STOCK + "B0352.mp4", t=6.0, fx=0.75, eq="eq=gamma=1.7:brightness=0.04:saturation=1.1"),      # r2: the printed unit scale on an insulin syringe, "units on the side of the barrel" (the held-up syringe had a long needle, judge B)
       dict(id="pharmacy", a=149.75, b=156.12, src=STOCK + "px8657614.mp4", t=2.0, fx=0.52)],
 "C": [dict(id="draw", a="o0.0", b=167.63, src=STOCK + "cand/px6824057.mp4", t=1.0, fy=0.45),      # r2: drawing a dose with an insulin syringe through "This takes about 10 seconds" (reviewer C: dark opener, staring man)
       dict(id="needle", a="o23.89", b="o26.40", src=STOCK + "px6824121.mp4", t=1.0, fx=0.5),      # r2: an insulin syringe with its short needle, being flicked (the held-up syringe had a long needle, judge B)
       dict(id="blood", a="o26.40", b="o29.80", src=STOCK + "B0536.mp4", t=1.0, fx=0.5),      # r2: "draw blood out of your arm"
       dict(id="plunger", a="o29.80", b="o36.62", src=STOCK + "B0352.mp4", t=2.0, fx=0.75, eq="eq=gamma=1.7:brightness=0.04:saturation=1.1")],      # r2: a thumb pressing an insulin plunger, "Inject the Zepbound slowly"; the arm-injection stock is out (reviewer C)
 "E": [dict(id="scale", a="o0.0", b="head", src=STOCK + "B0376.mp4", t=1.0, fx=0.85),      # r2: opens on the step, not the empty scale (reviewer E)
       dict(id="regain", a=347.83, b=350.95, src=STOCK + "px8045155.mp4", t=4.0, fx=0.45),           # r2: "go off it again, and then regain..."
       dict(id="week", a=372.80, b=375.68, src=STOCK + "px9057559.mp4", t=4.0, fx=0.40, rot=180),     # r2: covers a weak size step at 0:23.5 (judge E), "Keep lowering... per week"
       dict(id="scale2", a=392.02, b=396.13, src=STOCK + "px6719385.mp4", t=0.3, fx=0.58),
       dict(id="jumprope", a=396.13, b=402.03, src=STOCK + "B0448.mp4", t=0.9, fx=0.5),             # r2: "Done this way... hold your new body"
       dict(id="stairs", a=404.47, b=407.30, src=STOCK + "px9154824.mp4", t=2.0, fx=0.85)],
 "F": [dict(id="chicken", a="o0.0", b="o2.5", src=STOCK + "px6107302.mp4", t=3.0, fx=0.42),
       # r2: the film's AI split screen (A0058) is out: the body changes inside one take (VIDEO-RULES 2026-10-13, time jumps need a cut), judge F 4.3
       dict(id="curls", a=423.76, b=426.19, src=STOCK + "B0458.mp4", t=1.0, fx=0.5),      # r2: kept; reviewer F-1 read the adjustable dumbbell as an ab wheel (frames show single-arm curls)
       dict(id="abwheel", a=426.19, b=429.76, src=STOCK + "B0030.mp4", t=0.5, fit="span", span=(250, 1670)),      # r2: the rollout travels x 330-1620 of 1920; the square cut his head off (judge F 17.4)
       dict(id="app", a=441.14, b=444.98, src=LIB + "03 B-Roll - Real Footage/screen-recordings/B0035_app-meal-photo-macro-analysis-chicken-broccoli_660x1434_9s.mp4", t=3.85, phone=True),      # r2: starts after the recording's camera-dismiss transition (black block, reviewer F-5)
       dict(id="plate", a=452.95, b=455.35, src=STOCK + "B0063.mp4", t=0.0, fx=0.5),
       dict(id="slices", a=455.35, b=457.76, src=STOCK + "px10348440.mp4", t=1.2, fx=0.5),      # r2: jerky on a plate for "protein-focused snacks" (reviewer F-6: third chicken shot)
       dict(id="rotisserie", a=457.76, b=458.89, src=STOCK + "B0047.mp4", t=1.0, fx=1.0),
       dict(id="sardines", a=458.89, b=460.73, src=STOCK + "px6398611.mp4", t=4.5, fx=0.42),
       dict(id="egg", a=460.73, b=462.96, src=STOCK + "B0046.mp4", t=30.0, fx=0.45)],
 "D": [dict(id="calendar", a="o0.0", b="head", src=STOCK + "px9057559.mp4", t=0.6, fx=0.40, rot=180),
       dict(id="week", a=261.24, b=267.02, scene="week"),
       dict(id="cheers", a=275.11, b=279.85, src=STOCK + "px7039913.mp4", t=0.5, fx=0.66),
       dict(id="dinner", a=279.85, b=281.88, src=STOCK + "px8922355.mp4", t=3.0, fx=0.28, eq="eq=gamma=1.75:brightness=0.03:saturation=1.08"),      # r2: lifted (reviewer D: luma 0.16 against his 0.39)
       dict(id="pizza", a=281.88, b=283.25, src=STOCK + "px8045155.mp4", t=1.0, fx=0.45),
       dict(id="chips", a=283.25, b=285.92, src=STOCK + "B0490.mp4", t=1.0, fx=0.5)],
}
SPLIT = {"A": [], "B": [],
         "C": [["Inject into your thigh", 0.0], ["Pinch the fat.", 0.0], ["Stick the needle in,", 0.0], ["Inject the Zepbound slowly.", 0.0], ["Wait one second", 0.0], ["And here's how you grade", 0.0]],
         "E": [["If you do not gain", 0.0], ["Keep lowering by half", 0.0], ["If you go above", 0.0], ["You do not drop again", 0.0]],
         "F": [["Food stops being interesting.", 0.0], ["So what that looks like", 0.0]], "D": [["If you inject on a Monday", 0.0], ["You are giving the medication", 0.0]]}
SHOTS = {
 "A": {6: dict(win="mid"), 7: dict(win="full")}, "B": {}, "C": {}, "E": {}, "F": {},      # r2 A: the full window under the My Dose bar (reviewer A)
 "D": {1: dict(win="full"), 3: dict(win="mid"), 8: dict(win="full"), 9: dict(win="mid"), 10: dict(win="full")},
}
BARS = {
 "A": [dict(id="G1", topic="Key Point", parts=[["Most Of You Should Start", "should be taking"], ["BELOW The 2.5 mg Dose", "standard"]], a=-0.3, b=2.4),
       dict(id="G2", topic="My Dose", parts=[["1.5 mg A Week", "currently taking"], ["For Long-Term Maintenance", "a week and"]], a=-0.3, b=2.8)],
 "B": [dict(id="G2", topic="Key Point", parts=[["The Pen Only Gives", "more difficult"], ["Standard Doses", "get a dose"]], a=-0.3, b=2.3),
       dict(id="G3", topic="Key Point", parts=[["With A Needle, YOU Control", "than the pen"], ["The Dose And The Speed", "fires the drug"]], a=-0.3, b=2.2),
       dict(id="G4", topic="Key Point", parts=[["Know Your Units,", "pull back"], ["Then Draw To That Line", "entire skill"]], a=-0.3, b=3.2)],
 "C": [dict(id="G1", topic="Step 1 Of 5", parts=[["Outer Front Thigh,", "Inject into your thigh"], ["Midway Down", "around the middle"]], a=-0.2, b=3.4),
       dict(id="G2", topic="Step 2 Of 5", parts=[["Pinch A Fold Of Fat:", "Pinch the fat"], ["It Goes Into Fat, Not Muscle", "between your fingers"]], a=-0.2, b=5.8),
       dict(id="G3", topic="Step 3 Of 5", parts=[["Needle In,", "Stick the needle"], ["Not Too Deep", "not too deep"]], a=-0.2, b=2.6),
       dict(id="G4", topic="Step 4 Of 5", parts=[["Push The Plunger", "Inject the Zepbound"], ["SLOWLY", "slowly"]], a=-0.2, b=2.6),
       dict(id="G5", topic="Step 5 Of 5", parts=[["Wait 1 Second,", "Wait one second"], ["Then Withdraw", "then withdraw"]], a=-0.2, b=2.6),
       dict(id="G6", topic="Key Point", parts=[["Blood Or Pain Means", "If you bled"], ["Your Technique Was Off", "messed it up"]], a=-0.3, b=2.1)],
 "E": [dict(id="G1", topic="Taper Step 1", parts=[["Drop From 2.5 mg", "lowering your dose"], ["To 2 mg", "dose from"]], a=-0.2, b=2.2),
       dict(id="G2", topic="Taper Step 2", parts=[["No Weight Gain?", "do not gain"], ["Go Down To 1.5 mg", "any weight"]], a=-0.2, b=2.2),
       dict(id="G3", topic="Taper Step 3", parts=[["Drop 0.5 mg Each Week", "Keep lowering"], ["While At Or Below Goal", "as long as"]], a=-0.2, b=1.8),
       dict(id="G4", topic="If You Go Over Goal", parts=[["Even By 0.1 lb:", "even by"], ["Hold Your Dose", "stay at your"]], a=-0.2, b=2.6),
       dict(id="G5", topic="If You Gain 3+ lb", parts=[["Over Goal Weight:", "more than three"], ["Go Back Up 0.5 mg", "go back up"]], a=-0.2, b=2.0)],
 "F": [dict(id="G1", topic="Your Protein Target", parts=[["At Least 0.8 g Per Pound", "at least"], ["Of Lean Body Mass, Every Day", "grams of protein"]], a=-0.3, b=2.4)],
 "D": [dict(id="G1", topic="Key Point", parts=[["Inject Thursday Evening", "inject Thursday"], ["So It Peaks On The Weekend", "maximum strength"]], a=-0.3, b=2.6)],
}
TEXT = {
 "A": "Here's why you should start Zepbound at 1{one} milligram to avoid the side effects. | And for most of you watching this channel, you should be taking less than the standard 2.5{two point five} milligram minimum dose. | I have found that a dose as small as 1{one} milligram can be beneficial for people who are already in excellent shape. 1{one} milligram. That is less than half of what the pen would give you. For most of you watching this channel, you should start at 1{one} milligram and then step up to 2{two} and then to 2{two} and a half. That gradual ramp avoids nearly all of the side effects that come from stepping up your dose. The nausea, the fatigue, the days where you feel like garbage. Most of that is the jump, not the drug. Once you've lost the weight, you can dial it down to maintain. I'm currently taking 1.5{one point five} milligrams a week and this is a great long-term maintenance dose for me.",
 "B": "Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead. | There are two ways to inject Zepbound, by filling a needle from a vial or with a KwikPen{quick pen} or auto-injector. And it's important you use a needle and the vial. | The problem with the pen is that it's more difficult to get a dose outside standard doses. | With a vial and a needle, adjusting your dose precisely is much easier. | And here's the part nobody believes until they do it. Once you get good with a needle, it is less painful than the pen. The pen fires the drug at its own speed. You control the needle. | You are not doing surgery. You get a vial and you get insulin syringes, which are the tiny ones. And your dose is measured on units on the side of the barrel. Your doctor or your pharmacy will tell you exactly how many units equals a milligram for the concentration you have. And then you just pull back to that line. That is the entire skill. If you can read a measuring cup, you can do this.",
 "C": "Here's how to inject Zepbound with a needle, step by step. | This takes about 10{ten} seconds once you know what you are doing. Inject into your thigh on the outer front part, right around the middle. Not the inside of your leg, not down by your knee. Pinch the fat. You want a good fold of fat between your fingers because this is a subcutaneous injection. It goes into fat, not into muscle. Stick the needle in, not too deep. This is a tiny short needle, nothing like the needles that they used to draw blood out of your arm. Inject the Zepbound slowly. Do not slam it in too fast. Wait one second after it is all gone, then withdraw. That's the whole thing. And here's how you grade yourself. A good stick is nearly painless and there is no blood. If you bled, or if it actually hurt, you messed it up. Change something next time. You went too deep, or you were in the wrong spot, or you pushed the plunger too fast.",
 "E": "Here's how to come off Zepbound without gaining the fat back. | Coming off is where I see people destroy everything they built. I have watched multiple people lose a huge amount of fat on Zepbound, go off it again, and then regain almost all of it. | So here's the process that I use instead. Instead of going off totally, start by lowering your dose from 2.5{two point five} mg{m g} to 2{two}. If you do not gain any weight, go down to 1.5{one point five}. Keep lowering by half a mg{m g} per week as long as you stay at or below your goal weight. If you go above your goal weight, even by a tenth of a pound, you stay at your current dose. You do not drop again that week, and if you gain more than three pounds above goal weight, you go back up half a milligram. That is it. You are just walking the dose down and letting the scale tell you when to stop. Done this way, you can taper all the way off over a couple of months and hold your new body the entire time. Do not white-knuckle your way off this medication. Walk down the stairs instead of jumping off the roof.",
 "F": "Zepbound reduces your appetite, so eating less calories is easier. But studies have shown the average person loses a catastrophic amount of muscle on this medication. But you can avoid all muscle loss on Zepbound by making sure to eat enough protein and by weight training regularly. In fact, I have gained muscle and strength on Zepbound because of this. Hitting your daily protein is harder on this medication because you're not hungry. Food stops being interesting. And if you're not focused on your protein intake and you're just winging it, you might not get enough. So track your macros and ensure you hit your protein every day. What you're aiming for is at least 0.8{zero point eight} grams of protein per pound of lean body mass. So what that looks like in real life is a serious serving of protein with lunch and dinner, around 8{eight} ounces each, and then protein-focused snacks in between. Rotisserie chicken, sardines, jerky, eggs. Your snacks should be protein. Your snacks should not be carbs.",
 "D": "Here's why Thursday evening is the best time to inject Zepbound. | The medication is strongest in the first few days after your shot and it fades towards the end of the week. So the question is, which days of the week need the most help? For me and for basically every guy I have ever talked to about this, the answer is the weekend. Monday through Thursday, I am dialed in. Friday night, Saturday, Sunday, that is where diets go to die. That is the dinner out, the drinks, the pizza with the family, the nothing-to-do afternoon when you eat out of boredom. If you inject Thursday evening, your appetite suppression is at maximum strength Friday night through Sunday. You have the drug working hardest exactly when your willpower is working worst. If you inject on a Monday, you are spending your strongest days on the days you are going to win anyway. You are giving the medication to the version of you that did not need help.",
}
