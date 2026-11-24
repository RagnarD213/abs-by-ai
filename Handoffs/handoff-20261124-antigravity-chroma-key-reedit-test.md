# Antigravity (agy) re-edit test: long-form chroma key film, from scratch

**Category: LFC (long-form content), green screen. Test only, nothing ships, nothing is uploaded or scheduled.**
Date 2026-11-24. Owner: whoever Dan starts (Codex Sol high babysits `agy`; or Claude).

## Goal
Dan wants to know if Gemini in Antigravity (`agy`, agentic, on his Google AI subscription, never the paid key) edits a long-form chroma key film better than the Gemini desktop app did. Rebuild a film we already finished from scratch, then compare it with our approved master.

## Test subject (the control)
Reacting To Celebrity Ozempic Transformations (RO-24), the long-form green-screen standard. Approved master: `claude edited long form content/25 - Reacting To Celebrity Ozempic Transformations/`, the `claude round 5 | 16x9 | RO-24` file, SHA-256 `950120846b3b9a3b3d7ad418995a4138a998cefb10deacd281858dfe4703e2d3` (1920x1080, 8:35.58, -14.5 LUFS). Raw footage and clip windows: from that job's work files and `.claude/skills/longform-edit/reference/longform-greenscreen-standard/`. Locate the raw first; if it is gone from the drives, stop and report instead of picking another film.

## Rules for the Gemini run
- Give `agy` ONLY: raw footage, the final script/transcript, and the written standards (`_shared/chroma-key/README.md`, `longform-greenscreen-standard/README.md`, `_shared/greenscreen-bg/README.md`, `_shared/VIDEO-RULES.md`). It must NOT see the approved master or our build files (blind test).
- `gemini.sh` is answer-only; use `agy` in its agentic mode (check `agy --help`; do not use plan mode). Work in `~/Projects/_edit_work/AGY-RO24/`. Run `editcap.py acquire AGY-RO24` and `renderq.py` before heavy steps, as for any edit.
- Quota exit 3: wait, never switch to a paid key. Log every `agy` call, time and token counts.
- Key to the house standard (Claude R2 key, calibrated per source). Do not let Gemini invent its own key recipe.

## Compare (write `Docs/AGY_CHROMA_TEST_20261124.md`)
1. Key quality, measured with `mcflicker.py` and `measure_r2.py` on both: edge flicker (bar 0.69), dark rim (bar 2.7%), see-through over watch/glasses, specks, strands.
2. Structure vs R5 table: hook, per-person sequence, corner reactions, background changes on words, cards, recap, close.
3. Audio loudness/true peak; captions; graphics motion (Soft Blue Light).
4. Effort: hours, human fixes needed, number of retries.
5. Review page with the Gemini cut, the approved R5 and (if the Gemini desktop app attempt exists, ask Dan for its file) that one, three unlabeled, shuffled, silent-checks rule applied. Dan picks; reveal sources only when he asks.

## Done means
A review page link for Dan, the measurement table, and a one-line verdict (better / same / worse than the desktop app, with evidence). Slot released with `--review`. No upload, no schedule, no board entry beyond one line.

## Starter prompt
"Read Handoffs/handoff-20261124-antigravity-chroma-key-reedit-test.md and run it. Blind rebuild of the RO-24 Celebrity Ozempic long-form with Antigravity agy, then the comparison page. Test only."

Recommended model: Codex GPT-6.2 Sol, high effort, M2 (has the drives). Claude is paused for usage until the Thursday reset.
