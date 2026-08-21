# Abs By AI — Codex and Claude Code Coordination

Shared task board for Codex and Claude Code. This file is loaded in full into every
Claude Code message in this project, so it is kept deliberately minimal — Codex is used
rarely now, and most work happens directly in Claude Code sessions without needing a
handoff file. **Full project history, past decisions, and standing operational rules are
in [`AI_COORDINATION_ARCHIVE.md`](AI_COORDINATION_ARCHIVE.md)** (not auto-loaded — read it
only when you need historical context on a specific past task or decision). Git history
and commit messages remain the permanent record of code changes.

## Working rules

1. Read this file before starting project work involving Codex handoff.
2. Only one assistant owns implementation of the active task at a time. Don't overwrite
   or continue the other assistant's unfinished work without an explicit handoff or a
   user-requested review.
3. Update this file when starting work, hitting a milestone, getting blocked, handing
   off, or finishing — keep entries short and factual (what the next assistant needs to
   continue, not a transcript).
4. When a task is fully completed, committed, pushed, deployed, and verified, clear the
   active-task section back to `No active task`.
5. When you write a handoff doc for work that hasn't been executed yet, add a Key-priority
   dashboard task for it (mechanism + gotchas are in the `/dashboard-tasks` skill).
   When that work is fully executed, check it off in the same
   session — don't wait for Dan to click it.

## Status options

`No active task` · `Planning` · `Ready for implementation` · `Implementation in progress` ·
`Ready for review` · `Blocked` · `Complete — pending reset`

---

## Active task

### Exercise demo BATCH 2 — round-5 revisions delivered, awaiting Dan (2026-08-20 night, Claude Code)

Four fixes redelivered: pull-up (new almost-locked-hang bottom still + 6s re-roll; the winning cut has
BOTH the nearly-straight hang and the chin-over-with-daylight top), leg-curl (keyframe-locked regen,
full extension to past-90), press + side-lateral backgrounds FULLY locked (Dan caught stacks the ghost
scan missed inside the arm-sweep zone — new `_r2/bglock.py` validated-rectangle freezes and
`_r2/keyfreeze.py` per-pixel keyed composite are in the skill, verified on arm-free frames ≤3 gray
levels). Leg raise FINALIZED by Dan. ~$5 this round; batch-2 total ~$84. Batch-2 finals await Dan's
verdict; approved ones are NOT yet stamped -FINAL.

### Three longform videos CUT, QC'd and DELIVERED from the 8/3 shoot (2026-08-20, Claude Code)

**Deliverables (RELOCATED 2026-08-21 on Dan's instruction — finished videos live in the PROJECT
folder now, not the Seagate):** `claude edited long form content/` — three
finished MP4s + SRT + YouTube chapters + the pre-graphics rollback cut + `edl.json`/`ranges.py`/
`chips.py` each, plus a `README.md` with QC results and Dan's review list. **$0.00 AI spend** (local
Whisper, static ffmpeg, open-source colour analysis — no metered provider called). **No production
code touched, no deploy.**

| video | roll | raw → final | ranges | chips |
|---|---|---|---|---|
| My First Spray Tan | `C1512` | 30:42 → **19:00** | 42 | 26 |
| My Honest Zepbound Update | `C1513` | 40:16 → **30:28** | 49 | 23 |
| The Supplements I Actually Take | `C1514` | 37:39 → **23:30** | 62 | 27 |

**All three PASS all six QC checks**, and each SRT was validated by re-transcribing 10 windows of the
**finished render** (98.3 / 97.7 / 97.9 % word overlap). All 16 builder-flagged joints were
re-transcribed from the finished files and read as clean continuous speech.

**THE SEGMENT CACHE WORKS AND THAT IS THE HEADLINE FOR REVISIONS.** It was already fixed
(`~/Developer/video-use`, commit `efbfe69`) — verified rather than rebuilt: a beat edited AND a beat
inserted still reported `[cached]` for the untouched beats, including one whose index shifted 2→3, so
it keys on content not position. Production-proven three times today: **49/50, 40/42, 48/49 reused.**
Concat is lossless and loudnorm is `-c:v copy`, so a one-beat revision costs one segment extraction
plus a graphics pass. **Dan's revision notes are cheap now.**

**Three QC metrics were wrong before the media ever was** (skill updated, commits `74eae0a`,
`8fac0bf`, `3d233a1`): a splice rule normalised on the control *median* failed 4 clean joins on a
long talking head (controls span 613…4069, so a join beside a loud syllable "fails"); a graphics rule
assuming a chip makes the region *brighter* failed a video whose chips were perfect (a J2 chip is a
DARK box, and the supplements video is shot over bright granite); and the splice rule structurally
**cannot** see the one defect that was real — render.py's 30 ms fades make an amplitude *dip*, not a
*step*. That real defect was self-inflicted: two ranges split a continuous passage with 0.02 s
removed, purely to hang a chip. Chips map by SOURCE time, so the split was never needed. Merged;
worst join went 6.41× → 3.84×. Both the EDL builder and QC now assert no adjacent pair under 0.20 s.

**Other skill additions:** Step 0.5 (identify which video each unlabelled clip is with 100 s audio
probes + Whisper `base` — 84 clips mapped in one pass) and three more Whisper-timestamp rules (don't
clamp an in-point to a *stretched* previous word; a stretched *last* word is the mirror trap; measured
silence outranks Whisper's claimed next-word onset).

**Colour: graded PER ROLL, not per shoot** — three rolls from the same doorway on the same night had
black points 0.079 / 0.069 / 0.054. **The spray-tan roll got NO white-balance correction on purpose:**
its WB deviation read 3× the others because that is the actual spray tan, which is the video's subject.

**TWO THINGS DAN DECIDES, both listed with exact final-edit timecodes in the delivery README:**
1. **On-screen photos are still owed** — spray tan `00:03` and `09:21`, Zepbound `08:51` (192 lb) and
   `09:12` (181 lb). I did **not** guess which photo is which; asserting "this is Dan at 192 lb" is a
   claim about his body I cannot verify, and a wrong photo burned into a finished video is worse than
   an empty slot. Each beat carries a J2 chip with the numbers so it lands either way. The Zepbound
   injection-site callouts (`16:12`, `18:35`, `19:05`, `19:16`) are optional — he demonstrates on
   camera. Supplements needs nothing; he holds every bottle up.
2. **Seven lines flagged, none removed** — profanity ×4, the "injected my ex-girlfriend" line
   (Zepbound `03:37`), the Donald Trump tan joke (spray tan `12:35`), and "You are not smart enough to
   understand scientific research" (supplements `01:00`). All are his words and stay in; each is a
   one-line change in `ranges.py`. **No chip in the Zepbound video prints the drug name**, per his
   standing copy rule, and the "not medical advice" beat is kept in full at `07:09` — do not trim it.

**No native retest trigger row touched** — video files only; no product surface, server or client.

**Dashboard: nothing checked off, correctly.** All four lists searched. The nearest match,
`money::Clear editing backlog: batches 2-4 (~10 ads + ~25 content videos)`, is genuinely **advanced,
not finished** (3 of ~25 content videos). `money::Execute handoff: Build /longform-edit video pipeline`
covers building the pipeline, which earlier sessions did; today used it. Per Rule 9 that is reported,
not checked off early. **Useful input for `money::Decide the video-editing stack`: three finished
longform videos, one session, $0.00, zero human editor hours.**

**EXACT NEXT ACTION — DAN: watch the three videos** and send revision notes; they are cheap now. Then
`/youtube-packaging` for titles, descriptions and thumbnails (chapters are already generated).

**CONSOLIDATED 2026-08-21:** every earlier Claude-edited longform moved into the same folder —
`04 - Why You Should Invest More In Your Health` (INVEST_HEALTH_v3, 53:17, + a chapters file generated
from its chip timings) and `05 - Meal Prep Macro Tracking (app demo)` (SPLITSCREEN_v3, 3:48, no
chapters — under YouTube's 3-chapter minimum). Five videos, 14 GB, one README. Superseded
invest-health v1/v2 masters deliberately left in `Media/longform-raw/…/roughcuts/`.
**The repo is PUBLIC and that folder is now inside it** — `.gitignore` gained `claude edited*/` plus a
global `*.mp4`/`*.mov`/… rule (`a23ad9a`). Folder-name rules have failed twice after renames;
extensions don't get renamed. Verified zero tracked video files first, so nothing was orphaned.
Working files + `_edit_work/clips_graded/` (**the segment cache — never delete it**) stay on the Seagate.

**⚠ THIS ENTRY WAS DROPPED ONCE ALREADY** (commit `c4fb797`, wiped by a concurrent session's
whole-file rewrite — the same failure `0ca72b5` records). If you are another session: re-read this
file from disk immediately before writing it, and edit your own section only.

### Invest-health longform — v3 DELIVERED, awaiting Dan's review (2026-08-21, Claude Code)

`Media/longform-raw/absbyai-0803-shoot/invest-health/roughcuts/INVEST_HEALTH_v3.mp4` (53:17) +
`INVEST_HEALTH_v3.srt` (1015 cues). All 6 items of `Handoffs/HANDOFF_invest_health_v3.md` executed
in ONE render (52/110 segments cache-reused): repeated "all kinds of problems" sentence cut whole,
zoom 6%->10%, doubled Oura intro cut, "if you're middle class" dropped from the supplements intro,
Oura Ring 4 + WHOOP 5.0 J2 product cards from official press renders, Bryan Johnson 7.8s attributed
PiP, and the SRT drug/brand fix table with a hard no-"GOP" gate. QC v3 passes: 3197.45s, -14.3 LUFS,
0/109 splices above the control ceiling, all 4 changed joints re-transcribed clean, no fade notch
above the p90 control, zoom contrast verified on 6 join pairs.
SUBSTITUTION to confirm with Dan: item 5's "supplement bottles" graphic is a J2 SUPPLEMENTS card —
no usable bottle photography exists locally (the only ad-asset candidate is dominated by the ad's
robot arm). Also: the Bryan Johnson clip is 360p-sourced (YouTube 403s every HD format), so it is
shown at 600x338, a downscale rather than an upscale.
NEXT after Dan approves v3: `Handoffs/HANDOFF_invest_health_cutdowns.md` (conservative ~40 min +
aggressive <30 min variants) before any b-roll/AI-clip dressing. No baked-in speed-up.
New lessons 7-12 + the card-placement rule are in the `/longform-edit` skill; v3 scripts are in its
`reference/`.

### AD 1 REV-4 shipped (2026-08-21, Claude Code)

Both rev-4 items applied and delivered as `ad1_rev4_16x9.mp4`: (1) busy-dad AI clip (frames
Dan-approved, Veo 3.1 Fast on Gemini API, no lastFrame) replaces the tire-flip stock clip at
0:46, (2) AI-GENERATED tag moved upper-left + 50% larger on every full-frame AI clip (dad clip
+ the three benefit clips ~2:00); panel-style inserts keep the centered small tag. Lessons
17–18 appended to the ad-edit skill. Session AI spend ≈ $1.20. Awaiting Dan's rev-4 review;
9:16 build on approval (per `Handoffs/HANDOFF_ad1_rev4_and_9x16.md` Step 8).


### Exercise demo batch 3 — second revision COMPLETE, all 10 delivered (2026-08-21, Claude Code)

Dan finalized leg-press, db-row, face-pull, incline-pushup, dead-bug*, bird-dog* (*reluctant — he plans
to drop both; STANDING RULE: alternating-limb moves rendered single-side or with visible seams are
unacceptable in future). Final four fixes delivered: RDL (region-scoped analysis found the real hinge =
first 0.96s of the leg; the rest was bottom-bobbing invisible to whole-frame gating), bench (deeper,
elbows past 90°), goblet (no foot shuffle), pushdown (true lockout). **Replicate credit is DRAINED
(HTTP 402, auto-reload not firing — Dan must sign in at replicate.com/account/billing; sign-in tab was
left open in his Chrome by the ad session). Workaround used: Veo 3.1 Fast via the Gemini API**
(`_batch3/run-gveo.js`) — `lastFrame` unsupported there, so legs were generated as ASCENTS from the
bottom still (flip trick: depth/lockout guaranteed by construction) and reversed. 8s/1080p (4s+1080p
rejected); audio-directive words in prompts trip a safety filter — strip them. Round 3 same day: bench double pump root-caused (settle wobble at the segment boundary — new
VELOCITY-BOUNDARY RULE in the skill: every rep must be one clean velocity bell, trim boundary hovers,
tpad-hold at overshot extremums), goblet + bench backgrounds FROZEN via full frame-0 overlay outside
the subject corridor (ghost.py STRAY=NONE on both), pushdown REGENERATED keyframe-locked on Replicate
(credit restored by Dan) — acute top to full lockout with a 0.2s squeeze hold. All pass qc.py.
**BATCH 3 FULLY FINALIZED by Dan 2026-08-21 — all 10 approved.** Finals stamped
`<id>-AIDAN-narrated-FINAL.mp4`. The double-pump and background-ghost eliminations are consolidated
into the /exercisegeneration skill as the mandatory GATED CUT PIPELINE (step 5). Next exercise batch
can start fresh; remaining ~40 exercises are mostly step-based moves, kettlebell, barbell, warm-ups.
App integration + hosting remain separate tasks. AI spend this session ≈ $3 (stills + 4 Gemini Veo fast legs).

### AD 1 REV-3 shipped; import-time asset-clobber root cause fixed (2026-08-21, Claude Code)

Rev-3 items: zoom-safe uncropped shoot photos (root cause: prep_assets.py built assets at import
time, silently restoring rejected cover-crops — now guarded under __main__; lesson 14 in the skill),
crop screen eliminated from both demo flows (start at generation screen, si=3.2; lesson 15), stats
screen v3 (tag below picture / stats / plan line / teaser body text; lesson 16). Redelivered as
`ad1_rev3_16x9.mp4`. ALSO: checked Replicate per Dan — auto-reload is NOT topping up (402 persists
40+ min); billing page needs his GitHub sign-in (tab left open). Veo covers video gen meanwhile.
Awaiting rev-3 review; 9:16 on approval.


### AD 1 REV-2 — second revision round shipped (2026-08-21, Claude Code)

All 10 of Dan's rev-2 items applied and redelivered (`ad1_rev2_16x9.mp4`, 4:31): smooth
supersampled Ken Burns (shake fixed), three AI-generated benefit clips (frames Dan-approved, then
**Veo 3.1 Fast via Gemini API** because **Replicate credit is DRAINED — Dan to top up**; safety-filter
workaround recorded in the skill), the two iCloud dad photos with motion, clean phone-image mockup,
gen-screen-with-photo slice, oversized AI-GENERATED box hiding the email form (Dan's rule: never show
email capture in an ad), custom scan+stats animation ("Goal Muscle GAIN" — confirmed via question;
plan not revealed), "lagging" caption fix, and the end card replaced by the real sample-person
generation flow (after ALONE). Session AI spend ≈ $5. Lessons 7–13 appended to the skill's
graphics-placement learning log. Awaiting Dan's rev-2 review; 9:16 builds on approval.


No active task.

---

## Handoff template

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
