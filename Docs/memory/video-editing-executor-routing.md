---
name: video-editing-executor-routing
description: Dan's 2026-09-17 split of video editing between Codex and Claude — Codex cuts raw footage, Claude does secondary cuts
metadata:
  type: project
---

Dan's assignment (2026-09-17): **Codex edits every first cut from raw footage** — raw ads (RA), organic long-forms (RO) and dedicated shorts (DS; Claude does nothing on those). **Claude does every secondary cut of a finished video** — ad vertical, vertical ≤0:59, square (AV/AS) and shorts cut from a finished long-form (SL).

**Why:** from the Codex trial Dan is "pretty sure" Codex is better at raw → finished video; on cut-downs the two are close and "not conclusive", so he gave those to Claude. Refines [[video-editing-cost-quality-feedback]] and [[codex-owns-non-core-work]].

**How to apply:** route new jobs from [[video-editing-master-list]] this way; leave in-flight jobs with their owner. It is a decision, not an A/B test — keep recording results, but re-routing is Dan's call. The overnight queue design (dispatcher, AI-clip placeholder flow where Dan approves the draft and the start/end frames together) is in `Handoffs/handoff-20260917-overnight-edit-queue.md`.

**Models (Dan, 2026-09-17):** queue EDITS run Claude **Opus / high** and Codex **Sol / high**. Reviews have their own settings in `scripts/edit-queue/config.json` (`review_model` / `review_effort`): Claude reviewer Opus 5.5 / high since 09-24 (was Fable), Codex reviewer Sol / medium. Don't lower the edit settings without Dan. Full routing across all five models: [[model-routing-plan]] (09-30).

**Update 2026-10-02:** Dan made Opus 5.5 the default for routine first cuts, so the queue now routes RO and DS to claude for NEW jobs (in-flight stay with their owner; Sol is the fallback). RA raw ads stay codex and flagship cuts (VSL, website video) stay Astra until Opus has a track record. Supersedes the "Codex edits every first cut" line above. See [[model-routing-plan]].
