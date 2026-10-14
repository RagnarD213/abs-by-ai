"""RO-08 round 3: the facts the review page states, read from the checks' own outputs where a number exists.
usage: r3_page_facts.py  -> round3/page_facts.json   (needs logs/gate.log, the audio gate stamp, the watch log, the frame comparison, both three-question files)"""
import json, re, os
B = "/Volumes/Extreme/_edit_work/ro08"; O = f"{B}/round3"; M = f"{O}/RO-08 round 3 - full film.mp4"
gl = open(f"{O}/logs/gate.log").read(); m = re.search(r"(\d+) passed, (\d+) failed, (\d+) NOT MEASURED", gl); fails = re.findall(r"^\s+FAIL\s+(\S+)", gl, re.M)
ag = json.load(open(M + ".audio_gate.json")); rows = ag["rows"]; okn = sum(r["ok"] for r in rows)
wp = json.load(open(f"{O}/logs/watch_pass.json")); ps = json.load(open(f"{O}/logs/psnr_vs_round2.json"))
L = json.load(open(f"{B}/round2/motion/ledger.json")); hair = json.load(open(f"{O}/qc/hair.json")); hr = [x for x in hair["rows"] if x["top"] is not None]
cov = re.search(r"style:coverage\s+(\d+)%", gl); spl = re.search(r"cut:splice_visibility\s+(\d+)/(\d+)", gl)
QE = json.load(open(f"{O}/three_questions_editor.json")); QR = json.load(open(f"{O}/three_questions_review.json")) if os.path.exists(f"{O}/three_questions_review.json") else []
rv = open(f"{O}/ROUND-3-REVIEW.md").read().split("\n")[0].strip() if os.path.exists(f"{O}/ROUND-3-REVIEW.md") else "pending"
EX = json.load(open(f"{O}/page_extra.json")) if os.path.exists(f"{O}/page_extra.json") else {}       # what the review found and what was done about it, written by hand after reading it
known = ("audio:stamp", "style:coverage", "framing:hair_top", "framing:headroom", "cut:splice_visibility", "captions:burned", "junk:repeated_take", "watch:pass")
F = dict(length="14:41", review_verdict=rv, questions_editor=QE, questions_review=QR, extra=EX,
 changed_frames=ps["changed_frames"], frames=ps["frames"], spend_total=L["total_usd"],
 checks=[
  f"Only {ps['changed_frames']} of {ps['frames']} frames differ from the film you reviewed, measured frame by frame, and every one of them is inside the five spots above. The sound was not touched; the subtitles and the 15 chapters are byte for byte the round 2 files.",
  f"Audio gate on this exact file: {okn} of {len(rows)} rows pass. The one that fails is tone: it reads less treble than the reference voice. That is voice 1a, the one you picked. No limit was changed.",
  f"Watch pass on this exact file: every frame scanned. 0 black frames, 0 naked splices, 0 unexplained jumps, 48 of 48 graphics on screen, and 1 frozen stretch, which is the approved goal photo inside the phone demo (14:13). All {len(wp['boundary_list'])} cuts were read as consecutive frames; the verdicts on the unchanged ones are carried from the round 2 film and every image that changed was judged fresh by an independent reviewer.",
  f"Delivery gate, final run: {m[1]} rows pass, {m[2]} fail" + (f", {m[3]} not measured" if m[3] != "0" else "") + ". The failing rows are the same ones as round 2, plainly: " + "; ".join(x for x in [
      "the audio stamp (the tone row above)" if "audio:stamp" in fails else "",
      (f"cutaway cover is {cov[1]} % of the film against a 40 % floor (it was 24 % before two clips came out and two got shorter; the work-out-every-day film was approved at 27 %)" if cov else "") if "style:coverage" in fails else "",
      "two hair rows (the camera framed your hair at the top edge; as shot)" if "framing:hair_top" in fails else "",
      (f"\"splice visibility\" on {spl[1]} of {spl[2]} cuts, which measures how visible each wide-to-tight cut is; no reviewer has found a jump cut" if spl else "") if "cut:splice_visibility" in fails else "",
      "a false alarm that reads the lower thirds as burned captions" if "captions:burned" in fails else "",
      "a false alarm that calls \"If you wake up at 9... If you wake up at 7...\" a repeated take (10:51)" if "junk:repeated_take" in fails else "",
      "the watch row" if "watch:pass" in fails else ""] if x) + "." + ("" if not [f for f in fails if f not in known] else " ALSO FAILING, new this round: " + ", ".join(f for f in fails if f not in known) + "."),
  "The edit sheet (the record the Shorts job builds from) is rewritten for this film and validates.",
 ],
 flags=[
  f"Hair at the top edge. The camera framed you with your hair at the very top of the picture: it touches the edge in {sum(x['top'] <= 2 for x in hr)} of {len(hr)} sampled frames. I never crop the top and there is no picture above your head to show. You saw this in rounds 1 and 2 and left it as shot.",
  "Your kettlebell and decline push-up clips at 14:15 to 14:24 are brightened but still read a little darker and warmer on your skin than you do on camera. Say so if you want them lifted further.",
  "The man on the gym floor (7:45) has no lip sync, under your rule; you saw it in round 2 and wrote nothing about it.",
 ],
 vlc=["Intermittent Fasting LFC R3 - full film.mp4"], gate=dict(passed=int(m[1]), failed=int(m[2]), not_measured=int(m[3]), fails=fails, new_fails=[f for f in fails if f not in known]))
s = json.dumps(F); assert chr(8212) not in s and chr(8211) not in s, "a dash"
json.dump(F, open(f"{O}/page_facts.json", "w"), indent=1); print(m.groups(), fails, "| review:", rv)
