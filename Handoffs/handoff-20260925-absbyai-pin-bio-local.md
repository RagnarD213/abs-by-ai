# Handoff: finish the @abs.by.ai retirement on Dan's Mac (pin, bio, permissions, memory)

**Date:** 2026-09-25
**Executor:** Claude, local desktop task (needs the in-app browser or Claude in Chrome). Sonnet 5 / Medium.
**Parent:** `handoff-20260924-absbyai-ig-final-post-and-shutdown.md`, executed in a cloud session on 2026-09-25 except the items below.

## Already done (do not redo)

- Farewell post live on `@abs.by.ai`: https://www.instagram.com/p/DdsIKm8GPsv/ (image: revision-2 A, Drive `13ixxgyXdM8rTNkOr1sWh51iG-AUtnJMx`; Dan's own caption).
- All 37 queued `@abs.by.ai` (Blotato `65632`) posts deleted; queue 155 to 118; re-pull confirmed 0 left. Backup: `scripts/blotato/absbyai_retire_backup_20260924.json`.
- Queue scripts no longer build a mirror post; `danrosefit_migration.py` and `danrosefit_finish_mirror.py` refuse to run. `video-setup` and `shorts` skills say never queue it. Commit `09d72ee` on `main`.
- AGENTS.md: batch approval once, never per item (Dan, 2026-09-25).

## Do these (Dan approved all of them; do not re-ask)

### 1. Pin the post
Browser on instagram.com logged in as `@abs.by.ai` (switch accounts if it shows `@danrosefit`; if switching needs a password, stop and give Dan the phone steps, since Claude cannot type passwords). Open the post, "..." menu, "Pin to your profile". Instagram allows 3 pins; the account has 3 proof posts pinned, so unpin the oldest first.

### 2. Change the bio
Edit profile, Bio, replace with exactly:
`Posts paused. Follow @danrosefit for everything new.`
Dan chose this over the handoff's "We've moved" wording (his caption says "pausing posts"). Keep the Name field and the existing links (SixPackAbs.com, absbyai.com).

Reload the profile and confirm: the new post is first with the pin icon, and the bio reads correctly.

### 3. Stop per-item permission prompts for Blotato
Dan was prompted 37 times for 37 deletes and called it ridiculously annoying. The cloud session's attempt to edit `.claude/settings.json` was blocked as self-modification, so ask Dan to approve this one change (a single prompt), or have him run `/permissions` himself. Add to `permissions.allow` in `.claude/settings.json`:
`mcp__Blotato__blotato_list_schedules`, `mcp__Blotato__blotato_get_schedule`, `mcp__Blotato__blotato_delete_schedule`, `mcp__Blotato__blotato_update_schedule`, `mcp__Blotato__blotato_list_accounts`, `mcp__Blotato__blotato_get_post_status`, `mcp__Blotato__blotato_create_presigned_upload_url`.
Do not add `blotato_create_post` (that one publishes publicly).

### 4. Memory (auto-memory directory on the Mac)
- Update `instagram-account-state.md`: `@abs.by.ai` retired 2026-09-24/25, farewell post pinned (link above), bio says posts paused, no mirror posts ever again; account kept for the handle, support DMs, the Facebook Page pairing and ad-account insurance. Never delete or deactivate it.
- Add a feedback memory: for batch jobs ask Dan once for the whole batch with a count, never per item.

## Finish

- `grep -c '—'` on every file you wrote must be 0.
- Commit `.claude/settings.json` if changed, push to `main`.
- Delete this handoff's line from the HANDOFFS section of `AI_COORDINATION.md` (re-read from disk first) and its row in `Handoffs/README.md`; run `scripts/board-check.sh`.
- Report to Dan in plain language: pinned, new bio, permissions done, memory updated.
