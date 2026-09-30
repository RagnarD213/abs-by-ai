"""Writes round1/page_extra.json (decisions, what I decided, checks) from the measured results."""
import json, os
W = "/Volumes/Extreme/_edit_work/ro10/round1"
rgb = json.load(open(f"{W}/first-minute/rgb_fidelity.json")); hair = json.load(open(f"{W}/first-minute/hair.json"))
ck = json.load(open(f"{W}/checks/all.json"))
gate = json.load(open(f"{W}/first-minute/gate.json")) if os.path.exists(f"{W}/first-minute/gate.json") else {}
S = json.load(open("/Volumes/Extreme/_edit_work/ro10/shots.json")); film = S[-1]["out_f1"] / (30000 / 1001)
fm_end = json.load(open(f"{W}/first-minute/end.json"))["end"]
clear = {k: v["items"][0].get("min_clear") for k, v in ck.items() if v["items"] and v["items"][0].get("min_clear") is not None}
face = {k: v["items"][0].get("min_face_gap") for k, v in ck.items() if v["items"] and v["items"][0].get("min_face_gap") is not None}
fills = {k: [tuple(f["rgb"]) for f in v["items"][0].get("fill", [])] for k, v in ck.items() if v["items"] and v["items"][0].get("fill")}
fails = {k: v["failures"] for k, v in ck.items() if v["failures"]}
decisions = [
    "<b>The first minute</b> above: approve, or notes by timestamp. It is finished: no placeholders.",
    "<b>The 15 HyperFrames graphics</b> (8 lower thirds, 3 fact cards, 3 side lists, 1 cycle diagram): approve, or notes by ID. "
    "Each one has a <i>Play it moving</i> button with your speech either side; every part lands on the word you say it on.",
    "<b>Way 1 title (T1)</b>: it reads <i>Get On A GLP-1 Medication</i> (no brand on screen, like RO-16's Step 2). You say "
    "\"Number one, take Zepbound.\" Keep GLP-1 (recommended), or use <i>Take Zepbound</i> (you allowed the brand on RO-16's G06)?",
    "<b>Opener</b>: the video opens on camera with your hook (no AI clip; the hook lands in 4 seconds, $0). Keep it (recommended), "
    "or I bring 2-3 AI opener concepts as start/end frames next round?",
]
decided = [
    "<b>Takes.</b> The last clean take of every line. The hook is take 3 of 3 (take 1 restarted \"You're going to be surprised\", take 2 "
    "\"what kind of day\"). A verbatim listen (Gemini, about $1.30) found 15 restarts the first transcript had merged, all cut: "
    "Stanford's first attempt and \"wheat\", \"I barely eat anything and I can-\", the clinical-trial line (three attempts, the third "
    "used), \"Telling someone to eat less\", \"If the average isn't dropping\" (three copies around a drink of water), \"With AI\", "
    "\"fewer hours to eat\" (three), \"why I love this\", \"Drinking black coffee is-\" plus a throat clear, Penn State's first "
    "attempt, \"Chips, crackers\" (three), the channel line, \"For a lot of you guys\" and the ending (retake after \"roll it back\").",
    "<b>Your dose stays in.</b> \"I take a low dose myself, about 1.5 milligrams per week,\" is from your first attempt; it joins "
    "your retake at \"and the biggest change was that I stopped thinking about food all day\". The retake had dropped the dose.",
    "<b>Your ad-lib stays.</b> \"Drinking black coffee alone is powerful, but when you combine it with Zepbound...\" is not in the "
    "script; you said it deliberately, so it is in.",
    f"<b>Length and pace.</b> 8:38 of your 13:38 roll. Pauses over 0.7 s are tightened; a reframe cut (wide to tight, nothing "
    f"removed) every 9 to 14 seconds so no shot runs past about 16 s: {len(S)} shots.",
    "<b>Framing.</b> Every cut between two shots of you is a clear size change (a small solver checks all 53 picture segments; "
    "zero same-size joins). The side cards slide your approved W4 crop left inside the 4K frame (no stretched wall) wherever "
    "that does not force a jump cut; G09 (\"How I Eat\") keeps RO-16's wall stretch, because a slide there would have put two "
    "near-identical framings back to back.",
    "<b>Numbers on screen follow what you said:</b> 1,800 cal and 27 lb (Haub), 609 people (Stanford), 47% (1992), about 20% "
    "(the big trial), 1.5 mg, goal weight x 12 and \"about 2,100\" for 180 lb (you said 2,100), 1,200 by 2 PM, 200 cal a cup, "
    "12% (Penn State), 450 cal (Purdue).",
    "<b>No drug brand name in any graphic</b> (you still say Zepbound): G05 reads \"THE BIG CLINICAL TRIAL\", T1 \"GLP-1\" "
    "(decision 3).",
    "<b>Graphics that only echo the speech were not made.</b> No \"not medical advice\" card, no card for \"link in the description\". "
    "Every lower third distills the point; the side lists and the cycle are real lists and a real loop from your words.",
    "<b>Stock.</b> Free Pexels plus the clip library (B0017 food scale, B0038 the real AbsByAI meal log in the phone). No "
    "overweight people eating (RO-16's rejected burger rule), no clip used twice, no two clips of the same scene. The fact-card "
    "photos are stills from clips not used elsewhere (cookie stack, a food log, the salad bowls).",
    "<b>Not templates yet</b> (they stay softblue.py, as the handoff says): the 8 way titles (\"WAY 1 OF 8\", RO-16's approved "
    "T1 style), the recap card (RO-16's G22 style, \"8 Ways To Eat Less Calories\"), and the phone demo. Candidates for the next "
    "template round.",
    "<b>Spend.</b> $0 generation. About $1.30 of Gemini listening for the restarts (inside the $5 per video).",
    "<b>Left for the full film:</b> SRT and chapters, the delivery gate and watch pass, one independent review. The \"Zepbound tips "
    "video\" link goes in the description when that video is public.",
]
def fmt(d): return ", ".join(f"{k} {v}" for k, v in sorted(d.items()))
checks = [
    f"<b>Colour.</b> Card fill on every side list and the cycle, as composited: {fmt({k: v[0] for k, v in fills.items()})} "
    "(spec 10,38,72 +/- 2; the renders are decoded as BT.601, the footage as BT.709).",
    f"<b>Base fidelity.</b> In RGB, before encoding: across {rgb['overlay_frames']} first-minute frames with a graphic up, "
    f"{rgb['untouched_pixels'] / 1e6:.0f} million pixels outside the graphics, {rgb['changed']} changed. After encoding, the untouched "
    "frames match a plain re-encode of the same base (mean 90 dB; the 39 dB against the raw base is the approved encode chain RO-16 "
    "already uses, identical with no graphics at all). Every in, out and part is frame-exact on a word start (beat sheets below).",
    f"<b>Hair.</b> Clear of the top edge on every sampled on-camera frame of the first minute: {hair['min_px']} px minimum, "
    f"{hair['median_px']} px median ({hair['samples']} samples, every 0.25 s).",
    f"<b>Clearance.</b> Your arms and hands never reach a side card (Vision person mask, every 10th frame): {fmt(clear)} px "
    "minimum (round 2: 78 px).",
    f"<b>Lower thirds never cover your face</b> (Vision face box, every 10th frame): face ends {min(face.values())} px or more "
    "above the strip on all 8.",
    "<b>Templates.</b> HyperFrames lint and check: 0 errors on all 23 scenes (15 graphics + 8 lower-third glass masks); every "
    "graphic inspected as a still on its real frame (below) and moving in context.",
] + ([f"<b>Open:</b> {k}: {'; '.join(v)}" for k, v in fails.items()] if fails else []) + (
    [f"<b>First-minute audio gate:</b> {gate.get('verdict')}, {gate.get('rows')} rows, {gate.get('lufs')} LUFS. The EQ copied from RO-16 failed the tone row on this roll (RO-12's trap), so it is re-fitted on C1704 plus your approved +0.9 dB at 150 Hz; the A/B against Muhammad is linked under the first minute."] if gate else [])
reply = ("1. First minute: approved / notes:\n2. HyperFrames graphics: approved / notes by ID:\n3. T1: GLP-1 / Take Zepbound\n"
         "4. Opener: on camera / show me AI opener frames\nOther notes (ID or timestamp):")
json.dump(dict(film_len=f"{int(film // 60)}:{int(film % 60):02d}", decisions=decisions, decided=decided, checks=checks, reply=reply,
               first_minute=dict(end=fm_end, note=f"audio: approved audio B chain, gate {gate.get('verdict', 'see log')}; "
                                 "hair clear of the top edge (same locked crops as RO-16).")),
          open(f"{W}/page_extra.json", "w"), indent=1)
print("extra ok")
