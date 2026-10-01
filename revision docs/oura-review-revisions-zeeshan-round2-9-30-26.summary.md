# Zeeshan, 2026-09-30: Video 4 (Oura Ring review) round 2 + green screen drop-ins

Doc: https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit (new section at the top; pre/post-paste exports in `/Volumes/Extreme/_edit_work/revisions-20260930/doc_before.txt` / `doc_after.txt`, old text verified byte-identical)
Delivered Sep 30 11:54 AM (two folders). Work dir: `/Volumes/Extreme/_edit_work/revisions-20260930/`.

## What he sent
- Folder `1Ai6E5pW...`: four AI start/end frame pairs (Start/End 1-4) for the round-1 AI items at 4:15, 6:38, 14:10, 15:38.
- Folder `15kJXFS7...`: `Video 4 Rev 2.mp4` (1920x1080, 10.5 Mbps, 19:47.5), `v4.srt` (new), plus the round-1 `Video 4.mp4`, `Video 4 Srt.srt` and music (same files as round 1) and a copy of the frames.

## Measurements
- Audio: identical to round 1 except 0.83 s removed at 7:40 (the double start). Envelope match r 0.92-0.99 in every 20 s window. No audio item.
- Color (face patch R-B, reference 2:20-3:58 = +55 to +63): 0:30 +68.7, 5:00 +62.8, 10:00 +69.0, 16:40 +55.2. Much more even than round 1 (0:30 was +49.9, 5:00 +44.9), slightly past the reference on some shots. Item written as "a little too orange in places".
- Centering (gate framing check): face centre median +98 px right of centre, 83 % of samples more than 60 px right (round 1: +91). Not fixed. Item repeated.
- Hair top: median 63 px, p5 50. Only sustained 0 px stretch is the 4:03-4:06 ring punch-in. Item written.
- .srt: missing words and tool note fixed; 24 lines still say oral ring / or ring / Ora / Aura / "whooping Apple watch".

## Green screen drop-ins (his request)
Built and uploaded to the kit folder `1 Drop-in files for Video 4` (https://drive.google.com/drive/folders/1ispvFqk9CAv-WqZ_hBgVed3cedRWBLGJ), ProRes 422 HQ on pure #00FF00:
- `A_intro-card_GREEN-SCREEN_00-00-00-00.mov`, `B_not-sponsored-lower-third_GREEN-SCREEN_00-00-17-01.mov`, `E_oura-app-phone_GREEN-SCREEN_starts-12512.mov`, and new `G_key-point-lower-third_1-19_GREEN-SCREEN_starts-2384.mov` (1:19 blue lower third Dan asked for in round 1; still olive in Rev 2).
- Graphics are opaque in the green versions (the 91 % card and 54 % glass would key unevenly). Door-frame plates on A and E were re-graded from Rev 1 to his Rev 2 look (per-channel fit, residual 2-4 levels on the wide shot). Keyed-over-shifted-footage simulation: `green/sim.jpg`, no seam. Builder: `green/build_green.py`.

## Decisions for Dan (the doc already states these as your calls; overrule any)
1. AI frames 4:15 (Apple Watch wakes me): start approved, end frame redo (room, bedding, light and man all change; cartoon light rays).
2. AI frames 6:38 (watch notifications in the dark): approved, generate.
3. AI frames 14:10 (jiu-jitsu, strap on bicep): approved except the end frame, where the top guy looks into the camera.
4. AI frames 15:38 (late-night driving): redo both. It is an old analog-gauge sports car (you drive a Tesla Model 3 Performance), and the end frame has "HIGH SPEED POV" printed on the dash, a GoPro and a helmeted man in the mirror.
5. Not itemized: he laid the verdict card over the unshifted shot at a smaller size; it reads fine and does not touch you.

## AI CLIPS FLAGGED - watch before forwarding
- None in the cut beyond our own AI sleep clip (it is at 0:41 instead of 0:24, unlabeled; itemized). The four frame pairs above are stills, not clips.

## Paste-ready message

Hey Zeeshan, thanks for these! And no problem on the green screen, you're right that the drop-ins had my old color baked in. I added green screen versions of all of them to the same folder, plus one new one for the 1:19 key point: https://drive.google.com/drive/folders/1ispvFqk9CAv-WqZ_hBgVed3cedRWBLGJ. Key out the green, and for the intro card and the phone, move my shot right by 280 px like before. The door frame strip on the left edge is already matched to your new color.

Video 4 is really coming together! Almost all of round 1 is in, the color is way more even now, and the sleep score graphic and the verdict card look great. Round 2 notes are at the top of the same doc:
https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit

Three big things. The AI clip of me in bed ended up at 0:41 instead of 0:24, so it just needs to move and get its AI label. I'm still sitting about 100 px right of center in most shots, so the crop needs to move over. And on your AI frames: the watch notification one is approved, go ahead and generate it. The jiu-jitsu one and the Apple Watch one each need a new end frame, and the driving one needs to be redone inside a Tesla Model 3, since that's what I drive. Send me those new frames before you generate.

The rest is small text fixes and one more pass on the names in the .srt. That's the whole list. Thanks!
