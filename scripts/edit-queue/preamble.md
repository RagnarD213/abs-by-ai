# UNATTENDED RUN: read this before the job

You are running unattended from the overnight edit queue; Dan is not available. Job: **{JOB}**.

* **Never ask a question.** Make the documented default choice and record it in `notes.md` in the work directory.
* **Never upload, publish, post, schedule, send a message or email, or touch Google Ads, YouTube or Blotato.**
  Where the job text says "send me the review copy" or "upload", do not: leave the files on disk.
  (The one exception is not a publish: `scripts/edit-queue/queue.py` syncs a small status file to Dan's private
  Drive every time it sets a state. That is how his queue page updates. Run `queue.py` normally; never suppress it.)
* **Never spend beyond this video's remaining $5 generation budget.** Do not generate AI motion clips: follow the
  placeholder flow in `Handoffs/handoff-20260917-overnight-edit-queue.md` §5.
* **Your work directory is `{WORKDIR}`.** Use it even if the job doc names another folder for this job. Never run a
  script inside another session's build directory; copy what you need.
* **One editor owns this candidate.** Do not spawn a planning or supervisory agent. Read `WORK_PACKET.json` first;
  its short `requested_changes` list is the complete change scope and its `approved_elements` list is protected.
  Escalate only a concrete unresolved decision; do not start a repeated review loop yourself.
* **Reuse is the default.** Fingerprint and reuse every unchanged scene, accepted audio stream/mix, transcript and
  asset. Do not rerun transcription, asset search, audio processing or unchanged scene rendering. Record each of
  those four categories in `DELIVERY.json` as `reused`, `rebuilt`, `mixed`, `not_applicable` or `unavailable`, with
  the hash/path evidence in `REUSE_REPORT.json`. A filename by itself is not reuse evidence.
* **Check expensive choices before the full render.** For risky source choices (old-channel proof, workout/demo
  footage, app sessions, generated motion, identity/label scenes), verify the source and make a 0.5–15 second moving
  preview first. Write `PRE_RENDER_CHECK.json` with source/preview paths, SHA-256 values, duration and verdict. If no
  risky selection exists, record `status: "not_applicable"` and a specific reason. Before launching the full render,
  run `python3 scripts/edit-queue/pre_render_check.py "{WORKDIR}"`; do not proceed unless it prints `"status": "PASS"`.
  The queue rechecks the same evidence before it spends the independent review session.
* **Machine cap.** This run holds one of the machine's two build slots. Do not start a second parallel build of
  your own, and if `ps` shows two other builds already running, wait rather than add a third.
* **Do not add an `AI_COORDINATION.md` entry and do not set the job's state when you finish.** The queue page is
  the record for queue-run jobs, and the queue sets `delivered` only after the independent cross-review. The job
  is already marked `in_progress`; skip the "claim it" step in `00-RULES.md` §1.2.
* Everything else in `AGENTS.md`, `Handoffs/video-editing/00-RULES.md` and the job doc applies in full: every gate
  on the delivered file, the audio rules, the labels, a `REVIEW 540p` copy, `notes-*.md`, the recipe folder. Still run
  your own self-QA before you call it finished. The queue starts exactly one independent reviewer only after your
  complete candidate exists; do not wait for or poll that reviewer.
* Commit docs and scripts only, never media, and never another session's uncommitted files.

**When the edit is finished,** write `{WORKDIR}/DELIVERY.json`:

```json
{"files": ["<absolute path of every delivered video>"], "review_copy": "<absolute path of the REVIEW 540p copy>",
 "gate": "PASS | FAIL | DRAFT", "gate_failures": ["<row: reason>"], "revision_count": 0,
 "approved_elements": ["<short protected list for the next revision>"],
 "reuse": {"scenes": {"status": "reused", "evidence": "REUSE_REPORT.json"},
   "audio": {"status": "reused", "evidence": "REUSE_REPORT.json"},
   "transcript": {"status": "reused", "evidence": "REUSE_REPORT.json"},
   "assets": {"status": "reused", "evidence": "REUSE_REPORT.json"}},
 "generation_spend_usd": 0,
 "paid_provider_costs": [{"provider": "Replicate", "purpose": "motion", "usd": 0.25}],
 "summary": "<two plain sentences for Dan: what this is and what his call is>"}
```

A gate FAIL is reported honestly in that file, never tuned away. If a provider did not return a charge, set `usd`
to `null` and explain why; never turn an unavailable measurement into zero. The queue separately records the editor
and reviewer model settings, captures a per-session total when the command-line footer exposes one, and marks the
input/output/cache split unavailable when it is not exposed.

**If you hit a real blocker,** write `{WORKDIR}/BLOCKED.md` whose first line is the one-sentence reason and the rest
says exactly what is needed, run `python3 scripts/edit-queue/queue.py set {JOB} needs --by "edit queue" --note "<reason>"`,
and exit. Do not write DELIVERY.json in that case.
