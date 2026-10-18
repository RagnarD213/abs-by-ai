#!/usr/bin/env python3
"""SL-09 R2: the "What I decided" list for the round-1 page, plus per-item notes, with the gate and review results read from disk."""
import json, os, re
import plans as P
W9 = "/Volumes/Extreme/_edit_work/sl09/round2"
ORDER = ["A", "I", "H", "K", "J"]
def gate(S):
    f = f"/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/{P.NAME[S]}.mp4.deliver_gate.json"
    if not os.path.exists(f): return "not run yet"
    g = json.load(open(f)); return ("PASS" if g.get("verdict") == "PASS" or g.get("pass") else "FAIL")
def review(S):
    f = f"{W9}/build/{S}/ROUND-2-REVIEW.md"
    if not os.path.exists(f): return "not run yet"
    m = re.findall(r"VERDICT:\s*(SHIP|DOES NOT SHIP)", open(f).read()); return m[-1] if m else "no verdict"
NAMES = {"A": "Train Harder", "I": "Sleep Score", "H": "Adrenaline", "K": "Not Sleeping", "J": "Oura Or WHOOP"}
decided = [
 "<b>Order:</b> 1 Train Harder After A Bad Night's Sleep, 2 Your Sleep Score Shows Who's Toxic, 3 Cut The Adrenaline Before Bed, "
 "4 You're Not Sleeping As Well As You Think, 5 Oura Ring Or WHOOP (training and sleep rules first, the buying guide last).",
 "<b>Openings that stand alone, no pickups:</b> short 4 drops \"So the bottom line is\", short 5 drops \"So the overall verdict,\", short 2 "
 "drops its leading \"And\"; short 3 opens on your own line from the end of that passage (\"There might be something that you're doing...\") "
 "moved to the front.",
 "<b>Cut from short 2:</b> 17:16 to 17:36 of the film (\"Nobody is worth sacrificing your health for... especially late at night?\"), as on the "
 "shortlist; the step to a closer crop at 0:46 marks the join.",
 "<b>Zeeshan's AI Tesla clip is out</b> (its speedometer read 190 while you say 120): two real night-driving clips replace it. His real "
 "daytime Tesla self-driving footage stays, framed on the steering wheel.",
 "<b>Zeeshan's own graphics are never sliced:</b> every lower third of his in these passages is covered whole by a clip (and held about a "
 "second past its fade); his verdict list in short 5 stays outside the crop (the crop starts 26 px right of it).",
 "<b>Two of his graphics rebuilt as our moving Soft Blue scenes:</b> the sleep-score card (your real Oura chart from his card, with \"My Oura "
 "Sleep Score / Toxic Relationship / During It, And After It Ended\" landing on your words) and the Oura vs WHOOP lists (each row lands on "
 "the word that names it). The comparison is a new HyperFrames template; it joins the shared set once you approve it.",
 "<b>The comparison leaves out price and subscription:</b> you say \"for some people, there's no subscription and the cost is low\", which is "
 "kept in your voice and captions, but a WHOOP needs a membership, so the graphic does not print it.",
 "<b>Clips first from our library:</b> your own jump rope (B0448), curls (B0031) and lateral raises (B0450) for \"work out harder\" and "
 "\"low risk\"; library stock B0354 (a pillow thrown at 4:28 AM), B0535 (a stressed man, two different moments in two shorts), B0333 (a man "
 "sleeping well); Pexels stock for the rest (alarm smash, groggy man in bed, deadlift, power clean, light-streak tunnel, deserted highway, "
 "highway time-lapse, arguing couple, man alone, man awake in bed, door closing, Apple Watch, yawning man, scale, whiskey, fridge at night). "
 "Your real Oura app screenshot from the film opens short 5 and fills \"see the problem\" in short 4. Darker stock is brightened to sit "
 "with the studio shots.",
 "<b>Rejected clips:</b> B0494 (its actor reads as you at a glance), Pexels 6698753 (a montage with dissolves inside it), a Subaru WRX clip "
 "(an identifiable other car right after you name your Tesla), a busy Tokyo street (after \"nobody on the road\"), a stock opener that "
 "cut a man's head off, B0460 squats (you small and in shade), B0298 deadlift (never finishes a rep). No ring or WHOOP footage exists in "
 "the library or on Pexels (only wedding bands), hence the AI ring idea.",
 "<b>Fixed after the independent reviews:</b> short 1, your head tilt at 0:48 swung wider than any steady crop, so a clip covers \"be "
 "careful today, take it easy\"; short 3, a same-size cut hidden inside Zeeshan's footage got a real size step, his Tesla footage now starts "
 "on \"press a button\" and is cropped off its speed digits; short 4, the app stays on the sleep screen (the later screens said \"93 "
 "Optimal\" over \"the problem\") and the phone is back at full size; true peak kept at or under Zeeshan's -1.0 dBTP on every short by "
 "picking the AAC encoder mode, never by changing his level.",
 "<b>Key points (title case):</b> 1 \"Bad Sleep Is No Reason / To Slack Off In The Gym\"; 2 \"Someone Wrecks Your Sleep? / They Have To Go\"; "
 "3 \"Late-Night Adrenaline / Wrecks Your Sleep\"; 4 \"Track It To See What's / Wrecking Your Sleep\"; 5 none (the comparison is the graphic).",
 "<b>Captions print what you say:</b> short 3 says \"adrenaline in your bedtime\" (that is the audio), short 1 keeps \"Don't listen to that shit\".",
 "<b>No real-photo or AI labels needed:</b> there are no photos of you and no AI clips in the five as delivered; the two AI ideas above are frames only.",
 "<b>Spend: $0</b> (frames on the ChatGPT subscription, no motion made, stock from Pexels and our library).",
 "<b>Checks on each delivered file:</b> " + "; ".join(f"short {P.ORDER[S]} ({NAMES[S]}): audio PASS (Zeeshan's mix, cut only), delivery gate {gate(S)}, independent review {review(S)}" for S in ORDER) + ".",
]
item = {}
json.dump(dict(decided=decided, item=item), open(f"{W9}/decided.json", "w"), indent=1)
print(len(decided), "decided lines")
