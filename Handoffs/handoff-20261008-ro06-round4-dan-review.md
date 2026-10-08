# RO-06 "How To Work Out At Home On A Budget": round 4, after Dan reviews the round 3 page

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R4`.
Written 2026-10-08 by Claude (Opus 5.5) at the end of round 3. Replaces `handoff-20261008-ro06-round3-first-minute-ai-clips.md`
(executed). The full-film steps stay in `handoff-20261008-ro06-round1-dan-review.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md` (round 3 notes at the end),
`/Volumes/Extreme/_edit_work/ro06/round3/round3-record.json` (hashes, slots, costs, motion plan).

## What round 3 delivered (Dan has NOT answered yet)
- Review page: http://localhost:8848/index.html (restart: `python3 .claude/skills/_shared/review_server.py 8848 /Volumes/Extreme/_edit_work/ro06/round3`).
- First minute: `/Volumes/Extreme/_edit_work/ro06/round3/first-minute/DRAFT - RO-06 round 3 - first minute.mp4`, sha256
  `465271789c21b9da90f403b50b54c0f7d2c4b1a93da0848da0e63ae183edab04`. VLC copy: `Videos to Review/Work Out At Home LFC R3 - first minute.mp4`
  (replace after a re-render; delete when Dan finalizes the video).
- Jump rope (C01 clip 2, 6.07 to 8.44 s): now `B0448@4.0` (roll C1674 99.0 to 101.4 s, high-knee, 155 steps a minute).
  C06 keeps `B0430`. `B0447` is out of the film and marked as the beginner demo in the clip library.
- Equipment shot (C02, 20.18 to 23.12 s): `round3/c02/C02-pan-topaz.mp4`, a 2.25x window panning kettlebell to dumbbells,
  from a Topaz 4K upscale of C1557 3.0 s on. Grade `C1559` as before.
- Four AI clips as labelled START/END placeholders: A1 31.12 to 33.54, A2 33.54 to 35.80, A3 38.56 to 41.16 (slap lands on
  "destroy", 39.40), A4 41.16 to 46.68. Frames: `round3/frames/A{1..4}-{start,end}.png`; references in `round3/frames/ref/`.
- Checks run: audio gate PASS; audio identical to the approved round 2 file (untreated WAV md5 and decoded audio md5 both
  equal); every visible frame of Dan uses the round 2 crop and source frame (0 of 1204 differ); hair at least 26 px from
  the top on 158 samples; cut strip `round3/qc/fm_joins.jpg`.
- Not run (they need the complete film): delivery gate, watch pass, independent review, edit sheet.

## Locked by Dan (do not reopen)
Cropping, colour, audio, the tight open, the three-clip opening with ab wheel `B0436@2.0` and kettlebell `B0439@0.5`
(words in `round3-plan/decisions.json`). Soft Blue Light graphics.

## Waiting on Dan: 10 decisions on the round 3 page
1 frames for A1 and A2 · 2 frames for A3 · 3 A4 as one push-up clip, or two shorter clips (push-ups, ab wheel) ·
4 hair at the top edge on 9 later rolls · 5 length · 6 AI product pictures · 7 jump rope "$10" vs "$9" · 8 music bed ·
9 app demo treatment · 10 confirm no AI opener. He may also overrule the jump rope pick or the pan. Do not infer anything
from silence. When he replies, record his words and the reviewed hashes in `round4-plan/decisions.json` before building.

## If he approves frames: the motion step
- **No motion is authorized until his reply names the clips.** Budget: $5 per video; spent $0.24 (Topaz). Estimate $2.20
  for one take of each, $4.40 with one redo each. Past $5, stop and tell him the number and the reason.
- Motion: `google/veo-3.1-fast` with `image` + `last_frame`, 1080p, `generate_audio: false`, 4 s for A1 to A3 and 6 s for
  A4 ($0.10 a second). Submit one at a time (two at once get throttled). Trim each to its slot on the best-flowing part;
  never hold or slow a clip (a slight speed-up is allowed). A3: place the trim so the hit is at 39.40.
- Lip sync (A1, A2): `sync/lipsync-2-pro`, `active_speaker` on, audio = Dan's impression cut from the first minute's
  `.untreated.wav` at 31.12 to 33.12 and 33.54 to 35.68. The lips are picture only: the film's audio must stay
  sample-identical (repeat the two md5 checks). If the model animates the trainer's mouth too, crop to the client's face,
  sync, and composite back.
- Judge each clip at playback speed (VIDEO-RULES, 2026-10-08), then frame by frame for hands, the whistle, the wallet and
  the tank-top logo. Every AI clip keeps the AI-GENERATED chip. In `plan.py` replace `frames=` with `src=` and drop
  `pending` once a clip is approved.
- For `/video-setup` later: realistic AI footage, so the upload's AI flag is true.

## Costs
Metered: $0.24 (Topaz upscale). Codex stills on the subscription: 6 in round 1, 12 in round 3. Cap: $5 per video.

## Next action
Wait for Dan's reply. Apply his first-minute notes, generate approved motion, show the first minute with the clips moving,
then once nothing is pending build the full film per the round 1 handoff (start with the leans scan in the round 2 handoff's
open risks). Recommended: **Claude Opus 5.5, high.**

## Starter prompt
> Read `Handoffs/handoff-20261008-ro06-round4-dan-review.md` and execute it with /longform-edit. This is RO-06 "How To Work
> Out At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R4`. My answers to the round 3
> page are below. Record them, fix anything I flagged, generate the AI clips I approved (lip sync on the two excuse
> clips), and show me the first minute with them moving.
> [paste the reply box from the round 3 page here]
