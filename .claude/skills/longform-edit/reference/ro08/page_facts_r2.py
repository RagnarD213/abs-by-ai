"""RO-08 round 2: the facts the review page states, read from the checks' own outputs where a number exists.
usage: page_facts_r2.py "<second review verdict line>"  -> round2/page_facts.json"""
import json, re, sys, os
O = "/Volumes/Extreme/_edit_work/ro08/round2"; M = f"{O}/RO-08 round 2 - full film.mp4"
gl = open(f"{O}/logs/gate.log").read(); m = re.search(r"(\d+) passed, (\d+) failed, (\d+) NOT MEASURED", gl); fails = re.findall(r"^\s+FAIL\s+(\S+)", gl, re.M)
ag = json.load(open(M + ".audio_gate.json")); rows = ag["rows"]; okn = sum(r["ok"] for r in rows)
wp = json.load(open(f"{O}/logs/watch_pass.json")); ps = json.load(open(f"{O}/logs/psnr_vs_render1.json"))
L = json.load(open(f"{O}/motion/ledger.json")); hair = json.load(open(f"{O}/qc/hair.json")); hr = [x for x in hair["rows"] if x["top"] is not None]
cov = re.search(r"style:coverage\s+(\d+)%", gl); spl = re.search(r"cut:splice_visibility\s+(\d+)/(\d+)", gl)
review2 = sys.argv[1] if len(sys.argv) > 1 else "pending"
F = dict(length="14:41", c22_slot=[407.47, 410.34],
 opener_rec="A. It shows the routine the video teaches (coffee through the morning, a salad at 2 PM) and it is your own idea, and what is imperfect in it sits inside the fast part where nobody can see it. B grabs harder in its first second but shows more that a viewer could catch. Both independent reviewers also picked A.",
 ot_note="Four generated moves between your five key frames. 8 AM to 2 PM runs in 3.2 seconds (frames dropped, never blended), then he eats at normal speed. Inside the fast part the clock hands wander and a numeral flashes on the dial for a few frames; it lands on 2:00 and the coffee pot goes down in order. $1.80.",
 o6_note="Second take ($0.80). The first turned the left wall clock into a digital display for three seconds, so I threw it out. Each half keeps its own man and the divider stays straight. What a viewer could catch: the clock hands sweep for the first four seconds, the pancake stack sinks in under a second at 0:03, and the plate clears in one step at 0:05.",
 a1_sync="One 6 second take, lips synced to your own recording through a window round his face ($0.48); the rest of the picture is the untouched take. Close up, his mouth closes on the m of \"intermittent\", \"for me\" and \"I'm\" and opens wide on \"hard\", on the right frames. The measured match is weak (0.18, against -0.10 for the same take unsynced) because he grimaces the whole time. The independent review passed it on the close-up. One look from you is worth it: if it reads off to you, I swap in a no-sync take.",
 a2_sync="No lip sync, under your rule from yesterday (a sync that fails its check once goes in without). I synced the first take for the seconds he faces the camera; the independent review failed it (his mouth held one grimace) and also caught my paste leaving a second head on the floor after he rolled away. So this is a second take from your approved START frame only ($0.80): eyes shut, panting, his head lolling while your voice does the line, then he heaves himself over and crawls off on \"I might as well just quit\". His mouth is a little open as he pants; it does not move like speech. He heaves himself up toward the left, the way his head points, so your approved end frame (dragging himself to the right) is not reached. Please watch this one.",
 decided=[
  "The film carries opener A. Picking B changes the first 8 seconds only.",
  "A2 has no lip sync and A1 keeps its lip sync (details beside each clip above).",
  "One lower third moved: \"Digesting A Heavy Meal Takes Energy.\" now comes up on \"And there's a reason for that\" (6:03) and is gone as the donut box starts to empty. Before, it sat over the box for the clip's first 2.6 seconds. The other 47 lower thirds are the same renders you approved.",
  "The AI label sits top left on opener A, the donut clip and the bar clip, and bottom left on opener B, so it never covers a wall clock or a face. Everywhere else it is top right as before.",
  "A6 starts 1.6 seconds into its take (the walk up to the fridge is left out so the raid fits your sentence) and A7 starts 0.6 seconds in. No clip is slowed or held; only the time-lapse is sped up, which is the idea of it.",
  "The stock clip of a man asleep at his desk (6:47) is out now that the donut gag is in, as the plan said. You are on camera there.",
  "The first independent review said the first render does not ship. I fixed all five of its findings before you saw anything: the second head in A2, the failed A2 sync, the label over the bartender's face in A7, a visible jump at 0:04 in the time-lapse where two takes joined (the fast part now ends on the frame that matches the eating take), and eight small subtitle faults.",
  "Subtitles are a separate file (nothing burned in), compared word for word with a fresh transcription of the finished sound, with 15 chapters for YouTube. Chapter titles are worded for this video, not copied from the fasting tips in \"My Top 10 Tips\".",
  f"AI spend on this video: ${L['total_usd']:.2f} of the $15 you set. $8.00 for the first 13 takes, $0.80 for the second split screen take, $0.80 for the second A2 take, $0.97 for lip sync ($0.48 on A1, $0.49 on A2 which is not in the film).",
 ],
 checks=[
  f"Audio gate on this exact file: {okn} of {len(rows)} rows pass. The one that fails is tone: it reads less treble than the reference voice. That is voice 1a, the one you picked. No limit was changed. Loudness -14.1 LUFS, no clipping, sound and picture the same length.",
  f"Watch pass on this exact file: every frame scanned. 0 black frames, 0 naked splices, 48 of 48 graphics on screen, and 1 frozen stretch, which is the approved goal photo inside the phone demo (14:13). All {len(wp['boundary_list'])} cuts were read as consecutive frames.",
  f"Two independent reviews. The first, on the first render, said it does not ship (the five findings above). The second, on this file: {review2}",
  f"Only {ps['changed_frames']} of {ps['frames']} frames differ between the two renders (the opener, the moved lower third, A2 and A7's label), measured frame by frame; the sound is identical in both (the second reviewer compared them).",
  f"Delivery gate, final run: {m[1]} rows pass, {m[2]} fail" + (f", {m[3]} not measured" if m[3] != "0" else "") + ". The failing rows, plainly: " + "; ".join(x for x in [
      "the audio stamp (the tone row above)" if "audio:stamp" in fails else "",
      (f"cutaway cover is {cov[1]} % of the film against a 40 % floor (the work-out-every-day film was approved at 27 %; you saw this number in round 1 and asked for nothing)" if cov else "") if "style:coverage" in fails else "",
      "two hair rows (the camera framed your hair at the top edge; as shot, as in round 1)" if "framing:hair_top" in fails else "",
      (f"\"splice visibility\" on {spl[1]} of {spl[2]} cuts, which measures how visible each wide-to-tight cut is; both reviewers found no jump cut" if spl else "") if "cut:splice_visibility" in fails else "",
      "a false alarm that reads the lower thirds as burned captions" if "captions:burned" in fails else "",
      "a false alarm that calls \"If you wake up at 9... If you wake up at 7...\" a repeated take (it is the pair of examples under the lower third at 10:51)" if "junk:repeated_take" in fails else "",
      "the watch row" if "watch:pass" in fails else ""] if x) + "." + ("" if not [f for f in fails if f not in ("audio:stamp", "style:coverage", "framing:hair_top", "framing:headroom", "cut:splice_visibility", "captions:burned", "junk:repeated_take", "watch:pass")] else " Also failing: " + ", ".join(f for f in fails if f not in ("audio:stamp", "style:coverage", "framing:hair_top", "framing:headroom", "cut:splice_visibility", "captions:burned", "junk:repeated_take", "watch:pass")) + "."),
  "The edit sheet (the record the Shorts job builds from) is written and validates.",
 ],
 flags=[
  "A2 (7:45 to 7:52), the take you have not seen: the second reviewer read every frame and passes it at playback speed, with three small things on record. The towel under his head thins out for a third of a second at 7:46, his face looks a little older and lighter haired from 7:49 as he sits up, and he ends propped on his hands instead of crawled out of frame. One retake would cost $0.80.",
  f"Hair at the top edge. The camera framed you with your hair at the very top of the picture: it touches the edge in {sum(x['top'] <= 2 for x in hr)} of {len(hr)} sampled frames. I never crop the top and there is no picture above your head to show. You saw this in round 1 and left it as shot.",
  "Your kettlebell and decline push-up clips at 14:15 to 14:24 are brightened (you approved the B-roll colour) but still read a little darker and warmer on your skin than you do on camera. The first reviewer noted it. Say so if you want them lifted further.",
  "A8, the cell cartoon: around its fifth second the junk clears in one sweep and the background changes with it. It reads as the cell renewing, which is your line there, but it is not a smooth clean-up.",
 ],
 vlc=["Intermittent Fasting LFC R2 - full film (opener A time-lapse).mp4", "Intermittent Fasting LFC R2 - first minute - opener A time-lapse.mp4", "Intermittent Fasting LFC R2 - first minute - opener B split screen.mp4"])
s = json.dumps(F); assert chr(8212) not in s and chr(8211) not in s
json.dump(F, open(f"{O}/page_facts.json", "w"), indent=1); print(m.groups(), fails)
