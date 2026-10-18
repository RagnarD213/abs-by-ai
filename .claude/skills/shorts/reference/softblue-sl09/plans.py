"""SL-09: five Shorts from Zeeshan's "My Honest Oura Ring Review After 1.5 Years" (Video 4) as data. Film seconds are master
seconds (Zeeshan Rev 3, Dan finalized as is, MD5 5264285762af41f2a6644366e0bae7eb). Dan's picks 2026-10-18: A, H, I, J, K.
Order (handoff): short1 = A, short2 = I, short3 = H, short4 = K, short5 = J.
seg     audio pieces kept (film in, out); every edge sits in a measured pause of his voice (voice-band VAD + 20 ms envelopes,
        edges.py: his mix carries a soft music bed, so silencedetect is not the ground truth)
covers  picture that replaces his picture: dict(id, a, b = film times, src + t (clip in-point) + fx/fy + fit + eq,
        or hf=<HyperFrames scene render> (our moving Soft Blue scenes), or psolo + rect (the film's own app screen in our phone shell))
shots   per talking shot (index in `batch.py plan` order): win full|mid, cx
bars    key-point lower thirds: topic (title case), [[line, phrase it lands on]], a/b offsets
text    the captions as spoken: `shown{spoken}` for numbers, ` | ` at each audio piece join"""
W9 = "/Volumes/Extreme/_edit_work/sl09/round2/"
STOCK = W9 + "clips/"
MASTER = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Zeeshan Content Videos/my honest oura ring review - video 4/my honest oura ring review | zeeshan | 16x9 | video 4.mp4"
DISC = {}
Y0 = {"full": 0, "mid": 0}          # his wides and near shots put Dan's hair at source rows 0-60: every window starts at row 0 (handoff)
KEEP = 0.90
TRIM = {}
# Zeeshan's own cuts (first frame of his new shot, master seconds; cutframes.py, frame-exact) in the five passages
ZCUTS = [n * 1001 / 30000 for n in (
    5859, 6240, 6818, 6833, 7127,                                        # K
    20846, 21267, 21759, 22137, 22152,                                   # A
    27885, 27900, 28180, 28335, 28350, 28512, 28577, 28587, 28880, 29162,       # H (27900: his same-size cut at 15:30.93, hidden behind his zoom just before it; reviewer H)
    30009, 30210, 30711, 30718, 31223, 31643, 31918,                     # I (30718: the end of his white flash after the sleep-score card)
    32594, 33316)]                                                       # J (32594: his cut at 18:07.55, two frames before our comparison scene)
SEG = {
 "A": [[681.95, 738.95]],            # in: 0.13 s before "The" (gap 681.48-682.07); out: "injured" ends 738.70, next word 739.46
 "H": [[976.30, 984.45],             # the opener moved up from the end of its passage (handoff): "There" starts 976.40 (gap 975.79-976.40)
       [928.40, 976.10]],            # "Driving" starts 928.48; "driving." ends 975.80, pause to 976.40
 "I": [[989.16, 1035.35],            # the leading "And" (988.98-989.08) is dropped: in inside the dip before "here" (989.22)
       [1056.25, 1065.35]],          # 1035.54-1056.28 cut (Nobody is worth ... especially late at night?); "go." ends 1065.10
 "J": [[1066.95, 1113.17]],          # in: "should" 1067.06 ("So the overall verdict," dropped); out: "low." ends 1113.10 (his zoom into the outro starts 1112.85: the comparison scene covers the end, reviewer J)
 "K": [[195.00, 237.50]],            # in: "you" 195.13 ("So the bottom line is" dropped); out: "Ring." ends 237.40, his whip blur starts 237.54
}
PICKUP = {}
ORDER = {"A": 1, "I": 2, "H": 3, "K": 4, "J": 5}
NAME = {"A": "oura-short1_train-harder-after-a-bad-nights-sleep", "I": "oura-short2_your-sleep-score-shows-whos-toxic",
        "H": "oura-short3_cut-the-adrenaline-before-bed", "K": "oura-short4_youre-not-sleeping-as-well-as-you-think",
        "J": "oura-short5_oura-ring-or-whoop-which-one-to-buy"}
TITLE = {"A": ("Sleep And Training", ["Train Harder After", "A Bad Night's Sleep"]),
         "I": ("Sleep Better", ["Your Sleep Score Shows", "Who's Toxic In Your Life"]),
         "H": ("Sleep Better", ["Cut The Adrenaline", "Before Bed"]),
         "K": ("Sleep Better", ["You're Not Sleeping", "As Well As You Think"]),
         "J": ("Sleep Tracker Verdict", ["Oura Ring Or WHOOP?", "Which One To Buy"])}
DARK = "eq=gamma=1.25:saturation=1.06"
HF = W9 + "hf/renders/"
APP = dict(src=MASTER, psolo=True, rect=[96, 170, 323, 717])     # Dan's real Oura app recording from the film (7:00-7:18, his phone mock at x 91-424): the screen only, in our phone shell
# every cover: output times "oX" (seconds into the short). Clip choices and checks: clips/CANDIDATES.md (frame-checked every 0.25 s)
COVERS = {
 "A": [dict(id="wake", a="o0.0", b="o7.95", src=STOCK + "A-open__3801360.mp4", t=3.2, fx=0.5),          # first 5 s: a man jolted awake by his alarm (portrait, fills); covers his lower third 11:22-11:27 whole (+1.2 s fade)
       dict(id="rope", a="o16.55", b="o20.40", src=STOCK + "A-hard__B0448.mp4", t=1.0, fx=0.5),          # "work out harder": Dan's fast jump rope (the correct one, B0448)
       dict(id="deadlift", a="o31.80", b="o33.53", src=STOCK + "A-risky__12890962.mp4", t=4.4, fx=0.5),  # "the deadlifts"
       dict(id="clean", a="o33.53", b="o36.20", src=STOCK + "A-risky__5837790.mp4", t=6.8, fx=0.45),     # "the power cleans and those kind of high risk moves"
       dict(id="curls", a="o36.20", b="o45.00", src=STOCK + "A-end__B0031.mp4", t=0.0, fx=0.5, eq="eq=gamma=1.15:saturation=1.05"),     # "training in the low risk way we recommend": Dan's standing curls (B0031; from t=0, SL-07), to the pause before "if you" (reviewer: it ended 0.37 s into "So I would say"). B0460 squats: Dan small and in shade
       dict(id="groggy", a="o47.40", b="o50.15", src=STOCK + "A-open__7240841.mp4", t=1.2, fx=0.42),      # "you see that feedback like, be careful today, take it easy": a groggy man still in bed. Covers Dan's head tilt here, which swings 774 px (wider than any steady 724 crop: reviewer, 0:47.9)
       dict(id="raises", a="o51.30", b="o57.0", src=STOCK + "A-end__B0450.mp4", t=0.3, fx=0.5)],          # "Go harder today ... low risk workouts": Dan's lateral raises (B0450), to the end
 "H": [dict(id="tunnel", a="o0.0", b="o4.40", src=STOCK + "H-open__31196473.mp4", t=0.0, fx=0.5),       # first 5 s: night driving, light streaks ("spiking your heart rate and your adrenaline")
       dict(id="pillow", a="o4.40", b="o8.15", src=STOCK + "H-toss__B0354.mp4", t=2.5, fx=0.45, eq=DARK),   # "could be affecting your sleep": library B0354, a man at 4:28 AM throwing his pillow (Pexels 6698753 was a montage: dissolves at 5.3-6.4 and from 9.2 s); covers his lower third 16:17.5-16:22.9 whole
       dict(id="highway", a="o25.19", b="o29.00", src=STOCK + "H2__31720444.mp4", t=1.0, fx=0.5, eq="eq=gamma=1.5:saturation=1.1"),   # from his cut at 15:45.4: "nobody on the road ... have fun": a deserted highway from the driver's seat (reviewer H: the busy Tokyo street contradicted "nobody on the road")
       dict(id="streaks", a="o29.00", b="o34.40", src=STOCK + "H2__28924398.mp4", t=2.4, fx=0.5),       # "whipping it around, going 120": a night-highway time-lapse, no other car, no speed number (reviewer H: the Subaru WRX was an identifiable other car). Runs to 34.40, past Dan's lean out of the crop at 33.8-34.4 (reviewer H)
       dict(id="toss", a="o36.20", b="o40.60", src=STOCK + "H-toss__8376628.mp4", t=12.0, fx=0.5, rot=180, eq=DARK),   # "severely disrupting my sleep"; ends on "Now I just press a button"
       dict(id="tesla", a="o40.60", b="o49.60", src=MASTER, t=963.65, fx=0.30),                          # his real Tesla Full Self-Driving footage from "press a button" (reviewer H); fx 0.30 keeps the wheel and leaves the screen's speed digits out of the crop
       dict(id="sleep", a="o49.60", b="o52.79", src=STOCK + "I-end__B0333.mp4", t=2.6, fx=0.55)],        # "wound down for bed and my sleep has gotten a lot better": library B0333, a man sleeping peacefully; covers his white flash at 16:13.0
 "I": [dict(id="argue", a="o0.0", b="o5.60", src=STOCK + "I-open__8557555.mp4", t=0.0, fx=0.5),          # first 5 s: a couple arguing ("toxic")
       dict(id="alone", a="o7.65", b="o12.14", src=STOCK + "I-alone__7698608.mp4", t=2.0, fx=0.5, eq=DARK),  # "bad relationships in the past"; covers his lower third 16:37.2-16:41.3 to his cut
       dict(id="stress", a="o14.40", b="o18.847", src=STOCK + "I-stress__B0535.mp4", t=4.5, fx=0.5),      # "a couple of weeks of arguments, I'm stressed out"
       dict(id="chart", a="o18.847", b="o29.126", hf=HF + "I_chart.mov"),                                 # our moving sleep-score scene (Dan's real chart from Zeeshan's card)
       dict(id="awake", a="o29.126", b="o35.80", src=STOCK + "I-awake__6943535.mp4", t=28.0, fx=0.5, eq=DARK),   # "killing me by disrupting my sleep"; covers his white flash
       dict(id="door", a="o52.45", b="o55.29", src=STOCK + "I-end__7986201.mp4", t=12.8, fx=0.5)],         # "or they need to go": a door closes; covers his whip transition at the end
 "J": [dict(id="app", a="o0.0", b="o3.70", t=420.5, **APP),                                                 # first 5 s: Dan's real Oura app ("Should you buy the Oura Ring?")
       dict(id="watch", a="o11.15", b="o13.80", src=STOCK + "J-watch__8027978.mp4", t=5.4, fx=0.5, eq=DARK),  # "Apple Watch, Fitbit, not recommended"
       dict(id="compare", a="o20.603", b="o46.30", hf=HF + "J_compare.mov")],      # runs to the end: Zeeshan's zoom into his outro starts under "the cost is low" (reviewer J)                            # our moving comparison (his two advantage lists)
 "K": [dict(id="yawn", a="o0.0", b="o4.30", src=STOCK + "K-open__4588464.mp4", t=1.5, fx=0.5, eq="eq=gamma=1.15:saturation=1.04"),          # first 5 s: an underslept man yawning ("you are in denial"); ends on "ago," (reviewer K D6). Pexels 8134383 is out: from 4.5 s its own frame cuts the back of his head (reviewer K D3)
       dict(id="scale", a="o16.00", b="o19.60", src=STOCK + "K-scale__7802051.mp4", t=5.6, fx=0.5),      # "never weighing yourself to weighing yourself every day"; covers his lower third 3:32.8-3:37.7
       dict(id="app", a="o19.60", b="o25.45", t=420.0, hl=dict(box=[0, 433, 320, 474], on=20.05), **APP),        # "see the problem ... the specific things that are triggering": Dan's real Oura sleep screen (one still screenshot, 7:19.3-7:26.4 of the film), a pulsing outline on its one flagged row "Restfulness: Fair" from "the problem" (reviewer K D1: the later screens said "great day" and "93 Optimal" over "the problem")
       dict(id="drink", a="o25.45", b="o28.30", src=STOCK + "K-drink__7944546.mp4", t=1.6, fx=0.5, eq=DARK),
       dict(id="late", a="o28.30", b="o29.70", src=STOCK + "K-late__30205992.mp4", t=3.85, fx=0.5, eq=DARK),      # from 3.85 s: before it a food bag blurs the lens (reviewer K D4)
       dict(id="stress", a="o29.70", b="o33.00", src=STOCK + "I-stress__B0535.mp4", t=0.8, fx=0.5)],     # to his cut at 3:48.0. B0535's first seconds (head down on the desk); short I uses its later hands-on-head part. B0494 is out: its actor reads as Dan at a glance
}
SPLIT = {}
SHOTS = {"A": {}, "H": {}, "I": {}, "J": {}, "K": {}}
SHOTS_AT = {                       # per talking shot, keyed by a master time inside it
 "I": [(1056.4, dict(win="mid"))],
 "H": [(935.0, dict(win="mid"))],                                   # his same-size cut at 15:30.93 gets a real size step (reviewer H, 0:10.68)                                  # piece 2 opens on the same medium framing piece 1 ended on: a real size step (1.2x)
 "J": [(1075.0, dict(cx=1014)), (1084.0, dict(cx=1014)), (1111.0, dict(cx=1014)),     # his verdict card sits at x 60-626 from 17:50.6: the window starts at x 652
       (1112.5, dict(win="mid", cx=1014))],                          # his own same-framing cut at 18:31.6 gets a real size step
}
BARS = {
 "A": [dict(id="G1", topic="Key Point", parts=[["Bad Sleep Is No Reason", "this is exactly"], ["To Slack Off In The Gym", "In my opinion, you"]], a=-0.2, b=2.0)],
 "H": [dict(id="G1", topic="Key Point", parts=[["Late-Night Adrenaline", "late night adrenaline"], ["Wrecks Your Sleep", "severely disrupting"]], a=-0.2, b=1.9)],      # ends before the Tesla footage,
 "I": [dict(id="G1", topic="Key Point", parts=[["Someone Wrecks Your Sleep?", "And if you find"], ["They Have To Go", "has got to go"]], a=-0.2, b=2.5)],
 "J": [],
 "K": [dict(id="G1", topic="Key Point", parts=[["Track It To See What's", "You'll see how"], ["Wrecking Your Sleep", "when you drink"]], a=-0.05, b=4.0)],      # a=-0.05: starts after the cut from the phone (reviewer K D5),
}
TEXT = {
 "A": "The Oura Ring, when you get a bad night of sleep, it gives you advice like, better be careful today, better not do a hard workout today. In my opinion, though, this is exactly the wrong advice. In my opinion, you don't need to back off your workouts or be careful if you get a night of bad sleep. In fact, I think you should be making a conscious effort to work out harder. Now, the rationale behind this is that when you are less rested, then your odds of getting injured with a hard workout do increase if you're doing the wrong type of workout. So I would say, yeah, you should take it easy on the deadlifts and the power cleans and those kind of high risk moves. But if you're training in the low risk way we recommend, then your risk of injury is going to be zero, even if you're totally sleep deprived. So I would say if you do get a bad night of sleep and you see that feedback like, be careful today, take it easy. Don't listen to that shit. Go harder today if you get a bad night of sleep and just make sure you're doing low risk workouts so that way you don't get injured.",
 "H": "There might be something that you're doing that's spiking your heart rate and your adrenaline in your bedtime that you don't really expect right now could be affecting your sleep. | Driving fast late at night near bedtime. Now, I used to have a girlfriend where she wasn't able to sleep over my house and I had to drop her off late at night. So I'd be dropping her off at like 11,{eleven} 11:30,{eleven thirty} and I drive a Tesla Model 3{three} Performance. So, when it's late at night, there's nobody on the road, the chance of getting a ticket were pretty minimal, and I'd use that time to have fun. I was whipping it around, I was going 120,{a hundred twenty} I was really enjoying my car late at night. However, when I got the Oura Ring, I found out that type of late night adrenaline filled driving was severely disrupting my sleep. Now I just press a button, put it in Full{full} Self-Driving{self driving} so the car drives me home. Sometimes I even close my eyes as I'm driving home. I try to relax, listen to a boring podcast to kind of get myself wound down for bed and my sleep has gotten a lot better as a result of cutting out that fast driving.",
 "I": "Here was the most valuable and the most unexpected benefit of getting an Oura Ring for me. It showed me which people in my life are toxic and which I need to cut out of my life. Now I've been in some bad relationships in the past. So things started going downhill, you know, a couple of weeks of arguments, I'm stressed out all the time, and my sleep score goes off a cliff. It was just really one of the worst all-time{all time} sleep scores I had since getting the Oura Ring. I ended up breaking up with that girl. I didn't realize that being with this girl, the stress of that was literally killing me by disrupting my sleep. And if someone is disrupting your sleep, then you're gonna be conscious of that with the Oura Ring. And if you find someone who's disrupting your sleep, that person has got to go. They are literally killing you if they're disrupting your sleep. | These type of things, you underestimate how much they affect you, but once you have the data, you'll realize certain people in your life either need to change their behavior or they need to go.",
 "J": "Should you buy the Oura Ring? In my opinion, yes for most people. Now, should you buy a sleep tracker? Absolutely, everybody needs a sleep tracker. Which one is the best? It's a matter of preference. Apple Watch, Fitbit, not recommended. Oura Ring and WHOOP{whoop} are my top two options. Just more depends whether you prefer a wrist-based{wrist based} or a finger-based{finger based} sleep tracker. Advantages of Oura Ring over WHOOP.{whoop} More accuracy. It's on your finger, so that's a better location. Better app. More actionable insights that you are actually going to use. Advantages of the WHOOP,{whoop} better for workout tracking, more comfortable when you're grasping things or typing. Some people prefer a wrist-based{wrist based} sleep tracker that you can also move around. And for some people, there's no subscription and the cost is low.",
 "K": "You watching this video right now are probably where I was at a few years ago, which is to say you are in denial. You think you're sleeping okay. You think you're getting enough sleep, but you probably are not if you're like the average person. If you got the sleep tracker, this would be like going from never weighing yourself to weighing yourself every day. You would see the problem. Even more than that, you're going to see the specific things that are triggering this problem. You'll see how it affects your REM{rem} sleep when you drink alcohol, or when you eat late at night, or when you get stressed out, or when this or that thing happens. You're going to be surprised at some of these things that you see, and you're going to be able to make adjustments based on the data. So I can't stress this enough, you've got to buy a sleep tracker, even if it is not the Oura Ring.",
}
