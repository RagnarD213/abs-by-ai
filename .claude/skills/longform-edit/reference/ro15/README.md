# RO-15 "Sleep Better With Glycine" (9/23 C1709): round 1 recipe (Claude Opus 5.5, 2026-11-04)

Last film of the 9/23 studio set. One roll, 9:24 raw, cut to 5:24, 9 pieces. Starts from RO-18's round 4 recipe (`../ro18/`,
on `/Volumes/Expansion/_edit_work/RO-18/round4/recipe/`) with RO-31's round-1 pieces (`../ro31/`: colour and voice options, blind AI
start frames, page). Work dir `/Volumes/Extreme/_edit_work/RO-15/round1/` (recipe, review, logs). Review page port 9715. Never commit media.

## What is new here
- **One roll back on the RO-18 code:** `frames.py` without the virtual timeline; `build.py` with one room-tone stretch (C1709 291.0-292.9,
  -65 dB, crest 10-12, measured) and RO-31's rule that pending AI slots stay on the presenter (`placeholder_ai` only for their context clips,
  reading `review/aiframes/<id>/X1.jpg`).
- **`frames.GRADES`:** the colour options are look C (the locked 9/23 LUT) plus one varied property each (saturation, brightness), applied after
  the LUT; `RO15_GRADE` picks one.
- **The voice:** studio B + the +3 dB bass lift won the blind listens only WITHOUT the chain's gate (option 5, mean 6.3 of 10 over 6 runs; the
  gated version 3.8). `fit/eq.txt` = `FINISH:<eq>`; `build.py` then runs voice_chain `--finish-only` and stashes the untreated lav for the gate.
- **`word_fixes.py`:** after `patch_words.py`, the first word of every re-transcribed region is added back from the level strip (RO-14 trap),
  and a word medium.en started before a piece's in-point is moved inside it.
- **1080p review media only (Dan, 2026-11-02):** `review_media.py` remuxes the 1080p first minute for the page and cuts context clips at 1080p
  CRF 19; no 540p copies.

## Traps this round paid for
1. **Pexels `/download/video/<id>/` now returns a Cloudflare page to curl (403, 5.5 KB of HTML saved as .mp4).** Read the CDN file from the
   clip's own page in Chrome (`fetch('/video/<slug>-<id>/')`, keep only `videos.pexels.com/video-files/<id>/...mp4` whose folder is the same
   id: the page also lists related videos), then curl the CDN URL. `/video/<id>/` without the slug is 403 too. Output over about 1,000
   characters is truncated in javascript_tool, and a page cannot POST to 127.0.0.1; save a Blob download (only the first one per page lands).
2. **A background Flow helper deleted another session's file in ~/Downloads** (it picked "the newest .jpg"). Brief every Flow image helper:
   record the folder listing before each download, touch only the new file, copy then delete only that file.
3. **Start frames: 6 of 15 failed the first fresh review** (a headboard narrower than the bed twice, feet cut off, a logo on shorts, a head cut
   by the edge, a man hugging the duvet instead of pushing it off), then 3 of 5 redraws failed again (a squiggly "worm" texture on every
   fabric, a lamp with no base, 24 px of headroom). Say in the first prompt: "the headboard spans the full width of the bed", "plain natural
   fabric textures, no repeating pattern", "whole head in frame with clear space above". A Codex edit of a good composition with only
   "plain textures" fixed the worm texture.
4. **The independent page check found 17 fix-level problems** the gates passed: a sentence pause of 0.17 s that ran "results" into "Once"
   (widen the out to 0.3 s past the measured end and give the next piece 0.24 s of lead), a library clip with brand labels and Dan's head cut
   off (B0002), two stock clips from one shoot (Pexels 6944078 and 6944070: same actor and bedroom), a gamma lift that left no true black,
   and seven lower thirds whose LAST part was readable under 1.5 s or whose bar sat empty for seconds. Before rendering, compute for every
   lower third: first part delay from the strip (under 1.5 s) and last part to the fade (at least 1.5 s); make it one part when the parts
   come too late.
5. **`checks.py` side-card clearance measures sideways only:** L02 flagged "-5 px" where the hand is 300 px below the card. Look at the frame,
   then say so on the page (`page.py` `LOOKED`).
6. **The status board can sit at exactly 2,500 words;** the claim then lives in the Edit Queue and the edit slot.
7. **A second fresh re-check found 6 more** (three lower thirds still too quick, a list line, a join that cut into a lip smack and dropped his
   breath, an ungraded replacement clip). The join fix: keep the breath, end in the quiet after it, start the next piece after the smack
   (a 5 to 10 ms level profile shows both). Bright stock graded down with a curve, not to the studio's median (a white bedroom must stay white).
   Budget one re-check after any page fix pass. Both reports: `INDEPENDENT-CHECK-r1.md`, `INDEPENDENT-RECHECK-r1.md`.

## Round 2 frames (2026-11-05): START+END pairs, page port 9716
Work dir `/Volumes/Extreme/_edit_work/RO-15/round2/aiframes/pairs/<ID>/` (START, END, spec.json with `spec_history`, gate stamps,
reviews); page `round2/recipe/frames_page.py` (refuses any pair without `gate.py --verify`). Six pairs passed after 9 reviewer FAILs:
1. **Codex flags a handful of capsules as self-harm** on some edits (one retry passed); a full-frame outpaint with the capsules in it
   was refused twice. Outpaint only the parts without capsules (top band, then side strips), composite, keep every original pixel.
2. **Widening a frame for headroom:** fill the side strips with the already-filled top in view (separate fills leave tone seams),
   colour-match the new band to the original per column (`a7fix/`), and check light fixtures at the seam (one came out doubled).
3. **Spec anchors must match the intent.** A nose anchor fails a planned sit-up or head turn; with two people MediaPipe tracks at
   visibility 0.01-0.02, so drop the person block and declare both people as moving regions. Record every change in `spec_history`.
4. **lockstill's person mask finds one person:** it pasted the woman back from START. Pass a box for the second person, kept off the
   background between them.
5. **A lamp switching off** defeats the brightness templates (scores 0.2-0.8 with nothing moving). Measure on CLAHE copies
   (`A8/relit_still_measure.json`). I misread a side-by-side crop panel as a 100 px move once; measure, don't eyeball panels.
6. **Codex redraws hair on a head turn** (wet waves became tight curls in 4 of 4 takes); an END where the head stays put held it.
7. **Google refused the Thermostat START 8 of 8** this round (2 of 4 the first time): the second set is a second Codex take.
   Google's END from the X2 Night Sweats start failed review twice (duvet would not move), so that pair uses round 1's X1 start.
8. **Thermal-camera ENDs: never ask for "cooling toward green/blue".** That is a second palette a real camera cannot show; both models
   failed twice. Build the END in code instead (`round2/aiframes/pairs/A3/thermal_end2.py`): brightness = temperature on START's own
   iron palette, a smooth heat field (hands/feet up, core down, small soft warm patch on the sheet), START's residual kept.
9. **Edit chains breed texture.** Each Codex edit of an edit adds swirl fabric and grid skin (reviewers caught it 3 times on A6).
   Start a revision from a fresh text generation, make the END one edit from it, and keep START's pixels everywhere except the parts
   that act (`pairs/A6-r3/a6_composite.py`); keep the blend edge on background, never across a limb (a see-through elbow failed).
   Codex also aged the woman's face on every edit of her: she stays as START, he acts.
