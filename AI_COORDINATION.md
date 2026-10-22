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

**Edit cap LIVE 2026-10-21, Claude.** Pushed; main folder mid-merge (not mine), so its skills lack it until merged. Next: delete after that merge.

**SL-17:NEEDS-DAN:2026-10-20:Claude.**
**SL-18:REVIEW:2026-10-21:Claude.** Wasted Life SFL R1 on :8996; awaiting Dan.

**Boring Abs At 40 LFC R2 - ACTIVE 2026-10-20, Codex.** Executing R2 handoff. Colour C and voice B locked; R1 preserved. Next: calibrated headroom proof, corrected opening/contexts, complete existing-AI gallery, revised A01–A04 still pairs and independent checks. No new motion or full-film render before approval. Work: `/Volumes/Extreme/_edit_work/ro27/round2/`.

**Calories Not Losing Weight SFL R5 - REVIEW 2026-10-20, Codex.** Standing-counter Snack on Protein, Not Carbs pair passed measured and independent checks. Narrated review: http://127.0.0.1:9042/. Next: Dan approves this pair before Flow. Fasting R4 frames approved; R2/R3/R4 untouched. No covers or publishing.

**Bill Maher Fat 90-Year-Old SFC R4 - ACTIVE 2026-10-20, Codex.** Full edit authorized with approved R3 key, Balanced audio and warm color. Separate build: `/Volumes/Extreme/_edit_work/DS-40-codex/round4/`. Next: scripted take, clip-first assembly, BMI graphic, captions and full QA. Claude competition remains separate.



**RO-25 thumbnail sync BLOCKED 2026-10-17, Codex.** Final thumbnail C and deferred setup handoff are saved with verified Extreme backups. Commit `4b5b483` remains local; safe-push stopped on live `qc_corpus/corpus.json` and `scripts/blotato/fb_reel_covers.json`, plus stale files listed by the tool. Next: retry after owners clear; do not adopt live edits. Setup handoff is indexed in `Handoffs/README.md` and waits for the approved final film.

**RO-25 Git sync BLOCKED 2026-10-18, Codex.** Public video, article post 886, and manually uploaded 257-cue English SRT are verified. Caption uploader and receipt are committed locally as `340ed22`. Safe-push aborted on nine merge conflicts across other sessions' files; no merge is in progress. Next: hand-merge shared main with owners or push these records from a clean checkout, without discarding their work.

**RA-09:ACTIVE:2026-10-21:Claude.** AI Changing World AD R1. `/Volumes/Expansion/_edit_work/RA-09/`.

**Fat 90 Year Old SFC R3 - REVIEW :8940 2026-10-21, Claude.** Opening delivered, reviewer SHIP (re-check 4). Next: Dan's notes. Work: `ds40/r3/` (Expansion).

**DS-44:ACTIVE:2026-10-21:Claude.**

**SL-15 Setup PICKS 2026-10-22, Claude.** Short 2 C; short 1 F/G at :9151. Next: Blotato after RO-19.

**I'm 41. I Wasted My Life. LFC Setup QUEUED 2026-10-17, Codex.** Dan approved exact R7 film and thumbnail C. Blotato readback: YouTube Sun Oct 18 9 AM, Facebook/Instagram Mon Oct 19 noon. Direct TikTok Monday after public YouTube check. To free capacity, Dan authorized removal of the last queued video, RO-13; its four schedules are backed up and RO-13 is on the waitlist for Dec 30. Receipt: Docs/RO25_SETUP_RECEIPT_20261017.md. Next: verify public release, covers, TikTok, RO-26 link.

**Release calendars LIVE 2026-10-17, Claude.** Long-forms Sun+Wed, Shorts Mon-Sat minus Wed/Sun (DS Thu); 105 Blotato posts moved, re-read. Dates: `Docs/LONGFORM_RELEASE_CALENDAR.md`, `Docs/SHORTS_RELEASE_CALENDAR.md` (override older RO/SL entries). Next: RO-25 setup when file lands; top-up queues RO-19 Oct 21. Local commits f47634a, 75fa6fb, fe42792 await safe-push (live files).

**Top 1 Percent LFC Setup - RELEASE HOLD 2026-10-17, Codex.** Dan's frosted A cover installed; media/Drive backups verified, article ready, SL-17 registered. RO-26 finalized, not queued. RO-25 setup/release owner: once public, add actual watch URL and clear both holds, then existing top-up queues Oct25/26 when room opens. Receipt: `Docs/RO26_SETUP_RECEIPT_20261017.md`. Git sync blocked by live other-owner edits; shared FB/index changes preserved locally.


**RA-16 POLICY-RECHECK 2026-10-17, Codex.** Exact R4 films Unlisted and processed; selected R2 thumbnail 3 installed/read back. Trial group 202854620044, ads 828352448280 / 828398913310 enabled, review pending. Next 2026-10-18: existing campaign policy process, `node scripts/ads/api/client.js policy 24316364155`; if clear, delete this entry. Receipt: `Docs/RA16_SETUP_RECEIPT_20261017.md`.



**RA-13 POLICY-RECHECK 2026-10-17, Codex.** Both R3 films are Unlisted and processed; trial group 201534026375, ads 828468045056 / 828468037364 ENABLED, review pending. Next 2026-10-18: `node scripts/ads/api/client.js policy 24316364155`; if clear, delete this entry. Receipt: `Docs/RA13_SETUP_RECEIPT_20261017.md`.

**RO-26 RULE SYNC BLOCKED 2026-10-17, Codex.** R5 finalized after Dan approval; setup handoff in `Handoffs/README.md`. Local commits include `0534f03`, `ee3e292`, `2145530`, `3ff330e`, `200ebe4`; safe-push still stops on live owners. Own RO-26 queue/index/QC updates stay local alongside their changes. Next: retry after owners clear; do not adopt live work. Final files and verified Extreme backup are available. See `Docs/RO26_R5_DELIVERY_RECEIPT_20261017.md`.

**Main Git cloud read BLOCKED 2026-10-16, Codex.** Main-folder fetch waits on an iCloud-evicted local object, `.git/objects/29/f0dd02ad6df53b23db29ba79c5dcda29923390`. Download requested; object absent from GitHub. RA-13 records safely pushed via clean checkout, commit `f3d725b`. Next: restore that local object before main-folder pushes. No other session files or refs changed.






**Continue-or-handoff rule UNPUSHED 2026-10-17, Claude.** Commits 204433a, 74e0fbb, 8e73dff (AGENTS, VIDEO-RULES, PRE-RENDER-APPROVAL: auto continue-or-handoff) are local; safe-push stopped on live edits by other sessions. Next: any later safe-push from the main folder carries it; then delete this.

**Veo Flow helper commits UNPUSHED 2026-10-17, Claude.** Commits c778a01, ca37c53 (subscription-first Veo rule, `_shared/veo/`, flow-veo agent) wait on main; safe-push stopped on live corpus.json and DAN_DECISIONS edits. Next: any safe-push from the main folder carries them; then delete this.

**Voice P2C commits UNPUSHED 2026-10-16, Claude.** Two local commits (bench fix, pilot results) wait on main; safe-push stopped on live edits to the board, DAN_DECISIONS, 00-MASTER, jobs.json. Next: any safe-push from the main folder carries them; then delete this.

**COVERS:MOBILE:2026-10-15:Docs/COVER_AUDIT_20261015.md**






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

**RA-07 POLICY-RECHECK 2026-10-20, Claude.** 10-21: `node scripts/ads/api/client.js policy 24316364155`; clean, delete.

**Invest In Your Health 2026-10-20, Claude.** Videos 1, 2 (RO-20, RO-20B) finalized; setup handoff written. Video 3 (RO-20C) R5 handed off (new intro split, two lip-synced excuse clips). Both in `Handoffs/README.md` OPEN. Queue commit ff69bf1 local (safe-push stopped on a live file); next safe-push carries it. C1722 sidecar mark-used pending (Seagate unplugged).


**RA-05:POLICY-RECHECK:2026-10-16:Claude.** Live: `0DswKDBFW2E`, ad `828398569805` in review. Next 10-17: `node scripts/ads/api/client.js policy 24316364155`; clean, delete this.

**RA-14 POLICY-RECHECK 2026-10-15,Claude.**

**RO-17 - HOLD 2026-10-18, Claude.** On the waitlist (Blotato 197/200); routine queues YouTube Sun Dec 13, socials Mon Dec 14 noon. `Docs/RO17_SETUP_RECEIPT_20261018.md`.

**RA-04 POLICY-RECHECK 2026-10-16,Claude.**

**RA-06:POLICY-RECHECK:2026-10-16:Claude.** Ads `828274063389`, `828320387740` in review. Next 10-17: `node scripts/ads/api/client.js policy 24316364155`; clean, delete this.

**RO-24:R1-REVIEW:9124:2026-10-21:Claude.**

**RO-14 R2 REVIEW 2026-10-21, Claude.** Page :8965. bad60e5 unpushed.

**DS-33:REVIEW:9033:2026-10-21:Claude.** 875d823 unpushed.

**RO-20C HOLD 2026-10-21, Claude.** Waitlist, Dec 6. `Docs/RO20C_SETUP_RECEIPT_20261021.md`

**Zepbound Even If Ripped LFC R2 - ACTIVE 2026-10-22, Claude.** Resumed. A5 retime review and first-minute chain running (no priority). Next: page :8929. `/Volumes/Expansion/_edit_work/ro28/round2/`.

**Make Time Exercise LFC R2 - REVIEW :8982 2026-10-21, Claude.** RO-18 full film delivered; VLC copy in Videos to Review. Next: Dan's notes.

**Ad 6 remarketing 2026-10-04:** Awaiting Dan: copy to enabled campaign 24305381214?




**RO-19 HOLD 2026-10-13.** `Docs/RO19_SETUP_RECEIPT_20261013.md`

**RO-08 HOLD 2026-10-14.** Jan 24 2027; B test after. `Docs/RO08_SETUP_RECEIPT_20261014.md`

**RO-07 - HOLD 2026-10-11, Claude.** Blotato full. `Docs/RO07_SETUP_RECEIPT_20261011.md`


**SL-06:NEEDS-DAN:2026-10-22:Claude.** Top 5 Zepbound Tips SFL R6: D approved. A, B, C, E, F intro approach waits on Dan (`Docs/DAN_DECISIONS.md`). Work: `/Volumes/Extreme/_edit_work/sl06/round6/`.

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

**Handoff-pin rule UNPUSHED 2026-10-18, Claude.** VIDEO-RULES + AGENTS: handoffs put up a card and stay pinned (Dan unpins); commits local, safe-push stopped on live edits. Next: any later safe-push carries them; then delete this.

**Engagement-ads rule UNPUSHED 2026-10-18, Claude.** Commit 3f10579 (AGENTS, YTADS, memory: new engagement ads go in tier1, tier2 and both rmktg ad groups) local; safe-push stopped on live corpus.json and ra16 prompt edits. Next: any later safe-push carries it; then delete this.

**Video-title rule UNPUSHED 2026-10-17, Claude.** Commit bd14929 (AGENTS rule, README) local; safe-push stopped on live edits. Next: any later safe-push carries it; then delete this.

**VEO-ULTRA:UNPUSHED-f034bc5..fc78746:2026-10-20:Claude.**

**10-23 TP docs UNPUSHED 2026-10-20, Claude.** Commit 65f8c43 local. Next: any safe-push carries it; delete this.

**IG-MEMORY:UNPUSHED-f597b51:2026-10-20:Claude.**

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

**Arms Shoulders Workout LFC R3 - REVIEW 2026-10-20, Codex.** Full film checked: http://127.0.0.1:8974/. Next: Dan reviews. Records pushed (`a65ebf7`); local merge awaits another session's live `jobs.json` edit.
