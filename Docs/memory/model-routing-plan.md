---
name: model-routing-plan
description: "Dan's 2026-10-02 model routing (Opus default incl. first cuts and ship copy; Fable escalation only) plus the 2026-10-08 effort-level table; use it for every model + effort recommendation, in handoffs and when Dan asks"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e872385e-a790-4974-8aca-fbd16df0d64a
  modified: 2026-10-08T18:42:05.094Z
---

Dan revised this routing on 2026-10-02 (it replaces the 09-30 plan, which kept Fable for ship-critical copy and design locks). Basis: [[opus-5-5-release]], Opus ahead of Fable on every published benchmark, no measured category where Fable wins, and Fable costs 2.5x more per token. "Sol" is GPT-6 Sol (Codex default); "Astra" is GPT-6 Astra (Codex top). Fable shares the weekly allowance, capped at half.

**Opus 5.5 (the Claude default, high effort, never max):**
- All writing, including ship-critical copy: VSL scripts, /start page copy, ad scripts, outlines, shorts scripts, descriptions, editor messages, revision docs, handoffs.
- Design, including design-system locks (thumbnail style, graphics standards, HyperFrames decisions) and page/graphics work.
- Video edit plans, secondary cuts (AV/AS/SL), blind reviews (ra-reviewer), ra-editor builds, and ROUTINE FIRST CUTS: RO long-forms and DS shorts (queue routing flipped to claude 10-02 for new jobs).
- Photo retouching and picks; strategy and research memos.

**Fable 5.1 (escalation only, high effort):**
- An edit or review Opus has failed twice in a row; a disputed review where Dan wants a second model.
- Optional one-off second opinion on copy where a rewrite costs a filming day (VSL, /start, ad scripts before filming). Never a category default.

**Sonnet 5 (cheap runners, medium):** mechanical checklist work (uploads/platform setup after thumbnails, dashboard check-offs, filing, board cleanup, em-dash and format checks, recurring scheduled jobs such as the daily Social Queue refresh). Never editorial judgment, reviews, or anything a customer reads (ad headlines and copy are Opus high).

**Effort levels (Dan, 2026-10-08, from an audit of his last ~45 sessions).** Effort = how much the model thinks and verifies; it costs allowance and time, so spend it only where judgment or a costly miss is in play. Levels: low, medium, high, xhigh ("extra"), max.

| Level | Use it for | Examples here |
|---|---|---|
| Low | Status questions, lookups, no judgment | "is X ready in the edit queue", which file holds Y, renaming a session |
| Medium | Clear steps, answer mostly in the files; all Sonnet runner work | Social Queue refresh, upload/setup checklists, filing, handoffs written from clear notes, ranking priorities from the board, disk-cleanup recommendations |
| High (default) | Real judgment, a miss means a redo, someone watches/reads/pays for it | Edit builds and revisions rounds, reviewing an editor's cut and writing revision docs, scripts and ad copy, thumbnail/graphics design, code fixes, risky repo or file moves (git unjam, moving the project out of iCloud) |
| Extra (xhigh) | Open-ended and high-stakes, or High already missed once | Cart/page mockups Dan picks between, multi-file payment-flow builds, ship-critical copy before a filming day |
| Max | Almost never; diminishing returns and overthinking | A bug High and Extra both failed on; security audit of the Stripe webhook |

Rules of thumb: High when the output will be watched, read or paid for; Medium for filing, uploading, recurring jobs; Low for questions. Move to Extra only after High has failed once. A later revision round of something already rejected stays High (do not drop effort on round 3). Reviews of editor deliveries are Opus high, never medium. Anything destructive or hard to undo is High at minimum.

Audit findings that set these rules: Sonnet setup tasks had been run at High (7 sessions; should be Medium); Muhammad/Zeeshan revisions, Git Unjam and the iCloud move had been run at Medium (should be High); the Social Queue daily refresh ran on Opus medium (now Sonnet medium); Engagement ad headlines ran on Sonnet medium (customer-read copy, so Opus high).

**Astra (Codex top, high):** flagship first cuts (VSL, website video) until Opus has a track record on them; image and thumbnail generation; anything that must drive a GUI app (Final Cut, Affinity, Ads UI clicks). RA raw-ad first cuts stay codex in the queue for now.

**Sol (Codex default):** cheap fallback for routine first cuts; all ops and routines ([[codex-owns-non-core-work]]); Codex-side cross-reviews of Claude edits (`scripts/edit-queue/config.json`).

**Open tests, not opinions:** (1) thumbnails: Opus and Astra each build three from one locked spec, Dan picks blind; a tie or Opus win moves thumbnails to Opus. (2) Treat the first few Opus RO/DS cuts as the test against comparable Codex cuts; revert the queue routing only if Opus is clearly worse.

**Why:** Opus 5.5 matches or beats Fable at less allowance burn and writes less formulaically; Dan's experience is Codex still wins image/thumbnail generation, possibly because of process.

**How to apply:** recommend model + effort from this list and the effort table in every handoff ([[handoff-starter-prompt-rule]]) and whenever Dan asks "what model/effort should I use for X". Give one pick (model, effort) with a one-line reason tied to the table; do not offer a menu. Scheduled tasks cannot set their own model (the app has no per-task field and a session cannot switch itself), so a recurring job meant for Sonnet delegates to a Sonnet subagent from its SKILL.md (done for `social-queue-daily-refresh` 2026-10-08). Do not recommend Fable for a whole category. Related: [[video-editing-executor-routing]], [[reviews-on-opus-5-5]], [[three-role-video-pipeline]], [[organic-setup-codex-thumbnail-split]].
