# Handoff — freeze Claude video editing until the weekly reset; route the edit queue to Codex

Written 2026-09-18 by Claude (Fable 5.1) at Dan's request. **Executor: Codex** (so the fix costs no Claude allowance).

## Why

Dan's Claude weekly allowance reset Thu 2026-09-17 11:00 CT. By Fri 08:43 — **22 hours later — 52% of the week was
gone** (Fable 49%). The burn is Claude video editing: RA-01 on the three-role pipeline (Fable plan → Opus edit → Fable
review, 3 rounds), DS-04, VQC Phase 4 (two Ad 1 verticals), the overnight-queue proof run. Routines are small change
next to that. Dan needs the remaining Fable allowance for scripts, revision docs and planning.

## Goal

1. No new Claude video-editing or Claude video-review session starts before **Thu 2026-09-24 11:00 CT**.
2. The overnight queue keeps working for Dan — on Codex.
3. After the reset, Claude editing is the exception, not the default.

## Facts verified 2026-09-18 08:48

- Queue code: `scripts/edit-queue/` (read its `README.md` first). Routing lives in `scripts/edit-queue/config.json` → `routing`;
  "Flip a row by editing `config.json`. Nothing re-routes itself."
- Current routing: `RA/RO/DS` → Codex Sol/high, **reviewed by Claude `ra-reviewer` (Fable, high)**. `AV/AS/SL` →
  **Claude Opus/high**, reviewed by Codex.
- The unattended pilot (`config.json` → `unattended`) is groups `AV/AS/SL`, size S, 3 launches a night — i.e. **the
  overnight queue today launches only Claude edits.**
- `dispatcher.py status` showed 0 queue jobs running, 2 other builds running, nightly cap already reached.
- Job list: `Handoffs/video-editing/jobs.json` (76 jobs: RA 16, RO 8, DS 25, AV 12, AS 11, SL 3, RX 1). Each job doc has
  both a Claude and a Codex starter prompt.
- Open Claude video work waiting on Dan, per `AI_COORDINATION.md`: RA-01 (masters held), DS-04 (delivered), VQC Phase 4
  blind pick, Ad 4 vertical masters held. None of these burns allowance until Dan rules.

## Steps

1. `git pull --rebase`; read `AI_COORDINATION.md` from disk and `scripts/edit-queue/README.md`.
2. **Do not kill running renders.** ffmpeg / gate processes cost no model allowance. Only stop new model sessions from starting.
3. In `scripts/edit-queue/config.json` → `routing`:
   - `AV`, `AS`, `SL`: editor → **Codex** (same model/effort as the RA/RO/DS row). Reviewer → a **fresh Codex session**
     (a different session from the editor; the README's rule is "a *different* AI reviews" — record in the README that
     until 2026-09-24 the reviewer is a separate Codex session, by Dan's instruction, to protect Claude allowance).
   - `RA`, `RO`, `DS`: reviewer → fresh Codex session as well, until 2026-09-24.
   - If the runner cannot express "Codex reviews Codex", use `dispatcher.py pause-group <GROUP> claude --reason
     "Claude allowance freeze until 2026-09-24 11:00 CT"` for every group and tell Dan exactly what the runner needs.
     Do not leave any path that launches `claude` headless.
4. Prove it: `python3 scripts/edit-queue/dispatcher.py tick --dry-run` and confirm no line would launch a Claude editor
   or a Claude reviewer. Grep `runner.py` for the `claude` invocation and confirm both call sites are unreachable under the
   new config.
5. Update `scripts/edit-queue/README.md` "Who edits what" table to match, with the date and the revert date.
6. Revisions Dan sends back on RA-01, DS-04 or any Claude-built video before 09-24: they go to Codex using that job's Codex
   starter prompt plus the existing recipe folder. Note this in the two board entries' "Next:" only if you own them —
   otherwise tell Dan in chat.
7. Commit + push (`main`). No production deploy is involved; still confirm the push landed.
8. Board: replace the "Overnight edit queue" ACTIVE entry's state with one line — "all groups on Codex until 2026-09-24
   (Claude allowance freeze); revisit routing after the reset". Run `scripts/board-check.sh`.

## After the reset — the standing rule to propose to Dan (do not write it into AGENTS.md without his yes)

- Default every edit to Codex. Claude edits only (a) a job Codex has failed twice, or (b) by Dan's explicit call.
- No Fable reviewer leg. Review = Codex cross-session + Gemini quality review (standing-authorized under $5); Claude
  reads only the written verdict when Dan asks.
- Any Claude video session hands off at ~150k context, and sends renders/QC to the background rather than waiting in-session.

## Do not

- Do not change any gate, threshold or corpus file. Do not touch held masters. Do not start any job to "test" the
  routing beyond `--dry-run`.
- Do not un-pause or alter the `unattended:false` flags on SL-01/02.

## Done means

Dry-run proof pasted in chat, config + README committed and pushed, board entry updated and under budget, and one plain-English
paragraph to Dan saying what the queue will now do tonight.
