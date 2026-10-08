# RO-06 "How To Work Out At Home On A Budget": round 3, after Dan reviews the rebuilt first minute

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R3`.
Written 2026-10-08 by Claude (Opus 5.5) at the end of round 2. Replaces `handoff-20261008-ro06-round2-first-minute-revisions.md`
(executed). The full-film steps are still in `handoff-20261008-ro06-round1-dan-review.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md`, `/Volumes/Extreme/_edit_work/ro06/round2-plan/decisions.json`.

## What round 2 delivered (Dan has NOT answered yet)
- Review page: http://localhost:8847/index.html (restart: `python3 .claude/skills/_shared/review_server.py 8847 /Volumes/Extreme/_edit_work/ro06/round2`).
- First minute: `/Volumes/Extreme/_edit_work/ro06/round2/first-minute/DRAFT - RO-06 round 2 - first minute.mp4`,
  sha256 `7d02163e44ef7d1395c91ef07a16dbc5dd1436aead2d930141f39f33981edc41`. VLC copy: `Videos to Review/Work Out At Home LFC R2 - first minute.mp4`
  (replace it after a re-render; delete it when Dan finalizes the video).
- Order now: tight 0 to 3.7 s, three clips to 10.8 (ab wheel `B0436@2.0`, jump rope `B0447@1.0`, kettlebell `B0439@0.5`), wide to
  12.85, tight with the $58 lower third (now on "So this is great", 12.96 to 18.1), equipment clip, medium, tight, medium, tight,
  wide at 46.7 ("the stuff in front of me right here"), tight with G02, medium at 58.96 (he leans and points).
- Checks run: audio gate PASS; the audio is sample-identical to the approved round 1 file (decoded md5 equal); hair at least
  26 px from the top on all 210 samples; every cut is a size change (strip `round2/qc/fm_joins.jpg`); no hold over 22 s here.
- Not run (they need the complete film): delivery gate, watch pass, independent review, edit sheet.

## Locked (do not reopen)
Audio and colour (Dan, round 1, words in `decisions.json`). Soft Blue Light graphics and templates.

## Waiting on Dan: 8 decisions on the round 2 page
1 tight shot sharpness (new) · 2 hair at the top edge on 9 rolls · 3 length · 4 AI product pictures · 5 jump rope "$10" vs "$9" ·
6 music bed · 7 app demo treatment · 8 confirm no AI opener. Also listed for him to overrule: the medium size as the third
size, the 2 s wide after the clips, the lower third over his shorts on the tight shot. Do not infer anything from silence.
When he replies, record his words and the reviewed hash in `round3-plan/decisions.json` before building.

## How the framing works now (code in `recipe/build.py`, copied to the skill's `reference/ro06/`)
- Three sizes: `X` tight (`T2` crop, about 2x), `T` medium (1.5x), `W` camera frame. `all_segments()` solves the whole film:
  wide rolls prefer X, medium rolls their 1.3x T, close rolls (C1580, C1581) the camera frame; a real join needs sizes at least
  1.2x apart; one take at one size shares one crop; no size holds over 22 s; a shot is split where a full-screen clip starts
  inside it, so the picture can come back at another size (segment key `shot+c`).
- First-minute picks are in `OVERRIDE`. Extra cut points come from `split_shot.py SHOT T_LO T_HI` (picture only; `voice_shots()`
  merges them back so approved audio never moves).
- `build.py segs 80` prints the solution, the jumps and the longest holds. `fm_qc.py` and `hair_fm.py` make the QC pictures.

## Open risks for the full film (round 3 or 4 work, not started)
- **Leans and points.** The per-shot `active` flag misses a one-second lean inside a long shot (found by eye at 61 s and 70 s:
  he bends and points at the equipment). Before the full render, scan every X segment for head drop or sideways travel
  (`hair_fm.py` rows carry top, left, right per quarter second), then split and set those sentences to T or W.
  `exc3.0r3` (69.4 to 76.2, "With this stuff right here") is one: he bends at 70.0 under lower third G03.
- One hold of 24.4 s at 742 s (12:22) still exceeds the 22 s rule; W is 28 % of the film mostly from the close rolls and
  `active` shots. Look at `build.py segs 1100` and the stills before rendering.
- Lower thirds on the tight shot sit over his shorts. If Dan dislikes it, give lower-third shots the medium size
  (`options()`: add a cost to X when `sg["lt"]`).
- Hair at the top edge on rolls C1567 to C1574 is in the source (decision 2).

## Costs
$0 metered in rounds 1 and 2. Six Codex stills on the subscription (round 1). Cap: $5 per video for AI clips.

## Next action
Wait for Dan's reply. Then: apply his first-minute notes if any (re-render only the first minute, replace the VLC copy), record
decisions, and once nothing is pending build the full film per the round 1 handoff's full-film steps, starting with the
leans scan above. Recommended: **Claude Opus 5.5, high.**

## Starter prompt
> Read `Handoffs/handoff-20261008-ro06-round2-dan-review.md` and execute it with /longform-edit. This is RO-06 "How To Work
> Out At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R3`. My answers to the round 2
> page are below. Record them, fix anything I flagged in the first minute, then build the full film and show it to me.
> [paste the reply box from the round 2 page here]
