# Ad 13 "The Cost Of Getting Abs", round 4: the horizontal's zoom steps and the square files

Written 2026-10-03 at the end of round 3; updated the same day with Dan's approval. Recommended: **Claude Opus 5.5, High**.
Sidebar name: `The Cost Of Getting Abs AD R4`. Previous: `handoff-20261002-ad13-round3-full-builds.md`.

Round 3 built everything Dan authorized and stopped on one page: **http://127.0.0.1:8817/**
(`/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review3/`; restart with
`python3 .claude/skills/_shared/review_server.py 8817 /Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review3`).
Nothing was uploaded. The approved vertical and its cut were filed in the ad folder on 10-03. The live horizontal (`-SuKGXGcbIg` / `hrQf1240kQA`) is untouched.

## What Dan answered (2026-10-03, verbatim; recorded with hashes in `B/review3/decisions.json`)

*"All right, everything is looking good. Everything is approved. Give me the handoff to install or upload these and
set these up."* No option was named, so each decision takes the page's recommended option:

1. Horizontal: **add the zoom steps** at Muhammad's cuts at 2:14.9, 3:02 and 3:40. The horizontal is not final until built.
2. P03 vertical: the mobile YouTube page capture is approved as built. No iPhone recording.
3. The square look is approved: **build the square full film and its 59 second cut.**
4. The vertical and its 59 second cut are approved. Already filed in the ad folder; their setup is its own handoff,
   `handoff-20261003-ad13-vertical-setup.md`. Do not rebuild or re-render them.
5. The horizontal's full-screen phone cards and closing button are approved.

## Delivered in round 3 (build dir `B` = `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13`)

| file | state |
|---|---|
| `B/i added up what getting abs was supposed to cost \| claude \| 9x16 \| ad 13.mp4` (4:04.878) | DELIVERY GATE PASS, 39 rows, 314 watch images judged, 0 defects. sha256 `4a6f058e...` (copy: `review3/masters/Ad 13 9x16 round 3 - full 1080x1920.mp4`) |
| `B/i added up ... \| claude \| 9x16 59s \| ad 13.mp4` (0:54.288) | DELIVERY GATE PASS, 39 rows, 79 watch images judged, 0 defects (`B/cut/gate_final.json`) |
| `B/round3/h16x9/DRAFT - Ad 13 16x9 Soft Blue Light round 3b - full.mp4` (4:04.878) | audio identical to his master (md5 `d7d65e94...`). Gate FAIL on one row (`cut:jump_cut`, his own cuts), 3 framing rows NOT MEASURED, 35 pass. Reviewer: pictures clean, 210 watch images, 0 defects. `ROUND-3-EDITOR.md`, `ROUND-3-REVIEW.md` beside it |
| `B/review3/square/` | square look only: stills of every graphic at 1:1 and a 35 s moving sample (`sq_look.py`). No square film exists |
| opener motion | `B/assets_sbl/opener_motion_9x16.mp4`, `B/round3/assets/opener_motion_16x9.mp4`; raw Kling takes and prompts in `B/round3/opener/`. First take of each used |
| P03 vertical | `B/assets_sbl/yt3min_phone_capture.mp4` (builder `B/round3/p03/shot.py`: m.youtube.com in iPhone emulation; the player is Dan's 4K page recording from 8.0 s) |

Recipe copies in the skill: `.claude/skills/shortad-from-longform/reference/ad13-r2/` (`sbl_copy.json`, `h16x9_full.py`,
`gen_opener.py`, `phone_screens.py`, `page3.py`, `page3_facts.json`). Lessons: `kit9x16/README.md`, section "The full
build on a master, in Soft Blue Light".

## What round 3 changed beyond the plan (all on the page under "What I decided")

- Lip sync at 3:48: picture segments 60 and 61 of `edl_picture.json` now point at roll 370.63 and 371.85 (were 266.9).
  **Never rerun the `kit` or `track` stage on this build**: `kit` rewrites that file, `track` drops the segment 51
  centring patch. Fixed copies: `B/round3/edl_picture.fixed.json`, `B/round3/facetrack.fixed.json`. Rerun with
  `B/round3/run_v4.sh` (graphics to prewatch) and `B/round3/run_cut.sh`.
- Every phone demo is the bare app screen in our card (`B/round3/phone_screens.py`, plus the two `*_screen2.mp4` crops of
  the WV-01 demos). `beats.json` carries a hand-added real label on the 2:28 phone card.
- `render.py` crop timing fixed (frame grid, seek origin). `sbl_graphics.py` card label spans fixed.

## Work for round 4, in order

1. Re-hash the locked files against `B/review3/decisions.json` before touching anything.
2. **Horizontal:** in `B/round3/h16x9.py` (skill copy `ad13-r2/h16x9_full.py`) add a small zoom step at his cuts at
   134.87, 182.15 and 220.19 s, and correct the one-frame lag (most talking shots run 33 ms behind his master;
   reviewer, round 3b). Build in a new `B/round4/h16x9/` folder; never overwrite the round 3b file. Then the watch
   pass, one fresh judge, the gate (`B/round3/h16x9/gate/run_gate.sh` as the model; the plan's `declare` block and
   `negative_events_scan` must be remade for the new file) and one `ra-reviewer` pass. The three `framing:*` rows
   need per-shot window data in the plan (`talking_head_windows`); add it or report them as not measured. Never move
   a bound. Audio stays his, stream-copied (md5 `d7d65e94c6167facd5c74bf64958337f`).
3. **Square files:** build the square full film and its 59 second cut from this vertical build (layouts
   `_shared/hyperframes/square.py`; the `/shortad-from-longform` skill's square section; Ad 10's AS-06 and Ad 6's
   AS-04 builds under `/Volumes/Extreme/_edit_work/kit9x16/` are the nearest worked examples). Use the bare-screen
   phone media and the label fixes from the vertical. Gate format `ad1x1`, judges, fold. The square opener is the top
   square of the vertical clip. The 59 second square uses the vertical cut's ranges (`B/cut_plan.json`).
4. **File what passes** in `Muhammad Ad Videos/i added up what getting abs was supposed to cost - ad 13/` (names:
   `... | claude | 16x9 | ad 13.mp4`, `... | claude | 1x1 | ad 13.mp4`, `... | claude | 1x1 59s | ad 13.mp4`), update the
   Edit Queue rows (AS-10), and add them to the setup: either run `/ad-setup` on them in a fresh task with
   `handoff-20261003-ad13-vertical-setup.md` as the model, or write a short setup handoff for them. The new
   horizontal is a NEW unlisted video and never replaces the live `-SuKGXGcbIg`.
5. One short round 4 page (the horizontal's three cuts before and after, the square films). Dan has approved the look
   of both, so the page asks only for a final yes on the finished files. Then the board and a handoff.

Done already on 2026-10-03: the vertical and its cut filed with stamps and `recipe-vertical/`; both opener clips
registered in the clip library (Drive ids `1fcVAJKpB9fdf-0NiDhZ4wbZBh5XVLUiX` 9:16, `1K5MGw2kHEt2bK9mPvTn7NWazDC_WpT0A` 16:9).

## Gate status, stated plainly

- Vertical full: PASS (stamp beside the file).
- Vertical 59 s: PASS. Its judge noted the same trainer clip appears twice
  9 seconds apart in the cut (far apart in the full ad).
- Horizontal: FAIL on `cut:jump_cut` (ten of his own same-framing cut pairs; the reviewer saw one real jump and two
  one-frame snaps, the rest hidden by flashes or not visible). Three framing rows not measured. This is Dan's decision 1.

## Cost ledger (this video)

Rounds 1 and 2: under one cent paid, plus Codex subscription images. Round 3: two Kling v3 standard clips, 4 s each,
about $1.36 (Replicate; exact figure not read back from billing), cutdown picker $0.38, physique checks $0.0015.
Total about $1.75 of the $5 cap. No retries were needed.

## Traps

- `.claude/skills/shortad-from-longform/reference/render.py` is uncommitted on purpose: it holds round 3's two crop
  timing fixes AND another session's unfinished "vertical-land-then-hold" edits (it now refuses a `facetrack.json`
  without that policy). This build keeps its own working copy at `B/render.py`. Whoever finishes the landing work
  commits the file with both. `kit9x16/master_to_sbl.py` is still uncommitted for the same reason (Ad 6 session).
- The Extreme drive had 3.7 GB free at the start of round 3; it has about 70 GB now. `B/round3/judged_v*/` (2 GB) and
  `B/round3/h16x9/hf*` (3 GB) can go once Dan approves.
- At most two builds at once; the machine ran at load 100 to 400 during round 3 and a full vertical pass took about
  an hour. Run gates detached. No em dashes.

## Starter prompt

> Read `Handoffs/handoff-20261003-ad13-round4-after-round3-page.md` and the files it lists. Name this session "The
> Cost Of Getting Abs AD R4". I approved everything on the round 3 page. Build what is left: the horizontal with the
> zoom steps at Muhammad's three cuts and the one-frame fix, and the square full film and its 59 second cut. Gate,
> judge and review them, file what passes in the ad folder, and show me one short round 4 page. Do not upload anything.

Model and effort: Claude Opus 5.5, High.
