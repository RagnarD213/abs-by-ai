---
name: model-routing-plan
description: "Dan's 2026-10-02 model routing (Opus default incl. first cuts and ship copy; Fable escalation only); use it for every handoff's model + effort recommendation"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e872385e-a790-4974-8aca-fbd16df0d64a
  modified: 2026-09-30T17:45:43.386Z
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

**Sonnet 5 (cheap runners, medium):** mechanical checklist work (uploads/platform setup after thumbnails, dashboard check-offs, filing, board cleanup, em-dash and format checks). Never editorial judgment, reviews, or anything a customer reads.

**Astra (Codex top, high):** flagship first cuts (VSL, website video) until Opus has a track record on them; image and thumbnail generation; anything that must drive a GUI app (Final Cut, Affinity, Ads UI clicks). RA raw-ad first cuts stay codex in the queue for now.

**Sol (Codex default):** cheap fallback for routine first cuts; all ops and routines ([[codex-owns-non-core-work]]); Codex-side cross-reviews of Claude edits (`scripts/edit-queue/config.json`).

**Open tests, not opinions:** (1) thumbnails: Opus and Astra each build three from one locked spec, Dan picks blind; a tie or Opus win moves thumbnails to Opus. (2) Treat the first few Opus RO/DS cuts as the test against comparable Codex cuts; revert the queue routing only if Opus is clearly worse.

**Why:** Opus 5.5 matches or beats Fable at less allowance burn and writes less formulaically; Dan's experience is Codex still wins image/thumbnail generation, possibly because of process.

**How to apply:** recommend model + effort from this list in every handoff ([[handoff-starter-prompt-rule]]). Do not recommend Fable for a whole category. Related: [[video-editing-executor-routing]], [[reviews-on-opus-5-5]], [[three-role-video-pipeline]], [[organic-setup-codex-thumbnail-split]].
