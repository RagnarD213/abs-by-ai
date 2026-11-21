"""RO-29 visual plan ("Cortisol Belly Is Real, But TikTok Has It Wrong", 10/15 rolls C1772 + recap retake C1773). Every item is
anchored to the words Dan says (phrase -> output time via words_out.json). Graphics are HyperFrames only (VIDEO-RULES 2026-10-17):
lt (Motivation lower third), scene "fact" (before-card), l3 (the 3A left card). Clips: Dan's real 10/15 pool B-roll first (grades and
crops Dan approved in RO-28), then the clip library, then Pexels. kind "ai" = a new AI clip whose START/END frames go to Dan in round 1;
until its motion is approved the presenter stays on screen. kind "phone" = the iPhone card beside Dan (the TikTok trend clip).
Organic, not entirely about the drug: Zepbound is SAID, on-screen graphics say "Appetite Medication" (the script's own cue).
Title case; eyebrows in capitals (VIDEO-RULES 2026-10-20)."""
W = "/Volumes/Expansion/_edit_work/RO-29/round2"
ST = f"{W}/stock"; PH = f"{W}/stock/photos"; TK = f"{W}/stock/tiktok"
RD = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop"
POOL = "eq=contrast=1.04:brightness=-0.02:saturation=1.12"                         # RO-28 C01/C05/C12 (approved film)
POOL_SHADE2 = "curves=master='0/0 0.1/0.09 0.4/0.45 0.75/0.82 1/1',eq=saturation=0.90,colorbalance=rs=.015:bs=-.015"   # RO-28 C16
AI = "AI-GENERATED"
PLAN = [
 # ---------------- opening
 dict(id="A0", kind="ai", start="Cortisol belly is real", end="TikTok fixes", tail=0.0, name="The clickbait TikTok",
      note="R2 (Dan): close on his fat hand holding the phone, a ridiculous clickbait cortisol belly cocktail TikTok playing; he sets the phone down, still visible"),
 dict(id="A1", kind="ai", start="for it like the cortisol", end="off your waist", tail=0.45, name="The cocktail bartender",
      note="R2 (Dan): same phone on the island; he shakes the cocktail he just watched and ends triumphant and stupid"),
 dict(id="G01", kind="lt", topic_case="preserve", start="In today's video", end="get rid of it", tail=0.8, topic="IN THIS VIDEO", over_full=True,
      point="What Cortisol Does + 6 Real Fixes", parts=[["What Cortisol Does", "what cortisol does"], ["+ 6 Real Fixes", "six things"]]),
 dict(id="C01", kind="clip", start="If you've been told", end="hear this", tail=0.3, src=["B0494@0.5"],
      note="library B0494: a stressed office man rubs his face at his desk"),
 dict(id="G02", kind="lt", topic_case="preserve", start="So let's start with what TikTok", end="gets right", tail=0.8, topic="PART 1",
      point="What TikTok Gets Right", parts=[["What TikTok Gets Right", "what TikTok"]]),
 dict(id="F01", kind="scene", scene="fact", start="In a Yale study, women", end="without it", tail=0.6, photo=f"{PH}/p5717262.jpg",
      eyebrow=["Yale Study, 2000", "Yale study"], headline=[["More Cortisol", "release more cortisol"]],
      detail=["Women With More Belly Fat", "more belly fat"], note="Pexels 5717262: a woman stressed at her office desk. Epel et al., Yale, 2000 (script cue)"),
 dict(id="P01", kind="phone", start="But then TikTok tells you", end="is a drink", tail=0.4, src=[f"{TK}/ebbymoyer_7260977070203931950.mp4@4.0"], credit="@ebbymoyer on TikTok",
      note="The viral 'adrenal cocktail' TikTok from the script (@ebbymoyer, 3.5M views): she makes the drink. Muted under Dan's line"),
 # ---------------- what TikTok gets wrong
 dict(id="G03", kind="lt", topic_case="preserve", start="Here's what TikTok gets wrong", end="gets wrong", tail=0.8, topic="PART 2",
      point="What TikTok Gets Wrong", parts=[["What TikTok Gets Wrong", "what TikTok"]]),
 dict(id="G04", kind="lt", topic_case="preserve", start="Stress makes you eat more", end="on your belly", tail=0.5, topic="KEY POINT",
      point="Stress Raises Your Appetite", parts=[["Stress Raises Your Appetite", "makes you eat more"]]),   # independent check: the old copy echoed the line
 dict(id="A1B", kind="ai", start="Let's say you were in a calorie deficit", end="get leaner", tail=0.5, name="Fasting and grinding at the desk",
      note="R2 (Dan): AI Dan, wrecked at the computer, nothing but coffee, the clock spins from morning to night"),
 dict(id="A2", kind="ai", start="let's say you were eating in a calorie surplus", end="gain weight", tail=0.25, name="Zen and mellow, still gaining",
      note="AI gag: a heavyset man meditating, eyes closed and blissful, surrounded by pizza boxes and donuts, calmly takes a slice"),
 dict(id="C03", kind="clip", start="The problem is that in real life", end="has been proven", tail=0.25, src=["A0182@0.3"], label=AI, max_len=4.8,
      note="library A0182 (AI, RO-17): a heavy man in a grey hoodie on the sofa at night, eating from a bag of snacks without looking (A0145 was shirtless, belly centred: independent check)"),
 dict(id="F02", kind="scene", scene="fact", start="In another Yale study", end="stayed calm", tail=0.5, photo=f"{PH}/p6633205.jpg",
      eyebrow=["Yale Study, 2001", "another Yale study"], headline=[["More Calories", "ate more calories"]],
      detail=["After A Stressful Day", "stressful day"], note="Pexels 6633205: a woman eating chocolate cake on her couch. Epel et al., Yale, 2001 (script cue)"),
 dict(id="A3", kind="ai", start="On a calm day", end="more sweets", tail=0.3, name="Straight to the candy jar",
      note="AI: a frazzled office worker leaves a tense meeting and plunges his hand into the office candy jar"),
 dict(id="G05", kind="lt", topic_case="preserve", start="So the stress isn't putting fat", end="because you're stressed", tail=0.33, topic="KEY POINT",
      point="It's The Extra Food, Not The Stress", parts=[["It's The Extra Food, Not The Stress", "extra food"]]),   # one part so it reads 1.5 s before L01 (independent check)
 dict(id="L01", kind="l3", start="If you're under massive stress", end="will gain fat", tail=0.4, heading="The Real Rule",
      points=["Stressed + Deficit: Leaner", "Calm + Surplus: Fatter"], reveal=["under massive stress", "zero stress"],
      note="the script's 'STRESSED + CALORIE DEFICIT = LEANER / CALM + CALORIE SURPLUS = FATTER' graphic, on the line that sums it up"),
 # ---------------- the cocktail
 dict(id="C04", kind="clip", start="Now, let's look at what's actually", end="cortisol cocktail", tail=0.15, src=[f"{ST}/p6739355.mp4@1.0"],
      note="Pexels 6739355: orange juice poured into a glass"),
 dict(id="L02", kind="l3", start="It's orange juice", end="most of that is sugar", tail=0.4, heading="The Cocktail",
      points=["Orange Juice", "Coconut Water", "Salt", "About 80 Calories"], reveal=["orange juice", "coconut water", "salt", "80 calories"],
      note="the script's 'THE CORTISOL COCKTAIL' ingredient graphic"),
 dict(id="P02", kind="phone", start="And sucking down a sugar drink", end="cortisol either", tail=0.25, src=[f"{TK}/jezebel511_7525072235103554846.mp4@44.5"], credit="@jezebel511 on TikTok",
      note="the backup TikTok from the script (@jezebel511, 'Cortisol Cocktail'): her counter of juice and powders"),
 dict(id="G06", kind="lt", topic_case="preserve", start="So skip the cortisol cocktail", end="waste of money", tail=0.6, topic="ACTION STEP", over_full=True,
      point="Skip The Cocktail And The Supplements", parts=[["Skip The Cocktail", "skip the cortisol"], ["And The Supplements", "adrenal supplements"]]),   # the script's ON SCREEN cue sits on this line (independent check: it had landed on "what actually fixes")
 # ---------------- fix 1: sleep
 dict(id="G07", kind="lt", topic_case="preserve", start="the first one is sleep", end="is sleep", tail=1.9, topic="FIX 1 OF 6", over_full=True,
      point="Sleep", parts=[["Sleep", "sleep"]]),
 dict(id="C06", kind="clip", start="When you don't sleep", end="worse food choices", tail=0.25, src=[f"{ST}/p6944070.mp4@3.0"], grade="eq=brightness=0.06:contrast=1.03:saturation=0.68,colorbalance=rs=-0.05:gs=0.01:bs=0.05:rm=-0.04:bm=0.03",
      note="Pexels 6944070: a young man tossing and turning in bed at night"),
 dict(id="F03", kind="scene", scene="fact", start="In a University of Chicago study", end="same diet", tail=0.6, photo=f"{PH}/p6029065.jpg",
      eyebrow=["Sleep Study, 2010", "University of Chicago"], headline=[["55% Less Fat Lost", "55"]], count={"value": "55", "from": 0, "dur": 0.6},
      detail=["Short Sleep, Same Diet", "exact same diet"], note="Pexels 6029065: a woman awake in bed, exhausted, laptop beside her (the man-asleep photo repeated C08). Nedeltcheva et al., Annals of Internal Medicine, 2010 (5.5 h vs 8.5 h; the card names no hours)"),
 dict(id="C07", kind="clip", start="So get at least seven hours", end="cold room", tail=0.3, src=[f"{ST}/p39857556.mp4@6.3"], crop=(2560, 1440, 700, 520),
      note="Pexels 39857556: a finger scrolls a wall thermostat down from 73 to 68 degrees Fahrenheit, no readable brand (the GREE Celsius clip carried a logo)"),
 dict(id="G08", kind="lt", topic_case="preserve", start="So get at least seven hours", end="cold room", tail=1.4, topic="ACTION STEP",
      point="7+ Hours A Night, In A Cold Room", parts=[["7+ Hours A Night,", "seven hours"], ["In A Cold Room", "cold room"]], over_full=True),
 dict(id="C08", kind="clip", start="When you sleep well", end="the next day", tail=0.3, src=[f"{ST}/p5983694.mp4@1.0"],
      note="Pexels 5983694: a man sleeping soundly"),
 # ---------------- fix 2: train
 dict(id="G09", kind="lt", topic_case="preserve", start="The second thing is to train", end="every day", tail=1.9, topic="FIX 2 OF 6", over_full=True,
      point="Train Every Day", parts=[["Train Every Day", "train every day"]]),
 dict(id="C09", kind="clip", start="Training is one of the best ways there is", end="burn off stress", tail=0.25, src=[f"{RD}/C1746.MP4@2.5"], grade=POOL, crop=(2880, 1620, 320, 0),
      note="Dan's real B-roll (10/15 pool, roll C1746): dumbbell curls"),
 dict(id="G10", kind="lt", topic_case="preserve", start="I work out first thing", end="seven days a week", tail=1.6, topic="WHAT I DO",
      point="First Thing Every Morning, 7 Days A Week", parts=[["First Thing Every Morning,", "first thing"], ["7 Days A Week", "seven days"]]),
 dict(id="C10", kind="clip", start="Because of that, I ate less junk", end="fewer calories", tail=0.25, src=[f"{RD}/C1744.MP4@2.5"], grade=POOL, crop=(2880, 1620, 612, 500),
      note="Dan's real B-roll (roll C1744): push-ups on handles"),
 dict(id="C11", kind="clip", start="That's why I train first thing", end="you should too", tail=0.25, src=[f"{RD}/C1750.MP4@6.5"], grade=POOL, crop=(3456, 1944, 72, 60),
      note="Dan's real B-roll (roll C1750): kettlebell deadlift into goblet squats"),
 # ---------------- fix 3: alcohol
 dict(id="G11", kind="lt", topic_case="preserve", start="Here's the third one", end="on alcohol", tail=1.4, topic="FIX 3 OF 6", over_full=True,
      point="Cut Way Back On Alcohol", parts=[["Cut Way Back On Alcohol", "cut way back"]]),
 dict(id="C12", kind="clip", start="A lot of guys drink", end="deal with stress", tail=0.25, src=[f"{ST}/p8057697.mp4@1.0"],
      note="Pexels 8057697: a man drinking alone in his bedroom"),
 dict(id="C13", kind="clip", start="but alcohol wrecks your sleep", end="two different ways", tail=0.25, src=["A0174@0.6"], label=AI, max_len=5.3,
      note="library A0174 (AI, RO-08): one sip of beer and a man slides off his bar stool"),
 # ---------------- fix 4: Zepbound
 dict(id="G12", kind="lt", topic_case="preserve", start="The fourth thing is", end="stress eating too", tail=0.6, topic="FIX 4 OF 6",
      point="Appetite Medication (Talk To Your Doctor)", parts=[["Appetite Medication", "fourth thing"], ["(Talk To Your Doctor)", "turns down your appetite"]]),
 dict(id="C14", kind="clip", start="made eating less far easier", end="every week", tail=0.25, src=[f"{ST}/p5998399.mp4@1.0"],
      note="Pexels 5998399: a syringe and vials on a table (used in RO-28)"),
 # ---------------- fix 5: stressful relationships
 dict(id="G13", kind="lt", topic_case="preserve", start="Number five is the one", end="stressful relationships", tail=0.8, topic="FIX 5 OF 6",
      point="Quit Your Stressful Relationships", parts=[["Quit Your Stressful Relationships", "quit your"]]),
 dict(id="A4D", kind="ai", start="If your wife stresses you out", end="Divorce her", tail=0.95, name="The divorce papers",
      note="R3 (Dan): a ripped husband presents his average-looking wife with divorce papers"),
 dict(id="A5", kind="ai", start="stresses you out all the time quit", end="quit", tail=2.25, name="Quitting the stressful job",
      note="R2 (Dan): badge already on the desk; box in his arms, he visibly mouths I quit to the boss, then walks out"),
 dict(id="A6", kind="ai", start="oh Dan that's crazy", end="stresses me out", tail=0.03, name="The husband who can't",
      note="AI, excuse voice: a man on the couch protests to the camera while his wife glares at him (lip-synced to Dan's line if the sync passes; otherwise mouth closed)"),
 dict(id="G13B", kind="lt", topic_case="preserve", start="Is it worth killing yourself", end="regardless of what other value", tail=0.6, topic="ASK YOURSELF",
      point="Is It Worth Killing Yourself For This?", parts=[["Is It Worth Killing Yourself For This?", "worth killing"]]),
 dict(id="G14", kind="lt", topic_case="preserve", start="You'll find that if you have zero tolerance", end="refuse to change", tail=0.3, topic="KEY POINT",
      point="Zero Tolerance For Stress", parts=[["Zero Tolerance For Stress", "zero tolerance"]]),
 # ---------------- fix 6: no stress eating
 dict(id="G15", kind="lt", topic_case="preserve", start="And here's the sixth thing", end="excuse to overeat", tail=0.9, topic="FIX 6 OF 6",
      point="Don't Use Stress As An Excuse To Overeat", parts=[["Don't Use Stress", "Don't use"], ["As An Excuse To Overeat", "excuse"]]),
 dict(id="A7", kind="ai", start="Even if you had a bad day", end="hit your calories", tail=0.3, name="Weighing the chicken after a fight",
      note="AI (frames v2 after the independent check): his girlfriend shouts and points at him, he calmly sets his chicken on the scale; she storms off"),
 dict(id="C15", kind="clip", start="You should have a routine", end="feel great or terrible", tail=0.25, src=["A0082@1.2"], label=AI,
      note="library A0082 (AI): a man portions chicken, rice and vegetables into five meal-prep containers"),
 dict(id="G16", kind="lt", topic_case="preserve", start="you also need the discipline", end="can't avoid it", tail=0.6, topic="KEY POINT",
      point="Stick To The Plan On Bad Days", parts=[["Stick To The Plan On Bad Days", "discipline"]]),   # independent check: the old copy echoed the line
 # ---------------- recap (C1773)
 dict(id="L03", kind="l3", start="One, sleep", end="back on alcohol", tail=0.3, heading="The 6 Fixes",
      points=["Sleep 7+ Hours, Cold Room", "Train First Thing Daily", "Cut Way Back On Alcohol"], reveal=["sleep", "train every day", "cut way back"]),
 dict(id="L04", kind="l3", start="Four, talk to your doctor", end="how you feel", tail=0.3, heading="The 6 Fixes", first=4,
      points=["Appetite Meds (Ask A Doctor)", "Cut Out Stressful People", "Hit Calories And Protein Daily"], reveal=["talk to your doctor", "get the chronically", "hit your calories"]),
 dict(id="G18", kind="lt", topic_case="preserve", start="Pick the one", end="this week", tail=0.6, topic="ACTION STEP",
      point="Fix Your Worst One This Week", parts=[["Fix Your Worst One This Week", "pick the one"]]),
 dict(id="C16", kind="clip", start="Thank you for watching", end="subscribe for more", tail=0.25, src=[f"{RD}/C1743.MP4@2.5"], grade=POOL_SHADE2, crop=(3200, 1800, 0, 200),
      note="Dan's real B-roll (roll C1743): kettlebell deadlifts"),
 dict(id="G19", kind="lt", topic_case="preserve", start="If you enjoyed this video", end="published", tail=0.6, topic="SUBSCRIBE",
      point="New Videos First At SixPackAbs.com", parts=[["New Videos First", "subscribe"], ["At SixPackAbs.com", "go to"]]),
]
from grades import GR     # RO-29 R2: Dan, every B-roll clip colour corrected
for _it in PLAN:
    if _it["id"] in GR: _it["grade"] = GR[_it["id"]]
# RO-29 R2: the AI slots now hold their finished, retimed, colour-corrected takes (ai/final.py)
_LEFT = {"A1B", "A5", "A4D"}    # chip clear of the wall clock and of his hair
for _it in PLAN:
    if _it["kind"] == "ai":
        _it["kind"] = "clip"; _it["src"] = [f"{W}/ai/final/{_it['id']}.mp4@0.0"]; _it["label"] = AI
        if _it["id"] in _LEFT: _it["chip"] = ((54, 54), "lt")
    if _it["id"] == "C13": _it["chip"] = ((54, 54), "lt")    # the top-right chip sat on the bartender's face
