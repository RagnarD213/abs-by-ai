# Square and vertical framing: steady wider shots

Updated 2026-09-16 from Dan’s approval of the Ad 3 square revision. Applies to digital reframing of filmed footage in square and vertical layouts, including camera windows beside graphics or a phone. This supersedes older blanket instructions to track every talking-head crop. It does not change the shared delivery gate or its thresholds.

## Choose the crop from the actual visible shot

- **Hold wider shots steady whenever possible.** Choose a comfortable horizontal center for each continuous shot and let the person move naturally inside it. Especially in square, spare room usually makes continual face recentering unnecessary and distracting.
- **Track only when a very tight crop needs it** to keep the subject or essential action comfortably visible. Retain necessary tracking in tight shots; use the least correction that works. First try a better fixed center. If that cannot contain essential movement, document why tracking is needed and use a tolerance band and gentle corrections. Do not chase every lean or hand gesture.
- Judge the actual crop and layout, not just metadata such as FAR/NEAR. A wide source inside a narrow phone-side window can be visibly tight; a NEAR-tagged source in a broad text window can still have room for a fixed center.
- A fixed center is **per shot**, never one coordinate reused across different takes. Split at edits, layout changes and hold/zoom boundaries; never smooth across cuts. A robust median of measured positions is a starting point, then inspect the full range of poses. Torso position can be steadier than a hand-contaminated face/skin centroid.
- “Wider” means the wider existing composition. A request for steadier framing does not authorize extra zoom-out, more headroom, different vertical positioning or a new third zoom level. Preserve approved zoom timing, tight-shot behavior, captions, graphics, color and audio unless asked to change them. Essential exercise action must remain visible.

## Prove the choice before the full rebuild

1. Inspect proposed framing at shot start/end and the largest lean or gesture, including transitions into and out of the shot.
2. Compare **moving before/after excerpts at the original frame rate**: at least two wider sections, one tight-shot control and affected cuts. Include a wide graphic window when relevant. Stills establish geometry; they cannot establish comfortable motion.
3. Keep a per-shot framing plan and explain any tracking retained. Movement measurements are supporting evidence, not a perceptual pass or a universal numeric threshold. A motion reviewer should distinguish changed excerpts and recognize an identical control; exclude unreliable judgments and state any inability to watch continuous playback honestly.
4. Before an isolated rebuild, verify required assets and timing against the approved source. Missing transition references must fail loudly, never silently remove flashes or overlays. Compare non-target frames and all transition windows after rendering. Bind fresh QC evidence to the final file’s hash; preserve an approved editor’s audio exactly and leave accepted versions outside the revision scope unchanged.
5. Follow existing shared audio/delivery gates and the workflow’s independent-review requirements. Record Dan’s approval or rejection against the exact file in the regression corpus. Human motion approval does not turn failed or unmeasured machine checks into passes; an unimplemented camera-motion check stays PENDING. Changes to gate code, thresholds or settings still require the full regression corpus.

Source-specific pixel widths, sampling bands, smoothing periods and speed limits are recipe parameters, not defaults for every video.

## Vertical talking head: land on him, then hold (the standard centering, Dan 2026-10-03)

**Locked by Dan, 2026-10-05:** The right-hand `after.mp4` in the Codex before/after review is the approved framing reference for all future 9:16 videos. Use this land-then-hold method through shared `cut/landing.py`. Exact clip hash, measurements and Dan's approval are recorded in `Docs/VERTICAL_CENTERING_CODEX_20261003.json`. This locks the framing method; approved exports stay untouched.

Dan compared two first minutes of the RO-10 vertical and chose the calmer one: *"I like the calmest one, the two-thirds
calmer. That looks the best to me... Let's make this our standard way of centering for verticals going forward. I feel
like this is better than what we were doing."* It applies to the talking-head crop of every 9:16 vertical, whoever
builds it (Claude or Codex). Squares keep the steadier per-shot rule above. Horizontal footage stays static (below).

The method, in order:

1. **Per picture segment, never across a cut.** A new take, a punch-in or a return from a graphic starts a new segment.
2. **Land on him.** On the first frame after every cut the crop is centred exactly on his measured head centre
   (0 px landing error). Never land where he will be half a second later.
3. **Then hold.** The crop does not move while his head centre stays inside a dead band of **3.3 % of the crop's
   width** either side of the crop's centre (20 px on the kit's 608 px wide crop of the 1080-high graded base; 36 px
   in the delivered 1080-wide frame).
4. **Follow only when he leaves the band,** and then only far enough to keep him at the band's edge, eased over
   0.75 s and never faster than 28 % of the crop's width per second (170 px/s on the 608 px crop).
5. **A segment where he wanders less than 6.6 % of the crop's width (40 px) keeps one fixed centre** for its whole
   length, anchored to its measured first-frame head centre rather than its median.
6. The end of a segment is not pulled back to centre; the next segment lands on him anyway.

What it measured on RO-10 (8:38, 25 takes) against the old track that chased every movement: total crop travel 68 %
less (10,758 to 3,413 px), typical fast pan 64 % slower (62.9 to 22.8 px/s), the crop moving 31 % of the time instead
of 50 %, him 17 px off centre at the median and 92 px at the worst moment, still far inside the 608 px crop.

Code: `_shared/cut/landing.py` (`track(..., tolerance=20, fixed_under=40, slope_px_s=170)`; `python3 landing.py
selftest`), called by `kit9x16/kit_track.py`, whose `--tolerance` default is now 20. A build that uses its own tracker
reproduces the six steps and reports the same four numbers (travel, p90 pan speed, share of time moving, median and
maximum off-centre distance). The delivery gate's own centring bound is unchanged (a hold's median head centre within
6 % of the frame width); the dead band sits inside it.

Use `landing.vertical_track(n, raw_head_x, picture_segments, crop_width, fps)` for the scaled preset, or `vertical_dense` for a native-frame track. Both call shared `landing.track` with 170/608 speed, 40/608 fixed range, 20/608 tolerance and k=3. Supply the actual cut-start head measurement, never a later estimate. If a centred crop exceeds the source, choose a wider window instead of clamping him off centre. `vertical_crop_frames` adapts existing crop maps without changing their height or zoom schedule.

Report the four measurements via `landing.motion_stats`: travel, p90 speed, time moving and median/maximum head distance. Exclude picture-cut jumps and non-presenter spans, weight moving time by frame durations, state the pixel space, and define moving as over 5 px/s scaled from the 608 px reference crop. Inspect rendered cut landings, head clearance and native-frame-rate motion. These measurements supplement the unchanged delivery gate. Approved exports stay untouched.

## Horizontal footage stays completely static — Dan, 2026-09-17

- **No added camera movement or recentering on Dan in horizontal/16:9 videos.** No tracking, pan, drift, animated crop or zoom to follow or center him. Choose a fixed composition for each shot and leave it fixed. This supersedes earlier horizontal exceptions for approaching the frame edge; tracking is only for square/vertical layouts when actually needed.
- Ordinary cuts between fixed compositions remain editing cuts, not camera motion. Graphics may animate without moving the presenter picture beneath them. Check actual rendered background landmarks: a fixed-X setting alone does not prove a static picture. If the camera source itself drifts, resolve that in source choice/stabilization rather than silently claiming the delivered picture is static.
- Dan approved C1652 R4 as good enough to ship despite a small remaining movement near1:09. Do not reopen that accepted film to enforce the future rule. Its approved master is SHA256 `eace1bdbb9f7a16fadff8bb2d2e80812ea4e777cf413a1e06575527f95d64f44`.
- C1652’s Zepbound text size is approved. Dan would prefer a third benefit, “Makes you serious about fat loss,” in a future relevant treatment; he accepted the existing two-row graphic in this final film. Do not expand its content without speech/timing context in future work.
