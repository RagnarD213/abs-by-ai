---
name: claude-codex-major-decision-template
description: "Dan's template (2026-10-28) for major business decisions: Claude and Codex each plan independently, Claude verifies disputed facts, compares in a table, merges the best into one handoff a cheaper model executes"
metadata:
  node_type: memory
  type: feedback
  originSessionId: ceee13ec-8e0f-492d-9a6d-d7e71c250812
  modified: 2026-10-29T20:44:03.989Z
---

Dan, 2026-10-28, on the content-schedule overhaul: "excellent job collaborating with Codex on this and combining the best ideas into one handoff. This is an excellent example of how, in the future, you can collaborate with Codex on important business decisions. Let's save this as a template."

**The template (major decisions: schedules, strategy, budgets, offers, big process changes):**
1. **Two independent plans.** Claude and Codex each research and write a plan from the same brief, without seeing each other's. Claude pulls real data first (YouTube Studio via Chrome, Ads, Blotato, repo inventory), plus a background research subagent for outside evidence. Plan only, no execution (brainstorm rule).
2. **Verify before conceding.** When the plans disagree on a fact, check the source yourself (shoot report, live account read) and say plainly who was right. In the reference case Codex was right twice: the ad budget was $60/day, not $30, and the Sept 23 shoot was not kitchen.
3. **Compare in one table** (topic / Claude / Codex / merged), then "what Codex got right" and "what I kept from mine", each with the reason. Credit the other plan honestly. Withdraw your own claims the data no longer supports (e.g. the subscriber projection, once the paid subscribers turned out to barely watch).
4. **Merge into ONE handoff** that keeps the strongest parts of each. Here that was Claude's concrete dated calendar and Codex's data-led safeguards: engaged views, readiness buffers, expand-only-if rules, and verifying settings from footage. Mark the other handoff superseded in `Handoffs/README.md` and keep its doc as the evidence record.
5. **Iterate with Dan's answers.** Answer his follow-ups with counts against capacity, put his approval quote at the top of the handoff, and narrow the scope to exactly what he asks (here, ad budgets were removed because he changes them by hand).
6. **Hand off to a cheaper model** (Codex newest Sol, high, for ops) with a starter prompt. The executor's first step is to verify whatever is still unconfirmed.

**Why:** the two models catch each other's mistakes and blind spots. The merged plan was better than either one alone.

**Second reference case (2026-10-29, Upwork client plan).** Dan: "excellent job collaborating with Codex on this. I thought your unified plan was slightly better than Codex's, although you both made some important contributions. This is another good example." What made it work:
- Claude checked live state Codex hadn't (the Upwork profile in Chrome; unverified ID was the blocker).
- Claude verified a Codex correction on the primary source before conceding (Upwork testimonials retired) and said plainly that Claude was wrong.
- Codex's concrete pieces were adopted: $75/$150 trials, a $500 ceiling spent in tranches, payment timing, checkpoints, measuring by Dan's minutes.
- Claude kept its own points where its evidence was stronger (Freelancer Plus economics, off-Upwork outreach, all four source videos).
- The merge added ideas neither plan had (outreach buyers purchase the trial on Upwork for a real review; trials as permanent tripwire products).
- Files: `Docs/UPWORK_CLIENT_PLAN_MERGED_20261029.md`, which includes the comparison table in section 4.

**How to apply:** for any major business decision, offer to run it this way (ask Codex for an independent plan, or compare against one Dan brings), and follow these steps. Reference case: `Handoffs/handoff-20261028-content-schedule-overhaul.md` vs `Docs/CONTENT_STRATEGY_RECOMMENDATION_20261028.md`. Related: [[model-routing-plan]], [[codex-owns-non-core-work]], [[handoff-starter-prompt-rule]].
