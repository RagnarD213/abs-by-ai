AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `How AI Real Abs AD R4`.

# RA-05 "How AI Can Get You REAL Six Pack Abs": round 4 (Dan answers the whole 9:16, then delivery)

**Written 2026-10-14 by the round 3 session (Claude, Opus 5.5).** Round 3 page: http://127.0.0.1:8838/ (work dir
`/Volumes/Extreme/_edit_work/ra05/round3/`, page files in `round3/review/`, served by `_shared/review_server.py`, survives
restarts). Recipe and five lessons: `.claude/skills/ad-edit/reference/ra05/round3/README.md`. Fire it when Dan has answered.

Read: this file; that README; `/ad-edit`; `.claude/skills/_shared/VIDEO-RULES.md` (first sections); round 1's delivery list
(`handoff-20261013-ra05-round2-after-dan-review.md`, "Next action" item 5). Build round 4 in a new
`/Volumes/Extreme/_edit_work/ra05/round4/` (copy round 3, as rounds 2 and 3 did). Never overwrite `round3/review/`.

## What round 3 showed Dan (three decisions on the page)

1. **The whole 9:16**, 58.36 s, 1,749 frames, `draft_9x16.mp4` (also `Videos to Review/How AI Real Abs AD R3 - whole 9x16.mp4`).
2. **The couch clip moving** (film 3.47 to 7.91 s): shot A = Veo take A2, its first 2.30 s, HARD CUT at film frame 173 (on
   "six-pack abs in real life"), shot B = take B5, its first 2.14 s. Natural speed. The phone picture in both shots is the
   approved frame's own picture laid into the tracked phone (`lockscreen.py`; Veo animated and degraded it in every take).
3. **The vertical body scan** (film 25.99 to 29.96 s): A0044 cropped full height (608 x 1080 at x 653, from source 1.033 s),
   enlarged 1.78x, four Soft Blue notes (two top, two bottom) on cyan lines traced over the clip's own lines.
   Fallback offered, not made: a Codex 9:16 frame of the scan scene + one Veo take (about $0.40), frames to Dan first.

Also done without asking (on the page under "What I decided"): **the B0435 physique-poses cutaway was removed** (Dan's standing
rule of 2026-10-14, never a shot of him just standing around); he is on camera 45.45 to 50.52 s (FAR). Cards cover 38.5 %.

## Checks already passed on round 3's file (so round 4 does not redo them unless the picture changes)

Audio gate PASS on `draft_9x16.mp4` (stamp names its sha256; `--untreated mix.wav.audio_untreated.json`). Captions after
30 s match a fresh Replicate transcript word for word. End hold: mouth closed 2 frames after "real.", smile held to the last
frame. Hold edges (`s04b_holdstart.py`, 25 of 25): hair 77 to 113 px from the top, face 14 to 77 % of the width. Joins after
30 s and around both new items: clean size changes, no stray frame. Self-change map on both couch shots: nothing outside him
changes. Independent reviewer: both items PASS; its notes (phone face, scan frames 0 and 5 to 9) were fixed and re-reviewed
(`check3/REVIEW-takes-r3.md`, `check3/REREVIEW-r3.md`). Not run: `piccuts.py decide` (the cut and every join are unchanged
since round 2: `cut.json` 3e7410a0); `junk.py` on the final file was queued behind other sessions' builds; run it in round 4.

## Next action

1. Record Dan's reply (his words, per decision, with hashes) in `round4-plan/decisions.json`. Re-hash the files below.
2. If he asks for changes, make only those, then show only what changed (VIDEO-RULES later-round timestamps rule: a short
   list with exact timestamps and watch ranges). If the scan reads soft to him, make the fallback frame first and stop.
3. When he approves the whole 9:16, set Edit Queue `finalized` (his words only), then deliver, all of it owed:
   - **the 16:9 from the same edit** (`ra01lib.Aspect("16x9")`; lower thirds and plates in their 16:9 layout, models `from_plan.py`,
     `ad13-r2/h16x9_full.py`). ⚠ Two items have no 16:9 version Dan has seen: the couch clip is native 9:16 (put it in a
     plate like the app recordings, lesson 61, never crop it to 16:9) and the scan should use the original 16:9 A0044 as round
     1 did (its own readable callouts). Show both as stills on their 16:9 frames before the full 16:9 render if either looks
     like a new layout.
   - `junk.py` on both final files; the edit sheet (16:9) + `validate.py`; `deliver/gate.py --format ad9x16` and `ad16x9`;
     the watch pass + judge; one fresh independent reviewer on both files; `audio_gate.py` with the A/B clip.
   - delivery folder `Claude Ad Videos/how ai can get you real six pack abs - RA-05/` (9:16 master, 16:9, notes, recipe).
   - `queue.py set RA-05 delivered` plus the artifact db; clip library `add --used-in "RA-05"` for the couch clip (A2 + B5
     locked, with the START/END frames) and the vertical scan card; `roll_sidecar.py mark-used`.
4. Then the ad goes to `/ad-setup` (a separate task): it is an AD, unlisted YouTube + Google Ads only.

## Files (work dir `/Volumes/Extreme/_edit_work/ra05/round3/`, sha256 first 16)

| file | sha256 |
|---|---|
| `draft_9x16.mp4` (the reviewed whole ad) | fdab85b0c9537e09 |
| `review/How AI Real Abs AD R3 - whole 9x16.mp4` (faststart copy of it) | 28349ea37fc0b464 |
| `picture_9x16.mp4` | 7723335e1b36ee13 |
| `mix.wav` (unchanged from round 2, frame-locked) | 3857ef27e0e39167 |
| `cut.json` (unchanged) | 3e7410a0fb7d2a2e |
| `beats.json` (no poses card) | 50b393ee5c17ba36 |
| `timeline_9x16.json` | 80a8e335e3990a0e |
| `cards_9x16/couch.mp4` | 03c487476f9de206 |
| `cards_9x16/scan.mp4` | 1fd25fe2360a6128 |
| `cards_9x16/open.mp4` (approved round 2) | ad11958532e154b4 |
| `cap_9x16/captions.mov` (unchanged) | c29ac42adebd3d17 |
| `motion/A2.mp4`, `motion/A2_locked.mp4` | 2b6fa950fd941f63, 3598d19a1a0399f6 |
| `motion/B5.mp4`, `motion/B5_locked.mp4` | e26dce6cc92230c7, d53e92bbb873526e |
| `hf9/manifest.json` (unchanged) | 279afccecef1ce88 |
| `review/index.html` | 0be0fb80cd553a74 |

Cost ledger (`motion/ledger.json`): **$3.20 of $10** (eight Veo 3.1 Fast 4 s takes: A1 to A3, B1 to B5). Codex subscription:
3 images (round 2). Replicate transcript: under a cent.

## Risks, stated plainly

- The 16:9 needs two layouts Dan has not seen (couch clip in a plate, scan in its original 16:9 form).
- The scan's first quarter second shows the clip's own bright scan glow along the lines, and one frame (card frame 3) a
  short spark ahead of a growing line. Judged invisible at speed by the editor and the reviewer.
- Shot B keeps a thin dark beard edge along his jaw; it is in Dan's approved END frame.
- The machine ran at load average 150 to 200 from other sessions; a full 9:16 picture render took about 18 minutes.

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `How AI Real Abs AD R4`. Read `Handoffs/handoff-20261014-ra05-round4-delivery.md` and run round 4 of
> RA-05 "How AI Can Get You REAL Six Pack Abs" with /ad-edit. My answers to the round 3 page are: [paste]. Apply any change I
> asked for and show me only what changed; once I have approved the whole 9:16, build the 16:9 from the same edit, run every
> delivery gate and the independent review, deliver to the ad folder, update the queue and the clip library, then stop.

**Recommended model and effort: Opus 5.5, high.** Delivery is gate-heavy, mechanical work plus one new 16:9 layout pass.
