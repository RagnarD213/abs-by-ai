# Handoff: Build the @danrosefit posting queue

**Date:** 2026-08-24 (rev 3)
**Project:** Abs By AI
**Business goal this serves:** Marketing — build a presentable personal Instagram with a real
follower count, and make it the account paid traffic grows.

## Objective

Stand up a Blotato posting queue on `@danrosefit` with **two tracks**:

1. **A sync track** — everything that goes out on YouTube, Facebook and (after 2026-09-02) TikTok
   also goes out on `@danrosefit` at the same time. One piece of content, one moment, every platform.
2. **A backfill track** — the content already published on `@abs.by.ai` gets reposted to
   `@danrosefit` gradually, **only on days the sync track is idle**, so somebody following both
   accounts never gets the same thing twice in one scroll.

`@danrosefit` always posts **first**. The `@abs.by.ai` mirror runs **one day behind**.

Plus the queue surgery the audit called for, the profile copy Dan applies himself, and week one's
new content.

Full audit and plan: **https://claude.ai/code/artifact/3ff338e8-0b44-4132-9cf1-f58b30af2ea9**

## Current State

**The account move is DONE.** `@danrrose` → `@danrosefit`, switched to a Creator professional
account, Meta Verified paid and submitted. 494 followers, 438 following, 19 posts. Nothing in this
handoff waits on the verification badge — Blotato needs a Professional account, which exists.

**Blotato workspace as of 2026-08-24** (`blotato_list_accounts`):

| Platform | id | Account |
|---|---|---|
| Facebook | `47105` | Page "Abs by AI" (`pageId` `1294282227094660`) |
| YouTube | `46963` | Abs by AI |
| Instagram | `65632` | `abs.by.ai` |

**`@danrosefit` is NOT in that list.** Owning the Instagram handle and connecting it to Blotato are
two different things, and only the first is done. Connecting is an OAuth login **Dan must do** —
Blotato → Settings → Social accounts → add Instagram, signing in with the Instagram credentials
rather than through Facebook. If it errors, the usual cause is the Instagram account not being linked
to a Facebook Page; link it to the Abs by AI Page and retry.

**Existing queue:** 194 scheduled posts through Jan 2027 — 130 photo, 54 reel, 10 video — all
targeting `@abs.by.ai` and Facebook. Reels run Tue/Thu/Sat 5:00 PM CT (mirroring the YouTube Shorts
dates exactly). Photos run Mon/Wed/Fri 5:00 PM CT. Long-form runs 9:00 AM CT on its own days.

**Backfill inventory — 10 published posts, 9 unique.** Everything Blotato has ever published to
`@abs.by.ai`:

| Published | Content | Type | Views | Backfill? |
|---|---|---|---|---|
| Aug 22 | The trick that killed my night snacking | Reel | 267 | **Yes — best performer** |
| Aug 20 | Do this instead of crunches | Reel | 129 | **Yes** |
| Aug 19 | What this channel is going to teach you | Reel | 89 | **Yes — 26.3 s avg watch** |
| Aug 21 | All four ab muscle groups | Reel | 37 | **Yes** |
| Aug 23 | 1-minute ab workout, follow-along | Reel | 126 | No — 1.8 s watch |
| Aug 20 | Full 1-minute ab workout, follow-along | Reel | 122 | No — 2.0 s watch |
| Aug 20 | Full 1-minute ab workout (**duplicate**, posted 19:54 *and* 20:42) | Reel | — | No |
| Aug 24 | Do this instead of crunches | Photo | — | Story only |
| Aug 21 | I don't eat until 2pm | Photo | 37 | Story only |
| Aug 19 | Stop doing ab exercises | Photo | 43 | Story only |

**So the backfill is 4 reels, not a library.** At two a week it runs two weeks. Two posts were also
published to `@abs.by.ai` manually, outside Blotato (an Aug 4 captionless graphic and an Aug 13
jump-rope tip) — Blotato cannot see or repost those, and both were judged not worth recreating.

## Key Decisions Already Made

Do not reopen these.

- **Consolidate on the personal account.** 494 real followers beat 66 cold ones; Meta Verified for
  creators only works on an account representing a real individual; and it is the strategy from the
  July audit (Dan as the face, an audience that can't be taken from him).
- **Creator, not Business.** Instagram's publishing API treats both identically, so Blotato is
  unaffected. Creator keeps the full music library and fits Meta Verified's "real individual" rule.
- **Everything posts at the same time on all platforms.** This is Dan's rule and it drives the sync
  track. The existing Tue/Thu/Sat reel schedule already mirrors YouTube exactly; `@danrosefit` joins
  that spine rather than getting a schedule of its own.
- **The backfill drips onto idle days only.** Dan's constraint, verbatim: repost the old content
  "gradually, over time, not immediately, so I don't annoy people," and "on a day when it's not
  synchronizing with the other content."
- **`@abs.by.ai` is infrastructure, not a content account.** It holds the handle, takes support DMs,
  pairs with the Facebook Page, and is ad-account insurance. It keeps the mirrored reels with every
  CTA rewritten to point at `@danrosefit`, so the mirror feeds the main account.
- **`@danrosefit` posts FIRST; the `@abs.by.ai` mirror runs +1 DAY behind** (Dan's decision,
  2026-08-24), same time-of-day. Two reasons: a dual-follower never gets the same reel twice in one
  scroll, and the mirror's "full breakdown from @danrosefit" CTA is only truthful once that post is
  actually live — which a same-day mirror cannot guarantee.
- **Photos leave the Instagram feed.** They averaged 40 views against 130–270 for reels while
  occupying half the weekly slots. They stay on Facebook and become Story fuel.
- **Follow-along reels leave the feed.** Measured 1.8 s and 2.0 s average watch — they suppress
  whatever posts after them. They belong in a Highlight and on YouTube.
- **CTA becomes comment-to-DM** ("Comment ABS and I'll send you the free AI preview") instead of
  "link in the first comment," which spent the only comment slot on a URL and produced zero clicks.
- **Ads: Abs By AI keeps the ad account, budget and Page; `@danrosefit` is the ad IDENTITY**, because
  the identity account receives the profile taps and follows. Use "existing post" ads.
- **Name field stays "Daniel Rose"** (Meta Verified requires it match the ID) and **the "AI creator"
  label stays OFF** (it signals his content is AI-generated, feeding the exact suspicion the
  transformation previews already face).
- **TikTok stays disconnected in Blotato until ~2026-09-02.** When it comes online it joins the sync
  track with no extra production.

## Detailed Plan

### Step 0 — State check

Run `blotato_list_accounts` with `platform: instagram`. If `@danrosefit` is absent, **steps 2–4 are
blocked** — tell Dan and proceed to steps 1 and 6, which need nothing from Blotato. Capture the new
`accountId` when it appears; every step below needs it.

### Step 1 — Deliver the profile copy (no Blotato needed)

Dan applies these himself; produce them ready to paste.

- **Bio** (139 chars, under the 150 limit):
  ```
  200 lbs at 38. Real six-pack at 40.
  No trainer. No coach. I used AI.
  Ab tactics + fat loss for men 35+.
  See YOUR abs before you have them ↓
  ```
- **Link 1:** `https://absbyai.com/?utm_source=instagram&utm_medium=bio` · **Link 2:** YouTube.
- **Profile photo:** a face-and-shoulders crop from the pool shoot. The current full-body shot is
  illegible at 40 px and risks failing Meta Verified's photo-matching check.
- **Four Highlight covers** in the J2 tactical system (`.claude/skills/coverimage/`):
  `MY STORY` · `SEE YOUR ABS` · `AB WORKOUTS` · `THE APP`.

**OPEN — archive split.** Recommended: **keep** the physique shots, the "GENERATED MY DREAM BODY,
THEN I BUILT IT" transformation graphic, and the three jiu-jitsu posts; **archive** the family ski
trips, the photo collage, the ziplining, the hot tub and the group shots. Roughly 19 posts down to
9–10. Two archived posts contain children's faces, which is a deliberate reason to archive before
pointing paid traffic at the account, not just an aesthetic one. Archiving is reversible and Dan may
vary the list.

### Step 2 — Build the sync track on @danrosefit

Use the **REST API**, not MCP — this is ~200 operations and MCP would be ~250 individual tool calls.

- Base `https://backend.blotato.com/v2`, header `blotato-api-key`.
- Key at **`Business/blotato-api-key.txt`** (gitignored; the repo is public). Shown once — regenerate
  from Settings → API if lost.
- `GET /v2/schedules` paginates with `cursor`. `DELETE /v2/schedules/<id>` returns 204.
- `POST /v2/posts` takes `{post:{accountId,target,content},scheduledTime}`.
- **Reuse the existing `mediaUrls` — do not re-upload.** The media is already on Blotato's CDN, and
  reusing it sidesteps the rate limit entirely.

For every future-scheduled Instagram post, create the `@danrosefit` equivalent **at the identical
`scheduledTime`** so it lands with its YouTube and Facebook siblings. The `@abs.by.ai` original
becomes the mirror and gets shifted **+1 day** in step 4. Facebook and YouTube schedules are
untouched — they stay synchronized with `@danrosefit`.

**Build a manifest first** — one row per piece of content with its scheduled time and its target
accounts across all platforms — and diff it against what actually exists afterwards. That manifest is
what makes "synchronized" checkable rather than assumed.

### Step 3 — Build the backfill track

Take the **4 reels** in the backfill table above, best-performing first (night snacking → crunches →
channel intro → four ab muscles). Seeding the grid with the strongest content first matters, because
the account is thin after archiving and early visitors see the top row.

- **Schedule 2 per week, maximum**, on days the sync track is idle. With reels on Tue/Thu/Sat, that
  means **Monday and Friday**, 5:00 PM CT to match the established slot.
- **Never schedule a backfill post on a day that already carries a sync post** on any platform.
  Assert this in the script, don't eyeball it.
- **Never backfill something already in the future queue.** Check the content against the scheduled
  manifest before adding it — "Do this instead of crunches" appears both as a published Aug 20 reel
  and as a scheduled Aug 24 photo, and those must not collide.
- **Rewrite the caption** rather than reposting verbatim — same idea, fresh opening line, new CTA.
  A word-for-word repost is visible to anyone who saw the original.
- The **3 photos become Story posts**, not feed posts.

When the 4 run out, the backfill track goes quiet. That is fine and expected — it is a two-week
seeding exercise, not a permanent second cadence. Do not invent filler to keep it running.

### Step 4 — Queue surgery

1. **Remove all photo posts from the Instagram queue** (both accounts). They stay on Facebook.
2. **Remove the follow-along reels** from the Instagram queue.
3. **De-duplicate.** Four ideas run twice within a week as both a photo and a reel: milk (11 + 12
   Sep), supplements (27 Aug + 4 Sep), daily ab training (9 + 15 Sep), photographing food (26 + 29
   Aug). Keep the reel.
4. **Rewrite the CTA** across every remaining post:
   - `@danrosefit`: `Comment ABS and I'll send you the free AI preview 👇`
   - `@abs.by.ai` mirror: `Full breakdown from @danrosefit 👇`
5. **Turn off Blotato's auto `firstComment`** on Instagram once ManyChat is live. **Leave it on for
   Facebook**, where links are clickable.
6. **Preserve the CC-BY attribution** in the `short5_1-minute-workout` captions — a live licence
   obligation that must survive the rewrite.

7. **Stagger the `@abs.by.ai` mirror by +1 day.** DECIDED by Dan 2026-08-24 — this is no longer an
   open question. Shift every remaining `@abs.by.ai` Instagram post **one day later, keeping its
   time-of-day** (so a 5:00 PM reel mirrors at 5:00 PM the next day, and a 9:00 AM long-form mirrors
   at 9:00 AM the next day). `@danrosefit` always goes first.

   Prefer updating the existing schedule in place (`blotato_update_schedule`, or the REST equivalent
   against the schedule id) over delete-and-recreate — it is one call instead of two and cannot
   half-fail into a lost post. Fall back to delete + recreate only if an in-place time change is
   rejected.

   Two consequences to handle: the queue's tail moves from 2026-01-15 to 2026-01-16, which is still
   comfortably inside Blotato's 9-month limit; and Facebook is **not** shifted — it stays synchronized
   with `@danrosefit`, because the stagger exists to protect people following both *Instagram*
   accounts, not to desynchronize platforms.

### Step 5 — Verify

Re-read the queue from the API and assert, in the script:

- Every Instagram post targets the intended account.
- **Every sync-track post shares its `scheduledTime` with its YouTube/Facebook sibling** (this is the
  whole point of the track — check it, don't assume it).
- **Every `@abs.by.ai` mirror post is exactly 24 hours after its `@danrosefit` original**, same
  time-of-day, and never earlier. If any mirror lands before or on the same day as its original, the
  stagger has failed and the CTA it carries is a lie.
- No day carries both a sync post and a backfill post.
- No day carries both a photo and a reel.
- Every post has media, and no post is scheduled more than 9 months out (`code 20011`).
- No Instagram caption carries more than **5 hashtags** — a 6th is hard-rejected.

### Step 6 — Produce week one

Four reels and one carousel. Each reel under 30 s with the hook in the first frame. Everything
produced here joins the **sync track** — it posts to YouTube, Facebook and Instagram together.

| Slot | Format | Job |
|---|---|---|
| Mon | Myth-kill reel, 15–25 s ("stop doing X") | Reach — best-performing shape in the data |
| Tue | AI in action, 20–30 s screen recording | Differentiation — the one thing no competitor has |
| Wed | Carousel, 5–7 slides | Saves — the signal the account has exactly one of |
| Thu | One exercise, one cue, 10–15 s | Utility, plus a completion rate that lifts the next post |
| Fri | No feed post — Stories and outbound engagement | — |
| Sat | Over-40 / real life, 20–40 s | Identity — currently missing, and it's what converts |
| Sun | Review, recycle the winner to FB and YouTube | — |

Note this slate wants Mon and Fri for new content, while the backfill temporarily occupies them.
**The backfill yields** — it is two weeks of seeding and new content outranks it.

Cut reels from the finished longforms with `/shorts`. Build carousels with PIL in the J2 system.
**The Tuesday slot is the important one** — almost nothing in the existing queue is a screen recording
of the app generating an abs preview, and that is the only asset no competitor can copy.

## Things to Avoid / Lessons Learned

- **Do not re-upload media.** Existing `mediaUrls` are reusable. The rate limit is real — roughly 28
  uploads then `429 {"message":"Rate limit exceeded, retry in N seconds"}`. Honour the N and space
  sequential uploads ~1.2 s.
- **Never run two Blotato scripts at once.** Both write the same cache file and the loser's writes
  are lost — this regressed the media map from 124 to 120 entries on 2026-08-18.
- **Make every script idempotent** (cache `old id → new id` to disk) so a re-run resumes instead of
  double-posting. Blotato has already double-posted once by accident: "The full 1-minute ab workout"
  went out twice on Aug 20, 48 minutes apart.
- **Instagram hard-caps captions at 5 hashtags.** Instagram only, not YouTube.
- **Instagram Reels cap at 15 minutes, Facebook Reels at 90 seconds.** Long-form on Facebook must
  omit `mediaType` entirely; only ~60 s Shorts use `mediaType: "reel"`.
- **A feed photo takes no `mediaType`** — it is `reel|story` only. `shareToFeed` is reel-only.
- **Deleting a queued post needs the schedule id** from `blotato_list_posts`, not the
  `postSubmissionId` returned at creation.
- **Do not connect TikTok before 2026-09-02.**
- **Dan launches all ad campaigns himself** — standing rule since the 2026-08-09 Google Ads
  suspension. The paid side ships as a spec, never as agent execution.
- **Never use side-by-side before/after imagery in a paid ad.** Meta's health-and-fitness rules
  prohibit it, same as the Google policy that caused the suspension.
- **Do not show the app's email-capture screen in any ad or demo.**
- **Never write kettlebell *swings*** — Dan does kettlebell deadlifts and considers swings high risk.
- **Never tell people to stop tracking calories.** The angle is that AI made tracking easy, not
  optional; the opposite undermines the app's own macro feature.
- **Every post must give the viewer a reason to watch.** A clip whose only content is Dan's own
  result is a brag and gets killed.

## Relevant Files & Locations

- Repo: `/Users/danielrose/Documents/Claude/Projects/Abs By AI` (**public — never commit the API key
  or personal photos**)
- Plan artifact: https://claude.ai/code/artifact/3ff338e8-0b44-4132-9cf1-f58b30af2ea9
- Queue history and mechanics: `BLOTATO_QUEUE_PROGRESS.md`
- Coordination entry: `AI_COORDINATION.md`
- Blotato API key: `Business/blotato-api-key.txt` (gitignored)
- Photo caption plan: `photos/finalized social media photos/_blotato-photo-queue-plan.json`
- Skills: `.claude/skills/shorts/`, `.claude/skills/coverimage/`, `.claude/skills/dashboard-tasks/`
- Longforms to mine for reels: `claude edited long form content/`
- Exercise demo library (33 finished): `Media/exercise-demos/`
- Blotato UI: `my.blotato.com/queue/schedules` (real player; the calendar view is static thumbnails)
- Dashboard task: `money::Execute the Instagram growth plan (7 profile fixes + Blotato queue rework)`

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** Well-specified scripted API work against a documented surface, plus content that needs voice rather than deep reasoning. |
| **If Claude usage is high / approaching a limit** | **Split it.** Sync track, backfill and surgery (steps 2–5) → **Codex flagship, medium effort** — mechanical, idempotent, verifiable. Steps 1 and 6 stay on **Claude Sonnet 5**. |

**Always-Claude override:** the caption rewrites (both the CTA pass and the backfill rewrites) and all
week-one content are brand-voice work and stay on Claude regardless of usage. Sonnet 5 is sufficient —
do not reach for Opus.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260824-instagram-migration-danrosefit.md` in the Abs By AI project.
>
> Context: the Instagram operation is moving from `@abs.by.ai` (66 followers) to Dan's personal
> account, now renamed `@danrosefit` (494 followers, Creator, Meta Verified submitted). The audit
> found the old account reached 697 people in six days and converted zero of them. The account rename
> is already done — what is being built here is the **posting queue**.
>
> Two tracks: a **sync track** where every post lands on `@danrosefit` at the same timestamp as its
> YouTube and Facebook siblings, and a **backfill track** that drips the 4 previously-published reels
> onto idle days only (2/week, Mon and Fri), so anyone following both accounts never gets the same
> thing twice in one scroll. `@danrosefit` posts **first**; the `@abs.by.ai` mirror is shifted **+1
> day**, same time-of-day. Facebook is not shifted.
>
> **First action: run `blotato_list_accounts` with `platform: instagram` and capture the
> `@danrosefit` accountId.** If it is absent, steps 2–5 are blocked on Dan doing the OAuth connection
> in Blotato — tell him, then do steps 1 and 6, which need nothing from Blotato.
>
> Use the REST API rather than MCP for the queue work, reuse the existing `mediaUrls` rather than
> re-uploading, make the script idempotent, and verify against the API afterwards — especially that
> every sync-track post shares its timestamp with its siblings, that every `@abs.by.ai` mirror post
> is exactly 24 hours behind its `@danrosefit` original, and that no day carries both a sync post and
> a backfill post.
>
> The only open item is the archive split in step 1, and a recommendation is written in — take Dan's
> list if he gives one, otherwise use the recommendation.
>
> Read `AI_COORDINATION.md` first, and update it plus the dashboard task when done.
