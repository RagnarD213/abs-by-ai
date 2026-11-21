# Handoff — put `AI_COORDINATION.md` back on a diet (2026-09-14)

**Status: EXECUTED 2026-09-15** — board 11,722 words / 78,469 bytes → ~2,000 words / ~15 KB. Snapshot + inventory at the end of `AI_COORDINATION_ARCHIVE.md`; moved facts in `Docs/BOARD_REFERENCE.md`.

## Goal

`AI_COORDINATION.md` is loaded into **every message of every Claude Code session** in this project. Its own header
says "deliberately short", but it has grown to **~11,700 words / 78 KB (≈20,000 tokens)**. Together with `AGENTS.md`
(2,931 words), `CLAUDE.md` (845) and the memory index (1,903), every message re-reads **≈118 KB, ~30,000 tokens**
before it even sees Dan's question. In a 40-message session that is over a million tokens of re-reading.

Cut the board to **≤ 2,500 words (≈3,500 tokens)** without losing a single open item, a single thing Dan has to
do, or a single warning that changes what the next session does. Measured before/after goes in the report.

This came out of Dan's 2026-09-14 question about token-saving skills (Ponytail / Caveman). The finding was that
neither skill touches the real cost — this file does. Expected saving: ~15,000–17,000 tokens **per message**,
with no quality loss, because the detail it removes already lives in docs, skills and git.

## Scope — this task only

- **In:** `AI_COORDINATION.md` (rewrite), `AI_COORDINATION_ARCHIVE.md` (append), a one-line size budget in the
  board's header and in `CLAUDE.md`'s shared-workflow list, `Handoffs/README.md` (remove this doc's row when done).
- **Out:** `AGENTS.md` trimming (that is item 2 from the same conversation — a separate task, not this one), memory
  files, skills, any code. Do not "fix" anything an entry describes; only compress how it is recorded.

## Authorization

Dan asked for this directly (2026-09-14). That is the explicit authorization the "one session owns a task, edit only
your own entry" rule requires to edit other sessions' entries — **for compression only**. You may shorten, merge and
archive other sessions' text; you may not change their status, owner, or next action, and you may not delete an
item that is still open.

## Method

### 1. Snapshot first, so nothing can be lost
1. `git status` — note that `AI_COORDINATION.md` already carries other sessions' uncommitted edits. That is normal.
2. Measure: `wc -w -c AI_COORDINATION.md AGENTS.md CLAUDE.md ~/.claude/projects/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/memory/MEMORY.md`.
3. **Append the entire current board verbatim** to the END of `AI_COORDINATION_ARCHIVE.md` under a heading
   `## Board snapshot before the 2026-09-14 diet (verbatim)`. Every trimmed detail stays one grep away.
4. Build an inventory in your scratchpad: one row per entry (there are ~60 bold-titled entries across the four
   sections), columns: title · section · owner · open / done · Dan action (verbatim, short) · next action · where the
   detail already lives (doc path, handoff, memory, skill). This inventory is the acceptance checklist.

### 2. Classify every entry
- **A. Still open, someone other than Dan acts next** → keep, ≤ 3 lines.
- **B. Waiting on a Dan decision or click** → move the ask into a single **"Dan's decisions"** list at the top
  (one bullet each: what, the recommended default, link). Keep a ≤ 2-line entry only if a session also has
  follow-up work after he answers.
- **C. Done, and the only thing left is "Dan has seen it" / "delete once he reads"** → collapse to one bullet in a
  **"FYI for Dan (read once, then delete)"** list. Do not delete outright — Dan hasn't approved those as finished.
- **D. Duplicates / superseded** → merge. Known examples: the two "Longforms 02 + 03" entries (the "hold expires
  09-09" one is stale — hold is now purely Dan's call); "Google Ads account fixes 09-09" (its $2.00 CPC ceiling was
  removed by Google auto-apply on 09-11, per the rep-tasks entry) and the Ads-digest "Search went dark since the
  $2.00 ceiling" warning (same stale cause); Zepbound + supplements shorts + spray-tan (one "shorts parked behind the
  long-form hold" line); Video-quality Phase 1 + Phase 2 + VQC-A (one line + the Phase 3 handoff pointer); the Ad 5
  vertical entry + its separate gate.py findings entry.
- **E. Reference facts, not status** (e.g. "Meta API access — WORKING", token-minting recipe, Page ids, the
  `DATABASE_PUBLIC_URL` trap, the digest-changes trap) → **move to the right durable home first** (the doc or memory
  the entry already cites, e.g. `Docs/`, a memory file), verify it landed there, then leave at most a pointer. If no
  home exists, create a short `Docs/` note rather than dropping it.

### 3. Entry format
```
**<Title> — <STATUS> <date>, owner: <session/Dan>.** <One sentence of state.> Next: <exact action>.
⚠ <only a warning that changes what the next session does>. Detail: `<path>`.
```
≤ 3 lines. No measurements, commit lists, verification narratives or quotes unless they change the next action —
those live in the linked doc or git. Keep IDs a session needs to act (campaign ids, doc ids, video ids) only when no
linked doc holds them.

### 4. New structure (in this order)
1. Header + routing table (keep; tighten the prose) + working rules, adding: **"Size budget: this file stays under
   2,500 words. If an edit pushes it over, compress or archive before saving."**
2. **Dan's decisions** (bullets)
3. **FYI for Dan** (bullets)
4. **ACTIVE** (sessions currently working — including the Codex entries; keep their owner ids exactly)
5. **BLOCKED — external**
6. **HANDOFFS WRITTEN, NOT EXECUTED** (one line each: path — fire when — model; the long paragraphs already live in
   `Handoffs/README.md` and the docs themselves)

### 5. Concurrency — the real risk
Other sessions (Claude and Codex) write to this file many times a day; an entry was clobbered this way on 09-01.
- Build the new file in the scratchpad. **Immediately before writing, re-read the file from disk and diff it
  against your step-1 snapshot.** Any entry added or changed since then gets folded in (compressed) before you save.
- Write it in one Write call, then re-read once more; if it changed in the seconds between, repeat the fold-in.
- Check for running sessions before starting (`mcp__ccd_session_mgmt__list_sessions` if available) and mention in
  the report which were active.

### 6. Verify
- `wc -w AI_COORDINATION.md` ≤ 2,500. Report before/after words, bytes and estimated tokens (bytes ÷ 4).
- Walk the inventory: every A/B row findable in the new board; every B ask appears in "Dan's decisions"; every
  E fact confirmed present at its new home. Put the finished inventory (title → where it went) at the bottom of the
  archive snapshot so anyone can audit it.
- Spot-check five random warnings (⚠ lines) from the old file and confirm each is either kept, moved, or genuinely
  obsolete (say why).

### 7. Deliver
- Add the size-budget line to `CLAUDE.md` under "Shared-workflow requirements" (one line).
- Commit **only** `AI_COORDINATION.md`, `AI_COORDINATION_ARCHIVE.md`, `CLAUDE.md`, `Handoffs/README.md`, this doc, and
  any `Docs/`/memory homes you created. Other sessions' uncommitted edits to the board become part of this commit
  by necessity — say so in the commit message. Pull `--rebase` first, push to `main`.
- ⚠ A push redeploys Railway, which wipes in-memory locked holds (memory `deploy-drops-locked-holds`). This is a
  docs-only change: confirm the deploy succeeds and absbyai.com returns 200; no further live check is needed.
- Remove this handoff from the board's HANDOFFS section and from `Handoffs/README.md`. No dashboard row (Dan's
  09-08 rule).
- Report to Dan in plain language: tokens saved per message, what moved where, and the "Dan's decisions" list.

## Current state (2026-09-14)
Nothing executed. The measurements above were taken this session. Archive file exists and is tracked.

## Open risks
- Deleting an open item by mistake — mitigated by the verbatim archive snapshot + inventory.
- A concurrent session writing mid-edit — mitigated by §5.
- Regrowth: without the budget line the file will bloat again within a week; the rule is part of the deliverable.

## Starter prompt
> Execute `Handoffs/handoff-20260914-coordination-board-diet.md`. Cut `AI_COORDINATION.md` to under 2,500 words
> without losing any open item, Dan action or live warning — archive the verbatim snapshot first, build the
> inventory, fold in concurrent edits right before writing, verify against the inventory, then commit, push, and
> report the before/after token numbers to me in plain language.

**Recommended model:** Opus 5, high effort — one session. It is editorial judgment across ~60 entries where the
cost of a mistake is a lost blocker, so don't drop to a smaller model.
