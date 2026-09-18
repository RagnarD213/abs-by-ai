# RA-01 — "The AI Trick That Got Me Abs" — ROUND 3

> ## ⚠ THE TWO MASTERS ARE HELD. THEY ARE NOT IN THIS FOLDER.
>
> One gate row still fails on both finished files, so neither was put through the delivery script.
> They sit in the work dir at `/Volumes/Extreme/_edit_work/ra01/master_9x16.mp4` and
> `master_16x9.mp4`, with their stamps. What **is** in this folder is everything you need to judge
> the cut: the two **REVIEW 540p** copies, the audio **A/B** clip, these notes, `recipe-RA-01/`,
> `measurements-RA-01.json` and both gates' stamps.
>
> **What fails, on both masters — the same one row as rounds 1 and 2, and it is your call:**
>
> | gate | row | number | why |
> |---|---|---|---|
> | audio | `artifacts` | flux **0.090** against the bound **0.079** (Muhammad's 0.072 × 1.1) | the lav on this roll reads **0.0962 before anything touches it** — 1.22× the bound. The bound is beaten by the source, not by the mix; the voice chain takes it DOWN by 6 %. |
> | delivery | `audio:stamp` | — | one cause, two rows: the delivery gate refuses any file whose audio stamp is not a PASS. |
>
> **Everything else passes.** The delivery gate reads **35 passed, 1 failed, 0 NOT MEASURED, 0 pending**
> on each master at `GATE_VERSION 2.1.0`, and the audio gate passes **12 of its 13 rows**. Nothing was
> skipped and nothing is unmeasured.
>
> **I did not process harder to pass it and I did not touch the bound.** The round-2 planner ruled
> this one an exception only you can grant (DS-17 precedent). **Your call is item 8.**
>
> Round 1's and round 2's masters and stamps are preserved at `/Volumes/Extreme/_edit_work/ra01/round1/`
> and `/Volumes/Extreme/_edit_work/ra01/round2/`.

Built to `Handoffs/video-editing/RA-01-plan.md`, **§13 "Round 3 rulings"**, by the EDITOR session
(Claude Opus 5, high), 2026-09-18. Work dir `/Volumes/Extreme/_edit_work/ra01/`.
Recipe: `recipe-RA-01/` (`REBUILD.md` lists every stage in order).
**$0.00 of AI generation. Nothing uploaded. No dashboard row. Nothing committed. Raw footage untouched.**

---

## What changed since round 2, in plain language

Round 2 was reviewed by a fresh pair of eyes. It fixed eight of the nine things round 1 got wrong.
Round 3 is a small, targeted fix of the **four** the reviewer still flagged — nothing else in the film
was touched.

1. **The music no longer drops out near the end.** Just after your last word there was a tenth of a
   second where the music fell away to almost nothing and then jumped back in. It was not a bad join —
   it is a **rest in the music track itself**, about one a second, and after you stop talking there is
   nothing left to cover it. The music file we feed the mix now holds a steady level through that last
   couple of seconds and then fades out smoothly to the last frame. **Nothing about your voice, the
   loudness or the stereo was touched.**
2. **The moment you lean right at 0:22 no longer pushes your face to the edge of the vertical frame.**
   That shot's framing is nudged so your face stays inside the safe band on every single frame, while
   still keeping you within six per cent of the centre line. (The trade: the zoom cut into that shot at
   0:20 now moves you slightly more sideways than before. It still reads as a zoom, not a jump.)
3. **In the wide 16:9 version you no longer step sideways at every zoom cut.** The wide shot uses
   nearly the whole width of the camera file and cannot be moved, so the tighter shot now sits on
   exactly the same centre line. Across the eight visible zoom cuts your head used to shift 4–9 % of
   the screen width; it now shifts **0.1–2.9 %**, and most of that is you actually moving.
4. **The second call-to-action button in the wide version is now low in the frame**, bottom-left, like
   the first one — instead of floating at shoulder height. Over that whole line you are gesturing with
   both arms, and the only part of the frame you never occupy is the bottom-left corner, so the button
   is set in three short lines to fit there. **Both** buttons in the wide version now look identical.

**Deliberately unchanged:** the caption still says "200 pounds" (the planner ruled that burned captions
are a transcript of what you say), and the cut, the beat order, the photographs, the colour, the
vertical button and everything else are exactly as you saw them in round 2.

## What this is

A 9:16 ad master under the 0:59 Shorts ceiling, and a 16:9 built from the same edit, the same
audio and the same beats, with the graphics re-laid for the wide frame. One roll, one pass of the
script, cut airtight.

| | |
|---|---|
| source | `C1663.MP4` (8/28 pool shoot) — **native portrait**: stored 3840×2160 with a −90 rotation, ffmpeg autorotates to **2160×3840**. Read-only; nothing was written into the shoot folder. |
| audio | ONE stereo stream, **dual-mono**. `pick_lav.py`'s own JSON beside the roll chose `-map 0:a:0 -af "pan=mono\|c0=0.5*c0+0.5*c1"`. SNR 47.5 dB, −25.2 dBFS, 0 clipped samples. |
| length | **57.190 s**, both aspects — **1.81 s under** the 59.00 s ceiling |
| words | 193, captioned from **0.140 s** to 55.22 s — every one of them |
| takes | one full pass of the script; line L5 was read twice; one false start |
| the two files | same EDL, same beats, bit-identical audio |
| AI spend | **$0.00** |
| round 3 changed | the music bed's tail, one vertical shot's centre (0:20–0:23), every 16:9 tight-shot centre, and the 16:9 CTA buttons — nothing else |

## Your calls (nothing here was waited on)

1. **The BEFORE picture carries no label.** It is `01_LIGHT_plus8lb_PRIMARY.jpg` — a real 2022
   photograph of you, AI-adjusted +8 lb, shown with no chip, following the Ad 1 rev-5 precedent.
   Confirm, or label it, or swap it for the untouched `00_ORIGINAL_deckchair_upscaled3x.jpg` with
   the "Real picture of me" chip.
2. **No line was cut.** L11 stayed in; the airtight cut finished under the ceiling with room.
3. **Spoken claims kept exactly as filmed**, flagged not changed: *"This picture got me abs"* and
   *"AI analyzed it and figured out exactly how much fat I had to lose"*.
4. **The three after pictures are the studio set** (`studio-blue-10`, `studio-gray-41`,
   `studio-white-90`) — three backgrounds, three outfits, all smiling, none from `Frowning Photos/`.
   Say if you would rather they came from the pool shoot.
5. **⚠ NEW — the skin-colour look.** The 8/28 LUT was fitted indoors; this roll is outdoors and
   overcast. Round 2 re-chose both the exposure and the saturation by measuring your face against
   two approved files. The result is warmer and more saturated than round 1 — but it still reads
   cooler than the approved Ad 1 vertical: on the delivered frames your face carries **81 % of the
   colour** the Ad 1 vertical has, against a target of 85 %. The daylight on this roll is genuinely
   bluer than the tungsten indoors and the ruling forbids a white-balance change, so 81 % is as close
   as this round is allowed to get. **Watch the two side by side and say whether this is the look you
   want, or whether you want the white balance moved.**
   The proof sheet is `recipe-RA-01/grade_proof.jpg` and the numbers are in
   `measurements-RA-01.json → grade`.
6. **The 16:9 photo cards are a portrait picture on a wide dark field.** That is the round-2 ruling
   (no blurred-photo backing). It leaves a lot of empty field either side. Say if you want something
   else there.
7. **The macro-tracker screen shows its own calorie figures** and its "Powered by Claude + Gemini"
   footer — the app's real output, legible for about three seconds. Yours to keep or blur.
8. **⚠ THE BIG ONE — the audio row, unchanged from round 1.** Both masters carry a FAIL on the
   audio gate's `artifacts` row. The number comes from the roll, not from the mix: the untreated lav
   is already over the bound, and the voice chain *improves* it. The round-2 planner ruled this an
   exception only you can grant. Your options: (a) grant the exception for this outdoor roll and let
   the masters ship; (b) leave it failing and re-shoot the audio; (c) have someone look at the mic
   setup for the next outdoor shoot. **I did not process harder and I did not touch the bound.**
   Listen to `the ai trick that got me abs | AB audio ref-vs-ours | RA-01.mp4` before deciding.
9. **⚠ NEW — the outdoor-audio exception is a second, separate decision from the row itself.**
   Even if you grant it for RA-01, every other 8/28 outdoor roll will fail the same way. Say whether
   you want a standing exception for outdoor rolls recorded on this lav, or a per-video call each
   time.
10. **No transition SFX.** The plan asks for a whoosh/pop on each card in; measured in round 1, they
    break the audio gate's `tone` row, and the round-2 ruling accepts leaving them out.
11. **"Results are not guaranteed."** Still not on screen. Yours to call.
12. **⚠ NEW — the wide version's button is now three lines** ("Tap the button / below / AbsByAI.com"),
    bottom-left, because that is the only place in the frame you are never standing over during that
    line. Say if you would rather have one wide line and accept it sitting higher, or the button on the
    right instead.
13. **⚠ NEW — the music now holds its level under the end card** instead of following the track's own
    rhythm there. It is a level correction on the music only, in the last three seconds; your voice is
    untouched. Listen to the last five seconds and say if you would rather the music simply faded out
    earlier.

---

*The gate tables, the framing numbers and the full defect-by-defect account are in
`ROUND-3-EDITOR.md` (this round) and `ROUND-2-EDITOR.md` (everything round 2 changed), both in this
folder and in `/Volumes/Extreme/_edit_work/ra01/`.*
