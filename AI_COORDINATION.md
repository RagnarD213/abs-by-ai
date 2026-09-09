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

**Google Ads audit — DELIVERED 2026-09-09, seven ranked fixes waiting on Dan's go-ahead. Nothing changed in the
account.** Read live from account 342-717-0837: **$1,272.66 spent** (Aug $769.75, Sep 1–9 $502.91), $440.24 last week
across 5 campaigns, **0 paying customers**. Root cause: **"YouTube channel subscriptions" is a Primary account-default
conversion and is 1,088 of the 1,115 conversions** — so all five campaigns, including both Search ones, bid toward a
signal search traffic cannot produce; 99% of the subscribers bought are Philippines/Indonesia/Vietnam at ~$0.10 (US is
$5.23 and 1% of them). Also found: the "Brand" campaign runs generic terms and outbids the non-brand one on the same
query (`abs ai` at $12.20 vs $3.12); Trial Signup / Subscribe / Purchases all read Misconfigured; every final URL is
still the homepage, not `/start`. Site side (PostHog + prod DB, since 07-30): 207 ad visitors → 35 generations → 2
accounts → 0 sales. Report: https://claude.ai/code/artifact/f1b850c8-9cd4-456b-99ef-8c281e14a97a — the fix list is in
priority order and is all reversible; say which to execute. ⚠ Unresolved: both Search campaigns spent 1.3–2.5x their
stated daily budgets last week (check Change history), and Google's "all time" per-campaign view never loaded — the
Ads tab froze repeatedly. ⚠ Google Ads billing looks FIXED (successful $500 threshold charge 09-09 on Visa •7763),
which supersedes the "Dan fixes the payment method" line in the Paid ads entry below.

**`/start` ad landing page + A/B — LIVE 2026-09-09, two 1-minute steps for Dan.** Funnel pulled first (PostHog, 30 d):
571 landed → 55 generated (**9.6 %; 516 people, 90 %, never upload a photo — the biggest drop by far**) → analysis page 1
(test only) → 6 trial sign-ups → 4 trials → 2 paid. Built `public/start.html` (variants `control` image-led /
`analysis` numbers-led, `?v=a|b`, `?vp=1` placeholder), one-tap photo hand-off into the app that auto-runs the
generation, trial CTA, and a new `generation_started` event. Doc: `Docs/VSL_LANDING.md`. **Dan: (1) upload the rev-5
website video to YouTube as Unlisted and paste the id into `youtubeId` in `public/site-video.js` — the one file both
`/start` and the analysis page read; both hide the slot until then. (2) Create PostHog flag `vsl-landing-variant`
(variants `control` / `analysis`, 50/50) + an experiment on it — the stored API keys lack the flag scopes; the page
runs its own sticky 50/50 and fires the exposure events meanwhile, so nothing is lost.** Point new ad campaigns at
`absbyai.com/start`. Delete this entry once both are done.

**Post-lock-in "Your analysis" page — LIVE 2026-09-08, three defaults for Dan to confirm.** The email + bridge screens
are gone; "Lock in this goal" now opens `analysis` (video slot, height/weight sliders, the four numbers, body map from
`POST /api/body-analysis` on `claude-opus-5`, trial CTA + email ask). Defaults shipped: women's height default is 5'4"
(men 5'9"); the video block is hidden until `youtubeId` in `public/site-video.js` gets the id (`?vp=1` shows the placeholder; shared with `/start` since 09-09);
recommended hosting for rev 4 is a YouTube unlisted upload. **Out-of-credits path (Dan's asks, 2026-09-08):** a locked generation
now lands DIRECTLY on the analysis page (video → offer button → before/after → numbers → sliders → body map → plan →
offer → email; no top copy, no "tell us more" card); the result screen with its paywall block stays underneath for
"back". The body map always renders (table-derived when the photo read fails). ⚠ Every push redeploys and wipes the
in-memory held images — a locked result made before a deploy cannot be analyzed or unlocked (memory
`deploy-drops-locked-holds`). **Native retest needed** (lock-in → sliders → trial CTA, AND the locked result →
analysis → unlock on iOS/Android). Delete this entry once Dan confirms or changes the defaults.

**Editor rounds out 2026-09-08 — waiting on the editors, nothing for a session to do.** Dan reviewed, edited and
sent all eight docs on 09-08 (Muhammad Ads 3–8 in the batch-2 doc, Waleed round 3 in a new doc, Zeeshan round 3 at the
top of his doc). Next deliveries get the same sweep; the skill was recalibrated from his edits (calibration pass 2,
rules 12–21). The scripts doc's three before/after cue lines (Ad 5, Ad 6, Ad 8) were corrected 2026-09-08.
Delete this entry once the next cuts arrive.

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

**Website conversion video — REV 6 DELIVERED 2026-09-09 as TWO masters, Dan picks A or B.** All six rev-5 items are in
`claude edited long form content/06 - Website Conversion Video (post-generation)/`: `website_video_16x9_A_tan-corrected.mp4`
and `…_B_tan-as-is.mp4` (identical except the cheek patch; rev 5 kept as `*_REV5`), each through the full gate suite
(audio 12/12 incl. the new damage row — room 76 → 45 ms with the dereverb Dan approved by ear on the shorts A/B; QC all
PASS; hair 43 px min; fidelity 99.0 %; watch 0/0). 540p copies, `AB_tan_face.mp4` and the audio A/B were sent in chat;
`notes.md` explains every item. **On his pick: rename the winner `website_video_16x9.mp4`, keep the loser as
`website_video_16x9_ALT.mp4`, then delete this entry.** AI spend $6.67. Lessons 118–122 in `/ad-edit`; recipe in the
skill's `reference/website-video/`. ⚠ **Found on the way and fixed live (`10eda3b`): the 09-08 analysis page never closed
its section div, so the member hub / Trainer / program / nutrition / membership screens rendered BLANK for logged-in
members on absbyai.com.** Verified live. **Native retest needed:** log in on iOS/Android, open the hub and the Trainer.

**Exercise demos batch 4** — 9 final candidates delivered and sent in chat (kb-swing,
kb-deadlift, kb-goblet-squat, kb-row, kb-press, deficit-pushup, ab-wheel-rollout, step-up,
db-step-up), all gates green. Dan reviews; on approval stamp `-FINAL` and install per the
batch-2 recipe (**that install is a native-retest trigger**). `db-lunge` is blocked — Veo
drifts the camera on this large-translation move; options are full `google/veo-3.1`, Kling
with `end_image`, or filming it. Batch dir `Media/exercise-demos/_batch4/`.

**04 invest-health — AUDIO REJECTED 2026-09-09, re-render handed off. Picture and cut are approved-as-is.**
Dan: *"absolutely awful… it sounds underwater. We can never, ever strip audio like this."* **He is right and it
measures:** the file was gated 09-03, six days BEFORE the dereverb was re-tuned, so it carries the rejected
settings (α 0.62 / floor −24 / d2 150). Re-gated 09-09 → **FAIL on `artifacts`, flux 0.094 = 1.31× Muhammad's**
(bound 1.10×); every other row passes. The delivered file's stamp is now FAIL, so no deliver script will ship it.
A sweep of every `*.voice_chain.json` in the delivery trees confirms **04 is the only long-form affected** — the
three Shorts batches are the sibling handoff's job. Everything needed is staged (`voice_raw.wav`,
`picture_final.mp4`, bed, SFX); it is an audio-only re-mix + `-c:v copy` mux, no picture re-render.
⚠ Two prerequisites, both live: `common.stash_untreated()` was MISSING at 10:03 on 09-09 while
`voice_chain.py:158` calls it (module was being edited by another session — `MM` in git status), and
`selftest.sh` is broken. → `Handoffs/handoff-20260909-invest-health-audio-rerender.md`. No dashboard row (his
09-08 rule). The 29:16 cut, graphics and 12/12 style gate stand; only the audio is rejected.

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

**Spray tan shorts (01) — RE-RENDERED AND DELIVERED 2026-09-09 on the sound Dan picked; he listens.**
He chose the gentle build by ear ("number 3"); it is now the module default (a0.30 / d1 22 / d2 70 /
floor −10 / smooth 0.45) and all six shorts are rebuilt, gated, stamped and delivered — EDT 37–56 ms
against Muhammad's 40, flux ×1.05–1.11 and swirl ×1.25–1.29 of untreated. Sent: `review/AB_three-way_audio.mp4`
(untreated / new build / Muhammad, all at −14 LUFS) + six 540p copies. **Dan says yes or no to the sound.**
Rollback: `spray-tan-first/out/_PRE_AUDIO_20260909/`. Picture was never re-encoded (audio swapped into the
lossless .mov with `-c:v copy`, frame counts asserted).
⚠ Two defects found while doing it, both fixed: the pipeline kept a **forked `work/dereverb.py`** and
render.js passed the rejected numbers on its command line, so the 09-09 shared fix had not reached it;
and `finishaudio.py` fitted **7 octave bands while the gate grades 10**, so the batch had shipped
**ungated** — measured on 09-09 the old files fail 6/6 on artifacts and 5/6 on tone. Both now use the
shared module. New gate row `do_no_harm` (flux/swirl ≤ ×1.35 of the same file untreated) blocks 16/16
of the shipped 09-02 files; `selftest.sh` repaired and green (7 steps / 16 checks). Commit `9f42e12`.
**Still to re-render on the new sound: Zepbound (8) and supplements (8)** — parked behind the parent
long-form hold, not chased. Nothing is public.

**Supplements shorts (03)** — 8 delivered, **audio re-rendered 2026-09-02 through `_shared/audio`**
(room 67–88 ms → 29–45 ms, every file stamped PASS; pre-fix copies in
`_pre-audiofix-20260902/`; A/B clips beside supp-short1 and supp-short4). Same block: the parent
long-form is on hold (above), so nothing can post. Parked, not chased.

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
**Enhanced conversions — code side DONE 2026-09-08 (`ac51f50`, live-verified):** every logged-in browser conversion
fire now carries the hashed email (`em=` seen on the live hit), the offline feed has an 8th `Email` column (SHA-256,
Google-normalised) and emits email-only rows for members with no click id, privacy policy updated. **One step is
blocked by the same empty feed: Data Manager's "Edit mapping" refuses to open on a header-only file (error 4000) and
shows blank rows with Save disabled, so the `Email` column is NOT mapped yet.** After the first real sale imports,
open Tools → Data manager → HTTPS → the connection → Edit mapping → map `Email` → Google's Email field (already
hashed). Until then the two import-action EC warnings stay red by design. Driving traps: memory
`google-ads-ui-automation`.

---

**IG profile-visits campaign — LIVE since 2026-09-02 ~18:00 CT.** Campaign `120250753198730682`,
ad set `120250753601020682` (**$6.50/day ≈ $200/mo, Dan's call 2026-09-02**) and both ads on the real @danrosefit reels are ACTIVE; ads
clear Meta review on their own. **Auto-boost is LIVE since 2026-09-08 21:00 UTC** (`AUTO_BOOST_ENABLED=1`; first Railway live run 21:17 UTC, idempotent): campaign
renamed `[AUTO] …`, ad set renamed `CHAMPION`, six $5 tests running on the Sep 2–7 posts (end 09-13). The job judges tests on cost/visit;
**follows are NOT readable from the API, so cost/follow is a manual weekly check against the baseline of 566 followers at $40.02 spend
(2026-09-08)** — recipe in `Docs/AUTO_BOOST.md`. Kill >$5/follow, scale <$3/follow. Recipe: `scripts/ads/boost_danrosefit_posts.py`. ⚠ Never click the global
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

Swept 2026-09-08. The first four are on the dashboard's **Handoffs to fire** list (Dan's ask, 09-08) with their starter
prompts. Whoever runs one deletes its row there AND removes it here and from `Handoffs/README.md`.

- **`Handoffs/handoff-20260812-revenuecat-restore-behavior-audit.md`** — fire the day Apple approves (IN_REVIEW).
- **`Handoffs/handoff-20260812-purchase-before-account.md`** — after approval AND after the RevenueCat audit.
- **`Handoffs/handoff-20260818-android-public-build-swap.md`** — small; needs Dan's Android phone on adb.
- **`Handoffs/handoff-20260826-danrosefit-abs-image-gap-fill.md`** — last 7 of 70 posts; re-run
  `scripts/blotato/iggap_fill.py --apply` from ~09-12 once the 200/200 Blotato queue has drained 7 slots.
- **`Handoffs/handoff-20260909-audio-match-muhammad.md`** — PARTLY EXECUTED 2026-09-09: the do-no-harm row,
  the selftest repair and the **spray-tan re-render (6)** are done and pushed (`9f42e12`). What is left is
  **Zepbound (8) and supplements (8)** on the same settings, which are parked behind the long-form hold —
  fire it once Dan confirms the spray-tan sound. **Not on the dashboard** (his rule).
- **`Handoffs/handoff-20260909-invest-health-audio-rerender.md`** — 04 invest-health carries the SAME rejected
  dereverb (gated 09-03, before the fix) and is NOT covered by the batch handoff above. Gate now FAILS it on
  `artifacts` (flux 1.31× his). Audio-only re-mix from the staged `voice_raw.wav` + `-c:v copy` mux; picture,
  cut and graphics stand. Sonnet 5, standard, ~30–45 min. **Not on the dashboard** (his rule).
- **`Handoffs/handoff-20260908-google-ads-custom-segments.md`** — ten Google Ads custom segments (six search-term,
  four interest/site/app) + a `website | member hub | 540 day` exclusion list for the new Demand Gen app campaign;
  Dan's top three are #2 AI abs preview tool, #5 competitor apps, #9 get abs / belly fat. Fire once Dan says which
  to build (default all ten); Fable 5.1, high. **Not on the dashboard** (he has not asked).
- **`Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md`** — Dan, 2026-09-09: our cuts are "far
  below the quality the human editors have made" (audio, framing, jump cuts, junk footage) and he will not ship
  them. Audited: **33 QC scripts, one shared**; `_shared/` has no picture/framing/cut/caption module at all; the
  style gate reaches 1 of 6 skills; the watch pass is mandatory in 1 of 6 (`/shorts` mentions it zero times); four
  scripts SKILL.mds call **do not exist**; `--no-stamp`/`--synthetic`/`AUDIO_UNGATED` bypasses are live and one
  skill instructs one. The measured gap to Muhammad: **he cuts picture 1–15 frames off the audio splice on a
  pose-matched frame** (`piccuts.py`, already built for Ad 2 and never promoted), and our talk ran at one fixed
  crop. Six phases; run Phases 0+3 first (close bypasses, regression corpus). Fable 5.1, high, ~2 sessions for
  0+3. **Not on the dashboard** (his 09-08 rule).

Dead, do not run: `handoff-20260901-danrosefit-ad-identity-fix.md` (superseded — the @danrosefit profile-visits
campaign has been live via the API script since 09-02), `handoff-20260902-shorts-centering-queue-fix.md` (done
09-02), `handoff-20260902-google-ads-engagement-champion-automation.md` (LIVE since 2026-09-08 22:00 UTC; operating doc
`Docs/YTADS.md`).

---

# ACTIVE TASK

**Zeeshan content-video batch — 10 candidates delivered 2026-09-09, WAITING ON DAN TO PICK 5.** Full unedited
long-form inventory rebuilt from the outline docs + roll probes (transcribed, not assumed): **15 unedited items**
across shoots 2/3/4/5. Shoot-2 leftovers CONFIRMED filmed and unedited — C1485 = Why You MUST Workout Every Day
(27.4 min), C1486 = Intermittent Fasting (23.1), C1487+C1488 = STOP Deadlifting (15.7). Shoot-4 map confirmed:
C1605–08 Zepbound-muscle, C1609 Abs at 40 vs 25, C1610–13 Oura, C1614–29 Vacuum, C1630–33 ab wheel (done).
Protected for Muhammad: Belly Fat Emergency, Real Reason You Don't Have Abs, Keep Your Muscle On Zepbound,
Daily Salad, The Vacuum. Once Dan picks 5 → build the editing doc per `/editor-brief`, then make it a `/editing-doc`
skill (his instruction: skill LAST, after the doc is finalised). Roll→video mapping for the picked 5 still needs
`pick_lav.py` run for the per-shoot audio paragraph. No dashboard row (his 09-08 rule).

**Google Ads custom segments (handoff 20260908) — 9 OF 12 BUILT 2026-09-08 evening, PAUSED by machine load; resume
in a fresh session.** Built in Audience manager → Custom segments and reopen-verified (chips entered / kept, insights
estimate on reopen — the estimate is noisy, it changed 10× between open and reopen on the same list): 2 AI abs preview
tool 16/16 (1M–5M wk), 5 competitor apps 21/21 (10B–1T), 9 get abs belly fat 19/19 nothing flagged (10M–50M), 1 brand
10/10, 3 what would I look like 12/12 (5M–10M), 4 AI fitness 15/15 (5M–10M), 6 AI fitness sites 5 interests + 13 sites
(100M–500M), 8 AI body photo editing sites 4 + 13 (10B–1T), 10 transformation content 6 + 7 (10M–50M). All read "Under
review". No term was dropped or flagged. `/vp/hub` verified live 2026-09-08 20:35 CT: Google's `1p-user-list` collector
returned 200 for a hit carrying `url=absbyai.com/vp/hub` (fired from the live page; Dan's Chrome is not signed in to
absbyai.com so the real hub could not be rendered). **Still to do:** 7a/7b/7c (app picker — one MadMuscles pick was
verified working: type the title, the row shows the Play package id), the `website | member hub | 540 day` list
(Your data → rule "URL contains /vp/hub", 540 days — set the duration with a `blur`, archive 08-18), Phase 2 only if the
Demand Gen draft exists. Stopped because the Mac sat at load 50–90 (166 Claude Code processes at 460 % CPU + the
website-video ffmpeg) and the extension-driven Ads tab never reached document_idle after the first freeze — per the
handoff rule, stop rather than click into spinners. After the load fell to 20 (20:30 CT) a fresh tab still never left the "Google Ads" loading shell — the 08-17 refuse-to-render state; try again in a new session, ideally with fewer Claude Code sessions open. Trap: dispatching pointer events on a picker `material-list-item`
inside `javascript_tool` (or any `await` in one call while the page is busy) hung the renderer; use keyboard/ref clicks.
Working recipe for the other fields is in the handoff's Execution notes.

**YouTube engagement champion (Google Ads) — LIVE since 2026-09-08 22:00 UTC; one question for Dan.** Runs at :00
hourly; 4 videos have `AUTO test · <video title> · yt:<id> · …` ads in all 3 campaigns (the 9 legacy-named ones were removed
at 00:00 UTC 09-09 and recreated at 01:00 with Dan's edited headlines, all 9/9 OK — Ad.name is immutable in the API). Dan's
one-off edits go through `scripts/ads/ytads/manual.js` (recipe in `Docs/YTADS.md`); headline rules 1–3 in `headline-style.md`.
⚠ **Tier 1 has no champion:** "1 min ab workout workout only" (ad `821875813611`, $1.03/conv, 136 conv) was paused in the UI
between the dry run and the first live run — not by this system. Dan re-enables it if accidental
(`manual.js enable customers/3427170837/adGroupAds/206274722584~821875813611`), else leave it. Next check: the 09-09 morning
brief's "YouTube engagement ads" block (policy review of the 12 new ads). Delete this entry once Dan answers the tier-1 question.

**Shorts centring queue fix — DONE 2026-09-02, one decision left for Dan.** Every queued off-centre Short is
replaced: Blotato 10 posts swapped + MD5-verified; YouTube 8 stale scheduled Shorts re-uploaded as new ids at
the same slots (old→new in `SHORTS_UPLOAD_PLAN.json`), the 8 old copies + killed `v6-short1` deleted;
`v6-short3`/`v6-short5` re-cut, `v6-short2` measured centred and left. Dashboard task checked off. **Dan:
the four already-PUBLISHED off-centre Shorts (`y0XIbNoA2Xo` 08-22, `P9VUGyWeNtY` 08-27, `VOlZHV1ibmU`
08-29, `rqyK5IDsxX0` 09-01) — delete + re-upload on the next open Tue/Thu/Sat slots, or leave them?**
Delete this entry once he answers.
