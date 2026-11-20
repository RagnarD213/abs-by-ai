AD (Great Again T sales video). Task name: `Great Again T VSL AD R8`.

# Great Again T VSL (WV-03): transfer from Claude to Codex (2026-11-20)

**Why:** Dan, 2026-11-20: "Can you message all active edits here and tell them to pause work and create a handoff document to
transfer the edit to ChatGPT?" Claude's weekly limit is nearly used up (resets Thu Nov 26). Dan is upgrading to the $500 ChatGPT
plan, and this video moves to Codex at his explicit request (AGENTS.md: "Only Dan's explicit request moves a video to the other AI").
**Model:** Codex GPT-6.2 Sol, High effort. **Do not start until Dan says his ChatGPT upgrade is live.** Dan fires it.

One native 9:16 sales video (1080x1920, 29.97 fps), Dan on green screen keyed over Wood Kitchen 1 (roll C1903), about 24 min 20 s
after dead-air removal. Round 8 is the FIRST FULL FILM. Dan has not seen any of round 8's film yet.

## 1. Where the job is (the M2 only)

- **Mac:** the M2 Pro (`ssh m2`). Every command runs on the M2. Never do job I/O through the M6's SMB share of the M2 drives
  (it hung for an hour in round 7; VIDEO-RULES "Two Macs"). From the M6: `python3 .claude/skills/_shared/editroute/resume.py run WV-03 -- <cmd>`.
- **Job folder:** `/Volumes/Extreme/_edit_work/WV-03` (M2 Extreme; `~/_edit_work/wv-03` on the M2 is a symlink to it).
  Also `/Volumes/Expansion/_edit_work/WV-03` (3 items, older). The M6's `~/_edit_work/wv-03` is a frozen round 6 copy: never use it.
- Key: `round5/key/` (source `src/C1903.MP4`, 46 GB; plates in `plates/`, markers in `logs/plate_Q*.ok`, `logs/skip_Q*.txt`).
- Film recipe for round 8: `round5/film/recipe_r8/` (work files `round5/film/work_r8/`). Build log: `round5/film/BUILD_LOG.md`
  (sections 16 and 17 are round 8; read them).
- Round 8 folder: `round8/` (briefs `BRIEF_R8_*.md`, `motion/`, `graphics/`, `review/`, `review_ra/`, `FILM_STATUS.json`).
- Output when done: `round8/DRAFT - Great Again T VSL R8 - Full Film - Wood Kitchen.mp4`.

## 2. State right now (2026-11-20, about 9:40 AM Central)

- **Keying: DONE.** All 173 pieces handled: 169 plates, 4 deliberately skipped (Q38, Q73, Q108, Q168: wholly under full-screen
  graphics, `logs/skip_*.txt`). Finished 05:08 on Nov 20.
- **Final film chain: RUNNING, unattended, left running on purpose** (it costs no Claude allowance):
  `round5/film/recipe_r8/chain_final_r8.sh`, pid 39528 at handoff, log `round5/film/work_r8/chain_final.log`.
  Passed: plates ready, AI clips (`aiclips_r8.py build`), graphics manifest, shot plan (`SHOTS_DONE 181`).
  **At handoff it was rendering section 0 of 6** (started 09:22). Then: `render_film_r8.py join 6`, sha256 to
  `work_r8/film_sha256.txt`, `check_film.py W1`, the audio gate, `proof_captions.py`, then `FINAL_CHAIN_DONE`.
  Expected finish: early-to-mid afternoon Nov 20 (each section is a heavy render-queue step, one at a time).
  A section that already exists is skipped on a re-run, so re-running `chain_final_r8.sh` after a failure resumes where it stopped.
- **Edit slot: released** by Claude at handoff (`editcap.py release WV-03`). The running render steps still count until they
  finish. Codex: `editcap.py acquire WV-03 --title "Great Again T VSL" --type AD` (run on the M2) before any new production.
- **ETA tracker:** `eta.py` plan reported (4 steps). Keep it current: `eta.py step WV-03 <N>`, `eta.py retry WV-03 "why"`.
- **Nothing is waiting on Dan right now.** The round 8 review page has not been built for the full film yet.

### Three bugs fixed today (backups kept as `*.bak_20261120` in `recipe_r8/`)
The chain failed at 05:13 and 09:07; nobody noticed the first for three hours because the chat's background watcher died with the
session. Fixed:
1. `aiclips.py` `_conform`: asserted `n > 30` but `aiclips_r8.slots()` allows a 30-frame floor; AI-73's slot is exactly 30 frames.
   Now `n >= 30`.
2. `plates.py` `Plates.at_film_frame`: a frame inside a SKIPPED piece's range tried to open its missing plate (EOFError). Now
   falls through to the other-plate search and raises `LookupError` (covered, never shown) like other covered frames.
3. `gesture_shots.py` `main`: a shot wholly under graphics had no plate measures (`min()` of empty). Now uses film-wide values,
   catches `LookupError` per frame, and `plan_and_write` keeps it as "wholly under a full-screen graphic" (that branch already existed).
**Trap:** expect more of this kind wherever code assumes every film frame has a keyed plate. Round 8 keyed only frames that are seen
(`seen_r8.py`), which is new.

## 3. Everything Dan approved (his words outrank every summary here)

- Round 7 notes word for word: `round8-plan/notes_r7.txt` (sha256 `29bfa896cbc82148ac40d47afb9d3915c4e8b39a91c8c655b632a78f9756d3f7`),
  editor's reading `round8-plan/decisions.json` (`9e0939d1f5a89f83cb6fedc9e03c1696b4f00778f8bc8f376c97ea8a9f58d7f8`).
- Round 8 picks word for word: `round8/review/inputs/notes_r8_picks.txt`
  (`be2063bddbec4892d29b7fb32f17389041a7d3eec7a6f774894c940366bfc20e`). In short:
  - "For In Bed: The Aftermath, generate both. We'll see which one turns out better. Use whichever one you think turned out
    better in the full film, and then show me the other one on the next review page as well."
  - AI-78 Number Candles At Forty, Glasses On: X1. AI-81 The Jog That Stops: X1.
  - AI-70 love life: use X2. "Trim out the beginning of this where she smiles." (Done: `round8/motion/AI70_TRIM.json`, starts frame 54.)
  - Stock choices made for him: no changes.
  - "The full film": not answered yet (he has not seen it).
- **All graphics approved** (round 7): `round7/graphics/MANIFEST.json` (`e89314c535427df931da9396f038a2e6006324df3c83461180a87f9b50636f2a`):
  67 graphics + 7 stock + A0042. Maca root X2, Tongkat root X1. S10 tablets: a man's palm. Do not reopen their style.
- **Round 7 approved clips** stand (22 verified, `round7/motion/MANIFEST.json`), except **AI-02 Two PM Crash: OUT** (he dislikes it).
  AI-68 X1 takes 1:22. AI-71 at 0:58 had no pick: Dan stays on camera there.
- **Round 8 motion** (`round8/motion/MANIFEST.json`, `cab41b8eff5c25f4fdb2cc844f16f9c1b56db6ab09199ed7ba8acc217dd0fbff`). VERIFIED finals in
  `round8/motion/final/` (sha256, checked 2026-11-20):
  - AI-07-x1 `10e40c5ec6f9b43565ad8ef05c1e49be675ed3bdc4e468ab9bb3c6176d9ee05c`
  - AI-54-x1 `a79987c564a9b3ef29107b918ab6cb4099afa8a95073cd7ee5c3a145ac1ed673`
  - AI-58-x1 `8b1ddf81ce35d58aeac467b5f83c5f53b743ef5945d95261dc7519b5dcd09a56`
  - AI-62-x1 `fec64f4fac633c155a549a3806bcb8abae3850e7e0d43b16e1860940790e790f`
  - AI-63-x1 `254da110f20ebda072ae3aa87f07096d77553e44f2c698ed9ee904312d5075f4`
  - AI-67-x1 `8f93567865301a30fe8515a6956305239f6e2df6c794b9948dadca344337a92d`
  - AI-68-x1 `6970c5c701ee2a28fd999898aac54151ce610971c0ce4bef6561d5dcae4f2044`
  - AI-70-x1 `2f06f3d2e4021a92308254dc36c872d88b0401a6f0284dddaa785c57a8f59352`
  - AI-70-x2 `9a854e403dd48b55d15dced1e3386115b916eabd17bdf7b03d7a3f56228a58f1` (the film uses this one, trimmed)
  - AI-73-x1 `f1ad666af35ab7d690ffaa579b993d7269bca50b5fbfa1cf121be112aeed52b6`
  - AI-78-x1 `9cebe347b6a516bf386ae7712d5431b029debd8552fe7cdceafe9155a4771912`
  - AI-81-x1 `36ffd5f02822f87ad02664b6556f164e4be992691e2583125c6d5330d363ac68`
  - AI-86-x1 `43f4c13344be5331bdec7fed8a04f3cad547e2ba45c752e5d7e5f403719ccf20`
- **NOT verified (never in the film; Dan stays on camera there; list them on the page):** AI-86-x2 (4 takes: room drift, her top
  melting into the duvet f97-127, his hand fusing into his forehead f184-189, clean part 2.3 s < 2.5 s minimum, one take leans into
  him), AI-64-x2 and AI-76-x1 (Dan's picks, motion never passed), and the retries of AI-18, AI-26, AI-51 x2, AI-57.
- **AI-86 decision** (`round8/motion/AI86_CHOICE.json`): film uses X1 (the only one that passed). X2 has no verified clip, so the
  page must say plainly that X2 was tried four times and failed, with why, since Dan asked to see the other one.
- **Placements decided by the film builder (BUILD_LOG §17):** AI-78 X1 replaces AI-47 on "I know my body and my drive... after I
  turned 40" (from 0:54.7). AI-81 X1 replaces AI-66 on "it just seems harder and harder to stay in shape" (from 1:12.0; 2.1 s, ends
  before "shape", Dan returns). AI-86 gets its own beat on "you still wanted a love life like you used to have" (1:44.0 to ~1:46.2),
  straight before AI-04 "tapped out"; "Or maybe, like me," stays on Dan. Round 8 ideas Dan did not pick (AI-79, 80, 82, 83, 84, 85,
  87) are excluded (`round8/review/inputs/dropped.json` says why each failed).
- Standing preferences that apply here: memory `gat-upsells-cleaner-more-camera` is for the upsells, not this VSL; the VSL keeps the
  wood kitchen background (memory `gat-vsl-teal-studio-test-later`: Teal Studio is a later split test, not this round).
  Approved closer framing for the whole film; Dan's 2026-11-15 gesture rule: "close shot more ... if I do gesture wide, the wide shot".

## 4. Exact next actions (in order)

1. On the M2: `tail` `round5/film/work_r8/chain_final.log`. If it shows `FINAL_CHAIN_DONE`, go on. If `FAILED`, read the step's log
   in `work_r8/` (`section_<k>.log`, `join.log`, `shots.log`, `aiclips_build.log`), fix, and re-run
   `nohup bash chain_final_r8.sh > ../work_r8/chain_final.log 2>&1 &` from `recipe_r8/` (existing sections are kept).
   Keep a watcher on the log; do not rely on a chat staying open.
2. Watch pass on the exact delivered file (native frames around every join and clip, AI clip appearance, captions, card overlaps),
   the shared delivery gate, `check_film.py`, audio gate (`--untreated` json is in the chain), caption proof. Fix and re-render
   only the affected sections.
3. A fresh independent review of the full file (the round's rule: an independent reviewer that sees only the file, the plan and the
   standing rules, never the editor's notes). Fix what it finds. `film_done_r8.py` writes `round8/FILM_DONE.json` (open issues incl.
   the not-verified picks).
4. Round 8 review page: `python3 round8/review/build_page_r8.py` (port 9830, `review_server.py`, mirrored to the M6 at
   http://127.0.0.1:9830/; `PAGE_NOTES.md` explains flags). It must show the full film, a timestamped "what changed" list with
   chapters, the AI-86 X1 clip in the film plus the X2 failure note, and anything still open. Test in the side pane at 800 and
   1370 px: **Start silent checks** first, then **Finish checks for owner** (VIDEO-RULES, silent checks).
5. `editcap.py release WV-03 --review`, set the Edit Queue status to `delivered`, update the board line, and stop. Do not start
   round 9 while Dan is reviewing.
6. Filing (required, AGENTS.md "Every generated AI clip is filed"): reconcile every round 8 Flow/paid output against the source
   archive and every keeper against a library ID; `round8/motion/FILING.json` and `COLLECTION_VERIFICATION.json` hold what was
   done. Note in the receipt: an unexplained 186-credit drop in Flow credits during round 8 collection was never traced.

## 5. Build method, skills and traps

- Read first: `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`, `.claude/skills/ad-edit/SKILL.md`,
  `_shared/PRE-RENDER-APPROVAL.md`, `_shared/CUT-CONTINUITY-QC.md`, the house chroma key `_shared/chroma-key/README.md`
  (keyonce stamps: never re-key a stamped piece), `Handoffs/handoff-20261116-great-again-t-vsl-round8.md` (round 8 plan and round 7 traps).
- Render queue: every heavy step through `renderq.py run --group WV-03`; never write wait loops or count processes. The M2 is loaded
  (WV-04 and WV-05 upsells share it; 8 cores for edits).
- Key lanes (if anything ever needs re-keying): `round5/key/lane_r8f.sh <lane>` claims pieces with `mkdir claims/Q..`; STOP files
  `STOP_LANES`, `STOP_LANE_<x>`. An orphan claim with no plate blocks a piece forever (Q03 had one; fixed by removing the claim).
  Pieces took 22 to 40 minutes each under load.
- Motion traps: Flow refuses frames with children (paid Replicate Veo fallback ~$0.80 a take, $5 cap for this job); held objects,
  fabric, printed labels and fire fail the motion gate repeatedly: design them out; Google END frames edited in Flow can carry the
  START's portrait chips: check identity on every END; gate checks time out when the M2 queue is busy, re-run without a limit before
  calling a pair failed.
- Pause history: a mistaken "pause all edits" on 2026-11-18 stopped the lane for 35 minutes (`round8/PAUSED-20261118.md`); it was
  withdrawn for Claude edits the same day.

## 6. Open pages and waiting items
- Round 8 picks page (already answered by Dan): http://127.0.0.1:9830/ on the M2 (mirrored to the M6). It will be rebuilt for the film.
- Nothing else waits on Dan for this video.

## Starter prompt (Codex GPT-6.2 Sol, High effort; run from the project folder; start only after Dan's ChatGPT upgrade is live)

> AD (Great Again T sales video). Name this task "Great Again T VSL AD R8". This edit moves from Claude to you at Dan's explicit request (2026-11-20). Work in "/Users/danielrose/Projects/Claude/Projects/Abs By AI" on the M2 (`ssh m2` if you start on the M6; never use the SMB share). Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md` and `Handoffs/handoff-20261120-wv-03-transfer-to-codex.md`, then finish round 8 of the Great Again T VSL (WV-03) exactly as that handoff lists: check the unattended final film chain, fix and resume it if it failed, run the watch pass, gates and a fresh independent review on the full film, fix what they find, build and test the round 8 review page (port 9830, silent checks then owner handoff), release the edit slot with --review and stop for my review. Dan's approvals and picks are in the files the handoff names; his words outrank any summary. Acquire the edit slot on the M2 before any new production. Report each step with eta.py.
