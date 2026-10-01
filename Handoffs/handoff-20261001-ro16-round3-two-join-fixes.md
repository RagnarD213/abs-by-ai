# RO-16 round 3: fix two joins, keep everything else identical

**Job:** RO-16 "If I Had Belly Fat, Here's How I'd Lose It In 90 Days", organic long-form, 9/23 roll C1710.
**Written:** 2026-10-01 by Claude (Opus 5.5) after Dan watched the round-2 full film.
**Model:** Claude Opus 5.5, medium (two bounded edits to a locked recipe, then the standard checks).
**Sidebar name:** `If I Had Belly Fat LFC R3`.

Dan on round 2: *"Overall, this video is looking perfect except for those two little revisions that we have to make... Just fix
those two transitions and keep everything else in the video the same."*

## Read first
- `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/CUT-CONTINUITY-QC.md`, `Handoffs/video-editing/00-RULES.md`.
- Dan's words: `/Volumes/Extreme/_edit_work/ro16/round3-plan/decisions.json`.
- Round-2 record: `claude edited long form content/09 - If I Had Belly Fat, Here's How I'd Lose It In 90 Days/notes-RO16.md`.

## The locked film (do not change anything outside the two joins)
- Master: `/Volumes/Extreme/_edit_work/ro16/round2/RO16_MASTER.mp4`, sha256
  `3cf07a6c0d8c86865b7b274f0629f50c167443805d9101dcfa1056b1abb12a67`, 21,871 frames, 12:09.76. Re-hash it first.
- Recipe (run the SSD copy): `/Volumes/Extreme/_edit_work/ro16/recipe/`. Git copy `.claude/skills/longform-edit/reference/ro16/`.
  Chain: `edl.py` -> `shots.py` -> `assemble_audio.py` + medium.en ASR -> `words_out.py` -> `resolve.py` ->
  `build.py range 0 <end> round3/RO16_MASTER.mp4` -> `finish_chain.sh` (edit its `round2` paths to `round3`).
- Round-2 state to diff against: `round2/plan_resolved_candidate2.json` is NOT final; use the current `plan_resolved.json`,
  `shots.json` and `edl.json` (copy all three to `round3-plan/` as the "before" set before touching anything).

## Fix 1: the repeated "Most guys" at 5:00 (output 4:59.6 to 5:01.4)
Dan: *"There's a small amount of junk footage included where I repeat the words."*
- In the source he says "Most guys" (571.06-571.66), stalls, then says "Most guys do it the opposite way" (572.90-574.54).
  Whisper folded the second "Most guys" into one long "do", so both copies are in the film: piece `s3a` ends at 571.97 (first
  copy) and `s3a2` starts at 572.84 (second copy). Lav energy confirms two matching two-syllable bursts.
- Fix in `recipe/edl.py`: end `s3a` after "seven days a week." (word ends 570.44; hand-set the out-point from the energy profile,
  about 570.60, keeping the natural tail and no clipped "k"). Leave `s3a2`'s in-point at 572.84 so the fluent second take
  carries the whole sentence. Update the row's text and "why".
- The join stays a T2 to W2 framing cut (`s3a.0` T2, `s3a2.0` W2). Confirm on native frames it is not a same-size jump.
- After `words_out.py`, check the words around the join read "seven days a week. Most guys do it the opposite way." once; fix
  the word list by hand if Whisper folds "Most guys" again (the SRT is built from it).

## Fix 2: "health benefits." clipped at 11:40 (output 11:40.10)
Dan: *"The 'non-weight-loss health benefits' are very, very slightly cut off. I want you to work on that transition and make that
smooth."*
- Piece `s8b` ends at source 1072.905. The final "s" of "benefits" is the sibilant at about 1073.02-1073.12 (broadband, high
  frequency), so it was cut off, and round 2 then added a 70 ms tail fade there (`TAILFADE["s8b.0"]` in `build.py`), which made
  it worse. That was my misread of the burst as a lip noise.
- Fix: hand-set `s8b`'s out-point past the "s" (about 1073.22, where the level is back to room, near -65 dB) and delete the
  `"s8b.0"` entry from `TAILFADE`. Then check the next piece's start: `s8c` begins at 1086.99 but Whisper puts "If" at 1086.68,
  so measure the onset of "If" and move the in-point earlier if the word's start is clipped.
- "Make that smooth": listen to the rebuilt join in context (about 5 s each side). The picture join is W2 to T2. If it still
  feels abrupt, give it a natural beat (0.3 to 0.4 s of room between "benefits." and "If"), not a crossfade or a sound effect.
- Leave the "carbs." tail fade at 9:43 (`"s6d.0"`) alone. Dan watched it and did not flag it.

## What must come out the same
- Both fixes move the timeline (fix 1 removes about 1.4 s after 5:00; fix 2 adds about 0.3 s after 11:40). Every item after
  each join must keep its exact position relative to Dan's words. After `resolve.py`, diff against the "before" set: the only
  differences allowed are uniform time shifts after each join. Any item that changes length, order or snap target is a
  finding; fix the cause, do not accept it.
- Shot count stays 43 and every shot keeps its framing (`shots.py` assigns framing by index plus the `s5d.0` override).
- Prove it on pixels: compare the new master to the round-2 master frame by frame with the two offsets applied. Only the frames
  at the two joins may differ beyond re-encode noise. The round-2 reviewer did this for candidate 3; do the same here.

## Checks on the exact new file
Audio gate; watch pass; `haircheck.py`; `_shared/cut/junk.py` (confirm the "Most guys" repeat is gone); SRT and chapters
regenerated (`finish.py`; chapters shift after 5:00); one fresh `ra-reviewer` on the complete file, told to verify the two joins
by frames and audio levels and to confirm nothing else changed; then `watch.py --judge` and `gate.py --format longform` (plan now
carries `banned_source`). Expected gate reading: the same four known rows as round 2 (see notes-RO16.md); anything new is a
finding.

## Deliver
Same folder, `claude edited long form content/09 - If I Had Belly Fat, Here's How I'd Lose It In 90 Days/`, as
`... | claude round 3 | 16x9 | RO-16.*` (master, REVIEW 540p, `.srt`, chapters, audio A/B, both stamps); add a round-3 section
to `notes-RO16.md`; copy the changed recipe files to the delivery folder and the git copy. Upload the 540p to Drive folder
"RO-16 If I Had Belly Fat - review" in a `round 3` subfolder (anyone with the link) and send Dan the review copy with a short
"What I decided" list. `queue.py set RO-16 delivered`, mirror to the Edit Queue page, update the board entry.
After Dan finalizes: register A01 and the new stock inserts in the clip library and `roll_sidecar.py mark-used` for every C1710
range in `edl.json` (still owed from round 2).

## State and risks
- The shared checkout cannot push (board: "Shared checkout cannot push"). Commit locally; do not pull, rebase or stash.
- Machine cap: two video builds at once. The delivery gate took 107 minutes under load in round 2.
- Cost ledger: $2.70 of the $5 cap; this round needs no generation.

## Starter prompt
> Read `Handoffs/handoff-20261001-ro16-round3-two-join-fixes.md` and do RO-16 round 3: remove the repeated "Most guys" at 5:00
> and fix the clipped "health benefits" join at 11:40, keeping everything else identical. Rebuild, prove nothing else changed,
> run every check and an independent review, deliver, and send me the review copy. Name this session `If I Had Belly Fat LFC R3`.
