"""SL-07: five Shorts from RO-16 "If I Had Belly Fat, Here's How I'd Lose It In 90 Days" as data. Film seconds are on the RO-16
round 3 master (12:09.33, sha c535ab4c). Dan's picks 2026-10-12: A, B, D, E, F.
seg     audio pieces kept (film in, out); every edge sits in measured silence on the film's dry voice (snap.py)
pickup  Dan's recorded opening line (VIDEO-RULES 2026-10-11): text + the treated wav (pickup.py); it plays before piece 0
covers  picture that replaces the talking shot: dict(id, a, b = film times, or "o1.2" output time, or "head" = the pickup's end,
        src + t (clip in-point) + fx/fy (where the fill crop sits) + fit (fill|square|whole) + eq (colour correction) + ai (chip xy),
        or scene=<name in scenes.py> for a film graphic rebuilt for the vertical picture area)
shots   per talking shot (index in `batch.py plan` order): win full|mid, cx
split   a size step inside one continuous take, in the pause before a phrase
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets
text    the captions as spoken: `shown{spoken}` for numbers, ` | ` at each audio piece join (the pickup is piece 0)"""
STOCK = "/Volumes/Extreme/_edit_work/sl07/clips/"          # copies; never read from another session's build folder at render time
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
DISC = {}                           # no drug or medical line in any of the five (E stops before the Zepbound microdose lines)
Y0 = {"full": 0, "mid": 78}        # source top row of each window (1920-space): mid is hair-anchored (hair top 121 - 4 % of 900)
KEEP = 0.90
TRIM = {}
SEG = {
 "A": [[40.68, 67.75], [78.50, 103.55]],        # piece 1 opens 0.1 s before its first word; piece 2 at 78.50 so the pause between the two sentences is 0.33 s (at 78.68 it was 0.15 s against his usual 0.4 to 0.6: second reviewer, 10-13)
 "B": [[587.48, 636.62]],
 "D": [[299.62, 353.74]],
 "E": [[642.44, 685.46]],                          # 685.28 cut the final s of "sacrifice" (reviewer, 10-13); the film's own cut is at 685.52
 "F": [[440.99, 488.50]],
}
PICKUP = {
 "B": dict(text="Here's how to know if your fat loss plan is working.", wav="pickups/B.wav", xfade=0.06),      # round 3: studio-set lav take B2 (roll C1722 284.60-286.72) through the film's voice EQ (pickup.py make --film-chain); desk take kept in pickups/desk/
 "D": dict(text="Here's why you should work out every single morning.", wav="pickups/D.wav", xfade=0.06, preroll=0.2),      # round 3: take D2 (C1722 291.94-294.24), same treatment
}
NAME = {"A": "short1_stop-trying-to-lose-1-pound-a-week", "B": "short2_weigh-yourself-every-morning", "D": "short3_work-out-every-morning",
        "E": "short4_the-3-pound-rule", "F": "short5_track-your-calories-with-a-photo"}
EYE = "LOSE YOUR BELLY FAT"
TITLE = {"A": (EYE, ["Stop Trying To Lose", "1 Pound A Week"]), "B": (EYE, ["Weigh Yourself", "Every Morning"]),
         "D": (EYE, ["Work Out Every Morning,", "Not 3 Times A Week"]), "E": (EYE, ["The 3-Pound Rule That", "Keeps Belly Fat Off"]),
         "F": (EYE, ["Track Your Calories", "With A Photo"])}
# B "scale" is a square, not full screen: the scale is the subject and it is 1,000 px wide; a full-screen crop put the caption on it
DARK = "eq=gamma=1.35:saturation=1.08"      # stock that reads darker than the presenter frames (VIDEO-RULES 2026-10-11)
BRIGHT = "eq=gamma=1.2:saturation=1.05"      # Dan's overcast pool rolls (jump rope, curls): skin measured 77 against the presenter's 94 (reviewer, 10-13)
# AI chips: placed by chipplace.py (person mask over 8 frames of each clip), at u=1.6 (326 x 65) so one fits beside every head
COVERS = {
 "A": [dict(id="traffic", a=81.70, b=84.05, src=STOCK + "p32909774.mp4", t=2.0, fx=0.5),
       dict(id="family", a=84.05, b=87.09, src=STOCK + "B0073.mp4", t=0.0, fx=0.03),      # round 3: from 0.0, ends where "eat" begins (reviewer r3: at 87.66 a caption ran across the cut and the dad walked out of frame)      # real footage; the film's AI busy dad (A0063) morphs objects and the tall crop lost the kids (reviewer, 10-13)
       # round 3 B-roll share (gate style:coverage was 10%; round3-plan/coverage.json)
       dict(id="scale2", a=53.10, b=56.55, src=STOCK + "p6719385.mp4", t=0.0, fx=0.5),
       dict(id="rope", a=63.40, b=67.75, src=STOCK + "B0448.mp4", t=0.3, fx=0.5, eq=BRIGHT),
       dict(id="curls", a=97.38, b=101.45, src=STOCK + "B0031.mp4", t=0.0, fx=0.5, eq=BRIGHT)],      # t=0.0: from his first rep, ends mid-rep (at t=1.0 it ran into his rest with arms down: reviewer r3)
 "B": [dict(id="scale", a="o0.0", b="head", src=STOCK + "p6719385.mp4", t=0.5, fx=0.5, nohead="o1.45"),        # full screen, the scale readable in the middle (the side-view clip needed a card)
       dict(id="study", a=601.43, b=608.31, scene="study", t1=1.3, t2=4.4),
       dict(id="needle", a=608.31, b=613.62, src=STOCK + "AI_B1_fix.mp4", t=0.3, fy=1.0, ai=(40, 336, 1.6)),          # Dan 10-13: approved (B1). Round 3: the take swept once and stretched (frame-reviewer FAIL); the dial is rebuilt with a drawn needle that swings back and forth (r3_needle.py)
       dict(id="chart", a=613.62, b=621.19, scene="chart", avg_at=3.6, dots=5.5),
       dict(id="candles", a=632.65, b=636.62, src=STOCK + "AI_B2b.mp4", t=0.0, fy=1.0, ai=(40, 336, 1.6))],      # Dan 10-13: approved (B2). Round 3: the candles shot alone carries the whole line; the eyes-up shot (AI_B2a) changed his hair by itself mid-shot (frame-reviewer FAIL), so it is out
 "D": [dict(id="jumprope", a="o0.0", b="head", src=STOCK + "B0448.mp4", t=1.0, fx=0.5, nohead="o1.9", eq=BRIGHT),      # the opener: full screen, Dan front-on and moving
       dict(id="stairs", a=305.25, b=311.08, src=STOCK + "A0159.mp4", t=0.6, fx=0.5, ai=(40, 336, 1.6)),          # library AI clip (approved in RO-07): sore the morning after; the dark gym stock is out (reviewer, 10-13). Round 3: runs to the cut before "Short daily workouts" (was a 1.3 s talk sliver) for the B-roll share; t=0.6 so it ends inside the clip (6.42 of 6.46 s)
       dict(id="abwheel", a=321.70, b=325.73, src=STOCK + "B0030.mp4", t=0.9, speed=1.25, fit="span", span=(0.13, 0.88)),       # a card: the rollout travels 1,400 px sideways; 1.25x so the return shows
       dict(id="morning", a=335.67, b=338.93, src=STOCK + "p38756590.mp4", t=0.2, fx=0.6, eq="eq=gamma=1.2"),      # round 3: runs past "Let me tell you why." to the pause (a caption ran across the cut at 338.44: reviewer r3)
       dict(id="curls", a=349.95, b=353.74, src=STOCK + "B0031.mp4", t=0.0, fx=0.5, eq=BRIGHT)],             # the ending: Dan full screen (the toe touch needed a card over an empty field)
 "E": [      # round 3: B0435 (Dan posing by the pool, 646.30-648.89) is out (VIDEO-RULES 2026-10-14, never Dan standing around); library A0083 and A0086 (a man enjoying a plate) both carry a cut-out halo on every edge (frame-reviewer FAIL, r3), so he stays on camera there
       dict(id="beer", a=648.89, b=652.05, src=STOCK + "AI_E3.mp4", t=0.5, fy=1.0, ai=(714, 336, 1.6)),              # Dan 10-13: approved (E3); replaces the film's bar stock
       dict(id="scale", a=668.40, b=672.08, src=STOCK + "p6719385.mp4", t=0.0, fx=0.5),
       dict(id="salad", a=674.42, b=680.48, src=STOCK + "B0019.mp4", t=2.0, fx=0.62),          # round 3 B-roll share (gate style:coverage was 21%); runs through "Losing 3 pounds is not a big deal." to the pause
       dict(id="abwheel", a=682.50, b=685.46, src=STOCK + "B0030.mp4", t=0.9, speed=1.25, fit="span", span=(0.13, 0.88))],
 "F": [dict(id="cups", a=450.10, b=454.25, src=STOCK + "AI_F2.mp4", t=0.1, fy=1.0, ai=(714, 336, 1.6)),             # Dan 10-13: approved (F2); replaces the film's food-scale stock. Round 3: t=0.1 so it ends on frame 102, before the cup tower melts as it falls (frames 104+, frame-reviewer FAIL)
       dict(id="photo", a=459.50, b=465.70, src=STOCK + "B0035.mp4", t=0.6, phone=True, darkfill=True, skip=[(3.3, 4.0)]),      # the whole recording, fitted by height as in SL-03; while it shows the black camera the whole phone screen is black; 3.3 to 4.0 s of the recording (the camera sheet closing: a black block and a half page) is skipped
       dict(id="log", a=474.25, b=480.85, src=STOCK + "B0038.mp4", t=4.4, phone=True, vf="crop=536:1008:19:38,scale=518:982:flags=lanczos", round=44)],      # 38: clear of the bezel line at the top of the recording; t=4.4 so the shot ends at 11.0 s of the recording, before its page animation at 11.3 to 12.1 s (it flashed at the corners for a few frames)
}
SPLIT = {
 "A": [["In my opinion, that advice", 0.0], ["Let's say you have", 0.0], ["That is going to take", 0.0], ["It's far, far easier", 0.0], ["So if I was", 0.0]],
 "B": [["Same scale,", 0.0], ["You have to do this", 0.0]],
 "D": [["Short daily workouts", 0.0], ["You're not waking up", 0.0], ["The hour and a half workouts", 0.0], ["By 6 at night", 0.0]],
 "E": [["And once you have", 0.0], ["So how does somebody", 0.0], ["Losing 3 pounds", 0.0], ["Losing 30 pounds", 0.0]],
 "F": [["Now, before AI,", 0.0], ["But with AI,", 0.0], ["Once you start tracking,", 0.0]],
}
SHOTS = {
 "A": {0: dict(win="mid")},        # the opening is the tight window (first 5 seconds); the sizes alternate from there, so the bars land on the full window
 "B": {}, "D": {},      # round 3: the stairs clip now runs to "Short daily workouts", which opens on the wide size by default
 "E": {0: dict(win="mid")},
 "F": {0: dict(win="mid")},
}
BARS = {
 "A": [dict(id="G1", topic="THE MATH", parts=[["30 lb At 1 lb A Week", "That is going"], ["Takes 7 MONTHS", "seven months"]], a=-0.2, b=3.6),
       dict(id="G2", topic="KEY POINT", parts=[["Make Fat Loss", "I would make losing"], ["The Priority For 90 Days", "the number one priority"]], a=-0.2, b=3.4)],
 "B": [dict(id="G1", topic="WHEN TO WEIGH IN", parts=[["On An Empty Stomach,", "right after you"], ["Same Scale, Same Time", "Same scale,"]], a=-0.2, b=2.4),
       dict(id="G2", topic="YOUR WEEKLY CHECK", parts=[["Average Down 2+ lb?", "If my weekly"], ["Change NOTHING", "or more,"]], a=-0.2, b=1.9),
       dict(id="G3", topic="YOUR WEEKLY CHECK", parts=[["Stalled A Full Week?", "stalled out"], ["Cut 200 Calories A Day", "cut 200"]], a=-0.2, b=2.2)],
 "D": [dict(id="G1", topic="KEY POINT", parts=[["Short DAILY Workouts Beat", "Short daily workouts"], ["Long Occasional Ones", "occasional long"]], a=-0.2, b=3.6),
       dict(id="G2", topic="KEY POINT", parts=[["Start With 10 Or 15 Minutes.", "10 or 15 minutes,"], ["You Can Do That Every Day", "consistently do"]], a=-0.2, b=2.4),
       dict(id="G3", topic="WHY MORNINGS", parts=[["The One Time Of Day", "At 8 in the"], ["Nobody Needs You", "nobody is calling"]], a=-0.2, b=3.6)],
 "E": [dict(id="G1", topic="KEY POINT", parts=[["Without A Daily Weigh-In,", "not weighing yourself,"], ["5 lb Quietly Becomes 20", "gain 5 pounds,"]], a=-0.2, b=4.0),
       dict(id="G2", topic="THE 3-POUND RULE", parts=[["More Than 3 lb Over Goal?", "more than 3 pounds"], ["Cut Back Down Right Away", "go right back"]], a=-0.2, b=2.4)],
 "F": [dict(id="G1", topic="KEY POINT", parts=[["A Rough Calorie Count", "It's not perfect,"], ["Beats No Count At All", "reasonably accurate"]], a=-0.2, b=3.2)],
}
TEXT = {
 "A": "Most fitness channels tell you to make small, sustainable changes and to lose 1{one} pound a week. In my opinion, that advice is bullshit, and that is the reason why most of the people following it are still fat. Let's say you have 30{thirty} pounds to lose and you are losing 1{one} pound a week. That is going to take you seven months, and in my opinion, almost nobody can stay motivated for that long. It's far, far easier to go all-in for 90{ninety} days and get it over with. | Most people are trying to squeeze fat loss into their life. They work all day, they drive home, then they take care of their family, and then they try to work out and eat healthy with whatever time and energy is left over. And there usually isn't any left over, so it never happens. So if I was 30{thirty} pounds overweight, I would do it the opposite way. I would make losing fat the number one priority in my life for 90{ninety} days, and everything else would have to fit around that.",
 "B": "Here's how to know if your fat loss plan is working. | Weigh yourself every morning, right after you use the bathroom and before you eat or drink anything. Same scale, same time, every day, even on vacation. No exceptions. You have to do this because it's the only way to know if the plan is working. In one study, the people who weighed themselves every day lost about 13{thirteen} pounds more over six months than the people who didn't. Now, your weight is going to bounce around 2{two} or 3{three} pounds from day to day, just from water and salt. So don't freak out about any one day. What you want to look at is your 7{seven} day moving average for the week, compared to your average for the week before. If my weekly average was dropping about 2{two} pounds or more, I wouldn't change anything. But let's say it stalled out for a full week. I would cut 200{two hundred} calories a day and keep going. Most guys never adjust anything. They just keep doing the same thing for months and hope the scale is going to move.",
 "D": "Here's why you should work out every single morning. | Most guys do it the opposite way. They go to the gym two or three times a week for an hour and a half. They get really sore, then something comes up at work and they miss a day, and within a month they're not going at all. Short daily workouts are far better than occasional long workouts because when you're working out every day, you don't have to think about it. You're not waking up and asking yourself, is today a gym day or not? You just get up and you do it, even on weekends, even on vacation. And if all you can do at first is 10{ten} or 15{fifteen} minutes, that's fine. You can consistently do a 15{fifteen} minute workout every day. The hour and a half workouts are the ones that end up getting skipped. So why first thing in the morning? Let me tell you why. At 8{eight} in the morning, nobody is calling you, your boss doesn't need anything from you yet, and your kids are asleep. By 6{six} at night you're tired, something came up at work, and that's when the workout ends up getting skipped. I work out every morning, 7{seven} days a week, and that's the reason why.",
 "E": "Maintaining your weight is far, far easier than losing weight. And once you have your abs, you can eat more, you can have a drink on the weekend, and you can relax a little bit. You can't do that when you're trying to lose two and a half pounds a week. So how does somebody end up 30{thirty} pounds overweight in the first place? It's because they're not weighing themselves. If you're not weighing yourself, you're going to gain 5{five} pounds, gain 10{ten} pounds, gain 20{twenty} pounds before you even realize it. So here's what I would do. I would keep weighing myself every day. And if I ever got more than 3{three} pounds above my goal weight, I would go right back to cutting calories until it's gone. Losing 3{three} pounds is not a big deal. You could do that in a week or two. Losing 30{thirty} pounds is 90{ninety} days of sacrifice.",
 "F": "If you never look at your bank account, you're probably going to be poor. Same thing applies to your calories. Now, before AI,{a i} I was always against tracking calories. The old way where you weigh your food on a scale and look up every ingredient, that was way too much work for normal people like me and you. But with AI,{a i} everything has changed. Now you just take a picture of your food and you get the calories, the protein, the carbs, and the fat in a few seconds. It's not perfect, but it's reasonably accurate and it's far, far better than not tracking at all. And if you're eating the meal prep meals, you just take a picture of the label. We have a free macro tracker for this at AbsByAI.com.{abs by a i dot com} Just take a picture of your food and it adds up your day for you. Try ours out or use any other AI{a i} calorie tracking app you like. Once you start tracking, you'll be shocked at how much faster you start losing fat.",
}
