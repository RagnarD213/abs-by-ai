# Independent review brief: RA-06 "What's The Best Ab Exercise?" AD, round 3 full 9:16

You are the independent reviewer. You have not seen the editor's notes and should not trust them. Judge the delivered file
against the plan, Dan's recorded decisions and the standing rules. Be skeptical; say plainly if a problem was traded for another.

**File:** `/Volumes/Extreme/_edit_work/ra06/draft_9x16.mp4` (sha256 in the line above this brief when it was written: re-hash it and report).
1080x1920, 29.97 fps, 45.71 s, an AD (ends on "Tap the button below now to get started").
**Plan:** `/Volumes/Extreme/_edit_work/ra06/beats.json` (cards, Dan holds with levels, lower third LT2, CTA), `timeline_9x16.json`
(per-hold crop and motion stats), `cards_9x16/meta.json` (chip boxes), `round3/split/split_luts.json`.
**AI takes (raw):** `/Volumes/Extreme/_edit_work/ra06/round3/motion/*.mp4` (the shots used: I3_v1 0-5.0 s; I1_v1 0-2.05 s then I1_v2
3.10-4.55 s cropped closer; I4_v2 0.25-2.35 s). Approved start/end frames: `round2/frames/I1-*.png, I3-*.png, I4-*.png`.
**Previous round for comparison:** `round1/DRAFT - RA-06 round 1 - full ad.mp4`.
**Rules to read:** `/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/VIDEO-RULES.md` (top sections,
especially "Never a shot of Dan just standing around", "AI clips that make no physical sense ... never reach Dan", "AI clip faults:
judge at playback speed", "Verticals: the camera lands on Dan, then holds", "Hair never leaves the frame", "All B-roll is colour
corrected"), and `.claude/skills/_shared/CUT-CONTINUITY-QC.md`.
**Person mask CLI:** `/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask` (if useful).
**ffmpeg/ffprobe:** `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/`.

## Dan's decisions this round must carry out (his words are in `round2-plan/decisions.json` and `round3-plan/decisions.json`)
1. Colour C2 brighter gold (unchanged). Voice with bass lift (unchanged mix).
2. Shot sizes "pair 3": close 684x1216, wide 846x1504 source px. "The close is looking a little off-center. Just center that
   close a little bit more." Measure: on every close (NEAR) hold, how far is his head centre from the frame centre (median and
   worst, as % of frame width)? Is any pan the centring adds visible or distracting at speed?
3. Split screen opener (0 to 2.30 s): "make sure this is color corrected. This footage looks very dark. And also make sure I'm
   actively doing the vacuum when you show, not just standing around." Is Dan's body at least as bright as on the talking shots,
   backgrounds not blown or crushed? Does the Stomach Vacuum panel visibly show the draw-in (belly pulling in), not a hold?
   Captions must not sit on his face in any panel.
4. B1 poses clip removed ("A shot of me just standing around"): Dan on camera 27.56 to 32.67 s. Check no standing/posing cutaway
   remains anywhere in the film.
5. Button text must read "Tap The Button Below To / Start Training With AI".
6. AI clips approved on frames: I1 copier (10.98 to 14.48 s), I3 body scan (5.97 to 10.98 s), I4 robot waves goodbye
   (41.47 to 43.58 s, under the button). I5 rejected: the split screen stays the opener.
7. Claim lines are pre-approved: do not raise spoken claims.

## Required for each AI clip (one answer per clip, at playback speed AND frame by frame)
1. Does everything obey cause and effect? Nothing vanishes, appears, melts or changes by itself. (I1: does any sheet appear in a
   hand without being handed over, within a shot? The cut between its two shots is deliberate: judge whether it reads as a cut
   to a later moment or as a glitch. I3: do the outlines crawl or morph after drawing? I4: does the door open because he pushes
   it, and does anything about the box, door or towel break physics?)
2. With the sound off, would a stranger say what the clip shows?
3. Does it show the line he is saying, and does it land in one viewing?
Also: the AI-GENERATED chip present on every frame of every AI clip, never on a face, clear of captions and the button; any
frozen frames, baked dissolves, hard cuts inside a take, flicker, extra fingers/limbs, faces changing.

## Also check, on the whole film
- Every picture cut: no jump cut (same size across a pause splice inside Dan footage), no one-frame flashes at boundaries.
- Hair never at or outside the top edge on any Dan frame; framing lands on him at each cut then holds.
- Captions: never over a graphic, the chip, or a face; accurate to the audio in the first 30 s ("abs" lowercase).
- Lower third LT2 "Copy-Paste Plans Ignore Your Body" (15.65 to 19.95 s) clear of captions and his face.
- The end: what he does after the last word; the last frame.
- Audio: there is a stamped audio gate (`draft_9x16.mp4.audio_gate.json`); confirm its sha matches the file.

## Output
Write `/Volumes/Extreme/_edit_work/ra06/round3/review/ROUND-3-REVIEW.md` in the format of
`/Volumes/Extreme/_edit_work/ra06/review_r1b/ROUND-1B-REVIEW.md` (read it for the format only): first line VERDICT: SHIP or
DOES NOT SHIP with the count of blocking defects; then numbered findings, each with the exact time/frame, evidence file, and
BLOCKING / MINOR. Put evidence images in `round3/review/`. Do not edit any build file. Never use an em dash in what you write.
