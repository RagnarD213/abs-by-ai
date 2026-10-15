AD (paid ad: it ends on "Tap the button below now to get started"). Sidebar name for the next task: `Best Ab Exercise AD R4`.

# RA-06 "What's The Best Ab Exercise?": round 4, Dan's round 3 notes, then the 16:9 and delivery

**Written 2026-10-14 by the round 3 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-06-whats-the-best-ab-exercise.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit` (THE EDIT SHEET, THE DELIVERY GATE,
Step 9.9 THE WATCH PASS, "RA-14 round 4 lessons"), `_shared/PRE-RENDER-APPROVAL.md`, `_shared/deliver/README.md`.
Recipe: `.claude/skills/ad-edit/reference/ra06/` (round 1 README) and `reference/ra06/round3/` (README: order and six lessons).
Work dir `/Volumes/Extreme/_edit_work/ra06/`.

**READY TO FIRE (2026-10-15). Dan approved the 9:16**, recorded in `/Volumes/Extreme/_edit_work/ra06/round4-plan/decisions.json`:
*"Everything looks good. This is approved. Give me the handoff or setup."* The 9:16 below is locked as delivered; do not rebuild
or "improve" it. Hashes re-checked 2026-10-15, all match the table. What is left before `/ad-setup`: the 16:9 from the same edit,
the gates and independent review on both formats, and filing to the ad folder.

## What round 3 built (the review copy Dan watched)

- Full 9:16, 45.71 s, 1370 frames: `draft_9x16.mp4` (sha256 first 16 in the table), same file as
  `round3/DRAFT - RA-06 round 3 - full ad.mp4` and `Videos to Review/Best Ab Exercise AD R3 - full ad.mp4`.
- Applied Dan's round 1 answers: pair 3 framing (close 684x1216, wide 846x1504); close centred on a 1 % land-then-hold band
  (`round3/s10b_near_track.py`, median 0.8-1.2 % off his head centre); the split screen re-graded per roll (`round3/split/split_luts.json`)
  and the vacuum panel on the draw-in (C1677 from 138.95 s, crop 2304x1296 at 1263,279); B1 poses card removed; button
  "Tap The Button Below To / Start Training With AI".
- AI clips from the approved frames (Kling v3 standard, 7 takes, $7 of the ad's $10; ledger `round3/motion/ledger.json`):
  I3 body scan = I3_v1 0-5.0 s (5.97-10.98 s); I1 copier = I1_v1 0-2.05 s + I1_v2 3.10-4.55 s cropped 576x1024 (10.98-14.48 s,
  four takes could not draw three hand-offs); I4 robot waves goodbye = I4_v2 0.25-2.35 s (41.47-43.58 s, under the button).
- Audio: the approved mix plus one +3.5 dB phrase ride on "and replaced them with AI." (22.40-23.85 s), audio gate PASS.
- Independent review SHIP (0 blocking, `round3/review/ROUND-3-REVIEW.md`), fixes re-reviewed SHIP (`ROUND-3-REREVIEW.md`),
  then the vacuum in-point moved from 138.35 to 138.95 s on the re-review's suggestion (self-checked; gates re-run).
- Watch items the reviews left for Dan's eye: the wide at 27.56 s follows his lean (standard tracker); the trainer's sheet rests on
  his palm about 0.9 s in I1; his hand presses beside the navel during the draw-in (his own technique, as in B0419).

## Round 4

1. **Re-hash** the locked files below into `round4/HASHES.json`; build in `round4/`, never overwrite `round3/`.
2. **The 9:16 master**: the approved `draft_9x16.mp4` (423653d81972ae48) as is, bit for bit → `round4/whats the best ab exercise | claude | 9x16 | RA-06.mp4`.
3. **The 16:9 from the same edit** (`s10_render06.py 16x9`, `s07_captions.py 16x9`, the 16:9 HyperFrames templates for LT2 and the
   CTA, the split screen and AI cards re-laid for 16:9). Horizontal framing stays static per shot (VIDEO-RULES; `cx16` in the plan
   already shares the wide's centre so a zoom cut is a pure zoom). The AI clips are 9:16: place them as phone-shaped panels beside
   Dan or as plates on the Soft Blue field (ad-edit lesson 61), never cropped to 16:9; their chips by looking at each clip again.
   Show Dan stills of every 16:9 card before the full 16:9 render only if a layout is new to him.
4. **Edit sheet** for the 16:9 (`_shared/edit-sheet/sheet_from_claude_build.py`, then `validate.py --hash`); plan rows need `people`
   and `physique` beside `label` for every clip and photo.
5. **Gates on BOTH files**: `_shared/audio/audio_gate.py` (`--untreated mix.wav.audio_untreated.json`), `_shared/deliver/watch.py`
   then a FRESH judge subagent, `_shared/deliver/gate.py --format ad9x16` and `--format ad16x9` with `talking_head_windows`, the
   full-screen cards listed in `punch` with `punch_covered: true` (RA-14 round 4 lesson 3), and the measured phone box.
6. **Independent review of both** (`ra-reviewer`), including the three sense questions per AI clip. Fix and re-gate before delivery.
7. **Deliver** to `Claude Ad Videos/whats the best ab exercise - RA-06/` (both masters, REVIEW 540p copies, stamps, `notes.md` with the
   take map and every choice). Then: `python3 scripts/edit-queue/queue.py set RA-06 delivered` + the artifact db mirror;
   `roll_sidecar.py mark-used` for C1664, C1677, C1682, C1683; clip library `add --status used-final --used-in "RA-06"` for the three
   AI clips (I3_v1 cut, I1 two-shot cut, I4_v2 cut) and `clip_library.py sheet`. Then stop for Dan.
8. **When Dan finalizes**: delete `Videos to Review/Best Ab Exercise AD R1 - full ad draft.mp4` and `... R3 - full ad.mp4`, then
   `review_server.py 8806 --remove`, `8836 --remove`, `8837 --remove`; set the queue to `finalized`; delete the board entry.

## Locked files (sha256 first 16; re-hash before touching)

| file | sha256 | what |
|---|---|---|
| `draft_9x16.mp4` | 423653d81972ae48 | the round 3 9:16 Dan reviews |
| `mix.wav` | 9701430676ab05a6 | approved voice + the round 3 ride |
| `cut.json` | d04eb8248c43b42a | unchanged since round 1 |
| `beats.json` | 352b86b103f02a2f | round 3 plan |
| `cards_9x16/I3.mp4`, `I1.mp4`, `I4.mp4`, `split.mp4` | bbec5fdd11bfd1c5, 2579da72427feb11, f3b3b40dd9d9a22c, 136bb2e229cb2b9b | the AI cards and the split screen |

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `Best Ab Exercise 16x9 AD R4`. Read `Handoffs/handoff-20261014-ra06-round4-final-16x9-and-delivery.md` and continue
> RA-06 "What's The Best Ab Exercise?" with /ad-edit. I approved the round 3 9:16 as is. Build the 16:9 from the same edit, run every gate
> and the independent review on both formats, fix what they find, deliver both to the ad folder, update the queue and the clip library,
> and stop. Setup (/ad-setup) is the next task after that.

**Recommended model and effort: Opus 5.5, high.** A recipe-backed format build plus the delivery gates.
