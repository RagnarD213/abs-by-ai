AD (Great Again T upsell video). Task name: `GAT Upsell 4 AD R2`.

# Great Again T Upsell 4: Abs By AI (WV-07), round 2: transfer to Codex (2026-11-20)

**Why:** Dan, 2026-11-20: "Can you message all active edits here and tell them to pause work and create a handoff document to transfer
the edit to ChatGPT?" Claude's weekly limit is nearly used up; Dan is moving to the $500 ChatGPT plan. This is his explicit request to
move this video to Codex. **Do not start until Dan's ChatGPT upgrade is active.**

**Model:** Codex GPT-6.2 Sol, High effort. **Mac: the M6** (job is on its internal SSD, `~/Projects/_edit_work/WV-07`, 34 GB).
Run it on the M6 (editroute rule 1: a job never moves mid-flight). It runs on the M2 only if Dan asks; then copy the whole folder
to `/Volumes/Extreme/_edit_work/WV-07` (391 GB free) with `editroute.py push`, verify hashes, and run it there. Never edit through
the M2 network share from the M6 (`/Volumes/Extreme` and `/Volumes/Expansion` on the M6 are SMB mounts of the M2).

One native 9:16 upsell (1080x1920, 29.97), Dan on green screen over Wood Kitchen 1, roll C1904 Upsell 4 range (local copy in `src/`).
State: **PAUSED-FOR-CODEX-TRANSFER**. Edit slot released. Nothing rendered for round 2 yet.

## 1. Read first (in this order)
1. `~/Projects/_edit_work/WV-07/round2-plan/RESUME.md` (exact state, file by file) and `round2-plan/decisions.json` (the plan for each change).
2. `Handoffs/video-editing/WV-07-round-2-revisions.md` (the original round 2 brief; its section numbers are the work list).
3. `~/Projects/_edit_work/WV-07/round1/ROUND-1-NOTES.md` and `round1/ROUND-1-REVIEW.md` (source mapping, recipes, R1 fixes).
4. `.claude/skills/_shared/VIDEO-RULES.md` (top), `PRE-RENDER-APPROVAL.md`, `CUT-CONTINUITY-QC.md`, `/ad-edit`; the editcap,
   renderq and editroute READMEs under `.claude/skills/_shared/`.

## 2. What Dan approved (locked)
- **Round 1 film** (first 78 s): `round1/GAT Upsell 4 AD R1 - First 78 Seconds.mp4`, sha256
  d6822361fef29f9221fa3d3559ba464d1d7ce094416158617c13c1fcdc6ed0e3. Reviewed by Dan 2026-11-19.
- **Colour: Matched** (`look/LOOK_WV07.json`). **Voice: House bass** (`look/VOICE_WV07.json`). Dan: "Let's go with match for the color.
  House bass for the voice."
- **Key:** accepted as shown (no note). **All 30 key pieces are done; never re-key.**
- Accepted with no note: L01 four-signs list, P01 phone + bottle, S01 Leproult study card, A03 calorie tracking + Sleep Coach,
  A05 future body, O01 price card, K01 guarantee card.
- Dan's round 1 words verbatim: `round2-plan/notes_r1.txt` (also in the round 2 brief, section 1). Read them; they are the spec.

## 3. The four changes and their state
| id | Dan asked | state |
|---|---|---|
| J23 | smooth the slight pause at ~0:57 | **Done in the cut.** `work/edl/edl_tight.json` = R1's 91 segments with only seg 23 starting at 2945.709 (after a lip click at 2945.44); film now 280.347 s, everything after 0:56.6 shifts -0.367 s. `edl_build.py` has ONSET_FIX S06=2945.80, but a full `edl_build.py` rerun splits seg 26 at 2963 (92 segs, a new jump cut), so **do not rerun edl_build.py**; the hand-patched edl_tight.json is the one to use. |
| A01 | real B-roll side laterals, most ripped, two: gym + pool | **Ready, not rendered.** `demos/demo_insert.py` (Soft Blue field, 960 px square panels, chips "At The Gym" / "At Home"); sources in `demos/src/`; crops + colour in `demos/grade.json`, measured in `demos/GRADE.md`. Gym B0677 machine lateral (no gym dumbbell lateral exists in the library), pool B0450 shirtless dumbbell laterals. Full-width panels, not inside the phone (too small to read his physique). |
| A02 | meal plan screen WITH the food image right below the Honey-Garlic Salmon & Sweet Potato Bowls title and grey text, then one other recipe | **Ready, not rendered.** `meal/meal_pages.py` lays the photo into the real app recording between the grey meta line and "Grocery list" (layout checked on stills); the steak bowl tap lands on "steak and potatoes". Placed on the 2:39 line Dan quoted (segs 53-54), not the S09 line the brief named. Photos: four made at $0, blind Google vs Codex sets `meal/blind_salmon/`, `meal/blind_steak/` (X1, X2; key hidden, never tell Dan the source unless he asks). Film picks (editor default) `meal/picks.json`: salmon X1, steak X2. Show both pairs on the review page so Dan can swap. Food illustration: no AI label. Never the rejected chicken-and-broccoli plate. |
| C01 | "Click the button below to try Abs By AI" + arrows pointing down, no in-video button | **Coded, not rendered.** `downcta` element in `film/recipe/r7card.template.htm`; `graphics.py` builds one C01 from seg 90 ("Click Accept Offer below") to the end, C02 pill removed. Text "Click The Button Below / To Try Abs By AI" (cyan second line), three cascading down chevrons, captions stay at y 1545 above it. Dan: avoid confusing a prospect "maybe in their 60s or 70s". |

Backups of every R1 file changed: `edl_build.r1.py`, `graphics.r1_final.py`, `r7card.template.r1.htm`, `work/edl/r1_backup/`.

## 4. Exact next action
1. `editroute.py pick WV-07 --kind AD --round 2` (expect m6), then `editcap.py acquire WV-07 --title "Great Again T Upsell 4: Abs By AI" --type AD`.
2. Re-run `film/recipe/chain_piccuts.sh` through `renderq.py run` (it was stopped mid-run; `work/edl/piccuts.json` and
   `edl_picture_final.json` are still R1's). Confirm 91 segments and the picture_final report.
3. Audio: the `plates.build_audio` line of `film/recipe/chain_audio.sh` (only that line; the voice/colour option lines are R1 only).
   Seamscan the 0:57 join.
4. `python3 graphics.py --render --only A01,A02,C01` (A02 runs meal_pages.py from picks.json first), plus any graphic whose duration
   changed against the R1 manifest. Check stills of each.
5. Whole film with `render_film.py W1 --t0 0 --end <FULL_END> --out <round 2 film>` (pattern: `chain_r1_film.sh`), through renderq.
6. Every gate on the exact file: check_film, hair, `proof_captions.py`, sync, audio gate with seamscan on every join,
   `deliver/gate.py --format ad9x16` with its gate plan, watch pass, CUT-CONTINUITY-QC; check the two demo clips' colour in the final
   frames (B-roll rule). Then a fresh independent reviewer; fix what it finds.
7. Deliver to `Claude Ad Videos/Great Again T Upsell 4 Abs By AI - WV-07/` and `Videos to Review/` (replace the R1 file), build the
   round 2 review page (pattern `round1/review/make_inputs.py` + `build_page.py`, served by `_shared/review_server.py`; R1 used port
   9878) listing each change with its new timestamp, both blind food pairs and "What I decided"; test at 800 and 1150 px; silent checks,
   then owner handoff. Release `editcap.py release WV-07 --review`, `queue.py set WV-07 delivered`, update the board line, stop for Dan.
8. On Dan's final approval: write the Codex `/ad-setup` handoff. No covers, uploads or scheduling in this job.

## 5. Traps hit
- `editcap acquire` exits 3 while the M6 is reserved for a priority job (Joint Vigor): wait, never jump the line.
- Python has no `soundfile`, and `wave` fails on format 65534: read audio by piping `ffmpeg -f f32le` into numpy.
- Roll times are ROLL seconds; local video t = roll - 79721*1001/30000; local audio wav t = roll - 2660 (`src/MAPPING.json`).
- Graphics placements are by segment index (`segt(i)`); a segment count other than 91 moves every graphic. Keep 91.
- A 9:16 crop of the 16:9 demos cuts his arms at the top of the raise; keep the square crops in grade.json.
- Flow image downloads may land on the M2's ~/Downloads (connected Chrome is there).

## 6. Waiting on Dan
Nothing until the round 2 page. On that page: the four changes, the food photo pairs (swap option), and the R1 review items left for
his ear (D9/D10 room-tone steps). No review page is up for round 2 yet; the R1 page (port 9878) may have been retired.

## Starter prompt (Codex GPT-6.2 Sol, High; start only once Dan's ChatGPT upgrade is active)
```
AD (Great Again T upsell video). Name this task "GAT Upsell 4 AD R2". Dan moved this edit from Claude to you on 2026-11-20. Work on the M6
in ~/Projects/_edit_work/WV-07 (never through the M2 share). Read Handoffs/handoff-20261120-wv07-transfer-to-codex.md in the project
folder, then round2-plan/RESUME.md and decisions.json in the job folder, and finish round 2 from section 4 step 1: acquire the edit slot,
re-run picture cuts, audio, render A01/A02/C01, the whole upsell, every gate, independent review, deliver, round 2 review page with
the timestamp of each change, release the slot with --review, then stop for Dan. Never re-key; keep 91 segments; do not rerun edl_build.py.
```
