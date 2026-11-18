"""SL-36 R2: three Shorts from RO-31 "How To Get Rid Of Man Boobs" as data (recipe copied from softblue-sl21).
Film seconds are on the APPROVED RO-31 R4 master (3:52.3, sha bce049d0, Dan "Approve as final" 2026-11-05). Picture: the film's own
graphics-free base.mp4 (round3/final/base.mp4, the gate plan's source_picture: same 6963 frames and clock, no graphics or cutaways).
Segments, titles and transcripts: Dan approved all three on 2026-11-16 (round2/dan-decisions.json); R1 plan r1/plan.json.
seg     audio pieces kept (film in, out); every edge in measured silence on the master's own mix (snap.py, 10 ms levels)
covers  picture that replaces the talking shot: dict(id, a, b = film times, src + t (clip time at a) + fx/fy + fit + eq)
        Every cover is the film's own approved cutaway (plan_resolved.json) unless its comment says NEW.
bars    key-point lower thirds (HyperFrames), only on the film's WIDE (W2) talking shots: on T2 his chin reaches the bar
text    the captions as spoken (the film's corrected words), ` | ` at each audio piece join"""
CL = "/Users/danrrose/Projects/_edit_work/SL-36/round2/clips/"
PHO = "/Users/danrrose/Projects/Claude/Projects/Abs By AI/photos/finalized social media photos/"
BEFORE = "/Users/danrrose/Projects/Claude/Projects/Abs By AI/before-photo-candidates/B_deckchair_UPSCALED_3x_1080x1440.jpg"
DISC = {}
MASTER_CUTS = []
Y0 = {"full": 0, "mid": 40}        # roll C1775: ~45-60 px of room above his hair in base.mp4; the mid window starts 40 px down (checked by haircheck)
KEEP = 0.90
TRIM = {}
FADEIN = {"C": 0.004}             # C opens 10 ms before the plosive onset of "diet" (177.61): a 15 ms fade would soften the d
SEG = {
 # A: "does." ends 7.62, silence 7.69-8.10. "First," 16.58 (silence 15.78-16.61). "fat." ends 36.06, silence 36.18-36.40.
 # "So" 46.40 (silence 46.19-46.33). "need." ends 71.12, silence 71.13-71.67.
 "A": [[0.00, 7.72], [16.50, 36.24], [46.28, 71.18]],
 # B: "Your" 78.08 (silence 77.73-78.05). "hungry." 94.48 -> 94.60. "And" after the 116.93-116.99 silence; "alcohol." ends 121.44
 # (silence 121.48-121.68). "Push" 124.06 (silence 123.81-124.03). "months." ends 143.98 (silence 144.02-144.21, "Now," after it).
 "B": [[77.92, 94.60], [116.95, 121.52], [124.00, 144.10]],
 # C: the film's "Now," (177.22-177.42 plus its tail to 177.57) is cut off: the dip at 177.60 (-38 dB, 10 ms) before "diet" (onset 177.61).
 # "there." ends 181.60 (silence 181.66-181.87). "See" 147.46 (silence 147.34-147.44). "else." ends 176.62 (silence 176.57-177.07).
 # "If" from 182.13 (silence 181.94-182.13). "diet." decays to -42 dB at 189.22; the film's camera cut to T2 is at 189.222, so the
 # Short ends there (R1 ran to 189.32, which would flash three frames of the other camera).
 "C": [[177.60, 181.70], [147.40, 176.60], [182.04, 189.222]],
}
PICKUP = {}
NEG = {
 "A": "the footage is Dan in a black tank top talking in his studio, the film's approved opener (an AI-generated heavy man in a locker room pulling a T-shirt on, labelled AI-GENERATED), Dan's real before photo then his real after photo (each labelled Real Photo Of Me, Not AI-Generated), the film's hand-drawn chest diagram (no AI) and an AI-generated doctor talking with a patient (labelled); no belly pinching or belly-centred framing, no app screens",
 "B": "the footage is Dan in a black tank top talking in his studio, three real studio photos of Dan (labelled Real Photo Of Me, Not AI-Generated), the film's approved stock of drinks (water, soda, juice, sweet coffee, beer) and Dan's own B-roll doing push-ups by the pool and chest flies on a machine; no AI clips, no app screens, no belly pinching",
 "C": "the footage is Dan in a black tank top talking in his studio, the film's hand-drawn chest diagram (no AI), stock of a doctor with a patient and of a surgical team (nothing graphic) and an AI-generated bodybuilder in a locker room (labelled AI-GENERATED); no app screens, no belly pinching",
}
PATCH = {}
WORDFIX = {}
NAME = {"A": "manboobs-short1_man-boobs-or-chest-fat-do-this-check",
        "B": "manboobs-short2_you-cant-spot-reduce-chest-fat",
        "C": "manboobs-short3_why-diet-wont-fix-true-gynecomastia"}
TITLE = {"A": ("THE SELF-CHECK", ["Man Boobs Or Chest Fat?", "Do This Check"]),
         "B": ("CHEST FAT", ["You Can't Spot Reduce", "Chest Fat"]),
         "C": ("TRUE GYNECOMASTIA", ["Why Diet Won't Fix", "True Gynecomastia"])}
AI = (40, 336, 1.6)
# the chest diagram (film D01 / D02, HyperFrames, 1920x1080): each panel shown alone, as large as the picture area allows above the
# captions (the two panels side by side would be 960 px wide each in a 1080 px frame). Left panel x 50-930, right 990-1870, y 140-1015.
LP = "crop=880:875:50:140"; RP = "crop=880:875:990:140"; DBOX = (0, 330, 1080, 1074)
COVERS = {
 "A": [dict(id="A1", a=0.0, b=3.203, src=CL + "A1.mp4", t=0.0, fx=0.5, fy=0.3, ai=AI),          # film A1 (Flow, approved R3): the opener, as in the film (first 5 seconds)
       dict(id="R01b", a=5.205, b=6.32, scene="photo1", photo=BEFORE, tab="Before", t=0.45),     # film R01 was a side-by-side pair: now the before photo full screen ...
       dict(id="R01a", a=6.32, b=7.72, scene="photo1", photo=PHO + "photo-251_FINAL_PRIMARY.jpg", tab="After", t=1.0),   # ... then the after photo (VIDEO-RULES 2026-11-05)
       dict(id="D01L", a=19.253, b=27.42, src=CL + "D01.mp4", t=19.253 - 19.24, fit="box", box=DBOX, pre=LP),     # film D01: Chest Fat panel through "the same as your belly"
       dict(id="D01R", a=27.42, b=36.24, src=CL + "D01.mp4", t=27.42 - 19.24, fit="box", box=DBOX, pre=RP),      # the True Gynecomastia panel from "The second kind"
       dict(id="D02L", a=48.749, b=52.10, src=CL + "D02.mp4", t=48.749 - 48.76 if 48.749 > 48.76 else 0.0, fit="box", box=DBOX, pre=LP),   # film D02: "soft and spread out = fat"
       dict(id="D02R", a=52.10, b=56.356, src=CL + "D02.mp4", t=52.10 - 48.76, fit="box", box=DBOX, pre=RP),     # "firm disc = gland" from "But if you feel"
       dict(id="A6", a=65.032, b=68.268, src=CL + "A6.mp4", t=0.0, fit="span", span=(0.06, 0.94), y=430, ai=(40, 452, 1.6))],   # film A6: two people, so a full-height card (a fill crop would cut one of them); label on the card
 "B": [dict(id="R02a", a=77.92, b=78.90, scene="photo1", photo=PHO + "studio-blue-249_FINAL_PRIMARY.jpg", t=0.45),     # first 5 seconds: the film's three real after photos (R02), moved to the front,
       dict(id="R02b", a=78.90, b=79.68, scene="photo1", photo=PHO + "studio-blue-110_FINAL_PRIMARY.jpg", t=1.0),     # one at a time, cut on the phrases "Your chest leans out" / "with the rest of you" / "and you can't spot reduce it"
       dict(id="R02c", a=79.68, b=81.28, scene="photo1", photo=PHO + "studio-blue-6_FINAL_PRIMARY.jpg", t=1.0),
       dict(id="J1", a=116.95, b=121.52, src=CL + "J1.mp4", t=116.95 - 116.62, fx=0.45),          # film A4 slot: stock J1, one drink per spoken word
       dict(id="C02", a=124.00, b=127.05, src=CL + "B0546_dan-push-ups-on-handles-side-on-low-sun-first-rep_16x9_11s.mp4", t=0.2, fit="span", span=(0.14, 0.88), y=470,
            eq="eq=saturation=0.72:brightness=0.015,colorbalance=rm=-0.07:gm=-0.01:bm=0.03"),     # film C02 (B0546, its film grade), extended from 1.4 s to 3.05 s so whole reps show; a horizontal pose is a card, his whole body in it
       dict(id="C03", a=127.05, b=131.12, src=CL + "B0668_chest-fly-machine-low-angle-o23-c1846-01-t01_16x9_13s.mp4", t=1.7, fit="span", span=(0.03, 0.97), y=520,
            eq="eq=brightness=0.035:saturation=1.3,curves=all='0/0 0.25/0.31 0.5/0.58 0.75/0.81 1/1'")],      # R2: plus the Oct 23 gym footage midtone lift (SL-21 B0642): it read darker than the studio presenter                                            # film C03 (B0668, its film grade): both handles at full stretch need the width
 "C": [dict(id="D02Rc", a=177.60, b=181.70, src=CL + "D02.mp4", t=3.85, fit="box", box=DBOX, pre=RP),     # first 5 seconds: the film's diagram on its True Gynecomastia panel (approved R1 plan)
       dict(id="C04", a=147.40, b=152.419, src=CL + "C04.mp4", t=0.0, fx=0.5, fy=0.62),          # film C04 (Pexels 7579840, a native portrait clip, conformed 25 -> 29.97 frame for frame)
       dict(id="A7", a=161.595, b=165.532, src=CL + "A7.mp4", t=0.0, fx=0.40, fy=0.3, ai=AI),     # film A7 (Flow, approved R3)
       dict(id="C05", a=182.04, b=185.352, src=CL + "C05.mp4", t=0.0, fx=0.45)],                 # film C05 (Pexels 7584434, conformed)
}
SPLIT = {"A": [], "B": [], "C": []}
SHOTS = {"A": {}, "B": {}, "C": {}}
FULL_ALL = True      # every talk-to-talk cut in this film is already the film's own W2 <-> T2 camera change (a native 1.3x step), so every talking shot uses the full window
BARS = {
 "A": [dict(id="G1", topic="ACTION STEP", parts=[["Check Which One You Have Today", "Check yourself"]], a=-0.2, b=2.3)],          # the film's G03, on its W2 shot
 "B": [dict(id="G1", topic="LOSE THE FAT", parts=[["Appetite Meds, AI Tracking", "Zepbound, tracking"], ["No Liquid Calories", "cutting every"]], a=-0.2, b=0.9),   # the film's L01 list, as a bar on its W2 shot (83.1-88.2)
       dict(id="G2", topic="ACTION STEP", parts=[["Push-Ups And Flies", "Pair this"], ["Plus Fewer Calories", "reducing calories"]], a=0.05, b=2.0)],       # the film's G08, moved onto the W2 shot (137.8-) that follows
 "C": [dict(id="G1", topic="AMERICAN FAMILY PHYSICIAN", parts=[["Up To 1 In 4 Cases: Drugs", "Up to a quarter"]], a=-0.2, b=2.9),     # the film's L02 / G10 source line, on the W2 shot before the bodybuilder
       dict(id="G2", topic="LESS OFTEN", parts=[["Low Testosterone", "low testosterone"], ["Liver, Thyroid Or A Tumor", "a liver"]], a=-0.2, b=3.0),   # the film's L03
       dict(id="G3", topic="ACTION STEP", parts=[["Firm Disc? Book The Doctor", "book the doctor"]], a=-0.6, b=1.9)],                   # the film's G12
}
TEXT = {
 "A": "You think / that you have / man boobs, but you don't. You probably just have chest fat, and it comes off the same way that your belly fat does. | "
      "First, / you need to know / there are two kinds / of man boobs. The first kind is chest fat. It's soft / and it's spread / across your whole chest. "
      "It comes from having too much body fat, the same as your belly. The second kind is true gynecomastia. That's a firm, / rubbery disc / of gland tissue "
      "/ right under your nipple. It's breast tissue, not fat. | "
      "So how do you + tell / which one you have? Feel around your nipple. If it's soft and spread out, it's fat. But if you feel / a firm disc / right under the nipple, "
      "that's gland. If you're not sure, it's probably fat. If you do / truly have gynecomastia, you will feel a firm gland and you will definitely know that it's there. "
      "If you want a diagnosis, a doctor can tell + you / in about a minute. Check yourself today / so you know / which fix you need.",
 "B": "Your chest leans out / with the rest of + you / and you can't / spot reduce it any more than + you + can / spot reduce your belly. The fastest way / I know is Zepbound, "
      "tracking your calories / with AI / and cutting / every liquid calorie. On Zepbound, I went from 192{one ninety two} to about 175{one seventy five} in about 3{three} months because I wasn't as hungry. | "
      "And cut every liquid calorie. Soda, juice, sweet coffee, and alcohol. | "
      "Push-ups + and + chest + flies / build the muscle under the fat, so the area turned into a ripped pec instead of a saggy man-boob. As that fat comes off, "
      "what's left looks like a man's chest, so add push-ups and chest flies to your workouts this week. Pair this with + Zepbound / and reducing calories, "
      "and you'll be shocked at how different your chest looks in a t-shirt within a few months.",
 "C": "Diet won't remove gland tissue. You can get ripped / and the disc / will still be there. | "
      "See a doctor first. True gynecomastia has a cause, and you want to know what it is. In about a quarter + of + cases, it's left over from puberty. "
      "In another quarter, nobody can find a cause. Up to a quarter, it comes from drugs or other substances. Anabolic steroids / are one of the big ones, "
      "and the gynecomastia / they + cause often never goes away. Less often, it comes from low testosterone, a liver or thyroid problem, or very rarely, "
      "it can come from a tumor. That's why you should see a doctor before you do anything else. | "
      "If it's been there a long time, surgery is the fix. So if it's a firm disc, book the doctor / instead of starting / another diet.",
}
