# SL-16 round 1: independent review brief (one Short per reviewer)

You review ONE finished vertical Short cut from Dan Rose's approved long-form "Intermittent Fasting: The Best Way To Get Abs" (RO-08).
You did not build it; be skeptical. Expect "does not ship" the first time. Judge the delivered file, not the builder's notes.

Files for short <S> (S1, B, C or D):
- Delivered file: /Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/<name>.mp4 (name in /Volumes/Extreme/_edit_work/SL-16/plans.py NAME)
- Gate plan (joins, covers, graphics, caption states, AI inserts): /Volumes/Extreme/_edit_work/SL-16/build/<S>/gate/plan.json
- Shot table: /Volumes/Extreme/_edit_work/SL-16/build/<S>/shots.json ; captions: build/<S>/cues.json ; delivered transcript: build/<S>/delivered_asr.json
- The words Dan approved for this Short (full transcript under its title): /Volumes/Extreme/_edit_work/SL-16/SHORTLIST.md (Short 1 = S1, B, C, D). Short C opens "And here is" (the "And" cannot be cut cleanly; accepted deviation, say if it bothers you).
- Watch pass: /Volumes/Extreme/_edit_work/SL-16/build/<S>/gate/watch/ (CHECKLIST.md, sheets/, strips/) and log build/<S>/gate/logs/watch_pass.json
- Person mask CLI: "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
- ffmpeg/ffprobe: "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real" and ffprobe
- Use a private scratch folder /tmp/absbyai-scratch/SL-16/rev_<S>/ for every frame you decode.

## Part 1: the watch-pass judge (required, it is a gate row)
Give EVERY image in watch/sheets and watch/strips a verdict against CHECKLIST.md: clean, defect (item key + time) or expected (a change the plan declares; say which).
Write /Volumes/Extreme/_edit_work/SL-16/build/<S>/gate/findings.json as {"entries": [{"image": "<file name>", "verdict": "...", "item": "...", "t": <s>, "note": "..."}]}
then run: python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" --judge /Volumes/Extreme/_edit_work/SL-16/build/<S>/gate/logs/watch_pass.json --findings /Volumes/Extreme/_edit_work/SL-16/build/<S>/gate/findings.json --by "ra-reviewer <S> round 1"
Known source fact: the camera on this shoot framed Dan's hair at or near the top edge through the whole roll (the approved film has the same); the crop takes every row the source has (window from row 0). Mark hair_top frames as `expected` ONLY if the source itself has no more picture above (say so); a crop that cuts hair the source has is a defect.

## Part 2: the review (watch the whole file at full resolution, then check)
1. Stands alone for a viewer who never saw the long-form; one point; a reason to watch in the first 5 seconds; ends on its own point (not mid-thought, last word whole: listen to the last 0.5 s).
2. Every picture join: no naked jump cut on Dan (same framing both sides and he moves). Use the strips' -1|0 pairs and exact -ss grabs.
3. Audio: no click, hole or clipped word at any join (listen around each join in plan.json); no "um"/stumble/half-restarted word; level steady.
4. Captions: match what is heard, word timing (no caption early or late by more than ~0.2 s), never over his face, never covering a clip's subject; `abs` lower case.
5. Every clip: shows what the words say at that moment; colour sits with the presenter (not visibly darker); crop on the subject (nothing important cut, no blank space without a reason: two clips are deliberately square cards, the reason is in plans.py); no clip repeated inside the Short; AI clips carry the AI-GENERATED chip, the chip never touches a person; real stock carries no chip.
   AI clips kept (both passed a fresh frame-reviewer on their exact ranges): B uses A5 (donut then asleep, square card); D uses A0158 (boxing glove). Ask the three questions of each at playback speed: cause and effect, would a stranger with the sound off say what it shows, does it show the line / does the joke land.
6. Key-point bars (Soft Blue lower thirds): never over his face; line 2 lands on its words and stays at least 1.5 s; title capitalization, eyebrow in capitals; graphics move for their whole screen time.
7. Framing: Dan centred (land-then-hold; not panning distractingly), hair as above, no wide level, arms not cut with space on the other side.
8. The title band (top 310 px) reads cold and never overlaps him.
Measure, don't eyeball, wherever a number exists. Grab exact frames with -ss for anything you flag.

## Output
Write /Volumes/Extreme/_edit_work/SL-16/build/<S>/ROUND-1-REVIEW.md: a numbered defect list (time, what, why it matters, the fix), then "Accepted / fine" notes, and end with exactly one line: VERDICT: SHIP or VERDICT: DOES NOT SHIP. Your final message: the verdict and the defect list, short.
