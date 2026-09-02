# Handoff: Website conversion video — REVISION 3

**Created:** 2026-09-02 (same day rev 2 was delivered and reviewed) · **Runner:** Fable 5.1, extra-high
effort (Dan's standing choice for this video) · **Skill:** `/ad-edit` (read lessons 82–100 first)
**Working dir (all intermediates, on the Extreme drive):** `/Volumes/Extreme/_edit_work/website-video-828/`
**Delivered rev 2:** `claude edited long form content/06 - Website Conversion Video (post-generation)/website_video_16x9.mp4`
(rev 1 is beside it as `*_REV1_REJECTED.mp4`; rev 2's recipe is in `recipe/`, rev 1's in `recipe_REV1/`)
**Reference for audio AND look:** `Muhammad Ad Videos/this picture got me abs | muhammad | 16x9.mp4`

## What this video is

The 16:9 video that plays on absbyai.com right after a visitor generates their goal image — the last
thing they watch before they buy. Brief: clean and trustworthy, no fast cuts, nothing flashy. Footage:
8/28 shoot, rolls C1650 + C1651 (S-Log3 4K, lav on a:1). Script: section 4 of the Shoot 5 doc.

## Dan's rev-2 review, verbatim (2026-09-02, 4:13 PM)

> Okay, the audio is sounding much better. The frame is improved, but still not good, so we need to
> crop more above the head. There's too much space above my head in this opening shot. We need to
> crop in closer above the head. Just leave a minimal amount of space above my head, and you can show
> more of the counter if you want to zoom out. The close shot is even worse. Even more space above my
> head. We need to only keep a minimal amount of space above my head, not this much. This is not a
> good crop at all. Very, very bad crop. Basically, the crop should be lower overall. It should be
> just a little bit of space above my head, and then more on the bottom, with the shorts and the
> counter visible. At 32 seconds, I repeat, "I've been out of shape, and that can't happen again."
> Remove that repeated footage and check more thoroughly for repeated footage in the future. At 53
> seconds, we need to move the graphic down a little bit so it doesn't overlap with the captions.
> This issue recurs throughout the video. You got to move the graphics down so they don't overlap
> with the captions. Let's make this a standing rule going forward. All right, overall feedback:
> audio, you got it nailed. This is the audio that we want. The frame is better, but still not good.
> The main issue with the video is that excessive space above my head in all the shots. We need to
> crop in closer and also lower throughout the video. We also want to make sure that captions don't
> overlap graphics.

**Verdict, in order of severity:** (1) headroom — every shot, the tight ones worst; (2) the repeated
line at 0:32; (3) captions colliding with the lower thirds, every lower third. **Audio is APPROVED —
do not touch it.** Colour, cut, graphics set and card design were not questioned.

## 0 — What is locked and must not change

- **The audio chain, verbatim:** `audio3.py` (fitted EQ, expander, no compressor, bed at −44 dB,
  gain + limiter finish). Dan: "This is the audio that we want." Re-run it unchanged on the new
  picture; the gate (`reference/voice_ref_check.py --ab`) must still print `AUDIO GATE PASSED` on the
  exact delivered file, and the A/B clip goes out with the review copy again.
- The EDL, the grade, the 4K base (`base.mov`, already rendered), the 13-beat graphics set, the card
  designs (`gfx2.py`), the phone PiP, the caption style. The tight cut stays except for the one cut in §2.

## 1 — FRAMING (most serious): the crops were anchored to a frame that is not in the video

**Measured cause.** Rev 2's three levels were top-anchored at a fixed y=40 because a grid frame
(`pv/grid4k_lab.png`) read Dan's head top at y≈100. `headtrack.py` (new, in the work dir and in the
skill's `reference/website-video/`) measured the head top every 0.5 s across the whole 4K tight cut:

| head top in the 4K frame | value |
|---|---|
| minimum (he stands tallest) | **296** |
| 10th percentile | 316 |
| median | **336** |
| 90th percentile | 460 (partly detector misses, see below) |

So his head sits ~300–340 px down the 4K frame, not 100. With y0=40 that put **168–232 px of headroom
at 1080p on his tallest frames** (16–21 % of the frame), worst on TIGHT — exactly "the close shot is
even worse." The counter's near edge is at 4K y≈1570–1600 and the shorts line just above it, so "shorts
and counter visible" means the crop bottom must reach ≥ ~1700.

**The fix: anchor every crop to the measured head, not to the frame.**

1. Run `python3 headtrack.py` (already run; `headtrack.json` is in the work dir). Detector: first row of
   the centre band (4K x 1800–2160) that is ≥30 % skin, minus a 40 px hair allowance. ⚠ When he looks
   down (e.g. 65 s, "take a picture of your food") the forehead fails the skin test and the value jumps
   to 600–800: those are MISSES, not head positions. **Use the per-segment MINIMUM** (misses only go
   down, never up) — or improve the detector with a temporal median over ±1 s. Validate on
   `pv/headtrack_check.jpg` (red line = head top) before trusting it.
2. In `layout.py`, replace the fixed `y=40` with a per-punch-segment `y0 = seg_min_head_top −
   HEADROOM` where `HEADROOM = 0.03 × crop_h` (≈30 px at 1080p — "just a little bit of space above my
   head"). Keep the crop widths/zooms; keep x centred on 1980. Clamp `y0 + h ≤ 2160`. Assert
   `0 ≤ y0 ≤ 500` and re-assert the light guard (`x + w ≤ 3530`).
3. Resulting levels with the global minimum (296) — the per-segment values will sit within ~40 px:

| level | crop | y0 | bottom edge | shows |
|---|---|---|---|---|
| WIDE 1.256× | 3058×1720 | ≈250 | ≈1970 | head → shorts + the counter, plenty of it |
| MID 1.45× | 2650×1490 | ≈250 | ≈1740 | head → shorts line / counter edge |
| TIGHT 1.66× | 2312×1300 | ≈255 | ≈1555 | head → navel, just above the shorts |
| PIP (WIDE, x=0) | 3058×1720 | ≈250 | ≈1970 | same as WIDE, Dan at 65 % |

   Dan explicitly allowed zooming out ("you can show more of the counter if you want to zoom out"):
   if TIGHT at 1.66× still reads as cramped once the headroom is fixed, drop it to ~1.55× (head →
   shorts line) rather than adding headroom back. Never add headroom.
4. **New QC check (must exist before delivery):** run the same detector on the DELIVERED 1080p master
   every 0.5 s and assert the head top is within **15–60 px of the top edge** on every sample where a
   head is detected, and that no sample has the head cut (head top < 0). Print the distribution. Put the
   worst three frames in the watch strips. This is what would have caught rev 2 before Dan did.
5. Punch changes now also move the crop vertically a little (per-segment y0). That is fine — they are
   cuts — but keep the eyeline anchored: the head top lands at the same ~30 px in every level.

## 2 — The repeated line at 0:32

**Measured.** An isolated medium.en pass over tight 28–37 s reads: *"…finally lost. Now, I've been out
of shape, I've been out of shape, and now at 40, I have the most defined abs of my life."* The first
attempt is tight **31.44–32.26** ("I've been out of shape,"), the restart is **32.86–33.74** and flows
into "and now at 40" (33.86→). Whisper's full-roll pass had stitched this into one stretched token —
`and` timed **32.21–33.96 (1.75 s)** — which is why `orphan_scan.py` reported 0 orphans: the stretched
interval covered the energy. (Source: C1650 ≈ 47.0–51.2 s; the tight cut already removed a pause
inside this span, so measure on the tight timeline.)

**Fix.** Cut the FIRST attempt and keep the fluent restart (later fluent take wins): remove tight
**≈31.30 → ≈32.80**, with both edges snapped into the measured −40 dB pauses (31.18–31.44 after
"Now," and 32.26–32.86 before the restart). Result: "Now, I've been out of shape, and now at 40…".
Do it as an extra entry in `tight_cuts.json` → re-render `tight.mov` from the 4K base (or a two-range
trim of the existing tight.mov, `-c:v` re-encode at CRF 15), then `hard_splices.py`, `beats.py`
(phrase anchors re-place every beat automatically), and rebuild the card MOVs whose beats changed
length (`FORCE=1 python3 gfx2.py before today`, then `ffprobe` every reused MOV against its beat —
lesson 95).

The splice sits under the BEFORE card, so it needs no punch cover — but the BEFORE beat shrinks to
~1.3 s ("Now, I've been out of shape,") with "now at 40" arriving ~0.3 s later. Use 0.25 s fades on
the before card and keep it fully out ≥0.2 s before the first after photo fades in (before → Dan →
after, never a shared frame). If that is too brief to read, the acceptable alternative is to start the
before card on "Now," and let TODAY start on "at 40" instead of "now" — never overlap them.

**Check the rest of the cut the same way (Dan: "check more thoroughly for repeated footage").**
`reference/repeat_scan.py` (new) flags stretched words (>0.7 s) and repeated 4-grams within 25 s.
On this cut it flags, besides the 32 s `and`: `visualizing` 1.36–2.16 (the slow first word — verified
clean), `specifically` 108.17–108.87, `personalized` 129.29–130.21, `free` 180.84–181.60, and the
4-gram "I want you to" at 10.03/13.53 (scripted parallelism — clean). **Re-transcribe each of the three
unverified spans in isolation** (`ffmpeg -ss <t−2> -t 4 … pv/_span.wav` → whisper medium.en,
`condition_on_previous_text=False`, word timestamps) and confirm no hidden restart before cutting.

## 3 — Captions vs lower thirds (every lower third)

**Measured on the delivered master.** All six lower thirds occupy **y 757–905** (alpha bbox, x 90–~945).
The captions lifted over them (`MarginV 300`, 35 cues) put their ink at **y 727–806** — a 49 px overlap
with the lower third's top, on every lower-third beat. Rev 2's QC only asserted captions against
full-screen cards.

**Fix, in Dan's words: move the graphic down, and captions never overlap graphics.**

1. Lower thirds sit at the bottom: in `gfx.py`'s `_lt()` pass `y = 1080 − 80 − ch_h` to
   `lower_third_bar` (box ≈ **852–1000**). Rebuild all six (`FORCE=1 python3 gfx.py name num1 flyblind
   num2 num3 cancel`) and ffprobe each against its beat.
2. Captions during a lower third lift ABOVE it with clearance: measured, `MarginV=300` puts the ink
   bottom at 806, i.e. ink bottom ≈ 1080 − MarginV + 26. For a lower-third top of 852 and ≥30 px of
   clearance the ink bottom must be ≤ 822 → **`MV_LIFT = 290`** (ink bottom ≈ 816). Two-line cues grow
   upward, which is fine.
3. **New QC check 10 (pixel-measured, not geometry-assumed):** for every lifted cue, render `cap.ass`
   over a black frame at the cue's midpoint (`ffmpeg -f lavfi -i color=black:s=1920x1080 -vf
   ass=cap.ass -ss …`), take the ink bbox, take the lower third MOV's alpha bbox at that time, and
   assert a **≥ 20 px vertical gap**. Also assert no lifted or PiP-beat caption ink intersects the
   phone box (x 150–583, y 130–950) and none sits inside a full-screen card window (already checked).
   A FAIL is not deliverable.

## 4 — Delivery checklist (do not skip)

1. `voice_ref_check.py` **PASSED** on the exact delivered file; `AB_his-vs-ours.mp4` rebuilt and sent
   with the review copy (audio unchanged, but the file is new).
2. New headroom QC (§1.4) PASSED: head top within 15–60 px of the top on every sampled frame.
3. New caption-clearance QC (§3.3) PASSED; `repeat_scan.py` clean or every flag verified in isolation.
4. `qc.py` PASSED (update `covered`/`SUP` if any beat changed), `watch.py` run, contact sheet from
   exact `-ss` grabs (`deliver.sh` does this) checked for: no light, no wide shot, no black field, no
   head cut, no caption touching a graphic.
5. Deliver over the same filename; keep rev 2 beside it as `*_REV2_REJECTED.mp4` (rev 1 stays too).
6. Update `notes.md`, check off the Key dashboard task
   `money::Execute handoff: website conversion video REV 3 (head-anchored crops, cut the repeated
   line, captions clear of lower thirds)`, update `AI_COORDINATION.md`, commit the recipe + skill.

## 5 — Things NOT to do going forward (Dan's three reviews, distilled — now in `/ad-edit`)

- **Never anchor a crop to the frame.** Anchor it to the measured head top, per segment, with ~3 % of the
  crop height above the head; assert the headroom on the delivered frames. One reference frame is not
  the video (rev 2 lost a day to a grid frame where he stood 200 px taller).
- **Never show the full wide kitchen frame, never the light** (rev 1). The levels and the light guard
  are asserted in `layout.py` and `qc.py`.
- **Never trust the orphan scan alone.** A word interval longer than ~0.7 s is a hidden restart until an
  isolated re-transcription proves otherwise; run `repeat_scan.py` after every transcription and before
  the EDL.
- **Captions never overlap a graphic** — lower thirds, phone insets, cards. Lower thirds sit at the
  bottom, captions lift above them, and QC measures the clearance in pixels.
- **Graphics sparingly, never on a black field with one small element; app screens next to Dan in the
  footage; if a feature looks lame on screen, don't show it** (rev 1).
- **Audio: the gate decides.** The rev-2 chain (`audio3.py`, bed −44 dB, no compressor, EQ fitted to
  Muhammad's ad) is approved for this shoot — reuse it, re-gate every delivered file.

## Starter prompt (paste into a fresh session)

> Execute `Handoffs/handoff-20260902-website-video-rev3.md` with `/ad-edit`. It is revision 3 of the
> website conversion video from the 8/28 shoot. Rev 2's audio is approved and must not change; the
> handoff has the measured fixes for the three rejected items: head-anchored crops from
> `headtrack.py` (his head is at y≈300–340 in the 4K frame, the crops assumed 100), cutting the
> repeated "I've been out of shape" at tight 31.3–32.8 s, and moving the lower thirds down with captions
> lifted clear of them. Build the two new QC checks (headroom on the delivered frames, caption clearance
> in pixels) before rendering, run `repeat_scan.py` and verify its three flagged spans, and send the
> 540p review copy plus the audio A/B when every gate is green.

Recommended: **Fable 5.1, extra-high effort** (Dan's choice). Budget: $0.00 AI generation spend —
every asset exists; the 4K base and all cards are already rendered.
