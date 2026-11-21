AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Top 3 Tips AD R5`.

# RA-04 "Top 3 Tips For Getting Abs": round 5, a white man's generation up front, the lock screen on him, end 1 s earlier

**Written 2026-10-15 by the round 4 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-04-top-3-tips-for-getting-abs.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (read in full), `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe and lessons: `.claude/skills/ad-edit/reference/ra04/README.md` (round 4 = lessons 22-26, scripts in `round4/`).
Work folder: `/Volumes/Extreme/_edit_work/ra04/`. Round 4 delivery: `Claude Ad Videos/top 3 tips for getting abs - RA-04/`
(`notes-RA-04.md`, `ROUND-4-REVIEW*.md`, `recipe-RA-04/`). Round 4 page: http://127.0.0.1:8898/ (managed by `_shared/review_server.py`).

## Dan's words on round 4 (2026-10-15)

> "From 3 seconds to 7 seconds, I'd like to put in the generation clip of generating abs with the Asian guy's image, not my image, but
> the AI-generated Asian guy's image, and then go into the picture of him on the phone rather than me. Same clip at 8 seconds, but use a
> clip of him on the phone instead of me. When this appears again at 15 seconds, change this to the different guy. Change it to the image
> of the white guy. Actually, switch: I use the white guy in the beginning. Use the Asian guy where he is. Keep that where it is at 15
> seconds, and then put in the white guy generation clip at the beginning. For the end of the video, I want you to end it about 1 second
> earlier. There's about a second of awkward silence at the end."

**His final instruction, read plainly:**
1. **0:03-0:07: a generation clip of a WHITE man** (the app generating his abs picture), replacing Dan on camera there.
2. **Then the lock-screen card (0:06.84-0:09.94) shows that same white man's AI picture on the phone**, not Dan's.
3. **The Asian demo man stays where he is** (the app cards at 0:12.2-0:17.9 and the analysis card at 0:25-0:31). No change.
4. **End about 1 s earlier.**
Record his words and this reading in `round5-plan/decisions.json` (new) before building.

## What exists and what has to be made

* **No white man's generation recording exists.** The clip library's app recordings (B0049, B0006) are both the Asian demo man.
  `clip_library.py find` found nothing else. It has to be made.
* **Lock screen:** library clip `A0074` (a hand holding a phone, the lock screen showing Dan's AI goal picture, 9:16, used 0.5 s onward
  in the card). Keep the hand and phone motion; replace the screen picture with the white man's AI result.

### Step 1: the white man's before photo and his real generation (same person before and after)

* **Before photo:** a heavier white man, shirtless, standing, whole body or chest-up like B0049's before photo, ordinary and unposed.
  Look on Pexels first (known rights, no paid stock). If nothing fits, generate one with Codex (`_shared/codex-image.sh`, read
  `_shared/IMAGE-GENERATION.md`); an AI before photo then carries the AI-GENERATED chip on the generating screen too.
  **No belly close-up, no pinching, no shame framing** (VIDEO-RULES 2026-10-04): this sits in the first 7 seconds.
* **Generate his after picture through the live product**, never a composite (before/after are the SAME PERSON, VIDEO-RULES
  2026-09-12). Record the generation flow on a phone screen in the B0049 format (iPhone screen recording, about 1320 px wide): the
  `/make-ad` product-capture recipe in the iOS Simulator (`simctl addmedia` -> real picker -> real generation -> `simctl io recordVideo`)
  or the local-server capture of ad-edit lesson 113. Real generations cost real money: state the spend first (cents; this video has
  spent $5.80 of its $20 budget). Never generate on the Apple-review demo account.
* **Banned screens (lesson 12, RA-05 trap 1):** the app's "Meet the new you" BEFORE/AFTER screen and the email form must never appear.
  Check the first and last five frames of every piece you cut, and every frame of any piece that scrolls (round 4 lesson 25).
* **Do not stop for a separate stills round.** Dan asked for this change by name, and the short-ad rule (VIDEO-RULES 2026-10-14) says
  build the whole film. Put the before photo and the after picture as stills at the top of the round 5 page, one line each, so he can
  veto them. Offer two before-photo candidates only if the first choice is weak.

### Step 2: the generation card, 0:03.20-0:06.84

* **Slot:** the card replaces Dan's holds `dan01` (3.20-3.87, "Number one,") and `dan02` (3.87-6.84, "use AI to generate a picture of
  yourself with abs."), ending on frame 205 where the lock card starts. Dan said "3 to 7 seconds", so it starts at 3.2032 (frame 96).
* **Content, about 3.6 s:** the generating screen with his before photo and the progress/scan (about 2.4 s), then the result screen
  alone with his AI picture (about 1.2 s), the AI-GENERATED chip on the result. Cut like `flow_a`/`flow_b` in `s06_inserts04.py`:
  one crop window per app screen (a segment may carry its own crop, round 4), nothing sliced at an edge.
* **The TIP 1 lower third (LT1, 3.20-6.84, "Put Your Goal Picture On Your Lock Screen") now sits over a card instead of over Dan.**
  Keep it (TIP 2 and TIP 3 have theirs). Give this card a shorter media-card plate that ends above the strip, so the strip sits on the
  blue field, not across the phone: 9:16 strip box y 1058-1306 and captions at y 1400 (plate bottom about y 1030 or less); 16:9 strip
  top about y 840 with captions lifted above it (measure the lifted caption ink; the plate must end above it). **`s07_captions.py`
  asserts on a line that starts inside a card while a strip is up** ("a word starts under the strip"): add the rule for this one card
  (lift the line above the strip, plate shortened to clear it) and run `s88`-style checks that no caption touches the plate or strip.
* Build the plates with `round4/r4_plate9.py` (9:16) and `gfx16_04.py` PLATES_ONLY (16:9); register the recording in the clip library
  (`clip_library.py add ... --kind screen --people other-man`).

### Step 3: the lock-screen card, 0:06.84-0:09.94, on the white man

* Replace A0074's screen picture with his AI result, held still and tracked to the phone: start from RA-05's
  `reference/ra05/round3/lockscreen.py` (SIFT/RANSAC tracking against frame 0, corner smoothing, finger exclusion). It registers a `ref`
  picture to frame 0 by SIFT, which cannot work for a different man: add an option that maps the new picture straight onto frame 0's
  inner screen quad. Lock-screen clock optional (a reviewer noted A0074 shows none; Dan approved it so in round 1).
* Keep the AI-GENERATED chip at (60, 236) in 9:16 and on the field beside the plate in 16:9 (unchanged geometry).
* Treat it as a changed AI clip: the three questions (cause and effect / clear with sound off / shows the line), a frame-by-frame look at
  the screen edges and the fingers, then the watch-pass judge and the reviewer. Register it (`--kind ai --people other-man`).

### Step 4: end 1 s earlier

* Measured on round 4: the last word "app." ends at **57.51 s**, the mix falls to about -46 dB from **57.6 s**, and the file ends at
  **58.892 s** (1765 frames): 1.38 s after the word. One second off gives **57.89 s (frame 1735)**, a 0.38 s end hold.
* Before cutting, print his mouth and pose frame by frame from 57.4 s (RA-14 round 4 lesson 1) and end on the last frame of a held pose,
  between about 57.8 and 57.95 s. The CTA strip and the last caption run to the new end.
* Audio: the voice is unchanged. Shorten the mix to the new picture and smooth the music tail on the MIX after the last word (RA-14 round
  4 lesson 2, `s42`-style inverse envelope, voice bit-identical), or re-run `s08_audio.py` with `LOCK=picture_9x16.mp4` and the voice B
  EQ in `r4_chain.sh`. Re-gate.

## How the round 4 build fits together (read before editing the plan)

* The plan is rebuilt by a pipeline, in order: `round4/r4_home.py` (from `round4/backup/beats.json`) -> `round4/r4_split.py` ->
  `round4/r4_track.py` (writes `beats.json`). Add a `round5/r5_gen.py` after `r4_split.py` that replaces `dan01`+`dan02` with the `gen`
  card and re-indexes the holds. **`r4_track.py`'s per-hold overrides are by index** (`HOLD_LEVEL "10:FAR"`, `HOLD_TRACK
  "10:...;15:..."`): removing two holds shifts them. Key them by beat start time instead, then re-check that the CTA hold (52.42 s on)
  keeps its follow and that 43.44-45.38 s stays FAR. 14 of 16 holds are held still at the middle of his range (`HOLD_MAX` 12).
* Re-run `s04b_holdstart.py` on the new plan, `s06_inserts04.py` / `s06_inserts16_04.py` for the new cards, `s07_captions.py` both,
  `s10_render04r4.py` both (stage 1 must run: the timeline changes), then the mux with the shortened mix.
* **Gates (all of round 4's, on the exact delivered files):** `round4/r4_gates.sh` (measure, chips, gate plans, watch passes),
  `audio_gate.py --ab`, `s20_neg.py`, a fresh judge per aspect, `watch.py --judge`, `deliver/gate.py --format ad9x16` and `ad16x9`,
  `round4/s_sheet04.py` + `validate.py`, one fresh independent reviewer. Update `s_chips04.py` and `s_gateplan04.py` for the new `gen`
  card and the lock card's new chip, and `s_sheet04.py`'s FACTS (`lock` becomes `other`, physique true, label ai).
* **The Extreme drive was 100 % full on 2026-10-15** (other jobs). Check `df -h /Volumes/Extreme` first. Round 4 rendered with
  `SEG_DIR=<scratchpad>/seg_9x16` (`s10_render04r4.py` reads it) and `WATCH_ROOT=<scratchpad>/ra04_watch` (`r4_gates.sh`,
  `s_gateplan04.py`). Never delete another job's files to make room.
* Two-build cap: chains wait behind `buildcap.wait()`; run them in the background and let the notification bring the session back.

## Deliver

* Replace the two masters in `Claude Ad Videos/top 3 tips for getting abs - RA-04/` (same names), REVIEW 540p copies, A/B, stamps,
  `notes-RA-04.md` (round 5 section), `ROUND-5-REVIEW.md`, `recipe-RA-04/`. Replace the two `Videos to Review/Top 3 Tips AD R4 - ...`
  copies with `Top 3 Tips AD R5 - 9x16 ad.mp4` / `16x9 ad.mp4`.
* Round 5 page on port 8898 (`python3 .claude/skills/_shared/review_server.py 8898 <dir>`): the before photo and after picture stills,
  both films, and the revision list with exact timestamps from the delivered timeline: the generation card (0:03.2-0:06.8, watch
  0:01-0:11), the lock card (0:06.8-0:09.9), the new ending (watch 0:54 to the end), and "everything else unchanged".
* `queue.py set RA-04 delivered` + the artifact db mirror, push the recipe and lessons with `scripts/git/safe-push.sh`.

## Known risks

* The white man's before photo is the one genuinely new judgment in this round; if Dan dislikes it, only steps 2-3 re-run.
* Shortening the plate under LT1 makes the phone small in 16:9; if it ends up under about 600 px tall, show Dan the 16:9 frame on the
  page and say so in one line.
* Two different demo men now appear in one ad (white man up front, Asian man at 0:12-0:31). That is Dan's explicit choice.

## Starter prompt

> Read `Handoffs/handoff-20261015-ra04-round5-white-guy-generation-and-shorter-end.md` and `.claude/skills/ad-edit/reference/ra04/README.md`,
> then run round 5 of RA-04 "Top 3 Tips For Getting Abs" (an AD) with /ad-edit. Name this task `Top 3 Tips AD R5`. Make a white man's
> real app generation for 0:03-0:07, put his AI picture on the lock-screen phone at 0:07-0:10, keep the Asian demo man where he is, end
> the video about 1 second earlier, then build the full 9:16 and 16:9, every gate, independent review, and deliver.

**Recommended model and effort: Opus 5.5, high.**
