# 35:42 to 44:38  Middle class buys 5, 6 and 7 of 7 (GLP-1 weight loss medication, TRT, the three supplements), then
# the first "over $10,000 a month" buy (a home gym). IDs Gf.. / Cf...
#
# NEEDS A PICTURE:
#   42:35 to 43:00 "I had a very big shed in my backyard ... I finished the shed, I put in insulation, I put in air
#     conditioning, I put in the rubber floor, equipment in that shed": HIS OWN SHED GYM, outside and inside. Nothing of it
#     is in the library or in any shoot roll, and the Pexels sheds and home gyms are a tropical hut and one cluttered tent
#     gym full of motorcycles. He stays on camera with Gf27. A phone photo or 10 seconds of video of the real shed gym
#     would be the best single addition to this stretch. The same footage would also replace the two AI home gym clips
#     (Cf21, Cf25) and cover 44:01 "spending $20,000 on a home gym".
#   35:46 "GLP, weight loss medication" and 37:01 "I plan on staying on Zepbound for the remainder of my life": his own
#     injection pen or vial. No real footage of it exists (the Zepbound roll C1513 is all talking). Cf01 is a stock pen.
#   36:01 "they see the price tag on these drugs and the fact that insurance does not cover them": no pharmacy counter or
#     receipt clip fits (the library pharmacy shelf B0060 is used in an earlier part). On camera with Gf02.
#   43:48 "blast your own music through the speakers": no speaker clip anywhere. On camera with Gf31.
#   42:03 "the ballers, the guys who are millionaires": on camera with Gf24 (the Pexels mansion and cash clips are taken
#     by other parts).
#
# AI IDEAS:
#   36:07 "oh, I can't afford 400 bucks a month, I guess I'll just be fat the rest of my life": EXCUSE VOICE with the
#     lips synced to his recording. A heavyset middle class guy at his kitchen table says it with a shrug while a brand
#     new jet ski sits on a trailer outside the window behind him. Chest up, the table hides his midsection. Earns a slot:
#     it is a voice, and the picture makes the section's point (he has the money, he spends it elsewhere).
#   37:08 "you have a thought about food, you're getting distracted" (food noise): obviously unreal gag. A man types at
#     his office desk while a cartoon slice of pizza, a donut and a burger float around his head and tap him on the
#     shoulder until he stops working. Earns a slot: "food noise" has no literal picture, and Cf05 is only a tired
#     office worker.
#
# SPECIAL:
#   41:01 "I'll show you what it looks like on screen right now" (the vitamin D dropper): Cf18 puts his real bottle on
#     screen full frame from 40:57 to 41:04 (library B0470, the D3+K2 dropper bottle shot on this same shoot day, roll
#     C1520). Lead editor: confirm full frame is what you want here, or set it beside him as an inset. The bottle label
#     reads "AG d3+k2", the product he names.
#   Three clips use raw B-roll rolls of this shoot that are not in the clip library yet (same granite counter as B0470,
#     ungraded S-Cinetone): C1521 his supplement stack (Cf13), C1529 his fish oil bottle (Cf14), C1518 his magnesium
#     glycinate jar (Cf19). Product labels are readable in all of them (Thorne, Nutricost, Isopure): they are his own
#     products.
#   Studies he cites with a number: 40:30 "about 70% of the U.S. population is vitamin D deficient" (Gf18) and 41:26
#     "about 50% of the US population is deficient in magnesium" (Gf21). Both lower thirds carry his number with "About".
#     38:59 "Higher testosterone men tend to make more money" (Gf10) is stated without a source.
#   38:18 "you can't afford it, you can't afford it" (voice, take map note 5): left on camera, nothing on screen.
#   38:21 "Cash out that college account, cash out your 401k": Gf07 and Cf09 play it straight as he says it.
#   On-screen text has no drug brand name. "GLP-1" (Gf01) and "TRT" (Gf08) are the only capital-letter words in this
#     part and both are names, not emphasis: no lower third here uses a FULL CAPS punch word.
#   Section labels: he does not number the over $10,000 items, so Gf25 uses "OVER $10,000 A MONTH" like the next part.
#   Library clips used here, for the film-wide repeat check: B0351, B0502, B0449, B0318, B0431, B0527, B0536, B0434,
#     B0233, B0470, A0037, B0495, B0468, A0080, A0157 (checked against p00 to p04, p06 and p07 as they stood when this was
#     finished: nothing shared). B0318 is the same restaurant table as B0316 and B0317 (do not use
#     those elsewhere). B0351 shares its blue backdrop with B0483 (not used here). A0080 is the same man as A0081.
#   B0233 (sunscreen) and Pexels 8549741 (empty gym) are 1280x720 sources. Pexels 7131635 (Cf20, man asleep) is from the
#     same shoot as 7131561 and 7131718 in the index: do not pair it with those.
PART = [
 # ---- Middle class buy 5 of 7: GLP-1 weight loss medication ----
 dict(id="Gf01", kind="lt", start="putting your money into", end="or Ozempic", tail=0.1, topic="MIDDLE CLASS BUY 5 OF 7",
      point="GLP-1 Weight Loss Medication", parts=[["GLP-1 Weight Loss Medication", "GLP, weight loss medication"]]),
 dict(id="Cf01", kind="clip", start="GLP, weight loss medication", end="or Ozempic", tail=0.1, src=["B0351@0.5"], **OTHER,
      note="library stock (in the unpublished Zepbound cut only): hands in a beige sweater uncap and ready an injector pen against a blue backdrop. No brand visible"),
 dict(id="Cf02", kind="clip", start="So I know so many people", end="they're significantly overweight", tail=0.0, src=["B0502@0.0"], **OTHER,
      note="library stock: overhead of feet in blue socks stepping onto a bathroom scale (they want to lose weight). Legs only, no stomach"),
 dict(id="Gf02", kind="lt", start="insurance does not cover them", end="400 bucks a month", tail=0.4, topic="THE OBJECTION",
      point="Not Covered By Insurance. $400 A Month.", parts=[["Not Covered By Insurance.", "insurance does not cover them"], ["$400 A Month.", "400 bucks a month"]]),
 dict(id="Gf03", kind="lt", start="this is crunch time", end="serious medical bills", topic="CRUNCH TIME",
      point="Lose It Before The Medical Bills Start.", parts=[["Lose It", "this is crunch time"], ["Before The Medical Bills Start.", "you start getting"]]),
 dict(id="Gf04", kind="lt", start="sacrifice the bars and clubs", end="get your injections", topic="FIND THE MONEY",
      point="Cut Bars, Dates And Alcohol To Pay For It.", parts=[["Cut Bars,", "sacrifice the bars and clubs"], ["Dates", "expensive dates"], ["And Alcohol", "alcohol at home"], ["To Pay For It.", "get your injections"]]),
 dict(id="Cf03", kind="clip", start="sacrifice the bars and clubs", end="the alcohol at home", tail=0.1, src=[stock("pexels-28931125-bartender-shaking-cocktail-in-modern-bar.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): a bartender in a blue shirt shakes a cocktail behind a lit bar counter"),
 dict(id="Cf04", kind="clip", start="one of the primary reasons", end="remainder of my life", tail=0.1, src=["B0449@0.5"], **DAN,
      note="Dan's real B-roll, never used: shirtless seated dumbbell press by his pool, abs clearly lit and facing camera ('as someone with six pack abs'). The pose clips B0438 and B0459 are used in earlier parts"),
 dict(id="Gf05", kind="lt", start="It reduces the food noise and", end="you're getting distracted", topic="FOOD NOISE",
      point="Fewer Food Thoughts, More Focused Work.", parts=[["Fewer Food Thoughts,", "It reduces the food noise and"], ["More Focused Work.", "increases the productivity"]]),
 dict(id="Cf05", kind="clip", start="When you're working during the day", end="distracting your focus all day", tail=0.1, src=[stock("pexels-8865904-man-wearing-eyeglasses-working-at-the-office.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): an office worker in a headset takes off his glasses and rubs his eyes at his desk, focus gone"),
 dict(id="Cf06", kind="clip", start="your desire to waste money", end="going to seem as appealing", tail=0.1, src=[stock("pexels-4765778-pouring-alcoholic-drink-on-a-cocktail-glass.mp4", 1.3)], **NONE,
      note="Pexels stock (new): a pink cocktail is poured into a salted glass on a neon-lit bar"),
 dict(id="Cf07", kind="clip", start="Going to restaurants is not", end="you're wasting money on", tail=0.1, src=["B0318@0.5"], **OTHER,
      note="library stock (in the unpublished Zepbound cut only): a couple clink wine glasses over a full restaurant table"),
 dict(id="Gf06", kind="lt", start="that $400 per month", end="and alcohol expenses", topic="KEY POINT",
      point="The $400 A Month Can Pay For Itself.", parts=[["The $400 A Month", "that $400 per month"], ["Can Pay For Itself.", "you will easily save"]]),
 dict(id="Cf08", kind="clip", start="And again, if you have a savings", end="college fund for your kids", tail=0.1, src=[stock("pexels-7118320-kid-putting-the-coins-to-the-glass-jar.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): a child gathers coins off the floor and drops them into a glass savings jar (the college fund)"),
 dict(id="Gf07", kind="lt", start="Cash out that college account", end="that will benefit your finances", tail=0.1, topic="KEY POINT",
      point="Put Your Health Ahead Of Your Savings.", parts=[["Put Your Health", "Cash out that college account"], ["Ahead Of Your Savings.", "live a great life"]]),
 dict(id="Cf09", kind="clip", start="Cash out that college account", end="live a great life", tail=0.1, src=[stock("pexels-12033695-pulling-coins-out-of-jar.mp4", 0.2)], **OTHER,
      note="Pexels stock (new): a hand reaches into a savings jar and pulls the coins out (cash it out), pink background"),
 # ---- Middle class buy 6 of 7: TRT ----
 dict(id="Gf08", kind="lt", start="Here's the next thing you middle", end="started my TRT yet", topic="MIDDLE CLASS BUY 6 OF 7",
      point="TRT: Testosterone Replacement Therapy", parts=[["TRT: Testosterone Replacement Therapy", "TRT. Now, I haven't"]]),
 dict(id="Cf10", kind="clip", start="This is something I plan", end="absolutely changed their life", tail=0.1, src=[stock("pexels-6290576-person-filling-the-syringe.mp4", 1.0)], **OTHER,
      note="Pexels stock (new): a gloved hand draws a dose from a small vial into a syringe, plain pale background, no label readable"),
 dict(id="Gf09", kind="lt", start="this isn't very expensive", end="they can't afford this", topic="THE PRICE",
      point="Cheap For The Benefits: A Few Hundred A Month.", parts=[["Cheap For The Benefits:", "this isn't very expensive"], ["A Few Hundred A Month.", "a few hundred dollars"]]),
 dict(id="Gf10", kind="lt", start="Almost everybody on TRT reports", end="tend to make more money", tail=0.6, topic="KEY POINT",
      point="More Productive, And It Tends To Pay More.", parts=[["More Productive,", "their productivity gets so much higher"], ["And It Tends To Pay More.", "tend to make more money"]]),
 dict(id="Cf11", kind="clip", start="getting in better workouts", end="making better food choices", tail=0.1, src=["B0431@0.3", "B0527@0.0"], **DAN,
      note="Dan's real B-roll: kettlebell deadlifts by his pool, never used (better workouts), then his gloved hands seasoning a bowl of chopped salad vegetables, used only in the salad Shorts (better food choices)"),
 dict(id="Gf11", kind="lt", start="better workouts for the next", end="being more productive", tail=0.4, topic="THE NEXT 20 YEARS",
      point="Better Workouts, Better Food, More Work Done.", parts=[["Better Workouts,", "better workouts for the next"], ["Better Food,", "better food choices"], ["More Work Done.", "being more productive"]]),
 dict(id="Cf12", kind="clip", start="Now if you're a man in your", end="haven't been tested yet", tail=0.1, src=["B0536@0.5"], **OTHER,
      note="library stock: close on an arm with a tourniquet as gloved hands prepare a blood draw at a clinic (getting tested)"),
 dict(id="Gf12", kind="lt", start="you haven't been tested yet", end="make it happen", tail=0.0, topic="LOW TESTOSTERONE",
      point="Get Tested. If It's Low, Make It Happen.", parts=[["Get Tested.", "you haven't been tested yet"], ["If It's Low, Make It Happen.", "Sacrifice whatever needs"]]),
 # ---- Middle class buy 7 of 7: supplements ----
 dict(id="Gf13", kind="lt", start="the final thing you need", end="supplements per day", topic="MIDDLE CLASS BUY 7 OF 7",
      point="Supplements", parts=[["Supplements", "supplements. Now, I personally"]]),
 dict(id="Cf13", kind="clip", start="Now, I personally take 10", end="on supplements every month", tail=0.1, src=[br("C1521", 1.0)], grade="C1521", **NONE,
      note="Dan's real B-roll, raw roll C1521 of this shoot (not in the library yet): his own supplement bottles and protein bag lined up on the granite counter"),
 dict(id="Gf14", kind="lt", start="The first supplement that you need", end="cheap as dirt", topic="SUPPLEMENT 1 OF 3",
      point="Fish Oil", parts=[["Fish Oil", "a fish oil or Omega"]]),
 dict(id="Cf14", kind="clip", start="The first supplement that you need", end="cheap as dirt", tail=0.0, src=[br("C1529", 0.5)], grade="C1529", **NONE,
      note="Dan's real B-roll, raw roll C1529 of this shoot (not in the library yet): his own fish oil bottle (Thorne Super EPA) on the granite counter"),
 dict(id="Cf15", kind="clip", start="You can buy a hundred", end="about $50 or $60", tail=0.1, src=[stock("pexels-3752510-close-up-view-of-gel-capsules-inside-a-bottle.mp4", 8.0)], **NONE,
      note="Pexels stock (new): macro of golden oil softgels tumbling, from the bright part of the clip"),
 dict(id="Gf15", kind="lt", start="a hundred of them for about", end="about $50 or $60", tail=0.1, topic="WHAT IT COSTS",
      point="$20 To $30 Per 100. Top Brands, $50 To $60.", parts=[["$20 To $30 Per 100.", "for about $20"], ["Top Brands, $50 To $60.", "about $50"]]),
 dict(id="Gf16", kind="lt", start="you're going to take only one", end="any supplement that you can take", tail=0.0, topic="KEY POINT",
      point="Only Taking One Supplement? Make It Fish Oil.", parts=[["Only Taking One Supplement?", "you're going to take only one"], ["Make It Fish Oil.", "is what you need to take"]]),
 dict(id="Gf17", kind="lt", start="benefits your heart health", end="do hard workouts", topic="FISH OIL",
      point="Heart, Brain, Joints, Skin, Workout Recovery.", parts=[["Heart, Brain, Joints,", "benefits your heart health"], ["Skin,", "skin, and nails"], ["Workout Recovery.", "workout recovery"]]),
 dict(id="Cf16", kind="clip", start="It'll improve your workout recovery", end="do hard workouts", tail=0.1, src=["B0434@0.5"], **DAN,
      note="Dan's real B-roll, never used: V-up leg raises holding a medicine ball on the mat by his pool, a hard workout"),
 dict(id="Gf18", kind="lt", start="Second one that you need", end="is vitamin D deficient", tail=0.0, topic="SUPPLEMENT 2 OF 3",
      point="Vitamin D: About 70% Of The U.S. Is Deficient.", parts=[["Vitamin D:", "Second one that you need"], ["About 70% Of The U.S. Is Deficient.", "about 70"]]),
 dict(id="Gf19", kind="lt", start="If you are older", end="to be vitamin D deficient", topic="VITAMIN D",
      point="Older Or Darker Skin? Even More Likely.", parts=[["Older", "If you are older"], ["Or Darker Skin?", "darker skin"], ["Even More Likely.", "even more likely"]]),
 dict(id="Cf17", kind="clip", start="If you have extremely fair skin", end="vitamin D deficient as well", tail=0.1, src=["B0233@0.5"], **OTHER,
      note="library stock (in the unpublished spray tan cut only, 720p): a fair-skinned man rubs sunscreen into his forearm on a beach blanket ('because you burn')"),
 dict(id="Cf18", kind="clip", start="It comes in a liquid format", end="on screen right now", tail=0.1, src=["B0470@0.3"], **NONE,
      note="Dan's real B-roll, never used (roll C1520 of this shoot): his own liquid vitamin D3+K2 dropper bottle on the granite counter. This is the 'on screen right now' shot, see SPECIAL"),
 dict(id="Gf20", kind="lt", start="the cheapest form of vitamin D", end="more absorbable for you", topic="MY PICK",
      point="Liquid Vitamin D: Cheaper, Absorbs Better.", parts=[["Liquid Vitamin D:", "the cheapest form of vitamin D"], ["Cheaper,", "reduce your cost"], ["Absorbs Better.", "more absorbable"]]),
 dict(id="Gf21", kind="lt", start="Now the third thing", end="is deficient in magnesium", topic="SUPPLEMENT 3 OF 3",
      point="Magnesium: About 50% Of The U.S. Is Deficient.", parts=[["Magnesium:", "Now the third thing"], ["About 50% Of The U.S. Is Deficient.", "about 50"]]),
 dict(id="Cf19", kind="clip", start="All you need to get started", end="one form of magnesium", tail=0.0, src=[br("C1518", 0.5)], grade="C1518", **NONE,
      note="Dan's real B-roll, raw roll C1518 of this shoot (not in the library yet): his own magnesium glycinate jar (label reads Magnesium Bisglycinate) on the granite counter"),
 dict(id="Gf22", kind="lt", start="magnesium glycinate. In my opinion", end="It'll improve your sleep", topic="MAGNESIUM",
      point="Magnesium Glycinate, Right Before Bed.", parts=[["Magnesium Glycinate,", "magnesium glycinate. In my opinion"], ["Right Before Bed.", "take that right before bed"]]),
 dict(id="Cf20", kind="clip", start="take that right before bed", end="more relaxed and present", tail=0.1, src=[stock("pexels-7131635-a-man-sleeping.mp4", 0.0)], **OTHER,
      note="Pexels stock (new): a man asleep on white pillows, the calm first seconds only (he stirs after 5 s)"),
 dict(id="Gf23", kind="lt", start="just get that fish oil", end="the big three", tail=1.6, topic="THE BIG THREE",
      point="Fish Oil, Vitamin D, Magnesium.", parts=[["Fish Oil,", "get that fish oil"], ["Vitamin D,", "get the vitamin D"], ["Magnesium.", "and magnesium, the big"]]),
 # ---- Making over $10,000 a month: build a home gym ----
 dict(id="Gf24", kind="lt", start="So now let's talk about the ballers", end="10 grand a month", topic="FOR THE BALLERS",
      point="Making Over $10,000 A Month", parts=[["Making Over $10,000 A Month", "making more than 10 grand"]]),
 dict(id="Gf25", kind="lt", start="The first thing that you need", end="is a home gym", tail=1.0, topic="OVER $10,000 A MONTH",
      point="Build A Home Gym", parts=[["Build A Home Gym", "is a home gym"]]),
 dict(id="Cf21", kind="clip", start="is a home gym", end="a home gym that has everything", tail=0.1, src=["A0037@0.0"], **AIL, **OTHER,
      note="library AI clip: a fit man curls dumbbells in a bright home gym with a rack, a dumbbell rack and a bench (a home gym that has everything)"),
 dict(id="Gf26", kind="lt", start="for about $10 ,000", end="20 and $30 ,000", topic="WHAT IT COSTS",
      point="About $10,000. $20,000 To $30,000 If You Build.", parts=[["About $10,000.", "for about $10 ,000"], ["$20,000 To $30,000 If You Build.", "between 20 and"]]),
 dict(id="Gf27", kind="lt", start="Rather than tearing the shed down", end="the rubber floor", tail=1.5, topic="MY HOME GYM",
      point="An Old Shed, Insulated And Air Conditioned.", parts=[["An Old Shed,", "Rather than tearing the shed down"], ["Insulated", "I put in insulation"], ["And Air Conditioned.", "air conditioning"]]),
 dict(id="Cf22", kind="clip", start="the reason why I did this", end="my only option", tail=0.1, src=[stock("pexels-8549741-an-empty-gym.mp4", 1.0)], **NONE,
      note="Pexels stock (new, 720p): a slow move down a row of treadmills in a gym with nobody in it (the gym was closed)"),
 dict(id="Gf28", kind="lt", start="Back during COVID the gym", end="every single time", topic="WHY I BUILT IT",
      point="Gyms Were Closed. It Was My Only Option.", parts=[["Gyms Were Closed.", "Back during COVID the gym"], ["It Was My Only Option.", "my only option"]]),
 dict(id="Gf29", kind="lt", start="building a home gym that has", end="back and forth", topic="SHORT ON TIME?",
      point="A Home Gym Removes The Commute.", parts=[["A Home Gym", "building a home gym that has"], ["Removes The Commute.", "It eliminates commute time"]]),
 dict(id="Cf23", kind="clip", start="It eliminates commute time", end="back and forth", tail=0.1, src=["B0495@1.0"], **NONE,
      note="library stock: high view of a packed multi-lane highway in rush-hour traffic (the commute)"),
 dict(id="Gf30", kind="lt", start="It eliminates that 100", end="could actually pay for itself", topic="WHY A HOME GYM",
      point="Saves $100 To $200 A Month. Can Pay For Itself.", parts=[["Saves $100 To $200 A Month.", "It eliminates that 100"], ["Can Pay For Itself.", "could actually pay for itself"]]),
 dict(id="Gf31", kind="lt", start="work out more often", end="through the speakers", topic="WHY A HOME GYM",
      point="More Workouts. Your Rules. Your Music.", parts=[["More Workouts.", "work out more often"], ["Your Rules.", "You can work out shirtless"], ["Your Music.", "blast your own music"]]),
 dict(id="Cf24", kind="clip", start="You can work out shirtless", end="in your home gym", tail=0.1, src=["B0468@0.5"], **DAN,
      note="Dan's real B-roll, never used: shirtless plank up-downs on a mat in his own yard (working out shirtless at home)"),
 dict(id="Gf32", kind="lt", start="doing what I'm doing", end="best of both worlds", topic="WHAT I DO",
      point="A Gym Membership Plus A $20,000 Home Gym.", parts=[["A Gym Membership", "getting a gym membership"], ["Plus A $20,000 Home Gym.", "spending $20 ,000"]]),
 dict(id="Cf25", kind="clip", start="spending $20 ,000 on a", end="best of both worlds", tail=0.1, src=["A0080@2.6"], **AIL, **OTHER,
      note="library AI clip: a man stands up from the bench and curls dumbbells in a garage gym with a power rack and a full dumbbell rack"),
 dict(id="Gf33", kind="lt", start="anytime you wanna do a regular", end="the full equipment", topic="GYM DAYS",
      point="You Have Time And Want Full Equipment.", parts=[["You Have Time", "anytime you wanna do a regular"], ["And Want Full Equipment.", "you have your gym environment"]]),
 dict(id="Cf26", kind="clip", start="do a regular workout", end="everything you need right there", tail=0.1, src=[stock("pexels-37317187-modern-gym-interior-with-high-tech-equipment.mp4", 1.0)], **NONE,
      note="Pexels stock (new): a slow move through a big modern commercial gym, rows of racks and machines, nobody in frame (the gym with the full equipment)"),
 dict(id="Gf34", kind="lt", start="if you're strapped for time", end="someone new to fitness", tail=1.5, topic="HOME GYM DAYS",
      point="Short On Time, Or Teaching A Beginner.", parts=[["Short On Time,", "if you're strapped for time"], ["Or Teaching A Beginner.", "someone new to fitness"]]),
 dict(id="Cf27", kind="clip", start="you wanna be showing them", end="how to do the exercises", tail=0.1, src=["A0157@0.3"], **AIL, **OTHER,
      note="library AI clip (RO-06, approved): in a home garage gym the trainer (AI Dan) kneels beside a beginner doing push-ups on handles and cheers him on (showing someone new how to do the exercises)"),
]
