# Shorts from "02 — My Honest Zepbound Update"

Eight Shorts, 1080x1920, 29.97 fps, delivered to `Short-form video content/` as `zep-short1..8_*.mp4`
on 2026-09-01. 540p review copies in `review/`. **$0.00 AI spend** — local Whisper, ffmpeg, PIL,
Apple Vision. No production code, no deploy, no native-retest trigger.

## ⚠ POSTING IS BLOCKED ON THE PARENT VIDEO

The long-form is **not published** and `/youtube-packaging` has never run on it. Standing rule:
Shorts post every 2–3 days AFTER the long-form goes up. **Nothing is queued in Blotato.**

## ⚠ The drug is NAMED in the captions, not in any graphic

Dan's standing copy rule bans the drug name from graphics; every title and eyebrow says "GLP-1"
or "the shot". The burned captions transcribe his speech, and he says "Zepbound" in all eight —
the skill's Step 0 table and the shorts-organic research both record that organic Shorts may name
it. **If any of these ever runs as a PAID creative, re-render it with the name masked in
`captions.js` first.**

## Cut from the CLEAN master, right channel only

Source `CUT_v1_graded_NO-GRAPHICS.mp4` (1827.751 s, 49 EDL ranges). `work/chancheck.py`: L/R
correlation +0.12 at a −7.5 ms lag — two microphones, unrepaired, same as `*_PRE_AUDIOFIX`. Right
channel (the lav, 5–7 dB more dynamic range) as mono, high-pass 75 Hz, an 8-band tone EQ fitted
against `Muhammad Ad Videos/Daniel HQ Fitness AD Video v3 HD.mp4` (shape difference 2.03 → 0.33 dB),
de-esser. **No denoiser, no gate**: measured floor-relative-to-voice on this roll is already 3 dB
cleaner than his ad in every band (29.1/39.4/31.1 vs 25.7/36.1/28.8 dB), and the supplements
batch's gate cost word tails here (98.7 % → 100 % without). Batch tone-match to the median, then
**pure gain + limiter** to −14 LUFS, never loudnorm.

## Layout, measured

| | |
|---|---|
| picture | 1080x1580 at y=340; talk window 738x1080 (1.46x), punch 678x992 from the top |
| his head | at **source row 0 on every beat** — no ceiling to crop; picture dropped to 340 so the headline ink (ends y≤300) keeps 40–50 px of black above his hair |
| crop centre | **per SHOT, HEAD anchor** (see README — the torso-block anchor is bimodal on this waist-cut framing) |
| joins | every one hidden by the wide/tight alternation; no AI cover clips |

## Verification (all on the exact delivered files)

| check | result |
|---|---|
| QC gate `qc.js` | **PASS 8/8** — 1080x1920, 29.97, AAC 48 k stereo, durations on plan, 0 black frames, 0 silent seconds |
| caption-sync gate | **PASS 8/8** — median −30 … +10 ms, first word intact on all eight |
| title clearance | **PASS 8/8** — ink ends y290–300, picture starts y340 |
| **check 17 — centering on the delivered file** | **PASS 8/8** — head anchor, 2 fps, per-shot medians: worst single shot +32 px (A), weighted 5–22 px per short; B and G were nudged −47/+55 px after the first gate read and re-measured at +9/+21 |
| splice discontinuity | 0.00–0.09x of control (threshold 3x) |
| loudness / true peak | −14.0 to −14.2 LUFS, −1.0 to −1.4 dBTP |
| boundary slivers | 0 (11 fixed — see README) |
| review copies | scanned: 0 silent seconds, a/v delta < 0.15 s |
| source reuse | no second of source used twice (asserted in `segments.js`) |
| md5 | delivered files identical to the QC'd builds |

## Posting order and copy

Posting order A→H is the file number. A leads because it is the single most surprising, most
shareable claim in the video and needs no setup; H (the controversial one) is last so the account
has context behind it. UTM: `utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-shortN`.

### 1. `zep-short1_the-shot-that-killed-my-urge-to-drink.mp4`
**Title:** The Shot That Killed My Urge To Drink · **On-screen:** `THE KNOCKOUT ARGUMENT` / `THE SHOT THAT KILLED / MY URGE TO DRINK` · **Source:** 9:59–10:51 (4 pieces; two false starts removed)
> I went from 5–10 drinks a week to one or two, without trying. The single biggest reason I'm staying on a GLP-1 for life.
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-short1

### 2. `zep-short2_inject-thursday-evening.mp4`
**Title:** Inject Thursday Evening. Here Is Why · **On-screen:** `WHEN TO TAKE YOUR GLP-1` / `INJECT THURSDAY / EVENING. HERE IS WHY` · **Source:** 19:59–20:44
> It takes about 24 hours to hit peak effect. If your weekends are where the diet falls apart, this is when to take your shot.
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-short2

### 3. `zep-short3_start-at-1-mg-not-2-5.mp4`
**Title:** Start Your GLP-1 At 1 Mg, Not 2.5 · **On-screen:** `AVOID THE SIDE EFFECTS` / `START YOUR GLP-1 AT / 1 MG, NOT 2.5` · **Source:** 21:38–22:36 (2 pieces; the 15 mg context aside dropped)
> The standard starting dose gave me gas and killed my appetite for days. Going up gradually from 1 mg avoids nearly all of it.
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-short3

### 4. `zep-short4_why-the-needle-beats-the-pen.mp4`
**Title:** Why The Needle Beats The Pen · **On-screen:** `GLP-1 PEN VS NEEDLE` / `WHY THE NEEDLE / BEATS THE PEN` · **Source:** 16:40–17:36 (2 pieces; a 2.1 s dead stretch removed)
> The pen locks you into 2.5 or 5 mg. The needle lets you dose 1, 1.5 or 3 mg, and it hurts less once you're good at it.
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-short4

### 5. `zep-short5_dont-go-above-2-5-mg.mp4`
**Title:** Don't Go Above 2.5 Mg · **On-screen:** `THE DOSE MISTAKE I MADE` / `DON'T GO ABOVE / 2.5 MG` · **Source:** 25:43–26:44 (3 pieces; a stumble and a false start removed)
> 5 mg is for people who are severely obese. If you have 20 or 30 pounds to lose, slower gets you the same result with fewer side effects.
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-short5

### 6. `zep-short6_lose-fat-not-muscle-the-protein-target.mp4`
**Title:** Lose Fat, Not Muscle: The Protein Target · **On-screen:** `THE REAL RISK ON A GLP-1` / `LOSE FAT, NOT MUSCLE: / THE PROTEIN TARGET` · **Source:** 27:06–28:19 (2 pieces; the bulk/cut-cycle riff dropped)
> The biggest risk to your physique on a GLP-1 is losing muscle with the fat. 0.8 g of protein per pound, and what that looks like on the plate.
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-short6

### 7. `zep-short7_compounded-vs-brand-name.mp4`
**Title:** Compounded Vs Brand Name · **On-screen:** `BEFORE YOU BUY A GLP-1` / `COMPOUNDED VS / BRAND NAME` · **Source:** 13:05–14:27 (2 pieces; the legal-status riff dropped)
> Compounded is cheaper. Here's the 5% concentration risk and the contaminant risk you're taking for the discount.
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-short7

### 8. `zep-short8_why-i-take-a-glp-1-with-six-pack-abs.mp4`
**Title:** Why I Take A GLP-1 With Six Pack Abs · **On-screen:** `MY DOCTOR WOULD SAY NO` / `WHY I TAKE A GLP-1 / WITH SIX PACK ABS` · **Source:** 7:04–8:13 (2 pieces; the "old flawed thinking" recap dropped)
> Not medical advice, and it contradicts the medical consensus. Why I think the benefit outweighs the risk even if you're already ripped.
> https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound&utm_content=zep-short8

## The shortlist (14 candidates), and which eight were cut

Dan said "cut 6-8" and was not at the keyboard, so the pick is mine and every one is reversible:
swapping a candidate in is one entry in `segments.js` plus a single re-render (~3 min). Source
times are on the clean master. **Bold = cut.** Every candidate passes the "what does the viewer
walk away with" test; the transformation beat (192→181) was excluded on that rule (it is proof
about Dan, not a tactic for the viewer) and because its two photos were never supplied.

| | candidate | source | viewer takeaway | verdict |
|---|---|---|---|---|
| **A** | **the knockout argument: alcohol** | 9:59–10:51 | the shot removes the urge to drink, 5–10/wk → 1–2 | **cut** |
| **B** | **inject Thursday evening** | 19:59–20:44 | 24 h to peak, so dose for the weekend | **cut** |
| **C** | **start at 1 mg, not 2.5** | 21:38–22:36 | the escalation ladder that avoids side effects | **cut** |
| **D** | **needle beats the pen** | 16:40–17:36 | the needle lets you dose 1 / 1.5 / 3 mg | **cut** |
| **E** | **don't go above 2.5 mg** | 25:43–26:44 | 5 mg is for the obese; 20–30 lb to lose stays at 2.5 | **cut** |
| **F** | **lose fat, not muscle: 0.8 g/lb** | 27:06–28:19 | the protein target and what it looks like on a plate | **cut** |
| **G** | **compounded vs brand name** | 13:05–14:27 | why brand is worth the money (5 % concentration risk, contaminants) | **cut** |
| **H** | **why I take it with six-pack abs** | 7:04–8:13 | the argument, WITH the not-medical-advice beat in full | **cut** — the one controversial beat, per Dan's writing rules |
| I | where to inject: the thigh, don't go deep | 19:00–19:56 | "if it hurts you're going in too deep" | **not cut** — he says "you're seeing it on screen right now" three times about a graphic that does not exist on the clean master; the beat is 31 s once those lines go |
| J | it will not mark your skin | 23:59–24:48 | track-marks myth busted | alternate |
| K | it barely hurts (blood-draw comparison) | 24:51–25:40 | fear removed; ⚠ "I hate that shit" | alternate |
| L | users live longer | 1:45–2:30 | the longevity data | alternate; ⚠ "totally fucked situation" |
| M | 30 pounds is the line | 3:54–4:30 | when the benefit outweighs the risk | alternate; the ex-girlfriend injection line sits just before it |
| N | where to buy it / skip the $100–150 fees | 14:57–16:00 | Lilly Direct via a Walgreens/Amazon script | alternate; names Ro/Hims |
