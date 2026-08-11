---
name: prioritize
description: Brainstorm and rank what Dan should work on next — "what should I use my limit for", "what's the priority", "help me plan my hour/day". Reads the dashboard, coordination file and open handoffs, then delivers a ranked recommendation with a ready-to-paste starter prompt per item. NEVER executes the recommended work — Dan runs execution in separate sessions to preserve tokens and context.
---

# /prioritize — brainstorming & prioritization session

## The one hard rule

**This session's deliverable is the recommendation, not the work.** Do NOT start executing anything recommended — no browser driving, no code edits, no content drafting, no handoff execution. Dan deliberately runs execution in separate sessions to save tokens and keep each execution session's context clean. This is the standing exception to the bias-toward-action rule (CLAUDE.md, 2026-08-11). Reading and light verification (a curl, a grep, a status check) to *ground* the recommendation is fine and encouraged; producing the deliverable of a recommended task is not.

The only writes allowed in this session: updating this skill, memory, or the coordination/task boards if Dan asks.

## What to read before recommending (all cheap, do in parallel)

1. **Dashboard tasks:** `curl -s https://absbyai.com/api/todos` and `curl -s https://absbyai.com/api/task-checks` — what's open, what priority, what's already done. Remember `business` displays as `money`.
2. **`AI_COORDINATION.md`** — the active task, anything another session owns right now (do not recommend work that would collide with it), and "EXACT NEXT ACTION" lines.
3. **Unexecuted handoffs:** Key tasks whose `why` names a `handoff-*.md` file, cross-checked against the coordination file for whether they already ran.
4. **Anything time-sensitive:** deadlines recorded in task `why` fields or the coordination file (store-review windows, targetSdk dates, ad-account states, shoot dates).

## How to rank

In rough order of weight:

1. **Time-sensitive / decaying** — something that gets worse or expires if not done now (compliance windows, a reinstated-but-watched ad account, review deadlines).
2. **Unblocking** — work that unblocks revenue or other queued work (a skin that gates a campaign, a fix that gates spend).
3. **Claude-executable solo** — prefer items an agent session can finish end-to-end over items needing Dan's hands (his time is the scarcer resource). Flag Dan-only items separately.
4. **Fit for the model tier** — flagship-model time should go to judgment-heavy, multi-surface, verify-heavy work. Well-templated repeat work (another content batch, another script from a settled template) can go to Sonnet; say so.
5. **Sized to the window Dan named** — if he said "an hour", don't lead with a multi-day build.

## Output format

- A short ranked list (3–5 items max), each with one or two sentences of reasoning — why now, what it unblocks, roughly how long.
- **A ready-to-paste starter prompt for each recommended item**, so Dan can open a fresh session and paste it. If a handoff doc exists, the starter prompt should point at it by path and say "execute it"; if not, the prompt must be self-contained.
- Name which items need Dan personally vs. which a session can run alone.
- Name anything deliberately ranked low and why, in one line, so it isn't re-litigated.
- Then STOP. Do not ask "shall I start?" and do not start.

## Lessons

- **2026-08-11, the miss that created this skill:** Dan asked "what should I use my limit for?"; Claude gave good priorities and then immediately started driving Google Ads and drafting content in the same session — colliding with two other sessions Dan had already spun up for exactly that work. The recommendation was the whole job.
