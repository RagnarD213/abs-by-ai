# Muhammad shorts, 2026-10-15: five revised cuts and one HD export (CONTENT, SFC)

Doc: https://docs.google.com/document/d/1MSGEToSR_tXDndUVFaFNF0oNQxwLHlB6mggTOPn0pP0/edit (anyone with the link can view)
Answers the October 2 notes (doc `1AR_8AeBzwhTuGelBlz1IRPcvKi5MHr-HT2kUTQ29o6s`, read live today; it carried your
10-02 edits). Sections are in the order of his 8:44 PM links. Work dir: `/Volumes/Extreme/_edit_work/revisions-20261015/muhammad/`.

**Verdict: all six FINALIZED, no items.** Every video's section is the credit paragraph and your status line. You pick
the lines (the five are 3.3 Mbps review copies, so I wrote READY FOR HQ EXPORT; Fat Millionaire is the 10.4 Mbps HD).

| # | Video | Round | File | Result |
|---|---|---|---|---|
| 1 | DS-11 Why You Must Weigh Yourself Daily | V3 | 1080x1920, 3.3 Mbps, -13.3 LUFS, -0.9 dBTP | all 4 items done |
| 2 | DS-13 The #1 Change I Made To Get Abs At 40 | V3 | same, -14.5 LUFS | all 4 items done |
| 3 | DS-10 3 Unexpected Ways Zepbound Helped Me | V3 | same, -14.5 LUFS | all 6 items done |
| 4 | DS-06 What Every Body Fat Percentage Looks Like | V4 | same, -13.1 LUFS, -0.6 dBTP | both items done |
| 5 | DS-05 Why Having Abs Beats Being A Fat Millionaire | HD | 1080x1920, 10.4 Mbps, -13.6 LUFS | frame-identical to approved V3 |
| 6 | DS-07 Top 3 Ways To Use AI To Get Abs | V3 | same, -13.9 LUFS | all 3 items done |

## How each item was checked
- **Jump cuts (every video):** `cuts.py` on every hard cut, then a look at the frame pair. Every cut between takes now
  measures a 1.20 / 0.83 background scale (a 20% punch-in), and every camera shot measures zero zoom inside the shot.
  Hair top in the tight shots stays 270 to 330 px against graphic bottoms near 250 (one line) and 278 (two lines);
  the closest calls (Zepbound 0:55, Top 3 0:39 and 0:43, Body Fat 0:27) were looked at full size and are clear.
- **Weigh:** key point starts 0:39.7 (asked 0:39.6, "and" begins 0:39.58). Scale clip 0:32.8 to 0:34.8 read at 6 fps:
  looking down, mouth closed to the last frame. Feet clip fills the frame.
- **#1 Change:** egg clip 0:20.15 full size, whole face below the graphic. Steak 0:28.0 to 0:31.3 at 4 fps: steak and
  asparagus on the plate to the last frame. Sardines left unlabeled (the item said leave it if it is real stock).
- **Zepbound:** opener now a moving clip; title 0:00 to 0:05.9 with the label under it, top man's face below both.
  "First" caption at 0:06.0; chips 0:12.3 to 0:15.1, bartender 0:15.1 to 0:17.7, alcohol graphic on to 0:17.5;
  "Zepbound" at 0:37.0 has the capital.
- **Body Fat:** the "ed" letters are gone at 0:36.6 (compared with V3 at the same frame); the AI label moved to the
  bottom right on both 0:34.7 clips, on his shorts, off the face.
- **Top 3:** opener has three panels, title in its own band, phone picture now the hoodie man lean and ripped, no
  AbsByAI.com, bottom panel is one clip ending at a visible trash can. Supplement clip 0:23.1 to 0:27.1 is one
  continuous shot.
- **Fat Millionaire HD:** subtracted from the approved V3 frame by frame: average difference 0.9 levels, largest pixel
  difference 32 of 255 (re-encode noise). Same 1201 frames. It is also 20 bytes off the "V3 (HD)" copy already filed on
  10-14 in `/Volumes/Extreme/_edit_work/muhammad-shorts-publish/ds05/`, so the setup can use either.

## FIRST 5 SECONDS
- Weigh: AI clip of the lean man stepping on the scale and smiling (your 10-02 approval).
- #1 Change: camera open kept. He says the title line ripped on camera at 40, which is the proof, and the round is closed.
- Zepbound: AI three-way split opener (your approved frames, now moving).
- Body Fat: camera open, as you asked for in round 3 ("The open is on me on camera now, which is what I wanted").
- Top 3: AI three-way split opener (your approved frames, now moving).

## For Dan's call (not in the doc)
1. **Punch-in size.** Every tight shot is 20% closer than the wide; the notes asked for 25 to 30%. It reads as a
   clean cut at full size (pair image `work/ds11_weigh_v3/cuts/cut_0154.jpg`), so I did not hold the videos for it.
2. **Body Fat 0:41.9 to 0:44.9:** he added extra punch-ins, two of them only 0.27 and 0.4 s long. They are on cuts and
   do not jump; watch once if quick punches bother you.
3. **Top 3, 0:23 to 0:27:** he puts the phone down, picks up the bottle and lowers it below the counter. The trash can
   is not in that shot (it is in the opener's bottom panel).
4. Body Fat: he swapped which shots are wide and which are tight against your list, and added a few switches. Every
   cut still changes size, which was the point.
5. The #1 Change file is named "HQ" but is the same 3.3 Mbps review size as the others.

## AI CLIPS FLAGGED - watch before forwarding
None. Read frame by frame and at speed: Zepbound opener (the water bottle comes up in his hand from below the panel
edge as he turns down the drink; reads as cause and effect), Top 3 opener and the 0:23 supplement clip. No artifact
passed the false-positive tests.

## Batch status (from the 10-13 count)
Ten of 22 were finished on 10-13; these five make **15 of 22**, and DS-05's HD is in. Still owed by the 16th: Jiu
Jitsu, Last Ten Pounds, Battle Ropes and Five Levels Of Pushups (10-05 notes), Getting Abs, 3 Most Important
Supplements and Top 5 Ab Exercises (10-13 notes), and HQ exports of today's five.

## Not verified
Nothing was listened to beyond loudness numbers (round 3+: level and peaks are in range, so no audio item). Captions were
spot-read on the contact sheets, not transcribed word for word, since no caption item was open.

## Update 2026-10-16: Dan reopened three (calibration pass 13)
Dan kept #1 Change, Zepbound and Body Fat finalized and reopened three. The doc was regenerated in place (same link);
he had not edited it.
- **Weigh Daily:** remove the between-takes water clip at 0:42.8 - 0:45.2, camera scene, that stretch tight so both cuts switch.
- **Fat Millionaire HD:** the fat before picture at 0:10.4 - 0:14.4 contradicted "abs are rarer". Replaced by our full
  screen rarity card, 0:10.4 - 0:16.9 (real studio-blue-201 with 2 of 100 dots, AI Dan on a yacht in a blazer with 8 of
  100; dots fill on "About 8%" at 11.42 and "Fewer than 2%" at 14.74), key point held to 0:16.9, captions moved to the
  bottom band. Closing graphic now THE LESSON / "Focus On Getting Abs First, Then Money Later". Kit folder 24.
- **Top 3 Ways:** the 0:06.4 after picture goes on an iPhone as its lock screen; closing graphic THE LESSON / "AI Is The
  Ultimate Tool For Getting Six-Pack Abs" (tight shots 30 px lower). Kit folder 25.
- Files: card ProRes 422 HQ `1Rw9pGSgCmdfJt58lrSrysZDCo3yEa8yF`, g10 `1v-LPsOhnmc93TEHdNPj74fwLiZQPbBc-`, g11
  `1k50N_gySnxXCgIz2ufhWVcGKR37ulbaf`. Build: `/Volumes/Extreme/_edit_work/revisions-20261015/muhammad/card/`
  (`rarity.template.htm`, `rarity.json`; AI image `rich_dan.png`, Codex gpt-6.1-sol high, 1 image).
- Batch: 12 of 22 finished.

## Paste-ready message to Muhammad

Hey Muhammad, got all six, thank you! The jump cuts are fixed on every one of them, and the AI openers on Zepbound and Top 3 Ways came out really good.

The #1 Change At 40, 3 Unexpected Ways Zepbound Helped Me and Body Fat Percentage are FINALIZED. Please send me the high quality exports of those three.

Weigh Yourself Daily, Fat Millionaire and Top 3 Ways each have a short list. On Fat Millionaire, the before picture at 0:10 was my miss, I approved it last round when it doesn't fit what I'm saying there. I made a full screen graphic to replace it, plus new closing graphics for Fat Millionaire and Top 3 Ways, and every file is linked in the notes: https://docs.google.com/document/d/1MSGEToSR_tXDndUVFaFNF0oNQxwLHlB6mggTOPn0pP0/edit

Once these are in, those three are finished too. Really appreciate the work on this batch!
