# HANDOFF — Membership copy tasks

**Run with: Claude Haiku 4.5, LOW reasoning effort.** Pure writing tasks with exact target locations; no architecture decisions. Do not refactor any code.

## Context

Abs by AI (this repo) sells a membership: monthly $9.99 / annual $59.99. It unlocks: full 4-week AI training program + every later block, unlimited future-self image generations, unlimited AI meal & macro tracking, AI Nutritionist meal-prep plans, AI Sleep Coach full briefings, Decision Counsel (10 sessions/month), Progress Log AI weekly recap. 7-day money-back guarantee via email. Brand voice: direct, energetic, "go hard" coach — confident, never sleazy; short sentences.

## Task 1 — Member welcome email

Append to `EMAIL_MARKETING_PLAN.md` as a new section "## 8. Member welcome email (transactional, ready to paste)". Subject + preview text + body in the same blockquote format as the existing emails in that file. Content: thank them, list what just unlocked (the list above), tell them the two best first moves (generate their program; set up the Progress Log photo day), mention the 7-day guarantee, sign "— Dan".

## Task 2 — Hub member badge + FAQ copy

In `index.html`:
- Find the member hub (`#hubSection`). Add a small static block of copy (HTML comment `<!-- MEMBER-COPY -->` placed near `hubEmail`) — do NOT wire any JS: a one-line "Member" badge string and a 3-item FAQ (billing date, how to cancel — email support@absbyai.com or the Manage membership card, refund policy) inside a `<details>` element styled with existing classes (`hero-sub`, `lbl`). Keep it display:none with id `hubMemberFaq` so the Sonnet task can toggle it.

## Task 3 — Cancel/guarantee microcopy

In `index.html` `#membershipSection`, review the `guarantee-note` line and plan-card sublabels; tighten wording if flat, keeping length similar. No structural HTML changes.

## Done criteria

- `EMAIL_MARKETING_PLAN.md` gains section 8.
- `index.html` gains the hidden `hubMemberFaq` block; page still loads with zero console errors (`node --check` not needed for HTML; just don't touch scripts).
- Commit to main with a clear message and push (auto-deploy is fine; everything is hidden/static).
