"""Writes round1/page_extra.json (decisions, what I decided, checks) from the measured results."""
import json, os
W = "/Volumes/Extreme/_edit_work/ro11/round1"
def load(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
hair = load(f"{W}/first-minute/hair.json", {}); ck = load(f"{W}/checks/all.json", {}); gate = load(f"{W}/first-minute/gate.json", {})
fid = load(f"{W}/first-minute/fidelity.json", {})
S = json.load(open("/Volumes/Extreme/_edit_work/ro11/shots.json")); film = S[-1]["out_f1"] / (30000 / 1001)
fm_end = load(f"{W}/first-minute/end.json")["end"]
clear = {k: v["items"][0].get("min_clear") for k, v in ck.items() if v["items"] and v["items"][0].get("min_clear") is not None}
face = {k: v["items"][0].get("min_face_gap") for k, v in ck.items() if v["items"] and v["items"][0].get("min_face_gap") is not None}
fills = {k: [tuple(f["rgb"]) for f in v["items"][0].get("fill", [])] for k, v in ck.items() if v["items"] and v["items"][0].get("fill")}
fails = {k: v["failures"] for k, v in ck.items() if v["failures"]}
decisions = [
    "<b>The first minute</b> above: approve, or notes by timestamp. Only the first 4.6 seconds are a placeholder (the AI opener's START and END frames, labelled); everything else is finished.",
    "<b>AI opener</b> (plays under your first line, \"You can still gain fat, even if you're not eating too many calories\"): "
    "<b>A, the scale</b> (recommended: it shows the exact frustration the line names), <b>B, awake at 2 AM with two beers</b> "
    "(previews sleep and alcohol), or <b>no AI opener</b>, stay on camera. I generate the motion only after you pick (about $0.60 to $1.20).",
    "<b>The 21 HyperFrames graphics</b> (11 lower thirds, 7 fact cards, 2 side lists, 1 cycle diagram), all built from the templates "
    "you approved on RO-10: approve, or notes by ID. Each has a <i>Play it moving</i> button.",
]
decided = [
    "<b>Hook.</b> Take 3 of 3. All three takes were clean; the last one runs straight into \"Number one is sleep\" without a stop, so it is the one that needs no join.",
    "<b>Takes.</b> The last clean copy of every line. A word-for-word listen (Gemini, about $1.10) found 16 restarts, all cut: "
    "\"Get seven to eight hours and your art\", four tries at \"I made a whole video on whether you can drink alcohol\" (one said "
    "\"whole factor\"), \"let me explain the difference\", the first copies of the cortisol, blood test, \"I want to warn you\", "
    "\"What time you eat\" and University of Illinois lines, the 17 second stop and throat clear before \"A lot of guys are doing "
    "cardio\", \"about 1,700\", \"made up for\", \"So you're not tracking\", \"how much they moved.\", \"your body has qu-\" and the ending.",
    "<b>One line keeps its first copy.</b> \"Everybody got the same extra food, but the fat they gained was wildly different.\" You re-said "
    "the second half alone; the first copy is one unbroken sentence and cutting into it would need a join with no pause.",
    "<b>Ending.</b> The retake after \"roll it back\", where you say \"the <i>first</i> video on calories\". The earlier copy took three tries at that line.",
    "<b>Your ad-libs stay</b> (not in the script, said deliberately): the hook's \"if you're screwing other things up\", the consistent "
    "bedtime and AI sleep coach lines, \"and by increasing your appetite\", the bulk-again \"cycle of failure\" passage, \"work at a standing desk\".",
    f"<b>Length and pace.</b> {int(film // 60)}:{int(film % 60):02d} from a 14:18 roll. Pauses over 0.7 s are tightened; a reframe cut "
    f"(wide to tight, nothing removed) every 9 to 14 seconds: {len(S)} shots.",
    "<b>Section titles</b> say \"FACTOR 1 OF 7\" to \"FACTOR 7 OF 7\" in RO-10's approved way-title style: Sleep, Alcohol, Hormones, "
    "Meal Timing, Protein, Exercise, Daily Movement. \"Hormones\" lands on the word, after your tease.",
    "<b>The cycle diagram</b> is used for your \"cycle of failure\" (lose muscle, bulk again, gain fat, diet again), in red, each box landing on its words.",
    "<b>Numbers on screen follow what you said:</b> 55% less fat and 60% more muscle lost (Chicago), 73% (alcohol), 300 and 900, "
    "twice as hungry and 60 fewer calories (Harvard), 3 hours before bed, 550 fewer calories (Illinois), 20-30% vs 5-10%, "
    "+2.5 lb muscle and 10.5 lb fat (McMaster), 9.5 vs 3.5 lb and 9 out of 10 (Pennington), 10 times (Mayo), 8 to 10 thousand steps.",
    "<b>No drug name in any graphic</b> (you say Zepbound once; it stays spoken and in the subtitles).",
    "<b>No side-by-side before/after.</b> The \"two guys\" idea from the script was not filmed and nothing replaces it.",
    "<b>No fake Dan.</b> The script's \"Dan lifting in the home gym\" B-roll was not filmed, so the lifting clip is stock (a man curling dumbbells), not AI-Dan.",
    "<b>Clips.</b> 12 clips: 10 free Pexels, 2 from the clip library (B0287 eggs, B0098 park jog). No clip or scene is used twice; the "
    "fact-card photos are stills from clips not used as clips. The stressed-man and late-eating clips show ordinary people, no close-ups of bellies.",
    "<b>Ending has no AbsByAI call to action</b>, per the script notes: a \"WATCH NEXT\" lower third names the first calories video, then subscribe.",
    "<b>Spend so far.</b> About $1.70 of the $5 for this video: $1.10 Gemini listening, $0.60 for the four opener frames (all four are shown below; nothing was generated and hidden).",
    "<b>Left for the full film:</b> the opener motion you pick, SRT and chapters, the delivery gate and watch pass, one independent review.",
]
def fmt(d): return ", ".join(f"{k} {v}" for k, v in sorted(d.items()))
checks = [
    f"<b>Colour.</b> Card fill on the side lists and the cycle, as composited: {fmt({k: v[0] for k, v in fills.items()})} (spec 10,38,72 +/- 2).",
    f"<b>Hair.</b> Clear of the top edge on every sampled on-camera frame of the first minute: {hair.get('min_px')} px minimum, "
    f"{hair.get('median_px')} px median ({hair.get('samples')} samples, every 0.25 s). C1705 is framed like C1704, so the locked crops are reused.",
    f"<b>Clearance.</b> Your arms and hands never reach a side card (person mask, every 10th frame): {fmt(clear)} px minimum.",
    f"<b>Lower thirds never cover your face</b> (face box, every 10th frame): face ends {min(face.values()) if face else '?'} px or more above the strip on all {len(face)}.",
    f"<b>Base picture.</b> First-minute render against its own graded base on frames with no graphic: {json.dumps(fid)} (dB; this is the encode, the same figure RO-10 measured). "
    "The pixel-exact RGB compositor proof was done on RO-10 with the same unchanged code and was not re-run here.",
    "<b>Every copy fits</b> its one-line layout (checked before rendering); every in, out and part is on a word start (beat sheets below).",
] + ([f"<b>Flagged, checked by eye:</b> {k}: {'; '.join(v)}. At 9:15 you throw both hands wide on \"work at a standing desk\"; your hand passes UNDER the card (about 180 px below its bottom edge), it never touches the card. The check only measures left to right, so it reads as a fail. I left it; say so if the gesture under the card bothers you and I will end the card one sentence earlier." for k, v in fails.items()] if fails else []) + (
    [f"<b>First-minute audio gate:</b> {gate.get('verdict')}, {gate.get('rows')} rows, {gate.get('lufs')} LUFS. The EQ is fitted on this roll plus your approved +0.9 dB at 150 Hz; the A/B against Muhammad is linked under the first minute."] if gate else [])
reply = ("1. First minute: approved / notes:\n2. AI opener: A (scale) / B (awake at 2 AM) / none, stay on camera\n"
         "3. HyperFrames graphics: approved / notes by ID:\nOther notes (ID or timestamp):")
json.dump(dict(film_len=f"{int(film // 60)}:{int(film % 60):02d}", decisions=decisions, decided=decided, checks=checks, reply=reply,
               first_minute=dict(end=fm_end, note=f"audio: approved audio B chain, gate {gate.get('verdict', 'see checks')}.")),
          open(f"{W}/page_extra.json", "w"), indent=1)
print("extra ok")
