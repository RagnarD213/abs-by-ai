# Handoff: move the daily editor deliveries scan to the OpenAI dot (Codex sets it up)

Written 2026-09-30 by Claude (Fable 5.1). **Executor: a Codex session (GPT-6 Sol, medium), then the dot runs it
daily at 5:40 AM Central.** Read `handoff-20260930-codex-dot-00-shared-setup.md` first. Supersedes the
editor-deliveries row of `handoff-20260918-move-routines-to-codex.md`.

## Goal

Every morning, find any FINAL high-quality video Muhammad, Zeeshan or Waleed delivered on Upwork or Drive,
file it in the project folder under the naming convention, and put anything ambiguous in front of Dan by name.
Nothing is ever missed silently. The Claude routine `editor-deliveries-daily` is then turned off.

## The rulebook (do not rewrite it, point at it)

`.claude/skills/editor-deliveries/SKILL.md` is the complete, measured rulebook and stays the single source of
truth. `state.json` beside it is the state (`filed`, `not_final_seen`, `pending`, `last_run`).
`folder_scan.py` beside it lists Zeeshan's shared folders without a browser. The Codex session reads all three
in full before doing anything. The rules that matter most, so the assignment text is right:

1. **File only when all three are true:** the editor's message calls it HD / final (or answers Dan's "send the
   high quality"); no revision doc or thread message dated after it; the file is 1080p-class, hundreds of MB.
2. **Dan's latest word in the thread beats a revision doc from earlier the same day** (09-13 lesson).
3. **An unread thread is an unfinished run.** That editor goes in `pending` with "thread unread". A negative
   search result is never evidence. Carry a positive control query. Write what you did, not what you concluded.
4. **Zeeshan shares folders, not files.** Drive search cannot see his drops until someone opens the folder.
   `folder_scan.py` (or the dot opening the folder in its own browser) is the only detector for him. He ships a
   `.srt` every time; file it beside the video.
5. **Never download to check.** Drive `fileSize` decides rule 3. Ambiguous means `pending`, not download.

## How the dot does it

Detection and classification are all connector work, which is the free part:

- **Gmail connector:** `from:upwork.com newer_than:2d subject:"sent you a message"`. The sender
  `room_<hex>@email.upwork.com` is the room; the full message text is in the plain-text body (the snippet is
  only the preheader). Resolve `link.email.upwork.com` click-trackers to the real Drive URL.
- **Drive connector:** `sharedWithMe` videos since `last_run`, plus by owner for Muhammad's accounts
  (`wadeededitteam@`, `sharkimageryproduction@`) and Waleed (`info.taimoormirzaa@`). Positive control:
  Muhammad's known drafts must return.
- **Zeeshan's two folders:** the dot opens each folder page in its own cloud browser and lists every child,
  or runs `folder_scan.py` on the linked Mac. Mandatory every run.
- **Dan's own side of a thread:** only readable in the Upwork room. Use the dot's browser (Upwork login saved
  in the dot's secure store, Dan enters it once) or leave the editor in `pending` and say why.

Filing needs the Mac. Two options, the Codex session picks the first that works:

- **A. Dot with the linked Mac:** `curl` the link-shared file to `<target>.part`, compare bytes to Drive's
  `fileSize`, rename on exact match, `mv` under the convention, update `state.json`, commit and push. All of
  this is in the skill's download recipe.
- **B. Codex automation as the filer:** the dot writes its verdicts (drive id, editor, title, kind, number,
  final or pending, reason) to a Google Sheet or Doc "Editor deliveries verdicts"; a 6:00 AM Codex automation
  on the Mac reads it and files what is marked final, then updates `state.json` and commits.

## Output every run

One short paragraph to Dan: what was filed (path and size), what is `pending` and why (by editor name), or
"nothing new from the editors, all three threads read, Zeeshan's folders listed". The morning brief (handoff
01) reads `pending` from `state.json`; do not add dashboard rows and do not edit `AI_COORDINATION.md`.

## The dot assignment (paste-ready, the Codex session finalizes it)

> Every day at 5:40 AM Central, check whether any of my three video editors (Muhammad, Zeeshan, Waleed)
> delivered a FINAL high-quality video. Read the Upwork notification emails in Gmail from the last two days
> (full body, not the snippet), check Google Drive for new videos shared with me, and open Zeeshan's two
> shared folders and list every file, because search never sees his drops. A file is final only if the
> editor called it HD or final, nothing newer was requested, and it is hundreds of MB. When all three are
> true, file it on my Mac under the rule in `.claude/skills/editor-deliveries/SKILL.md` and update
> `state.json`. If you could not read an editor's thread, list him as pending with "thread unread". Never
> report a quiet run from an empty search. Tell me what you filed, what is pending and why, in one paragraph.

## Steps for the Codex session

1. Read the skill, `state.json`, `folder_scan.py`, and the old Claude prompt at
   `~/.claude/scheduled-tasks/editor-deliveries-daily/SKILL.md`.
2. Confirm the three editors' rooms and Drive owners in `state.json` are current (Muhammad, Zeeshan, Waleed).
3. Decide filing option A or B; build B only if A is unavailable.
4. Finalize the assignment text and hand it to Dan with the connector list (Gmail, Drive, GitHub, linked Mac)
   and the schedule.
5. Prove one run in the afternoon (never the same morning as the Claude routine): the dot must re-find the
   already-filed ids in Zeeshan's folders as its correctness check, and must produce a report that names
   every editor.
6. Give Dan the toggle: Claude app, Routines, `editor-deliveries-daily`, off. Record in `Docs/ROUTINES.md`.

## Traps

- The Claude routine has a warning icon in Dan's sidebar. Read its last run log first; do not port a broken
  step.
- Muhammad's team re-uploads the same final under new names. Compare `fileSize` against `filed` first.
- Two exports (h264 + h265) both get filed with a codec tag before the extension. The `.audio_gate.json`
  sidecar is renamed with its mp4.
- Never use Drive's "download file content" style API for a video; it returns base64 into context.

## Done means

One proven afternoon run with all three editors accounted for, `state.json` updated and committed, the dot
scheduled for 5:40 AM, the Claude routine toggled off by Dan, and `Docs/ROUTINES.md` updated.

## Starter prompt

```
Read Handoffs/handoff-20260930-codex-dot-00-shared-setup.md, then execute Handoffs/handoff-20260930-codex-dot-02-editor-deliveries.md in full. Read the editor-deliveries skill and state first, prove one afternoon run, and give Dan the Claude toggle in one message.
```

Model: GPT-6 Sol, medium effort.
