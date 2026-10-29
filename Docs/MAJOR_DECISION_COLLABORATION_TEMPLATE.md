# Claude and Codex collaboration for major business decisions

Dan approved this workflow on October 28, 2026, using the content-release strategy review as the example. Use it for consequential business choices where independent judgment can improve the outcome: marketing strategy, release plans, pricing, product priorities and substantial resource allocation. Routine execution and small decisions do not need two full analyses.

The aim is one better decision and one executable plan. Judge recommendations by business value and evidence. Neither AI owns the answer because it proposed it first.

## Workflow

1. **Give both AIs the same brief.** State the decision, objectives in priority order, constraints, dates, resources, existing approvals and what is outside scope. Share the same primary evidence where practical, with its date and definitions. Distinguish research from authorization to change live systems.
2. **Form independent recommendations.** Each AI explains its preferred approach, supporting evidence, key assumptions, workload, costs, tradeoffs and what would change its mind. Do this before reading the other's conclusions when practical, to avoid simply echoing the first proposal. Reuse verified factual extracts rather than paying to repeat every data pull.
3. **Exchange the actual proposals.** Compare the documents and supporting evidence, not summaries of what the other AI supposedly said. When Dan passes documents between chats, describe this accurately as a review of the other proposal. Do not claim direct AI-to-AI communication that did not happen. Use direct task messaging only with the required user authorization; this template does not launch or message tasks by itself.
4. **Compare consequential differences.** Show a short table: issue, Claude's recommendation, Codex's recommendation, evidence, and proposed resolution. Check dates, units, population, paid versus organic effects where relevant, attribution, arithmetic and current resource limits. Quantify the extra work as well as the expected benefit. Separate facts, assumptions and forecasts.
5. **Revise openly.** Each reviewer identifies ideas worth adopting, corrections to its own proposal, ideas it still rejects and why. Do not split the difference mechanically or force agreement. When uncertainty matters, propose a bounded test with a decision date, success measure and fallback. Prefer total business outcomes over an attractive intermediate metric.
6. **Merge once.** One named planner writes a self-contained final plan incorporating Dan's decisions. Record what changed and why, unresolved choices that actually block execution, dependencies, deadlines, fallback inventory and measurable review points. Preserve analytical drafts as evidence and mark their implementation handoffs superseded. Maintain one current execution handoff.
7. **Assign one implementation owner.** Use a capable, lower-cost model for well-specified operational execution when appropriate; resolve current model availability and effort when making the actual recommendation. Honor Dan's chosen owner and existing approvals. Do not reopen settled decisions, start a competing implementation or change another owner's work. Execute only the approved scope, verify results, and feed the measured outcomes into the next decision.

## Reusable briefs

### Independent proposal

> Help me decide [decision]. My objectives, in order, are [objectives]. Constraints and existing approvals are [constraints]. Review [primary evidence and date], research what is needed, and give an independent recommendation before reading the other AI's conclusions. Explain assumptions, costs, workload, alternatives, risks to the objective, and how we would measure success. This task is [planning only / authorized implementation scope].

### Comparison and revision

> Compare your recommendation with [other AI's proposal]. Show the important differences and check the underlying evidence and arithmetic. Identify what you would adopt, where you would change your own mind, and what you still disagree with. Quantify additional workload and cost. Recommend a combined approach or a bounded test where the evidence cannot settle the issue. Do not change the live system during this review.

### Final merge and handoff

> Merge [proposals and comparison] into one final plan reflecting these decisions from me: [decisions]. Use the strongest supported ideas, preserve unresolved differences only when they matter, and specify scope, sequence, dependencies, deadlines, measures and fallbacks. Mark competing implementation handoffs superseded and name one execution owner. Include a ready-to-paste starter prompt and a currently verified model and effort recommendation in the delivery. Implementation is [authorized scope / not yet authorized].

## Final plan outline

- Decision and expected business benefit.
- Approved scope, exclusions and implementation owner.
- Evidence and remaining assumptions, with dates and sources.
- Chosen approach and the material changes made after comparison.
- Concrete actions, timing, resource needs and dependencies.
- Success measures, review dates, expansion/stop conditions and fallback.
- Current handoff, starter prompt and model/effort recommendation.

## Reference case

The October 2026 content-release decision combined Claude's detailed film sequence and deadlines with Codex's organic-versus-paid analysis, workload calculations and sustainable cadence. Both proposals were challenged and revised; Dan made the final choices, and Claude merged them.

- Research and original Codex proposal: [content strategy evidence](CONTENT_STRATEGY_RECOMMENDATION_20261028.md).
- Final approved plan: [merged content schedule](../Handoffs/handoff-20261028-content-schedule-overhaul.md).
- Dan reported on October 28 that **Claude is implementing the final plan**. This records ownership, not verified completion.

Second case (2026-10-29): the Upwork client plan. Claude and Codex wrote independent plans. Claude checked the live account and verified Codex's corrections on primary sources, then merged them. The merge kept Codex's scoped trials, budget tranches and measures, and Claude's live-profile findings, outreach engine and research. It also added ideas neither plan had. Dan judged the merged plan slightly better than Codex's, with both contributing. Final plan: [merged Upwork plan](UPWORK_CLIENT_PLAN_MERGED_20261029.md), comparison table in section 4.

The lesson to reuse is the decision process. Content counts, budgets, dates and model names from this case are not defaults for future decisions.
