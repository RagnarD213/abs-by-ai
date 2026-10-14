"""RO-08 round 3: the hand-written part of the review page (what the independent reviews found and what was done about each finding, Dan's
decisions, what I decided, the reply box) -> round3/page_extra.json. Also merges the reviewers' three-question answers into
round3/three_questions_review.json: review 1 read all eight AI clips on the first render (five of them have not changed a frame since),
review 3 re-read the donut clip on the third render, review 4 read the fridge raid and the donut clip as they now stand (and stopped a cut version of the cell cartoon), review 5 read the cell cartoon as it now ends.
Written after the reviews were read. usage: r3_page_extra.py"""
import json, os
B = "/Volumes/Extreme/_edit_work/ro08"; O = f"{B}/round3"; FPS = 30000/1001
R = {r["id"]: r for r in json.load(open(f"{B}/plan_resolved.json"))}; a5, a6, a8 = R["A5"], R["A6"], R["A8"]
def mm(t): return f"{int(t//60)}:{t % 60:04.1f}"
def ms(t): return f"{int(t//60)}:{int(t % 60):02d}"
def first(p): return open(p).read().split("\n")[0].strip().replace("VERDICT: ", "") if os.path.exists(p) else "pending"
IDS = ["OT", "A0158", "A8", "A5", "A1", "A2", "A6", "A7"]
r1 = json.load(open(f"{O}/render1/three_questions_review.json")); assert len(r1) == 8
merged = {i: dict(q, id=i, by="reviewer 1") for q, i in zip(r1, IDS)}
if os.path.exists(f"{O}/three_questions_review_3.json"): merged["A5"] = dict(json.load(open(f"{O}/three_questions_review_3.json"))[0], id="A5", by="reviewer 3")
if os.path.exists(f"{O}/three_questions_review_4.json"):
    for q in json.load(open(f"{O}/three_questions_review_4.json")):
        if q["id"] != "A8": merged[q["id"]] = dict(q, by="reviewer 4")          # its A8 answer was about the cut version that did not ship
if os.path.exists(f"{O}/three_questions_review_5.json"): merged["A8"] = dict(json.load(open(f"{O}/three_questions_review_5.json"))[0], id="A8", by="reviewer 5")
json.dump([merged[i] for i in IDS], open(f"{O}/three_questions_review.json", "w"), indent=1)
v1, v2, v3, v4, v5 = (first(f"{O}/ROUND-3-REVIEW-{k}.md") for k in (1, 2, 3, 4, 5))
X = dict(
 review_map={i: i for i in IDS},
 decisions=[
  dict(q=f"The midnight fridge raid ({ms(a6['t0'])}): I ended the clip 1.4 seconds early. Keep that, or put the ending back?",
       body="You did not name this clip, so this is yours to overrule. In the round 2 film, after he freezes with the spoon in his mouth, he lifts one leg out to the side and holds it in the air for about a second, and the clip ends there. It is the take reaching for the tiptoe pose in the end frame you approved and stopping halfway. Under your new rule the first independent reviewer would not bet on you passing it. The clip now ends on the frozen stare and you are on camera for \"is not going to work for you\". Free, and putting it back is free.",
       rec="keep the shorter clip. The frozen stare is the punchline and the held leg added nothing.",
       clips=[["A6-now", f"Now: ends on the stare ({ms(a6['t1'])})"], ["A6-round2", "Round 2: with the held leg (watch its last second)"]]),
  dict(q=f"The clean-up crew inside the cell ({ms(a8['t0'])}): I ended the clip before the sweep. Keep that, put the sweep back, or remake the ending?",
       body="You did not name this clip either. In the round 2 film, as the furnace flared at 5:00, the heaps of junk on both sides of the crew cleared away by themselves in about half a second. Your new rule quotes that exact sweep as a fault I had written on a page and shipped anyway. I first tried putting the change on a hard cut to the clean cell, and the fourth reviewer stopped that: in the clean part, rubble at the workers' feet goes on fading and a wheelbarrow breaks up, so the take has no clean second shot. So the clip now ends on \"for fuel\" (4:59.9), while the crew is still wheeling the junk to the furnace, and you say \"renews your cells and makes you younger\" on camera. It no longer shows the clean cell from the end frame you approved. One thing in the part that stays, so you hear it from me: at 4:57.5 a second loaded wheelbarrow turns up on the left, where two of the crew were shovelling a heap. The fifth reviewer does not think it is caught at speed; these are the same frames you watched in round 2. Putting the sweep back is free. Getting the clean cell back properly means two short new takes from your two approved frames joined by a cut, $0.80, which fits the $4.43 left in this video's budget.",
       rec="keep the shorter clip. If you miss the clean cell, say \"remake\" and I spend the $0.80.",
       clips=[["A8-now", "Now: ends before the sweep (4:59.9)"], ["A8-round2", "Round 2: the junk clears by itself (watch 5:00)"]]),
  dict(q="Finalize the film?",
       body="Yes, or your notes with a time. If you put either ending back, I make only that change, re-run every check on the new file, compare it frame by frame with this one, and close the film out without another review round, unless you ask to see it again."),
 ],
 a5_note=("Free: no new generation, so the AI spend on this video is unchanged at $10.57 of your $15. This is your second option, a part of the clip. "
          f"The first shot is 1.0 second, which is all the clean eating the take has before its clock starts to spin. The clip now starts on \"to digest\" ({mm(a5['t0'])}), 1.8 seconds later than before, so his head still lands on \"food coma\"; you are on camera until then. "
          "Two repairs inside it. The wall clock is steadied: in the take its minute hand ran round the dial while he sank and the 12 at the top turned into a 10, so each shot carries one still clock from a clean frame of the same take, nine o'clock then ten. "
          "And an orange smear in the box where the last donut was, a leftover of the old fast-forward that faded over the second shot's first frames, is painted out. That shot also starts a quarter second later than in my first render, where a reviewer found a faint smear on the desk beside the muffin. The independent reviewers found both leftovers in my first two renders; neither went out."),
 decided=[
  "The donut clip is built from the take you already paid for, in the order you gave: a part of the clip first. I did not spend on a retake because the two-shot cut answers all three questions.",
  "One framing change, at 1:53 to 2:04 (described beside the first change above). Every other shot is held at the size and crop of the round 2 film.",
  "The lower third \"Digesting A Heavy Meal Takes Energy.\" (6:03 to 6:06) is the same render as before. It now clears a full second before the donut clip starts; in round 2 it sat over the clip's first second.",
  "Two clips you had not named are cut down to the part that works, because the three questions caught them: the fridge raid and the cell cartoon. They are decisions 1 and 2 at the top, each with its round 2 version beside it. Nothing was regenerated and nothing was spent.",
  "This is the fifth render of the round and the only one sent to you. A fresh independent reviewer read each of the first four and stopped three of them: the first for a faint smear on the desk in the donut clip (and it flagged the fridge raid's held leg), the second for an orange smear in the donut box that I had not looked at, the fourth for the cell cartoon's clean shot. The third passed the donut clip with one note about a patch of mine, which I took out.",
  "The opener is your pick and is not reopened. For the record, the first reviewer notes that inside its fast-forward the salad bowl appears between his hands and the laptop closes and reopens (0:02.6 to 0:02.9); the eating at normal speed after it is clean.",
  "Subtitles and the 15 chapters are the round 2 files, unchanged, because the sound is unchanged.",
 ],
 new_flags=["Hair at the top edge, in four spots that a clip used to cover and you have not seen: 2:00 (a third of a second, in the new wider shot), 5:00 to 5:01 (just under a second, as you tip your head back on \"renews\"), 6:06 to 6:07 (just under a second, before the donut clip) and 12:15 (half a second, after the fridge raid). It is the same as-shot framing as the rest of the film (next flag), and your round 1 answer on it is recorded against each of these in the check log. If any of the four bothers you, give me the time and I will cover it."],
 checks_first=[f"Five independent reviews, each by a fresh reviewer who saw neither my notes nor the reviews before it. First render: {v1.lower()}. Second render: {v2.lower()}. Third render (the donut clip, frame by frame): {v3.lower()}. Fourth render (the fridge raid, the cell cartoon and the donut clip): {v4.lower()}, for the cell cartoon alone; it passed the fridge raid and the donut clip. This file (the cell cartoon as it now ends, and every cut that changed): {v5.lower()}."],
 reply="RO-08 round 3\n1. Fridge raid at 12:11 (keep the shorter clip / put the ending back):\n2. Cell cartoon at 4:55 (keep the shorter clip / put the sweep back / remake the ending for $0.80):\n3. Finalize (yes / no, or notes with a time):\n4. AI budget for long-form videos from now on ($15 per video / $15 per clip):\nAnything else (with a time):\n")
s = json.dumps(X); assert chr(8212) not in s and chr(8211) not in s, "a dash"
json.dump(X, open(f"{O}/page_extra.json", "w"), indent=1); print("page_extra written;", v1, "|", v2, "|", v3, "|", v4)
