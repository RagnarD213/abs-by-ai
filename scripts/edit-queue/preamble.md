# UNATTENDED RUN: read this before the job

You are running unattended from the overnight edit queue; Dan is not available. Job: **{JOB}**.

* **Never ask a question.** Make the documented default choice and record it in `notes.md` in the work directory.
* **Never upload, publish, post, schedule, send a message or email, or touch Google Ads, YouTube or Blotato.**
  Where the job text says "send me the review copy" or "upload", do not: leave the files on disk.
* **Never spend beyond this video's remaining $5 generation budget.** Do not generate AI motion clips: follow the
  placeholder flow in `Handoffs/handoff-20260917-overnight-edit-queue.md` §5.
* **Your work directory is `{WORKDIR}`.** Use it even if the job doc names another folder for this job. Never run a
  script inside another session's build directory; copy what you need.
* **Machine cap.** This run holds one of the machine's two build slots. Do not start a second parallel build of
  your own, and if `ps` shows two other builds already running, wait rather than add a third.
* **Do not add an `AI_COORDINATION.md` entry and do not set the job's state when you finish.** The queue page is
  the record for queue-run jobs, and the queue sets `delivered` only after the independent cross-review. The job
  is already marked `in_progress`; skip the "claim it" step in `00-RULES.md` §1.2.
* Everything else in `AGENTS.md`, `Handoffs/video-editing/00-RULES.md` and the job doc applies in full: every gate
  on the delivered file, the audio rules, the labels, a `REVIEW 540p` copy, `notes-*.md`, the recipe folder. Still run
  your own independent audit before you call it finished.
* Commit docs and scripts only, never media, and never another session's uncommitted files.

**When the edit is finished,** write `{WORKDIR}/DELIVERY.json`:

```json
{"files": ["<absolute path of every delivered video>"], "review_copy": "<absolute path of the REVIEW 540p copy>",
 "gate": "PASS | FAIL | DRAFT", "gate_failures": ["<row: reason>"], "generation_spend_usd": 0,
 "summary": "<two plain sentences for Dan: what this is and what his call is>"}
```

A gate FAIL is reported honestly in that file, never tuned away.

**If you hit a real blocker,** write `{WORKDIR}/BLOCKED.md` whose first line is the one-sentence reason and the rest
says exactly what is needed, run `python3 scripts/edit-queue/queue.py set {JOB} needs --by "edit queue" --note "<reason>"`,
and exit. Do not write DELIVERY.json in that case.
