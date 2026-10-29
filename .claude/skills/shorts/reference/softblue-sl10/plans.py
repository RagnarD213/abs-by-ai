"""SL-10: four Shorts from RO-13 "Can You Drink Alcohol And Still Have Abs?" as data. Film seconds are on the RO-13 round 2 master
(7:10.63, sha 2296902b). Dan's picks 2026-10-29: "Let's do A, but ... start with 'When you drink alcohol, it should taste bad' ...
then go to 'Kill the sugary mixers' and all that content on top, and then eliminate the 'drink water' content at the end."
"B, but eliminate ... 'A real night out ...' [and] 'One drinking occasion a week ... take the edge off.' See if there's some additional
content you can put at the end as well to fill out that short." "D ... Start it with 'Your last drink should be 3 hours before you go
to bed,' and then ... put everything [from] before the skip after that." "Let's make E as is."
seg     audio pieces kept (film in, out); every edge sits in measured silence on the film's dry voice (snap.py)
covers  picture that replaces the talking shot: dict(id, a, b = film times or "o<sec>" output times, src + t (clip in-point) + fx/fy
        + fit + eq + ai (chip xy, u) + speed)
split   a size step inside one continuous take, in the pause before a phrase
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets
text    the captions as spoken, ` | ` at each audio piece join (spellings from the film's corrected .srt)"""
STOCK = "/Volumes/Expansion/_edit_work/SL-10/clips/"          # copies; never read from another session's build folder at render time
DISC = {}
Y0 = {"full": 73, "mid": 78}      # C1707 hair top min 118 (track.json, A/B/D/E): full 676x1007 from y 73, mid 580x865 from y 78 (72-74 px over his hair on the 1610 picture)
KEEP = 0.90
TRIM = {}
VIRT = []
SEG = {
 # A: "When" 198.90 (silence 198.52-198.87) .. "dessert." 221.42 (silence 221.48-221.91; film join 221.72);
 #    "kill" ~185.07 (silence 184.59-185.07, "three," ends 184.56) .. "lime." 196.38 (silence 196.47-196.92). Pause at the join ~0.55 s.
 "A": [[198.70, 221.70], [184.80, 196.60]],
 # B: "The" 231.73 (silence 231.33-231.73) .. "noticed." 261.86 (film join 262.00; "rule" from ~262.08: the 2-frame tail folds);
 #    "The reason" 163.89 (silence 163.71-163.89, film join 163.80: 3 frames of the outgoing take fold into the shot) .. "tracking." 178.76 (silence 178.84-179.00)
 "B": [[231.50, 262.05], [163.80, 178.90]],      # reviewer B r1: from 163.70 a 90 ms tail of "evening" (the removed line) sat in the pause; the film is silent from 163.79. Pause now ~0.27 s (his own range in this film: 0.22-0.8 s)
 # D: "your" 263.24 (silence 262.87-263.24) .. "bed" 266.36 (silence 266.43-266.94); "And" 66.63 (silence 66.15-66.63) .. "anything." 89.36
 #    (silence 89.44-89.64, film join 89.56); "This" 266.94 .. "early." 284.12 (silence 284.20-284.57)
 "D": [[263.05, 266.62], [66.40, 89.52], [266.80, 275.83], [279.80, 284.35]],      # reviewer D r1: "This one sounds annoying, but it's the single highest return rule on the list." pointed back at the film's list: cut ("you." ends 275.75, film join 275.84; "Same" from 280.03, silence 279.57-280.03)
 # E: "I" ~370.59 (silence 370.34-370.59) .. "struggling." 410.60 (silence 410.67-410.86, film join 410.78)
 "E": [[370.45, 410.76]],
}
PICKUP = {}
WORDFIX = {}
NAME = {"A": "short1_your-drinks-should-taste-bad", "B": "short2_your-nightly-wine-is-killing-your-abs",
        "D": "short3_stop-drinking-3-hours-before-bed", "E": "short4_what-killed-my-urge-to-drink"}
TITLE = {"A": ("DRINKING", ["Your Drinks Should", "Taste Bad"]),
         "B": ("DRINKING", ["Your Nightly Wine Is", "Killing Your Abs"]),
         "D": ("SLEEP", ["Stop Drinking 3 Hours", "Before Bed"]),
         "E": ("MY STORY", ["What Killed My", "Urge To Drink"])}
# B-roll colour (VIDEO-RULES 2026-10-11): each clip measured beside the graded presenter (grade.py), real curves with true blacks
G = {'cocktails': "curves=all='0/0 0.06/0.045 0.5/0.5 1/1',eq=saturation=0.95", 'soda': "curves=all='0/0 0.5/0.48 1/1',eq=saturation=1.10", 'margarita': "curves=all='0/0 0.5/0.47 1/0.98',eq=saturation=0.80,colorbalance=rm=-0.04:bm=0.03", 'beers': "curves=all='0/0 0.38/0.24 0.75/0.68 1/0.96',eq=saturation=1.10", 'bartender': "curves=all='0/0 0.5/0.5 1/1',colorbalance=rm=0.03:bm=-0.03", 'whiskey': "curves=all='0/0 0.25/0.29 1/1'", 'bed': "curves=all='0/0 0.25/0.33 0.6/0.68 1/1',eq=saturation=0.90", 'ring': "curves=all='0.06/0 0.5/0.46 1/0.97',eq=saturation=1.05", 'asleep': "curves=all='0.10/0 0.5/0.45 1/1',eq=saturation=1.25,colorbalance=rm=0.03:bm=-0.02", 'cheers': "curves=all='0.03/0 1/1'", 'date': "curves=all='0.03/0 1/1',eq=saturation=0.92", 'club': "curves=all='0.04/0 1/1'", 'winepour': "curves=all='0/0 0.5/0.47 1/0.97',eq=saturation=1.05"}
COVERS = {
 "A": [dict(id="cocktails", a=190.06, b=193.25, src=STOCK + "p8942658.mp4", t=1.0, fx=0.92, eq=G["cocktails"]),      # the film's C09: the red sugared cocktail (fx 0.92: a fill window holds one glass while the camera pans; clip 1.0-4.2 s: sharp before the focus pull at ~4.5, reviewer A r1), "Alcohol and liquid sugar at the same time"
       dict(id="soda", a=193.25, b=196.60, src=STOCK + "p10014741.mp4", t=5.0, fx=0.50, eq=G["soda"]),          # the film's C10: soda water with lime, "You want dry wine or spirits with soda water and lime"
       dict(id="margarita", a=214.32, b=221.70, src=STOCK + "p7603355.mp4", t=6.0, fx=0.45, eq=G["margarita"])],     # the film's C11: margarita poured into a salt-rimmed glass, "Most guys don't have six margaritas ..."
 "B": [dict(id="fact", a=236.77, b=249.87, src=STOCK + "wine_fact.mov", t=0.0),                     # the film's G15 (1,700 calories), the approved fact card rebuilt at 1080 x 1610 (factcard.py)
       dict(id="beers", a=169.60, b=170.73, src=STOCK + "p5240991.mp4", t=2.0, fx=0.45, eq=G["beers"]),          # the film's C07, three hard cuts: "in their beers, their cocktails, and the liquor they drank"
       dict(id="bartender", a=170.73, b=171.86, src=STOCK + "p11268027.mp4", t=3.0, fx=0.40, eq=G["bartender"]),
       dict(id="whiskey", a=171.86, b=173.00, src=STOCK + "p14058816.mp4", t=2.0, fx=0.40, eq=G["whiskey"])],
 "D": [dict(id="bed", a=263.05, b=266.62, src=STOCK + "p6944077.mp4", t=2.0, fx=0.95, eq=G["bed"]),            # opener, the film's C02: the nightstand at night, 4:40 on the alarm clock beside a glass of whiskey (fx 0.95; reviewer D r1: the man alone lost what the clip is about)
       dict(id="ring", a=73.49, b=79.05, src=STOCK + "A0205.mp4", t=0.0, fx=0.5, ai=(40, 336, 1.6), eq=G["ring"]),   # library A0205 (AI, used in SL-09 Oura shorts): a smart ring on a hand on white sheets, "I can see it on my Oura ring"
       dict(id="asleep", a=269.00, b=273.00, src=STOCK + "B0333.mp4", t=1.8, fx=0.92, eq=G["asleep"]),            # library B0333: a man asleep, "the less of your deep sleep it takes from you"
       dict(id="cheers", a=279.80, b=284.35, src=STOCK + "B0499.mp4", t=0.5, fx=0.55, eq=G["cheers"])],           # library B0499: friends clinking beers in a bar, "Same number of drinks, same night out, ... stop early"
 "E": [dict(id="date", a=375.95, b=377.23, src=STOCK + "B0318.mp4", t=1.0, fx=0.50, eq=G["date"]),              # library B0318: a couple toasting with wine at dinner, "1 or 2 on a date"
       dict(id="club", a=377.23, b=382.99, src=STOCK + "p9003382.mp4", t=0.5, fx=0.50, eq=G["club"]),           # the film's C17: crowd at a club, "a blowout party night ... Those blowout nights are gone."
       dict(id="cheers", a=387.13, b=389.74, src=STOCK + "B0499.mp4", t=0.5, fx=0.55, eq=G["cheers"]),        # library B0499: friends clinking beers, "Now when I go out, I have one or two,"
       dict(id="winepour", a=393.19, b=396.21, src=STOCK + "p7687087.mp4", t=4.76, fx=0.50, eq=G["winepour"])],                  # the film's C12 red wine pour, "Taking Zepbound massively reduced my desire to drink alcohol." (reviewer E r1: B0348 was a glucose kit, not a pen; no real pen clip in the library, so he stays on camera for the recommendation)
}
SPLIT = {"A": [["When alcohol tastes good", 0.0]], "B": [["If you are counting", 0.0]], "D": [["more hunger the next", 0.0]],
         "E": [["Now when I go out", 0.0], ["It helped me tremendously", 0.0]]}      # a size step inside long talking runs (10 s+)
SHOTS = {"A": {}, "B": {}, "D": {}, "E": {}}
BARS = {
 "A": [dict(id="G1", topic="Key Point", parts=[["Bitter Beats Sweet", "drink alcohol"], ["Less Sugar Per Glass", "taste bad"]], a=-0.2, b=2.85),
       dict(id="G2", topic="Key Point", parts=[["Bad Taste Is", "drinking bad tasting"], ["A Built-In Brake", "You drink less"]], a=-0.2, b=1.9),
       dict(id="G3", topic="Key Point", parts=[["Mixers Are", "Cocktails and sugary"], ["Liquid Dessert", "sugary mixed"]], a=-0.2, b=2.1)],      # reviewer A r1: G1/G2 echoed the captions; the practical half had no bar
 "B": [dict(id="G1", topic="Key Point", parts=[["Wednesday Beers", "Wednesday beers"], ["Count Too", "doing the same thing"]], a=-0.2, b=1.9),
       dict(id="G2", topic="Key Point", parts=[["Untracked Drinks", "Those calories count"], ["Still Count", "write them down"]], a=-0.2, b=1.9)],
 "D": [dict(id="G1", topic="Key Point", parts=[["Passing Out Fast", "knocks you out"], ["Isn't Real Sleep", "Falling asleep"]], a=-0.2, b=2.4),
       dict(id="G2", topic="Key Point", parts=[["Stop Early,", "cleared"], ["Keep Your Deep Sleep", "the less of"]], a=-0.05, b=2.6)],
 "E": [dict(id="G1", topic="Key Point", parts=[["Then: Blowout Nights", "I used to drink"], ["Every Single Week", "most weeks"]], a=-0.2, b=2.15),      # reviewer E r1: distil, not echo
       dict(id="G2", topic="Key Point", parts=[["It Was Zepbound,", "Realistically"], ["Not Willpower", "the willpower"]], a=-0.2, b=2.4)],
}
TEXT = {
 "A": "When you drink alcohol, it should taste bad. If it tastes bad, it is not sugary. And drinking bad tasting drinks has a second benefit that's even more important. You drink less. When alcohol tastes good, you will keep drinking it even when you do not want to get any drunker. Most guys don't have six margaritas because they wanted to be six drinks drunk. They had six because they tasted like dessert. | Kill the sugary mixers. Cocktails and sugary mixed drinks are a double hit. Alcohol and liquid sugar at the same time. You want dry wine or spirits with soda water and lime.",
 "B": "The nightly glass of wine is the one I want to call out because people defend it the hardest. Two glasses a night is 14{fourteen} glasses a week. That is somewhere around 1,700{seventeen hundred} calories plus 7{seven} nights of degraded sleep, every week, forever. There is no version of that where you get abs. And be honest about what the occasion actually is. If you are counting the Wednesday beers as not really drinking because there was only 2,{two} you are doing the same thing you do with your food. You're only counting the times you noticed. | The reason why a lot of guys fail to lose their belly fat is they only count what they're eating, but they don't count the calories in their beers, their cocktails, and the liquor they drank. Those calories count whether you write them down or not. Your body does not care that you did not feel like tracking.",
 "D": "Your last drink should be at least 3{three} hours before you go to bed. | And I know a lot of you are about to argue with me because alcohol knocks you out faster. Falling asleep quickly is not high quality sleep. Alcohol wrecks your sleep quality and I can see it on my Oura ring every single time I drink. Deep sleep collapses, heart rate stays elevated all night and bad sleep means worse recovery, more hunger the next day, and less willpower to say no to anything. | This is the sleep protection rule. The further the alcohol is from your bedtime, the more of it your body has already cleared, and the less of your deep sleep it takes from you. | Same number of drinks, same night out, you just frontload it and stop early.",
 "E": "I used to drink 5-10{five to ten} drinks per week, and most weeks it was closer to 10.{ten} 1{one} or 2{two} on a date, then a blowout party night once or twice a week where I would have 4{four} to 6.{six} Those blowout nights are gone. Not because I forced myself, they stopped appealing to me. Now when I go out, I have one or two, and then I'm done, and I genuinely don't feel like I'm missing anything. Taking Zepbound massively reduced my desire to drink alcohol. If you're struggling to reduce your drinking, I encourage you to try Zepbound to get this habit under control. Realistically, I probably would not have had the willpower to cut down on drinking if I had not gone on Zepbound. It helped me tremendously, and it can probably help you too if you're struggling.",
}
