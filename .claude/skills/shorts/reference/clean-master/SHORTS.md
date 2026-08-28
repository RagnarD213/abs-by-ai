# Shorts from "03 — The Supplements I Actually Take"

Eight Shorts, 1080x1920, 29.97 fps, all delivered to `Short-form video content/` as
`supp-short1..8_*.mp4`. 540p review copies in `review/`.

**$0.00 AI spend** — local Whisper, ffmpeg, PIL, Apple Vision. No production code, no deploy,
no native-retest trigger.

## ⚠ POSTING IS BLOCKED ON THE PARENT VIDEO

The long-form is **not published**. No packaging record exists, `/youtube-packaging` was never
run on it, and it appears in no upload or queue document. The standing rule is to post Shorts
every 2–3 days **after** the long-form goes up, so **nothing here is queued in Blotato and
nothing should be without Dan's say-so.**

## Cut from the CLEAN master, not the delivered one

Source: `CUT_v1_graded_NO-GRAPHICS.mp4` (1409.523 s) — same picture edit as
`FINAL_supplements.mp4`, graded, with no graphics and no stock inserts, and its audio is
already the fixed single-mic chain. The delivered master runs 43 % insert coverage after the
8/27 rebuild, so cutting from it would have made nearly half of every short a full-frame
graphic. `*_PRE_AUDIOFIX.mp4` was never touched — that voice is comb-filtered.

## Layout: full-bleed, and the handoff's premise turned out to be wrong

The handoff expected product shorts to use the **band layout** because "the counter is the
payload" — Dan stands behind the whole supplement stack. Measured instead of assumed:

* From 0:15 to the end, the products on the counter deviate from their own temporal median by
  a mean of **1.07 grey levels**. The stack never changes.
* Across 25 frames sampled inside the four product segments, **he never picks anything up** —
  hands stay gesturing at chest height throughout.

So the counter is set dressing, not payload, and the band layout would have shrunk him to a
third of frame height to preserve a row of packaging nobody looks at. **All eight are
full-bleed 9:16.** The Thorne tubs directly in front of him stay in frame anyway.

## Geometry, measured

| | |
|---|---|
| source window | **644 x 960 at cropTop 120** → 1080 x 1610 at y=310 |
| upscale | **1.68x** — sharper than the V2/V3 full-height 9:16 crops at 1.78x |
| his head lands at | y=406, **96 px clear** of the title band |
| torso centre | **0.6676 – 0.6969**, measured per beat with Apple Vision |

⚠ **The handoff estimated his torso at x 0.60–0.63 from frame grabs. Vision measured
0.668–0.697** — a 192 px error in the delivered frame, i.e. building to the estimate would have
reproduced exactly the off-centre fault this batch exists to avoid. There is **no batch-wide
`TALK_X`**; every shot carries its own measured centre.

⚠ **The AG1 bag is cut by every window and that is the right call.** It sits at x 0.804–0.964
with its printed logo at 0.804–0.946, so no window centred on Dan avoids it. Both alternatives
were measured and both are worse: including the whole bag needs centre 0.776 (255 px off
centre), excluding it needs 0.616 (206 px off, with a dead dark cabinet filling the left
third) — and 133 px is the offset Dan rejected on `v2-short3`. A partly-visible product on a
real counter is set dressing, not a sliced editorial graphic.

## Verification

| check | result |
|---|---|
| QC gate | **PASS, all checks green, 8/8** |
| caption-sync gate | **PASS** — median −60 to 0 ms, no clipped first words |
| title clearance | **PASS 8/8** — title ink ends y291, face/abs begins y399+ |
| splice discontinuity | 0.02x–0.06x of control (threshold 3x) |
| loudness | all **−14.0 to −14.4 LUFS**, true peak −0.8 to −1.3 dBTP |
| review copies | 0 silent seconds, a/v delta 0.000 s on all eight |
| source reuse | no second of source used twice; asserted in `segments.js` |

### 1. `supp-short1_the-3-supplements-that-matter.mp4`  (42.6s)

**Title:** The 3 Supplements That Actually Matter
**On-screen:** eyebrow `IF YOU ONLY TAKE THREE` / headline `THE 3 SUPPLEMENTS / THAT ACTUALLY MATTER`
**Source (shortlist letter B):** 1046.14-1088.72
**Description:**
> The three supplements to start with if you're taking nothing right now, and why they get you about 70% of the benefit of a full stack.
>
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=supp-short1

### 2. `supp-short2_stop-buying-a-big-supplement-stack.mp4`  (44.2s)

**Title:** Stop Buying A Big Supplement Stack
**On-screen:** eyebrow `MY BIGGEST MISTAKE` / headline `STOP BUYING A BIG / SUPPLEMENT STACK`
**Source (shortlist letter E):** 996.49-1040.67
**Description:**
> The mistake I made when I first got into supplements, and the 30-day rule that fixes it.
>
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=supp-short2

### 3. `supp-short3_you-need-5x-more-vitamin-d.mp4`  (49.0s)

**Title:** You Need 5x More Vitamin D
**On-screen:** eyebrow `70% OF PEOPLE ARE DEFICIENT` / headline `YOU NEED 5X MORE / VITAMIN D`
**Source (shortlist letter J):** 282.95-285.89 + 287.74-333.74
**Description:**
> About 70% of people are deficient in vitamin D. Here's the dose I take and why I think the USDA number is too low.
>
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=supp-short3

### 4. `supp-short4_let-ai-pick-your-supplements.mp4`  (41.4s)

**Title:** Let AI Pick Your Supplements
**On-screen:** eyebrow `YOU CAN'T UNDERSTAND THE STUDIES` / headline `LET AI PICK / YOUR SUPPLEMENTS`
**Source (shortlist letter A):** 60.14-74.85 + 98.57-112.96 + 128.54-140.76
**Description:**
> Nobody can actually read all the research on supplements. Here's what I do instead.
>
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=supp-short4

### 5. `supp-short5_the-supplement-that-does-nothing.mp4`  (49.9s)

**Title:** The Supplement That Does Almost Nothing
**On-screen:** eyebrow `MOST TEST BOOSTERS DO NOTHING` / headline `THE SUPPLEMENT THAT / DOES ALMOST NOTHING`
**Source (shortlist letter M):** 674.47-724.31
**Description:**
> The supplement in my stack that's most likely doing nothing, and the one ingredient in it that actually works.
>
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=supp-short5

### 6. `supp-short6_if-you-take-one-take-fish-oil.mp4`  (32.3s)

**Title:** If You Take One Supplement, Take Fish Oil
**On-screen:** eyebrow `THE MOST PROVEN SUPPLEMENT` / headline `IF YOU TAKE ONE THING / TAKE FISH OIL`
**Source (shortlist letter C):** 419.56-451.83
**Description:**
> If you only take one supplement, take this one. It's the most proven thing you can buy.
>
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=supp-short6

### 7. `supp-short7_you-should-be-taking-creatine.mp4`  (39.5s)

**Title:** You Should Be Taking Creatine
**On-screen:** eyebrow `THE ONE I DON'T TAKE` / headline `YOU SHOULD BE / TAKING CREATINE`
**Source (shortlist letter H):** 934.83-974.28
**Description:**
> The supplement I don't take myself but think most people should.
>
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=supp-short7

### 8. `supp-short8_supplements-are-only-5-percent.mp4`  (58.3s)

**Title:** Supplements Are Only 5% Of Your Results
**On-screen:** eyebrow `THE HARD TRUTH ABOUT PILLS` / headline `SUPPLEMENTS ARE ONLY / 5% OF YOUR RESULTS`
**Source (shortlist letter D):** 1244.57-1302.80
**Description:**
> Supplements are about 5% of your results. Here's why I still take them.
>
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=supp-short8
## Flags for Dan

| item | where | note |
|---|---|---|
| **"You are not smart enough to understand scientific research"** | short 4, opening line | You reviewed and kept this on 8/20. It is the hook. Still spicy for anything paid. |
| **"if you're fat and broken and you say stupid things"** | short 8, ~0:38 | The joke landing. Fine organically; flag before anything paid. |
| **"It reduces your risk of cancer"** | short 6, ~0:10 | A health claim, compressed into a 32 s Short. It is in the parent video and it is your opinion on camera — but it is the one line here most likely to attract a YouTube medical-claims flag. One word to cut it. |
| **"the level of diarrhea and gas that I get"** | short 7, ~0:22 | Your words, on register. |
| **Brand names** (Thorne, Athletic Greens/AG1, Isopure, Anthony's, Cure) | throughout | Correct and allowed — you name them on camera. |
| **No before/after side-by-side** | — | None exists in this video; nothing was added. |

**Not built, and why:** [F] pre-workouts ends on a Zepbound recommendation and you did not rule
on the drug name; [I] whey protein carries "I just uncontrollably shit myself" *and* a sentence
that does not parse as transcribed; [L] skin needs a 248→180 word trim and names a third-party
influencer; [N] joint health drifts into the bragging failure mode that killed `v6-short1`;
[K] is the least distinctive; [P] curcumin is only 29 s.

## Caption notes

* Standing rules applied: `abs` prints lower case, `AI` upper case; the title holds for the
  whole short on the black field and never touches his face or abs.
* **Mis-hearings corrected, each checked against two other independent transcriptions of the
  same audio:** `phytoplasmic acne` → `fighting cystic acne` (short 5), `Thorn` → `Thorne`.
* `Shilajit mushrooms` is left as spoken — all four transcription runs agree that is what he
  says, and captions transcribe speech.
* Short 6 prints "Especially, especially if you're not eating a lot of fish" — he does say it
  twice, confirmed against 1.06 s of continuous speech before "if".

## ⚠ Two pipeline defects were found and fixed during this build

Both would have shipped, and both are recorded in `work/TIMELINE_TRAP.md` and the skill.

1. **The source's two timelines disagree.** This master was assembled from 62 concatenated
   ranges and its AAC stream holds 0.76 s more audio than its container declares, spread
   through the file. Whisper word timestamps and the silence map live on the decoded-sample
   timeline; the cuts and the picture live on the container timeline. The first build shipped
   **captions 280–650 ms late** and clipped the first word off two shorts — while passing every
   existing gate. Fixed by extracting analysis audio with `aresample=async=1:first_pts=0`, and
   there is now a **preflight** check and a **caption-sync gate** wired into `qc.js`.
2. **Zero-duration Whisper words were silently dropped from captions.** The `>50 % overlap`
   test computes `0/1e-6 = 0` for a word with `start == end`, so it failed. Nine such words on
   this roll; it ate one in five of the eight shorts, turning "creatine is not an **option** for
   me" into "not an for me". This affects every batch previously cut with this code.
