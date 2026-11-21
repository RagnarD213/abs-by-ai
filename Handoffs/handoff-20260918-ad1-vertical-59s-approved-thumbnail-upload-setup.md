# Ad 1 "This Picture Got Me Abs" — 9:16 59s cutdown: approved → thumbnail, YouTube Unlisted, Google Ads

Prepared 2026-09-18 (Claude, Fable 5.1). **Recommended: Codex, GPT-6 Astra / High effort.** Operations handoff for a
new task. The edit is finished and approved; do not re-edit, re-render, re-review or reopen the creative.

## Exact next action

Read current `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `AI_COORDINATION.md`, this handoff and
`.claude/skills/ad-setup/SKILL.md`. Verify the master's SHA256 below, file it into the Ad 1 folder under the naming
convention, set the 9:16 thumbnail, upload the exact file to YouTube as **Unlisted**, add it as a new `Claude vertical
59s` variant in the two existing Ad 1 Demand Gen groups, read everything back, record the IDs.

## Dan's approval (2026-09-18, after watching the review copy in VLC)

> That ad looks good to me. I think that's actually good to ship.

He then asked for this handoff: Codex makes the thumbnail, uploads and sets it up in a new task. The job (`AV-01`)
is marked `finalized` in the edit queue with these words. Do not ask again whether the edit is approved.

## Exact approved asset — do not substitute or transcode

- **Master (held in the work dir, not yet filed):** `/Volumes/Extreme/_edit_work/AV-01/ad1_vertical_59s.mp4`
- **SHA256:** `aaa81b8a09c673285f18dd4df776a6355dc238e713e13f1cbdc9096d86f61c69`
- 61,749,767 bytes; 1080×1920; 30000/1001 fps; 1,493 frames; 49.816 s; H.264 / AAC stereo 48 kHz.
- Review copy Dan watched: `/Volumes/Extreme/_edit_work/AV-01/REVIEW 540p 9x16 59s.mp4`
  (SHA256 `97f9fa2866e38fae7847f8df43b687226906143e9589ec2c19fc2bd8b592e333`).
- Stamps beside the master: `.deliver_gate.json` (GATE_VERSION 2.1.0), `.audio_gate.json` (verbatim PASS against
  Muhammad's mix), `.labelcheck.json` (3 added chips, 0 px contact with face/abs), `.framing_proof.jpg`.
- Editor notes and recipe: `notes-AV-01.md`, `recipe-AV-01/` in the work dir; skill entry `[A13]` in
  `.claude/skills/shortad-from-longform/` (commit `55cc226`). Word timings: `words_ctc.json` (104/104 words).
- Do **not** use `/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/ad1_vertical_59s.mp4` (Aug 25, superseded, unlabelled).

## Verification state and the approval boundary

- Delivery gate 2.1.0: 34 rows PASS, **2 FAIL → aggregate FAIL**: `watch:pass` (ten picture defects) and
  `framing:push_coverage` (×1.039 vs ×1.10). Audio gate: PASS, verbatim. Independent Codex review
  (`QUEUE-REVIEW-1.md`): DOES NOT SHIP, same defects.
- **Every defect is in the approved full-length vertical `Iz0u8KHRbyE` that is already live as an ad** (two strobing
  white card exits at 6.7 / 20.7 s, one-frame take-splice jumps, the yellow orb on the beach AI clip 36.9–37.8 s,
  captions over the tight photo and phone card). Proven frame by frame in `notes-AV-01.md`. The cutdown introduced none.
- **Dan approved this exact file after being shown that list.** Use it as approved. Do not alter media, loosen or
  bypass a gate, forge a PASS stamp, or hold setup for the inherited findings. Keep the approval and the measured
  results together in the setup record.
- The gate's `watch:pass` row "closes only by a re-render or by Dan's own words". His words are above. If the delivery
  script refuses a FAIL-stamped file, record the approval the way the gate's README prescribes (the Ad 4 verticals'
  −0.9 dBTP acceptance is the precedent); do **not** change a bound or `GATE_VERSION` to get it through.
- **Corpus entry owed** (AGENTS/`qc_corpus` README: an approval becomes an entry in the same session it is filed):
  add this file as an APPROVED entry with Dan's verbatim words once it sits at its final path, then run
  `python3 .claude/skills/_shared/qc_corpus/run.py` and report the result. ⚠ `corpus.json` has another session's
  uncommitted edits — re-read from disk, add only your entry, and if the corpus run fails on this entry that is a
  finding to report, never a threshold to tune. Then set the scoreboard row's `corpus_entry` to done
  (`scripts/edit-queue/scoreboard.json`, run `AV-01-20260918-031351`).

## 1. File the master

Copy (do not move until verified) into `Muhammad Ad Videos/this picture got me abs - ad 1/`:

- `this picture got me abs | claude | 9x16 59s | ad 1.mp4` + its three stamp files renamed to match
- `this picture got me abs | REVIEW 540p 9x16 59s | ad 1.mp4`
- `notes-vertical-59s.md` (from `notes-AV-01.md`) and `recipe-vertical-59s/` (from `recipe-AV-01/`)

Re-hash after the copy; the SHA256 must match. Never commit media (public repo).

## 2. Thumbnail

Dan asked for a thumbnail. The approved Ad 1 9:16 design already exists and is the right one for this cutdown —
same ad, same aspect, and the precedent is the square 59s, which reused the full square's file:

`social media graphics/youtube/thumbnails/Ad 1 This Picture Got Me Abs/ad1-vertical-Iz0u8KHRbyE_O1-dark-studio-9x16-FINAL.jpg`
(SHA256 `e3f155b67092168491aee57416da938cd548c5bc1a0ba95be290f7db707332e6`; studio-blue-89, "HOW TO USE AI / TO GET IN SHAPE").

Verify it opens at 1080×1920 (or the 9:16 size YouTube accepts) and use it. Build a new one with
`/youtube-packaging` only if it is missing, corrupt or the wrong aspect — and then to the same design: no claims in
the copy (memory `thumbnail-no-claims`), no "Real picture" label and no `AbsByAI.com` on a thumbnail, no frowning
photo, abs visible. Save a `readback-<videoId>.jpg` beside it after setting.

## 3. YouTube upload — Unlisted, never Public

- Channel `UC236gjadarHAhEhOMYNGJ9g`. Check channel uploads first so a retry cannot create a duplicate.
- Title: keep Ad 1's title family — model on the square 59s (`C8tjH0-hPFg`); read its live title back and match it.
- Description: start from `Muhammad Ad Videos/this picture got me abs - ad 1/youtube-description-square-59s.md`
  (same 1,493-frame selection, so the wording and AI disclosure carry over). Keep the tracked link
  `utm_campaign=dgen-conv-ad1`. A 50-second video needs no chapters. Save as `youtube-description-vertical-59s.md`.
- `--synthetic true` (AI goal image + AI clips). Upload with `scripts/youtube/upload.js` as **Unlisted**; never
  Public, never YouTube-scheduled. Set the thumbnail, wait for processing, read back: channel, title, duration
  (0:50), embeddable, thumbnail, `privacyStatus=unlisted`. After any network error inspect channel uploads before
  retrying (an interrupted upload leaves a husk). Log to `youtube-upload-vertical-59s.log`.

## 4. Google Ads — add to the existing Ad 1 groups

Not a new campaign. Verify live before writing:

- Demand Gen campaign `24243839443` (ENABLED, Target CPA $30, shared budget $40/day — read live, preserve exactly).
- Ad 1 `/start` group `199420011065`; Ad 1 home group `202965542111`; audience `358261317`.
- Existing Ad 1 videos stay untouched: `lf46ytHacss`, `1oEcwdp21Fg`, `Iz0u8KHRbyE`, `VFCQAgzNIkA`, `C8tjH0-hPFg`.
- Model the config on `scripts/ads/api/dgen-ads/ad1-square.json` → new `ad1-vertical-59s.json`: version
  `Claude vertical 59s`, utm `claude-vertical-59s`, **copy byte-identical to the live Ad 1 ads** (read it back from
  the account; that copy is Dan's own and already cleared the CLICKBAIT history — do not reword it).
- `dgen-add-ad.js` validate-only first: it must propose exactly one new video asset and two new ads. If it proposes
  touching any existing ad, group, budget or bid, stop and fix the config. Then `--apply`, read back asset id, both
  ad ids, names, final URLs/UTMs, status and policy. Record `REVIEW_IN_PROGRESS` honestly; note the next-day policy check.
- Never enable a paused campaign, change a budget, or pause another ad.

## 5. Records and boundaries

- Update `Docs/AD_VIDEO_IDS.md`, `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the new config + its `.result.json`, and
  `Handoffs/video-editing/00-MASTER.md` (Ad 1 row: 9:16 59s ✅). `queue.py set AV-01 uploaded` when done.
- Remove this handoff's line from `AI_COORDINATION.md` HANDOFFS and its row in `Handoffs/README.md`. No dashboard row.
- Commit and push only this task's docs/configs. Preserve concurrent sessions' uncommitted work; never
  `git stash -u` a shared checkout.
- **An ad is never published organically.** No Facebook, Instagram, TikTok, Blotato or YouTube Public. This handoff
  authorizes only the Unlisted YouTube asset and the Google Ads variant.
- Not included: any re-edit, fixing the master's inherited faults, a new square/16:9 variant, budget changes.

## Ready-to-paste starter prompt (Codex, GPT-6 Astra / High)

> Read and execute `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20260918-ad1-vertical-59s-approved-thumbnail-upload-setup.md` using `.claude/skills/ad-setup/SKILL.md`. Dan approved Ad 1's 9:16 59-second cutdown as is ("That ad looks good to me… good to ship"). Verify the SHA256-locked master, file it into the Ad 1 folder under the naming convention, add the owed qc_corpus approval entry, set the existing approved Ad 1 9:16 thumbnail (build a matching one only if it's missing), upload the exact file to YouTube Unlisted, and add it as a new `Claude vertical 59s` variant in the two existing Ad 1 Demand Gen groups with copy byte-identical to the live Ad 1 ads. Preserve every existing ad and live setting, read back visibility and all returned IDs, record the setup, and never publish the ad organically.
