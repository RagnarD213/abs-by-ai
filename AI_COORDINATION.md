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

### iOS THIRD REJECTION FIXED — resubmitted to Apple 2026-08-22 (Claude Code)

`Handoffs/handoff-20260821-ios-third-rejection-fix.md` executed. **Submission
`a5fcdbf2-3eca-412e-8c20-b1f075a32c24` sent 2026-08-22 19:12 UTC with all 4 items
WAITING_FOR_REVIEW**: app version 1.0 build 3, subscription group 22294450, Monthly
(`com.absbyai.app.membership.monthly`), Annual (`com.absbyai.app.membership.annual`).

**2.1(b) (IAP never submitted) — resolved.** Both products carry an App Review screenshot of the
in-app paywall (`app-store-assets/iap/paywall-membership-screen.jpg`, captured on the non-comp
account `+iostest1`, NOT the comp demo account) plus reviewer notes. Build 1.0 (3) archived,
validated and uploaded via `altool`; ASC auto-attached it. No app code changed — the bump was purely
Apple's requirement.

**1.1 (\"app morphs body parts\") — fought, not conceded.** Photo feature kept. Metadata rewritten so
coaching leads (`app-store-assets/LISTING_COPY.md` is canonical): new description (2,185 chars) and
promo text, and the screenshot sets rebuilt — iPhone is now trainer workout → plank exercise demo →
macro tracker → nutritionist → home hero last; iPad is trainer → nutritionist → home hero. **Every
before/after morph pair was removed except the one labeled \"AI AFTER\" home hero**, kept deliberately
so the listing still represents the app honestly. Reply drafted and Dan-approved in
`app-store-assets/APP_REVIEW_REPLY_20260821_G11.md`.

**THE TRAP THAT CAUSED 2.1(b), now documented in the reply doc:** a version can belong to only ONE
submission. The version sat in the dead rejected submission `be7d8b49` while the subscriptions sat in
a new draft, and ASC's \"Update Review\" button keeps re-attaching it to the OLD one — silently
splitting them. Fix: red minus in the rejected submission's ACTION column to remove the version, then
`POST /v1/reviewSubmissionItems` with an `appStoreVersion` relationship to add it to the draft (the
UI's button greys out at that moment; the API works). The subscription GROUP is also its own separate
submission item.

**THE REPLY CHANNEL IS GONE — the 1.1 argument now lives in App Review Notes.** Removing the version
from submission `be7d8b49` closed that thread and its "Reply to App Review" link disappeared with it.
Net still positive (the alternative was a guaranteed repeat 2.1(b)), but **next time: post the reply
BEFORE removing the item.** Replacement Notes text (3,901 chars, fits the 4,000 cap, leads with the
four-point 1.1 argument and keeps every Guideline 2.1 answer Apple demanded on 2026-08-17) is
`app-store-assets/APP_REVIEW_NOTES_20260822.txt` — supersedes `APP_REVIEW_NOTES_20260817.md`.
**Notes field APPLIED 2026-08-22 via `PATCH /v1/appStoreReviewDetails/{id}` (200) — verified live at
3,901 chars, opening with the 1.1 argument.** The ASC API accepts a Notes edit while the version is
WAITING_FOR_REVIEW, so this needed no UI step. **Nothing manual remains; the task is closed.**

**Deferred to 1.0.1 (after approval):** fuller screenshot set incl. Sleep Coach + Supplement Audit,
and an iPad-sized exercise-demo capture (2064×2752).

**Test-account note:** `danroseconsulting+iostest1@gmail.com` (users.id 20) had its expired sandbox
membership cleared, then was set to comp (`status=comp, plan=beta`) to capture the trainer screenshot.
Leave or clear as convenient — it is a test account, not a customer.

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


### MODERN-EDIT 60s SAMPLE — REV 1 DELIVERED, all four of Dan's notes applied (2026-08-22, Claude Code)

Head-to-head sample against Muhammad A's Upwork trial edit. **$0.00 AI spend across both rounds**
(local Whisper/ffmpeg/PIL/numpy). Delivered to `EDITED ADS 8-20-26/ad1-how-ai-got-me-abs/`:
`SAMPLE_modern-edit-60s_rev1_16x9.mp4` (65.8s), a 720p review copy,
`SAMPLE_compare_trial-vs-pipeline_rev1.mp4`, the pre-graphics rollback, every script, and
`notes_modern_sample.md`. **rev-4's ad chain was NOT touched.**

**Dan's rev-1 notes, all four done.** (1) **Graphic screens rebuilt to HIS design in J2 dark
green** — he compared both and picked his structure: a solid brand FIELD (not a white page with a
card), photos straight on the field, big heavy type, tight leading, top-aligned blocks, accent
rules/bands, square list markers, oblique caps in an accent band. Every number measured off his
frames by pixel scan then solved back into Manrope sizes. (2) **Grade re-fitted PER CHANNEL to his
percentiles** — the real gap was never brightness: rev-0 crushed blacks to [0,5,0] vs his [10,10,12]
and ran the blue midtone 22 levels under his. Now p10/p50/p90 match within 1–2 levels on all three
channels. (3) **Audio de-roomed** — ours measured 3 dB hot at 3.2–8 kHz (where reverb lives) and
5.5 dB thin at 400–700 Hz; that combination *is* the "echo". EQ-matched (mean error 9 bands:
2.6 → 1.2 dB), gentle downward expander for the tails, light compression (LRA 3.8 → 1.9 LU, his note
"a little flatter"). (4) **"Where I'm at today" is the shoot photos again**, not the ab-workout
b-roll.

**Re-transcription QC earned its keep twice this round**: the expander at first settings ate the /f/
in "for free" and the "n't" in "isn't" (97.9 → 96.0 %), and after fixing that the music bed was
still masking "isn't" until the sidechain release went to 420 ms. Final **97.4 %**, −14.2 LUFS,
**0 bare visible splices** (20 of 21 cuts under a graphic or on a punch change), visual change every
3.3 s.

**The reusable output: `.claude/skills/ad-edit/reference/motionlib.py`** (now palette-driven —
`GREEN` is the locked CONTENT style, `PAPER` kept for ads) and **`sfxlib.py`** (synthesised
one-shots, no licence to track). Worked example in `reference/modern60/`. Skill lessons 25–31 and
four decision rows added.

**Music = *Werq* (Kevin MacLeod, incompetech) — CC BY 4.0, needs a description credit.** Fine for a
sample; budget a paid library if this becomes house style. One constant to swap.

Compliance unchanged: AI-GENERATED on all three AI assets, before/after **sequenced not
side-by-side** (verified frame-by-frame). Flagged for Dan: his own ~200 lb before photo on screen
6.1–7.8 s (already shipped in rev-1…rev-4, neutral shot, left in).

**EXACT NEXT ACTION — DAN: watch rev-1 and decide the editing stack.** One honest gap left: he is
4.3 s shorter on the same words (his extra cuts are inside words; ours only in measured silence).
No native retest trigger — video files only, no product surface.

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

### Exercise demo BATCH 2 — INSTALLED IN THE APP, all 20 live (2026-08-22, Claude Code)

Dan approved the full set on 2026-08-20; installed and deployed 2026-08-22. Encoded each
`<id>-AIDAN-narrated-FINAL.mp4` to 960x540 web mp4 + poster jpg into
`public/exercise-demos/<id>.{mp4,jpg}` (41MB total for all 33 exercises now installed), added
the 20 ids to `EXERCISE_DEMO_IDS` in `public/index.html`, renamed the `db-lateral-raise` library
entry's `name` to "Side Lateral" per Dan's request (id unchanged — programs reference it), and
installed `side-lateral`'s video under that same id. Committed (`2cddc76`), pushed, Railway
deploy verified — all 20 `.mp4` files return 200 live on absbyai.com, "Side Lateral" confirmed
in the deployed `exercises.js`. **This IS a native-retest trigger** (changes what the iOS/Android
trainer screens display) — flagged to Dan.

The 20: side-plank, wall-sit, hollow-hold (static holds) · knee-pushup, pike-pushup, chair-dip,
split-squat, glute-bridge, calf-raise, crunch, lying-leg-raise, superman (bodyweight) · pullup,
lat-pulldown, seated-cable-row, leg-extension, leg-curl, db-shoulder-press, db-curl, side-lateral (gym).

**`bw-squat` (the original pilot) is NOT installed and NOT finalized** — checked its folder: only
an unstamped `bw-squat-AIDAN-narrated.mp4` exists (no `-FINAL` suffix, no Dan approval), predating
the double-pump-rule and background-lock fixes later batches used. It would need a regeneration
pass through the current `/exercisegeneration` pipeline before it could ship, same as any new exercise.

Everything learned across the five revision rounds is consolidated in `/exercisegeneration`: the
DOUBLE-PUMP RULE (monotonic cuts + unimodal verification), the FULL-FRAME BACKGROUND LOCK
(`_r2/lockbg.py`, supersedes box-hunting), landmark tracking when frame-diff lies, reverse-generation
for poses Veo won't reach, and Dan's settled form standards per exercise. Scripts live in
`Media/exercise-demos/_batch2/` and `_r2/`.

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

### YouTube subscriber-campaign geo restructure — HANDOFF WRITTEN, not executed (2026-08-22, Claude Code)

`Handoffs/handoff-20260822-youtube-ads-geo-restructure.md` + Rule-5 Key dashboard task added
(verified persisted). **Strategy session only — no ad-account change made, no code touched, no deploy.**

Dan's three asks are scoped in the doc: (1) add all ~250 countries as explicit targeted locations on
the All Countries campaign, (2) exclude the low-quality geos (full Tier-1 list in the doc; Tier 2 —
India, Philippines, Indonesia, Vietnam, Thailand, Malaysia, South Africa, Brazil, Mexico, Turkey,
Colombia, Peru, Ecuador, Dominican Republic — stays targeted deliberately as the cheap-volume engine),
(3) clone the campaign targeting only US/CA/UK/IE/AU/NZ.

**VERIFIED FACT that killed Dan's original plan:** the campaign runs **Target CPA**, and on Smart
Bidding all non-device bid adjustments are **ignored** — a location bid modifier would have been
accepted by the UI and silently done nothing. Confirmed against Google's own docs. Budget separation
(separate budgets, NOT shared) is the only lever that forces geo allocation.

**STEP 0 IN THE DOC MAY REFRAME EVERYTHING:** earned subscribers aren't a Google Ads conversion
action, so it is unknown what that tCPA campaign has actually been optimizing toward. Find out before
changing anything; if conversion volume is near zero, the clone should launch on Maximum CPV.

**Highest-consequence setting on the clone:** location option must be **"Presence"**, not "Presence or
interest" — the default reimports the exact problem the clone exists to avoid, and fails quietly.

Dan's position, recorded because it drives the plan: he believes sub count under 10k gates whether
people take the channel seriously, so the cheap campaign keeps running to 10,000 and is then paused —
the authority number is a one-time purchase, not an ongoing strategy.

**EXACT NEXT ACTION — run the handoff in a fresh session** (Opus 5, Medium), starting with Step 0.

No active task.

---

## Handoff template

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
