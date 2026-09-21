# Handoff: Ads 9 + 13 round 4, policy check and removal of the old ads

**Written 2026-09-21.** The round 4 swap is done (`Docs/DGEN_CONVERSION_CAMPAIGN.md`, section 2026-09-21). Four new
ads went into Google review on 09-21 and the four old ads were paused. This job finishes the swap. Ops work, all
reversible except the ad removal, which the original handoff already authorized once the new ads are approved.

## IDs (campaign `24243839443`, account 342-717-0837)

| ad | new ads (ENABLED, in review) | old ads (PAUSED, to remove) | old video to retire |
|---|---|---|---|
| 9 | `825520817992` (/start, group `200857678952`), `825520817995` (home, group `198969095463`) | `824966559286`, `824966559307` | `l4myK7f-sKo` |
| 13 | `825601774244` (/start, group `197465035822`), `825601774247` (home, group `200980520340`) | `824925676464`, `824966566927` | `hrQf1240kQA` |

New videos: Ad 9 `zvVk680kSfo`, Ad 13 `-SuKGXGcbIg` (both Unlisted).

## Steps

1. `node scripts/ads/api/client.js policy 24243839443 | grep -E "Ad (9|13) "`
2. **Only if all four new ads are APPROVED** (or APPROVED_LIMITED with no disapproved line): remove the four old ads
   with `client.js mutate ops.json --note "…"`, one `adGroupAdOperation: { remove: "customers/3427170837/adGroupAds/<group>~<ad>" }`
   per ad. Read back that each is gone and the four new ads are still ENABLED.
   - Still `REVIEW_IN_PROGRESS`: change nothing, update the board entry's date, stop.
   - Any new ad DISAPPROVED: leave the old ads paused (do not re-enable without Dan), rewrite only the flagged line
     per `/ad-setup` step 6 policy rules, report to Dan.
3. `Docs/AD_VIDEO_IDS.md`: mark the `l4myK7f-sKo` and `hrQf1240kQA` rows retired (not in any ad). Leave the videos up
   on YouTube (unlisted); do not delete them.
4. `Docs/DGEN_CONVERSION_CAMPAIGN.md`: append one line to the 2026-09-21 section with the verdict and removal date.
5. Also report to Dan: the campaign budget read **$50/day** on 09-21 while the docs say $40. Read it again
   (`SELECT campaign_budget.amount_micros FROM campaign WHERE campaign.id = 24243839443`) and say the number. Do not change it.
6. Delete the "Ads 9 + 13 round 4 swap" entry in `AI_COORDINATION.md` (re-read from disk first, run
   `scripts/board-check.sh`), this handoff's line there and in `Handoffs/README.md`. Commit and push to `main`.

Never enable a paused campaign. Nothing organic.

## Starter prompt

> Execute `Handoffs/handoff-20260922-ads-9-13-round4-policy-and-remove-old.md`: run the Google Ads policy check on
> the four new Ad 9 and Ad 13 ads, and if they are approved remove the four paused old ads, retire the old videos in
> the docs, and close the board entry.

Recommended: Sonnet 5 / medium (or Codex / medium).
