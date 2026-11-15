---
name: eta
description: Quick ETA for a running task. Use when Dan types /eta, or asks "how long", "when will this be done", "ETA?" about this chat's task, a render or build in progress, or another session (/eta <session or video name>). Answers from measured progress, in two or three plain sentences, and never starts or changes any work.
---

# /eta: how long until this task is done

Dan wants one fast answer: when will it finish. **Read-only.** Do not start, stop, re-prioritize or "help along" any work while answering. No wrap-up boxes: this is a quick question-and-answer reply.

## Which task

- `/eta` alone: the task in THIS chat (what you were last doing, any background commands, renders, uploads or sub-agents you started).
- `/eta <name>`: another task. Match the name against sessions (`mcp__ccd_session_mgmt__list_sessions`, then `get_session` and `list_events` for its latest state) and against video jobs (`python3 .claude/skills/_shared/renderq/renderq.py status`, `python3 .claude/skills/_shared/editcap/editcap.py status`). A job on the other Mac: `python3 .claude/skills/_shared/editroute/resume.py check <JOB>`, then run the status commands there with `resume.py run <JOB> -- <command>`.

## Get the number from evidence, not a guess

Check in this order and use the first that gives a real rate:

1. **Running command with progress output:** read its output file or log (ffmpeg `time=` / `speed=`, Whisper, upload percent, test count). ETA = remaining work / measured speed. Take two readings a few seconds apart if the log shows only a position.
2. **Render queue:** `renderq.py status` shows slots, waiters and the job's step. If the job is waiting, the ETA is queue wait plus its own run time; say which part is which. If edit slots are full (`editcap.py status`), say it is waiting for a slot and who holds them.
3. **Your own task list** (`update_plan` steps): steps left times how long finished steps actually took this session. Only if nothing in 1 or 2 applies.
4. **Waiting on Dan** (a review, a pick, an approval): the ETA is "blocked on you", say exactly what he must do and give the link.
5. **No measurable basis:** say so, give a rough range labeled as a guess, and name what would make it measurable.

Never invent precision. Round to the nearest minute under an hour, to 5 minutes above that. Use clock times in Central (America/Chicago) next to the duration, e.g. "about 12 minutes, around 3:40 PM."

## Answer format

Two or three short sentences, plain words, no file paths or jargon:

> **ETA: about 12 minutes (around 3:40 PM Central).** Right now it is rendering the final video, 60% done and moving at about 5 minutes per 10%. Then it runs the last quality check, roughly 3 more minutes.

Include, only when true: what it is doing now, how far along, the biggest risk to the estimate (queue wait, a retry, a check that might fail), and whether it is waiting on Dan. Name any video by its title (code after, never alone). If several tasks are running, one line each, soonest first.
