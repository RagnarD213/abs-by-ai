# Handoff: use the Google AI Ultra credits to stock the clip library with reusable AI clips (2026-11-07)

**Owner:** Claude, Opus 5.5 high (ideas, frames and checks). Flow is driven by background `flow-veo` agents (Sonnet).
**Authorization:** Dan, 2026-11-07: "Give me separate handoffs for #1 and #4." Item #4 was "Reusable gag and B-roll clips for the clip library", meaning generic moments any future edit can pull without generating anything new. Do every step without asking. Stop only for Dan's frame-pair approvals (a standing rule) and for anything that would cost money.
**Deadline:** the plan drops from the $199.99 Ultra (20x Pro) to the $99.99 Ultra (5x) on **Nov 29, 2026**. Spend this work's share by **Nov 28**.

## Credit budget

- **Balance:** 22,266 on 2026-11-07.
- **This handoff:** up to **7,000**, about 700 Veo 3.1 Fast 8 s takes.
- **Other handoff:** the clips-for-next-edits handoff (`handoff-20261107-flow-credits-ai-clips-for-next-edits.md`) gets up to 14,000, and it goes first when both want Flow on the same day.
- **Reserve:** about 1,200 credits stay untouched.
- **Logging:** read the balance before and after every batch, and log it in the shared `Media/flow-credit-log.md`.
- **Money:** never pay, top up or buy credits.

## What to make

About 60 to 100 finished reusable clips, chosen from gaps in the library, not from guesses.

1. **Find the gaps.** Go through the shot needs that keep recurring across recent scripts and revision docs:
   - the excuse gags;
   - eating, cravings and junk food versus salad;
   - weighing in and the mirror check;
   - waking tired;
   - phone scrolling;
   - gym intimidation;
   - the trainer upsell;
   - age 40+ moments;
   - before-and-after concepts;
   - generic gym, kitchen and street B-roll.

   Also mine `Docs/` revision docs, `Handoffs/video-editing/*.md` and the last month's scripts for lines that asked for a clip. Run `clip_library.py find` for each need, and list only the ones with no good hit. Write the list to `Media/clip-library/gap-list-20261107.md`, ranked by how often the need came up.
2. **Mix of people.** Follow the library categories (ai-dan, people, food-nutrition, gym-and-exercise, lifestyle, concepts-and-gags):
   - **AI Dan:** mostly, since Dan picks AI images of himself most often.
   - **Other people:** add generic men and women where a gag needs someone other than Dan.
   - **Shapes:** make both 16:9 and 9:16 versions of the best ones, because Shorts need vertical.
3. **Not exercise demos:** those have their own handoffs.

## Standing rules that apply (read before starting)

Read these first:
- `.claude/skills/_shared/VIDEO-RULES.md`: the top section, the AI clip rules and the AI label rule.
- `.claude/skills/_shared/IMAGE-GENERATION.md`, "Blind Google test".
- `.claude/skills/_shared/cliplib/README.md`.
- `.claude/skills/_shared/veo/README.md` and `FLOW-RUNBOOK.md`.

Rules:
- **Frame pairs:**
  - Every clip idea reaches Dan first as two complete, unlabeled START and END pairs: one made by Codex (`codex-image.sh`) and one by Google Nano Banana Pro in Flow, free, per `_shared/blind-image/FLOW-IMAGE-RUNBOOK.md`, with each END made from its own START.
  - Register both pairs with `blind.py`.
  - Every pair passes `framecheck/gate.py` and a fresh `frame-reviewer` first.
  - Google keeps the camera still only when the prompt says outright: "keep the framing identical: do not zoom, crop, pan or re-center; no new objects."
  - Keep pose changes small, because Google redraws limb proportions on big moves.
- **Clip quality:**
  - Each clip has cause and effect.
  - The look is calm and real, with a closed-mouth smile and no shake.
  - No AI giveaways: melting hands, warped faces, mirrors fogging, breath smoke.
  - Regenerate a sloppy take instead of patching it.
  - Check every AI Dan face against the identity reference `Media/exercise-demos/_character/ai-dan-canonical.jpg` and the photo references the clip skills use.
- **Approvals:**
  - Put up one review page per batch of 25 to 40 ideas, phone layout first.
  - Each idea shows a one-line description and what video moment it serves, plus the two unlabeled pairs, with X1, X2 or reject.
  - Log his picks with `blind.py pick`.
  - Run one batch a week, interleaved with the next-edits handoff's batches so Dan isn't flooded.
- **Video:**
  - Generate the videos in Flow with background `flow-veo` agents (`veo.py add` for approved pairs), up to 3 agents at once, each in its own tab.
  - Agents never close tabs they didn't open.
  - Check the motion with `clipcheck.py` and a motion reviewer.
- **Filing:**
  - Register each good clip with `clip_library.py add --kind ai --status usable-unused --category <cat> --people <...> --model veo-3.1-fast --prompt "..."`.
  - After each batch, run `clip_library.py sheet`.
  - Rejected takes never go in.

## Deliver

- **Each batch:** the review page link in chat, the credits used so far, and the two wrap-up boxes. Stop there for Dan's picks.
- **By Nov 28:** `Docs/FLOW_CREDITS_CLIP_LIBRARY_RECEIPT_20261128.md`, listing:
  - the gap list;
  - the clips added, with their IDs and categories;
  - credits used;
  - the blind-test pick counts by batch (labels only; never reveal sources unless Dan asks for the scorecard);
  - anything left half done, with the exact next step.
- **Board:** keep one board entry under 80 words for this work while it is running.

## Progress (2026-11-07, Claude session "Clip library: reusable AI clips (Flow credits)")

- Gap list written: `Media/clip-library/gap-list-20261107.md` (52 recurring needs, ranked; main gap: almost no AI Dan versions, few verticals).
- Batch 1: 28 ideas drawn as Codex and Google START/END pairs, every pair gated and independently reviewed; each failed version got one corrected redraw, a second failure dropped it. Result: **18 ideas on the page, 4 with two blind versions (X1/X2), 14 with one.** 9 ideas dropped (both versions failed: snooze, salad vs burger, chips, fridge stare, old shirt mirror, plate photo, wide gym, stairs, buffet) plus the jeans idea (belly focus).
- Review page (phone first, picks save to the page's store): https://claude.ai/artifact/Emyh9ByuYemSPfo5fRrWtd . Read picks with ArtifactData `list` collection `picks` on that URL.
- Work folder: `~/Projects/_edit_work/CLIPLIB-FLOW/` (b1/ ideas, tools/, page/, review-fails.txt, motion-notes.txt, google-redo-notes.txt). Blind keys in `b1/<ID>/blind/.blind-key.json` (two-version ideas only; never show).
- Credits: 22,226 before and after (no video generated yet).
- Lessons: lockstill with tight boxes leaves ghosts and seams, so gate the raw END first and box each person's whole path including shadows and reflections; Google failed far more reviews than Codex on these gag frames (scale digits, food/hands continuity, faces changing).
- **Next:** read Dan's picks; log two-version picks with `blind.py pick b1/<ID>/blind --chose X?`; `veo.py add` each picked pair (Veo 3.1 Fast, 16:9, prompt from `idea.json` motion_prompt plus `motion-notes.txt`), up to 3 `flow-veo` agents; clipcheck + fresh reviewer per take; file keepers with `clip_library.py add --kind ai --status usable-unused`; then `sheet`. Then 9:16 versions of the best, and batch 2 from the gap list.

## Progress 2 (2026-11-07, same session)

- Dan approved all 18 batch-1 ideas. Video done: 17 clips filed as **A0229 to A0245** (`clip_library.py sheet` refreshed). Receipt: `Docs/FLOW_CREDITS_CLIP_LIBRARY_RECEIPT_20261128.md`.
- Credits used: 450 of 7,000 (balance 21,776).
- Dropped after three takes: both scale clips (garbled numbers), gym-door (morphing in a busy scene). Genetics Codex version: Flow rejects its END upload.
- Tools for the next batch are in `~/Projects/_edit_work/CLIPLIB-FLOW/tools/` (gen_codex, prep_google, mkspec, lockgate raw-first, build_page, gen_page, take_spec, motion_gate2, mbrief2, file_keeper, file_queue). Trap: a `while pgrep -f X` wait loop matches its own command line and never ends; run chains directly with nohup.
- **Next:** batch 2 ideas from the gap list (see receipt "Open / next"), then 9:16 versions of the best clips.
