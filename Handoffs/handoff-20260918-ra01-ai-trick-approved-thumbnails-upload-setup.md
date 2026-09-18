# RA-01 "The AI Trick That Got Me Abs" — approved → thumbnails, YouTube Unlisted, Google Ads

Prepared 2026-09-18 (Claude, Fable 5.1). **Recommended: Codex, GPT-6 Astra / High effort.** Operations handoff for a
new task. The edit is finished and approved; do not re-edit, re-render, re-review or reopen the creative.

## Exact next action

Read current `AGENTS.md`, `AI_COORDINATION.md`, this handoff and `.claude/skills/ad-setup/SKILL.md` (plus
`.claude/skills/youtube-packaging/SKILL.md` for the 9:16 thumbnail rules). Verify the two masters' SHA256 below, build
the thumbnails, upload both exact files to YouTube as **Unlisted**, add the ad to the Demand Gen conversion campaign
as a **new ad** (it is not a variant of Ad 1), read everything back, record the IDs.

## Dan's approval (2026-09-18, after watching the 9:16 review copy)

> All right, this is looking excellent. I think you nailed it. Audio sounded good, and color correction looks good.
> The way you cut it, I think, is good. Transitions, yeah, I think this was a template for future videos here. […]
> Excellent job with this video. […] Make a handoff document for Codex to upload. Set this video up and make the
> thumbnails.

Full quote and what it settles: `APPROVAL.md` in the delivery folder. Do not ask again whether the edit is approved.

## Exact approved assets — do not substitute or transcode

Folder: `Claude Ad Videos/the ai trick that got me abs - RA-01/` (already filed under the naming convention).

| file | SHA256 | facts |
|---|---|---|
| `the ai trick that got me abs \| claude \| 9x16 \| RA-01.mp4` | `02d032180a3eb42dc81d1857613df55ef4b715ab4d31e315834baf2a63003e51` | 1080×1920, 30000/1001, 1,714 frames, 57.190 s, H.264 / AAC stereo 48 kHz — Shorts-eligible (≤ 0:59) |
| `the ai trick that got me abs \| claude \| 16x9 \| RA-01.mp4` | `bcace8c490c8c8a3f105469c106ee1cbe40f4d839fb480fd7781fb1e4afb6a45` | 1920×1080, same edit, byte-identical audio mix, 57.190 s |

Beside them: the six gate stamps, `APPROVAL.md`, `notes-RA-01.md` ("Your calls"), `measurements-RA-01.json`,
`recipe-RA-01/`, and every round's editor + reviewer report. Work dir (same files): `/Volumes/Extreme/_edit_work/ra01/`.
Never commit media (public repo; `*.mp4` and `._*` are ignored — check `git status` before every commit).

## Verification state and the approval boundary

- Delivery gate 2.1.0 on each master: **35 PASS, 1 FAIL, 0 NOT MEASURED, 3 n/a → aggregate FAIL.** The one failing
  row is `audio:stamp`, caused by the audio gate's `artifacts` row: flux 0.090 vs bound 0.079. **The untreated outdoor
  lav already reads 0.096**; the chain lowers it and cannot pass without over-processing.
- **Dan listened and approved the audio ("Audio sounded good").** Use the files as approved. Do not alter media,
  loosen or bypass a gate, forge a PASS stamp, or hold setup for this row. The regression corpus already records the
  approval as entry `ra01-ai-trick-9x16-approved-20260918` with a `known_gap` on `audio_gate:artifacts`
  (`run.py --id …` → CORPUS PASS). Nothing is owed there.
- If a delivery/upload script refuses a FAIL-stamped file, record the approval the way the gate README prescribes
  (precedents: Ad 4 verticals' −0.9 dBTP acceptance; AV-01 today). Never change a bound or `GATE_VERSION`.
- Independent round-3 review: everything the editor controls is ship-clean; three cosmetic minors listed in
  `ROUND-3-REVIEW.md`. Not a reason to hold.

## 1. Thumbnails — Dan asked for them

Ad thumbnails use the clean look (`ad-setup` §4: Manrope caps, red bar, wordmark; builder
`social media graphics/youtube/thumbnails/_ad-setup-2026-09-11/build.py`, which imports the Ad 5 clean builder —
never copy that code; it must print ALL PASS).

- New folder: `social media graphics/youtube/thumbnails/RA-01 The AI Trick That Got Me Abs/`.
- Build **both grounds (O1 dark studio, O2 his own backdrop) in both aspects**: a **9:16** pair for the vertical and
  a **16:9** pair for the horizontal. Install the dark one on each video; give Dan the REVIEW sheet with all four so
  he can swap.
- **Copy:** a command or topic, never a result, a number or a claim (memory `thumbnail-no-claims`), and **never the
  word "trick"** (memory `ad-retry-rule-and-no-trick`). Suggested: `SEE YOURSELF / WITH ABS` (first choice) or
  `HOW TO USE AI / TO GET ABS`. No "Real picture" label and no `AbsByAI.com` on a thumbnail (AGENTS.md thumbnail
  exception).
- **Photo:** a smiling hands-on-hips studio frame with abs visible, not from `Frowning Photos/`, and not already on
  another ad thumbnail (used so far per `ad-setup` §4: blue-89, blue-173, blue-247, white-23, gray-87, white-57 —
  re-check the thumbnail folders for anything newer). Do **not** use the three pictures that appear inside this ad
  (`studio-blue-10`, `studio-gray-41`, `studio-white-90`). Run `ad-setup/ruler.py` for the waist line; cutouts are in
  `photos/finalized social media photos/_cutouts/`.
- Save `readback-<videoId>.jpg` beside each after setting it.

## 2. YouTube upload — Unlisted, never Public

- Channel `UC236gjadarHAhEhOMYNGJ9g`. Check channel uploads first so a retry cannot create a duplicate.
- **Title: `How AI Got Me Abs`** for both (append ` (Vertical)` on the 9:16 if Studio needs them told apart). The
  script's own title contains "Trick", which Dan's retry rule bans from ad-facing copy; a YouTube title is shown in ad
  placements. Keep "trick" out of title, description and tags; the folder and file names stay as they are.
- Description: write `youtube-description.md` in the delivery folder from the transcript (`ad-setup` §3). Tracked
  link `https://absbyai.com/start?utm_source=youtube&utm_medium=video_description&utm_campaign=dgen-conv-ra01`
  (match the exact UTM convention the other ad descriptions use — read one back first). A 57-second video needs no
  chapters. Include the AI-content disclosure line the other ads carry.
- Tags: `ab workout,abs by ai,ai fitness,six pack abs` + two topic tags.
- `--synthetic true` (the AI goal image appears four times and on the end card). Upload with
  `scripts/youtube/upload.js` as **Unlisted**; never Public, never YouTube-scheduled (AGENTS.md). Set the thumbnail,
  wait for processing, read back: channel, title, duration (0:57), embeddable, thumbnail, `privacyStatus=unlisted`.
  After any network error inspect channel uploads before retrying. Log to `youtube-upload.log` in the delivery folder.

## 3. Google Ads — a NEW ad in the Demand Gen conversion campaign

- Campaign `24243839443` (read live first: ENABLED, Target CPA, shared budget — preserve exactly; never enable a
  paused campaign, change a budget or bid, or touch another ad).
- New config `scripts/ads/api/dgen-ads/ra01.json` (copy the shape of `ad3.json` / a recent `adN.json`): label
  `RA-01 AI Got Me Abs`, `utm_campaign=dgen-conv-ra01`, two `videos` entries — version `claude-vertical` (the 9:16)
  and `claude-16x9` — so the builder makes one audience, the two ad groups (`| /start`, `| home`, $30 target CPA on
  the group, US + CA, English) and one ad per video per group.
- **Copy** (5 headlines ≤ 40, 3 long ≤ 90, 3 descriptions ≤ 90) per `ad-setup` §6: lead with Dan's approved shapes
  **How AI Got Me Abs** and **How I Got Abs At 40**; the rest plain statements of what the video shows (he generated
  an AI picture of himself with abs, the app analysed it and built his workout and nutrition plan, he tracks macros
  with AI). No "trick", no question, no reveal, no withheld payoff, no number, no user count, no drug words. Every line
  must pass `scripts/ads/ytads/lint.js`.
- `dgen-add-ad.js` validate-only first: it must propose exactly two new video assets, one audience, two ad groups and
  four ads, and touch nothing that exists. Then `--apply`; read back asset ids, ad-group ids, ad ids, names, final
  URLs/UTMs, status and policy. Record `REVIEW_IN_PROGRESS` honestly and note the next-day
  `node scripts/ads/api/client.js policy 24243839443`.

## 4. Records and boundaries

- `Docs/AD_VIDEO_IDS.md` (two rows), `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the new config + `.result.json`,
  `Handoffs/video-editing/00-MASTER.md` (RA-01 row → uploaded; List 3 coverage row for RA-01), and
  `python3 scripts/edit-queue/queue.py set RA-01 uploaded --by codex --note "<video ids>"`.
- Remove this handoff's line from `AI_COORDINATION.md` HANDOFFS and its row in `Handoffs/README.md`. **No dashboard
  row** (Dan's 09-08 rule).
- Commit and push only this task's docs/configs. Preserve concurrent sessions' uncommitted work; never
  `git stash -u` a shared checkout.
- **An ad is never published organically.** No Facebook, Instagram, TikTok, Blotato or YouTube Public.
- Not included: any re-edit; the 1:1 square and hook variants (List 3 jobs, only when Dan asks); budget changes.
- Still Dan's open calls, **not blocking** (`notes-RA-01.md`): the AI-adjusted BEFORE picture runs unlabelled as in
  Ad 1 (the board already carries "label his 200 lb BEFORE pictures?"); no "Results are not guaranteed" line; a
  standing ruling for the other outdoor 8/28 rolls' audio.

## Ready-to-paste starter prompt (Codex, GPT-6 Astra / High)

> Read and execute `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20260918-ra01-ai-trick-approved-thumbnails-upload-setup.md` using `.claude/skills/ad-setup/SKILL.md`. Dan approved RA-01 "The AI Trick That Got Me Abs" as is ("I think you nailed it. Audio sounded good…"). Verify the two SHA256-locked masters in `Claude Ad Videos/the ai trick that got me abs - RA-01/`, build the clean-look thumbnails in 9:16 and 16:9 (both grounds, no "trick", no claims, a studio photo not used on another ad or inside this ad), upload both files to YouTube **Unlisted** titled "How AI Got Me Abs" with `--synthetic true`, read the visibility back, then add RA-01 to Demand Gen campaign `24243839443` as a new ad (validate-only first; touch nothing existing; preserve the shared budget), and record every ID. Do not re-edit the video, change a gate, or publish anything publicly. Finish with the records in §4 and a plain-language report for Dan with the thumbnail review sheet.
