AD (Great Again T sales video). Task name: `Great Again T VSL AD R7`.

# Great Again T VSL (WV-03): round 7 handoff (2026-11-16, replaces the 11-15 round 7 file)

Written by the round 5 and 6 editor after Dan finished his round 6 review. **Model: Claude Opus 5.5, high effort.**
**Runs on the M2** (Dan, 11-16: "Have the handoff run this edit on the M2."). **Dan fires this himself**: do not start it
for him. A round 7 chat was started too early on 11-16 and stopped by Dan within minutes; it wrote nothing to disk. Start clean.

One native 9:16 sales video (1080x1920, 29.97), Dan on green screen over the wood kitchen, roll C1903.

## 0. Move the job to the M2 first

The job folder is on the M6's internal drive: `m6:~/_edit_work/wv-03/` (245 GB). The M6 is reserved for the Joint Vigor
VSL (job SRM-JV-R4), which is why Dan moved this edit.
1. Start this chat on the SSH connection `m2`. If this file is not yet in the M2's checkout, run
   `python3 scripts/two-mac/checkout-sync.py` there (or read it with `ssh m6 cat`).
2. Record the move: `python3 .claude/skills/_shared/editroute/editroute.py pick WV-03 --kind VSL --round 7 --host m2 --move`
   (the dry run on 11-16 answered `m2`). Then `editcap.py acquire WV-03 --title "Great Again T VSL" --type AD` on the M2.
3. Work folder on the M2: `renderq.py workdir WV-03 --need <honest GB>` (expect the Extreme; it had 271 GB free and Joint
   Vigor also works there, so do not copy all 245 GB). Copy from the M6 what round 7 uses, checksummed, and add more
   only when a step needs it: `plan/` `script/` `round2-plan/` to `round7-plan/` `round6/` (small), `round5/` (11 GB:
   frames, the film recipe, the review page), the key pieces the first 3 minutes are built from (H5 in `round2/`, S1 and
   P1 to P6 in `round5/key/`; `round2/` is 49 GB in all, take the pieces, not the folder), and `src/` (46 GB) only when
   the build goes past 2:52. `round1/` (138 GB) should not be needed. Never re-key a piece that has a keyonce stamp.
   Keep the folder layout so the recipe's relative paths work; grep the recipe for `~/_edit_work/wv-03` and absolute M6
   paths and fix what points at the M6.
4. The M6 copy is the source of record until Dan approves a round built on the M2. Delete nothing on the M6.
5. Flow and Chrome already run on the M2, so picture and clip downloads land locally now (`~/Downloads`).

## 1. Where round 6 ended

- **Film:** `round6/DRAFT - Great Again T VSL R6 - First 3 Minutes - Wood Kitchen.mp4`, 2:51.57, sha256
  `58011fa4ede52e0d6270992f4c4bc21a77293252ffa7a7c4f634570d6205d8cc`. Recipe `round5/film/recipe/` (`chain_film.sh`),
  log `round5/film/BUILD_LOG.md`, report `round5/film/REPORT.json`.
- **Review page (round 6):** http://127.0.0.1:9764/ on the M6, generator `round5/review/build_page.py` (inputs
  `round5/review/inputs/films.json`, `pairs.json` from `round5/frames/assemble_pairs.py` run with `GATE_OFF=1`). It has a
  page-level Full screen button (the app's side pane ignores the native one): keep it on the round 7 page.
- **Pictures:** 43 ideas with verified START/END pairs, 61 pairs, under `round5/frames/AI-xx/`. Characters in
  `round5/frames/characters/` (`everyman`, `everyman_after`, `everyman_far`, `wife`, `fitman`, `dan_before_ref_*`).
- **Motion so far** (`round5/clips/MANIFEST.json`): only AI-17-1 (The Iceberg) verified, and it is in the film.
  Failed: AI-11 (eggs fly), AI-45 (eating: mouth faults), AI-15 (Flow refuses a child; Kling slow motion), AI-17-2.
- **Spend:** $1.57 of the $5 paid cap. Flow credits were 19,665 after the clips. Google subscription first; paid API only
  after a recorded subscription failure.
- **Independent review of the round 6 file:** started 11-16 9:24 AM from the round 6 chat (Fable 5.2), writing
  `m6:~/_edit_work/wv-03/round6/ROUND-6-REVIEW.md`. If the file is missing when you start, ask the round 6 chat
  ("Great Again T VSL AD R5") for the verdict; do not start a second review of the same file. Fix its must-fix items.

## 2. Dan's round 6 decisions

His words, all three messages, are in `round7-plan/decisions.json` (sha256
`4fb7a6ab3c840ce40a76c1de59f6bb659ffbda2ef4759eb022e4a757a97e2c3a`), with the 13 pairs he selected on the page. Read
it first; his words outrank this summary. The id mapping below is the editor's reading of his spoken names.

**Film**
- Framing approved: "the closer shot works. I like the way you did the framing here." Keep the rule for the whole film.
- KEY POINT card (0:48.45 to 0:54.15): new text "You Want To Fight Back Against Age-Related Testosterone Decline";
  slightly higher and very slightly larger, centred between the top of his head and the top of the frame.
- Background: Wood Kitchen 1, final (11-15). Kitchen-only renders.

**One consistent character through the story:** "that white guy in his 50s", the Everyman (`everyman.png`), with his
`everyman_after` and `everyman_far` portraits for the clips after the product. Every prospect clip uses him. AI-46
(frustrated then determined) and AI-61 (the mechanic) show other men: remake both with him. AI-47 and AI-50 stay Dan
(his own lines). The fit man over 50 (`fitman`) stays in the food clips Dan approved (AI-45, AI-60, AI-51).

**New prospect-story series, 0:53 through the love-life line (script lines 21 to 26):** one clip per thing he says, so
the stretch tells the full story. New START/END pairs (new ids from AI-62; `round5/frames/BRIEF_WAVE3.md` is the pattern):
1. Doing his best to eat right: a low-fat breakfast, egg white omelet and protein shake, looking disgusted (about 1:02).
2. Doing his best to stay active: trying to work out, looking miserable.
3. "Your belly keeps growing a little bit each year": he looks at his belly with frustration (mid shot, no pinch, no close-up).
4. Strength and stamina decline: exhausted walking up a hill, hiking.
5. "It's harder and harder to stay in shape."
6. "It seems like you're always tired."
7. Working long days is exhausting.
8. An active vacation is exhausting.
9. "It's harder and harder to maintain a good love life": with his wife, who looks frustrated with him (tasteful, clothed).
Lay the series against the script with film times so every phrase has a clip and no idea repeats; the approved clips in
this stretch (AI-02, AI-03, AI-04, AI-14, AI-15, AI-16) each cover a phrase, say which.

**Not approved, do not make:** AI-19 The Empty Chair; AI-22 Plate Over Needle (and keep needles and drug items out of
the whole VSL: check every other idea and graphic for them); AI-25 Down The Drain; AI-05 The Endless List; AI-37 The
Tank Of Gas; AI-39 The Dabbler's Treadmill.

**Approved, make both pairs:** AI-51 The Fit Man's Cart; AI-07 Supplement Aisle (the editor's reading of "both
supplement piles"; Dan was told and can correct it).

**Changed, new pairs needed:**
- AI-52 Double The Tongkat Roots: not approved. Two variations, each a large pile for us beside a small pile for them,
  ours double, not literal bottle amounts: one of root pieces, one of powder. (Counting fails in image models: piles,
  not counted pieces. The earlier powder idea, AI-53, was dropped for that.)
- AI-34 Out The Door (16:46): keep the idea; the man visibly in slightly better shape (`everyman_after`).
- AI-35 Back Two Notches: not a belt close-up. The man himself, the one character after his change, with a visibly flat stomach.
- AI-56 The Trail, No Belly: replaced. A man running on the beach who then raises his arms victoriously. Dan believes
  such a clip exists: search the clip library and his finished ads first (a quick search found A0042, a shirtless man
  with abs jogging on a beach, 16:9 AI, used in WV-01 and Ads 1, 5, 6; B0109 and B0103, stock beach runners; none noted
  with raised arms). Reuse it if found and it suits 9:16; otherwise make it with the one character.
- AI-38 Backyard Catch: he pitches a wiffle ball to his small son, the son hits it, he raises his arms and runs after it.
  Known traps: Flow refuses photoreal frames of a child, and airborne objects fail. Design around them (the son seen from
  behind or small in frame, the hit implied by the swing and his reaction) and tell Dan plainly what was possible.

**Everything else on the round 6 page is approved as shown, to generate.** For an idea with two pairs, make the pair
he selected; where he selected neither, the first-listed pair, and say so. Log only his own selections with
`blind-image/blind.py pick`. Never reveal which model made which picture.

## 3. Order of work

1. Section 0, then the independent review's must-fix items and the KEY POINT card; re-render the first 3 minutes.
2. Design and make the new and changed pairs (the nine story ideas, AI-46 and AI-61 remakes, both tongkat piles,
   AI-34, AI-35, AI-38, the beach run if no clip exists): both models as blind pairs, the frame gate, a fresh frame
   reviewer per pair with a neutral link folder. Tell Dan the Codex image count before the batch (memory
   `codex-image-batches-exhaust-subscription`). Dan sees START and END before any motion for these.
3. Motion for the pairs approved as shown, film order, the first 3 minutes first (hook: AI-11 X1 with the ready
   "You'll Feel Like A New Man" overlay in `round5/film/work/hf/`, or AI-60 if eggs still fly). A clip that cannot be made
   cleanly is reported with the reason, not shipped. Still owed an answer: a moving Shoulder Ride (AI-15) and the
   mechanic fast-forward; give the workable route in one line each.
4. Still required before any full render (round 2 decision): the full graphics review of everything after 2:52.
5. The round 7 review page, tested in the side pane at about 800 and 1370 px, with later-round timestamps of what changed.
6. Stop for Dan (`editcap.py release WV-03 --review`). **Do not start round 8 or any next chat while he is still
   reviewing or a decision is open** (Dan, 11-16; memory `no-next-round-until-review-finished`).

## 4. Traps and open items

Sections 3 ("Traps learned today") and 4 ("Open items") of `Handoffs/handoff-20261115-great-again-t-vsl-round7.md` still
apply in full: static drift and `lockstill.py`; what image and video models fail; never say "START" or "END" in a Flow
prompt; Flow's upscaled 1080p download; the page build refusing model names; the audio gate's three failing rows; nobody
has listened through speakers; captions "you've felt" and "as I got older" uncertain; the closest framing 0.87x as sharp.

## Starter prompt (Claude: Opus 5.5, high effort, on the M2)

> AD (Great Again T sales video). Name this chat "Great Again T VSL AD R7". Run this edit on the M2. Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/handoff-20261116-great-again-t-vsl-round7.md`, then run round 7 of the Great Again T VSL (WV-03) as that handoff lists: move the job to the M2, apply my round 6 notes (saved word for word in `round7-plan/decisions.json`), make the new start and end pictures with the one consistent character, make moving clips for everything I approved, and send me the round 7 review page tested in the side pane. Use /ad-edit.
