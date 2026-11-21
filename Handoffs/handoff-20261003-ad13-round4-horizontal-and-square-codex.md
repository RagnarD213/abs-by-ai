# Ad 13 "The Cost Of Getting Abs", round 4: the horizontal's zoom steps and the square files

Written 2026-10-03 at the end of round 3, rewritten 2026-10-04 for **Codex** at Dan's request. Recommended:
**GPT-6.1 Sol, High** (a bounded build on a locked look: timeline, render and gate work; no open creative choices).
Sidebar name: `The Cost Of Getting Abs S/Sh Ad R4`. Previous round: `handoff-20261002-ad13-round3-full-builds.md`.

Dan, 2026-10-03, on the round 3 page: *"All right, everything is looking good. Everything is approved. Give me the
handoff to install or upload these and set these up."* On 2026-10-04: *"Change both of these handoffs to be for Codex."*
Recorded with file hashes in `B/review3/decisions.json` (`B` = `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13`).

**Where things are.** This handoff, the kit scripts and the ad folder are in the MAIN project folder,
`/Users/danielrose/Documents/Claude/Projects/Abs By AI/`. Round 3's fixes to the kit (`sbl_graphics.py`, `render.py`,
the README lessons, `ad13-r2/h16x9_full.py`) and this handoff are NOT on GitHub: the main folder's push is stopped (see
Traps). A fresh worktree will not have them. **Run the kit scripts from the main folder by absolute path, and read and
write the build on the Extreme drive by absolute path.** Every relative path below is relative to the main folder.

Read first: `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (in full), `Handoffs/video-editing/00-RULES.md` (Codex
column and environment table; the environment traps are in `Handoffs/handoff-20260914-ad3-square-codex.md` section 2),
`.claude/skills/shortad-from-longform/SKILL.md`, and in
`.claude/skills/shortad-from-longform/reference/kit9x16/README.md` the sections "The full build on a master, in Soft
Blue Light" (this build's own lessons) and "Ad 6 round 2 lessons" (the square renderer). `B/round3/h16x9/ROUND-3-EDITOR.md`
and `ROUND-3-REVIEW.md` for the horizontal. The round 3 page is at http://127.0.0.1:8817/ (`B/review3/`; restart with
`python3 .claude/skills/_shared/review_server.py 8817 /Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review3`).

## What Dan approved (no option was named, so each decision takes the page's recommended option)

1. Horizontal: **add the zoom steps** at Muhammad's cuts at 2:14.9, 3:02 and 3:40. The horizontal is not final until built.
2. P03 on the vertical: the mobile YouTube page capture, approved as built.
3. The square look: approved. **Build the square full film and its 59 second cut.**
4. The vertical and its 59 second cut: approved and already filed in the ad folder. Their setup is its own task,
   `handoff-20261003-ad13-vertical-setup-codex.md`. **Do not rebuild, re-render or re-mux them.**
5. The horizontal's full-screen phone cards and its closing button: approved.

## State of the build

| file | state |
|---|---|
| `B/i added up what getting abs was supposed to cost \| claude \| 9x16 \| ad 13.mp4` (4:04.878) | LOCKED. Delivery gate PASS, 39 rows. sha256 `4a6f058e203dbd41965f34b0ebc4b5d1c9a90badf0bec96bd9afda1da472df60` |
| `B/i added up ... \| claude \| 9x16 59s \| ad 13.mp4` (0:54.288) | LOCKED. Delivery gate PASS, 39 rows. sha256 `8bb442a0331c9884a49472bea1678ca41ab4f787922a724c4d0aba65f2bfc5e7` |
| `B/round3/h16x9/DRAFT - Ad 13 16x9 Soft Blue Light round 3b - full.mp4` (4:04.878) | look approved; NOT final. Audio identical to his master (md5 `d7d65e94c6167facd5c74bf64958337f`). Gate: 35 rows pass, `cut:jump_cut` fails (his own cuts), three `framing:*` rows not measured. Reviewer: pictures clean, 210 watch images, 0 defects |
| `B/review3/square/` | the approved square LOOK only (stills of every graphic at 1:1, a 35 s sample; `sq_look.py`). No square film exists |

Recipe copies in the skill: `.claude/skills/shortad-from-longform/reference/ad13-r2/` (`sbl_copy.json`, `h16x9_full.py`,
`gen_opener.py`, `phone_screens.py`, `page3.py`). The horizontal's builder is `B/round3/h16x9.py` (same file as
`ad13-r2/h16x9_full.py`).

**Hand fixes in `B` that a rerun must not undo:**
- `edl_picture.json` segments 60 and 61 point at roll 370.63 and 371.85 (the take his audio uses; lip sync at 3:48).
  **Never rerun the `kit` or `track` stage on this build**: `kit` rewrites that file, `track` drops the segment 51
  centring patch in `facetrack.json`. Fixed copies: `B/round3/edl_picture.fixed.json`, `B/round3/facetrack.fixed.json`.
- `beats.json` carries a hand-added real label on the 2:28 phone card.
- Every phone demo is the bare app screen in our card (`B/assets_sbl/*_screen*.mp4`, built by `B/round3/phone_screens.py`).
- `B/render.py` is this build's own working copy of the renderer, with the round 3 crop timing fixes.

## Work, in order

1. **Re-hash the two locked files** against the table above before touching anything. Claim the job:
   `python3 scripts/edit-queue/queue.py set AS-10 in_progress --by "Codex"`, and one short board line.

2. **Horizontal.** Copy `B/round3/h16x9.py` to `B/round4/h16x9.py` and build in a new `B/round4/h16x9/` folder; never
   overwrite the round 3b file.
   - Add a small zoom step at his cuts at **134.87, 182.15 and 220.19 s**, so each reads as a deliberate change of
     framing instead of a jump (the same size step the vertical's joins use, about 15 to 20 percent, landing ON the cut
     frame). The other seven pairs the gate lists are hidden by his flashes or are not visible (the reviewer checked
     each one, table in `ROUND-3-REVIEW.md`): leave those as his master has them unless the gate still fails on a
     visible one.
   - Correct the one-frame lag: most talking shots run one frame (33 ms) behind his master (reviewer, round 3b).
   - Audio stays his, stream-copied whole. Assert the audio md5 above on the new file. 7,339 frames.
   - No burned captions (his master has none; the plan's `declare` block says why). No AbsByAI.com end mark.
   - Then, on the new file: your own watch of the changed spans, the audio gate (`--reference-mix <his master>
     --verbatim`), the watch pass, a **fresh Codex subagent or second session** as the watch judge (every sheet, strip
     and pair image gets a verdict; brief in the `JUDGE_PROMPT.md` the watch pass writes), a 30-frame negative-events
     sheet (`kit_negscan.py sheet`, then `record`), and the delivery gate `--format ad16x9` run detached.
     `B/round3/h16x9/gate/run_gate.sh` and `gate_plan.py` are the model; the plan's `declare` block,
     `negative_events_scan` and `watch_log` are tied to a file's hash and must be remade for the new file.
   - The three `framing:*` rows need per-shot window data in the plan (`talking_head_windows`); add it honestly or
     report them as not measured. **Never move a bound, never add a `known_gap`.**
   - One **independent reviewer** (a fresh Codex session that has not read your notes) watches the finished file
     against Muhammad's master and writes `ROUND-4-REVIEW.md` with SHIP or DOES NOT SHIP.

3. **Square files.** Build the square full film and its 59 second cut from the locked vertical build with the kit's
   square renderer: `sq_render.py` + `sq_plan.py` in `kit9x16/` (commands in their docstrings; stages `fit`,
   `graphics`, `picture`, `mux`, then `--cut` for the 59 second square from the vertical's `B/cut_plan.json`). It
   writes its own folder; give it `B/round4/square/`. Worked examples from this week: Ad 6
   (`/Volumes/Extreme/_edit_work/kit9x16/as04-ad6-sq/`) and Ad 10 (`handoff-20261002-ad10-square-round2-full-builds.md`).
   - Match the approved look in `B/review3/square/` (stills and sample). The square opener is the top square of the
     vertical opener clip. Phones use the bare-screen media, and the real-picture labels at 2:28 and 3:51 must show.
   - Audio is the vertical's stream, md5 asserted. **Mux before gating** (README trap). Never render the square while
     anything is rewriting the vertical's `captions.mov`; nothing should be, the vertical is locked.
   - Gate format `ad1x1` (`FORMAT=ad1x1` for `kit_fold.sh`), watch pass, fresh judges for both files, fold. Keep each
     judged round's `watch/` before any re-render (README: "Keep the judged round before re-rendering").

4. **File what passes** in `Muhammad Ad Videos/i added up what getting abs was supposed to cost - ad 13/`, named per
   `00-RULES.md`: `... | codex | 16x9 | ad 13.mp4`, `... | codex | 1x1 | ad 13.mp4`, `... | codex | 1x1 59s | ad 13.mp4`,
   each with its gate stamps, a `REVIEW 540p` copy and a recipe folder. The new horizontal is a NEW deliverable and
   never replaces the live `-SuKGXGcbIg`.

5. **One short round 4 page for Dan** on a new port (`review_server.py`, never `python3 -m http.server`; seek in one
   player before sending): the three finished files, the horizontal's three cuts before and after, a "What I decided"
   list, and one question only: a final yes on the finished files. He has already approved both looks.
   `python3 scripts/edit-queue/queue.py set AS-10 delivered --by "Codex"`, then `queue.py push`.

6. **Close the round** with a board line and a setup handoff for these three files, modelled on
   `handoff-20261003-ad13-vertical-setup-codex.md` (same group `204553316830` in the trial campaign `24316364155`, a
   1:1 thumbnail in the 13-R3B design, the new horizontal as a new Unlisted video and a new ad). Do not upload anything
   in this task.

## Cost ledger (this video)

Rounds 1 to 3: about $1.75 of the $5 cap (two Kling opener clips about $1.36, the cutdown picker $0.38, small checks).
Round 4 needs no generation. The square's 59 second cut reuses the vertical's ranges, so no picker call.

## Traps

- `.claude/skills/shortad-from-longform/reference/render.py` in the main folder is uncommitted on purpose: it holds
  round 3's crop timing fixes AND another session's unfinished "vertical-land-then-hold" edits (it now refuses a
  `facetrack.json` without that policy). Do not revert it and do not commit it; this build uses `B/render.py`.
  `kit9x16/master_to_sbl.py` is uncommitted for the same reason.
- The main project folder's push has been stopped by other sessions' uncommitted edits since 10-01 (see the board).
  From a Codex worktree, commit only your own files and push with plain git. Do not touch the unpushed kit commits.
- At most two video builds at once across the machine; it ran at load 100 to 400 during round 3 and a full pass took
  about an hour. Run gates detached; two gates at once stall each other.
- The Extreme drive has about 70 GB free. `B/round3/judged_v*/` (2 GB) and `B/round3/h16x9/hf*` (3 GB) may be deleted
  if space runs short; nothing else in `B`.
- ffprobe is not on PATH: use `Media/video_edit/bin/ffmpeg`. exFAT: skip `._*` files in globs.
- An ad never goes organic and never uploads Public. Nothing is uploaded in this task.
- No em dashes in anything written.

## Starter prompt

> Read `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20261003-ad13-round4-horizontal-and-square-codex.md`
> and the files it lists. Name this session "The Cost Of Getting Abs S/Sh Ad R4". I approved everything on the Ad 13
> round 3 page. Build what is left: the new horizontal with zoom steps at Muhammad's three cuts and the one-frame fix,
> and the square full film and its 59 second cut. Gate, judge and independently review them, file what passes in the ad
> folder, and show me one short round 4 page. Do not rebuild the approved vertical. Do not upload anything. No em dashes.

Model and effort: GPT-6.1 Sol, High.
