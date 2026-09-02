# Handoff: Connect TikTok to Blotato and mirror the scheduled queue onto it

**Date:** 2026-09-02
**Project:** Abs By AI (organic social)
**Business goal this serves:** marketing performance → app adoption (TikTok is the one big short-form platform still getting nothing from the content already made and queued)

## Objective

Connect Dan's TikTok account to Blotato, then schedule every video already queued for Instagram / Facebook onto TikTok as well, on a ramped cadence (one per day for the first week, then the full cadence), with TikTok-appropriate captions. Photo posts do NOT go to TikTok. When done, TikTok gets the same Shorts on the same days as the other platforms with zero further manual posting from Dan.

## Current State

- **The TikTok warm-up hold is over.** The dashboard rule was "do not connect Blotato before ~2026-09-02; early third-party connection risks a bot flag on a brand-new account." The account is now ~4 weeks old, Dan has used the app natively (20–30 min, ~2×/week) and the risk window has passed. Decision made 2026-09-02: connect it.
- **Blotato workspace has 4 accounts, no TikTok.** Live account ids (from `blotato_list_accounts`):
  - Facebook `47105` → page `1294282227094660` "Abs by AI"
  - YouTube `46963` "Abs by AI"
  - Instagram `65632` `@abs.by.ai` (mirror account, infrastructure only)
  - Instagram `67203` `@danrosefit` (the MAIN content account)
- **The queue (measured 2026-09-02 via `fetch_schedules`, 183 scheduled posts):**

  | account | posts | of which videos | dates |
  |---|---|---|---|
  | IG `@danrosefit` 67203 | 53 | **23** | 2026-09-03 → 2026-10-24 |
  | IG `@abs.by.ai` 65632 | 50 | 21 | 2026-09-02 → 2026-10-25 |
  | FB page 47105 | 80 | 21 | 2026-09-02 → 2027-01-15 |

  The **23 videos on `@danrosefit`** are the set to mirror. They sit on Tue/Thu/Sat (plus a few Mon/Wed) at **22:00 UTC = 5:00 PM Central**, every one already carrying a caption, hashtags, a `utm_source=instagram` link and an `.mp4` on `database.blotato.io` public storage. Photo posts (`.jpeg`) fill the other days — skip them.
- **YouTube Shorts are not in Blotato.** They were uploaded natively per `YouTube Long Form Video Content/SHORTS_UPLOAD_PROGRESS.md` on the same Tue/Thu/Sat 5 PM Central dates. Nothing to mirror from YouTube; the IG queue is the source of truth for media + dates.
- **Existing tooling to reuse:** `scripts/blotato/danrosefit_migration.py` (has `api_key()`, `call()`, `fetch_schedules()`, `content_key()`, `rewrite_cta()`, `BASE = https://backend.blotato.com/v2`) and `scripts/blotato/danrosefit_finish_mirror.py` (the create-then-delete mirror pattern, idempotent by construction). API key file: `Business/blotato-api-key.txt` (gitignored). The Blotato MCP is also connected in Claude Code (`blotato_list_accounts`, `blotato_create_post`, `blotato_list_schedules`, `blotato_delete_schedule`).
- **Dashboard rows involved** (`todos.json`, `business` list): `Post on TikTok` (key, recurring — Dan's manual daily post), `Connect Blotato and start scheduled posting (TikTok warm-up ends ~2026-09-02)` (high), `Catch TikTok up to the posting schedule (manual backfill)` (high).

## Key Decisions Already Made

- **Connect now, ramp the volume.** Week 1: max one TikTok post per day. After 7 days with no restriction notice, post on every queued video date. Reason: the residual risk on a young account is volume, not the API connection itself (Blotato posts through TikTok's official, audited Content Posting API).
- **Mirror `@danrosefit` (67203), not `@abs.by.ai`.** `@danrosefit` is the consolidated audience account (memory `instagram-account-state`); its captions are the canonical ones.
- **Videos only.** TikTok is a video platform; the photo posts stay on IG/FB.
- **Same dates and time as the other platforms (22:00 UTC).** Same content on every platform the same day — simplest, already how IG/FB/YouTube run. Ramp week shifts nothing; it only drops surplus posts (see plan step 5).
- **Captions: same hook + body, TikTok link and tags.** Swap `utm_source=instagram` → `utm_source=tiktok`, keep `utm_medium`/`utm_campaign`/`utm_content` so PostHog attribution works. Keep the hashtags. TikTok caption limit is 2,200 chars — the IG captions all fit. NOTE: links in TikTok captions are not clickable; keep the `AbsByAI.com` mention anyway (memory `shorts-production-style`) since the bio link does the work.
- **TikTok required fields (Blotato):** `privacyLevel: "PUBLIC_TO_EVERYONE"`, `disabledComments: false`, `disabledDuet: false`, `disabledStitch: false`, `isBrandedContent: false`, `isYourBrand: true`, `isAiGenerated: false` (these are Dan's real filmed Shorts, no AI disclosure needed). Confirm the exact field names against what `blotato_list_accounts` returns for the TikTok account once it's connected — the tool prints the `requiredFields` per platform.
- **Dan does the OAuth.** Connecting TikTok is a login in Blotato → Accounts → Add → TikTok. Claude cannot enter credentials; this is a platform restriction on Claude, not Dan's rule. Everything after that is Claude's.

## Detailed Plan

1. **Dan connects TikTok** in Blotato (blotato.com → Accounts → Add account → TikTok → log in on the Abs By AI / Dan Rose TikTok account). Then the session runs `blotato_list_accounts` with `platform: tiktok` and records the new `accountId` and its `requiredFields`.
2. **Confirm posting headroom.** Blotato's plan caps scheduled posts at **200**; the queue is at 183 (2026-09-02) and shrinks as posts publish. Adding 23 TikTok posts needs ≤177 in the queue. Check `fetch_schedules` count first. If short, the cheapest room is the Facebook mirrors dated after 2026-10-25 (the FB queue runs to 2027-01-15 — pull the latest ones and re-add them later, or upgrade the plan). Do NOT delete `@danrosefit` posts. **OPEN:** Dan may prefer to upgrade the plan rather than trim — say which in the starter prompt if you have a preference.
3. **Build `scripts/blotato/tiktok_mirror.py`** modelled on `danrosefit_finish_mirror.py`:
   - `fetch_schedules()` → filter `accountId == "67203"` and `mediaUrls[0].endswith(".mp4")` → 23 items.
   - For each: target time = same `scheduledAt`; caption = `rewrite` of the IG text with `utm_source=tiktok` (regex on the `utm_source=` param only); media = the same `mediaUrls` (Blotato accepts its own storage URLs as `mediaUrls` for a new post — the IG migration already relied on this).
   - Idempotent by construction: before creating, look for an existing TikTok schedule with the same `content_key` (media URL) and skip it. No state file.
   - `--dry-run` default, `--apply` to write. Print the plan as a table (date, hook line, action).
   - Post body per Blotato v2: `POST /v2/posts` with `{"post": {"accountId": <tiktok>, "target": {"targetType": "tiktok", <required fields>}, "content": {"text", "platform": "tiktok", "mediaUrls": [...]}}, "scheduledTime": "<iso>"}` — verify the exact shape against `blotato_create_post`'s description in the session; the MCP tool can also be used directly for the first one as a smoke test.
4. **Smoke test one post first**, scheduled for the next available slot (not immediate), then check `blotato_get_post_status` / `blotato_list_schedules` shows it on the TikTok account with the right time.
5. **Apply the ramp.** Week 1 = the first 7 days after connection. Within that window schedule at most one TikTok video per day; where two `@danrosefit` videos fall on consecutive days that is fine, but never two on the same day. Videos beyond day 7 go on their normal dates. The current queue only has 3–4 videos per week, so in practice the ramp changes nothing — just assert it in the script (`max 1/day`) so it holds if the queue is later densified.
6. **Run `--apply`**, then re-run `--dry-run` and confirm it reports 23 done / 0 todo.
7. **Verify live after the first post publishes** (next evening 5 PM Central): `blotato_list_posts` with `platform: ["tiktok"]`, `status: ["published","failed"]`. A `failed` with a TikTok error usually means a required field or a privacy-level mismatch on an unaudited account — fix and re-add that one post.
8. **Housekeeping:**
   - Check off the dashboard task `business::Connect Blotato and start scheduled posting (TikTok warm-up ends ~2026-09-02)` and `business::Catch TikTok up to the posting schedule (manual backfill)` (the backfill is superseded: the queue now covers TikTok going forward). Leave `Post on TikTok` (recurring) to Dan — ask him whether he wants it removed now that posting is automated.
   - Check off the Key task for this handoff.
   - Update `AI_COORDINATION.md`: delete this handoff's line; add a two-sentence "TikTok live via Blotato, first post verified <date>" note only if something is still open.
   - Commit `tiktok_mirror.py` and push.
9. **Do not touch:** the 16 Zepbound/Supplements shorts, the spray-tan shorts, or the ab-wheel shorts — those are parked on unpublished parent long-forms (coordination file). Only the videos already in the Blotato queue go to TikTok.

## Things to Avoid / Lessons Learned

- **`PATCH /v2/schedules/{id}` only honours `scheduledTime`.** Any content-shaped patch returns a 500. Retiming is a patch; recaptioning is create-then-delete. (From `danrosefit_finish_mirror.py`.)
- **Create before delete, always.** A half-finished run should leave a visible duplicate, never a lost post.
- **Blotato 200-post cap** is real and silently blocks creates — the IG gap-fill got stuck on it (coordination file, "IG image gap-fill"). Count before you create.
- **Do not post immediately** as the smoke test; schedule it. An instant public post on a fresh TikTok connection is the pattern most likely to trip review, and it can't be un-sent.
- **Copyright audio:** an earlier TikTok upload was flagged for its music track and the bed was swapped to `organic_flow.mp3` (Pixabay). The queued Shorts use the cleared bed; if any new short is added later, keep to the cleared music library.
- **Don't add TikTok to the ManyChat or IG auto-first-comment logic** — those are Instagram-only.
- The `blotato_list_schedules` MCP tool returns a 75 KB page and paginates at 50; use the Python `fetch_schedules()` helper instead for anything that needs the whole queue.

## Relevant Files & Locations

- `scripts/blotato/danrosefit_migration.py` — helpers (`api_key`, `call`, `fetch_schedules`, `content_key`, `rewrite_cta`)
- `scripts/blotato/danrosefit_finish_mirror.py` — the mirror pattern to copy
- `scripts/blotato/iggap_fill.py` — example of a `--apply` idempotent scheduler
- `Business/blotato-api-key.txt` — API key (gitignored; never print it)
- `Handoffs/handoff-20260812-instagram-facebook-content-queue.md` — how the IG/FB queue was built, caption conventions, UTM scheme
- `YouTube Long Form Video Content/SHORTS_UPLOAD_PROGRESS.md` — the YouTube Shorts dates (same dates as the IG queue)
- `todos.json` — the three TikTok dashboard rows (use the `/dashboard-tasks` skill, not direct edits)
- Blotato: https://my.blotato.com (Accounts → Add account → TikTok); API base `https://backend.blotato.com/v2`
- Memory: `instagram-account-state`, `shorts-production-style`, `tiktok-ads-account-access` (ads only, unrelated login trap)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking — well-specified API scripting with a template to copy |
| **If Claude usage is high / approaching a limit** | Codex flagship, medium effort — but the Blotato MCP is only wired into Claude Code, so if you want the smoke test done through the MCP rather than raw HTTP, stay on Claude Sonnet 5 |

No always-Claude override: captions are copied and lightly rewritten (UTM swap), not authored.

## Starter Prompt for the Next Task

> I've connected TikTok in Blotato. Execute `Handoffs/handoff-20260902-tiktok-blotato-connect-and-mirror.md`: mirror the 23 queued `@danrosefit` Instagram videos (account 67203) onto the new TikTok account at the same dates/times, videos only, captions with `utm_source=tiktok`, max one per day for the first 7 days. Start by running `blotato_list_accounts` for the TikTok account id and required fields, then count the queue against the 200-post cap (if there's no room, [trim the latest Facebook mirrors / I'll upgrade the plan — pick one]). Build `scripts/blotato/tiktok_mirror.py` on the `danrosefit_finish_mirror.py` pattern, dry-run, smoke-test one scheduled post, then apply. Finish with the dashboard check-offs, the coordination-file update, commit and push.
