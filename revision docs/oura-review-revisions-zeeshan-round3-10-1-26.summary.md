# Zeeshan, 2026-10-01: Video 4 (Oura Ring review) round 3 + blue lower-third PNG set

Doc: https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit (new section at the top, inserted through the Docs API; pre/post exports in `/Volumes/Extreme/_edit_work/revisions-20261001/doc_before.txt` / `doc_after.txt`, earlier text verified unchanged).
Delivered Oct 1 12:54 PM, folder `15kJXFS7...`. Work dir: `/Volumes/Extreme/_edit_work/revisions-20261001/`.

## What he sent
- `Video 4 Rev 2.mp4` (same name as last round, new file, md5 1576926a..., 1920x1080, 10.5 Mbps, 19:47.5), `v4_fixed.srt`, new AI frames Start/End 1, 3 and 4, and one generated AI clip at 6:47.

## Round 2 list against this cut
- Done: centering (face centre median +6 px, was +98), green screen drop-ins A, B, E, G, opening on the tight shot with a zoom out (Dan's own item), AI sleep clip moved to 0:24 with label, 0:41 plain camera, text fixes at 2:45, 2:54, 7:22, 10:54, 13:08, 13:46, ring punch-in hair at 4:03 (no sustained 0 px hold), subtitle names (0 wrong lines left).
- Color: skin tone now sits in one band for the whole video (face R-B 54 to 64; intro 61 to 65). 0:20 and 6:59, the two spots Dan flagged, now match their neighbours. Not itemized.
- Not done: the green chips. He converted only one (1:47) as a style sample and asked for approval and for the software used.
- Audio: -14.6 LUFS, true peak -0.8. No audio item (round 3).

## What I built
- 43 transparent 1920x1080 PNGs, one per lower third, in the locked Soft Blue Light lower third, named by timecode. Drive: kit folder > "5 Lower thirds for Video 4 (PNG)" https://drive.google.com/drive/folders/1ygUojZy5j7EqVlMyecjHHfvwaBsYBJ4J. Builder: `revisions-20261001/png/build_png.py`. Stills only, no video render (the Mac was at load 125 from other sessions).

## What I decided (overrule anything)
1. His 1:50 sample is not approved: centered thin text, no topic line, no blur. He gets our finished PNGs instead of building his own.
2. Topic lines on the non-key-point chips: "#1 TIMING", "WHOOP DISADVANTAGE #1", "DRAWBACK #1", "ALTERNATIVE #1", "WHY IT'S WORTH IT" and so on.
3. Small rewordings baked into the PNGs: 6:40 "A Tracker With A Screen Can Disrupt Your Sleep" (was "Tracker With Screen Can Become Cause Of Sleep Disruption"); 5:44 "The Oura Ring Is More Accurate And Comfortable On Your Index Finger Or Thumb"; 10:02 and 10:10 numbered #2 and #3 after the #1 at 9:54; 7:34 "Drawbacks Of The Oura Ring"; 19:14 "On AbsByAI, Your Workout And Nutrition Plan Adjust To Your Sleep"; 4:10 "Aura" corrected to "Oura".
4. No chip during the phone stretch 6:57 - 7:19 (a full-width lower third would cover the phone). This reverses last round's ask.
5. Upper-left lists, the AbsByAI.com pill and the end card: he recolors them navy himself.
6. AI frames: 4:15 end frame redo (man is still asleep, the story is the watch waking you); 14:09 jiu-jitsu approved; 15:37 Tesla approved.
7. Not itemized: wide shots from 4:28 to 11:14 and 12:20 to 15:14 are about 10 % brighter on the face than the rest. It reads as the lighting change you already accepted.

## AI CLIPS FLAGGED - watch before forwarding
- 6:47 - 6:48 (his new clip, a bearded man asleep with a lit watch): no artifact found, but it is 0.9 s long and unlabeled. Itemized. POSSIBLE nothing else.

## Needs Dan
- He asked for "a studio shot" to test settings on. I did not pick one. Send him one raw clip from the studio shoot, or tell me which and I will upload it.

## Paste-ready message

Hey Zeeshan, thanks for this one! Video 4 took a big step. I'm centered in every shot now, the color holds together through the whole video, and the opening on the tight shot with the zoom out is exactly what I wanted. Really nice work!

Round 3 notes are at the top of the same doc:
https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit

On your question about the templates: they aren't made in an editing app, they're generated with code, so there's nothing for you to install. To make this easy, I made every lower third in this video as a finished transparent PNG, named by timecode: https://drive.google.com/drive/folders/1ygUojZy5j7EqVlMyecjHHfvwaBsYBJ4J. Just swap each green chip for the PNG with the same timecode. They're full frame, so they drop in at 100% with no positioning.

On the AI frames: the jiu-jitsu one and the Tesla one are approved, go ahead and generate them. The Apple Watch one needs one more end frame, with him awake and looking at the watch. And the clip you added at 6:47 looks good, it just needs to stay up for about 4 seconds and get the AI label.

That's the whole list. Once those are in, this one is finished. I'll send you a studio clip separately so you can test your settings. Thanks!
