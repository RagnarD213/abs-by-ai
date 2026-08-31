# HANDOFF: Google Ads API setup → engagement-ad automation for new YouTube videos

- **Handing off from:** Claude Code (scoping session, 2026-08-31)
- **Handing off to:** Claude Code (fresh session)
- **Reason for handoff:** Execution. The design is settled with Dan; this session was scoping only.
- **Last completed step:** Dan approved the full design (all four decisions below) and **confirmed
  the Google Ads payment method is FIXED** — the "New form of payment required" banner from the
  8/26–31 audit is no longer a blocker.
- **Exact next action:** Phase 1, step 1 — open the Google Ads API Center in Dan's real Chrome
  (claude-in-chrome MCP, his logged-in session) and apply for a developer token under the MCC.

---

## What Dan wants (the product of this automation)

For **every new video published on the YouTube channel**, automatically:

1. **Detect** the new video (scheduled daily check of the channel).
2. **Draft** one new engagement ad per Demand Gen campaign — headlines relevant to the video,
   written in the same style as the existing ads in those campaigns — and send the draft to Dan.
3. **On Dan's approval** (he reviews copy before anything is created — this is also his
   compliance gate), create the ads **inside the existing three Demand Gen campaigns**, never as
   new campaigns.
4. **Run the $20/$100 loop** (scheduled daily, fully automatic, no approval needed):
   - Ad under **$20 lifetime spend** → keep running.
   - At **$20+**: compare its **cost per conversion** against the other **active ads in the SAME
     campaign** (never across campaigns — tier 2 conversions cost ~$0.09–0.35 vs tier 1's $2–3+,
     so a cross-campaign comparison would always kill tier 1).
     - **Lowest** cost/conv in its campaign → keep running until **$100 spend**, then pause.
     - **Not lowest** → pause immediately.

### Decisions Dan locked in on 2026-08-31 — do not re-litigate

| decision | Dan's answer |
|---|---|
| Winner comparison scope | **Within the same campaign only** |
| New-video trigger | **Auto-detect new uploads** (scheduled job watches the channel) |
| Ad copy | **Draft for Dan's approval first** — never launch copy he hasn't seen |
| Campaigns in scope | **All three Demand Gen campaigns** (tier 1, tier 2, AND remarketing) |

### Two edge rules, agreed with Dan

1. **Zero conversions at $20 = "not lowest" = paused.** Cost/conv is undefined at zero; strict
   reading of his rule. This will hit the remarketing campaign hardest (it has 0 conversions on
   ~$9 lifetime) — that is accepted, not a bug. Spend is capped at $20 per ad there.
2. **The comparison metric is Google's "conversions" column**, not earned subscribers. It is
   measured at ~2x the real earned-subscriber count (tier 2: 1,553 conversions vs 792 earned
   subs) but the inflation is consistent across ads, so relative ranking picks the same winner —
   and unlike earned subscribers it is reliably readable programmatically. State costs as
   "cost per conversion (≈2x per real subscriber)" when reporting to Dan.

---

## The account facts (verified in prior sessions — do not rediscover)

- Google Ads account: **Abs by AI, 342-717-0837** (`ocid=8444849202`).
- It sits under **"Daniel Rose Marketing MCC" (324-458-6445)** — NOT Social Response Marketing
  (that MCC has zero clients; this mistake cost a prior session real time). The account does not
  appear in the top-level picker — **type "abs" in the account chooser search box**.
- The three Demand Gen campaigns:
  - `[DAN] [DGEN] [ENGAGEMENT] … geo tier 2` — **campaignId 24122099676** (the cheap-geo one)
  - the **geo tier 1** clone (US/CA/UK/IE/AU/NZ, Presence-only targeting)
  - `[DGEN] [RMKTG] youtube viewers` (remarketing, $5/day)
- Campaign goal is "YouTube engagements" with the **"YouTube channel subscriptions" native
  conversion goal checked and alone** — verified in the UI 2026-08-22. Target CPA optimization
  is genuinely pointed at subscriptions.
- All 29 existing ads: zero disapprovals (8/31 audit). Both search campaigns and Meta are OUT of
  scope — this automation touches only the three DGEN campaigns.
- **Payment method: FIXED by Dan 2026-08-31** (his statement; verify the banner is gone when
  first in the account, and flag if it is not).
- ⚠ Compliance standing rule that makes the approval gate matter: **ab-wheel short 1 must never
  run paid** (archival infomercial footage). Videos must be live/public on YouTube before ads
  can reference them.

---

## PHASE 1 — API access (this is "step 2" Dan asked to start)

All browser work in **Dan's real Chrome via the claude-in-chrome MCP** (his logged-in Google
session). The in-app browser has no Google login.

1. **Developer token.** Google Ads UI → switch into the **MCC 324-458-6445** → Admin/Tools →
   **API Center** → apply for a developer token.
   - ⚠ The application involves **accepting the Google Ads API Terms of Service — confirm with
     Dan in chat at that moment before accepting** (explicit-permission category).
   - A fresh token starts at **test-account-only access**; apply for **Basic access** in the same
     API Center form (use case: first-party automation managing our own account's ads —
     creating ads for our own YouTube videos and pausing them on spend/CPA rules; no third
     parties, no resale). Basic approval typically takes a few days and this account's volume is
     far under its limits.
   - Record the token in `~/.absbyai-secrets.env` as `GOOGLE_ADS_DEVELOPER_TOKEN` (0600 file,
     never in the repo, never pasted in chat).
2. **OAuth client + refresh token.** Google Cloud Console (Dan's same Google account) → create or
   reuse a project → enable the **Google Ads API** → OAuth client (Desktop type) → run the
   standard installed-app flow to mint a refresh token with scope
   `https://www.googleapis.com/auth/adwords`. Dan will need to click the consent screen (OAuth
   grant = his click, not ours — that is fine, he is present-ish; if unattended, leave the
   consent URL for him with exact instructions).
   - ⚠ The existing `GOOGLE_REFRESH_TOKEN` in `~/.absbyai-secrets.env` is **calendar.readonly
     only** — do not reuse it; mint a new one. Store as `GOOGLE_ADS_OAUTH_CLIENT_ID`,
     `GOOGLE_ADS_OAUTH_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`.
3. **Smoke test.** With `login-customer-id: 3244586445` and customer `3427170837`, run a GAQL
   query (`SELECT campaign.id, campaign.name, metrics.cost_micros FROM campaign`) via the REST
   endpoint (curl is fine; no client library needed for a read). Confirm the three DGEN
   campaigns come back and spend figures match the UI.
   - If the token is still test-access-only, reads against the live account will be rejected —
     that is the signal Basic access hasn't been granted yet. **Stop there and record the state**;
     the rest waits on Google's approval email (arrives at Dan's Gmail — searchable).

## PHASE 2 — verify the two capabilities before building anything

1. **Per-ad reporting**: GAQL at `ad_group_ad` level for the three campaigns —
   `metrics.cost_micros`, `metrics.conversions`, `metrics.cost_per_conversion`, ad status.
   Cross-check one campaign's totals against the UI. (Also probe whether earned-subscriber
   metrics exist at ad level in the API; not required — conversions is the agreed metric — but
   worth one query to know.)
2. **Demand Gen ad creation**: create ONE **paused** test ad in the tier-2 campaign via the API
   (Demand Gen video ad referencing an existing already-advertised video, headlines copied from
   an existing ad). Verify it appears correctly in the UI, then remove it. This is the only
   genuinely uncertain technical piece — Demand Gen mutate support is newer than the classic
   campaign types. **If ad creation is not supported for this format via the API**, the fallback
   is: automation does detection/drafting/monitoring/pausing via API, and ad CREATION stays a
   guided manual step for Dan (or a carefully-driven browser session) — the $20/$100 loop is the
   part that must be hands-off and it only needs reads + pause mutations.

## PHASE 3 — build the automation (separate session(s) once Phase 2 passes)

- **Detector/drafter** (daily): channel's public uploads (RSS feed
  `https://www.youtube.com/feeds/videos.xml?channel_id=…` — no API key needed) → diff against a
  state file → for a new video, read the existing ads' headlines per campaign, draft matching
  copy, deliver the draft to Dan for approval. Skip-list honored (ab-wheel short 1).
- **Monitor** (daily): per-ad lifetime spend + conversions for automation-created ads (tag them —
  ad name prefix or a label — so hand-made ads are never auto-paused) → apply the $20/$100 rules →
  pause via API → report every action taken to Dan.
- **Scheduling**: Claude scheduled routines (cloud) or a local cron running a plain script —
  decide in the build session; the monitor should be a deterministic script, not a judgment call.
- ⚠ **Never auto-pause an ad the automation did not create.** Dan's hand-made ads are out of
  scope for the pause logic (his existing 29 ads keep running under his own management).
- Rules doc for the loop lives in this handoff; keep the thresholds ($20/$100) as constants at
  the top of the monitor script.

## Risks / cautions

- **Terms acceptance and OAuth consent are Dan-in-the-loop moments** — pause and confirm.
- **Do not create/enable any live ad during Phase 2** — paused test ad only, then delete.
- Browser fallback in the live account is fragile (documented Copy/Paste and menu-drift failures
  2026-08-22) — screenshot before every click if you must drive the UI, and prefer the API.
- The repo is public: no tokens, no customer data in anything committed. Secrets go in
  `~/.absbyai-secrets.env` only.
- Dashboard: a Key task for this handoff exists (added 2026-08-31). Check it off only when the
  automation is fully built, scheduled, and verified live — Phase 1 alone does not close it.
