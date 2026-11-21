AD (Great Again T sales video). Task name: `Great Again T VSL AD R5`.

# Great Again T VSL (WV-03): round 5 handoff (the graphics round)

Written 2026-11-14 by the round 1 editor (Claude Fable 5.2). **Do not start until Dan has picked a background on the round 4 page.**
Round 1 put the style, take, colour, voice and plan decisions in front of Dan. He answered them on 2026-11-14 (all locked
except the exact background: `~/_edit_work/wv-03/round2-plan/decisions.json`, his words). Round 2, run in the round 1
session, shows five darker background options as intro clips on take 5 (`~/_edit_work/wv-03/round2/`), plus an expanded
AI clip idea menu (`plan/ai_clip_ideas_r2.md`). This handoff is the round after that.

**Dan's process instruction (2026-11-14):** "because this is an important video, I want to make sure that we do a full
graphics review before we render the full video ... proceed conservatively with this edit, keeping in mind that more rounds
of review are probably what makes sense than what we do for unimportant videos like YouTube content." So: small rounds, one
kind of thing per round, nothing built ahead of his approval. He also asked for extra effort on AI clips: many more ideas
and START/END pairs than usual, of which only a fraction go to motion.

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

## Round 2 result (2026-11-14, same session)

- Round 2 page: http://127.0.0.1:9761/ (rebuild: `python3 ~/_edit_work/wv-03/round2/review/build_page.py`). Two decisions:
  the background (1 Dark Kitchen, 2 Gym, 3 Study, 4 Lab, 5 Dark Studio; editor's pick Dark Kitchen, close call) and which of
  44 AI clip ideas to develop into START/END pairs (`plan/ai_clip_ideas_r2.json`, nothing pre-selected).
- Take 5 is keyed: `round2/key/` (`READY.json`). **Use the RIM=3 stage 1.5 setting for the whole film**: it passes the dark-rim
  bar (1.86% vs the camera's own 3.17%; default 3.20% failed by 0.03) and has less light fringe on dark backgrounds. The lens
  window past his cheek still measures see-through and is left clear on purpose.
- Background recipe (light match, skin saturation trim, food glow on dark sets, take 5 point sides): `round2/intro/recipe/`,
  `round2/intro/OPTIONS.json`, sources `round2/intro/assets/SOURCES.md`. Pages must be tested in the app's side pane
  (800 and 1150 px) with a video preloaded in the player (memory `review-page-plays-in-side-pane`).

## Round 3 result (2026-11-14, same session)

- Dan rejected all five round 2 backgrounds: "very dark, untrustworthy, and kind of shady, like a late-night infomercial"
  (his words and their meaning: `round3-plan/decisions.json`). He wants trustworthy, scientific, appropriate, with more
  contrast than the round 1 bright kitchen. Night-time mood (low-key light, glowing strips, heavy darkening) is what to avoid.
- Round 3 page: http://127.0.0.1:9762/ (rebuild: `python3 ~/_edit_work/wv-03/round3/review/build_page.py`). Nine clips on
  take 5: Kitchen 1 Round 1 Kitchen Fixed, 2 Teal, 3 Sage Green, 4 Warm Wood, 5 Slate Gray; Colour 1 Black, 2 Gray,
  3 Forest Green, 4 Deep Navy (flat, no spotlight). Editor's pick: Kitchen 3 Sage Green; runner-up Kitchen 2 Teal. Known
  flaw: Kitchen 4's wood is his skin colour, so his arms blend. Numbers, sources and recipe: `round3/intro/OPTIONS.json`,
  `assets/SOURCES.md`, `recipe/`. The 44 AI clip ideas are on the page again with nothing selected.
- Graphics for a LIGHT or mid-tone kitchen need the light-background treatment for food names and tags (Kitchen 1 used
  round 1's dark names; the others used light names with a soft glow). Re-check card and caption contrast on whichever
  background he picks before building the card families.

## Round 4 result (2026-11-14, same session)

- Dan on round 3: he likes warm wood best ("the wood seems kind of trustworthy"), worries it "does seem a little bit like
  a fake artificial background" to a man in his 50s or 60s, finds green and blue plain colours his favourites but "a little
  weird for the sales video", and says "this is a marketing decision and a business decision, not an artistic decision, so
  base your decision on the data" (`round4-plan/decisions.json`).
- Evidence added (`round4/refs/`, single mid-video frames of his own winners): the TestMax "10 lbs lard" finalized win is a
  presenter in a gray tank top in a real wood-cabinet kitchen; the TestMax and Test Reload pool winners deliver the pitch
  keyed over a teal studio with a lighter centre. V Shred's competing VSL is a plain white studio.
- Round 4 page: http://127.0.0.1:9763/ (rebuild: `python3 ~/_edit_work/wv-03/round4/review/build_page.py`). Seven clips on
  take 5: Wood Kitchen 1 Medium Wood (closest to the lard ad), 2 Walnut, 3 With Window, 4 Dark Backsplash; Teal 1 Teal Studio
  (winners' look, centre toned down), Teal 2 Flat Teal; Light Studio (warm putty). Editor's pick on the data: Teal 1 for the
  film, Wood Kitchen 1 as the first-minute challenger; a cold "where is he standing?" check with two or three men in their
  50s or 60s before locking any kitchen. Every wood kitchen passes the arm-separation rule (CIELAB difference of arm skin vs
  the set beside it at or above about 30; round 3's wood was 22 and failed). Numbers, verdicts, sources, recipe:
  `round4/intro/OPTIONS.json`, `assets/SOURCES.md`, `recipe/`.
- Lesson for briefs: check Dan's own winners' frames BEFORE advising on look. The editor told him to drop plain colours in
  round 3 and had to reverse it once the teal-studio winners were looked at.

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

## Round 5 onward, in order (one review round per numbered group; do not batch them)

1. Record Dan's background pick in `round5-plan/decisions.json`. Re-hash anything he locks. Build in `round5/`, never over earlier rounds.
2. Re-transcribe the whole roll with whisper `medium.en` word timestamps (the small model garbled 840-870 s and
   dropped a line at 1249 s; the medium model is already downloaded), re-time the take map, apply `RECHECK.md`,
   confirm by picture the egg line's four takes and the listed words ("4 million", "Unfortunately", "eleuthero", "Maca").
   Then run `_shared/cut/piccuts.py` and `deadair.py --preset ad --pair` on the final EDL.
3. Key the rest of the chosen takes with `round1/key/CALIBRATION.md` through `keyonce.py` (about 6.5 CPU-seconds a
   frame; roughly 42,000 frames for the film, so plan the queue time). (Superseded by the round 2 result above: RIM=3 settles (a).) `READY.json` has `all_pass: false`
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
7. First minute finished in the chosen style, then the review page: every graphic and clip in narrated context (the full graphics review Dan asked for).
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

> AD (Great Again T sales video). Name this chat "Great Again T VSL AD R5". Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/handoff-20261114-great-again-t-vsl-round5.md`, then run round 5 of WV-03 as that handoff lists, in small review rounds: record my background pick (below), re-time the cut with the stronger transcript, build the study-card and offer-card designs and every graphic as stills on the real frame in the look I picked, make the AI clip start and end pairs for the ideas I selected, and send me the graphics review page before anything moves or the rest of the roll is keyed. Use /ad-edit. My round 4 answers: [paste the reply box from the round 4 page]
