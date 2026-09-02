# Handoff: Fix every off-centre Short still in a posting queue (YouTube + Blotato)

**Date:** 2026-09-02
**Project:** Abs By AI (organic short-form)
**Business goal this serves:** marketing performance — Dan's rule, stated 2026-09-02: *"No centering issues like this can be allowed in posted content."*

## Objective

No Short goes public with Dan off-centre in the vertical crop. Replace every queued file that
still carries the pre-2026-08-27 crop, re-cut the two V6 Shorts whose CURRENT masters are
still off-centre, and re-measure the borderline ones — then verify, on the queue itself, that
the file each platform will actually post is the corrected one.

## What happened (root cause — read this before touching anything)

- On **2026-08-27** ten Shorts were re-centred (`v2-short1/3/4/5/7`, `v3-short4/7/9/11`,
  `v6-short2`). The fixed masters replaced the files in `Short-form video content/`, the old
  ones went to `Short-form video content/_pre-recentre-2026-08-27/`, and **25 Blotato posts
  were swapped** to the fixed files.
- **The YouTube Shorts were never swapped.** They were uploaded natively in YouTube Studio on
  2026-08-11 (`YouTube Long Form Video Content/SHORTS_UPLOAD_PLAN.json`), YouTube cannot
  replace a video file after upload, and the 8/27 session flagged it as "Dan's call" and it was
  never made. So **YouTube has been publishing the stale, off-centre files on schedule ever
  since.** The one Dan caught (`rqyK5IDsxX0`, "Ask AI This Before It Writes Your Workout",
  published 2026-09-01) is the pre-recentre `v2-short5`: **171 px off-centre median, 209 px on
  the opening shot** (measured on the file, 2026-09-02). Dan is taking that one down himself.
- **One Blotato post was missed by the 8/27 swap:** the 2026-09-07 `@danrosefit` Instagram post
  ("I lost the weight in the hour I wasn't training") still carries the pre-recentre
  `v2-short1` (MD5 `638e8299…` = the `_pre-recentre` file), and the 2026-09-02 TikTok mirror
  copied it verbatim, so TikTok has it too.
- Two V6 Shorts (`v6-short2`, `v6-short5`) were judged "clean"/"hand-tuned" on 8/27 and are
  **still visibly right-shifted** in their current masters (see below).

## Measured findings (2026-09-02)

Method: every unique file in both queues was downloaded / read from disk, sampled at 2 fps,
person-masked with Apple Vision, torso-block anchored (`recentre/anchor.py`), and reported as
px off the 540 px centre line of the delivered 1080-wide frame; then **every file was looked
at on an 8-frame contact strip** because the metric over-fires on stock b-roll with people in
it, graphics-in-graphic cards and handheld shots. Thresholds are the ones calibrated on the
Short Dan rejected on 8/27: ≤35 px invisible, ≥60 px re-cut, ≥110 px on any one shot re-cut.
Tools: `.claude/skills/shorts/reference/recentre/delivered_gate.py`, `strip.py`, `timeline.py`
(installed by this audit).

### A. YouTube — stale pre-recentre files (the defect Dan saw). Hard fail.

| YouTube id | file on YouTube | scheduled | offset on the stale file | status |
|---|---|---|---|---|
| `y0XIbNoA2Xo` | `v2-short1_sugar-free-gum-trick` | **published 08-22** | left ~60–110 px through every talk shot | live, off-centre |
| `P9VUGyWeNtY` | `v2-short3_supplements-3-percent` | **published 08-27** | 118 px median, 210 px worst | live, off-centre (the 8/27 calibration short) |
| `VOlZHV1ibmU` | `v2-short4_macro-tracking-obsolete` | **published 08-29** | left ≥110 px most of the runtime | live, off-centre |
| `rqyK5IDsxX0` | `v2-short5_ask-ai-to-interview-you` | **published 09-01** | 171 px median, 209 px worst | Dan is taking it down |
| `broQqQ7We4k` | `v2-short7_chicken-soup-trick` | 09-05 | left ≥110 px through the talk shots | **scheduled — 3 days out** |
| `sY5T9_sl8gk` | `v3-short4_train-abs-every-day` | 09-15 | left ≥110 px for the first 30 s | scheduled |
| `7_dRh8Zhscs` | `v3-short7_fast-until-2pm` | 09-22 | left 60–110 px through the talk shots | scheduled |
| `qpJnLUevrJ8` | `v3-short9_break-fast-low-carb` | 09-26 | left 60–110 px, milder | scheduled |
| `USLrZHrajGQ` | `v3-short11_bubble-gut-vacuums` | 10-01 | right 60–110 px in the talk shots | scheduled |
| `4e9jrnSq_pk` | `v6-short2_knee-yourself-in-the-face` | 10-06 | right ≥110 px for the whole talk section | scheduled |

Every other YouTube-scheduled Short (`v2-short6`, `v3-short1/2/3/5/6/8/10`, `v6-short1/3/4/5`)
is byte-identical to the current master, so it inherits section C's verdict on that master.
⚠ `v6-short1` (`78pojxcmNeg`, 10-03) — Dan killed this Short on 2026-08-17 ("just more me
bragging"). The 8/11 plan still lists it as scheduled; **confirm in Studio it is not going out,
and if it is, make it private.** It also measures right-shifted throughout.

### B. Blotato — one stale file. Hard fail.

| post ids | account | date | file | fix |
|---|---|---|---|---|
| IG `3793999`, TikTok `4064594` | `@danrosefit` 67203 + TikTok 58181 | 2026-09-07 22:00 UTC | pre-recentre `v2-short1` (media `…/e2ed7153-4d39-4cc8-a31a-9300a71e64d6.mp4`) | swap both to the current `v2-short1` master (create-then-delete, same time/caption) |

All 49 other queued video posts (IG `@danrosefit`, `@abs.by.ai`, Facebook, TikTok) are
MD5-identical to the current masters — verified by downloading every one. Two queued videos are
16:9 long-forms posted whole (V7 follow-along on Facebook 09-06; an 8-min 16:9 cut on IG/TikTok
09-21) — no crop, structurally immune.

### C. Current masters that are STILL off-centre (in both queues). Must re-cut.

| file | where it is queued | what's wrong |
|---|---|---|
| `v6-short2_knee-yourself-in-the-face` | Blotato IG/FB/TikTok 10-06, `@abs.by.ai` 10-07; YouTube 10-06 (stale copy) | seated talk shot 8–30 s: Dan sits right of centre with empty pavement on the left in every frame; the 8/27 re-cut moved him but not far enough. Legs extend left so the torso anchor under-reports — **set the offset by eye on 5 frames**. |
| `v6-short5_you-always-have-three-minutes` | Blotato IG/FB/TikTok 10-13; YouTube 10-13 | standing talk shot 7–16 s: right of centre ~110–130 px, grass on the left; opening towel shot also right. Never re-cut on 8/27 ("hand-tuned"). |

### D. Borderline — re-measure per shot in the build folder, re-cut only if ≥60 px weighted

- `v3-short4_train-abs-every-day` — the last shot (`L-p0-s00`, the zoom shot, ~58–64 s) reads
  right-shifted on the strip; the torso metric says left 60–110 on that window. Sign conflict =
  hands in frame; measure it on 5 frames.
- `v2-short7_chicken-soup-trick` (current) — metric flags 25–27 s right ≥110 px; the strip looks
  centred. Likely the mirror reflection in the doorway is being masked. Confirm and leave.
- `v3-short8_weigh-yourself-every-day` — several 60–110 px right windows at 23–27 s.
- `v3-short2_whey-protein-insulin` — 16–18 s right 60–110 px (hands), talk frames read ~+60–85 px
  at 5–8 s by eye.
- `v6-short3_look-at-the-sky-deadlift` — metric says right ≥110 px for most of the runtime, but the
  kettlebell on the ground is part of the frame and the 8/27 A/B judged it right. Leave unless it
  fails by eye.

Clean by measurement AND by eye: `v2-short5` (current), `v2-short6`, `v3-short1/3/5/6/7/9/10/11`,
`v6-short4`, and the four band-layout Shorts (`short1–4`, structurally immune).

## Detailed Plan

Do it in this order — the 09-05 YouTube slot is the nearest hard deadline.

1. **Re-cut section C first** (`v6-short2`, `v6-short5`), because every later step wants the
   final files. Build folder `YouTube Long Form Video Content/v6-3min-home-workout/`; edit
   `shots/crops.json` with the shipped values backed up to `.pre-recentre-20260902` (recompute
   from the 8/27 backup, never from a prior edit), `node render.js <SEG>`, then
   `recentre/verify_recut.py` — identical frame count, duration, fps, resolution and audio MD5.
   Judge with `ab_multi.py`, **5 frames across each shot, shipped beside proposed**. Copy the
   finished files over the masters in `Short-form video content/` (old ones into
   `_pre-recentre-2026-09-02/`).
2. **Section D**: measure per shot from each build's `shots/crops.json` + `recentre/audit.py`
   (paths at the top need fixing), look at the A/B, re-cut what fails, leave what passes, and
   record the verdict in this doc.
3. **Run the delivered-file gate on every final master** (`delivered_gate.py` → `timeline.py`
   → `strip.py`) and look at every strip. Nothing ships on the numbers alone.
4. **Blotato swap** (section B + any file changed in steps 1–2): reuse the 8/27 pattern —
   upload the master, create the new post with the same `scheduledTime`, caption, first comment,
   cover and account, verify it exists, then delete the old id. Do it for every account that
   carries the video (IG `@danrosefit` 67203, `@abs.by.ai` 65632, Facebook 47105, TikTok
   58181). Queue is at the 200-post cap — create-then-delete needs one free slot; delete the
   stale post first *only* if the create refuses. Verify by **downloading the new media URL and
   MD5-matching the master** (Blotato re-hosts under a new UUID; a URL comparison proves
   nothing). Helpers: `scripts/blotato/danrosefit_migration.py` (`fetch_schedules`, `call`,
   `content_key`).
5. **YouTube**: the 6 scheduled stale Shorts (section A rows 5–10) — for each: in Studio set
   the existing video to **Private** (do not delete until the replacement is live), upload the
   corrected master with the identical title / description / tags / made-for-kids answer /
   schedule from `SHORTS_UPLOAD_PLAN.json`, confirm "Checks complete", then delete the old one.
   Verify the schedule for all 26 with the `row.polymerController.__data.video` trick in
   `SHORTS_UPLOAD_PROGRESS.md`. ⚠ The Chrome extension's `file_upload` is capped at 10 MB and
   these are 15–65 MB — **the upload itself is Dan's, or a browser session with the native file
   picker**; everything else in Studio Claude does. New ids: update `SHORTS_UPLOAD_PLAN.json`.
6. **YouTube, already-published stale Shorts** (`v2-short1/3/4`, published 08-22/27/29, and
   `v2-short5` if Dan hasn't deleted it): these are live and off-centre. Recommendation: delete
   and re-upload as new Shorts on the next open Tue/Thu/Sat slots — none of them is an ad
   destination (the ads point at the V4/V5 long-forms), so the id change costs nothing but the
   ~2 weeks of views. **Dan decides**; ask in one line, then do it.
7. **`v6-short1`**: confirm it is private/unlisted on YouTube per Dan's 8/17 kill. If it is
   still scheduled for 10-03, make it private.
8. **Close the loop so this cannot recur**: add to `/shorts` Step 5 the rule that a re-cut is
   not finished until *every* queue holding the file has been swapped and re-downloaded —
   Blotato AND YouTube Studio — and that a YouTube-scheduled Short must be replaced by
   private → re-upload, not left "for Dan to decide". Put the new gate in the skill's
   pre-delivery checklist (it already exists there for the Zepbound batch as `centregate.py`;
   `delivered_gate.py` is the file-agnostic version).
9. Housekeeping: check off the Key dashboard task for this handoff, delete the
   `AI_COORDINATION.md` entry, commit and push (`Short-form video content/` masters,
   crops.json, plan json, skill changes).

## Gotchas

- **Blotato re-hosts media on create under a new UUID** — verify swaps by download + MD5, never
  by comparing URLs. The same trap fooled the 8/27 verification until it downloaded.
- **The queue is exactly 200/200** (TikTok mirror, 2026-09-02) and Blotato silently refuses
  creates past the cap. One swap = one create before one delete; if the create fails with no
  error, that's the cap.
- **`v6-short2` is seated with legs to the left** — the torso-block anchor reports him LEFT of
  centre while the frame reads RIGHT of centre. Trust the strip, set the offset by hand
  (`override_v6.json`, as the 8/27 session did for every V6 shot but one).
- **A pan on a locked tripod reads as a mistake** — one constant per shot, never a time-varying
  crop.
- **Don't run more than two renders at once** (AGENTS.md); check `ps` for other sessions' builds.
- **Two Studio uploads of the same file within minutes can be flagged as duplicates** — private
  the old one before uploading the new.

## Relevant Files & Locations

- `Short-form video content/` — current masters; `_pre-recentre-2026-08-27/` — the stale ones
- `YouTube Long Form Video Content/{six-ways-ai-abs,v3-top10-tips,v6-3min-home-workout}/` —
  build folders (`shots/crops.json`, `render.js`, `qc.js`)
- `YouTube Long Form Video Content/SHORTS_UPLOAD_PLAN.json` — YouTube ids, dates, metadata
- `YouTube Long Form Video Content/SHORTS_UPLOAD_PROGRESS.md` — Studio schedule-verification trick
- `.claude/skills/shorts/reference/recentre/` — `README.md`, `audit.py`, `ab_multi.py`,
  `apply_crops.py`, `verify_recut.py`, `personmask.swift` (compile: `swiftc -O -o personmask
  personmask.swift`), and the new `delivered_gate.py` / `strip.py` / `timeline.py`
- `.claude/skills/shorts/SKILL.md` Step 5 — the centring doctrine, thresholds, and lessons
- `scripts/blotato/` — API helpers; `Business/blotato-api-key.txt`
- `AI_COORDINATION_ARCHIVE.md` ~line 7385 — the 8/27 re-centre record

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **Claude usage low** | Claude Fable 5.1, high effort — the judgment calls (V6 by eye, sign conflicts, what counts as centred) are exactly where a cheaper model shipped the wrong answer on 8/27 |
| **Claude usage high** | Claude Opus 5, standard — acceptable for the Blotato swap and Studio work; do the V6 re-framing on Fable |

Always-Claude: yes — the Blotato MCP, Chrome extension and Apple Vision tooling are wired only into Claude Code.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260902-shorts-centering-queue-fix.md`. YouTube has been publishing the pre-8/27 off-centre Shorts and one Blotato post still has a stale file; two V6 masters are still off-centre. Order: (1) re-cut `v6-short2` and `v6-short5` by eye with 5-frame A/B sheets and `verify_recut.py` parity; (2) re-measure the section-D borderline shots per shot and re-cut what fails; (3) run `delivered_gate.py` + strips on every final master; (4) swap the Blotato 09-07 `v2-short1` post on IG and TikTok and any file you changed, verifying by download + MD5; (5) for the six stale YouTube-scheduled Shorts, private the old, re-upload the master with identical metadata and schedule — the 09-05 one (`v2-short7`) is first; tell me when you need me at the file picker. Ask me in one line whether to delete + re-upload the three already-published stale Shorts. Then add the "swap every queue" rule to `/shorts` Step 5, check off the dashboard task, clear the coordination entry, commit and push.
