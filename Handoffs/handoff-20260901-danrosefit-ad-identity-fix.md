# Handoff — Finish the @danrosefit follower campaign (unblock the ad identity)

**Written:** 2026-09-01 (Claude Code, Opus 5)
**Status:** NOT EXECUTED. Draft ad set is in an error state. Nothing live, nothing spending.
**Spend so far:** $0.00 AI generation. No production code, no deploy, no native-retest trigger.

---

## THE ONE-LINE VERSION

A Meta follower campaign is 90% built but blocked because the ad account lacks
ad-running permission on the Facebook Page that @danrosefit is linked to — and
because a previous session (mine) left **two duplicate Pages** behind. Delete one,
fix the permission, set two dropdowns, pick two posts, publish.

---

## ⚠ READ THIS FIRST — THE DUPLICATE PAGE IS THE TRAP

There are **TWO Facebook Pages named "Daniel Rose Fitness"** in the portfolio.
They are NOT interchangeable. Getting them mixed up is how this stays broken.

| | Page ID | How it was made | Instagram linked? | Keep? |
|---|---|---|---|---|
| **#1 (red "D" avatar)** | `1380236418500031` (public URL `profile.php?id=61593725683658`) | facebook.com/pages/creation, outside the portfolio | ✅ **YES — @danrosefit is linked to this one** | **KEEP** |
| #2 (grey person avatar) | asset id `61593951123927` | Business Settings → Pages → Add → Create new | ❌ no | **DELETE** |

**Why both exist:** on 8/31 Business Settings refused to import Page #1
("Only people with full control access of the Page can add it into this business
portfolio") — twice, including after a 40s wait. So I created Page #2 inside the
portfolio instead. **Page #1 has since appeared in the portfolio on its own**, so
that refusal was temporary/propagation. Dan then linked Instagram to Page #1 (both
Pages show identical names in Instagram's picker, so he had no way to tell them apart).

**Lesson worth keeping:** create Pages from **Business Settings → Pages → Add →
Create a new Facebook Page**, never from facebook.com/pages/creation. And if an
"add existing Page" fails, wait and retry rather than creating a second one.

---

## KEY IDs

```
Business portfolio   1750995772698195   (Abs by AI - Daniel Rose)
Ad account           2143998876461525   (asset id 120250271103060682)
Campaign             120250711730650682 ([DAN] [ENGAGEMENT] IG GEO — the one marked "In draft")
Ad set               120250711730660682 (New Engagement Ad Set)
@danrosefit          IG 17841401601139982   business asset 1337229942796165
@abs.by.ai           IG 17841436713703364   business asset 1197916060081804
Page "Abs by AI"     1294282227094660
Page "Daniel Rose Fitness" #1 (KEEP)   1380236418500031
Page "Daniel Rose Fitness" #2 (DELETE) 61593951123927
```

⚠ There are **two campaigns named `[DAN] [ENGAGEMENT] IG GEO`**. The one to work on is
the one showing **In draft**; the other is Off with $42.45 historical spend. Don't touch that one.

Direct link to the ad set editor:
```
https://adsmanager.facebook.com/adsmanager/manage/adsets/edit/standalone?act=2143998876461525&business_id=1750995772698195&selected_campaign_ids=120250711730650682&selected_adset_ids=120250711730660682
```

---

## WHAT IS ALREADY DONE (verify, don't redo)

- ✅ **Placements are Instagram-only** and correct: IG Feed, profile feed, Explore home,
  Stories, Reels, IG search results. Facebook / Audience Network / Messenger / WhatsApp /
  Threads all off. Facebook search results off.
- ✅ **@danrosefit added to the business portfolio** (it was never there before — that
  was the original cause of it not appearing anywhere).
- ✅ **@danrosefit connected to the ad account.**
- ✅ **@danrosefit linked to Page #1** — verified in Business Settings → Instagram accounts
  → @danrosefit → Connected assets, which now reads **2 assets: Facebook Page "Daniel Rose
  Fitness" + Ad account "Abs by AI"**. Dan did this in the Instagram app
  (Settings → Account type and tools → Other → Connect to Facebook → Change or create Page).
- ✅ **Page #1 and Page #2 are both in the portfolio.**

## WHAT IS BROKEN RIGHT NOW

- ❌ **Ad set has "Review 1 error":** *"Insufficient Page Permission to Run Ads: You need
  access to create ads for this Page. Send a request for access to someone with full
  control of the Page, or select a different Page if available. (#1487202)"*
  This appeared when Identity was set to **danrosefit**.
- ❌ **Performance goal drifted** from "Maximize number of Instagram profile visits" to
  **"Maximize number of Facebook Page visits"** — Meta auto-changed it when Identity moved
  off the Abs by AI Page. Must be set back.
- ❌ **Destination still only offers @abs.by.ai.** It did NOT pick up @danrosefit even after
  full reloads, ~20 min after the Instagram link was made. May be propagation; may be
  downstream of the permission error.
- ⚠ Ads Manager shows **"Review and publish (6)"** — six pending draft changes.

---

## THE PLAN

### Step 1 — Delete the duplicate Page #2 (`61593951123927`)
Business Settings → Pages → select the **grey-avatar** "Daniel Rose Fitness" → confirm it is
asset `61593951123927` and that its Connected assets show **no Instagram account** → remove/delete.
⚠ **Confirm the ID before deleting.** Deleting Page #1 would undo Dan's Instagram work and
force him back into the app.

### Step 2 — Give the ad account permission to run ads for Page #1
This is the actual blocker. Things already tried that do NOT work:
- Page → **Connect assets** only offers "Instagram account" (no ad account option).
- Ad account detail view has **no Connect assets button** at all (only Assign people / Assign partner).

Untried and most likely to work, in order:
1. **Business Settings → Pages → Daniel Rose Fitness (#1) → Assign people → add
   "Abs by AI Daniel Rose" with full control.** Page #1 currently lists only "Daniel Rose".
   By contrast the working Abs by AI Page lists **two** users ("Conversions API System User"
   and "Daniel Rose"), and the ad account lists **"Abs by AI Daniel Rose (You)"** and
   "Daniel Rose". That asymmetry is the strongest lead — the identity the ad account runs
   under is not assigned to the new Page.
2. Facebook Page → Settings → **Page access** → add the business/ad account.
3. Business asset groups — put Page #1 + the ad account + @danrosefit in one group.

### Step 3 — Set the ad set correctly
In the ad set editor:
- **Identity → Facebook Page → "Daniel Rose Fitness"** (Page #1). If Ads Manager offers
  **danrosefit** directly, that is also acceptable — but only once Step 2 clears the error.
- **Performance goal → "Maximize number of Instagram profile visits."** Do not leave it on
  Facebook Page visits; that optimises for the wrong thing entirely.
- **Destination → tick Instagram profile @danrosefit**, untick the Facebook Page.
  If @danrosefit still does not appear after Step 2, wait and reload — Meta's asset caching
  ran 20+ min behind during this session.

### Step 4 — Verify the settings that were configured but never re-checked
- **"Allow limited spending to excluded placements"** (under Placements → Show more settings)
  must be **UNCHECKED**. It was found checked and set to leak ~5% of budget to each of 3
  excluded placements (~15% of spend into Facebook inventory). Dan was asked to uncheck it;
  never confirmed.
- **Audience:** men, 25–54, locations **US / CA / UK / IE / AU / NZ only**. Was recommended,
  never verified as applied. Estimated audience last read 55.2M–64.9M.
- Budget $10/day.
- ⚠ Do **not** click "Apply now" on the campaign-score card ("Expand your placements… Turn on
  Advantage+ Placements"). That reverts the Instagram-only placement work. A score of 76 vs
  100 is expected and fine — the score measures conformity to Meta's defaults, not fit to goal.

### Step 5 — Pick the posts (measured, not guessed)
@danrosefit has exactly five published posts. Pulled from Blotato analytics 2026-09-01:

| Post | Reach | Avg watch | Interactions |
|---|---|---|---|
| **"I was 200 lbs at 38" (channel intro reel)** | 269 | 15.1s | 26 |
| **3-minute total body workout** (`DcqrXotjlsk`) | 92 | **18.2s** | 12 |
| Supplements are only 3% | 195 | 11.5s | 7 |
| Towel back workout (photo) | 104 | — | 13 |
| Food scale / just a photo | 158 | **3.4s** | 1 |

**Use the channel-intro reel as the primary** — it is the only creative that argues for
following the account ("that is what this account is"), and it has the widest reach and most
interactions. **Add the 3-minute total body workout as a second ad** in the same ad set; best
watch time in the set. **Skip the food-scale reel** (3.4s average watch would poison the
retargeting pool).

⚠ **All five posts end with "Comment ABS and I'll send you the free AI preview 👇" and
ManyChat is still not live**, so that DM never arrives. **Edit the caption on whichever posts
get boosted** — replace that line with `AbsByAI.com`. Free, takes a minute, and the ad picks
up the edited caption.

### Step 6 — Publish, then check back
Kill criteria from the original plan: after **$50** of spend, check cost per follow.
**Kill at >$5/follow; scale at <$3/follow.**

---

## ⚠ OPEN QUESTION FOR DAN — ASK BEFORE EXECUTING

This campaign is **$10/day** and buys roughly **$1.50–3.00 per follower**. Unblocking it has
already consumed most of two sessions. **Ask Dan whether he still wants the full two-step
funnel, or just the simplest thing that runs.** A legitimate cheaper answer: run the
engagement campaign from **@abs.by.ai** (works today, zero further setup) and accept that
follows accrue to the mirror account — then revisit the @danrosefit identity later. He may
also reasonably decide the Google Ads side is the better use of the same effort.

Do not assume the answer. It is a real fork.

---

## OTHER THINGS FOUND, NOT BLOCKING

- **Meta Verified is a bundle covering @danrosefit + Dan's personal Facebook profile
  ($21.31/mo).** It depends on both being in the same Accounts Center. **Never remove
  @danrosefit from Accounts Center** — that is a different setting from the professional
  Page connection and could cost the verification. This was flagged to Dan and avoided.
- **BecomeSharp is settled — do not re-chase it.** It is its own separate portfolio
  (`1351301711643094`), not inside Abs by AI. Restricted ad account cannot be deleted or
  detached. **Dan's call 2026-08-31: leave it alone.**
- Dan manages four live Pages: Abs by AI, SixPackAbs.com, BecomeSharp, Daniel Rose Fitness
  (plus a deactivated Social Response Marketing). ⚠ **Never use SixPackAbs.com as an ad
  identity** — live federal trademark on SIXPACKABS.COM held by another company.
- **Instagram's Page-connection setting does not exist on web.** Only the mobile app:
  Settings → Account type and tools → Other → Connect to Facebook. The web
  Professional-account page carries only category/email/WhatsApp/phone. Don't waste time
  looking for it on desktop.
- The two pre-existing Meta campaigns are both toggled **OFF**, and there were 3 unpublished
  draft edits pending as of 8/31. Worth confirming that was intentional.

---

## STARTER PROMPT (paste into a fresh session)

```
Execute Handoffs/handoff-20260901-danrosefit-ad-identity-fix.md.

Context: a Meta follower campaign for @danrosefit is 90% built but the draft ad set
is erroring with "Insufficient Page Permission to Run Ads". Two duplicate Facebook
Pages named "Daniel Rose Fitness" exist and only one is linked to Instagram — read
the handoff's duplicate-Page table before touching anything.

Work in Dan's real Chrome (claude-in-chrome tools); Business Suite and Ads Manager
are already logged in. Everything is a draft — nothing is live or spending.

START by asking Dan the open question in the handoff: does he still want the full
two-step funnel, or the simplest thing that runs? Then execute Steps 1-6.
```

**Recommended runner: Opus 5, default (high) effort.** This is fiddly Meta UI work with
several near-identical assets and one genuinely destructive step (deleting a Page), so it
needs care rather than speed. Not a good fit for a cheaper model.
