# RA-14 "The Cheat Code For Six Pack Abs": round 4, the full 9:16 (everything approved)

**AD (short-form, filmed).** Sidebar name for the next task: `Cheat Code Six Pack AD R4`.
Written 2026-10-14 after Dan approved round 3 (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-14-cheat-code-for-six-pack-abs.md`.
Read first: `.claude/skills/_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md` (step 5, the full video), the `/ad-edit` skill
(THE EDIT SHEET, THE DELIVERY GATE, Step 9.9 THE WATCH PASS, "RA-14 round 3 lessons"), `_shared/deliver/README.md`.
Dan's words and hashes per item: `/Volumes/Extreme/_edit_work/ra14/round4-plan/decisions.json` (repo copy:
`.claude/skills/ad-edit/reference/ra14/round4-plan/decisions.json`).

## What Dan approved (2026-10-14, page http://127.0.0.1:8819/)

Dan, verbatim: *"Everything is approved and looks good. Give me the handoff to build the full video in the next round."*

| item | approved |
|---|---|
| O2 | the 8-bit power-up opener as built, `round3/opener/O2.mp4` (fb479022004e9c07) |
| A1 | the Soft Blue analysis card, as the standard for every video, and its RA-14 timing (`round3/gfx/renders/A1.mov` 7cfa16597c98b7bd) |
| R1 | the recap list card, KEPT (option A, as shown with captions lifted above it) |
| L1 L2 L3 P1 T1 C1 | every graphic and clip as shown moving in context |
| first 30 s | the cut, the shot plan `beats_r3.json`, the captions, the voice `mix_bass_r3.wav` |

Nothing is pending. No AI motion is left to make. Spend $0 of $10. Do not re-ask any of these; a locked item is reopened only by Dan.

## Locked files (re-hash before touching; sha256 first 16, under `/Volumes/Extreme/_edit_work/ra14/`)

| file | hash |
|---|---|
| `cut.json` | 394e9127a580ce5c |
| `words_aligned.json` | b01781a5203792fb |
| `mix_bass.wav` (approved voice) / `mix_bass_r3.wav` (the same, frame-locked to 1512 frames) | a969e60b871ecd8d / 84d5c8831b57c2c3 |
| `beats_r3.json` (shot plan, 17 holds, every cut a size change) | 5ccd71cb0aad3d14 |
| `round3/opener/O2.mp4` | fb479022004e9c07 |
| `round3/cards/P1.mp4`, `T1.mp4` | 04b715ab683b7b00, 39a2f9bdf5b5f2ee |
| `round3/gfx/renders/` L1 L2 L3 R1 C1 A1 `.mov` | c524ab3668112f1f, 157e4667408fe2a1, f38794ec6d3f8e19, d25f9a2dddb922aa, f771c595440c1642, 7cfa16597c98b7bd |
| `round3/cap_9x16/captions.mov` | f3116b522e4ab7ce |
| `round3/work/picture_9x16.mp4` (all 1512 frames, picture only, built from the parts above) | 9da73ea7ea1447a9 |

⚠ **Do not re-render a locked part.** A parallel task (started 2026-10-14) is fixing the BT.601-under-BT.709 encode bug in
`_shared/adkit/cardlib.py` and the `ra01lib.py` copies. RA-14's O2, P1 and T1 were already encoded with the fix (this job's
`ra01lib.py`), so they are correct as they are. If anything forces a rebuild, re-hash it against the table and say so.

## Round 4: build, gate, review, deliver

1. **Re-hash** every locked file (expected vs actual into `round4/HASHES.json`). Build in `round4/`; never overwrite `round3/`.
2. **The master.** `round3/work/picture_9x16.mp4` is the full picture. Mux it with `mix_bass_r3.wav` (AAC 256k, +faststart) into
   `round4/the cheat code for six pack abs | claude | 9x16 | RA-14.mp4`. If the picture is rebuilt for any reason, use
   `python3 s86_assemble.py work` (it reads only locked parts).
3. **Music tail (carried, decided).** Two rests in the bed at 49.2 and 49.6 s dip 6 to 7 dB inside the final fade (RA-01's audible step
   was 15 dB). Listen to the last 2 s of the master. Smooth it with `s42_bed.py` only if it is audible, then re-make the mix, null-test it
   against `mix_bass_r3.wav` before 47 s (must be identical there), and record the choice. Otherwise leave the approved mix untouched.
4. **Audio gate** on the delivered file: `_shared/audio/audio_gate.py <file> --ab AB.mp4`. The outdoor 8/28 lav fails the `artifacts`
   (flux) row before any processing (ad-edit RA-01 lesson 2): that is Dan's known per-roll exception, recorded with his RA-01 approval,
   not a reason to process harder or tune the bound. Every other row must pass.
5. **Edit sheet** (required before the gate stamp; for the 9:16 the sheet is written from this build): plan must carry `people` and
   `physique` beside `label` for every clip and photo (they are in `beats_r3.json` `cards`). If `sheet_from_claude_build.py` is 16:9
   only, write the sheet with what it supports and record the gap rather than hand-editing a sheet.
6. **Watch pass** `_shared/deliver/watch.py <file> --plan plan.json`, then a FRESH judge subagent over every sheet and strip
   (`--judge`). Expected changes: every cut in `beats_r3.json`, the card and overlay in/outs, O2's flash (frames 37-39).
7. **Delivery gate** `_shared/deliver/gate.py <file> --format ad9x16 --plan plan.json`. Geometry for the plan comes from the renders:
   graphic boxes in `round3/gfx/manifest.json`, caption ink from `round3/cap_9x16/caption_states.json`, label chips: O2 chip
   (60,1296), A1 chip box in its manifest entry, P1 real-picture chip and result card from `s83_phone.py`. A row that does not apply goes
   in `not_applicable` with a reason, never a skipped check. Measured checks already run on the composite (`s88_checks.py`): face at least
   374 px above every lower third, the button and R1; zero caption collisions.
8. **Independent review** (`ra-reviewer` agent) on the delivered file against the plan and the standing rules, including the three
   sense questions for O2 and the AI label on every AI picture. Fix and re-gate anything it finds before Dan sees the file.
9. **Deliver:** `Claude Ad Videos/the cheat code for six pack abs - RA-14/` (master + `REVIEW 540p` copy + gate stamps + `notes.md` with
   the take map and every choice), a copy in `Videos to Review/` (the ad is 50.5 s), a short review page or the file link, the edit queue
   set to `delivered` (`scripts/edit-queue/queue.py` + the artifact db mirror), the board entry updated. Then stop for Dan's review.
10. **After Dan approves the 9:16: the 16:9** from the same edit (the analysis card's 16:9 layout is built; lower thirds and R1 use the
    16:9 templates; horizontal framing stays static per shot, VIDEO-RULES). Then `/ad-setup`.

Recipe: `/Volumes/Extreme/_edit_work/ra14/` and `.claude/skills/ad-edit/reference/ra14/round3/` (s81 opener, s82 holds, s83 phone
cards, s84 plan, s85 captions, s86 assemble, s87 page, s88 checks). The Mac runs other sessions' renders: wait through
`_shared/buildcap.py`.

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `Cheat Code Six Pack AD R4`. Read `Handoffs/handoff-20261014-ra14-cheat-code-round4-after-dan-picks.md` and build round 4 of RA-14 "The Cheat Code For Six Pack Abs" with /ad-edit. Everything from round 3 is approved and locked. Build the full 9:16 from the locked parts, run the audio gate, edit sheet, watch pass, delivery gate and an independent review, fix anything they find, then deliver it to the ad folder and Videos to Review and stop for my review.
