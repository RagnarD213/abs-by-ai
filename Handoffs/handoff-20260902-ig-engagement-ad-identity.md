# Handoff — Finish the @danrosefit IG profile-visits campaign (ONE blocker left: ad identity)

**Written:** 2026-09-02 (Claude Code, Opus 5)
**Status:** Campaign + ad set BUILT and PAUSED. Zero ads attached. Nothing spending. $0.00 AI spend.
**Supersedes:** `Handoffs/handoff-20260901-danrosefit-ad-identity-fix.md` (that doc's draft is dead — see below)

---

## THE ONE-LINE VERSION

Everything is built and paused. The only thing standing between this and launch is that Ads
Manager runs the ad under the **@abs.by.ai** identity while the posts belong to **@danrosefit**,
so Meta refuses to boost them (**#2238052**). Find the Identity control on the ad set, set it to
@danrosefit, attach two posts, unpause.

---

## READ THIS BEFORE TOUCHING ANYTHING

1. **DO NOT click "Review and publish (7)"** in Ads Manager. Those 7 pending draft changes belong
   to the ABANDONED 9/01 campaign. Publishing them republishes the broken draft. Only publish from
   inside the specific new ad's editor.
2. **Unpublished Ads Manager drafts are INVISIBLE to the Marketing API.** This is why the 9/01
   handoff's campaign `120250711730650682` / ad set `120250711730660682` could never be repaired by
   API and had to be rebuilt. Any draft you create in the UI is likewise unreadable by API — don't
   waste time trying to `GET` it.
3. **`promoted_object` is IMMUTABLE after ad set creation.** If the fix requires a different
   promoted object, you must create a NEW ad set. Do not burn calls trying to update it.
4. **Do NOT delete the duplicate Page** without eyeballing it in Business Settings first. See IDs.

---

## WHAT IS BUILT (verify, do not rebuild)

```
Campaign   120250753198730682   [DAN] [TRAFFIC] IG PROFILE VISITS - danrosefit   OUTCOME_TRAFFIC  PAUSED
Ad set     120250753601020682   IG profile visits - danrosefit v2                PAUSED
```

Ad set settings, all verified by API read-back:

| Setting | Value |
|---|---|
| daily_budget | 1000 ($10.00/day) |
| optimization_goal | `VISIT_INSTAGRAM_PROFILE` |
| destination_type | `INSTAGRAM_PROFILE` |
| billing_event | IMPRESSIONS |
| bid_strategy | LOWEST_COST_WITHOUT_CAP |
| promoted_object | `{"page_id":"1380236418500031"}` |
| publisher_platforms | `["instagram"]` — Facebook inventory impossible |
| instagram_positions | stream, story, reels, explore_home, profile_feed, ig_search |
| targeting | men, 25–54, US/CA/GB/IE/AU/NZ, home+recent |
| advantage_audience | **0 (off)** |

The 9/01 handoff's Step 4 worries are structurally solved: with `publisher_platforms:["instagram"]`
there are no excluded placements, so the ~15% budget-leak checkbox cannot exist, and Advantage+
placements cannot silently revert what was never set.

---

## THE BLOCKER

Attaching the @danrosefit reel to an ad produces:

> **Instagram user cannot boost this instagram media: Instagram user selected in the ad is not the
> creator of the instagram media. Please change the user to be the creator of the media or change
> the media in the ad (#2238052)**

The ad preview renders as **abs.by.ai**. The posts belong to **@danrosefit**. That mismatch is the
whole problem.

### What was tried and FAILED (do not repeat)

| Attempt | Result |
|---|---|
| `POST /{adset}` with `promoted_object.instagram_profile_id` | "promoted object is immutable" |
| `POST /{adset}` with `promoted_object.instagram_actor_id` | same |
| `promoted_object.instagram_account_id` | "Invalid keys" |
| CREATE ad set with `promoted_object.instagram_profile_id` | **Accepted, then silently discarded** — read-back shows page_id only |
| `POST /adcreatives` `object_story_spec{instagram_user_id,page_id}` + `source_instagram_media_id` | "The link field is required" |
| same + top-level `link` | "The link field is required" |
| same + `call_to_action` in spec | "The link field is required" |
| same + `video_data.call_to_action` | "Please choose a video for your ad" |
| same + `link_data.link` | "object you are trying to promote is ambiguous" |
| `object_story_spec` without `page_id` | "Select a Facebook Page to represent your business" |
| Ads Manager → ad-level "Review defaults" panel | Advantage+ enhancements only, no identity |

### Where the answer most likely is (UNTRIED — start here)

**The ad set editor's Identity section in the Ads Manager UI.** The 9/01 handoff explicitly
describes it ("Identity → Facebook Page", "Destination → tick Instagram profile @danrosefit"), so it
exists for this objective. It was NOT reached this session — the session was stopped on the way to:

```
https://adsmanager.facebook.com/adsmanager/manage/adsets/edit/standalone?act=2143998876461525&business_id=1750995772698195&selected_adset_ids=120250753601020682
```

Set **Identity → Instagram account → danrosefit** there. If the UI writes a field the API refused,
capture what it did (the ad set becomes API-readable once published) so the API path is known next time.

Secondary theory if that fails: the ad account's DEFAULT Instagram identity is @abs.by.ai and is
overriding. Check Business Settings → Ad accounts → Abs by AI → connected Instagram accounts.

---

## THE POSTS TO BOOST (already resolved — do not re-derive)

Instagram media V2 IDs, pulled live from `GET /17841401601139982/media`:

```
18188183254395331   channel-intro reel  "I was 200 lbs at 38..."   Aug 25   32 likes, 3 comments
18192762022391478   3-min total body     "A three-minute total..."  Aug 30    8 likes, 2 comments
```

Primary = the channel-intro reel (only creative that argues for FOLLOWING the account; widest reach).
Second = 3-min total body (best watch time, 18.2s). **Skip the food-scale reel** (3.4s avg watch).

⚠ **MUST be these existing posts, not fresh uploads.** Dan was explicit. The ManyChat "Comment ABS"
automation listens on the comment threads of the real posts; a fresh upload has no threads, so the
funnel does not exist on it and the spend is wasted. This session wrongly substituted uploads and
was corrected.

⚠ The 9/01 handoff says to strip "Comment ABS" from boosted captions because ManyChat wasn't live.
**That is now OBSOLETE — ManyChat IS live. Leave the captions alone.**

---

## CREDENTIALS AND APP STATE (all working — do not redo)

`~/.absbyai-secrets.env` (0600):
- `META_ADS_TOKEN` — system user `abs-automation`, **never expires**. Scopes: `ads_management`,
  `ads_read`, `business_management`, `pages_show_list`, `pages_read_engagement`,
  `pages_manage_posts`, `instagram_basic`.
- `META_APP_SECRET` — app `1598463548528030`.

⚠ **The Business Settings "Generate token" UI SILENTLY FAILS for ads scopes** — it bounces to the
regular screen with no error, even though Dan IS an app Administrator (the "you are not an admin of
this app" warning it displays is simply wrong). **Mint tokens via API instead:**

```bash
SU=122096883771469881; APP=1598463548528030
PROOF=$(python3 -c "import hmac,hashlib;print(hmac.new(b'$META_APP_SECRET',b'$META_ADS_TOKEN',hashlib.sha256).hexdigest())")
curl -s -X POST "https://graph.facebook.com/v21.0/$SU/access_tokens" \
  -d "business_app=$APP" -d "scope=ads_management,ads_read,business_management,instagram_basic,..." \
  -d "appsecret_proof=$PROOF" -d "access_token=$META_ADS_TOKEN"
```

App use cases added this session (all saved): **Marketing API** ("Create & manage ads with Marketing
API" — NOT the "Meta Ads Manager" one, which explicitly excludes API access) and **Instagram API**,
with "Add required content permissions" clicked under **API setup with Facebook login** (that is the
variant that grants `instagram_basic` to a Facebook system-user token; the Instagram-Login variant
does NOT).

⚠ **The app is still in DEVELOPMENT mode ("Unpublished").** Creating an ad creative from a NEW upload
fails with "Ads creative post was created by an app that is in development mode." Boosting an
EXISTING post did not hit this error, so publishing may not be needed — but if it is:
App settings → Basic needs Privacy `https://absbyai.com/privacy`, Terms `https://absbyai.com/terms`,
domain `absbyai.com`, a Category, then toggle Live. **Meta blocks app-settings writes via API**
("Changing app settings through API calls has been disabled for this app"), so that is UI-only.

---

## KEY IDs

```
Business portfolio      1750995772698195
Ad account              act_2143998876461525   (active, $96.64 lifetime spend)
System user             61594096438582  / app-scoped 122096883771469881
App                     1598463548528030
@danrosefit  IG user    17841401601139982      (business asset 1337229942796165)
@abs.by.ai   IG user    17841436713703364
Page "Daniel Rose Fitness"  KEEP      1380236418500031   (red "D" avatar)
Page "Daniel Rose Fitness"  DUPLICATE 1348044195050800   (grey person avatar) — NOT deleted
Page "Abs by AI"                      1294282227094660
```

⚠ **ID CORRECTION to the 9/01 handoff:** it recorded the duplicate as `61593951123927`. That is the
duplicate's **business-asset id**, not its Page id. The Page id is **`1348044195050800`**. Deleting
by the wrong number is exactly how this goes wrong.

⚠ **Do NOT use the API to decide which Page to delete.** `instagram_business_account` and
`connected_instagram_account` read as EMPTY for every Page on this token — including the Abs by AI
page that demonstrably has one. It is a false negative, not an answer. Confirm in Business Settings:
the keeper shows "@danrosefit shares these permissions" and a red "D" avatar.

---

## VERIFIED FACTS (established this session — trust these, don't re-verify)

- ✅ Page permission is **NOT** the blocker any more. Page `1380236418500031` → People shows
  **Daniel Rose: Full access** and **abs-automation: Partial access (Ads and Insights)**.
  The system user was granted `ADVERTISE`+`ANALYZE` via `POST /{page}/assigned_users` (that write
  succeeds even though the matching READ needs `pages_manage_metadata`, which Meta never offered).
- ✅ @danrosefit → Connected assets = Facebook Page "Daniel Rose Fitness" (the keeper) + Ad account
  "Abs by AI". Correct.
- ✅ @danrosefit People = Daniel Rose (full), abs-automation (full).
- ✅ Errors **#1487202** (Insufficient Page Permission) and **#1341012** (no permission to access
  this profile) appeared once and then **CLEARED on reload** — Meta's async validation lagging, not a
  real gap. Do not chase them; if they reappear, reload before believing them.
- ⚠ **IG `explore` placement is DEPRECATED in v21.0** and rejects ad set creation. Use `explore_home`.
- ⚠ Campaign creation now requires `is_adset_budget_sharing_enabled` (set **false**).

---

## MESS LEFT BEHIND (clean up)

- **Orphan draft ad `120250753499300682`** ("danrosefit - channel intro reel") — it belonged to ad set
  `120250753200250682`, which was DELETED. Discard this draft rather than editing it.
- **Two unused videos in the ad account video library**, uploaded during the wrong-turn attempt at
  fresh-upload creatives: `1786872992455194`, `1845227913307673`. **They cannot be deleted via API**
  ("Application does not have permission"). Inert, no spend, no visibility. Delete in Ads Manager →
  Media Library if it bothers Dan.
- **7 pending draft changes** in Ads Manager from the abandoned 9/01 campaign. Leave them or discard
  deliberately — but never bulk-publish them.

---

## STEPS

1. Discard orphan draft ad `120250753499300682`.
2. Open the ad set editor for `120250753601020682` and set **Identity → Instagram account →
   danrosefit**. Save.
3. Create an ad in that ad set → **Use existing posts** → add media `18188183254395331`.
   Confirm error #2238052 is gone and the preview renders as **danrosefit**, not abs.by.ai.
4. Create a second ad in the same ad set for media `18192762022391478`.
5. Publish both ads **from inside the ad editor** (never the global "Review and publish").
6. Leave the campaign and ad set **PAUSED**. Report to Dan and let him unpause — he has not approved
   spend starting.
7. Kill criteria for when it does run: after **$50** spend, check cost per follow.
   **Kill >$5/follow, scale <$3/follow.**
8. Check off the dashboard Key task for this handoff.

---

## STILL OPEN, NOT PART OF THIS TASK

- The duplicate Page `1348044195050800` is not deleted. Irreversible; Dan's call, UI only.
- `ads_read` is now live, so **the morning ads digest can finally read Meta**. Untested. Run
  `scripts/ads/ads-digest.js` and confirm the Meta section populates — it has been reporting blind
  daily for exactly this missing credential.

---

## STARTER PROMPT (paste into a fresh session)

```
Execute Handoffs/handoff-20260902-ig-engagement-ad-identity.md.

The @danrosefit Instagram profile-visits campaign is fully built and paused. Exactly one
thing blocks it: Ads Manager runs the ad under the @abs.by.ai identity while the posts
belong to @danrosefit, so Meta refuses to boost them (#2238052).

Read the handoff's "What was tried and FAILED" table BEFORE making any API call — eleven
approaches are already ruled out and repeating them wastes the session. The untried lead is
the Identity control in the ad set editor UI.

Work in Dan's real Chrome (claude-in-chrome). META_ADS_TOKEN and META_APP_SECRET are in
~/.absbyai-secrets.env and work. Everything is paused; nothing is spending.

Two hard rules: the ads MUST boost the two existing @danrosefit posts (media IDs are in the
handoff) and NOT fresh uploads, because ManyChat listens on those posts' comment threads.
And never click the global "Review and publish (7)" — it would republish an abandoned
broken draft.

Leave the campaign paused when done and report to Dan.
```

**Recommended runner: Fable 5.1, extra-high effort.** This is UI-forward Meta work where the
remaining unknown is where one control lives, and the failure mode is burning a session on API
shapes that are already known not to work. Read first, click second.
