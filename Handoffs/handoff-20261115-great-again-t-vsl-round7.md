AD (Great Again T sales video). Task name: `Great Again T VSL AD R7`.

# Great Again T VSL (WV-03): round 7 handoff

Written 2026-11-15 (evening) by the round 5 and 6 coordinator (Claude Fable 5.2 with Opus, Sonnet and Fable workers).
**Model: Claude Opus 5.5, high effort** (a video stays on the AI it started on). Fire after Dan replies on the round 6 page.

One native 9:16 sales video (1080x1920, 29.97), Dan on green screen, roll C1903. The job lives on the M6's internal drive:
`~/_edit_work/wv-03/`. On resume: `python3 .claude/skills/_shared/editroute/resume.py check WV-03`, then
`editcap.py acquire WV-03 --title "Great Again T VSL" --type AD`.

## 1. Where round 6 ended

Review page (round 6, same address as round 5 so Dan's selections persist): http://127.0.0.1:9764/. Generator
`round5/review/build_page.py` (`build_page.r5.bak.py` is the round 5 wording); inputs `round5/review/inputs/films.json` and
`pairs.json` (`pairs.json` is written by `round5/frames/assemble_pairs.py`: run it with `GATE_OFF=1`, then `python3 build_page.py`).
Each idea row shows the words Dan says around the clip (`round5/frames/say_context.py`).

**Film:** `round6/DRAFT - Great Again T VSL R6 - First 3 Minutes - Wood Kitchen.mp4`, 2:51.57, sha256
`58011fa4ede52e0d6270992f4c4bc21a77293252ffa7a7c4f634570d6205d8cc`. Kitchen only. Report `round5/film/REPORT.json`, log
`round5/film/BUILD_LOG.md` (sections 10 to 15 are today's passes), recipe `round5/film/recipe/` (`chain_film.sh`).
What is in it: the pause at 0:27 tightened (0.47 s to 0.17 s); close framing (1.5) by default with hair 4% from the top, 1.25
where 1.5 cuts his hands (`work/gesture_shots.json`), the old wide placement only under the hook foods (0:02.55 to 0:15.92);
one wide shot at 0:48.45 to 0:54.15 with the KEY POINT card "Fight Back Against Age-Related Testosterone Decline"; the
iceberg clip (AI-17-1) with two labels from 2:47.83 to the end. Dan stays on camera in the other AI slots.

**Dan's decisions today** (his words: `round6-plan/decisions.json`): Wood Kitchen 1 is final ("Let's go to the wood kitchen");
the close shot by default, the wide shot only with something above his head or a cutaway; kitchen-only renders from here.

**Pictures on the page:** 41 ideas with at least one verified START/END pair, 59 pairs; 7 ideas dropped after every attempt
(AI-01, AI-30, AI-40, AI-41, AI-42, AI-48, AI-53: plain reasons in `round5/frames/final_dropped.json`); AI-59 (Yolk Over
Steak) and AI-61 (the mechanic, redesigned, clock composited in code) failed on the Google side and their Codex twins
were still being gated when this was written (`round5/frames/AI-59/wave2c/state.json`, `AI-61/wave2c/state.json`,
markers `WAVE5C_DONE`, `WAVE6C_DONE`): check them first, re-run the assembly and rebuild the page.
Ideas Dan replaced are hidden once their replacement verifies (`retired_ids.txt`); new ideas are AI-45 to AI-61.

**Motion so far** (`round5/clips/MANIFEST.json`): only AI-17-1 (The Iceberg, first pair) verified. Failed: AI-17-2 (picture
shifts), AI-11 (eggs fly off the spatula), AI-45 both pairs (a man eating: mouth faults in every take), AI-15 (Flow refused
the frames of a child; two paid Kling takes moved in slow motion). Paid spend: $1.57 of the $5 cap. Flow credits 19,822 to
19,665 for clips; pictures cost 0 credits.

## 2. What round 7 does

1. Record Dan's reply from the page's reply box in `round7-plan/decisions.json` in his words; log two-model pair picks
   with `blind-image/blind.py pick` on the idea's `blindset` (never reveal sources; single-source ideas are keyed in
   `.manual-key.json`).
2. An independent `ra-reviewer` on the round 6 film file has NOT been run: do it before anything else is built on it.
3. Motion only for the pairs he selected, through Flow, with what today taught (section 3). The hook: if he selects a
   "Ready To Dig In" pair (AI-60), make it and lay the ready overlay "You'll Feel Like A New Man" over it
   (`round5/film/work/hf/`, built on placeholder timing).
4. His notes on the film and on the framing question ("does the closest shot work, or is it too tight?").
5. Still required before any full render (round 2 decision): the full graphics review of everything after 2:52.
6. Two things Dan asked for that are not delivered: the mechanic "working all day" fast-forward clip and a moving
   Shoulder Ride. Offer the workable route in one line each, do not rebuild blind (section 3).

## 3. Traps learned today (frames and motion)

- Static drift is repaired with `framecheck/lockstill.py` before an END counts as failed (`round5/frames/NOTE_LOCKSTILL.md`).
- Image models fail: sit-down or stand-up, walking toward the camera, an object pushed by another object, tools whose
  mechanics must be right, anything counted or measured (a fourth tub, exactly half a glass), printed money, product
  labels, "finished work" versus "work in progress" (a closed bonnet, an assembled part). Design one small caused change.
- Video models fail: anything airborne (eggs off a spatula), eating and chewing, a photoreal child (Flow refuses the
  upload), walking in Kling (slow motion). Flow's "upscaled" 1080p download adds a fake texture: check and deliver from the
  720p original. A take sped up to fix slow motion needs 2.5 s left afterwards.
- Never tell a Flow prompt "START" or "END": it returns a two-picture collage. Say "the attached image".
- Reviewers get a neutral link folder under `round5/frames/_rev/`; two agents must not share link names or a scratch folder
  (it happened twice today; reviews were checked against their pictures and matched).
- The Codex subscription was exhausted at 1:34 PM by about 150 images and reset that afternoon; about 120 more were drawn
  after the reset (memory `codex-image-batches-exhaust-subscription`). Tell Dan the count before a large batch.
- Frame gates share the render queue: about one a minute, and they stall while a render holds memory. Run gates before
  renders, or use `/away`.
- The page build refuses any visible text that names a picture model, and input pictures named like its own media.

## 4. Open items, stated plainly

- No independent review of the round 6 file. On its last render the editor re-watched only the changed parts.
- Audio gate fails three rows on every draft (tone: the fixed bass lift; floor -3.5 vs -3.0; do-no-harm not measured).
  Nobody has listened through speakers.
- Arm separation on the kitchen: median 32.75, minimum 27.1. Caption to High/Low card gap 11 px.
- Captions "you've felt" and "as I got older" (after 0:30) are uncertain against a second transcription.
- The closest size (1.5) is 0.87x as sharp as the old close shot; a sharper one needs the key at full resolution.
- Some Codex pairs had a swirl texture removed by shrinking and re-enlarging both frames before review.
- Git: nothing from rounds 5 and 6 reached GitHub (other sessions' live edits block the merge); commits are local.
- The status board is over its word limit from other sessions' entries.

## Starter prompt (Claude: Opus 5.5, high effort)

> AD (Great Again T sales video). Name this chat "Great Again T VSL AD R7". Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/handoff-20261115-great-again-t-vsl-round7.md`, then run round 7 of the Great Again T VSL (WV-03) as that handoff lists: record my round 6 reply (below), have the round 6 film independently reviewed, make moving clips only for the picture pairs I selected, apply my notes to the first 3 minutes, and send me the round 7 review page tested in the side pane. Use /ad-edit. My round 6 reply: [paste the reply text from the round 6 page]
