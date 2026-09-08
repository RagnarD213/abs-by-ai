# Abs By AI — Coordination / Status Board

**This file is loaded in full into every Claude Code message in this project, so it is
deliberately short.** It is a STATUS BOARD, not a log: what is open right now, who is
blocked, and the exact next action. Nothing else belongs here.

Everything that happened before 2026-09-02 — every completed task, measurement, trap and
lesson — is in [`AI_COORDINATION_ARCHIVE.md`](AI_COORDINATION_ARCHIVE.md) (1 MB, NOT
auto-loaded; read it only when you need history on a specific past decision). Git history
is the permanent record of code changes.

## Where things actually live — check these before writing anything here

| what | where it belongs |
|---|---|
| a technique, trap, recipe or measured calibration | the relevant **skill** (`.claude/skills/…`) — commit it there |
| what changed in code and why | **git history** |
| work spec'd but not yet executed | a doc in **`Handoffs/`**, listed in the HANDOFFS section below + `Handoffs/README.md`; on the dashboard's **Handoffs to fire** list ONLY if Dan asks (cap 7, deleted when run) |
| durable facts about Dan, the product or providers | **memory** (`~/.claude/projects/…/memory/`) |
| standing rules and authorizations | **`AGENTS.md`** / **`CLAUDE.md`** |
| open state between sessions | **here**, in three or four sentences |

## Working rules

1. One assistant owns implementation of a task at a time. Don't continue or overwrite
   another session's unfinished work without an explicit handoff or a review request.
2. Update this file when you start, get blocked, hand off, or finish — a few factual
   sentences, never a transcript.
3. **Re-read this file from disk before finishing a task**, not just before starting.
   Another session may have written to it; edit only your own entry.
4. When a task is finished, delivered and approved, **delete its entry** rather than
   marking it complete. Put anything durable in the right place from the table above.
5. When you write a handoff doc for work not yet executed, list it in the HANDOFFS section
   below and in `Handoffs/README.md`. **Do not add a dashboard task for it unless Dan explicitly
   asks** (Dan's rule 2026-09-08). Remove it from both lists in the session that executes it.

---

# OPEN — waiting on Dan

**Editor rounds out 2026-09-08 — waiting on the editors, nothing for a session to do.** Dan reviewed, edited and
sent all eight docs on 09-08 (Muhammad Ads 3–8 in the batch-2 doc, Waleed round 3 in a new doc, Zeeshan round 3 at the
top of his doc). Next deliveries get the same sweep; the skill was recalibrated from his edits (calibration pass 2,
rules 12–21). The scripts doc's three before/after cue lines (Ad 5, Ad 6, Ad 8) were corrected 2026-09-08.
Delete this entry once the next cuts arrive.

**IG auto-boost — BUILT, DEPLOYED, DRY-RUNNING HOURLY; waiting on Dan's word to switch it ON** (2026-09-02).
`scripts/ads/auto-boost.js` runs on Railway cron service `auto-boost` (`15 * * * *`, commit `51989d7`),
`AUTO_BOOST_ENABLED=0` so every run is a dry run that plans and records but writes nothing to Meta.
The dry-run report was shown in chat: it would rename the campaign/ad set, and create one $5 test on the
Sep 2 "Pick a sport" image post. **To go live Dan says the word and a session sets `AUTO_BOOST_ENABLED=1`
on that service** (`railway variables --service auto-boost --set AUTO_BOOST_ENABLED=1`). First Railway run observed 00:15 UTC 2026-09-03 (exit 0, run recorded). ⚠ `instagram_profile_visits` is
now reporting (5 visits on $0.10) but neither metric is count-matched to Ads Manager yet — the job self-verifies
(no loser verdicts, no champion kill until each metric is observed); the check is `node scripts/ads/auto-boost.js
--dry-run --verify` once spend exists, recipe in `Docs/AUTO_BOOST.md`. Delete this entry once enabled and the
first live run is observed.

**Ad-1 vertical audio — REBUILT, Dan listens** (2026-09-02). He rejected the audio on
`Muhammad Ad Videos/this picture got me abs/… | claude | 9x16.mp4` and attributed it to the
two-mic fault. **It was not that** — both delivered files measure L/R corr 0.99 at lag 0, and
the 9:16's audio IS Muhammad's mix (per-second corr 0.997). The cause was `loudnorm` silently
falling back to DYNAMIC mode (his master −18.2 LUFS at +0.0 dBTP, so a linear +4 dB lift is
impossible): it was swinging the gain +1.2→+9.5 dB second to second, 133 of 232 seconds pushed
up. Rebuilt as constant +4.2 dB + `alimiter=limit=0.85:level=disabled` → −14.5 LUFS, −1.3 dBTP,
picture stream untouched (6977 frames, `-c:v copy`). Master replaced in place; A/B + 540p sent.
New gate `/shortad-from-longform reference/gain_flatness.py` + skill rules committed (`a54686f`)
and cross-referenced from /shorts and /longform-edit. Delete this entry once he confirms.

**ManyChat per-topic keywords — DONE AND LIVE 2026-09-08, awaiting Dan's OK to delete this entry.**
`ABS` is split into six live keywords — ABS / FOOD / TRAIN / TRACK / SLEEP / COACH — each with its own
DM copy and `utm_campaign`. All 47 queued Instagram CTA captions rewritten to match (34 changed, 13 stayed
ABS); re-read from the API afterwards, every caption matches its topic, queue still 179, no media lost.
Verified live: commented FOOD from @abs.by.ai on `instagram.com/p/DdAIo4-j_RS/` → public reply
"Just sent it, check your DMs 📩" → the FOOD-specific DM. The second-beat link DM was NOT tapped
(Instagram **web** never renders ManyChat's quick-reply button, and typing its text does not fire it — the
payload is a postback, phone only); its `utm_campaign` was instead read straight out of each of the five
live automations. Ids, copy, keyword-collision reasoning and the editing traps: `Docs/MANYCHAT_KEYWORDS.md`.
Rewriter: `scripts/manychat/keyword_split.py` (idempotent, dry run by default).
The test comment and its auto-reply were deleted afterwards (post re-read: "No comments yet").
⚠ Instagram in Dan's Chrome is left signed in as **@abs.by.ai** (switched for the test) — switch it back to
@danrosefit; the extension wedged before it could be done.
⚠ The ManyChat account shows a **TRIAL** badge. If the Pro trial lapses, "any post or reel" dies for all six
keywords at once. Still open from the original build: whether to switch off Blotato's IG auto first-comment
(**ask before touching it**, queue-wide), and the CTA reels are eligible for the 2026-08-31 paid-ads specs.

**Website conversion video — REV 3 DELIVERED 2026-09-02 (~6 PM), awaiting Dan's review.** Same folder,
same filename (`claude edited long form content/06 - …/website_video_16x9.mp4`, 3:50); rev 2 is beside it as
`*_REV2_REJECTED`. Fixed from measurements: every crop anchored to his head (median headroom 201 → 53 px,
min 21, never cut), the repeated "I've been out of shape" cut, lower thirds at the bottom with captions
62–73 px clear (both now pixel-measured QC checks that FAIL rev 2's file). Audio chain unchanged and
approved; the new shared gate passes it. 540p review copy + audio A/B sent in chat; `notes.md` flags one
judgment call (the after-photos now start on "I have the most defined abs"). Recipe in the skill
(`ad-edit/reference/website-video/`, lessons 101–106). Delete this entry once Dan approves; the next step
after approval is installing it on absbyai.com (separate Key task).

**Exercise demos batch 4** — 9 final candidates delivered and sent in chat (kb-swing,
kb-deadlift, kb-goblet-squat, kb-row, kb-press, deficit-pushup, ab-wheel-rollout, step-up,
db-step-up), all gates green. Dan reviews; on approval stamp `-FINAL` and install per the
batch-2 recipe (**that install is a native-retest trigger**). `db-lunge` is blocked — Veo
drifts the camera on this large-translation move; options are full `google/veo-3.1`, Kling
with `end_image`, or filming it. Batch dir `Media/exercise-demos/_batch4/`.

**04 invest-health — DELIVERED 2026-09-03, awaiting Dan's review.** `claude edited long form content/04 - …/
FINAL_invest_health.mp4` (29:16, sub30 + therapy beat, clean frame + `.srt`), with the audio-gate stamp, A/B clip
and `REVIEW_540p_invest_health.mp4` beside it; the 53:17 v3 is `FINAL_invest_health_PRE_REBUILD.mp4`. Gates:
audio 11/11, style 14/14, watch 65/65 graphics + frozen runs 40 → 2. Audio went through `_shared/audio` (bed at
−36 dB — −30 failed the floor row; lesson recorded in the skill). Rollback copies in the work dir
`/Volumes/Extreme/_edit_work/invest-health-cutdowns/style/*_PRE_DRIFT*`. Delete this entry once Dan approves;
next is /youtube-packaging (thumbnail + Shorts) — a Key task if he wants it.

**Longforms 02 + 03 — HOLD EXPIRES 2026-09-09 AND MUHAMMAD HAS DELIVERED NOTHING.** Checked Drive
2026-09-08: his only delivery since Sep 1 is `Daniel HQ Ad 2 V2 HD.mp4` (Sep 3) — no Zepbound and no
Supplements edit exists, shared or otherwise. **Dan's own rule says ours go up as they are if Muhammad
never gets to them, so on 09-09 this becomes his call to make.** Note Claude cannot do the upload (see
the 10 MB cap below).

**Longforms 02 + 03 — ON DELIBERATE HOLD UNTIL DAN DECIDES. DO NOT UPLOAD.** Both are cut,
packaged and thumbnailed and are staying in the project folder. **Dan's call 2026-09-02: he is
sitting on them until Muhammad delivers his own edits of the same two videos.** If Muhammad's are
significantly better, his ship and ours become the backup; if Muhammad never gets to them, ours go
up as they are. **Nothing about this is blocked on a session — do not offer to upload, and do not
treat it as an open task before 2026-09-09.**
⚠ Verified in Studio 2026-09-02: neither video exists on the channel (8 videos, neither is these),
so no thumbnail is installed and no A/B test exists. **Claude cannot upload them anyway** — the
Chrome extension's `file_upload` is capped at **10 MB** against files of 1.30 GB and 0.91 GB, and
the stored `GOOGLE_REFRESH_TOKEN` is calendar-scoped. Thumbnails, at ~150 KB, DO upload through
`file_upload` — that supersedes the clipboard-paste trick in `/youtube-packaging`.
**Reminder wired, not left to memory:** a dormant self-deleting block in the morning-brief task's
`SKILL.md` wakes on **2026-09-09** and prints a pinned "Still on you" row every morning until he
resolves it. There is no dashboard row for this any more (board cleared 2026-09-08); the brief's block is the only reminder. **Whoever closes this out must delete
the block from the brief's SKILL.md**, or it nags forever.
**16 cut Shorts (8 per video) stay blocked until one version or the other is public.**

**Zepbound shorts** — 8 delivered (`zep-short1..8_*.mp4`), **audio re-rendered 2026-09-02 through
`_shared/audio`** (room 69–93 ms → 32–48 ms, every file stamped PASS; pre-fix copies in
`Short-form video content/_pre-audiofix-20260902/`; A/B clips `AB_his-vs-ours_zep-short1/2…mp4`).
Dan says which to swap for one of the six alternates in `SHORTS.md`. ⚠ Picks were mine, not his.
**Posting is blocked on the parent long-form, which is on a deliberate hold** (above). Do not chase.

**Spray tan shorts (01) — REV 1, audio rebuilt** — 6 delivered (`tan-short1..6_*.mp4`), down from
8: Dan killed the briefs/boxers and first-shower shorts and retitled two. All gates green (QC,
sync 8/8, centering 8/8, new audio gate). $0.00 AI spend. 540p copies + an audio A/B sent.

⚠ **HE REJECTED THE AUDIO AND ATTRIBUTED IT TO THE TWO-MIC FAULT. IT WAS NOT THAT** — the
delivered file measured **+0.9912** against the source's RIGHT channel through the same EQ (left
0.60, sum 0.69). **The cause was ROOM REVERB, which nothing in the pipeline had ever measured:
early decay 85 ms against his reference ad's 40 ms.** Fixed with spectral dereverb
(`work/dereverb.py`) → **29–40 ms**; new hard gate `work/audiogate.py` is wired into `qc.js` so
no batch from this shoot can ship again without the room being measured.

⚠ The same room was in the Zepbound and supplements Shorts — **fixed 2026-09-02** through
`.claude/skills/_shared/audio/` (one lav pick, one chain, one gate; every QC requires its stamp).

⚠ Three bugs found on the way, all documented in the batch README: a stereo WAV read as mono is
invisible to a byte-size check (cost a full render, 11–16 dB above 450 Hz); `finishaudio` was
matching the batch to its own median rather than the reference; and it predicted its EQ instead of
verifying it. **Short 2 measures 1.08 dB shape against a 1.00 gate** — one band, 2.7 dB bright at
6.7 kHz; reported rather than hidden, and the threshold was not relaxed.

**Supplements shorts (03)** — 8 delivered, **audio re-rendered 2026-09-02 through `_shared/audio`**
(room 67–88 ms → 29–45 ms, every file stamped PASS; pre-fix copies in
`_pre-audiofix-20260902/`; A/B clips beside supp-short1 and supp-short4). Same block: the parent
long-form is on hold (above), so nothing can post. Parked, not chased.

**AD 2 vertical 9:16 — REBUILT AGAINST MUHAMMAD'S V2 HD, DELIVERED 2026-09-03 (final 14:09), awaiting Dan's review.**
`Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/stop wasting money on nutritionists | claude | 9x16.mp4`
(+ `REVIEW_540p_9x16.mp4`, `REVIEW_480p_9x16_phone.mp4`, `AB_audio_his-vs-ours.mp4`, gate stamp, `notes-vertical-v2.md`,
`recipe-vertical-v2/`). His V2 differs from V1 in five windows only; all five conformed to his frames. **His V2 shows
the app's email-capture screen at 3:12 and 3:22 — banned; ours shows the after-only result (tell Muhammad).** Two
independent Fable audits: the first found our talking head cutting the picture at every AUDIO splice where he cuts on
a pose-matched frame nearby → his picture cut recovered at 26 of 33 splices and the base re-conformed to them; the
second found a duplicated frame after cuts and a one-frame crop miss at the cut → both fixed and re-measured on the
delivered file (every cut ≤ 70 px at the frame before/at/after, 0 duplicates; centering sd 18 px, 2/319 beyond 70).
QC 20/20, watch pass, shared audio gate (reference-mix mode) on the delivered file; −14.7 LUFS / −1.1 dBTP.
Work dir `/Volumes/Extreme/_edit_work/ad2-vert-v2/`; rev 3 stays in `EDITED ADS 8-20-26/ad2-fire-your-nutritionist/`.
Then Phase B: Dan cuts `SCRIPT_FOR_DAN.md` to ~200 words for the 0:59 — **Dan cuts it himself**. Delete this entry
once he approves.

**Cutout thumbnails** — six built in the Brandon Carter style (A/B/C typographic, D/E/F
device-heavy) in `social media graphics/youtube/thumbnails/The 17 Dollar Ab Wheel…/`. Dan
picks from the compare sheets, or says which devices to push. On a pick: install in Studio
and load a second as the A/B test per `/youtube-packaging`.

**3-min total body workout thumbnails** — A/B/C delivered, Dan picks one, then it gets
installed in YouTube Studio.

**Ab-wheel shorts covers** — 10 built (A and B per short, IG + YouTube). Dan picks A or B
for each of the five; then delete the losing variant. Not installed on YouTube by design.

**Studio batch 6** — all four waves delivered, 100 finished picks. 14 of wave 4's 15 are
finalized; **White-49 rev 2 is awaiting Dan's word.** The moment he approves it, check off
the Key dashboard task `money::Execute handoff: studio batch 6…` — that closes the whole
programme. ⚠ 60 ` 2.jpg` conflict copies sit in the delivery folder (pre-warp-bump versions,
not duplicates); recommend deleting once he confirms the current files are the ones he wants.

**Home filming set** — final buy list ($1,083.65), 21 product pages open in his Chrome.
Dan buys (TL60 **qty 2**, stand 2-pack, rod 72-144, backdrop stand 10x8.5), then runs the
3 phone tests before the gear lands. Then: build the look-A telemetry loop file once the
monitor is in the room.

**Paid ads** — Dan fixes the Google Ads payment method ("New form of payment required"),
and decides whether both Meta campaigns being toggled OFF was intentional (3 unpublished
draft edits still pending). Launch specs are in the 8/31 artifact.

**Ads digest — BUILT AND LIVE, BLIND UNTIL DAN GRANTS TWO TOKENS** (2026-09-02). Daily
Meta + Google spend brief with anomaly and winning-ad detection; renders as an "Ad spend"
section in the morning brief. Engine `scripts/ads/ads-digest.js` → `brief-ads.json`, gated
`GET /api/ads-digest` (live-verified, 401 without the key). Dashboard task checked off.
⚠ **Neither platform is readable and both fixes are Dan's**: the stored
`FACEBOOK_PAGE_ACCESS_TOKEN` is a PAGE token with no `ads_read` (Graph returns "(#200) Ad
account owner has NOT grant ads_management or ads_read"), and `GOOGLE_REFRESH_TOKEN` is
`calendar.readonly` only with no developer token in existence. **Dan: the Meta fix is ~5
minutes — Business settings → System users → token with `ads_read` → `META_ADS_TOKEN` in
`~/.absbyai-secrets.env`.** Google needs the API handoff's Phase 1 first. The digest names
the missing credential in the brief every morning and goes quiet by itself once it lands —
no follow-up task. Setup paths, detection rules and the ~2x Google conversion correction:
`Docs/ADS_DIGEST.md`. Rules are tested against the 8/26 + 8/31 figures
(`scripts/ads/ads-digest.test.js`, 28 cases). The render spec lives in the morning-brief
task's `SKILL.md` (`~/.claude/scheduled-tasks/abs-by-ai-morning-brief/`), outside the repo.

**Resend read key** — delivery rates can't be queried; the stored key is send-only. Dan
creates a full-access key at resend.com/api-keys → `RESEND_READ_API_KEY` in
`~/.absbyai-secrets.env`.

**V4 and V5 longform Content ID claims** — local masters are fixed and delivered; the
claims on YouTube are still live. Dan decides: Replace song, or leave it (the claims cost
nothing until the channel monetises). ⚠ Both videos are live ad destinations — delete +
re-upload would change the video id and break the campaigns pointing at them.

---

# BLOCKED — external

**iOS submission `ccc7a7ae`** — **IN_REVIEW with Apple as of 2026-09-08** (was WAITING_FOR_REVIEW
since 2026-08-26; 5.1.1(v) argued, UX fixed, no new binary). A reviewer has picked it up — expect an
approval or a rejection within a day or two. Fallback if they hold the line is spec'd at the bottom of
`app-store-assets/APP_REVIEW_REPLY_20260826_G511v.md`. Status check:
`GET /v1/apps/6794097836/reviewSubmissions` with the ASC key (`~/.appstoreconnect/private_keys/AuthKey_D7UC9KJD3B.p8`).

**IG image gap-fill** — 63 of 70 scheduled. The last 7 are blocked on Blotato's 200-post
plan cap; Dan either deletes queued posts or upgrades. Then re-run
`scripts/blotato/iggap_fill.py --apply` (idempotent). ⚠ The queue is now **exactly 200/200**
(TikTok mirror, 2026-09-02) and drains ~2/day.

**TikTok via Blotato — LIVE, one restore left.** To make queue room, the 6 latest Facebook photo mirrors
(2027-01-04 → 01-15) were removed and saved to `scripts/blotato/fb_trimmed.json`; run
`tiktok_mirror.py --restore-fb --apply` once the 200/200 queue has room, then delete this entry.
(The `Post on TikTok` dashboard row was removed 2026-09-08 — posting is automated.)

**Blotato queue — one genuine open failure:** post `667411` (2026-08-18, "My ten best tips…")
exceeded the **400 MB Blotato plan cap**. Long-form masters are ~1.1 GB / 11 Mbps and the queue's
transcodes land ~322 MB, right against that ceiling; re-encode smaller before re-queuing. No other
queued video is close (largest is 197 MB, TikTok 09-21). ⚠ A Blotato `failed` state on a big video
is not proof — verify against the platform's API first (memory: `blotato-false-failure-large-video`).

**Google Ads conversion goals** — Purchase still reads Misconfigured and Campaign diagnostics
shows "connection failed its last run" + a stale "Unparseable gclid (Aug 27)". **Root cause verified
2026-09-02: the feed is EMPTY because no sale has ever happened** — the one real trial (annual, real
gclid) was declined at trial end on Sep 1 and the customer deleted their account 3 minutes later.
Google cannot infer a schema from a header-only file (error 4000); it clears itself on the first paid
conversion. **Do not manufacture a row.** Fixed in code the same day (`ee91b26`): the trial→paid
stamp now comes from Stripe's `invoice.paid` (webhook endpoint updated), because Stripe flips a
subscription to `active` an hour BEFORE it tries the charge — the old rule would have reported a
$69.99 sale for a declined card. The Purchase/Subscribe tidy-up (delete the orphan action, rename
the auto-created one) still waits for a real row in the feed.

---

**IG profile-visits campaign — LIVE since 2026-09-02 ~18:00 CT.** Campaign `120250753198730682`,
ad set `120250753601020682` (**$6.50/day ≈ $200/mo, Dan's call 2026-09-02**) and both ads on the real @danrosefit reels are ACTIVE; ads
clear Meta review on their own. **After $50 spend: kill >$5/follow, scale <$3/follow** — the auto-boost job
applies exactly this once it is enabled (entry above); until then it is a manual check. Recipe: `scripts/ads/boost_danrosefit_posts.py`. ⚠ Never click the global
"Review and publish (7)". This ad set is the first CHAMPION of the auto-boost system
(`Handoffs/handoff-20260902-ig-auto-boost.md`). Delete this entry once the $50 review is done.

**Meta API access — WORKING.** `META_ADS_TOKEN` (system user `abs-automation`, never expires:
ads_management, ads_read, business_management, pages_show_list, pages_read_engagement,
pages_manage_posts, instagram_basic) + `META_APP_SECRET` in `~/.absbyai-secrets.env`.
⚠ The Business Settings token UI silently fails for ads scopes even for an app Administrator —
**mint via `POST /{system_user_id}/access_tokens` with `appsecret_proof`** (recipe in the handoff).
✅ `ads_read` verified 2026-09-02: `scripts/ads/ads-digest.js` now populates the Meta section
(spend, campaigns, anomalies). Google still blind pending the developer token.
✅ App `1598463548528030` is LIVE as of 2026-09-02 (dev mode blocked ALL API ad creatives, subcode
1885183). App-settings writes are disabled via API and Claude is platform-blocked from the settings
form — Dan fills Basic, Claude can click Publish.
⚠ Duplicate Page's real id is **`1348044195050800`** (9/01 handoff's `61593951123927` is its
business-asset id). Keeper `1380236418500031`. Not deleted. **Do not use the API to tell them
apart** — `instagram_business_account` reads empty for ALL pages, a false negative.
⚠ IG `explore` placement is deprecated in v21.0; campaigns now require `is_adset_budget_sharing_enabled`.

---

# HANDOFFS WRITTEN, NOT EXECUTED

Swept 2026-09-08. All four are on the dashboard's **Handoffs to fire** list (Dan's ask, 09-08) with their starter
prompts; whoever runs one deletes its row there AND removes it here and from `Handoffs/README.md`.

- **`Handoffs/handoff-20260812-revenuecat-restore-behavior-audit.md`** — fire the day Apple approves (IN_REVIEW).
- **`Handoffs/handoff-20260812-purchase-before-account.md`** — after approval AND after the RevenueCat audit.
- **`Handoffs/handoff-20260818-android-public-build-swap.md`** — small; needs Dan's Android phone on adb.
- **`Handoffs/handoff-20260826-danrosefit-abs-image-gap-fill.md`** — last 7 of 70 posts; re-run
  `scripts/blotato/iggap_fill.py --apply` from ~09-12 once the 200/200 Blotato queue has drained 7 slots.

Dead, do not run: `handoff-20260901-danrosefit-ad-identity-fix.md` (superseded — the @danrosefit profile-visits
campaign has been live via the API script since 09-02), `handoff-20260902-shorts-centering-queue-fix.md` (done
09-02), `handoff-20260902-google-ads-engagement-champion-automation.md` (built 09-03; only Dan's two clicks remain,
see ACTIVE TASK).

---

# ACTIVE TASK

**YouTube engagement champion (Google Ads) — BUILT, DEPLOYED, SCRIPT INSTALLED; waiting on two Dan clicks** (2026-09-03).
Brain live (`scripts/ads/ytads/`, 88 tests, `YTADS_ENABLED=0` = dry run); Ads Script id `12241942` saved in 342-717-0837
with the key, **unauthorized + unscheduled** (Google won't schedule before the OAuth grant). **Dan: (1) Tools → Bulk
actions → Scripts → Frequency pencil → Hourly → Save → Authorize → Grant access; (2) MCC API center form is filled in
his Chrome — tick the Terms box, click Create token, paste it into `~/.absbyai-secrets.env` as
`GOOGLE_ADS_DEVELOPER_TOKEN`.** Next session after (1): refine `headline-style.md` from the first snapshot, pin the
tier-1/RMKTG ids, show Dan the dry-run day-one pause list, set `YTADS_ENABLED=1`, watch the first live hour, then check off
the Key task. Execution notes at the bottom of the handoff; operating doc `Docs/YTADS.md`.

**Shorts centring queue fix — DONE 2026-09-02, one decision left for Dan.** Every queued off-centre Short is
replaced: Blotato 10 posts swapped + MD5-verified; YouTube 8 stale scheduled Shorts re-uploaded as new ids at
the same slots (old→new in `SHORTS_UPLOAD_PLAN.json`), the 8 old copies + killed `v6-short1` deleted;
`v6-short3`/`v6-short5` re-cut, `v6-short2` measured centred and left. Dashboard task checked off. **Dan:
the four already-PUBLISHED off-centre Shorts (`y0XIbNoA2Xo` 08-22, `P9VUGyWeNtY` 08-27, `VOlZHV1ibmU`
08-29, `rqyK5IDsxX0` 09-01) — delete + re-upload on the next open Tue/Thu/Sat slots, or leave them?**
Delete this entry once he answers.
