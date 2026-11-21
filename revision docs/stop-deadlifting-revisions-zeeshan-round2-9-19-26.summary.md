# STOP Deadlifting (Zeeshan "Video 3 Rev 1"), ROUND 2, 2026-09-19

Doc (pasted at the TOP, old text verified byte-identical by text export, 81,443 → 90,312 bytes):
https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit

Folder: https://drive.google.com/drive/folders/1KSgdrBmiX8REMqJ47tg7naAfTXc25bJn
File: "Video 3 Rev 1.mp4", 740 MB, 9:25.3 (was 9:30.6), 1920x1080 @ 29.97, 10.5 Mbps.
Work dir: `/Volumes/Extreme/_edit_work/revisions-20260919/`

**Round number: I am calling this round 2 of the deadlift video** (his own label is "Rev 1"). Confirm before forwarding.
The live Google Doc still matched our round-1 markdown byte for byte, so nothing was deleted by you; the whole
round-1 list is what he was working from.

## Round-1 items: 16 of 20 done

Done: all 14 KEY POINT graphics rebuilt with the exact wording · junk shot at 3:04 cut · 5:31 jump cut now a zoom cut ·
6:07-6:17 "footage of me doing these exercises" promise trimmed out of the line · 2010 archive deadlift clip installed
at 0:15.5 · two inserts added in the dead stretch · powerlifter physique clip added at 4:58 · skinny kid at 5:11 recast
as a lean Asian man with abs, labelled · T-bar row machine clip added at 6:23 · barbell row AI clip regenerated with a
plain shirt, no Gymshark · lat pulldown replaced with a controlled motion · leg press replaced with real reps ·
"AI Personal Traniner" → "AI Personal Trainer" · "www.AbsByAI.com" → "AbsByAI.com" · "Bar Bell Row" → "Barbell Row" ·
"Exercise #2: Lat Pulldowns" fixed · "Safest Way To Train Your Legs" deleted · no further cropping.

Not done or wrong: the 2:04.5 chip still runs only 4 s instead of through 2:17 · "Exercise #1:T-Bar Row" still has no
space after the colon · "Exercise#4:Rear Delt Fly" at 7:58.5 untouched · the colour fix overshot into the highlights
and the saturation · the music file he sent is not the track in the video.

## Measurements

**Colour.** Same frame, matched by audio correlation, in all four sources:

| | Y p1 (black point) | Y median | clipped highlights | overall sat | face R−B | face sat |
|---|---|---|---|---|---|---|
| raw camera C1487 | 15.4 | 52.0 | **0.00 %** | 23.5 % | +22.8 | 30.0 % |
| round 1 | 21.7 | 82.1 | 1.26 % | 33.7 % | +45.8 | 36.8 % |
| **Rev 1 (new)** | **4.2** | 69.0 | **4.24 %** | **45.5 %** | **+57.8** | **46.5 %** |
| reference ad (16:9) | 2.0 | 46.9 | 1.05 % | 25.8 % | +47.9 | 30.6 % |

Black point is now exactly on the reference. Second frame at 150 s reads the same (4.4 / 70.1 / 4.70 % / 44.3 %), so it
is not a one-frame artifact. The clipping is no longer only the fridge: his left shoulder and forearm are pinned at
255 with no skin texture. Proof built: `crops/clipping_3up.png` (clipped pixels flagged red, raw / round 1 / Rev 1) and
`colour_round1_vs_rev1_12s.mp4` (12 s moving side by side). Also `crops/three_up.png`.

**Audio.** −13.90 LUFS, true peak −1.00 dBTP, one mic (L/R +0.998), EDT 80 ms, 0 clipped samples, no dead air.
Residual against round 1's mix is −24 dB, i.e. the same mix re-encoded. Round ≥ 2, so not itemised (skill rule 22).
The gate's tone/floor rows grade through the music bed and were not quoted.

**Framing.** Delivery-gate check: hair top median 0 px, p95 14, head height median 401 px. Round 1 read median 0,
p95 15, head 401. He did not crop any tighter. Nothing recoverable, same as last round (skill lessons 57-58).

**Music: the track he named is measurably not in this video.** Envelope correlation of
`knox-gym-energy-gym-thunder-538872.mp3` against four 80 s windows of the cut: r = 0.05 to 0.14, offsets inconsistent,
both full-band and bass-band. Sensitivity control: the same track mixed under a raw camera file at −20 dB returns
r = +0.795 at the exact correct offset, at −26 dB +0.620, at −32 dB +0.443, always the right offset. So a ducked bed
IS detectable by this method and this one is not that track. A bed is definitely present: gap floor p5 −37 to −39 dB
against the raw's −56 dB. Positive control on the arms video's live round: +0.825 band / +0.941 full.

**Subtitles.** `Video 3 Subtitle.srt` is md5-identical to the one he sent on 09-17 (`7c71114d…`). It still contains the
sentence he cut, and everything after 6:09 runs ~5 s late because the cut is 5.3 s shorter.

## AI CLIPS FLAGGED: watch before forwarding

- **4:58 - 5:05, the powerlifter deadlift: CONFIRMED, tier A.** The barbell leaves his hands at the top of the lift.
  Two-frame identity test: at 299.0 s the bar is clearly in both hands with plates on both ends; at 300.5 s and
  302.0 s he is standing upright with **empty hands and no bar between them**, the two plate stacks sitting on the
  floor unconnected. It happens twice in a 7.3 s clip and roughly 4 of those seconds are the broken state, so it reads
  at playback speed, not just in stills. Not an occlusion and not a light. Frames saved as `crops/pl_299.0.png`,
  `crops/pl_300.5.png`, `crops/pl_302.0.png`.
- 5:10.5 - 5:16, the lean man: clean. Hands, face and the machine he touches all hold up at full resolution.
- 6:28 - 6:32.5, the barbell row: clean, and the Gymshark logo is gone. Same shot as last round, plain shirt now.

None of these are your own assets; all three are his generations for this video.

## For Dan

- **The gym clip at 3:40.5 - 3:54 is a woman.** Confirmed at full resolution (hair in a bun, bra strap, feminine
  shoulders), 13.5 s of the back of her head. The item asks him to recast it as a man 30-50. Say the word if you would
  rather live with it.
- **The T-bar row clip at 6:23 has "GYMAHOLIC" printed across the shirt**, legible for the whole shot. I wrote it as
  the same item as the Gymshark shirt, with your logos standing rule. It is stock, not AI, so the fix is a different
  clip or a tighter crop, not a regeneration. Your rule says company *names* are fine and *logos* are not, and this one
  is a styled wordmark, so it is a judgement call. Delete the item if you read it the other way.
- The stock exercise models are still all men in their early twenties. Same call as last round: I did not itemise it.
- The back pain clip he substituted for injury footage is the right idea and I credited it. It is one shot for 8.7 s
  with a slow zoom out, which is long, but you told me not to itemise how long a picture holds.

## Message to Zeeshan (paste-ready)

Hey Zeeshan, this is a big jump, nice work.

Every one of the KEY POINT graphics is rebuilt and the wording is exactly what I asked for, which was the thing I cared
most about. The four minutes of nothing is broken up, the junk shot is gone, the jump cut is a zoom cut now, and you
cut the promise out of that line at 6:09 so I am not telling people they are about to see footage of me any more. The
archive clip is in, the barbell row is regenerated without the logo, and there is a real T-bar row and a real leg press
on screen. Round 2 is at the top of the same doc:
https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit

Three big things.

The AI powerlifter clip at 4:58 falls apart. He is bent over with the bar in his hands and it looks completely real,
and then every time he stands up the barbell is gone out of his hands and the plates are sitting on the floor either
side of him with nothing between them. He is lifting nothing, twice, in seven seconds. The casting is perfect so I want
to keep the idea, but that clip needs regenerating until the bar stays in his hands, or swapping for real footage.

Colour, and half of this is good news. The black point is fixed, it was at 22 and it is at 4 now, right where I wanted
it. But the top end went the other way. The camera file has nothing blown out, the last version had 1.3 percent of the
frame blown, this one has 4.2 percent, and it is on me now, not just the fridge. My left shoulder and my forearm are
pure white with no skin left in them. The saturation also came up a lot and it has changed my skin tone, which I told
you last time was already right. Pull the highlights back and put the saturation back where it was. I am sending you
stills with the blown-out pixels marked in red and a side by side so you can see it.

At 7:25 the chip over the leg press section says "Exercise #4: Rear Delt Fly". It should say "Exercise #3: Leg
Presses". That one would confuse somebody following along.

The rest is small stuff in the doc.

Two housekeeping things. The track you sent is clean and I have cleared it, but it genuinely is not what is playing in
this video. I checked it against the mix across four different stretches and it does not line up anywhere, and I tested
my method by burying that same track under a camera file to make sure it was not just failing because the music is
ducked. So send me the name of the actual track. And the .srt in the folder is the old one, it still has the sentence
you cut in it and it runs five seconds late after 6:09, so I need a fresh one off this cut.

Thanks!
