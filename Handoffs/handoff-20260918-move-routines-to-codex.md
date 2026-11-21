# Handoff — move the Claude routines to Codex

Written 2026-09-18 by Claude (Fable 5.1) at Dan's request. **Executor: Codex.**

## Why

Dan is at 52% of his Claude weekly allowance one day into the week. Routines are not the main burn (video editing is —
see `handoff-20260918-claude-video-freeze-and-codex-routing.md`), but each one opens a session that loads ~15k tokens of
project instructions before it does anything, every day, for work that needs no Claude-level judgment. Memory
`codex-owns-non-core-work` (2026-09-15) already says routines and ops belong to Codex.

## Current Claude routines (listed 2026-09-18; prompts live in `~/.claude/scheduled-tasks/<id>/SKILL.md`)

| id | schedule | verdict |
|---|---|---|
| `editor-deliveries-daily` | daily 05:40 | **Move to Codex.** Pure filing: scan Upwork threads (Muhammad, Zeeshan, Waleed), list Zeeshan's two Drive folders, download finals, file under the naming convention, write ambiguous ones to `state.json` pending. Rules: `.claude/skills/editor-deliveries/SKILL.md`. |
| `daily-watch-history-review` | daily 06:04 | **Move to Codex and make it weekly (Sunday 06:00).** Lowest-value daily run; the Sunday run already covers IG/FB/TikTok. |
| `unemployment-payment-reminder` | Wed 08:04, biweekly logic inside | **Move to Codex.** One dashboard write; mechanics in `.claude/skills/dashboard-tasks/SKILL.md`. |
| `twc-work-search` | Mon + Thu 08:00 | **Leave on Claude.** Already Sonnet 5 / medium via the `twc-applier` agent, signed-in WorkInTexas flow, legally sensitive logging. Revisit only if Dan asks. |
| `abs-by-ai-morning-brief` | disabled | Leave disabled. If Dan wants it back, it comes back on Codex. |

Everything else in the list is a spent one-time task, already disabled — ignore.

## Steps (per routine being moved)

1. Read the Claude routine's `SKILL.md` and the skill it references. Read `AI_COORDINATION.md` from disk.
2. Create the equivalent **Codex automation** on the same schedule (weekly for the watch-history review), in this project
   directory, at the lowest model/effort that does the job (start at Sol / Medium; filing and reminders may run lower).
   Carry the prompt over verbatim except for Claude-only tool names — replace those with the Codex equivalent
   (Codex browser for Upwork/Drive/YouTube; `curl` with `X-Dash-Key` from `~/.absbyai-secrets.env` for the dashboard).
   Never paste a secret into the automation text; read it from the secrets file at run time.
3. **Prove one run by hand** before trusting the schedule:
   - editor-deliveries: run it; confirm it reads the three Upwork threads and both of Zeeshan's folders, and that
     `state.json` is updated. It must file nothing it cannot prove is a FINAL (the skill's rule).
   - watch-history: run it; confirm output lands where the Claude routine wrote it.
   - unemployment reminder: dry-run only (read the dashboard, show the row it would add); do not add a duplicate row.
4. Only after a proven run, turn the Claude copy **off, not deleted**. Codex cannot reach Claude's scheduler, so tell Dan:
   "Claude app → Routines → <name> → toggle off." List all three names in one message so he does it once.
5. Record the change: add a short `Docs/ROUTINES.md` (new) listing every routine, which tool runs it, its schedule, and
   where its prompt lives. (Claude's memory files are Claude-side; leave them.) Commit + push.

## Traps

- The editor-deliveries routine shows a warning icon in Dan's sidebar (so does TWC) — read its last run via the routine's
  folder/logs first; if it has been failing, fix the cause in the Codex version rather than copying a broken prompt.
- Zeeshan's deliveries: Drive search cannot see folder drops or `.srt` files — list his two folders every run (memory
  `zeeshan-delivery-includes-srt`).
- Chrome's Instagram is signed in as @abs.by.ai, not @danrosefit (board, 09-17) — the Sunday watch-history run must not
  assume the account.
- Two runs of the same routine on the same morning (Claude + Codex) would double-file. Keep the Codex schedule disabled
  until Dan has toggled the Claude one off, or offset the proof run to the afternoon.
- No dashboard rows for this handoff (Dan's 09-08 rule). No customer email, no publishing — none of these routines needs either.

## Done means

Three Codex automations exist and each has one proven run; Dan has the one-message list of Claude toggles to flip;
`Docs/ROUTINES.md` committed and pushed; plain-English summary in chat.
