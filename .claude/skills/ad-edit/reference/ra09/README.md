# RA-09 "Do You Think AI Is Changing The World?": round 1 (2026-10-21)

AD, 9:16 first (16:9 after Dan approves). Roll C1666 (8/28 pool set, one read of the script). Built on RA-12 R2's scripts (prospect
everywhere, graphics under the captions) with RA-05 R2's speed-up and RA-07 R6's approved clip cards reused pixel for pixel.
Work dir `/Volumes/Expansion/_edit_work/RA-09/`; page `:9109`; delivery `Claude Ad Videos/do you think ai is changing the world - RA-09/round 1 review/`.

## Order
`s01_env.py` (lav) -> Replicate words in two overlapping pieces -> `s02b_patch09.py` -> `HEAD_SRC=10.28 EDGE_OVERRIDE="R2.start=23.50,R3.start=64.35" s03_edl.py`
-> `s03s_speed.py` (1.06x) -> `chain_a09.sh` (Rubber Band audio, voice options, CTC, head track) -> `r1_plan.py`, `s04b_holdstart.py`, `r1_plan.py`,
`r1_s84b_sheet.py` -> `chain_c09.sh` in `renderq.py run` (HyperFrames, cards, captions, holds, assemble, cuts) -> `gate_seq09.sh` -> `s20_neg.py`
(cwd r1/gate), `haircheck916.py`, `r1_gateplan.py`, `watch.py` + fresh judge, `gate.py --format ad9x16`.

## What this ad taught
1. **Replicate large-v3 merges a stopped-and-restarted sentence into one with a 2.5 s word.** An isolated medium.en pass (disfluency prompt) heard
   the restart at 23.24 s. Every word over ~1 s in a merged transcript gets an isolated window before the EDL. A disfluency `initial_prompt` made
   local medium.en return EMPTY on several clean 8 s windows; re-check empty windows on Replicate instead.
2. **When a range edge moves inside a word's Whisper span, the 60 % overlap test drops the word from the caption list** while the audio still has
   it ("I'm", "Got"). Re-time those words in the patch whenever an EDGE_OVERRIDE moves an edge; print the cut's word list against the script.
3. **The 1.06x retime of a hold can come out a frame short** (span rounding): read 2 spare source frames after the last talk span and trim to n.
4. **A card that starts less than a frame after an audio join shows one frame of the next piece in the previous hold's crop** (a one-frame jump the
   reviewer caught at 16.78 and 44.18 s). Start such a card on the frame that contains the join (`r1_plan.py`), unless a card ends there.
5. **Fixed-length approved clip cards (RA-07's 62/14/60 frames) can leave 0.2-0.5 s Dan holds between them.** Keep the pause (PROTECT) rather
   than stretch or trim an approved clip, and anchor a short clip to the words it shows (G2 ends 2 frames after "day?", not under the next line).
6. **A mouth click or lip noise 50-80 ms after a pause cut reads as a +10-15 dB low-band thump** (reviewer measured). Move the range edge past it
   to just before the word onset (`EDGE_OVERRIDE`).
7. **Wrapping a short audio/analysis chain in `renderq.py run` made it wait behind hours of heavy renders on the same drive.** Audio-only work,
   frame grabs and cloud transcripts never need the queue: run them directly and let the ffmpeg wrapper queue only what is heavy.
