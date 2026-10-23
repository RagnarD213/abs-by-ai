**SFC.** Task name: `Ronaldo Ab Belt SFC R5`. Model: Claude Opus 5.5, high (the video started on Claude).

# DS-33 "Cristiano Ronaldo Sells An Ab Belt. It's Harder Than A Workout." Round 5

CONTENT, dedicated Short. Round 4 delivered 2026-10-23: review page http://127.0.0.1:9036/, master
`/Volumes/Expansion/_edit_work/DS-33/r4/review/Ronaldo Ab Belt SFC R4 - complete Short.mp4`, sha256
`5845b5af8f02df6e8b086192899cfbc53cbb4f94f0a8e09f277ddc4727a9e879`, 1867 frames, 62.30 s. Independent review SHIP
(`r4/ROUND-4-REVIEW.md`). Read `Handoffs/video-editing/00-RULES.md` and `.claude/skills/_shared/VIDEO-RULES.md` first, and the
shorts skill section "Green-screen reaction shorts: what DS-33 (Ronaldo Ab Belt) cost" (its R2 lessons apply).

## Dan's round 4 notes (verbatim, 2026-10-23)

> Okay, revisions. After the intro clip plays, right now the horizontal clip on top is playing above my head. What I want is a
> slight overlap between my head and my hair and the horizontal clip. I want my head and my hair to be in the foreground and the
> horizontal clip to be in the background. That way, my head and my hair are over the horizontal. Put it so the bottom 10%
> overlaps slightly. I don't want it too far. I want the clip to overlap with this slightly behind my head and my hair. Yeah,
> handoff for the next round

## Locked (do not reopen)

The R4 opening (0:00-0:14.114, Dan floating lower left at 0.40 with the laptop, the Bill Maher B format; Dan did not object to the
reviewer's note about the faded forearm strip at 0:00-0:02, keep it). Soft Blue Light background. Warm colour, Balanced voice,
house key (keyed once in R2, reuse). Audio, captions text and timing, G03, G04, B-roll, everything after 0:28.762. The full-width
ad card (1080x608, top, the 60 s version, silent). Upload title for the later setup: "Does Cristiano Ronaldo's Electric Shock Ab
Belt Work?" (Dan, 2026-10-22).

## What to build: the split only (0:14.114-0:28.762, film frames 423-861, shots SP1 423-604 and SP2 605-861)

1. **Layer order flips:** the ad card is drawn FIRST (over the Soft Blue Light field), then Dan on top of it with his key alpha.
   His head and hair are in front of the clip. Today (`r4/recipe/assemble_r4.py`, `frames_film()`, the `split` branch) Dan is drawn
   first and the card pasted over him, plus a 14 px shadow strip under the card edge: drop that shadow strip (or keep it only on
   the background, never over Dan).
2. **Overlap = the bottom ~10 % of the card**, "slightly, not too far": the card is 608 px tall, so Dan's hair top sits about 60 px
   above the card's bottom edge (608), at about y 548 on screen, at his usual head height. Measured R2/R3 hair tops at the R2 panel
   position (y 531, DY 0): SP1 p10/median/p90 = 587/601/618, SP2 585/596/617 (screen px). So DY ≈ SP1 -53, SP2 -48 (R4 has -10 /
   -6). Re-measure on the actual frames and set DY so the MEDIAN hair top sits ~60 px above 608; report min/max (it will overlap a
   bit more when he rises and a bit less when he dips: never let the card's edge cut across his eyebrows; with Dan in front this
   only affects what of the clip is hidden, not Dan).
3. Dan's window still extends to the frame bottom (R3 fix: `win` height scaled by (1389 - dy)/1389); check the window stays inside
   the keyed 1620x2880 frame (R4 SP1 bottom ~2686 at DY -10; at -53 it is ~2750, fine; verify).
4. **G02 "The Catch"** moves up with him: box top = measured lowest chin point + 25 px (R3 method: FaceMesh on every 2nd frame of
   SP2, `r3/recipe/chin_measure.py`; R2 measured 1196 at DY 0, so ~1148 + 25 at DY -48). Captions under G02 follow automatically
   (`captions_r3.py` MarginV rule from the manifest). Re-render G02 with `graphics_r3.py` (SHIFT).
5. Update `gateplan` split talking-head rects to the new DY (rect y = 531 + DY, height 1389 - DY). With Dan in front of the card the
   gate's hair rows should now read real headroom in the split; the opening's hair rows still misread Ronaldo's picture above Dan
   as hair at the window top (known since R4).

## Cheapest build (the queue is slow: plan for waits)

- Work folder: `/Volumes/Expansion/_edit_work/DS-33/r5/` (copy r4: recipe, edl.json, shots.json, framing-frames.json, words_out.json,
  captions.ass, mix wavs, graphics-manifest.json, negative-events.json; symlink `key` -> `r2/key`, `keypm` -> `r3/keypm`, `src` -> `r2/src`).
- Render only the split: `BG=softblue assemble_r5.py --range 14.114:28.762` (frames 423-861; note the range mode iterates from frame 0,
  so it decodes the intro too), then join three parts into the master like `r4/recipe/mux_r4.py` does: R4 `composite_softblue_0_423.mp4`
  (frames 0-422) + the new split composite (423-861) + R3 `/Volumes/Expansion/_edit_work/DS-33/r3/composite_softblue.mp4` from frame
  862, captions burned, `mix-balanced.wav`. The audio stream will be bit-identical to R3/R4 (stream md5 fe8e53a5a59d5e2292e3850ceb4745fe):
  if so, reuse `r4/finished-asr.json` with the new video sha and that proof (as R4 did) instead of re-transcribing.
- Then: audio gate, negative-events sha, gate plan, watch pass, independent review (fresh `ra-reviewer`; brief it with Dan's words
  above and ask specifically about the head/hair-over-clip edge: key edge of his hair over the bright ad, any halo or dark rim there),
  `watch.py --judge`, delivery gate, review page (copy `r4/recipe/page_r4.py`, new port, e.g. 9037), VLC copy in `Videos to Review/`
  replacing the R4 copy, delivery folder `Short-form video content/Ronaldo Ab Belt - DS-33/`, `queue.py set DS-33 delivered`,
  timestamped revision list in chat (the change is 0:14.1-0:28.8; watch 0:12-0:31).

## When Dan says final

Close out (approval JSON with his words in the delivery folder and the Extreme backup folder, regression corpus entry, delete the
VLC copy, `review_server.py <port> --remove` for 9033, 9034, 9035, 9036 and the R5 port, `queue.py set DS-33 finalized`), then write
the setup handoff (one Claude task, covers via "Use the Codex subscription to generate the images.", five-cover mix, stop for the
pick, Blotato on the dedicated-Short Thursday slot per `Docs/SHORTS_RELEASE_CALENDAR.md`, `ai_generated: false`: no AI footage in
this Short) with the title above. Example: `Handoffs/handoff-20261020-ds31-ai-homework-setup.md`.

## Ready-to-paste starter prompt

SFC. Name this chat Ronaldo Ab Belt SFC R5. Read Handoffs/video-editing/00-RULES.md, then execute Handoffs/handoff-20261023-ds33-ronaldo-ab-belt-r5.md: Dan's round 4 note on "Cristiano Ronaldo Sells An Ab Belt. It's Harder Than A Workout." (DS-33). In the split after the intro, put my head and hair in front of the horizontal clip, with the bottom 10% of the clip slightly behind my head; everything else stays as round 4. Every gate, independent review, deliver, send me the review page and the VLC copy, update the master list.
