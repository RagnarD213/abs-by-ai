# SL-20 round 1: independent review brief (one Short per reviewer)

You review ONE finished vertical Short cut from Dan Rose's approved long-form "Why You Should Invest More In Your Health" (RO-20).
You did not build it; be skeptical. Expect "does not ship" the first time. Judge the delivered file, not the builder's notes.

Files for short <S> (C, B or G):
- Delivered file: /Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/<name>.mp4 (name in /Volumes/Expansion/_edit_work/SL-20/recipe/plans.py NAME)
- Gate plan (joins, covers, graphics, caption states, AI inserts): /Volumes/Expansion/_edit_work/SL-20/build/<S>/gate/plan.json
- Shot table: build/<S>/shots.json ; captions: build/<S>/cues.json ; delivered transcript: build/<S>/delivered_asr.json ; plan data: recipe/plans.py
- The words Dan approved, with the title: /Volumes/Expansion/_edit_work/SL-20/invest-SHORTS.md. Accepted deviations: C opens "Now, in today's dating environment" ("Now" runs into "in" with no gap, it cannot be cut cleanly); B's second piece opens "So if you're married" (same reason).
- Watch pass: build/<S>/gate/watch/ (CHECKLIST.md, sheets/, strips/) and log build/<S>/gate/logs/watch_pass.json
- Person mask CLI: "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
- ffmpeg/ffprobe: "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg" and ffprobe
- Picture source: /Volumes/Expansion/_edit_work/SL-20/src/ro20_base.mp4 is the approved film's own picture without its lower thirds and cutaways (same frames and clock as the master); the approved master is the RO-20 round 4 file named in invest-SHORTS.md.
- AI clip frame review already done (clips/review_*.md): A0032 0-57 PASS, A0072 frames 6-143 PASS (6-156 FAIL: greens appear on a plate from 146; B plays 6-143 at 0.912x over its slot), the Cb11 phone screens PASS.
- Use a private scratch folder /tmp/absbyai-scratch/SL-20/rev_<S>/ for every frame you decode. Heavy decodes go through the render queue if a tool asks.

## Part 1: the watch-pass judge (required, it is a gate row)
Give EVERY image in watch/sheets and watch/strips a verdict against CHECKLIST.md: clean, defect (item key + time) or expected (a change the plan declares; say which).
Write build/<S>/gate/findings.json as {"entries": [{"image": "<file name>", "verdict": "...", "item": "...", "t": <s>, "note": "..."}]}
then run: python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" --judge /Volumes/Expansion/_edit_work/SL-20/build/<S>/gate/logs/watch_pass.json --findings /Volumes/Expansion/_edit_work/SL-20/build/<S>/gate/findings.json --by "ra-reviewer <S> round 1"
Known source fact: the RO-20 camera (roll C1511) framed Dan's hair at the top edge through the whole roll (the approved film has the same; reported in its round 1). The crop takes every row the source has (window from row 0). Mark hair_top frames as `expected` ONLY if the source itself has no more picture above (check base.mp4); a crop that cuts hair the source has is a defect.

## Part 2: the review (watch the whole file at full resolution, then check)
1. Stands alone for a viewer who never saw the long-form; one point; a reason to watch in the first 5 seconds; ends on its own point, last word whole (listen to the last 0.5 s).
2. Every picture join: no naked jump cut on Dan (same framing both sides and he moves). Use the strips' -1|0 pairs and exact -ss grabs. No one-frame flash of another shot at any cut.
3. Audio: no click, hole or clipped word at any join (listen around each join in plan.json); no stumble or half-restarted word; level steady; natural pause (0.4-0.6 s) at the audio join.
4. Captions: match what is heard, timing within about 0.2 s, never over his face, never covering a clip's subject; never split a phrase badly; `abs` lower case.
5. Every clip: shows what the words say at that moment; crop on the subject (nothing important cut; whole-frame cards have a reason in plans.py); colour sits with the presenter; AI-GENERATED chip on every AI clip, readable, not on a face.
6. Framing: his face centred and whole in every talking shot (measure with personmask on exact frames); size step at every same-camera cut; no shot that is too tight to read.
7. Title band and key-point bar: title fully inside the band (no clipped descenders), the bar's lines distil (not echo) what he says, line 2 readable for at least 1.5 s, bar never over his face.
8. Anything else a viewer would notice. Also give an explicit opinion on the trade-offs the builder made (cards for 16:9 graphics, the 91% speed dinner clip, opening words).

Write /Volumes/Expansion/_edit_work/SL-20/build/<S>/ROUND-1-REVIEW.md: each finding with output time, what is wrong, evidence (exact frame grabs, measurements) and the fix, then `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`. Report back a short summary: verdict, the must-fix list in one line each, the watch-judge result (open defects count).

## Round 1b (2026-11-05): what changed since the round 1 reviews (read build/<S>/ROUND-1-REVIEW.md first; re-check every must-fix)
- All Shorts: every talking shot now uses `_shared/cut/landing.vertical_track` (lands on his face at the cut, holds inside a tolerance band, follows at the slope cap). Captions under 0.4 s merge into a neighbour; a cut mid-sentence no longer capitalises the next word. A gate stamp will be produced after your review.
- C: the repeated "such a" is cut ("make such a | huge difference", join at about 40.7 s, size step); Cb08 now runs over "looks are paramount" (to 10.5 s); the key-point bar holds 1.1 s longer; Cb11 starts in the silence before "and I know this" and plays at 1x to clip frame 229 (frames 223-235 are the same static screen as reviewed frame 224, max pixel difference 2); Cb12 starts in the silence before "The guys", 0.5 s into the card.
- B: the half-started "or" after "married" is cut (audio join, size step); 0.3 s of the hook pause after "right now" trimmed under the cutaway; Cb01 starts at "in a relationship"; the Cb02/Cb03 cut moved to the silence before "Those are the reasons"; the closing AI dinner clip A0072 is REPLACED by library stock B0485 (a family at dinner), because no clip is ever slowed or held to fill a slot (VIDEO-RULES 2026-10-08).
- G: the half-started "b-" before "just being slaves" is cut; Cc13 starts one frame earlier (no flash); B0214 saturation lowered (eq=saturation=0.55); the key-point bar moved to the WIDE opening shot ("Money Can't Buy Health" / "Health Comes First") so it never reaches his chin.
Write ROUND-1B-REVIEW.md (same format) and re-run the watch judge on the new watch pass.

## Round 1c (2026-11-05): changes since ROUND-1B-REVIEW (read it first; re-check each must-fix)
- G: the shot table had the film's part-3 camera cuts 54 frames (1.80 s) early (a numbering offset in the film's layout); a scene scan of base.mp4 confirmed every corrected cut (723.997, 752.056, 754.525, 767.872). So G's shots, windows and size steps are all new. The end is now film 767.85, before the camera cut at 767.872 (no last-frame flash). The "b-" join: piece 1 runs to 739.41, pause about 0.41 s. Internal audio joins in all Shorts now fade 5 ms each side (was 15 ms; reviewer G measured a 7 ms room-tone dropout).
- C: "is going to make such a" (head down, eyes shut) is covered by a later, unused stretch of the film's Cb10 stock (she lifts her phone for a selfie), straight into Cb11; "a" re-timed (CTC had it after the join).
- B: captions never merge or carry words across an audio join or pause (R1b showed "and you're getting" 1.6 s early); "right now" is never split; the hook trim keeps 0.37 s of the pause; B0485 is a whole 16:9 card at y 560 (the handheld drift cut the mother out of the span crop), graded with curves and saturation 1.2.
Write ROUND-1C-REVIEW.md (same format) and judge the NEW watch pass (the watch folder was cleared before it ran).
