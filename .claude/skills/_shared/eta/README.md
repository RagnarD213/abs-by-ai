# Edit ETA: what the Edit Queue page shows for each running edit (Dan, 2026-11-18)

Dan asked "ETA?" in chat many times a day. Now the Edit Queue page
(https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs) shows a **Running now** panel and an ETA line on each job row,
rechecked every 10 minutes by a plain script. No AI tokens, no messages, nothing at night but a quiet file update.

## Pieces

| piece | what it does |
|---|---|
| `eta.py plan/step/left/retry/done` | an editing session reports its plan and each step (rule: VIDEO-RULES.md, "Report the ETA as you go") |
| `~/.absbyai-eta/<JOB>.json` | the job's progress, on the Mac doing the work |
| `~/.absbyai-eta/history.jsonl` | real minutes per step, so estimates learn (step names drop numbers: "Key 14 pieces" = "Key 9 pieces") |
| `eta.py refresh` | M6 LaunchAgent `com.absbyai.edit-eta`, every 10 min: reads this Mac and the M2 (sends its own copy of eta.py over ssh, so versions never differ), plus editcap and the render queue on both, writes `tmp/edit-queue-export/edit-queue-eta.json` and uploads it to Drive only when something changed, or every 30 min |
| Drive `Abs By AI automation/edit-queue-eta.json` | file id `1qTfELTbTmh6jFctW0SlCeDBp-WeBvx5J`; the page reads it every 2 minutes |
| `install.sh` | installs the LaunchAgent (M6 only). Log: `~/Library/Logs/absbyai-edit-eta.log` |

## What a row says

- **ETA: 3:30 to 4:15 PM** with `estimate`, `measured` (session gave `left`), `running long` (step past its time) or
  `rough guess` (a step with no time and no history). Detail line: step N of M and its name; "redoing after a failed
  check" after `retry`; "waiting in the render line" when its steps are queued.
- **Waiting on you since Nov 15**: editcap says the edit is with Dan (release --review).
- **Waiting for an edit slot (#2 in line)**: editcap waiting.
- **May be stuck: no activity for 52 min**: no editcap heartbeat, no progress update and nothing rendering for 45
  min. A stalled edit stops showing a countdown.
- **Running, no ETA reported yet**: the edit holds a slot but never ran `eta.py plan` (sessions started before
  2026-11-18 or skipping the rule).

## Estimate method

Current step: the session's `left` if given (tight range), else expected minus elapsed, else (overrun) 35% of the
elapsed time so the range keeps growing honestly. Future steps: history median blended 50/50 with the plan's
minutes once a step name has 2+ real runs, else the plan's minutes, else 20 min marked unknown. Range: low 0.7x (0.85x
when measured and nearly done), high 1.25x plus extra for the share still in future steps, unknown steps and retries.
Times are rounded to 5 minutes. Tests: `python3 .claude/skills/_shared/eta/test_eta.py`.
