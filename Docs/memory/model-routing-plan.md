---
name: model-routing-plan
description: "Newest available GPT by default (Dan, 2026-10-20); older GPT needs a strong task-specific reason. Preserve Claude routing and the effort-level table. Use for every model recommendation and handoff."
metadata:
  node_type: memory
  type: feedback
  originSessionId: e872385e-a790-4974-8aca-fbd16df0d64a
  modified: 2026-10-20
---

**Green-screen executor update (Dan, 2026-10-25):** Codex now owns green-screen editing, including reactions, after Dan selected Bill Maher Fat 90-Year-Old Codex R5. This overrides older Opus/Claude routine-first-cut routing below for green-screen work. Use the newest supported stable Sol at high effort under the video rule; verify availability when recommending a specific model. Reaction format: [[greenscreen-reaction-format]]. Other categories and setup retain their routing. Do not start or transfer a live job merely to save this decision.


## Current GPT rule, October 20, 2026

Dan: "Let's change these recommendations to always use the newest GPT model unless there is some very strong reason not to".

Default to the newest GPT model available to Dan for every GPT recommendation, handoff and newly requested GPT task. Verify official guidance and actual client availability at recommendation time. Current default: GPT-6.1 Sol, verified October 20, 2026. Select effort using the task table below; the Arms & Shoulders full-film assembly uses high effort.

An older GPT model needs strong current evidence of a task-specific advantage or required capability, or a confirmed regression in the newest model. Explain the reason directly. An old skill, saved model number, established recipe, habit or untested claim is not sufficient. This rule supersedes all older GPT version pins and automatic Astra/Sol/Luna category assignments below or in other project guidance. Claude routing remains as recorded.

Official source checked: https://developers.openai.com/codex/models . Recheck when recommending; this dated example does not pin future tasks to GPT-6.1.


Dan revised this routing on 2026-10-02 (it replaces the 09-30 plan, which kept Fable for ship-critical copy and design locks). Basis: [[opus-5-5-release]], Opus ahead of Fable on every published benchmark, no measured category where Fable wins, and Fable costs 2.5x more per token. The GPT names and category assignments in this older routing are historical; the October 20 newest-GPT rule above controls current recommendations. Fable shares the weekly allowance, capped at half.

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

**Codex work:** use the newest available GPT by default for video work, image/thumbnail work, GUI tasks, ops and reviews. A recommendation for an older Astra, Sol or Luna must satisfy the strong-reason rule above. Preserve the existing Claude/Codex executor assignments; they do not pin a GPT version.

**Effort:** choose the effort for the task from the table above. Full-film assembly and verification use high effort; simple filing or routine checks can use less. Do not select an older GPT merely because a task is routine.

**Open tests, not opinions:** (1) thumbnails: Opus and Astra each build three from one locked spec, Dan picks blind; a tie or Opus win moves thumbnails to Opus. (2) Treat the first few Opus RO/DS cuts as the test against comparable Codex cuts; revert the queue routing only if Opus is clearly worse.

**Why:** Opus 5.5 matches or beats Fable at less allowance burn and writes less formulaically; Dan's experience is Codex still wins image/thumbnail generation, possibly because of process.

**How to apply:** recommend model + effort from this list and the effort table in every handoff ([[handoff-starter-prompt-rule]]) and whenever Dan asks "what model/effort should I use for X". Give one pick (model, effort) with a one-line reason tied to the table; do not offer a menu. Scheduled tasks cannot set their own model (the app has no per-task field and a session cannot switch itself), so a recurring job meant for Sonnet delegates to a Sonnet subagent from its SKILL.md (done for `social-queue-daily-refresh` 2026-10-08). Do not recommend Fable for a whole category. Related: [[video-editing-executor-routing]], [[reviews-on-opus-5-5]], [[three-role-video-pipeline]], [[organic-setup-codex-thumbnail-split]].

**Update 2026-10-20 (video edits, from the skills audit):** `AGENTS.md` and VIDEO-RULES ("Video rounds start automatically", 2026-10-20) say every video edit and new round defaults to the newest stable Sol at high effort, and that this video rule takes precedence over older routing. Read literally it overrides the Opus-for-routine-first-cuts line above and the queue routing (RO/DS to claude). Open question for Dan, logged in `Docs/DAN_DECISIONS.md`: does the Sol default cover Claude-run edits too, or only Codex rounds? Until he answers, a session in progress keeps its model and a new video round follows the 10-20 rule. The Claude editorial defaults for writing, reviews, revision docs and design are unchanged.

**Dan answered, 2026-10-20 evening:** a video stays with the AI it started on. Claude-started video: Opus 5.5 high every round. Codex-started video: newest stable Sol high (`gpt-6.1-sol`). Only his explicit request moves a video to the other AI ("My limit was almost burned up"). Rule text: `AGENTS.md`, "Video rounds", and VIDEO-RULES "Video rounds start automatically". The queue routing (RO/DS to claude, RA to codex) stands for NEW jobs; it decides where a video starts.
