# Handoff: SL-05 Stop Deadlifting shorts, round 3: Dan's two revisions, then finalize (written 2026-10-01)

## EXECUTED 2026-10-01. Dan: "Both are finalized." Close-out done (queue finalized, clips A0138-A0142 registered, covers and setup handoffs written: `handoff-20261001-sl05-shorts-covers-codex.md`, `handoff-20261001-sl05-shorts-video-setup.md`).

## Earlier status: both revisions built, reviewed (SHIP) and gated (PASS 39/39); review copies sent to Dan. Only "Close-out" below is left, after Dan says finalized.
Short 2 as built: parent frames 123-188 (pull off the floor to lockout), then 207-224 (the X; the 18 identical still frames before it skipped), X at output 2.20 s. Reviews: `r2/review7/`. Gate logs: `gate/S2|S3/gate_out_r3.txt`.

## Goal
Apply Dan's two notes from his review of the round-2 copies, re-review only shorts 2 and 3, re-gate, send him the two
updated review copies, and finalize the batch. Nothing is uploaded or queued (the parent goes public Sun Oct 11; shorts
follow it; covers are a separate Codex task).

## Dan's review (2026-10-01, his words)
- **Short 2:** "I like how you include the AI-generated clip... I want you to cut the beginning where he's loading the
  weight. Just include the part where he's lifting the weight and where he gets X'd out at the end... Cut the part where
  he's loading. Include the X."
- **Short 3:** "I like the clip that you used in the beginning; however, it's a little bit cut off and unnecessarily
  cropped on the bottom. Show a little bit more of that clip so that the barbell is visible. It looks like it's cropped
  shorter than it needs to be."
- **Everything else:** "Everything else is looking good." Shorts 1, 4 and 5 are approved as delivered. The olive
  key-point bar, the draft titles and short 2's chin caption were all in front of him and he asked for no change.
  Title copy was never edited by him: treat the draft titles as accepted with "everything else is looking good", and say
  so in the delivery message so he can still change one.
- **This graphic set ends here** (see "Standing rule" below). Finish this batch in the current set.

## The two revisions

### Short 2: opening AI clip = the lift and the red X, no loading
Measured on the parent (`r2/look/s2x.jpg`, frames at 1.1-7.5 s): the AI clip is one shot from 1.068 s to its cut at
about 7.54 s. 0.00-1.07 is the man loading the plate (cut it). 1.07-4.0 he sets up, 4.0-5.5 he pulls, 5.5-6.9 he stands
with the bar, 6.9-7.5 the red X draws over him.
- Today: `segments.js` S2 piece 0 is 0.45-2.95 (audio "Stop doing deadlifts."), and `plan_shots.py` S2 shows source
  0.45-1.07 (loading) then 1.068 on, running 0.5 s past the join to hide Zeeshan's blur (card ends at output 3.04 s).
- Do: keep the audio exactly as it is. Replace both card rows with ONE whole-frame card row from output 0 to the same
  end (the row before `241.27`), picture not lip-synced: `('lcut:0.45:<src>', 'card', ..., w())` with `<src>` about
  4.47, so the card plays source 4.47-7.51 (the pull, the lockout, the whole X) and ends on the X fully drawn, just
  before his cut at 7.54. Check the exact last X frame and his cut frame with `r2/cutframe.py`-style differences; the
  card must not show a frame past his cut. If the X reads late against "Stop doing deadlifts." (the line ends at output
  2.2 s), start a little later in the source rather than speeding anything up.
- `style:static_run` / `change_rate` gate rows: the card loses one picture change (the 1.07 cut). If a row fails, the
  11.18 s MID to FULL step is still there; report rather than inventing a cut.
- Short 2's open watch item (caption on the underside of his chin, 0:44.0-0:44.2 and 0:46.5-0:47.0): Dan saw it listed
  and said everything else looks good. A fresh render gets a fresh watch pass; brief the reviewer that this item was
  shown to Dan and not objected to, and if it is recorded again, close it with `"disposition": "accepted_by_dan"` and
  his sentence "Everything else is looking good." (2026-10-01).

### Short 3: the opening AI powerlifter clip shows the barbell
- Today: `plan_shots.py` S3 row `F(8929)` is a K card cropped to source rows 0-745 (`cardCrop [0,1,0,0.69]`), a
  1080x419 strip. The crop exists to hide Zeeshan's burned pill (rows 771-896, visible to 303.30 s); the barbell and
  plates sit at rows ~700-950, so they are cut.
- Do: make it the WHOLE frame (`w()`, 1080x608 at y420). His pill is then whole inside the card, over the middle of the
  bar, so our olive bar must not also be on: end bar `S3-kp1` on the frame before the card (`F(8929) - 0.02`, the same
  handling as `S4-ex2`). Result: 0-2.2 s Dan full frame with our bar, then the whole AI clip with his own pill.
  Confirm no frame shows both, and that "*AI Generated" is whole.
- If the whole frame with his small pill reads worse than expected, the alternative is rows 0-1080 with our bar kept
  and his pill covered by nothing (not possible), so do not improvise: show Dan the still.

## How to build
`/Volumes/Extreme/_edit_work/sl05/build/` (scripts mirrored in `.claude/skills/shorts/reference/zeeshan-master/sl05/`).
`./build.sh S2 S3` → look at `r2/sheet.py S2|S3` → `./deliver_all.sh S2 S3` → `python3 r2/post_deliver.py S2 S3` →
`watch.py` → a fresh `ra-reviewer` each (judge + review; prompts as in round 2, scoped to the change) →
`watch.py --judge` → `r2/gate_all.sh r3 S2 S3` → `r2/review_copies.sh <names>`. Machine cap: two builds.
Do not touch S1, S4, S5 (gate PASS stamps are bound to their files). Do not run `r2/retime.py --apply`.

## Close-out
Update `Short-form video content/stop-deadlifting-SHORTS.md` (status table, the two changes). Send Dan the two review
copies. When he says finalized: `queue.py set SL-05 finalized` + artifact db, register Zeeshan's clips in the clip
library, delete the board entry, then write the Codex covers handoff (five options per short) and the `/video-setup`
handoff for after Oct 11.

## Standing rule recorded with this handoff (Dan, 2026-10-01)
SL-05 is the last shorts batch in the J2 / olive graphic set. Every NEW batch of shorts uses Soft Blue Light and the
HyperFrames templates. The first vertical and the first square made that way get a full approval round with every
asset shown to Dan before anything is built. Written into `_shared/VIDEO-RULES.md`, `shorts/SKILL.md` and memory
`shorts-soft-blue-hyperframes-from-now`.

## Recommended model
**Opus 5.5, medium effort** (two scoped picture changes on a working build).

## Starter prompt
> Read `Handoffs/handoff-20260930-sl05-round3-dan-review.md`, then make the two SL-05 revisions it describes (short 2:
> the opening AI clip shows the lift and the red X, no loading; short 3: the opening AI clip shows the whole frame so
> the barbell is visible), re-review and re-gate those two shorts only, send me their review copies, and tell me what
> is left before I finalize the batch.
