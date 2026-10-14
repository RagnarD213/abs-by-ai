# RA-07 "Fire Your Trainer!": round 2 (new AI frames, three clips moving, the RA-14 look, the first 30 seconds)

**AD (short-form, filmed).** Sidebar name for the next task: `Fire Your Trainer AD R2`.
Rewritten 2026-10-14 after Dan answered the round 1 page (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-07-fire-your-trainer.md`.
Read first: `.claude/skills/_shared/VIDEO-RULES.md` (first sections: AI clip sense check, the bass lift, outdoor look options,
whole short in one round), the `/ad-edit` skill ("RA-07 lessons, round 1", "RA-14 round 3 lessons" if present),
`_shared/PRE-RENDER-APPROVAL.md`, `_shared/IMAGE-GENERATION.md`, `_shared/CUT-CONTINUITY-QC.md`.
Dan's words, verbatim, per item with hashes: `/Volumes/Extreme/_edit_work/ra07/round2-plan/decisions.json` (sha 36041c71dc38958c).

## What Dan said (2026-10-14, about the page http://127.0.0.1:8807/)

| item | his words | what it means |
|---|---|---|
| Opening | "I want the AI-generated clip of the trainer getting fired and the robot spotting right in the first few seconds: 'Fire your trainer now and replace them with AI.' Then cut to the camera scene after that." | Option A. H1 (library A0147) from 0.00 under the whole hook line, hard cut to Dan on "Why are thousands". |
| Framing, colour, voice | "Yes, I want the wider framing like in the cheat code, the color in the cheat code. Basically, all the cheat code settings are good." | RA-14's picks: framing F2, grade C2 brighter golden skin, voice with the bass lift. Details below. |
| Claim lines | "All the claim lines are fine." | Run as spoken. Closed. |
| I1 The sad paper | "skip I1" | Not made. Dan on camera for the paper line. |
| I2 Same sheet for everyone | "generate I2" | Motion authorized from the round 1 frames. |
| I3 Tweaked shoulder | "He injures his shoulder, then he looks at his phone, and then he gets an alternate exercise. Let's say he can't do the press, and instead he goes to the side lateral machine" | I3a (press, wince) motion authorized from the round 1 frames. NEW I3b frames: the fix. |
| I4 Out of order | "Let's say the leg squat machine is broken. He goes to the hack squat machine instead." | The round 1 frames show a cable machine, so I4a needs NEW frames (same gag, leg squat machine). NEW I4b frames: the hack squat. No motion on the old cable-machine frames. |
| I5 Back next week | "'Back next week' is actually good as is" | Motion authorized from the round 1 frames. No follow-on clip. |

He said "additional frames for I3, I4, and I5" and then that I5 is good as is: read as no I5 follow-on. Say so in "What I decided".
Everything else on the round 1 page drew no objection (cut, takes, signposts L1 to L3, P1, K1, W1, T1, M1, C1, the 0.80 s end
hold, no analysis card). It is carried as shown, not approved in words.

## The RA-14 settings, converted to this roll

- **Framing.** RA-14's pick on C1667 is close 576x1024, wide 720x1280 (`/Volumes/Extreme/_edit_work/ra14/framing_choice.json`).
  Dan is bigger on C1664 (head 370 px, face 228 px) than on C1667 (head 290, face 178), x1.276, so the same look here is
  **close 738x1312 (m=41), wide 918x1632 (m=51)** on the exact 9:16 lattice (w = 18m, h = 32m), y0 = the hold's minimum hair top
  minus 4 % of the crop height. Put the numbers in `ra01lib.py` `Aspect.levels`, re-run `s60_plan.py`, then check two stills
  (one close, one wide) beside RA-14's round 3 frames: he should fill the frame the same way. Adjust by one lattice step only if
  he clearly does not, and say so.
- **Colour.** RA-14 `grade.json`: one baked LUT, `/Volumes/Extreme/_edit_work/ra14/round2/colour/luts/ra14_C2_brighter_gold.cube`
  (params expo 2.4, knee 0.45, sat 0.85, vib 0.5, contrast 0.2, pivot 0.46, skin_rot 8, skin_sat 0.96). Copy it into this job's
  `grade.json`. C1664 was shot earlier the same day: measure face luma and saturation against RA-14's approved frames and look
  at them side by side. If it misses, rebuild the LUT from those params with exposure only, and say so on the page.
- **Voice.** RA-14's `mix_bass.wav` is the fitted tone plus `equalizer=f=120:t=q:w=0.8:g=+3.0`
  (`/Volumes/Extreme/_edit_work/ra14/mix_bass.wav.voice_chain.json`). Re-make this job's mix the same way from `cut_audio.wav`
  (Realizer bed at -32), then frame-lock it to the picture with `LOCK=` once the length is final. Audio gate on it.
- **The BT.601 fix.** RA-14's `ra01lib.py` `encode_h264` now converts RGB to YUV with the BT.709 matrix
  (`-vf scale=in_range=pc:out_color_matrix=bt709:out_range=tv`). This job's copy was taken before that fix: port it before
  any card is rendered.

## Round 2 deliverable: one review page, then stop

Build in `/Volumes/Extreme/_edit_work/ra07/round2/`; serve with `review_server.py` on a free port (keep 8807 for round 1).
Wait for a build slot through `_shared/buildcap.py` (the Mac runs other sessions' renders).

1. **Re-hash** the round 1 files (table below) into `round2/HASHES.json`.
2. **Re-plan** (`s60_plan.py`): H1 at 0.00; I1 removed (Dan's hold on the paper line); the new framing; the clips laid out as below.
   Every cut a size change or an insert; the three pause splices inside holds (13.01, 23.42, 35.07 s on the round 1 timeline)
   get covered; the holds that wander get the land-then-hold track (`_shared/cut/landing.py`).
3. **Lay out the problem-then-fix run.** The words (round 1 timeline): "And three, AI can adjust your plan" 34.30 / "when life
   gets in the way. When you get injured" 36.47 / "or you can't make it to the gym one day," 38.54 / "or when the equipment you
   need is broken." 40.44 / "AI adjusts your plan in seconds," 42.11 / "while human trainers" 43.94 / "leave you confused until
   next week." 44.98 to 47.01. Recommended, and shown on the page so he can overrule: I3a on "when life gets in the way. When
   you get injured" (wince lands on "injured"), M1 on "or you can't make it to the gym one day", I4a on "or when the equipment
   you need is broken", then the two fixes on "AI adjusts your plan in seconds, while human trainers" (I3b then I4b, about 1.4 s
   each, the moment the AI solves it), and I5 on "leave you confused until next week" (about 2 s, so I5's motion must read in
   that length). T1, the app's Swap screen, comes out: the phone in I3b carries "AI adjusts your plan". If a fix reads better
   straight after its own problem, show that as option B. No clip under 1.2 s.
4. **New START and END frames** (Codex subscription, `codex-image.sh`, 9:16, the same man as I2 to I5: pass `round1/frames/I3-end.png`
   as the reference image): **I3b** START he sits on the bench holding his shoulder and looks at his phone; END he is on the side
   lateral raise machine doing a light rep, no wince. **I4a** START he walks toward a leg squat machine with the yellow OUT OF ORDER
   sign hanging on it (round 1's I4 sign, same lettering); END he stops and turns to the camera, palms up. **I4b** START he walks
   up to the hack squat machine; END he is in it, mid-rep. Step 4.5 prompt rules (no cinema words, ordinary face, no logos), no
   belly framing, subject in the centre third. Each pair on the page under its idea name with: when it appears, what he says
   before, the line it plays under (bold, word for word), what comes right after, what you see, length, cost, and what plays if
   he says no. **No motion for these until Dan approves the frames.**
5. **Motion for I2, I3a, I5 only** (frames approved, unchanged), image to video from START and END, about $1 a take, inside the
   $10 ad cap (spent so far $0; keep the ledger, failed takes included). Check each take at playback speed with the three sense
   questions (cause and effect, readable with the sound off, shows the line). I3a: the dumbbell is lowered into his lap, never
   vanishes. I5: the BACK NEXT WEEK sheet stays readable and unchanged. Trim to the part that works; never slow or hold a clip.
   AI-GENERATED chip on each, placed by looking at the people in that clip (on A0147 it sits on the floor above the captions).
   Register every keeper in the clip library at the end of the job.
6. **Sharpen the two small library clips** for full screen (A0147 720x1280, A0039 848x480): Real-ESRGAN locally, or A0147's
   upscaled copy from the Ad 13 vertical build. Look at them at 1080x1920.
7. **Cut QC** that round 1 had no slot for: `_shared/cut/junk.py` on C1664 with `cut.json` (stretched: "firing" 0.72 s, "now."
   0.72 s), `s25_hard.py`, `_shared/cut/piccuts.py`, CUT-CONTINUITY-QC section 5 on the new opening.
8. **The page:** the new frames (I3b, I4a, I4b) on top; then I2, I3a and I5 moving in context; every graphic and clip moving in
   context ("Play it moving, in context") with the new framing and colour; then **the finished first 30 seconds** (H1, the hook,
   L1, P1, K1, the paper line, L2, W1: nothing in it is pending). The full film waits for round 3 because three clips are still
   frames (VIDEO-RULES "whole short in one round" keeps the 30 s step when AI motion is unseen). Listen to and watch the 30 s
   before sending. Copy it to `Videos to Review/` only if it is 45 s or longer.
9. Record nothing as approved that he has not said. Write the round 3 handoff (motion for the approved new frames, then the
   whole 9:16, both gates, edit sheet, watch pass, independent `ra-reviewer`, delivery to `Claude Ad Videos/fire your trainer - RA-07/`,
   then the 16:9) and stop.

## Round 1 files (work dir `/Volumes/Extreme/_edit_work/ra07/`, sha256 first 16)

| file | what | hash |
|---|---|---|
| `edl_spec.json` | take map by phrase, with the reasons | 0b411437c8335156 |
| `tx/c1664.whisper.json` | word list 372 to 460 s (two Replicate passes joined, three times corrected from the envelope) | ae704fdd66930086 |
| `cut.json` | 51.89 s of talk, 16 pause cuts, take seam at 47.01 s | d548aa837fe38410 |
| `mix.wav` | RA-01 chain, no bass lift (to be re-made) | a0c8e558e1e523ef |
| `words_aligned.json` | 183 words, CTC aligned | 0f3b808eed7bbedb |
| `framing.json` | head and hair track, 257 samples | ebe37beb873262e3 |
| `beats.json` | round 1 plan (changes now) | 1727ccf8492ee000 |
| `round1/frames/I2,I3,I5-start/end.png` | approved frames | in `decisions.json` |

Scripts: `recipe/` in the work dir, plus the live copies (`s03_edl.py`, `s60_plan.py`, `s62_sample.py` with `SKIP1=1`,
`s63_stills.py`, `s63_cards07.py`, `s64_page.py`, `tx/replicate_words.js`). RA-14's round 3 scripts (s81 opener, s82 holds,
s83 phone cards, s85 captions, s86 assemble, s88 checks) in `.claude/skills/ad-edit/reference/ra14/round3/` are the newest
version of the same pipeline: start from them where they cover a step.

Carried from round 1 and unchanged: hook second read (head edge 389.95 s), body one take to "until next week", CTA the last
take ("to take the first step"), end hold 0.80 s, captions punctuated from the script, no analysis card, no URL on the button.

## Cost ledger

AI generation $0 (frames on the Codex subscription). Replicate transcripts under 2 cents. Cap for the ad $10, all rounds.

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `Fire Your Trainer AD R2`. Read `Handoffs/handoff-20261013-ra07-fire-your-trainer-round2-after-dan-review.md` and run round 2 of RA-07 "Fire Your Trainer!" with /ad-edit. My round 1 answers are recorded in `round2-plan/decisions.json`. Apply the Cheat Code (RA-14) framing, colour and bass-lift voice, put the fired-trainer clip at the very start, make the new frames for the shoulder fix, the leg squat machine and the hack squat, make the motion for I2, I3a and I5, then send me the review page with everything moving in context and the finished first 30 seconds. Write the round 3 handoff and stop. Use the Codex subscription to generate the images.
