# Handoff 2026-11-20: Great Again T Upsell 1: Prepaid Packs (GAT Upsell 1 AD R3, job WV-04) moves from Claude to Codex

**Category: AD** (paid upsell video played on the Great Again T order page after someone buys one bottle; it sells the
6-bottle prepaid pack). Round 3, not yet delivered to Dan. Sidebar name: `GAT Upsell 1 AD R3`.

Dan, 2026-11-20 (relayed by his "Editing setup for Massachusetts trip" session): pause every active Claude edit and transfer it
to ChatGPT; Claude's weekly limit is nearly used up (resets Thu Nov 26) and he is upgrading to the $500 ChatGPT plan. This is
his explicit request to move this video to Codex. **Do not start until Dan's ChatGPT upgrade is active and he fires this.**

## Where everything is (all on the M2 Pro, the headless Mac with the drives)
- Job folder: `/Volumes/Expansion/_edit_work/WV-04/` (Seagate "Expansion").
  - `round3-plan/RESUME.md`: **read first.** Exact state, every file's status (which ones are stale), what each build
    changed, and the next action. Also `round3-plan/PLAN.md` (the round 3 plan) and `round3-plan/notes_r2.txt` (Dan's
    round 2 notes word for word).
  - `round3/`: the round 3 film, four independent reviews (`ROUND-3-REVIEW.md`, `-3B`, `-3C`, `-3D`) with evidence folders,
    `ROUND-3-NOTES.md`, AI frame pairs `frames/AI-A*/`, option clips `options/`, review page `review/`.
  - `film/recipe/`: the build (Python + bash). `film/work/`: EDL, graphics manifest, audio, logs.
  - `round2/`: round 2 (film sha `774c2f17...`, notes `ROUND-2-NOTES.md`, references `round2/frames/characters/`).
  - `key/`: the keyed green-screen plates. **Never re-key pieces A or B.**
- Source roll: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1904.MP4` (lav on audio 0:a:0, channel 0).
- Project copy for Dan's VLC: `Videos to Review/` in the project folder (a link onto the Seagate; the M6 reads the same file).
  The copy there now is the stale R3d build; replace it with the checked final.
- No edit slot is held and nothing is in the render queue for WV-04 (verified 2026-11-20).

## What Dan approved or decided (keep these)
- Round 1 picks (2026-11-16/17): **Matched colour**, **House bass voice**, the house green-screen key, background **Wood
  Kitchen 1**, product shot **A** (`round2/product/P01_codex_plate.png`).
- Round 2 notes, word for word in `round3-plan/notes_r2.txt`. In short: fewer, slower cuts (more continuous takes, "less
  frenetic"); more clip and graphic OPTIONS even if he rejects most; an after-man AI clip for "how you use Great Again T every
  day"; a pool clip ("the guy with abs who takes off his shirt at the pool, and his wife and kids admire him"); a full-screen
  product + ingredients graphic for cortisol/testosterone; full-screen "8 to 12 weeks"; the guarantee full screen with our seal;
  O01 bottles in a V; K05 styled like the real order page ("make it look more like what they're actually going to click on");
  end text "Tap the button below to upgrade your order".
- Standing rule he set 2026-11-19 (VIDEO-RULES top): in funnel videos the call to action is plain text with down arrows, never
  a button, pill or tap-target inside the video. The film follows it; the K05 order-page button picture is left as a question on
  the page because his R2 note asked for that look.
- Priority (2026-11-18): this edit ranks second on the M2, after the Great Again T VSL (WV-03).
- Review page preference from earlier in this edit: the full-screen button must work (shared helper; it was fixed in round 2).
- Approved round 2 graphics carried unchanged: G01 Warning card, G02 Difference card, P01 product shot.
- No AI clip motion is made until Dan picks a START/END pair (frame approval rule). None picked yet.

## Current state and exact next action
Four round 3 builds each got DOES NOT SHIP from a fresh reviewer; every must-fix was fixed in the next build. A fifth build
(R3e, film sha `bcead3c7d924ff675b8e38093466fb8545463bf49bcdbf6caf30c7f8c5ea8123`) finished rendering but its checks were stopped
by Dan's pause, so it is **unchecked**. Next, in order (full detail in RESUME.md, "Exact next action"):
1. `editroute.py pick` / `editcap.py acquire WV-04 --type AD` on the M2.
2. Checks on the R3e film (`film/recipe/check_film.py W1`, `audio_gate.py` with `--untreated ../work/voice_film.wav.audio_untreated.json`,
   `deliver/gate.py --format ad9x16`), all through the render queue.
3. One fresh independent review of the exact file against `ROUND-3D-REVIEW.md`'s must-fixes (pause sound at the take joins,
   the 4:04 take-start breath, take-start captions) plus a regression pass at every join.
4. If it ships: re-render the 5 option clips, update `review/inputs/extra.json` times, `make_inputs.py` + `build_page.py`, serve,
   silent checks then owner handoff, copy to `Videos to Review/` + `editroute.py push`, `editcap.py release WV-04 --review`,
   Edit Queue row delivered, board line, then tell Dan (title, link, revision list with times, What I decided).
   If it does not ship: fix only what the review lists and rebuild with `film/recipe/chain_r3c.sh` (EDL step commented out;
   uncomment it when `edl_build.py` changes).

## Build method, skills, traps
- Read: `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/ad-edit/SKILL.md`, `_shared/PRE-RENDER-APPROVAL.md`,
  `_shared/CUT-CONTINUITY-QC.md`, `_shared/framecheck/` (AI frame gate), `_shared/review_server.py` + `review_player.js`.
- Chain: `film/recipe/chain_r3c.sh` -> `chain_r3b.sh` (picture cuts, steps, audio, graphics `--render`) -> `chain_r3.sh` (two
  half renders, concat, checks) -> option clips. Full chain about 1.5 to 2 h on the M2 under load. Everything heavy goes through
  `renderq.py run --priority --group WV-04`.
- Recipe files: `edl_build.py` (take picks, join pauses), `plates.py` (`build_audio`: room tone, click repairs, breath dips,
  voice chain), `captions.py`, `graphics.py`, `r7card.template.htm`, `render_film.py`, `options_r3.py`, `timeline.py`.
- Traps hit this round (all fixed in R3e; do not undo):
  - Room tone must not be searched near each join (it pasted speech, then a breath, into pauses). R3e uses one clean 2 s sample
    from the roll's quietest stretch (roll 32.95 s), set to -57 dBFS RMS.
  - Join pauses stop 30 ms before any SPEECH in the source (-36 dB on the 5 ms lav envelope), inside the keyed plates.
  - The click finder can grab the next word: windows for the 2:25 click and 4:36 tick are measured on the 3 kHz band and pinned
    with `"fixed"`.
  - Caption words are dropped only when wholly inside a room-tone pause; `DROP` 602.96 and `START_FIX` 299.6 are deliberate.
  - Two cards in one shot overlapped (G01/G02): `graphics.plan` splits them by their own words.
  - Full-screen cards must hold to the next picture cut (a 2-frame flash otherwise).
  - The render queue starves light steps under memory pressure; a fix (max wait) landed 2026-11-19 (commit 11a46ca).
- Accepted gate rows (record them on the final file): audio tone (House bass) and edt (about 83 vs 80 ms, untreated about 77,
  nobody heard room); delivery style:coverage and change_rate (Dan wants fewer cuts); delivery junk:repeated_take near 6:08 is a
  false positive ("sixty-four dollars on ... every bottle", said once).
- AI frame pairs: passed/failed list in RESUME.md. Blind key `round3/review/inputs/blind_key.json` stays hidden from Dan.

## Review pages and what waits on Dan
- Round 2 page http://127.0.0.1:9813/ (reviewed by Dan). Round 3 page not given to Dan; its server (9877) was stopped at the
  pause and its content is the stale R3d build. Pages made on the M2 open on the M6 at the same link.
- Waiting on Dan once round 3 is delivered: AI pair picks, which extra graphic options go in, keep or remove the orange button
  picture on the K05 checkbox card, the exact tick-box words on the live upsell page (stand-in "Keep My Monthly Bottle Too").

## Starter prompt (Codex GPT-6.2 Sol, High; run from the project folder on the M2; only after Dan's ChatGPT upgrade is live)
```
You are taking over the video edit "Great Again T Upsell 1: Prepaid Packs" (GAT Upsell 1 AD R3, job WV-04), category AD,
round 3, from Claude. Dan moved it to you on 2026-11-20. Work on the M2 from the project folder. Read, in order:
Handoffs/handoff-20261120-wv04-transfer-to-codex.md, then /Volumes/Expansion/_edit_work/WV-04/round3-plan/RESUME.md,
round3-plan/notes_r2.txt, round3/ROUND-3D-REVIEW.md, .claude/skills/_shared/VIDEO-RULES.md and .claude/skills/ad-edit/SKILL.md.
Acquire the edit slot, run the checks on the unchecked R3e film, get one fresh independent review of the exact file, fix only
what it lists, then build, test and deliver the round 3 review page to Dan with the revision list and What I decided. Never
re-key pieces A or B; subscriptions only, $0 spend. Do not start round 4.
```
