# RO-05 "How I Make My Daily Salad": round 4, record Dan's round-3 answers, fix only what he flags, then the full film

**Written 2026-09-29 by Claude (Opus 5.5) at the close of round 3.** Job RO-05 on `Handoffs/video-editing/00-MASTER.md`. One round of
the round method (`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`). Supersedes `handoff-20260928-ro05-round3-graphics-motion-and-clips.md`.

## 1. Where things stand
Round 3 packet sent to Dan 2026-09-29. **Round 4 starts only once his answer exists** (he downloads `RO05-R3-batch-decisions.json`
from the page, or answers in chat).

- Review page: `/Volumes/Extreme/_edit_work/ro05-fable/round3/index.html`, served at `http://127.0.0.1:8776/index.html` with
  `python3 -m http.server 8776 --bind 127.0.0.1` from `round3/` (restart it if the port is dead).
- Moving previews: `round3/ctx/<ID>-context.mp4` + `.jpg` poster, 1080p, grade B, about 5 s of narration either side; hashes and windows in
  `round3/ctx/ctx_manifest.json`; audio sync vs the raw lav in `round3/ctx/sync_check.txt`.
- First minute without G02: `round3/DRAFT - RO-05 round 3 - first minute.mp4` (+ `REVIEW 540p`), audio stream-copied from round 2.
- Decisions so far (round 2, recorded with Dan's exact words): `round3-plan/decisions.json`; his raw file `round3-plan/RO05-R2-batch-decisions.json`.
  Round-4 scaffold: `round4-plan/decisions.json` (write it from his round-3 file).
- Recipe: `round3/recipe/` (`build_r3.py` shifts / segs / ctx / firstmin, `gfx_r3.py` = round-2 proposals + Dan's edits, `stills_r3.py`, `page_r3.py`, `sync_check.py`).

## 2. Locked (never reopen unless Dan does)
Grade **B** (`round2/grade/luts_B/`; "Let's go with B for the grade"). Opening incl. the two salad close-ups and the bite ("I like that salad
close up clip that you chose for the intro. I think that was exactly what we need there"). First minute ("Once we lock in the grade and the
other decisions, that is set"; re-exported only to drop G02). Section titles **A, full screen**. The wording of all 45 kept graphics, including
Dan's own rewrites of G05 item 4, T05, G19, T06, G22, T08, G29 (exact strings in `round3-plan/decisions.json` `dan_copy`). **G02 and G14 removed.**
The cut, audio chain, bed, framing and flash transitions from round 4 of the old build. B01/B02/B03 (opening shots) locked with the opening.

## 3. What round 3 asked (record Dan's words per item into round4-plan/decisions.json, verbatim)
1. **Question 1, the three list cards on moving footage.** The 3A left card, clear on its approved still, covers Dan on the handheld
   kitchen takes (per-piece check in `round3/shifts.json`, sheet `round3/tmp/l3_sheet.jpg`): G05 pieces 20-21 (1:56.7 to 2:25.3, camera on
   the chicken bag and olives), G20 pieces 76-77 (8:14 to 8:25.6), G27 piece 117 (11:47 to 11:57, close-up). Option A = card as approved
   (`G05/G20/G27-context.mp4`, per-piece fixed shift, never animated). Option B = one Motivation lower third per item as he names it
   (`G05-B/G20-B/G27-B-context.mp4`, times in `gfx_r3.L3_ALT`). Recommended B.
2. **Question 2, G15 label.** G14's removal makes the count jump 4 OF 11 to 6 OF 11. Option: G15 topic `INGREDIENT 5 OF 11` instead of
   `KEY POINT` (still `round3/graphics/G15-alt.jpg`). Recommended.
3. **Every item** (Approve / Changes requested / Remove + note): FIRSTMIN, every graphic G01 to G33 (less G02, G14), T01 to T08, D01, D02, F01,
   and the clips L01, L02, L03, B07, B08, B10, B11, B12, B14 and B15 (GoPro onion cover, C1544 150.76 to 154.36).

## 4. What round 4 builds
1. Re-hash every locked file (round2 `locked_hashes.json` + round-3 hashes in section 7) before touching anything; record expected vs actual.
2. New `round4/` folder; copy `round3/recipe/`; never edit round3 in place. Apply Q1 (edit `gfx_r3.py` into `gfx_r4.py`: for B, drop the
   three l3 items and use `L3_ALT`), Q2, and any per-item notes.
3. **If anything is "Changes requested":** rebuild only those previews (`build ctx <ID>`) and send a small page with just them. No full film.
4. **If nothing is pending:** the full film. Build from the locked components with the round-3 machinery: all pieces are cached in
   `round3/segs_B/` (link them), overlay every approved item with `paint()`, flashes via `B.Overlay`. Audio: run the locked chain once on the
   full timeline (the old `firstmin()` path in `round2/recipe/build_r2.py` generalised to the full length; `voice_chain.py` settings unchanged)
   so the opening's new audio joins the rest; the round-4 old film's mix is not reusable for the first 12.5 s. Then exact-file gates
   (`_shared/deliver/`), the watch pass, subtitles + chapters regenerated from the new timing, and one independent `ra-reviewer`.
   Deliver to `claude edited long form content/08 - How I Make My Daily Salad (Fable recut)/` with a new name (never overwrite the round-4 file).
5. Organic content video: after Dan approves the delivered film it goes through `/video-setup`, never an ad path.

## 5. Traps found in round 3
- Moving check of side cards: see the new paragraph in `PRE-RENDER-APPROVAL.md` (Editing checks). The head detector reads hands as heads
  when the camera tilts to the counter (G05 piece 18), so judge failures from the sheet, not the flag alone.
- `build_r2.py` reads `sys.argv[2]` as the grade at import; `build_r3.py` sets `BR.OPT = "B"` after import. Keep that when copying.
- The ctx job re-loads the timeline per window (`load()` in each worker); the segments cache key ignores title copy, which is why titles are
  drawn in the overlay pass and the title segment is only a black placeholder.
- Audio for windows after the opening comes from the locked round-4 film at a per-piece offset (-12.5 s, one-frame drift at most); windows
  inside the first minute use the round-2 draft. `audio_src()` refuses a window that straddles both.
- Cap two concurrent builds.

## 6. Gates and costs
No delivery gate was run or claimed on any round-3 preview (review copies). Sync: every ctx clip checked against the raw lav (see section 1).
Cost ledger for this recut: $0 generation (all existing footage). Cap $5 per video (VIDEO-RULES).

## 7. Round-3 file hashes
All 107 round-3 files (55 previews, 47 stills, first minute, page, recipe) with sha256: `round3/locked_hashes_round3.json`.
Key ones: first minute `63291971b8fa5d8b...`, its 540p `14bc5155d98164cf...`, page `a4cad2de43d996b4...`. Round-2 locks: `round2/locked_hashes.json`
(re-hashed 2026-09-29, 76 of 76 matched: `round3-plan/rehash_round3.json`).
Verification done in round 3: first minute 1960 frames = round 2; picture differs only inside G02's old slot (0:15.4 to 0:22.0);
decoded audio sample-identical to round 2 (last 1024 samples trimmed to picture length). All 55 previews within one frame of the raw lav
(`round3/ctx/sync_check.txt`, 55 of 55 OK). Eye check sheets (graphic vs face) `round3/tmp/eye_*.jpg`: every lower third and title clear of the face;
3A option A overlaps as described in section 3.

## 8. Close round 4
Record decisions, build, send Dan the page (or the delivered film), write the round-5 handoff if anything is left, update the queue
(`python3 scripts/edit-queue/queue.py set RO-05 ...`), the board entry and `Handoffs/README.md`. Then stop.

## 9. Model and starter prompt
Claude Opus 5.5, effort high.

> Read `Handoffs/handoff-20260929-ro05-round4-motion-decisions-then-full-film.md` in full, then `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/_shared/SOFTBLUE.md` and `.claude/skills/_shared/GRAPHICS-STANDARDS.md`. My round-3 decisions are in ~/Downloads/RO05-R3-batch-decisions.json (plus any notes I add here). Record them in round4-plan/decisions.json, then run RO-05 round 4: rebuild only what I flagged; if nothing is pending, build the full video and run every gate. Send me the page or the film, then write the next handoff if anything is left.
