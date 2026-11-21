# RA-06 "What's The Best Ab Exercise?": upload and Google Ads setup (16:9 + 9:16)

**AD.** Never organic: Unlisted on YouTube, then Google Ads, nothing else. Sidebar name for the task: `Best Ab Exercise AD Setup`.
Written 2026-10-16 by Claude Opus 5.5, right after Dan approved both formats. **Use the Codex subscription to generate the images.**

## What Dan approved

Dan, 2026-10-16, on the round 4 page: *"This is approved. Give me the handoff or setup."* Record:
`Claude Ad Videos/whats the best ab exercise - RA-06/APPROVAL.md` and `/Volumes/Extreme/_edit_work/ra06/round5-plan/decisions.json`.

| | 16:9 | 9:16 |
|---|---|---|
| master | `Claude Ad Videos/whats the best ab exercise - RA-06/whats the best ab exercise \| claude \| 16x9 \| RA-06.mp4` | same folder, `... \| 9x16 \| RA-06.mp4` |
| sha256 | `db9a35d066e3bd7e684f4a8b110407d6eb76092e2417ce0ee76bb8874c8186ee` | `93fd39ba6db012bc76f74f50b1d8dd7f80448921b5379a845ebed04f418bd928` |
| format | 1920x1080, 45.71 s, 1,370 frames, H.264 BT.709 + AAC | 1080x1920, same length and audio |
| gates | audio PASS, delivery gate PASS 39/39, watch pass 0 open defects, independent review SHIP | the same |

Assert both hashes before anything. **The delivery checks are done on these exact files** (stamps beside them): do not re-run or
re-render. Closing line: "Fire your trainer and replace them with AI. Tap the button below now to get started." (button CTA: an AD).
Words: `/Volumes/Extreme/_edit_work/ra06/words_aligned.json`; captions `cap_16x9/captions.srt`. Notes: `notes-RA-06-round4.md`.
16:9 edit sheet: `... 16x9 ... .edit-sheet.json` (approved).

AI content (for the disclosure flag and the description): realistic AI people in I3 body scan 5.97-10.98 s, I1 copier 10.98-14.48 s,
the fired trainer 19.95-23.86 s, the app's AI result picture 35.37-37.10 s and the robot goodbye 41.47-43.58 s. **`--synthetic true` on
both uploads.**

## Read first

`/ad-setup` (the whole skill), `.claude/skills/_shared/VIDEO-RULES.md` first sections ("Thumbnails: the five"), `AGENTS.md` sections
"Thumbnail and cover mix", "Google Ads final URLs within ad groups", "YouTube visibility", "An AD is never published organically".
The nearest precedents: `Handoffs/handoff-20261014-ra05-setup.md` and the RA-14 setup (ids in `Docs/AD_VIDEO_IDS.md`).

## Steps

1. **Preconditions** (`/ad-setup` step 0): hash both masters, grep the board for RA-06 (the HANDOFFS line for this doc is the only one).
2. **Title and tags.** Working title "What's The Best Ab Exercise?". Run it through `scripts/ads/ytads/lint.js` (a question title may
   fail the "no questions" rule for ad copy; if so use one of Dan's approved shapes such as **How AI Got Me Abs**). Tags from the topic.
3. **Description** from the transcript (`/ad-setup` step 3). A 46 s ad needs no chapters. Keep the AI-image sentence. Link and UTMs as
   the skill sets them.
4. **Thumbnails: five choices, made by Codex, then STOP for Dan's pick.** `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol
   --effort high` on Dan's subscription. The five: (1) a real pool-shoot photo of Dan, (2) a real studio-shoot photo, (3) one
   AI-enhanced or AI-generated image of Dan on the ad's subject (which ab exercise is best, AI picking it for you), (4) and (5) two more
   AI images of Codex's choice. Five unique designs (one line each: layout, type, colour, composition, before building). Real photos:
   his real cutout over a Codex background, type set in code, never redrawn. Build each pick in 16:9 and 9:16. No claims or numbers,
   no "Real picture" label, no AbsByAI.com, text off his face and hair, no frowning photo, Speedo crop at the waistband, photos not
   already used on another ad (`/ad-setup` step 4 list and `Docs/AD_VIDEO_IDS.md`). One review sheet, then **stop and ask Dan to pick.**
5. **Upload both** (`/ad-setup` step 5) after the pick: `--privacy unlisted`, `--category 26`, `--made-for-kids false`,
   `--synthetic true`. Set the picked thumbnails, read back `privacyStatus: unlisted`, `embeddable: true`, `processingStatus:
   succeeded`, channel `UC236gjadarHAhEhOMYNGJ9g`.
6. **Google Ads: the cold TRIAL campaign `24316364155`** (`[DAN] [DGEN] [TRIAL] VSL page`, where every current ad lives; never enable
   a paused campaign). One new ad group for RA-06 with both videos, in the same shape as the newest Claude ad group there (read its
   settings live and copy them: target CPA, the campaign's audience, US + CA, English, logo, CTA asset, business name *Abs by AI*).
   Final URL `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra06&utm_content=claude-<format>-vsl`,
   same domain and page as every ad in that ad group's campaign (check before creating). Copy: 5 headlines, 3 long headlines, 3
   descriptions per `/ad-setup` step 6, linted (no "trick", no questions, no withheld payoff). `validateOnly` first, then apply and read
   back. **Read the campaign's shared budget and do not change it**; say in the report it is now shared by one more ad group. Run
   `node scripts/ads/api/client.js policy 24316364155`, record the verdicts, recheck the next day.
7. **Record** (`/ad-setup` step 7): `Docs/AD_VIDEO_IDS.md` rows, a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, config and
   result JSON under `scripts/ads/api/dgen-ads/`, `APPROVAL.md` updated, edit queue `python3 scripts/edit-queue/queue.py set RA-06
   uploaded` + the artifact mirror (only after both read-backs and the ads exist). Commit with `scripts/git/safe-push.sh`. Delete this
   doc's line from the board's HANDOFFS section and its row in `Handoffs/README.md` once the policy check is clean.

## Already done (do not redo)

Clip library: the three AI clips are A0189 (body scan), A0190 (copier), A0191 (robot goodbye), used-final RA-06; A0147 lists RA-06.
Rolls C1664, C1677, C1682, C1683 marked used. Review pages 8806, 8836, 8837, 8977 removed; review copies deleted from `Videos to Review`.
Edit queue: RA-06 `finalized`.

## Not this task

No Facebook, Instagram, TikTok, Blotato or Public YouTube copy. No pinned comment (ads get none). No square or 59 s cut (the ad is 46 s).

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `Best Ab Exercise AD Setup`. Read `Handoffs/handoff-20261016-ra06-setup.md` and set up the approved RA-06 "What's The Best Ab Exercise?" 16:9 and 9:16 with /ad-setup. Both masters already passed every delivery check. Use the Codex subscription to generate the images: make the five thumbnail choices, show me one review sheet and stop for my pick. After my pick, upload both to YouTube as Unlisted, add them to the trial campaign 24316364155 in their own ad group, run the policy check and record everything.
