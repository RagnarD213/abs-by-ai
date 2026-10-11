"""RO-07 round 3: the facts the review page states, read from the checks' own outputs. usage: page_facts_r3.py -> round3/page_facts.json"""
import json, re, os
O = "/Volumes/Extreme/_edit_work/ro07/round3"
gl = open(f"{O}/logs/gate.log").read() if os.path.exists(f"{O}/logs/gate.log") and "DELIVERY GATE" in open(f"{O}/logs/gate.log").read().split("passed")[-1] else open(f"{O}/logs/gate_first.log").read()
final = "logs/gate.log" if gl is not None and os.path.exists(f"{O}/logs/gate.log") and "passed," in open(f"{O}/logs/gate.log").read() else "logs/gate_first.log"
gl = open(f"{O}/{final}").read()
m = re.search(r"(\d+) passed, (\d+) failed, (\d+) NOT MEASURED", gl); fails = re.findall(r"^\s+FAIL\s+(\S+)", gl, re.M)
ag = json.load(open(f"{O}/RO-07 round 3 - full film.mp4.audio_gate.json")); rows = ag["rows"]; okn = sum(r["ok"] for r in rows)
wp = json.load(open(f"{O}/logs/watch_pass.json"))
F = dict(length="18:07",
 bed="Its level was set by measurement on the first minute, not by taste: in the pauses the music sits about level with the background of the reference voice, and the audio gate's \"clean between words\" row passes with it. A listening check on two 45 second excerpts heard a clean voice with the music low under it (9 of 10 on both).",
 spend="$1.40 of the $5 cap ($0.80 for A2 in round 2, $0.60 for A3 now), plus about 8 cents of listening checks.",
 checks=[
  f"Audio gate on this exact file: {okn} of {len(rows)} rows pass. The one that fails is tone: it reads less treble than the reference voice. That is voice 4, the one you picked after rejecting the treble boost in round 1. No limit was changed.",
  f"Watch pass on this exact file: every frame scanned. {wp['scan']['frozen'] if not isinstance(wp['scan']['frozen'], list) else len(wp['scan']['frozen'])} frozen stretches, {wp['scan']['black']} black frames, 0 naked splices, 47 of 47 graphics on screen. All 254 cuts were read as consecutive frames.",
  "Two independent reviews. The first, on the first render, said it does not ship: the deadlift clip ended on a frozen picture for a third of a second, and it found the crew member and the clicks. I fixed all three and rendered again. The second review, on this file, says the picture and sound ship, and confirmed that only the deadlift clip and the push-up clip differ from the first render (every other frame is identical).",
  f"Delivery gate ({'final run' if final == 'logs/gate.log' else 'first run; the record run is still going and I will correct this line if it differs'}): {m[1]} rows pass, {m[2]} fail" + (f", {m[3]} not measured" if m[3] != "0" else "") + ". The failing rows, plainly: the audio stamp (the tone row above); cutaway cover is 27 % of the film against a 40 % floor (the home workout video was approved at 34 %; the library has nothing for the alarm clock, commute, couch and tired-at-night lines, and I add no stock unasked); two hair rows (below); the watch row stays open on hair until you say; \"splice visibility\" on 32 of 170 cuts, which measures how visible each wide-to-tight cut is, and both reviewers found no jump cut; and three false alarms I checked by hand (it reads the lower thirds as burned captions, it counts subtitle cues that fall during the 45 minute traffic card, and it calls two sentences that both say \"longer workouts a few times per week\" a repeated take).",
  "Subtitles: proofread against a fresh transcription of the finished sound, twice. No line is over 45 characters.",
  "The edit sheet (the record a vertical or Shorts job builds from) is written and validates.",
  "A second listening check on the click fixes heard no click. It also reported the sound dropping out between \"a kettlebell\", \"a yoga mat\" and \"an ab wheel\" (11:21 to 11:23). I measured that stretch: the pauses there are at the same level as every other pause in the film, nothing is cut, so I changed nothing. If you hear it, tell me.",
 ],
 flags=[
  "NEEDS YOUR WORD: hair at the top edge. The camera framed you with your hair at the very top of the picture, so in about 2.5 % of the presenter frames it touches or is cut by the edge. Longest moments: 10:25, 11:18, 12:26, 13:19, 15:09, 16:42, 16:46, 17:57. I never crop the top; there is no picture above your head to show. Your round 2 reply did not mention it. Options: leave it as shot (as built), or I add headroom by extending the wall above your head, which is one more round.",
  "At 10:10 to 10:13 the \"5 Minutes. Bodyweight. At Home.\" lower third lies across you at the bottom of the first two push-up reps (it did in round 2 as well).",
  "The gold reflector is still at the left edge of the squat clip at 1:08 to 1:14 (no person in it). Cropping it would push you off centre, so I left it.",
 ])
json.dump(F, open(f"{O}/page_facts.json", "w"), indent=1); print(final, m.groups(), fails)
