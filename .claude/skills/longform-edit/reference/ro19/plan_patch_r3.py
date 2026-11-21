"""RO-19 round 3: the plan changes from Dan's round 2 notes, applied to the round 2 plan as he reviewed it (round3-plan/plan_resolved.round2.json, itself
hand-patched in round 2: do not re-run resolve.py). Writes plan_resolved.json and hf/manifest.r3.json. Idempotent. usage: plan_patch_r3.py"""
import json
W = "/Volumes/Extreme/_edit_work/ro19"; FPS = 30000/1001
R = json.load(open(f"{W}/round3-plan/plan_resolved.round2.json")); S = {s["id"]: s for s in json.load(open(f"{W}/shots.json"))}
# THE CUT FIX (found proofreading the full film's captions): edl piece "pros" ended on the first of two "goes out in the sun", mid-sentence. edl.py now ends it on the
# second; shot pros.0r3 runs 215 frames longer and everything after it moves later by that much (round3-plan/timeline_shift.json; shots.json and words_out.json are
# already on the new timeline). Every plan item and lower third after the insert point moves with it; nothing spans it.
SH = json.load(open(f"{W}/round3-plan/timeline_shift.json")); AT = SH["at_out_frame"]/FPS; DT = SH["frames"]/FPS
def late(t): return t + DT if t >= AT - 0.05 else t
for r in R:
    assert not (r["t0"] < AT - 0.05 < r["t1"] - 0.05), ("an item spans the insert point", r["id"]); r["t0"], r["t1"] = late(r["t0"]), late(r["t1"])
by = {r["id"]: r for r in R}
# P02: Dan rejected the soft-looking pale photo; the driveway frame with defined abs (photocrop19r3.py)
by["P02"].update(photo="pale3_single", src=[f"{W}/gfx/r3/P02.mp4@0"], note="ROUND 3 (Dan): the driveway photo from the 1 April pale shoot (14:50:13, asset 06D979F4), pale with defined abs")
# P04: the pale half is the untinted original of the same frame, same crop box
by["P04"].update(pair=["pale3_down", "tan2_down"], src=[f"{W}/gfx/r3/P04.mp4@0"], note="ROUND 3 (Dan): the pale half is the untinted original of the same frame (asset 99501C7F), same crop box as the card he approved")
# A5: the doctor clip has motion (Veo take 1, frames D1 approved 2026-10-12); 0.2 s in, the slot is 5.57 s of a 6 s take
a5 = by["A5"]; a5.pop("frames"); a5.pop("pending"); a5["src"] = [f"{W}/round3/motion/A5-t1.mp4@0.2"]
a5["note"] = "TALK TO YOUR DOCTOR, AI clip (finished motion, Veo take 1): an ordinary man of about 45 listens to a male doctor in an exam room; the doctor lifts a clipboard, points at it with a pen, and the man leans in and nods"
AI = dict(kind="clip", label="AI-GENERATED", people="other", physique=False, anywhere=True)
# G1 (eight hour wait): under "a rapid drying tan, I needed to wait eight hours before taking the shower." Lower third Gb15 sits over it.
# Take 1 from 0.6 s: upright and impatient, the clock's hands spin from nine to five as the light turns to evening, he ends slumped. (One-frame jump of light at 2.0 s: reads as the time-lapse.)
G1 = dict(id="G1", start="a rapid drying tan, I needed", end="before taking the shower.", t0=349.21, t1=353.10, src=[f"{W}/round3/motion/G1-t1.mp4@0.6"], **AI,
          note="EIGHT HOURS, AI clip (finished motion, Veo take 1), a gag: a tanned man in a bathrobe sits facing a shower taped shut, staring at the clock; the hands spin from nine to five, morning light turns to evening, and he ends slumped on the stool, bored")
# G3 (the spot he could not reach): under "If you don't have a partner and you can't reach your whole body, it's going to be less even than a professional tan." Lower third Gd03 sits over it.
# Take 1 from 0.7 s: the proud thumbs up, he turns, the pale patch is on screen from "whole body". (The mitt changes hands over 6 frames at 3.5 s of the take, low in the frame: a note, not a reject, VIDEO-RULES 2026-10-08.)
G3 = dict(id="G3", start="If you don't have a partner", end="than a professional tan.", t0=late(819.12), t1=late(823.42),     # typed on the round 2 timeline
          src=[f"{W}/round3/motion/G3-t1.mp4@0.7"], **AI,
          note="THE SPOT HE COULD NOT REACH, AI clip (finished motion, Veo take 1), a gag: a man by a pool shows off his do-it-yourself tan with a thumbs up, turns to walk away, and the middle of his back is one big pale patch his mitt never reached")
# P07: the approved app tour beside him (phone_side19.py) replaces the two feature lower thirds on the trainer and nutritionist lines; the clip is exactly shots outro.0r4 + outro.0r5
a, b = S["outro.0r4"], S["outro.0r5"]
P07 = dict(id="P07", kind="clip", start="We have an AI personal trainer,", end="get you to your goal.", anywhere=True, t0=a["out_f0"]/FPS, t1=b["out_f1"]/FPS, src=[f"{W}/round3/phone/P07-side.mp4@0.0"],
           people="dan", physique=False, label="AI-GENERATED", label_in_picture=True,
           note="THE APP TOUR beside him (the approved Work Out At Home ending, rebuilt on this take): he sits to the right, the app in an upright phone on the left. A tap on AI Trainer and two workout demo videos on the trainer line; a tap on Macro Tracker and calorie tracking from a meal photo on the nutritionist line")
assert round(a["out_f0"]) == a["out_f0"] and a["out_f1"] == b["out_f0"]
# B-roll graded against the presenter frames (Dan, 2026-10-11). Dan's skin in the presenter picture measures 0.43 (median luma, person mask + skin hue, round3/broll);
# his own clips that measured well under it get a luma lift toward 0.40, and four stock clips that read dark beside the kitchen get a smaller one. build.lift().
FX = {"Cb12": [dict(gamma=1.40, sat=1.05), dict(gamma=1.45, sat=1.15)],     # B0427 ab wheel 0.29, B0432 dumbbells 0.27 and flat
      "Cd17": [dict(gamma=1.45, sat=1.08), None, None],                     # B0547 push-up 0.27
      "Cd07": [None, dict(gamma=1.45)],                                     # B0459 side pose 0.35, dark hedge behind; 1.25 still read dark to the independent review
      "Cd20": [dict(gamma=1.35)],                                           # B0438 front pose 0.32, the same set
      # stock the independent review still read darker than the kitchen (dark sets by design; a smaller lift)
      "Cb04": [dict(gamma=1.25)], "Cb07": [dict(gamma=1.20)], "Cb08": [dict(gamma=1.20)], "Cb11": [dict(gamma=1.20)], "Cd04": [dict(gamma=1.25), None], "Cd14": [dict(gamma=1.20)],
      "Cd06": [dict(gamma=1.0, sat=1.15), None],                            # B0441 meal prep: bright enough, flat
      "Cd01": [dict(gamma=1.40), None, None],                               # B0141 gym, frame median 0.16
      "Cd11": [dict(gamma=1.30), None, dict(gamma=1.25)],                   # B0192 photo studio 0.10, B0191 church wedding 0.19
      "Cc08": [dict(gamma=1.20)],                                           # studio portrait session 0.24
      "Cd09": [dict(gamma=1.20)]}                                           # B0024 handshake 0.25
for k, v in FX.items(): assert len(v) == len(by[k]["src"]), k; by[k]["fx"] = v
# Two stock faces sat under a lower third (hyperframes/checks.py on the first full film: Gc09 over the swimmer's face at 8:29, Gc17 over the woman's chin at 12:03).
# The swimmer clip now plays from 0.5 s (he is at the pool edge, face well above the bar; from 4.6 s he sank to the bottom of the frame). The tight portrait of the
# red-haired woman cannot be moved up (no picture below her chin), so the ginger man's portrait, whose face stays clear, holds the whole slot.
c7 = by["Cc07"]; assert "8686094" in c7["src"][0]; c7["src"][0] = c7["src"][0].split("@")[0] + "@0.5"
c20 = by["Cc20"]; assert "8724508" in c20["src"][0] and len(c20["src"]) == 2; c20["src"] = [c20["src"][0]]
# The independent review of the first full film: (1) the fashion stock clip was started at 7.0 s, inside the clip's own glitch effect (the picture rolls and tears);
# its first clean stretch is 1.0 to 4.2 s. (2) the AI-GENERATED chip sat on the AI characters' heads in A3 and A2: those two carry it top left.
c10 = by["Cd10"]; assert "855563" in c10["src"][0]; c10["src"][0] = c10["src"][0].split("@")[0] + "@1.2"
by["A2"]["chip"] = "lt"; by["A3"]["chip"] = "lt"
c7["note"] = "Pexels stock, two shots: a swimmer in a cap rests on the wall of a pool and pulls his goggles down (the clip from 0.5 s; from 4.6 s his face sank under the lower third); then bare feet wade out into shallow open water"
c20["note"] = "Pexels stock, one clothed portrait for the whole slot: a red-haired man in a pink sweater against a blue wall (the second portrait, a red-haired woman, was dropped: her chin sat under the lower third)"
c10["note"] = c10["note"] + " ROUND 3: the model shot starts at 1.2 s (clean); 7.0 s was inside the clip's own glitch effect"
R = [r for r in R if r["id"] not in ("Gz04", "Gz05", "G1", "G3", "P07")] + [G1, G3, P07]
R.sort(key=lambda r: (r["t0"], r["kind"] != "clip"))
full = sorted((r["t0"], r["t1"], r["id"]) for r in R if r["kind"] in ("clip", "scene"))
for x, y in zip(full, full[1:]): assert x[1] <= y[0] + 0.02, ("two full-screen items overlap", x, y)
assert not [r["id"] for r in R if r.get("pending") or r.get("frames")]
json.dump(R, open(f"{W}/plan_resolved.json", "w"), indent=1)
M = [m for m in json.load(open(f"{W}/hf/manifest.json")) if m["id"] not in ("Gz04", "Gz05")]
for m in M: m["a"], m["b"] = round(late(m["a"]), 3), round(late(m["b"]), 3)
json.dump(M, open(f"{W}/hf/manifest.r3.json", "w"), indent=1)
lts = [r["id"] for r in R if r["kind"] in ("lt", "l3") or (r["kind"] == "scene" and r.get("scene") == "fact")]; mids = [m["id"] for m in M]
print(len(R), "items;", len(lts), "lower thirds in the plan,", len(mids), "in the manifest; missing from the manifest:", sorted(set(lts) - set(mids)), "extra:", sorted(set(mids) - set(lts)))
