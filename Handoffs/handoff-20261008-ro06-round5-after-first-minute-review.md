# RO-06 "How To Work Out At Home On A Budget": round 5, act on Dan's reply to the first minute with the AI clips moving

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R5`.
Written 2026-10-08 by Claude (Opus 5.5) at the end of round 4. Replaces `handoff-20261008-ro06-round4-ai-motion-first-minute.md`
(executed). The full-film steps stay in `handoff-20261008-ro06-round1-dan-review.md`; its open risks are in
`handoff-20261008-ro06-round2-dan-review.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md` (round 4 notes at the end),
`/Volumes/Extreme/_edit_work/ro06/round4/round4-record.json` (takes, trims, hashes, costs, checks).

## Where it stands
Round 4 built the first minute with A1, A2, A3 and A4 as real moving clips and showed it to Dan. **He has not replied yet.**
- Page: http://localhost:8849/index.html (restart: `python3 .claude/skills/_shared/review_server.py 8849 /Volumes/Extreme/_edit_work/ro06/round4`).
- File: `round4/first-minute/DRAFT - RO-06 round 4 - first minute.mp4`, sha256
  `8d0c592092943e7f0f2b97343021205e854ef55f201acb1cce82442193c12099`. VLC copy: `Videos to Review/Work Out At Home LFC R4 - first minute.mp4`.
- **Start of round 5: put Dan's exact words in `/Volumes/Extreme/_edit_work/ro06/round5-plan/decisions.json`** (per item: verdict, his
  words, hashes). Do not infer anything from silence.

## Locked by Dan (do not reopen)
- Cropping, colour, audio, the tight open, the three-clip opening, the jump rope clip `B0448@4.0`, the panning equipment shot.
- The start and end frames of all four AI clips (A3: the round 4 left-hand pair). Hashes: `round4-plan/decisions.json`.
- Not locked yet: the four clips in motion. That is decision 1 on the round 4 page.

## What round 4 put in the film (picture only; the voice track is bit-identical to round 2)
| ID | on screen | take, used from | notes |
|---|---|---|---|
| A1 | 31.12 to 33.54 | `round4/motion/A1-t1.mp4` from 1.50 s, as `A1-final.mp4` | lips synced to Dan's impression, client's face only |
| A2 | 33.54 to 35.80 | `A2-t1.mp4` from 1.70 s, as `A2-final.mp4` | wallet opens and the facepalm land on "money"; lips synced |
| A3 | **38.87** to 41.16 | `A3-t1.mp4` from 1.341 s | the take has two slaps; the film uses the second. Hit on "destroy" (39.40). Starts 0.312 s later than the placeholder (`late=0.312` in `plan.py`) |
| A4 | 41.16 to 46.68 | `A4-t1.mp4` from 0.30 s | two push-ups, whistle then fist pump |

Things Dan was told and may answer: A3 can show both slaps with no new generation (`late=0`, `src @0.115`); the A3 hit is a
flat hand on the side of the face, not a glancing cheek slap; the tank top shows the shield only in A1 and A2 and the
shield plus "Abs by AI" in A3 and A4 (as in the approved frames); the M of "gym" is loose in the lip sync.

## If Dan asks for a clip change
- New take: edit `round4/motion/<ID>.txt`, then `python3 recipe/gen_motion.py <ID> <ID>-t2` (hash-checks the approved frames; one
  prediction at a time). Read it with `recipe/clipsheet.py` at full size, then decide at playback speed (VIDEO-RULES, 2026-10-08).
- Lip sync (A1, A2): `recipe/lipsync.py <ID> <take> <offset> <tag>`, then **always** `recipe/syncfix.py <tag>.trim.mp4 <tag>.mp4
  <client face box> <ID>-final.mp4`: the sync model also moves the trainer's mouth. Prove it with `recipe/syncdiff.py`.
- Trim, never stretch. Put the take in `plan.py` (`src=[path@offset]`), `resolve.py`, `build.py range 0.0 62.9963 <out>` in a new
  `round5/` folder, then the same checks as round 4: the two audio md5s (`fbf7798364cf1f0592144e03827a3b8a`,
  `351d8f6d7a42a63ae44c42c9d46db45a`), crop and source frame against round 3's `build.json` (0 differences), `fm_qc.py`,
  `hair_fm.py`, the audio gate. Materially different frames need his approval again before motion.
- New page from `recipe/page4.py`; replace the VLC copy.

## If Dan approves the clips and answers the open decisions
Build the full film per `handoff-20261008-ro06-round1-dan-review.md`, then run what has not been run yet because it needs the
complete film: the delivery gate, the watch pass, one independent review, the edit sheet.

## Still open (Dan has not answered; do not infer from silence)
Hair at the top edge on 9 later rolls · length (trim repeats or keep 17:39) · AI product pictures in the price cards ·
jump rope "$10" vs "$9" · music bed · app demo treatment · confirm no AI opener. They are decisions 2 to 8 on the round 4
page, with recommendations. The full film waits for these.

## Budget
$5 per video for AI clips, retries included. **Spent: $2.43** ($0.24 Topaz upscale, $1.80 Veo 3.1 Fast for 18 s, $0.39 two lip
syncs). Left: $2.57. A new take is $0.40 (A1, A2, A3) or $0.60 (A4), plus about $0.20 of lip sync on A1 or A2. Past $5: stop and
tell Dan the number and the reason first.

## Notes for later steps
- The upload's AI flag is true (`/video-setup`): the film contains realistic AI footage.
- When the film is finalized: register the four AI clips in the clip library, delete this video's copies in `Videos to Review/`,
  and stop the page services (`review_server.py 8848 --remove`, `8849 --remove`).
- An outside playback check (Gemini, one frame a second) called the lip sync unconvincing; the frame read of the finished
  file shows the lips closing on the M sounds. Dan's eye decides. `round4/qc/gemini_review.txt`, `round4/qc/lipsync_closures.jpg`.

## Next action
Record Dan's reply, then take the matching branch above. Recommended: **Claude Opus 5.5, high.**

## Starter prompt
> Read `Handoffs/handoff-20261008-ro06-round5-after-first-minute-review.md` and execute it with /longform-edit. This is RO-06
> "How To Work Out At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R5`. My reply to the
> round 4 page is below. Record it, make any clip changes I asked for and show me, or if I approved everything and answered
> the open decisions, build the full film.
>
> [paste your reply from the round 4 page here]
