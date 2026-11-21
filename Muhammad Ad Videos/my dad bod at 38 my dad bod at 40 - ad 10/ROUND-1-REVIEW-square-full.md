# Ad 10 square full (1x1), round 1 independent review

File reviewed: `my dad bod at 38 my dad bod at 40 | claude | 1x1 | ad 10.mp4`
sha256 `ec45e38adf01186925a3bccd1d9c910e11c353389a5ad5271b64fd51f4c3823d`, 1080x1080, 5,443 frames, 29.97 fps, 181.615 s.
Reviewer: independent, Opus 5.5. I did not read any notes-*.md, ROUND-*-EDITOR.md or recipe-square file. I read the
plan (`Handoffs/handoff-20261002-ad10-square-round2-full-builds.md`, `AS-06-ad10-square.md`), `00-RULES.md`,
`VIDEO-RULES.md`, `framing-motion.md`, SKILL.md [S1], and the build's `sq/sq_copy.json` (the per-picture fill/card reasons).

## VERDICT: DOES NOT SHIP

One blocker, small and local: a 0.63 s freeze frame on a moving clip near the end. Everything else is either clean
or a nit. Fix that one beat, re-check it on the delivered file, and this ships.

## Findings

1. **2:52.20 to 2:52.84 (frames 5161 to 5179): the AI beach runner freezes mid-stride for 19 frames (0.63 s), then
   hard-cuts to the phone demo.** Frame-to-frame difference in the square is 0.0 to 0.1 for every frame from 5161 to
   5179 (a true freeze, not slow motion), while the approved vertical keeps the clip moving through 5169 and then plays
   its in-card transition at 5170. The square also cuts to the phone 10 frames later than the vertical (5180 vs 5170),
   so the frozen runner sits under the start of "So generate your future self image". `sq_copy.json` shows
   `ai_beach_end hold_from 83` (5079 + 83 = 5162), so the hold starts 8 frames before the vertical's own transition
   point. A still runner on a moving shot reads as a stall in a paid ad. Fix: cut to the phone at 5170 (the vertical's
   cut), or end the hold no earlier than the clip's last usable moving frame, and prove frames 5155 to 5185 move.
   **Severity: blocker.**

2. **1:06.83 to 1:07.17 (frames 2003 to 2012): the daughter photo's slow push stops for 10 frames before the flash.**
   The vertical has an in-card flash to Dan at 2008 here (Muhammad's frame); the square holds the clean photo instead
   (`daughter_event hold_from 52`). It is a still photo, so the stop is hard to see. **Severity: nit.**

3. **1:30.22 to 1:33.19 (frames 2704 to 2793), AI pool goal image, full frame: the picture only updates on every
   other frame** (difference alternates about 2.3 / 0.0 for 90 frames; the vertical changes on every frame). The push
   is about 3.8 % over 3 s, so the stepping is roughly half a pixel per step and probably invisible at speed; I could
   not confirm by real-time playback. **Severity: nit.**

4. **Real-picture label wording differs inside one video.** The full-bleed photos (0:08.1 to 0:10.8, 0:27.0 to 0:30.0,
   1:46.2 to 1:48.5) carry "Real picture of me. Not AI-generated." The boxed pictures and phone screens (0:00 to 0:03.1,
   0:09.1 to 0:10.8, 1:03.1 to 1:07.2, 2:01.8 to 2:05.6, 2:52.8 to 2:56.7) carry "Real picture of me - not
   AI-generated", which is also what the approved vertical uses on every photo. The standing label is the second form.
   Both are clear of his face and abs. **Severity: nit** (Dan saw the 0:08 to 0:11 photos on the look page).

5. **0:23.72 to 0:23.79 (frames 711 to 713), tight shot: hair top about 12 to 15 px below the frame edge.** Not cut, but
   under the 20 px bound for 3 frames as he rises. The gate samples every 0.25 s and read min 21 px, so it missed this.
   Dense check on all 3,590 talking frames: median 42 px, 1st percentile 27 px, only these 3 frames under 18 px.
   **Severity: nit.**

6. **Video bitrate 6.64 Mbps** against the shared square rules' 8 to 12 Mbps
   (`handoff-20260911-square-ads-00-shared-rules.md` line 25). Full-size crops of the blue fields and the pool image
   show no banding or blocking. **Severity: nit.**

7. **Three picture changes land one frame later than the vertical:** 1:05.07 (frame 1950 vs 1951), 2:02.79 (3680 vs
   3681), 2:47.27 (5013 vs 5014). Cause: the square holds the clean photo one frame where Muhammad's card already showed
   the next picture (`hold_from`). This is 33 ms, no next-shot leak, no viewer impact. **Severity: nit (informational).**

8. **Opener, 0:00 to 0:03.1: shirtless before photo with his stomach in shot, in the first 30 s.** Dan's 2026-10-04
   rule (no belly emphasis, above all in the first 30 s) landed after the look lock. Measured: the photo is shown
   whole in a card, there is no pinch, and the push's fixed point is at (535, 59), on his head, not the belly. The same
   photo is in the approved vertical and the live 16:9 ad. `sq_copy.json` gives the card reason as "the stomach is the
   point of the before picture". **Severity: Dan's call, not a build defect.**

Inherited from the approved vertical and not counted against the square: "40" at 0:22.9 is not captioned (the
"HOW I DID IT" lower third starts there), and the photo beats carry no captions.

## What I checked, and how

- **Container:** ffprobe on the real file: 1080x1080 H.264 High yuv420p tagged BT.709 tv range, 30000/1001, 5,443
  frames, 181.615 s, AAC LC 48 kHz stereo 317 kbps. Duration and frame count equal the vertical's (5,443, 181.615 s).
- **Audio:** `-map 0:a -c copy -f md5` gives `f552a844696ce1fbb6d111ad42cadafa` for both the square and the vertical:
  byte-identical. ebur128 on the square: -13.5 LUFS integrated, LRA 2.9 LU, true peak -1.0 dBTP (at the -1.0 limit,
  not over). Because the stream is the approved vertical's, there are no new audio seams. I could not listen by ear.
- **Stamps:** `.deliver_gate.json` gate 2.4.0 (current `GATE_VERSION` in `_shared/deliver/gate.py`), format ad1x1,
  PASS, sha256 matches the file. `.audio_gate.json` gate 2.0.0 (current in `audio_gate.py`), reference-verbatim mode,
  PASS, sha256 matches. Two info rows (tone max 2.93, HF swirl) are flagged false but marked "not ours to gate"
  (editor's mix, untouched).
- **Every cut:** per-frame difference on a 360x360 decode of both files; 75 picture changes shared with the vertical
  at the same frame, 3 one frame late (finding 7), 2 vertical in-card transitions replaced by holds (findings 1 and 2),
  2 square-only punch-ins on pause splices (0:15.90, 0:37.85) with eased pull-outs at 0:17.2 to 0:17.8 and 0:39.2 to
  0:39.8 (about 17 % over 0.6 s, under the list cards). I pulled n-1, n, n+1 at full 1080 for all 80 cuts, cards,
  flashes and graphics, plus first frame and last frame. No naked jump cut (every same-scene change is a framing step
  or a flash), no next-shot leak, no thin edge lines, no wrong label, no double label, no black frame (minimum frame
  mean luma 50 on 0 to 255).
- **Freezes:** scanned every frame for runs of 6 or more near-identical frames while the vertical moves: 2003 to 2012
  (finding 2), 3669 to 3680 (a static phone screen, fine), 5162 to 5179 (finding 1).
- **Camera on the talking head** (3,590 kitchen frames, 3,536 consecutive pairs, background shift by phase correlation
  on both side strips, in 1080 px): no isolated one-frame sideways pop anywhere (none over 1.5 px with still
  neighbours); largest per-frame shift 4.8 px; smoothed pan speed p90 29.5 px/s, p99 80 px/s, peak 117 px/s (brief
  follows at 0:14.3, 0:35.2, 1:25.4); moving on 35 % of talking frames; total travel about 1,390 px. Landings: head
  (hair centroid) at the first frame after 40 talking cuts sits median 9 px, worst 33 px from centre. This matches
  Dan's calmer "land on him, then hold".
- **Framing:** hair never touches the frame edge on talking frames (finding 5 is the tightest); full-bleed photos keep
  hair inside the frame (tightest about 16 px on the park close-up at 0:28.6). Cards: every boxed clip or photo has a
  written reason in `sq_copy.json` (cut head at the source edge, phone screens, flag arms, label with no clear spot);
  16:9 clip cards keep full source height (about 1.78:1 on the delivered frame).
- **Labels:** every AI image carries AI-GENERATED, every real photo of Dan carries a real-picture label, one label per
  picture, none on his face or abs (checked on every labelled cut frame). Before and after in both app demos are Dan
  (deckchair photo to the AI pool goal). No side-by-side before/after screen, no "Meet the new you", no email screen.
  No em dash on screen; labels use a hyphen.
- **Captions, first 30 s, word for word against the audio:** read every 5th frame from 0:03.2 to 0:30. Burned text:
  "I was eating healthy / working out four times / a week and doing my / absolute best / same business same kid /
  same stress about two / years apart / So / how did I get my abs / back at / with abs". This matches the speech; the
  photo beats (0:00 to 0:03, 0:08 to 0:11, 0:27 to 0:30) and the list card carry the rest by design, as in the
  vertical. Against my own audio energy onsets ("I" at 3.32 s, "working" 4.72 s, "absolute" 7.32 s) the highlight
  lands within about one sampling step (0.17 s). Graphics read cleanly: "What Didn't Change", "HOW I DID IT / I Used
  AI To Get REAL ABS", "In This Video", "THE TRUTH / Life Gets Better For You AND Your Kids When You Get In Shape",
  "MY LOCK SCREEN", "How The Plan Is Built", "YOUR WORKOUTS / Built Around Your INJURIES", "Snap A Photo Of Your
  Plate", "BAD WEEK? / The Plan ADJUSTS.", end CTA "Get A FREE AI Image Of Yourself / With Abs". No garbled text.
- **Would it embarrass Dan as a paid ad:** not after finding 1 is fixed. The rest of the film looks like the approved
  vertical in the approved Soft Blue Light square layout, with a calm camera.

## What I could not verify

- I could not watch at real-time speed or listen; motion and audio judgements come from frame measurements and the
  byte-identical audio stream. Findings 1 and 3 should be confirmed by eye on playback.
- I did not see Dan's look page, so I cannot say which square-only choices (photo chip wording, pull-outs) he saw.
- The 59 s square cutdown was out of scope for this review.
