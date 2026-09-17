---
name: plantheday
description: Plan and prioritize Dan's workday for Abs By AI from his current ideas, relevant recent tasks, and a checked dashboard. Produce a realistic schedule and ready-to-paste task prompts with model and effort recommendations. Use for /plantheday, planning today or tomorrow, or deciding what deserves today's attention.
---

# Plan the day

Help Dan decide what deserves his time, contribute a few well-grounded ideas, and produce a usable day plan. Business priorities: profitability, adoption, product quality, then marketing performance. Explain decisions plainly and challenge busywork that crowds out the main outcome.

## Scope

This is a planning conversation. Read and verify enough to ground recommendations; do not execute recommended projects, start editing/rendering, send messages, create tasks, or dispatch agents unless Dan explicitly asks. Skill creation or refinement requested in this conversation is permitted. Give starter prompts directly in chat so Dan can launch the work himself. Continue adjusting the plan when he adds ideas.

## Evidence and conversation

1. Start with Dan's current ideas, stated priorities, deadlines, energy, and constraints. These are the primary source. Do not make him repeat information already supplied.
2. Ask early for missing work windows, appointments, or a decision that changes the plan; continue independent reading while awaiting his answer. Without exact times, give ordered blocks and label assumptions.
3. Read `AI_COORDINATION.md`, inspect pinned and relevant recent tasks with available task tools, and read only the handoffs needed for candidate work. Prefer compact status and final messages over complete tool histories. Use returned task titles verbatim. A pin is not proof work is unfinished; distinguish running, review-ready, blocked, completed, and unknown.
4. Read the live dashboard at https://absbyai.com/dashboard through its APIs using `.claude/skills/dashboard-tasks/SKILL.md` for authentication and mechanics. Read `/api/todos`, `/api/task-checks`, and `/api/plan`; interpret completion from task-checks. If access fails, disclose it and proceed using current conversation and verified local context.
5. The dashboard and coordination board are fallible memory. Check dated or contradictory rows against newer evidence before reviving them. Do not turn the entire backlog into today's agenda. Check editor-deliveries `state.json` pending items when relevant; do not send or file editor work within planning.

## Prioritize and schedule

- Name one principal outcome and two or three supporting outcomes, each with a concrete definition of done. Distinguish business importance from launch order: a brief decision may go first to unblock background work.
- Favor deadlines, revenue/conversion bottlenecks, and prerequisites over more content volume or speculative features. Add only a few ideas beyond Dan's list; say what evidence supports them and whether the evidence is historical or freshly verified.
- Separate Dan's decisions and physical work from agent work. Protect substantial uninterrupted time for the highest-value Dan work. Allow lunch, transitions, review time, and a firm stopping point.
- Respect gym/travel windows and the provider-limit resets Dan reports. Never assume another provider's balance or reset is verified. Do not fill quota merely because it exists.
- For video work, use `Handoffs/video-editing/00-MASTER.md` and current owners. Do not duplicate an owned job. Maximum two simultaneous video builds/QC pipelines across all local sessions and providers; new jobs wait for capacity. Planning or scriptwriting can proceed independently.
- Give a small ranked plan plus a time-block table. Explain what is deferred and why. Frame ambitious output as a target, not a guaranteed completion time.

## Ready-to-paste prompts

For each recommended agent assignment, provide: exact existing task title or proposed new task title; provider; model and effort; self-contained starter prompt; expected deliverable and any dependency. Continue the owning task when its context is useful. Never create new tasks merely because you recommended them.

Point to verified handoff paths when available, and tell the next task to recheck ownership and current status before execution. Carry forward project rules and task-specific restrictions, including private trials, approvals already given, same-person before/after, approved audio, and delivery checks. Do not convert a review request into publication authorization.

Choose models from currently available settings and official guidance when needed. Use stronger models for difficult creative judgment or unresolved audio/graphics work, and economical models for bounded reconciliation/status tasks. Identify recommendations as judgment, not benchmark facts. Do not invent Grokbot/Claude models or settings; use the user's known setup or explicitly leave the model choice to that setup.

## Dashboard hygiene

Do not inherit /prioritize's automatic task intake: mentioning an idea during planning is not a request to grow the backlog. Offer a focused plan without auto-adding handoff rows. Only add a handoff row when Dan explicitly asks. Respect current authorization for focus-plan updates and completed-task checkoffs; freshly read all data, preserve unrelated fields/lists, and verify saved results.

When Dan requests cleanup, distinguish verified completed tasks, obsolete candidates, duplicates, blocked items, and still-valid later work. Do reversible, evidence-backed changes within authorization. Do not delete or rewrite Dan-authored tasks without his specific authorization. Never mark blocked work complete. A cleanup proposal can be a bounded separate task; do not let it displace the day's main work.

For tomorrow, use tomorrow's date and actual known constraints. Do not assume /prioritize's Claude-only morning-brief integration exists in Codex or create a reminder without a request.
