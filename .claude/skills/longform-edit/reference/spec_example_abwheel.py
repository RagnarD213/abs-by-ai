#!/usr/bin/env python3
"""THE AUTHORED PLAN: every graphic and every cutaway, on the TIGHT timeline.

Cue times come from find_cue.py (searched AFTER a time, never globally -- a repeated
line matches the wrong occurrence otherwise), so each graphic lands on the words it
illustrates instead of on an even spacing.

Dan's round-1 revision notes on this video are folded in verbatim:
  * graphics green is the darker military green (motionlib.MIL), not the brand olive
  * the three progression cards carry HIS text: "How Beginners Should Do It",
    "How Intermediate Guys Should Do It", "How Advanced Guys Should Do It"
  * the two CTA graphics read "AbsByAI.com"
  * the toe-touch clip he had /findassets cut and deliver is used for the beat about
    resting at the top and bottom of a crunch -- his own footage, not stock
"""

# ---------------------------------------------------------------- stock library
# id -> (file stem, default in-point). Chosen off a contact sheet of all 38
# downloads, not off the titles: casting matters (Dan's standing note from the
# spray-tan revision is white or Asian men 30-50), and four Pexels results titled
# as men are women.
STOCK = {
 "wheel_product":  ("px_8026520",  2.0),   # ab wheel alone on a dark surface
 "wheel_kit":      ("px_8027453",  1.0),   # shoes, bottle and an ab roller
 "wheel_kit2":     ("px_8027708",  2.0),   # ab wheel + dumbbells, dark
 "wheel_board1":   ("px_8544638",  1.0),   # man, ab roller, boardwalk
 "wheel_board2":   ("px_8544669",  2.0),   # man, ab roller, boardwalk (wider)
 "wheel_sunset":   ("px_8544601",  3.0),   # man, ab roller, outdoors, low sun
 "wheel_mat":      ("px_8026518",  6.0),   # man rolling out on a mat, home
 "wheel_mat2":     ("px_8026507",  8.0),   # man rolling out, full extension
 "crunch_man":     ("px_4259064",  3.0),   # man doing crunches at home
 "crunch_bench":   ("px_4367634",  4.0),   # man, incline sit-ups
 "crunch_older":   ("px_6293127",  2.0),   # man doing crunches
 "curlups":        ("px_8026546",  3.0),   # man doing curl-ups on a mat
 "plank_man":      ("px_4325592",  6.0),   # man in the rollout/plank position
 "sideplank":      ("px_6023266",  1.5),   # man, side plank
 "abs_bw":         ("px_5432439",  6.0),   # abs, black and white
 "flex":           ("px_6060022",  1.0),   # shirtless man flexing
 "bodybuilder":    ("px_5319758",  5.0),   # heavy bodybuilder, gym
 "bodybuilder2":   ("px_5319762",  3.0),   # bodybuilder, gym
 "gymtrain":       ("px_10441577", 6.0),   # shirtless man training, gym
 "gym_interior":   ("px_28436821", 2.0),   # gym floor, treadmills
 "dumbbell_rack":  ("px_6389051",  2.0),   # dumbbell rack
 "kettlebells":    ("px_7187429",  1.0),   # kettlebells on a shelf
 "mat_rollout":    ("px_8939150",  0.6),   # a yoga mat being rolled out
 "bars_legraise":  ("px_8520198",  4.0),   # man, leg raises on parallel bars
 "sitgrass":       ("px_8402089",  3.0),   # man, sit-ups on grass
}
# our OWN footage -- always preferred over stock when it says the same thing
OWN = {
 "toe_touches": ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
                 "03 B-Roll - Real Footage/toe-touches_1min-ab-workout_4.47s_graded.mp4", 0.0),
 "app_flow":    ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
                 "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4", 3.0),
}

WINDOW = [280, 168, 1640, 933]     # the inset window, 1360x765 = 16:9
# A vertical source fitted into the 16:9 window is only 352 px wide and reads as lost on
# the field. Anything vertical gets a phone-shaped window instead.
WINDOW_PHONE = [760, 96, 1160, 940]        # 400 x 844
WINDOW_FOR = {"app_flow": WINDOW_PHONE}

# (start, dur, kind, key, note)   kind: "full" | "inset"
INSERTS = [
 # ---- INTRO: the object itself, then the infomercial framing
 (  2.90, 4.20, "inset", "wheel_product",  "this $17 infomercial gimmick -- show the object"),
 (  8.20, 3.20, "full",  "wheel_kit",      "because it was sold on an infomercial"),
 ( 12.60, 2.80, "full",  "wheel_kit2",     "but this is different"),
 ( 15.40, 3.00, "full",  "wheel_board1",   "why you need to be buying an ab wheel"),
 # ---- WHY 01 constant tension
 ( 29.00, 4.60, "full",  "wheel_mat2",     "AS YOU CAN SEE FROM THE VIDEO ON THE SCREEN RIGHT NOW"),
 ( 34.20, 4.47, "full",  "toe_touches",    "a crunch has a part where I'm resting (Dan's own clip)"),
 ( 39.10, 3.30, "inset", "wheel_board2",   "higher time under tension"),
 # ---- WHY 02 progression
 ( 47.20, 3.20, "full",  "wheel_mat",      "benefit even if you're a beginner"),
 ( 52.20, 3.20, "full",  "curlups",        "how to modify it for a beginner"),
 ( 55.80, 3.60, "full",  "bodybuilder",    "if you're a ripped monster bodybuilder"),
 ( 60.60, 3.20, "full",  "wheel_sunset",   "do your ab wheel in a different way"),
 # ---- WHY 03 every ab muscle
 ( 78.20, 4.00, "full",  "abs_bw",         "all your ab muscles at once"),
 ( 83.60, 3.40, "full",  "crunch_older",   "crunches only hit the rectus abdominis"),
 ( 89.20, 3.30, "full",  "flex",           "chest, shoulders and arms too"),
 ( 93.20, 2.80, "inset", "gymtrain",       "a great total body exercise"),
 # ---- WHY 04 cheap and small
 (103.40, 2.60, "full",  "wheel_kit2",     "it'll last a lifetime, fits in a drawer"),
 (106.30, 2.40, "full",  "dumbbell_rack",  "you don't need any complicated equipment"),
 (108.90, 2.90, "full",  "gym_interior",   "if you can't make it to the gym"),
 # ---- HOW TO DO IT. Dan is demonstrating here, so this section stays on him:
 # covering a form demo with stock would remove the thing the viewer came for.
 (119.60, 2.80, "full",  "mat_rollout",    "I recommend getting a yoga mat"),
 (131.50, 3.20, "inset", "plank_man",      "the biggest mistake is the back gets arched"),
 (167.50, 3.00, "full",  "curlups",        "locked out arms and a straight back"),
 # ---- PROGRESSION
 (246.00, 3.00, "inset", "wheel_board2",   "gradually step it up each workout"),
 (266.00, 3.00, "full",  "bodybuilder2",   "you see bodybuilders doing this"),
 # ---- LIVE INTRO
 (282.50, 2.60, "full",  "wheel_mat2",     "leave one rep in the tank"),
 # ---- OUTRO
 (399.50, 3.00, "inset", "wheel_board1",   "if you want more ab workouts like this"),
 (413.60, 9.40, "inset", "app_flow",       "generate a picture of yourself with abs"),
]

# ---------------------------------------------------------------- graphics
# (start, dur, kind, key, payload)
G = [
 (  0.55, 2.25, "number",  "price1",   {"text": "$17"}),
 ( 20.90, 3.40, "title",   "why",      {"h": "WHY THE AB WHEEL\nBEATS EVERY CRUNCH",
                                        "sub": "and why you need to be using one"}),
 ( 25.40, 3.60, "section", "s01",      {"n": "01", "t": "It Has Constant Tension"}),
 ( 43.10, 3.60, "section", "s02",      {"n": "02", "t": "It Has A Built In Progression"}),
 ( 65.90, 3.60, "section", "s03",      {"n": "03", "t": "It Hits Every Ab Muscle At Once"}),
 ( 67.80, 9.60, "stack",   "muscles",  {"head": "every ab muscle",
                                        "items": [(0.20, "Rectus Abdominis"),
                                                  (1.24, "Transverse Abdominis"),
                                                  (6.21, "Obliques")]}),
 ( 97.40, 3.60, "section", "s04",      {"n": "04", "t": "It's Cheap And It's Small"}),
 (100.31, 2.70, "number",  "price2",   {"text": "$17"}),
 (114.50, 3.20, "title",   "howto",    {"h": "HOW TO DO IT", "sub": "the four details that matter"}),
 (143.26, 3.40, "lower",   "flatback", {"lines": ["FLAT BACK, NEVER ARCHED"]}),
 (146.90, 3.40, "lower",   "arms",     {"lines": ["ARMS LOCKED OUT, KNUCKLES DOWN"]}),
 (173.73, 3.40, "lower",   "slow",     {"lines": ["SLOW AND CONTROLLED"]}),
 (205.80, 3.80, "section", "beg",      {"n": "01", "t": "How Beginners Should Do It"}),
 (226.97, 3.40, "section", "int",      {"n": "02", "t": "How Intermediate Guys Should Do It"}),
 (235.00, 3.60, "section", "adv",      {"n": "03", "t": "How Advanced Guys Should Do It"}),
 (253.19, 3.80, "section", "skip",     {"n": "!", "t": "One To Skip: The Standing Version"}),
 (278.16, 3.40, "lower",   "reps",     {"lines": ["AS MANY REPS AS YOU CAN",
                                                  "leave one rep in the tank"]}),
 (289.00, 3.20, "title",   "live",     {"h": "THE LIVE WORKOUT", "sub": "three sets, slow and controlled"}),
 (294.60, 3.20, "section", "set1",     {"n": "01", "t": "Set One"}),
 # The three sets are Dan actually performing, so they are NOT covered with stock --
 # that footage IS the payoff. But set one and set two each ran 32 s and 36 s with
 # nothing on screen, over Dan's own 30-second rule, so each set carries one form cue
 # in the middle. They earn their place: they are the teaching points restated at the
 # moment the viewer is watching the movement.
 (312.00, 3.40, "lower",   "cue1",     {"lines": ["TIME UNDER TENSION BEATS REPS"]}),
 (347.00, 3.40, "lower",   "cue2",     {"lines": ["KEEP THE BACK FLAT"]}),
 (386.00, 3.40, "lower",   "cue3",     {"lines": ["LEAVE ONE REP IN THE TANK"]}),
 (330.00, 3.20, "section", "set2",     {"n": "02", "t": "Set Two"}),
 (369.60, 3.20, "section", "set3",     {"n": "03", "t": "Set Three"}),
 (404.14, 3.40, "lower",   "sub",      {"lines": ["SUBSCRIBE FOR MORE AB WORKOUTS"]}),
 (409.00, 3.60, "title",   "cta1",     {"h": "ABSBYAI.COM", "sub": "the first step to six pack abs"}),
 (427.60, 5.97, "endcard", "end",      {"h": "ABSBYAI.COM", "sub": "get your free AI preview"}),
]

if __name__ == "__main__":
    import json
    DUR = json.load(open("plan.json"))["dur"]
    def mm(t): return f"{int(t//60)}:{t%60:05.2f}"
    ev = sorted([(a, a+d, "GFX " + k, kk) for a, d, k, kk, _ in G] +
                [(a, a+d, "INS " + k, kk) for a, d, k, kk, _ in INSERTS])
    print(f"{len(INSERTS)} inserts + {len(G)} graphics")
    for a, b, k, kk in ev: print(f"  {mm(a):>8s} - {mm(b):>8s}  {k:12s} {kk}")
    # coverage + the longest stretch with nothing on screen
    merged, cur = [], None
    for a, b, _, _ in ev:
        if cur and a <= cur[1] + 0.001: cur[1] = max(cur[1], b)
        else:
            if cur: merged.append(cur)
            cur = [a, b]
    if cur: merged.append(cur)
    cov = sum(b - a for a, b in merged)
    gaps, t = [], 0.0
    for a, b in merged:
        if a - t > 0: gaps.append((t, a))
        t = b
    if DUR - t > 0: gaps.append((t, DUR))
    gaps.sort(key=lambda g: -(g[1] - g[0]))
    print(f"\ncoverage {cov:.0f}s of {DUR:.0f}s = {100*cov/DUR:.0f}%   "
          f"({len(INSERTS)} inserts, {len(G)} graphics)")
    print("longest stretches with nothing on screen:")
    for a, b in gaps[:8]:
        flag = "   *** OVER Dan's 30 s rule" if b - a > 30 else ""
        print(f"   {mm(a)} - {mm(b)}   {b-a:5.1f}s{flag}")
