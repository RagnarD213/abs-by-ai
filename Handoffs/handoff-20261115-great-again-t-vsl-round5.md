AD (Great Again T sales video). Task name: `Great Again T VSL AD R5`.

# Great Again T VSL (WV-03): round 5 handoff

Written 2026-11-15 by the round 1 to 4 editor (Claude Fable 5.2), at Dan's request ("Give me a handoff document for the
next round"). **Model: Claude Opus 5.5, high effort** (a video stays on the AI it started on). Ready to fire.

This is a ~25 minute direct-response sales video for the Great Again T men's testosterone supplement: one native 9:16
phone video (1080x1920, 29.97), Dan on green screen in a light tank top, roll C1903 from the 11/13 shoot. No 16:9.
Dan calls it "a very important video" and wants more, smaller review rounds than a content video.

## 1. What round 5 delivers (Dan's words, 2026-11-15)

> "Okay, let's go with number one: the medium wood kitchen ... medium wood kitchen number one is our choice."
> "For the AI clips, it's too time-consuming to go through all those descriptions and too hard to say what you're going
> to generate ... give me start and end frames for all clips" [next round].
> "also I want to see the first 3 minutes in the Teal Studio next round."

So the round 5 review page carries exactly three things, and nothing else is rendered:

**A. The first 3 minutes of the film, finished to draft standard, in two backgrounds from one cut.**
   - Version 1: **Wood Kitchen 1 (Medium Wood Kitchen)**, the look he chose for the film.
   - Version 2: **Teal Studio**, which he asked to see for the first 3 minutes and wants to test later
     (memory `gat-vsl-teal-studio-test-later`).
   - Same EDL, same key, same grade, voice, captions and graphics; only the background plate (and each plate's own light
     match and food-name treatment) differs. Key once, composite twice.
   - My reading of "the first 3 minutes in the Teal Studio": built literally, plus the kitchen version because it is the
     film's look. Say this on the page in one line so he can tell me if he wanted only one.

**B. START and END frame pairs for ALL 44 AI clip ideas**, as pictures he can pick from. He will not read descriptions
   again: the page leads with the two pictures, and the text is one short line. No motion until he picks pairs.

**C. Nothing else.** The full graphics review of the rest of the film (every card after 3:00 as a still, then moving)
   is a later round, still required before any full render. Do not key or build past the first 3 minutes.

## 2. Locked decisions (do not reopen; his exact words are in the decisions files)

| Decision | Locked choice | Record |
|---|---|---|
| Category and format | AD; one native 9:16 VSL | `Handoffs/video-editing/WV-03-great-again-t-vsl.md` |
| Opening take | Take 5 (he points up) | `round2-plan/decisions.json` |
| Background | Wood Kitchen 1, Medium Wood Kitchen (real photo, Unsplash, Sanju Pandita) | `round5-plan/decisions.json` |
| Later test | Teal Studio, background only | `round5-plan/decisions.json`, memory |
| Colour | "Matched" foreground grade | `round1/look/LOOK.json` |
| Voice | House bass lift | `round1/look/VOICE.json` |
| Foods, bottle, tablets | Inserts (real photos, bottle art); nothing was filmed in his hands | round 1 |
| Root pictures | AI stills with the AI label | round 1 |
| "Links below this video" | A stand-in studies page now, the real page later | round 1 |
| Study cards | At the bottom, Dan above | round 1 |
| Captions | Burned in for the whole film | round 1 |
| CTA bar | Always on from the first call to action | round 1 |
| Egg line (four takes) | Editor picks | round 1 |
| Process | Small rounds; full graphics review before any full render | `round2-plan/decisions.json` |

All paths below are under `~/_edit_work/wv-03/` on the M6's internal drive unless they start with `Handoffs/`, `Docs/` or
`.claude/`. On resume run `python3 .claude/skills/_shared/editroute/resume.py check WV-03` (the job lives on the M6) and
`python3 .claude/skills/_shared/editcap/editcap.py acquire WV-03 --title "Great Again T VSL" --type AD` before production.

Locked files (re-hash before building; record expected vs actual):

| File | SHA-256 |
|---|---|
| `round4/intro/assets/bg/W1.png` (wood kitchen plate) | `1e201feab2f175cbc274cc7f4376f88292229d3a55ead74c9ae9896e72e3ef22` |
| `round4/intro/assets/bg/T1.png` (teal studio plate) | `ff4d5b89f1987ab4b1e863934c3bda67cce6d047506b52278220764b7f9df34c` |
| `round2/key/plates/H5_fg_straight_alpha_ungraded_rim3.mov` (take 5, keyed) | `873e937c27a47c761ad8aa1d9fcfb76d72c1010f39d7f9ac11c8aed6dfa19996` |
| `round4/intro/DRAFT - Great Again T VSL R4 - Wood Kitchen 1 Medium Wood Kitchen.mp4` (the clip he approved the look on) | `8f13d43cf6a8f5790d156d44d2226dcb246397667f5ed1af457bd6722a1cea19` |
| `round4/intro/DRAFT - Great Again T VSL R4 - Teal 1 Teal Studio.mp4` | `99db338bea847e4463058386d3c71fcfaaf6c2811ac01f01f98b5770a45f2c16` |

## 3. What exists

| What | Where |
|---|---|
| Source roll (read-only), portrait 2160x3840 after autorotate, S-Cinetone | `src/C1903.MP4` (pulled from `gdrive_backup:`; the drives are on the M2) |
| Final script with Dan's bracketed cues (spoken words win) | `script/vsl_script_final_doc.txt` (Google Doc `1CmK7ZG45x-p7mXATjvlWzuUpvlr7AQMHUbiQcdMYCFI`) |
| Take map: 268 lines, every take, a chosen take per line, film times | `plan/take_map.json`, `plan/take_map.md` |
| Take map corrections (two "missing" lines found; four takes of the egg line) | `plan/recheck/RECHECK.md` |
| Full visual plan: 110 items with times, copy, sources, card-family specs, 14 verified studies | `plan/visual_plan.json`, `plan/visual_plan.md` |
| 44 AI clip ideas with START, END, action, line, film time, rating, first-eight shortlist | `plan/ai_clip_ideas_r2.json`, `.md` (rebuild: `plan/build_ai_clip_ideas_r2.py`) |
| Asset inventory, creative direction | `plan/asset_inventory.md`, `plan/VISUAL_DIRECTION.md` |
| House key calibrated to this roll | `round1/key/CALIBRATION.md`, `round1/key/recipe/`, `round1/key/chain_piece.sh`, `round2/key/` |
| Keyed pieces: H5 (take 5 hook, RIM=3), S1 (first-minute continuation, default rim: redo stage 1.5 with RIM=3 from cached stage-1 frames), H6, H1 | `round2/key/plates/`, `round1/key/plates/`, `READY.json` in each |
| Intro recipe that built the approved clips (compositor, light match per plate, captions, food cut-outs, checks, separation measures) | `round4/intro/recipe/` (README first), `round4/intro/OPTIONS.json`, `round4/intro/assets/` |
| Review pages and their generators | rounds 1 to 4: http://127.0.0.1:9760/ to :9763/, `roundN/review/build_page.py` |
| Dan's decisions, every round, in his words | `round2-plan/` to `round5-plan/decisions.json` |
| Reference frames of his own winning ads | `round4/refs/` |

## 4. Part A: the first 3 minutes (kitchen and teal)

The first 3:00 of film covers script lines L001 to about L038: the food-swap hook, "not just my opinion / links below",
the problem and agitation passage, "why is this happening", high T versus low T, and "about 1% a year"
(take map rows up to 3:03; it will shift a little once pauses are tightened).

1. **Re-time before cutting.** Re-transcribe the roll with whisper `medium.en` word timestamps (the small model garbled
   840-870 s and dropped a line; `medium.en` is downloaded; load audio as a numpy array or put the project ffmpeg on PATH).
   For round 5 only the first ~460 s of the roll matter. Confirm word starts against the lav waveform: `words.json` ran
   0.2 to 0.9 s early on several takes. The opening is **take 5** (roll 168.60 to 196.46 s, already keyed, 835 frames).
2. **EDL for 0:00 to 3:00** from the take map's chosen takes (last clean take; he repeats several lines: "serious hit
   after I turned 40", "active vacation", "my girlfriend noticed", "you just don't get the results", "wife definitely
   notices"). Run `_shared/cut/piccuts.py decide` and `deadair.py --preset ad --pair`; every join gets a W/T punch or an
   insert, never a naked jump. Hair-anchored NEAR/FAR framing, at least 20 px hair clearance on the rendered frames.
3. **Key only what the EDL uses**, with handles, through `keyonce.py` in the heavy lane (group WV-03), using the round 1
   calibration and **RIM=3 in stage 1.5** (it passes the dark-rim bar: 1.86% against the camera's own 3.17%; the default
   fails by 0.03). Give each piece a duration that ends mid-frame. Roughly 5,400 frames at about 6.5 CPU-seconds a frame:
   plan two to three hours of queue time on four cores. The lens window past his cheek measures see-through and is left
   clear on purpose (forcing it solid prints a grey slab). Measure specks on lossless output only.
4. **Composite twice** with `round4/intro/recipe/`: W1 (wood kitchen: its light match, light food names with soft glow)
   and T1 (teal: the same, tank must stay white). Background is camera-locked: a tight punch zooms the plate with him.
5. **Graphics inside these 3 minutes** (visual plan items up to 3:00; build them now, as Soft Blue Light HyperFrames,
   moving for their whole screen time, title capitalization, no em dashes): the six hook foods with More / Less tags and
   names (exist); the stand-in studies page scroll and three abstract cards (exist from round 1; the studies are verified in
   `visual_plan`); the lower third naming "Age-Related Testosterone Decline"; the high T versus low T compare card; the
   "about 1% a year" line graph. Study cards sit at the bottom with Dan above. Check every card over BOTH backgrounds: the
   kitchen is mid-tone and busy, the teal is flat. Captions never touch a graphic.
6. **AI inserts in these 3 minutes are not made yet** (their frames are part B). Keep Dan on camera there and mark each
   slot on the page as "AI clip pending your pick".
7. **Audio:** lav only through `voice_chain.py` with the house-bass-lift settings from `VOICE.json`; no dereverb (the
   blind listener never heard the room); no music or effects yet. Run `audio_gate.py` on the draft and report its rows
   honestly; a draft is not a delivery, but a failing row is still stated.
8. **Checks before Dan sees it:** captions word for word against the audio for the first 30 seconds and spot-checked
   after; foods on the side he points to on the right word (take 5 points right, left, right, left, right, left);
   hair clearance; caption and graphic collisions; edges at 3x on both backgrounds; arm separation on the kitchen over
   the whole 3 minutes (CIELAB difference of arm skin against the set beside it, about 30 or more; round 4's 28-second
   clip passed on its median and dipped at a few moments); one silent watch of both files end to end.
9. Files: `DRAFT - Great Again T VSL R5 - First 3 Minutes - Wood Kitchen.mp4` and `... - Teal Studio.mp4`, 1080p, in
   `round5/`. Both are over 45 seconds, so copy them to `Videos to Review/` (it links to the Seagate, reachable when
   the M2's drive is; the page build reports if it is not).

## 5. Part B: START and END pairs for all 44 AI clip ideas

Source of truth: `plan/ai_clip_ideas_r2.json` (ids, names, the line each plays under, film time, START, END, action,
duration, fallback, rating, risk note, recurring characters). Dan approved "all ten ideas" in round 1, then asked for
"even more ... put extra effort into the AI clips for this one", then on 11-15 asked for frames for **all** of them.

- **Rules that bind** (read them in `.claude/skills/_shared/VIDEO-RULES.md` and `.claude/skills/_shared/IMAGE-GENERATION.md`):
  START and END together from the first step; the blind Codex-and-Google test (two complete unlabeled pairs per idea,
  each END made from its own START on the same model; never reveal which is which); Google subscription first, Codex
  subscription for its half; every pair through `framecheck/gate.py START END --verify` and a **fresh `frame-reviewer`
  agent per pair and per retry**; a pair whose END fails twice is dropped and listed; no text inside generated pictures;
  no belly close-ups; nothing that needs lip sync; AI clips of Dan only if they pass as real footage of a calm man
  (most ideas use a recurring man in his late 40s and a couple, not Dan: keep those characters identical across clips
  by generating each from the same reference START).
- **Volume:** 44 ideas x 2 pairs x 2 frames = 176 pictures plus reviews. Work in film order so the first five minutes
  are done first. If a subscription throttles, deliver in film-order batches and say how many are still to come; do not
  silently drop the second pair or switch to a paid API (cap: $5 paid for this video unless Dan raises it; so far $0).
- **Vertical 9:16 frames**, composed for a full-screen insert under burned captions (keep the lower caption band and the
  top-left AI label area clear of faces).
- **The page:** pictures first. Each idea is one row: its plain name, the film time, the line in one short sentence,
  then the two unlabeled pairs side by side (START | END, START | END), each with one **Select** button. Nothing
  pre-selected; untouched means not chosen (memory `review-pages-select-not-kill`). Group by film section in film order;
  mark the eight "first to make" ideas with a small badge; a sticky "N selected" counter; filters for section and
  Selected. No paragraphs of description: he said the descriptions were "too time-consuming". Put the action sentence
  behind a small "what moves" toggle.
- **After his picks:** motion only for selected pairs, through Flow (`flow-veo` agent), `clipcheck.py` and a fresh
  frame reviewer on the frames the edit uses. That is a later round.

## 6. The review page

- Copy `round4/review/build_page.py` (it already has the side-pane layout fix) to `round5/review/` and adapt. New port in
  9764-9790; leave 9760-9763 running. Serve with `.claude/skills/_shared/review_server.py`; require "Managed review ready".
- **Dan reviews in the Claude app's side browser pane** (about 800 to 1150 px wide) as well as full screen. The first
  video must be loaded into the one shared player at page load so its own play button works; the player is a fixed side
  panel from 760 px. Test at 800, 1150 and 1920 px in silent check mode, then Finish checks for owner, and clear test
  selections from localStorage (memory `review-page-plays-in-side-pane`).
- Order: header and "Locked so far" list; "Your decisions"; the two 3-minute films with Play buttons (kitchen loaded
  first) and a list of what to look at with film times (each graphic's time, each pending AI slot); "What I decided";
  the AI pairs; one reply box. Plain language, no em dashes, the video's title and never a bare job code.
- Decisions to ask (keep it short): approve the first 3 minutes in the kitchen or list changes by time; anything from
  the teal version he wants carried over; which AI pairs to turn into clips.
- Close the round: `queue.py set WV-03 delivered`, mirror to the Edit Queue artifact db, `editcap.py release WV-03
  --review`, one board entry (the board is at its word limit: keep the entry to one token-length line), the two wrap-up
  boxes, and a round 6 handoff with its starter prompt in chat.

## 7. Traps learned in rounds 1 to 4

- Stage 1 can decode one frame past the end of a piece; prove which frame, quarantine it, never relax the count check.
- The locked long-form "warm" grade is too bright and orange on this roll; "matched" is the rebalanced version. On dark or
  saturated backgrounds his skin reads more orange: trim skin saturation a few percent in the light match, not the grade.
- A wood background the colour of his skin makes his arms vanish (round 3's honey wood). Measure arm separation, not
  only the tank.
- Night-time mood reads as "a late-night infomercial" to Dan (round 2): no low-key light, glowing strips or heavy
  darkening. The kitchen must stay a daytime room.
- Check his own winners' frames before advising on look. The editor told him to drop plain colours in round 3 and had to
  reverse it after looking at `round4/refs/` (two of his winners pitch over a teal studio).
- A page tested only at 1920 px failed in the side pane ("I can't play the video on the review page").
- A page generator that falls back to estimates when it cannot read measured numbers must say so; round 3's contrast
  meter showed estimates as if measured.
- `Videos to Review/` links to the Seagate; copies are skipped when it is unreachable.
- No props were filmed. The live store price is $47: never show a store screenshot for the $97 line; use the price card.
  The label source file has a home-address panel: facts-only crop for any Supplement Facts shot.
- The repo's shared files are often blocked by other sessions' live edits: `safe-push.sh` then commits locally and reports
  "NOT pushed". Retry at the end of the round; never force.

## 8. Cost and gate status, stated honestly

- Paid AI spend so far: $0. Cap for paid fallback: $5 for this video unless Dan raises it.
- No delivery gate has been run; nothing delivered is a master. Drafts so far passed their own checks (hair, captions
  against a second transcription, food sides, sync, 3x edges). No one has listened to audio through speakers.
- Key: flicker and dark rim (RIM=3) pass; specks zero on lossless; the lens-window see-through measure fails by design.

## Starter prompt (Claude: Opus 5.5, high effort)

> AD (Great Again T sales video). Name this chat "Great Again T VSL AD R5". Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/handoff-20261115-great-again-t-vsl-round5.md`, then run round 5 of the Great Again T VSL (WV-03) exactly as that handoff lists. My decisions are locked in it: the background is Wood Kitchen 1 (Medium Wood Kitchen). Build the first 3 minutes of the film from one cut in two backgrounds, the wood kitchen and the Teal Studio, and make start and end frame pairs for all 44 AI clip ideas as pictures I can pick from. Nothing else is rendered. Use /ad-edit. Send me the round 5 review page, tested in the side pane, when both are ready.
