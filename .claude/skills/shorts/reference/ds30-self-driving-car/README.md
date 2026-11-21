# DS-30 Self-Driving Car SFC R1: dedicated Short from raw 9/23 portrait roll C1720, stock-heavy B-roll

"Make Time For Exercise With A Self-Driving Car" (2026-11-15, Claude on the M2). Work folder (media, gitignored):
`/Volumes/Extreme/_edit_work/DS-30/round1/`. Built from the DS-31 AI Homework recipe (same roll, same set). Run from the
work folder: `work/asr.py` + `work/asrw.py` (medium.en words + windowed re-reads) > `prep.py` (cut list, fitted voice +
120 Hz +3 dB, word map, captions) > `picture.py` (wide = camera's original portrait frame, tight = 1056x1878 punch-in,
B-roll) > `graphics.py` (HyperFrames lower thirds + compare card + its transparent evidence twin) > `finish.py` >
`options.py` (colour + voice options) > `gateplan.py` > `watch.py` + judge > `deliver/gate.py --format short` > `page.py`.

## Lessons (each cost a render or a review round)
- **The Oura master's "Tesla self-driving footage" is NOT Dan's car.** It is frame-for-frame Pexels 33016018 (independent
  audit, 19 samples at correlation 1.000). Do not label it his car, and never use it beside Pexels 33016018 in one video:
  that is a repeated stock clip. Cut it from the 2560x1440 Pexels original instead (1.33x enlargement against 1.78x).
- **Check stock for location against the narration.** Rejected under "the average American" / "here in Austin": a Waymo
  in front of Jimmy Kimmel Live (Hollywood), a Zoox pan that ended on the Las Vegas Strip, a night motorway that read as
  Istanbul, a jam with Cape Town plates. Zoom on plates and signs before using any traffic clip. Austin aerials exist on
  Pexels (27811282 Lady Bird Lake).
- **A stock person who looks into the lens or mouths words under Dan's voice is a defect.** Pick the stretch where they
  only listen or look at their screen (5636178 from 2.5 s; 39343985 from 7.0 s).
- **24p stock judders at 29.97** (a held frame every 5th). Play every source frame once instead:
  `setpts=N/(30000/1001)/TB` (1.25x, never blended). Also check stock for sped-up timelapse (13790663 strobed).
- **Whisper word starts after a pause can be 0.3-0.5 s early, and inside running speech a "silence snap" can land late.**
  Snap a word to the first frame above -40 dB after the previous word's end + 0.10 s; verify every sentence-start cue
  against the delivered audio (qa/caption_sync_editor.json style).
- **Cut in-points inside a breath click at the join.** Measure the 10 ms level map, cut at a dip, 20 ms fades at every
  piece edge, and give a new sentence after a join 0.3-0.4 s of pause.
- **The 1120x1990 tight window of DS-28/DS-31 clips the lamp bulb at the bottom.** 1056x1878 from row 780 keeps the same
  headroom and clears the bulb (bulb top at source row ~2670). Raising the window instead pushes headroom past the gate.
- **Lower thirds at the default 9:16 height sit across his torso on the original-frame wide shot.** Use `top_y: 150` in the
  empty backdrop above his head (hair top never above y 438 on this set).
- **Opaque HyperFrames compare card vs captions:graphic_clearance:** render a transparent evidence twin of the same card
  (local template copy, `CFG.transparent` skips the field) and give its MOV to the gate plan.
- **Known gate-vs-rule rows on this set (confirmed by the independent audit):** `framing:no_wide_level` and
  `framing:push_coverage` (wide = original frame, Dan 2026-11-15), audio `tone` (the +3 dB bass lift), `captions:sync`
  (legacy energy method reads the previous cue's speech on continuation cues; sentence starts measured within 10 ms).
