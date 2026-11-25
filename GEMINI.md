# Antigravity Persistent Memory & Improvement Loop (Abs By AI)

This file wires Google Antigravity into the **single shared brain** already used by Claude Code and Codex for the Abs By AI workspace. Do not create separate memory silos (no separate Obsidian vault or disconnected notes).

---

## 1. Full Rules Coverage (Bypassing the 24 KB Per-File Cap)

Antigravity automatically loads the first 24 KB of `AGENTS.md` (roughly lines 1–112) and truncates the rest. To ensure zero standing rules are lost:

- The workspace startup hook (`.agents/hooks.json` → `.agents/hooks/session_start_memory.py`) automatically reads `AGENTS.md` live at the start of every new session and injects the full remainder (past byte 24,000) plus the merged `MEMORY.md` index.
- **Fallback:** If you are in a resumed, compacted, or CLI session where the startup hook message is not present in context, read `AGENTS.md` from line 110 to the end and read `MEMORY.md` before starting any domain task (video, ads, writing, design, publishing, deployments, or machine changes).

---

## 2. Where Shared Memory Lives (Read Before Acting)

| Layer | Location | Purpose |
| :--- | :--- | :--- |
| **Local memory (canonical on Dan's Mac)** | `~/.claude/projects/-Users-danrrose-Projects-Claude-Projects-Abs-By-AI/memory/` (index: `MEMORY.md`) | All 360+ memory files, including private/local-only entries |
| **Repo memory mirror (PUBLIC)** | `Docs/memory/` (index: `Docs/memory/MEMORY.md`) | Public-safe mirror synced via `scripts/sync-memory-to-repo.sh` |
| **Standing rules (all AIs)** | `AGENTS.md` (and `CLAUDE.md` summary) | Non-negotiable business, production, and routing rules |
| **Active coordination board** | `AI_COORDINATION.md` | Open multi-AI work, blockers, ownership (re-read before claiming/editing) |
| **Dan's open decisions** | `Docs/DAN_DECISIONS.md` | Items waiting on Dan |
| **Workflow skills** | `.claude/skills/` and `~/.gemini/config/plugins/migrated-settings/skills/` | Step-by-step procedures, recipes, and quality gates |

**Before starting work in any domain:**
1. Scan the `MEMORY.md` index injected at session start (or read it from disk) and open any memory `.md` file relevant to the task so you never repeat a past mistake.
2. Check `AI_COORDINATION.md` before modifying shared code, schedules, or active video/ad jobs so you never overwrite work owned by Claude or Codex.
3. For any video, photo, thumbnail, cover, audio, or publishing work, read `.claude/skills/_shared/VIDEO-RULES.md` first.

---

## 3. Continuous Improvement Loop (Write Back What You Learn)

Whenever Dan corrects you, gives a new preference or rule, approves a standard, or you discover a non-obvious trap/fix that future sessions should know, **close the loop immediately** so Antigravity, Claude, and Codex all get smarter together:

1. **Put the lesson in the right home:**
   - **Durable preference, feedback, or project fact** → Create or update a Markdown file in the local memory folder (`~/.claude/projects/-Users-danrrose-Projects-Claude-Projects-Abs-By-AI/memory/<slug>.md`) using standard YAML frontmatter (`name`, `description`, `metadata: {node_type: memory, type: feedback|project|user|reference, modified: <ISO-8601>}`) and add a concise 1-line link to `MEMORY.md`.
   - **Standing rule every AI must always obey** → Add a dated `## <Rule Title> (Dan, YYYY-MM-DD)` section near the top of `AGENTS.md` (linking the memory slug) and add a brief matching entry to `CLAUDE.md` if appropriate.
   - **Workflow trap, calibration, or recipe** → Update the relevant skill in `.claude/skills/<skill>/SKILL.md` (and mirror the update to `~/.gemini/config/plugins/migrated-settings/skills/<skill>/SKILL.md` if that copy exists).
   - **Open task state** → Update only your own entry in `AI_COORDINATION.md` (≤3 lines, ≤80 words, dated; delete it once finished and approved; run `scripts/board-check.sh`).
2. **Public Repo Privacy Guard (CRITICAL — `abs-by-ai` is a PUBLIC GitHub repo):**
   - Before syncing any memory entry to `Docs/memory/`, decide if it is private (Dan's personal life, health beyond public videos, money/finances, legal matters, other people's private names/emails, credentials/logins, or live product vulnerabilities).
   - **If private:** Add its slug (without `.md`) to `.repo-private` in the local memory folder so it stays on Dan's Mac only.
   - **If safe for the repo:** Run `scripts/sync-memory-to-repo.sh` (which runs the secret scanner and rebuilds `Docs/memory/`), then push with `scripts/git/safe-push.sh -m "Sync memory: <short topic>" -- Docs/memory` (plus any edited shared files like `AGENTS.md`).
3. **Confirm briefly in chat:** Tell Dan in one plain-English line what lesson was saved and whether it was kept local-only or synced for all AIs.

---

## 4. Core Guardrails (Always Active)

- **Plain-English communication:** Dan is a non-technical founder. Explain actions and results simply, in a direct, businesslike tone. Put numbered action items at the bottom when Dan has decisions or next steps.
- **Protect Claude and Codex (`protect-codex-and-other-ais`):** Before any machine-level path, symlink, config, or hook change, verify it does not break Claude Code or Codex. Never turn on Codex fast mode (`service_tier="priority"`) without asking Dan first.
- **Safe git pushes only:** From the main project folder, commit and push ONLY with `scripts/git/safe-push.sh -m "<message>" -- <your files>`. Never run `git pull --rebase`, `git stash`, or `git add -A` here.
- **No secrets or private media in git:** Never commit personal photos, videos, credentials, or private docs to this public repository.
