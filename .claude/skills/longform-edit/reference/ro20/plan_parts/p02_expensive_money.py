# 9:01 to 16:36  Reason 4 (bad health is ludicrously expensive), money does you no good dead or sick, the "I'm broke"
# excuse, and the three things never to cut (healthy food, sleep, the basics).
# Voices left on camera with no clip: 11:53 mediocre health, 12:24 heirs, 12:51 in my 20s, 15:08 brokie.
#
# NEEDS A PICTURE:
#   10:43 to 10:53 "He had to get a toe amputated ... having one less toe is going to lower your productivity": nothing
#     tasteful in the library or the Pexels index (a bandaged foot, a man on a cane). He stays on camera, no graphic.
#   13:44 to 13:51 "you develop joint problems. Everything you do is gonna be harder and more painful": a man wincing as
#     he gets out of a chair or holds his knee. The one library fit (B0027, patient holding his neck) is already used in
#     an earlier chapter. He stays on camera.
#   13:58 to 14:03 "so painful to climb up the steps, you're just gonna stay on the first floor like an old person": an
#     older person hauling himself up a staircase by the rail. The index has no stairs; the only library stairs clip is a
#     fit man jogging up them (wrong). Gc13 carries it, and it is AI idea 2 below.
#   15:58 to 16:04 "Number two your mattress": his own bed. Cc24 is a library stock clip of a man asleep (B0333); a shot
#     of his real mattress would replace it if the mattress chapter has one to spare.
#   16:13 to 16:15 "I'm talking about rent on something basic": a plain small apartment. Nothing usable in the index
#     (bedroom clips already taken by another part), so only the luxury side of the contrast is pictured (Cc25).
#
# AI IDEAS:
#   15:08 "oh well damn that's easy for you to say, you have money. But I am a brokie, I don't have any money ... nothing
#     I can do": EXCUSE VOICE with the lips synced to his recording. A guy turns out two empty pockets to camera on his
#     sofa, wedged between a stack of takeout bags, a bar cart, sneaker boxes and a giant TV. Earns a slot: it is the
#     voice that sets up the whole second half, and the picture already makes his answer ("you're just spending it on
#     the wrong things") before he says it.
#   13:58 "it'll be so painful to climb up the steps, you're just gonna stay on the first floor like an old person":
#     obviously unreal gag. A man in a bathrobe stands at the foot of the grand staircase in his dream mansion kitted out
#     like a mountaineer (rope, ice axe, a little base camp tent on the marble), looks up at it and gives up. Earns a
#     slot: no stock picture exists for the line, and it is the funniest image in a chapter that is otherwise hospitals.
#
# SPECIAL:
#   10:05 to 11:20 the friend with diabetes is a real, unnamed person: every picture is generic stock (insulin pen,
#     paramedics, a patient with a doctor, an eye exam). Nothing shows or suggests who he is.
#   12:33 his own family's inheritance lawsuits: Cc13 is stock lawyers at a table, no real family photo or document.
#   10:35 Gc05 puts his spoken prices on screen as "$5K To $15K" and "$10K To $15K" (he says five, ten, fifteen grand
#     per trip; ten, fifteen grand per visit). Change the style if the other parts write prices out in full.
#   15:30 he says "cut bullshit": Gc18 says "Cut The Waste" on screen, his audio is untouched.
#   Cc25 (pexels-16580831, the villa with a pool) is a 1280x720 source, on screen 2.7 s.
#   Library IDs used here, for the film-wide repeat check: B0213 B0286 B0275 B0364 B0349 B0336 B0465 B0535 B0231 B0188
#     B0073 B0458 B0456 B0333 (checked against p00, p01, p03, p06 and p07 when this was finished: nothing shared). B0458 is Dan's standing dumbbell curls: if the $100 home setup chapter wants it for
#     "light dumbbells for doing curls", swap Cc21 to B0462 (walking lunges by the pool).
#   Caption fixes seen in the words: 12:45 "if you live a big pile of money behind" is "leave"; 15:12 "bro -key" is
#     "brokie".
PART = [
 # ---- Reason 4: bad health is ludicrously expensive (9:01) ----
 dict(id="Gc01", kind="lt", start="even if you only care", end="ludicrously expensive", tail=1.6, topic="REASON 4 OF 4",
      point="Bad Health Is Ludicrously Expensive", parts=[["Bad Health Is Ludicrously Expensive", "being in bad health"]]),
 dict(id="Cc01", kind="clip", start="When you're in the United", end="pay for everything", tail=0.1,
      src=[stock("pexels-6997944-couple-walking-towards-the-counter-in-the-hospital.mp4", 5.0)], **OTHER,
      note="Pexels stock (new): a couple stand at a clinic front desk sorting out paperwork with the receptionist, 'you're on your own to pay for everything'"),
 dict(id="Gc02", kind="lt", start="but the worse your health", end="even if you do have insurance", tail=0.6, topic="HEALTH INSURANCE",
      point="Worse Health Costs More, Even With Insurance.", parts=[["Worse Health", "but the worse your health"], ["Costs More,", "the more you are going"], ["Even With Insurance.", "even if you do have"]]),
 dict(id="Cc02", kind="clip", start="The lawyer who's working 100", end="doctor who's working 100 hours a week", tail=0.0,
      src=[stock("pexels-8061562-man-using-laptop-in-office.mp4", 9.5), stock("pexels-7579841-doctor-reading-an-x-ray-scan.mp4", 0.3)], **OTHER,
      note="Pexels stock (new), two shots on his two examples: a lawyer in a suit sits down at his desk beside a Lady Justice statue and opens his laptop; then a doctor in a white coat and stethoscope at work"),
 dict(id="Cc03", kind="clip", start="they stack millions and millions", end="get to their 50s and 60s", tail=0.1, src=["B0213@2.0"], **NONE,
      note="library stock: hands count a thick stack of hundred dollar bills on a wooden table, 'they stack millions and millions of dollars'"),
 dict(id="Cc04", kind="clip", start="they get diabetes or they", end="all kinds of heart issues", tail=0.1, src=["B0286@1.0", "B0275@1.0"], **NONE,
      note="library stock, two shots: a gloved nurse does a finger-prick blood sugar test (diabetes), then an ECG machine prints a heart trace (heart issues)"),
 dict(id="Cc05", kind="clip", start="They get cancer. These are", end="expensive problems to solve", tail=0.0, src=["B0364@1.0"], **OTHER,
      note="library stock: a technician fits the head coil on a patient sliding into an MRI scanner, 'they get cancer, these are very very expensive problems to solve'"),
 dict(id="Gc03", kind="lt", start="most people who neglect their", end="they're not even successful", tail=0.1, topic="KEY POINT",
      point="Neglect Your Health, Pay It All Back Later.", parts=[["Neglect Your Health,", "most people who neglect"], ["Pay It All Back Later.", "spend all their money"]]),
 dict(id="Cc06", kind="clip", start="spend all their money and", end="trying to fix", tail=0.1,
      src=[stock("pexels-7546417-elderly-woman-looking-at-the-invoice-while-on-the-table.mp4", 0.0)], **OTHER,
      note="Pexels stock (new): an elderly woman goes through a table covered in invoices with a pen, 'spend all their money and more at the end of their life'"),
 # ---- the friend with diabetes (10:05): the story stays on camera, the costs get pictures ----
 dict(id="Gc04", kind="lt", start="he ended up getting diabetes", end="lost productivity for him", tail=0.25, topic="SOMEONE I KNOW",
      point="Diabetes: Huge Bills And Lost Productivity.", parts=[["Diabetes:", "he ended up getting diabetes"], ["Huge Bills", "massive amount of expense"], ["And Lost Productivity.", "lost productivity"]]),
 dict(id="Cc07", kind="clip", start="Insulin injections all the time", end="get things checked up", tail=0.1,
      src=["B0349@1.0", stock("pexels-4352135-a-doctor-checking-on-a-patient-s-blood-pressure.mp4", 0.5)], **OTHER,
      note="two shots: library stock of hands preparing an insulin pen on a white table (no injection, no stomach), then Pexels stock (new) of a doctor taking a patient's blood pressure, 'go to the doctor all the time to get things checked up'"),
 dict(id="Cc08", kind="clip", start="there's an emergency where you", end="fifteen grand per trip", tail=0.1,
      src=[stock("pexels-6520287-paramedic-pulling-a-stretcher.mp4", 0.3), stock("pexels-6520321-ambulance-on-the-road.mp4", 0.0)], **OTHER,
      note="Pexels stock (new), one scene in two shots: paramedics pull the stretcher out of the back of an ambulance, then the ambulance drives off, under 'you have to get an ambulance to go to the hospital'"),
 dict(id="Gc05", kind="lt", start="Five grand, ten grand", end="fifteen grand per visit", tail=0.0, topic="WHAT IT COSTS",
      point="Ambulance $5K To $15K. Hospital $10K To $15K.", parts=[["Ambulance $5K To $15K.", "Five grand"], ["Hospital $10K To $15K.", "Staying in the hospital"]]),
 dict(id="Cc09", kind="clip", start="Staying in the hospital", end="fifteen grand per visit", tail=0.1, src=["B0336@1.0"], **OTHER,
      note="library stock, never used before: a patient in a gown sits on a hospital bed while a doctor in scrubs goes through scans on a tablet"),
 dict(id="Cc10", kind="clip", start="He has to get injections", end="risk of losing his vision", tail=0.1,
      src=[stock("pexels-5241182-person-having-eye-examination.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): a woman rests her chin on the slit lamp while the eye doctor's scope moves in on her eye"),
 dict(id="Gc06", kind="lt", start="Needless to say you lose", end="money making days are over", tail=1.4, topic="KEY POINT",
      point="Lose Your Vision, Lose Your Income.", parts=[["Lose Your Vision,", "you lose your vision"], ["Lose Your Income.", "your money making days"]]),
 dict(id="Gc07", kind="lt", start="then it's too late for", end="throwing the Hail Mary", tail=0.5, topic="KEY POINT",
      point="Once The Damage Is Done, It's A Hail Mary.", parts=[["Once The Damage Is Done,", "then it's too late for"], ["It's A Hail Mary.", "throwing the Hail Mary"]]),
 dict(id="Gc08", kind="lt", start="If you just invest a", end="expenses down the road", tail=0.1, topic="KEY POINT",
      point="A Little Now Avoids Millions Later.", parts=[["A Little Now", "If you just invest a"], ["Avoids Millions Later.", "you can avoid millions"]]),
 dict(id="Cc11", kind="clip", start="So stop putting that money", end="much much better investment", tail=0.1,
      src=[stock("pexels-31602655-coins-dropping-into-clear-glass-jar.mp4", 0.0), "B0465@0.3"], **DAN,
      note="two shots: Pexels stock (new) of coins dropping into a savings jar on 'stop putting that money in your 401k', then Dan's own footage, never used before, shirtless towel pull-aparts on his lawn in full sun, on 'put it into your health, a much much better investment'"),
 # ---- money does you no good if you're dead or sick (11:50) ----
 dict(id="Gc09", kind="lt", start="I just want you guys", end="if you're dead", tail=0.1, topic="THE FINAL POINT",
      point="Money Does You No Good If You're Dead.", parts=[["Money Does You No Good", "money doesn't do you any"], ["If You're Dead.", "if you're dead"]]),
 dict(id="Cc12", kind="clip", start="your life was a total waste", end="long enough to spend the money", tail=0.1, src=["B0535@0.5"], **OTHER,
      note="library stock: a worn out man slumps face down on his desk beside his laptop, then holds his head, 'your life was a total waste if you spent it all working'"),
 dict(id="Cc13", kind="clip", start="my extended family started suing", end="than they inherited", tail=0.1,
      src=[stock("pexels-8135853-a-woman-giving-documents-to-lawyers.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): a woman pushes papers across the table to two lawyers who pick them apart, a scales of justice figure between them (his family's inheritance lawsuits, no real family shown)"),
 dict(id="Gc10", kind="lt", start="started suing each other", end="than they inherited", tail=1.2, topic="MY OWN FAMILY",
      point="The Lawsuits Cost More Than The Inheritance.", parts=[["The Lawsuits", "started suing each other"], ["Cost More Than The Inheritance.", "wasted more money on"]]),
 dict(id="Gc11", kind="lt", start="But the problems from bad", end="money is no longer going", tail=0.25, topic="KEY POINT",
      point="Bad Health Hits Long Before It Kills You.", parts=[["Bad Health Hits", "But the problems from bad"], ["Long Before It Kills You.", "way earlier than you think"]]),
 dict(id="Gc12", kind="lt", start="A lot of activities are", end="doing a lot of walking", tail=0.25, topic="IF YOU GET SICK",
      point="Too Sick To Enjoy What Your Money Buys.", parts=[["Too Sick To Enjoy What Your Money Buys.", "A lot of activities are"]]),
 dict(id="Cc14", kind="clip", start="Hard vacations where you're doing", end="not going to be doing that", tail=0.0,
      src=[stock("pexels-15288120-back-view-of-a-man-walking-while-carrying-a-black-backpack.mp4", 3.5)], **OTHER,
      note="Pexels stock (new): a traveller with a backpack walks away down a tree-lined path, 'hard vacations where you're doing a lot of walking'"),
 dict(id="Cc15", kind="clip", start="Days at the pool or", end="more challenging for you", tail=0.1,
      src=[stock("pexels-6629925-side-view-of-man-jumping-into-the-swimming-pool.mp4", 5.5), stock("pexels-3997809-a-person-doing-stand-up-paddleboarding.mp4", 2.0),
           stock("pexels-5363094-woman-throwing-hat-in-the-air-sitting-at-beach.mp4", 1.0)], **OTHER,
      note="Pexels stock (new), three quick shots on the three things he names: a man dives into a backyard pool (mid-air to splash), a paddle boarder against the sunset, a woman on the sand tossing her hat at the sea"),
 dict(id="Cc16", kind="clip", start="Let's say if you become", end="challenging to drive", tail=0.1, src=["B0231@1.0"], **OTHER,
      note="library stock, never used before: extreme close-up of an older man's eye behind a thick glasses lens, 'if you become visually impaired'"),
 dict(id="Cc17", kind="clip", start="You could go see the", end="if you're visually impaired", tail=0.1, src=["B0188@1.0"], **NONE,
      note="library stock: a boat crosses a deep blue mountain lake under pine-covered cliffs, 'the most beautiful vacation destination in the world, but if you're visually impaired'"),
 dict(id="Cc18", kind="clip", start="Having that gigantic house that", end="probably won't even matter", tail=0.1,
      src=[stock("pexels-35825271-aerial-view-of-luxurious-residential-neighborhood.mp4", 2.0)], **NONE,
      note="Pexels stock (new): drone shot over a huge white mansion and its gardens, 'that gigantic house that you've been dreaming of'"),
 dict(id="Gc13", kind="lt", start="Having that gigantic house that", end="like an old person", tail=0.0, topic="JOINT PROBLEMS",
      point="A Dream House, Stairs Too Painful To Climb.", parts=[["A Dream House,", "Having that gigantic house"], ["Stairs Too Painful To Climb.", "so painful to climb"]]),
 dict(id="Cc19", kind="clip", start="They would much rather have", end="able to take care of them", tail=0.0, src=["B0073@0.0"], **OTHER,
      note="library stock: a fit dad in a grey T-shirt hands his young daughter a drink in a sunny kitchen, 'a parent who's healthy and able to take care of them'"),
 dict(id="Gc14", kind="lt", start="They would much rather have", end="leaving them a pile of money", tail=0.0, topic="IF KIDS COME FIRST",
      point="Kids Need You Healthy, Not A Pile Of Money.", parts=[["Kids Need You Healthy,", "They would much rather"], ["Not A Pile Of Money.", "leaving them a pile"]]),
 dict(id="Cc20", kind="clip", start="she would far rather have", end="healthy and in great shape", tail=0.1,
      src=[stock("pexels-8795423-a-couple-doing-exercise.mp4", 6.0)], **OTHER,
      note="Pexels stock (new): a fit older couple do push-ups side by side on a lakeside dock at sunrise, 'a husband or boyfriend who is alive, healthy and in great shape'"),
 dict(id="Gc15", kind="lt", start="Money does you no good", end="or if you're sick", tail=2.5, topic="KEY POINT",
      point="Money Does You No Good Dead Or SICK.", parts=[["Money Does You No Good", "Money does you no good"], ["Dead", "if you're dead"], ["Or SICK.", "or if you're sick"]]),
 dict(id="Cc21", kind="clip", start="this makes you more productive", end="makes you more money", tail=0.0, src=["B0458@0.3"], **DAN,
      note="Dan's own footage, never used before: shirtless single-arm dumbbell curls in front of his pool and house in full daylight, under 'investing in your health makes you more money'"),
 dict(id="Gc16", kind="lt", start="this makes you more productive", end="makes you more money", tail=0.1, topic="KEY POINT",
      point="Health Pays: More Productive, More Money.", parts=[["Health Pays:", "this makes you"], ["More Productive,", "more productive in the long"], ["More Money.", "makes you more money"]]),
 # ---- "I'm broke" (14:54): the brokie voice stays on camera ----
 dict(id="A2", kind="clip", start="But I am a bro-key", end="nothing I can do", tail=0.05,
      src=[f"{W}/round2/motion/A2-t1.mp4@0.12"], **AIL, **OTHER,
      note="EXCUSE VOICE, AI clip from the frames Dan approved: the brokie turns out his empty pockets and shrugs, surrounded by where the money went. He does not speak"),
 dict(id="Gc17", kind="lt", start="But that is wrong", end="on the wrong things", tail=1.2, topic="THE BROKE EXCUSE",
      point="You Have Money. It Goes To The Wrong Things.", parts=[["You Have Money.", "you do have the money"], ["It Goes To The Wrong Things.", "you're just spending it"]]),
 dict(id="Gc18", kind="lt", start="You could just cut bullshit", end="maximize your fitness", tail=0.1, topic="KEY POINT",
      point="Cut The Waste, Fund Your Fitness.", parts=[["Cut The Waste,", "You could just cut"], ["Fund Your Fitness.", "more than enough money"]]),
 dict(id="Cc22", kind="clip", start="and have more than enough", end="maximize your fitness", tail=0.1, src=["B0456@0.0"], **DAN,
      note="Dan's own footage, never used before: handstand push-ups against the patio pillar, reps from the first second, under 'everything you need to maximize your fitness'"),
 # ---- what you should never cut (15:36) ----
 dict(id="Gc19", kind="lt", start="Number one healthy food", end="money you're spending on your food", tail=0.25, topic="NEVER CUT 1 OF 3",
      point="Healthy Food: The Last Place To Save Money.", parts=[["Healthy Food:", "Number one healthy food"], ["The Last Place To Save Money.", "doesn't make any sense to sacrifice"]]),
 dict(id="Cc23", kind="clip", start="you should be spending the most", end="delicious healthy food", tail=0.0,
      src=[stock("pexels-4818260-a-woman-shopping-for-fresh-fruits-and-vegetables.mp4", 2.5)], **OTHER,
      note="Pexels stock (new): a woman loads a paper bag of greens and bananas into her car and stops to smell a fresh orange, 'the most that you can afford on delicious healthy food' (his own salad footage is all used in the productivity chapter)"),
 dict(id="Cc24", kind="clip", start="Number two your mattress", end="deserves your money as well", tail=0.1, src=["B0333@0.5"], **OTHER,
      note="library stock: a man sleeps soundly on his side in a white bed, 'your sleep is going to be important' (stands in for his own mattress, see NEEDS A PICTURE)"),
 dict(id="Gc20", kind="lt", start="Number two your mattress", end="deserves your money as well", tail=0.25, topic="NEVER CUT 2 OF 3",
      point="Your Mattress: Sleep Deserves Your Money.", parts=[["Your Mattress:", "Number two your mattress"], ["Sleep Deserves Your Money.", "anything that affects your sleep"]]),
 dict(id="Gc21", kind="lt", start="And then number three", end="such as rent", tail=0.2, topic="NEVER CUT 3 OF 3",
      point="The Necessities Of A Regular Life", parts=[["The Necessities Of A Regular Life", "And then number three"]]),
 dict(id="Cc25", kind="clip", start="I'm not talking about rent", end="on a luxury crib", tail=0.25,
      src=[stock("pexels-16580831-pool-drone-shot.mp4", 6.0)], **NONE,
      note="Pexels stock (new, 720p source): drone pulls back from a terracotta villa with a pool and hot tub, 'rent on a luxury crib'"),
 dict(id="Gc22", kind="lt", start="I'm talking about rent on something", end="talking about utilities", tail=0.6, topic="THE NECESSITIES",
      point="Basic Rent, A Basic Car, Utilities.", parts=[["Basic Rent,", "I'm talking about rent on something"], ["A Basic Car,", "a car payment on"], ["Utilities.", "talking about utilities"]]),
 dict(id="Cc26", kind="clip", start="a car payment on a", end="point A to point B", tail=0.0,
      src=[stock("pexels-8103389-a-young-man-driving-a-car.mp4", 8.5)], **NONE,
      note="Pexels stock (new): a plain old hatchback trundles up a quiet road and turns toward the camera, 'a very basic car that gets you from point A to point B'"),
 dict(id="Cc27", kind="clip", start="And I'm talking about utilities", end="need for your life", tail=0.1,
      src=[stock("pexels-35402332-close-up-of-energy-bill-review-with-hands.mp4", 3.4)], **NONE,
      note="Pexels stock (new): a finger runs down the lines of an electricity bill (starts after the supplier's logo has left the frame), 'utilities, just electricity'"),
 dict(id="Gc23", kind="lt", start="Everything else though", end="sacrifice that if necessary", tail=0.25, topic="KEY POINT",
      point="Everything Else Can Go To Fund Your Health.", parts=[["Everything Else", "Everything else though"], ["Can Go To Fund Your Health.", "we're gonna sacrifice that"]]),
]
