# CONTENT: Meal Prep SFC R2, review picks

Chat: Meal Prep SFC R2. Dedicated Short, DS-28. Round2 review packet: http://127.0.0.1:8891/. Managed server caches linked assets on internal storage and restarts at login. Round1 left intact, 33/33 packet hashes matched. No complete film exists. No paid motion generated.

## Read

Original brief: Handoffs/handoff-20261011-ds28-round2-crops-intro-graphics.md. Work: /Volumes/Extreme/_edit_work/ds28/round2/. Decisions: round2-plan/decisions.json. Packet hashes: packet-manifest.json. Review page/notes: review/index.html and review/notes.md. R1 verification: round2-plan/round1-rehash.json. HTTP evidence: http-check.json. Graphic word drivers: graphics-sheet.json. Crop light/hair measurements: review/crop-measurements.json.

## Pending picks

1. Crop A/B/C. B recommended. Each pair compares the same speech wide/tight at two postures, film 4.97-8.24 and 22.49-25.72. Wide includes both entire blue light fixtures; tight excludes both. Actual hair and light landmarks measured every 0.25 s. All paired clips exist. Full-width A clamps to source bounds, so exact horizontal centering cannot be guaranteed. Preserve the requested lights rather than tightening to the legacy head-size gate.
2. Four new AI start/end frames, two scenes, generated via codex-image.sh using gpt-6-sol high on subscription. Paths: review/frames/top-start.png, top-end.png, bottom-start.png, bottom-end.png. Concept follows Dan's exact brief. Split and full-screen compositions alongside. Upper man places a sealed purchased meal from the bag onto counter; lower man stirs food with a frustrated reaction. These are pending frame pairs, not motion approval.
3. Seven graphics, G01-G07. Every one has a graded still and moving speech context on the page. G03/G06 use shared Motivation HyperFrames 0.8.97 through vertical.py and maintained RGB compositor. Other graphics propose an illustrated ribbon from maintained Soft Blue Light components; this new layout is pending, not a shared template approval. No shared templates changed. Faces and captions clear on inspected frames, some arm gesture space behind the translucent card is disclosed in notes.

## Applied scope

Opening context 0.00-8.24: labelled start/end frame preview through 4.97, then Dan on camera with G01 on Here's what I do instead. B0503 removed from this placement.

Reuse context begins at film 16.90, full-screen top scene at 18.62-22.49, then camera with G04. B0018 rejected for this video and replaced in proposal. Dan expressly authorized repeating the top scene here. The scene reuse context is a frame-placement preview, not finished AI footage.

No audio cuts, speed changes or pause removals were applied. The 59.56-second film word map still applies. Wider/tighter picture changes land at natural phrase boundaries and graphic parts reveal on spoken words. Caption price section split into two-word chunks for width. No full closing pickup assembled. G07 context ends before that pickup. Later full build must rebuild time maps if it removes verified pauses.

## Verification and open work

All 33 prior packet hashes matched. Linked local URLs return 200; MP4 byte ranges return 206. Chrome crop B playback and forward/backward seeking succeeded. Opening final concat re-encoded to maintain consistent seekable stream after an initial seek fault. Recheck the fresh cached opening before continuation.

The exact short opening audio gate FAILS comb ripple, room early decay and word-tail dryness. Tone, loudness, no clipping and measured do-no-harm pass. The short test uses a six-second analysis window. It does not replace round1's longer audio measurements. No thresholds relaxed. Prior full-context tone, coverage, legacy head size and independent caption alignment failures remain open. This creative packet is not final delivery certification. No independent complete-candidate review yet because no complete candidate exists.

## Build and cost

Recipe: crops.py, hf.py, graphics.py, compose_frames.py, context.py, packet.py. Original C1720 source path in crops.py. S-Cinetone Rec.709 portrait, no transpose/log LUT. Caption repair can reuse unchanged G06 base with `graphics.py --caption-repair --only G06`; normal builds regenerate measured bases. Preserve exact-file hashes after repairs and refresh review cache.

Images: four subscription stills, reported 103733 Codex tokens. Paid generation this round $0; cumulative motion $0. Earlier Gemini review $0.434918. Editor/reviewer token use and provider invoices unavailable. After approved frames, check current provider estimate and state it before generating motion. All paid motion/retries stay inside cumulative $5 content-video cap unless Dan separately raises it.

## Exact next action

Record Dan's crop and frame picks verbatim with actual hashes in next decisions record. Generate only approved scene motion, with enough top-scene movement for both placements, inspect hands/bag/lids/meal consistency at speed, and show opening/reuse in context. Assemble full film after material choices lock; perform exact-file gates, full picture/audio inspection and one independent candidate review. Dispatcher stays paused. No covers, alternate formats, upload or publishing.

Recommended model: GPT-6 Sol, high effort.

Ready-to-paste prompt:

Continue Meal Prep SFC R2. Read Handoffs/handoff-20261011-ds28-round2-review-picks.md. Record my crop/frame/graphics picks with hashes, generate only approved motion inside the cumulative $5 cap, and show the split-screen opening, immediate camera return and full-screen ripped-man reuse in moving context. Use the Codex subscription to generate any replacement images. Preserve round1 and the selected crop's light rules. Resolve open sound and caption checks before the complete film. No covers or uploads.
