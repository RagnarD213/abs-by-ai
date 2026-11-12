---
name: video-orchestrator
description: Supervise a Codex video edit with Astra directing a Sol production worker, or run an authorized blind comparison against all-Astra and all-Sol edits. Use for requested video orchestration and measured model trials; ordinary edits keep their existing workflow.
---

# Video orchestrator

This delegates work within the existing editing system. Read the live project
AGENTS.md, AI_COORDINATION.md, job handoff, source map, VIDEO-RULES.md in full,
and applicable editing skill. Keep all source, audio, graphics, generation,
approval, independent-review, edit-cap/render-queue and silent-check rules.
This skill does not approve a film or authorize setup/upload/publishing.

## Mode and model contract

- **Orchestrated edit:** Astra owns direction, consequential exceptions and
  acceptance; one Sol worker owns production through self-QA.
- **Blind comparison:** read [the trial protocol](references/blind-test.md).
  A neutral controller prepares identical inputs and isolated production arms.
  It must not improve baseline arms using its own editorial judgment.
- Preparing a skill, handoff or starter prompt does not launch an edit or chat.

Verify models in the destination's supported catalog. Dan explicitly selected
`gpt-6-astra` and `gpt-6.1-sol`, **high effort**, for the November 11 trial.
This overrides the normal newest-Sol default only for the authorized arm.
Never silently substitute an unavailable model or downgrade effort.

## Astra directs; Sol produces

Use native subagent tools with explicit model/effort. Start the Sol production
worker in a **fresh context** (`fork_turns="none"` where supported); some
clients force full-history forks to inherit the parent model. Give a complete
brief with outcome, source paths, rule reading order, approvals, isolated job
directory, stage, required checks and stop conditions. Confirm observed model
and effort from runtime metadata, not merely the requested settings.

One production worker owns take selection, timeline/build files, previews,
graphics and repairs. Astra directs once, intervenes on consequential problems
and assesses actual media at required stage boundaries. It does not repeat the
worker's tasks or supervise every cut. A summary is not picture/audio evidence.
Resume the same worker where supported rather than continually recreating it.

Use the existing WORK_PACKET/manifest for approvals, sources, changes, stage,
evidence and next action. Do not add competing approval databases. Don't spend
model turns polling renders; use supported completion signals and the queue.
Fresh mandatory reviewers remain independent. An ordinary hybrid edit uses an
explicit Astra complete-candidate reviewer; specialized asset checks remain.
Dan's judgment decides quality, not a panel score.

## Track all work

Register parent, worker, reviewer, helper, retry and continuation sessions from
the start. Keep raw logs outside the public repo. `scripts/trial.py` tracks the
comparison. Native session JSONL provides observed models/effort and cumulative
tokens; `codex exec --json` is a fallback. Never register both representations
of one session. Log unavailable evidence explicitly.

Input includes cached input; output includes reasoning. Do not add those
subsets twice. Keep cache-write counters separate. Unknown subscription credits,
rate-limit effects, prices or charges stay unknown, not zero. Tokens do not
prove allowance savings. Separate rendering/queue time, external generation
spend and waiting for Dan from model usage.

Maintained source: `skills/video-orchestrator/`. Install the complete validated
folder at `~/.codex/skills/video-orchestrator/`; don't change global defaults.
New chats discover it; existing chats can read its absolute path. Installation
and synthetic checks do not mean the video comparison has run.
