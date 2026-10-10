# Voice bench ledger

Every setup scored on the blind bench (`scripts/voice/bench.py`): 40 held-out passages of Dan's, 80 trials (a fresh
Opus 5.5 and Gemini each judge every pair). "Caught" is how often a judge picked the AI piece. Chance is 50%, the
goal is 60% or less, and about 8 trials in 80 is noise. A change is kept only if it moves the number.

| date | setup | what the writer saw | caught | Opus judge | Gemini | long-form | shorts | ads | conversion | products | verdict |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 10-08 | `cold` | nothing | 69 of 80, 86% | 100% | 72% | 100% | 50% | 75% | 92% | 94% | floor |
| 10-10 | `guide` | the old guide: rules, examples, facts (re-judged with equal dash handling) | 73 of 80, 91% | 100% | 82% | 100% | 75% | 80% | 92% | 100% | baseline |
| 10-10 | `set5` | 5 whole real passages by format and length, no rules | 66 of 80, 82% | 98% | 68% | 79% | 75% | 70% | 92% | 100% | **KEPT: the method** |
| 10-10 | `pairs5` | 5 worked pairs (brief, Claude's version, his version) | 69 of 80, 86% | 100% | 72% | 88% | 88% | 70% | 92% | 100% | dropped: weaker than set5 |
| 10-10 | `set5-core` | set5 plus the core and type notes | 74 of 80, 92% | 98% | 88% | 92% | 88% | 90% | 92% | 100% | dropped: worse than set5 (9 trials newly caught, 1 newly fooled, p = 0.02) |
| 10-10 | `set5-crit` | set5, then a critic and checker revision pass | 66 of 80, 82% | 98% | 68% | 83% | 75% | 75% | 75% | 100% | dropped: no change (8 trials each way) |
| 10-10 | `set12` | 12 passages instead of 5 | 64 of 80, 80% | 98% | 62% | 88% | 88% | 50% | 92% | 94% | dropped: inside the noise (p = 0.77), more cost |
| 10-10 | `set5-fable` | set5 with Fable 5.1 as the writer | 65 of 80, 81% | 100% | 62% | 75% | 88% | 70% | 83% | 100% | dropped: no change; Opus stays the writer |

Gemini column: includes the few pairs where Sonnet 5.5 stood in because Gemini refused the pair.

## What the rounds say

- **Real passages with no rules is the only thing that moved the number**: 91% to 82% (10 trials newly fooled, 2
  newly caught, p = 0.065 on one run). It held on two more independent runs of the same idea (`set12` 80%,
  `set5-fable` 81%): pooled, 195 of 240 trials, 81%.
- **Voice notes in the writer's prompt cancel the gain.** Same passages plus 1,200 words of notes: 92%.
- **A revision loop does not help.** The checker's score fell from 22 to 8 (his own held-out passages score 17), so
  the drafts' numbers ended up "better than Dan's", and the judges caught them exactly as often. The critic, with
  no real version to compare against, called 29 of 40 drafts "would pass".
- **The hard judge is the wall.** A fresh Opus with 8 reference passages was right 39 or 40 times of 40 on every
  setup. The whole gain is with Gemini (82% to 68%). Dan himself, on the first page, was right 13 of 19 (68%).
- **By type:** long-form content moved most (100% to 79%), ads some (80% to 70%), conversion and products not at
  all. Written books and sales scripts are where Claude is furthest from him.
- **Still above the 60% goal.** By the plan's own gate, Phase C (a small model trained on his text) is the next
  step, along with Lane 1 (his words first) for the pieces that matter most.

## Dan's blind pages

| page | pairs from | Dan's score |
|---|---|---|
| Round 1, https://claude.ai/artifact/P7rivcXAjD9weMTyupvTfm | `guide` run, 20 pairs | picked his own in 13 of 19 (68%), 2026-10-10 |
| Round 2, https://claude.ai/artifact/QbzMfnMzQzNsrGDxCyRydK | `set5` run, the 20 passages he has not seen | open |

Round 2 uses every held-out passage he has not seen. A third page needs new held-out passages first (his next
off-the-cuff takes, ads and letters).

## Costs, 2026-10-10

Six new bench runs and eight re-judged baseline trials: about $3.30 of Gemini. Every Claude call (bank briefs, cold twins, writers, judges, critic) ran on
the subscription.
