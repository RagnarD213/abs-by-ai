# 03: Two-Mac edit routing: M6 primary, M2 takes the overflow (Claude, on the M6)

Category: ops (video-pipeline build). Read `README.md` in this folder, then `.claude/skills/_shared/renderq/README.md`, `.claude/skills/_shared/editcap/editcap.py`, and the "render queue" and "Active edit cap" sections of `.claude/skills/_shared/VIDEO-RULES.md`. Requires handoff 02 verified (`ssh m2` works both ways, drives mounted on the M6).

Model: Claude Fable 5.2, high. Shared pipeline code used by Claude and Codex: test on both (memory `protect-codex-and-other-ais`).

## The rules Dan gets (build exactly this; numbers live in one config file so he can change them)

`.claude/skills/_shared/editroute/hosts.json`:

| | M6 (Dan's machine) | M2 (headless) |
|---|---|---|
| Edit slots | 2 | 3 |
| Cores edits may use while Dan is at the Mac | about half the M6's cores (measure, leave the rest for him) | 8 (as today) |
| Cores when Dan is away 30+ minutes, or 10 PM to 7 AM | all but 2 | 8 |

**Where the next edit goes** (`editroute.py pick <JOB> --kind ...` prints `m6` or `m2` and why):

1. An edit that already has a work folder goes back to the Mac that holds it. Never move a job mid-flight.
2. Dan says a machine by name: that machine.
3. Short, interactive work goes to the M6 first: Shorts (SFC, SFL), ad cutdowns, later-round revisions he is waiting on. The M6 is faster and he is reviewing those the same day.
4. Long unattended work goes to the M2 first: long-form first cuts (LFC R1), anything with a full chroma key, exercise-demo batches.
5. If the preferred Mac's slots are full, use the other. If the M6 is under real load from Dan's own work (memory pressure not normal, or load above its core count for 5 minutes), treat the M6 as full for new edits.
6. So from idle the usual order is: 1st edit M6, 2nd M2, 3rd M2, 4th M6 (only if rule 5 allows), 5th M2, then the line waits. Total stays 5.
7. When both are full the job waits for the first free slot on either Mac, oldest first.

## Build

1. **Per-machine queues stay per machine.** `renderq` already budgets cores per Mac; give it the per-host budget from `hosts.json` (hostname lookup, `m6`/`m2`), including the away/night budget on the M6 (idle time from `ioreg -c IOHIDSystem`, hour from the clock). `editcap` runs on each Mac with that host's slot count (`EDITCAP_MAX` from `hosts.json`). Move both state folders out of `/tmp` (lost on restart) to `~/.absbyai-renderq` style folders only if a test shows that is safe for running holders; otherwise leave them.
2. **`editroute.py`** (`pick`, `status`, `where <JOB>`): reads both Macs' `editcap.py status` and `renderq.py status` (local call plus `ssh` to the other, 3 s timeout; an unreachable Mac counts as full and is reported), applies the rules above, records the decision in `~/.absbyai-editroute/decisions.jsonl`. `status` prints one plain table for both Macs. Add a combined waiting line so a job waiting on one Mac starts on whichever frees first, only if it has not started work.
3. **How an edit starts on the M2.** Claude: the desktop app's SSH connection (`start_session` with `target: "ssh"`, host `m2`; check `list_start_targets`, and have Dan add the SSH connection in the app once if it is not listed). The session then appears in Dan's M6 sidebar but works on the M2. Codex: verify what works today before choosing, in this order: the Codex app's own remote option, `ssh m2 codex exec` from an M6 Codex task, then Screen Sharing to the M2 as the fallback. Record what was verified, not what should work.
4. **Shared project folder on the M2.** Share `~/Projects/Claude` from the M6 (Dan turns on File Sharing on the M6 and adds the folder; one Finder connect on the M2 through Screen Sharing with "Remember this password"; login item). On the M2: rename the local `~/Projects/Claude` to `~/Projects/Claude.m2-local-20261112` (do not delete; edits in progress may hold paths in it, so do this only when `editcap.py status` on the M2 shows nothing active, or leave running jobs to finish first) and link `~/Projects/Claude` to the mounted share. **Benchmark** `git status`, a skills grep and `safe-push.sh --dry-run` over the share. If `git status` takes over 10 s or locks misbehave, use the fallback: the M2 keeps its own git clone, pulls before each job and pushes with plain git from a clean checkout (as Codex worktrees do), and mounts the M6 folder read-only at `/Volumes/Claude` for untracked media.
5. **Work folders.** `renderq.py workdir` on each Mac keeps Dan's order (internal, Extreme, Seagate), where "internal" is that Mac's own SSD. On the M6 the Extreme and Seagate are network mounts: weight them below the M6's internal drive and never run a heavy encode against the Seagate share. Finished jobs still move to the Seagate checksummed, done by the M2 (the drive is attached there).
6. **Review pages.** Pages for M2 jobs are served on the M2 and must open from the M6: bind `review_server.py` to the link address as well as localhost when on the M2, make every review link an edit prints use `http://m2.local:PORT` (or `10.66.0.2`), and have the review hub on the M6 list both Macs. The silent-check and owner-handoff audio rules are unchanged.
7. **Skills and rules.** Add one short section "Two Macs" to `VIDEO-RULES.md` and one paragraph to `AGENTS.md` (which Mac, `editroute.py pick` before `editcap.py acquire`, review links). Update `/longform-edit`, `/shorts`, `/ad-edit` and the video-rounds controller only where they start a job. Memory entry `two-mac-edit-routing`; run `scripts/sync-memory-to-repo.sh`.
8. **Scheduled tasks switch** (the list from the 02 receipt), once Dan confirms the M6 is his daily machine: enable on M6, disable on M2, confirm nothing is enabled on both.
9. **Tests.** Unit tests for every routing rule and for an unreachable M2. One real proof: a short job of the right category (a queued SFC, never a made-up task) routed to the M2 end to end: started from the M6, rendered on the M2, review page opened on the M6, finals in the project folder. Report timings for the same render step on both Macs so the slot and core numbers can be tuned.

## Done looks like

`editroute.py status` shows both Macs; a new edit lands on the right Mac by itself and says why; M2 edits show up in Dan's M6 sidebar and their review pages open on the M6; the M6 stays responsive with two edits running while Dan works; nothing was deleted on either Mac. Receipt: `Docs/TWO_MAC_EDIT_ROUTING_RECEIPT_<date>.md`. Leftover for Dan's decision (put in `Docs/DAN_DECISIONS.md`): deleting the M2's old local copies to free about 240 GB.
