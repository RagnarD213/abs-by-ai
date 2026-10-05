# Ad 10 square full (1x1), round 2 independent review

File reviewed: `my dad bod at 38 my dad bod at 40 | claude | 1x1 | ad 10.mp4`
sha256 `f2c98162b8aa3ced8abeeeacf6008fa22bd856e80d17912aa626ac1e18ca22eb`, 1080x1080, 5,443 frames, 29.97 fps, 181.615 s.
Reviewer: independent, Opus 5.5. I did not read any notes-*.md, ROUND-*-EDITOR.md or anything under recipe-square. I read
`VIDEO-RULES.md`, `framing-motion.md`, `00-RULES.md`, `AS-06-ad10-square.md`, the round 2 plan
(`Handoffs/handoff-20261002-ad10-square-round2-full-builds.md`), SKILL.md [A10] and [S1], and `ROUND-1-REVIEW-square-full.md`.
Every finding below comes from frames I decoded (BT.709, full 1080) or numbers I measured on the delivered file.

## VERDICT: SHIP

The round 1 blocker (frozen beach runner before the phone) is fixed, and so are the AI pool picture's every-other-frame
push and the low bitrate. No blockers. One should-fix (a fast 0.23 s camera slide at 0:33.0 where the approved vertical
holds still) and nits, most carried over from round 1 unchanged. The film reads as the approved vertical in the
approved Soft Blue Light square layout, with a calmer camera. It would not embarrass Dan as a paid ad.

## Findings

1. **0:33.03 to 0:33.27 (frames 990 to 997): the talking-head crop slides 34 px left in 7 frames, then stops dead at
   frame 998.** Right after the punch-in cut at 990 Dan leans to frame right; the crop follows at a constant
   4.4 to 4.8 px per frame (about 140 px/s) from the first frame after the cut and stops in one frame (998: +0.4 px).
   Measured two ways: phase correlation on both side strips agrees (left -5.0, right -3.8 px/frame), and the door edge
   at row 100 to 200 walks x 89 to 55 over 990 to 997 and sits at 55 to 58 after. The approved vertical holds still on
   the same frames (its top band moves under 0.5 px per frame from 992 to 1010). This is the fastest camera move in the
   square (the next fastest follows run about 2 px/frame), it is not eased, and it lands exactly where Dan asked for a
   calmer camera. It is short and starts on a cut, so it may read only as a small settle. **Severity: should fix**
   (not blocking; fix if the square is re-rendered for any other reason, for example by widening the hold band on
   this one segment so the crop stays put as the vertical does).

2. **Round 1 #1 (freeze before the phone card): FIXED.** The beach runner now moves through frame 5169 (frame
   differences 1.4 to 2.7, with the clip's own 24 fps repeat every fifth frame, identical in the vertical) and hard-cuts
   to the phone at 5170 = 2:52.506, the vertical's own cut. No freeze anywhere in 5150 to 5190.

3. **Round 1 #3 (AI pool picture stepping): FIXED.** 1:30.22 to 1:33.19 (2704 to 2793): the push now changes on every
   frame (difference 1.1 to 1.2 every frame, no zero frames).

4. **Round 1 #6 (bitrate): FIXED.** Video stream now 10.26 Mbps (was 6.64).

5. **Round 1 #2, unchanged: 1:06.83 to 1:07.13 (frames 2003 to 2012), the daughter photo's push stops for 10 frames**
   (difference exactly 0.0) before the photo brightens into the flash at 2013. The vertical has its in-card flash to
   Dan here; the square holds the clean photo (an intended difference). A still photo stopping for 0.33 s is hard to
   see. **Severity: nit.**

6. **Round 1 #4, unchanged: two wordings of the real-picture label.** Full-bleed photos (0:08.1 to 0:10.8, 0:27.0 to
   0:30.0, 1:47.2 to 1:48.5) say "Real picture of me. Not AI-generated." Carded photos and phone screens (0:00 to
   0:03.1, 0:09.1 to 0:10.8, 1:03.1 to 1:07.2, 2:01.8 to 2:05.6, 2:52.5 to 2:56.7) say "Real picture of me - not
   AI-generated". All are clear of his face and abs. **Severity: nit.**

7. **Round 1 #5, unchanged: 0:23.66 to 0:23.82 (frames 709 to 714), tight shot, hair top 14 to 22 px below the frame
   edge** as he rises (full-res measurement: 709 22, 710 18, 711 15, 712 14, 713 14, 714 17, 715 21 px). Not cut;
   under the 20 px bound for 5 frames. Dense check on all 3,590 talking frames: median 42 px, 1st percentile 27 px,
   nothing else under 24 px. The park close-up photo (0:08.8 to 0:09.1 and 0:28.6 to 0:30.0) keeps about 15 px over
   his hair. **Severity: nit.**

8. **Round 1 #7, unchanged: three picture changes one frame after the vertical's:** 1:05.10 (1951 vs 1950), 2:02.82
   (3681 vs 3680), 2:47.30 (5014 vs 5013). The square holds the previous clean picture one frame (intended "hold the
   last clean frame"). 33 ms, no next-shot leak. **Severity: nit (informational).**

9. **2:31.58 to 2:35.0 (4543 onward), plate stock full frame: white caption words sit over a white plate.** "and it
   logs your", "and macros" read only thanks to the drop shadow; the lit word is legible. The vertical shows the same
   words over a dark field, and the caption "two dinners." riding 2 frames onto the clip at 4543 to 4544 is the same
   in the vertical. Full-frame fill of this clip is the approved square look. **Severity: nit.**

10. **Round 1 #8, unchanged: opener 0:00 to 0:03.1 is the shirtless deckchair before photo with his stomach in shot,
    inside the first 30 s.** Shown whole in a card, no pinch, no push centred on the belly; the same photo is in the
    approved vertical and the live 16:9. Dan's 2026-10-04 belly rule postdates the 10-03 look lock. **Severity: Dan's
    call, not a build defect.**

Inherited from the approved vertical, not counted: "40" at 0:22.9 is not captioned (the HOW I DID IT lower third
starts there), photo beats carry no captions.

## What I checked, and how

- **Container (ffprobe on the real file):** H.264 High, yuv420p, BT.709 tagged tv range, 1080x1080, 30000/1001,
  5,443 frames, 181.614767 s, video 10.26 Mbps; AAC LC 48 kHz stereo 317 kbps, 181.614771 s. Duration and frame
  count equal the vertical's.
- **Audio:** `-map 0:a -c copy -f md5` gives `f552a844696ce1fbb6d111ad42cadafa` for the square, the approved vertical
  and the square's REVIEW 540p copy: byte-identical. ebur128 on the square: -13.5 LUFS integrated, LRA 2.9 LU, true
  peak -1.0 dBTP (at the limit, not over). Because the stream is the approved vertical's, there are no new seams. I
  could not listen by ear.
- **Stamps:** `.deliver_gate.json` gate 2.4.0 (current `GATE_VERSION` in `_shared/deliver/gate.py`), format ad1x1,
  PASS, sha256 equals the file. `.audio_gate.json` gate 2.0.0 (current in `audio_gate.py`), mode reference-verbatim,
  PASS, sha256 equals the file; verbatim level 0.00 dB against his mix.
- **Structure:** per-frame differences of the whole square (360 px decode) and the whole vertical (270x480). Every
  picture change matches the vertical's frame except the intended differences: the in-card transitions at 2008 and
  5170 to 5180 replaced by a held photo and a direct cut, the three one-frame holds (finding 8), and the square-only
  closer zoom steps at 0:15.92 and 0:37.87 with smoothly eased pull-outs at 0:17.2 to 0:17.8 and 0:39.2 to 0:39.8
  (difference ramps 1.4 to 5.4 and back, no steps).
- **Frames at full 1080:** n-1, n, n+1 at every cut, card in and out and flash (116 change points), every 30th frame
  (182 frames, all 3 minutes), first frame (opener card) and last frame (end CTA), the title build-in 59.1 to 60.1 s,
  all AI and stock cards. No naked jump cut (every talking-to-talking cut is a framing step or a flash), no one-frame
  glitch at any card edge, no black frame (lowest frame mean luma 44 of 255), no garbled text, no em dash on screen.
  A few talking segments put the white edge of the wall poster as a 4 to 8 px sliver on the left frame edge (for
  example 1:38); it is real background, not a render line.
- **Freezes:** every run of 5 or more identical frames: 1:01 and 1:41 are the text title cards (static by design),
  1:06.8 is finding 5, 2:53.7 is a static phone screen. Nothing else.
- **Camera on the talking head (3,590 frames):** background shift by phase correlation on both side strips, in 1080 px:
  no isolated one-frame sideways pop (one 2 to 4 px step on 2203 to 2204, the last frames before a cut, invisible);
  smoothed speed p50 3 px/s, p90 28 px/s, p99 57 px/s, peak 108 px/s smoothed (finding 1 is the peak); moving on 31 %
  of talking frames; total travel about 1,350 px. Landings: head centre at the first frame of 38 talking cuts sits
  median 10 px, worst 32 px from centre. Head off centre over all talking frames: median 20 px, p95 57 px.
- **Framing:** dense hair top on every talking frame (finding 7 is the tightest); full-bleed photos keep hair inside
  the frame. Cards keep the 16:9 clips at full source height.
- **Labels:** every AI image or clip carries one AI-GENERATED chip (the editor's burned chip on his AI clips, ours on
  the pool goal picture and the lock-screen phone), every real photo of Dan one real-picture label, none on his face
  or abs. Both app demos go from Dan's deckchair photo to the AI pool picture of Dan (same person). No side-by-side
  before/after screen, no "Meet the new you", no email screen.
- **Captions, 0:00 to 0:31, every 4th frame read against the editor's transcript:** "I was eating healthy / working out
  four times / a week and doing my / absolute best / same business same kid / same stress about two / years apart /
  So / how did I get my abs / back at / with abs / Listen," with the list card (I didn't get younger, I didn't quit my
  job, I didn't move into a gym) and HOW I DID IT / I Used AI To Get REAL ABS carrying the rest. Matches the speech
  word for word; the lit word advances in order. Gate row captions:sync reads 252/252 words, median 1.5 ms.
- **Would it embarrass Dan as a paid ad:** no.

## What I could not verify

- I could not watch at real-time speed or listen; motion and audio judgements come from frame measurements and the
  byte-identical audio stream. Finding 1 should be confirmed by eye at 0:32.5 to 0:34.
- I did not see Dan's look page, so I cannot say which square-only choices (label wording, pull-outs) he saw.
- The 59 s square cutdown was out of scope.
