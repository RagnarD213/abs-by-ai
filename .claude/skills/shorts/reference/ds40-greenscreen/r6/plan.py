"""DS-40 R6 edit plan: the film timeline in frames, the cuts, the silent Maher footage in the card, the four graphics.

    python3 plan.py            -> plan.json, gfx/sheet.json

Film = the locked R4 B opening (clip 4.40-23.78, 581 frames, small Dan) + the R3 move (15 frames, scripted take starts
under it) + the ONE scripted take on roll C1730, with two ad-libs cut out where the full-screen BMI table covers him.
Roll frame grid: frame n at n*1001/30000 s. Cache frame j of the scripted take = roll frame ROLLF0 + j.
"""
import json, math
FPS = 30000 / 1001
N_CLIP = 581                     # clip frames (4.40 .. 23.78 of the clip file)
MOVE = 15
ROLLF0 = 41966                   # first roll frame of the scripted take: -ss 1400.25 lands on frame 41966 (pts 1400.2656; frames sit on n*1001/30000)
ROLL0 = ROLLF0 / FPS

def rf(t): return math.ceil(t * FPS - 1e-6)             # roll frame a -ss t seek lands on
# cuts (roll seconds): out at a silence, back in an exact whole number of frames later (picture and sound stay locked)
CUT1 = (1426.86, 137)            # removes "So look at your weight, look at your height and then see if you're overweight or obese."
CUT2 = (1436.34, 102)            # removes "Most people in America are in the overweight category."
BMI_IN, BMI_OUT = 1422.96, 1444.80   # roll: the table is up from the pause before "So, on screen" to after "...can do."
END = 1449.10                    # roll: 0.48 s after "abs."
REM = CUT1[1] + CUT2[1]

def film_s(roll):
    """Film seconds of a roll time inside the kept scripted take."""
    j = (roll - ROLL0) * FPS
    if roll >= CUT2[0] + CUT2[1] / FPS: j -= REM
    elif roll >= CUT1[0] + CUT1[1] / FPS: j -= CUT1[1]
    else: assert roll <= CUT1[0] or roll >= CUT1[0] + CUT1[1] / FPS
    return (N_CLIP + j) / FPS

def film_f(roll): return int(round(film_s(roll) * FPS))

j_bmi_in = rf(BMI_IN) - ROLLF0           # cache frame where the table cuts in
j_bmi_out = rf(BMI_OUT) - ROLLF0         # cache frame where he is back
j_end = rf(END) - ROLLF0
F_BMI0 = N_CLIP + j_bmi_in
F_BMI1 = N_CLIP + j_bmi_out - REM
F_END = N_CLIP + j_end - REM + 1         # total frames
assert rf(CUT1[0]) - ROLLF0 > j_bmi_in and rf(CUT2[0] + CUT2[1] / FPS) - ROLLF0 < j_bmi_out

def dan_j(f):
    """Cache frame j (scripted take) for film frame f, or None where the clip / BMI table fills the screen."""
    if f < N_CLIP: return None
    j = f - N_CLIP
    if F_BMI0 <= f < F_BMI1: return None
    if f >= F_BMI1: j += REM
    return j

# silent Maher footage in the card: other moments of the same episode (yfiWjnStE3w "New Rule: Fat Acceptance").
# The reaction clip is episode 2:14.4-2:33.8 (clip file time + 130 s, matched on the picture); nothing from 2:10-2:40.
EP = "/Volumes/Expansion/_edit_work/ds40/r6/src/maher_full_yfiWjnStE3w.f398.mp4"
F_SETTLE = N_CLIP + MOVE                 # the card has landed
CARD = [
    # film frames [f0, f1), episode start seconds, what it shows
    dict(f0=F_SETTLE, f1=None, ep=360.55, what="Maher at the desk, laughing, hands up (6:00; a quote graphic is gone by 6:00.4, an audience cut at 6:05.64)"),
    dict(f0=None, f1=None, ep=286.00, what="Maher beside the bathroom-scale photo (4:46)"),
    dict(f0=None, f1=F_BMI0, ep=396.00, what="Maher at the desk, both hands talking (6:36)"),
    dict(f0=F_BMI1, f1=F_END, ep=91.00, what="Maher at the desk, wide (1:31)"),
]
# split the first stretch into three about equal shots, on whole frames
span = F_BMI0 - F_SETTLE
CARD[0]["f1"] = CARD[1]["f0"] = F_SETTLE + round(span * 0.22)
CARD[1]["f1"] = CARD[2]["f0"] = F_SETTLE + round(span * 0.58)

W = lambda roll: round(film_s(roll), 3)
graphics = [
    dict(id="G1", template="lower-third", t0=0.40, t1=4.80, what="name lower third over the clip",
         config=dict(id="G1", a=0.40, b=4.80, topic="REAL TIME (HBO)", topic_case="preserve", parts=[["Bill Maher", 0.55]], drift=-4)),
    dict(id="G2", template="lower-third", t0=W(1413.95), t1=W(1418.96), what="key point at 'treat your belly fat as an emergency'",
         config=dict(id="G2", a=W(1413.95), b=W(1418.96), topic="KEY POINT", topic_case="preserve",
                     parts=[["Treat Your Belly Fat", W(1414.18)], ["As An EMERGENCY", W(1415.36)]], drift=-4)),
    dict(id="G3", template="bmi-table", t0=F_BMI0 / FPS, t1=F_BMI1 / FPS, what="full-screen BMI table",
         config=dict(id="G3", eyebrow="BMI TABLE", headline="Where Do You Land?",
                     heights_in=[60, 62, 64, 66, 68, 70, 72, 74, 76], weights_lb=[120, 140, 160, 180, 200, 220, 240, 260, 280],
                     beats=[["overweight", round(W(1426.24) - F_BMI0 / FPS, 3)], ["normal", round(W(1435.76) - F_BMI0 / FPS, 3)],
                            ["obese", round(W(1440.56) - F_BMI0 / FPS, 3)]],
                     bottom=1380)),
    dict(id="G4", template="cta", t0=W(1444.98), t1=F_END / FPS, what="subscribe button",
         config=dict(top="Learn To Lose Your Belly Fat", big="Subscribe", hold_out=True)),
]
graphics[2]["config"]["dur"] = round(graphics[2]["t1"] - graphics[2]["t0"], 3)

plan = dict(fps="30000/1001", n_clip=N_CLIP, move=MOVE, rollf0=ROLLF0, cut1=CUT1, cut2=CUT2, rem=REM,
            f_bmi0=F_BMI0, f_bmi1=F_BMI1, f_end=F_END, j_bmi_in=j_bmi_in, j_bmi_out=j_bmi_out, j_end=j_end,
            dur_s=round(F_END / FPS, 3), card=CARD, episode=EP, graphics=graphics,
            audio=dict(roll_in=round(ROLL0, 4), cut1_in=round(CUT1[0] + CUT1[1] / FPS, 4), cut2_in=round(CUT2[0] + CUT2[1] / FPS, 4),
                       roll_end=round((ROLLF0 + j_end + 1) / FPS, 4)))
if __name__ == "__main__":
    json.dump(plan, open("plan.json", "w"), indent=1)
    json.dump(dict(graphics=[g for g in graphics if g["template"] != "bmi-table"]), open("gfx/sheet.json", "w"), indent=1)
    json.dump(graphics[2]["config"], open("gfx/bmi.json", "w"), indent=1)
    for k in ("f_bmi0", "f_bmi1", "f_end", "dur_s"): print(k, plan[k], round(plan[k] / FPS, 3) if k != "dur_s" else "")
    for c in CARD: print("card", c["f0"], c["f1"], round((c["f1"] - c["f0"]) / FPS, 2), "s from ep", c["ep"], c["what"])
    for g in graphics: print(g["id"], round(g["t0"], 3), round(g["t1"], 3), g["what"])
    print(graphics[2]["config"]["beats"])
