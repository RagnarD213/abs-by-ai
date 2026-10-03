# Ad 13 "The Cost Of Getting Abs", round 4: Dan's round 3 answers, the square files, the horizontal's last fixes

Written 2026-10-03 at the end of round 3. Recommended: **Claude Opus 5.5, High**.
Sidebar name: `The Cost Of Getting Abs AD R4`. Previous: `handoff-20261002-ad13-round3-full-builds.md`.

Round 3 built everything Dan authorized and stopped on one page: **http://127.0.0.1:8817/**
(`/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review3/`; restart with
`python3 .claude/skills/_shared/review_server.py 8817 /Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review3`).
Nothing was uploaded. Nothing was filed in the ad folder. The live horizontal (`-SuKGXGcbIg` / `hrQf1240kQA`) is untouched.

## What is waiting for Dan (5 decisions, on the page)

1. Horizontal: add a zoom step at three of Muhammad's own cuts (2:14.9 visible jump, 3:02 and 3:40 one-frame mouth
   snaps), or leave them as his live ad has them. Recommended: add.
2. P03 vertical: approve the mobile YouTube page capture, or allow iPhone Mirroring so the app itself is recorded
   (the app shows the 4.47M subscriber count; the mobile web page does not). The access request was declined on
   screen in round 3; do not paint a subscriber count onto the capture.
3. The square look (first square in Soft Blue Light): approve so the square files can be built.
4. The finished vertical and its 59 second cut: approve for setup, or notes.
5. The horizontal's two new layouts: full-screen phone cards where Muhammad had phones beside Dan, and the closing button.

## Delivered in round 3 (build dir `B` = `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13`)

| file | state |
|---|---|
| `B/i added up what getting abs was supposed to cost \| claude \| 9x16 \| ad 13.mp4` (4:04.878) | DELIVERY GATE PASS, 39 rows, 314 watch images judged, 0 defects. sha256 `8bb442a0...` (copy: `review3/masters/Ad 13 9x16 round 3 - full 1080x1920.mp4`) |
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

1. Record Dan's answers verbatim with scope in `B/review3/decisions.json` (format: `B/review2/decisions.json`).
2. **Horizontal, if he picks the zoom steps:** in `B/round3/h16x9.py` add a punch step at his cuts at 134.87, 182.15 and
   220.19 s, and correct the one-frame lag (most talking shots run 33 ms behind his master; reviewer, round 3b). Re-run
   the watch pass, one judge, the gate (`B/round3/h16x9/gate/run_gate.sh`; the plan's `declare` block and
   `negative_events_scan` are already set), and one `ra-reviewer` pass. The three `framing:*` rows need per-shot
   window data in the plan (`talking_head_windows`); add it or report them as not measured. Never move a bound.
3. **Square files, if he approves the look:** build the square full film and its 59 second cut from this vertical
   build (layouts `_shared/hyperframes/square.py`; the `/shortad-from-longform` skill's square section; Ad 6's AS-04
   build `/Volumes/Extreme/_edit_work/kit9x16/as04-ad6-sq/` is the nearest worked example). Gate format `ad1x1`,
   judges, fold. The square opener is the top square of the vertical clip.
4. **P03, if he wants the app:** `request_access` for iPhone Mirroring, record the YouTube app playing `GJHDRlepMTM`
   at about 0:08 to 0:16 in portrait, swap `yt3min_phone` in `sbl_copy.json` (new file name), re-render that span.
5. **When the vertical and its cut are approved:** `kit_run.py ... --from deliver --deliver "Claude Ad Videos/<ad 13
   folder>"` (naming per memory `ad2-vertical-approved`), register the two opener clips in the clip library
   (`clip_library.py add ... --status used-final --used-in "Ad 13 AV-11"`), update the Edit Queue rows AV-11 and AS-10,
   and write the `/ad-setup` handoff (Unlisted YouTube + Google Ads; the new horizontal is a NEW video, never a
   replacement of the live one).
6. One round 4 page with only what changed; then the board and a handoff.

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
> Cost Of Getting Abs AD R4". My answers to the round 3 page are: <paste>. Record them, then do what they authorize:
> the horizontal's zoom steps and one-frame fix, the square files if I approved the look, and the delivery of the
> vertical and its 59 second cut into the ad folder if I approved them. Show me one round 4 page with only what
> changed. Do not upload anything.

Model and effort: Claude Opus 5.5, High.
