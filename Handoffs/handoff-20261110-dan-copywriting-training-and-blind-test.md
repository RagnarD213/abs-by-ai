# Handoff: train and blind-test the Dan Copywriting skill (2026-11-10)

**Goal (Dan):** "The goal of this is for a blind reviewer to not be able to tell which one I wrote and which one the system wrote." Dan's limit is tight, so this was split off from the build. Do it when he fires it.

## Where things stand
- New skill: `.claude/skills/dan-copywriting/SKILL.md` (method, section map, style rules, "Never" list).
- Training set so far: `.claude/skills/dan-copywriting/examples/great-again-t-vsl-final-20261110.txt` (Dan's finished Great Again T VSL, 5,211 words) and the verbatim voice passages in `.claude/skills/_shared/voice/passages-conversion.md`. Learning log: `examples/LOG.md`.
- Old `/scriptwriting` is retired (stub redirects). The copy-edit skill is v3 (bold style layer by default).
- Background on why: `Docs/VSL_SCRIPT_CONTEST_RESULT_20261110.md`.

## Steps
1. **Grow the training set with copy Dan wrote himself.** Only his own writing, or Claude edits he accepted. Candidates to confirm with Dan in ONE message (list them, he answers yes or no per item): the "AI Got Me Abs at 40" sales letter (`1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o`), the /start VSL (`1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA`), the long VSL "AI Got Me Abs at Forty" (`1lHzTMJydS7CBH3yigTYDDv1g3z9AJMcqwaPNyyKcIVc`), his Great Again T outline (`1JA4ICZK7zh2wB73Acegteaq46SAMjludhXXLF5eAyes`), the 15 Steps launch material, The Sex God Method (Drive `1KVRHZ04oGliUoQd9EISUl0DySIVTu-C3`, his favorite example of his writing, though it is a product, not a sales piece), and any older sales videos he names. Export each to text with the Docs connector `read_doc` (large results save to a file; parse with python, never pull them into context) and save them in `examples/`.
2. **Index the examples by section type** (hook, empathy, cause, stakes, story, proof, reveal, future pacing, price, risk reversal, FAQ, close) in `examples/INDEX.md`, with file and line ranges, so a writer opens only the matching sections.
3. **Blind test.** Hold out 4 sections Dan wrote that the skill never saw (different types). For each, write a short outline of what the section says, have the skill write it, and present Dan's original and the skill's version unlabeled, shuffled. Ask Dan which is his (and two fresh reviewers too, as a secondary signal only; AI judges are not proof). Record results in `examples/LOG.md`. Pass: Dan cannot pick his own in at least half. Reuse the blind-bench approach in `.claude/skills/_shared/DAN-VOICE.md` if it helps.
4. **Fix from the misses.** For every section Dan spotted, write down what gave it away, add a rule or a "Never" line, and rerun only that section type.
5. **Repoint old references.** These skills still mention `/scriptwriting`: ad-copy, ad-edit, ad-outlines, copy-edit, dan-voice, imagesandclips, plantheday, design-sales-page, scriptfromoutline. Change sales-copy references to `/dan-copywriting`; leave the Doc delivery helpers.
6. **Later, separate skills per copywriter or company** (Dan's plan): for example V Shred copywriting and TestoGreens copywriting, each trained on that company's transcripts in `Docs/testosterone-funnels-20261105/VSL_TRANSCRIPTS.md` with the same structure as this skill. Separate handoffs when Dan asks.

## Model and cost
Fable 5.2, high effort, for the writing and the blind-test generations (it won the 2026-11-09 blind test). Sonnet 5 is enough for steps 1, 2 and 5. Keep each step lean: Dan's allowance is tight.

## Done when
Dan has done the blind test and cannot reliably tell his sections from the skill's, the rules from his picks are in the skill, and the old references point to `/dan-copywriting`.
