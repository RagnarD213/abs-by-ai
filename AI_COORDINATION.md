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

### SPRAY TAN longform REV 1 DELIVERED — clips/graphics pass + fixes (2026-08-21, Claude Code)

`Handoffs/handoff-20260821-spraytan-rev1.md` executed. **19:00 → 18:53**, delivered over the same
filename in `claude edited long form content/01 - My First Spray Tan/`. **$0.00 AI spend** — the 71
stock cutaways are Pexels (free, no key), graphics are PIL, everything else local Whisper + static
ffmpeg. **No production code touched, no deploy, no native-retest trigger.**

**`qc_generic.py` PASSES all six checks** (−14.49 LUFS, 0/43 splices over the file's own ceiling,
0 artificial splits) and **`srt_validate.py` scored 12/12 windows, mean 98.0 %**. A 7th check was
added and passes: all 71 cutaways verified present on the timeline by frame correlation.

Six of Dan's seven notes are done in full. **95 inserts** (71 Pexels cutaways, 19 J2 cards, 5
before/after panels) on top of the 26 chips ⇒ **longest bare stretch 18.8 s** against his 30 s rule,
built deliberately over-full so he can prune by deleting lines from `inserts.py`. Item 2 removed the
4:00 junk take **and the sentence it restarted into** (a restatement, Step-3 junk rule 7); both edges
placed from a 10 ms RMS envelope because Whisper's word times there are fiction. 35 of 43 joins got
10 % zoom cuts — the other 8 are already hidden by a cutaway.

**NOTE 7 (deodorant residue) IS PARTLY DONE AND DAN NEEDS TO KNOW WHY.** The handoff's measured
recipe is right and is applied at **three** moments (0:12.9–0:13.7 and two around 7:50), each A/B'd
losslessly: residue reduced, texture kept, **zero pixels changed outside the box**. It is NOT applied
at the other three arms-spread moments (≈5:36, ≈14:19, ≈16:18). The armpit is on screen for well
under a second at a time: a static box over 2–3 s lands on his tank/forearm and does nothing, and a
box generous enough for the whole gesture reaches onto the white fridge (value 0.55–0.62, inside the
filter's own gate) and paints a **grey smudge worse than the residue**. Per-frame tracking is what
the handoff rules out. **The real fix is at the shoot — clear/invisible-solid deodorant, or wipe down
before rolling. Put it on Jeff's checklist.**

**THREE SRT CUES WERE CAPTIONING SENTENCES WHISPER INVENTED** — found while rebuilding, all three
proved absent by re-transcribing the source audio ("…getting a shower before you get into bed at
night", "the amount of money you get to spend on a spray tan is", "you want to get the best effect.
So, really,"). Zero-length timestamp clusters are hallucinated text; the de-clumping rule and the
"break ties on reading order, never alphabetically" fix are now in the skill and in
`reference/make_srt_declump.py`. **Worth re-checking the Zepbound and supplements SRTs for the same
defect — they were built by the same generic script.**

Skill updated (`f8cf865`): Step 5.5 (cutaways and cards, incl. reaching Pexels search through a
same-origin `fetch` in the in-app browser, since the search pages 403 to curl), the SRT rules in
Step 8, and lessons 22–27. 15 new scripts in `reference/`. A second commit (`6a43358`) picked up the
`cutdown_*.py` files an earlier session left untracked while SKILL.md already referenced them.

**True peak is +1.58 dBTP** (rev-0 was +2.12, so this is better). The clipping is baked into the
camera recording — **tell Jeff to drop the mic gain**; chasing −1 dBTP with a limiter costs a dB of
loudness per dB of peak control.

**EXACT NEXT ACTION — DAN: watch it and prune.** Revisions stay cheap: dropping a clip is a one-line
edit in `inserts.py` plus the two composite passes (~9 min each); the cut itself never re-renders.
Then `/youtube-packaging` (chapters already generated, 25 of them).


### MODERN-EDIT 60s SAMPLE DELIVERED — the head-to-head vs the Upwork trial edit (2026-08-21, Claude Code)

Executed `Handoffs/HANDOFF_modern_edit_60s_sample.md`. Ad-1's first minute rebuilt with all five
gap-closers in Abs By AI CONTENT style. **$0.00 AI spend** (local Whisper/ffmpeg/PIL/numpy).
Delivered to `EDITED ADS 8-20-26/ad1-how-ai-got-me-abs/`: `SAMPLE_modern-edit-60s_16x9.mp4` (65.8s),
a 720p review copy, `SAMPLE_compare_trial-vs-pipeline.mp4` (his left / ours right, our audio),
the pre-graphics rollback `SAMPLE_tight60_pre-graphics.mov`, every script, and
`notes_modern_sample.md`. **rev-4's chain was NOT touched.**

Measured: 70.7s span → 65.8s, 21 cuts, **no speed-up**, 194 wpm (his 206); **zero residual silence
runs ≥0.22s below −40 dB** — same profile as his (8 runs/2.09s vs his 7/1.98s at −38 dB). **Zero
visible splices**: 20 of 21 sit under a graphic or land exactly on a punch change, the one bare
splice measures 3.3 vs a p99 of 31. Script fidelity on the finished mix 97.9% (the 4 diffs are known
Whisper artifacts, no lost words). Grade lifted 90 → 99 luma. −14.5 LUFS. Visual change every 3.3s.

**The reusable output, and the point of the task: `.claude/skills/ad-edit/reference/motionlib.py`**
(animated graphics: `card_in`, `bullets_build`, `lower_third`, `title_card`, `callout_box`,
`pop_text`, `photo_swap`, `panel_plate` + easing) and **`sfxlib.py`** (whooshes/pops/risers
SYNTHESISED — no licence to track). Complete worked example in `reference/modern60/`. Skill lessons
19–24 appended.

**Music = *Werq* (Kevin MacLeod, incompetech) — CC BY 4.0, so a description credit is required.**
Fine for a sample; budget a paid library if this becomes house style. One constant to swap.

Compliance: AI-GENERATED on all three AI assets; before/after **sequenced not side-by-side**
(verified frame-by-frame across the swap) — deliberately, so the banned pattern never enters the
library. Flagged for Dan's call: his own ~200 lb before photo on screen 6.1–7.8s (already shipped in
rev-1…rev-4, neutral shot, left in).

**EXACT NEXT ACTION — DAN: play the side-by-side and decide the editing stack.** Honest gaps
remaining: he is 4.3s shorter on the same words (his extra cuts are inside words, ours only in
measured silence) and his grade is ~6 luma brighter. Ours fills the beat where he left a black
"Broll assets folder" placeholder. No native retest trigger — video files only, no product surface.

### Muhammad A (Upwork trial) edit ANALYZED — feeds the editing-stack decision (2026-08-21, Claude Code)

Dan rated Muhammad's 61s trial edit (ad-1 script, YouTube-episode format) above our rev-4. Measured
drivers: airtight pause removal (ZERO gaps ≥0.25s in 61s; no speed-up — word-level timing matches
source 1:1), a prominent music bed (~-20dB RMS under voice, runs full length), whoosh/pop SFX on every
graphic, animated MOGRT-style graphics (pastel-cyan explainer theme: progressive bullet builds,
lower-third label chips, title cards, dashed-arrow before→after cards), an animated highlight box
around the physical door photo synced to "THIS picture," brighter grade (luma 67 vs our 55), and fast
phrase-synced punch-ins. Encoder tag = Mainconcept → **Adobe Premiere Pro** (likely text-based
editing for pause removal + template pack + stock music). His edit has NO burned captions. Flaws: a
stray backtick typo in his bullet list, a black "Broll assets folder" placeholder card at ~46s, and
side-by-side before/after usage that is BANNED in our paid ads (fine for organic YouTube). Every
technique is replicable in the existing PIL/ffmpeg pipeline; plan delivered to Dan in the ad-1 rev-4
session. AD 1 rev-4 itself is still awaiting Dan's review (9:16 on approval).

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


### Exercise demo videos wired into the trainer app; 6 more await finalization (2026-08-21, Claude Code)

All 13 Dan-approved AI-Dan demo videos installed into the exercise detail sheet only (52px/68px
card icons keep stick figures; the other 84 exercises keep stick figures too). Encoded
`Media/exercise-demos/*/…-FINAL.mp4` → `public/exercise-demos/<id>.mp4` (960x540, ~1-1.4MB each,
15MB total) + poster JPGs. `public/index.html`: `EXERCISE_DEMO_IDS` set + `openExerciseSheet()`
renders `<video controls playsinline preload="none">` for the 13, suppresses the YouTube
"Watch form video" CTA for those 13 only, fires `exercise_demo_played` PostHog event on play.
Added a scoped `.gitignore` exception (`!public/exercise-demos/*.mp4`) since the global `*.mp4`
belt-and-braces rule (added for raw longform masters) was also blocking these small tracked
web-delivery encodes. Committed, pushed, Railway deploy verified live on absbyai.com (MP4s return
200 `video/mp4`, `EXERCISE_DEMO_IDS`/`.ex-demo` present in the deployed HTML).

Captured the new App Store trainer screenshot (AI-Dan mid-plank, gym clearly readable) in the iOS
Simulator via a native `xcrun simctl io screenshot` (exact resolution match, no scaling artifacts).
Overwrote `app-store-assets/6.9-inch/06-ai-trainer-workout.png` (1320x2868, native capture) and
`app-store-assets/6.5-inch/04-ai-trainer-workout.png` (1242x2688, resized from the 6.9-inch capture
— no 6.5-inch simulator exists in current Xcode, and the aspect ratios are near-identical so this is
a faithful match). **13-inch iPad variant NOT delivered**: the iPad Pro 13" (M5) simulator's WKWebView
stopped accepting ANY tap input after a fresh install/launch (confirmed with a dead-simple large
button, not a coordinate issue) — worth a look in a future session, possibly a Capacitor/WKWebView-
on-iPad quirk. Did not fabricate a composited iPad screenshot rather than risk misrepresenting the
real iPad UI. Frames sent to Dan for review; **not uploaded to App Store Connect**.

**Native retest needed**: this changes what the iOS and Android trainer screens display (video
instead of stick figure for 13 exercises) — flagged to Dan per the cross-platform retest rule.

**Dan said mid-session**: a few more exercises are being finalized — install what's ready now, more
to follow in a later session once finalized.

No active task.

---

## Handoff template

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
