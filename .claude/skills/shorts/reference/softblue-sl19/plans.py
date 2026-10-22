"""SL-19: three Shorts from RO-17 "3 Healthy Foods That Made Me Fat" as data. Film seconds are on the approved RO-17 round 5
master (7:32.15, sha 62187e39..., Dan "final" 2026-10-18). Dan's picks 2026-10-20: "Let's do A, C. Let's do D, but start with
'if I do snack.'" Order (my recommendation, he did not overrule): C = Short 1 (airs Mon Dec 14), A = Short 2, D = Short 3.
seg     audio pieces kept (film in, out); every edge sits in measured silence on the film's dry voice (snap.py + 20 ms levels)
covers  picture that replaces the talking shot: dict(id, a, b = film times, src + t (clip in-point) + fx/fy + fit + eq + ai (chip xy, u)
        + speed, or hf=<mov> for a film fact card rebuilt for the vertical picture area by scenes_hf.py)
split   a size step inside one continuous take, in the pause before a phrase
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets (the film's approved G06/G13/G16/G18/G25/G26/G27 copy)
text    the captions as spoken, ` | ` at each audio piece join (spellings from the film's corrected .srt); shown{spoken} for numbers"""
# R1 review: library B0047 (rotisserie spits) dropped from D: it opened on a Turkish shop sign with a lira price before "$5 at Costco"
STOCK = "/Volumes/Extreme/_edit_work/SL-19/clips/"          # copies; never read from another session's build folder at render time
HF = "/Volumes/Extreme/_edit_work/SL-19/hf/renders/"
DISC = {}
Y0 = {"full": 0, "mid": 60}        # source top row of each window (1920-space). C1713 hair top >= 100 (RO-17 hair_pre, 4K row 200): mid = 100 - 4 % of 900 ~ 64 -> 60 (verified by the hair check on the render)
KEEP = 0.90
TRIM = {}
SEG = {
 # A: "Trail" from 48.24 (silence -77 dB to 48.22, film title card T1 before it); "fat." decays by 100.52, film join 100.70
 "A": [[48.18, 100.64]],
 # C: "Coconut" from 215.84; "soda." decays 238.36 (-65 at 238.40); "I've talked about this before on the channel, but" cut: "you" from 240.86;
 # "calories." ends 242.98; "And let me tell you why." cut: "Liquid" from 245.18 (film join 245.14); "powder." decays 276.42
 "C": [[215.78, 238.76], [240.945, 243.38], [245.15, 276.48]],      # R1 review: soda. now runs to 238.76 (0.25 s pause was rushed; the film has 0.52 s); 240.945: the dip after the "but" burst (240.86-240.94); from 240.84 the delivered transcript heard "But you should" (Whisper on the cut from 240.95: "You should be avoiding")      # round-1 build check: the trimmed joins left ~0.1-0.3 s between sentences (rushed); each piece now keeps its own silence (soda. to 238.69, calories. to 243.41)
 # D: Dan's opening "If I do snack": the film's "And" is 329.33-329.49, a dip to -50/-54 dB 329.50-329.55, "If" from 329.56 (Whisper on the cut: "If I do
 # snack, I snack on something..."); "anything." decays 345.56; the sardine taste lines cut; "Number" from 357.20; "there." decays 392.70
 "D": [[329.556, 345.88], [356.95, 392.80]],      # pause at the join widened from ~0.1 s to ~0.55 s (silence 345.50-345.94 and 356.60-357.21)
}
PICKUP = {}
FADE_IN = {"D": 0.004}      # D opens 26 ms later than round-1 build (329.556): a 4 ms fade so the "If" onset is not softened; reviewer R1 heard the last 27 ms of the cut "And"
WORDFIX = {}
NAME = {"C": "short1_coconut-water-is-just-sugar-water", "A": "short2_trail-mix-more-calories-than-a-big-mac", "D": "short3_my-4-high-protein-snacks"}
TITLE = {"C": ("LIQUID CALORIES", ["Coconut Water Is", "Just Sugar Water"]),
         "A": ("THE HEALTHY SNACK TRAP", ["Trail Mix Has More", "Calories Than A Big Mac"]),
         "D": ("WHAT I SNACK ON", ["My 4 Go-To", "High-Protein Snacks"])}
COVERS = {
 "A": [dict(id="scale", a=48.18, b=51.20, src=STOCK + "A3.mp4", t=0.0, fit="span", span=(0.135, 0.97), y=480, ai=(40, 500, 1.6)),     # a card, with a reason: the gag needs both pans (burger x 0.18-0.38, trail mix pan 0.56-0.95 as it sinks); a fill crop shows only the post      # the opener (first 5 seconds): the film's approved AI opener A3 (trail mix outweighs a cheeseburger), moved here
       dict(id="hikers", a=51.20, b=55.51, src=STOCK + "p4763784.mp4", t=3.0, fx=0.5),                 # the film's C02: "what people eat when they go hiking"
       dict(id="G04", a=58.422, b=65.172, hf=HF + "A_G04.mov"),                                        # the film's G04 fact card: 1 serving = 3 tbsp, 170 calories
       dict(id="couch", a=75.954, b=81.254, src=STOCK + "A2.mp4", t=0.0, fx=0.5, ai=(40, 336, 1.6)),   # the film's A2: "you keep reaching into the bag"
       dict(id="G05", a=81.254, b=88.875, hf=HF + "A_G05.mov")],                                       # the film's G05: 1 cup = 700 calories, more than a Big Mac
 "C": [dict(id="coconut", a=215.78, b=221.647, src=STOCK + "p8249559.mp4", t=0.343, fx=0.5, eq="eq=contrast=1.08:saturation=1.25"),   # the opener: the film's C10 (a man drinking from a coconut)
       dict(id="G15", a=228.477, b=235.8361, hf=HF + "C_G15.mov"),                                     # the film's G15: the 1-liter carton, 180 calories, 40 g sugar (AI image, chip)
       dict(id="soda", a=235.8361, b=238.76, src=STOCK + "B0408.mp4", t=25.0, fx=0.5),                 # the film's C11: "just as bad as soda"
       dict(id="marathon", a=254.257, b=259.947, src=STOCK + "p28569519.mp4", t=0.3, fx=0.5, eq="eq=contrast=1.08:saturation=1.30"),     # the film's C12
       dict(id="powder", a=262.614, b=266.75, src=STOCK + "p13662132.mp4", t=0.5, fx=0.5)],           # the film's C14: drink mix stirred into water; runs to 266.75 so the shot of Dan opens on "I drank", not 0.3 s of open mouth (watch judge R1)
 "D": [dict(id="sardineman", a=329.556, b=331.47, src=STOCK + "A10.mp4", t=0.0, fx=0.52, ai=(40, 336, 1.6)),     # the opener: the film's A10, frames 0-46 only (him eating the sardine; cut between "that's" and "high"): frame-reviewer FAILED 0-59 (f52-59 the tin swings across his chin as a blur and leaves the crop); fx 0.52 shows more of the fork hand; clipcheck failed 0-97 where the tin is set on the sofa back (f60-84); cut to the part before it
       dict(id="tin", a=334.991, b=337.271, src=STOCK + "B0501.mp4", t=0.5, fx=0.6),                   # the film's C16: "Number one, sardines"
       dict(id="fork", a=342.89, b=345.88, src=STOCK + "p6398604.mp4", t=3.0, fx=0.55),                 # the film's C17 (fork lifting a fish), moved onto "about $2 a can ... don't have to cook anything"
       dict(id="egg", a=356.95, b=359.392, src=STOCK + "B0046.mp4", t=1.54, fx=0.55),                   # the film's C18: "Number 2, hard boiled eggs"
       dict(id="chicken", a=375.306, b=377.276, src=STOCK + "B0443.mp4", t=0.5, fx=0.55),               # the film's C19: Dan's hands pulling the chicken apart
       dict(id="G28b", a=380.006, b=387.9209, hf=HF + "D_G28b.mov")],                                  # the film's G28b: the Chipotle cup, 180 calories, 32 g protein (AI image, chip)
}
SPLIT = {"A": [["And let's keep it", 0.0]],                       # size steps inside long continuous takes, in the pause before a phrase
         "C": [["You just add the", 0.0], ["but these days", 0.0]],
         "D": [["Or buy pre-packaged", 0.0], ["Number 3", 0.0]]}      # "Number 3": a size step where the rotisserie clip was (R1 review dropped it); the $5 bar lands on the wide window
SHOTS = {"A": {9: dict(win="mid"), 10: dict(win="full")},       # every key-point bar sits on the wide window; sizes still alternate at every same-camera cut
         "C": {4: dict(win="mid"), 5: dict(win="full"), 6: dict(win="mid"), 11: dict(win="mid"), 12: dict(win="full")},
         "D": {}}
BARS = {
 "A": [dict(id="G06", topic="The Trap", parts=[["A 700-Calorie", "700 calories of"], ["'Healthy' Snack", "healthy trail mix"]], a=-0.2, b=2.6)],
 "C": [dict(id="G13", topic="Coconut Water", parts=[["Really, It's SUGAR WATER.", "really it's sugar"]], a=-0.2, b=3.0),
       dict(id="G16", topic="Liquid Calories", parts=[["Skip Them.", "Liquid calories don't"], ["They Don't Fill You Up.", "don't fill you up"]], a=-0.02, b=2.4),
       dict(id="G18", topic="My Swap", parts=[["Zero-Calorie Electrolytes Instead", "these days"]], a=-0.2, b=4.6)],
 "D": [dict(id="G25", topic="1. Sardines", parts=[["18 g Protein. 0 Carbs.", "18 grams"]], a=-0.2, b=4.75),
       dict(id="G26", topic="2. Hard-Boiled Eggs", parts=[["2 Eggs: 150 Calories,", "Two eggs"], ["12 g Protein", "12 grams"]], a=-0.05, b=2.6),
       dict(id="G27", topic="3. Rotisserie Chicken", parts=[["$5 At Costco.", "$5"], ["Already Cooked.", "already cooked"]], a=-0.2, b=0.75)],
}
TEXT = {
 "A": "Trail mix has a great reputation. It's nuts and fruit. It's what people eat when they go hiking, so everyone assumes it has to be good for you. But go look at the label. A serving of trail mix is 3{three} tablespoons and those 3{three} tablespoons are about 170{one hundred seventy} calories and 14{fourteen} grams of carbs. Now go and measure out 3{three} tablespoons. It's one small handful. And let's keep it real, you're not eating one small handful of trail mix and then putting the bag away. I know I wasn't. What really happens is you're watching TV{t v} or you're working at your desk and you keep reaching into the bag. One cup of trail mix is about 700{seven hundred} calories and 65{sixty five} grams of carbs. That's more calories than a Big Mac. And that was just a snack in between meals and you thought you were being healthy the whole time. That's how you become the average American, eating 700{seven hundred} calories of healthy trail mix at your desk and wondering why you're still fat.",
 "C": "Coconut water is sold as a natural, healthy way to hydrate because it has electrolytes and it has potassium, but really it's sugar water. One of the normal-sized cartons is about 90{ninety} calories and 20{twenty} grams of sugar and a lot of people buy the big one-liter carton and drink it throughout the day. That's about 180{a hundred and eighty} calories and 40{forty} grams of sugar. So in my opinion it's just as bad as soda. | you should be avoiding all liquid calories. | Liquid calories don't fill you up, so you don't eat any less to make up for it. You just add the drink on top of everything else you ate for the day. And you don't need it. Unless you're running a marathon in the heat, you're not so low on potassium that you need to drink sugar to fix it. Just drink water. And if you want the electrolytes, get a zero-calorie electrolyte powder and put a scoop of that in your water. I drank large amounts of coconut water for years thinking I needed it to stay hydrated, but these days I stay just as hydrated or better from using a zero-calorie electrolyte powder.",
 "D": "If I do snack, I snack on something that's high in protein and low in carbs. Here's what I eat. Number 1{one}, sardines. A can of sardines is about 18{eighteen} grams of protein and zero carbs, and you're getting your omega-3s{omega threes} at the same time. They're about $2{two dollars} a can and you don't have to cook anything. | Number 2{two}, hard-boiled eggs. Two eggs are about 150{a hundred and fifty} calories and 12{twelve} grams of protein. You can boil a dozen of them on Sunday and you have snacks for the whole week. Or buy pre-packaged hard-boiled eggs like I do to make it easy. Number 3{three}, rotisserie chicken. It's $5{five dollars} at Costco and it's already cooked. You just pull some off and eat it. And number 4{four}, the protein cups from Chipotle. It's just a cup of chicken or steak with nothing else in it. The chicken one is about 180{a hundred and eighty} calories and 32{thirty two} grams of protein and it costs about $7{seven dollars}. If you're out running around and you get hungry, I would say that's the best fast food snack out there.",
}
