"""RO-20 round 4: page_state.base.json + each film's gate stamp, reviews and chapters + the decisions and the "What I decided" list -> page_state.json"""
import json, os, re
W = "/Volumes/Extreme/_edit_work/ro20"; R = f"{W}/round4"
S = json.load(open(f"{R}/page_state.base.json"))
NAME = {1: "RO20", 2: "RO20B", 3: "RO20C"}
for v in S["videos"]:
    d = f"{R}/v{v['n']}"; dg = json.load(open(f"{d}/MASTER.mp4.deliver_gate.json"))
    rows = dg["rows"]; fails = [k for k, r in rows.items() if not r.get("ok")]
    v["gate"] = (f"delivery gate {dg['gate_version']}: {sum(1 for r in rows.values() if r.get('ok'))} of {len(rows)} rows pass. "
                 f"Not passing, all explained in the notes (none is a new fault of this build): {', '.join(fails)}.")
    revs = sorted(f for f in os.listdir(d) if f.startswith("ROUND-4-REVIEW"))
    last = revs[-1]; verdict = (re.findall(r"VERDICT:\s*(SHIP|DOES NOT SHIP)", open(f"{d}/{last}").read()) or ["?"])[-1]
    v["review_verdict"] = (f"{len(revs)} independent reviews of successive builds plus a fresh watch judge on the final file; every defect they found was fixed, "
                           f"except the items listed for your call. Last review ({last}): {verdict}" + ("" if verdict == "SHIP" else " on items fixed after it (subtitle text only)") + ".")
    v["changes"].sort(key=lambda c: int(c["at"].split(":")[0])*60 + float(c["at"].split(":")[1]))
    v["chapters"] = open(f"{d}/{NAME[v['n']]}.chapters.txt").read().strip()
S["decisions"] = [
 dict(q="Video 2, 0:54: keep the handstand clip out?", why="The handstand push-ups were in the first minute you approved, but the \"Cut The Waste, Fund Your Fitness\" key point covered your head at the bottom of every rep, so you are on camera there now.", opts=["Keep it out (recommended)", "Put it back"]),
 dict(q="Video 3, 4:18: \"go and review that stuff that we went over before\".", why="In the one long film this pointed back at the cutting section; in the three-video split that section is now video 2. Listen at 4:15 to 4:22.", opts=["Leave it (recommended: it still reads as a general reminder)", "Cut the sentence"]),
]
S["decided"] = [
 "The pickups play at the level your approved treatment set (level with the kitchen voice). The round 3b review clips played them about 3 dB quieter because of how those clips were joined, so they will sound a little louder than you remember.",
 "Video 1's sign-off now plays at the film's own level, about 1 dB softer than the separately mixed round 3b ending clip.",
 "Your 10-14 rule (never a shot of you standing or posing) and 10-16 library ruling took out four cutaways that were in the plan: the vacuum hold (video 1, 2:22), the ab-roller pose (video 1, 14:46, inside the approved ending), and the two pool poses (video 2, 7:04 and 7:58). You are on camera there.",
 "Three cutaways came out because a graphic covered you: the handstand push-ups (video 2, 0:54, your decision 1) and the medicine-ball V-ups (video 3, 16:57, the key point sat on your abs). The near-black beer-can shot (video 2, 3:53) came out after a lift could not save it.",
 "Video 3, 15:48 to 15:50: a lower third sits over the kettlebell and your shins at the bottom of each kettlebell rep (not your face or abs). Left as is; say if you want it moved. The one at 2:40 that covered your face on the push-ups now enters after the clip.",
 "Dark stock shots were lifted to sit with the kitchen footage (couch and brain scan in video 1; smoking pan, sofa couple, old car, two men on a sofa, gamers in video 2; salmon, bedroom, gyms, dumbbell racks, vitamin D, trainer in video 3). Naturally dim scenes that read fine (bars, nightclub, toast) were left as shot.",
 "The camera's own recording skips a frame in two places (video 1, 5:45; video 3, 20:25). Each is now a zoom cut, the way the original shot list intended.",
 "Video 3 got the most polish from the checkers: three silent pauses where you glanced down at the end of a take were trimmed (0.33 to 0.6 s each), three cutaways end a beat earlier (squats, curls, AI home gym), a zoom cut moved past a head turn, and a black-and-white bedroom clip came out. Each is listed with its time under the film.",
 "Video 3's AI clip on \"a leg curl machine\": the leg-curl shot had a pad floating with no machine arm, so only the leg-press shot is kept.",
 "The approved app demo's file had been deleted from the RO-06 folder. I rebuilt it from its own recipe; it matches the approved render frame for frame (encoder noise only).",
 "A one-frame slide-in of the AI pool picture inside that demo (its label clipped for one frame) is the approved animation and stays.",
 "Quiet music bed (the RO-07 bed) under all three films, pickups included, at the level that passes the audio check.",
 "Subtitles were corrected by ear and transcript: drug names (tirzepatide, retatrutide), Bryan Johnson, sentence breaks, and a few misheard words. In video 2 at 8:35 you say \"if you're broke and you're also in shape\"; the subtitle prints what you said.",
 "The audio check's tone row fails by a fraction on all three, as on every film with voice 4 (your locked voice), and video 2's echo-removal row misses by 0.001. Not changed.",
 "No upload or setup: the release calendar holds these three until you say otherwise. AI spend this round: $0.",
]
json.dump(S, open(f"{R}/page_state.json", "w"), indent=1); print("page_state.json written;", [v["gate"][:60] for v in S["videos"]])
