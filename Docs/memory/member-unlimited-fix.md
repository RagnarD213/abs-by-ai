---
name: member-unlimited-fix
description: Fixed (2026-07-16) — members were credit-blocked on image generation; both code changes are on main. Live verification on absbyai.com still pending.
metadata: 
  node_type: memory
  type: project
  originSessionId: 911c9809-c7ad-4cbf-9b52-f0d52952887e
---

Diagnosed July 15 2026, fixed and pushed to main July 16 2026: members were credit-blocked on `/api/generate-image` because `callGeminiImage` in index.html sent no Authorization header, so the server's `isActiveMembership(req.user)` check never saw the user. Both changes from `HANDOFF_member_unlimited_fix.md` are now live on main:
1. `callGeminiImage` (index.html) now sends `Authorization: Bearer` when `auth.token` exists — commit `afcca82`.
2. `isActiveMembership` (server.js) has an ADMIN_EMAILS unlimited bypass — this landed earlier than expected, folded into an unrelated commit `0ac348d` ("Dashboard: add Key task tier...") by a concurrent session working in the same working directory.

No 23-generations/month cap was added — members stay unlimited; free users keep 3 lifetime credits, per Dan's explicit decision.

**Still pending:** live verification on absbyai.com per the handoff's "Verification" section (log in as a member with 0 device credits, confirm unlocked generation + unchanged credit balance; confirm logged-out/anonymous still gets paywalled; confirm admin email bypass works). Also confirm Railway env var `ADMIN_EMAILS` includes `danroseconsulting@gmail.com`.

**Process note:** this repo's working directory was being edited live by another concurrent session while this fix ran. `git commit -m "..." -- <path>` stages and commits the *entire current working-tree state* of that path, not just what was previously staged — it silently swept in ~200 lines of unrelated in-progress work on the first attempt. Had to `git reset --soft HEAD~1`, re-stage only the intended hunk via `git apply --cached` on a hand-built patch, then commit with no pathspec. When multiple sessions may share a working directory, isolate hunks with `git apply --cached` + plain `git commit` (no pathspec) rather than `git commit -- <file>`.

Related: [[accounts-member-hub]], [[pay-for-generations]], [[ai-trainer-membership]].
