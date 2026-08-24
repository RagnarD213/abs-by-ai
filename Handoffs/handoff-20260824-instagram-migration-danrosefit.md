# Handoff: Instagram migration to @danrosefit

**Date:** 2026-08-24
**Project:** Abs By AI
**Business goal this serves:** Marketing — build a presentable personal Instagram with a real
follower count, and make it the account paid traffic grows.

## Objective

Move the Instagram operation off `@abs.by.ai` and onto Dan's personal account, now renamed
`@danrosefit`. Three pieces of work: **(1)** re-point the 194-post Blotato queue to the new account
and perform the queue surgery the audit called for, **(2)** apply the profile fixes that need no
Instagram login, **(3)** produce week one's content under the new weekly slate. `@abs.by.ai` is not
deleted — it becomes a mirror that feeds the main account.

The full audit and plan: **https://claude.ai/code/artifact/3ff338e8-0b44-4132-9cf1-f58b30af2ea9**

## Current State

**The account move is DONE and was executed by Dan on 2026-08-24:**

- `@danrrose` → **`@danrosefit`**. 494 followers, 438 following, 19 posts.
- Switched to a **Creator** professional account.
- Meta Verified paid ($21.31/mo bundle covering this account plus his personal Facebook). ID and
  selfie submitted; 48-hour review, confirmation deadline Thu 2026-08-27. A one-off cloud routine
  (`trig_01KUFtsLkShYKTEwvsAdR2E3`) fires Wed 2026-08-26 18:00 CT to check.
- **Verification has NO bearing on any work in this handoff.** Blotato needs a Professional account,
  which exists. Do not wait on the badge.

**What has NOT been done:**

- **`@danrosefit` is not connected in Blotato.** `blotato_list_accounts` returns only
  `@abs.by.ai` (id `65632`). **This is a hard blocker on step 2 and only Dan can clear it** — it is
  an OAuth login. If his connect attempt errors, the usual cause is the Instagram account not being
  linked to a Facebook Page; link it to the Abs by AI Page and retry.
- Bio, links, profile photo, Highlights, grid archive — all still pending, all need an IG login.
- The 194-post queue still points entirely at `@abs.by.ai` and Facebook.
- No ManyChat account exists yet.

**The audit that drove this** (8 posts, 19–24 Aug, on `@abs.by.ai`): **697 accounts reached, 1 save,
3 shares, 0 profile visits, 0 follows, 0 real comments.** Every `commentsCount: 1` is Blotato's own
auto first-comment, not a human. Reach was never the problem.

## Key Decisions Already Made

Do not reopen these.

- **Consolidate on the personal account.** 494 real followers beat 66 cold ones; Meta Verified for
  creators only works on an account representing a real individual; and it is the strategy from the
  July audit (Dan as the face, an audience that can't be taken from him — the Six Pack Shortcuts
  correction).
- **Creator, not Business.** Instagram's publishing API treats both identically, so Blotato is
  unaffected — that removed the only argument for Business. Creator keeps the **full music library**
  (Business is restricted to commercial-use tracks) and fits Meta Verified's "real individual" rule.
  `@abs.by.ai` stays Business.
- **`@abs.by.ai` is infrastructure, not a content account.** It holds the handle, takes support DMs,
  pairs with the Facebook Page, and is ad-account insurance. **Dan correctly rejected two earlier
  suggestions**: that duplicating was harmful (it isn't — marginal cost through Blotato is zero and
  the redundancy is real insurance), and that it could run product-demo content ("why would anyone
  follow a profile that's just a product demo"). **Settled: mirror the reels there with every CTA
  rewritten to point at `@danrosefit`, so the mirror feeds the main account instead of competing.**
- **Photos leave the Instagram feed.** They averaged 40 views against 130–270 for reels while
  occupying half the weekly slots. They stay on Facebook and become Story fuel.
- **Follow-along reels leave the feed.** Measured 1.8 s and 2.0 s average watch. They suppress
  whatever posts after them. They belong in a Highlight and on YouTube.
- **CTA becomes comment-to-DM** ("Comment ABS and I'll send you the free AI preview") instead of
  "link in the first comment," which spends the only comment slot on a URL and produced zero clicks.
- **Ads: Abs By AI keeps the ad account, budget and Page; `@danrosefit` is the ad IDENTITY.** The
  identity account is the one that receives profile taps and follows. Use "existing post" ads so paid
  engagement accumulates on the real organic post rather than being discarded with the campaign.
- **Name field stays "Daniel Rose."** An earlier recommendation to keyword-load it was reversed —
  Meta Verified requires it to match the government ID.
- **The "AI creator" profile label stays OFF.** It signals his content is AI-generated, feeding the
  exact suspicion the transformation previews already face.
- **TikTok stays disconnected in Blotato until ~2026-09-02** (warm-up). Nothing here touches it.

## Detailed Plan

### Step 0 — Blocker check (do this first)

Run `blotato_list_accounts` with `platform: instagram`. If only `abs.by.ai` (id `65632`) comes back,
**stop and tell Dan to connect `@danrosefit` in Blotato.** Steps 2–4 cannot run without it. Steps 1
and 5 can proceed regardless.

### Step 1 — Deliver the profile copy (no login needed, ~15 min)

Dan applies these himself; produce them ready to paste.

- **Bio** (139 chars, under the 150 limit):
  ```
  200 lbs at 38. Real six-pack at 40.
  No trainer. No coach. I used AI.
  Ab tactics + fat loss for men 35+.
  See YOUR abs before you have them ↓
  ```
- **Link 1:** `https://absbyai.com/?utm_source=instagram&utm_medium=bio`
- **Link 2:** the YouTube channel.
- **Profile photo:** a face-and-shoulders crop from the pool shoot. The current full-body shot is
  illegible at 40 px AND risks failing Meta Verified's photo-matching check. Produce the crop.
- **Four Highlight covers** in the J2 tactical system (`.claude/skills/coverimage/` has the design
  system): `MY STORY` · `SEE YOUR ABS` · `AB WORKOUTS` · `THE APP`.

**OPEN — archive split.** Recommended: **keep** the physique shots, the "GENERATED MY DREAM BODY,
THEN I BUILT IT" transformation graphic, and the three jiu-jitsu posts; **archive** the family ski
trips, the photo collage, the ziplining, the hot tub, and the group shots. Roughly 19 posts down to
9–10. Two of the archived posts contain children's faces, which is a deliberate reason to archive
them before pointing paid traffic at the account, not just an aesthetic one. Archiving is reversible.
Dan may vary this — take his list if he gives one.

### Step 2 — Re-point the queue to @danrosefit

Use the **REST API**, not MCP — this is ~200 operations and MCP would be ~250 individual tool calls.

- Base `https://backend.blotato.com/v2`, header `blotato-api-key`.
- Key at **`Business/blotato-api-key.txt`** (gitignored; the repo is public). Blotato shows the key
  once — regenerate from Settings → API if lost.
- `GET /v2/schedules` paginates with `cursor`. `DELETE /v2/schedules/<id>` returns 204.
- `POST /v2/posts` takes `{post:{accountId,target,content},scheduledTime}`.
- Media already lives on Blotato's CDN — **reuse the existing `mediaUrls`, do not re-upload.** That
  avoids the rate limit entirely.

For every currently-scheduled Instagram post, create the equivalent on `@danrosefit` and delete the
`@abs.by.ai` original, **except** the reels, which stay on `@abs.by.ai` as the mirror (see step 3).
Facebook posts are untouched.

**Write the script idempotently** — cache `old schedule id → new post id` to disk so a re-run resumes
instead of double-posting. Verify after: total count, no date carrying two posts, zero posts missing
media.

### Step 3 — Queue surgery

1. **Remove all photo posts from the Instagram queue** (both accounts). They stay on Facebook.
2. **Remove the follow-along reels** from the Instagram queue.
3. **De-duplicate.** At least four ideas run twice within a week as both a photo and a reel: milk
   ("not a health food", 11 + 12 Sep), supplements ("3% of your results", 27 Aug + 4 Sep), daily ab
   training (9 + 15 Sep), and photographing food instead of weighing it (26 + 29 Aug). Keep the reel.
4. **Rewrite the CTA** across every remaining post:
   - On `@danrosefit`: `Comment ABS and I'll send you the free AI preview 👇`
   - On `@abs.by.ai` (the mirror): a line pointing at `@danrosefit`, e.g.
     `Full breakdown from @danrosefit 👇`
5. **Turn off Blotato's auto `firstComment`** on Instagram posts once ManyChat is live. **Leave it on
   for Facebook**, where links are clickable.
6. **Preserve the CC-BY attribution** in the `short5_1-minute-workout` captions. It is a live licence
   obligation and must not be dropped in the rewrite.

### Step 4 — Verify

Re-read the queue from the API and assert: every Instagram post targets the right account, no date
carries both a photo and a reel, every post has media, no post is scheduled more than 9 months out
(Blotato rejects those with `code 20011`), and no Instagram caption carries more than **5 hashtags**
(a 6th is hard-rejected).

### Step 5 — Produce week one

Four reels and one carousel, per the weekly slate. Each reel under 30 s with the hook in the first
frame.

| Slot | Format | Job |
|---|---|---|
| Mon | Myth-kill reel, 15–25 s ("stop doing X") | Reach — best-performing shape in the data |
| Tue | AI in action, 20–30 s screen recording | Differentiation — the one thing no competitor has |
| Wed | Carousel, 5–7 slides | Saves — the signal the account has exactly one of |
| Thu | One exercise, one cue, 10–15 s | Utility + a completion rate that lifts the next post |
| Fri | No feed post — Stories and outbound engagement | — |
| Sat | Over-40 / real life, 20–40 s | Identity — currently missing entirely, and it's what converts |
| Sun | Review, recycle the winner to FB and YouTube | — |

Cut the reels from the finished longforms with `/shorts`. Build the carousels with PIL in the J2
system. **The Tuesday slot is the important one** — almost nothing in the existing queue is a screen
recording of the app generating an abs preview, and that is the only asset no competitor can copy.

## Things to Avoid / Lessons Learned

- **Do not re-upload media.** The existing `mediaUrls` are reusable. Blotato's rate limit is real and
  aggressive — roughly 28 uploads then a `429 {"message":"Rate limit exceeded, retry in N seconds"}`.
  Honour the N from the message and space sequential uploads ~1.2 s.
- **Never run two Blotato scripts at once.** Both write the same cache file and the loser's writes
  are lost — this briefly regressed the media map from 124 to 120 entries on 2026-08-18.
- **Instagram hard-caps captions at 5 hashtags.** A 6th is rejected with an error. Not a YouTube
  constraint; Instagram only.
- **Instagram Reels cap at 15 minutes, Facebook Reels at 90 seconds.** Long-form on Facebook must
  omit `mediaType` entirely (a regular video post); only ~60 s Shorts use `mediaType: "reel"`.
- **A feed photo takes no `mediaType`** — it is `reel|story` only. `shareToFeed` is reel-only.
- **Deleting a queued post needs the schedule id** from `blotato_list_posts`, not the
  `postSubmissionId` returned at creation.
- **Do not connect TikTok in Blotato before 2026-09-02.** Early third-party connection risks a bot
  flag on a new account.
- **Dan launches all ad campaigns himself** — standing rule since the 2026-08-09 Google Ads
  suspension. The paid side ships as a spec, never as agent execution.
- **Never use side-by-side before/after imagery in a paid ad.** Meta's health-and-fitness rules
  prohibit it outright, same as the Google policy that caused the suspension. The transformation
  graphic is the strongest organic asset and is unusable in paid.
- **Do not put the app's email-capture screen in any ad or demo.** Standing rule.
- **Never write kettlebell *swings*** — Dan does kettlebell deadlifts and considers swings high risk.
- **Never tell people to stop tracking calories.** The angle is that AI made tracking easy, not
  optional; the opposite undermines the app's own macro feature.
- **Every post must give the viewer a reason to watch.** A clip whose only content is Dan's own
  result is a brag and gets killed — `v6-short1_gained-muscle-in-quarantine` was cut, captioned,
  scheduled and pulled on sight for exactly this.

## Relevant Files & Locations

- Repo: `/Users/danielrose/Documents/Claude/Projects/Abs By AI` (**public — never commit the API key
  or personal photos**)
- Plan artifact: https://claude.ai/code/artifact/3ff338e8-0b44-4132-9cf1-f58b30af2ea9
- Queue history and mechanics: `BLOTATO_QUEUE_PROGRESS.md`
- Coordination entry: `AI_COORDINATION.md` (active task section)
- Blotato API key: `Business/blotato-api-key.txt` (gitignored)
- Caption plan for the photo queue: `photos/finalized social media photos/_blotato-photo-queue-plan.json`
- Skills: `.claude/skills/shorts/`, `.claude/skills/coverimage/`, `.claude/skills/dashboard-tasks/`
- Finished longforms to mine for reels: `claude edited long form content/`
- Exercise demo library (33 finished): `Media/exercise-demos/`
- Blotato UI: `my.blotato.com/queue/schedules` (upcoming posts, with a real player — the calendar
  view shows static thumbnails only)
- Dashboard task: `money::Execute the Instagram growth plan (7 profile fixes + Blotato queue rework)`

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** The Blotato work is well-specified scripted API work against a documented surface; the content work needs brand voice but not deep reasoning. |
| **If Claude usage is high / approaching a limit** | **Split it.** Give the queue re-point and surgery (steps 2–4) to **Codex flagship, medium effort** — it is mechanical, idempotent, verifiable. Keep steps 1 and 5 on **Claude Sonnet 5**. |

**Always-Claude override:** the caption rewrites and all week-one content are brand-voice work and
should stay on Claude regardless of usage. Codex should not write copy in Dan's voice. Sonnet 5 is
sufficient — do not reach for Opus here.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260824-instagram-migration-danrosefit.md` in the Abs By AI project.
>
> Context: we moved the Instagram operation from `@abs.by.ai` (66 followers) to Dan's personal
> account, now renamed `@danrosefit` (494 followers, Creator account). The audit found the old
> account reached 697 people in six days and converted zero of them — no profile visits, no follows,
> one save. The handoff has the full diagnosis and plan.
>
> **First action: run `blotato_list_accounts` with `platform: instagram`.** If `@danrosefit` is not
> in the results, stop and tell Dan he needs to connect it in Blotato — that is an OAuth login only
> he can do, and steps 2–4 are blocked until it exists. Steps 1 and 5 can run regardless, so start
> there if blocked.
>
> If it is connected, work steps 2–4: re-point the queue using the REST API (reuse existing
> `mediaUrls`, do not re-upload), drop the photo posts and follow-along reels from the Instagram
> queue, de-duplicate the four repeated ideas, and rewrite the CTAs — comment-to-DM on
> `@danrosefit`, a redirect to `@danrosefit` on the `@abs.by.ai` mirror. Make the script idempotent
> and verify against the API afterwards.
>
> Read `AI_COORDINATION.md` first, and update it plus the dashboard task when done.
