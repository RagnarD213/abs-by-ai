# WV-01 round 5: final creative lock before full A/B assembly

Prepared 2026-09-26 from Dan's round-4 review. Recommended model: **GPT-6 Astra, High**. Execute with **$abs-edit-organic**, adapted to this 16:9 website VSL. This handoff supersedes the pending decisions in the round-4 handoff. It records work for the next task; no round-5 media has been generated or rendered in this documentation task.

## Goal and boundary

Make one focused final review package for the remaining changes, preserving everything Dan approved. He considers the first three minutes locked apart from the specific revisions below, the selected SCAN opening and replacing the approved B01 frame placeholder with its motion. Do not redesign the opening or ask him to reapprove accepted components.

Best next step: finish the remaining photo/layout/G03 revisions, generate motion from the approved J1/J2/B01 storyboards, and show those moving clips in their intended speech context. Then, once the outstanding graphics and clips are locked, assemble complete A and B and perform final checks. Do not make another broad style board or full placeholder film. No publishing, website replacement, app deployment, new dashboard row or unattended dispatcher launch.

Read project instructions, `.claude/skills/_shared/VIDEO-RULES.md` in full, `GRAPHICS-STANDARDS.md`, `PRE-RENDER-APPROVAL.md`, the invoked skill and `Handoffs/video-editing/00-RULES.md`. Read the current board and WV-01 queue row. These latest explicit decisions override older background-free-list instructions.

Project root **R**: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Work root **W**: `/Volumes/Extreme/_edit_work/wv01-edit`.
Build in new **W/round5/**. Preserve round-4 reviewed files unchanged.

Read `W/STATE.json`, `W/round5-plan/decisions.json`, `W/round4/QA.md`, `W/round4/review/source-register.json` and `W/round4/review/exact-timings.json`. Review page: `http://127.0.0.1:8766/round4/index.html`. Server: `W/round3/recipe/serve_review.py`, with byte-range seeking and video `preload="none"`.

## Settled approvals

| Item | Round-4 decision and scope |
|---|---|
| Opening structure | Approved apart from the walking flash, photo changes, selected SCAN and approved B01 motion replacement. Preserve spoken edit, placement and rhythm otherwise. |
| W2 / T2 | Locked crops: `3552:1998:144:162` / `2608:1466:616:184`. Fixed camera compositions. |
| Color / audio | C LUT `W/round2/recipe/grade-C.cube`; B audio approved. Reuse exact accepted opening AAC where timing remains unchanged. No redesign. |
| SCAN | Selected and locked as opening. Use **W/round4/motion/SCAN-readable.mp4**, not raw SCAN with imperfect lettering. H2 is superseded as opening; no repeat comparison. |
| Early exercise | Dumbbell rows approved. Remove only the walking tail. |
| C01 | Finished motion approved. Reuse `W/round4/motion/C01.mp4` with disclosure. |
| J1 / J2 | Round-4 storyboards, approved endpoints and new intermediates approved. Proceed to real motion using those exact images/actions; no new frame-permission request. |
| B01 | Round-4 three-cyborg-coach start/end pair approved. Proceed to real motion; no new frame-permission request. |
| P05-P09 | Consistent iPhone shell and all five contents approved, including final P06 corner fix, tracked calories and complete P08 sleep sequence. Reuse exact round-4 previews/recipe. |
| G01 | 165 bars with three highlighted approved. |
| G-simple / One App | Phone-only treatment approved. No new panel or heading. |
| Motivation / numbered points | Both approved. Keep exact #1 copy and the four subsequent numbered titles. |
| Prior approvals | Before photograph, both family photos, full YouTube archive proof, exact P04 goal generation, G-oldwork and G-preferences remain approved. |

Do not confuse frame approval with final-film approval. New J1/J2/B01 motion should receive editor QA and appear in the final contextual review, without reopening the approved imagery. G03 is specifically rejected and needs changed frames first.

## 1. Remove the five-frame walking flash

Dan: "just keep the clip of him doing the dumbbell rows" and "kill that little clip of the walking that snuck in after the dumbbell rows in the intro".

The error is verified inside `W/round3/previews/P06-early-existing-option.mp4`, not a separately named timeline insert. It was missed by the earlier broad review. At 30000/1001 fps:

- Current insert: output frames `[672,756)`, 22.4224-25.2252 seconds.
- Local frames 0-78 show the row. **Local frame79 is the first walking frame**, corresponding to output frame751 at25.0583667 seconds. Walking occupies the last five frames79-83.
- Shorten the picture insert to `[672,751)`, 79frames / 2.6359667seconds. Return directly to Dan at output frame751, using the corresponding existing presenter source frame1064 from C1697. Preserve the current soundtrack and total timeline length. Do not freeze or stretch the row to fill those five frames.
- Verify the cut frame by frame, including the source immediately before it. Update the in-context audition so it cannot retain the old tail.

Evidence: `W/round5-plan/references/early-tail-exact-frames.jpg` and `early-tail-inspection.jpg`. Keep complete speech; this is a picture-only correction.

## 2. Two horizontal pool photographs with natural backgrounds

Replace the two studio horizontal results near0:20 with Dan's attached pool photographs, one after another. Preserve the natural pool/trees background here. White backgrounds apply to the separate vertical triptych below.

Exact references under `R/photos/finalized social media photos/`:

1. `photo-180_FINAL_PRIMARY copy.png`, attached crop, 2051x1676. The matching wider finalized original **`photo-180_FINAL_PRIMARY.jpg`**, 4096x2747, was located and visually checked. Prefer a landscape composition from this original if it retains complete hair and abs and looks good.
2. **`photo-97_FINAL_PRIMARY.jpg`**, attached flag/pool photograph, 4096x2747.

Dan authorizes the attached crop or a wider landscape crop from the original. Do not synthesize extra background or change his physique/expression. Keep the locked Soft Blue Light presentation, sequential rhythm and truthful real-photo disclosures clear of face/abs. Existing slot is output frames569-672 /18.9856333-22.4224seconds. Keep the separate200-pound before beat unchanged.

## 3. Three vertical portraits, all on white

Retain the three-picture layout around2:27 and the left portrait. Replace the other two sources:

- **Left remains:** `R/photos/finalized social media photos/studio-blue-11_FINAL_PRIMARY.jpg`.
- **Muay Thai portrait:** use the exact photo from Dan's installed channel banner, **studio-blue-89**, confirmed by `Handoffs/handoff-20260916-install-youtube-channel-banner-codex.md`. Full portrait: `R/photos/finalized social media photos/studio-blue-89_FINAL_PRIMARY.jpg`. Existing cutout: `_cutouts/studio-blue-89_CUTOUT.png` in the same directory. Use the full portrait for this layout, not the banner's tight crop.
- **Jeans portrait:** select the real finalized jeans photograph where his abs look most ripped, preserving a natural expression. Compare full-size candidates before choosing. Useful search seeds from photo manifests: studio-blue-177, studio-white-32, studio-white-25 and studio-white-34. These are candidates, not a preapproved winner. Avoid the AI environment composites.

Replace the background of **all three** with white, including the retained left photo. Preserve actual body, face, clothing and proportions. Prefer existing clean cutouts if available; if an AI background-only edit is needed, use imagegen and verify the subject against the original. No additional body retouching. Keep complete heads and abs, tall consistent frames and the real-photo disclosure. The surrounding three-card graphic retains the approved style; do not infer a request for an all-white full-screen layout.

Existing slot: frames4367-4491 /145.7122333-149.8497seconds. Show the revised triptych in context in the final review.

## 4. G03: realistic phone use with screen insets

Dan rejected both round-4 G03 endpoint interpretations because the phones are oversized and the character appears to look at their backs. Preserve the underlying workout, food and sleep behaviors across weeks/months and exact CTA **`Try AbsByAI free for 7 days.`** Change the staging in every scene/panel:

- A normal-sized phone, held or positioned believably, with its screen facing the character and his eyes directed at that screen. Hands, gaze, phone plane and perspective must agree. The audience may see the phone's back or side if that is the honest camera angle; the character must see the screen.
- Add a separate readable screen graphic at the **top right of each corresponding scene/panel**, showing what he is seeing: workout guidance, food/logging results, or sleep data. The inset is an editorial display, not a giant physical phone. Keep it clear of his head, action, calendar and CTA.
- Use the now-approved P05/P06/P08 visual language/content where appropriate. Match the inset to the physical action. Do not show different content on the physical screen and inset or impossible mirrored orientations.
- Preserve the same prospect, realistic anatomy, ongoing habits and visible progression from Week1 to Month3. Trial length remains distinct from progress over months.

Current rejected references: `W/round4/frames/G03-{start,end}.png`. Re-read actual later narration in `W/drafts/PLAN-{A,B}.json`, especially workout/food use and months-later pool-result speech. A coherent short sequence may communicate this more clearly than three crowded simultaneous panels; retain all three functions and show the proposed layout explicitly.

Prepare corrected START/END frames and intended action before motion. Send that small changed-frame batch early while continuing the approved J/B motion and other revisions. New G03 frames require Dan's approval before generation. Once received, generate and inspect motion for the final contextual review. If approval has not arrived, deliver the finished independent work with G03 honestly pending; do not interpret elapsed time or "one final round" as approval of unseen frames.

## 5. Standard left-third text card, with one background only

Dan clarified his earlier "remove the background" request. **Restore a rounded blue rectangle directly behind the text. Remove only the secondary full-height blue field that ran to the top/bottom/left screen edges.** Text floating directly on the camera scene is rejected because it is hard to see.

Use this as the standard left-third **text/list** format: one content-sized Soft Blue Light rounded blue/glass card, readable large bold type and comfortable padding, visible margins around the card, and the ordinary camera background visible outside it. No second field behind the card. Keep Dan fixed and safely centered in the remaining right space with full moving arm/hair clearance.

- **G02 five benefits:** retain its substantive five bullets; restore only the local rounded card.
- **G-lagging:** apply the same card. Replace `FIND THE GAP` with exactly **`How AI customizes a plan just for you.`** Wrap the heading deliberately at a readable size. Preserve the approved list content unless space requires sensible reflow.
- Audit other unapproved left-third text graphics for the same issue. Preserve already approved G-oldwork/G-preferences content and accepted phone-only One App. This clarification does not add panels to the approved iPhones or redesign the lower thirds.

Dan's screenshot is preserved at `W/round5-plan/references/Dan-left-third-feedback.png`; it shows the rejected floating G02 text. The shared graphics standard has been updated with this clarification so another task does not repeat the old interpretation.

## Final review package and next stage

Deliver one consolidated round-5 page emphasizing only changes:

1. Revised locked opening with SCAN, corrected row-only tail, both photo replacements and approved B01 motion when available. Reuse unchanged audio/timing where possible.
2. Revised horizontal pair and white-background triptych in context.
3. Revised G02 and custom-plan cards with the spoken sentence before, speech under and sentence after each. Reuse full-film source maps, not silent generic plate only.
4. Newly generated J1/J2/B01 motion in its planned narration context; approved storyboard stills may be collapsed as references.
5. Corrected G03 frames, then motion after their approval, with a clearly stated remaining decision if still pending.
6. A compact list of locked components, not repeated approval questions for P05-P09/G01/One App/lower thirds/C01/SCAN.

Do not claim all graphics in the full film are approved merely because a representative template is. Reconcile the full A/B planned graphic IDs against the accumulated specific approvals; show only any genuinely missing item alongside the final batch. After the package is locked, render full films from approved components, then editor full picture/audio review and one independent complete-candidate review. No extra design round is planned; fix actual motion defects if they arise.

Preserve `W/selection/EDL-{A,B}-REPAIRED.json` and current `W/drafts/PLAN-{A,B}.json` until the approved opening timing is conformed. All **six B callbacks** remain mandatory. The prior21-frame opening pause correction must propagate carefully into full maps/subtitles when assembling the complete films.

## Records, QA, costs and restart

- Round4 opening master: `W/round4/sample/DRAFT - WV-01 round 4 - opening.mp4`; review540p adjacent; SRT and word map adjacent. Duration188.354833seconds,5645frames. Both exact-file audio gates passed; zero confirmed repeated-speech/high-unresolved findings. These are old-file results, not new-file stamps.
- Current audio selftest passed09-26. Prior full A/B silence failures and historical corpus ds17 artifact mismatch/NOT MEASURED gaps remain unresolved. Do not relax gates or rerun the entire expensive corpus blindly. Do not commit unrelated shared gate changes.
- Reuse `round4/recipe/graphics.py`, `build_opening.py`, `numbered_lowers.py`, `package_assets.py`, `records.py` as references, but write revised recipes under round5. Fresh cache keys must include crop/filter/grade/source hashes. The old cache omitted crop/filter details.
- Never exceed two simultaneous local video pipelines across tasks. Dispatcher remains paused. Use supported parked queue states; frame approval alone does not authorize unattended full assembly.
- Known cumulative motion estimate through round4: **$0.615374** against the existing $5 video-generation allowance. Round4 QC **$0.283571**, round3 QC **$0.35275**, earlier QC **$2.167282**, older failed-call upper bound **$0.1333** remain separate. **Thirty prior built-in still calls have unreported charges**, not zero. No paid call occurred in this handoff task. State the next batch estimate before running; track every retry. Do not repeat a request to approve unchanged J1/J2/B01 frames.
- No independent reviewer has reviewed a complete placeholder-free film yet. Creative approvals are recorded with hashes in `W/round5-plan/decisions.json` and the shared scoped corpus. Semantic checks are pending; no new automated PASS claimed.
- Private media/recipes remain on SSD and local ref `codex/video-trial-plan-private`. Public handoff/status changes may be committed/pushed separately without app deployment. No new task or dashboard row was automatically created by this handoff.

**Exact next action:** read the decision manifest, verify locked asset hashes, begin G03 revised frames and the remaining photo/card changes, then generate the already-approved J1/J2/B01 motion and prepare the final contextual review.

**Starter prompt:** Execute `Handoffs/handoff-20260926-wv01-round5-final-creative-lock.md` with `$abs-edit-organic`. Preserve all round-4 approvals. Lock SCAN, remove the five-frame walking tail, use the specified pool photos and white-background portrait trio, fix G03 phone perspective/insets, and restore the single rounded blue left-third card. Generate motion from approved J1/J2/B01 storyboards and deliver one final contextual review before full A/B assembly.
