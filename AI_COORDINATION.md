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

**Website conversion video (post-generation)** — cut from the 8/28 shoot (C1650+C1651) to
the trust brief, delivered 2026-09-02 to `claude edited long form content/06 - Website
Conversion Video (post-generation)/` (`website_video_16x9.mp4`, 3:51.56, QC pass + watch
pass, $0.00 AI spend, no production code, no deploy). 540p review copy sent in chat. Dan
watches; on approval it goes onto the site's post-generation page (a separate web task —
the player/embed does not exist yet). No dashboard task covers this. Recipe + lessons 73–81
are in `/ad-edit` (`reference/website-video/`).

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

**Zepbound shorts** — 8 cut and delivered (`zep-short1..8_*.mp4`), all gates green, 540p
review copies sent. Dan says which to swap for one of the six alternates in `SHORTS.md`
(one re-render each). ⚠ Picks were mine, not his. **Posting is blocked on the parent
long-form, which is unpublished** — and that parent is now on a deliberate hold (above), so
these are parked too. Do not chase them.

**Spray tan shorts (01)** — 8 cut and delivered (`tan-short1..8_*.mp4`, 45.8–59.4 s), all
gates green (QC pass, caption-sync 8/8, centering 8/8), 540p review copies sent. $0.00 AI
spend. ⚠ Picks are mine, not his; six alternates in
`YouTube Long Form Video Content/spray-tan-first/SHORTS.md`, one re-render each. Three
things need his ruling: **"full Donald Trump"** in short 6, **"my shitty pictures"** in
short 4, and Bryan Johnson named in short 7. **Posting is blocked and harder than 02/03:
this long-form has no `PACKAGING.md` at all** — `/youtube-packaging` has never run on it.
⚠ Two `syncgate.py` bugs fixed in the process (wrong `.ass` path; a first-word test that
cannot pass a `base.en`-vs-`medium.en` tokenisation difference) — both would have failed
future batches, both fixed in the gate rather than overridden.

**Supplements shorts (03)** — 8 rev-4 copies delivered, unwatched. Same block: the parent
long-form is packaged but on hold (above), so nothing can post. Parked, not chased.

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

**Zeeshan's ab-wheel cut — round 2 reviewed 2026-09-02.** Claude's items appended under Dan's two in the round-2 section at the top of his doc (markdown copy `revision docs/organic-video-abwheel-revisions-zeeshan-round2-9-2-26.md`). Most of round 1 landed; still missing: the live workout sets, voice levelling (middle 10 dB louder than the start, clipping), and the email form on screen at 5:06. Dan forwards the doc.

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
`scripts/blotato/iggap_fill.py --apply` (idempotent).

**Google Ads conversion goals** — the Purchase/Subscribe tidy-up (delete the orphan action,
rename the auto-created one) must wait until a real row exists in the offline feed.
**Do not manufacture a row to silence error 4000.**

**Dashboard cleanup** — 23 stale rows removed on branch
`claude/dashboard-handoff-cleanup-m8u78j`. ⚠ The live board is `todos.json` on **main**, so
this does not take effect until the branch merges. Dan merges, or says the word.

**Assistant time tracking** — merged and live-verified on GitHub, but **not** verified in a
browser (that session's egress blocked absbyai.com). Whoever is next at a browser: load
`/assistant` and confirm it reads `Unpaid: …`, and that the dashboard's "Mark as paid"
button appears under the timer.

---

# HANDOFFS WRITTEN, NOT EXECUTED

Each has a Key dashboard task. Run in a fresh session.

- **`Handoffs/handoff-20260901-danrosefit-ad-identity-fix.md`** — the @danrosefit follower
  campaign. Blocked on a Meta page-permission error; the draft ad set is in an error state
  and nothing is spending. **It opens by asking Dan whether the two-step funnel is still
  worth the effort** — unblocking has eaten most of two sessions for a $10/day campaign, and
  running from @abs.by.ai works today with zero further setup. ⚠ Two Pages named "Daniel
  Rose Fitness" exist: keep `1380236418500031`, delete `61593951123927`.
- **`Handoffs/handoff-20260831-manychat-comment-abs-setup.md`** — ManyChat "Comment ABS" on
  @danrosefit. Needs Dan at the keyboard (IG toggle, signup, OAuth, plan). ~60 queued posts
  promise a DM that nothing currently sends. Don't touch Blotato's IG auto first-comment.
- **`Handoffs/handoff-20260831-google-ads-api-setup-engagement-ad-automation.md`** —
  engagement-ad automation. Phase 1 is the Google Ads developer token.

---

# ACTIVE TASK

**04 invest-health — style-standard rebuild IN PROGRESS** (Claude Code, 2026-09-02).
Dan picked sub30 + the therapy/psych-meds beat (L1) restored: 165 ranges, 29:13. Picture
rendered, audio rebuilt right-channel-only, 124 cutaways + 65 graphics built; composite and
gate remain. Work dir `/Volumes/Extreme/_edit_work/invest-health-cutdowns/{sub30f,style}`.
Do not write to `claude edited long form content/04 - …` from another session.
