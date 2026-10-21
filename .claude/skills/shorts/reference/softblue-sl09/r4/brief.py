#!/usr/bin/env python3
"""R4: print the independent reviewer brief for one short: brief.py S"""
import sys, hashlib
sys.path.insert(0, "/Volumes/Extreme/_edit_work/sl09/round2")
import plans as P
S = sys.argv[1]
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
V = f"{ROOT}/Short-form video content/{P.NAME[S]}.mp4"
sha = hashlib.sha256(open(V, "rb").read()).hexdigest()
TITLES = {"A": "Train Harder After A Bad Night's Sleep", "I": "Your Sleep Score Shows Who's Toxic In Your Life", "H": "Cut The Adrenaline Before Bed",
          "K": "You're Not Sleeping As Well As You Think", "J": "Oura Ring Or WHOOP? Which One To Buy"}
CHANGED = {
 "K": ["since the latest review (round 3, which shipped this short): ONLY the opener changed. 0:00-0:04.30 (\"You watching this video right now are probably where I was at a few years ago,\") now plays a new AI-generated clip (Veo, from start/end frames Dan approved): a tired man at a kitchen table gives a confident thumbs-up, then dozes off toward his coffee mug (the \"you are in denial\" gag). It replaces the stock yawning man. It carries the AI-GENERATED chip, which must sit off his face. Ask the three sense questions of it and check it frame by frame for AI faults (hands, fingers, the mug, the coffee, the kitchen).",
       "everything after 0:04.30 is meant to be unchanged from the reviewed round-3 file (verify the joins at 0:04.30 and that captions, key point, phones and crops still hold): the round-3 file is at /Volumes/Extreme/_edit_work/sl09/round2/r3_delivered/oura-short4_youre-not-sleeping-as-well-as-you-think.mp4 for comparison"],
 "J": ["since the latest review (round 3, which shipped this short): two AI-generated clips (Veo, from start frames Dan approved) replace two pictures. (1) 0:00-0:03.70 (\"Should you buy the Oura Ring? In my opinion, yes for most people.\"): a close-up of a man's hand on white bed sheets that lifts slightly with its fingers open so a matte black smart ring on the index finger catches the light, then settles; it replaces Dan's real Oura app recording in the phone frame (two earlier takes of this clip were rejected because the fingers clenched into a fist; check the fingers). (2) 0:16.30-0:20.60 (\"Just more depends whether you prefer a wrist-based or a finger-based sleep tracker.\"): a close-up from above of one hand on a light desk wearing the smart ring on the index finger and a WHOOP-style strap (knit band, small rectangular screenless sensor pod on top of the wrist); the open hand lifts and tilts so ring and pod catch the light, then settles. It replaces Dan on camera there. Dan's round-3 note on this clip: the band must read as a WHOOP, not a plain bracelet. Each clip carries the AI-GENERATED chip off the hand (J2's sits on the empty desk at lower left). Ask the three sense questions of each and check frame by frame for AI faults (fingers, the ring staying on the same finger, the pod staying on the strap, the sheets and desk staying still).",
       "Dan stays on camera from 0:03.70 to 0:11.14 and from 0:13.81 to 0:16.30 (\"Oura Ring and WHOOP are my top two options.\"); verify the joins at 0:03.70, 0:13.81, 0:16.30 and 0:20.60, captions, the comparison scene and crops. Everything else is meant to be unchanged from the reviewed round-3 file at /Volumes/Extreme/_edit_work/sl09/round2/r3_delivered/oura-short5_oura-ring-or-whoop-which-one-to-buy.mp4"],
}
SEC = {"J": "J.", "K": "K."}[S]
chg = "\n".join(f"- {c}" for c in CHANGED[S]) or "- (first review of this file)"
print(f"""You are the independent reviewer of one delivered YouTube Short. Expect it NOT to ship; the builder believes it is fine.

FILE: `{V}` (short {P.ORDER[S]} of 5, "{TITLES[S]}"). sha256 should be {sha}.
CATEGORY: CONTENT, a Short extracted from Zeeshan's finished long-form "My Honest Oura Ring Review After 1.5 Years" (his finished master: `{P.MASTER}`, 1920x1080 29.97 fps, decode BT.709).
SOURCE PIECES (master seconds, played in this order): {P.SEG[S]}.

READ FIRST (and nothing the builder wrote about how it built this short: no editor notes, no build scripts, no shots.json):
- `{ROOT}/AGENTS.md`
- `{ROOT}/Handoffs/video-editing/00-RULES.md`
- `{ROOT}/.claude/skills/_shared/VIDEO-RULES.md`
- `{ROOT}/.claude/skills/_shared/GRAPHICS-STANDARDS.md` (the "Soft Blue shorts standard": title band y 0-310 whole short, picture 1080x1610 below it, key-point bars at 68,1130-1012,1378, captions from y 1412)
- The plan: `/Volumes/Extreme/_edit_work/sl09/round2/_r4/handoff-r2-plan.md`, the general sections plus section "{SEC}"; and this round's brief: `/Volumes/Extreme/_edit_work/sl09/round2/_r4/handoff-r4.md` (Dan's words and what this round changes)
- The previous review of the earlier render, for what it found (verify each item yourself on THIS file, which is a new render): `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/ROUND-2-REVIEW.md` (the round-3 review; a copy is kept in r3_delivered).

WHAT THE BUILDER CHANGED SINCE THAT REVIEW (verify each on the delivered file; do not take it on trust):
{chg}

Standing rules to check in particular: Zeeshan's picture and mix carried untouched (audio cut only at seams, --verbatim); his burned graphics whole or absent, never sliced; hair never leaves the top of the frame and Dan's head never cut at the sides; land-then-hold framing (no busy pans, no window change on continuous footage, no jump cuts: a same-framing join must have a real size change or a clip over it); every clip shows what the words say (with sound off, would a stranger see it?); no stock actor who reads as Dan; no repeated stock; no identifiable other car or plate on driving clips; B-roll colour matched to the presenter and never a flat grey or near-black screen; captions print exactly what he says (swearing stays) and never sit on a card or vanish before the word is finished; title capitalization on graphics; every graphic keeps moving for its whole screen time; key points distill, never echo, and never cover a face; the first 5 seconds are attention-getting; length under 0:59; clean start and end (no clipped word, no editor transition leaking in at the end). If the short contains an AI-generated clip, ask the three sense questions of each (cause and effect; would a stranger say what it shows with the sound off; does it show the line) and check its AI-GENERATED chip sits off faces and abs. A stock-only short needs no chip.

JOB 1 (watch pass): follow `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/gate/watch/JUDGE_PROMPT.md` exactly (read CHECKLIST.md, open EVERY sheet, strip and pair image listed in `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/gate/logs/watch_pass.json`, one verdict per image) and write `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/gate/logs/findings.json` in the format it gives. Only judge images that watch_pass.json lists, and check its sha256 matches the file.

JOB 2 (full-resolution audit): decode the delivered file yourself (project ffmpeg `{ROOT}/Media/video_edit/bin/ffmpeg`, BT.709 decode `scale=in_color_matrix=bt709:in_range=tv`, frame-exact `select=eq(n\\,N)` or seek at least 2 s before a target), transcribe its audio with Whisper yourself, compare against the master at the source pieces, and audit every area above. Work in scratch folder `/Volumes/Extreme/_edit_work/sl09/round2/review_{S}R4_scratch/` (create it; never write anywhere else except the two output files). Heavy decodes and Whisper wait their turn in the shared render queue automatically (`python3 "{ROOT}/.claude/skills/_shared/renderq/renderq.py" status` shows the line); run long steps in the background, keep your own work light (short ranges, small scales), and never set GATE_OFF. Do not render, do not run gates, do not edit any build file.

Write `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/ROUND-4-REVIEW.md` with: file facts (measured), watch pass result, audit by area, the previous review's items one by one (fixed or not), defects that block shipping (output timestamps, what is wrong, what to change), advisories, what you could not verify, and a last line exactly `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`. No em dashes anywhere in what you write. Report back the verdict, each defect with its time, and the findings counts.""")
