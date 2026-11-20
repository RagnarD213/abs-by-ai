AD (Great Again T upsell video). Task name: `GAT Upsell 2 AD R2`.

# Great Again T Upsell 2: Eternal Burn AM/PM (WV-05), round 2: transfer from Claude to Codex (2026-11-20)

**Why this exists.** Dan, 2026-11-20: "Can you message all active edits here and tell them to pause work and create a handoff document to
transfer the edit to ChatGPT?" Only Joint Vigor stays on Claude. Claude's weekly limit resets Thu Nov 26; Dan is moving to the $500
ChatGPT plan. This is his explicit request to move this video to Codex. **Model: Codex GPT-6.2 Sol, High effort.** Do not start until Dan's
ChatGPT upgrade is active. Round 2 continues; this is NOT a new round and nothing Dan approved is reopened.

## 0. Where it is
- **Mac: the M2** (headless; moved from the M6 at Dan's request on 2026-11-19). Job folder: **`m2:/Volumes/Extreme/_edit_work/WV-05`**.
  The old M6 copy is kept untouched as `~/Projects/_edit_work/WV-05.moved-to-m2-20261119` on the M6 (do not use, delete nothing).
- From the M6 project, run every job command through the router so it executes on the M2:
  `python3 .claude/skills/_shared/editroute/resume.py run WV-05 -- <command>` (its cwd is the M2 repo
  `/Users/danielrose/Projects/Claude/Projects/Abs By AI`; `cd /Volumes/Extreme/_edit_work/WV-05/...` inside `bash -c`). Or `ssh m2` directly.
- M6 side folder for browser/Flow work: `~/Projects/_edit_work/WV-05-flow` (motion/, frames/). M2 mirror of frames: `m2:~/Projects/_edit_work/WV-05-flow/frames`.
- Edit slot: **released** (paused by Dan). Run `editcap.py acquire WV-05` on the M2 (via resume.py) before any render. Every heavy step goes through
  `renderq.py run --group WV-05 -- ...` on the M2.
- One native 9:16 film (1080x1920, 29.97 fps), Dan on green screen keyed over Wood Kitchen 1, roll C1904 13:45-30:31 of the 11/13 shoot
  (`/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1904.MP4` on the M2).

## 1. Read first
- `round2-plan/RESUME.md` (state, "PAUSED" section at the end), `round2-plan/decisions.json`, `round2-plan/notes_r1.txt`.
- `Handoffs/video-editing/WV-05-round-2-revisions.md` (the round 2 brief, Dan's round 1 words verbatim in section 1).
- `round1/ROUND-1-NOTES.md`, `round1/ROUND-1-REVIEW.md`, `round2/ROUND-2-REVIEW.md` (independent review of the first R2 draft).
- `.claude/skills/_shared/VIDEO-RULES.md` (top sections; "Funnel sales videos: the call to action is text with arrows pointing down",
  Dan 2026-11-19), `.claude/skills/ad-edit/SKILL.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/_shared/cliplib/README.md`,
  `.claude/skills/_shared/veo/README.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`, `.claude/skills/_shared/framecheck/` README.

## 2. Approved by Dan (locked; never reopen)
- Dan's round 1 review, 2026-11-19 (verbatim in the round 2 brief, section 1): "first minute looks good", "Let's go with match color",
  "Match or the house-based voice" (= House bass, Wispr Flow), "all graphics are looking good".
- First minute as cut: `round1/GAT Upsell 2 AD R1 - First Minute.mp4` sha256 `b4b7f63907dd369d37fc624a73bdad1b4757ff4c04a56211f096326f3861fab9`.
- Colour **Matched**: `look/LOOK.json` (recommended = matched) sha256 `bba45452fb9bf804e87f564d8f7ffa3717f917bf800cc4ce5d16c3c5f92fbb8a`.
- Voice **House bass**: `look/VOICE.json` (recommendation = C-house-bass) sha256 `c1f540e5f49ce1e9b88a84a47c0493719ee50957ecde5b40e2fed9739ad6faa6`.
- Green-screen key: all 68 pieces K001-K068 keyed (`key/pieces.json` sha256 `07788dd9bddbb3488caa867a9eeb4cb77c61b31a40abec2655b5275b1e7aac8c`).
  **Never re-key.** The `key/K0xx.done` markers and frame-gate stamps hold old M6 paths: leave those records as they are.
- All 15 round 1 graphics (K01, S01, P02, P03 garcinia photo A, K02, S02, T01-T05, O02, K03 ...) approved, EXCEPT the old "Accept Offer"
  button and pill, replaced under the standing CTA rule.
- Dan's standing preferences for this video (his words, round 1): "we don't want to make this as busy as the main VSL", "we don't want any
  frenetic fast cuts", "I want to see some options. Even if you aren't completely sure, I'll accept them", "I can always reject what doesn't
  make sense", "Keep it trustworthy, but give me some more options so that it's not just so much straight camera scene."
  Reading used: each option at least about 4 s, at least about 3 s of Dan on camera between full-screen items.
- Upsells WV-04 to WV-07: cleaner than the VSL, more Dan on camera, fewer AI clips, larger cards (memory `gat-upsells-cleaner-more-camera`).

## 3. Decisions made in round 2 (Claude's defaults; overrule-able on the page)
- **CTA (C01)**: text "Click The Button Below / To Try Eternal Burn" (line 2 cyan) with 2 pulsing down chevrons, no button/pill, from
  seg 164 ("click..." line, film about 8:43) to the last frame, kind "top" so it stays on over the N11 card. Why: Dan's own wording for the
  same fix on Upsell 4 ("Click the button below to try Abs By AI"), with this product named. Alternative noted: "Click Accept Offer Below"
  (his spoken line). Layout fixed after review D2: text y 1612/1686 at 56 px, chevrons y 1764, gap 22, width 56; lowest pixel 1839 (keep <= 1840).
- **Pauses**: breath restored at the two paragraph breaks (film about 0:12.7 "results. / But before", 0:37.6 "used to. / We've helped")
  and before "Other men" (0:56.7); the film's last words end on their decay with a 0.25 s audio fade. (Round 1 decision 3, unanswered.)
- **Garcinia**: photo A stays in the film; B offered again (round 1 decision 6, unanswered).
- **Drain clip E01 (2:12)**: both round 1 frame pairs offered again (unanswered).
- **Eight new full-screen card options in the film** (Keep/Reject each), all Soft Blue Light, opaque, word-timed:
  N02 The One Thing They Did Differently (starts on "one thing", about 1:14), N03 The Belly Fat Cycle (1:40), N04 Two Critical Jobs (2:48),
  N05 Why Two Bottles (starts on "one set of ingredients", about 3:15), N06 Eternal Burn AM Ingredients (3:59, ends where K02 starts),
  N07 Eternal Burn PM Ingredients (4:56), N10 Your Potential 60 To 70% (7:32; solid grey bar to 60% + hatched band to 70% vs full "Complete"),
  N11 When It Arrives AM/PM (8:49, content above y 1450 so the CTA stays visible). Ingredients checked against the real labels:
  AM (VTL4FATB): Garcinia cambogia 50% HCA, CLA, MCT oil, L-Carnitine, Chromium, no caffeine. PM (JTP4SLEE): Valerian, Chamomile, GABA,
  L-Tryptophan, Lemon balm, Passion flower, Melatonin 2 mg.
- **Review notes not changed (tell Dan on the page)**: D3 (reviewer called N10 a printed numbered claim) kept as an option because it shows
  Dan's own spoken line "60 to 70% of your potential"; D5 K02 (approved) lands right after N06, so a long run of graphics there (Dan is on camera behind K02).

## 4. Current state (paused 2026-11-20 about 09:20 Central)
- **Done**: EDL rebuilt with the breaths, the ending, and review fix D1 (a false-start "Plus" after "HCA." at 4:03 cut; "Plus it has MCT oil"
  gets a 0.13 s natural lead). `film/work/edl/edl_tight.json` 184 segments, 603.84 s, sha256 `3da4f894fc8de52d8528ce01807138ad746a04a4544e0ce029de939716dc5a10`.
  Soundtrack rebuilt and length-checked: `film/work/voice_film.wav` 603.837 s, sha256 `836338ce7f9c93487e1b57f074d15a2e799e73729fdbd0b602f9de332d397bc8`.
  Picture cuts rebuilt (`edl_picture_final.json`). Graphics manifest re-planned. All 9 new renders done in `film/work/hf/shared/renders/`
  (N02 N03 N04 N05 N06 N07 N10 N11 C01), including the review fixes. Stills: `round2/stills/`.
- **NO current full draft exists.** The R2b full render was stopped about halfway by the pause. The first R2 draft (sha `4ca4e4b5...`, the
  one reviewed in ROUND-2-REVIEW.md) was overwritten by a move step. `round2/superseded/DO NOT USE - R2b render with OLD soundtrack, out of
  sync after 4m03s.mp4` (sha `2f1e94aa...`) is broken: never use or show it.
- **Wives clip E02 (0:26-0:32)**: motion made on the paid fallback (see section 6): 4 takes in `round2/motion/takes/`
  (E02x1-api-t1/t2 from pair X1, E02x2-api-t1/t2 from pair X2; 1080x1920, 6 s, 24 fps; sha256 in `round2/motion/takes/job.json`,
  sha `5bf89c5f...`). Motion gate (clipcheck) and frame-reviewer NOT run. Not filed in the clip library yet.
  The frames are `round1/frames/E02/{codex,google}/START|END.png`, copied to `round2/motion/frames/E02`.
- **New AI clip ideas (START/END pairs, two blind pairs each)**, briefs in `<frames>/<ID>/idea.json`:
  N01 bottles being packed (0:08, Dan asked), N12 Eternal Burn added to the same box (8:46), N08 waking up the way you did at 25 (5:35),
  N09 the bag of chips at 9 at night (5:54).
  - Codex pairs PASS gate + fresh reviewer + verify: N01, N08, N09 (`~/Projects/_edit_work/WV-05-flow/frames/<ID>/codex` on the M6).
    N12 Codex: 3 pairs failed (every Codex edit re-renders the table: bottle scale, box, hands, colour); 16 of about 20 Codex images used.
  - Google pairs (paid Gemini image API, model gemini-3-pro-image, about $0.134/image): N08 and N09 generated (N09 gated on the M2, no
    reviewer); N01 and N12 only raw tries. Logs in each `attempts.log`.
- **Spend this round**: Veo API $2.40 + Gemini image API about $1.34 = about $3.74 (inside the $25/session authorization). Flow credits: 0.
- Review page: builder ready at `round2/review/build_page.py` (side player, decisions, changes with timestamps, Keep/Reject per option, E02
  takes side by side, AI pairs, auto-filled reply). `round2/review/inputs/page.json` NOT written yet. Round 1 page was http://127.0.0.1:9877/ (M6).
- Edit Queue: WV-05 `blocked`, needs "Dan says resume"; set it back to in_progress when you start (`scripts/edit-queue/queue.py`).

## 5. Exact next actions
1. `editcap.py acquire WV-05` on the M2; `eta.py plan WV-05 ...`.
2. Full draft render + checks: `cd film/recipe && renderq.py run --group WV-05 -- bash chain_r2_full.sh > ../work/chain_r2c.log 2>&1`
   (audio is already rebuilt; the chain moves any existing draft to superseded, renders `round2/GAT Upsell 2 AD R2 - Full Draft.mp4`,
   then check_film, audio gate, seamscan, caption proof). About 2 h on a busy M2. Do NOT set `CARDS` (cards are done).
   Fix the chain's move step first so it never overwrites an earlier superseded file (use a dated name).
3. Fresh independent review of the new file against the brief (ROUND-2-REVIEW.md's D1/D2/D4/D6 should be gone); fix what it finds.
4. E02 takes: `framecheck/clipcheck.py TAKE.mp4 --spec <frames>/E02/<codex|google>/spec.json` (X1 = the pair in `codex/`, X2 = `google/`;
   never put that mapping on a page), then a fresh independent frame review per take and `--review`, `--verify`.
5. Finish the Google pairs for N01, N08, N09, N12 (Flow first if uploads work for you; else the documented Gemini API fallback with
   `ALLOW_API_IMAGE=1`), gate + fresh reviewer each. N12 has no usable Codex pair, so its Google pair is the only one.
6. File every AI take before the review pause: all 4 E02 takes (used or not) in `07 AI Generation Source Archive` + `source-register.json`
   on the M2 under `clip_library.catalog_lock()`; keepers via `clip_library.py add` after approval (cliplib README).
7. Review page: write `round2/review/inputs/page.json` (pattern: `round1/review/make_inputs.py`), run `build_page.py`, serve with the
   shared review server, test at 800 and 1150 px in silent check mode, then hand over paused with sound ready.
   On the page: the CTA wording and its alternative; the breath changes with watch buttons (0:12.7, 0:37.6, 0:56.7, end); D1 fix at 4:03;
   each N card with Keep/Reject; E02 four takes side by side; new AI pairs (X1/X2 blind); E01 pairs; garcinia B; notes for D3/D5;
   N12's both-hands START (both bottles carried in so neither pops in from nowhere) and the single whole-frame colour match on its Codex END
   (no pixel edits) if that pair is shown; "What I decided".
8. `editcap.py release WV-05 --review`, `queue.py set WV-05 delivered` + artifact db mirror (https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs),
   board line, `scripts/git/safe-push.sh`, two wrap-up boxes.

## 6. Traps hit in this round
- **Flow uploads do not work from this M6 for automation**: Claude's Chrome extension cannot reach Flow's file chooser, computer use is
  read-only for Chrome, and Codex's native picker failed twice ("Sky Computer Use native pipe startup failed"; first try failed only because
  the screen was locked). Evidence: `~/Projects/_edit_work/WV-05-flow/motion/CODEX_REPORT.md`. Also a mounted Chrome installer disk image
  (`/Volumes/Google Chrome`) makes `com.google.Chrome` ambiguous for Sky: target `/Applications/Google Chrome.app` by path. Flow project
  "WV-05 R2 motion E02" (https://flow.google.com/project/af20ca53-1494-41af-93ba-0f7ac5c945f4) is empty.
- `veo.py api` downloads fine but crashes recording the take if `ffprobe` is not on PATH (add `Media/video_edit/bin`).
- `ssh` non-interactive on the M2 lacks `/usr/local/bin`: HyperFrames needs `npx` there (`export PATH="/usr/local/bin:$PATH"`).
- `edl_build.py` now matches each segment to its source piece by midpoint and takes the key piece from `key/pieces.json` (with a
  check that every extent sits inside keyed frames); `SRC_OUT` / `BREATH_LEAD` / `END_OUT` hold the round 2 changes.
- Never call `plates.build_audio` through nested shell quoting; use `chain_r2b_audio_and_film.sh` style (it asserts wav length = EDL length).
  A render with a stale soundtrack still passes "audio vs picture length" if the wav is longer, so check the wav first.
- The M6 render queue was parked for long stretches by the Joint Vigor priority reservation; the M2 queue is often full (WV-03, WV-04).
- Audio gate fails only "tone" (+7.6 dB at 80 Hz): that is the approved House bass voice; round 1 failed the same row.
- check_film's 21 caption-box edge flags are all on the approved garcinia photo P03 (3:34-3:40).

## 7. Starter prompt (Codex GPT-6.2 Sol, High; fire only after Dan's ChatGPT upgrade is active)
```
AD (Great Again T upsell video). GAT Upsell 2 AD R2. Dan moved this edit from Claude to you (2026-11-20). Read
Handoffs/handoff-20261120-wv05-transfer-to-codex.md in full, then continue round 2 of "Great Again T Upsell 2: Eternal Burn AM/PM"
(WV-05) on the M2 at /Volumes/Extreme/_edit_work/WV-05, starting at section 5 step 1. Nothing Dan approved is reopened; never re-key.
Render the full draft, run every check and a fresh independent review, check and file the wives-clip takes, finish the AI picture
pairs, build and test the review page, then hand it to Dan with the two wrap-up boxes. Dan authorized this round's work and the paid
fallbacks within the $25/session cap; do not stop to ask.
```
