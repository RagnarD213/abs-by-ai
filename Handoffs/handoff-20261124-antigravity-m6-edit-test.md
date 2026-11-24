# Antigravity (agy) edit test, M6 + Extreme only: DS-107 green-screen Short

**Category: SFC (dedicated short-form content), green screen. Test only. Nothing ships, uploads or schedules.**
Date 2026-11-24. Replaces the RO-24 plan in `handoff-20261124-antigravity-chroma-key-reedit-test.md` (too big: needs the Seagate). Supersedes the open questions in `handoff-20261124-agy-chroma-test-m6-rescope.md`.
Assumes Grokbot has already cleared space (see Gate 0). Do not clear space yourself.

## Goal
Find out whether Gemini in Antigravity (`agy`, Dan's Google AI subscription, never a paid key) can edit and chroma-key a green-screen talking Short to our house standard. Rebuild a Short we already finished, blind, then compare against the approved master.

## Test subject (the control), all already on Extreme
- Film: **Metabolism Not The Reason (DS-107)**, SFC R2, about one minute, Dan approved Nov 15.
- Approved master (control, agy must NOT see it): `/Volumes/Extreme/Short-form video content/Metabolism Not The Reason - DS-107/Metabolism Not The Reason SFC R2.mp4` (52 MB) and its `.srt`.
- Raw green-screen roll: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1908.MP4` (4.7 GB, plus `C1908M01.XML`). Confirmed as the source from the DS-107 R2 recipe files.
- Script/transcript for agy: take it from the `.srt` words only (copy text to a plain `script.txt`; strip timings). The approved cut's timings stay hidden.
- Not needed, so no M2 and no Seagate: the film has no external reaction clip, celebrity footage or AI inserts.
- Our reference recipe lives in `/Volumes/Extreme/_edit_work/DS-107/r2/` (103 GB folder, leave alone, do not read it into agy's workspace).

## Gate 0: space (check, do not fix)
Run `df -h /System/Volumes/Data /Volumes/Extreme` and `python3 .claude/skills/_shared/renderq/renderq.py workdir AGY-DS107 --need 15`.
- Needed: about 15 GB (raw is read in place from Extreme, not copied; 4K key frames, cache and renders are the bulk).
- Proceed only if `workdir` returns a path. It prefers internal (keeps the 80 GB reserve), else Extreme (30 GB reserve). Honor its answer; never bypass the reserve.
- If it refuses both, stop and report the exact free GB on each. Do not delete anything, do not touch `SRM-JV-R5*`, and do not edit `~/.absbyai-editroute/storage.json` by hand.
- Prior run `AGY-RO24` (another session, started 14:19 ET) may still hold a slot and cores. This test does not continue or replace it. If it is still running, wait; do not stop it unless Dan says so.

## Priority: strictly below Joint Vigor VSL (SRM-JV-R5)
Joint Vigor is the client job and always goes first.
1. `python3 .claude/skills/_shared/editcap/editcap.py status`. If `SRM-JV-R5` is active or waiting, and no free slot exists, do not acquire. Arm the wait (`editcap.py wait AGY-DS107`), tell Dan "waiting behind Joint Vigor" and stop.
2. Acquire only a slot that would otherwise sit idle: `editcap.py acquire AGY-DS107`. Exit 3 means wait. Exit 5 or 6 follow the editroute messages.
3. Run every heavy step through `renderq.py` (first-come queue). If a Joint Vigor step is waiting, yield: never use the away or priority boosts for this job (no `/away`, no `priority-edit`).
4. If `SRM-JV-R5` later needs the slot, release immediately with `editcap.py release AGY-DS107` and resume after.
5. Keep core use to 2 cores for this job where the step allows it (`ffmpeg -threads 2`), and cap any key or render at the lowest priority (`nice -n 19`).
6. Never run this job while Joint Vigor is in a heavy ffmpeg step that is waiting on cores.

## Rules for the agy run (blind test)
- Give `agy` ONLY: raw `C1908.MP4` (read-only path), `script.txt`, and the written standards: `.claude/skills/_shared/chroma-key/README.md`, the Short caption, audio and Soft Blue Light graphics rules in `_shared/VIDEO-RULES.md`. It must not see the approved master, the `.srt` timings or the `r2` recipe folder.
- Use `agy` in agentic mode (check `agy --help`, not plan mode). Work only in the folder `renderq.py workdir` returned (`.../AGY-DS107/`).
- Models: `agy -m gemini-4-neon-high` first. A failed step retries once on `gemini-4-neon-xhigh`. Log model, time and token count for every call. Quota exit 3: wait, never switch to a paid key.
- Key to the house standard (Claude R2 key via `chroma-key/README.md`, calibrated to this source). Do not let Gemini invent its own key recipe.
- Deliverable format: 1080x1920, captions burned in word-timed, Soft Blue Light moving background, voice at -14 LUFS, house framing (hair-anchored, vertical centering). Review export is 1080p only.

## Compare (write `Docs/AGY_DS107_TEST_20261124.md`)
1. Key quality, measured on both with `mcflicker.py` and `measure_r2.py` (edge flicker bar 0.69, dark rim bar 2.7%), plus see-through, specks, strands.
2. Structure vs the approved master: hook, cuts, take choices (last clean take), captions, background motion, close line.
3. Audio loudness and true peak, offline measurements only.
4. Effort: hours, retries, human fixes needed.
5. Two-way review page: agy cut vs approved master, unlabeled and shuffled with `blind.py`, silent-checks rule applied (`review_player.js`, start silent, hand off paused with sound ready). The Gemini desktop-app attempt was never found in Drive, Downloads, Media or Extreme, so this is a 2-way comparison. If Dan later supplies that file, add it as a third option.

## Done means
Review page link for Dan, the measurement table, a one-line verdict (acceptable / needs fixes / not usable, with evidence), edit slot released with `editcap.py release AGY-DS107 --review`, and one line on the board. No upload, no schedule, no setup handoff. Clean up the work folder only when Dan says (the nightly archive handles idle jobs).

## Starter prompt for Antigravity (paste as is)
"Read Handoffs/handoff-20261124-antigravity-m6-edit-test.md and run it. Blind rebuild of the DS-107 Metabolism Not The Reason green-screen Short from raw C1908.MP4 using only M6 and the Extreme drive. Check space first with renderq.py workdir and stop if it refuses. Stay strictly below Joint Vigor (SRM-JV-R5) in editcap and renderq: wait or yield whenever it needs the slot or cores. Never open the approved master. Test only: no upload, no scheduling."

Recommended model: `agy` Gemini 4 Neon XHigh runs the work; Claude is not needed until the review page (Opus 5.5 high on request after the Thursday reset, or Codex Sol high).
