# Independent review brief: Invest In Your Health LFC R4 (one reviewer per film)

You review ONE delivered film against the plan and the standing rules. You never see the editor's notes. Write
`/Volumes/Extreme/_edit_work/ro20/round4/{V}/ROUND-4-REVIEW.md` ending in `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`,
with every defect as `time (mm:ss.ss) | what | why it matters | suggested fix`.

## The film
- File: `/Volumes/Extreme/_edit_work/ro20/round4/{V}/MASTER.mp4` (1920x1080, 29.97 fps). Check its sha256 and write it at the top.
- Its part layout (which stretch of the one long cut, or which pickup, sits where): `round4/{V}/layout.json`.
- Subtitles (uploaded sidecar, not burned in): `round4/{V}/{NAME}.srt`. Chapters: `round4/{V}/{NAME}.chapters.txt`.
- Delivery-gate plan (labels, joins, graphics): `round4/{V}/plan.json`. Watch-pass sheets and strips: `round4/{V}/watch/`.

## What the film is
One 54-minute kitchen roll (C1511), edited and approved by Dan in rounds 1 to 3b, was split into three videos joined by
four short "pickup" lines Dan recorded on the studio lav (10/15 shoot). Each pickup plays over a full-screen card with a
picture window. Video 1 = "Why You Should Invest More In Your Health" (RO-20). Video 2 = "What To Cut To Afford Getting
In Shape" (RO-20B). Video 3 = "What To Buy For Your Health At Every Income Level" (RO-20C). The three videos as ranges:
`/Volumes/Extreme/_edit_work/ro20/round2-plan/videos.json`. Dan's approvals, word for word: `round3-plan/decisions.json`,
`round3b/decisions.json`. Approved review clips to compare against (independent components):
`round3/first-minute-3b/` (video 2 first minute, video 3 first minute, video 1 ending), `round3/pickups/P1-P4.mp4`.

## Check, on the exact file
1. **Every join** listed in layout.json: watch native consecutive frames (extract with ffmpeg `-ss` before `-i` plus a
   decode lead-in, never OpenCV random seek) and the moving context several words either side. Pickup entries and exits
   especially: picture, voice level and tone (does the pickup voice sit with the kitchen voice?), no clipped word, no
   gap or doubled word, music bed continuous. Compare with the approved round 3b clips at the same joins.
2. **The words around every join** against the plan: nothing that points at material now in another video ("in a
   minute", "later in this video", "like I said earlier") unless it is true inside this video. Read the SRT around joins.
3. **Framing**: hair-anchored near/far sizes only, no naked jump cut (same framing both sides, he jumps), no one-frame
   flash, no camera movement added in 16:9. The camera clipped the top of his hair on most of this roll (known, unfixable).
4. **Labels**: every AI clip carries AI-GENERATED; every real photo of Dan carries the real-photo chip; no label over his
   face or abs. Real moving footage of Dan carries no label.
5. **AI clips, the three questions, one answer per clip** at playback speed: (1) does everything obey cause and effect;
   (2) with the sound off, would a stranger say what the clip shows; (3) does it show the line he is saying, and if it is
   a joke, does it land in one viewing.
6. **B-roll**: every B-roll clip colour corrected to sit with the presenter (none visibly darker or off-colour); no clip of
   Dan just standing around, looking at a phone, or between-takes junk; a cutaway shows the thing he names.
7. **Freezes**: read every `scan.frozen` entry in `round4/{V}/logs/watch_pass.json` (including inside_declared) and give
   each one a disposition from the actual pixels.
8. **Audio**: the whole film for level jumps, clicks at joins, room-tone dips, the music bed (quiet, never over words).
9. **Opening and ending**: the first 5 seconds, and the last 10 (does it end cleanly, nothing cut off).
10. **Graphics**: title capitalization, no typos, nothing running off-screen, nothing covering his face.

Write what you actually watched (which stretches at full speed, which joins frame by frame). A sampled check is never
called a full watch. Expect DOES NOT SHIP the first time if anything above fails.
