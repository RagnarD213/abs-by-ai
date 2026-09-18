# Handoff — DS-04 revision 1: a better opening vacuum clip (2026-09-18)

**Job:** DS-04 "The Only Ab Exercise That Shrinks Your Belly Fat" (dedicated 9:16 short). Read
`Handoffs/video-editing/00-RULES.md` and `Handoffs/video-editing/DS-04-plan.md` first; this doc only adds the revision.

## Dan's words (2026-09-18, after watching the round-2 review copy)

> "Everything's looking good except for the beginning. I don't feel like it was a good vacuum clip that you used in the
> beginning… ideally one where it's from the front or a 45° angle of me doing a more dramatic vacuum where it's obvious
> I'm doing that. The clip you're using in the beginning looks like I'm standing there. The one that is in the screenshot
> [the profile draw-in at 0:25, caption "posture and suck"], I think, would work if you can't find anything better."
> "Show me a few clips of me doing the vacuum to approve. If none of them are good enough, then we'll generate it from AI."
> "No cover images. I'm going to transition that to Codex."

**What that settles:** the rest of the cut is approved as delivered — title band, chips, cue 2, cue 3 cards, captions,
framing, music, and the sound as he heard it. Only the opening beat changes. **Covers are out of scope** (leave the four
existing cover files where they are; do not rebuild or send them).

## Current state

* Delivered master: `Short-form video content/ds-04_only-ab-exercise-that-shrinks-belly-fat.mp4`, 50.117 s, sha256
  `18f6490dba27c794b722fa33269e228fb2977a1bd646760b64d8bad5247291e2`. Notes beside it: `ds-04_notes.md`. Recipe:
  `ds-04_recipe/` (`REBUILD.md`, `plan.json`, `beats.json`, `timeline.json`, `s10_render.py`, `s34_rebuild.sh`).
* Work dir (ours, reusable): `/Volumes/Extreme/_edit_work/ds04/` — pipeline `s01…s34`, `mix.wav` (the final mix),
  `ROUND-1/2-EDITOR.md`, `ROUND-1/2-REVIEW.md`, `measurements-DS-04.json`.
* The opening beat is timeline piece `cue1_vac_front`, **frames 0–125 (0.000–4.204 s)**, under L1 "THIS is the only ab
  exercise that actually shrinks your stomach." It currently shows C1677 2:03.0–2:07.6: a **static** hands-on-hips hold.
  That is why it reads as standing there — the stomach never moves.
* Edit queue: DS-04 = DELIVERED. Set `in_progress` when the rebuild starts, `delivered` again with the new review copy.
* Still open from round 2 (fold into this rebuild, both tiny): two caption chunks bridge a full stop ("lean, but if you"
  0:08.08, "stomach, but it does" 0:35.03) — split at the sentence boundary; the card cut at 0:06.10 is missing from
  `plan.json` `joins`.
* ⚠ The audio gate's `artifacts` row FAILS on this roll's raw lav (0.088 vs 0.079; untreated 0.101; RA-01 identical).
  Dan listened and called the cut good. Do not process harder and do not touch the threshold. In the clip-approval
  message, ask him one line: "the audio gate flags one row on every outdoor 8/28 roll; you've heard it — accept the
  sound as delivered?" and record his answer. The stamp stays an honest FAIL until the row is recalibrated by a
  separate, corpus-gated task.

## Step 1 — find candidates and show Dan (STOP here for his approval)

What makes a vacuum obvious is the **motion**: relaxed belly → exhale → stomach drawn up under the ribs. Pick windows
that **contain the draw-in**, not a hold. Useful measurement: run the person mask on a front pass and track waist
width (and, on a 45°/profile pass, belly depth) per frame; the best candidate is the largest, fastest relaxed→drawn-in
change with his eyes open and mouth closed or nearly so.

Where to look, in order:

1. **C1677** (`/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1677.MP4`,
   4K 16:9, sunny): front A 0:00–0:28 (dramatic but he strains — mouth open at 8.4/11.2/14.4/16.4–17.2/18.4/21.6–22.0/23.6–24.0,
   eyes shut most of 9–23; look for the **onset** of each rep, where the face is still calm), front B 1:40–2:52 (onsets
   near 1:50–1:52 and after the arm drops at 1:48 and 2:34), the turn between front and profile (0:44–0:50 and
   1:20–1:42 — he passes through 45°), profile 0:47–1:20.
2. **8/14 vacuum long-form rolls C1614–C1629** (`/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/`),
   especially **C1625** (the live set, front view). ⚠ 1080p: a vertical crop will be soft (≈ 2.5–4×). Offer it only if
   the vacuum itself is clearly more dramatic, and say it is softer.
3. The V3 long-form's vacuum section (source of `v3-short6_vacuum-exercises.mp4`) — from the no-graphics master or raw,
   never from the finished Short (burned captions).
4. `grep -il vacuum /Volumes/Extreme/_edit_work/_transcripts-828-full/*.txt` and the other shoot transcripts for any
   roll where he demonstrates it while talking.

Build **3–5 candidates**, each the real 4.2 s beat rendered **in the delivered layout** (title band, 1080×1540 picture
window, hair-anchored hair→below-the-knee crop so the caption band clears the stomach, the L1 caption burned, the real
L1 audio under it) at 540p, named `A`…`E`, plus one side-by-side contact sheet. **Include the screenshot clip as one
candidate** (C1677 profile draw-in, source ≈ 0:55.5–0:59.7). Send them with `SendUserFile` and one line each on what is
different (angle, how big the draw-in is, sharpness, face). **Then stop and wait for his pick.**

⚠ **No repeated clip inside one video** (`AGENTS.md`). The how-to beat (cue 2, 0:22.1–0:29.4) already uses the C1677
profile draw-in at ≈ 0:53–1:00. If Dan picks the screenshot clip for the opening, the opening and the how-to must not
show the same rep: use the **second** profile rep (≈ 1:11–1:20) for one of them, or a front draw-in for the opening.
Say this in the candidate notes so he chooses knowingly.

**If he rejects all of them → AI.** Budget $5 for this video including retries (`AGENTS.md`). Show him the **start
frame, end frame and the intended action** before generating motion (start = a real front frame of Dan relaxed from
C1677; end = the same framing with the stomach drawn in). The clip carries the **AI-GENERATED** chip, placed off his
face and abs by measuring the person mask. Check every frame for the giveaways (melting hands, morphing shorts, a
changing face). It must be Dan, same shorts, same pool set.

## Step 2 — after his pick: rebuild the opening only

1. Copy nothing new into another session's dir; work in `/Volumes/Extreme/_edit_work/ds04/`. Machine cap: never a
   third concurrent build (`ps` line in the plan §7).
2. Replace `cue1_vac_front` (frames 0–125) with the approved clip: same length, same grade (1.30× LUT + sat 0.88,
   BT.709 decode), fixed centre, hair-anchored, **no speed change**, no duplicated first frame. Time it so the draw-in
   lands on "shrinks your stomach" (≈ 2.5–4.0 s).
3. **Audio stays bit-identical**: reuse `mix.wav`; rebuild the picture only. Fix the two caption chunks and add the
   0:06.10 join to `plan.json`.
4. Gates on the delivered file: `audio_gate.py` → `watch.py` (judged) → `gate.py --format short --plan plan.json`.
   Expected: everything PASS except the known `artifacts` / `audio:stamp` rows. Anything else failing is a real defect.
5. **Independent review** (`ra-reviewer`, fresh, never sees the editor's notes): the new opening frame by frame, every
   join ±4 frames, captions word for word, and a diff proving frames 126–1501 are unchanged from the round-2 master
   apart from the two caption chunks.
6. Deliver over the same names in `Short-form video content/` (+ `REVIEW_540p_…`, stamps, `ds-04_notes.md` revision
   section, recipe). Send Dan the review copy. `queue.py set DS-04 delivered` + `Artifact write_db` + `mark-synced`.
   Update the DS-04 line on `AI_COORDINATION.md`. Commit docs only.
7. When Dan says it is finalized: `queue.py set DS-04 finalized`, record his approval (his words, this file's sha) in
   the regression corpus, delete the board entry and this handoff's index rows. Upload/queueing is `/video-setup`,
   a separate step. Covers: Codex.

## Starter prompt

> Read `Handoffs/handoff-20260918-ds04-opening-vacuum-clip-revision.md` and execute Step 1 only: find 3–5 better
> opening vacuum clips for DS-04 (front or 45°, a dramatic draw-in where it's obvious I'm doing a vacuum), render each
> as the real 4.2-second opening in the delivered layout, include the profile "posture and suck" clip as one option,
> send them to me and stop for my pick. After I pick, do Step 2 (rebuild the opening only, same audio, gates,
> independent review, send me the review copy). No cover images.

**Recommended model:** Claude **Opus 5, effort high** (the pipeline and recipe already exist; this is a scouting pass
plus a one-beat rebuild). The independent check runs as the `ra-reviewer` subagent (Fable 5.1, high). Codex alternative:
GPT-6 Astra, high, following `.claude/skills/shorts/SKILL.md`.
