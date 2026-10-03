"""SL-03 round 2: the six shorts as data. Film seconds are on RO-05 round 4 MASTER.mp4.
seg     audio pieces kept (film in, out); every edge sits in measured silence or 20 ms inside a long-form audio join
trim    pauses over the gate's 1.0 s dead-air bound, shortened to 0.9 s; the picture runs faster across them (no jump)
covers  picture that replaces the talking shot: [film a, film b, roll, raw in, cx, speed]
shots   per talking sub-piece (keyed by its index in `batch.py plan` order): win full|mid, cx (fixed) or keys [[raw t, cx]],
        cap (caption top), dh/dy (demo Dan window: source rows and top row), layout phone (phone alone)
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b phrases or offsets
text    the captions as spoken: `shown{spoken}` for numbers, ` | ` at each audio piece join"""

SEG = {
 "S1": [[29.77, 65.38], [97.82, 100.66]],
 "S2": [[65.76, 97.76], [574.15, 586.10]],
 "S3": [[378.16, 419.06], [422.45, 429.77]],
 "S4": [[145.31, 172.15], [485.95, 494.01], [522.32, 539.45]],
 "S5": [[744.20, 751.81], [758.78, 770.85], [789.30, 801.36], [818.80, 844.30]],
 "S6": [[771.45, 811.50], [818.80, 833.36]],
}
TRIM = {"S4": [[531.76, 533.25], [535.10, 537.37, None, 1.35]], "S5": [[766.08, 767.40]], "S6": [[777.14, 778.25]]}
KEEP = 0.90
NAME = {"S1": "short1_break-your-fast-with-this", "S2": "short2_the-20-dollar-salad-for-4", "S3": "short3_keep-salads-fresh-7-days",
        "S4": "short4_stop-buying-salad-dressing", "S5": "short5_track-a-week-of-meals-from-1-photo", "S6": "short6_the-one-line-that-makes-it-accurate"}
TITLE = {"S1": ("INTERMITTENT FASTING", ["BREAK YOUR FAST", "WITH THIS"]), "S2": ("MEAL PREP", ["THE $20 SALAD YOU", "CAN MAKE FOR $4"]),
         "S3": ("MEAL PREP", ["KEEP YOUR SALADS", "FRESH FOR 7 DAYS"]), "S4": ("DAILY SALAD", ["STOP BUYING", "SALAD DRESSING"]),
         "S5": ("AI MACRO TRACKING", ["TRACK A WEEK OF", "MEALS FROM 1 PHOTO"]), "S6": ("AI CALORIE TRACKING", ["THE ONE LINE THAT", "MAKES IT ACCURATE"])}
DEMO_ROLL = "C1541"

COVERS = {
 "S1": [[29.77, 31.97, "C1550", 116.30, 660, 1], [59.52, 61.10, "C1550", 112.40, 800, 1], [97.82, 98.52, "C1550", 120.00, 900, 1]],
 "S2": [[65.76, 67.80, "C1550", 118.60, 930, 1], [580.40, 584.10, "C1548", 117.30, 900, 1]],
 "S3": [[378.16, 380.08, "C1550", 111.30, 800, 1], [396.86, 399.30, "C1548", 91.00, 900, 1], [392.83, 393.33, "C1547", 19.00, 560, 1], [422.45, 422.86, "C1547", 6.90, 990, 8]],
 "S4": [[145.31, 146.80, "C1550", 114.00, 600, 1], [161.16, 161.86, "C1533", 33.20, 1150, 1], [165.41, 166.26, "C1548", 3.70, 950, 1], [485.95, 486.40, "C1550", 98.00, 920, 1]],
 "S5": [], "S6": [],
}
SPLIT = {"S1": [["If you break your fast", 0.0]], "S2": [], "S3": [], "S4": [["You can just pour", 0.0], [36.04, 0]]}
SHOTS = {
 "S1": {1: dict(win="full", cx=980), 2: dict(win="mid", cx=1000), 3: dict(win="full", cx=1000), 5: dict(win="full", cx=1000), 7: dict(win="full", cap=1500, follow=True, lead=0.15)},
 "S2": {1: dict(win="full"), 2: dict(auto=True), 3: dict(auto=True), 5: dict(win="full")},
 "S3": {1: dict(auto=True), 2: dict(win="mid"), 4: dict(win="full"), 6: dict(win="full"), 7: dict(auto=True), 8: dict(win="full"), 11: dict(win="full")},
 "S4": {1: dict(win="full", cap=1500, follow=True, lead=0.0, sigma=0.3, head=True), 3: dict(win="full", keys=[[24.71, 1250], [25.3, 1150], [25.7, 1200], [26.2, 1060], [27.5, 1040], [28.6, 960], [29.2, 900], [29.7, 1300], [30.2, 1220], [30.7, 1120], [31.2, 980], [32.4, 1000]]), 5: dict(win="mid"), 6: dict(win="full"), 8: dict(win="mid", cx=1027), 9: dict(win="full", cx=1017), 10: dict(win="mid"), 11: dict(win="full"), 12: dict(win="mid")},
 "S5": {0: dict(win="full", cap=1500, follow=True, lead=0.0, sigma=0.3, head=True), 1: dict(dh=1080), 2: dict(dh=900), 3: dict(dh=1080, follow=True, lead=0.0, sigma=0.3), 4: dict(layout="phone"), 5: dict(dh=1080),
        6: dict(dh=1080), 7: dict(dh=720, dy=90), 8: dict(win="full", cap=1500, follow=True, lead=0.0, sigma=0.3, head=True)},
 "S6": {0: dict(dh=1080), 1: dict(dh=900, dy=60), 2: dict(layout="phone"), 3: dict(dh=1080, follow=True, lead=0.0, sigma=0.3), 4: dict(layout="phone"), 5: dict(dh=1080), 6: dict(dh=720, dy=90)},
}

BARS = {
 "S1": [dict(id="G1", topic="KEY POINT", parts=[["Break Your Fast With CARBS", "ton of carbs"], ["And Fasting Barely Works", "anywhere near"]], a=-0.6, b=2.1),
        dict(id="G2", topic="KEY POINT", parts=[["A LOW-CARB First Meal", "low carb meal"], ["Means Far More FAT LOSS", "far more effective"]], a=-1.7, b=2.9)],
 "S2": [dict(id="G1", topic="KEY POINT", parts=[["Salad Bar: $20 A SALAD", "about $20"], ["Homemade: About $4", "about $4"]], a=-0.6, b=2.6),
        dict(id="G2", topic="KEY POINT", parts=[["Buy A ROTISSERIE CHICKEN", "This I think"], ["Better Taste, HALF THE PRICE", "tastes much better"]], a=-0.3, b=3.85)],
 "S3": [dict(id="G1", topic="KEY POINT", parts=[["An UNSEALED Salad Bowl", "not sealing"], ["GOES BAD In A Couple Days", "will go bad"]], a=-0.5, b=1.22),
        dict(id="G2", topic="KEY POINT", parts=[["OXO GLASS Containers", "OXO"], ["LOCKING LIDS Keep It FRESH", "great brand"]], a=-0.3, b=3.95)],
 "S4": [dict(id="G1", topic="KEY POINT", parts=[["Skip STORE DRESSING", "This olive oil based"], ["Use OLIVE OIL Instead", "will taste"]], a=0.0, b=3.6),
        dict(id="G2", topic="KEY POINT", parts=[["Dress It RIGHT ON THE MEAL", "pour it onto"], ["Olive Oil + Spices, NO PREP", "put your spices"]], a=-0.3, b=3.2),
        dict(id="G3", topic="KEY POINT", parts=[["120 CALORIES A Tablespoon", "calories per tablespoon"], ["So MEASURE Your Olive Oil", "freehand"]], a=-0.3, b=2.45)],
 "S5": [], "S6": [],
}

TEXT = {
 "S1": "Let's talk about why you should be making a daily salad and why I consider this my most important fitness habit. So I practice intermittent fasting, which means I'm fasting until about 2{two} PM{p m} every day. Scientific research has proven that the way that you break your fast is incredibly, incredibly important. If you break your fast with a ton of carbs or sugar or, worst of all, alcohol, then intermittent fasting is not going to be anywhere near as effective. However, if your first meal consists of a low carb meal, like this salad for example, then your fast is going to be far more effective for fat loss and for supporting your health. | So if you really want to lock in, start doing what I'm doing right here.",
 "S2": "Let's talk about why I make it myself and why I don't just get it from Whole Foods or another salad bar. That is actually what I used to do before the pandemic. I went to Whole Foods, went to that salad bar every single day. But that approach had a few drawbacks. Number one, I had to drive to Whole Foods 10{ten} minutes and back every day. Doing that made it so that way I basically never did this on the weekends. Sometimes I wouldn't get to it during the week, and it just made the habit a lot more inconvenient. It also cost about $20{twenty dollars} per salad. This costs you about $4{four dollars} per salad, so it's much, much cheaper. | I used to buy shredded chicken from Whole Foods or from the grocery store. This I think is far superior though for a couple different reasons. Number one, the chicken tastes much better. Number two, it's about half the price as shredded chicken.",
 "S3": "How to keep these salads fresh for 7{seven} days. So if you make the mistake of just putting everything in a giant bowl or not sealing everything, your salads will go bad after a couple days. You need glass food prep containers like this that have a sealable lid. For these type of containers, your food is in the glass, so it's not getting all that plastic on it. And now I have a real good seal. So it's going to stay fresher in a container like this much better than, let's say, if I use a cheap plastic Tupperware. What I recommend, if you can see this here, is OXO{oxo}. That's the ones I buy. They make a great brand of glass containers. About $20{twenty dollars} per container. Definitely worth it. I'm going to go through here and just box everything up. | So you notice that we did a minimum of chopping in here. That's the key to keeping these fresh. That and also keeping it in these sealed glass containers.",
 "S4": "Now let's talk about the dressing. What you don't want to do, what will ruin your salad, is just go into a store and buy that store-made dressing. The reason for that is they use polyunsaturated oils, soybean oil or rapeseed oil, or oil that is designed to have a long shelf life. Instead, you want this: olive oil. In my opinion, the healthiest fat that you can consume and also the best tasting fat. This olive oil based dressing will taste better than this store-bought dressing. | So I've discovered that you don't need to pre-make your dressing. You can just pour it onto the meal, put your spices right on there, and it's going to be a really good tasting dressing. | This olive oil has 120{one hundred twenty} calories per tablespoon. I used to just pour it freehand, but then it's easy to pour on a little bit too much. So pour it in here. One tablespoon. Two tablespoons. There we go.",
 "S5": "Make sure that you're tracking your macros when you make these meal preps. AI{a i} has made it so, so easy, so there's no excuse to not do this. | And the option that we want is the meal prep option right here. So I'm going to tap on Meal Prep. I then add photos of my batch, and I take my photos. And then I'll get a shot of my olive oil. | 7{seven} salads, all vegetables consumed, 2{two} eggs per salad, 80%{eighty percent} of chicken consumed, 2{two} tablespoons of olive oil per salad. Then I'm going to tap on Analyze Meal. | So scrolling down to the bottom here, you see it's 683{six hundred eighty three} total calories per salad. When I tracked this manually, it was about 720{seven hundred twenty} calories per salad. So that's pretty accurate, almost near accurate for taking pictures. All you have to do is take a picture of all the individual ingredients and you have about a third or maybe two thirds of the meals for your entire week tracked just by doing this one meal prep thing alone.",
 "S6": "The spices and the vinegar, you don't need to worry about taking a picture of, because they're not caloric. If you just took the pictures alone, it would work to some extent, but it doesn't know exactly how much olive oil you're putting on and how much chicken you're using. You're probably not eating 100%{one hundred percent} of the chicken down to the skeleton. 7{seven} salads, all vegetables consumed, 2{two} eggs per salad, 80%{eighty percent} of chicken consumed, 2{two} tablespoons of olive oil per salad. Then I'm going to tap on Analyze Meal. OK{okay}, so I got my results. Now you can see the AI{a i} has asked me a couple additional questions for context. Did you use the entire jar? Nope. Just a few olives per salad. | So scrolling down to the bottom here, you see it's 683{six hundred eighty three} total calories per salad. When I tracked this manually, it was about 720{seven hundred twenty} calories per salad. So that's pretty accurate, almost near accurate for taking pictures.",
}
