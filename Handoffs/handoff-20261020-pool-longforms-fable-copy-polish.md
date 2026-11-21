# Handoff: final copy polish of the seven 10/23 pool long-form scripts (Fable)

Written 2026-10-20 by Claude (Opus 5.5). Type: CONTENT (LFC scripts, not ads). Not a video edit.
**Model: Fable 5.1, high effort (Dan asked for Fable by name).** Task name: `Pool Long-Form Scripts Copy Polish`.

## Goal

One final copy polish of the seven long-form scripts Dan reads by the pool on **Friday 10/23**, then the filming
documents, so he can load the teleprompter that morning. Run `/copy-edit` (its "Polishing scripts, not sales copy"
section and the "Straight in, or tracked" rule): edits Dan is sure to accept go straight into the Doc, anything
uncertain goes in as a tracked suggestion.

## Where

- Scripts doc: "Gym Shorts Scripts - Friday 10-23 Pool Shoot",
  https://docs.google.com/document/d/11nUmri621xbb7K44Wxan7IAljK2mJeizDFCRgK752AA/edit
- **Scope: from the heading `SCRIPT: I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time` to the end of
  the doc** (seven `SCRIPT:` headings). The 29 shorts above it already had two polish passes; leave them alone.
- Dan's finished text as of 2026-10-20 (your baseline): `Docs/SCRIPTS_1023_POOL_LONGFORM_DAN_EDITED_20261020.md`.
- What he changed and why: `.claude/skills/scriptfromoutline/SKILL.md`, section THE 10/23 POOL LONG-FORMS (P to Y), and
  `.claude/skills/scriptfromoutline/references/dan-edits-2026-10-20.md`. Read both before touching anything.
- Docs connector mechanics (read_doc output is large: save it, parse with Python; write with `targetRevisionId`; Dan
  may be typing in the doc at the same time): `/copy-edit`, "Mechanics: edits through the Docs connector".

## The seven scripts

1. I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time (1452 words)
2. The 5 Muscles Women Notice First, And The Machine That Builds Each One (1078)
3. How To Fix Your Posture At The Gym And Instantly Look Leaner (1084)
4. Stop Squatting, Deadlifting And Bench Pressing: The Machine-Only Plan That Got Me Abs At 40 (996)
5. Bulking Is A Scam: Why 95% Of Men Should Never Bulk (1220)
6. Why I Never Get Sore, And Why Soreness Means You're Doing It Wrong (1115)
7. Body Part Splits Are Dead: Why I Train My Whole Body Every Day (1131)

## Decisions already made (do not reopen)

- **The openings were cut hard on purpose.** Every script goes hook, at most one credibility line, a sentence or two of
  context, then point one. Do not add back an agenda, "let's get into it", "stick with me" or any warm-up. If you see a
  remaining warm-up line before point one, cutting it is a sure edit.
- **Keep every line Dan wrote on 2026-10-20** (the `>` lines in the diff): his CAPS words, the swear in the bulking close,
  the Brad Pitt split-screen cue, his bulking story, his softer "more likely to skip". Fix only typos and flow around them.
- Scripted claim lines are pre-approved (AGENTS.md): no claims, compliance or "PROVEN" commentary. This is organic
  content, not sales copy.
- No em dashes or en dashes in the scripts. His spaced hyphen (" - ") is his style; keep it.
- Leave curly versus straight apostrophes as they are; churning them is noise in the diff.

## Specific things found while reading his edits

Sure (straight in):
- Bulking: "But if you're fat and strong, you just look sloppy" has no closing period.
- Stop Squatting: "So between those three exercises, I'm covering what the deadlift was doing" now covers four exercises
  (Dan added the leg press). Make it "four", or drop the count.
- Recount every word-count line at the top of each script (spoken words only, not the [BRACKETED CAPS] cues; minutes at
  about 150 words a minute).

Uncertain (tracked, with a one-line reason in the suggestion):
- Bulking: "Move to a 10% caloric deficit - about a net cut of 500 calories." On the script's own 2,500-calorie example,
  10% is 250; 500 would be 20%. Suggest either "about 250 calories" or "a 20% deficit"; Dan picks.
- Bulking: "Even a guy without that much muscle looks great if he's lean" sits after "That's why it's better to cut down
  until you can see your abs first..." and reads as an afterthought. Suggest moving it and the Brad Pitt cue up, after
  "the lean guy with abs is the one who looks bigger."
- Never Sore: Firas Zahabi is now introduced twice in a row ("one of the best MMA coaches in the world. He coached
  Georges St-Pierre" then "Firas trains some of the most elite MMA athletes in the world"). Suggest cutting the second
  introduction clause and keeping his THEY / YOU line: "If he's recommending THEY never get sore, YOU should definitely
  never get sore from a workout."

Then the normal pass: typos, a repeated sentence or word, a line Dan would trip over reading aloud, consistent numbers
across scripts (one warm-up set of 10 to 15 reps, two working sets of 8 to 12, 2 to 3 seconds down, explode up; add
weight at 13 reps; 15-minute workouts in script 1).

## Steps

1. Read `/copy-edit` SKILL.md in full, then the two reference files above.
2. Read the doc fresh. Diff its long-form section against the baseline file; if Dan changed anything since 2026-10-20,
   his version wins.
3. Apply sure edits directly; add uncertain ones as tracked suggestions (`suggest_builder.py`,
   `verify_suggestions.py` in `.claude/skills/scriptfromoutline/references/gdoc_edits/`). Verify with a whole-doc
   export that nothing outside the edited spans moved.
4. Write the as-delivered record `Docs/COPYEDIT_POOL_LONGFORMS_1023_AS_DELIVERED_20261020.md` (straight-in list, tracked
   list, left alone) and push it with `scripts/git/safe-push.sh`.
5. Report to Dan in chat: what went in directly, what is tracked for him, links. Wrap-up boxes.
6. Once Dan has ruled on the tracked suggestions, make the filming documents per `/copy-edit`, "When the scripts are
   final: make the filming documents" (teleprompter copy with no blank lines, cues stripped), in time for Friday 10/23.

## Current state

- Scripts are in the doc with Dan's 2026-10-20 edits. No polish run yet.
- Unpushed local commits from the main folder (safe-push stopped on other sessions' merge conflicts): `ff823c5` (HOOKS.md
  rule) and the lessons commit from this session. A later safe-push carries them; they do not block this task.

## Starter prompt

> Pool Long-Form Scripts Copy Polish. Run the handoff at
> `Handoffs/handoff-20261020-pool-longforms-fable-copy-polish.md`: a final /copy-edit pass on the seven 10/23 pool
> long-form scripts in the scripts doc, sure edits straight in, uncertain ones tracked, keeping every line I wrote on
> 10/20 and the short openings. Then report and stop for my rulings before making the filming documents.
