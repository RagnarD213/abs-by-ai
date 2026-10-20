# Boring Abs At 40 LFC R2

Ready to start, October 20, 2026. RO-27, “It's Boring, But It Got Me Abs At 40”, 10/15 shoot C1769–C1770. Release target Sunday November 15, 2026; not uploaded or scheduled. Current chat remains R1. This is a substantial new round, so the October 18 continue/handoff rule applies. Context percentage is unavailable; no percentage was inferred.

## Exact next action

Read `round2-plan/decisions.json` and the current head/hair rule at the top of VIDEO-RULES.md. Re-hash locked references. Start a new `round2/` folder. Calibrate hair-top measurement on C1769/C1770 and prove a safe static wide/tight pair before rendering the revised opening. In parallel editorial work, reconcile the existing AI clip inventory and revise A01–A04 START/END pairs. Deliver one checked R2 review page with the corrected first minute, all existing AI clip choices, and revised pairs. Do not build a full film or generate new motion yet.

## Files to read and reuse

- Project `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/CUT-CONTINUITY-QC.md`; Codex `$long-form-content-edit`.
- `Handoffs/video-editing/RO-27-its-boring-but-it-got-me-abs-at-40.md`, `Docs/SHOOT_1015_FOOTAGE_REPORT.md` and `Docs/RO27_R1_RECEIPT_20261017.md`. Current choices override obsolete studio no-options prose.
- `/Volumes/Extreme/_edit_work/ro27/round2-plan/decisions.json` contains every request, exact user words, affected file hashes and authorizations. `WORK_PACKET.json` repeats the actionable packet. Two original screenshot attachments are preserved beside it.
- `/Volumes/Extreme/_edit_work/ro27/round1/`: `build_opening.py`, `opening_cut_map.json`, `build_options.py`, `plan_resolved.json`, `later_plan_resolved.json`, `cards_plan_resolved.json`, `asset_ledger.json`, `build_contexts.py`, `build_ai_contexts.py`, `make_page.py`, `ai/` and `review/`.
- R1 page is http://127.0.0.1:8932/. Current managed server caches files locally. Preserve its repair: `review/review-controls.js`, `review-controls.css`, default source, hide/show, explicit seek, ±5s, and injected `/__review_player.js` recovery. Re-run maintained `review_server.py` for R2 once ready. Do not overwrite R1 assets. Test silently, leave paused with normal audio. Preserve any user notes before navigating/reloading.

## Locked choices

Colour **C Richer Colour**, voice **B Warm Bass**. Do not ask again. Grade: `eq=contrast=1.045:brightness=0.012:saturation=1.17`; apply before graphics. Voice B exact chain is recorded; use left lav, not silent right channel. Source lav has flat-topped loud words; retain clean takes and verify actual output. Recompute output normalization rather than blindly copying gain.

- `colour-C`: `/Volumes/Extreme/_edit_work/ro27/round1/options/colour-C-Richer-Colour.mp4`, SHA-256 `b1b926a24dceba1b2113589c8febcc861d40aeadb7c27b45b9c8ae1638808617`
- `colour-C`: `/Volumes/Extreme/_edit_work/ro27/round1/options/colour-options.json`, SHA-256 `e49ec705079f6a72891c3860a92791534786264c2ee9781009d1b8912e9d24c1`
- `voice-B`: `/Volumes/Extreme/_edit_work/ro27/round1/options/voice-B-warm-bass.mp4`, SHA-256 `16189e9aa2d27dd082bdd4a5c69b0369ccfb59e11b04b800e8b8b65cf9b1aae4`
- `voice-B`: `/Volumes/Extreme/_edit_work/ro27/round1/options/voice-B-warm-bass.wav.voice_chain.json`, SHA-256 `c9a301c1b7cd44130f0f66dbdb8515fc023bae2f8059f7ecd79db21fea10ce18`

## Requested R2 changes

1. Opening: Dan wants an existing AI clip of himself fasting, and to see **all AI clips already made** before choosing. Present fasting/AI-Dan candidates first, plus a complete searchable/browsable existing-AI gallery rather than silently limiting him to a shortlist. Snapshot currently has 194 catalogued AI clips; this is not proof all ever-made clips are registered. Reconcile recent clean keepers with catalog and approved project registries. Identify missing/offline/defective assets honestly; do not present rejected defective takes as keepers. Verify identity from actual footage, not a tag. The fasting search returns A0169 (laptop/black coffee time lapse), A0171 (empty plate excuse), A0174 (beer while fasted), but all three are tagged `other-man`, not confirmed AI-Dan. Do not relabel them as Dan. Check recent fasting work, including SL-08, for existing generated versions without editing another task's files. No new fasting generation is requested. Gallery selection must not auto-insert a clip. Once picked, show exact trim on opening narration with surrounding context.
2. Framing: more headroom in both wide and tight, entire hair/head visible throughout. Screenshots show failures near output 0:22 and 0:29. Check all presenter spans and all contextual returns, not merely those two frames.
3. A01 Neighbor Peek: elderly woman foreground; recognizable AI-Dan in background behind wall, nudity implied but fully concealed. Preserve privacy-wall spoken joke. New START/END pair required.
4. A02 Skipped Gym Day: keep all else. Calendar 💪 marks three days each week for first two weeks, then two days, then one in final week on final day. This is the practical interpretation of “1 the last day”; make layout explicit on review card. Keep the calendar physically consistent and readable in both frames.
5. A03 Meal Prep Rescue: keep all else; varied meals in different containers in both START and END. Preserve identity, framing, fridge hinge and container continuity.
6. A04 replace pastry temptation with mildly overweight ordinary adult man drinking beer and watching American football with adult friends. No exaggerated obesity. New START/END pair, linked to the weekend line.
7. Remove A05 Chip Spill and A06 Motivation Is Asleep. Use presenter there. No substitute gags requested.

A01–A04 are approved concepts with changes, **not approved revised frames**. `motion_authorized=[]`; `new_frames_before_motion=[A01,A02,A03,A04]`. Generate and check revised still pairs, then get Dan's approval before Flow motion. No unrelated graphic/real-insert approval should be inferred from silence. Preserve their existing treatment and carry pending status accurately.

## Why the crop failed and Claude comparison

RO-27 `build_opening.py` applies W `3440:1935:200:112` and T `3000:1688:420:236` without measured hair anchoring. `verify_review.py` checks links, streams and media counts, not headroom. The existing graphic face-clearance tests and join checks are not hair checks. No rendered hair report was located in this R1 work directory. Prior quality statements must not be treated as framing approval.

Claude's current implementation supplies the missing tests:
- `.claude/skills/longform-edit/SKILL.md`, framing standard near line 1681: anchor crop to actual minimum hair top minus 4% crop height, inspect native proof, gate delivered frames.
- `.claude/skills/longform-edit/reference/ro10/hair_first.py` and `haircheck.py`: Vision person mask every 0.25s, report top clearance and worst moments.
- `.claude/skills/website-video/reference/recipe/hairdet.py`: distinguish real hair top from lower forehead/skin boundary; validate detections against native source.
- Same folder `hairgate.py`: minimum 20px clearance at 1080 scale, tight/loose proof images, plus an independent EVERY-FRAME top-edge check. Its background thresholds are specific to the website door; calibrate for this studio, do not blindly transplant them. Historical ad-edit path is stale.

R2 must include exact-file hash, coverage, minimum clearance, worst timestamps, native proof frames of tallest posture in EVERY hold and both sides of every join, and moving review. Invalid/missed detection is unresolved. Prove regression catches the rejected R1 examples and passes corrected R2; block publishing the review page if clipped or unverified. Export conversion cannot silently reintroduce a crop. Apply shared horizontal no-motion rule: fixed framing per hold, no tracking. If raw footage itself cuts hair, disclose that and use an intact take; do not manufacture hair or claim a crop restored it.

The new shared VIDEO-RULES head/hair section records this as a mandatory pre-review check for Claude and Codex. It is a rule update, not proof R2 has passed; no R2 picture has been rendered yet.

## Preserve and verify

Keep all original cuts/words unless a demonstrated fault requires change. Existing opening: seven selected C1769 spans in opening_cut_map.json, six joins near 21.62, 23.62, 26.73, 43.81, 48.58, 56.69s, 66.199s delivered length. Cuts already removed failed starts, repeated arm phrase and incorrect action-step take; do not remove again. Preserve complete words/breaths and meaningful wide/tight differences after moving crops higher.

R1 exact audio gate passed (-14.30 LUFS/-2.10 dBTP) for A; this does not validate a B rebuild. R1 still-pair checks covered original hashes only; all changed frames need new checks. R1 hair framing is rejected. No new motion, full film, captions, final independent full-candidate review, upload or schedule exists. New review needs exact audio/visual checks, full moving inspection and all required independent frame checks. Actual listening limitations must remain explicit.

Costs: this intake/audit generated no images or motion and incurred $0 provider-generation charges. Historical imagegen cost/editor usage unavailable. Use subscription image generation and Google Flow by default after frame approval; no paid motion without Dan's explicit rush instruction or further authorization under current rules. Never buy credits automatically.

## Starter prompt

LFC. Name this task `Boring Abs At 40 LFC R2`. Execute `Handoffs/handoff-20261020-ro27-round2-headroom-and-ai-revisions.md` with `$long-form-content-edit` and current `.claude/skills/_shared/VIDEO-RULES.md`. Read the saved decisions first. Fix and prove hair/headroom in every wide and tight shot using Claude's source-calibrated checks, apply richer colour C and warm-bass voice B, show all existing AI clips with fasting/AI-Dan options first for my opening choice, revise A01–A04 frames exactly as recorded, and remove A05–A06. Deliver a checked R2 review page. No new AI motion or full-film render before required approvals. Release target Sunday November 15.

Recommended model: GPT-6.1 Sol, high effort, the newest available GPT model in this client's tool inventory on October 20. This follows the current AGENTS.md newest-model rule, overriding the older skill's GPT-6 pin.
