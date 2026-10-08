# RO-06 "How To Work Out At Home On A Budget": round 4, generate the four AI clips and show the first minute with them moving

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R4`.
Written 2026-10-08 by Claude (Opus 5.5) after Dan approved the round 3 first minute and all four AI frame pairs.
Replaces `handoff-20261008-ro06-round3-first-minute-ai-clips.md` (executed). The full-film steps stay in
`handoff-20261008-ro06-round1-dan-review.md`; its open risks are in `handoff-20261008-ro06-round2-dan-review.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md` (round 3 notes at the end),
`/Volumes/Extreme/_edit_work/ro06/round4-plan/decisions.json` (Dan's words, hashes, what is authorized),
`/Volumes/Extreme/_edit_work/ro06/round3/round3-record.json` (slots, costs, motion plan).

## Scope of this round
Generate motion for A1, A2, A3 and A4 from their approved frames, sync the client's lips to Dan's impression in A1 and A2,
put the four clips into the first minute in place of the placeholders, and show Dan that first minute. Build in
`/Volumes/Extreme/_edit_work/ro06/round4/` (frames and a small A3 page are already there; never overwrite `round3/`).
**No full film this round**: seven older decisions are still unanswered (below).

## Locked by Dan (do not reopen)
- Cropping, colour, audio, the tight open, the three-clip opening (round 2 words in `round3-plan/decisions.json`).
- The round 3 first minute: "everything is looking good except A3". That covers the jump rope clip `B0448@4.0` and the
  panning equipment shot `round3/c02/C02-pan-topaz.mp4`. Reviewed file: `round3/first-minute/DRAFT - RO-06 round 3 - first
  minute.mp4`, sha256 `465271789c21b9da90f403b50b54c0f7d2c4b1a93da0848da0e63ae183edab04`. Re-hash before building.
- Frames, all approved, motion authorized for all four:
  - A1 and A2: `round3/frames/A1-start.png`, `A1-end.png`, `A2-start.png`, `A2-end.png`.
  - **A3: the ROUND 4 pair only**, `round4/frames/A3-start.png` and `A3-end.png` ("A3 is approved"). The round 3 A3 pair was
    rejected (right hand raised, left hand used, ended before the slap landed). Do not use it.
  - A4: `round3/frames/A4-start.png`, `A4-end.png`, as one clip of push-ups.
  Hashes for every frame are in `round4-plan/decisions.json`. Re-hash them before spending anything.

## Slots (output time, from `plan_resolved.json`; picture only, the voice track must not change)
| ID | slot | he is saying | action |
|---|---|---|---|
| A1 | 31.12 to 33.54 | "Dan I don't have time to go to the gym" (ends 33.12) | client whines and taps his bare wrist; Dan arms crossed, rolls his eyes |
| A2 | 33.54 to 35.80 | "or Dan I don't have the money for a gym membership." (ends 35.68) | closer shot; client turns his wallet upside down, empty; Dan facepalms |
| A3 | 38.56 to 41.16 | "I'm about to destroy all those excuses," | Dan's LEFT hand slaps across the client's cheek toward the camera; the hit is on "destroy" at 39.40; the hand carries on past his face; his head turns to the camera |
| A4 | 41.16 to 46.68 | "show you why they're all a crock of shit ... not valid in any way whatsoever." | client does push-ups on the push-up handles on the blue mat; Dan kneels beside him, whistle, then fist pump |

## How
- **Motion:** `google/veo-3.1-fast` on Replicate, `image` (start) + `last_frame` (end), 1080p, `generate_audio: false`,
  4 s for A1, A2, A3 and 6 s for A4 ($0.10 a second). Submit one at a time (two at once get throttled; `E005` on a create
  is transient). The frames are 1672x941: scale to 1920x1080 before sending.
- **Trim, never stretch:** cut each clip to its slot on the best-flowing part. Never hold or slow a clip; a slight speed-up
  is allowed. A3: choose the trim so the palm reaches his cheek at 39.40 (0.84 s into the slot).
- **Lip sync (A1, A2):** `sync/lipsync-2-pro` with `active_speaker` on, audio = Dan's impression cut from
  `round3/first-minute/DRAFT - RO-06 round 3 - first minute.mp4.untreated.wav` at 31.12 to 33.12 and 33.54 to 35.68. If it
  also moves the trainer's mouth, crop to the client's face, sync, composite back. No new voice is made.
- **Plan:** in `recipe/plan.py` give each item `src=[clip@offset]` in place of `frames=`, drop `pending`, keep
  `label="AI-GENERATED"`. A3's entry still points at the round 3 frames: it gets the clip made from the round 4 pair.
- **Checks:** judge every clip at playback speed, then frame by frame for hands, fingers, the whistle, the wallet and the
  tank-top logo (VIDEO-RULES, AI clip faults, 2026-10-08). The client stays fully clothed and no frame centres on his
  stomach. Then: `build.py segs 66`, the cut strip (`fm_qc.py`), the hair check (`hair_fm.py`), the audio gate, and the two
  md5 checks that prove the voice is identical to round 2 (untreated WAV `fbf7798364cf1f0592144e03827a3b8a`, decoded audio
  `351d8f6d7a42a63ae44c42c9d46db45a`). Compare crop and source frame of every visible presenter frame against
  `round3/...build.json` (expect 0 differences).
- **Deliver:** page from `recipe/page3.py` (first minute on top, the four clips each with a "play it in place" button, What
  changed, What I decided, the open decisions, one reply box), served with `review_server.py`. Replace the VLC copy
  `Videos to Review/Work Out At Home LFC R3 - first minute.mp4` with the R4 file. Show Dan, then stop.

## Budget
$5 per video for AI clips, retries included. Spent: $0.24 (Topaz upscale). Estimate: $2.20 for one take of each clip with
the lip sync, $4.40 with one redo of each. If the total would pass $5, stop and tell Dan the number and the reason first
(he is generally open to $10 with a reason).

## Still open (Dan has not answered; do not infer from silence)
Hair at the top edge on 9 later rolls · length (trim repeats or keep 17:39) · AI product pictures in the price cards ·
jump rope "$10" vs "$9" · music bed · app demo treatment · confirm no AI opener. Ask again on the round 4 page, in one
list, with the recommendations from `recipe/page3.py`. The full film waits for these.

## Notes for later steps
- Realistic AI footage is now in the film, so the upload's AI flag is true (`/video-setup`).
- When the film is finalized, register the four AI clips in the clip library and delete the copies in `Videos to Review/`.
- Round 3 page: http://localhost:8848/index.html. A3 page: http://localhost:8849/index.html. Restart either with
  `python3 .claude/skills/_shared/review_server.py PORT /Volumes/Extreme/_edit_work/ro06/roundN`.
- Not run yet (they need the complete film): delivery gate, watch pass, independent review, edit sheet.

## Next action
Re-hash the locked files, generate A1 first as the test of the motion and lip-sync path, then the other three, build the
first minute, show Dan. Recommended: **Claude Opus 5.5, high.**

## Starter prompt
> Read `Handoffs/handoff-20261008-ro06-round4-ai-motion-first-minute.md` and execute it with /longform-edit. This is RO-06
> "How To Work Out At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R4`. I approved the
> round 3 first minute and the start and end frames for all four AI clips (A3 is the new left-hand slap pair). Generate
> the four clips, sync the client's lips to my impression in the two excuse clips, put them in the first minute, and show
> it to me. Then stop.
