# SL-21 round 1: independent review brief (one Short per reviewer)

You review ONE finished vertical Short cut from Dan Rose's approved long-form "What To Cut To Afford Getting In Shape" (RO-20B).
You did not build it; be skeptical. Expect "does not ship" the first time. Judge the delivered file, not the builder's notes.

Work folder: /Users/danielrose/Projects/_edit_work/SL-21 (WORK below). Shorts: A (restaurants, Short 1), D (vacation, Short 2), E (therapy, Short 3).
Files for short <S>:
- Delivered file: /Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/<name>.mp4 (name in WORK/recipe/plans.py NAME)
- Gate plan (joins, covers, graphics, caption states): WORK/build/<S>/gate/plan.json
- Shot table: WORK/build/<S>/shots.json ; captions: build/<S>/cues.json ; delivered transcript: build/<S>/delivered_asr.json ; plan data with the reason for every choice: recipe/plans.py
- The words Dan approved (his picks, 2026-11-13) are plans.TEXT for that Short: the film's own sentences. Accepted openings: D opens "Now I know some of you guys" and E opens "Now, I'm not a psychologist" (in both, "Now" runs into the next word with no dip, so it cannot be cut cleanly). A skips the film's app-tracking passage between its two pieces (one audio join).
- Watch pass: build/<S>/gate/watch/ (CHECKLIST.md, sheets/, strips/) and log build/<S>/gate/logs/watch_pass.json
- Person mask CLI: "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
- ffmpeg/ffprobe: "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg" and ffprobe
- Picture source: WORK/src/ro20b_base.mp4 is the approved film's own picture without its lower thirds and cutaways (same frames and clock as the master). The approved master: "/Volumes/Extreme/Claude Content Videos/What To Cut To Afford Getting In Shape - RO-20B/What To Cut To Afford Getting In Shape | claude round 4 | 16x9 | RO-20B.mp4" (sha256 88a6314f...).
- Cutaways: WORK/clips/. All are the film's own approved stock or Dan's own B-roll at the film's own lines, except two that are new in the Shorts: B0326 in D (library stock, a loaded restaurant table; the film uses it elsewhere) and B0642 in E (Dan doing pull-ups, October 23 gym shoot). No AI clips in any of the three. 25 fps stock was conformed frame for frame to 29.97 (it plays 1.2x fast, no repeated frames).
- Use a private scratch folder /tmp/absbyai-scratch/SL-21/rev_<S>/ for every frame you decode. Do not write anywhere else except the two files named below.

## Part 1: the watch-pass judge (required, it is a gate row)
Give EVERY image in watch/sheets and watch/strips a verdict against CHECKLIST.md: clean, defect (item key + time) or expected (a change the plan declares; say which).
Write WORK/build/<S>/gate/findings.json as {"entries": [{"image": "<file name>", "verdict": "...", "item": "...", "t": <s>, "note": "..."}]}
then run: python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" --judge WORK/build/<S>/gate/logs/watch_pass.json --findings WORK/build/<S>/gate/findings.json --by "ra-reviewer <S> round 1"
Known source fact: the RO-20B camera (roll C1511) framed Dan's hair at the top edge through the whole roll (the approved film has the same; reported in its round 1). The crop takes every row the source has (window from row 0). Mark hair_top frames as `expected` ONLY if the source itself has no more picture above (check base.mp4); a crop that cuts hair the source has is a defect.

## Part 2: the review (watch the whole file at full resolution, then check)
1. Stands alone for a viewer who never saw the long-form; one point; a reason to watch in the first 5 seconds; ends on its own point, last word whole (measure the last 0.5 s of audio).
2. Every picture join: no naked jump cut on Dan (same framing both sides and he moves). Use the strips' -1|0 pairs and exact -ss grabs. No one-frame flash of another shot at any cut.
3. Audio: no click, hole or clipped word at any join in plan.json; no stumble or half-restarted word inside a kept take (measure levels, compare the transcript); level steady; a natural pause (0.4-0.6 s) at A's audio join. Automated checks stay silent: do not play audio through the speakers; decode and measure.
4. Captions: match what is heard, timing within about 0.2 s, never over his face, never covering a clip's subject; never split a phrase badly; no caption straddling a picture cut; `abs` lower case.
5. Every clip: shows what the words say at that moment; crop on the subject (nothing important cut; the push-up card in D is a whole-body card because the pose is horizontal); colour sits with the presenter; no judder or repeated frames; no stranger shown as "I".
6. Framing: his face centred and whole in every talking shot (measure with personmask on exact frames); a real size step at every same-camera cut; no shot too tight to read.
7. Title band and key-point bar: title fully inside the band (no clipped descenders); the bar's lines distil (not echo) what he says, line 2 readable for at least 1.5 s, bar never over his face, never across a picture cut.
8. Anything else a viewer would notice. Give an explicit opinion on the builder's trade-offs: the opening clip (A, D) versus opening on Dan (E); the 1.2x conformed stock; the two new clips; the key-point wording; E ending 0.13 s after "priority." because the film's camera cuts 0.14 s after the word.

Write WORK/build/<S>/ROUND-1-REVIEW.md: each finding with output time, what is wrong, evidence (exact frame grabs, measurements) and the fix, then `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`. Report back a short summary: verdict, the must-fix list in one line each, the watch-judge result (open defects count).

## Round 1b (2026-11-13): what changed since the round 1 reviews (read build/<S>/ROUND-1-REVIEW.md first and re-check every must-fix on the NEW file)
The delivery gate has now run on each file (stamp beside the delivered file; log build/<S>/gate/gate_run.log). The gate plan's negative-events text now describes this Short (plans.NEG).
- All Shorts: caption breaks can be set in plans.TEXT (` / ` forces a break, `a_b{a b}` keeps words together); a camera change between two talking shots now counts as a cut for caption timing; "going to" and "if" no longer strand at a line end.
- A: captions over the card reader (5.67-10.18), the cooks' hands (24.69-31.93) and the noodles (38.41-41.71) sit at the top of the picture, in empty wall / above the lamps / above the wok; "to get in shape, Dan." is one caption; "I don't have the money / for a gym membership."; "at their credit card statement,"; "hundreds of dollars / that you could reinvest".
- D: the opening is the aerial part of the same beach clip (from 13.5 s of the source); the pancake clip's built-in repeated frames were removed (mpdecimate) and it is conformed like the other 25 fps stock; the buffet clip is lifted (curves + saturation 1.1) and now ends in the gap after "rules" (13.14 s); the table clip B0326 is cropped onto the beer, cocktails and plates; caption breaks reset ("the usual rules / of working out / and eating / for most people / go out the window.", "every morning / and I fast until", "I would gain / 5 or 6 pounds of fat / per week / that I was on vacation.", "but it's going to be / way more enjoyable / when you're ripped / and when you have / your health habits dialed in."). "going to" stays: the film's corrected transcript, Whisper medium.en and a wav2vec2 greedy decode all read "going to" (Whisper small.en reads "gonna").
- E: captions over the pills (26.06-29.56) sit in the felt above them; "you get in great shape," is one caption, "a gym membership / if you're broke?", "is ever going to make you"; "Now again I'm not" starts on the cut frame; the pull-up clip's midtones are lifted (curves); the counseling clip starts 1.45 s in, after its fast opening tilt.
Not changed, on purpose: the landing camera (Dan's standard: it lands on his face at each cut, holds, and follows only past its tolerance at a capped speed), so his face can sit about 10 % off centre for a second when he turns; the key-point wording.
Write build/<S>/ROUND-1B-REVIEW.md (same format, VERDICT line) and judge the NEW watch pass (--by "ra-reviewer <S> round 1b"). The watch folder was cleared before it ran.

## Round 1c (2026-11-13): what changed since the round 1b reviews (read build/<S>/ROUND-1B-REVIEW.md first; re-check each must-fix on the NEW file)
- All Shorts: frame mapping fixed. A talking shot that starts on a film camera cut started one frame late (its first frame showed twice, one source frame was skipped: E at 22.39 and 37.04), and a rounding offset could hold a shot's last frame; the build now maps every output frame to consecutive source frames (verified: zero non-unit steps in all three). Captions: ` / ` forces a break, ` + ` keeps the next word in the caption being built.
- A: "at restaurants / two or three times per week."; "But you look at their / credit card statement,"; "oh, I don't have the money / to get in shape, Dan."; "and they just care about / how the meal tastes,"; raised captions now start 90 px under the title band (y 400); the closing vinegar clip's captions are raised too (they covered the measuring spoon).
- D: the last repeated pancake frame is gone (every frame of the window is measured and each repeat dropped by index; the prepared clip has none); "and I fast / until 2pm every day."; "of you guys / aren't gonna like hearing this."; "your health habits / dialed in."; no second punch-in on the closing line (the close crop had to pan when he stepped sideways), so 39.91 to the end is one full-window shot.
- E: caption breaks: "That's a whole / different discussion.", "The discussion / that we're having is,", "On the other hand, / if you have" (one two-line caption), "great physical health,", "attaining great / mental health" (one two-line caption), "you've got to / sacrifice that" then "permanently.", "to sacrifice that / until you get in great shape,", "the productivity / to make more money,", "and eventually / you can reinvest in that / once you've taken care / of the higher priority." The pull-up clip keeps its captions in the standard place (they cross his shins on the low half of a rep; two-line captions do not fit the floor under his feet). The gate text now says a person seen from behind walks into the gym.
Known and accepted, not defects: hair at the top edge (source framing); the delivery gate's two hair rows fail for that reason on every Short from this roll and need Dan's acceptance, which is requested on the review page.
Write build/<S>/ROUND-1C-REVIEW.md (same format, VERDICT line) and judge the NEW watch pass (--by "ra-reviewer <S> round 1c").

## Round 2 (2026-11-13): one new lip-synced AI clip in Short 1 and in Short 2 (two versions of Short 2). Read this section, not the round 1 files' verdicts.
Dan watched round 1 and approved Short 3 as is, and Shorts 1 and 2 except for ONE new clip each: an AI "excuse guy" whose lips are synced to
Dan's own recording of the excuse line. Everything else in both Shorts is approved and must be unchanged. Builds: A2 = Short 1; D1 and D2 =
Short 2 with two different beach guys (Dan asked to see both and will pick one). Delivered names: plans.NAME["A2" | "D1" | "D2"]; build
folders WORK/build/<A2|D1|D2>/ (gate plan, shots, cues, watch pass as before). The approved round 1 files are in
"/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/whattocut REVIEW/round1/".
What changed, exactly:
- Short 1 (A2), 0:01.53 to 0:05.67: Dan on camera is replaced by the restaurant excuse guy (WORK/clips/AIr.mp4 from its 0.4 s). The line:
  "oh, I don't have the money to get in shape, Dan. I don't have the money for a gym membership." Captions in that shot sit at y 1540.
- Short 2 (D1, D2), 0:02.61 to 0:05.94: the aerial beach clip now runs to 0:02.85 (through Dan's "You're like,") and the beach excuse guy
  plays from 0:02.85 to 0:05.94 (WORK/clips/AIb1.mp4 or AIb2.mp4 from its 0.4 s). The line: "I need a vacation. I deserve a break because
  I work hard." The "You're like," caption now shows over the aerial clip. Dan's shot after the clip keeps the round 1 camera path.
- Each AI clip carries an AI-GENERATED chip. The mouth is the take's own closed mouth before his first word and after his last.
Your job:
1. Prove nothing else changed: compare the delivered file with its round 1 file frame by frame and sample by sample outside the changed
   stretch (WORK/recipe/samecheck.py NEW OLD T0 T1 does it; run it yourself with the window above, then spot-check with your own grabs).
   Any difference outside the window is a must-fix.
2. The new clip, at playback and frame by frame: does it show the line (a fat man at an expensive dinner / on a tropical beach, whining the
   excuse); cause and effect (nothing vanishes, appears, changes hands); does it look like real footage or like AI; hands and fingers;
   the lip sync against the words (lips closed on m, b, p; open on the vowels; no talking in the silences; no seam, smear, doubled lips,
   soft patch or border on the lower face; teeth); no repeated or held frames beyond the normal 24-in-30 cadence; the cut into and out of
   the clip (no flash frame, no caption across the cut, the first and last word whole).
3. Captions in the new shot: match the words, never over his face or mouth, do not hide what makes the joke (the food; the cocktail and beach).
4. The AI-GENERATED chip: present on every frame of the clip, readable, not on his face or body.
5. Judge the NEW watch pass (--by "ra-reviewer <S> round 2"): every image a verdict; hair at the top edge on Dan's shots is the accepted
   source framing (Dan approved it), mark it `expected`.
6. Would Dan, who rejects AI slop on sight, be embarrassed by this clip? Say yes or no and why.
Write WORK/build/<S>/ROUND-2-REVIEW.md with findings (time, what, evidence, fix) and `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`. Report a short
summary: verdict, must-fix list, watch-judge open defects. Automated checks stay silent: decode and measure, never play audio aloud.
