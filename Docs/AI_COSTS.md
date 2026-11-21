# Monthly AI cost report

Dan's request (2026-10-01): one monthly total for all AI spend, as an artifact.

- Page source: `Docs/ai-costs/report.html` (the `MONTHS` array holds every month; newest last).
- Artifact: see the URL recorded at the bottom of this file. Always republish to the same URL.

## What counts

1. Claude subscription (Anthropic Max 20x, $200 + tax, renews on the 20th).
2. Codex subscription (Dan states $100/month; no receipt lands in Gmail, so it is entered as stated and flagged).
3. Extra Claude or Codex credits (OpenAI "Codex & Work Usage Reset" receipts, Anthropic extra usage or API credit receipts).
4. API spend: Replicate (prepaid auto-reload), Google Cloud / Gemini (prepayments), and any new metered AI provider.

Not counted: non-AI tools (VidTao, Railway, Blotato, ManyChat) and ad spend.

## Monthly run (first days of each month, for the month just ended)

Rule (Dan, 2026-10-01): prepaid APIs are counted by USAGE in the month, not by what was paid in. Reloads and prepayments are ignored.

1. Replicate usage: Chrome (Dan's login) at `https://replicate.com/account/billing`, table "Monthly usage", the row for the month. Wait a few seconds, the table loads late.
2. Gemini usage: Chrome at `https://console.cloud.google.com/billing/011B02-5AB636-DF0D31/reports;timeRange=CUSTOM_RANGE;from=YYYY-MM-01;to=YYYY-MM-DD;grouping=GROUP_BY_SERVICE`, read the Total.
3. Subscriptions and extra Claude or Codex usage: Gmail receipts for the month (`mail.anthropic.com`, Stripe receipts named "OpenAI OpCo"). Take "Amount paid", tax included. A Codex usage reset counts in the month it was bought.
4. One wider Gmail search for new AI vendors (xAI, ElevenLabs, MiniMax, fal, Kling, Runway, OpenRouter). A new prepaid vendor follows the usage rule.
5. Append a month object to `MONTHS` in `report.html`, add a Ledger row here, republish to the same URL, and tell Dan the total plus the change against the prior month.

## Traps

- Replicate's API token cannot read billing, and Python urllib gets a 403 from its API (curl works). Use the billing page.
- Replicate marks the finished month "In progress" for a few days. Re-read it on the next run and correct the ledger if it moved.
- The local `ANTHROPIC_API_KEY` is a normal key, not an admin key, so it cannot read Anthropic cost reports.

## Ledger

| Month | Total | Subscriptions | Usage on top |
|---|---|---|---|
| 2026-09 | $645.57 | $310.00 | $335.57 |

Artifact URL: https://claude.ai/artifact/CxHaMP9F7zwzUgPSb2KqXv
