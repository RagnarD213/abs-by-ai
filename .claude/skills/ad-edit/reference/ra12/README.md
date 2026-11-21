# RA-12 "The First Step To Getting Abs Isn't A Workout": round 1 (2026-10-15)

A 9:16 ad from the C1667 pool roll (178-245 s), the same roll as RA-13 and RA-14. Built on RA-14's round 3/4 scripts
(phone cards, HyperFrames graphics, holds, compositor) with RA-15's newer pieces (EDL edges, hold-start sampler, caption
writer). Work dir: `/Volumes/Expansion/_edit_work/ra12/` (the Extreme drive was full). Review page `http://127.0.0.1:8842/`.
Round 1 is the WHOLE 46 s ad (every item reused or from the clip library, VIDEO-RULES 2026-10-14), not a first 30 s.

## Order

| # | command | makes |
|---|---|---|
| 1 | lav/env copied from `ra14/` (same roll, same pick); `replicate_words.js` on 170-217 + 205-250 s, then 8 s windows | word list, restart check |
| 2 | `HEAD_SRC=178.26 EDGE_OVERRIDE="R1.end=194.86,R2.start=211.98" TAIL_EXTRA="abs:0.06,generate:0.10" python3 s03_edl.py` | `cut.json` (45.6 s talk) |
| 3 | `chain_a.sh` (s08 audio, s09 CTC, s04 track) | `cut_audio.wav`, `mix.wav` (fitted EQ), words, `framing.json` |
| 4 | `chain_c.sh` (the post-review chain; `chain_b.sh` was the first pass) | voice (fitted EQ + 1.5 dB at 120 Hz), plan, gfx, cards, captions, holds, composite, review cuts |
| 5 | `s88_checks.py`, `s87_page.py`, `review_server.py 8842 round1` | checks, page |
| 6 | master mux, `audio_gate.py`, `s09_align.py <master>`, Replicate transcript, `junk.py`, `s20_neg.py`, `s92_chips.py`, `s94_phonebox.py`, `s93_gateplan.py`, `watch.py` + judge, `gate.py --format ad9x16` | stamps |

## What this ad taught

1. **A roll's approved LOOK carries to another part of the same roll; its EQ curve does not.** RA-14's fitted EQ (its 340-414 s)
   read 6 dB too bright at 5.5 kHz on 178-245 s and failed the tone row by 4-6 dB. Use the chain's fit on THIS cut plus the bass lift;
   the lowest band already read +0.6 dB over the reference, so the lift is +1.5 dB (rule: a mic that already reads full gets less).
2. **`voice_chain.py --frame-lock` hung twice** (its ffmpeg loudness pass idle at 0 % CPU for 17 min, buildcap counted it as a build).
   Make the mix without it and trim with `apad,atrim=0:<frames*1001/30000>`; the audio gate's length row then passes to the sample.
3. **KEEP_TAIL clips a final fricative.** The -40 dB silence starts inside the /s/ of "abs" and the /z/ of "yours", so the pause cut
   kept 19-30 ms of a 55-100 ms sound (independent review, measured >4 kHz share). `TAIL_EXTRA` keeps it; key it on the word Whisper
   puts BEFORE the pause (its contiguous times hand "yours." the pause, so the key is "generate"). A pause that drops under
   MIN_REMOVE after the extension is simply kept.
4. **Library traps.** A0138 (man slumped on a gym bench) has another video's KEY POINT banner burned across it: unusable in 9:16.
   A0069 is PIZZA, not pasta, and the file cuts to a push-up shot at 1.9 s: use 0.55-1.47 s. A0172 (worn out on a gym floor,
   0.40-1.87 s) reads as "everyone else quits".
5. **The P1 self-generation demo from frame 60 opens on another scroll state and clicks Subtle then Ripped (frames 67-71).** Start at
   72; the phone part is then 33 frames (72-104; 105 is the blank hand-over frame), so the card starts 0.37 s after its splice.
6. **`softblue.scene_photo` from t=1.0 pushes 1.4 %/s: a 1.1 s card reads as a freeze** (review D4). Advance t 4x per frame.
7. **RA-14's caption builder still wrote a concat list at 0.033367 s per frame** (RA-15 lesson 23 drift). Ported RA-15's per-frame pipe.
8. **The gate's compliance:labels samples a card at a+0.9 s**, which on a 0.9 s card is its last instant and ffmpeg resolves to the
   NEXT card's first frame (D1 read -0.05 while its chip is on every frame). Gate fix flagged as its own task; not changed here.
9. **RA-14's `s08_audio.py` still shortens the talk 6 ms per splice** (the bug RA-05 round 2 fixed): 15 splices put the voice up to
   90 ms ahead of his lips by the end, and two reviews of the earlier renders only caught it on the second pass (cross-correlation of
   each delivered piece against `lav16.wav`). Ported RA-05's length-preserving crossfade; every piece now within 0.5 ms. Any recipe
   copied from `ra14/` carries the old one: check `seg = seg[XF:]` is gone.
10. **Library clip A0074 animates the photo on its phone** (he tilts his head and squints). K1 is built in code instead: the goal
    picture filling the approved iPhone shell's whole screen (the shell draws a white screen larger than `phone_card`'s content box;
    find it with a pure-red content pass), a 4 % push, the chip drawn after the push so the gate's chip reference still matches.
11. **Graphics over his midsection.** The Soft Blue lower third and CTA sit at 57-68 % of the height, across his lower chest and abs
   in a full-frame 9:16 hold. RA-14 shipped it; the watch judge calls it a defect each time. It is Dan's decision 3 on the round 1 page.

## Round 2 (2026-10-20): prospect everywhere, graphics under the captions, Dan's own opening clips

Scripts: `round2/` (copies of the work-dir `r2_*.py`; the work dir is `/Volumes/Expansion/_edit_work/ra12/`, outputs in `round2/`,
master in `deliver_r2/`). Chain: `r2_chain.sh`, then `r2_gate_seq.sh`, `s20_neg.py`, `r2_s93_gateplan.py`, `watch.py` + a fresh judge, `gate.py`.

12. **Graphics "immediately below the subtitles" need the WIDE level under them.** Shorts start at y 1400-1470 on FAR holds and
    about y 1720 on NEAR holds (green-shorts row scan, `round2/measure/shorts_top.py`), so a graphic at y 1530 sits on his abs on a
    NEAR hold. Swap levels so every hold carrying a graphic is FAR, keep levels alternating at uncovered splices, and end a lower
    third where a NEAR hold starts. `vertical.py` now takes `top_y` for the lower third and the CTA.
13. **24 px under the caption INK is not enough for the gate**: `captions:graphic_clearance` counts the shadow and measured 14-15 px
    at y 1520 (min 20). y 1530 passes.
14. **B0550 (the prospect's live generation) at 60 fps**: his before photo appears at frame 41; the chip must be on from there
    (a fresh judge caught one unlabelled frame). The real scan takes 35 s, so the phone shows the tap and the first second of it,
    then hard-cuts to the result.
15. **B0427 (golden-hour ab wheel) reads orange** beside the overcast presenter at saturation 1.05; 0.78 matches skin saturation.
16. **No library or AI clip of Dan eating salad exists.** Real holds of the bowl are on the 8/3 salad shoot roll C1546 (24, 46, 57,
    74 s). 24 s and 46 s clip his hair at the frame top; 74 s has 54-66 px of headroom (used, window x 560).
17. **Captions over the full photo cards (G1, P1 result) fail `watch:pass` as label_over_face** until Dan accepts them; R2 puts it
    to him as a decision rather than shrinking the pictures.
