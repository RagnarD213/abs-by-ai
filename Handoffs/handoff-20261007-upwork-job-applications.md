# Upwork job criteria, proposals and first applications

Created: 2026-10-07. Status: ready for interview; profile must be ready before submission.
Task name: Upwork Jobs and Proposals.
Recommended owner: Codex GPT-6.1 Sol, high effort, for qualification, tools and tracking. Claude Opus 5.5, high effort, is recommended for final proposal copy and custom-video scripts. A single Claude task can own the workflow if preferred. Do not spawn or message another task unless Dan authorizes it.

## Goal and prior decisions

Interview Dan, establish job-selection and spending rules, decide whether to promote his profile, create strong proposals with selective custom videos/sample edits, and submit the approved initial applications. Build an economical repeatable acquisition process. Do not jump directly to bulk autonomous submissions.

Dan's business should eventually run with very little personal involvement. Initially he wants close involvement. Important client communication, scripts and actual editing stay with Codex and Claude. He specifically means the Grok Bot app powered by xAI when asking about inexpensive background work. Its exact account plan and available integrations have not been inspected.

Workspace: /Users/danielrose/Documents/Claude/Projects/Abs By AI
Read Handoffs/handoff-20261007-upwork-profile-and-portfolio.md and its completed working brief/results. Profile work can proceed alongside the criteria interview, but no proposal should depend on nonexistent examples or unapproved claims.

## Interview first, in short rounds

Ask 3-5 related questions at a time and record the resulting rules in Handoffs/upwork-acquisition-rules.md.

1. Services and clients: fitness-only or adjacent niches, agencies versus brands/coaches, desired deliverables, exclusions, hourly versus fixed-price, languages/time zones, meetings and availability.
2. Economics and capacity: minimum project price/net margin, desired monthly accounts, maximum source-footage length, deadlines, active-project cap, weekly time Dan can give, and how to reserve production capacity before promising a date.
3. Acquisition spending: total and weekly Connects budget, per-proposal cap, whether boosts or profile promotion are worth testing, and what subscriptions he already has. Prior plan proposed $150 initial Connects, not authorized spending.
4. Proposal videos: will Dan record personal 45-60 second introductions, how frequently, and can existing introduction footage be reused? Does he authorize 10-20 second sample edits when the client provides usable footage? Agree on sample time/cost limits and public/private delivery.
5. Authority: which initial batch must he approve, who sends messages, what can later be sent without review, and what still needs him. Obtain explicit sending and spend authorization before the first real batch, then preserve it rather than asking per item.
6. Background work: identify his Grok Bot plan/access, notification destination, permitted cadence, usage limits and quiet hours. He wants alerts for real client interest, offers, acceptance decisions and failures that need action, not every empty scan.

## Job selection and tracking

Use the official Upwork MCP/API where supported, approved notifications, and manual discovery as a fallback. Do not build scraping, auto-refresh browser loops or unsupported auto-submit tools.

Suggested score to tailor: offer/portfolio fit 30, clarity and usable assets 20, economics 20, client signals 15, recurring-work potential 15. Starting shortlist threshold 75/100. Missing data is unknown, not a made-up score. Record score reasons and evaluate new clients fairly even if they have little hiring history.

Reject jobs outside approved services, price floors, turnaround or capacity. Flag ambiguous scope, huge unpaid tests, extensive original animation and custom strategy work separately.

Track each job by its unique Upwork ID: URL, discovery time, last checked time, budget, scope, client signals, required Connects, score, chosen sample, proposed price, proposal version, approval, submission receipt, client response, interview, hire, revenue, costs and next action. Deduplicate before spending tokens or Connects. Keep closed or already-applied jobs out of the queue.

Initial target: 10-15 researched candidates and 3-5 excellent proposal packages for Dan's review, not a forced quota. Recheck job status, actual Connects, fees and available capacity immediately before submission.

## Profile promotion decision

Distinguish profile boosting, Availability Badge, proposal boosts and a membership upgrade. Inspect current account prices and functions. Recommend starting with a credible profile and unboosted targeted applications, then a bounded test if Dan wants one. No automatic activation.

Present the exact proposed spend cap, duration, targeting, baseline, success measure and stop rule. Judge by qualified interviews, hires and acquisition cost, not profile views alone. A small test may be inconclusive; do not claim causal lift from a handful of responses. Do not renew or increase spend beyond authorization.

## Proposals and custom video experiment

Use only approved profile facts. Proposals should be brief and specific: understanding of the job, one relevant example, concrete approach, deliverable/price/timing, and one useful question. Answer required screening questions directly. Codex/Claude owns client-facing wording; Grok can extract facts and prepare an internal proposal brief.

Test three approaches where appropriate:
- Relevant portfolio example plus tailored text for normal good matches.
- A 45-60 second personal video for a strong fit, with Dan's specific observation and a clear next step.
- A 10-20 second edited sample of supplied footage for exceptional fits where it demonstrates the exact requested skill.

A reasonable initial sample cap to discuss is 30 minutes production effort and no paid generation, maximum two speculative samples per week. Do not make a whole unpaid deliverable. If source material is unavailable, use a clearly labeled relevant example or a concise edit plan rather than pretending to have the client's footage. Do not present synthetic speech as a newly recorded personal message.

Read .claude/skills/_shared/VIDEO-RULES.md and the relevant editing skill before editing. Categorize the sample AD/LFC/SFC first. Use the client's style/reference and preserve existing approved assets. Show Dan the actual moving sample and proposal before the initial submission batch. Test every attachment/link in its recipient-facing state. Use private proposal delivery or an approved share link; do not publish client samples organically.

Record sample time and cost. Compare qualified responses and hires for text, personal video and sample edits. This is an exploratory comparison, not a statistically established result. Stop costly samples if they are not producing enough additional value.

## Execute the approved batch

Show a compact packet: job, reason to bid, price, scope/deadline, Connects including boosts, proposal text, screening answers and video/sample. Obtain one batch approval if no prior sending authority covers it. Submit through the supported confirmation flow. Reopen submitted proposals and confirm receipts; do not assume a tool success message means the proposal is live. Never blindly retry an uncertain submission.

Draft client replies promptly with Codex/Claude. During initial supervision, Dan approves replies unless he has granted a clear exception. An interview or offer is not a won contract. Notify him of an offer with exact price, scope, deadline and the action needed to accept. Do not start paid production before the agreed contract/milestone is ready.

## Optional background pilot, only after criteria and account capabilities are established

Dan wants background discovery without manually firing tasks. Establish a concrete pilot and obtain approval of the exact cadence, budget and authority before activation. Do not create a monitor merely because this handoff exists.

Proposed division:
- Simple code: dates, minimum-budget checks, deduplication, state tracking and no-change detection.
- Grok Bot or a small API model: parse new job descriptions, flag missing inputs, score against Dan's rules, pick relevant approved portfolio IDs, and produce compact internal briefs.
- Codex/Claude: final proposals, conversations, scope negotiation, scripts, editing and final quality review.
- Dan: initial approvals, required platform confirmations, exceptional commercial/creative decisions.

Start with one worker, not a fleet. Prefer supported event notifications; otherwise test an approved connector search on an agreed cadence such as every 1-2 hours, respecting service limits. Run all day without continuously thinking. Only process new/changed jobs, cache stable criteria, cap candidates and calls, and avoid passing the whole project history to every run.

Verify Grok Bot can actually authenticate to and use the required Upwork tools; its generic browser capability is not proof of an approved Upwork integration. Upwork's published MCP flow requires confirmation for writes and on-site binding acceptance. Do not promise unattended submission or simulate human confirmation. If unsupported, automate scouting and drafting and present a compact approval queue.

For a 7-day draft-only test, measure useful shortlisted jobs, missed good jobs from an audited rejected sample, false matches, token/usage cost, duplicate rate and Dan's minutes. Configure bounded retries, one submission owner, a pause switch and failure alerts. Notify only for actionable client replies/offers, approval-ready exceptional opportunities, or failures requiring intervention. Stay quiet on unchanged/non-actionable checks. Verify at least one scheduled run and notification before declaring it working.

Grok Bot has a cloud computer and routines, but has usage limits. It is not unlimited free labor. An alternative is a small scheduled service plus a metered API model. An illustrative 1,000-job text screen at 2,000 input and 300 output tokens per job using published Grok 4.3 rates ($1.25/$2.50 per million) is $3.25 in base tokens. This excludes tool calls, retries, hosting, additional reasoning and proposal writing, and is NOT Grok Bot subscription pricing. Recheck rates at implementation. Propose a separate hard acquisition-AI budget; do not assume general generation allowances authorize subscriptions or Connects.

## Completion and continuing ownership

Deliver saved selection rules, promotion decision, initial submission receipts, sample links, spend ledger, response workflow, and any approved pilot's next run/owner. If the monitor is not activated, say so and list the specific remaining decision. Keep important creative work in Codex/Claude. Never leave two agents independently submitting for one account.

No Victory Dashboard access. No new app deployment is needed for this workflow. Follow task-file commit rules; no em/en dashes in new writing.

## Sources checked 2026-10-07; recheck before setup

- https://www.upwork.com/ai/mcp
- https://support.upwork.com/hc/en-us/articles/55446516654611-How-to-use-Upwork-with-AI-agents-through-MCP
- https://support.upwork.com/hc/en-us/articles/43342677368467-Use-bots-and-other-automation-properly
- https://docs.x.ai/grok-bot/overview
- https://docs.x.ai/grok-bot/skills-routines-and-automations
- https://docs.x.ai/developers/pricing

## Starter prompt

Name this task Upwork Jobs and Proposals. Read Handoffs/handoff-20261007-upwork-job-applications.md and execute it. Interview me first to establish job criteria, rates, capacity, Connects spending, promotion preferences and approval boundaries. Use my completed profile and portfolio. Prepare a first batch of excellent proposals and selectively recommend personal videos or short sample edits using available client footage. Get one batch approval before initial submissions unless I already authorized them. Assess Grok Bot for economical background scouting and preparation, while keeping final proposals, client communication, scripts and editing with Codex and Claude. Do not activate recurring spending or unattended submissions without the agreed setup and supported platform permissions.
