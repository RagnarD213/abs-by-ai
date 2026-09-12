# `a11_sq_ad1/` — the SECOND square (Ad 1, 2026-09-11/12), and the four defects its CUTDOWN had

The Ad 2 square is `a10_sq/` and its geometry lessons stand. This directory is the **attempt-3
pipeline** re-laid-out for 1:1 (Ad 1 predates a4/a5), and it exists mostly for one reason: the
independent audit returned **DOES NOT SHIP on the cutdown** after `qc.py`, the watch pass, the hair
gate, the caption gate, the landing check and `_shared/deliver/gate.py` had all passed it. Every
defect was in how a SELECTION cutdown is built, so every one of them is waiting for the next square.

| file | what it is | reuse it? |
|---|---|---|
| `sqcutdown.py` | the ≤0:59 selection: CTC-anchored ranges, frame-exact picture cut, `assert_range_lands()`, the editor's mix cut at the seams, the one mute/word list | **yes** — this is the corrected one |
| `sqcut_build.py` | writes `cut/beats.py`, copies the gates into `cut/`; it no longer re-derives the word list | **yes** |
| `cut_edl.py` | a picture EDL for the CUTDOWN, so `sqlanding.py` can run there at all (master cuts mapped through `cut_plan.json` + the seams) | **yes** |
| `plan_sq.py` | `plan.json` for `_shared/deliver/gate.py` from an attempt-3 build (framing segments from `beats.PUSHES`, per-insert label chips) | **yes**, adapt the media keys |
| `sqlib.py` `sqassets.py` `render.py` | the 1:1 layout library, the per-media square treatment + label, the compositor | Ad 1 specific; read the diffs |
| `sqmux.py` | copies the APPROVED VERTICAL's AAC stream and asserts its md5; asserts the editor's frame count | **yes**, change `VERT` |
| `sqhairgate.py` `sqlanding.py` `deliver_sq.py` | the square hair gate, the landing check, delivery | **yes** |

## The four cutdown defects, in the order they cost time

1. ⚠⚠ **`-ss f"{t:.4f}"` DROPS A FRAME whenever the rounding lands above that frame's own pts.**
   4 of 9 ranges started one frame late. It flashed one frame of a third photo at a seam, dropped
   the peak frame of one of Muhammad's light leaks, and ran the picture **33 ms ahead of the audio
   over 23.6 s of a 49 s cut** — with every duration and frame-count check green, because the counts
   were right; it was the CONTENT that was shifted. Seek `(n0 − 0.5)/FPS`, and **assert each range's
   first and last frame against the master on the pixels** (270² gray, mean |diff| < 1.0; a slip
   reads 1.4–122). The assert is the part that matters.
2. **Range edges come from the CTC alignment, never from Whisper.** Whisper's starts run ~130 ms
   early and its ends truncate. On a beat edge that is harmless; on a SEAM it clipped the onset of
   "You're" and cut "changes." 118 ms early with the sibilant still at −25 dBFS. **Floor a start,
   ceil an end** so a range contains every word it carries — **except an edge that snapped onto a
   beat boundary, which is ROUNDED**, because a boundary is one frame index and the previous range's
   exclusive end has to be the same number as the next range's start. Flooring a snapped start
   re-opens the range inside the graphic the snap existed to clear (it fires the A6.15 assert);
   ceiling a snapped end leaks the first frame of the next beat.
3. **Three separate things conspire to delete the first word after a seam.** The range map has to
   **clamp** a straddling word rather than drop it ([S1].16 one level down); `captions.groups()`
   treats a word within 0.15 s of a muted span as muted, and that slack **must be clipped at
   `beats.SEAMS`** — the CTA pill that ends on the seam was muting the next range's first word;
   and that clip needs **a 1 ms tolerance**, because a span clamped to a range edge and the seam
   itself are two different float sums and came out 1e-5 apart, which silently undid the fix once.
   The clip lives in `groups()`, not in the cutdown builder, because `caption_sync_check.py`
   re-derives its grouping from that same function.
4. ⚠⚠ **THE CUTDOWN'S MUTE LIST AND WORD LIST WERE EACH DERIVED TWICE.** Once by the builder from
   the master's spans through the in-memory plan, once by `sqcut_build.py` from `cut_plan.json`,
   whose numbers are rounded to 5 decimals. The two agreed to a few milliseconds — and a few
   milliseconds is enough: one word fell on opposite sides of that 0.15 s mute line, so the render
   burned 103 caption states while the gate re-derived 104 and reported three misses on captions
   that are **correct on the frame**. `cut/mute.json` and `cut/words_ctc.json` are written once now,
   by the builder, from the lists it hands to `captions.render()`. **Any number a gate re-derives
   instead of reading is a number that can disagree with the render.**

## Two more that are not the cutdown's

* **The concat demuxer's trailing `file` line is RENDERED, and it must be the blank** ([S1].6, which
  was written up on Ad 2 and never applied in code). The last caption state re-showed its lit word
  past its own end: "six pack abs," printed across the closing CTA pill's "With Abs" for 7 frames,
  in the master AND the cutdown, with `cap/list.txt` ending correctly at the pill's own mute start.
  **The approved 9:16 verticals of Ad 1 and Ad 2 carry the same overprint.**
* **`_shared/deliver`'s `compliance:labels` needed a per-insert chip and position** (GATE_VERSION
  1.1.0). One chip per KIND cannot see a label drawn in the editor's card language, where the chip
  hangs off the card's own media hole in a smaller face: the card read **−0.031** against a
  full-bleed reference while its label was present and correct on every frame. `plan_sq.py` renders
  each insert's chip with the same `sqlib` calls the compositor makes. With that, both Ad 1 square
  files pass `compliance:labels` at min correlation **0.986**.

## Two copies of the delivered file, one name

`sqcutdown.py` writes `ad1_square_59s.mp4` into the BUILD ROOT; the gate chain copies it into
`cut/` so the cut-side gates can run beside `cut/beats.py`. **Check the mtimes and the md5 before
you believe a frame you pulled out of `cut/`** — three extractions in this build were of a stale
copy, and one of them looked like a defect that had already been fixed.
