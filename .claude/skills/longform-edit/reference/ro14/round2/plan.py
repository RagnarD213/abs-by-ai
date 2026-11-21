"""RO-14 visual plan ("Why You're Not Losing Weight", 9/23 roll C1708). Every item is anchored to the words Dan says
(phrase -> output time via words_out.json). Kinds from the approved HyperFrames templates (hyperframes/from_plan.py): lt (Motivation
lower third, parts land on their words), scene/fact (photo + glass fact card), l3 (3A side list, items land on their words).
Kinds that stay softblue.py (gfx.py): title (section card with a picture on the right, RO-11 layout "bleed"), scene/photo (one real
photo), scene/study (bars), scene/week (RO-14: the weekday deficit erased by the weekend), scene/chart (daily weigh-ins vs the 7-day
average, RO-16), scene/recap (numbered list, items land on their words). clip = full-frame cutaway (Pexels / clip library), hard cuts.
phone = the approved iPhone shell beside Dan. ai = an AI clip slot: labelled START/END placeholder frames until Dan approves the
frames and the motion exists. start = phrase whose first word starts the item; end = phrase whose last word ends it (or dur);
end_at_start = end on the FIRST word of the end phrase (a montage cut lands on the next named thing).
Capitals: title case by default; FULL CAPS on a word only where it carries the punch (VIDEO-RULES 2026-10-09, about 1 in 6)."""
ST = "/Volumes/Extreme/_edit_work/RO-14/round1/stock"
PH = "/Volumes/Extreme/_edit_work/RO-14/round1/assets/photos"
TP = "/Volumes/Extreme/_edit_work/RO-14/round1/assets/titles"
BEFORE = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/before-photo-candidates/B_deckchair_UPSCALED_3x_1080x1440.jpg"
REAL = "Real Photo Of Me, Not AI-Generated"          # Dan 2026-10-17 wording (VIDEO-RULES), title case in a graphic
AI = "AI-GENERATED"
# round 2: the seven approved AI clips (Veo 3.1 Fast in Flow from the approved START/END frames, Dan 2026-10-20 "it is good to
# generate all of them"); window per clip in round2/motion/windows.json (24 fps frame A -> seconds); the takes have a dark 2-3 px
# strip on the right edge: a 0.4 % crop removes it
VEO = "/Volumes/Extreme/_edit_work/RO-14/round2/veo"
import json as _json
_WIN = _json.load(open("/Volumes/Extreme/_edit_work/RO-14/round2/motion/windows.json"))
VEOCROP = "crop=1912:1076:3:2,scale=1920:1080"
def ai_clip(k, **kw):
    """an approved AI slot as a full-frame clip: its take from the window's first frame, AI-GENERATED chip where the slot had it"""
    wn = _WIN[k]; d = dict(kw, kind="clip", src=[f"{VEO}/{wn['take']}@{wn['frames'][0]/24:.4f}"], label=AI, grade=VEOCROP, ai_take=k)
    if wn.get("partial"):     # only the clean part of a take (reviewer-named window); Dan stays on camera for the rest of the line
        d.update(start_t=wn["start_t"], max_len=round((wn["frames"][1] - wn["frames"][0] + 1) / 24 - 0.01, 3))
    return d
GREY = (150, 170, 190); RED = (235, 64, 64)
PLAN = [
 # ---------------- opening (0:00 - 0:30)
 ai_clip("A1", id="A1", chip=((54, 54), "lt"), start="You are eating healthy", end="will not move", tail=0.15, name="The broken scale",
      note="AI opener: a man in gym clothes steps on the bathroom scale, looks down, then picks it up and shakes it like it must be broken"),
 dict(id="G01", kind="lt", start="It is almost certainly not", end="not your genetics", tail=1.2, topic="The Real Reason",
      point="Not Metabolism. Not Hormones. Not Genetics.", parts=[["Not Metabolism.", "metabolism"], ["Not Hormones.", "hormones"], ["Not Genetics.", "genetics"]]),
 dict(id="G02", kind="scene", scene="recap", start="the four ways", start_t=16.206, end="fixes all of it", tail=0.3,
      eyebrow="IN THIS VIDEO", headline="Why The Scale Won't Move",
      items=["4 calorie leaks", "The hidden reasons", "The system that fixes it"], reveal_items=["four ways", "hidden reasons", "simple system"], photo=f"{TP}/G02",
      note="round 2: starts on the 10/15 pickup ('four hidden reasons', recipe/pickup.py, film 16.62-26.06) so the new line is never on Dan's face"),
 # ---------------- part 1: the uncomfortable truth (0:30 - 1:07)
 dict(id="T1", kind="title", start="For 80", dur=2.4, step="PART 1 OF 4", headline="The Uncomfortable\nTruth", photo=f"{TP}/T1", layout="bleed"),
 dict(id="G03", kind="lt", start="the reason why is simple", end="this over and over", tail=0.2, topic="For Most Dieters",
      point="Too Many Calories, Without Realizing It", parts=[["Too Many Calories,", "too many calories"], ["Without Realizing It", "without realizing"]]),
 dict(id="G04", kind="scene", scene="study", start="People underestimate", end="40 % or more", tail=0.5,
      eyebrow="NEW ENGLAND JOURNAL OF MEDICINE, 1992", headline="They Ate About Twice\nWhat They Reported",
      bars=[["What they said they ate", 1028, GREY, "1,028 cal a day"], ["What they actually ate", 2081, RED, "2,081 cal a day"]],
      detail="Lichtman et al. Dieters who said they could not lose weight on under 1,200 calories a day. They under-reported by 47%.",
      note="real study (NEJM 1992;327:1893); supports 'sometimes by 40 % or more'"),
 dict(id="C01", kind="clip", start="Untracked eating is invisible", end="doing it", src=[f"{ST}/p5970707.mp4@2.0"],
      note="Pexels 5970707: a man at his desk eats a snack from a bowl without looking away from the screen"),
 dict(id="P01", kind="scene", scene="photo", photo=BEFORE, start="I was 200 pounds", end="ate pretty well", tail=0.3, label=REAL,
      note="the standard before picture (deck chair by the pool, heavier), real, labelled"),
 # ---------------- part 2: the four leaks (1:07 - 3:23)
 dict(id="T2", kind="title", start="There are four leaks", dur=2.4, step="PART 2 OF 4", headline="4 Calorie\nLeaks", photo=f"{TP}/T2", layout="bleed"),
 dict(id="G05", kind="lt", start="Leak number one", end="tracking your calories", topic="Leak #1",
      point="You're Not Tracking Calories", parts=[["You're Not Tracking Calories", "Leak number one"]]),
 dict(id="C02", kind="clip", start="Eyeballing your portions", end="almost everybody", src=[f"{ST}/p28099100.mp4@0.3"],
      note="Pexels 28099100: food piled onto a plate at a buffet, no measuring"),
 dict(id="C03", kind="clip", start="on a scale", end="normal guys", end_at_start=True, max_len=3.06, src=["A0050@0.0"], label=AI,
      note="library A0050 (AI): a man weighs his plate on a kitchen scale and types it into his phone"),
 dict(id="C04", kind="clip", start="normal guys with jobs", end="going to do that", src=[f"{ST}/p3192261.mp4@3.0"],
      note="Pexels 3192261: a dad getting two kids ready for school in a busy kitchen"),
 dict(id="P02", kind="phone", start="With AI, you take a photo", end="two seconds", src=["B0035"],
      note="library B0035 (real app screen recording): a photo of a chicken-and-broccoli plate, Analyze Meal, 363 calories itemized"),
 dict(id="G07", kind="lt", start="Leak number two", end="Weekend blowouts", topic="Leak #2", point="Weekend Blowouts",
      parts=[["Weekend Blowouts", "Leak number two"]]),
 dict(id="G08", kind="scene", scene="week", start="5 disciplined weekdays", end="erases all of it", tail=0.4,
      eyebrow="ONE WEEK OF DIETING", headline="5 Good Days. 1 Weekend. Back To Zero.",
      days=[["MON", -500], ["TUE", -500], ["WED", -500], ["THU", -500], ["FRI", -500], ["FRI NIGHT", 1500], ["SAT", 1000]],
      reveal_days=["5", "disciplined", "weekdays", "build", "deficit", "Friday dinner", "lazy Saturday"],
      note="each bar lands on its word; the running total counts to -2,500 then back to 0 on 'erases all of it'"),
 dict(id="C05", kind="clip", start="This is why Monday to Friday", end="for years", src=[f"{ST}/p7555158.mp4@0.2"],
      note="Pexels 7555158: bare feet step onto a glass bathroom scale"),
 dict(id="G09", kind="lt", start="They are not failing", end="averaging out to zero", topic="Key Point",
      point="Not Failing. Averaging Out To ZERO.", parts=[["Not Failing.", "not failing"], ["Averaging Out To ZERO.", "averaging"]]),
 ai_clip("A3", id="A3", start="Every week they build", end="they spend it", tail=0.35, name="Smashing the piggy bank",
      note="AI gag: Friday night, a man in a party shirt smashes his piggy bank with a hammer, coins everywhere, pizza and beer beside it"),
 dict(id="G10", kind="lt", start="Leak number three", end="liquid calories", tail=0.1, topic="Leak #3", point="Liquid Calories",
      parts=[["Liquid Calories", "Leak number three"]]),
 dict(id="C06", kind="clip", start="The coffee drinks", end="the juice", end_at_start=True, src=[f"{ST}/p32272236.mp4@2.0"],
      note="Pexels 32272236: a sweet coffee drink piled with whipped cream"),
 dict(id="C07", kind="clip", start="the juice", end="the smoothies", end_at_start=True, src=[f"{ST}/p6739355.mp4@3.0"],
      note="Pexels 6739355: orange juice poured into a glass"),
 dict(id="C08", kind="clip", start="the smoothies", end="the protein shakes", end_at_start=True, src=[f"{ST}/p8492293.mp4@4.0"],
      note="Pexels 8492293: a pink smoothie in a blender"),
 dict(id="C09", kind="clip", start="the protein shakes", end="the alcohol", end_at_start=True, src=[f"{ST}/p4945360.mp4@31.0"],
      note="Pexels 4945360: a man drinks a protein shake from a shaker"),
 dict(id="C10", kind="clip", start="the alcohol", end="the alcohol", tail=0.35, src=[f"{ST}/p4752641.mp4@5.0"],
      note="Pexels 4752641: an amber pint with a foam head (replaces a cloudy beer in a plastic cup that read as juice)"),
 dict(id="G11", kind="lt", start="You know my rule", end="do not drink it", tail=1.0, topic="My Rule",
      point="If It Has Calories, Don't Drink It.", parts=[["If It Has Calories,", "if it has calories"], ["Don't Drink It.", "do not drink"]]),
 ai_clip("A7", id="A7", start="In some cases", end="calories don't matter", tail=0.25, name="The giant drink",
      note="AI gag: a man with a tiny side salad ignores it and blissfully sips a bucket-sized whipped-cream iced coffee"),
 dict(id="G13", kind="lt", start="Leak number four", end="invisible calories", tail=0.1, topic="Leak #4", point="Invisible Calories",
      parts=[["Invisible Calories", "Leak number four"]]),
 dict(id="C11", kind="clip", grade="eq=brightness=0.08:contrast=1.06:saturation=1.10:gamma=1.40", start="The cooking oil in the pan", end="the salad dressing", end_at_start=True, src=[f"{ST}/p4912636.mp4@1.0"],
      note="Pexels 4912636: olive oil poured into a frying pan"),
 dict(id="C12", kind="clip", grade="eq=brightness=0.04:contrast=1.04:saturation=1.05:gamma=1.15", start="the salad dressing", end="the sauces", end_at_start=True, src=[f"{ST}/p6162044.mp4@1.0"],
      note="Pexels 6162044: dressing poured over a salad as it is tossed (replaces a sauce poured into an empty bowl)"),
 dict(id="C13", kind="clip", grade="eq=brightness=0.03:contrast=1.04:gamma=1.12", start="the sauces", end="the bites", end_at_start=True, src=[f"{ST}/p5789851.mp4@0.5"],
      note="Pexels 5789851: sauce squeezed over dumplings"),
 ai_clip("A2", id="A2", start="the bites of your kids food", end="finishing the plate", tail=0.3, name="The trash-can nuggets",
      note="AI: a dad holds his kid's plate over the open trash can and eats the three leftover chicken nuggets instead"),
 dict(id="G15", kind="scene", scene="fact", start="A tablespoon of olive oil", end="nobody uses one tablespoon", photo=f"{PH}/px10420382.jpg",
      eyebrow=["1 TBSP OLIVE OIL", "tablespoon"], headline=[["120", "120"], ["Calories", "calories"]],
      count={"value": "120", "from": 0, "dur": 0.5}, detail=["And nobody uses just one.", "nobody"], push=1.06, drift=-8),
 dict(id="C14", kind="clip", start="You pour it straight", end="into the pan", src=[f"{ST}/p5593558.mp4@3.4"],
      note="Pexels 5593558: oil poured straight from the bottle into a cast iron pan"),
 dict(id="C15", kind="clip", start="in a meal you would describe", end="chicken and vegetables", src=[f"{ST}/p35637548.mp4@1.0"],
      note="Pexels 35637548: chicken, carrots and peppers cooking in a pot"),
 dict(id="G16", kind="lt", start="400 invisible calories", end="40 pounds in a year", topic="Invisible Calories",
      point="400 A Day = 40 Pounds A Year", parts=[["400 A Day", "400"], ["= 40 Pounds A Year", "40 pounds"]]),
 dict(id="G17", kind="lt", start="it is hiding in the stuff", end="counts as eating", topic="Key Point",
      point="It's Hiding In What You Don't Count", parts=[["It's Hiding In What You Don't Count", "hiding"]]),
 # ---------------- part 3: the hidden reasons (3:23 - 6:20)
 dict(id="T3", kind="title", start="Now let me tell you the real reasons", dur=2.4, step="PART 3 OF 4", headline="The Hidden\nReasons",
      photo=f"{TP}/T3", layout="bleed"),
 dict(id="G18", kind="lt", start="reason number one", end="fat wife", topic="Reason #1",
      point="A Fat Girlfriend Or Wife", parts=[["A Fat Girlfriend Or Wife", "reason number one"]]),
 ai_clip("A4", id="A4", chip=((960, 54), "mt"), start="She orders a dessert", end="do not need to do that", tail=0.3, name="Dessert for two",
      note="AI: at dinner, his heavier girlfriend smiles and slides a huge slice of chocolate cake toward him, then offers him a bite"),
 dict(id="G19", kind="lt", start="So you have to decide", end="overweight girlfriend", tail=1.8, topic="You Have To Decide",
      point="Your Body, Or An Overweight Girlfriend?", parts=[["Your Body,", "the body"], ["Or An Overweight Girlfriend?", "overweight girlfriend"]]),
 dict(id="C16", kind="clip", start="You will spend your 50s", end="instead of living", src=[f"{ST}/p8088977.mp4@3.0"],
      note="Pexels 8088977: an older husband takes his wife's blood pressure at the kitchen table"),
 dict(id="C17", kind="clip", start="you'll probably develop", end="problems yourself", src=[f"{ST}/p8460079.mp4@10.6"],
      note="Pexels 8460079: a blood pressure cuff on a man's arm, close-up (the masked wide part of the clip is not used)"),
 dict(id="G20", kind="lt", start="I do not think it is ever worth settling", end="to the relationship", topic="My Opinion",
      point="Never Settle For Someone Who Ignores Her Health", parts=[["Never Settle", "worth settling"], ["For Someone Who Ignores Her Health", "does not care"]]),
 dict(id="G21", kind="lt", start="Reason number two", end="fat friends", topic="Reason #2",
      point="Fat Friends", parts=[["Fat Friends", "Reason number two"]]),
 ai_clip("A5", id="A5", chip=((54, 54), "lt"), start="The guy ordering a salad", end="normal Tuesday", tail=0.3, name="The salad guy",
      note="AI gag: at a sports bar table loaded with wings, nachos and pitchers, the one fit guy gets a salad and the whole table stares"),
 dict(id="G22", kind="lt", start="So decide", end="fitness goals", topic="Two Options",
      point="Separate From Them, Or Sacrifice Your Goals", parts=[["Separate From Them,", "separate"], ["Or Sacrifice Your Goals", "sacrifice"]]),
 dict(id="C18", kind="clip", start="going out 4 nights a week", end="also get abs", src=[f"{ST}/p5389335.mp4@2.0"],
      note="Pexels 5389335: three guys toasting and drinking beers at a bar"),
 dict(id="G23", kind="lt", start="Reason number 3", end="another GLP -1", topic="Reason #3",
      point="You're Not On A GLP-1", parts=[["You're Not On A GLP-1", "Reason number 3"]]),
 dict(id="G24", kind="l3", drift=-6, start="You keep doing exactly", end="1 to 2 months", heading="Your Two Choices",
      points=["Same plan: months or years", "GLP-1: last 10 lb in 1-2 months"], reveal=["You keep doing", "or you take"]),
 dict(id="C20", kind="clip", start="I'm not a doctor", end="final decision", src=["A0166@0.0"], label=AI,
      note="library A0166 (AI): a man like the viewer talking with a male doctor; Dan's default for every 'talk to your doctor' line (RO-19)"),
 dict(id="P03", kind="scene", scene="photo", photo="studio-blue-240", start="But Zepbound has helped me", end="lose their belly fat", tail=0.2, label=REAL,
      note="real studio photo, smiling, glasses, shorts"),
 dict(id="G26", kind="lt", start="Reason number 4", end="bad sleep", topic="Reason #4", point="Bad Sleep", parts=[["Bad Sleep", "Reason number 4"]]),
 dict(id="C21", kind="clip", grade="eq=brightness=0.06:contrast=1.12:saturation=1.05:gamma=1.25", start="Poor sleep raises", end="to say no", src=[f"{ST}/p6944072.mp4@3.0"],
      note="Pexels 6944072: a man sits up awake on his bed at night (dark source, lifted)"),
 dict(id="C22", kind="clip", start="If you sleep five hours", end="you wake up", src=[f"{ST}/p7131835.mp4@1.5"],
      note="Pexels 7131835: a man wakes up exhausted, arm over his eyes"),
 dict(id="G27", kind="lt", start="You cannot out discipline", end="Nobody can", topic="Key Point",
      point="You Can't Out-Discipline 4 Hours Of Sleep", parts=[["You Can't Out-Discipline", "out discipline"], ["4 Hours Of Sleep", "four hours"]]),
 ai_clip("A6", id="A6", start="On 5 hours you stand there", end="eventually you lose", tail=0.3, name="Negotiating with the donut",
      note="AI: an exhausted man stands over the office donut box, hand hovering, then gives in and takes a huge bite"),
 # ---------------- part 4: the simple system (6:23 - 8:10)
 dict(id="T4", kind="title", start="here is my simple system", dur=2.4, step="PART 4 OF 4", headline="My Simple\nSystem", photo=f"{TP}/T4", layout="bleed"),
 dict(id="G28", kind="lt", start="Fast until 2pm", end="Fast until 2pm", tail=1.6, topic="Step 1", point="Fast Until 2 PM", parts=[["Fast Until 2 PM", "Fast"]]),
 dict(id="C23", kind="skip", start="automatically", end="single decision", max_len=1.0, src=["A0169@0.0"], label=AI,   # R2 watch judge: the clock face warps (numbers pop, ghost hands) from 1.0 s into the clip; only its clean first second
      note="library A0169 (AI): the fasting workday, laptop and black coffee from 8 AM toward lunch"),
 dict(id="C24", kind="clip", grade="eq=brightness=0.09:contrast=1.06:saturation=1.10:gamma=1.45", start="And drink", end="kill your appetite", src=["B0486@1.0"],
      note="library B0486: black coffee poured into a mug"),
 dict(id="G29", kind="lt", start="Track everything with a photo", end="with a photo", tail=1.0, topic="Step 2", point="Photograph Everything",
      parts=[["Photograph Everything", "Track"]]),
 dict(id="C25", kind="clip", start="every drink", end="no exceptions", src=[f"{ST}/p8870151.mp4@1.0"],
      note="Pexels 8870151: a phone photographing a plate and a coffee from above"),
 dict(id="G30", kind="lt", start="Especially on the weekend", end="whole ballgame", topic="Key Point",
      point="The Weekend Is The Whole Ballgame", parts=[["The Weekend Is The Whole Ballgame", "Especially"]]),
 dict(id="G31", kind="lt", start="Weigh yourself daily", end="single day readings", topic="Step 3",
      point="Weigh Daily. Watch The 7-Day Trend.", parts=[["Weigh Daily.", "Weigh"], ["Watch The 7-Day Trend.", "Watch"]]),
 dict(id="G32", kind="scene", scene="chart", start="One day means nothing", end="means everything", tail=0.5,
      eyebrow="WEIGH DAILY", headline="One Day Means Nothing. The Trend Means Everything."),
 dict(id="G33", kind="lt", start="Number four, identify", end="less time with them", topic="Step 4",
      point="Less Time With People Who Pull You Down", parts=[["Less Time With People", "identify"], ["Who Pull You Down", "pulling you down"]]),
 dict(id="G34", kind="lt", start="Number five, protect your sleep", end="gym time", topic="Step 5",
      point="Protect Your Sleep. Pick A Bedtime.", parts=[["Protect Your Sleep.", "protect"], ["Pick A Bedtime.", "Pick a bedtime"]]),
 dict(id="G35", kind="scene", scene="recap", start="That is five things", end="sleep properly", tail=0.6,
      eyebrow="MY SIMPLE SYSTEM", headline="5 Things. That's It.",
      items=["Fast until 2 PM", "Photograph everything", "Weigh daily, read the trend", "Cut time with people who pull you down", "Protect your sleep"],
      reveal_items=["Fasten till", "photograph everything", "weigh daily", "cut your time", "sleep properly"]),
 dict(id="G36", kind="lt", start="Notice that not one of them", end="is a supplement", tail=2.5, topic="Key Point",
      point="No New Workout. No Supplement.", parts=[["No New Workout.", "new workout"], ["No Supplement.", "supplement"]]),
 dict(id="G37", kind="lt", start="your problem is that nothing in your day", end="your day is real", tail=1.6, topic="The Real Problem",
      point="Nothing Measured. Nothing Real.", parts=[["Nothing Measured.", "measured"], ["Nothing Real.", "real"]]),
 dict(id="G38", kind="lt", start="You are not stuck", end="You are guessing", tail=1.5, topic="The Blunt Version",
      point="You're Not Stuck. You're GUESSING.", parts=[["You're Not Stuck.", "not stuck"], ["You're GUESSING.", "guessing"]]),
 dict(id="G39", kind="lt", start="Do this honestly for 30 days", end="hormones", topic="The Challenge",
      point="30 Days Of Honest Tracking", parts=[["30 Days Of Honest Tracking", "honestly"]]),
 # ---------------- wrap (8:10 - 8:27)
 dict(id="P04", kind="phone", start="AI macro tracker", end="with AI now", tail=0.1, src=["B0544"],
      note="library B0544: the approved app tour (RO-06) in the phone beside Dan, calorie tracking from a meal photo first, then the workouts"),
]
