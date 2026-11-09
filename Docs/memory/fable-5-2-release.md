---
name: fable-5-2-release
description: "Fable 5.2 launched 2026-11-09: first Fable that beats Opus 5.5 on most benchmarks (coding, agents, charts); writing/design not better; the analysis given to Dan"
metadata:
  node_type: memory
  type: reference
  originSessionId: 1d04aab9-a324-4f28-9baf-3564413c0396
  modified: 2026-11-09T22:25:33.374Z
---

Claude Fable 5.2 (`claude-fable-5-2`) launched 2026-11-09, with Mythos 5.2 (same model minus cyber/bio safeguards, vetted orgs only). API $8/$40 per M (Fable 5.1 $10/$50, Opus 5.5 $4/$20). Max: included up to 50% of weekly limit, shares the Claude Code pool. Default effort medium; Anthropic still says start with Opus 5.5 as "daily driver", move up to Fable for the most ambitious open-ended technical work.

Anthropic table (Fable 5.2 vs Opus 5.5): FrontierSWE v2 69.9 vs 62.3; FrontierCode 2.0 49.1 (xhigh) vs 45.5; AutomationBench 51.4 vs 42.5; Remote Labor Index 41.3 vs 21.3; Chartography 73.4 vs 64.4; HLE tools 74.2 vs 67.7; OSWorld 2.1 89.3 vs 87.2. Opus wins AA-Briefcase Elo 1800 vs 1785 and GDPval-AA 1866 vs 1831. Independent: Vals Index #1 (71.3, Sonnet 5.5 70.9); Artificial Analysis 65 vs Opus 59; Terminal-Bench 4.0 tie at higher cost. Max effort scored below xhigh on FrontierCode.

Early users: code review found 3-4 of 5 planted defects vs Opus 1-2; most other head-to-heads tie; writing "not settled" in a blind test; reviewers won't let it design websites alone; judges video from still frames and claims success before checking; over-cautious, approval loops; cyber tasks blocked (fall back to Opus 4.8).

Adopted 2026-11-09 (AGENTS.md, Model routing): Opus 5.5 stays default for writing, design, video edits, photo picks. Fable 5.2 high for hard coding (multi-file app/payment/pipeline builds, bugs Opus missed), code review of risky changes, and a trial as the blind video/frame reviewer. Never max. Related: [[model-routing-plan]], [[fable-included-in-max]], [[opus-5-5-release]].

## Reviewer trial log (3 rounds, then decide)
- (none yet) format: date, video title, reviewer found X, Dan later flagged Y.
