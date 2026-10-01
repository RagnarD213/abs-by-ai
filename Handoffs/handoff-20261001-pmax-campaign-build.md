# Handoff: build the Performance Max campaign for the $450 credit

Written 2026-10-01 by Claude (brainstorm session), settings decided by Dan the same day. Not executed.
Recommended: **Codex GPT-6 Sol, high effort** (ads ops). Task name: `Performance Max Build AD`.

## Goal

Build one Performance Max campaign in Google Ads account 342-717-0837 that spends the $450 Performance Max promo
credit Dan redeemed on 2026-10-01. It mirrors the cold trial campaign `24316364155`: same six ads, same sales page,
Trial Signup as the only goal. One campaign, one asset group.

## Fire when

The finished campaign images exist. Dan's picks and the image build come from `Docs/CAMPAIGN_IMAGES_RESEARCH.md`
(section 6, cold image plan; section 8, build spec). **If the picked finals are not on disk, stop and say so. Do not
substitute video thumbnails or make new images in this task.** Dan rejected the thumbnails as the image set.

## Step 0: the credit (do this first)

Open Billing > Promotions and read the full terms of the "Performance Max $450.00" promotion. Record in the doc:
whether it is applied, the expiry date, and whether it needs paid spend before it kicks in. If it is not applied, or
it requires spend first, build the campaign PAUSED, report to Dan and stop there.

## Settings Dan decided

| Setting | Value |
|---|---|
| Campaigns | One. One asset group. |
| Name | `[DAN] [PMAX] [TRIAL] VSL page | 6 ads | US+CA | site visitors 30 day` |
| Budget | $15/day, end date 30 days after the start date |
| Goal | Trial Signup `7704441545` (SIGNUP / WEBSITE) as the only campaign-specific goal |
| Bidding | Maximize conversions, no target. Note in the doc: add a $40 target after the first few trials. |
| Final URL | `https://absbyai.com/start`, with `utm_source=google&utm_medium=pmax&utm_campaign=pmax-trial` |
| Final URL expansion | OFF |
| Automatically created assets (text and video) | OFF |
| Location | United States + Canada, presence only (people in the location, not interested in it) |
| Language | English |
| Age | Exclude 18-24 and 65+. Keep 25-64 and unknown. |
| Gender | Male + unknown, if the account offers gender exclusion in Performance Max |
| Brand terms | **NOT excluded** (Dan's call). Add no brand exclusion list. |
| Negative keywords | Campaign-level: copy the negatives on Non-Brand Search campaign `24148587722`, plus `free` and the generator terms (generator, abs editor, abs creator, six pack ai, ai six pack, give me abs ai). Do not add any negative that contains "abs by ai" or "dan rose". |
| Member exclusion | Exclude `website | member hub | 540 day` `9480144404`, `All Converters` `9441311426`, `Purchasers of Abs By AI` `9469016618`, by whatever route Performance Max offers in this account. If none exists, report it. |
| Audience signal | **Only our own data, only one list: website visitors, 30 day.** No custom segments, no interests, no YouTube viewer lists, no search themes. |

The 30 day website list is one of `9452848282`, `9453529251`, `9452257061` (7, 30 and 365 day; the windows were fixed
on 2026-10-01). Read each list's name and membership days and pick the 30 day one. Do not guess from the order.

If the account does not offer one of the exclusions (age, gender, members), build without it and list it in the report.

## Assets

- **Videos:** the six ads of `24316364155`, every format that campaign runs (table in
  `Docs/DGEN_CONVERSION_CAMPAIGN.md`, 2026-10-01 section; ids in `scripts/ads/api/dgen-ads/trial-campaign.result.json`).
  Performance Max takes up to five videos per asset group, so pick five that cover the six angles and all three
  shapes (16:9, 9:16, 1:1), leading with whichever ads have the best cost per trial, or the best click-through if
  there are no trials yet. Say which were left out and why.
- **Text:** Dan's own headlines as they stand in `24316364155` today (he rewrote all six ads on 2026-10-01), plus that
  campaign's long headlines and descriptions. Performance Max limits: up to 15 headlines of 30 characters, 5 long
  headlines of 90, 5 descriptions of 90 with one of 60 or fewer. Use his lines unchanged. If a line is too long for a
  slot, leave it out. If a slot cannot be filled from his lines, write the missing line with `/ad-copy` and list every
  new line in the report.
- **Images:** the picked cold set, 4 landscape (1.91:1), 4 square (1:1), 2 portrait (4:5). Set Google's AI label on
  the AI-made ones.
- **Logo, business name, call to action:** same as the trial campaign.

## Build method

API first (`scripts/ads/api/client.js`, notes in `Docs/GOOGLE_ADS_API.md`; memory `google-ads-api-client`,
`google-ads-scripts-mutate-traps`). Follow the trial campaign's pattern: `validateOnly` first, then apply, then read
everything back and save the result as `scripts/ads/api/dgen-ads/pmax-campaign.result.json`. Anything the API refuses
goes through the Ads interface (memory `google-ads-ui-automation`). Build PAUSED, read back every setting in the table
against what Google stored, then ENABLE. Dan has authorized enabling; do not hold it for review unless Step 0 says to.

Do not change any other campaign. `24316364155` and both remarketing campaigns stay exactly as they are.

## After it is live

- Add a dated section to `Docs/DGEN_CONVERSION_CAMPAIGN.md`: ids, settings as read back, which exclusions were
  unavailable, start and end dates, credit terms.
- One board entry (short) with the two check dates:
  - **Day 5:** spend by channel, new versus returning visitors, policy status of every asset.
  - **$150 spent (about day 10):** judge per `Docs/CAMPAIGN_IMAGES_RESEARCH.md` section 9. Three or more trials is a
    winner, zero is a loser, one or two runs to $300.
- Commit with `scripts/git/safe-push.sh`, naming only your files.
- Delete this handoff's line from the board and its row from `Handoffs/README.md`.

## Things to know

- An audience signal in Performance Max is a starting hint, not a wall. Google will show the ads to people outside the
  30 day visitor list once it runs out of them or finds signups elsewhere. That is expected. Report the new versus
  returning split at day 5 so Dan can see how far it wandered.
- The 30 day visitor list is small. If the campaign barely spends in the first five days, report it with the list
  size; do not widen the targeting without Dan.
- Trial Signup has had almost no conversions, so bidding starts with little to learn from.
- The end date matters: once the credit is used up, spend goes to Dan's card.
- No em dashes in anything written.

## Starter prompt

> Name this task `Performance Max Build AD`. Read `Handoffs/handoff-20261001-pmax-campaign-build.md` and execute it.
> Build one Performance Max campaign in Google Ads account 342-717-0837 to spend my $450 credit: one asset group,
> `/start` only, Trial Signup as the only goal, $15/day with an end date 30 days out, the six trial-campaign ads with
> my own headlines, and the campaign images I picked. Targeting is our own data only: website visitors in the past
> 30 days as the one audience signal, nothing else. Use every hard control in the handoff (US + Canada by presence,
> English, ages 18-24 and 65+ excluded, URL expansion off, auto-created assets off, the negative keywords, members
> excluded) but do NOT exclude brand terms. Read the credit's terms first. Build it paused, read it back, enable it,
> record the ids, and tell me which settings the account did not offer.

Model: Codex GPT-6 Sol, high effort.
