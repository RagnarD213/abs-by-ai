AD (paid ad: it ends on "Tap the button below now to get started"). Sidebar name for the next task: `Best Ab Exercise AD R3`.

# RA-06 "What's The Best Ab Exercise?": round 3, after Dan reviews the AI clip frames

**Written 2026-10-14 by the round 1/2 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-06-whats-the-best-ab-exercise.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (read the two 2026-10-14 sections at the
top: scripted claim lines are pre-approved; never a shot of Dan just standing around), `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe: `.claude/skills/ad-edit/reference/ra06/` (README: stage order and ten lessons). Work dir `/Volumes/Extreme/_edit_work/ra06/`.
Supersedes `Handoffs/handoff-20261014-ra06-round2-after-dan-review.md` (written before Dan answered round 1).

**Do not fire this until Dan has replied to the frames page: http://127.0.0.1:8836/** (folder `ra06/round2/`).
His frame verdicts go word for word into `ra06/round3-plan/decisions.json` before anything is built.

## What Dan already decided (round 1, recorded word for word in `ra06/round2-plan/decisions.json`)

| item | his answer | what to build |
|---|---|---|
| colour | "let's go with the C2 brighter gold" | keep `grade.json` (C2 re-baked for C1664) |
| shot size | "let's go with pair 3. Also, the close is looking a little off-center. Just center that close a little bit more." | `framing_choice.json` = close 684x1216, wide 846x1504 (landmark conversion in `look/crops.json`); see "Centre the close" below |
| voice | "Use a bass lift on the voice." | keep `mix.wav` (bass lift + the three `RIDE`s in `s08_audio.py`) |
| claim lines | "Claim lines are okay, and going forward, you don't need to ask me..." | keep all; never ask again (new standing rule) |
| S1 split screen | "I like this, but make sure this is color corrected. This footage looks very dark. And also make sure I'm actively doing the vacuum when you show, not just standing around." | brighter panels; the vacuum panel shows the draw-in itself |
| B1 poses clip | "Remove B1. That doesn't make any sense or add any value to the video..." | pose card out; Dan on camera there (or an approved AI clip) |
| C1 button | change the text to "Tap the button below to start training with AI." | `gfx06.py` `CTA_COPY = ("Tap The Button Below To", "Start Training With AI")` |
| AI ideas | frames for all except number 2 | done: I1, I3, I4, I5 on the frames page; idea 2 (tracksuit) is out |

## The frames on Dan's page (Codex subscription, gpt-6.1-sol medium, $0; `ra06/round2/frames/`, prompts in `prompts/`)

| id | idea | slot (film time, round 1 cut) | frames (sha256 first 16) |
|---|---|---|---|
| I1 | The copier: same sheet off the copier to three different men | 11.28 to 15.65 ("generic plans ... always fail") | start 6ff2a15af054ec6b, end 86346750b48a17e5 |
| I3 | The body scan, played straight | 5.97 to 11.28 ("depends on your body fat ... other things") | start 007f091edf75e32d, end 4cb5bee5f1850ac3 |
| I4 | Robot waves goodbye (A0147's two characters, A0147 frame as reference) | 41.47 to 43.58 ("Fire your trainer and replace him with AI") | start 83a3e87dc69cec66, end c1112686f9f54468 |
| I5 | Exercise wheel, opener alternative | 0.00 to 2.30 (instead of or before the split screen) | start 0e9b91038d859308, end 06432b340a01b5d6 |

Hashes also in `ra06/round2/frames/HASHES.txt`. Re-hash before generating motion; materially different frames need his approval again.

## Next action (round 3)

1. Record his frame reply. For each approved idea: motion from its exact START and END frames (the method Dan approved on RO-06:
   `longform-edit/reference/ro06/gen_motion.py`; RA-14's O2 opener is the latest ad example). Ad budget $10 for the whole ad,
   $0 spent; state the estimate before each take. Check every take with the three sense questions in VIDEO-RULES (cause and
   effect, readable with the sound off, shows the line) and the first/last-second frame strips. Specific risks: I1 the trainer
   must visibly hand each man his sheet (sheets never appear in hands by themselves); I3 the outlines must not crawl or morph;
   I4 the door must open as he pushes it; I5 the pictograms stay put until the wheel blurs. A take that fails once: cut to the
   part that works, or one retry; at the cap with problems left, ask Dan for budget first, never ship it. AI-GENERATED chip on
   each, placed by looking at the people. Register approved takes in the clip library.
2. Apply the round 1 decisions:
   - **Pair 3**: write `framing_choice.json`, re-run `s04b_holdstart.py beats.json`, check hair margins at the new sizes.
   - **Centre the close**: round 1's close holds sat 10 to 24 source px (median) off his head centre under the land-then-hold
     track (`timeline_9x16.json` `motion`), up to 58 px. For the NEAR holds only, tighten the deadband (Dan's request for this
     video overrides the 3.3 % default; try `tolerance` about 1 % of the crop width in `landing.track`) or land on the hold's
     median centre. Show a still of every close hold's first frame plus the median offset; aim under 1.5 % of the crop width.
   - **Split screen**: brighter on all three panels. His "very dark" was on the round 1 file with gamma trims 1.30 / 1.22 / 0.80.
     Re-bake each panel from the S-Log3 source with a higher exposure (`s31_bake.py`-style LUT per roll), then LOOK at each panel
     beside a talking-head still at full size; his body should read at least as bright as on the talking shots, the backgrounds
     not crushed. Order stays spiderman / toe touches / vacuum (captions cross the vacuum panel's chest).
   - **Vacuum draw-in**: C1677 front-on, from library B0419's approved range (C1677 @136.6 s, "belly drawn in with ribs flaring",
     Dan picked it for DS-04's cold open). Measure his waist width across the window and start so the draw-in happens inside the
     2.3 s; the profile version (B0420, C1677 @52.43 s) is the fallback.
   - **B1 out**: delete the `pose` card in `s05_plan06.py`; Dan on camera 28.86 to 31.13 (the planner puts a level change on any
     splice). Do not put any other standing or posing clip there.
   - **Button**: the new copy in `gfx06.py`.
   - **Placement of approved clips**: I3 covers 5.97 to ~11.0 (LT1 drops if I3 is in: the scan makes that point); I1 covers 11.28
     to 15.65 (LT2 then runs 15.65 to 19.95 over Dan); I4 covers 41.47 to 43.58 under the button (button stays on top, clear of
     faces); I5: show it first then the split screen (about 1.2 s each) unless he says otherwise. Re-check `_cov` / bare-splice
     asserts in the planner and the cut QC on every new boundary.
3. Rebuild with `r1_chain_c.sh` then `r1_chain_d.sh` (round 3 folder `round3/`, new page on 8836 or a free port), and run the
   independent review on the full 9:16 (brief: `review_r1b/ROUND-1B-REVIEW.md` shows the format; include the AI-clip sense
   questions and the no-standing-around rule). Fix what it finds before Dan sees it. Copy the full file to `Videos to Review/`.
4. Page: the full 9:16 with the clips moving in context, only what changed since round 1, a short "What I decided" list, no claim
   question. Then a round 4 handoff for the final round (16:9 from the same edit, edit sheet, `deliver/gate.py` both formats, watch
   pass, independent review of both, delivery folder `Claude Ad Videos/whats the best ab exercise - RA-06/`, `queue.py set RA-06
   delivered` + artifact db, `roll_sidecar.py mark-used`, clip library `add --used-in "RA-06"`), and stop.

## Files (sha256 first 16; re-hash before touching)

| file | sha256 | what |
|---|---|---|
| `round1/DRAFT - RA-06 round 1 - full ad.mp4` (= `draft_9x16.mp4`) | ba0f647e2e175ee3 | what Dan reviewed in round 1 |
| `mix.wav` | 0e7e79bb22df9815 | voice: fitted tone + bass lift + rides, bed -32, -14.2 LUFS, audio gate PASS |
| `cut.json` | d04eb8248c43b42a | 45.41 s talk + 0.30 s end hold, 13 pause cuts, seam 19.95 s |
| `beats.json` | e21e5fe2d080afdf | round 1 plan (changes this round) |
| `round2-plan/decisions.json` | see file | Dan's round 1 answers, word for word |
| `round2/index.html` | see file | the frames page |

Review copies to delete when the ad is finalized: `Videos to Review/Best Ab Exercise AD R1 - full ad draft.mp4`; then
`review_server.py 8806 --remove` and `8836 --remove`.

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `Best Ab Exercise AD R3`. Read `Handoffs/handoff-20261014-ra06-round3-after-frames.md` and
> `.claude/skills/ad-edit/reference/ra06/README.md`, then continue RA-06 "What's The Best Ab Exercise?" with /ad-edit. My answers
> to the frames page are: [paste the reply box]. Record them word for word first. Make the motion for the frames I approved and
> check it before I see it, apply my round 1 answers (pair 3 with the close centred, brighter split screen with the vacuum
> actually happening, poses clip out, new button text), rebuild the full 9:16, run the independent review, fix what it finds,
> send me the page and the round 4 handoff, and stop. Use the Codex subscription to generate any images.

**Recommended model and effort: Opus 5.5, high.** Motion generation with sense checks plus a recipe-backed rebuild.
