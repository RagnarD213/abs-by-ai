# RA-05 "How AI Can Get You REAL Six Pack Abs": delivery checks, upload and Google Ads setup (9:16)

**AD.** Never organic: Unlisted on YouTube, then Google Ads, nothing else. Sidebar name for the task: `How AI Real Abs AD Setup`.
Written 2026-10-14 by Claude Opus 5.5, right after Dan approved the 9:16. **Use the Codex subscription to generate the images.**

## What Dan approved

Dan, 2026-10-14, on the round 3 page (http://127.0.0.1:8838/): *"Everything looks great. This ad is approved. Give me the handoff for
setup."* Record: `Claude Ad Videos/how ai can get you real six pack abs - RA-05/APPROVAL.md` and
`/Volumes/Extreme/_edit_work/ra05/round4-plan/decisions.json`.

| | |
|---|---|
| master | `Claude Ad Videos/how ai can get you real six pack abs - RA-05/how ai can get you real six pack abs \| claude \| 9x16 \| RA-05.mp4` |
| sha256 | `c0a57092fc85b01575d507ec3dcedf28cd1d60b35c1e56ef96f9a298acbcaceb` (assert before anything; a faststart stream copy of the reviewed `round3/draft_9x16.mp4`, `eb19a240...`; no HD export step) |
| format | 9:16, 1080x1920, 58.36 s, 1,749 frames, H.264 BT.709 + AAC 320k, about 95 MB |
| closing line | "Tap the button below to see how great you look with abs and to get your AI fitness plan to make your dream body real." (button CTA: an AD) |
| words | `/Volumes/Extreme/_edit_work/ra05/round3/words_aligned.json` (film time), captions `round3/cap_9x16/captions.srt` |
| notes | `notes.md` in the same folder (what plays when, AI content) |
| audio | audio gate PASS on this exact file (stamp beside it) |

Only the 9:16 exists. The 16:9 is a separate edit job, not part of this setup (the couch clip and the vertical scan have no 16:9 layout
yet). If it is built later it joins the same ad group as one more `videos` entry.

## Read first

`/ad-setup` (the whole skill), `.claude/skills/_shared/VIDEO-RULES.md` first sections ("Thumbnails: the five"), `AGENTS.md` sections
"Thumbnail and cover mix", "Google Ads final URLs within ad groups", "YouTube visibility", "An AD is never published organically".
The RA-14 setup (`Handoffs/handoff-20261014-ra14-cheat-code-setup.md`, ids in `Docs/AD_VIDEO_IDS.md`) is the same job one ad earlier.

## Steps

1. **Delivery checks on the master, before any upload** (owed: the round 3 review copy had the audio gate and three independent reviews
   of the AI items, not the delivery gate). Adapt `.claude/skills/ad-edit/reference/ra14/round4/s93_gateplan.py` to RA-05
   (`round3/beats.json`, `timeline_9x16.json`, `hf9/manifest.json`, the cards' chip boxes in `cards_9x16/meta.json`, the CTA box,
   `talking_head_windows` per hold, full-screen cards listed in `punch` with `punch_covered: true`), run
   `_shared/deliver/watch.py` on the master and judge it with a fresh subagent, then `_shared/deliver/gate.py --format ad9x16`.
   Known: the audio `tone` row fails on every bass-lift voice (Dan's standard since 2026-10-12, as on RA-14); any OTHER failing row
   or an open watch-pass defect: stop and tell Dan in one line before uploading. Never change the approved picture to pass a gate.
2. **Preconditions** (`/ad-setup` step 0). Re-hash the master. Grep the board for RA-05 (this handoff's entry is the only one).
3. **Title and tags.** Working title "How AI Can Get You REAL Six Pack Abs". Run it through `scripts/ads/ytads/lint.js` before using
   it; title case, "REAL" in caps only if the lint and Dan's capitals rule allow (VIDEO-RULES 2026-10-09); otherwise one of Dan's
   approved shapes (**How AI Got Me Abs**). Tags from the topic.
4. **Description** from the transcript (`/ad-setup` step 3). A 58 s ad needs no chapters. Keep the AI-image sentence (the ad shows AI
   pictures, an AI couch clip and an AI body scan). Link and UTMs as the skill sets them.
5. **Thumbnails: five choices, made by Codex, then STOP for Dan's pick.** Call `.claude/skills/_shared/codex-image.sh --model
   gpt-6.1-sol --effort high` on Dan's subscription. The five: (1) a real pool-shoot photo of Dan, (2) a real studio-shoot photo, (3)
   one AI-enhanced or AI-generated image of Dan on the ad's subject (AI showing him his six-pack future; give Codex a real photo as
   reference, "lean and shredded, not bulky, same size as the reference", check the face reads as him), (4) and (5) two more AI images
   of Codex's choice. Five unique designs: write one line per option naming layout, type treatment, colour and composition before
   building, and check no two share them. Options 1 and 2: his real cutout over a Codex background, type set in code (never redraw a
   real photo). 9:16 thumbnails for a 9:16 video. No claims or numbers, no "Real picture" label, no AbsByAI.com, text off his face and
   hair, no frowning photo, Speedo crop at the waistband. Photos not already used on another ad (used list: `/ad-setup` step 4 and
   `Docs/AD_VIDEO_IDS.md`; RA-14 took studio-blue-187). One review sheet with all five, then **stop and ask Dan to pick.** Nothing is
   uploaded before his pick.
6. **Upload** (`/ad-setup` step 5) after the pick: `--privacy unlisted`, `--category 26`, `--made-for-kids false`, **`--synthetic
   true`**: the couch clip (3.47 to 7.91 s) and the body scan (25.99 to 29.66 s) are realistic AI people. Set the picked thumbnail, read
   back `privacyStatus: unlisted`, `embeddable: true`, `processingStatus: succeeded`, channel `UC236gjadarHAhEhOMYNGJ9g`.
7. **Google Ads: the cold TRIAL campaign `24316364155`** (`[DAN] [DGEN] [TRIAL] VSL page`, where RA-01, RA-14 and every current ad
   lives; the old campaign `24243839443` is paused, leave it). One new ad group for RA-05 in the same shape as RA-14's there (read its
   settings live and copy them: target CPA, the campaign's Audience, US + CA, English, logo `400941168572`, CTA `401407635767`, business
   name *Abs by AI*). Final URL `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra05&utm_content=claude-9x16-vsl`,
   the same domain and page as every ad in that campaign (check before creating). Copy: 5 headlines, 3 long headlines, 3 descriptions,
   written per `/ad-setup` step 6 and linted (Dan's shapes *How AI Got Me Abs*, *How I Got Abs At 40*; no "trick", no questions, no
   withheld payoff, nothing like "Why My X Kept Failing"). `validateOnly` first, then apply and read back. **Read the campaign's shared
   budget and do not change it** ($50/day when last read), and say in the report that it is now shared by one more ad group. Run
   `node scripts/ads/api/client.js policy 24316364155` and record the verdicts; recheck the next day.
8. **Record** (`/ad-setup` step 7): `Docs/AD_VIDEO_IDS.md` row, a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the config and
   result JSON under `scripts/ads/api/dgen-ads/`, `APPROVAL.md` gate lines updated, edit queue RA-05 `uploaded` (`queue.py set RA-05
   uploaded` + the artifact mirror) only after the Unlisted read-back and the ad exist. Clip library `add --used-in "RA-05"` for the
   couch clip (`/Volumes/Extreme/_edit_work/ra05/round3/motion/A2_locked.mp4`, `B5_locked.mp4`, START/END frames) and the vertical scan
   card (`round3/cards_9x16/scan.mp4`). Commit with `scripts/git/safe-push.sh`. Update this job's board entry; delete it once the policy
   check is clean, and remove this handoff's row from `Handoffs/README.md`.

## Not this task

No Facebook, Instagram, TikTok, Blotato or Public YouTube copy. No pinned comment (ads get none). No 16:9, square or 59 s cut (RA-05 is
58 s; each would be its own job if Dan asks). Never enable a paused campaign.

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `How AI Real Abs AD Setup`. Read `Handoffs/handoff-20261014-ra05-setup.md` and set up the approved RA-05 "How AI Can Get You REAL Six Pack Abs" 9:16 with /ad-setup. First run the delivery gate and the watch pass on the approved master. Use the Codex subscription to generate the images: make the five thumbnail choices, show me one review sheet and stop for my pick. After my pick, upload it to YouTube as Unlisted, add it to the trial campaign 24316364155 in its own ad group, run the policy check and record everything.
