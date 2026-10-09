# Abs By AI — Coordination / Status Board

A STATUS BOARD, not a log. History: [`AI_COORDINATION_ARCHIVE.md`](AI_COORDINATION_ARCHIVE.md). Facts: `Docs/BOARD_REFERENCE.md`.

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

- **Belly Fat Emergency early copies (09-23):** re-release queued Sun Oct 4. IG reel archived, TikTok set to Only me (09-23). Left: the Sep 23 FB reel is still live; only a permanent delete exists (Business Suite → Content → ⋯ → Manage post → Delete post). Dan deletes it, or leaves it.
- **TikTok covers on older posts (09-22):** every post before Sep 16 still shows a screenshot; TikTok's
  7-day edit window has closed on them, so the only fix is delete + re-upload (loses views/comments). Do it, or leave them? `Docs/TIKTOK_COVERS.md`
- **sixpackabs.com Search Console (09-22):** danroseconsulting@gmail.com has no property, so the 25 new /videos/ articles
  can't get indexing requests or an impressions check (due ~10-06). Add + verify it (Yoast meta tag), or name the owning account? `sixpackabs/articles/README.md`
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
- **Fire the phone handoff (updated 09-22):** 3 TikTok covers in Photos. `Handoffs/handoff-20260917-phone-tiktok-delete-ad5-and-install-covers.md`
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
- **Forward, Waleed + Muhammad:** Waleed V1 r4 (doc `1Uxd6a2qSuazts6lSASbVhatNkvCFINhlLAtrcmXlFBw`; ⚠ new side-by-side
  before/after 0:06.6–0:08.1). Muhammad doc `1L2XJKLFrRJHKlcL4Iii70iFvZeiNNeplxYQw2aeAJ_A`: 09-10 (Ad 13 watermark;
  Ad 15 empty slot 0:25.5, an ad?) and 09-12 (Ads 6 + 7 same closing man; Ad 14 watermark 0:20).
- **Approve / listen (09-11):** Zeeshan's Ad 1 verticals (his audio untouched; ⚠ YouTube `rimBWjT9-oo` / `JOZVk4_HDwQ` carry the
  REJECTED audio — replace only on approval, then check off dashboard row "Cut 9:16 vertical ads…"). Spray-tan shorts sound (`review/AB_three-way_audio.mp4`;
  yes unlocks the audio-match handoff).
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
  (`549946a`); native still shows IAP + account-first; new demo videos on the russian-twist + reverse-crunch exercise sheets (09-28).

# ACTIVE

**Waist-cover 2026-10-08.** TikTok:phone-upload-pending.


**SL-03 shorts 3/6 - OWED 2026-10-09, Claude.** `Handoffs/handoff-20261008-sl03-queue-shorts-2-3-6.md`

**Meta follower test - RUNNING 2026-10-08, Claude.** Auto-boost OFF; one $40/day ad self-runs Oct 16-22. Resume nothing. Nov 1 report: `Docs/AUTO_BOOST.md`.

**WV01-B-Codex:REVIEW R3 2026-10-09.** Opening review 8873; awaiting Dan. `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round3/review/R3-execution-status.json`.

**RO-01 - QUEUED 2026-10-07, Codex.** Dec6/7. TikTok limit unresolved. Next: release check. `Docs/RO01_SETUP_RECEIPT_20261007.md`.

**Video Views - HANDOFF 2026-10-07, Codex.** `24321429584`: $2 CPV, $5/day, zero spend. Thumbnail: `Handoffs/handoff-20261007-belly-fat-emergency-thumbnail-replacement.md`. Next: Oct 8 spend check.



**Nightly footage - CLOUD PENDING 2026-10-09, Codex/Claude.** Seagate: 6/6 shoots verified. Drive: 1/6 verified; 9/23 upload resumes tonight. Extreme intact; deletion paused. 8 pm Codex copies to Seagate then Drive with checksums. Next: Codex verifies Drive; Claude decides archives. Detail: `Handoffs/handoff-20261005-claude-nightly-footage-offload.md`.

**Codex revisions recovery - OPEN 2026-10-05, Codex.** Tool fixes and test Doc delivered; external video judge failed the known case. Fresh passes: 0. Next: eligible short plus sealed Claude Doc, then complete motion/AI coverage and blind comparison. Keep Claude editorial default. Detail: `Handoffs/results-20261005-codex-revisions-quality-recovery.md`.




**Ad13 setup REVIEW 2026-10-04.** Policy 10-05: `Docs/AD13_VERTICAL_SETUP_RECEIPT_20261004.md`.


**Oura review (Video 4) - QUEUED 2026-10-07, Codex.** Sun Nov 8, 9 AM CST. Then: thumbnail A/B, captions, article. `Docs/OURA_SETUP_RECEIPT_20261002.md`.

**PMax `24308574894` - LIVE 2026-10-02, Claude.** Checks 10-07, 10-12: `Docs/DGEN_CONVERSION_CAMPAIGN.md`. Campaign images: package.





**SL-05 shorts - QUEUED 2026-10-01, Claude.** Blotato Oct 17-27. Next: Oct 11, confirm parent posted, else hold these. `Docs/SL05_SETUP_RECEIPT_20261001.md`.

**RO-11 - QUEUED 2026-10-09, Claude.** YouTube Sun Dec 13, socials Mon. Then: captions, article, links. `Docs/RO11_SETUP_RECEIPT_20261009.md`.

**RO-06 NEEDS DAN 2026-10-09, Claude.** Film: localhost:8850. `Handoffs/handoff-20261008-ro06-round6-dan-review.md`.

**RO-07-R1-NEEDS-DAN 2026-10-09.** page:8857,`Handoffs/handoff-20261009-ro07-round1-dan-review.md`

**RO-12 - QUEUED 2026-10-01, Claude.** Blotato Oct 25. Then: `Docs/RO12_SETUP_RECEIPT_20261001.md`, delete.

**RO-13 - QUEUED 2026-10-07, Codex.** Sun Nov 15, 9 AM CST. Then: thumbnail A/B, captions, article. `Docs/RO13_SETUP_RECEIPT_20261005.md`.

**RO-10 - QUEUED 2026-10-07, Codex.** R3 YouTube 5287937: Nov 29, 9 AM CST. Original Private; socials live. Next: verify release, captions, article, SL-08. `Docs/RO10_SETUP_RECEIPT_20261002.md`.

**RO-16 - QUEUED 2026-10-02, Claude.** Blotato Nov 1 9AM CST. Owes: RO-12 link in description after Oct 25; captions, article after Nov 1. `Docs/RO16_SETUP_RECEIPT_20261002.md`.

**Studio posts - PARTIAL 2026-10-03, Claude.** 40 of 54 live; plan cap blocked 14 FB. Next: as slots free, `studio27_queue.py plan`, `create`. `Docs/STUDIO27_BLOTATO_QUEUE_RECEIPT_20261003.md`

**Stashed edits - NEEDS OWNER 2026-09-29, Claude.** A rebase kept upstream versions of softblue.py, SOFTBLUE.md, GRAPHICS-STANDARDS.md, deliver/gate.py, coverimage SKILL.md, 00-MASTER.md, jobs.json. Uncommitted edits: `stash@{0}` (5d8284a). Next: owner re-applies.

**SL-04 shorts - QUEUED 2026-09-30, Claude.** Blotato Oct 6-15; delete once posted. `Docs/SL04_SETUP_RECEIPT_20260930.md`.

**Stop Deadlifting - QUEUED 2026-09-29, Claude.** Blotato Oct 11 9AM CT, 4 platforms. Next: once posted, publish `sixpackabs/articles/TBD-stop-deadlifting.md`, then delete.


**RO-05 salad - QUEUED 2026-09-30, Claude.** Oct 18: fire `handoff-20260930-ro05-captions-and-article-after-release.md`.

**STOP Deadlifting clip - NEEDS DAN 2026-09-20, Codex.** R3 review copy in shared Drive folder `1dXUbQajUzM-uO_Xl92telO0qsa-Ob7uV`: full head visible, bar path rises once. Next: Dan approves R3 or names corrections.

**Overnight edit queue - PAUSED 2026-09-24, Dan's call.** Resume only if Dan says: `dispatcher.py resume`.

**Ads 6, 7, 10, 14 YouTube + Google Ads - REVIEW 2026-09-15, Codex 01a0a744.** Four unlisted uploads, eight enabled campaign ads, shared budget $40/day, policy `REVIEW_IN_PROGRESS`. Next: re-run policy; swap in Ad 7 typo / Ad 14 bitrate exports when delivered. Detail: `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**RA-01 square + headline swap - LIVE 2026-10-02, Claude.** Square ad `826755066385`. Dan's new long headline on 7 trial ads (old one CLICKBAIT). 10-03: `node scripts/ads/api/client.js policy 24316364155`; if flagged, rewrite only that line. `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**Trial thumbnails - INSTALLED 2026-10-02, Claude.** 10-03: recheck policy `24316364155`. 10-09: CTR vs week before 10-02 11:17 CT. `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**Trial `24316364155` LIVE, remarketing `24305381214`/`24316408288` PAUSED, 2026-10-01, Claude.** 10-04: delivery+policy. `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**Web push storage — OPEN 2026-09-15.** Move `push-subs.json` to Postgres before enabling web push. Subscriber-list migration is already finished.

**PostHog signup funnels — OPEN 2026-09-15.** Rebuild `account_signup` funnels after the web-cart changes. Next: assign a session.

**Published cutdown audio — UNOWNED 2026-09-15.** 21 of 23 V2/V3/V6 cutdowns miss −14 LUFS. Next: scope remediation from `Docs/BOARD_REFERENCE.md`; preserve editor mixes under the standing audio rule.

**Google Ads policy checks - OVERDUE, next session (baseline 2026-09-15).** `node scripts/ads/api/client.js policy 24243839443` (Ad 3 ads incl. squares 824906283483/824906283486; DGen r2 824329225648/824329225651; Ad 5 groups), then `… 24148587722` / `… 24086091285`. If r2 limited again: text-free thumbnail on `1oEcwdp21Fg`, then remove. ⚠ Ad 5 headline "Why My Diets Kept Failing" DISAPPROVED. Zeeshan Ad 1 / Ad 5 verticals only after Dan approves. `Docs/DGEN_CONVERSION_CAMPAIGN.md`

**Ads 3 + 4 in Demand Gen — LIVE 09-11.** Watch the new groups; delete after days of data. Dashboard row "Add the new finished ads…" open for Ad 1 verticals only.

**Scheduled posts — confirm and delete.** $17 Ab Wheel `bkzT-3ENpoU` public 09-13 (⚠ TikTok 6:58 vs the length cap);
its 5 shorts post Oct 27–Nov 5. Zeeshan Ab Wheel Workout `b_bS9NdmL-g` public 09-20 — ⚠ confirm the Studio thumbnail
test starts. `BLOTATO_QUEUE_PROGRESS.md`

**Google Ads custom segments — 9 OF 12 BUILT 09-08, resume fresh.** Left: 7a/7b/7c (app picker), `website | member hub |
540 day` list, Phase 2 if the Demand Gen draft exists. ⚠ No pointer events or `await` in `javascript_tool` on a busy Ads
tab; stop rather than click into spinners. `Handoffs/handoff-20260908-google-ads-custom-segments.md`


**RO-03-R1-NEEDS-DAN:2026-10-09,Claude,page:8877,`Handoffs/handoff-20261009-ro03-round1-dan-review.md`**

**RO-02 - QUEUED 2026-10-07, Codex.** Sun Nov 22, 9 AM CST. Then: captions and article. `Docs/RO02_SETUP_RECEIPT_20261005.md`.

**Shorts parked behind the long-form hold. (baseline 2026-09-15; age unknown)** Zepbound (8) + Supplements (8) need the new spray-tan sound
(`Handoffs/handoff-20260909-audio-match-muhammad.md`); nothing posts until a parent long-form is public.

⚠ **Ad 5 vertical: BT.601 colour fault in its build (baseline 2026-09-15).** Memory `untagged-video-bt601-trap`; method: shortad SKILL [A15].

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






`[dash]` = on the dashboard fire list; the runner deletes that row, this line and its README row.

- `handoff-20261007-ro10-subtle-reedit-sunday-reupload.md` (10-07): RO-10 R3 end graphic, Sunday replacement. Codex Sol high.
- `handoff-20261006-1017-shoot-outlines.md` (10-06)
- `handoff-20261008-dan-voice-training-part2-plan.md` (PhaseB,10-08)
- `handoff-20260930-codex-adopt-review-page-format.md` (09-30). Sol medium.

- `handoff-20261001-move-project-out-of-icloud.md` (10-01): move the project out of iCloud's Documents sync (109k duplicates, 199 cloud-only files). Run when nothing else runs here. Opus 5.5 high.
- iPhone rebuilt 10-07 outside iCloud, tracked on GitHub. Recovery list partly uninspected after Chrome crash; closes about 10-17. See `Handoffs/results-20261007-ios-rebuild.md`.
- `handoff-20261001-search-campaigns-to-vsl-page.md` (10-01). Sol high.
- `handoff-20260924-generator-consult-call-outreach.md` (09-24, overdue).
- `handoff-20260917-phone-tiktok-delete-ad5-and-install-covers.md` [dash]: PHONE ONLY, 3 TikTok covers (updated 09-22). Sonnet 5 or Fable 5.1 / Medium.
- `handoff-20260915-finalized-ads-6-14-youtube-and-google-ads.md` (09-15). Codex, high.
- **`video-editing/00-MASTER.md` — THE video-editing list (2026-09-16):** 16 raw short ads, 25 dedicated shorts, 8 long-forms, 3 shorts-from-long-form, 15 ad variants; one doc per job, Claude + Codex prompts.
- **Token savings, all Codex (09-30):** `handoff-20260918-claude-video-freeze-and-codex-routing.md` (fire first), `…-shrink-always-loaded-instructions.md`; routines now `handoff-20260930-codex-dot-00..04` (dot, free launch month). Sol.
- `handoff-20260917-overnight-edit-queue.md` — Phase 1 built; **Phase 2** next (placeholder flow). Fable or Astra, high.
- `codex-video-trial/06h-organic-r4-motion-graphics-and-variety.md` — C1652 R4, ready09-17; supersedes executed06f. Astra/High.
- `handoff-20260912-ad5-vertical-revisions-round2.md` (spec for AV-04) — same man before/after (after picture `13_AFTER_ai-generated_app-demo-man.jpg`
  named, no spend); real-picture label on every real photo. ⚠ `g5.real_chip` is shared with Ad 4. Opus high.
- `handoff-20260911-video-quality-engine.md` — master plan; Phases 1–4 done. VQC-B/VQC-D superseded, do not fire.
- `handoff-20260910-start-vsl-edit-and-install.md` — after Dan records the VSL. Fable 5.1 high.
- `handoff-20260909-audio-match-muhammad.md` — Zepbound + supplements, after Dan OKs the spray-tan sound.
- `handoff-20260908-google-ads-custom-segments.md` — partly executed (ACTIVE). Fable 5.1 high.
- `handoff-20260812-revenuecat-restore-behavior-audit.md` [dash] — the day Apple approves.
- `handoff-20260812-purchase-before-account.md` [dash] — after approval and the RevenueCat audit.
- `handoff-20260818-android-public-build-swap.md` [dash] — needs Dan's Android on adb.
- `handoff-20260826-danrosefit-abs-image-gap-fill.md` [dash] — once Blotato has 7 free slots.

## ACTIVE
**Ad 6 remarketing 2026-10-04:** Awaiting Dan: copy to enabled campaign 24305381214?
