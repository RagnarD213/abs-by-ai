# Abs By AI — Coordination / Status Board

Status board. History: [`AI_COORDINATION_ARCHIVE.md`](AI_COORDINATION_ARCHIVE.md). Facts: `Docs/BOARD_REFERENCE.md`. Dan's open decisions: `Docs/DAN_DECISIONS.md`.

| what | where it belongs |
|---|---|
| a technique, trap, recipe or calibration | the relevant **skill** (`.claude/skills/…`) |
| what changed in code and why | **git history** |
| work spec'd, not executed | **`Handoffs/`** + `Handoffs/README.md` (the only list); dashboard only if Dan asks |
| a decision only Dan can make | **`Docs/DAN_DECISIONS.md`** |
| durable facts about Dan, the product or providers | **memory**, or a `Docs/` note |
| standing rules and authorizations | **`AGENTS.md`** / **`CLAUDE.md`** |
| open state | **here**, in ≤3 lines |

## Working rules

1. One owner per task; no overwriting without handoff or review request.
2. Update on start, block, handoff or finish. **Re-read from disk first; edit only your entry.**
3. Finished and approved → **delete the entry**, durable details first; report in chat.
4. Budget: ≤2,500 words; entries ≤80 words, dated. Run `scripts/board-check.sh` after edits.
5. Dates: `Updated: YYYY-MM-DD`; keep `Decision since: YYYY-MM-DD`. Aging: `Docs/BOARD_MORNING_MAINTENANCE.md`.
6. Entry, ≤3 lines: `**Title — STATUS date, owner.** State. Next: action. ⚠ = changes next action. Detail: path.`

---

# ACTIVE

**Muhammad Shorts Batch B SFC Setup - HOLD 2026-10-27, Claude.** DS-13/06/10 waitlisted Jan 7/14/21 2027. `Docs/MUHAMMAD_SHORTS_BATCH_B_SETUP_RECEIPT_20261027.md`

**DS-02/03/07/11 HOLD 2026-10-27, Claude.** Waitlist Feb 4-25 2027. `Docs/DS02_03_07_11_SETUP_RECEIPT_20261027.md`


**[DS20:DESIGN3-TITLE:REVIEW:2026-10-26:Codex:pickA-C](http://127.0.0.1:9180/)**

**Mouthpiece SFC R1 REVIEW 2026-10-26, Codex.** [Look/assets](http://127.0.0.1:9274/). Full Short awaits Dan choices; sound/caption finishing flags retained. Queue/Drive updated. Local Git push blocked by live shared edits. `Docs/DS105_R1_CHECKPOINT_20261026.md`.

**Five Minute Exercises SFC Setup - REVIEW 2026-10-26, Codex.** [Tightened A pair](http://127.0.0.1:9270/). Next: Dan approves. Commit0b22c31 local.


**DS-84 R3 REVIEW 2026-10-26, Codex.** [Full Short](http://127.0.0.1:9284/). F, tighter exercise crops and matching large titles rendered; independent review ready. Original automatic framing/caption flags retained with audit. Native VLC copy verified; queue/Drive delivered. Next: Dan approves or lists changes. Slot released; dispatcher/heartbeat paused. No setup. Git2811712 local; shared edits block push.


**[SL-11 R1](http://127.0.0.1:9411/) REVIEW 2026-10-26, Codex.** A/B/C checked; full-film review awaits Dan. AI Natural approved; Git local.

**RO-30:R2-REVIEW:8832:2026-10-26:Codex:01a17836;await-picks;push12e0e78-local**

**DS-47 R4 REVIEW 2026-10-26,Codex:01a179fe.** [Intro](http://127.0.0.1:9214/). D enlarged/arrows/title checked. A/B/portrait locked; full Short unfinished. Next: Dan. `Docs/DS47_R4_INTRO_REVIEW_20261026.md`.

**Brief overlap NEEDS DAN 2026-10-27, Codex.** Pause old cloud routine; local publication verified.


**DS-01 HOLD 2026-10-27, Claude.** Waitlist, Jan 28. `Docs/DS01_SETUP_RECEIPT_20261027.md`

**Make Time Exercise LFC Setup (RO-18) COVERS 2026-10-27, Claude.** Five choices out; awaiting pick + Jan 13 2027 date OK. `social media graphics/youtube/thumbnails/Make Time For Exercise/THUMBNAIL-REVIEW.md`


**Footage records sync - BLOCKED 2026-10-25, Codex.** August3 offload, October23 copy/routing and initial finished B-roll backups verified. Processing owner backs up later clips. Next: safe-push owned records after live shared edits clear. Receipts: `Docs/SHOOT_20260803_OFFLOAD_RECEIPT_20261025.md`, `Media/footage-index/shoot-20261023/finished-broll-backup-20261025/result.json`.
**Wallpaper favorites - MAC APPROVAL PENDING 2026-10-25, Codex task-7.** Web save/remove/restore verified on 49b86329, correct October 21 original, private access preserved. Source recovery hashes match. Reader remains uninstalled; disable/restore safeguards tested. Next: Dan approves separate Keychain key, favorites-only server grant and LaunchAgent, then real three-screen rotation verification. `scripts/brief/wallpaper/README.md`.

**Calories Not Losing Weight SFL Setup - HOLD 2026-10-25, Codex.** Five C covers approved; all media/backups checked. Five shared-waitlist entries: Jan 4/5/8/9/11, 2027, 9 AM Central, after parent Dec 27. Blotato 197/200; no live Short schedules. Next: existing daily top-up queues four destinations per Short, then release checks. Receipt: `Docs/SL08_SETUP_RECEIPT_20261025.md`.

**Fat 90 Year Old SFC Setup - HOLD 2026-10-25, Codex.** Exact Codex R5 and approved cover installed; media verified. Shared waitlist Dec 31, 9 AM Central (Blotato 197/200). Next: daily top-up queues four, then public-cover checks. Receipt: `Docs/DS40_CODEX_R5_SETUP_RECEIPT_20261025.md`.

**Morning brief recovery - MOVE WATCH 2026-10-24, Codex.** October 24 brief published and stored document verified; planning paths repaired, 30 tests pass. Codex mover running; cloud-only files decreased 3,162 to 2,432 at 13:57 Central. Hourly heartbeat `verify-codex-icloud-move` waits for Codex DONE, then verifies local files, Git and trust config. Detail: recovery handoff.


**Arms Shoulders Workout LFC Setup - CAPACITY HOLD 2026-10-25, Codex.** Dan approved Jan 6, 2027 YouTube 9 AM Chicago; socials Jan 7 noon. Setup ready; shared waitlist eligible. Queue 197/200, needs four. Top-up preserves approved date; seven tests pass. Backups/covers/article verified. Commits saved; push blocked by live shared files. Next: existing daily top-up schedules when room opens. No Dan action. RO-04 stays finalized until verified scheduling. Receipt: `Docs/RO04_SETUP_RECEIPT_20261025.md`.


**Codex folder iCloud move WATCHING 2026-10-24, Claude.** `rename.sh Codex` downloads 3,162 cloud-only files, then moves `~/Documents/Codex` to `~/Projects/Codex`. Next: `DONE` in `~/Projects/.icloud-move.log`; Codex verifies per `Handoffs/handoff-20261024-codex-icloud-repair-followup.md`.


**Ronaldo Ab Belt SFC Setup - HOLD 2026-10-25, Codex.** Approved cover 3 R3 installed; exact R5 backed up, four media uploads hash-checked, pinned question saved. Blotato 197/200: one DS-33 shared-waitlist entry for Thu Dec 24, 9 AM Central. Next: daily top-up queues four posts, then saved-schedule/public-tile checks. `Docs/DS33_SETUP_RECEIPT_20261025.md`.


**ChatGPT Ads account - NEEDS DAN 2026-10-23, Codex.** Final creation prepared for Rose Digital Holdings LLC (US, USD, Chicago); awaiting action-time approval of OpenAI advertising/promo terms. Research complete: BetterMe and Fitbod observed. No campaign or spend. Evidence: `Research/ChatGPT Ads 2026-10-23/research-evidence.json`. Next: submit once approved, verify account.

**SL-06 QUEUED 2026-10-22, Claude.** Six shorts Nov 9-Dec 8, nothing blocked; delete after Dec 8. `Docs/SL06_SETUP_RECEIPT_20261022.md`

**Edit cap LIVE 2026-10-21, Claude.** Pushed; main folder mid-merge (not mine), so its skills lack it until merged. Next: delete after that merge.

**SL-16 HOLD 2026-10-27, Claude.** Waitlist Dec 4/7/15, Jan 12 after RO-08. `Docs/SL16_SETUP_RECEIPT_20261027.md`

**Boring Abs At 40 LFC R5 - REVIEW 2026-10-26, Codex.** [Full 8:01 film](http://127.0.0.1:9357/?r5=20261026#current) checked, independent review complete; numerical flags preserved. Neighbour kept, fridge/phone-goal removed. Next: Dan approves or gives timestamped changes. No upload/scheduling. Heartbeat paused. Recovery: `Docs/RO27_R5_CHECKPOINT_20261026.md`, round5 state.

**RA-09:POLICY-RECHECK:2026-10-22:Claude.** 10-23.


**DS-44 Hormozi QUEUED 2026-10-27, Claude.** Off-cuff R2 (DS-44B) queued Thu Dec 17, all four (6108255/59/60/62), replacing scripted. Commits f0284c0/f43babe local (live shared edits block push): next safe-push carries them. Next: release checks. `Docs/DS44_SETUP_RECEIPT_20261023.md`

**SL-15 HOLD 2026-10-22.** `Docs/SL15_SETUP_RECEIPT_20261022.md`

**I'm 41. I Wasted My Life. LFC Setup QUEUED 2026-10-17, Codex.** Dan approved exact R7 film and thumbnail C. Blotato readback: YouTube Sun Oct 18 9 AM, Facebook/Instagram Mon Oct 19 noon. Direct TikTok Monday after public YouTube check. To free capacity, Dan authorized removal of the last queued video, RO-13; its four schedules are backed up and RO-13 is on the waitlist for Dec 30. Receipt: Docs/RO25_SETUP_RECEIPT_20261017.md. Next: verify public release, covers, TikTok, RO-26 link.

**Release calendars LIVE 2026-10-17, Claude.** Long-forms Sun+Wed, Shorts Mon-Sat minus Wed/Sun (DS Thu); 105 Blotato posts moved, re-read. Dates: `Docs/LONGFORM_RELEASE_CALENDAR.md`, `Docs/SHORTS_RELEASE_CALENDAR.md` (override older RO/SL entries). Next: RO-25 setup when file lands; top-up queues RO-19 Oct 21.

**Top 1 Percent LFC Setup - RELEASE HOLD 2026-10-17, Codex.** Dan's frosted A cover installed; media/Drive backups verified, article ready, SL-17 registered. RO-26 finalized, not queued. RO-25 setup/release owner: once public, add actual watch URL and clear both holds, then existing top-up queues Oct25/26 when room opens. Receipt: `Docs/RO26_SETUP_RECEIPT_20261017.md`.

**RA-16 POLICY-RECHECK 2026-10-17, Codex.** Exact R4 films Unlisted and processed; selected R2 thumbnail 3 installed/read back. Trial group 202854620044, ads 828352448280 / 828398913310 enabled, review pending. Next 2026-10-18: existing campaign policy process, `node scripts/ads/api/client.js policy 24316364155`; if clear, delete this entry. Receipt: `Docs/RA16_SETUP_RECEIPT_20261017.md`.

**RA-13 POLICY-RECHECK 2026-10-17, Codex.** Both R3 films are Unlisted and processed; trial group 201534026375, ads 828468045056 / 828468037364 ENABLED, review pending. Next 2026-10-18: `node scripts/ads/api/client.js policy 24316364155`; if clear, delete this entry. Receipt: `Docs/RA13_SETUP_RECEIPT_20261017.md`.

**COVERS:MOBILE:2026-10-15:Docs/COVER_AUDIT_20261015.md**

**/start video test RUNNING 2026-10-10, Claude.** Reads 10-24, 10-31: `Docs/VSL_LANDING.md`.

**Waist-cover 2026-10-08.** TikTok phone upload pending.

**Meta follower test - RUNNING 2026-10-08, Claude.** Auto-boost OFF; one $40/day ad self-runs Oct 16-22. Nov 1 report: `Docs/AUTO_BOOST.md`.

**RO-01 - QUEUED 2026-10-07, Codex.** Dec6/7. TikTok direct Dec7. Next: release check. `Docs/RO01_SETUP_RECEIPT_20261007.md`.

**Video Views - HANDOFF 2026-10-07, Codex.** `24321429584`: $2 CPV, $5/day, zero spend. Thumbnail: `Handoffs/handoff-20261007-belly-fat-emergency-thumbnail-replacement.md`. Next: Oct 8 spend check.

**Nightly footage - COPYING ACTIVE 2026-10-26, Codex/Claude.** Eight shoots, including 10/23, checksum verified on Seagate and Drive. Nightly 8 pm copy-only routine remains active. Current Extreme originals remain; deletion paused. Next: decide the offload rule before enabling deletion. Detail: `Handoffs/handoff-20261005-claude-nightly-footage-offload.md`.

**Codex revisions recovery - OPEN 2026-10-05, Codex.** Tool fixes and test Doc delivered; external video judge failed the known case. Fresh passes: 0. Next: eligible short plus sealed Claude Doc, then complete motion/AI coverage and blind comparison. Keep Claude editorial default. Detail: `Handoffs/results-20261005-codex-revisions-quality-recovery.md`.

**Ad13 setup REVIEW 2026-10-04.** Policy 10-05: `Docs/AD13_VERTICAL_SETUP_RECEIPT_20261004.md`.

**Oura review (Video 4) - QUEUED 2026-10-07, Codex.** Sun Nov 8, 9 AM CST. Then: thumbnail A/B, captions, article. `Docs/OURA_SETUP_RECEIPT_20261002.md`.

**PMax `24308574894` - LIVE 2026-10-02, Claude.** Checks 10-07, 10-12: `Docs/DGEN_CONVERSION_CAMPAIGN.md`. Campaign images: package.

**SL-05 shorts - QUEUED 2026-10-13, Claude.** Moved to Nov 5-14. `Docs/SL05_SETUP_RECEIPT_20261001.md`.

**RO-11 - QUEUED 2026-10-09, Claude.** YouTube Sun Dec 13, socials Mon. Then: captions, article, links. `Docs/RO11_SETUP_RECEIPT_20261009.md`.

**RO-06 - QUEUED 2026-10-13, Claude.** YouTube Sun Dec 27, socials Mon. Then: captions, article check.

**Video 5 setup - 2026-10-11, Claude.** Queue blocked (200 cap). Task `abs40-vs-25-blotato-queue` queues Jan 3 2027 on Oct 12. `Docs/ABS40VS25_SETUP_RECEIPT_20261011.md`.

**Muhammad-Shorts QUEUED 2026-10-13.** DS-05 waitlisted 10-16; queued: set Edit Queue uploaded. `Docs/MUHAMMAD_SHORTS_SETUP_RECEIPT_20261013.md`

**RA-07 POLICY-RECHECK 2026-10-20, Claude.** 10-21: `node scripts/ads/api/client.js policy 24316364155`; clean, delete.

**Invest In Your Health 2026-10-20, Claude.** Videos 1, 2 (RO-20, RO-20B) finalized; setup handoff written. Video 3 (RO-20C) R5 handed off (new intro split, two lip-synced excuse clips). Both in `Handoffs/README.md` OPEN. C1722 sidecar mark-used pending (Seagate unplugged).

**RA-05:POLICY-RECHECK:2026-10-16:Claude.** Live: `0DswKDBFW2E`, ad `828398569805` in review. Next 10-17: `node scripts/ads/api/client.js policy 24316364155`; clean, delete this.

**RA-14 POLICY-RECHECK 2026-10-15,Claude.**

**RO-17 - HOLD 2026-10-18, Claude.** On the waitlist (Blotato 197/200); routine queues YouTube Sun Dec 13, socials Mon Dec 14 noon. `Docs/RO17_SETUP_RECEIPT_20261018.md`.

**RA-04 POLICY-RECHECK 2026-10-16,Claude.**

**RA-06:POLICY-RECHECK:2026-10-16:Claude.** Ads `828274063389`, `828320387740` in review. Next 10-17: `node scripts/ads/api/client.js policy 24316364155`; clean, delete this.

**Celebrity Ozempic LFC R4 - HANDOFF 2026-10-27, Claude.** Dan approved R3 and LOCKED the green-screen template as the long-form standard. Next: Opus 5.5 high fires the R4 handoff (whole film, AI frames A1/A3/A4/A6/A7/A8); R4 pins itself, unpins R3. `Handoffs/handoff-20261025-ro24-celebrity-ozempic-round4.md`.

**RO-14:QUEUED-JAN3-2027:2026-10-22:Claude.** `Docs/RO14_SETUP_RECEIPT_20261022.md`

**RO-20C HOLD 2026-10-21, Claude.** Waitlist, Dec 6. `Docs/RO20C_SETUP_RECEIPT_20261021.md`

**Zepbound Even If Ripped LFC R3 - REVIEW 2026-10-22, Claude.** Full film, page :8930. Next: Dan; then setup handoff.


**Ad 6 remarketing 2026-10-04:** Awaiting Dan: copy to enabled campaign 24305381214?

**RO-19 HOLD 2026-10-13.** `Docs/RO19_SETUP_RECEIPT_20261013.md`

**RO-08 HOLD 2026-10-14.** Jan 24 2027; B test after. `Docs/RO08_SETUP_RECEIPT_20261014.md`

**RO-07 - HOLD 2026-10-11, Claude.** Blotato full. `Docs/RO07_SETUP_RECEIPT_20261011.md`

**SL-07 HOLD 2026-10-18, Claude.** Covers picked, media and configs ready; Blotato full, five shorts on the waitlist for Dec 21-29. Next: the daily top-up routine queues them as slots free. `Docs/SL07_SETUP_RECEIPT_20261018.md`

**RO-12 - QUEUED 2026-10-01, Claude.** Blotato Oct 25. Then: `Docs/RO12_SETUP_RECEIPT_20261001.md`, delete.

**RO-13 - QUEUED 2026-10-07, Codex.** Sun Nov 15, 9 AM CST. Then: thumbnail A/B, captions, article. `Docs/RO13_SETUP_RECEIPT_20261005.md`.

**RO-10 - QUEUED 2026-10-07, Codex.** R3 YouTube 5287937: Nov 29, 9 AM CST. Original Private; socials live. Next: verify release, captions, article, SL-08. `Docs/RO10_SETUP_RECEIPT_20261002.md`.

**RO-16 - QUEUED 2026-10-02, Claude.** Blotato Nov 1 9AM CST. Owes: RO-12 link in description after Oct 25; captions, article after Nov 1. `Docs/RO16_SETUP_RECEIPT_20261002.md`.

**Stashed edits - NEEDS OWNER 2026-09-29, Claude.** Upstream kept: softblue.py, SOFTBLUE.md, GRAPHICS-STANDARDS.md, deliver/gate.py, coverimage SKILL.md, 00-MASTER.md, jobs.json. Edits: `stash@{0}` (5d8284a). Next: re-apply.

**SL-04 shorts - QUEUED 2026-10-13, Claude.** Last: Nov 3. `Docs/SL04_SETUP_RECEIPT_20260930.md`.

**RO-05 salad - QUEUED 2026-09-30, Claude.** Oct 18: fire `handoff-20260930-ro05-captions-and-article-after-release.md`.

**STOP Deadlifting clip - NEEDS DAN 2026-09-20, Codex.** R3 review copy in shared Drive folder `1dXUbQajUzM-uO_Xl92telO0qsa-Ob7uV`: full head visible, bar path rises once. Next: Dan approves R3 or names corrections.

**Overnight edit queue - PAUSED 2026-09-24, Dan's call.** Resume only if Dan says: `dispatcher.py resume`.

**Ads 6, 7, 10, 14 YouTube + Google Ads - REVIEW 2026-09-15, Codex 01a0a744.** Four unlisted uploads, eight enabled campaign ads, shared budget $40/day, policy `REVIEW_IN_PROGRESS`. Next: re-run policy; swap in Ad 7 typo / Ad 14 bitrate exports when delivered. Detail: `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**RA-01 square + headline swap - LIVE 2026-10-02, Claude.** Square ad `826755066385`. Dan's new long headline on 7 trial ads (old one CLICKBAIT). 10-03: `node scripts/ads/api/client.js policy 24316364155`; if flagged, rewrite only that line. `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**Trial thumbnails - INSTALLED 2026-10-02, Claude.** 10-03: recheck policy `24316364155`. 10-09: CTR vs week before 10-02 11:17 CT. `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**Trial `24316364155` LIVE, remarketing `24305381214`/`24316408288` PAUSED, 2026-10-01, Claude.** 10-04: delivery+policy. `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

**Web push storage — OPEN 2026-09-15.** Move `push-subs.json` to Postgres before enabling web push.

**PostHog signup funnels — OPEN 2026-09-15.** Rebuild `account_signup` funnels after the web-cart changes. Next: assign a session.

**Published cutdown audio — UNOWNED 2026-09-15.** 21 of 23 V2/V3/V6 cutdowns miss −14 LUFS. Next: scope remediation from `Docs/BOARD_REFERENCE.md`; preserve editor mixes under the standing audio rule.

**Google Ads policy checks - OVERDUE (baseline 2026-09-15).** `node scripts/ads/api/client.js policy 24243839443` (Ad 3 ads incl. squares 824906283483/824906283486; DGen r2 824329225648/824329225651; Ad 5 groups), then `… 24148587722` / `… 24086091285`. If r2 limited again: text-free thumbnail on `1oEcwdp21Fg`, then remove. ⚠ Ad 5 headline "Why My Diets Kept Failing" DISAPPROVED. Zeeshan Ad 1 / Ad 5 verticals only after Dan approves. `Docs/DGEN_CONVERSION_CAMPAIGN.md`

**Ads 3 + 4 in Demand Gen — LIVE 09-11.** Watch the new groups; delete after days of data. Dashboard row "Add the new finished ads…" open for Ad 1 verticals only.

**Scheduled posts — confirm and delete.** $17 Ab Wheel `bkzT-3ENpoU` public 09-13; its 5 shorts post Oct 27–Nov 5.
Zeeshan Ab Wheel Workout `b_bS9NdmL-g` public 09-20: confirm the Studio thumbnail test started. `BLOTATO_QUEUE_PROGRESS.md`

**Google Ads custom segments — 9 OF 12 BUILT 09-08, resume fresh.** Left: 7a/7b/7c (app picker), `website | member hub |
540 day` list, Phase 2 if the Demand Gen draft exists. ⚠ No pointer events or `await` in `javascript_tool` on a busy Ads
tab; stop rather than click into spinners. `Handoffs/handoff-20260908-google-ads-custom-segments.md`

**RO-03 - QUEUED 2026-10-10, Claude.** YouTube Dec 20, socials Dec 21. Then: captions, article. `Docs/RO03_SETUP_RECEIPT_20261010.md`.

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

List: `Handoffs/README.md` (OPEN section). Add new handoffs there, never here.
