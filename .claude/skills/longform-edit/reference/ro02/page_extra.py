"""Writes round2/page_extra.json (decisions, what I decided, checks, reply) from the measured results."""
import json, os
W = "/Volumes/Extreme/_edit_work/ro02"; R2 = f"{W}/round2"; FPS = 30000/1001
def load(p, d=None): return json.load(open(p)) if os.path.exists(p) else d
hair = load(f"{R2}/first-minute/hair.json", {}); gate = load(f"{R2}/first-minute/gate.json", {}); fid = load(f"{R2}/first-minute/fidelity.json", {})
ck = load(f"{R2}/checks/all.json", {}); cc = load(f"{R2}/checks/cardclear.json", {}); notes = load(f"{R2}/flag_notes.json", {})
S = json.load(open(f"{W}/shots.json")); film = S[-1]["out_f1"]/FPS; PR = json.load(open(f"{W}/plan_resolved.json"))
fm_end = load(f"{R2}/first-minute/end.json", {"end": 61.7})["end"]; O = next(r for r in PR if r["id"] == "O01")
mm = lambda t: f"{int(t//60)}:{t%60:04.1f}"
face = {k: v["items"][0].get("min_face_gap") for k, v in ck.items() if v["items"] and v["items"][0].get("min_face_gap") is not None}
clear = {k: v["items"][0].get("min_clear") for k, v in ck.items() if v["items"] and v["items"][0].get("min_clear") is not None}
fails = {k: v["failures"] for k, v in ck.items() if v["failures"]}
n = lambda k: sum(1 for r in PR if r["kind"] == k)
decisions = [
    "<b>The first minute</b> (player at the right): approve, or notes by timestamp. The opener in it is a labelled placeholder (the START and END frames swapping); everything else in it is finished.",
    "<b>Opener clip A, crunches</b> (frames below): a heavyset man in a grey t-shirt on a mat in a living room, side-on. <i>Approve the frames (recommended), or tell me what to change.</i>",
    "<b>Opener clip B, sit-ups</b> (frames below): a different heavyset man, bald with a beard, navy t-shirt, on a gym floor, side-on. <i>Approve the frames (recommended), or tell me what to change.</i>",
    f"<b>The opener graphic</b> (three stills below): your title top left, the two clips side by side, a red X drawn across each one on your words (\"Stop doing crunches\" at {mm(O['x']['A'])}, \"stop doing sit ups\" at {mm(O['x']['B'])}). "
    f"It ends at {mm(O['t1'])} with a hard cut to you on \"stop doing all those ab exercises\". <i>Approve (recommended); or hold the graphic until {mm(8.3)}, after \"all those ab exercises\"; or notes.</i>",
    "<b>The anatomy card</b> (AN1, a new kind of graphic): a drawn torso in the left card beside you. The six pack lights up on \"rectus abdominis\", the deep belt around the waist on \"transverse abdominis\". <i>Approve (recommended), or notes on the drawing or the wording.</i>",
    "<b>Sound</b> (carried from round 1, not answered): your lav through the shared voice chain, no room removal, no music. Play the A/B link under the first minute. <i>Sound OK (recommended), or tell me what you hear.</i>",
    "<b>Length</b> (carried from round 1, not answered): the cut keeps everything. (a) keep all of it; (b) remove only the aside at 0:49 to 0:56, \"you can skip ahead about 30 seconds\" (recommended, 7 seconds: it invites viewers to skip and the timing no longer matches); "
    "(c) also end the three types section at 4:42, after \"the only one I do myself and recommend to clients is the standing vacuum\" (the next 42 seconds repeat the mirror and psychology points). The first minute here still contains the aside.",
]
ai = dict(
    A="<b>Action:</b> one crunch. Shoulders flat on the mat, then curled up a few inches, hands behind his head. Only his upper body moves; same room, same camera. In the film he does a rep or two, up and back down, for the 6.6 seconds the graphic is up. Estimated $0.60 to $1.20 for the motion.",
    B="<b>Action:</b> one sit-up. Flat on his back with his arms crossed, then sitting fully upright. Only his torso moves; hips and feet stay put. A rep or two in the film. Same cost. One thing I saw: the START frame has a small N on his shoe; I remove it before generating motion.",
    graphic="The panels hold the START frames here. Each clip carries the AI-GENERATED chip for its whole time, in its top left corner, clear of the title, the man and the X. The crossed-out clip dims and its label turns red. The whole 16:9 clip is shown in each panel, nothing cropped.")
decided = [
    f"<b>Framing.</b> Your note is applied: the space above your head is halved on both sizes (25 and 20 source pixels above the highest your hair gets in each shot, was 50 and 40) and the bottom edge of each frame is unchanged. FAR is now about x1.50, NEAR about x1.86. Hair measured every quarter second in the first minute: {hair.get('hair_min_px', '?')} px minimum, {hair.get('hair_median_px', '?')} px median (round 1: 70 and 106).",
    f"<b>Where the opener ends.</b> At {mm(O['t1'])}, on the cut to you saying \"stop doing all those ab exercises\". You are on camera inside the first seven seconds and the cut lands on the start of a phrase. The second X has just over a second on screen. The alternative is in decision 4.",
    "<b>Two different men, different rooms</b> (a living room and a gym) so the two panels never read as the same clip twice. Both are clothed and shown whole, with no hands on the stomach and no close-up of it.",
    "<b>Your real footage, no stock.</b> Four seconds of this film's own live set play under \"the vacuum, the only ab exercise that can actually shrink your waist\" (0:26). I tried the clip library's vacuum clip first (B0428, the 8/28 shoot): it is in shade and read dark and small beside this film, so I did not use it. "
    "Your own toe-touch crunches from the finished 1 Minute Ab Workout video play under \"an ab workout where they do a thousand crunches\" (1:04). This replaces the round 1 idea of your crunches at 0:03, which your opener now covers.",
    "<b>Six section titles</b>, full screen for about 2.4 seconds each, in the approved title style, reading PART 1 OF 6 to PART 6 OF 6: Why Ab Exercises Do Not Burn Belly Fat; The Muscle That Shrinks Your Waist; Why The Standing Vacuum; How To Do It; A Live Set; Your Routine.",
    "<b>Fact card</b> (1:10): YOU BURN FAT / EVENLY, ALL OVER / Spot reduction is a myth. Each line lands on the words that say it. The photo is a frame of you from the ab workout video, labelled as a real picture.",
    f"<b>Key point lower thirds:</b> Ab Exercises Build Muscle UNDER The Fat; Bodybuilders Have Used It Since THE 1960s; The Mirror Is HALF The Exercise; Do It On An EMPTY STOMACH; Take SHORT BREATHS Through Your Nose (shortened from \"Keep Breathing: SHORT BREATHS Through Your Nose\" so it fits one line).",
    f"<b>Four side lists</b>, each item landing on the word that names it: 3 Types Of Vacuums; Why Standing; Before You Start; The Routine. The camera is a 1080p frame with no wall to stretch, so for each list your framing window slides left inside the frame and you sit to the right of the card, same size, same colour. "
    "Every list was checked against every piece it spans (numbers under Checks).",
    "<b>The steps are lower thirds, not a list.</b> While you demonstrate the slump and the suck-in, your elbows cross 144 px into where a side card would sit, so each step gets its own lower third as you say it: STEP 1 Slump. Let Your Stomach OUT. / STEP 2 Suck It In As HARD As You Can. / STEP 3 Use A Timer. Hold 20 SECONDS. "
    "The Routine list ends at the cut before your deep-breath explanation for the same reason.",
    "<b>\"Supine\" stays in your speech;</b> the list says Hands And Knees. No drug name in any graphic.",
    "<b>The demo of you generating your goal picture</b> (the exact approved sequence with its AI-GENERATED label) plays at \"a real life AI transformation picture\" (5:50) and again in the ending as you describe generating the picture (11:07). It is the approved file, so it keeps its original olive card; say so if you want it rebuilt on the blue field.",
    "<b>A 20-second countdown</b> (a new small chip, top left) runs through the live set and reaches zero on your phone timer's beep. It is listed here rather than asked; it has a play button below.",
    "<b>Recap card</b> in the takeaway (10:24 to 10:52): If You Have Belly Fat / Stop the ab exercises for now / Fat burns evenly, all over / Total body workouts + nutrition / Vacuums every morning. <b>AbsByAI.com chip</b>, top left, when you say the address in the ending. No end mark.",
    "<b>Arnold and Frank Zane:</b> no photos of them (we own none); that beat has the 1960s lower third.",
    "<b>Spend.</b> $0 of the $5 for this video. The four AI frames were made on the Codex subscription (four images, no spares); the transcript was local.",
    "<b>Left for the next rounds:</b> the two AI clips' motion (after you approve the frames), the full film, SRT and chapters, the delivery gate, the watch pass, one independent review.",
]
checks = [
    "<b>Every cut changes size.</b> The framing was solved for the whole film with the side lists in place: zero same-size joins.",
    "<b>Side lists and the anatomy card against your body</b> (person mask on every 10th frame of each moving clip; pixels between the card's edge and the nearest part of you): " + ", ".join(f"{k} {v} px" for k, v in sorted(clear.items())) + f"; the anatomy card {cc['AN1']['clear_px']} px (every half second).",
    f"<b>Hair</b> under the side cards: {min((v['hair_min_px'] for k, v in cc.items() if k != 'L4'), default='?')} px minimum from the top edge. First minute: {hair.get('hair_min_px')} px minimum. No shot needed extra headroom.",
    "<b>The first minute's eight picture changes</b> were looked at frame by frame (two frames either side of each): every one is a clean change of size or a hard cut to a graphic or clip.",
    (f"<b>Lower thirds never cover your face</b> (face box, every 10th frame of each context clip): your face ends {min(face.values())} px or more above the strip on all {len(face)}." if face else "<b>Lower third face check:</b> not run."),
    f"<b>Base picture.</b> The first minute against its own graded base on frames with no graphic: {json.dumps(fid) if fid else 'not measured'} (dB; this is the encode).",
    "<b>Every copy fits</b> its one-line layout (checked before rendering); every in, out and part is on a word start (beat sheets on each card).",
] + [f"<b>Flagged by the automatic check:</b> {k}: {'; '.join(v)}. " + notes.get(k, "Not yet looked at by eye.") for k, v in fails.items()] + [
    (f"<b>First-minute audio gate:</b> {gate.get('verdict')}, {gate.get('rows')} rows, {gate.get('lufs')} LUFS." if gate else "<b>First-minute audio gate:</b> not run."),
    "<b>Not done yet (not claimed):</b> no full film, no AI motion, no SRT or chapters, no delivery gate, no watch pass, no independent review. Joins outside the first minute have not been looked at frame by frame.",
]
reply = ("RO-02 round 2\n1. First minute: approved / notes:\n2. Opener clip A (crunches) frames: approved / change:\n3. Opener clip B (sit-ups) frames: approved / change:\n"
         "4. Opener graphic: approved, ends at 0:06.6 / hold to 0:08.3 / notes:\n5. Anatomy card: approved / notes:\n6. Sound: OK / notes:\n7. Length: (a) keep all / (b) remove the skip-ahead aside / (c) also trim the three types section\n"
         "Anything in 'What I decided' to overrule:\nOther notes (ID or timestamp):\n")
json.dump(dict(film_len=f"{int(film//60)}:{int(film%60):02d}", decisions=decisions, decided=decided, checks=checks, reply=reply, ai=ai, item_notes=notes,
               first_minute=dict(end=fm_end, note=f"Colour A, the new headroom. Audio gate {gate.get('verdict', 'see Checks')}" + (f", {gate.get('lufs')} LUFS." if gate else "."))),
          open(f"{R2}/page_extra.json", "w"), indent=1)
print("extra ok")
