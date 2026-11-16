SUPERSEDED 2026-11-16 by `handoff-20261116-great-again-t-vsl-round7.md` (Dan's full round 6 reply, the move to the M2). Sections 3 and 4 below are still referenced by it.

AD (Great Again T sales video). Task name: `Great Again T VSL AD R7`.

# Great Again T VSL (WV-03): round 7 handoff

Written 2026-11-15 (evening) by the round 5 and 6 coordinator (Claude Fable 5.2 with Opus, Sonnet and Fable workers).
**Model: Claude Opus 5.5, high effort** (a video stays on the AI it started on). Dan replied on 2026-11-16; round 7 was started from the round 6 chat the same morning.

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

**Pictures on the page:** 43 ideas with at least one verified START/END pair, 61 pairs; 7 ideas dropped after every attempt
(AI-01, AI-30, AI-40, AI-41, AI-42, AI-48 in its first design, AI-53: plain reasons in `round5/frames/final_dropped.json`).
All picture waves are finished (markers `WAVE*_DONE` in `round5/frames/`). AI-59 (Yolk Over Steak) and AI-61 (the mechanic,
redesigned as two moments of ongoing work with the clock composited in code) each have one verified pair.
Ideas Dan replaced are hidden once their replacement verifies (`retired_ids.txt`); new ideas are AI-45 to AI-61.

**Motion so far** (`round5/clips/MANIFEST.json`): only AI-17-1 (The Iceberg, first pair) verified. Failed: AI-17-2 (picture
shifts), AI-11 (eggs fly off the spatula), AI-45 both pairs (a man eating: mouth faults in every take), AI-15 (Flow refused
the frames of a child; two paid Kling takes moved in slow motion). Paid spend: $1.57 of the $5 cap. Flow credits 19,822 to
19,665 for clips; pictures cost 0 credits.

## 2. What round 7 does (UPDATED 2026-11-16 from Dan's round 6 reply)

Dan replied by voice in the round 6 chat on 2026-11-16, not through the page's reply box. His words, the 13 pairs he had
selected on the page, and the editor's reading are in `~/_edit_work/wv-03/round7-plan/decisions.json` (sha256
`3c62ae283171190e43d9f41a9bd3262f9736828de44bbeeaa6c49537f0212904`). Read it first; his words outrank this summary.

What he decided:
- **Framing approved.** "The closer shot works. I like the way you did the framing here." Keep the round 6 rule for the whole film.
- **KEY POINT card (0:48.45 to 0:54.15):** he likes it. New text, from his words: "You Want To Fight Back Against Age-Related
  Testosterone Decline". Move it slightly higher and make it very slightly larger, centred in the gap between the top of
  his head and the top of the frame.
- **AI clips:** "All AI clips are approved except for these with these modifications." Every idea on the round 6 page is
  approved for motion as shown, except where the new series below changes it. For an idea with two pairs, use the pair he
  selected (13 selections in decisions.json); where he selected neither, make the first-listed pair and say so. Log only
  his own selections with `blind-image/blind.py pick`.
- **The prospect story, 0:53 through the love-life line (script lines 21 to 26):** tell it as a series of AI clips, one per
  thing he says, with ONE consistent character. He asked the editor whether one character or a variety is stronger; the
  editor recommended one (the Everyman, `round5/frames/characters/everyman.png`, whose leaner self is in the later clips
  he approved) and round 7 proceeds on that. Check `dan_followups` in decisions.json and the round 6 chat's last messages
  for his answer before generating.
  New START/END pairs he asked for (new ids from AI-62; `BRIEF_WAVE3.md` is the pattern; both models, blind pairs):
  1. Doing his best to eat right: a low-fat breakfast, egg white omelet and a protein shake, looking disgusted (about 1:02).
  2. Doing his best to stay active: trying to work out, looking miserable.
  3. "Your belly keeps growing a little bit each year": the same man looking at his belly with frustration (no pinch, no
     belly close-up, mid shot).
  4. Strength and stamina decline: exhausted walking up a hill, hiking.
  5. "It's harder and harder to stay in shape."
  6. "It seems like you're always tired."
  7. Working long days is exhausting.
  8. An active vacation is exhausting.
  9. "It's harder and harder to maintain a good love life": with his wife, who looks frustrated with him (tasteful, clothed).
  Existing ideas in this stretch (AI-02 desk nap, AI-03 trail bench, AI-04 date night, AI-14 stairwell, AI-16 in bed,
  AI-46 frustrated then determined, AI-61 mechanic, AI-15 shoulder ride, AI-47 Dan's candles) are approved; AI-46 and
  AI-61 show other men, so remake them with the one character (AI-47 stays Dan: it is his own line). Lay the series out
  against the script so every phrase has a clip and none repeats an idea; say which existing clip covers which phrase.

Order of work:
1. `resume.py check WV-03`, then `editcap.py acquire`. **The M6 is reserved for the Joint Vigor VSL (job SRM-JV-R4) until
   its checked preview, target Tuesday 11-17 evening**, so expect exit 3: run `editcap.py wait WV-03` in the background, tell
   Dan his place in line in one line, and do read-only preparation meanwhile (the series layout against the script, the
   idea folders and prompts, the KEY POINT card spec). No generation, render or build before the slot is granted.
2. The independent review of the round 6 file was started from the round 6 chat on 11-16 at 9:24 AM (Fable 5.2): it writes
   `~/_edit_work/wv-03/round6/ROUND-6-REVIEW.md`. If the file is not there yet, the round 6 chat will forward the verdict;
   do not start a second reviewer. Fix its must-fix items in this round.
3. START and END pairs for the new series (Dan sees pairs before any motion), each through the frame gate and a fresh
   frame reviewer. Tell Dan the Codex image count before the batch (memory `codex-image-batches-exhaust-subscription`).
4. The KEY POINT card revision and the review's must-fix items in the first 3 minutes; re-render with `chain_film.sh`.
5. Motion for approved pairs, the first 3 minutes first (hook: AI-11 X1 with the ready "You'll Feel Like A New Man"
   overlay in `round5/film/work/hf/`; AI-60 if it serves better), then the rest in film order, with what section 3
   teaches. Clips that cannot be made cleanly are reported with the reason, not shipped.
6. Still required before any full render (round 2 decision): the full graphics review of everything after 2:52.
7. Not delivered and still owed an answer: a moving Shoulder Ride (AI-15, selected by Dan) and the mechanic fast-forward.
   Offer the workable route in one line each.
8. The round 7 review page (same generator; it now has a page-level Full screen button, keep it), tested in the side pane.

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

> AD (Great Again T sales video). Name this chat "Great Again T VSL AD R7". Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/handoff-20261115-great-again-t-vsl-round7.md`, then run round 7 of the Great Again T VSL (WV-03) as that handoff lists. My round 6 reply is saved word for word in `~/_edit_work/wv-03/round7-plan/decisions.json`: the closer framing is approved, the KEY POINT card gets new text and moves up, all AI clips on the page are approved, and I want a series of new start and end pictures that tell the prospect's story from 0:53 with one consistent character. Use /ad-edit. Send me the round 7 review page tested in the side pane.
