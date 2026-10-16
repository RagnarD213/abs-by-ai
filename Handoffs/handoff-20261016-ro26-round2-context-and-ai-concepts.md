# RO-26: revise the first-round review with context and AI concepts

Prepared 2026-10-16 at Dan’s explicit request. Recommended executor: **GPT-6 Sol, High**, with `$long-form-content-edit`. This supersedes `handoff-20261016-ro26-round1-graphics-review.md`. Do not restart source selection or build the full film.

## Current state and source of truth

Project: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Work: `/Volumes/Extreme/_edit_work/ro26/`; build next work in `round2/`, preserve original evidence in `round1/`.
Video: “I’m 41. My Life Is Top 1%. How I Did It.” Organic 16:9, C1768 from the 10/15 shoot. Source paths and edit ranges are in `round1/cut_map.json`; selected speech is in `round1/words_out.json`. Provisional story length is about 5:07. No finished first minute/full film, final SRT or full-film gate stamps exist.
Read current AGENTS.md, VIDEO-RULES.md, PRE-RENDER-APPROVAL.md, the Codex skill, job brief and environment table. Read `round2-plan/decisions.json` and `Docs/memory/ro26-ai-pool-photo-correction.md`. Current review: http://127.0.0.1:8982/ (Mac-local only). The old page is not an approved treatment; its false O01 claim has been withdrawn.

## Dan’s decisions

1. **O01 rejected.** The image proposed at 00:01 is AI-generated. Source: `photos/dan transformation photos/dan by pool.png`, SHA-256 `c65698bf5a648b9e8f76d8f46a36267942dea312fc29a130dba3d0d707d4c81a`. Never label this or its derivatives a real photo. Its erroneous derivative was `round1/review/assets/O01-pool-proof.jpg`.
2. **Opening replacement:** full-screen graphic with three vertical images of Dan with six-pack abs. Reuse an existing suitable approved trio or compose it from verified real photographs. Lead: `studio-blue-11_FINAL_PRIMARY.jpg`, `studio-blue-89_FINAL_PRIMARY.jpg`, `studio-blue-177_FINAL_PRIMARY.jpg` in `photos/finalized social media photos/`, documented in `Handoffs/handoff-20260927-wv01-round6-A-only-revisions.md`. Check the actual approved component, photo provenance, hair/abs clearance and current Soft Blue Light style; do not generate replacement physiques. Real-photo disclosure only after provenance verification.
3. **G05 approved:** Dan said, “I like that full-screen graphic.” Preserve the four-things recap design; hash and record the actual `round1/review/assets/G05-recap.png`. Contextual timing is still to be shown; do not ask him to pick its design again.
4. **Other clips/graphics remain unapproved:** Dan could not decide without context. B0030 ab wheel and B0524 salad may be retained as candidates, not inferred approvals. Show every proposed item with narration in its intended place.
5. **Each of four top-level points gets an AI clip and a lower third naming that point:** Working Out, Nutrition, Business, Martial Arts. The original G01–G04 takeaway text is not automatically the requested section title. Use numbered section labels, with exact wording grounded in the spoken point; do not stack redundant takeaway graphics.
6. **Text ideas first:** ten AI clip concepts per point (40 total) supplied in `Handoffs/ro26-ai-clip-concepts-20261016.md` and chat. Dan chooses concepts first. Then create start/end-frame options for the chosen concepts in the next review, with narration context and intended action. Obtain frame approval before generating a few motion variants. No concept or frame is approved merely because it was recommended. No AI generation is authorized by a missing selection.

## Revised first-round deliverable (next review)

- A playable draft of the first 60 seconds AT THE TOP, plus 540p review and 1080p copies. Include the three-photo opening and proposed visuals under actual speech. Use recommended provisional colour/audio; explain pending choices. If an AI insert is still awaiting approved motion, keep presenter footage and identify the pending insert on the page. Do not postpone this limited draft until every graphic is approved.
- Colour-correction options on the SAME source moments, including moving comparison, with a recommendation. Studio standard is a baseline, not an exemption. At least three candidates following the shared procedure.
- Level-matched audio options on the SAME narrated passage, plainly labelled and playable. Include untreated lav and shared-chain baseline in the internal comparison; expose meaningful alternatives with one-click audition and recommend one. Follow shared audio modules and source checks; do not infer quality from meter values alone or add dereverb without the documented audible/measurement basis.
- All proposed graphics, photos and existing clips in timeline order. Each has **Play In Context**: actual narration, intended trim/crop and about 3–5 seconds before and after, including entrance/exit and return to presenter. Four silent seconds or isolated source B-roll are insufficient. Include the approved recap in context without reopening its design.
- Start/end frames for selected AI concepts, clearly separated from actual motion: point name, precise spoken line, before/during/after speech, intended action, duration, and cost estimate. No unapproved motion generation.
- Reuse the Claude review-page standard from `.claude/skills/longform-edit/reference/ro10/page.py` and `review_media.py`, plus shared PRE-RENDER-APPROVAL.md: one floating scrubbable context player, stills/cards feeding it, timeline/beat information and one reply box. Do not repeat the eight-card isolated-asset page.
- Test playback WITH audible narration and seeking in the browser, not only HTTP status or ffprobe. Use the managed range-capable `.claude/skills/_shared/review_server.py`; refresh after changes. Copy review videos >=45 seconds into project `Videos to Review/` as required. Tell Dan explicitly if the URL is local-only.

## Edit/QC reminders

C1768 is studio S-Cinetone/Rec.709 with left-channel lav; confirm through pick_lav. Check loud-word flat-topping and glasses reflections against actual footage. Follow shared HyperFrames integration and audio chain, static horizontal compositions, word-timed graphics, every-join continuity and exact-file preview checks. Inspect the suspected duplicate syllable near provisional output 00:57 and extra utterance near 02:01 using actual audio, preserving words. All times are provisional until the next cut is conformed.
Check current ownership/buildcap; no more than two heavy pipelines. Reuse matches; do not rebuild unrelated assets. Preserve G05’s approved appearance. Final film still requires locked assets, exact-file gates and independent full-candidate review. No upload or public release in this handoff.

## Next action and completion boundary

First read Dan’s subsequent concept picks from this chat or an updated decisions file; do not invent selections. Independent preparation of context, colour/audio comparisons and the draft can proceed while picks are pending. After picks, build the chosen frame pairs and deliver the revised round with everything above. Record exact choices, sources/hashes, review links and pending motion decisions. Update only RO-26’s queue/master/coordination entries. The complete film is not delivered or finalized.

## Ready-to-paste starter

Read `Handoffs/handoff-20261016-ro26-round2-context-and-ai-concepts.md` and execute it with `$long-form-content-edit`. Use my selected RO-26 AI concept IDs from this chat; do not choose for me. Build the revised first-round review with a playable first-minute draft, colour/audio options, the verified three-photo opening, every graphic and clip in narrated context, and start/end frames for my selected AI concepts. Preserve the approved recap. Do not generate motion until I approve its frames.
