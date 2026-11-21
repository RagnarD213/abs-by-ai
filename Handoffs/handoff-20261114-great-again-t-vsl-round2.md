AD (Great Again T sales video). Task name: `Great Again T VSL AD R2`.

# Great Again T VSL (WV-03): round 2 handoff

Written 2026-11-14 by the round 1 editor (Claude Fable 5.2). **Do not start until Dan has answered the round 1 page.**
Round 1 decided nothing by itself: it put the style, take, colour, voice and plan decisions in front of Dan.

## State

- Round 1 review page: http://127.0.0.1:9760/ (managed review service; rebuild with
  `python3 ~/_edit_work/wv-03/round1/review/build_page.py`). Twelve decisions; Dan's reply goes in
  `~/_edit_work/wv-03/round2-plan/decisions.json` with his exact words before anything is built.
- Work folder: `~/_edit_work/wv-03/` on the internal drive (the Extreme and the Seagate were unplugged on 11-14;
  the roll was pulled from `gdrive_backup:` and matches the sidecar's content key size). The house location for a new
  job is `~/Projects/_edit_work/<JOB>`; this one stays where it is.
- Source: `~/_edit_work/wv-03/src/C1903.MP4` (read-only). Portrait 2160x3840 after autorotate, 29.97, S-Cinetone.
- Queue: WV-03 `delivered` for round 1 review. Edit slot released for review; `editcap.py acquire WV-03` before production.
- Paid spend so far: $0. Nothing uploaded. Nothing approved.

## What exists (all under `~/_edit_work/wv-03/`)

| What | Where |
|---|---|
| Final script with Dan's bracketed cues | `script/vsl_script_final_doc.txt` (Google Doc `1CmK7ZG45x-p7mXATjvlWzuUpvlr7AQMHUbiQcdMYCFI`) |
| Take map, 268 lines, all takes and a chosen take per line | `plan/take_map.json`, `plan/take_map.md` |
| Take map corrections (two "missing" lines found, four takes of the egg line) | `plan/recheck/RECHECK.md` |
| Asset inventory | `plan/asset_inventory.md` |
| Creative direction | `plan/VISUAL_DIRECTION.md` |
| Full visual plan, 110 items with times, copy, sources, specs, verified studies | `plan/visual_plan.json`, `plan/visual_plan.md` |
| House key calibrated to this roll; plates for H6 (hook take 6), S1 (first minute continuation), H1 (hook take 1) | `round1/key/` (`READY.json`, `CALIBRATION.md`, `plates/`) |
| Colour candidates and recommendation ("matched") | `round1/look/LOOK.json`, `colour_*.jpg` |
| Voice candidates, blind ranking, recommendation (house bass lift) | `round1/look/VOICE.json`, `voice_*` |
| Five intro style drafts and their recipe | `round1/intro/` (`OPTIONS.json`, `recipe/`) |
| Hook take reel (six takes, raw green) | `round1/takes/` |
| Style research | summarized on the review page ("What the research found") |

## Round 2, in order

1. Record Dan's answers. Re-hash anything he locks. Build in `round2/`, never over `round1/`.
2. Re-transcribe the whole roll with whisper `medium.en` word timestamps (the small model garbled 840-870 s and
   dropped a line at 1249 s; the medium model is already downloaded), re-time the take map, apply `RECHECK.md`,
   confirm by picture the egg line's four takes and the listed words ("4 million", "Unfortunately", "eleuthero", "Maca").
   Then run `_shared/cut/piccuts.py` and `deadair.py --preset ad --pair` on the final EDL.
3. Key the rest of the chosen takes with `round1/key/CALIBRATION.md` through `keyonce.py` (about 6.5 CPU-seconds a
   frame; roughly 42,000 frames for the film, so plan the queue time). `READY.json` has `all_pass: false`
   for two reasons, both to settle on the three round 1 pieces BEFORE the long run: (a) dark rim a hair over this
   camera's own on H6 (3.18% vs 3.11%) and H1 (3.76% vs 3.43%): next try is stage 1.5 with `RIM=3` on the cached
   stage-1 frames, written as `_r2` plates; (b) the lens window past his cheek measures as see-through (H6 1,533 px);
   forcing it solid prints a grey slab (`round1/key/stills/lens_forced_solid_H6.jpg`), so it was left clear: show Dan
   the crop and take his call. Specks were a measurement artefact of lossy check videos (lossless shows none). No
   `_r2` plates exist. Do not raise a threshold.
4. Build every graphic in the chosen style as a still on its real frame, then moving in context (visual plan items;
   study-card and offer-card families first so Dan locks one design). Soft Blue Light HyperFrames. No em dashes in copy.
5. AI clips: START and END pairs for the ideas Dan picks (blind Codex and Google pairs, frame gate, fresh
   `frame-reviewer`), Google subscription first. Motion only after he approves a pair. Cap $5 paid unless he raises it.
6. Fetch and grade the stock and owned clips; the 14 items marked "on the unplugged drive" need the Extreme back.
7. First minute finished in the chosen style, then the round 2 page: every graphic and clip in narrated context.
8. Full render only when nothing is pending; gates, watch pass, a fresh `ra-reviewer`, then deliver.

## Known traps from round 1

- Stage 1 can decode one frame past the end of a piece (S1 gave 1225 of 1224). The extra frame is the one after the
  piece; quarantine it, do not relax the count check. Details in `round1/look/BUILD_LOG.md`.
- The locked long-form "warm" grade is too bright and orange on this roll. "matched" is the rebalanced version.
- `Videos to Review/` is a link to the unplugged Seagate; copies were skipped. Re-run the page build once it is back.
- Dan filmed no props. Every food, the bottle "in his hand" and the tablets are inserts.
- The live store price is $47; never show a store screenshot for the $97 line. Use the price card.
- The label source file carries a home address panel: facts-only crop for any Supplement Facts shot.

## Starter prompt (Claude: Opus 5.5, high effort)

> AD (Great Again T sales video). Name this chat "Great Again T VSL AD R2". Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/handoff-20261114-great-again-t-vsl-round2.md`, then run round 2 of WV-03 exactly as that handoff lists: record my round 1 answers (pasted below), re-time the cut with the stronger transcript, key the remaining takes with the round 1 calibration, build every graphic and clip in the style I picked as stills then moving in context, make the AI clip start and end pairs, finish the first minute, and send me the round 2 review page. Use /ad-edit. My round 1 answers: [paste the reply box from the round 1 page]
