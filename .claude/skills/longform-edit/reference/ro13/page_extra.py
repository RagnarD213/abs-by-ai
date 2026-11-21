"""Writes round1/page_extra.json (decisions, what I decided, checks) from the measured results."""
import json, os
W = "/Volumes/Extreme/_edit_work/ro13/round1"
def load(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
hair = load(f"{W}/first-minute/hair.json", {}); ck = load(f"{W}/checks/all.json", {}); gate = load(f"{W}/first-minute/gate.json", {})
fid = load(f"{W}/first-minute/fidelity.json", {})
S = json.load(open("/Volumes/Extreme/_edit_work/ro13/shots.json")); film = S[-1]["out_f1"] / (30000 / 1001)
fm_end = load(f"{W}/first-minute/end.json")["end"]
clear = {k: v["items"][0].get("min_clear") for k, v in ck.items() if v["items"] and v["items"][0].get("min_clear") is not None}
face = {k: v["items"][0].get("min_face_gap") for k, v in ck.items() if v["items"] and v["items"][0].get("min_face_gap") is not None}
fills = {k: [tuple(f["rgb"]) for f in v["items"][0].get("fill", [])] for k, v in ck.items() if v["items"] and v["items"][0].get("fill")}
fails = {k: v["failures"] for k, v in ck.items() if v["failures"]}
FLAG_NOTES = load(f"{W}/flag_notes.json", {})      # id -> what I saw by eye
decisions = [
    f"<b>The first minute</b> above (it runs to {int(fm_end // 60)}:{fm_end % 60:04.1f}, the first cut after 60 seconds): approve, or notes by timestamp. "
    "The two AI clips in it are labelled placeholders (their START and END frames); everything else is finished.",
    "<b>AI clips</b> (frames below; I generate motion only for the ones you approve, about $0.60 to $1.20 each). "
    "<b>A, the opener</b>, 3 seconds under \"Can you drink alcohol and still have six pack abs?\": a lean man with abs at a pool cookout raises a beer and takes a sip. "
    "<b>B, the mirror</b>, 7.6 seconds under \"Your training can be perfect... wondering why nothing changed\": a heavier man in gym clothes checks his stomach in the mirror and drops his head, two beer bottles on the counter. "
    "Recommended: <b>both</b>. Other options: only A, only B, or neither (you stay on camera).",
    "<b>\"An entire day's deficit\" or \"an entire week's deficit\"?</b> You said the line twice: first \"That is an entire <i>day's</i> deficit gone in one evening\" (the script), then again with \"<i>week's</i>\". "
    "I used <b>day's</b> (recommended: 1,000 calories is about a day's deficit, and fact card G10 says the same). Say \"week's\" and I swap the take and the card.",
    "<b>\"Take a photo of your drink and you're done.\"</b> Right now this is a stock clip of hands photographing a drink (C08). "
    "Recommended for the full film: <b>a real capture of the AbsByAI macro tracker logging a drink</b>, in the phone beside you (the approved app-demo layout); I record it on the live app next round. Or keep the stock clip.",
    "<b>The 25 HyperFrames graphics</b> (19 lower thirds, 3 fact cards, 3 side lists), all on the templates you approved on RO-10: approve, or notes by ID. Each has a <i>Play it moving</i> button.",
]
decided = [
    "<b>Hook.</b> Take 4 of 4. Takes 1 to 3 each ended with \"roll to the top\"; take 4 is the only one that runs on into \"First, let me explain\", so the first 47 seconds has no join in it. (Take 4 says \"you'll still be standing in the mirror in six months\".)",
    "<b>Takes.</b> The last clean copy of every line. A word-for-word listen (Gemini, about $1.10) found about 30 restarts, all cut: three hooks, two tries at \"almost as calorie dense as\", \"the worst offender in the at-\", "
    "six tries at the falling-asleep line and five at \"Alcohol wrecks your sleep quality\" (one came out \"sweet bleh\"), the first \"Number three\", \"the liquor they're drank\", the first app line, \"And this has an ev-\", "
    "\"no version of you\", the first \"Rule number five\", \"and it is a single\", the doubled \"Not because it cancels anything out\", two tries at the next-morning passage (with the \"roll it back\"), "
    "\"if you're trying to\", two tries at \"Once you are maintaining\", three at \"one or two nights\", \"if I had not have gone on a\", and the first two endings.",
    "<b>Your rewrites stay.</b> You changed several lines on camera and I kept your final wording: \"Falling asleep quickly is not high quality sleep\", \"Take a photo of your drink and you're done\", "
    "\"And drinking bad tasting drinks has a second benefit\", \"Your last drink should be at least three hours before you go to bed\", \"but it's the single highest return rule\", "
    "and the added \"Realistically, I probably would not have had the willpower to cut down on drinking if I had not gone on Zepbound. It helped me tremendously...\"",
    "<b>Ending.</b> The third and last take (\"Fast first, count it, and drink things that taste bad. Low sugar. Cap it at one or two nights per week and stop three hours before bed. Do not let one bad night become a weekend.\"). It is clean in one run.",
    "<b>One slip left in, no clean copy exists:</b> \"far more moderately than I <i>do</i> in the past\" (5:55). Both takes say \"do\". Say so if you want the sentence trimmed to \"I drink myself, but far more moderately.\"",
    f"<b>Length and pace.</b> {int(film // 60)}:{int(film % 60):02d} from a 14:29 roll. Pauses over 0.7 s are tightened; a reframe cut (wide to tight, nothing removed) every 9 to 14 seconds: {len(S)} shots.",
    "<b>Structure on screen.</b> The four things alcohol does are numbered lower thirds (1. LIQUID CALORIES to 4. RECOVERY AND TESTOSTERONE). The six rules each get a full-screen title, \"RULE 1 OF 6\" to \"RULE 6 OF 6\", in RO-10's approved title style: "
    "Eat First, Count The Calories, Kill The Sugary Mixers, Cap Your Nights, Stop 3 Hours Before Bed, Run Your Normal Fast. The recap card at the end lists all six.",
    "<b>Numbers on screen follow what you said:</b> 7 calories per gram, 30 minutes, 1,000+ calories, 1 night a week and 2 at the max, 1,700 calories a week and 7 nights, 3 hours before bed, 5 to 10 drinks a week, 1 or 2 drinks now.",
    "<b>Your real photos.</b> On \"that's how I can maintain my abs\" the film shows the three-photo slate you picked on RO-16 (studio-white-23, studio-blue-173, studio-blue-240), labelled \"Real pictures of me. Not AI-generated.\"",
    "<b>No drug name in any graphic.</b> You say Zepbound three times; it stays spoken and in the subtitles. The lower third there reads \"WHAT HELPED ME: My Desire To Drink DROPPED.\"",
    "<b>No Oura screenshot.</b> You say you can see it on your Oura ring; I have no real screenshot of a night after drinking and did not fake one. A stock clip of a man awake at night covers the line. Send a screenshot and I will put it in.",
    "<b>Clips.</b> 17 stock placements from 21 different free Pexels clips; the clip library has no alcohol footage that is not already in the Zepbound video. No clip or scene is used twice; the three fact-card photos are stills from clips not used as clips. "
    "I rejected one stock clip because it was a close-up of a belly.",
    "<b>The ending has no AbsByAI call to action</b> beyond your own app line in rule 2, as scripted: recap card, then you on camera for the subscribe line.",
    "<b>Spend so far.</b> About $1.70 of the $5 for this video: $1.10 Gemini listening, $0.60 for the four AI frames (all four are shown below; nothing was generated and hidden).",
    "<b>Left for the full film:</b> the AI motion you approve, the app capture if you want it, SRT and chapters, the delivery gate and watch pass, one independent review.",
]
def fmt(d): return ", ".join(f"{k} {v}" for k, v in sorted(d.items()))
checks = [
    f"<b>Colour.</b> Card fill on the side lists, as composited: {fmt({k: v[0] for k, v in fills.items()})} (spec 10,38,72 +/- 2).",
    f"<b>Hair.</b> Clear of the top edge on every sampled on-camera frame of the first minute: {hair.get('min_px')} px minimum, "
    f"{hair.get('median_px')} px median ({hair.get('samples')} samples, every 0.25 s). C1707 is framed like C1704, so the locked crops are reused.",
    f"<b>Clearance.</b> Your arms and hands against each side card (person mask, every 10th frame): {fmt(clear)} px minimum.",
    f"<b>Lower thirds never cover your face</b> (face box, every 10th frame): face ends {min(face.values()) if face else '?'} px or more above the strip on all {len(face)}.",
    f"<b>Base picture.</b> First-minute render against its own graded base on frames with no graphic: {json.dumps(fid)} (dB; this is the encode, the same figure RO-10 measured). "
    "The pixel-exact RGB compositor proof was done on RO-10 with the same unchanged code and was not re-run here.",
    "<b>Every copy fits</b> its one-line layout (checked before rendering); every in, out and part is on a word start (beat sheets below).",
    "<b>Framing.</b> The solver found zero same-size joins: every cut between two on-camera shots changes size.",
] + [f"<b>Flagged by the automatic check:</b> {k}: {'; '.join(v)}. " + FLAG_NOTES.get(k, "Not yet looked at by eye.") for k, v in fails.items()] + (
    [f"<b>First-minute audio gate:</b> {gate.get('verdict')}, {gate.get('rows')} rows, {gate.get('lufs')} LUFS. The EQ is fitted on this roll plus your approved +0.9 dB at 150 Hz; the A/B against Muhammad is linked under the first minute."] if gate else
    ["<b>First-minute audio gate:</b> not run."])
reply = ("1. First minute: approved / notes:\n2. AI clips: both / only A (opener) / only B (mirror) / neither\n"
         "3. Deficit line: day's / week's\n4. Photo-your-drink beat: real app capture / keep the stock clip\n"
         "5. HyperFrames graphics: approved / notes by ID:\nOther notes (ID or timestamp):")
json.dump(dict(film_len=f"{int(film // 60)}:{int(film % 60):02d}", decisions=decisions, decided=decided, checks=checks, reply=reply,
               first_minute=dict(end=fm_end, note=f"audio: approved audio B chain, gate {gate.get('verdict', 'see checks')}.")),
          open(f"{W}/page_extra.json", "w"), indent=1)
print("extra ok")
