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
rejected); audio-directive words in prompts trip a safety filter — strip them. All 10 pass qc.py;
awaiting Dan's verdict on the last 3. AI spend this session ≈ $3 (stills + 4 Gemini Veo fast legs).

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
