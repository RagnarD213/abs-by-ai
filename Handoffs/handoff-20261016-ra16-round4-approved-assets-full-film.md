AD. AI Took Job AD R4. Build the complete approved film in 9:16 and 16:9, each 59 seconds or less.

# Authorization and exact next action

Recommended model: GPT-6.1 Sol, high effort. Name the next chat **AI Took Job AD R4**. Use `Media/codex-video-trial/skills/abs-edit-ad/SKILL.md` and current shared VIDEO-RULES. This handoff supersedes `Handoffs/handoff-20261015-ra16-round3-approved-look-and-intro.md` and the older October 14 handoff.

Dan approved all remaining assets on 2026-10-16: **"Everything is approved. Go ahead and give me the handoff for the next round to generate the full film"**. All four assets, D01/G01/G02/G03, are approved in both formats. Color B, medium crop pair 1, complete intro and warm-bass voice were already approved. There are no pending asset choices. Do not ask for those approvals again.

The exact next action is to verify the protected inputs in the approval record, create an isolated `round4/` assembly recipe, rebuild final presenter plates with correct native cut/return tracking, and render both complete films. Deliver the whole ad in this round under the shared short-ad rule, not another opening-only excerpt. No complete master exists yet. Dan has approved the components and authorized assembly, not approved an unseen final film.

# Authoritative locations

- Project: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/`.
- Work root: `/Volumes/Extreme/_edit_work/ra16/`. Keep Extreme connected. Raw media stays read-only.
- Speech, words, graphic plans and approved look: `round2/` under the work root.
- Approved R3 repairs and QA: `round3/`; final horizontal caption layout and native clearance evidence: `round3/v2/`.
- Exact approval record: `/Volumes/Extreme/_edit_work/ra16/round3/round4-plan/decisions.json`.
- Durable approval copy: `Codex Ad Videos/ai took my job - RA-16/R3 asset review/approval-R3.json` in the project. It records Dan's words, all 24 native/review/poster hashes, the six prior look hashes and six protected assembly input hashes. All were verified when this handoff was written.
- `round2/asset-preview-QA.json` now says assets approved and full assembly authorized; matching copies exist in `round3/` and the delivery package. `round3/WORK_PACKET.json` has no remaining approvals and points to R4. Historical R2 decisions remain unchanged; their pending-asset language is superseded by the new record.
- Review page: http://127.0.0.1:8976/, served from `round2/`. Preserve this port and managed service. The R3 page is historical asset review; replace its pending-choice language when adding R4 full films.

# Preserve exactly

- Full opening: **"I'm a personal trainer. And AI just took my job."** Dan is on camera. No robot opener and no ending URL mark.
- Delete only **"And it's completely free"** and **"while human trainers leave you confused until next week."** Retain every other filmed line, including obsolete/everyone, the early free-app CTA, complete human-plan comparison and final CTA. Scripted claim lines are approved.
- The authoritative 12-piece cut is `round2/cut.json`, SHA-256 `2d3d48cd8ec0f29a43859482a8d8e07fa55285bfb2ac3f2ea8a221f2a3c79ae3`. Do not use the old `proposed-cut.json`. The R2 cut file's pending-look and source-listening strings are historical; speech checks and approvals are recorded elsewhere.
- Authorized pitch-preserving speed: `1.1147707979626484`; retained source is 65.66 seconds. Use one synchronized timeline and identical sound for both formats.
- Target: **1765 frames at 30000/1001, 58.8921667 seconds**, 1080x1920 and 1920x1080. The mapped final word ends at 58.73853 seconds, with about 0.154 seconds of picture tail. Verify actual delivered speech and mux duration; neither export may exceed 59 seconds. Trim only unused tail if required, never a word ending.
- Color B: daylight S-Log3 LUT `/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.45.cube`, saturation 1.12, gamma 1.03, BT.709 interpretation. Preserve native rotation handling for C1668: encoded 3840x2160 with -90 rotation, displayed 2160x3840. Source identity/current path is `source/roll.json`.
- Medium/closer crop pair 1: vertical source windows 800x1422 and 612x1088; horizontal 2160x1216 and 1728x972. Horizontal presenter composition stays fixed within each shot.
- Chosen voice: `round2/audio/warm-bass-final-timing.wav`, SHA-256 `00eef07fc0028d1a1632151f740207366a27ecc9b3d6e7b346f8c39f1b8922d1`. Preserve the selected warm bass, no dereverb and no rerun of the voice chain merely to build picture. WAV measures 58.919 seconds. Encode the common final audio once and reuse it in both formats where feasible.

# Approved assets and repairs

The times below are planned film positions, not a claim that a final master already exists. Resolve final events on the native output grid from `round2/words_out.json` and `round2/plan_resolved.json`.

| Asset | Planned film time | Locked content |
|---|---|---|
| D01 | 19.402-24.193 | Same-person sunglasses real photo, generation in the modern phone shell, original AI pool goal picture. |
| G01 | 25.25183-32.81392 | Shared Soft Blue Light HyperFrames analysis card, AI pool photo, scan, Body Fat/Fat To Lose/Muscle To Gain bars, Your Workout Plan band, no numbers. |
| G02 | 32.81392-38.10649 | Motivation lower third: A Plan Built Around Your Goal. |
| G03 | 42.66348-47.41782 | Motivation lower third: Keep Progress Going When Life Changes, parts driven by AI adjusts and when life gets. |

Use `round3/DEMO-9x16-CLEAN.mp4` and `round3/DEMO-16x9-CLEAN.mp4`. These sources have no baked captions. Apply the final caption layer exactly once after composition. The old demo sources caused doubled phrases at film frames 661 and 679. Preserve the approved phone/image/label sequence: REAL through source demo frame 107; AI starts at 108 at the grid transition before the goal appears. Do not replace the sequence with phone-scrolling filler or generate new motion.

Use the shared HyperFrames method and existing matching builds in `round2/hf16/` and `round2/hf9/`. Do not fork templates or redesign approved graphics. The final horizontal caption reference is `recipe/round3_caption_clearance.py`: Manrope ExtraBold, balanced three/four-word phrases, captions under the right-hand analysis panel at center X 1370.5 and Y 930, clear of the AI label beneath the left photo. Measured native separation is at least 381.5 pixels horizontally and 61 pixels at the bottom. Preserve the separately lifted horizontal demo and lower-third caption positions. Recheck actual final composites at caption boundaries.

# Build traps and final framing

No ready-made R4 full-render command exists. Adapt the existing recipes into a new R4 assembly recipe; the context renderers do not produce full masters. Do not import `round2_visuals.py` as a harmless module: it has top-level source sampling/render side effects. Do not restart the completed R2 preview queue, rerun the R3 packaging script over approvals or overwrite reviewed R3 contexts.

Existing R2 presenter plates predate the final tracker correction and are not a final framing pass. `recipe/round2_visuals.py` now uses `FPS * speed` with the shared landing tracker for source-frame samples, so the easing remains 0.75 seconds in delivered time. Final assembly must split tracking at every visible picture cut and return from full-screen inserts, measure the actual first visible head position and use shared `cut/landing.py`. In particular, G01 ends inside P07: land at its actual return, not P07's hidden start. Avoid smoothing across cutaways. Report shared motion statistics and inspect dense native hair clearance; face-box hair estimates alone do not pass it.

`round3/final-verification-preparation.json` records provisional source joins, asset spans and return frames. It is preparation only, not final state or a gate stamp. Rebuild native word/event timing in R4 and validate it. Useful expected boundaries:

- Continue P03 picture through frames 578-580 before D01 appears at 581, instead of a tiny P04 close-up island. Picture only; audio timing stays unchanged.
- D01 exits at 725. G01 begins at 757, covering the P05/P06 splice at 777, and returns at 983 after the P07 source join at 980.
- G02 fades across the intentional wide-to-close cut at 1139 and is gone at 1142.
- G03 starts at 1279. "And finally" is uninterrupted inside P08, not an audio splice. The intentional close-to-wide cut at 1390 retains the lower third; it fades at 1419-1420 and is gone at 1421.
- Expected visible native landings include 0, 284, 451, 725, 983, 1139, 1390, 1523, 1593 and 1710. Audit actual rendered boundaries, not just these preparation numbers.

# Required review, gates and honest status

R3 completed native chronological samples, consecutive-frame boundary strips, disclosure/phone/caption checks and independent moving-context/layout checks. `round2/asset-preview-QA.json` retains the reports and native dispositions. Gemini mistook fully covered presenter returns for naked splices and missed brief lower-third fades. Keep those records; inspect actual final boundaries before accepting or rejecting a new finding. Final layout still review found no overlap or clipping. None of this replaces a complete-film review.

The approved warm-bass input has an existing **audio gate FAIL on tone only**, with 11 of 12 measurements passing: mean tone error 2.721 dB, max 5.27 dB, -14.30 LUFS, -2.30 dBTP. Dan's approval does not turn that technical stamp into PASS. Preserve his sound, run exact-file checks and report actual outcomes. Never tune a threshold or alter his chosen voice to hide this recorded mismatch. Prior complete audio listening rated intelligibility 9/10; full picture/lip-sync review is still required.

Complete the renderer-emitted caption/label states, delivered ASR, full validated edit sheet, exact-file audio and delivery gates, full chronological picture/audio watch, every join and frozen-scene disposition, and one independent complete-candidate review after editor self-QA. Use the current shared standards and gates, with no invented pass or silent skip. Fix actual defects and recheck changed material. Unresolved gate findings stay explicit.

Respect the two-build cap through shared `buildcap.py`; do not start a third build. Keep the global dispatcher paused. R3's `recipe/round3_build_slot.py` preserved queue age across nested stages; it is a local scheduling helper, not authorization to bypass capacity. Long rendering/waits go through the existing supported queue/waiting workflow with a persisted packet, not repeated model polling.

R3 generation spend was $0. Successful asset/layout reviews returned 56,780 input, 4,590 output and 18,894 thought tokens; estimated under $2, billed dollars unavailable. Earlier reviews were estimated under $1.50. No new generation is needed. State the estimate before the next independent review batch and follow standing spend limits. Editor usage unavailable from runtime stays unavailable.

# Delivery and review page

Deliver native masters, matching 540p review copies, reference/current audio A/B, actual gate stamps, final edit sheet, review evidence, notes and rebuild recipe to `Codex Ad Videos/ai took my job - RA-16/` in the project. Both full review videos are over 45 seconds, so also place them in `Videos to Review/` with clear R4 and format names. Make each file easy to identify and link both formats in chat.

Reuse the managed :8976 page, with the complete films and clear revision/watch timestamps. R3 player repair is in `recipe/round3_player.js` and `recipe/round3_page.py`: fresh video element per selection, scroll player into view before decoder startup, initial preload/poster, seek controls, explicit Play / Pause, Reload Clip and separate-clip link. Preserve that repair when adding R4. Refresh with `python3 .claude/skills/_shared/review_server.py 8976 /Volumes/Extreme/_edit_work/ra16/round2`; get Managed review ready. A launchd bootstrap exit 5 immediately after bootout may need one retry after the old worker exits. Never substitute a temporary terminal server.

Test playback, format switching and seeking in the actual panel. **Mute assistant playback tests and leave playback paused**, under the current shared rule. Preserve Dan's ability to hear the review normally. Verify HTTP 200 and byte-range 206, but do not treat those as proof that the picture plays. Save a visible browser proof.

This round is full-film production and review only. No publishing, upload, ad setup, organic derivatives, covers or additional formats. Keep any genuine new final-film decision separate from the now-settled asset choices.

# Ready-to-paste starter prompt

AD. Name this chat "AI Took Job AD R4". Use Media/codex-video-trial/skills/abs-edit-ad/SKILL.md and execute Handoffs/handoff-20261016-ra16-round4-approved-assets-full-film.md. Everything on the R3 asset page is approved in both formats. Generate and review both complete films at 59 seconds or less, targeting 58.89 seconds. Preserve color B, medium crop pair 1, the complete intro, warm bass voice and approved assets. Complete the final vertical framing, native checks, exact-file gates and independent full-film review. Reuse the repaired review panel and mute your playback tests. No publishing.
