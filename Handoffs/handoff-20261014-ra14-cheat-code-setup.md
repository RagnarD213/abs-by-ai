# RA-14 "The Cheat Code For Six Pack Abs": upload and Google Ads setup (9:16)

**AD.** Never organic: Unlisted on YouTube, then Google Ads, nothing else. Sidebar name for the task: `Cheat Code Six Pack AD Setup`.
Written 2026-10-14 by Claude Opus 5.5, right after Dan approved the 9:16. **Use the Codex subscription to generate the images.**

## What Dan approved

Dan, 2026-10-14: *"Everything looks good. Give me the handoff document for setup."* Record: `Claude Ad Videos/the cheat code for
six pack abs - RA-14/APPROVAL.md`.

| | |
|---|---|
| master | `Claude Ad Videos/the cheat code for six pack abs - RA-14/the cheat code for six pack abs \| claude \| 9x16 \| RA-14.mp4` |
| sha256 | `4b520fd149ddb1d0e8acd5d369c5b0b730139309aad0c8de99399b8361442138` (assert before upload; it is the approved file, no HD export step) |
| format | 9:16, 1080x1920, 49.45 s, H.264 BT.709 + AAC 256k, about 193 MB |
| closing line | "Tap the button below now to get started." (button CTA: it is an AD) |
| transcript | `/Volumes/Extreme/_edit_work/ra14/round4/transcript_9x16.json` (Whisper on the delivered file); script words `/Volumes/Extreme/_edit_work/ra14/words_aligned.json` |
| notes | `notes.md` in the same folder (take map, every choice) |

Only the 9:16 exists. The 16:9 is not built; it is a separate edit job, not part of this setup. If it is built later it joins the
same ad group as one more `videos` entry.

## Read first

`/ad-setup` (the whole skill), `.claude/skills/_shared/VIDEO-RULES.md` first section ("Thumbnails: the five"), `AGENTS.md` sections
"Thumbnail and cover mix", "Google Ads final URLs within ad groups", "YouTube visibility", "An AD is never published organically".

## Steps

1. **Preconditions** (`/ad-setup` step 0). Re-hash the master. Grep the board for RA-14 (this handoff's entry is the only one).
2. **Title and tags.** Working title the ad has carried: "The Cheat Code For Six Pack Abs". Run it through `scripts/ads/ytads/lint.js`
   before using it; if "cheat code" is flagged, use one of Dan's approved shapes (**How AI Got Me Abs**). Tags from the topic.
3. **Description** from the transcript (`/ad-setup` step 3). A 49 s ad needs no chapters. Keep the one-line AI-image sentence (the ad
   shows his AI goal picture). Link and UTMs as the skill sets them.
4. **Thumbnails: five choices, made by Codex, then STOP for Dan's pick.** Call `.claude/skills/_shared/codex-image.sh --model
   gpt-6.1-sol --effort high` on Dan's subscription. The five: (1) a real pool-shoot photo of Dan, (2) a real studio-shoot photo, (3)
   one AI-enhanced or AI-generated image of Dan on the ad's subject (give Codex a real photo as reference, "lean and shredded, not bulky,
   same size as the reference", check the face reads as him), (4) and (5) two more AI images of Codex's choice. Five unique designs:
   write one line per option naming layout, type treatment, colour and composition before building, and check no two share them.
   Options 1 and 2: his real cutout over a Codex background, type set in code (never redraw a real photo). 9:16 thumbnails for a 9:16
   video. No claims or numbers, no "Real picture" label, no AbsByAI.com, text off his face and hair, no frowning photo, Speedo crop at
   the waistband. A pool photo not already used on another ad (used list in `/ad-setup` step 4 and `Docs/AD_VIDEO_IDS.md`). One review
   sheet with all five, then **stop and ask Dan to pick.** Nothing is uploaded before his pick.
5. **Upload** (`/ad-setup` step 5) after the pick: `--privacy unlisted`, `--category 26`, `--made-for-kids false`. **`--synthetic true`**:
   the app tour shows the AI Trainer's Push-Up demo (AI-Dan exercise footage, 36.3 to 38.3 s), which the 2026-09-27 rule lists as
   realistic AI footage. Confirm on those frames before uploading; the 8-bit opener is drawn pixel art and the goal picture is a labelled
   still, neither of which sets the flag alone. Set the picked thumbnail, read back `privacyStatus: unlisted`, `embeddable: true`,
   `processingStatus: succeeded`, channel `UC236gjadarHAhEhOMYNGJ9g`.
6. **Google Ads: the cold TRIAL campaign `24316364155`** (`[DAN] [DGEN] [TRIAL] VSL page`, where RA-01 and every current ad lives; the
   old campaign `24243839443` is paused, leave it). One new ad group for RA-14 in the same shape as the others there: $40 target CPA,
   the campaign's Audience, US + CA, English, logo `400941168572`, CTA `401407635767`, business name *Abs by AI*. Final URL
   `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra14&utm_content=claude-9x16-vsl`, the same
   domain and page as every ad in that campaign (check before creating). Copy: 5 headlines, 3 long headlines, 3 descriptions, written
   per `/ad-setup` step 6 and linted (Dan's shapes *How AI Got Me Abs*, *How I Got Abs At 40*; no "trick", no questions, no withheld
   payoff, nothing like "Why My X Kept Failing"). `validateOnly` first, then apply and read back. **Read the campaign's shared budget and
   do not change it** (it was $50/day on 2026-10-01), and say in the report that it is now shared by one more ad group. Run `client.js policy 24316364155` and record the
   verdicts; recheck the next day.
7. **Record** (`/ad-setup` step 7): `Docs/AD_VIDEO_IDS.md` row, a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the config and
   result JSON under `scripts/ads/api/dgen-ads/`, edit queue RA-14 `uploaded` (`queue.py set RA-14 uploaded` + the artifact mirror) only
   after the Unlisted read-back and the ad exist. Commit with `scripts/git/safe-push.sh`. Update this job's board entry; delete it once
   the policy check is clean, and remove this handoff's row from `Handoffs/README.md`.

## Not this task

No Facebook, Instagram, TikTok, Blotato or Public YouTube copy. No pinned comment (ads get none). No square or 59 s cut (RA-14 is
49 s; a square would be its own AS job if Dan asks). Never enable a paused campaign.

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `Cheat Code Six Pack AD Setup`. Read `Handoffs/handoff-20261014-ra14-cheat-code-setup.md` and set up the approved RA-14 "The Cheat Code For Six Pack Abs" 9:16 with /ad-setup. Use the Codex subscription to generate the images: make the five thumbnail choices, show me one review sheet and stop for my pick. After my pick, upload it to YouTube as Unlisted, add it to the trial campaign 24316364155 in its own ad group, run the policy check and record everything.
