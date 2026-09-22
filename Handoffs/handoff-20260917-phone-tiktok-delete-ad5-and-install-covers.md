# HANDOFF — Phone session: delete the Ad 5 TikTok post, then install 2 TikTok covers

**Written 2026-09-17. Everything here is done on Dan's iPhone through iPhone Mirroring.**
Dan fires this when he has walked away from both the computer and the phone.

Two unrelated jobs, both phone-only, batched into one session because both need the TikTok app:

| # | Job | Deadline |
|---|---|---|
| A | **Delete** the Ad 5 TikTok post (an ad that went out organically by mistake) | none — do it first |
| B | **Install a cover** on 2 published TikToks | Sep 19 and Sep 22, 22:00 UTC — hard |

---

## Before you touch the phone

**iPhone Mirroring mechanics** (memory `iphone-mirroring-control`, verified 2026-09-01):

1. `ToolSearch` query `computer-use`, `max_results: 30` — load the whole toolkit in one call.
2. `request_access` for **iPhone Mirroring**. It is granted at the FULL tier, so taps and typing work.
3. `open_application` → `switch_display`. The window usually sits on the second monitor (`C32F391 (1)`).
4. Drive it with `computer_batch`. `switch_display auto` when finished.

**Requirements:** the iPhone must be locked and nearby. **Mirroring pauses the moment Dan picks up and
unlocks the phone** — that is why this runs when he has walked away. Face ID, hardware buttons and
passwords still need Dan; none of the steps below need any of those.

**Warn before taking over the desktop** (memory `computer-takeover-frustration`) — but Dan has already
walked away here, so a single line in chat is enough.

---

## Job A — delete the Ad 5 TikTok post

**The post:** https://www.tiktok.com/@absbyai/video/7686132607964269855
Caption opens *"Every diet you've tried failed for the same reason. It isn't willpower."*
Posted 2026-09-16, ~119 views. On the profile grid it is the **2nd tile** (top row, second from left) —
Dan talking in a black tank, no designed cover.

**Why it is being deleted:** it is **Ad 5**, a paid ad, and an ad is never published organically
(`AGENTS.md`, "An AD is never published organically", Dan 2026-09-17). The Facebook post and both
Instagram reels have already been deleted and YouTube is back to unlisted; this TikTok is the last
copy still live. The rule is now enforced in code (`scripts/blotato/ad_guard.py`), so this is cleanup
of the one that got out, not a recurring problem.

**Why it has to be the phone:** TikTok's web Studio **greys out Delete** on anything flagged
"Promotional content". The iPhone app allows it.

**Steps**

1. Open **TikTok** → **Profile**.
2. Tap the post described above. Confirm the caption starts *"Every diet you've tried failed…"*
   **before** doing anything else — deleting is irreversible and there is no undo.
3. Tap the **⋯ / Share** button on the right rail → scroll the bottom row → **Delete**.
4. Confirm.

**Verify:** back on the profile, the tile is gone and the post count has dropped by one
(21 → 20 at the time of writing, but a new post publishes most days — compare against the list you
saw in step 1, not against the number 21).

⚠ **Delete only this one video.** Every other post on the account stays.

---

## Job B — install a cover on 2 published TikToks

> **UPDATE 2026-09-22 (read first, it overrides the tables below).** Job A is already done: the Ad 5
> TikTok `7686132607964269855` no longer resolves. The Sep 12 milk window has closed. Job B is now
> THREE posts, all images already in Photos (match by the words on the image):
>
> | Post | Video id | Image in Photos | Window closes |
> |---|---|---|---|
> | "Train abs every single day." (Sep 15) | `7685885160851590430` | `TIKTOK-COVER-train-abs-every-day.jpg` (9:16) | **2026-09-22 22:00 UTC** (Tue 5 PM CT) |
> | "3 sets of ab wheel rollouts" long-form (Sep 20) | `7687616895175904543` | `TIKTOK-COVER-live-ab-wheel-workout-16x9.jpg` | 2026-09-27 14:01 UTC |
> | "Hundreds of crunches" long-form (Sep 21) | `7688111710657465630` | `TIKTOK-COVER-ultimate-1-minute-ab-workout-16x9.jpg` | 2026-09-28 22:01 UTC |
>
> The two long-forms are 16:9 videos whose cover was squashed sideways by a bug (fixed in
> `scripts/blotato/tiktok_cover.py` on 09-22). Their replacement images are 16:9 on purpose: the
> designed tall cover sits in the middle third, so TikTok's crop preview should need no adjustment
> and the grid tile shows the full headline. Do not crop to the blurred side panels.


### Why this is only 2 posts

TikTok's API has no cover-image field at all — only a timestamp into the video — so every TikTok we
posted fell back to frame 0, which on our Shorts is Dan mid-word under a caption. That is fixed going
forward: **all 21 queued posts were rebuilt on 2026-09-17** so their first frame *is* the designed
cover, and it is **proven live** — the 2026-09-17 22:00 UTC post ("Jelly beans beat soda") published
with its designed "WHY YOU MUST AVOID LIQUID CALORIES" cover on the grid. Background:
`Docs/TIKTOK_COVERS.md`.

**A published video's cover can only be changed within 7 days of posting, and only in the app.** Of the
six published posts that were still in that window this morning, only two can actually be fixed:

| Post | Video id | Cover | Window closes |
|---|---|---|---|
| "Milk is not a health food…" (Sep 12) | `7684771938362838303` | ✅ ready | **2026-09-19 22:00 UTC** (Sat 5 PM CT) |
| "Train abs every single day." (Sep 15) | `7685885160851590430` | ✅ ready | **2026-09-22 22:00 UTC** (Tue 5 PM CT) |
| "Your protein shake…" (Sep 10) | `7684029775345732895` | had a cover | ❌ **window closed 2026-09-17 22:00 UTC** |
| "$17 ab wheel" long-form (Sep 13) | `7685019292215168287` | ❌ none exists | Sep 20 14:01 UTC |
| "You can have abs and still look wide" (Sep 14) | `7685514110699605279` | ❌ none exists | Sep 21 22:00 UTC |

The last two have **no designed cover anywhere** — the ab-wheel long-form was queued with
`"cover": None` and the Sep 14 post is a backfill reel, and backfill entries in
`danrosefit_migration.py` carry no `coverImageUrl`. They are uncovered on **Instagram** too, so this is
not a TikTok-specific regression. Designing covers for them is a separate `/coverimage` job; if Dan
wants it, it has to happen before those dates. **Do not invent a cover in this session.**

### The two images are already on the phone

Imported into Photos on 2026-09-17 at 18:02 CT, so iCloud has had hours to sync. In the camera roll
they are the two most recent additions, both 1080×1920:

| File in Photos | Reads | Goes on |
|---|---|---|
| `TIKTOK-COVER-milk-belly-fat.jpg` | **WHY MILK MAKES YOU GAIN BELLY FAT** | the Sep 12 milk post |
| `TIKTOK-COVER-train-abs-every-day.jpg` | **WHY YOU SHOULD TRAIN ABS EVERY DAY / ONCE YOU'RE ALREADY LEAN** | the Sep 15 train-abs post |

Masters, if they ever need re-importing:
`Short-form video content/covers/posted covers/v3-short3_liquid-calories-milk_cover.png` and
`…/v3-short4_train-abs-every-day_cover.png`. Re-import with
`sips -s format jpeg` then `osascript -e 'tell application "Photos" to import {POSIX file "<jpg>"} skip check duplicates true'`.

**Match them by the words on the image, never by position in the camera roll** — Dan may have taken
photos since.

### Steps, per post

1. TikTok → **Profile** → tap the post.
2. **⋯ / Share** on the right rail → **Edit post**.
3. Tap the cover thumbnail / **Edit cover**.
4. Tap the **Upload** icon → pick the matching image from the camera roll.
5. TikTok shows a crop preview. **The grid tile is a tighter crop than the full frame — check the
   headline text is still fully inside it** before accepting, exactly like the Instagram profile-grid
   check in `/coverimage`. Nudge the crop rather than accepting a cut-off headline.
6. ✓ / **Done**, then ✓ / **Save**.

**Verify:** go back to the profile grid and confirm the tile now shows the designed cover.
The **app caches its own tile for a while** — if it still looks like the old screenshot, check
https://www.tiktok.com/@absbyai in a browser instead, which updates sooner.

⚠ If **Edit post** or **Edit cover** is missing on a post, the 7-day window has closed. Stop on that
post, say so, and do not delete-and-re-upload to get around it — that throws away the post's views,
likes and comments, and it is Dan's call, not the session's.

---

## Done / not done

Report back, plainly:

* Ad 5 post deleted — yes/no.
* Each of the 2 covers — installed / window closed / blocked, and what you saw.
* Whether Dan should commission covers for the Sep 13 and Sep 14 posts before Sep 20 / Sep 21,
  or let them keep the screenshot.

**Nothing in this handoff touches the repo**, so there is no commit, no deploy and no dashboard row to
check off. Update the `DAN'S DECISIONS` line "TikTok covers on 6 published posts" in
`AI_COORDINATION.md` when finished — correct it to what actually happened, or delete it if nothing is
left open — and delete this handoff's rows from `AI_COORDINATION.md` and `Handoffs/README.md`.

**Out of scope** (do not start): the board's separate "Native retest (one phone session)" item. It
needs Dan's app running and his judgement, not an unattended session.

---

## Starter Prompt

> Read `Handoffs/handoff-20260917-phone-tiktok-delete-ad5-and-install-covers.md` and execute it.
> It is a phone-only session driven through iPhone Mirroring — my iPhone is locked and I have walked
> away from both it and the computer, so take over the screen and work straight through.
> Job A: delete the Ad 5 TikTok post `7686132607964269855` (confirm the caption reads "Every diet
> you've tried failed for the same reason" before you delete anything — it is irreversible).
> Job B: install the two designed covers, already in my Photos, on the Sep 12 "milk" and Sep 15
> "train abs" posts, checking the crop preview keeps the headline before you save each one.
> If a post no longer offers Edit post / Edit cover its 7-day window has closed — stop on that post,
> say so, and do NOT delete-and-re-upload to get around it. Report what landed and what didn't.

**Model:** Sonnet 5 or Fable 5.1, medium effort. It is careful UI work with two irreversible moments
(the delete, and each cover save), not a reasoning problem.
