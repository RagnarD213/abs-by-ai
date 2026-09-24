# Handoff 2 of 2: Publish the @abs.by.ai farewell post and stop the account posting

**Date:** 2026-09-24
**Executor:** Claude, Sonnet 5 / Medium (Opus 5.5 / Medium if the Instagram web steps get fiddly)
**Fire when:** handoff 1 (`handoff-20260924-absbyai-ig-final-post-image.md`, Codex) is done **and Dan has
picked image A, B or C**. If he has not picked, stop and ask for the pick. That is the only question allowed.

## Goal

Retire `@abs.by.ai` as a posting account without deleting it. Dan approved this exact plan on 2026-09-24:

1. Publish one final post on `@abs.by.ai` pointing people to `@danrosefit`, and pin it.
2. Remove every future `@abs.by.ai` post from the Blotato queue.
3. Change the `@abs.by.ai` bio to say it moved to `@danrosefit`.
4. Keep the account. **Do not delete or deactivate it.** It holds the handle, takes support DMs, pairs with
   the Abs by AI Facebook Page, and protects the ad account (memory `instagram-account-state`).

Plus: make sure nothing adds new mirror posts to `@abs.by.ai` again.

## Facts you need

- Blotato account ids: Instagram `@abs.by.ai` = **`65632`**, Instagram `@danrosefit` = `67203`,
  Facebook Page = `47105`, TikTok = `58181`. Confirm with `blotato_list_accounts` first.
- The `@abs.by.ai` mirror has run one day behind `@danrosefit` since 2026-08-24, with captions rewritten to
  point at `@danrosefit`. Scripts that create mirror posts: `scripts/blotato/longform_queue.py`,
  `organic_short_queue.py`, `abwheel_queue.py`, `ad5_queue.py`, `danrosefit_finish_mirror.py`,
  `iggap_*`. Skills that tell sessions to create them: `.claude/skills/video-setup/SKILL.md` (line ~90 and the
  description), `.claude/skills/shorts/SKILL.md` (~583). Queue record: `BLOTATO_QUEUE_PROGRESS.md`.
- Blotato has a 200 scheduled-post cap. Freeing the mirror slots also unblocks the IG gap-fill item on the board.
- The image and its Drive link are in `social media graphics/instagram/abs-by-ai-final-post/` (gitignored;
  never commit it, the repo is public).

## Steps

### 1. Snapshot, then clear the future mirror posts
- Pull every scheduled Blotato post whose target is account `65632`. Save the full list (ids, dates, captions,
  media URLs) to `scripts/blotato/absbyai_retire_backup_20260924.json` **before deleting anything**, so any
  post can be recreated.
- Delete those schedules. Only `65632` targets. Do not touch any post on `67203`, `47105`, `58181` or YouTube.
  If one Blotato post targets several accounts at once, remove only the `65632` part, or recreate it without
  `65632`; never lose the other platforms' copy.
- Do NOT delete anything already published on `@abs.by.ai`.
- Re-pull and confirm zero future posts remain on `65632`. Report how many were removed and the new queue total.

### 2. Publish the farewell post
- Upload Dan's picked image with `blotato_create_presigned_upload_url`, then publish **now** to `65632` only.
- Caption (use as written; no em or en dash):

  ```
  This account is retiring.

  Everything from Abs By AI now lives on my personal account: @danrosefit

  Workouts, the food I actually eat, and the AI tools I use to stay lean. Follow me there so you don't miss anything.

  Thanks for being here.
  Dan
  ```
- No hashtags, no ManyChat keyword (ManyChat runs on `@danrosefit`, not here).
- Verify it is live with `blotato_get_post_status`, and get its public Instagram URL.

### 3. Pin it and change the bio
Blotato cannot pin or edit a profile. Use the in-app browser on instagram.com, logged in as `@abs.by.ai`.
Dan approved both changes, so do them without re-asking. If the browser is logged into `@danrosefit`,
switch accounts in the Instagram account switcher; if that needs a password, stop and give Dan the 30-second
phone steps instead (Claude cannot type passwords).
- **Pin:** open the new post, "..." menu, "Pin to your profile". Instagram allows 3 pins; the account already
  has 3 proof posts pinned, so unpin the oldest one first.
- **Bio:** replace it with:
  `We've moved. Follow @danrosefit for everything Abs By AI.`
  Keep the Name field and the existing profile links (SixPackAbs.com, absbyai.com) as they are.
- Reload the profile and confirm: new post is first in the grid with the pin icon, bio reads correctly.

### 4. Stop mirroring for good
- `video-setup` and `shorts` skills: remove `@abs.by.ai` / `65632` from the platforms they queue. Add one
  line: "@abs.by.ai retired 2026-09-24; never queue it."
- Queue scripts listed above: remove the mirror step (or make `65632` a refused target with a clear error,
  the same way `ad_guard.py` blocks ads). Run each script's dry-run mode to prove nothing targets `65632`.
- `BLOTATO_QUEUE_PROGRESS.md`: one short line recording the retirement and the backup file path.
- Leave `@abs.by.ai` on the Blotato account list (disconnecting it is not part of the plan).

### 5. Memory
Update `instagram-account-state.md` (in the auto-memory directory): `@abs.by.ai` is retired as of 2026-09-24,
farewell post pinned, bio says moved, no mirror posts; still kept for the handle, support DMs, the Page
pairing and ad-account insurance.

## Finish

- `grep -c $'\u2014'` on every file you wrote or edited must be 0 for the new text.
- Commit the skill, script, backup json and `BLOTATO_QUEUE_PROGRESS.md` changes (nothing from `photos/` or
  `social media graphics/`), push to `main`.
- Delete this handoff's line from `Handoffs/README.md` and the HANDOFFS section of `AI_COORDINATION.md`
  (re-read the board from disk first; edit only this line). Run `scripts/board-check.sh`.
- Report to Dan in plain language: the post link, that it is pinned, the new bio, how many queued mirror posts
  were removed, and that nothing will post there again.
