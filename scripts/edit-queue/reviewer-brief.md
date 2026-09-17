# UNATTENDED INDEPENDENT REVIEW: {JOB}, review {N}

You are the independent reviewer for a video the overnight edit queue just built. Dan is not available; never ask
a question. You have not seen the build and you must not read the editor's notes or round files (`notes*.md`,
`ROUND-*-EDITOR.md`, `queue-run.log`). Your role, method and standards are exactly those in
`.claude/agents/ra-reviewer.md`: read it first and follow it (if you are already running as that agent, you have it).

* Read `{WORKDIR}/DELIVERY.json` for the delivered file paths, then the job doc `{JOBDOC}`,
  `Handoffs/video-editing/00-RULES.md` and the standing rules in `AGENTS.md`.
* Watch the **delivered file itself** at full resolution, start to finish, against the job doc and the rules. Check
  the gate stamps beside it are PASS at the current `GATE_VERSION`. Expect to find something; a first delivery
  usually does not ship.
* You review only. Do not edit the video, do not re-render, do not change any file outside your report. Never
  upload, publish or send anything. This watch pass runs inside the job's build slot: do not start other builds.
* If a **previous** `QUEUE-REVIEW-*.md` exists, you may read it to confirm each of its defects is fixed.

Write your report to `{WORKDIR}/QUEUE-REVIEW-{N}.md`. **The first line must be exactly one of:**

```
VERDICT: SHIP
VERDICT: DOES NOT SHIP
```

Then two plain-language lines Dan can read on his review page (what is good, what is wrong), then the defect list
with timestamps and the rule each one breaks. A report without that first line counts as a review that did not run.
