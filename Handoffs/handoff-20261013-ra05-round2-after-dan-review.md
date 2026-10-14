AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `How AI Real Abs AD R2`.

# RA-05 "How AI Can Get You REAL Six Pack Abs": round 1 record (SUPERSEDED for the next action)

**Dan answered round 1 on 2026-10-14. Fire `handoff-20261014-ra05-round2-after-dan-answers.md` instead.** This file stays as
the round 1 record: take map, traps, file hashes.

**Written 2026-10-13 by the round 1 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-05-how-ai-can-get-you-real-six-pack-abs.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe: `.claude/skills/ad-edit/reference/ra05/` (README has the stage order and what this ad taught).

**Do not fire this until Dan has replied to the round 1 page.** His reply goes, word for word, into
`/Volumes/Extreme/_edit_work/ra05/round2-plan/decisions.json` before anything is built.

## Where it stands

Round 1 is with Dan: **http://127.0.0.1:8805/** (managed review service, folder `/Volumes/Extreme/_edit_work/ra05/round1/`).
The page shows the finished first 30 seconds (31.7 s, it ends as the curls clip ends), every graphic and clip as a still
with a play-in-context button, the four colour versions on this roll, a "What I decided" list and four decisions.
No full film has been shown to him (the round method). A full 9:16 draft exists in the work folder for internal checks only.

Nothing is gated, stamped, audited, delivered or uploaded. Queue state: `in_progress`. Spend: $0 of the $10 ad cap.

## The four decisions waiting for Dan

1. **Length.** Every line in is 62.1 s; the limit is 59. A (in the cut): "AI is a transformative technology that's rapidly
   changing the world. And now you can change your body with AI too." is out, 55.0 s. B: keep it, cut "It's free, it only
   takes a few seconds, and it could change your life." (about 58 s). C: cut both (about 51 s).
2. **Opening.** A (in the cut): Dan on camera for 1.4 s, then the app's result screen, then Dan. B: the app from frame 0
   (the Generating screen with the man's starting photo, then his result).
3. **Claim lines as spoken** (captions only, no graphic): "But now guys are using AI to get them six pack abs in real
   life." and "It's free, it only takes a few seconds, and it could change your life." A keep, B he names the cut.
4. **Two AI clip ideas, yes or no each** (frames next round, no motion before he approves frames):
   *Steps out of the phone* (0:03.7 to 0:08.4, under "but now guys are using AI to get them six pack abs in real life")
   and *Robot tailor* (0:27.6 to 0:31.7, under "where you need to gain muscle and tailor your workout program").

## Three answers that come from OTHER pages (do not ask again here)

The round 1 page tells Dan these are applied from his answers elsewhere:

- **Colour and the two shot sizes: his picks on RA-14** (`Handoffs/handoff-20261013-ra14-cheat-code-round2-after-dan-review.md`,
  `/Volumes/Extreme/_edit_work/ra14/round3-plan/decisions.json` once it exists). Round 1 here uses RA-14's RECOMMENDED look
  (C2 brighter gold) and pair (F2), neither of which is his pick yet.
  - ⚠ **RA-14's LUT files do not transfer to this roll.** C1664 is about half a stop brighter in the source than C1667:
    RA-14's C2 LUT puts the face at 122 here against 96 there. `s31_bake.py E1 E2` re-bakes the same three looks at this
    roll's exposure (C1 expo 1.20, C2 and C3 expo 1.60; RA-14 used 1.8 and 2.4). Face brightness measured here (close /
    wide): RA-01 grade 79 / 87, C1 77 / 86, C2 91 / 101, C3 90 / 98. Write his pick into `grade.json` (`filter`).
  - **Shot sizes are converted by body landmark, not by pixels.** `framing_choice.json`: close 648x1152 (ends about 70 px
    under the waistband), wide 810x1440 (about 320 px under it); hair top about 1120, waistband about 2170 on this roll.
    If he picks RA-14's pair 1 or 3, convert the same way (RA-14 pair 1 ends about 10 px and 220 px under the waistband,
    pair 3 about 130 px and 380 px).
- **Voice (extra bass or not): his answer on RA-04 or RA-14.** `mix.wav` is the RA-01 chain, no bass lift (audio gate PASS on the unlocked mix, stamp beside it).
- **Analysis card colours (Soft Blue or RA-01 olive): his answer on RA-04.** Soft Blue is in the cut.

If any of these is still unanswered when this fires, keep what round 1 used and say so on the round 2 page.

## The cut, for the record

- Roll `C1664.MP4` (8/28 portrait pool roll, dual-mono lav; `pick_lav.py` JSON beside the roll). This ad is 205 to 300 s.
- Takes (`edl_spec.json`, by phrase): R1 208.24 to 219.15 (hook, second read, with the first "Seriously, I'll show you
  how"); R2 227.65 to 243.45 ("The first step is generating yourself..." to "based on your goal"); R3 246.68 to 257.47
  ("It'll determine..." second read, to "the picture you generated"); R3B 264.60 to 273.30 ("The first step is generating
  an image..." to "change your life"); R4 276.52 to 284.65 ("And once you have your goal picture..." second read, to "So
  take the first step"); R5 292.62 to 299.52 (call to action, last read).
- `edl_spec_full.json` keeps the cut sentence (decision 1 option B or a no-cut answer needs it).
- 15 pause cuts are already applied in `cut.json`: do not apply them again. Five take seams: 9.98, 24.09, 33.60 (the line
  cut), 41.34, 47.68 s.
- Four Whisper word times were corrected from the envelope and two caption words fixed (`s02b_patch.py`): "Seriously,",
  the second "It'll", "So", "Tap"; "Addis" to "Abs".
- Head edge pinned at 208.24 s (`HEAD_SRC=208.24 python3 s03_edl.py`): the automatic onset found the tail of the false
  start one second earlier.
- End hold 0.85 s. He holds his smile to about 300.6 s, then drops his hands (301.2 s); "All right" starts 301.5 s.

## Graphics and clips in round 1

| id | what | where (film time) | source |
|---|---|---|---|
| P1 | app result screen, AI-GENERATED | 1.37 to 3.67 | B0049 from 28.0 s (after the banned before/after screen) |
| L1 | STEP 1 / Generate Your Goal Body | 9.98 to 12.85 | HyperFrames lower third |
| K1 | goal picture on a lock screen, AI-GENERATED | 12.85 to 14.91 | A0074 |
| A1 | analysis card (Soft Blue) | 14.91 to 19.62 | adkit analysis card, the app man's result picture |
| T1 | app tour: AI Trainer sheet, then meal analysis | 19.62 to 24.09 | B0544 |
| L2 | STEP 2 / Get A Plan Built For Your Goal | 24.09 to 27.56 | HyperFrames lower third |
| B1 | Dan's dumbbell curls | 27.56 to 31.70 | B0458, colour brought toward the presenter look |
| B2 | Dan's physique poses | 42.84 to 46.71 | B0435 from 4.3 s (same pool shoot; he faces the camera from there), colour matched to the presenter's wide shot |
| C1 | button: Tap The Button Below To / See Yourself With Abs | 47.68 to end | HyperFrames glass button |

Insert coverage 39.2 % (the gate wants 38 %). If an AI idea replaces B1, coverage is unchanged.

## Next action (round 2)

1. Record Dan's reply. Re-hash the files below (expected against actual) before touching anything; build in `round2/`.
2. Apply his picks: length (rerun `s03_edl.py` with the right spec, then stages 4 to 12), opening (opening B needs the
   `flow_a` card back: `plate_card("flow_a", [(B0049, 13.0, d)], "crop=1320:2420:0:170")` and its plate in `gfx05.py`),
   colour and sizes from RA-14, voice, analysis colours.
3. AI ideas he said yes to: START and END frames with `.claude/skills/_shared/codex-image.sh` (9:16, subject in the centre
   third, an ordinary non-model face, no stomach framing, no generated lettering). "Steps out of the phone" is two shots
   joined by a cut, never a morph. Show the frames and stop. No motion before he approves them.
4. When nothing is pending, the full film: 9:16 master, then the 16:9 from the same edit (`ra01lib.Aspect("16x9")`; the
   phone plates and lower thirds need their 16:9 layout, models: `from_plan.py`, `ad13-r2/h16x9_full.py`).
5. Work round 1 did NOT do, all owed before delivery: frame-lock the mix to the picture (see the trap below); the
   land-then-hold centring check (`cut/landing.py motion_stats`; crops are fixed per hold now, and holds 1, 2, 3 and 8 have
   face spans of 370 to 394 px, well past 3.3 % of the crop width); `s04b_holdstart.py` (a head sample on each hold's first
   frame); `piccuts.py decide`; `junk.py` on the final cut; `roll_sidecar.py mark-used`; the edit sheet for the 16:9;
   `audio_gate.py` with the A/B clip; `deliver/gate.py --format ad9x16|ad16x9`; the watch pass; one fresh independent
   reviewer; the negative-imagery scan; REVIEW 540p copies; notes; the delivery folder
   `Claude Ad Videos/how ai can get you real six pack abs - RA-05/`; a copy in `Videos to Review/` (the full ad is over
   45 s); `queue.py set RA-05 delivered` plus the artifact db; clip library `add --used-in "RA-05"`.

## Traps found in round 1

- **B0049's banned before/after screen ("Meet the new you") runs to about 27.6 s.** Start the result at 28.0 s. RA-04's
  round 1 draft started at 27.3 s and shows the banned screen for 0.3 s at 0:15.3 (noted in RA-04's handoff, fixed in the
  shared RA-04 recipe).
- **`s08_audio.py` with `LOCK=picture_9x16.mp4` hung twice** (its ffmpeg sat at 0 % CPU for 34 minutes) while another
  session's full render had the machine at load 63. The round 1 draft is muxed with the unlocked `mix.wav` (16 ms longer
  than the picture, `-shortest`). Re-run the lock on a quiet machine and `sample` the process if it stalls again.
- **The pose clip B0438 was built and dropped:** hard overhead sun and his hands cover his abs. B0435 (same shoot as the
  talking rolls) replaced it.
- The status board was at its 2,500 word limit all session; this job's entry is one token (`RA-05-R1-...`).

## Known risks, stated plainly

- The lower thirds and the button sit across his torso (the vertical kit's 68 % position); the wider shots put the lower
  third on his upper abs in the wide shot. He sees it in round 1.
- Three quick size changes sit at 24.09, 26.09 and 27.56 s because pauses were cut there. If he dislikes them, keep those
  pauses (0.5 s in total).
- Face sharpness: the close shot is a 1.67x enlargement and the wide 1.33x (better than RA-01's 1.82x and 1.54x).

## Files (work folder `/Volumes/Extreme/_edit_work/ra05/`, sha256 first 16; re-hash before touching)

| file | sha256 (first 16) | what |
|---|---|---|
| `round1/DRAFT - RA-05 round 1 - first 30 seconds.mp4` | b61778942b1fb372 | what Dan is reviewing (31.70 s, ends as the curls clip ends) |
| `draft_9x16.mp4` | 84c62d784e1f6c0f | internal full 9:16 draft, 54.99 s, not shown to Dan (unlocked mix, `-shortest`) |
| `picture_9x16.mp4` | 750a859cc50a05cd | its picture, 1,648 frames |
| `mix.wav` | 719fa73dcf64615e | voice (RA-01 chain, fitted tone, no dereverb) + Realizer bed at -32; audio gate PASS, -14.2 LUFS |
| `cut.json` | 6085e08766e6dd27 | the airtight cut: 54.15 s of talk + 0.85 s end hold, 15 pause cuts, 5 seams |
| `edl_spec.json` | 151d4dbfcf65e161 | take map with the sentence cut |
| `edl_spec_full.json` | 46231d6d2377bf1b | take map with every line |
| `tx/c1664.whisper.json` | a80ed2fd4efdd572 | word list 188 to 304 s, patched by `s02b_patch.py` |
| `words_aligned.json` | 16a3f7ccd0349bf3 | 202 words, CTC aligned to `mix.wav` |
| `framing.json` | dbc5c7db377a77cc | head and hair track, 269 samples, 0 misses |
| `beats.json` | c3c68df33721be0d | cards, Dan holds, lower thirds, button |
| `grade.json` | 5c6afef7ee85ed09 | the C2 look for this roll (not his pick yet) |
| `framing_choice.json` | 38ee6870595e8494 | close 648x1152, wide 810x1440 (not his pick yet) |
| `colour/luts/ra05_C1_approved_level.cube` | 5dd935186b26e7c0 | look C1 for C1664 |
| `colour/luts/ra05_C2_brighter_gold.cube` | 910440d9553814e1 | look C2 for C1664 (in the sample) |
| `colour/luts/ra05_C3_brighter_cool.cube` | 04c8a0406a1b0977 | look C3 for C1664 |
| `hf9/manifest.json` | 531fe8dffb929e4d | Soft Blue overlays (lower thirds, button) |
| `round1/index.html` | 4806d5c39b225807 | the review page |

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `How AI Real Abs AD R2`. Read `Handoffs/handoff-20261013-ra05-round2-after-dan-review.md` and
> `.claude/skills/ad-edit/reference/ra05/README.md`, then continue RA-05 "How AI Can Get You REAL Six Pack Abs" with
> /ad-edit. My answers to the round 1 page are: [paste the reply box]. Record them word for word first. Apply them, apply
> my colour, shot size and voice picks from the Cheat Code ad (RA-14) and the analysis card answer from Top 3 Tips
> (RA-04), make frames for any AI clip I said yes to and stop for my approval; if nothing is pending, build the full 9:16
> and the 16:9 from the same edit, run every gate and the independent review, deliver, and send me the review copy.
> Use the Codex subscription to generate the images.

**Recommended model and effort: Opus 5.5, high.** A bounded revision plus a recipe-backed full build with gates.
