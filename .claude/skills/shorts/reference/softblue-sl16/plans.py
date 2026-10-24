"""SL-16: four Shorts from RO-08 "Intermittent Fasting: The Best Way To Get Abs" as data. Film seconds are on the RO-08 round 3
master (14:40.75, sha 976b9761, approved 10-14). Dan's picks 2026-10-22: "Just Skip Breakfast" (Short 1, airs Tue Dec 15), then
"Okay, let's do B, C, D." (shortlist with full transcripts: SHORTLIST.md).
seg     audio pieces kept (film in, out); every edge sits in measured silence on the film's dry voice (snap.py + 10 ms levels)
covers  picture that replaces the talking shot: dict(id, a, b = film times, src + t (clip in-point) + fx/fy + fit + eq + ai (chip xy, u) + speed)
split   a size step inside one continuous take, in the pause before a phrase
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets (copy from the film's approved G12/G14/G21/G22/G34/G35/G37/G46/G47)
text    the captions as spoken, ` | ` at each audio piece join (spellings from the film's corrected .srt; "gonna" where he says it)"""
STOCK = "/Volumes/Extreme/_edit_work/SL-16/clips/"          # copies; never read from another session's build folder at render time
DISC = {}
Y0 = {"full": 0, "mid": 0}        # C1486: the camera framed his hair at the top edge through the roll (RO-08 shot_framing hair_top 3-16 px; accepted by Dan for the film): keep all the head the source has
KEEP = 0.90
TRIM = {}
SEG = {
 # S1: "The" from 543.85 (levels -60 dB to 543.84); "coffee." ends 558.44, silence 558.49 (film join 558.62 after it); "There's" 612.18 after silence 611.90-612.35;
 # "purpose." ends ~624.30, silence 624.36-624.55 (film join 624.49 after it); "Let's" 631.76 after silence 631.19-631.77; "window." decays to -41 dB by 662.27, silence to 662.42.
 "S1": [[543.80, 558.55], [612.10, 624.40], [631.50, 662.36]],
 # B: "When" 364.44 after silence 364.11-364.50; "working." ends 419.12, silence 419.17-419.44 (film join 419.35 after it).
 "B": [[364.30, 419.30]],
 # C: the film's join at 791.99 sits in the silence before "And" (speech from 792.06): start 20 ms after the join. "And here" cannot be split (no dip between them),
 # so the Short opens "And here is the number one most important mistake" (the shortlist showed "Here is"). "reasons." ends 829.36, silence 829.49-829.89 (film join 829.80).
 "C": [[792.42, 829.60]],      # review r1: "And" ends 792.34; a room-level dip 792.36-792.45 before "here": the Short opens "Here is the number one ..."
 # D: the film's own cut at 196.963 opens "Mike" (silence 196.49-197.04); "it." ends 251.56, silence 251.56-251.93 (film join 251.85 after it).
 "D": [[196.99, 211.76], [212.04, 251.75]],      # review r1: an "uh" at film 211.78-212.02 before "There's gonna be things" is cut (under the papers clip)
}
PICKUP = {}
WORDFIX = {}
NAME = {"S1": "fasting-short1_just-skip-breakfast", "B": "fasting-short2_carbs-are-killing-your-workday",
        "C": "fasting-short3_never-break-your-fast-with-alcohol", "D": "fasting-short4_life-will-punch-you-in-the-face"}
EYE = "INTERMITTENT FASTING"          # the eyebrow stays in CAPITALS (Dan, 2026-10-20); typed, never uppercased in code
TITLE = {"S1": (EYE, ["How To Start Fasting:", "Just Skip Breakfast"]), "B": (EYE, ["Carbs Are Killing", "Your Workday"]),
         "C": (EYE, ["Never Break Your Fast", "With Alcohol"]), "D": (EYE, ["Life Will Punch", "You In The Face"])}
LIFT = "eq=gamma=1.2"
DARK = "eq=gamma=1.35:saturation=1.08"
COFFEE = "eq=gamma=1.75:saturation=1.05"
LAPTOP = "curves=all='0/0 0.05/0.02 0.25/0.38 0.65/0.82 0.92/0.97 1/1',eq=saturation=1.12,colorbalance=rm=0.03:gm=0.0:bm=-0.03"     # review r1b (VIDEO-RULES 2026-10-23: a real grade, never a gamma lift alone): p2/p50/p98 0.031/0.431/0.887 against Dan 0.018/0.449/0.924     # review r1: B0486 (dark beans, warm light) measured median 0.11 against Dan's 0.38-0.46     # stock that reads darker than the presenter frames (VIDEO-RULES 2026-10-11; SL-07 value)
COVERS = {
 "S1": [dict(id="opener", a=543.80, b=548.90, src=STOCK + "coldbrew.mp4", t=2.0, fx=0.5),                      # the opener (first 5 s): cold brew poured over ice (the film's C27), bright; review r1: library B0486 read too dark (median 0.11) and a lift made it milky
        # the film's approved AI opener (library A0169) FAILED a fresh frame-reviewer on 2026-10-22: in frames 0-87 the clock face melts and runs backwards, the laptop folds by itself,
        # a spoon appears and vanishes. Frames 88-230 passed (clock holds at 2:00, he eats the salad). Only frames 94-230 are used (reviewer's safest start).
        # ...and a second fresh reviewer FAILED frames 94-230 too (the forkful vanishes inside his open mouth, a held pursed pout): no AI clip in this Short. Real stock instead:
        dict(id="dinner", a=548.90, b=552.09, src=STOCK + "B0485.mp4", t=1.0, fx=0.5),                          # library B0485 (the film's C29): a family tosses a salad at the dinner table, over "keep everything else you're eating throughout the day the same. That's it."
        dict(id="coffeewalk", a=554.00, b=612.70, src=STOCK + "coffeewalk.mp4", t=8.5, fit="square", y=310, fx=0.0),      # review r1c: the stock camera pans, no fixed 9:16 window holds him; SQUARE from 8.5 s keeps face and cup in frame (person mask, 13 samples) and his second sip lands on "drinking black coffee";                 # the film's C17 stock: a man sips his coffee on the walk to work, over "So to help with the hunger ... drinking black coffee", across the join
        # the film's A6 fridge raid (library A0173) FAILED a fresh frame-reviewer: the pizza box changes material, a spray can appears from nowhere, a garbled label. Real stock instead:
        dict(id="milkshakes", a=612.70, b=614.40, src=STOCK + "milkshakes.mp4", t=1.0, fx=0.5),                 # the film's C31 stock: "There's gonna be a temptation to kind of compensate"
        dict(id="sundae", a=614.40, b=616.10, src=STOCK + "icecream.mp4", t=1.0, fx=0.5),                       # the film's C31 second shot: "and eat more in the later part of the day"
        dict(id="wake", a=651.45, b=653.35, src=STOCK + "B0334.mp4", t=2.0, fx=0.5),                            # library B0334 (the film's C36): "So if you wake up at 9 a.m. like me"
        dict(id="lunch", a=653.35, b=655.20, src=STOCK + "salad_dish.mp4", t=0.2, fx=0.5)],                     # Dan's daily salad (the film's C30): "you eat lunch at two o'clock" (from 0.2 s: the clip's first 5 frames are another shot)
 "B": [dict(id="pancakes", a=364.30, b=367.709, src=STOCK + "pancakes.mp4", t=1.0, fx=0.5),                    # the opener: a heavy breakfast (the film's C23) on "When you eat a heavy breakfast"
       dict(id="donut", a=367.709, b=371.672, src=STOCK + "A5.mp4", t=0.0, fit="square", y=310, fx=0.7, ai=(714, 340, 1.6)),      # chip top right (chipplace: 0 overlap with the man; at top left it sat on his head, review r1);      # SQUARE: the full donut box, then the empty box and the clock moving 9 to 10, are the joke; a vertical fill shows only the man          # the film's approved A5 (donut, then asleep on the keyboard) on "food coma", exactly as the film has it
       dict(id="coffee", a=373.10, b=375.75, src=STOCK + "coldbrew.mp4", t=2.0, fx=0.5),                        # the film's C27 (cold brew): "if you're just drinking your black coffee, not consuming anything"
       dict(id="salad", a=386.55, b=389.889, src=STOCK + "salad_bowl.mp4", t=0.0, fx=0.5),                       # Dan lifts the lid off his salad (the film's C08): "eat a salad or a very low carb meal for your lunch"; runs to the film's cut at 389.889 (no 0.2 s sliver of Dan)
       dict(id="laptop", a=401.568, b=405.633, src=STOCK + "laptop.mp4", t=0.5, fx=0.45, eq=LAPTOP),                        # the film's C21: "Nobody is grinding out insane productive 12 hour days"
       dict(id="donuts", a=405.633, b=407.50, src=STOCK + "donuts.mp4", t=0.5, fx=0.5)],                        # the film's C18 stock: "while eating donuts and pizza"
 "C": [dict(id="wine", a=792.42, b=796.70, src=STOCK + "B0517.mp4", t=2.4, fx=0.5),                            # the opener: library B0517 (red wine pouring) under "the number one most important mistake with fasting"
       dict(id="beer", a=800.89, b=805.282, src=STOCK + "beer.mp4", t=1.0, fx=0.5),                             # the film's C34: "Don't drink alcohol with your first meal or God forbid ..."
       # the film's A7 (library A0174) FAILED two fresh frame-reviewers on 2026-10-22 (from frame 50 his face turns cartoonish with scratch marks on the cheek; from 72 a watch
       # appears and the plate vanishes); the clean part is 1.4 s. Dropped: Dan stays on camera for "It's going to hit you faster" (VIDEO-RULES: the camera scene is always acceptable).
       dict(id="laptop", a=823.84, b=827.50, src=STOCK + "laptop.mp4", t=0.5, fx=0.45, eq=LAPTOP)],                         # the film's C21 stock: "If you are working during the day ... avoiding alcohol while you're working"
 "D": [dict(id="glove", a=203.138, b=206.273, src=STOCK + "A0158.mp4", t=0.0, fx=0.5, ai=(40, 340, 1.6)),     # library A0158 (Dan's approved RO-07 gag), exactly where the film has it: the glove lands on "punch"
       dict(id="alarm", a=207.70, b=210.40, src=STOCK + "alarm.mp4", t=1.0, fx=0.5),
       dict(id="papers", a=210.40, b=212.588, src=STOCK + "papers.mp4", t=2.0, fx=0.5),                          # the film's C15 second shot: a man stuffs papers into his work bag (the alarm clip turns to a blur after 3 s)                            # the film's C15 stock: "You're gonna wake up certain days and you won't have time to eat your normal breakfast"
       dict(id="couple", a=212.588, b=215.749, src=STOCK + "couple.mp4", t=2.4, fit="square", y=310, fx=0.4),                        # the film's C12: "with your girlfriend or wife". SQUARE: both faces stay in (a fill keeps one of the two people arguing)
       dict(id="sick", a=215.749, b=218.598, src=STOCK + "sick.mp4", t=3.0, fx=0.3),                            # the film's C13: "times that you're sick"
       # review r1: the food-scale clip (B0017) lost its readout in the vertical crop and read as a bowl of ice cream: dropped, Dan on camera as in the film
       dict(id="overeat", a=229.70, b=235.135, src=STOCK + "spaghetti.mp4", t=2.0, fx=0.62)],                     # the film's C32 stock: "they end up overeating calories"
}
SPLIT = {"S1": [], "B": [["Try it for yourself", 0.0], ["What people are doing", 0.0]], "C": [["It's gonna hit", 0.0]], "D": [["If you had a more", 0.0], ["And in my experience", 0.0]]}
SHOTS = {"S1": {}, "B": {}, "C": {}, "D": {}}
BARS = {
 "S1": [dict(id="G34", topic="WATCH OUT", parts=[["Don't Eat Your Breakfast", "if you eat all"], ["Calories Later", "later in the day"]], a=-0.2, b=2.0),
        dict(id="G35", topic="THEN STEP IT UP", parts=[["Noon, Then 12:30,", "Move that back"], ["Then 1:00", "move it back another"]], a=-0.2, b=2.0),
        dict(id="G37", topic="FOR EXAMPLE", parts=[["Wake Up At 7", "wake up at 7"], ["Eat Lunch At Noon", "eat lunch at noon"]], a=-0.2, b=2.0)],
 "B": [dict(id="G21", topic="KEY POINT", parts=[["It's The Carbs", "the real problem"], ["That Make You Tired", "is the carbs"]], a=-0.2, b=2.0),
       dict(id="G22", topic="WHAT PRODUCTIVE PEOPLE DO", parts=[["Skip Breakfast", "skipping breakfast"], ["Eat A Low Carb Lunch", "super low carb lunch"]], a=-0.2, b=1.8)],
 "C": [dict(id="G46", topic="THE BIG MISTAKE", parts=[["Never Break Your Fast", "Do not break"], ["With Alcohol", "with alcohol"]], a=-0.2, b=1.6),
       dict(id="G47", topic="THE RULE", parts=[["No Alcohol Until 30", "No alcohol until"], ["Minutes After You Eat", "minutes after"]], a=-0.2, b=1.8)],
 "D": [dict(id="G12", topic="MIKE TYSON SAID", parts=[["Everyone Has A Plan", "everybody has a plan"], ["Until They Get Punched", "until they get punched"]], a=-0.3, b=2.2),      # review r1 asked for the film's full "...Punched In The Face": it wraps to 3 lines in the vertical bar (2 max); the caption under it carries the whole quote
       dict(id="G14", topic="KEY POINT", parts=[["You Can Still Fast", "Intermittent fasting though"], ["On Your Worst Day", "feeling bad"]], a=-0.05, b=2.4)],
}
TEXT = {
 "S1": "The easiest way to get started with intermittent fasting is simply to skip your breakfast, keep everything else you're eating throughout the day the same. That's it. Just skip your breakfast. So, to help with the hunger, what I recommend is drinking black coffee. | There's gonna be a temptation to kind of compensate and eat more in the later part of the day. You can eat a little bit more and it will still work, but if you eat all the calories you were gonna eat at breakfast later in the day, you're defeating the purpose. | Let's say you normally eat lunch at noon. Move that back half an hour. Now you eat lunch at 12:30{twelve thirty}. Do that until you feel comfortable and not hungry eating lunch at 12:30{twelve thirty}, probably about 30{thirty} days. Then, move it back another hour until one o'clock. Keep doing that until you're fasting five hours in the morning. So, if you wake up at 9{nine} a.m.{a m} like me, you eat lunch at two o'clock. If you wake up at 7{seven} a.m.,{a m} that means you eat lunch at noon. So, that gives you a daily 5{five} hour fasting window.",
 "B": "When you eat a heavy breakfast, your body has to consume energy to digest. And that's what gives you that food coma, lethargic type of feeling. On the other hand, if you're just drinking your black coffee, not consuming anything, then your energy is actually gonna be higher because your body doesn't need to waste energy on digesting heavy foods. Now, you can maintain this productivity throughout your entire day if you do what I do and eat a salad or a very low carb meal for your lunch. In my experience, the real problem with eating during your workday is the carbs. Try it for yourself. If you're eating a ton of carbs for breakfast or for lunch, it will lower your productivity. Nobody is grinding out insane, productive 12{twelve} hour days while eating donuts and pizza. You just can't do it because it's gonna make you tired. What people are doing who are the most productive in life is skipping breakfast and then eating a super low carb lunch so there's hardly any carbs going into their system when they're working.",
 "C": "Here is the number one most important mistake with fasting that you have to avoid. Do not break your fast with alcohol. Don't drink alcohol with your first meal or, God forbid, don't drink alcohol before you eat anything at all. The reason for that is when you've been fasting for a while, the alcohol will absorb faster, your body is more sensitive to it, and it will do more damage to your fat loss and to your health. It's gonna hit you faster, you're gonna feel more drunk, and the health effects are gonna be a lot worse. No alcohol until 30{thirty} minutes after you've broken your fast. If you are working during the day, then I highly recommend avoiding alcohol while you're working for obvious reasons.",
 "D": "Mike Tyson once said, everybody has a plan until they get punched in the face. And when you're dieting, when you're trying to get lean, life is gonna punch you in the face. There's gonna be emergencies. You're gonna wake up certain days and you won't have time to eat your normal breakfast. | There's gonna be things that come up with your family, with your girlfriend or wife. There's gonna be times that you're sick and you're not feeling your best. There's gonna be so many of these little things that come up. And in my experience, when people are following a complex plan to evenly reduce their calories throughout the day, it doesn't really work out for them in real life. Things come up and they end up overeating calories when they didn't intend to because life punched them in the face. Intermittent fasting though is a plan you can execute when life punches you in the face. If you're feeling bad, if there's an emergency, if you get in an argument with your girlfriend, you still fast your five hours per day or whatever your fasting window is. If you had a more complicated plan, you probably couldn't stick to it.",
}
