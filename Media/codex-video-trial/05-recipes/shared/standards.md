# Shared editing standards, 1.8.0

Applies to the two Codex raw-edit workflows. Project root is `/Users/danielrose/Documents/Claude/Projects/Abs By AI`; `T` below is its `Media/codex-video-trial` directory. Read current project instructions and claim only your task in `AI_COORDINATION.md`. Trial work stays private; no publication, deployment, messages, or extra formats are implied.

## Approval and source identity

Use [the recipe registry](../../templates/recipe-registry-v1/recipe.json) to distinguish approved components from complete exports. Every approval belongs to a specific media hash and scope. Ad 1 sound/color are accepted, with four picture corrections outstanding. Organic V4b edit/audio and the later 30-second color sample were accepted separately; there is no combined full-film color export. Historical `youtube-organic-v1` and proposed `template-v1.1-proposed` remain frozen. Neither numerical passes nor model praise establish Dan's preference or publication approval.

Record raw camera media, shared original assets, generated media, finished human references and finished AI examples separately. Check existence, stream properties and hashes before use. Human finished pixels/audio are comparison material in a raw edit, never undisclosed ingredients. A replay of accepted components is explicitly a replay, not a new original or a first-cut quality result.

## Approved graphics and layout standards, updated 2026-09-26

Read [the shared approved graphics reference](../../../../.claude/skills/_shared/GRAPHICS-STANDARDS.md) before graphic or phone work. Soft Blue Light is the standard graphic family for all videos: website VSLs, paid ads, organic long-form, Shorts and newly revised square/vertical graphics. The Motivation lower-third format is locked for all lower thirds. This supersedes historical Ad 1 palettes, olive/white graphic defaults and Muhammad graphics reproduction wherever a new or revised graphic is being authored. Sound, camera color, captions and transitions retain their separate rules. Preserve existing approved exports on a format-only conversion unless Dan requests a graphics revision. Use three vertical portraits in triptychs, sequential horizontal photos, credible rounded iPhone displays, and safe fixed presenter positioning beside background-free website bullet lists. These current approvals supersede conflicting older graphic examples. Source-specific WV-01 crop, color and sound settings remain scoped to that shoot. Both installed Codex skills inherit this reference.

## Sound and color

Read [source calibration](source-calibration.md) before adapting a recording. Use the project's existing `pick_lav.py`, `voice_chain.py`, `audio_gate.py` and delivery gate; do not copy their signal processing or thresholds into a skill. Source-specific parameters live in the video manifest or frozen recipe. Identify the microphone on every new roll; a channel number from a previous shoot is not evidence.

## Square and vertical camera movement

Read [the shared framing rule](../../../../.claude/skills/_shared/framing-motion.md) before choosing crop motion. For squares, Dan approved Ad 3’s steadier wider shots on 2026-09-16: choose a fixed horizontal center per wider shot whenever possible; retain tracking only where a very tight visible crop needs it. Judge the actual layout, not FAR/NEAR tags. Preserve approved zoom timing, framing height and audio. Compare moving wide excerpts, a tight control and affected cuts before a full rebuild. The shared rule also covers required-asset preflight, honest motion review and exact-file approval evidence. Both Codex adapters inherit this update through this file.

## Editorial meaning

Before expensive picture work, produce a compact scene map: spoken beat and source/output time; asset path and provenance; depicted person; action; before/goal/real-result/neutral role; why it supports the sentence; any demonstrative referent; label and attention treatment. Read [scene review](scene-review.md), including the four Ad 1 corrections. Review this map against the actual source and speech. Store observations and unresolved items, with the scene-map hash. Schema validation checks that evidence is present; it does not see whether an asset is truthful.

Keep the same person through upload and generated result. A visible speaking take must match its audio; a silent exercise demonstration may support a different spoken explanation. Demonstrations must actually play, remain readable and contain the relevant body/equipment through the whole action. Fitness-themed stock is not evidence of Dan doing the action described.

When reusing Dan's older published work, treat the final edited/color-corrected export as the source master; raw or unfinished camera footage is not an acceptable substitute. When the point is Dan's Six Pack Shortcuts or SixPackAbs.com channel history, retain the YouTube screen-capture context and keep the channel name, view count and subscriber count legible. A clean crop of the old video loses the credibility evidence and is not equivalent.


### Ad14 R3/R4 source selection and final approval — Dan, 2026-09-17

Old-channel references must show a **native close-up of Dan speaking**, with the full YouTube screen capture, channel name, subscriber count and views visible. Do not select a Mike-speaking two-person shot that makes Dan look secondary. Use the diet source for diet references; use M100s for exercise/SixPackAbs.com references. Selecting the close-up within the original player is different from cropping the whole page.

For the one-minute ab workout, the approved source candidates are the V4 explainer+workout and V5 workout-only **UPLOADED** exports under `YouTube Long Form Video Content/V4 + V5 - The Ultimate 1 Minute Ab Workout - UPLOADED/`. The exact filenames/hashes are in `T/records/ad14-r3-feedback-20260917-final-revisions/verified-workout-sources.json`. `Media/video_edit/out/abs_workout_final_edited.mp4` was incorrectly classified as the desired finished export; Dan rejected its appearance as raw/uncorrected. Never reuse it or `Media/video_edit/work/main.mp4` as finished reference footage. Verify visual provenance, not the word “final” in a filename.

Dan approved R3 g17 (132.499–142.709s) as the reusable demonstration whenever he refers to generating his own photo with AbsByAI. Preserve that exact sunglasses-before → app interaction → pool-goal sequence and labels. The clean reusable asset needs the finish-layer disclosures documented in its provenance. Future reuse of this exact simulation is authorized; keep the internal simulated/composited record. This is scene approval, not approval of the whole R3 export.

Evidence: `T/records/ad14-r3-feedback-20260917-final-revisions/`; scoped approval/rejections also recorded in the shared corpus. The new editorial predicates remain PENDING, not implemented automatic checks.

Dan approved the complete Ad14 R4 master, SHA256 `515953918d223c389754153cd1fa6388ba9d2d18b942024b6c680d3184979785`, praising its color correction, audio, clips, final revisions, selected workout footage and app demonstration. R4 used source30.000–38.008s from the verified diet screen capture for Dan's native close-up and source56.000–61.4054s from the exact V5 UPLOADED export for uninterrupted Spiderman Planks. Those ranges are source-specific evidence, not universal defaults.

The reusable revision method is recorded in `Media/codex-video-trial/skills/abs-edit-ad/references/ad14-r4-methods.md`: freeze the approved-element list, rebuild only rejected picture jobs, validate actual finished pixels instead of filenames, preserve approved audio/app pixels exactly, measure codec spill honestly, and keep inherited out-of-scope gate findings visible. This final approval does not turn those inherited findings into machine passes.

## Review, revision and learning

Read [review and revisions](review-and-revisions.md) before a render or delivery. Make source-specific decisions once and reuse unchanged analysis, picture, sound and assets by input fingerprints. Record real cache hits, actual costs and preserved first cuts. Validate the exact new export even when its AAC packets are unchanged.

One editor owns each candidate from scope through self-QA. One independent reviewer enters at the complete-candidate checkpoint and returns one consolidated verdict. A rejection parks the candidate with that correction list; it does not automatically start an editor/reviewer supervision loop. Use a short work packet containing only requested changes and approved elements to preserve. Additional high-cost planning or review is reserved for a named unresolved problem, not routine oversight.

Before a full render, verify risky source selections against the actual file and inspect a 0.5–15 second moving preview. Risky choices include old-channel proof, exercise or product demonstrations, generated motion, app-session continuity, before/after identity and disclosure placement. Record source and preview hashes. Reuse fingerprint-matching scenes, accepted audio, transcripts and assets. Let the existing queue hold the build slot, heartbeat and wait; an AI session must not repeatedly poll unchanged render state.

Every full-video result records the production revision number, model/effort for the editor and reviewer, available per-session token/cache counts, and every paid-provider cost. If the launcher or provider does not expose a measurement, record `null` plus the reason; never report unavailable as zero or allocate an account-wide allowance delta to one video.

## Approval before a full render

Follow the canonical [pre-render approval workflow](../../../../.claude/skills/_shared/PRE-RENDER-APPROVAL.md): first 30 seconds to lock source-specific color/audio and opening treatment; all graphics with surrounding speech; all clips in context; and authorized AI start/end frames followed by finished clips. Preserve unchanged scoped approvals and explicit sample waivers. Do not build a full placeholder film while awaiting approval. Use plans and isolated/contextual previews, persist the work packet and park with no model polling. The existing clip [asset records](../../../../.claude/skills/_shared/ASSET-APPROVAL.md) remain in use; queue frame approval alone is not approval of every graphic or of a complete film.

After concrete feedback, update the rule that caused the mistake, its evidence and version. Keep per-source coefficients scoped to that source. New approval/rejection evidence goes into the private trial records and the shared regression corpus in coordination with its owner. Never mark an unimplemented semantic predicate as an automated detector. Both skills link to this same file; update it once.

## Horizontal footage stays completely static — Dan, 2026-09-17

- **No added camera movement or recentering on Dan in horizontal/16:9 videos.** No tracking, pan, drift, animated crop or zoom to follow or center him. Choose a fixed composition for each shot and leave it fixed. This supersedes earlier horizontal exceptions for approaching the frame edge; tracking is only for square/vertical layouts when actually needed.
- Ordinary cuts between fixed compositions remain editing cuts, not camera motion. Graphics may animate without moving the presenter picture beneath them. Check actual rendered background landmarks: a fixed-X setting alone does not prove a static picture. If the camera source itself drifts, resolve that in source choice/stabilization rather than silently claiming the delivered picture is static.
- Dan approved C1652 R4 as good enough to ship despite a small remaining movement near1:09. Do not reopen that accepted film to enforce the future rule. Its approved master is SHA256 `eace1bdbb9f7a16fadff8bb2d2e80812ea4e777cf413a1e06575527f95d64f44`.
- C1652’s Zepbound text size is approved. Dan would prefer a third benefit, “Makes you serious about fat loss,” in a future relevant treatment; he accepted the existing two-row graphic in this final film. Do not expand its content without speech/timing context in future work.

## Vertical crop standard, 2026-10-03

For 9:16 presenter footage, the newer shared **Vertical talking head: land on him, then hold** section supersedes the wider-shot fixed-centre advice above. Use `.claude/skills/_shared/cut/landing.py` and `landing.vertical_track`: land on the measured cut frame, hold within 3.3% of crop width, ease to its edge over 0.75 seconds, cap travel at 28% of width per second, fix small-wander takes (under 6.6%) at the first-frame centre, and never anchor the exit. Report travel, p90 speed, time moving and median/maximum head offset. Approved exports and frozen per-video recipes remain untouched.
