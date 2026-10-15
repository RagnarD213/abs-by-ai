# RA-04 "Top 3 Tips For Getting Abs": the first 8/28 raw ad in Soft Blue Light (round 1, 2026-10-13)

A 9:16 ad cut from portrait roll C1664 with the approved RA-01 recipe (cut, grade, voice chain, hair-anchored
FAR/NEAR crops, captions) and Soft Blue Light graphics through the shared HyperFrames templates. Work dir:
`/Volumes/Extreme/_edit_work/ra04/`. Start the next 8/28 raw ad (RA-02, RA-05 ... RA-16) from this folder, not from RA-01.

## Order

| # | command | makes |
|---|---|---|
| 1 | `python3 s01_env.py` | `lav.wav`, `env.json` (after `pick_lav.py` wrote the roll's `audio_source.json`) |
| 2 | `bash s02_tx.sh` | `tx/<roll>.whisper.json` (chunked medium.en), orphan and repeat scans. Set `-ss`/`-t`/`OFF` to the ad's span |
| 3 | `python3 s03_edl.py` | `cut.json` from `edl_spec.json` (take spans by phrase), airtight pauses |
| 4 | `BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py`, `python3 s09_align.py` | `mix.wav`, `words_aligned.json` |
| 5 | `python3 s04_track.py` | `framing.json` (slow: one 4K seek per sample) |
| 6 | `python3 s05_plan04.py` | `beats.json`: cards, Dan holds and levels, lower thirds, CTA |
| 7 | `python3 gfx04.py` | `hf9/`: lower thirds + CTA (`manifest.json`) and media-card plates (`plates.json`) via `hyperframes/vertical.py` |
| 8 | `python3 s06_inserts04.py` | `cards_9x16/<name>.mp4`, each exactly its frame count |
| 9 | `python3 s07_captions.py 9x16` | `cap_9x16/captions.mov` |
| 10 | `python3 s10_render04.py 9x16` | Dan segments, concat, shared Compositor (glass over footage), captions on top |
| 11 | `LOCK=picture_9x16.mp4 ... python3 s08_audio.py`, mux | the mix locked to the picture length, `draft_9x16.mp4` |
| 12 | `python3 page04.py --media` | `round1/index.html` + stills + context clips (`page_notes.json` holds the copy) |

`r1_chain_a.sh` (4-5) and `r1_chain_c.sh` (3-12) are the chains as run, each behind `capwait4.sh` (two-build cap).

## What this ad taught (keep for the other fifteen)

1. **A pause splice inside a same-size shot is a jump cut.** `s05_plan04.py` puts a level change ON every splice that
   no card covers and asserts none is left bare. "Number one / two / three," became 0.6 s punch-ins, the same on all three tips.
2. **Card and graphic edges snap to the nearest splice** (`snap_to(t, SPL)`), so a cut and a card never land a few frames apart.
3. **Phone cards end above the caption line.** A phone that ran down behind the captions put white words on white app
   screens and a caption across the result picture's abs. `gfx04.py` passes `max_w` so every hole (and its chip) ends by y 1376.
4. **Whisper can give a word zero length** ("Whatever", 172.40-172.40) and the 60 % overlap rule then drops it from the
   captions while the audio still says it. `s03_edl.py` keeps a zero-length word that sits inside the range.
5. **RA-01's caption fix map is per ad.** It rewrote "app" to "abs" ("the Abs by AI abs"). `s09_align.py` now carries no map,
   joins "absbyai" + ".com" into `AbsByAI.com` and cases the brand `Abs By AI`.
6. **The tail guard tests where the silence ENDS.** The silence after the last word starts inside Whisper's last word, so
   "s0 >= last word end" let a pause cut through and made a splice in the end hold.
7. **Length is tight on these scripts** (215 words at 222 wpm): 58.06 s of talk leaves 0.85 s of end hold under 0:59.
8. **The RA-01 grade (1.15x LUT, saturation 1.25) transfers to C1664** (checked side by side with C1663: same set and light).
9. **The fitted voice EQ already lifts the lows to the reference** (+3.8 dB at 110 Hz on this lav), so the 2026-10-12 bass
   standard is offered as an A/B (`mixB.wav`, `--eq "<fitted>,equalizer=f=120:t=q:w=0.8:g=+3.0"`), not stacked blind.
10. **`capwait` can wait 30 to 40 minutes** when three sessions are rendering. Launch chains in the background and let the
    task notification bring the session back; do not poll.
11. **The analysis card takes Soft Blue colours by patching module globals** (`AC.LIME`, `AC.OLIVE`, `AC.PLAN_GREEN`,
    `cardlib.field`) in `s06_inserts04.py`; `ANALYSIS=olive` renders the RA-01 colours. If Dan picks blue, move the
    palette switch into `adkit/analysis_card.py` as an argument.

12. **The app recording B0049 shows the banned before/after screen ("Meet the new you") until about 27.6 s.** Round 1 started
    the result card at 27.3 s, so the banned screen was on screen for the card's first 0.3 s (0:15.3 in the round 1 draft).
    Start the result at 28.0 s (fixed in `s06_inserts04.py`) and look at the first five frames of every app card.

## Round 2 (2026-10-14)

`r2_chain_a.sh` rebuilds the picture with the fixed `flow_b` and mixes voice B locked to it (`s08_audio.py` now takes `EQ=`
and `OUT=`). `r2_context.py` builds a context preview with AI frames as labelled stills on the real words; `page_r2.py`
writes the round 2 page. Frame prompts and hashes: `round2/`.

13. **Make an AI clip's END frame by editing its START frame** (pass the start frame as `--image` with "keep the camera
    position, framing and background exactly; change only ..."). Frames generated separately from one reference come back
    from different camera angles (side-on start, front-on end), and a start/end pair from two cameras makes the video model
    warp the room. Generate the shot's anchor frame first, then derive its partner from it.
14. **Check where the subject is walking, not only who he is.** The first walk-in frame was clean on every checklist item
    and still wrong: he walked toward the camera with the rack behind him, so it could not read as "walks up to the rack".

15. **Dan rejected round 2b's leg press: the man sat upright and pushed 26 to 43 degrees off the rails** ("No human body works
    like that"). Round 2c measured every frame (`_shared/framecheck/posecheck.py`), and seven fresh independent reviews caught, in
    turn: a stretching machine frame, a sled sliding off its rails, an upright platform, legs 24 % longer in the END, a floating
    leftover phone, a phantom toe, a pillar patch, feet sliding down the platform, a smeared platform corner and a vanished shoe.
    The pair that passed (F4h / F5p) builds the END machine in code from the START (`r2c_sled.py`); only the man is generated.
16. **With the start knee at 127 degrees, the honest push is short** (about 42 px, ~10 cm). A deeper rep needs a start frame with
    the knees bent further; the image model shrinks bent legs, so check bone lengths again if that is tried.

## Round 3 (2026-10-14): the broken-arm clip in motion

Scripts in `round3/`: `gen_motion04.py` (Veo 3.1 Fast, asserts every frame's sha256 against `decisions.json`, ledger, budget stop),
`check_take04.py` (sheets, first/last second, cut scan, self-change, pose and rigid per take), `strip04.py`, `platform04.py` (masked
platform-rim tracker), `selfchange04.py`, `assemble04.py` (raw-YUV frame picking into the card's exact frame count), `r3_lt3.py` (one
lower third re-rendered), `r3_context.py` (context preview over the round 2 base without a full render), `page_r3.py`. Prompts in
`round3/prompts/`, gate spec `round3/AI1-3_b.spec.json`. Spend $5.80 of $20 (12 takes).

17. **Veo lands NEAR its last_frame, not on it.** Two takes that share an approved middle frame (A ends on F2, B starts on F2) do not
    join: take A's last frame was 20.6 levels off F2 on the man, so at the join he jumped 21-37 px in one frame, the floor grain
    switched and an earring vanished. The first independent review caught it; my own check had measured the 12.8-level jump and
    waved it through because the pose matched. Continuous action is ONE take from the first approved frame to the last (6 s held
    walk, stop, reaction, phone out, reading). Never cut inside a continuous action between two takes.
18. **Pick whole source frames.** 24 fps played at 1.12x on 29.97 repeats every tenth frame, and the sled visibly paused three times.
    At 1.249x every output frame is a distinct source frame (`assemble04.py`); a slight speed-up, no repeats.
19. **Veo fills the duration.** A 4 s take of "take out the phone" spent 2 s fumbling in the pocket; "in one quick smooth movement...
    within the first second" fixed the pacing. A 4 s leg press take did two full reps; use one push, bottom to top.
20. **A gate box on a moving edge measures the background.** The footplate corner boxes failed (0.50, 0.63) because the corner passes
    from a dark rack to the grey pillar. A box on the footplate FACE (its two slots) and a mask on the platform rim both track within
    3-7 px of the plates. The rail strip the plates uncover is a `may_change` region, not a static fault.
21. **Shot choice by the prop, not only the physics.** Both leg press takes passed the sled checks; take A's phone smeared as he turned
    it to his chest, take B holds it flat and sharp the whole push.

## Round 4 (2026-10-14): the full 9:16 and 16:9

Scripts in `round4/`: `r4_home.py` (home card re-timed), `r4_track.py` (land-then-hold track + per-hold level and track overrides,
writes `beats.json`), `s10_render04r4.py` (RA-15's render with the tracked strip and the input seek, RA-04's grade), `gfx16_04.py` +
`hv16.py` + `s06_inserts16_04.py` (the 16:9 graphics and cards), `r4_plate9.py`, `cta16_check.py`, `r4_measure.sh`, `s_chips04.py`,
`s_gateplan04.py`, `s_sheet04.py`, chains `r4_chain*.sh`.

22. **Measure the drift before keeping fixed 9:16 crops.** On C1664 his head drifted 3.5-20.8 % of the crop width off the fixed centre in
    11 of 14 holds. The standard track (20 px band per 608, 170 px/s, Gaussian ease) keeps every hold's median within the gate's 6 %;
    RA-15's slower 70/52 left four holds at 6-12 %. Calming a follow by slowing it only moves him off centre. Two levers that work: a
    hold with a card on BOTH sides can go FAR (no zoom cut to keep), and a long hold under the CTA can take a wider band (dan14: 100 px/s,
    35 px, sigma 12). `r4_track.py` HOLD_LEVEL / HOLD_TRACK. When he walks a third of the frame inside one hold (dan03, 1187 -> 1408 px in
    1.6 s), no follow passes a judge: cut the hold in two at a word boundary with a zoom change (`r4_split.py`, "make a | picture"), so
    each half lands on him and the recentring is a cut, not a pan. Three judge passes failed the pan before the split. **What finally
    passed: hold the crop STILL at his median position wherever that keeps him within 16 % of the width at his furthest** (14 of 16
    holds; his median head centre is then exactly on the centre line, the gate's framing:centering measure). On a roll where he is
    moving at most cuts, a landed crop pans from its first frame and every judge calls it drift; only the two holds where he travels
    over a fifth of the frame keep the follow (`r4_track.py` HOLD_MAX 12). Centre a held crop on the MIDDLE of his range (kept within 5 %
    of his median), not on his median: a median centre opened dan10 with him at 33 % and empty space on the other side.
23. **The caption concat list put every caption change ONE FRAME LATE** (`duration 0.033367` is longer than 1001/30000; 217 of 217
    changes late). Harmless on a word, a defect where a lifted 16:9 line is clipped at a card's first frame (the caption sat on the card
    picture for one frame). `s07_captions.py` now writes one symlink per frame and encodes an image sequence at 30000/1001. The
    `seq/` folder on the Extreme drive collects `._*` AppleDouble files: read only names that do not start with a dot.
24. **Person-mask a library clip over its whole window before using it.** B0464 (lawn squats) cuts his head off at the top of EVERY rep in
    the source (`round4/b0464_mask.json`); the only clean stretch is 7.30-9.45 s, so the card became 64 frames and Dan comes back on
    camera for "to do instead". A tighter crop cannot fix a head the camera did not record.
25. **App recording crops:** B0049's result screen cropped from y 170 sliced the "Your future self" header (y 150-196). y 250-1770 sits
    below it and above the email text (y 1830). Its generate screen cropped to y 2590 sliced the blue "Generate my future self" button
    (y 2488-2680). The generating screen SCROLLS 72 px while it plays (footnote 2462-2492, then 2390-2420), so each screen gets its own
    1320x2300 window: y 170 (options) and y 215 (generating); a segment may carry its own crop in `media()`. Check every frame of an app
    card that scrolls, not one frame. B0544 at 2.1-2.47 s scrolls a half sentence through the top edge: its second shot starts at 2.50. B0544's page slide runs 6.00-6.23 s: start the tour at 6.25.
26. **16:9 from this portrait roll:** one fixed centre (cx16 1088) for every hold, both levels; the 9:16 clips and phone recordings whole in
    a media-card plate (hole y 40-892), chip on the field; the CTA upper left beside his shoulder, cleared by person mask on the CTA hold
    (`cta16_check.py`). The lower thirds keep the locked full-width 16:9 Motivation box (a reviewer called it wide over his abs; that is
    Dan's call, not a defect).

## Open for the final round

Land-then-hold centring is not wired in (crops are fixed per hold, the RA-01 method); measure with `cut/landing.py
motion_stats` and switch if any hold drifts past 3.3 % of the crop width. The 16:9, the edit sheet, the delivery and
audio gates, the watch pass and the independent review all belong to the round that builds the full film.
