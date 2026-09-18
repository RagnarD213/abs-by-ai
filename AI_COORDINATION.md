# Abs By AI — Coordination / Status Board

Loaded into every message here — keep it short. A STATUS BOARD, not a log: what is open, who is blocked,
the exact next action. History and the pre-2026-09-15 board: [`AI_COORDINATION_ARCHIVE.md`](AI_COORDINATION_ARCHIVE.md)
(not auto-loaded). Facts: `Docs/BOARD_REFERENCE.md`. Code changes: git history.

| what | where it belongs |
|---|---|
| a technique, trap, recipe or calibration | the relevant **skill** (`.claude/skills/…`) |
| what changed in code and why | **git history** |
| work spec'd but not executed | **`Handoffs/`** + `Handoffs/README.md`; dashboard only if Dan asks |
| durable facts about Dan, the product or providers | **memory**, or a `Docs/` note |
| standing rules and authorizations | **`AGENTS.md`** / **`CLAUDE.md`** |
| open state between sessions | **here**, in ≤ 3 lines |

## Working rules

1. One owner per task; don't overwrite another session's work without a handoff or review request.
2. Update when you start, get blocked, hand off or finish. **Re-read from disk before saving; edit only your entry.**
3. Finished and approved → **delete the entry** (preserve durable details first); report in chat, never as FYI here.
4. Budget: ≤2,500 words; each bold-titled entry ≤80 words and dated. Run `scripts/board-check.sh` after editing; compress if it fails.
5. Dates: `Updated: YYYY-MM-DD`; preserve `Decision since: YYYY-MM-DD`. Aging/archive: `Docs/BOARD_MORNING_MAINTENANCE.md`.
6. Entry format, ≤ 3 lines: `**Title — STATUS date, owner.** State. Next: action. ⚠ only a warning that changes the next action. Detail: path.`

---

# DAN'S DECISIONS

- **Covers for the Sep 13 + Sep 14 TikToks (09-17):** neither ever had a designed cover (uncovered on IG too); the
  7-day window shuts Sep 20 / Sep 21. Commission `/coverimage` before then, or keep the screenshot? The queue is
  fixed and proven live. `Docs/TIKTOK_COVERS.md`
- **Make the GitHub repo private (baseline 09-15)** (Settings → General → Danger Zone). Rec: yes — breaks nothing; closes the
  subscriber addresses in git history. A session then pushes a trivial commit and confirms deploy. `Docs/SUBSCRIBER_STORE.md`
- **Create the empty SixPackAbs.com Google Ads account (baseline 09-15)** (CAPTCHA blocks Claude): MCC `324-458-6445` → Accounts →
  + → Create new account; SixPackAbs.com, America/Chicago, USD, skip billing, no campaign. `Docs/GOOGLE_ADS_API.md`
- **Search bidding:** Google auto-apply removed the $2 CPC ceiling on 09-11 (both campaigns Maximize conversions, no
  target). Accept, or change it / turn auto-apply off. Brand's 09-04 over-delivery is creditable if asked. `Docs/GOOGLE_ADS_API.md`
- **Ad 2 16:9 master (live in Google Ads) shows the banned BEFORE/AFTER screen at 3:11 and email screen at 3:12, 3:23 (baseline 2026-09-15; age unknown)** —
  also in its vertical `7XgHxn59Tsg` and square. Pull, or have the beats replaced. (Zeeshan's Ad 1 email screen 3:09, known.)
- **Web cart: (baseline 2026-09-15; age unknown)** Google Pay on (rec on); OK the shipped defaults (cart video hidden until the file exists, anonymous trial
  reuse, no email before card, no urgency device). `Docs/WEB_CART.md`
- **Analysis page defaults: (baseline 2026-09-15; age unknown)** women's height 5'4" (men 5'9"). **/start:** create PostHog flag `vsl-landing-variant`
  (control/analysis 50/50) + experiment — API keys lack flag scopes. `Docs/VSL_LANDING.md`
- **/start VSL: (baseline 2026-09-15; age unknown)** read script doc `1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA`, decide §7 (on-screen line under real
  photos), record. ⚠ Live post-generation video
  says "thousands of guys" (3:16, 3:41); 75 people have ever generated.
- **@danrosefit Meta ads: (baseline 2026-09-15; age unknown)** raise champion ad set `120250753601020682` $6.50 → $8/day? Confirm both [DAN] [ENGAGEMENT]
  campaigns stay OFF. Report: https://claude.ai/code/artifact/18397bc8-efc4-4554-a440-7961cbaa423d
- **Fire the phone handoff (09-17):** deletes the Ad 5 TikTok `7686132607964269855` AND installs the 2 covers still in
  window. Run it when away from computer + phone. `Handoffs/handoff-20260917-phone-tiktok-delete-ad5-and-install-covers.md`
- **Chrome's Instagram is signed in as @abs.by.ai (09-17)** — switched to delete the mirror; Chrome hung before switching back.
- **Google Ads remarketing `24169507109` (baseline 09-15)** — ~$2.50/day, 0 clicks/conversions ever. Pause?
- **Ad 3: (baseline 2026-09-15; age unknown)** delete empty husk `J-fOMvEJwDs` in Studio; campaign budget reads $40/day (docs said $20); label his 200 lb
  BEFORE pictures?; paste Muhammad round-6 ask `revision docs/ad3-revisions-muhammad-round6-9-14-26.md`.
- **YouTube engagement tier 1 (baseline 09-15):** ad `821875813611` paused in the UI — re-enable if accidental. `Docs/YTADS.md`
- **Four off-centre published Shorts (baseline 09-15)** (`y0XIbNoA2Xo`, `P9VUGyWeNtY`, `VOlZHV1ibmU`, `rqyK5IDsxX0`): delete + re-upload
  on open Tue/Thu/Sat slots, or leave?
- **Longforms 02 (Zepbound) + 03 (Supplements):** on hold by Dan's call; Muhammad delivered neither (09-08). **Do not
  upload or chase.** ⚠ Whoever closes it deletes the reminder block in the morning-brief task's `SKILL.md`.
- **V4 + V5 longform Content ID claims: (baseline 2026-09-15; age unknown)** Replace song or leave (they cost nothing until monetised). ⚠ Never delete +
  re-upload — both are live ad destinations.
- **Upload the welcome-video shoot (114 GB) to Drive (baseline 09-15)** as its only second copy? ⚠ Personal rclone client_id first
  (the shared one hit a 403 quota). Memory `drive-backup-capability`.
- **Muhammad batch 09-14 reviewed 2026-09-15** (6 + 14 finalized; 7 r5, 8 r3, 9 r3, 13 r3, 15 r2 in his doc). Forward
  via `handoff-20260916-muhammad-ads-8-9-13-15-forward-revisions.md` (Ad 9 r3 not yet pasted into his doc; 8/13/15
  just need Upwork messages sent). ⚠ Four AI clips from **Dan's own** "AI clips for Muhammad" folder show artifacts
  (beach smudge, hands, coffee pot, robot arm live in Ad 3) — replace centrally? Ad 14 needs its HD export.
- **Forward editor docs + his calls:** Zeeshan Arms & Shoulders **r3** 09-17 (`revision docs/arms-shoulders-revisions-zeeshan-round3-9-17-26.summary.md`;
  3 items: Content-ID bed, .srt, black tail; colour is your call). Waleed V1 r4 (doc `1Uxd6a2qSuazts6lSASbVhatNkvCFINhlLAtrcmXlFBw`;
  ⚠ new side-by-side before/after 0:06.6–0:08.1). Muhammad batch doc `1L2XJKLFrRJHKlcL4Iii70iFvZeiNNeplxYQw2aeAJ_A`:
  09-10 sections (Ad 13 SIXPACKSHORTCUTS watermark; Ad 15 empty slot 0:25.5 and whether it runs as an ad) and 09-12 sections
  (Ads 6 + 7 end on the same generated man; Ad 14 watermark at 0:20).
- **Approve / listen:** Zeeshan's Ad 1 verticals (his audio untouched; ⚠ YouTube `rimBWjT9-oo` / `JOZVk4_HDwQ` carry the
  REJECTED audio — replace only on approval, then check off dashboard row "Cut 9:16 vertical ads…"). Ad 4 vertical +
  cutdown (ear check, `notes-vertical.md`; −0.9 dBTP accepted 09-11). Spray-tan shorts sound (`review/AB_three-way_audio.mp4`;
  yes unlocks the audio-match handoff). 04 invest-health room: dry (delivered) vs 09-09 dereverb.
- **Picks: (baseline 2026-09-15; age unknown)** studio-blue-89 variations (`photos/finalized social media photos/_variations/studio-blue-89/`); 3-min total
  body thumbnails A/B/C; ab-wheel shorts covers A or B ×5; Zepbound shorts swaps (`SHORTS.md`, picks were Claude's);
  exercise demos batch 4 (9 in `Media/exercise-demos/_batch4/`; `db-lunge` blocked — full Veo 3.1, Kling end_image, or film; approved ones get `-FINAL` + batch-2 install = native retest);
  **White-49 rev 2** (approval closes studio batch 6 → check off `money::Execute handoff: studio batch 6…`; delete the 60 ` 2.jpg` copies?).
- **Research to act on: (baseline 2026-09-15; age unknown)** SixPackAbs rebrand — Claude memo 09-16 says split brands, no migration before mid-2027, https://claude.ai/artifact/Xt9JYgKgo62JaQSwoNjBoC (Codex PDF said yes); ⚠ Dan: do you control the old 4.46M @sixpackshortcuts channel?; conversion funnel
  (Codex, `~/.codex/visualizations/2026/09/14/01a0a186-e6d4-7a61-9300-dba78b1932e7/abs-by-ai-conversion-strategy.docx`;
  Drive upload needs approval); "The Muhammad Standard" https://claude.ai/code/artifact/0fac6195-accb-415b-99fa-70e3825d4906
  (⚠ folds VQC-B into the engine).
- **sixpackabs.com: (baseline 2026-09-15; age unknown)** confirm the live video-first redesign; update the Yoast homepage title/description? `Docs/SIXPACKABS_SITE.md`
- **ManyChat: (baseline 2026-09-15; age unknown)** OK to close the keywords task; switch Chrome's Instagram back to @danrosefit; turn off Blotato's IG auto
  first-comment? (ask before touching). ⚠ Account shows TRIAL — lapse kills all six keywords. `Docs/MANYCHAT_KEYWORDS.md`
- **Resend (baseline 09-15):** create a full-access key → `RESEND_READ_API_KEY` in `~/.absbyai-secrets.env`.
- **Home filming set:** pick an installer, share the work order (https://claude.ai/code/artifact/2b21b748-62f0-455f-aafb-ac9a6a23ad44).
  VIVO stand return: UPS pickup was Mon 09-14 (# 298404F1F6B) — confirm it went. After install a session builds the look-A telemetry file.
- **Native retest (one phone session): (baseline 2026-09-15; age unknown)** analysis page YouTube iframe (inline vs fullscreen, pauses on leaving); `10eda3b`
  member screens; lock-in → sliders → trial CTA and locked result → analysis → unlock; iOS sandbox Restore purchases
  (`549946a`); native still shows IAP + account-first.

# ACTIVE

**Ad 1 vertical 59s setup — ACTIVE 2026-09-18, Codex.** SHA-locked AV-01 master + approved 9:16 thumbnail verified. Next: file master/corpus entry, upload YouTube Unlisted, add only `Claude vertical 59s` to the two existing Ad 1 Demand Gen groups, read back and record IDs. Detail: `Handoffs/handoff-20260918-ad1-vertical-59s-approved-thumbnail-upload-setup.md`.

**Overnight edit queue — LIVE 2026-09-18, all groups on Codex until 2026-09-24 (Claude allowance freeze); revisit after reset.** `Handoffs/handoff-20260918-claude-video-freeze-and-codex-routing.md` executed: `config.json` routes every group + review to Codex; dry-run confirms no launch resolves to Claude. Idle until an eligible job (SL-01/02 need picks). Pause: `dispatcher.py pause`.

**RO-01 ACTIVE 2026-09-17, Codex.** `/Volumes/Extreme/_edit_work/ro01/`.

**DS-04 vacuum short — REVISION 1 ACTIVE 2026-09-18, Claude.** Opening beat only; `handoff-20260918-ds04-opening-vacuum-clip-revision.md` running. Next: Dan picks a draw-in. ⚠ Audio `artifacts` FAIL is his call.


**Ads 6, 7, 10, 14 YouTube + Google Ads — REVIEW 2026-09-15, owner: Codex 01a0a744.** Four unlisted uploads and eight enabled campaign ads are complete; shared budget stays $40/day. Google policy is `REVIEW_IN_PROGRESS`. Next: re-run policy 09-16; replace Ad 7 typo/Ad 14 low-bitrate exports when delivered. Detail: `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**Ads results follow-up — OPEN 2026-09-15.** Review Google Ads results after the 09-09 account fixes (`Docs/GOOGLE_ADS_API.md`). Meta $50 review: next reading 2026-09-18; last result $2.02/follow against <$3 target.

**Web push storage — OPEN 2026-09-15.** Move `push-subs.json` to Postgres before enabling web push. Subscriber-list migration is already finished.

**PostHog signup funnels — OPEN 2026-09-15.** Rebuild `account_signup` funnels after the web-cart changes. Next: assign a session.

**Published cutdown audio — UNOWNED 2026-09-15.** 21 of 23 V2/V3/V6 cutdowns miss −14 LUFS. Next: scope remediation from `Docs/BOARD_REFERENCE.md`; preserve editor mixes under the standing audio rule.

**Google Ads policy checks — OVERDUE, next session. (baseline 2026-09-15; age unknown)** `node scripts/ads/api/client.js policy 24243839443` (eight new Ad 3
ads, including square 824906283483/824906283486; Demand Gen r2 ads 824329225648/824329225651; Ad 5 groups) and `… 24148587722` / `… 24086091285` (final-URL change).
If r2 is limited again: attempt 3 = text-free thumbnail on `1oEcwdp21Fg`, then remove. ⚠ Ad 5 headline "Why My Diets Kept
Failing" DISAPPROVED (clickbait). Add Zeeshan Ad 1 / Ad 5 verticals only after Dan approves. `Docs/DGEN_CONVERSION_CAMPAIGN.md`

**Ads 3 + 4 in Demand Gen — LIVE 09-11.** Watch spend/conversions on the new groups; delete once they have a few days of data.
Dashboard row "Add the new finished ads…" stays open only for Zeeshan's Ad 1 verticals.

**Scheduled posts — confirm and delete.** $17 Ab Wheel `bkzT-3ENpoU` public 09-13 (⚠ TikTok 6:58 vs the length cap);
its 5 shorts post Oct 27–Nov 5. Zeeshan Ab Wheel Workout `b_bS9NdmL-g` public 09-20 — ⚠ confirm the Studio thumbnail
test starts. `BLOTATO_QUEUE_PROGRESS.md`

**Google Ads custom segments — 9 OF 12 BUILT 09-08, resume fresh.** Left: 7a/7b/7c (app picker), `website | member hub |
540 day` list, Phase 2 if the Demand Gen draft exists. ⚠ No pointer events or `await` in `javascript_tool` on a busy Ads
tab; stop rather than click into spinners. `Handoffs/handoff-20260908-google-ads-custom-segments.md`

**Ad 4 vertical masters — HELD (baseline 2026-09-15; age unknown)** in `/Volumes/Extreme/_edit_work/ad4-vert/` (`deliver4.py` refuses the −0.9 dBTP verbatim
stamp). Next: after Dan approves, deliver masters and check off the verticals row. Skill [A8].

**Shorts parked behind the long-form hold. (baseline 2026-09-15; age unknown)** Zepbound (8) + Supplements (8) need the new spray-tan sound
(`Handoffs/handoff-20260909-audio-match-muhammad.md`); nothing posts until a parent long-form is public.

⚠⚠ **Vertical build owners (Ads 4/5): the BT.601 colour fault is in your builds (baseline 2026-09-15; age unknown)** — memory `untagged-video-bt601-trap`;
decode with `accurate_rnd`. Re-copy the skill's `caption_sync_check.py` into `ad3-vert/` / `ad4-vert/` (fixed `/tmp` paths collide).

# BLOCKED — external

**iOS `ccc7a7ae` — REJECTED 2026-09-17: 4.3(b) Spam + 1.1, account warning.** ⚠ No resubmit/reply until Dan
rules on the 09-18 plan. Thread `c20863ae-678d-3055-b91e-4b5f8fd9014c`.

**Blotato 200/200 queue. (baseline 2026-09-15; age unknown)** IG gap-fill: last 7 of 70 wait for slots → `scripts/blotato/iggap_fill.py --apply`. TikTok: then
`tiktok_mirror.py --restore-fb --apply` (6 FB mirrors in `fb_trimmed.json`). Post `667411` exceeded the 400 MB cap — re-encode
before re-queuing. ⚠ A Blotato `failed` on a big video may be live (memory `blotato-false-failure-large-video`).

**Google Ads Purchase conversion + enhanced-conversion mapping — wait for the first real sale. (baseline 2026-09-15; age unknown)** The feed is empty because no
sale has happened; do not manufacture a row. Then map the `Email` column in Data manager and tidy Purchase/Subscribe.
Memory `google-ads-ui-automation`.

# HANDOFFS WRITTEN, NOT EXECUTED

- `handoff-20260918-ad1-vertical-59s-approved-thumbnail-upload-setup.md` — 09-18: approved Ad 1 9:16 59s → thumbnail, Unlisted, DGen. Astra/High.
- `handoff-20260917-install-approved-a06-short-thumbnail.md` — ready 2026-09-17: approved A06 cover, exact YouTube Short, desktop Change verified. GPT-5.6 Sol / High.

**C1652 organic setup — ACTIVE 2026-09-17, Codex.** R4 hash verified; five thumbnails built/QC'd. Next: Dan picks one or two, then upload YouTube Private and queue five organic accounts through Blotato. Detail: `Handoffs/codex-video-trial/06j-c1652-approved-r4-upload-and-setup.md`.

`[dash]` = on the dashboard's Handoffs to fire list; whoever runs one deletes that row, this line and its README row.

- `handoff-20260918-kit-first-production-ad10-vertical.md` — kit builds AV-07 (Ad 10 vertical). Codex Astra, high.
- `handoff-20260917-phone-tiktok-delete-ad5-and-install-covers.md` [dash] — PHONE ONLY, fire away from computer + phone:
  delete the Ad 5 TikTok, install the 2 covers still in window. ⏰ Sep 19 / Sep 22 22:00 UTC. Sonnet 5 or Fable 5.1 / Medium.
- `codex-video-trial/06k-ad14-codex-r4-approved-upload-and-setup.md` — ready09-17, GPT-6 Astra/High; exact approved R4 → YouTube Unlisted + existing Ad14 DGen groups; preserve Muhammad HD, no organic posting.
- `handoff-20260915-finalized-ads-6-14-youtube-and-google-ads.md` — Ads 6, 7, 10, 14 → YouTube + DGen (2026-09-15). Codex, high.
- `handoff-20260918-ra01-ai-trick-approved-thumbnails-upload-setup.md` — RA-01 approved 09-18 → thumbnails, YouTube Unlisted ×2, new DGen ad. Codex Astra/High.
- **`video-editing/00-MASTER.md` — THE video-editing list (2026-09-16):** 16 raw short ads, 25 dedicated shorts, 8 long-forms, 3 shorts-from-long-form, 15 ad variants; one doc per job, Claude + Codex prompts. Supersedes the J1–J18 ad-variants queue. Dan picks the order.
- **Token savings, all Codex (09-18):** `handoff-20260918-claude-video-freeze-and-codex-routing.md` (fire first), `…-shrink-always-loaded-instructions.md`, `…-move-routines-to-codex.md`.
- `handoff-20260917-overnight-edit-queue.md` — Phase 1 built; **Phase 2** next (placeholder flow). Fable or Astra, high.
- `codex-video-trial/06h-organic-r4-motion-graphics-and-variety.md` — C1652 R4, ready09-17; supersedes executed06f. Astra/High.
- `handoff-20260912-ad5-vertical-revisions-round2.md` (spec for AV-04) — same man before/after (after picture `13_AFTER_ai-generated_app-demo-man.jpg`
  named, no spend); real-picture label on every real photo. ⚠ `g5.real_chip` is shared with Ad 4. Opus high.
- `handoff-20260909-vqc-C-phase4-cut-technique.md` — before engine Phase 4. Fable 5.1 high.
- `handoff-20260911-junk-footage-pass.md` — parallel-safe with engine Phases 2–4. Fable 5.1 high.
- `handoff-20260911-video-quality-engine.md` — master plan; Phases 1–4 done (kit tied blind 09-18); next format: Dan. VQC-B/VQC-D superseded, do not fire.
- `handoff-20260910-start-vsl-edit-and-install.md` — after Dan records the VSL. Fable 5.1 high.
- `handoff-20260909-audio-match-muhammad.md` — Zepbound + supplements, after Dan OKs the spray-tan sound.
- `handoff-20260908-google-ads-custom-segments.md` — partly executed (ACTIVE). Fable 5.1 high.
- `handoff-20260812-revenuecat-restore-behavior-audit.md` [dash] — the day Apple approves.
- `handoff-20260812-purchase-before-account.md` [dash] — after approval and the RevenueCat audit.
- `handoff-20260818-android-public-build-swap.md` [dash] — needs Dan's Android on adb.
- `handoff-20260826-danrosefit-abs-image-gap-fill.md` [dash] — once Blotato has 7 free slots.

Dead, do not run: `handoff-20260901-danrosefit-ad-identity-fix.md`, `handoff-20260902-shorts-centering-queue-fix.md`,
`handoff-20260902-google-ads-engagement-champion-automation.md` (live; `Docs/YTADS.md`).

## ACTIVE
- **Grok / AV-05 Ad 6 vertical** (2026-09-17 17:36 CT): building 9x16 + ≤0:59 from Muhammad Ad 6 via shortad-from-longform; workdir `/Volumes/Extreme/_edit_work/av05-ad6-vert/`.
