---
name: priority-edit
description: Prioritize an Abs By AI video edit on the two Macs when Dan marks it urgent, asks for the next editing slot, or requests dedicated M6 editing time through a milestone.
---

Resolve the video from the current edit, title or job ID. Keep its original chat, AI, Mac, folder, approvals and outputs. Read `.claude/skills/_shared/VIDEO-RULES.md` and `editroute/README.md`. Continue the normal editing skill and checks. Priority never approves media, authorizes spending or resumes the overnight dispatcher.

First run `python3 .claude/skills/_shared/editroute/resume.py check JOB`. For a remote owner, execute the controls there through `resume.py run JOB -- COMMAND`, keeping this chat as editor. An unresolved owner means wait and recheck, never a local duplicate.

**Ordinary priority.** For a genuinely new job, use `editroute.py pick JOB --kind KIND --priority --need-gb GB`, quoting real additional peak footage, scratch, output and check space. Preserve named-host decisions. On the owning Mac:

```bash
python3 .claude/skills/_shared/editroute/priority.py set JOB
python3 .claude/skills/_shared/editcap/editcap.py acquire JOB --priority --title "Video title" --type SFC
```

Use the video's actual type. Exit 3 means waiting, not production permission. Priority carries through the combined host line, whole-edit admission and eligible render tickets. After two compatible openings bypassed, a ready normal project receives its owed turn. Running steps are never displaced; other jobs use free capacity. Continue normal `renderq.py run --group JOB -- COMMAND` in its proper heavy/light/quick class. Ordinary urgency has a two-hour lease; repeat `set` during a longer active edit when needed.

**Dedicated M6.** An explicit request to give one edit the M6 through a milestone creates this temporary reservation. Default milestone: `checked-preview`. If the film already lives on M2, inspect its stage and moving cost and get an explicit move instruction before migration. A new dedicated request already names M6; preserve it, applying the established recommendation rule when another host has a clear advantage.

On M6 after ownership checks:

```bash
python3 .claude/skills/_shared/editroute/priority.py reserve JOB --milestone checked-preview --minutes 120
python3 .claude/skills/_shared/editcap/editcap.py acquire JOB --priority --title "Video title" --type SFC
python3 .claude/skills/_shared/editroute/priority.py status
python3 .claude/skills/_shared/renderq/renderq.py status
```

The reservation holds other new M6 grants. Running steps finish normally. Editcap parks an affected edit only after its last running holder exits, preserving its owner, checkpoints and original waiting place. A parked edit yields capacity for a third job. M2 continues independently. M6 keeps six cores while Dan is present and ten after 30 minutes idle, including at night. Renew with `priority.py renew JOB --minutes 120`. Optional `--owner-pid PID` on `reserve` must identify the actual long-lived M6 owner process: PID/start identity detects a crash. Otherwise expiry bounds a crashed reservation.

When the actual milestone passes its normal checks, automatically run `priority.py milestone JOB checked-preview`. A rendered preview is not checked until its gates pass. `editcap.py release JOB --review` also clears the reservation when waiting for Dan. Cancel with `priority.py release JOB --reason "cancelled"`. Expiry or a recorded owner crash releases it as the queues poll. Verify that parked edits restore their original place, reacquire capacity and continue with their original chats and existing waiter/wake mechanisms. Never kill/suspend processes, pause the global queue or change slot limits to simulate dedication.

**Rollout boundary.** `set`/`reserve` returns exit 3 before safe activation. Report that wait accurately. Infrastructure uses `priority.py activate` only after old holders/waiters drain naturally; it refuses old or unknown records. `priority.py deactivate` is the scoped off switch. Do not force activation for a live film.

**Authorized client verification.** When Dan explicitly asks to test this skill, run `python3 .claude/skills/_shared/editroute/client_acceptance.py --client codex --physical-host m6`, substituting `claude` and the actual physical host as appropriate. It invokes real commands against five private state directories and fixture ownership, with two occupied slots and a third reservation job. It checks ordinary priority, a running checkpoint, parking, milestone/cancellation/expiry/crash release, owner restoration and independent M2 policy. Read the receipt. Distinguish simulated host policy from physical-host evidence. It creates no production edit. Never use fixture overrides for a real film.

Report the title/job, actual owner Mac, effective priority, running/waiting state and release milestone. Installation and fixture success do not prove a real film is checked, delivered, approved or published.
