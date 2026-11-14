# DS-41 Kevin James Cheat SFC R1: two-version reaction build and lessons

Reaction Short in the locked Codex R5 format (JRE Clips, "Kevin James on Cheat Days and Losing 60lbs After Fasting for 41 Days", two
pieces), cut twice from roll C1730 (scripted 27:53, off the cuff 28:51) with a shared opening. Built from the DS-36 Fat Shaming recipe
(`../ds36-fat-shaming/`). Work folder: `/Volumes/Expansion/_edit_work/DS-41/r1/` (recipe/, key/, src/, scripted/, offcuff/, review/).
`chain2.sh VERSION` runs prep -> shot times -> graphics -> framing -> `build.sh` (render + gates); `AUDIO_ONLY=1 build.sh VERSION`
remixes and re-burns captions on the existing picture; `gate_only.sh VERSION` reruns the plan and gate, keeping the judged watch pass.
The recipe copy is in `recipe/` here. Read the DS-36 and DS-43 READMEs first; only what was new on this job is below.

## Lessons (each cost a rebuild or a review round)

- **Key only where Dan is on screen.** A take keyed whole was projected at 8 hours. Keying the on-screen stretches as sub-pieces
  (`key_subs.json`, looked up by roll time in `assemble.tsub`) saved about 1,330 frames. Pick each start two decimals with the frame
  fraction of `T0 * 29.97` in 0.78-0.92 so key frame i pairs with source frame i. A shot added later needs its own stretch (`Of`).
- **A clip with two quoted pieces and no room between them.** Kevin has 20 ms after "want" and a false start ("'cause he's") before
  "your one day". Start piece 2's PICTURE about 0.2 s early, hold its own sound out until the quiet (ffmpeg `afade=t=in:st=`), and fill
  the gap with a bed at the clip's floor. Pink noise read 10 dB bright at 1-2 kHz against his room; brown noise high-passed at 60 Hz
  matched its bands. Set the bed level from the FINISHED clip (the compressors lift a bed 3-4 dB more than the room beside speech).
- **Measure the clip's first 300 ms yourself.** The first reviewer placed a fragment at the wrong spot ("20 ms tail"); the clip really
  started inside "thought" (41.43-41.60) and "you" started at 41.76. A 10 ms level map of the head settles it in one look.
- **Whisper's word starts run early, so moving an in-point into the pause drops the first word** from the caption list ("you",
  "Your"). After any in-point change, print the first words of each piece. Fix the time in `audio/clip_words.json` / the wordfix file.
- **Whisper invents a word the sentence expects.** It heard "Because" before "your one day" with the false start cut and nothing but
  -57 dB there, and "I thought" from a 20 ms tail. Trust the level map over the transcript, both ways: it also heard a real soft "And"
  that I had called a breath.
- **No caption sits on a full-screen card** (`captions:card_collision`). `captions.py` drops cues inside card shots; the card must
  carry those lines, so build it one row per spoken step (rows land on words via the template's `rows[].t`).
- **The shared title card is small in 9:16** (headline 72, rows 46 px: 74 % of the frame empty). `graphics.math_card` lays the same
  template out 1.3x larger. A ledger of markers - = + = reads as ONE sum; it only works when line 4 is the net of lines 2 and 3
  ("3,000 Down + 1 Big Cheat Day = 3,000 Back"). Otherwise use two equations (bullet, =, bullet, =).
- **A cutaway that mocks the viewer fails.** A0202 (a heavy man pouting over hot dogs, never eating) did not show "eat any high
  calorie food you want" and read as mocking. A0242 (drive-thru bag, neutral) replaced it. Check what the person in the clip DOES.
- **A 24 fps AI clip juddered through `fps=30000/1001`** (every fifth frame doubled). When the shot is short enough, cache the native
  frames and play one per film frame (1.25x): no doubled frames (`A0242x`).
- **Do not trim sentence pauses to 0.1-0.15 s.** Both reviewers flagged it as rushed; Dan's own pauses run 0.3-0.4 s with one soft
  in-breath. Where nothing was removed between two sentences, let the take run on (adjacent pieces, cut in the quiet). Where a restart
  was removed, cut in the dip beside the breath and keep the whole breath, never half of one.
- **Lower thirds:** the shared template shows its box for 11 frames before the first line whatever lead you give it (0.27 s is the
  lowest that still lands the line on its word). A part that wraps alone builds out of order ("Hit" before "Cheat Day Can"): make each
  line its own part. Off-the-cuff key points must distil, not repeat the words the captions are already showing.
- **Captions:** a cue cut by a join keeps its larger side; cues under 0.30 s merge with a neighbour or borrow the previous cue's last
  word; join tests allow 60 ms for Whisper's early starts (`captions.py`).
- **Per-take voice tone again.** Scripted was bright at 3.5/5.5 kHz and thin at 900 Hz; off the cuff was bright at 3.5 kHz and DULL at
  5.5 kHz. Fit `TAKE_EQ` per take on the voice wav (`audio_gate.py <wav> --video <master> --no-stamp --reference-rows-only`).
- **The banned-screen reference moved** (footage offload): point the plan at the library copy, see `deliver/README.md`,
  "Recovering the banned-screen reference". An absolute path, not one built from the version folder.
- **Every rebuild resets the review.** A new sha needs the watch pass judged and the body scan redone. Batch fixes, and send the SAME
  reviewer the new file (SendMessage) so it re-judges with its measurements in hand; a picture-identical sound-only rebuild took it
  3 minutes, a fresh reviewer takes 30. Never edit a shell script while it runs.

Gate rows that stay failing on this format (same as DS-36 / DS-43 / DS-44B, each measured by the reviewers): full-mix tone (the clip's
sound is in the window; the voice alone passes), hair_top on the panel (planned overlap), splice visibility on zoom cuts, and
captions:sync on the scripted file (the energy method reads the cue after the card; cue starts match delivered speech).
