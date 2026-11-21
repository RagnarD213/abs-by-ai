LFC (long-form content). Task name for this session: `My First Spray Tan LFC R4`.

# RO-19 "My First Spray Tan": round 4, Dan's two final revisions

**Written 2026-10-13 by Claude (Opus 5.5), after Dan reviewed the round 3 full film.** Job doc: `Handoffs/video-editing/RO-19-my-first-spray-tan.md`. Rules: `.claude/skills/_shared/VIDEO-RULES.md` (read in full), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/_shared/CUT-CONTINUITY-QC.md`. Recipe and traps: `.claude/skills/longform-edit/reference/ro19/README.md` (the "Round 3" section lists the order of scripts and every trap this film paid for). Earlier round: `Handoffs/handoff-20261012-ro19-round3-full-film.md`.

## Round 4 is built and waiting for Dan (added 2026-10-13, end of the round 4 session)

- Film: `/Volumes/Extreme/_edit_work/ro19/round4/film/RO-19 round 4 - full film.mp4`, 18:46.46, 33,760 frames, sha256 `b4b309991b414674e2469fadad7f9b6fb3352ee61f5b02654d1567bbf5b317d8`. Page: http://127.0.0.1:8867/ (folder `round4/`). VLC copy: `Videos to Review/My First Spray Tan LFC R4 - full film.mp4` (the two R3 copies are deleted). Hashes: `round4/round4-hashes.sha256`.
- Both changes are in: P02 is his picture (0:48.6 to 0:55.1); the false start is out (the join is at 9:05.545, 63 frames removed, everything after is 2.102 s earlier). Nothing else differs from round 3 (every frame compared).
- Checks on that file: audio gate 12 of 13 (tone); delivery gate 31 pass, 8 fail (round 3's seven plus `audio:click_at_joins`, which flipped on the gate's random baseline; the two flagged cuts measure the same in round 3); watch pass 664 of 664 judged, 0 open; independent review `round4/film/ROUND-4-REVIEW.md`: SHIP, no defects; scene check 69 of 69; edit sheet valid. One note told to Dan: a 7 ms left/right encoding blip at 15:29.7.
- Not done, waiting for his "final": everything under "When Dan says the film is final" below. Use the round 4 film and `round4/` paths there (stop page service 8867 too). The recipe's "Round 4" section in `.claude/skills/longform-edit/reference/ro19/README.md` has the order and the traps. `round4/film/review4/` is 6.5 GB of the reviewer's evidence: clear it at finalization.
- If he asks for another change: build in `round5/` on a new port, never into `round4/`.

## Where it stood before round 4

- Round 3 film: `/Volumes/Extreme/_edit_work/ro19/round3/film/RO-19 round 3 - full film.mp4`, 18:48.56, 33,823 frames, sha256 `2031c3e31eb5f3f2ea7620182134e29583417ba7a0c8517969a4b7056bdb880d`. Page: http://127.0.0.1:8866/ (folder `round3/`, do not overwrite; build in `round4/` on a new port, 8867 if free).
- Dan: "Those are the only revisions." Everything else in the film is approved. His words and hashes: `round4-plan/decisions.json`. Re-hash `round3/round3-hashes.sha256` (42 files) first and record expected against actual.
- The plan is built by `recipe/plan_patch_r3.py` from the round 2 plan (never `resolve.py`). `build._PIN` plus the named `OVERRIDE` lines hold every shot's size. `build.MANIFEST` is `hf/manifest.r3.json`. The timeline already carries one shift (`round3-plan/timeline_shift.json`, +215 frames at 623.656 s).

## The two changes

| item | his words | do |
|---|---|---|
| Photo at 0:48 (P02) | "the picture at 49 seconds, change it to this picture here." | Use the picture he sent: `round4-plan/dan-pick-P02.jpg` (804x978, sha256 `9a85df83...6aa6`). It is Photos asset `77D35A5F-E3CD-4877-B8C7-77485F19760C` (1 April, 14:50:50, 2865x3486; correlation 1.0 with his attachment). The full-size file is on disk: `~/Pictures/Photos Library.photoslibrary/originals/7/77D35A5F-....heic`. Export with `sips`, then `exif_transpose`. Crop for the card the way the current one is cropped (head to just below the hands, 4:5, `photocrop19r3.py`: head top from the person mask, navel row read off a ruled close-up, 0.06 above the hair, 0.45 below the navel), so his abs read at the same size. Save as `photos/pale4_single.jpg`, render `gfx/r4/P02.mp4` (`PAIRS_OUT=gfx/r4 pairs.py P02`). It is his explicit pick: use it, do not swap it. It is a smaller same-second copy in his library, so it may be an edit of frame `5AC50078`: if it is tinted against that frame, say so in one line on the page and still use his picture. |
| Repeat at 9:07 | "I say 'in my normal life,' then say 'in my normal life' again. Cut that so that it is smooth... No repeated junk footage there." (He first typed 0:07, then corrected it: "That repeated footage is at 9:07.") | A false start is in the cut. Film 9:05.5: "In my normal life, I'm" (shot `water2.0`, roll 837.80 to 839.81), a pause, then the restart "in my normal life I'm in the water all the time, so I'm not entirely sure it would hold up as good as this in my normal life." (shot `water2.1`, from roll 840.41). Drop the first attempt: 60 frames. The sentence then starts on the restart. The sentence itself still ends on "in my normal life": that is how he said it and it stays; say so under What I decided. |

## How to make the cut at 9:07

1. Prove it before cutting. Whisper stretched three words across the restart ("I'm" 546.6, "the" 547.9, "water" 549.1), so no transcript shows the second "in my normal life". The lav does: speech 837.9 to 839.4, silence to 840.5, speech again from 840.6 (0.1 s envelope). Transcribe roll 837.0 to 847.0 alone with word times and print the envelope; confirm what is said from 840.4 on.
2. `recipe/edl.py`, piece `water2`: its start phrase "In my normal life, I'm in" matched the false start. Give it a measured in point on the restart (9th field, roll-local, about 0.1 s before the restart's onset) and say why in the comment. Re-run `edl.py` and confirm only `water2` changed (the round 3 README has the ten line check that every piece ENDS on its own text; run it for starts as well).
3. Shots: do it surgically, as round 3 did for `pros.0r3`. Remove `water2.0` from `shots.json`, set `water2.1`'s start to the new in point, move every later shot earlier by the frames removed, assert the shots still butt. Then `words_src_out.py`, and check every later word moved by exactly that amount.
4. The shift list. `plan_patch_r3.py` applies one shift (`late()`). Make it a list: first +215 frames at 623.656 s (round 2 timeline), then the new negative shift at 545.54 s. Copy the script to `plan_patch_r4.py`, keep it idempotent from `round3-plan/plan_resolved.round2.json`. The lower third manifest moves with it (`hf/manifest.r4.json`; point `build.MANIFEST` at it).
5. The swimmer clip `Cc11` (9:05.5 to 9:10.1) covers both attempts, so no picture join shows. After the cut it must still end where it ends now by the words (after "all the time", before "so I'm not entirely sure"): shorten its slot by the frames removed. Check the clip is long enough and its lower third neighbours are untouched.
6. `build.py segs`: no jumps, every shot at its round 3 size and crop (compare with `round3-plan/segs_r3.txt`).
7. Listen check on a 20 s `render_range` around 9:05 before the full render: the sentence is said once, no clipped word at the new in point, level steady.

## Then the film, in order

1. `ps` first (two-build cap: other sessions render on this Mac).
2. Before the full render: 30 s test renders of both changed stretches (`render_range(..., audio=False)`) and `hyperframes/checks.py --film-t0` on them.
3. Full film to `round4/film/` (`round3_19.py` copied to `round4_19.py`; same bed, same voice B2). Then the chain (`finish_chain19r3.sh` copied and pointed at round 4): audio gate, transcript, `finish19r3.py` (captions with the proofread list, chapters, label references, plan), watch pass, hair, graphics checks. `scene_check19.py`.
4. Carry the verdicts: `carry19r3.py` against `round3/film` with `logs/findings.json`. The cut moves the timeline, so match strips by SOURCE content, not film time: shift the judged render's boundary times by the frames removed before matching, and compare frames with the same offset. Only what truly changed (P02, the 9:05 stretch) goes to a fresh `ra-reviewer`, with the same brief shape as `ROUND-3-REVIEW-3.md`. Merge, `watch.py --judge`.
5. Negative-events scan for the new master, edit sheet (the shadow build folder trick in the README, with both shifts), delivery gate. Expect the same seven rows to fail as round 3 (tone stamp, hair x2, burned-caption false alarm, coverage, three take joins, the 2:53 false start). Report them, tune nothing.
6. One page (later-round layout): the full film, the two changes with exact times and watch ranges, the photo old and new side by side, What I decided, one reply box. Copy the film to `Videos to Review/` as `My First Spray Tan LFC R4 - full film.mp4` and delete the two R3 copies of this video from that folder. Then stop for Dan. No upload, no queue.

## When Dan says the film is final (same session if he answers, else next)

- Register the new clips in the clip library (`clip_library.py add ... --status used-final --used-in "RO-19"`): A1, A2, A3 (the cut version), A4, A5, G1, G3, and the photo scenes if the library takes them. A5 is the default "talk to your doctor" clip (his round 1 ask). Then `clip_library.py sheet`.
- Regression corpus entries (`_shared/qc_corpus/`): the round 3 film as rejected-with-notes (his 9:07 words; the gate's `junk:repeated_take` row did not flag this restart, record that as the finding) and the final film as approved. Run `qc_corpus/run.py`.
- File the master, captions, chapters, edit sheet and recipe under `claude edited long form content/` (the RO-07 `deliver_r3.sh` is the pattern). Delete this video's copies from `Videos to Review/`, stop the 8863, 8865, 8866 and 8867 page services with `review_server.py PORT --remove`. Delete the board entry. Write the one Claude upload-and-setup handoff (it must say: "Use the Codex subscription to generate the images.").

## Not answered, and what to do

- Doctor clip as the library default: he raised no note on it and called these the only revisions. It stays in the film and is registered at finalization.
- The quiet music bed: not mentioned. Keep it as is.

## Cuts already applied (do not apply twice)

All in `recipe/edl.py`. Round 3 restored the end of piece `pros` (the Bryan Johnson sentence). Round 4 removes only the false start of `water2`. Pauses of 0.70 s or more were tightened once in round 1.

## Gate status, stated honestly

- Round 3 film: audio gate 12 of 13 (tone row, the known mismatch for voice B2); delivery gate 32 pass, 7 fail (listed above); watch pass judged, 0 open; three independent reviews, the last one SHIP. None of that carries to the round 4 file: it is a new render and every stamp is redone.
- Nobody has listened to the film by ear. Sound is cleared by measurement and transcription only.

## Cost ledger

- AI motion: $4.80 of $5.00 (`round3/motion/ledger.json`). Nothing new is needed.
- Images: none needed. If one is, use the Codex subscription.

## Model and effort

Opus 5.5, high.

## Starter prompt

```
My First Spray Tan LFC R4. Read Handoffs/handoff-20261013-ro19-round4-final-revisions.md and make my two final revisions to RO-19 exactly as it lists: the photo at 0:48 becomes the picture I sent (round4-plan/dan-pick-P02.jpg), and the false start at 9:07 comes out so the sentence is said once, with no repeated footage. Then the full film again with every gate, the watch pass and an independent review of what changed. One review page with a timestamped revision list, then stop for my reply. Use the Codex subscription for any images. Do not upload or queue.
```
