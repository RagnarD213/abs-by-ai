# RO-05 "How I Make My Daily Salad": round 3, record Dan's round-2 decisions, then moving graphics + clips in context

**Written 2026-09-28 by Claude (Opus 5.5) at the close of round 2.** Job RO-05 on `Handoffs/video-editing/00-MASTER.md`. One round of
the round method (`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`). **Do not render the full video in this round.**

## 1. Where things stand
Round 2 packet sent to Dan 2026-09-28. **Nothing is approved yet.** Dan answers on the page (downloads
`RO05-R2-batch-decisions.json`) or in chat. Round 3 starts only once his answer exists.

- Review page: `/Volumes/Extreme/_edit_work/ro05-fable/round2/index.html` (served at `http://127.0.0.1:8775/index.html` with
  `python3 -m http.server 8775 --bind 127.0.0.1` from `round2/`; restart it if the port is dead).
- First-minute draft (0:00 to 1:05.4, to the end of the fasting explanation): `round2/DRAFT - RO-05 round 2 - first minute.mp4`
  (sha256 `9accaa9d8032e362...`) and `... REVIEW 540p.mp4` (`0950944d53a87c62...`). Grade B, new opening, G01/G02/T01/G03 in place.
- Decisions scaffold (every item pending, hashes filled): `/Volumes/Extreme/_edit_work/ro05-fable/round3-plan/decisions.json`.
- Stills manifest (copy, times, speech, face check, presenter-shift values): `round2/graphics/manifest.json`.

## 2. What round 2 asked (fill Dan's words per item into decisions.json, verbatim)
1. **Grade:** A / B / C (recommended B). Same luma curve as round 4; chroma + vegetable vibrance, skin held. Mean of six moments,
   saturation current 0.30, A 0.35, B 0.40, C 0.44; greens 0.42 / 0.45 / 0.51 / 0.57; skin 0.40 / 0.42 / 0.43 / 0.44. LUTs
   `round2/grade/luts_{A,B,C}/`, recipe `round2/recipe/grade2.py`, sheet `round2/grade/GRADE_OPTIONS_SHEET.jpg`.
2. **Opening** (`round2/recipe/edl_r2.py`, first section): C1535 3.30 to 7.55 on camera; with ONE continuous C1535 audio span
   3.30 to 18.50 underneath, salad close-ups C1550 111.0 to 113.4 and 115.2 to 117.2, then C1551 4.95 to 7.10 (bite at 5.0, chewing,
   fork raised; picture only), back on camera C1535 14.10 at "Now this salad". Old C1550 VO hook removed. Flagged to Dan: no clear smile
   after the bite; the smiling close-up (C1551 2.3 to 4.4) crops his hair, so not used; alternative offered: a third salad angle
   (C1545 top-down, 10.0 to 14.5 is unused) in place of the bite.
3. **Section titles:** A full-screen Soft Blue title scene (T01 to T08), B a lower third "PART n OF 8", or C none.
4. **Every graphic** G01 to G33, T01 to T08, L01 to L03 (old glow cards shown full frame), D01/D02 (app demo: C1541 with the
   presenter shifted right + the approved WV-01 iPhone on the left; phone-only beat on the field), F01 (speed-up chip). G03 (the 1:06
   graphic Dan disliked) has two copy options. Merged/removed list is on the page and in `round2/recipe/gfx_r2.py` `REMOVED`.

## 3. What round 3 builds (after recording the decisions)
1. Re-hash every locked file against `round2/locked_hashes.json` and the round-2 hashes above; record expected vs actual.
2. Apply Dan's copy edits and verdicts in a NEW `round3/` folder (copy `round2/recipe/` there; never edit round2 in place).
   Re-render only the stills whose copy or placement changed, for approval, if he asked for changes.
3. **Moving previews of the APPROVED stills only**, each `<ID>-context.mp4` with about 5 s of narration either side, in the approved
   grade, audio excerpted from the chain output (no new processing). For the 3A cards (G05, G20, G27) check the fixed presenter shift
   over the whole moving piece (the camera is handheld; the shift is `shift_presenter` with the empty kitchen stretched at most 1.45x);
   G05 builds its four items as Dan names them (item times in the old stack: piece starts + 0.2, and +12.7 s in the C1537 59.20 piece).
4. **Clips in context** (never explicitly approved): the 14 B-roll previews sent 2026-09-24 (`packet/broll/`, reel
   `packet/BROLL_PREVIEWS_reel.mp4`), the GoPro onion cover (C1544 150.76 to 154.36), and the new opening shots if Dan did not already
   approve them as part of the opening.
5. If Dan approved the grade and opening but asked for first-minute changes, re-export the first minute (`build_r2.py firstmin <OPT>`)
   with the same file naming. Full video only when nothing is pending (round 4 or later).

## 4. Traps found in round 2
- `build_r2.py firstmin` and `stills` both call `resolve()`; only `stills` writes `graphics/manifest.json` now (a firstmin run wiped it
  once). Run `stills` last before building the page (`round2/recipe/page.py`).
- The head detector flags hand close-ups (G12, G13, G14) and the bowl hold (G17) as overlaps; checked by eye, the lower third sits over
  hands/bowl, not face or hair. Keep the eye check in the moving previews.
- Cap two concurrent builds (Codex WV-01 round 12 was rendering during round 2).
- The operator framed Dan's hair at the top edge in several punch-ins (for example G06's frame, C1538 at 1.2); round 4 accepted that as
  a known source limit. If Dan raises it, the fix is the wide level for that piece, not a new crop.

## 5. Gates and costs
- No delivery gate was run or claimed on the first-minute draft (review copy only). Loudness measured -14.4 LUFS integrated, LRA 2.7.
- Cost ledger for this recut: $0 generation so far (rounds 1 to 4 and round 2 used only existing footage). Cap $5 per video (VIDEO-RULES).

## 6. Close round 3
Record decisions, build the packet, send Dan the page and previews, write the round-4 handoff, update the queue
(`python3 scripts/edit-queue/queue.py set RO-05 needs --note ...`), the board entry and `Handoffs/README.md`. Then stop.

## 7. Model and starter prompt
Claude Opus 5.5, effort high.

> Read `Handoffs/handoff-20260928-ro05-round3-graphics-motion-and-clips.md` in full, then `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/_shared/SOFTBLUE.md` and `.claude/skills/_shared/GRAPHICS-STANDARDS.md`. Here are my round-2 decisions: [paste the downloaded RO05-R2-batch-decisions.json or your notes]. Record them in round3-plan/decisions.json, then run RO-05 round 3 only: moving previews of the graphics I approved and the B-roll clips in context. Do not render the full video. Send me the page, then write the round-4 handoff.
