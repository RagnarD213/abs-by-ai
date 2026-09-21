# Handoff: swap Ads 9 and 13 to Muhammad's round 4 finals on YouTube and Google Ads

**Written 2026-09-21.** Dan finalized Muhammad's round 4 HD exports of Ads 9 and 13 on 09-21 and asked for a handoff
to set them up on YouTube and Google Ads. Ops work, Codex's lane (memory `codex-owns-non-core-work`). Run `/ad-setup`.

## Current state

| ad | new final (Drive) | live now (09-16 cut) |
|---|---|---|
| 9 I Tried to Get Abs With ChatGPT. Here's What Happened. | `16WCOA3ZfSbTkV229PYAUutZkslM2ksyz`, 3:13.7, 263 MB, -14.5 LUFS / -0.9 dBTP | YouTube `l4myK7f-sKo`, asset `422033283313`, group `359424269`, ads `824966559286`, `824966559307` |
| 13 I Added Up What Getting Abs Was Supposed to Cost | `1m4QtkkGFBsMWsLfeBGvO-Q1YFnYhHKS7`, 4:04.9, 329 MB, -14.1 / -1.0 | YouTube `hrQf1240kQA`, asset `421933351559`, group `359747866`, ads `824925676464`, `824966566927` |

Round 4 changes vs live: Ad 9 matching ChatGPT label at 0:14 and the black real-photo chip at 1:56; Ad 13 the
black real-photo chip at 0:41. Checked against the live doc: `revision docs/muhammad-ads-9-13-15-hd-check-9-21-26.summary.md`.
Campaign `24243839443`; row detail `Docs/DGEN_CONVERSION_CAMPAIGN.md` ~line 254; ids `Docs/AD_VIDEO_IDS.md`.

## Steps

1. Download both, file them over the master paths in `Muhammad Ad Videos/<title> - ad N/` (keep the 09-16 files as
   `… ad N (09-16).mp4`). ffprobe: 1920x1080, 29.97, durations above. Audio untouched (memory `editor-audio-untouched`).
2. Upload each as a NEW **unlisted** YouTube video (never Public, never publish-at). YouTube cannot replace a file in
   place. Copy title, description, chapters (re-time if any beat moved), tags, AI disclosure and the existing
   `-FINAL` thumbnail from the live video.
3. In each ad group, create ads on the new video asset copying the live ads' headlines, descriptions, final URLs and
   `utm_campaign=dgen-conv-ad9|ad13` exactly. Then **pause** (not remove) the four old ads. Budget stays $40/day.
4. Run `node scripts/ads/api/client.js policy 24243839443` and record the new ads' status. Recheck next day if
   `REVIEW_IN_PROGRESS`; once approved, remove the paused old ads.
5. Leave `l4myK7f-sKo` and `hrQf1240kQA` up (unlisted) until the new ads are approved, then note them retired in
   `Docs/AD_VIDEO_IDS.md`. Update both docs with the new ids.
6. Nothing organic, ever (ads never go organic rule). Commit and push the doc changes. Delete this handoff's line in
   `AI_COORDINATION.md` and its `Handoffs/README.md` row.

Also note: AV-10, AV-11, AS-09, AS-10 in `Handoffs/video-editing/` now build from these round 4 files.

## Starter prompt

> Execute `Handoffs/handoff-20260921-ads-9-13-round4-youtube-and-google-ads.md` with `/ad-setup`: file Muhammad's
> round 4 finals of Ads 9 and 13, upload each unlisted, swap the Demand Gen ads onto the new videos, run the policy
> check, and update the ids docs.

Recommended: Codex, high effort (or Sonnet 5 / medium if on Claude).
