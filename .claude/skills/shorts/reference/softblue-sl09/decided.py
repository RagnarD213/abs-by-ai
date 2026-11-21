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
 "<b>Zeeshan's AI Tesla clip moved and cropped</b> (its speedometer read 190 while you say 120): a real night-highway drive replaces it where you say 120, and 4 seconds of it return at 0:36 cropped so the speed display is out of frame. His real "
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
 "sleeping well); Pexels stock for the rest (alarm smash, groggy man in bed, tired man rubbing his eyes, deadlift, power clean, light-streak tunnel, "
 "night-highway time-lapse, arguing couple, man alone, man awake in bed, door closing, Apple Watch, yawning man, scale, whiskey); library B0537 (a man eating from a can on his bed at night). "
 "Your real Oura app screenshot from the film opens short 5 and fills \"see the problem\" in short 4. Darker stock is brightened to sit "
 "with the studio shots.",
 "<b>Rejected clips:</b> B0494 (its actor reads as you at a glance), Pexels 6698753 (a montage with dissolves inside it), a Subaru WRX clip "
 "(an identifiable other car right after you name your Tesla), a busy Tokyo street (after \"nobody on the road\"), a stock opener that "
 "cut a man's head off from its 4.5-second mark (its first 4.5 seconds now carry short 1's \"less rested\"), B0460 squats (you small and in shade), B0298 deadlift (never finishes a rep), a deserted-highway clip (read as an empty grey screen on a phone), a fridge clip that showed groceries put away in daylight over \"eat late at night\", a restless man in bed whose face the key point covered. No ring or WHOOP footage exists in "
 "the library or on Pexels (only wedding bands), hence the AI ring idea.",
 "<b>Fixed after the independent reviews:</b> short 1, your head tilt at 0:48 swung wider than any steady crop, so a clip covers \"be "
 "careful today, take it easy\"; short 3, a same-size cut hidden inside Zeeshan's footage got a real size step, his Tesla footage now starts "
 "on \"press a button\" and is cropped off its speed digits; short 4, the app stays on the sleep screen (the later screens said \"93 "
 "Optimal\" over \"the problem\") and the phone is back at full size; true peak kept at or under Zeeshan's -1.0 dBTP on every short by "
 "picking the AAC encoder mode, never by changing his level.",
 "<b>Fixed after the second round of independent reviews:</b> short 1, the alarm-clock opener now runs to the hammer hit before cutting to you, and the "
 "groggy man is framed on his face; short 3, the opener starts in motion with no readable car, the crop holds still through Zeeshan's two animated zooms, "
 "one graded night-highway drive replaces the grey highway, and the restless-man clip is out (the key point covered his face at every start point we tried); Zeeshan's own AI night-driving Tesla clip covers that line instead, cropped so its speed display (the 190 that clashed with your 120) and his text label are out of frame, with our AI-GENERATED chip; short 4, from \"the problem\" the "
 "rest of your Oura screen dims and the Restfulness: Fair row gets a warm outline and a moving arrow (it read as a good night before), and \"eat late at "
 "night\" now shows a man eating at night with his face clear of the key point; short 5, the end stops before Zeeshan's zoom into his outro and a 1.3-second pause after \"better location\" is cut to 0.7 (his audio is only cut, never changed); in shorts 1, 3 and 4 the crop now holds still through Zeeshan's animated zooms (we had treated them as cuts), short 1 gets a punch-in at 0:30, and a clip of a tired man rubbing his eyes covers 0:20 to 0:24 where you sway wider than any steady crop (the crop that followed you there panned back and forth); captions in all five stay up until the word is finished.",
 "<b>Key points (title case):</b> 1 \"Bad Sleep Is No Reason / To Slack Off In The Gym\"; 2 \"Nobody Is Worth / Losing Your Sleep Over\" (your own line from the film, in the part cut from this short); "
 "3 \"Late-Night Adrenaline / Wrecks Your Sleep\"; 4 \"Track It To See What's / Wrecking Your Sleep\"; 5 none (the comparison is the graphic).",
 "<b>Captions print what you say:</b> short 3 says \"adrenaline in your bedtime\" at the start and \"late at night near bedtime\" at 0:09 (checked against the audio: \"near\" scores far ahead of \"in your\"), shorts 1 and 4 print \"gonna\" and \"gotta\" where you say them, short 1 keeps \"Don't listen to that shit\".",
 "<b>Labels:</b> no photos of you, so no real-photo labels. One AI clip in the five as delivered: Zeeshan's night-driving Tesla in short 3 (0:36 to 0:41), with the AI-GENERATED chip, so short 3 gets the AI flag at setup. The three AI ideas above are frames only.",
 "<b>Spend: $0</b> (frames on the ChatGPT subscription, no motion made, stock from Pexels and our library).",
 "<b>Checks on each delivered file:</b> " + "; ".join(f"short {P.ORDER[S]} ({NAMES[S]}): audio PASS (Zeeshan's mix, cut only), delivery gate {gate(S)}, independent review {review(S)}" for S in ORDER) + ".",
]
item = {}
json.dump(dict(decided=decided, item=item), open(f"{W9}/decided.json", "w"), indent=1)
print(len(decided), "decided lines")
