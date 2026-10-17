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

**RO-26 R5 REVIEW 2026-10-17, Codex.** Two requested revisions, full film, subtitles and complete QA delivered at `:8982/r5/` and `Videos to Review`. Full gate FAIL: 31/39 pass; three inherited crop flashes remain open. Next: Dan reviews. Shared recap code committed locally; cloud sync blocked by other live-session edits, none adopted. Detail: `Docs/RO26_R5_DELIVERY_RECEIPT_20261017.md`. No platform upload or publishing.

## Working rules

1. One owner per task; no overwriting without handoff or review request.
2. Update on start, block, handoff or finish. **Re-read from disk first; edit only your entry.**
3. Finished and approved → **delete the entry**, durable details first; report in chat.
4. Budget: ≤2,500 words; entries ≤80 words, dated. Run `scripts/board-check.sh` after edits.
5. Dates: `Updated: YYYY-MM-DD`; keep `Decision since: YYYY-MM-DD`. Aging: `Docs/BOARD_MORNING_MAINTENANCE.md`.
6. Entry, ≤3 lines: `**Title — STATUS date, owner.** State. Next: action. ⚠ = changes next action. Detail: path.`

---

# ACTIVE

**RO-25 R6 BUILDING 2026-10-17, Codex.** Dan approved exact one-pill START/new open-bottle END and $25 cumulative motion cap; approved-pair 10s take4 is processing, estimated cumulative $17.50 including three rejected takes. Free clock, bed, lotion, recap, X audio and six intros built; audio numeric gates FAIL. Next: whole-take naturalness/independent review, then limited R6 opening and component page if passing. Detail: `/Volumes/Extreme/_edit_work/RO-25/round6/WORK_PACKET.md`.

**AI Took Job AD Setup PICK 2026-10-17, Codex.** Five unique Codex thumbnail choices delivered in 16:9 and 9:16. Both approved R4 masters verified unchanged. Next: Dan picks, then upload both Unlisted and add RA-16 to trial 24316364155. No upload or Ads write yet. Detail: `Docs/RA16_SETUP_RECEIPT_20261017.md`.



**RA-13 POLICY-RECHECK 2026-10-17, Codex.** Both R3 films are Unlisted and processed; trial group 201534026375, ads 828468045056 / 828468037364 ENABLED, review pending. Next 2026-10-18: `node scripts/ads/api/client.js policy 24316364155`; if clear, delete this entry. Receipt: `Docs/RA13_SETUP_RECEIPT_20261017.md`.

**RO-26 RULE SYNC BLOCKED 2026-10-17, Codex.** Dan reviewed R4; the ready R5 handoff is in `Handoffs/README.md`. New graphics guidance is saved locally in AGENTS, VIDEO-RULES and the long-form skill. `safe-push.sh` committed `0534f03` and `ee3e292` locally but exited 2 on six live other-session files. Next: retry only after those owners clear; do not adopt their work. R4 stays a review baseline, no upload.

**Main Git cloud read BLOCKED 2026-10-16, Codex.** Main-folder fetch waits on an iCloud-evicted local object, `.git/objects/29/f0dd02ad6df53b23db29ba79c5dcda29923390`. Download requested; object absent from GitHub. RA-13 records safely pushed via clean checkout, commit `f3d725b`. Next: restore that local object before main-folder pushes. No other session files or refs changed.






**Voice P2C commits UNPUSHED 2026-10-16, Claude.** Two local commits (bench fix, pilot results) wait on main; safe-push stopped on live edits to the board, DAN_DECISIONS, 00-MASTER, jobs.json. Next: any safe-push from the main folder carries them; then delete this.

**RO-04:R1-REVIEW:8974:2026-10-15:Codex**
**COVERS:MOBILE:2026-10-15:Docs/COVER_AUDIT_20261015.md**

**SL-08:PICKS:2026-10-14:Codex.**

**SL-09:PICKS:2026-10-15:Claude.**




**/start video test RUNNING 2026-10-10, Claude.** Reads 10-24, 10-31: `Docs/VSL_LANDING.md`.

**Waist-cover 2026-10-08.** TikTok phone upload pending.


**Meta follower test - RUNNING 2026-10-08, Claude.** Auto-boost OFF; one $40/day ad self-runs Oct 16-22. Nov 1 report: `Docs/AUTO_BOOST.md`.


**RO-01 - QUEUED 2026-10-07, Codex.** Dec6/7. TikTok direct Dec7. Next: release check. `Docs/RO01_SETUP_RECEIPT_20261007.md`.

**Video Views - HANDOFF 2026-10-07, Codex.** `24321429584`: $2 CPV, $5/day, zero spend. Thumbnail: `Handoffs/handoff-20261007-belly-fat-emergency-thumbnail-replacement.md`. Next: Oct 8 spend check.



**Nightly footage - COPYING ACTIVE 2026-10-17, Codex/Claude.** Seven shoots, including 10/15, checksum verified on Seagate and Drive. Nightly 8 pm copy-only routine remains active. Extreme originals remain; deletion paused. Next: decide the offload rule before enabling deletion. Detail: `Handoffs/handoff-20261005-claude-nightly-footage-offload.md`.

**Repository merge blocked 2026-10-17, Codex.** The verified footage status is committed locally, but `safe-push.sh` stopped on conflicts in `Docs/DAN_DECISIONS.md`, `Handoffs/README.md`, and `Handoffs/handoff-20261016-ds05-correct-version.md`. Next: hand merge those files, then push. Do not commit more on top.

**Codex revisions recovery - OPEN 2026-10-05, Codex.** Tool fixes and test Doc delivered; external video judge failed the known case. Fresh passes: 0. Next: eligible short plus sealed Claude Doc, then complete motion/AI coverage and blind comparison. Keep Claude editorial default. Detail: `Handoffs/results-20261005-codex-revisions-quality-recovery.md`.




**Ad13 setup REVIEW 2026-10-04.** Policy 10-05: `Docs/AD13_VERTICAL_SETUP_RECEIPT_20261004.md`.


**Oura review (Video 4) - QUEUED 2026-10-07, Codex.** Sun Nov 8, 9 AM CST. Then: thumbnail A/B, captions, article. `Docs/OURA_SETUP_RECEIPT_20261002.md`.

**PMax `24308574894` - LIVE 2026-10-02, Claude.** Checks 10-07, 10-12: `Docs/DGEN_CONVERSION_CAMPAIGN.md`. Campaign images: package.





**SL-05 shorts - QUEUED 2026-10-13, Claude.** Moved to Nov 5-14. `Docs/SL05_SETUP_RECEIPT_20261001.md`.

**RO-11 - QUEUED 2026-10-09, Claude.** YouTube Sun Dec 13, socials Mon. Then: captions, article, links. `Docs/RO11_SETUP_RECEIPT_20261009.md`.

**RO-06 - QUEUED 2026-10-13, Claude.** YouTube Sun Dec 27, socials Mon. Then: captions, article check.

**Video 5 setup - 2026-10-11, Claude.** Queue blocked (200 cap). Task `abs40-vs-25-blotato-queue` queues Jan 3 2027 on Oct 12. `Docs/ABS40VS25_SETUP_RECEIPT_20261011.md`.

**Muhammad-Shorts QUEUED 2026-10-13.** DS-05 waitlisted 10-16; queued: set Edit Queue uploaded. `Docs/MUHAMMAD_SHORTS_SETUP_RECEIPT_20261013.md`

**RA-07:R6-STAGE2-HANDOFF:2026-10-17:Claude.** Dan approved the phone frames. Next: fire stage 2 of `Handoffs/handoff-20261016-ra07-fire-your-trainer-round6-trim-and-phone.md` (motion, full film, gates). $12 of $20 spent. Commits d8f5c20, d398cc9 local: push blocked by live edits; next safe-push carries them.

**RO-20/B/C:R3b-REVIEW:8868:2026-10-16:Claude.** Studio pickups laid in. Next: Dan's pickup A/B + sign-off answers, then three films (handoff step 2).


**RA-15 setup PICK 2026-10-17, Claude.** Dan rejected round 1; round 2 sheet (3 designs, NUTRITIONISTS DESPISE HIM) waiting his pick. Next: upload both Unlisted, trial group, policy. `Handoffs/handoff-20261016-ra15-setup.md`

**RA-05:POLICY-RECHECK:2026-10-16:Claude.** Live: `0DswKDBFW2E`, ad `828398569805` in review. Next 10-17: `node scripts/ads/api/client.js policy 24316364155`; clean, delete this.

**RA-14 POLICY-RECHECK 2026-10-15,Claude.**

**RA-12:R1-REVIEW:8842:2026-10-15:Claude.**

**DS-31:R1-REVIEW:8931:2026-10-15:Claude.**

**RA-04 POLICY-RECHECK 2026-10-16,Claude.**

**RA-06:POLICY-RECHECK:2026-10-16:Claude.** Ads `828274063389`, `828320387740` in review. Next 10-17: `node scripts/ads/api/client.js policy 24316364155`; clean, delete this.

**RO-17:R4-REVIEW:8880:2026-10-15:Claude.**

**RO-14-R1-REVIEW:8964:2026-10-14.**

**RO-18:R1-REVIEW:8981:2026-10-16:Claude.** `handoff-20261015-ro18-round2-full-film.md`

**Ad 6 remarketing 2026-10-04:** Awaiting Dan: copy to enabled campaign 24305381214?




**RO-19 HOLD 2026-10-13.** `Docs/RO19_SETUP_RECEIPT_20261013.md`

**RO-08 HOLD 2026-10-14.** Jan 24 2027; B test after. `Docs/RO08_SETUP_RECEIPT_20261014.md`

**RO-07 - HOLD 2026-10-11, Claude.** Blotato full. `Docs/RO07_SETUP_RECEIPT_20261011.md`


**SL-06:R2-REVIEW:8819:2026-10-16:Claude.** All six delivered, gated. Commits b1e35a1, 2a22a47 local: push blocked by live edits; next session runs safe-push. Next: Dan's review.

**SL-07:R3-REVIEW:8874:2026-10-16:Claude.** All five pass review and gate 39/39. Next: Dan replies on the page, then `Handoffs/handoff-20261016-sl07-round4-after-dan-r3-review.md`.

**RO-12 - QUEUED 2026-10-01, Claude.** Blotato Oct 25. Then: `Docs/RO12_SETUP_RECEIPT_20261001.md`, delete.

**RO-13 - QUEUED 2026-10-07, Codex.** Sun Nov 15, 9 AM CST. Then: thumbnail A/B, captions, article. `Docs/RO13_SETUP_RECEIPT_20261005.md`.

**RO-10 - QUEUED 2026-10-07, Codex.** R3 YouTube 5287937: Nov 29, 9 AM CST. Original Private; socials live. Next: verify release, captions, article, SL-08. `Docs/RO10_SETUP_RECEIPT_20261002.md`.

**RO-16 - QUEUED 2026-10-02, Claude.** Blotato Nov 1 9AM CST. Owes: RO-12 link in description after Oct 25; captions, article after Nov 1. `Docs/RO16_SETUP_RECEIPT_20261002.md`.

**Studio posts - PARTIAL 2026-10-03, Claude.** 40 of 54 live; plan cap blocked 14 FB. Next: as slots free, `studio27_queue.py plan`, `create`. `Docs/STUDIO27_BLOTATO_QUEUE_RECEIPT_20261003.md`

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
