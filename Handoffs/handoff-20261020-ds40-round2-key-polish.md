**SFC.** Task name: `Fat 90 Year Old SFC R2`.

# DS-40 R2: "Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right." Make the green screen key beat Codex

Written 2026-10-20 by the R1 task (Claude, Opus 5.5). Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and the job doc `Handoffs/video-editing/DS-40-bill-maher-asks-if-youve-ever-seen-a-fat-90-year-old-hes-rig.md` first.

## Why this round exists
This is the project's first green screen video and a bake-off: Codex is editing the same video, and whoever does better edits every future green screen video. Dan asked for small rounds: R1 was key, colour and voice only, on a 9.3 s sample. His R1 reply (verbatim, also in `/Volumes/Extreme/_edit_work/ds40/r1/decisions.json`):

> "Okay, let's go with the warm vivid color B for the color. Let's do the house voice plus a half-bass lift for the voice. For this key, this is looking pretty good. This is about the same as what Codex did. You have both done a pretty good job with that. I want you to see, though, if there are any further improvements here. There's very little flickering in the hair. Codex had some issues in the first round with the hair, but then it was corrected. You're about even with Codex now. Work on that chroma key a little bit more and see if you can make it even better. That way, it beats Codex."

## Locked (do not reopen)
- Colour: **B Warm Vivid**, `LOOKS['B_warmvivid']` in `key/grade.py`.
- Voice: **house chain plus +1.5 dB at 120 Hz** (`audio/a30/E_bass15.wav`; EQ in its `.voice_chain.json`). Build the full Short's voice from the same chain on the full take.
- Key method: everything in `.claude/skills/shorts/reference/ds40-greenscreen/README.md` (read it in full; code beside it, identical to `/Volumes/Extreme/_edit_work/ds40/r1/key/`).

## Goal of R2: a visibly better key than R1, proven, still on the same 9.3 s sample
Scope stays the key (plus the sample re-rendered in colour B with the chosen voice). No layout, captions or full film yet unless the key is done early and Dan's words allow it (they do not).

Measured R1 state (independent reviewer, `/Volumes/Extreme/_edit_work/ds40/r1/audit/R1-REVIEW.md`, scripts in `audit*/scripts/`):
- Edge flicker vs the camera source: 1.018 average, 1.083 worst. The hair flicker that remains is the SOURCE's own grain on a 10-bit S-Cinetone roll. **Beating Codex means going below 1.0: a key that is steadier than the raw footage.**
- Dark rim on skin edges: 15% of edge samples vs 8% in the source (shows on light backgrounds only).
- Watch glass edge-on still see-through: 0:00.00 to 0:00.40 (frames 0 to 12), frame 236 (0:07.87), frames 250 to 254 (0:08.34 to 0:08.44).
- One faint 13 px speck, frame 142 (0:04.74, x 13, y 1707).

Ideas, in the order I would try them (measure each against R1 with the reviewer's flicker and rim scripts, keep only what wins):
1. **Temporal stabilisation of the matte in the hair and edge band:** motion-compensated averaging of the colour-difference map (or alpha) over 3 to 5 frames (OpenCV DIS optical flow, already installed: cv2 5.0), only where local motion is small, so moving hands keep their blur. Target hair flicker ratio well under 1.0.
2. **Temporal denoise of the source before keying** (motion-compensated, e.g. averaging aligned neighbours) in the edge band only; the interior uses the original pixels.
3. **Edge colour decontamination** instead of plain screen subtraction for partly transparent pixels: estimate the foreground colour by pushing interior colours outward (normalised-convolution inpaint of F from alpha > 0.95 pixels) and blend toward it as alpha falls. Should remove the 15% dark rim.
4. **Watch glass:** a hand-drawn polygon per frame for frames 0 to 12, 236 and 250 to 254 (keyframe 3 or 4, interpolate), forced solid. The automatic hold-out (`watch_holdout` in keylib) cannot see a perfect mirror of the screen.
5. Light wrap and edge softness tuning only after 1 to 3, judged on navy, pale and saturated pink.

## Deliverable
- The 9.3 s sample re-rendered (colour B, voice E) with the improved key, plus the same over pale and pink.
- An R2 page on the same port 8940 (`review_server.py 8940 <dir>`; build in a new `r2/` folder, never overwrite `r1/`): R1 vs R2 side by side, looping 3x crops of the hairline, ear, shoulder and fast hand over 5 consecutive frames, and the measured flicker, rim and watch numbers before/after. Plain words, "What I decided", one reply box.
- A fresh independent reviewer (same brief style as R1: files only, every frame, the reviewer's scripts) must confirm the gains and no regressions before Dan sees it.
- Rename the task first to `Fat 90 Year Old SFC R2`.

## Files and facts
- Work: `/Volumes/Extreme/_edit_work/ds40/r1/` (key/, cache/ = R1 keyed frames, review/ = R1 page, audit*/ = reviewer evidence, audio/, src/maher_yfiWjnStE3w_210-238.mp4 and card_last.png).
- Source: roll C1730 of `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/`, sample = 1400.25 to 1409.55 s (scripted take 1400.25 to about 1449; off-the-cuff take from 1453.7).
- Speed: key stage about 1 s a 4K frame with 4 workers; composite about 0.6 s a frame. Respect the two-build cap (`_shared/buildcap.py`).
- Trap: R1 once shipped empty 261-byte MP4s after a keylib edit truncated the file; the stage scripts now assert, keep the asserts.
- Queue: DS-40 is `draft_review` in the Edit Queue. Board entry `DS-40:R1-REVIEW:8940` (rename to R2 when you start).

## Starter prompt
> Fat 90 Year Old SFC R2. Read `Handoffs/handoff-20261020-ds40-round2-key-polish.md` and execute it: Dan locked colour B and the house voice with a half bass lift; make the green screen key measurably better than R1 (hair flicker below the source's own, no dark rim, watch glass solid), prove it with an independent reviewer, and put R1 vs R2 on the review page at port 8940.

Recommended model: Claude Opus 5.5, high effort.
