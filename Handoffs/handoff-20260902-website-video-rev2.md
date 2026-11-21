# Handoff: Website conversion video — REVISION 2

**Created:** 2026-09-02 · **Runner:** Fable 5.1, extra-high effort (Dan's call) · **Skill:** `/ad-edit`
**Working dir (all intermediates, on the Extreme drive):** `/Volumes/Extreme/_edit_work/website-video-828/`
**Delivered rev 1 (rejected):** `claude edited long form content/06 - Website Conversion Video (post-generation)/website_video_16x9.mp4`
**Reference for audio AND look:** `Muhammad Ad Videos/this picture got me abs | muhammad | 16x9.mp4` (project folder, 3:52, his Ad 1 cut — the file Dan pointed at)

## What this video is

The 16:9 video that plays on absbyai.com right after a visitor generates their goal image — the
last thing they watch before they buy. Brief: **clean and trustworthy, no fast cuts, nothing flashy.**
Script: section 4 of the Shoot 5 doc (`1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`). Footage:
8/28 shoot, rolls **C1650** (script through "charged a dime") + **C1651** (price line re-read at
$19.99 + the close). Rev 1's cut, transcript, EDL and grade are all fine and stay. **Three things
were rejected, in this order of severity: the audio, the framing, the graphics.**

## Dan's rev-1 review, verbatim where it matters

> "The audio is no good. We need to make it sound like Muhammad's video… It sounds like we still have
> the two-channel audio issue going on. We've got to change our skill so this doesn't keep happening."

> "The opening shot is much too wide. I don't want to use this wide shot ever. I want to go in
> significantly tighter. It should crop between having my head and my belly button in the frame, and
> the top of my head and my shorts visible, with the counter barely visible. Don't use that ultra-wide
> crop for this video at all. This was shot in 4K intentionally from far away so we have room to
> punch in, but don't ever use this super wide crop. Many of these shots also have a light in the shot.
> That's totally unacceptable."

> "0:21 remove this image. 0:29 remove that image — that is the opposite of what we're trying to
> convey [belly fat, not being fat]. 0:31 repeated footage, remove. Move the fat/before picture to
> where I say 'I've been out of shape'. Where I say 'I've been in shape' [= "now at 40 I have the
> most defined abs of my life"] display the images of me from the photo shoot looking ripped — **all
> the same photos Muhammad did in his ad**. 0:57: keep the camera scene and put this graphic next to
> me in the camera scene — it looks weird with a graphic on the left and a huge amount of black space;
> a little wider crop is OK to accommodate it. Remove [the assessment screen] — what we want them to
> look at is their image and then the stats, body-fat stats, and everything below that. Remove this
> [1:53 bullets]. 2:07 remove this — this graphic looks awful with the stick figures in it and the
> black space. Remove the graphic at 2:33 — just a bunch of text, generic, too much black space."

> "Overall the color correction is looking good. The footage looks good. The zoom being way too far
> away and the audio are the most serious issues. The third most serious issue is the horrible
> graphics. Graphics sparingly — much more sparingly. When we do put in a graphic it can't have black
> space over half of the screen. If a feature we're bragging about looks lame in the app, better not
> to show it at all."

## 1 — AUDIO (most serious). What was actually wrong, measured

It was **not** the two-mic comb filter this time — the delivered file reads L/R **+0.998**, the lav
alone. It was the **floor**. New gate `reference/voice_ref_check.py` (in `/ad-edit`) measured the
delivered mix against Muhammad's ad:

| | Muhammad's ad | rev 1 delivered | raw lav a:1, untouched |
|---|---|---|---|
| voice over floor, 80–250 Hz | 27.6 dB | **18.1** | 35.5 |
| voice over floor, 250 Hz–1 k | 34.7 dB | **25.1** | 42.5 |
| voice over floor, 1–4 kHz | 28.0 dB | **20.2** | 35.8 |
| dryness (drop 64 ms after a word) | 7.4 dB | 6.9 | 9.3 |
| 10-band tone error vs his | — | mean 1.70 / max 2.83 | mean 2.48 / max **7.5 (5.5 kHz, −7.5)** |

**The raw lav is 8 dB CLEANER than his ad. The chain made it 9.5 dB dirtier** — the music bed at
−23 dB + a 3:1 compressor with makeup + two treble shelves (+4.6 @3.5 k, +3 @6.5 k) lifted everything
between the words. That is what Dan hears as "the two-channel issue": a wash under the voice.

**Rev-2 audio recipe (then PROVE it with the gate, then ship an A/B):**
1. Start from `audio/C1650.right48.wav` / `C1651.right48.wav` (the lav, a:1) — already extracted.
2. **No compressor.** His LRA is 3.5; ours went to 2.4. Use at most a gentle 1.5:1 above −18 dB.
3. **EQ fitted to his ad, not copied from Ad 3.** The raw lav vs his: +5 dB honk at 600–1.4 k (cut
   ~3 dB at 900 Hz, Q 1.0), thin at 150 Hz (+2.5), and **−7.5 dB at 5.5 k+** — that air has to come
   from a shelf, and a shelf lifts hiss, so pair it with a gentle downward expander
   (`agate` threshold ~0.012, ratio 1.8, range 0.35, release 250) and re-measure the floor.
   `reference/fitvoice_longform.py` / `modern60/fitvoice.py` do the band fit; run over 5 windows.
4. **Bed at −30 dB or lower**, ducked with `sidechaincompress` release 420 ms — or no bed at all.
   His floor between words is what the gate measures; the bed counts.
5. Loudness: keep −14 LUFS integrated with the **gain + limiter** finish (`audio2.py`, never
   `loudnorm` — it went DYNAMIC on this mix). His master is −18.2; if Dan A/Bs by ear and ours
   sounds "pushed", a −16 master is one number.
6. **Gate:** `python3 .claude/skills/ad-edit/reference/voice_ref_check.py <mix> --ab AB_his-vs-ours.mp4`
   must print `AUDIO GATE PASSED`. Send the A/B clip with the review copy. **Do not deliver on a FAIL.**

## 2 — FRAMING (second). Never the wide shot again

Read off the 4K source frame with a burned grid (`pv/grid4k_lab.png`), Dan centred at **x≈1980**:
head top **y≈100**, chin ≈330, navel ≈1290, shorts waistband ≈1580, counter top edge behind him
≈1720, **the studio light enters at x≈3560**.

| level | crop (3840×2160 source) | zoom | what it shows |
|---|---|---|---|
| WIDE (the widest allowed) | 3058×1720 @ (451, 40) | 1.256× | top of head → shorts, counter barely visible, **light excluded** |
| MID | 2650×1490 @ (655, 40) | 1.45× | head → hips |
| TIGHT | 2311×1300 @ (825, 40) | 1.66× | head → belly button (Dan's stated tight frame) |

- **Re-render `base.mov` at full 3840×2160** (`base.py`, change the `scale=` in `grade.txt` to
  3840:2160 or drop it) so TIGHT is still a downscale to 1920. Rev 1's 1440p base makes 1.66× a
  1.25× upscale. Cost ~30 min. Everything downstream (`env.py`, `tight.py`, `layout.py`) reads
  base/tight dimensions from constants — set `SW,SH=3840,2160` in `layout.py`.
- Levels alternate WIDE/MID/TIGHT the way rev 1 alternated A/B/C; keep the 9 s minimum hold and the
  hardest-first splice cover. The "a little wider to fit the phone" crop for the PiP beat is the WIDE
  level with Dan pushed to one side (see §3).
- **No level may ever show x>3500 (the light) or the full frame. Assert it in `layout.py`.**
- Look at Muhammad's own framing in his ad (`pv/muhammad_sheet.jpg`): he holds Dan from the top of
  the head to the waist, filling the frame. That is the target.

## 3 — GRAPHICS (third). Sparingly, and never on a black field

Rev 1 had 21 beats; **rev 2 keeps about eight.** Per-beat, in rev-1 timecodes:

| rev-1 beat | Dan's note | rev 2 |
|---|---|---|
| 0:03 NAME lower third | not mentioned | keep |
| 0:18 POOL photo | "0:21 remove" | **remove** |
| 0:28 BEFORE photo over "belly fat finally lost" | "opposite of what we convey" | **move** — starts on "Now I've been out of shape" only, ends before "and now at 40" |
| 0:32 TODAY (photo-158, photo-172) | "repeated footage" | **replace** with **Muhammad's four photos**, in sequence: `00 ASSETS USED IN THE REFERENCE AD/04_SHOT1…07_SHOT4`, on "now at 40 I have the most defined abs of my life" |
| 0:50 NUM1 lower third | not mentioned | keep |
| 0:57 MACRO phone panel, black field left | "keep the camera scene, put it next to me" | **PiP over the footage**: the phone recording (`app-flow-macro-tracker-itemized.mp4`, same slices) as a phone-shaped inset at ~560 px tall beside Dan in the WIDE level, Dan pushed to the other side of the crop. No field, no plate — a thin olive hairline at most |
| 1:16 FLYBLIND lower third | not mentioned | keep |
| 1:23 NUM2 lower third | not mentioned | keep |
| 1:32 ASSESS screenshot panel | "remove — they should look at their image and the stats below it" | **remove**. (Dan on camera; the viewer has their own screen in front of them) |
| 1:53 TELLAI bullets | "remove" | **remove** |
| 2:05 WORKOUT screenshot (stick figures) | "remove, awful" | **remove** — and never show that screen again |
| 2:17 NUM3 lower third | not mentioned | keep |
| 2:26 MEALPLAN screenshot | not named, but the same class | **remove** |
| 2:35 MEALBUL bullets | "remove, generic text" | **remove** |
| 2:47 SLEEP daily-brief screenshot | not named | **remove** (sparingly) |
| 2:57 TRIAL card | not named | keep, but **restyle** (below) |
| 3:02 TRYLIST bullets | not named, same class as 2:33 | **remove** |
| 3:10 CANCEL lower third | not mentioned | keep |
| 3:22 PRICE card | not named | keep, restyle |
| 3:36 SOLVED goal image | not named | keep (his own AI goal image, tagged) |
| 3:47 CTA end card | not named | keep, restyle, holds to the last frame |

**Restyle rule for anything that is not a lower third:** look at Muhammad's panels in
`pv/muhammad_sheet.jpg`. His field is a **mid-olive gradient**, roughly (84,93,55)→(141,152,97),
with Dan filling the other half of the frame — never a near-black field with one small element on
it. The measured version of his system is `reference/orglib.py` in `/longform-edit` and
`motionlib.MIL`; use those, not `J2AD` black. A full-frame card (TRIAL/PRICE/CTA) is acceptable only
if the type fills the frame the way his title cards do — big, oblique caps in a band — otherwise
make it a side panel with Dan still on screen.

**Standing rules from this review (now in the skill):** graphics sparingly; no graphic with more than
~40 % empty field; app screens go next to Dan in the footage, not on a plate; **if a feature looks
lame on screen, don't show it** (the stick-figure workout screen is the example); a photo run for
"how I look today" is Muhammad's four shots.

## 4 — Everything that stays from rev 1

- The EDL (`edl.json`, two rolls, all edges in measured silence, 0 orphan speech runs), the tight
  pass (50 pauses shortened, 203 wpm), the grade (S-Log3 LUT at 1.45×, sat 0.88 — Dan: "the color
  correction is looking good"), the captions build (136 cues; keep suppressing over full cards),
  `hard_splices.py` cover, the QC gate, the watch pass.
- Take selection: hook is C1650 14.5 s; the $20 slip is cut; CTA is C1651 take 2.

## Delivery checklist (do not skip)

1. `voice_ref_check.py` PASSED on the exact delivered file, A/B clip built and sent.
2. Contact sheet at 1 frame / 5 s: **no frame shows the light, the full-wide frame, or a black field**.
3. `qc.py` PASSED (update its `covered` / `SUP` lists for the new beat sheet), `watch.py` run,
   0 silent seconds on master and review copy.
4. Deliver over the same filename in the project folder; keep rev 1 as `*_REV1_REJECTED.mp4`.
5. Update the `notes.md` beside it; check the Key dashboard task off; update `AI_COORDINATION.md`.

## Starter prompt (paste into a fresh session)

> Execute `Handoffs/handoff-20260902-website-video-rev2.md` with `/ad-edit`. It is revision 2 of the
> website conversion video from the 8/28 shoot; rev 1 was rejected on audio, framing and graphics
> and the handoff has the measurements and the exact fixes. Start with the audio: build the rev-2
> voice chain against Muhammad's ad and make `reference/voice_ref_check.py` pass before touching
> anything else. Then re-render the base at 4K and the three tight framings. Then the reduced
> graphics set. Send the 540p review copy and the audio A/B clip when QC and the watch pass are green.

Recommended: **Fable 5.1, extra-high effort** (Dan's choice). Budget: $0.00 AI generation spend is
expected — every asset already exists.
