# Metabolism Not The Reason SFC (DS-107): edit it in Antigravity, M6 + Extreme only

**Category: SFC (dedicated short-form content), green screen. Test: nothing uploads, schedules or goes to setup.** Date 2026-11-25. Task name: `Metabolism Not The Reason SFC R1`. Replaces `handoff-20261124-antigravity-m6-edit-test.md` (that one dictated key, format and structure details; this one leaves creative choices to the editor).

## What this is
A normal edit job, handed to Gemini in Antigravity (`agy`, Dan's Google AI subscription, never a paid key) instead of Claude or Codex, because Dan is low on both. Dan wants to see whether its edit, run the regular way, is as good as ours. Dan approved a finished version of this Short on Nov 15, and it is the comparison only after Gemini delivers.

## Inputs
- Raw green-screen roll: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1908.MP4` (plus `C1908M01.XML`). Read it in place.
- Script: the spoken words are the approved Short's captions. Copy the words (no timings) from `/Volumes/Extreme/Short-form video content/Metabolism Not The Reason - DS-107/Metabolism Not The Reason SFC R2.srt` into a plain `script.txt` first.
- Do not open the approved video, its timings, or `/Volumes/Extreme/_edit_work/DS-107/` until your own cut is delivered.

## Machines and drives
M6 and the Extreme only. No M2, no Seagate or Expansion. Pick the work folder with `python3 .claude/skills/_shared/renderq/renderq.py workdir AGY-DS107 --need 15`; if it refuses both drives, stop and report the free space on each (the Extreme had about 27 GB free at last check). Do not delete anything to make room.

## How to edit
Edit it the regular way: read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` and the project's editing skills and standards (green-screen key, short-form rules, graphics, audio, captions), and follow them as written. Creative decisions (cuts, takes, framing, graphics, timing) are yours. Run the normal gates on the exact export. Review export is 1080p.

## Job rules
- Priority is strictly below Joint Vigor (`SRM-JV-R5`): `editcap.py status`, acquire only an idle slot (`editcap.py acquire AGY-DS107`), run heavy steps through `renderq.py`, yield or release if Joint Vigor needs the slot or cores.
- Model: `gemini-4-neon-high`; retry a failed step once on `gemini-4-neon-xhigh`. Log model and time per call. Quota exit: wait.
- No Claude or Codex calls. No paid key. No upload, schedule or setup handoff.

## Done means
1. A silent-checks review page for Dan (`review_server.py`, sound-ready owner handoff) with Gemini's cut and the approved cut, unlabeled and shuffled.
2. A short report, `Docs/AGY_DS107_TEST_20261125.md`: gate results, what Gemini decided, hours, retries, anything a human had to fix.
3. Edit slot released with `editcap.py release AGY-DS107 --review`; stop for Dan's review.

## Starter prompt (paste into Antigravity)
"Read Handoffs/handoff-20261125-antigravity-regular-edit-test.md and do it. Edit the DS-107 Metabolism Not The Reason green-screen Short from raw C1908.MP4 the regular way, using only the M6 and the Extreme drive. Stay below Joint Vigor in editcap and renderq. Never open the approved video until yours is delivered. Test only: no upload, no scheduling."

Recommended: `agy` Gemini 4 Neon High.
