"""SL-17: three Shorts from RO-26 "I'm 41. My Life Is Top 1%. How I Did It." as data. Film seconds are on the RO-26 R5 master
(5:03.74, sha 395cd8fb). Dan's picks 2026-10-20: "Let's do A, but start with 'Believe it or not, nutrition made an even bigger
impact.' See if you can add some content to the end... B: Let's start with 'If you're watching this, you want to start working
out...' See if you can add some content to the end to fill it out... Let's do D as is."
seg     audio pieces kept (film in, out); every edge sits in measured silence on the film's dry voice (snap.py + 10 ms levels)
VIRT    raw C1768 ranges the film never used, at a virtual film time (master_audio_ext.wav, the film's fixed voice chain)
covers  picture that replaces the talking shot: dict(id, a, b = film times or "o<sec>" output times, src + t (clip in-point) + fx/fy
        + fit + eq + ai (chip xy, u) + speed, or scene=<name in scenes.py>)
split   a size step inside one continuous take, in the pause before a phrase
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets
text    the captions as spoken, ` | ` at each audio piece join (spellings from the film's corrected .srt)"""
STOCK = "/Volumes/Extreme/_edit_work/SL-17/clips/"          # copies; never read from another session's build folder at render time
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
DISC = {}
# C1768 (4K, x in 1920 space): hair top 48-64 px (film shot_framing hair_top 96-128 in 4K). full = whole height (48 px over his hair
# = 72 px on the 1610 picture); mid 604x900 from y 8 (40 px = 72 px on the picture). Verified on the delivered frames (hairgate).
Y0 = {"full": 4, "mid": 9}      # hair top min 46 (1920 space, track masks): 42 px over it in a 1010 window, 37 in 865 = 66-69 px on the 1610 picture (4 %)
KEEP = 0.90
TRIM = {}
# A's restored line: Dan's own filmed script line the film dropped (raw C1768 181.81-184.88 "I meal prep, which costs me about $8 or
# $9 a meal." and his retake 187.72-189.32 "That's less than ordering Chipotle." (Gemini 3.1 Pro: take 2 clean, take 1 slurs "ordering")).
# The raw lav through audio/film_voice_chain.txt + 7.8 dB + the film's limiter matches the master at 0.9997 correlation (film 90-118 s).
V0 = 400.0
def V(raw): return round(V0 + raw - 181.50, 4)
VIRT = [dict(at=V0, raw=181.50, dur=8.2)]
SEG = {
 # A r3 (reviewer A2): piece 2 keeps Dan's own 0.43 s pause before "I" (from raw 181.86) and the whole breath after "meal." (to 185.21,
 # speech resumes 185.25); take 2 from 187.70 (speech 187.75). A: "Believe" from 99.84 (silence 99.61-99.84); piece 1 runs to the film's own join 122.92 (pillar2_a end, raw 181.81), and the
 # take runs on in raw into the meal-prep line (no audio join: the same continuous take); "meal." ends 184.70, breath to 185.2;
 # take 2 from 187.72 (speech 187.75), "Chipotle." decays to -52 dB at 189.29; the film's pillar2_b from 123.00 ("If" 123.36).
 "A": [[99.66, 122.92], [V(181.81), V(185.16)], [V(187.66), V(189.32)], [123.12, 132.48]],
 # B: "If" from 65.31 (silence 65.17-65.31); "too." ends 86.48 (silence 86.55-86.74); then the film's own earlier lines:
 # "Starting" from 50.56 (silence 50.19-50.56); "ways." ends 64.80 (silence 64.92-65.07)
 "B": [[65.18, 86.56], [50.30, 64.95]],
 # D: "I strongly" (silence 246.91-246.98); "can't." ends at the film join 254.45; "I'm" from 215.20 (silence 214.79-214.98);
 # "more." ends 246.70 (silence 246.78-246.90); "Training" from 254.66 (silence 254.44-254.66); "better." ends 258.06
 "D": [[246.92, 254.45], [214.90, 246.78], [254.46, 258.14]],
}
PICKUP = {}
WORDFIX = {}
NAME = {"A": "short1_nutrition-matters-more-than-your-workouts", "B": "short2_start-with-5-minutes-every-morning", "D": "short3_every-man-should-train-a-martial-art"}
TITLE = {"A": ("NUTRITION", ["Nutrition Matters More", "Than Your Workouts"]),
         "B": ("WORKOUT HABIT", ["Start With 5 Minutes", "Every Morning"]),
         "D": ("MARTIAL ARTS", ["Every Man Should Train", "A Martial Art"])}
# B-roll colour (VIDEO-RULES 2026-10-11): measured beside the graded presenter (skin 121/75/46, rich and warm). The 8/3 kitchen clips are
# ungraded S-Cinetone and read flat (skin 135/110/78); the overcast 8/28 and 7/8 pool clips read dull. Light lifts, checked on stills.
KITCHEN = "eq=contrast=1.06:saturation=1.15:gamma=0.97"
POOL = "eq=contrast=1.05:saturation=1.10:gamma=1.06"
COVERS = {
 "A": [dict(id="cucumber", a=103.10, b=106.55, src=STOCK + "B0469.mp4", t=0.2, fx=0.5, eq=KITCHEN),        # library B0469, Dan slicing cucumber (real, 10/17 kitchen): "Taking my nutrition seriously made me look better and feel better."
       dict(id="food", a=111.22, b=115.02, src=STOCK + "B0528.mp4", t=0.0, fx=0.5),           # library B0528 (RO-05 graded) vinegar pour, replaces B0524 (first 2 s out of focus, reviewer A3); was: the film's P07, same lines as the film
       dict(id="fork", a=118.06, b="o23.40", src=STOCK + "Nutrition-B-approved-motion.mp4", t=0.0, fx=0.5, ai=(40, 336, 1.6)),   # the film's P08 (approved AI salad bite), from "Then I start with a big salad"
       dict(id="mealprep", a="o23.40", b="o24.30", src=STOCK + "B0525.mp4", t=0.0, fx=0.5),   # library B0525 (RO-05 graded): the finished salad with sealed glass meal-prep containers around it, "I meal prep". B0441 (Dan sealing containers) is out: his hair reaches the top of the source (reviewer A r1)
       dict(id="garlic", a="o24.30", b="o25.05", src=STOCK + "B0527.mp4", t=0.5, fx=0.5),     # library B0527 (RO-05 graded): gloved hand seasoning the chopped vegetables
       dict(id="lids", a="o25.05", b="o26.75", src=STOCK + "B0526.mp4", t=0.0, fx=0.5)],    # library B0526 (RO-05 graded): gloved hands pressing a lid onto a container, "...$8 or $9 a meal." (covers the take-2 join)
 "B": [dict(id="rope", a=65.18, b=67.72, src=STOCK + "B0448.mp4", t=0.5, fx=0.5),             # opener: library B0448, THE correct jump rope clip (fast skip, VIDEO-RULES 2026-10-09)
       dict(id="abwheel", a=69.03, b=75.03, src=STOCK + "B0030.mp4", t=0.0, fit="span", span=(0.30, 0.98)),           # the film's P06 (B0030 ab wheel rollouts), same lines as the film. A card the width of the rollout (x 0.30-0.98: kneeling to full extension): a vertical crop cut his head and feet off
       dict(id="kbdl", a=82.00, b=85.30, src=STOCK + "B0431.mp4", t=1.0, fx=0.5, eq=POOL),             # library B0431, kettlebell DEADLIFTS: "That's why I still work out first thing in the morning, seven days a week"
       dict(id="squats", a=55.76, b=58.40, src=STOCK + "B0460.mp4", t=0.0, fx=0.48, eq=POOL)],  # library B0460, bodyweight squats by the pool (Dan at x 0.49 of the source: fx 0.48 centres him; 0.88 showed the empty deck, reviewer B r1) (one full rep in 2.6 s; B0031 curls rest with both arms down 1.75-2.75 s): "Working out made me healthier and it made me feel better." (covers the film's own join at 55.76)
 "D": [dict(id="judo", a=246.92, b=251.52, src=STOCK + "p6254568.mp4", t=0.0, fx=0.5, fy=0.6),     # opener (first 5 s): Pexels 6254568, a full judo throw then the pin, over "I strongly believe that every man should train in some kind of martial art. Every man should be able to". Replaces Dan's promotion clip: its Instagram source cuts his hair on every frame (reviewer D r1). Covers the film's own cut at 250.28
       dict(id="group", a=218.00, b=223.55, scene="group", photo="black-belt-group.png"),      # the film's P14, his supplied group photo, original aspect (a landscape group: the card keeps every person)
       dict(id="hug", a=223.55, b=225.05, src=STOCK + "insta-hug.mp4", t=0.6, fx=0.5, fy=0.0, zoom=1.15),         # same Instagram post (source 36.4-38.8 s: arms out after the belt, then the hug; from 38.8 his hair meets the top of the source): "It also made me a better person in so many ways."
       dict(id="muaythai", a=242.50, b=244.15, src=STOCK + "p7989824.mp4", t=3.35, fx=0.5)],     # Pexels 7989824 (Muay Thai kick, native portrait): "but you can do Muay Thai,"
}
SPLIT = {
 "A": [["It'll make a huge", 0.0]],
 "B": [["Once the habit", 0.0], ["Working out has made", 0.0]],
 "D": [["It also gave me", 0.0], ["If you're in your", 0.0]],
}
SHOTS = {"A": {}, "B": {}, "D": {}}
BARS = {
 "A": [dict(id="G1", topic="Key Point", parts=[["Nothing Until 2 PM,", "for me today"], ["Then Salad And Protein", "anything until"]], a=-0.2, b=1.82),
       dict(id="G2", topic="Key Point", parts=[["Fix Your Diet First", "start taking your"], ["To Lose Belly Fat", "It's the biggest"]], a=-0.2, b=2.2)],
 "B": [dict(id="G1", topic="Key Point", parts=[["5 Minutes A Day,", "You can start"], ["Then Grow To 15", "build it up"]], a=-0.2, b=1.9),
       dict(id="G2", topic="Key Point", parts=[["Breaks Are Fine,", "never quitting"], ["Quitting Isn't", "a few months"]], a=-0.2, b=1.9)],
 "D": [dict(id="G1", topic="Key Point", parts=[["It Teaches You To Stay", "dealing with conflict"], ["Calm Under Pressure", "less frustrated"]], a=-0.2, b=1.9),
       dict(id="G2", topic="Key Point", parts=[["Your Pick: BJJ,", "start training"], ["Muay Thai Or Judo", "I personally love"]], a=-0.2, b=1.9)],
}
TEXT = {
 "A": "Believe it or not, nutrition made an even bigger impact than working out. Taking my nutrition seriously made me look better and feel better. It made me more productive. It made me more money. It was really the foundation for a lot of the other success I found. And here's what that looks like for me today. I don't eat anything until about 2pm{two p m}. Then I start with a big salad. Every meal has a large serving of meat, fish, or eggs. | I meal prep, which costs me about $8{eight} or $9{nine dollars} a meal. | That's less than ordering Chipotle. | If you're in your 20s{twenties} or 30s,{thirties} start taking your nutrition seriously right now. It's the biggest single factor in losing your belly fat. It'll make a huge impact on the rest of your life.",
 "B": "If you're watching this and you want to start working out, here's what I want you to do. Start with 5{five} minutes every day, first thing in the morning. Then step it up to 10{ten} minutes, then 15{fifteen} every day. You can start small and build it up. Once the habit is locked in, you'll be shocked at how much better your life gets. That's why I still work out first thing in the morning, seven days a week and why you should too. | Starting early and never quitting for more than a few months at a time is what let me build the body that I have today. Working out made me healthier and it made me feel better. It made me more productive and it made my dating life better. Working out has made my life better in so many ways.",
 "D": "I strongly believe that every man should train in some kind of martial art. Every man should be able to protect himself and his family, and most men today can't. | I'm really glad I dedicated about 20{twenty} years to training, invested in private lessons, and earned my black belt. It didn't just give me self-defense and martial arts skills. It also made me a better person in so many ways. It made me better at dealing with conflict. I get far less frustrated when things get complicated. It also gave me a mentality that's better in business, in relationships, and in every area of my life. If you're in your 20s{twenties} or 30s,{thirties} start training martial arts. I personally love Brazilian Jiu-Jitsu, but you can do Muay Thai, Judo or another martial art that appeals to you more. | Training will make you a better man. It'll make your life so much better.",
}
