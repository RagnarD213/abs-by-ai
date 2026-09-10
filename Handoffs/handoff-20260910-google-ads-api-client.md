# Handoff: Google Ads by API — mint the Ads-scope token, prove a call, build the client, retire the paste-a-script channel

**Date:** 2026-09-10
**Project:** Abs By AI
**Business goal this serves:** marketing performance (every Google Ads change becomes a minute of API work instead of an hour of driving the Ads UI or pasting scripts), and Dan's time.

## Objective

Make direct Google Ads API calls the normal way this project reads and changes account **342-717-0837**. Access is
already granted: the Google Ads API is enabled on Cloud project **`abs-by-ai`** (project number 768453214640, the
project whose OAuth client is stored as `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`) and the project holds
**Explorer** access (2,880 production operations/day, campaign management + reporting). What is missing is a refresh
token that carries the Ads scope, one proven call, a small reusable client module, and the first jobs run through it.

## Current State

- **Access:** Google retired the developer-token form. The MCC's API center
  (`ads.google.com/aw/apicenter?ocid=364714550`) now serves only the App Conversion Tracking API and says Google Ads
  API access is managed in Cloud Console. On 2026-09-10 the API was enabled and Explorer access applied for and
  granted within ~2 minutes at `console.cloud.google.com/google/ads-apis/overview?project=abs-by-ai`. The page
  lists "Basic" as the next level ("more production operations and full API functionality"); Explorer says "some
  API functionality may be restricted". Whether requests still need a `developer-token` header under this model
  is **unknown** — the first call settles it (if required, the token is shown on that same access page).
- **Tokens:** `~/.absbyai-secrets.env` has `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`
  (scope `calendar.readonly` only — useless here) and `YOUTUBE_REFRESH_TOKEN` (`youtube.upload` + readonly). The
  OAuth client's **only registered redirect URI is the OAuth Playground** (`scripts/youtube/upload.js` header
  records the recipe used for the YouTube token). No Ads-scope token exists.
- **Accounts:** client account 342-717-0837 (`customers/3427170837`, `ocid=8444849202`); manager account Daniel
  Rose Marketing MCC 324-458-6445 (`login-customer-id: 3244586445`, `ocid=364714550`).
- **Today's write channel** is a Google Ads Script pasted into Tools → Scripts and run from the editor, with results
  POSTed to `absbyai.com/api/ytads/dump` (header `X-YTADS-Key` = `YTADS_KEY`) and read back from Postgres table
  `ytads_events` (`DATABASE_PUBLIC_URL`). It works but each iteration costs ~2 minutes of driving a UI that
  wedges. The hourly engagement-champion script (`scripts/ads/ytads/ads-script.js`, `Docs/YTADS.md`) also carries a
  **manual mutation queue** (`scripts/ads/ytads/manual.js`, table `ytads_manual`) whose rows only execute on the
  next live hourly run.
- **Just built through that channel:** Demand Gen campaign `24243839443` (`[DAN] [DGEN] [CONVERSION] MU 25-54 |
  US+CA | ad 1 + ad 2 | start vs home`), PAUSED, 4 ad groups, 10 ads, 2 Audiences. Full record, ids and every
  API trap measured while building it: `Docs/DGEN_CONVERSION_CAMPAIGN.md`; builder
  `scripts/ads/oneoff/build-video-campaign.js`. The one-off script is still listed in the account, unscheduled —
  Dan removes it from the editor's ⋮ menu (the row's Options menu has no Remove).

## Key Decisions Already Made

- **Go direct to the API; keep Ads Scripts only as the fallback channel.** Reason: the editor paste/run loop is the
  slowest, flakiest part of every Ads task, and Explorer access removes the only reason it existed.
- **Same Cloud project, same OAuth client.** The Explorer grant is per project; the client in `abs-by-ai` is the
  one that carries it. Do not create a second client or project.
- **Explorer is enough for now.** 2,880 production ops/day is >10× anything this project does. Apply for Basic
  only if a call is refused for access level or the cap binds — that form wants company details, so it is Dan's.
- **The hourly ytads Ads Script stays running.** Porting the engagement-champion engine to a Railway cron is
  optional later work; nothing depends on it.
- **All account writes stay logged to `ytads_events`** (or a sibling table) the way the script channel logs them,
  so the ledger of what changed and why survives the channel change.
- **Dan's copy rule stands for any copy the client writes:** no claim that reads unbelievable without the video
  (`scripts/ads/ytads/headline-style.md` rule 2; memory `ad-copy-no-unbelievable-claims`).

## Detailed Plan

1. **Mint the Ads-scope refresh token (needs Dan's one click).**
   - Build the consent URL for `GOOGLE_CLIENT_ID` with `redirect_uri=https://developers.google.com/oauthplayground`,
     `scope=https://www.googleapis.com/auth/adwords`, `access_type=offline`, `prompt=consent` — or use the OAuth
     Playground itself with the client id/secret entered under its gear icon ("Use your own OAuth credentials"),
     exactly as the YouTube token was minted. Send Dan the link; he signs in as `danroseconsulting@gmail.com` (the
     account that owns both Ads accounts) and clicks Allow. Claude cannot enter his password — that is the only
     hands-on step.
   - Exchange the code at `https://oauth2.googleapis.com/token` (Playground does this), store the refresh token as
     **`GOOGLE_ADS_REFRESH_TOKEN`** in `~/.absbyai-secrets.env` (0600) and on Railway service `abs-by-ai`
     (`~/.npm-global/bin/railway variables --service abs-by-ai --set GOOGLE_ADS_REFRESH_TOKEN=…`). Never paste the
     value in chat, docs or the coordination file.
   - OPEN: if the consent screen refuses the scope, the OAuth consent screen in `abs-by-ai` may need the `adwords`
     scope added (APIs & Services → OAuth consent screen) or Dan's account added as a test user. Fix there, retry.

2. **Prove one read call, then one write.**
   - `POST https://googleads.googleapis.com/v<current>/customers/3427170837/googleAds:search` with headers
     `Authorization: Bearer <access token>`, `login-customer-id: 3244586445`, JSON body
     `{ "query": "SELECT campaign.id, campaign.name, campaign.status FROM campaign WHERE campaign.id = 24243839443" }`.
     Check the current API version in the docs first (v22 was current in mid-2026; do not hardcode blindly).
   - If Google answers that a `developer-token` header is required, copy it from the Cloud Console access page
     (`…/google/ads-apis/overview?project=abs-by-ai`) into `GOOGLE_ADS_DEVELOPER_TOKEN` and retry. Record which it
     was in `Docs/DGEN_CONVERSION_CAMPAIGN.md` §API access.
   - Write test that is harmless and reversible: update the campaign's own budget name, or add and remove a label.
     Confirm the change in the UI's change history.

3. **Build `scripts/ads/api/client.js`** (Node, no new dependencies — `fetch` + the token exchange, same shape as
   `scripts/youtube/upload.js`):
   - `search(cid, gaql)` with paging; `mutate(cid, ops, {partialFailure:false})` over
     `customers/{cid}/googleAds:mutate` (mixed operation types in one request, temp ids `-1, -2…` allowed);
     `mutateOne(cid, op)`; retry on 429/5xx with backoff; every mutate logged to `ytads_events` with the operations
     and Google's response verbatim (reuse the `pg` pattern in `scripts/ads/ytads/manual.js`).
   - Bake in the measured traps from `Docs/DGEN_CONVERSION_CAMPAIGN.md`: helper to build derived resource names for
     constant-id criteria (`adGroupCriteria/<ag>~2840`, languages `~1000`, audiences `~<id>`); Demand Gen needs plain
     `targetCpa`; API-made DG ad groups are audience-grouped → targeting via an `Audience` resource; location +
     language on the ad group; campaign conversion goals written wanted-goal-first with `partialFailure:false`.
   - A `--dry-run` that sends `validateOnly: true` (the REST mutate supports it) so every future change gets the same
     Google-validated preview the Ads Script editor gave.
   - A tiny CLI: `node scripts/ads/api/client.js search "<GAQL>"`, `… mutate ops.json [--dry-run]`.

4. **First jobs through the client** (each one replaces a paste-into-editor cycle):
   - Read campaign 24243839443's per-line policy status
     (`ad_group_ad_asset_view.policy_summary` + `asset.text_asset.text`) and report whether Ad 1's Clickbait
     verdict cleared after the 2026-09-10 rewrite.
   - **Enable the campaign only when Dan says go** (`campaignOperation.update status ENABLED`). Not before.
   - Port `scripts/ads/ytads/manual.js` so a queued edit executes immediately through the client instead of waiting
     for the hourly script (keep the queue table as the ledger; the hourly script simply finds nothing pending).
   - Re-point `scripts/ads/ads-digest.js`'s Google section at the client (it is blind today for lack of a token) so
     the morning brief's "Ad spend" block finally shows Google.

5. **Write it down:** the setup recipe and the header answer in `Docs/DGEN_CONVERSION_CAMPAIGN.md` §API access (or
   a new `Docs/GOOGLE_ADS_API.md` if it outgrows a section), the memory `google-ads-scripts-mutate-traps` updated with
   "prefer `scripts/ads/api/client.js`", and the `google-ads-ui-automation` memory's API-center line corrected. Then
   remove this handoff from `Handoffs/README.md` and the HANDOFFS section of `AI_COORDINATION.md`. No dashboard row.

6. **Later, optional:** move the engagement-champion engine (`scripts/ads/ytads/engine.js` + routes) off the
   hourly Ads Script onto a Railway cron that calls the client. Only worth it once the client has run a few weeks.

## Things to Avoid / Lessons Learned

- The MCC API center form is NOT the Google Ads API any more — do not fill it in.
- The OAuth client has one registered redirect URI (OAuth Playground). Adding a localhost redirect is possible in
  Cloud Console → Credentials but unnecessary.
- `GOOGLE_REFRESH_TOKEN` is calendar-only; `YOUTUBE_REFRESH_TOKEN` is YouTube-only. A token's scopes cannot be
  extended — mint a new one.
- `login-customer-id` must be the MCC (3244586445) when calling the client account through the manager.
- Explorer level: "some API functionality may be restricted". If a specific mutate is refused for access level,
  note which, and that is the trigger for the Basic application (Dan's form).
- Every trap in `Docs/DGEN_CONVERSION_CAMPAIGN.md` was hit against the same backend the REST API talks to — the
  Scripts wrapper added only the temp-resource-name stamping; the Demand Gen rules (audience grouped, ad-group
  locations, plain targetCpa, goal ordering) will apply to REST calls too.
- Never put a token value in chat, a doc, a commit or the coordination file; the repo is public.
- A push to `main` redeploys Railway and wipes held images (memory `deploy-drops-locked-holds`) — batch commits.

## Relevant Files & Locations

- `Docs/DGEN_CONVERSION_CAMPAIGN.md` — campaign ids, the measured API traps, §API access.
- `scripts/ads/oneoff/build-video-campaign.js` — the Ads Script build (reference for operation shapes that worked).
- `scripts/ads/ytads/manual.js`, `routes.js`, `ads-script.js`, `Docs/YTADS.md` — the current script channel + queue.
- `scripts/youtube/upload.js` — the token-minting recipe (Playground redirect) and the `fetch` token-exchange pattern.
- `scripts/ads/ads-digest.js`, `Docs/ADS_DIGEST.md` — the Google section that needs the client.
- Cloud Console: `console.cloud.google.com/google/ads-apis/overview?project=abs-by-ai` (access level),
  `console.cloud.google.com/apis/credentials?project=abs-by-ai` (the client, redirect URIs, consent screen).
- Env var names: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, new `GOOGLE_ADS_REFRESH_TOKEN`, maybe
  `GOOGLE_ADS_DEVELOPER_TOKEN`, `DATABASE_PUBLIC_URL`, `YTADS_KEY`. Local cache `~/.absbyai-secrets.env`; Railway
  via `~/.npm-global/bin/railway variables --service abs-by-ai`.
- Memories: `google-ads-scripts-mutate-traps`, `google-ads-ui-automation`, `ad-copy-no-unbelievable-claims`,
  `ad-retry-rule-and-no-trick`.

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking (steps 1–4 are well-specified integration work; escalate to Opus / extended thinking only if the auth or access-level answer turns out surprising) |
| **If Claude usage is high / approaching a limit** | Codex flagship, medium effort (routine build work; the traps are already written down) |

No always-Claude override applies — this is integration code, not brand copy or Anthropic-API code. Fable 5.1 is a
fine middle choice if it is in the plan at the time (it is today; check), since the Google console driving in step
1 tends to burn retries on weaker models.

## Starter Prompt for the Next Task

> Read `Handoffs/handoff-20260910-google-ads-api-client.md` and `Docs/DGEN_CONVERSION_CAMPAIGN.md` §API access, then
> execute the handoff: (1) build me the OAuth consent link (Ads scope, OAuth Playground redirect, our `abs-by-ai`
> client) and tell me exactly what to click; once I paste the code or the Playground gives you the token, store it as
> `GOOGLE_ADS_REFRESH_TOKEN` locally and on Railway without showing it. (2) Prove one read call against campaign
> 24243839443 through the MCC and tell me whether a developer-token header is still needed. (3) Build
> `scripts/ads/api/client.js` with search, atomic mutate, validate-only dry run, and logging to `ytads_events`, with
> the Demand Gen traps baked in. (4) Use it to report Ad 1's Clickbait status and to port the manual queue so edits
> run immediately — do NOT enable the campaign unless I say so. Commit, push, update the docs and remove the
> handoff from the lists. Bias toward action: only my consent click needs me.
