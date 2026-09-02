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
| work spec'd but not yet executed | a doc in **`Handoffs/`** + a Key task on the dashboard |
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
5. When you write a handoff doc for work not yet executed, add a Key-priority dashboard
   task for it (mechanics: the `/dashboard-tasks` skill). Check it off in the same session
   the work is actually executed.

---

# OPEN — waiting on Dan

**IG auto-boost — BUILT, DEPLOYED, DRY-RUNNING HOURLY; waiting on Dan's word to switch it ON** (2026-09-02).
`scripts/ads/auto-boost.js` runs on Railway cron service `auto-boost` (`15 * * * *`, commit `51989d7`),
`AUTO_BOOST_ENABLED=0` so every run is a dry run that plans and records but writes nothing to Meta.
The dry-run report was shown in chat: it would rename the campaign/ad set, and create one $5 test on the
Sep 2 "Pick a sport" image post. **To go live Dan says the word and a session sets `AUTO_BOOST_ENABLED=1`
on that service** (`railway variables --service auto-boost --set AUTO_BOOST_ENABLED=1`). ⚠ Two metric
strings are still unmatched to Ads Manager because the campaign had no insights yet — the job self-verifies
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

**ManyChat "Comment ABS"** — DONE. Live on **any post or reel** for @danrosefit (Pro),
verified end to end (comment → public reply → DM → button → absbyai.com with
`utm_campaign=comment-abs`). All ~60 queued CTA posts are now covered. Remaining: Dan
decides whether to switch off Blotato's IG auto first-comment (the growth plan said to,
once ManyChat was live — **ask before touching it**, it's a queue-wide change), and the
comment-ABS reels are now eligible for the 2026-08-31 paid-ads specs. Delete this entry
once Dan confirms.

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

**04 invest-health longform** — the last of the five-longforms handoff. Blocked on Dan
picking a cutdown variant: conservative (43:31), sub30 (28:25), or the recommendation,
sub30 with the therapy/psych-meds beat restored (~29:15). Comparison artifact + 480p review
copies delivered. ⚠ **Whichever wins needs the right-channel audio rebuild** (both variants
were rendered before that fix) — `edit/build_audio_singlemic.py` + `finish_audio_invest.py`,
muxed `-c:v copy`. Then style pass → graphics → captions → deliver.

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
resolves it; the dashboard row is
`money::Upload longforms 02 (Zepbound) and 03 (Supplements) to YouTube — on hold pending
Muhammad's edits` (high, not key — it is parked on purpose). **Whoever closes this out must delete
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

**AD 2 vertical 9:16** — rev 2 delivered and independently cleared on centering. Dan
watches, looking specifically at 0:45–0:49 and 1:20–1:27 (the two hardest lunges). Then
Phase B: he cuts `SCRIPT_FOR_DAN.md` to ~200 words for the 0:59. **Dan cuts it himself** —
a cutdown selected by doctrine is what he rejected on Ad 1.

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

**Muhammad's Ad 3** — round-1 revisions appended to his existing batch-2 doc. Dan reads the
AD 3 section and tells Muhammad it is in the same doc.

**Waleed's Video 1** — round-2 revision doc + three paste-ready Upwork messages drafted.
Dan sends message 1 with the doc link. Recommendation: don't release the funded $100
milestone yet — it's the only structural reason left for him to finish the visual list.

**Zeeshan's ab-wheel cut — round 2 reviewed 2026-09-02.** one unified round-2 section (Dan's two items folded in, written as Dan) at the top of his doc (markdown copy `revision docs/organic-video-abwheel-revisions-zeeshan-round2-9-2-26.md`). Most of round 1 landed; still missing: the live workout sets, voice levelling (middle 10 dB louder than the start, clipping), and the email form on screen at 5:06. Dan forwards the doc.

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

**Gemini prepaid credit is depleted** (HTTP 429, since 2026-09-01). The same key serves
production's primary image leg, which **fails open to the challenger silently**.
**Dan: top up at ai.studio/projects.** Fourth provider-credit outage — see memory
`provider-credit-outages`.

**iOS submission `ccc7a7ae`** — WAITING_FOR_REVIEW with Apple since 2026-08-26 (5.1.1(v)
argued, UX fixed, no new binary). Fallback if they hold the line is spec'd at the bottom of
`app-store-assets/APP_REVIEW_REPLY_20260826_G511v.md`.

**IG image gap-fill** — 63 of 70 scheduled. The last 7 are blocked on Blotato's 200-post
plan cap; Dan either deletes queued posts or upgrades. Then re-run
`scripts/blotato/iggap_fill.py --apply` (idempotent). ⚠ The queue is now **exactly 200/200**
(TikTok mirror, 2026-09-02) and drains ~2/day.

**TikTok via Blotato — LIVE, first post unverified.** TikTok `@absbyai` (Blotato id 58181)
connected 2026-09-02; all 23 queued `@danrosefit` videos mirrored at identical times via
`scripts/blotato/tiktok_mirror.py`. First TikTok post fires **2026-09-03 22:00 UTC** — next
session checks `blotato_list_posts` (platform tiktok, status published/failed); a `failed`
usually means a privacy-level mismatch on an unaudited account. To make room, the 6 latest
Facebook photo mirrors (2027-01-04 → 01-15) were removed and saved to
`scripts/blotato/fb_trimmed.json`; `tiktok_mirror.py --restore-fb --apply` puts them back once
the queue has room. Dan: say whether the recurring `Post on TikTok` dashboard row should go now
that posting is automated. Delete this entry once the first post is verified.

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

**Dashboard cleanup** — 23 stale rows removed on branch
`claude/dashboard-handoff-cleanup-m8u78j`. ⚠ The live board is `todos.json` on **main**, so
this does not take effect until the branch merges. Dan merges, or says the word.

**Assistant time tracking** — merged and live-verified on GitHub, but **not** verified in a
browser (that session's egress blocked absbyai.com). Whoever is next at a browser: load
`/assistant` and confirm it reads `Unpaid: …`, and that the dashboard's "Mark as paid"
button appears under the timer.

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

Each has a Key dashboard task. Run in a fresh session.

- **`Handoffs/handoff-20260902-shorts-centering-queue-fix.md`** — **URGENT, 09-05 deadline.**
  YouTube has been publishing the pre-8/27 off-centre Shorts (the native queue was never
  swapped; 4 already live, 6 still scheduled, `v2-short7` goes out 09-05). One Blotato post
  (09-07 `v2-short1`, IG + TikTok) still has the stale file. `v6-short2` and `v6-short5` are
  off-centre in their CURRENT masters. Dan is deleting `rqyK5IDsxX0` himself.
- **`Handoffs/handoff-20260901-danrosefit-ad-identity-fix.md`** — the @danrosefit follower
  campaign. Blocked on a Meta page-permission error; the draft ad set is in an error state
  and nothing is spending. **It opens by asking Dan whether the two-step funnel is still
  worth the effort** — unblocking has eaten most of two sessions for a $10/day campaign, and
  running from @abs.by.ai works today with zero further setup. ⚠ Two Pages named "Daniel
  Rose Fitness" exist: keep `1380236418500031`, delete `61593951123927`.
- **`Handoffs/handoff-20260902-google-ads-engagement-champion-automation.md`** — YouTube
  engagement champion, design LOCKED with Dan 2026-09-02: every new video → one $5 test ad in each
  of the three DGEN campaigns (spend read, then paused), one champion per campaign on cost/conv,
  day-one pause of the losing hand-made ads, no approval gate. Brain on our server, hands = Google
  Ads Script; apply for the API developer token in the same session. Supersedes the 8/31 handoff's
  loop (its Phase 1 API steps still apply). Fable 5.1 high.

---

# ACTIVE TASK

**Shorts centring queue fix — DONE 2026-09-02, one decision left for Dan.** Every queued off-centre Short is
replaced: Blotato 10 posts swapped + MD5-verified; YouTube 8 stale scheduled Shorts re-uploaded as new ids at
the same slots (old→new in `SHORTS_UPLOAD_PLAN.json`), the 8 old copies + killed `v6-short1` deleted;
`v6-short3`/`v6-short5` re-cut, `v6-short2` measured centred and left. Dashboard task checked off. **Dan:
the four already-PUBLISHED off-centre Shorts (`y0XIbNoA2Xo` 08-22, `P9VUGyWeNtY` 08-27, `VOlZHV1ibmU`
08-29, `rqyK5IDsxX0` 09-01) — delete + re-upload on the next open Tue/Thu/Sat slots, or leave them?**
Delete this entry once he answers.


**04 invest-health — style-standard rebuild IN PROGRESS** (Claude Code, 2026-09-02).
Dan picked sub30 + the therapy/psych-meds beat (L1) restored: 165 ranges, 29:13. Picture
rendered, audio rebuilt right-channel-only, 124 cutaways + 65 graphics built; composite and
gate remain. Work dir `/Volumes/Extreme/_edit_work/invest-health-cutdowns/{sub30f,style}`.
Do not write to `claude edited long form content/04 - …` from another session.
