# Lessons 73–122 — the website conversion video, six revisions (extracted verbatim from /ad-edit on 2026-09-09)

Every rule below was paid for by a rejected revision. Paths `reference/recipe/…` are this skill's. The numbering is
shared with /ad-edit so cross-references from other skills still resolve.

Website conversion video (2026-09-01/02) — the post-generation video on absbyai.com, cut from
the 8/28 shoot (C1650+C1651) to a TRUST brief: no fast cuts, nothing flashy, the last thing a
visitor watches before they buy. Reproducible from `reference/recipe/`. What it added:

73. **A trust cut is the same pipeline with the dials turned down, not a different pipeline.**
   Three punch levels, 9 s minimum hold, pauses shortened to ~0.30 s instead of 0.16 s, cards
   that fade over 0.5 s and drift slowly, no SFX bed at all, music at −23 dB. Every insert is
   REAL: the actual macro-tracker recording, the real trainer/meal-plan/brief screens, Dan's
   real photos, one AI image (his own goal image) tagged. Dan stays on screen beside every
   phone panel (panel LEFT, Dan in the right column) — the product and the person together is
   the trust device. Coverage 54 %, Dan fully replaced only 16 %.
74. **The 8/28 shoot is S-Log3 / S-Gamut3.Cine 4K with FOUR mono audio tracks.** No prior
   grade transfers. `make_lut.py` builds a 33³ .cube in numpy (Sony's S-Log3 transfer →
   linear, the S-Gamut3.Cine→Rec709 matrix in linear, a soft shoulder, the 709 OETF) and
   `lut3d=...:interp=tetrahedral` applies it; exposure 1.45× and `eq=saturation=0.88` were
   picked against the approved Ad 3 skin. **The lav is a:1** (SNR 40 dB); a:0 is the far mic,
   7.2 ms late, polarity inverted; a:2/a:3 silent. `-map 0:a:1`, never `-ac 1`. → measured per file by `pick_lav.py`; `base.py` reads its JSON.
75. **Render the base at 2560×1440 when the source is 4K.** The 1.30 punch of 1440p is
   1969 px wide, so no framing level ever upscales; the cost is ~1.8× the base encode.
76. **`loudnorm` fell back to DYNAMIC on this mix and the JSON said so.** −19.3 LUFS in with
   TP −1.8 cannot reach −14 / −1.5 linearly. `audio2.py` is the replacement: measured gain +
   `alimiter`, the limiter's delay MEASURED by cross-correlation (239 samples here, not the
   remembered 219) and trimmed, then ebur128 on the result. Set the limiter low enough for
   the AAC overshoot (0.71 → −2.2 dBTP on the delivered file). → the finish stage of `_shared/audio/voice_chain.py`.
77. **Previewing a QTRLE alpha .mov with `-ss` + `overlay` onto a single PNG shows NOTHING and
   looks like a broken graphic.** The still base has one frame at t=0 and the seeked overlay
   never lines up. Extract the graphic frame to RGBA PNG and composite in PIL instead —
   `pv/preview_sheet2.jpg` is the pattern. Cost 20 minutes and nearly a needless rebuild.
78. **Assert panel-heading width before building** (`ml.text_size(heading.upper(), font(68,
   'ExtraBold'))[0] <= panel_w − 2·PAD`). "A plan you can actually follow" measured 1215 px
   against a 794 px limit and ran straight across Dan's chest in the preview; even "A plan you
   can follow" (851) failed. Lesson 55 as a one-line assert, so it cannot recur.
79. **A card the video ENDS on must not fade out.** `card_in`'s default out-fade exposed the
   talking head for the last 0.36 s — visible only on the watch pass's final frames. `hold=True`
   in `_card` sets `out_dur=0`; the website's button sits under the player, so ending on the
   CTA card is the design.
80. **Thin hard splices HARDEST-FIRST inside the spacing floor.** With a 3.5 s floor, first-come
   ordering covered a 1.2-diff splice at 50.35 s and left the 2.62 one at 51.08 s bare. Sort
   the candidates by measured difference, accept greedily against the floor.
81. **Two-roll EDLs: `edl.py` anchors spans by phrase per roll and validates every edge against
   a −40 dB envelope**; `base.py` takes N sources. The price line was re-read on the second
   roll after Dan caught the script's `$[X.XX]` on camera (`"$20 … I forgot to put that in the
   script"` → `$19.99` on C1651) — take the correction, cut the slip.


Website conversion video rev 1 — REJECTED 2026-09-02 (audio, framing, graphics, in that order).
Handoff for rev 2: `Handoffs/handoff-20260902-website-video-rev2.md`. Standing rules that came out
of it, all three of which now fail a build rather than living in prose:

82. **NEVER SHIP THE FULL WIDE FRAME FROM THE KITCHEN SET, AND NEVER A LEVEL THAT SHOWS THE LIGHT.**
   Dan: "I don't want to use this wide shot ever… this was shot in 4K intentionally from far away so
   we have room to punch in." The widest allowed level is top-of-head → shorts with the counter
   barely visible (1.256× on the 8/28 set: 3058×1720 @ (451,40)); the tight level is head → navel
   (1.66×). The studio light sits at x>3560 in the 4K frame — any crop reaching it is a defect.
   Render the base at full 4K so the tight level never upscales. `layout.py` asserts the crop
   never exceeds the widest level and never crosses the light.
83. **GRAPHICS SPARINGLY, AND NEVER ON A BLACK FIELD WITH ONE SMALL ELEMENT.** Dan on the J2AD
   phone panels and bullet panels: "a graphic on the left and a huge amount of black space… just a
   bunch of text, generic… horrible." Rule: no graphic with more than ~40 % empty field; an app
   screen goes NEXT TO DAN over the footage (a phone-shaped inset in a slightly wider crop), not on a
   plate; when a full-frame card is used it fills the frame the way Muhammad's title cards do. His
   panel field is the mid-olive gradient (`orglib.py` / `motionlib.MIL`), not near-black.
84. **IF A FEATURE LOOKS LAME ON SCREEN, DON'T SHOW IT.** The trainer workout screen with stick-figure
   exercise icons was called "awful". The choice is not "which screen" but "screen or Dan"; Dan wins
   unless the screen is genuinely good. Before/after and body-fat stats live on the viewer's own
   screen for the website video — the script says "look near your image".
85. **"How I look today" = Muhammad's four photos**, `00 ASSETS USED IN THE REFERENCE AD/04–07`, in
   sequence, never side by side with the before picture. The before picture goes ON "I've been out
   of shape" and nowhere near a line about being lean.
86. **The audio complaint will be described as "the two-channel issue" whether or not it is one.**
   Measure first (Step 0.5). Comb filter = L/R correlation near 0 with a 7–8 ms lag peak; floor =
   voice-over-floor per band; tone = the 10-band fit. Three different fixes, one word from Dan.


Website conversion video rev 2 — delivered 2026-09-02, the same day rev 1 was rejected. Audio gate
PASSED on the delivered file (tone 0.80 dB mean / 2.10 max vs his ad; floor +2.6 / +0.3 / +0.6 dB vs
his), QC 14/14, watch pass clean, $0.00 spend. Reproducible from `reference/recipe/` (rev-2
scripts; rev 1's are in its `rev1/`). What it added:

87. **Fit the EQ against the GATE'S OWN metric, iterate, and stop at the smooth iteration.**
   `voicefit.py` copies `voice_ref_check.py`'s analysis and iterates 10 parametric bands (they
   interact — one pass leaves 2.9 dB at the top band). Iteration 2 passed (0.76 mean / 1.06 max);
   iteration 6 reached 0.30 only by alternating +4 / −3.4 / +1.5 / −7.4 / +1.7 / −5.2 on neighbouring
   bands — an over-fit comb, not a voice EQ. A hand "+1.2 at 950 Hz" on top made the max error worse
   (1.06 → 1.69). Ship the first smooth passing curve.
88. **The bed is a floor problem, and every 4 dB of bed is ~2.5 dB of floor.** The bed file is
   −9.5 LUFS against a −22 LUFS voice, so rev 1's "−23 dB" sat 10 dB under the voice and 9.5 dB over
   his floor. Measured: −30 fails by 8 dB, −34 by 5.6, −40 passes 1.9 dB dirtier than his, **−44 lands
   on his floor**. State the bed as dB below the VOICE's integrated level (34 dB here), never as a
   volume on the file, and let the gate pick it.
89. **The loudness finish costs floor too.** +9 dB of gain into the limiter took 0.5–2.6 dB off
   voice-over-floor (premix +8.8 / +5.4 / +3.8 → finished +8.3 / +3.8 / +1.2, no bed). EQ alone does
   not move the ratio (it scales voice and floor together in-band); makeup, limiting and the bed do.
   Run the gate on the FINISHED file — the premix passes things the master does not.
90. **Measure the reference's cards; do not inherit a description of them.** The handoff said his
   photo cards put Dan in the other half of the frame. A pixel scan of his native frames showed
   FULL-FRAME plates — 1476×924 on 1920×1080, photo inset 28 px, plate (66,76,37)→(80,89,49) on a
   (10,11,5) grid field, title plate 1497×764 with ~142 px oblique caps at 0.88 leading — and his
   phone splits at ~475×922 with Dan filling the right half. That is why his cards never read as
   "one small element on black": the plate IS the frame. `gfx2.py` is that system.
91. **Framing levels are code.** `layout.py` asserts every crop is no wider than the widest allowed
   level and ends before the light (first bright pixel measured at x=3672 on two frames; guard 3530),
   and `qc.py` re-asserts it on the plan. Two traps on the way: crop widths must be even (2311
   failed), and the alternation counter must advance exactly once per segment — the rev-1 pattern
   double-stepped into MID/WIDE/MID/WIDE with no TIGHT for the first minute.
92. **Before → Dan → after needs an explicit gap.** Dan's note put the before photo on "out of
   shape" and the after photos on the very next clause; the beat sheet's 0.35 s merge rule would have
   crossfaded the two cards into a superimposed before/after for 0.4 s. End the before card 0.5 s
   before the after card, so Dan is on camera between them.
93. **A phone beside Dan in the footage is one alpha MOV**: the recording through a rounded-rect
   mask (`alphamerge`), onto a transparent `color` source with `overlay=format=rgb`, then a
   hairline+shadow plate PNG, `fade=…:alpha=1` at both ends, QTRLE argb. `layout.py pip` builds it
   and `mix()` overlays it like any card. Size it like his (433×820 at 1080p), Dan pushed to 65 %.
94. **A contact sheet made with `fps=1/N` and `%{pts}` labels lags the content by ~N/2 s.** Tile
   "0:40" showed a card's fade-out that happens at 42.5–42.9 s, "3:35" showed a card that starts at
   216.45 — three false alarms in one review. Grab suspect frames with exact `-ss` before calling
   anything a defect; `deliver.sh` now builds the sheet from exact grabs.
95. **Reusing a rev-1 graphic requires its beat to be unchanged — ffprobe it.** Five of the six
   lower thirds matched; `num2.mov` was 0.15 s short of its rev-2 beat (rev 1's beat sheet had
   trimmed it against a neighbour that no longer exists), which would have repeated a transparent
   last frame for four frames. Assert `|mov − beat| < 0.1 s` for every reused MOV before the mix.
96. **Concurrency held at two builds all session** by putting the long chain in the background with
   a process waiter (`wait_stage2.sh`: `kill -0 PID` loop, hard timeout, grep for the wrapper's
   RENDER COMPLETE line, then launch the next stage) — the audio fit, card previews and script work
   ran in the foreground while the 4K base (29 min) and the 4K tight (~25 min) encoded.


Website conversion video rev 2 — REVIEWED 2026-09-02: **audio approved** ("you got it nailed. This is
the audio that we want"), rejected on headroom (every shot), one repeated line, and captions colliding
with every lower third. Handoff for rev 3: `Handoffs/handoff-20260902-website-video-rev3.md`. Standing
rules from it, each of which must be a measurement or an assertion, not prose:

97. **ANCHOR EVERY CROP TO THE MEASURED HEAD, NEVER TO THE FRAME.** Rev 2's levels were top-anchored
   at y=40 from a grid frame that read the head top at y≈100; `reference/recipe/headtrack.py`
   measured the real head top every 0.5 s across the cut at **296–340 px** (median 336) — that frame
   was not in the video. Result: 168–232 px of headroom at 1080p, worst on the tight level, which is
   Dan's "very, very bad crop." Rule: per punch segment, `y0 = segment_min_head_top − 0.03 × crop_h`;
   the head top lands ~30 px from the top edge in every level; the bottom edge goes as low as the
   zoom allows (shorts and counter visible on the wide level). **QC asserts the headroom on the
   DELIVERED frames** (head top within 15–60 px of the top, never cut). One reference frame is not
   the video; measure the whole cut. Detector caveat: when he looks down the skin test misses and the
   value jumps — use the per-segment minimum, misses only go down.
98. **A STRETCHED WORD IS A HIDDEN RESTART UNTIL PROVEN OTHERWISE.** Whisper stitched "Now, I've been
   out of shape, — I've been out of shape, and now at 40" into one 1.75 s `and`, and `orphan_scan.py`
   passed because the stretched interval covered the energy. Dan heard the repeat at 0:32. Run
   `reference/repeat_scan.py` (words > 0.7 s, repeated 4-grams within 25 s) after every transcription
   and before the EDL, and re-transcribe every flagged span IN ISOLATION (4 s window, medium.en,
   `condition_on_previous_text=False`). Cut the first attempt, keep the fluent restart.
99. **CAPTIONS NEVER OVERLAP A GRAPHIC — measured in pixels, asserted in QC.** All six lower thirds
   sat at y 757–905 and the "lifted" captions (MarginV 300) inked at 727–806: 49 px of overlap on
   every lower-third beat, and QC only checked captions against full cards. Dan: "move the graphics
   down so they don't overlap with the captions. Let's make this a standing rule." Lower thirds sit
   at the bottom (box ≈852–1000), captions lift above them (`MV_LIFT` from the measured ink bottom:
   ink bottom ≈ 1080 − MarginV + 26 → 290 for ≥30 px clearance), and QC renders the ASS over black at
   each lifted cue and asserts a ≥20 px gap to the lower third's alpha bbox, plus no ink inside the
   phone box. Geometry you assumed is not geometry you measured.
100. **When a revision passes every gate and still gets rejected, the gate was measuring the wrong
   thing.** Rev 2 passed 14/14 and a clean watch pass; none of them measured headroom, caption
   clearance to lower thirds, or restarts hidden inside a token. Each review adds the check that
   would have caught it — that is how this skill scales out of Dan's eye.


Website conversion video rev 3 (2026-09-02, same day) — the three rejected items rebuilt from the
handoff's measurements; audio chain untouched. Reproducible from `reference/recipe/`
(`rev3.sh` is the whole chain). Both new checks were run on rev 2's delivered file FIRST and failed it
(caption gap −47 px on 21 cue/graphic pairs; headroom 159–261 px, median 201) — that is the proof a
new gate is measuring the right thing before it is trusted on the new render.

101. **Fix a stitched restart in the TRANSCRIPT first, then cut — and DROP every word inside a removed
   span.** `to_tight()` collapses a word that sits inside a removed span onto the splice, so the first
   attempt's five words would have captioned the cut line twice; the dry run showed it before any
   render. `tx_patch.py` splices the isolated medium.en pass's words into the roll JSON (the first
   word keeps the envelope onset; the restart's first word takes the measured −40 dB rise, 0.15 s
   after Whisper's start), `tight.py` `MANUAL_CUTS` takes a BASE-time span with both edges asserted
   against the envelope, absorbs the pause cuts inside it, and drops the words. Set the patch window's
   edges BETWEEN the last token to replace and the first to keep — a window ending at 51.95 removed the
   "I" at 51.90 and the isolated pass's "I" at 52.14 fell outside it. A dry run (`RENDER=0`) that
   prints the words around the cut costs seconds; a render that captions a ghost word costs an hour.
102. **Track the head on the BASE, not on the tight cut, and key the track to the keeps.**
   `headtrack.py` samples `base.mov` at 4/s and maps each sample through `tight_cuts.json`; a re-cut
   needs no re-extract, and `layout.py` asserts the track's keeps signature at import so a stale
   track fails the build instead of framing the video. 982 samples, 0 without a detection, head top
   min 296 / median 340 (4K px). Validate the detector on the TALLEST frames, not just a random
   sheet — `pv/headtrack_tallest.jpg` is what proves the per-segment minimum is a head and not wood.
103. **A fixed crop can hold the headroom at his TALLEST instant, not on every frame — assert what the
   crop controls.** Anchored to each segment's minimum head top, the head sits ~33 px below the edge
   at his tallest and the rest of the spread is his own posture inside the hold (up to ~50 px of 4K in
   10–15 s). A crop that followed the slouch would cut his head when he stands up. So the gate is:
   ≥15 px on every valid frame (never cut), per-segment minimum ≤45 px (the crop IS anchored), median
   ≤60 px, ceiling 90 px — not "60 px on every frame". Look-down misses only ever read LOW, so a
   sample is valid when it is within 40 px of the ±1.5 s minimum; print the rejected count.
104. **Measure caption clearance by rendering the cue ALONE, retimed to t=0, over GREEN.** Rendering
   the whole ASS over lavfi black at the cue's real time decodes minutes of frames per cue, and over
   black the outline and shadow are invisible to a bbox — the ink measures ~6 px smaller than what the
   viewer sees. Green frame, bbox of everything not green, against the graphic's own alpha bbox at
   three points across the cue (the lower third is still growing in at its first frames); assert
   ≥20 px wherever they overlap horizontally. The fix itself: `motionlib.lower_third_bar(bottom=1000)`
   (plate 878–1000, alpha incl. its shadow 858–1044) and `MV_LIFT=290` (ink bottom 795, two-line cues
   grow up to 668): 63 px clear.
105. **A cut shrinks the card that sits on the cut line — re-plan the beat, don't just rebuild the
   MOV.** BEFORE went 2.6 → 1.8 s. Fades 0.30/0.30, card out by "and" (Dan: never let the before
   picture run into "and now at 40"), Dan on camera for "and now at 40," (1.1 s), and TODAY moved
   from "now at 40" to "I have the most defined abs" — the claim the four photos prove. `beats.py`
   asserts ≥0.5 s of Dan between the before and after cards, so the merge rule can never crossfade
   them. This was a judgment call and is flagged as such in the delivery.
106. **The head track must be measured at the DELIVERED scale too, and the crop takes the minimum over
   both.** The first rev-3 render passed 17 of 18 checks and failed its own headroom floor: 7–11 px in
   three TIGHT holds, hair on the edge, although the base-sampled track had placed the head 33 px down.
   Two causes, both structural: the delivered check samples at a different phase, and its narrower
   band (the same physical width the QC uses) reads the crown a few rows higher than the 90-px band on
   the 4K did. `headtrack_refine.py` runs the QC detector on `punched.mov`, maps every head top back
   into 4K through that segment's crop, and stores them under `refine`; `layout.py` merges both tracks
   before the per-segment minimum. Segment anchors moved 3–34 px (4K); the two near-cut holds by 34
   and 29. The plan → render → measure → refine → render loop can only move a crop UP, so it converges
   in one pass. Rule: the sampler that gates the delivery is the sampler that anchors the crop.


Website conversion video rev 3 — REJECTED 2026-09-08: **the top of Dan's hair is cut off in every hold**, the wide
level is banned, and he wants AI clips to break up the talking head. Handoff for rev 4:
`Handoffs/handoff-20260908-website-video-rev4.md`. The framing failure is the lesson, and it is a bad one:

107. **HAIRLINE IS NOT HAIR. A detector line that "looks right" on a small tile can be 90 px inside the hair — validate
   at NATIVE scale on his tallest frames, and never gate with the same detector that built the plan.** Rev 3's "head
   top" was the first row with ≥30 % skin at `r>120`, minus a 40 px allowance from the same bad grid frame as rev 2's
   y=40. On his tallest frames it read 296–300 (4K); the real top of his hair is at 196–215 (`pv/hair_measure.jpg`,
   contrast-stretched 4K crops with a 50 px grid), and the hair band is 64 px, not 40. Every proof sheet — the 480 px
   tiles of `headtrack_check.jpg`, `headtrack_tallest.jpg`, `headroom_sheet.jpg` — showed a red line "on the head",
   because at that scale a line at the hairline and a line at the hair top are two pixels apart. So 23 of 26 holds
   cropped the hair by 17–50 px at 1080p, and the delivered-frame gate passed 21–95 px of "headroom" because it
   measured to the same wrong point. Three rules, each of which alone would have caught it: (a) the anchor is the HAIR
   TOP, found by climbing from the skin start through the dark hair band until the row is back at the doorway header's
   luma (hair ≈(26,28,25), header ≈(34,38,37)); a climb under 55 px is a MISS and reads LOW, the dangerous direction —
   discard it; (b) the proof sheet is native-scale crops of the head with a grid, tallest AND median frames, contrast
   stretched, looked at; (c) the delivered-frame gate needs a test independent of the detector — hair-coloured pixels
   in the top rows of the head band = FAIL — because a gate built from the plan's detector inherits the plan's bias.
   Dan's screenshot at 0:05 (hair against the top edge) is the reference failure.


Website conversion video rev 4 (2026-09-08, same day) — the hair fix, the AI inserts and the two phone PiPs, built to
`Handoffs/handoff-20260908-website-video-rev4.md`. Reproducible from `reference/recipe/` (`rev4.sh` is the
chain after the first punch). What it added, each as a measurement or a gate:

108. **THE HAIR DETECTOR THAT WORKS, in numbers (`reference/recipe/hairdet.py`).** On the graded 4K base the door
   panel behind Dan's head is luma 36–37 with a row-mean sd of 0.5 for the whole video; his hair is luma 20–30; the
   relaxed skin test (`r>g+10, r>55, g>b`) fires 50–78 px of 4K below the true hair top when he is upright. Two things
   made the handoff's sketch fail on 92 % of frames and this one succeed on 1786 of 1963: (a) a pixel counts as HAIR-DARK
   only when it is 5 levels darker than ITS OWN COLUMN's header luma — the door's dark grooves chain a naive per-column
   walk straight up to the top of the frame (a 12-px gap tolerance read the hair top at rows 25–105); (b) the walk
   runs on the band's hair-dark FRACTION per row (≥ 0.20, band 160 px centred on the dark-hair blob, not on a fixed x),
   tolerating 12 consecutive rows under it so the hairline transition and the crown sheen do not stop it. Valid climb
   50–110 px (short = stopped inside the hair = reads LOW = discarded). Longest run of discarded samples 1.5 s.
   The delivered-scale callers resize the head region back to 4K scale and use the base's static column profile
   (`hairtrack.json` `hdr_col`), so there is ONE detector, three callers.
109. **Prove the gate on the known-bad file first, and make one of its tests detector-free.** `hairgate.py` on rev 3's
   master: hair top 1 px, 626 of 771 samples discarded because the climb starts at the frame edge, and the independent
   test — the top 12 rows of the head band hair-coloured against the door's column profile — failed 5371 of 5781
   frames. The same file had passed rev 3's headroom gate at 21–95 px. A gate that finds nothing (it only asks whether
   the top rows look like the door) cannot inherit the plan detector's bias.
110. **Veo's "celebrity likeness" filter is per STILL, not per character.** Seven stills of the same generated man from
   one reference image: six passed, the frontal kitchen one was filtered. Regenerating that still in three-quarter
   profile (same reference, same prompt otherwise) passed; nothing about the man changed. Filtered attempts are not
   charged; budget one retry per set.
111. **Veo can bake a cross-DISSOLVE between two shots into an 8-s clip** (D2, 3.9–4.6 s: a translucent double image
   of the close shot over the wide one). Scan every clip's frame strip for it. The fix is free: cut the two clean
   shots together with a straight cut (`build_inserts.py EDIT`), which reads as ordinary b-roll editing where a
   dissolve reads as an edit inside the AI clip.
112. **Concurrent builds starve short jobs past the harness timeout.** A 6-s insert render took 143 s beside the 4K
   punch encode, and a foreground `build_inserts.py` call was killed at five minutes with nothing lost only because
   each asset writes last. Run asset builds as a background script with per-step timing and a completion line, and
   make the chain grep for that line before it needs the assets.
113. **Capture logged-in app screens on a LOCAL server with a fixture account, never with a real login.** `node
   server.js` with `DATABASE_URL=pgmem://local` and `ADMIN_EMAILS=<fixture>` (in `.claude/launch.json`), then the
   app's own signup → admin beta-members → login endpoints from a Playwright script (`hub/hub_capture.py`) and the
   session token dropped into `localStorage` (`absbyai_session_token`) before the page loads. The hub hero
   (before+after side by side) never renders because the fixture has no transformation; the comp-account wording
   ("Beta tester") and the Daily Brief (needs the live AI) are hidden for the capture; all nine feature tiles are real.
   A full-page screenshot (1170×3048 at DPR 3) plus a sliding 2214-px window is a perfect slow scroll, and the scroll
   ends on the last feature tile, not on the account-deletion link below it.
114. **A phone PiP is 433×820: capture at 390×738 CSS (DPR 3 → 1170×2214) so it fits the box with no crop.** The Ad 2
   session's iPhone-13 viewport (390×664) is a different aspect. The macro tracker was re-recorded on absbyai.com at the
   right viewport (`macro2/record_macro.py`, one real analysis call, no account); viewport shots are located inside the
   full-page shots by exact pixel match (`_offset`, error < 3 levels), so scrolls between states are animated smoothly
   instead of jumping between screenshots.

115. **Every Veo clip's FIRST and LAST second get a frame strip and a look before the clip goes in — that is where all
   three artifacts of the website video lived.** Rev 4 shipped two Dan caught at once: the grilling clip's "leans in and
   breathes in the smell" rendered as smoke from his mouth in the insert's last second, and the portioning clip's static row
   of containers drifted and vanished in its last second (a third, the baked dissolves, was caught before delivery — lesson
   111). Two rules: (a) `build_inserts.py`-style strips of 0–1 s and the final second of every insert are part of the
   by-eye pass, not optional; (b) never prompt an action the model renders badly — anything with breath, smell, steam or
   blowing near the face, and any beat that ends on static objects (the model drifts them). Fix by trimming to the clean
   span and shortening the beat (start the run a word later, give the difference to a neighbour with spare clip), never by
   slowing below 0.85×; regenerate only when the clean span cannot fit.

Website conversion video rev 5 (2026-09-08, same evening) — Dan's rev-4 review: the framing APPROVED and LOCKED, plus two
Veo clip-tail artifacts and the goal-image card removed. Built to `Handoffs/handoff-20260908-website-video-rev5.md`,
$0.00 spend, all gates green. Two rules came out of it, and the second one is worth more than the video:

116. **A moved beat edge is not automatically a re-render — diff the plan, then diff the PIXELS.** Rev 5 moved three
   insert edges; the punch plan changed on paper (two boundaries), which by the standing rule forces a ~20-minute punch
   encode. Comparing the two plans FRAME BY FRAME — the crop each output frame would get under the old plan against the
   new — showed **29 frames of 6900 differ, and all 29 sit inside a full-frame opaque insert**, so nothing visible
   changed and `punched.mov` was reused unmodified. The test is three steps: build the per-frame (level, crop y) for both
   plans; intersect the differing frames with the opaque-coverage map (an AI insert is opaque except during its own alpha
   fade, and `ai_inserts()` only fades at the OUTER edges of a run, so mid-run clips are opaque end to end); re-render
   only if anything is left. Run it before every punch a beat change appears to force — it cost 40 seconds here.
117. **ffmpeg LIVELOCKS on a deep multi-input overlay graph, and it is indistinguishable from a slow machine until you
   `sample` it.** The 21-input `layout.py mix` ran 11 minutes to 5 % (3.5 h projected) against rev 4's 9 minutes for the
   identical graph. Every measurement said the machine was fine: the x264 encode floor was 38 s per 60 s of picture
   (0.63x real time), decoding EVERY overlay MOV cost 2 s in total (`today.mov` is 554 MB and decodes in 0.9 s), the
   drive read at 427 MB/s and wrote at 150 while doing 0.1, and RSS was 2 GB of 32. `sample <pid>` settled it in four
   seconds: **336 threads, 336 of them parked in `tq_receive`, 0 busy, and the process burning 23 % CPU on the
   park/wake cycle alone.** 21 inputs × ~11 default decode threads is the trigger; `-threads 1` per input does not fix it
   (QTRLE has no frame threading, so the threads are the scheduler's, not the decoder's). **The fix is fewer inputs per
   ffmpeg process:** `layout.py mix()` now takes `MIX_STAGES=N` and runs the overlay list as N sequential passes
   (7 inputs each → 126 threads, 81 % CPU) through **rawvideo .nut intermediates, so staging is lossless** — 20 GB per
   stage on a drive with 1.7 TB free, and they are deleted at the end. 24 minutes for the full mix instead of 3.5 hours.
   `MIX_T` and `MIX_OUT` make a 20-second benchmark of the real graph one command; that benchmark is what proved the
   graph was healthy at the start of the video and pathological later. Diagnosis rule: **all threads parked = livelock,
   kill and restage; threads in encode/decode = genuinely slow, wait.** A caption burn on the same box at the same
   moment ran at 242 % CPU with 53 threads, which is the control.

