# RO-06 "How To Work Out At Home On A Budget": round 3, first-minute revisions and four AI clip frame pairs

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R3`.
Written 2026-10-08 by Claude (Opus 5.5) after Dan reviewed the round 2 first minute. Replaces
`handoff-20261008-ro06-round2-dan-review.md` as the next action. The full-film steps stay in
`handoff-20261008-ro06-round1-dan-review.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`,
`/Volumes/Extreme/_edit_work/ro06/round3-plan/decisions.json` (Dan's words, verbatim, with the reviewed hash).

## Scope of this round
Two picture fixes in the first minute, plus START and END frames for four new AI clips. Build in
`/Volumes/Extreme/_edit_work/ro06/round3/` (never overwrite `round1/` or `round2/`). Show Dan the rebuilt first minute with
the frame pairs sitting in their slots as labelled START/END placeholders, then stop. **No AI motion is generated this round.**
No full film.

## Locked by Dan (do not reopen)
- **Cropping, colour, audio:** "All the cropping, color correction, and audio look good." The three sizes and their order as
  built in round 2 are approved. Reviewed file: `round2/first-minute/DRAFT - RO-06 round 2 - first minute.mp4`, sha256
  `7d02163e44ef7d1395c91ef07a16dbc5dd1436aead2d930141f39f33981edc41`. Re-hash before building.
- **The tight open:** "I like the tight shot at the beginning."
- **Three clips at the start:** "I like how you added three clips in." Ab wheel `B0436@2.0` and kettlebell `B0439@0.5` stay.
- The voice track must stay sample-identical: after the render, md5 the untreated WAV and the decoded audio against round 2
  (the method is in the ro06 README, round 2 notes). The AI clips are picture only.

## Change 1: the jump rope clip (C01, clip 2, 6.07 to 8.44 s)
Dan: "I want the one where I'm jump roping fast at full speed. This was a demonstration of how beginners should start off,
not how jump roping is really done. Change out the jump roping clip for one of me jump roping smoothly at full speed."
- `B0447` (alternating feet) is the beginner demo: out. Look at `B0430` (both feet, poolside) and `B0004` first, then the raw
  rolls behind the DS-17 "how to jump rope" short (`clip_library.py find "jump rope" --rolls`; `B0421` and `B0422` are its
  9:16 garage cuts). Pick 2.4 s of smooth, fast, continuous jumping with no trip. Judge it moving, not on a still.
- `B0430` is C06 later in the film. No source repeats: if it moves to the opening, give C06 another clip (the beginner
  demo `B0447` may fit the jump rope section, where he talks about starting out).
- Correct `B0447`'s catalog description (`Media/clip-library/catalog.json`) so it reads as the beginner demo, then
  `clip_library.py sheet`.

## Change 2: the equipment shot (C02, 20.18 to 23.12 s)
Dan: "take a tighter crop where the workout stuff is centered and then pan through that. Start at the kettlebell and then
move through that all the way to the right by the end of that clip's duration, rather than just showing at the bottom of the
screen. If necessary, upscale that clip."
- Source `C1557.MP4@3.0` is 1920x1080, locked off, 14.5 s. The equipment spans about 12 % to 75 % of the width and sits in the
  bottom fifth of the frame, touching the bottom edge.
- Build: a fixed-height crop window (about 2x to 2.5x) with the equipment centred top to bottom, travelling left to right from
  the kettlebell to the dumbbells over the full 2.94 s, eased at both ends, sub-pixel (render the crop per frame from a
  float x, never integer steps). This is an object shot, so the no-camera-movement rule for Dan on camera does not apply.
- At that size it is an enlargement: upscale the 88 source frames first (a video upscaler on Replicate is cents for 3 s; the
  session cap covers it) and compare at full size against plain lanczos plus sharpening. Use the cleaner one. Grade stays
  `grade="C1559"` as in round 2.

## New: four AI clips, frames only this round
Dan's words are in `decisions.json`. Slots, anchored to the words (output times from `words_out.json`):

| ID | when | he is saying | what the clip shows |
|---|---|---|---|
| A1 | 31.12 to about 33.4 | "Dan I don't have time to go to the gym" | AI-Dan in a trainer outfit in a home gym; the fat, whiny loser whines this excuse |
| A2 | 33.54 to 35.80 (the shot join) | "or Dan I don't have the money for a gym membership." | same room, same two men; the loser whines the second excuse |
| A3 | about 38.56 to 41.1 | "I'm about to destroy all those excuses," | Dan slaps the loser in the face; the hit lands on "destroy" (39.40) |
| A4 | 41.16 to 46.68 (the join into the wide) | "show you why they're all a crock of shit ... not valid in any way whatsoever." | Dan has the loser doing simple home workouts with this equipment (mat, push-up handles, jump rope, ab wheel) |

- **Lip sync (A1, A2):** "sync up the loser's voice to my lips as best as you can, so it looks like he's the loser making
  excuses and talking when I do that impression." The loser's mouth is driven by Dan's own impression audio for those words
  (cut from `lav.wav` at the source times of 31.12 to 35.80). No new voice is made and the film's audio does not change. Plan
  the motion step around a lip-sync capable model and say which on the frames page.
- **Frames:** every still through `.claude/skills/_shared/codex-image.sh` on the subscription, 16:9. Dan's likeness from the
  AI-Dan references in `/exercisegeneration`. One consistent loser and one consistent home gym across all four clips: make a
  character and room reference first, then the eight frames from it. The equipment in A4 must match the real items in
  `C1557.MP4`. Keep both men in the centre third (Shorts are cut from this film later).
- **Frame prompts:** show the loser whole and clothed; do not frame on his stomach and no hands on his belly
  (VIDEO-RULES, 2026-10-04; A1 and A2 sit right at the 30 s mark). Every AI clip carries the AI-GENERATED chip.
- **Budget:** $5 per video for AI clips including retries; $0 spent so far. Put the motion estimate for all four clips, with
  the lip sync, on the frames page. If it is over $5, say the number and the reason there (Dan is generally open to $10 with a
  reason) so one reply approves frames and spend together.
- **In the first minute:** A1 to A4 go in as labelled START/END placeholders at their slots (the 2026-09-28 preview
  convention) so Dan judges them against the speech. The plan gets four `clip` items with `pending=True`. The framing solver
  splits shots at each new clip start by itself (`shot+c` segments); re-check `build.py segs 64`, the cut strip and the hair
  check afterwards, since the tight, medium and wide pieces between the clips will shift.
- **Later, at setup:** these are realistic AI footage, so the upload's AI flag is true (VIDEO-RULES, 2026-09-27). Note it in
  the edit notes for `/video-setup`.

## Still open (Dan has not answered; do not infer from silence)
Hair at the top edge on 9 later rolls · length (trim repeats or keep 17:39) · AI product pictures in the price cards · jump
rope "$10" vs "$9" · music bed · app demo treatment · confirm no AI opener. Ask again on the round 3 page, in one list.
Round 2's decision 1 (tight shot sharpness) is answered: keep as built.

## State
Round 2 page: http://localhost:8847/index.html (`review_server.py 8847 /Volumes/Extreme/_edit_work/ro06/round2`). VLC copy
`Videos to Review/Work Out At Home LFC R2 - first minute.mp4`: replace it with the R3 file, do not keep both. Recipe:
`/Volumes/Extreme/_edit_work/ro06/recipe/` (mirrored in the skill's `reference/ro06/`); `page2.py` is the page generator to
copy for round 3 (first minute on top, AI frame pairs directly under it, What changed, What I decided, open decisions, one
reply box). Open risks for the full film (leans inside tight shots, one 24 s hold) are listed in the round 2 handoff.
Not run yet: delivery gate, watch pass, independent review, edit sheet (they need the complete film).

## Starter prompt (Claude, Opus 5.5, high)
> Read `Handoffs/handoff-20261008-ro06-round3-first-minute-ai-clips.md` and execute it with /longform-edit. This is RO-06
> "How To Work Out At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R3`. In the first
> minute: swap the jump rope clip for me jumping rope smoothly at full speed, and make the equipment shot at 20 seconds a
> tighter crop that pans from the kettlebell to the right (upscale it if needed). Then make start and end frames for four
> AI clips: two at 31 seconds of me as a trainer in a home gym with a fat, whiny loser making the excuses (his lips synced
> to my impression), one at 39 seconds where I slap him, and one where I have him doing simple home workouts with this
> equipment. Use the Codex subscription to generate the images. Cropping, colour and audio are approved, do not change
> them. Show me the new first minute with the frames in place, then stop.
