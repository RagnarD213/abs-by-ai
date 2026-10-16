# RA-04 "Top 3 Tips For Getting Abs": upload and Google Ads setup (9:16 + 16:9)

**AD.** Never organic: Unlisted on YouTube, then Google Ads, nothing else. Sidebar name for the task: `Top 3 Tips AD Setup`.
Written 2026-10-16 by Claude Opus 5.5, right after Dan finalized round 5. **Use the Codex subscription to generate the images.**

## What Dan approved

Dan, 2026-10-16, on the round 5 page: *"This looks good. This ad is finalized. Give me the handoff for setup."* Record:
`Claude Ad Videos/top 3 tips for getting abs - RA-04/APPROVAL.md` and `/Volumes/Extreme/_edit_work/ra04/round5-plan/decisions.json`.

| | 9:16 | 16:9 |
|---|---|---|
| master | `Claude Ad Videos/top 3 tips for getting abs - RA-04/top 3 tips for getting abs \| claude \| 9x16 \| RA-04.mp4` | same folder, `... \| 16x9 \| RA-04.mp4` |
| sha256 | `c97bd87651f32d66d53d499c4fea39866ca061f46a9a28e2161b40b6683db6cb` | `d8d95ab3e74b40ea3708f28ae83b0942afbbaf8bb73d9068a494a1501704fdc4` |
| format | 1080x1920, 57.92 s, 1,736 frames, H.264 BT.709 + AAC, 76 MB | 1920x1080, same length, 63 MB |

* **Closing line:** "So take the first step. Tap the button below to generate a picture of yourself with six-pack abs using the Abs By AI
  app." (button CTA: an AD)
* **Gates already run on these exact files** (stamps beside the masters): audio gate PASS, watch pass + fresh judge 0 open defects,
  delivery gate PASS (ad9x16 / ad16x9, GATE_VERSION 2.6.0), 16:9 edit sheet valid with Dan's approval, independent review
  `ROUND-5-REVIEW.md`. **No gate is owed.** Re-hash both masters before anything; if either hash differs, stop and tell Dan.
* **Words:** `/Volumes/Extreme/_edit_work/ra04/words_aligned.json`; captions `cap_9x16/` and `cap_16x9/` there; what plays when:
  `notes-RA-04.md` in the delivery folder.
* **AI content (the synthetic flag is TRUE):** 39.14-43.44 s is a realistic AI person (the broken-arm gym clip, Veo); 6.84-9.94 s an AI
  phone clip; AI pictures in the app cards (3.20-6.84 s the white demo man, 15.3-17.9 s and 25.2-31.2 s the Asian demo man).

## Read first

`/ad-setup` (the whole skill), `.claude/skills/_shared/VIDEO-RULES.md` first sections ("Thumbnails: the five"), `AGENTS.md` sections
"Thumbnail and cover mix", "Google Ads final URLs within ad groups", "YouTube visibility", "An AD is never published organically".
The two setups one ad earlier: `Handoffs/handoff-20261014-ra05-setup.md` and `Handoffs/handoff-20261014-ra14-cheat-code-setup.md`
(ids in `Docs/AD_VIDEO_IDS.md`, campaign log in `Docs/DGEN_CONVERSION_CAMPAIGN.md`). RA-01 is the one earlier ad that went up in both
aspects; copy its pattern for the pair.

## Steps

1. **Preconditions** (`/ad-setup` step 0): re-hash both masters against the table; grep the board for RA-04 (this handoff's entry is
   the only one); confirm in `Docs/AD_VIDEO_IDS.md` that no RA-04 video exists yet.
2. **Title and tags.** Working title "Top 3 Tips For Getting Abs" (the job title). Run it through `scripts/ads/ytads/lint.js`; title case,
   no full-caps word unless it carries real emphasis (VIDEO-RULES 2026-10-09). Both uploads share the title; tags from the topic.
3. **Description** from the transcript (`/ad-setup` step 3). A 58 s ad needs no chapters. Keep the AI-image sentence (AI pictures, an
   AI phone clip, an AI person). Link and UTMs as the skill sets them, one slug per aspect.
4. **Thumbnails: five choices, made by Codex, then STOP for Dan's pick.** `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol
   --effort high` on Dan's subscription. The five: (1) a real pool-shoot photo of Dan, (2) a real studio-shoot photo, (3) one
   AI-enhanced or AI-generated image of Dan on the ad's subject (the three tips: a goal picture on his phone's lock screen, an AI plan,
   AI that adapts when life gets in the way; give Codex a real photo as reference, "lean and shredded, not bulky, same size as the
   reference", and check the face reads as him), (4) and (5) two more AI images of Codex's choice. Five unique designs: write one line
   per option naming layout, type treatment, colour and composition before building, and check no two share them. Each option in a
   **9:16 and a 16:9 layout** (one design, two crops; they count as one option). Options 1 and 2: his real cutout over a Codex
   background, type set in code (never redraw a real photo). No claims or numbers, no "Real picture" label, no AbsByAI.com, text off his
   face and hair, no frowning photo, Speedo crop at the waistband. Photos not already used on another ad (used list: `/ad-setup` step 4
   and `Docs/AD_VIDEO_IDS.md`; RA-14 took studio-blue-187). One review sheet with all five (both layouts), then **stop and ask Dan to
   pick.** Nothing is uploaded before his pick.
5. **Upload both** (`/ad-setup` step 5) after the pick: `--privacy unlisted`, `--category 26`, `--made-for-kids false`,
   **`--synthetic true`**. Set the picked thumbnail on each (its own aspect), read back `privacyStatus: unlisted`, `embeddable: true`,
   `processingStatus: succeeded`, channel `UC236gjadarHAhEhOMYNGJ9g`, for both.
6. **Google Ads: the cold TRIAL campaign `24316364155`** (`[DAN] [DGEN] [TRIAL] VSL page`, where RA-01, RA-14 and the current ads live;
   the old campaign `24243839443` is paused, leave it). One new ad group for RA-04 with BOTH videos as one ad's `videos` entries (or two
   ads in the group, matching how RA-01's pair sits there: read it live), in the same shape as RA-14's group (read its settings live and
   copy them: target CPA, the campaign's Audience, US + CA, English, logo `400941168572`, CTA `401407635767`, business name *Abs by AI*).
   Final URL `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra04&utm_content=claude-<aspect>-vsl`,
   the same domain and page as every ad in that campaign (check before creating). Copy: 5 headlines, 3 long headlines, 3 descriptions,
   written per `/ad-setup` step 6 and linted (Dan's shapes *How AI Got Me Abs*, *How I Got Abs At 40*; no "trick", no questions, no
   withheld payoff). `validateOnly` first, then apply and read back. **Read the campaign's shared budget and do not change it**, and say
   in the report that it is now shared by one more ad group. Run `node scripts/ads/api/client.js policy 24316364155` and record the
   verdicts; recheck the next day.
7. **Record** (`/ad-setup` step 7): two `Docs/AD_VIDEO_IDS.md` rows, a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the config
   and result JSON under `scripts/ads/api/dgen-ads/`, `APPROVAL.md` updated with the video ids and the ad id, edit queue RA-04
   `uploaded` (`python3 scripts/edit-queue/queue.py set RA-04 uploaded` + the artifact db mirror per `_shared/edit-queue/README.md`) only
   after both Unlisted read-backs and the ad exist. The clip library already has the round 5 clips (B0550, A0180, used-final). Commit
   with `scripts/git/safe-push.sh`. Update this job's board entry; delete it once the policy check is clean, and remove this handoff's
   row from `Handoffs/README.md`.

## Not this task

No Facebook, Instagram, TikTok, Blotato or Public YouTube copy. No pinned comment (ads get none). No square and no 59 s cut (RA-04 is
57.9 s; a square would be its own job if Dan asks). Never enable a paused campaign. Never change the approved picture or audio.

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `Top 3 Tips AD Setup`. Read `Handoffs/handoff-20261016-ra04-setup.md` and set up the approved RA-04 "Top 3 Tips For Getting Abs" 9:16 and 16:9 with /ad-setup. The gates already passed on both masters; re-hash them first. Use the Codex subscription to generate the images: make the five thumbnail choices in 9:16 and 16:9, show me one review sheet and stop for my pick. After my pick, upload both to YouTube as Unlisted, add them to the trial campaign 24316364155 in their own ad group, run the policy check and record everything.
