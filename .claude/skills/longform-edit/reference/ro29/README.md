# RO-29 "Cortisol Belly Is Real, But TikTok Has It Wrong" (10/15 C1772 + C1773): round 1 recipe (Claude Opus 5.5, 2026-10-29/30)

Same 10/15 studio set as RO-28 (`../ro28/`, read it first); only the files that differ are kept here. Work dir:
`/Volumes/Expansion/_edit_work/RO-29/round1/`. Two rolls on one virtual source timeline: C1772 at frame 0, retake C1773 at frame 11400
(380.38 s). Cut: 15 pieces, 5:28.8, 28 shots. Never commit media.

## Choices this round
- Voice: **untreated** (rumble filter + loudness only, `voice_chain --finish-only`) won 10 blind listens at 7.6, ahead of warm bass + no
  gate (5.4), warm bass + 3 dB (5.3), warm bass (3.6) and the chain default (3.6). On this roll the warm-bass EQ that won RO-28 lost.
  Consequence: the audio gate's **tone row fails by design** (3.8 dB mean gap to the I'm 41 reference); every damage row passes. The page
  says so in plain words (`page_extra.py`, checks list) so Dan does not read a red row as a fault.
- Colour: A = RO-28's pick (Rich Balanced, warmer skin), recommended; B = I'm 41 grade; C = Richer Colour.
- TikTok phone cards (P01, P02): the chip credits the creator (`credit=` on the plan item, `@handle on TikTok`), drawn in the phone's
  empty white band under the video (`gfx.py`, anchor `mt` at 326, 918, size 17). The old top-left chip at (600, 54) touched Dan's hair.
- New lower third G13B "Is It Worth Killing Yourself For This?" (eyebrow ASK YOURSELF) on the cortisol-vs-stressor line.
- No Fahrenheit thermostat clip exists in the library; the Celsius one (22 to 21) stands in, flagged on the page.

## Traps this round paid for
1. **Whisper on the assembled audio needs the bundled ffmpeg on PATH** (`asr_assembled.sh` exports `Media/video_edit/bin`), or it dies
   with "No such file: ffmpeg".
2. **A restart inside a kept piece ("now I know a lot" said twice) must be split in `edl.py`**, not trimmed later: two pieces with the
   second starting on the clean start (level strip to find voice onset).
3. **After any EDL change, remake `assembled16k.wav`** before ASR, or Whisper transcribes the old cut and every timing drifts.
   `rebuild_cut.sh` runs the whole chain (edl, assemble, shots, 16 k mono, ASR, words_out, hair_pre, crop_y) in order.
4. **`words_out.to_src` must clamp to the last piece** (a word ending on the final frame raised StopIteration).
5. **The FINISH (untreated) voice path did not stash the `.audio_untreated.json` baseline**, so the gate's do-no-harm row read NOT
   MEASURED. `build.py` now calls `common.stash_untreated` on that path too.
6. **A clip's `max_len` longer than the source left after its in-point** fails the context render with "short read" (C13, A0174 is 6 s used
   from 0.6: max 5.3).
7. **`review_media.py context_all` reuses any existing block file.** After a graphic changes, use `context_one <IDs>` (fresh small blocks)
   and rerun `stills.py`; re-render the first minute if the item sits inside it.
8. **zsh:** `echo ==` is equals expansion (use `echo "--"`); an escaped `\$PATH` inside a single-quoted `bash -c` stays literal, so write a
   small `.sh` instead.
9. **The render queue was busy: the context step waited 74 min for a heavy slot.** Start the reviewer on finished items while a re-render
   of a few items runs, and tell it which files to check last.
