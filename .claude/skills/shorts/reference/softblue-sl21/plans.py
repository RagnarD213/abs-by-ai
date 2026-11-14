"""SL-21: three Shorts from RO-20B "What To Cut To Afford Getting In Shape" as data. Film seconds are on the APPROVED RO-20B round 4
master (9:28.5, sha 88a6314f, Dan finalized 2026-10-20). Picture: the film's own graphics-free base.mp4 (same frames and clock).
Dan's picks 2026-11-13: A (restaurants, Short 1), D (vacation, Short 2), E (therapy, Short 3), titles as proposed.
seg     audio pieces kept (film in, out); every edge sits in measured silence on the master's own mix (snap.py, 10 ms levels)
covers  picture that replaces the talking shot: dict(id, a, b = film times, src + t (clip in-point) + fx/fy + fit + eq)
        Every cover is the film's own approved cutaway unless its comment says NEW. 25 fps stock is conformed frame for frame to
        29.97 (prep_clips.py; never the fps filter: it repeats every fifth frame, DS-49), so t is on the conformed file.
bars    key-point lower thirds: topic, [[line, phrase it lands on]], a/b offsets
text    the captions as spoken (the film's corrected words), ` | ` at each audio piece join; `shown{spoken}` for the aligner"""
CL = "/Users/danielrose/Projects/_edit_work/SL-21/clips/"
DISC = {}
MASTER_CUTS = []
Y0 = {"full": 0, "mid": 0}                  # roll C1511 framed the top of his hair at the frame edge (RO-20 round 1, reported unfixable): no headroom to give
KEEP = 0.90
TRIM = {}
SEG = {
 # A: "restaurants." ends 244.68, silence 244.87-245.20, "A" 245.20. "extent." ends 291.33 (silence 291.33-291.59); the film's camera cut is at
 # 291.525, so piece 1 ends 291.50. "If" onset 318.25 (silence 317.52-318.25; camera cut 317.751): piece 2 from 317.95, so the pause at the join is
 # 0.17 + 0.30 = 0.47 s. "health." ends 323.58, silence to 323.82.
 "A": [[245.05, 291.50], [317.95, 323.80]],
 # D: "vacation." ends 376.47, silence 376.56-376.87, "Now" 376.87 (-22 dB): no dip between "Now" and "I" (377.10 -10 dB), so "Now" stays.
 # "in." ends 428.07, silence 428.08-428.35; the camera cut is at 428.295: the Short ends 428.27.
 "D": [[376.70, 428.27]],
 # E: "medication." ends 448.27, silence 448.30-448.82 (camera cut 448.315), "Now," 448.82 runs into "I'm" (no dip): it stays.
 # "priority." ends 498.29, silence 498.30-498.52; the camera cut is at 498.431, so the Short ends 498.42 (the word has decayed to -49 dB by 498.33).
 "E": [[448.60, 498.42]],
}
PICKUP = {}
NEG = {      # what each Short shows, for the gate plan's negative-events record (deliver.py)
 "A": "the footage is Dan in a black tank top talking in his kitchen, the film's approved stock (a restaurant table, a card going into a card reader, cooks plating at the pass, a smoking pan, noodles tossed over a flame) and Dan's own B-roll measuring vinegar over a salad; no AI clips, no app screens, no belly framing or pinching",
 "D": "the footage is Dan in a black tank top talking in his kitchen, the film's approved stock (holidaymakers on a beach from a drone, a resort buffet, a piled plate, pancakes, a loaded restaurant table) and Dan's own B-roll doing push-ups beside a pool (shirtless, exercising, not a result picture); no AI clips, no app screens, no belly framing or pinching",
 "E": "the footage is Dan in a black tank top talking in his kitchen, the film's approved stock (a counseling session, a person seen from behind walking into a gym, loose pills with no names) and Dan's own B-roll doing pull-ups in a gym; no AI clips, no app screens, no belly framing or pinching",
}
PATCH = {}
WORDFIX = {"A": [("oh,", 1.64, 1.59, 1.89), ("I", 1.84, 1.92, 1.98)]}      # CTC scored "oh," 0.0: measured levels put "oh" at film 246.63-246.93 and "I" from 246.97 (dip 246.95)
NAME = {"A": "whattocut-short1_restaurants-dont-care-about-your-fitness-goals",
        "D": "whattocut-short2_you-dont-deserve-a-vacation-until-youre-ripped",
        "E": "whattocut-short3_if-you-cant-afford-a-gym-you-cant-afford-therapy"}
TITLE = {"A": ("EATING OUT", ["Restaurants Don't Care", "About Your Fitness Goals"]),
         "D": ("VACATIONS", ["You Don't Deserve A Vacation", "Until You're Ripped"]),
         "E": ("THERAPY VS THE GYM", ["If You Can't Afford A Gym,", "You Can't Afford Therapy"])}
_DARK = "curves=all='0/0 0.06/0.09 0.20/0.32 0.50/0.66 1/1'"      # the film's own stock grade (films_r4.STOCK_GRADE)
COVERS = {
 "A": [dict(id="Cd08", a=245.05, b=246.59, src=CL + "Cd08.mp4", t=0.0, fx=0.88),      # film Cd08 (Pexels): a restaurant table crowded with plates, a diner serving herself. The Short OPENS on it (first 5 seconds: the restaurant under the title), held through "they're like," to the dip before "oh, I don't have the money" (246.55-246.61, -33 dB; the film cut back at 246.31, inside "they're")
       dict(id="Cd09", a=250.717, b=255.222, src=CL + "Cd09.mp4", t=0.0, fx=0.52),    # film Cd09 (Pexels): a card goes into the card reader ("But you look at their credit card statement ... three times per week")
       dict(id="Cd10", a=269.736, b=276.977, src=CL + "Cd10.mp4", t=0.0, fx=0.50),    # film Cd10 (Pexels): cooks plating at the pass ("They just want you to have a delicious meal ... how the meal tastes")
       dict(id="Cd11a", a=280.10, b=283.467, src=CL + "Cd11a.mp4", t=0.0, fx=0.50, eq=_DARK + ",eq=saturation=1.25"),      # film Cd11, shot 1 (Pexels): a chef pours fat into a smoking pan ("loaded with much more butter")
       dict(id="Cd11b", a=283.467, b=286.753, src=CL + "Cd11b.mp4", t=0.0, fx=0.50),  # film Cd11, shot 2 (Pexels): noodles tossed over a flame while oil goes in ("unhealthy fats and sugar, unhealthy carbs"); the film splits the slot evenly
       dict(id="Cd13", a=320.554, b=323.80, src=CL + "Cd13.mp4", t=0.0, fx=0.47, eq="curves=all='0/0 0.0701/0.0842 0.2805/0.3822 0.5316/0.7242 0.9759/0.9759 1/1'")],      # film Cd13 (library B0528, Dan's own B-roll): Dan measures vinegar over his salad ("reinvest in your health"); the Short ends on it
 "D": [dict(id="Cd18", a=376.70, b=379.312, src=CL + "Cd18.mp4", t=13.5, fx=0.55),      # R1b (reviewer D): the aerial part of the same clip (the drone high over the beach, sunbeds and the waterline), not its ground-level opening on one sunbather     # film Cd18 (Pexels): a drone lifts off over holidaymakers on a white beach. The Short OPENS on it (first 5 seconds) and cuts to Dan where the film does
       dict(id="Cd19a", a=386.987, b=389.84, src=CL + "Cd19a.mp4", t=1.0, fx=0.70, eq="curves=all='0/0 0.08/0.03 0.3/0.42 0.55/0.72 1/1',eq=saturation=1.1"),      # R1b (reviewer D): lifted (luma 83 with no blacks against 124-135 on the talking shots); ends in the gap after "rules"   # film Cd19, shot 1 (Pexels): a resort breakfast buffet ("When you go on vacation, the usual rules ...")
       dict(id="Cd19b", a=389.84, b=393.193, src=CL + "Cd19b.mp4", t=0.0, fx=0.58),   # film Cd19, shot 2 (Pexels): a guest's plate piled high over the buffet trays ("... go out the window")
       dict(id="Cd20", a=395.44, b=399.032, src=CL + "Cd20.mp4", t=0.5, fit="span", span=(0.18, 0.82), eq="eq=saturation=1.15"),      # film Cd20 (library B0461, Dan's own B-roll): push-ups beside the pool ("I work out every morning"); a horizontal pose is a card, his whole body in it
       dict(id="Cd21", a=408.074, b=411.544, src=CL + "Cd21.mp4", t=0.0, fx=0.53),      # R1b: conformed copy (repeats removed), t=0 is the film's in-point    # film Cd21 (Pexels): chocolate syrup over a stack of pancakes ("breakfast every morning of pancakes")
       dict(id="B0326", a=414.15, b=416.60, src=CL + "B0326.mp4", t=1.0, fx=0.77)],      # R1b (reviewer D): the crop sits on the beer, the two cocktails and the plates (it was on one aubergine plate)   # NEW in the Short (library stock B0326, the film's own Cd12 clip at 5:12): a sunny restaurant table loaded with steak, fries, beer and cocktails, on "per week that I was on vacation"; B-roll share 36 %
 "E": [dict(id="Cd24", a=461.10, b=467.133, src=CL + "Cd24.mp4", t=1.45, fx=0.55),      # R1b (reviewer E): from 1.45 s, after the stock's fast opening tilt (its frames step unevenly there)    # film Cd24 (Pexels): a counseling session, the therapist's clipboard in the foreground
       dict(id="Cd25", a=467.133, b=471.004, src=CL + "Cd25.mp4", t=1.0, fx=0.56),    # film Cd25 (Pexels): from behind, a person in a tank top with their hair in a bun walks onto a gym floor ("than having a gym membership")
       dict(id="Cd26", a=474.674, b=478.178, src=CL + "Cd26.mp4", t=0.0, fx=0.50),      # R1b (reviewer E): its captions sit in the empty felt above the pills (SHOTS cap)    # film Cd26 (Pexels): a slow slide past loose capsules and tablets, no names
       dict(id="B0642", a=478.178, b=482.80, src=CL + "B0642.mp4", t=0.0, fx=0.52, eq="curves=all='0/0 0.25/0.31 0.5/0.58 0.75/0.81 1/1'")],      # R1b (reviewer E): midtones lifted (his skin read 96 in the gym against 130 in the kitchen)  # NEW in the Short (library B0642, October 23 gym shoot, Color C): Dan doing pull-ups, full body, on "if you have great physical health, attaining great mental health will be much easier"; straight from the pills clip on "On the other hand"; B-roll share 35 %
}
SPLIT = {"A": [],
         "D": [("Before I have this routine,", 0.0)],      # R1c (reviewers D, both rounds): no second punch-in on the closing line: he steps sideways right after it and the close crop had to pan
         "E": [("And in my opinion,", 0.0)]}      # no second step in the closing wide shot: a caption would straddle it
# Windows: the film's wide camera (W, the whole 1920 frame) and its 1.3x close crop (T) keep their native size step in the full window;
# where two same-size shots meet (an audio join, a SPLIT inside one take), the second goes to the mid window (1.2x punch-in).
SHOTS = {"A": {2: dict(cap=600), 4: dict(win="full"), 5: dict(cap=400), 8: dict(cap=400), 11: dict(cap=400)},      # R1c (reviewer A): 90 px under the title band; the closing clip's captions also go up (they covered the measuring spoon)      # R1b (reviewer A): captions over the card reader (#2), the cooks' hands (#5) and the noodles (#8) move up into empty picture                       # W #3 -> T #4 is already a real size step
         "D": {},      # the table clip keeps its captions low: the drinks (its subject) fill the top of the crop
         "E": {5: dict(cap=560), 8: dict(win="full")}}      # the pull-up clip keeps its captions in the standard place: they cross his shins on the low half of a rep, the bar, arms and torso stay clear (two-line captions do not fit the floor under his feet)  # T #7 -> W #8 (full) is the film's own size step
# Key-point bars sit only on the film's WIDE shots in the full window: on its close shots his chin reaches canvas y 1175-1300 (track.json
# face bottoms 580-664 px), under the bar's top at 1130; on the wide shots it stays at 1023-1029.
BARS = {
 "A": [dict(id="G1", topic="KEY POINT", parts=[["The Gym Money", "And they're like,"], ["Is Going To Restaurants", "I just need a treat"]], a=-0.2, b=3.6)],      # the film's own Gd09 line, on the first wide shot after the card clip
 "D": [dict(id="G1", topic="KEY POINT", parts=[["Get Ripped First", "But you don't deserve"], ["Then Take The Trip", "You deserve a break once"]], a=-0.2, b=2.3)],      # distils the film's Gd18 / Gd21 key points without repeating the title
 "E": [dict(id="G1", topic="KEY POINT", parts=[["Not Forever", "I'm not telling you"], ["Until You're In Great Shape", "until you get in great shape"]], a=-0.2, b=2.0)],      # the film's own Gd26, on the same wide shot
}
TEXT = {
 "A": "A lot of people I_know,{I know} they're like, oh, I don't have the_money{the money} / to get in shape,_Dan.{shape Dan} I don't have the_money{the money} for a gym membership. "
      "But you look at_their{at their} / credit card statement, and they're eating out at restaurants / two or three times per week. "
      "And they're like, oh, well, I just need a treat for myself every once in a while. But you don't need a treat for yourself. And here's why. "
      "When you're going to restaurants, they don't care about your long-term fitness goals. They only care about making you happy in the moment. "
      "They just want you to have a delicious meal. They want you to have a five-star Google review, and they just care_about{care about} / how the meal tastes, not its nutritional value. "
      "Because of that, the food at restaurants is usually loaded with much more butter, unhealthy fats and sugar, unhealthy carbs and those type of things "
      "that you would never load up your own food at home to that extent. | "
      "If you sacrifice to restaurants for just a few weeks, that will free up hundreds of dollars that_you{that you} could reinvest in your health.",
 "D": "Now I know / some of you guys / aren't gonna like hearing this. You're like, I need a vacation. I deserve a break because I work hard. "
      "But you don't deserve a break. You deserve a break once you're ripped. And let me tell you why. "
      "When you go on vacation, the usual rules / of working out and eating / for most people / go out the window. "
      "Now, I've been able to establish a good routine where I work out every morning / and I fast / until 2pm{two p m} every day. "
      "Despite doing that though, I usually do gain / 2_or_3_pounds{two or three pounds} of fat / for each week / I'm on vacation. "
      "Before I have this routine, when I didn't work out, when I ate breakfast every morning of pancakes and whatever I ate, "
      "I would gain / 5_or_6_pounds{five or six pounds} of fat / per week / that_I{that I} was on vacation. "
      "So before you establish good health habits, vacation is toxic to your fitness goals. "
      "You can enjoy / those vacations eventually, but it's going to be / way more enjoyable / when you're ripped / and when you have + your + health + habits / dialed in.",
 "E": "Now, I'm not a psychologist, obviously this is not medical advice, but this is my opinion. "
      "And in my opinion, if you don't have enough money for a gym membership, you have no business spending money on therapy or psychiatric medication. "
      "Now, I'm not even claiming that that stuff does you no good. That's a whole / different discussion. "
      "The discussion / that we're having is, is that doing you more good than having a gym membership if you're broke? I don't think it is. "
      "If your health isn't there, no amount of therapy, no amount of medication is ever going to make you have good mental health. "
      "On the other hand, if you have / great physical health, / attaining + great + mental + health / will be much easier, even if you have to sacrifice the therapy and the medication. "
      "Now again I'm not telling you / you've got to + sacrifice + that / permanently. I'm just telling you to sacrifice that / until you get in great shape, "
      "and you have the productivity / to make more money, and eventually / you can reinvest in_that{in that} / once you've taken care / of the higher priority.",
}

# ---- Round 2 (2026-11-13): Dan approved Short 3 as is, and Shorts 1 and 2 except one new lip-synced AI excuse clip each.
# A2 = Short 1 with the restaurant excuse guy; D1 / D2 = Short 2 with beach pair X1 / X2 (Dan: "generate both, I'll see which
# one looks better"). Everything else is the approved round 1 build, untouched.
import copy as _copy
for _d in (BARS, COVERS, NAME, NEG, SEG, SHOTS, SPLIT, TEXT, TITLE, WORDFIX):
    if "A" in _d: _d["A2"] = _copy.deepcopy(_d["A"])
    if "D" in _d: _d["D1"] = _copy.deepcopy(_d["D"]); _d["D2"] = _copy.deepcopy(_d["D"])
NAME["D1"] += "_X1"; NAME["D2"] += "_X2"
# the excuse line, film time: Short 1 "oh, I don't have the money to get in shape, Dan. I don't have the money for a gym
# membership." = 246.59 (Cd08's out) to 250.717 (Cd09's in); Short 2 "I need a vacation. I deserve a break because I work
# hard." = 379.312 (Cd18's out) to 382.649 (the middle of the pause before "But you don't deserve a break").
COVERS["A2"].insert(1, dict(id="AIr", a=246.59, b=250.717, src=CL + "AIr.mp4", t=0.4, fy=0.484, ai=(40, 336, 1.6)))
COVERS["D1"].insert(1, dict(id="AIb1", a=379.546, b=382.649, src=CL + "AIb1.mp4", t=0.4, fy=0.387, ai=(40, 336, 1.6)))
COVERS["D2"].insert(1, dict(id="AIb2", a=379.546, b=382.649, src=CL + "AIb2.mp4", t=0.4, fy=0.69, ai=(40, 336, 1.6)))
SHOTS["A2"][1] = dict(cap=1540)      # captions under the steak, over the lobster and the tablecloth; his face and the fork stay clear
for _k in ("D1", "D2"): COVERS[_k][0]["b"] = 379.546      # the aerial beach holds 7 frames longer, through Dan's "You're like,", so the excuse guy comes in on silence and his first word is "I" (his lips never mouth Dan's "like,")
# The AI clips are the lip-synced files (round2/lipsync/*_final.mp4, 25 fps): each starts 0.4 s before its slot (t=0.4), the lead-in LatentSync needs.
# Which beach take is "pair X1" and which "pair X2" on Dan's page is the blind key (never printed): D1 is always the X1 build, D2 the X2 build.
import json as _json
_lab = _json.load(open("/Users/danielrose/Projects/_edit_work/SL-21/round2/blind/B/.label-to-take.json"))
_TAKE = {"B1": dict(id="AIb1", src=CL + "AIb1.mp4", fy=0.387), "B2": dict(id="AIb2", src=CL + "AIb2.mp4", fy=0.69)}
for _k, _l in (("D1", "X1"), ("D2", "X2")):
    COVERS[_k][1].update(_TAKE[_lab[_l]])
    if _lab[_l] == "B2": SHOTS[_k][1] = dict(cap=1600)      # the blue-shirt take: captions under the pineapple, on his forearms and the rail (at 1412 they covered the drink)
PINPATH = {"D1": {2: ("D", 1)}, "D2": {2: ("D", 1)}}      # Dan's shot after the excuse clip keeps the round 1 camera path (his approval covers that framing)
NEG["A2"] = NEG["A"].replace("no AI clips, ", "one AI clip (a heavy man at a steakhouse table behind a steak and lobster dinner, lips synced to Dan's own recording of the excuse line, 0:01.5 to 0:05.7, labelled AI-GENERATED); ")
for _k in ("D1", "D2"): NEG[_k] = NEG["D"].replace("no AI clips, ", "one AI clip (a heavy sunburnt man on a beach lounger with a pineapple cocktail, lips synced to Dan's own recording of the excuse line, 0:02.85 to 0:05.9, labelled AI-GENERATED); ")
