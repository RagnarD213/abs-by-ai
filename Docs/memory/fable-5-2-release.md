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
- format: date, video title, reviewer found X, Dan later flagged Y.
- 2026-11-09, Flow-credits batch 2 AI clip frames (Why I Use Machines At 41 / Walk Between Your Sets), 3 frame-reviewer runs on Fable 5.2 high:
  (1) B2-01 Can't Go In: FAIL, caught a walking stride that would need a backward slide to reach END, legs 10.6% longer in START, a gym bag hanging from no strap (all real; my own screen missed them).
  (2) B2-02 Sitting On His Phone: PASS, noted the gate measured nothing so its PASS rested on its own measurements.
  (3) B2-03 Jogging Between Sets: FAIL, caught same-side arm and knee forward (nobody jogs like that); my screen missed it.
  Cost ~176-194k tokens each vs ~140-160k for Opus reviewers. Dan's verdict on these frames: pending.
- 2026-11-09, Three More Exercise Demos R3 (Dumbbell Fly, Overhead Triceps Extension seated), extra Fable 5.2 high frame-reviewer runs:
  (4) Fly bent-elbow Codex pair: FAIL, caught THREE arms in START (my own screen missed it), near elbow 155 to 65 deg (press, not fly), changed background machine and soft floor patch. ~209k tokens. Dan's verdict: pending.
  (5) Seated triceps Codex pair: FAIL, measured dumbbell 12% longer, upper arms 8-11% longer, half rep with forearms resting on the head, knob hands; gate had passed. ~200k tokens. Dan's verdict: pending.

## Blind tests vs Opus (2026-11-09, after Dan's limit reset)
- **Graphics test:** same locked brief (full-screen Soft Blue HyperFrames comparison, "Love Handles Go Last", 8.5 s, test only), Opus 5.5 high vs Fable 5.2 high, no peeking. Both passed Claude's checks (no frozen frames, title-safe clean). Dan picked Fable blind: "slightly better, but it's a very slight difference." Fable: larger type, solid pills, red row; Opus: amber, smaller eyebrow. Tokens: Fable ~249k, Opus ~234k (Fable costs ~2x allowance per token). Files `~/Projects/_edit_work/GRAPHICS-FABLE-TEST/`.
- **Chroma key test:** locked R2 key re-run byte-identical to approval (C1730 sample). Fable (2 attempts, ~473k tokens, ~100 min) changed only stage 1.5: flicker 0.686 to 0.624, hair 0.677 to 0.593, hair worst 1.173 to 0.933 (Claude re-measured, matched); rim flat (0.0266 to 0.0267), see-through 402 px/24 frames to 311/25, specks 0. Not a clean sweep, so no promotion. Indistinguishable at 2x. Dan's blind pick: pending (page :9462). Files `~/Projects/_edit_work/CHROMA-FABLE-TEST/RESULT.md`.
- **VSL script test (2026-11-10):** blind three-way, same brief on Dan's own Great Again T outline, all extra-high effort: Fable 5.2 ranked 1st by Dan (most natural language, smoothest transitions, best counterintuitive swap, strongest ingredient/nutrient breakdowns), Opus 5.5 2nd, Codex Astra 3rd. None shippable. ~332k tokens Fable vs ~297k Opus. Detail: `Docs/VSL_SCRIPT_CONTEST_RESULT_20261110.md`.
- Takeaway so far: Fable edges Opus on motion-graphic polish and numeric key tuning, at roughly double the allowance; gains are small. Related: [[model-routing-plan]].
