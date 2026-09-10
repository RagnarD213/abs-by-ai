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

**Web pay-first cart — LIVE 2026-09-10, Dan runs the live card test.** The web checkout is now analysis page →
cart (`#cartSection`: Monthly $19.99 pre-selected, Annual $69.99 "save 71%", trial timeline, disclosure above the
button, video slot) → Stripe collects the email with the card → account created after payment (one-time claim login +
set-password email; an existing email gets the membership attached and is told to log in, never auto-logged-in) →
"You're in" → the five questions as onboarding → the program. Native/IAP untouched. Research: the private "Cart
teardown" artifact (https://claude.ai/code/artifact/a7424907-bc1a-41a9-b7af-b0f7a17d8512). Doc + Dan's test script:
`Docs/WEB_CART.md`. Review without paying: `absbyai.com/?demo=checkout` (+`&locked=1`, `&sex=female`); `?vp=1` shows
the cart video placeholder. Server fixture tests green (`node scripts/cart/cart-fulfillment.test.js`, 45 checks).
**Dan: (1) the live card test in a private window — cart → Monthly → pay $0 → confirm logged in + set-password email →
cancel before day 7; (2) Google Pay on/off in Stripe (recommended on; Claude will not flip it unasked); (3) the shipped
defaults — cart video hidden until the file exists, anonymous trial reuse allowed and logged, no email before the card,
no urgency device.** ⚠ Native retest: the apps load the same page — confirm iOS/Android still show the IAP screen and
the account-first flow (verified locally with `IS_NATIVE_APP` forced, not on a phone). ⚠ PostHog funnels that used
`account_signup` between the trial button and payment must be rebuilt (`cart_viewed` → `cart_checkout_opened` →
`cart_checkout_completed` → `account_claimed`). Delete this entry once Dan's card test passes.

**$17 Ab Wheel long-form + its 5 shorts — SCHEDULED ON EVERY PLATFORM 2026-09-10, nothing blocked.** Muhammad's v2 HD
goes public Sun 09-13 9 AM CT: YouTube `bkzT-3ENpoU` (full-quality master, thumbnail A, chapters) + FB / IG @danrosefit /
TikTok via Blotato (@abs.by.ai 09-14). The 5 approved shorts (cut 08-28 from this exact file) post Oct 27/29/31, Nov 3/5
5 PM CT, IG cover A. Optional in Studio: thumbnail F as the A/B test, a pinned comment. ⚠ TikTok long-form is 6:58 — if
the 09-13 TikTok post fails, that is the account's length cap. Table: `BLOTATO_QUEUE_PROGRESS.md`. Delete once it posts.

**/start VSL script — WRITTEN 2026-09-10, Dan reads it and records.** Google Doc
`1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA`: hero cut (≈1:15, demo-first — Dan uploads his own before photo, "I'll
go first"), full cut (≈3:15, "This picture got me abs"), four hook takes, shot list, B-roll, research, compliance. One
call is Dan's (doc §7: the on-screen line under his real photos). After recording, fire
`Handoffs/handoff-20260910-start-vsl-edit-and-install.md` — /start needs its OWN video slot. The dashboard row "Write
and record a video sales letter (VSL) for /start" stays unchecked until the recording is live. ⚠ Found: the live
post-generation video claims "thousands of guys" twice (3:16, 3:41) — 75 people have ever generated; a task chip for
the fix was offered. Delete this entry when the edit+install handoff runs.

**Website conversion video — LIVE ON THE SITE 2026-09-09, Dan looks.** Rev 6 version A (Dan's final) is uploaded UNLISTED to the
**Abs by AI** channel as `CwEGFxpIM-E` (3:51, HD, embeddable, processing succeeded) and embedded via
`public/site-video.js`, which BOTH the post-lock-in analysis page and `/start` read — verified rendering on
both live. Swapping the video later = paste a new id in that one file. **Review without generating:**
`absbyai.com/?demo=analysis` (add `&locked=1`, `&sex=female`, `&cond=…`) — real photo read on the public
sample pair, no credits, no localStorage writes, no funnel/ads events. ⚠ **Native retest, one phone session, two things:** the analysis page now shows a YouTube iframe inside the
iOS/Android wrappers (check inline vs fullscreen playback), and the `10eda3b` fix for the member hub / Trainer / program /
nutrition / membership screens that the 09-08 analysis page had left blank for logged-in members (verified on web only). Delete this entry once he confirms it plays.

**Google Ads account fixes — EXECUTED AND VERIFIED 2026-09-09. Live in account 342-717-0837; Dan reviews the results in
a few days.** All of `Handoffs/handoff-20260909-google-ads-account-fixes.md` is done, read back from the account after
saving. Both Search campaigns now carry **campaign-specific goals = Submit lead forms only** (Brand was on the
account defaults, where "YouTube channel subscriptions" was biddable; non-brand already was correct) and both moved
off conversion bidding to **Maximize clicks with a $2.00 CPC ceiling** (they were Target CPA $40 / $20 on ~8
conversions a week; Google's own UI flagged the budget/target conflict). **Tier-2 Demand Gen $15 → $5.00/day**, the
only budget touched — tier 1 $20, remarketing $10, both Search budgets unchanged; remarketing has no change event
today. Brand got **8 measured phrase negatives** (`ai abs`, `abs ai`, `ai ab`, `ab generator`, `abs generator`,
`abs creator`, `give me abs`, `6 pack`) — in 30 days EVERY paid term in that campaign was a generic close variant of
`[abs by ai]`, $155 of them and zero real brand searches. Non-brand got 3 wrong-intent negatives and **14 new PHRASE
keywords** (75 → 89; the campaign was almost all EXACT, which is why it drew 53 impressions a week). **Five new
`/start` RSAs**, one per Search ad group, copy verified byte-identical to the original, originals still enabled, and
all five ad groups set to **rotate indefinitely** so the landing-page test is not confounded.
⚠ **Two answers Dan should see.** (1) The over-budget mystery is solved and benign: non-brand's $5/day was set by Dan
on **09-08**, so last week's $88.91 was against a $10/day budget. Brand, though, has been $10/day throughout and
Google still delivered **$24.43 on 09-04** — above its own 2× daily cap, and $92.80 over the Sep 2–8 week ($13.26/day
average). That is an over-delivery Google credits back if asked. (2) **Trial Signup is not broken.** PostHog shows
`membership_subscribed` — the line immediately before the conversion fires — has fired **6 times, last on 08-25**, and
the identical `fireAdConversion()` path recorded 8 Free Generation Started conversions last week. "Misconfigured" is
Google's label for *no attributable conversions recently*: 4 of the 6 were native IAP (no ad click) and only one web
checkout ever carried a real gclid. Add **Sign-ups** to both campaigns' goals the day a real ad-attributed trial lands.
⚠ Also found, not fixed (out of scope): `handleIapRestore()` calls `handleMembershipComplete()`, so an iOS **restore**
would fire a Trial Signup conversion. Harmless today (the app is not approved) — worth fixing before it is.
Channels used, and why: the one-off Ads Script ran the READ (`scripts/ads/oneoff/search-repair.js`, now disabled in the
account, never scheduled); the writes went through the **ytads manual mutation queue** (36/44 first pass) and the **Ads
UI** for the two the queue cannot do — campaign conversion goals need `{partialFailure:false}` and the bidding switch
needs a leaf field mask. Google Ads billing is confirmed working ($500 threshold charge cleared 09-09, Visa •7763).
Delete this entry once Dan has looked at a few days of data.

**`/start` ad landing page + A/B — LIVE 2026-09-09, two 1-minute steps for Dan.** Funnel pulled first (PostHog, 30 d):
571 landed → 55 generated (**9.6 %; 516 people, 90 %, never upload a photo — the biggest drop by far**) → analysis page 1
(test only) → 6 trial sign-ups → 4 trials → 2 paid. Built `public/start.html` (variants `control` image-led /
`analysis` numbers-led, `?v=a|b`, `?vp=1` placeholder), one-tap photo hand-off into the app (body type + Generate
happen there), trial CTA, and a new `generation_started` event. Dan's round-1 edits applied 09-09 (his headline, no
eyebrow/disclosure block/chips, pool-shoot avatar). Doc: `Docs/VSL_LANDING.md`. **Dan: (1) upload the rev-5
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

**Muhammad round out 2026-09-09 — DOCS WRITTEN, Dan reads and forwards.** Eight sections appended to his batch doc
(`1L2XJKLFrRJHKlcL4Iii70iFvZeiNNeplxYQw2aeAJ_A`): Ad 3 r4 (3 items), Ad 5 r3 (2), Ad 6 r2 (7), Ad 7 r2 (9), Ads 9/10/13/14
r1 (15/14/14/9). Level landed on 5/6/7/14 (−13.4 to −14.0 LUFS); the new failure class is over-done noise reduction
(gate `artifacts` row) on 3/6/7/9/13/14. Md copies in `revision docs/`, work dir `/Volumes/Extreme/_edit_work/revisions-0909/`.
⚠ His "AD 02 v2" link is byte-identical to Ad 4 v2 (md5 match) and the "AD 08" link is the unchanged 09-07 file — no Ad 2 v2,
Ad 4 v3 or Ad 8 v2 exists yet; Dan's message asks for them. Dan's calls (not in the doc): Ad 13 0:24 Six Pack Shortcuts
screenshot with the SIXPACKSHORTCUTS.COM watermark; Ad 7 whether we generate the Dan's-face Photoshop gag ourselves; Ad 10
the "slightly enhanced" before picture does not exist. Zeeshan r3 / Waleed r3 still waiting on those editors.
Delete this entry once Dan has forwarded the doc and the next cuts arrive.

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

**Exercise demos batch 4** — 9 final candidates delivered and sent in chat (kb-swing,
kb-deadlift, kb-goblet-squat, kb-row, kb-press, deficit-pushup, ab-wheel-rollout, step-up,
db-step-up), all gates green. Dan reviews; on approval stamp `-FINAL` and install per the
batch-2 recipe (**that install is a native-retest trigger**). `db-lunge` is blocked — Veo
drifts the camera on this large-translation move; options are full `google/veo-3.1`, Kling
with `end_image`, or filming it. Batch dir `Media/exercise-demos/_batch4/`.

**04 invest-health — RE-RENDERED AND DELIVERED 2026-09-09, gate PASS. One question for Dan.** The
"underwater" master is replaced; `FINAL_invest_health.mp4` now passes all 13 gate rows (flux 0.072 = 1.00×
Muhammad's, was 1.31×), picture byte-identical (52,618 frames, `-c:v copy`). The rejected one is parked beside
it as `FINAL_invest_health_UNDERWATER.mp4`. Both prerequisites were already fixed by the sibling session —
`selftest.sh` passes 15/15, and its step 7 now refuses the rejected dereverb outright.
⚠ **The delivered mix has NO dereverb, which is not the setting Dan picked by ear on 09-09** — measured on
this programme, *any* spectral subtraction fails the artifacts row (untreated 1.03× his → approved dereverb
1.20× on the lav, 1.14× in the mix; bound is 1.10×), because it varies the gain frame to frame by
construction. Shipping it dry has precedent: website rev 2, the cut he called *"you got it nailed"*, measures
EDT 74.7 ms and flux 0.86× his with no dereverb — same shoot, same room. **A three-way A/B (dry / his 09-09
dereverb / Muhammad) was sent 09-09; if he prefers the dereverbed room it is a re-mux of the staged
`audio/final_mix_v5.wav`, but that file cannot carry a PASS stamp.** ⚠ Soft number: the delivered `edt` reads
80.00 ms against an 80.0 bound — passes with zero margin (EDT is quantised to 2.667 ms steps).
Full measurements + traps: `REBUILD_NOTES.md` in the delivery folder. Delete this entry once Dan picks a room.

**Longforms 02 + 03 — HOLD EXPIRES 2026-09-09 AND MUHAMMAD HAS DELIVERED NOTHING.** Checked Drive
2026-09-08: his only delivery since Sep 1 is `Daniel HQ Ad 2 V2 HD.mp4` (Sep 3) — no Zepbound and no
Supplements edit exists, shared or otherwise. **Dan's own rule says ours go up as they are if Muhammad
never gets to them, so on 09-09 this becomes his call to make.** Note Claude cannot do the upload (no longer true —
see the upload note below).

**Longforms 02 + 03 — ON DELIBERATE HOLD UNTIL DAN DECIDES. DO NOT UPLOAD.** Both are cut,
packaged and thumbnailed and are staying in the project folder. **Dan's call 2026-09-02: he is
sitting on them until Muhammad delivers his own edits of the same two videos.** If Muhammad's are
significantly better, his ship and ours become the backup; if Muhammad never gets to them, ours go
up as they are. **Nothing about this is blocked on a session — do not offer to upload, and do not
treat it as an open task before 2026-09-09.**
⚠ Verified in Studio 2026-09-02: neither video exists on the channel (8 videos, neither is these),
so no thumbnail is installed and no A/B test exists. ✅ **The upload blocker is GONE as of 2026-09-09** —
`scripts/youtube/upload.js` + `YOUTUBE_REFRESH_TOKEN` upload any size (memory `youtube-upload-capability`);
the old 10 MB `file_upload` cap no longer applies. The hold is now purely Dan's call, not a capability limit. Thumbnails, at ~150 KB, DO upload through
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

**Home filming set — GEAR ARRIVED, Dan hiring an installer (2026-09-10).** Installer work order published
(https://claude.ai/code/artifact/2b21b748-62f0-455f-aafb-ac9a6a23ad44 — look B plant+lamp default, rod drilled, NO
floor marks: Jeff marks spots at the first shoot); job ad + TaskRabbit recommendation given in chat. Dan: buy 3 pre-filled
Sandbaggy 15 lb saddle bags (2-pack + single, $113) + LUXON amber E26 bulb 4-pack ($18.99) — both pages open in his
Chrome — then book a Tasker (Mounting, ~5 h) and share the sheet link. Stool = the Linon 29" barstool he already has.
Verified 09-10: the 09-01 duplicate order set was cancelled EXCEPT one VIVO TV floor stand ($54.11) → he owns TWO
(both delivered 09-04); return one by ~Oct 5 unless intended. After install: build the look-A telemetry loop file.

**Paid ads** — Dan decides whether both Meta campaigns being toggled OFF was intentional
(3 unpublished draft edits still pending). Launch specs are in the 8/31 artifact.
(Google Ads billing is fine — a $500 threshold charge cleared 2026-09-09 on the Visa •7763.)

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
- **`Handoffs/handoff-20260910-start-vsl-edit-and-install.md`** — fire after Dan records the /start VSL: edit the
  hero (×4 hooks) + full cut with /website-video, give /start its own video slot (the analysis page keeps
  `CwEGFxpIM-E`), verify live, then check off the dashboard VSL row. Fable 5.1 high. **Not on the dashboard** (his rule).
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
  crop. **Split into four executable handoffs 2026-09-09. ✅ VQC-A (Phase 0 + 3) IS DONE AND PUSHED —
  every bypass closed, `_shared/qc_corpus/` built and green, standing rule in `AGENTS.md`. B, C and D
  are unrun; **B is refreshed against what A found (2026-09-09) and is the next one to fire**:
  `…-vqc-B-phase1-2-shared-gate-and-watch.md`, `…-vqc-C-phase4-cut-technique.md`,
  `…-vqc-D-phase5-6-framing-and-junk.md`; B and C can run in parallel now.** The corpus names
  **14 checks nothing implements** — that list is the build queue, and B covers the most of it.
  Baseline: `Docs/VQC_baseline_20260909.md`. **Not on the dashboard** (his 09-08 rule).

Dead, do not run: `handoff-20260901-danrosefit-ad-identity-fix.md` (superseded — the @danrosefit profile-visits
campaign has been live via the API script since 09-02), `handoff-20260902-shorts-centering-queue-fix.md` (done
09-02), `handoff-20260902-google-ads-engagement-champion-automation.md` (LIVE since 2026-09-08 22:00 UTC; operating doc
`Docs/YTADS.md`).

---

# ACTIVE TASK

**Ad 1 "this picture got me abs" — 9:16 vertical from ZEESHAN's final (2026-09-10, this session owns it).** Building the
full-length 9:16 + a ≤0:59 cutdown per `/shortad-from-longform` in `/Volumes/Extreme/_edit_work/ad1-zee-vert/`, his mix
verbatim (constant gain + limiter), hair-anchored framing. His cut is 24 fps / 4:09.2 from raw C1591. ⚠ His 3:09 shows
the banned "Download Your Future Self" email screen — the vertical substitutes the cropped after-only card. Delivery goes
beside his 16x9 in `Zeeshan Ad Videos/this picture got me abs - ad 1/`; dashboard row stays unchecked until Dan approves.

**Video quality VQC-A (Phase 0 + 3) — DONE AND PUSHED 2026-09-09. Two things for Dan to know, nothing to do.**
The seven bypasses are closed (`require_stamp` strict by default; the instructed `--no-stamp` gone; an unmeasured
`do_no_harm` now FAILS; `qc_style`'s silent skips now FAIL; the four named-but-missing scripts written or promoted;
`AUDIO_UNGATED=1` removed) and the regression corpus is live at `.claude/skills/_shared/qc_corpus/` — 14 files in
Dan's verbatim words, `run.py` green, `selftest.sh` (19/19) folded in as its step 0, standing rule in `AGENTS.md`.
**Baseline: `Docs/VQC_baseline_20260909.md` — every delivered master re-gated, 166 files, 159 would not ship today.**
Read the "before reading the numbers" table first: 88 are exercise demos failing two rows their format makes
inevitable, 71 are the pre-09-09 do-no-harm gap, 6 are editor cuts graded against the wrong reference. **The real
finding is 62 of our own Shorts and longforms failing on substance — including 21 of 23 V2/V3/V6 cutdowns missing
−14 LUFS while already published, which nothing currently owns.** ⚠ `selftest.sh` was never broken: it is zsh, and
`bash selftest.sh` produces a fake "unbound variable". ⚠ Nothing was re-rendered and no stamp was changed.
Delete this entry once Dan has seen the baseline.


**Zeeshan content-video batch — BRIEF WRITTEN AND VERIFIED 2026-09-09. Dan fills in the rate, then shares and sends.**
Doc: `1Tdng5SrBthSaFDxaPnY2bWVhxp5e14YKbe3EVGhfjPE` ("Abs By AI — 5 Organic Content Videos — EDITING BRIEF", 15 pp,
tables + links verified in Chrome). His five picks: **ab wheel workout-only (C1630–33), arms & shoulders (C1582–87),
STOP Deadlifting (C1487–88), Oura review (C1610–13), abs at 40 vs 25 (C1609)**. Everything in it is measured, not
assumed: roll→video map from 51 whisper probes, durations from ffprobe, the standard from Zeeshan's own approved
ab-wheel cut (−14.8 LUFS / −1.6 dBTP / 39 framing changes in 7:00), mic wiring from `pick_lav.py` on all 17 rolls
(**right channel on every one** — 7/8 and 8/14-talking are two-mic, 8/3 and 8/14-abwheel have a dead left input).
**Three things are Dan's:** (1) the rate/bonus/turnaround — a highlighted blank in section 1; (2) open sharing on the
doc + the three shoot folders (`1l7UyY6…`, `1LCgVb5h…`, `1TItiv5J…`) or every link 404s; (3) the video-3 asset hole —
Dan says "you can see me doing right now" over rows, pulldowns, a rear-delt flye and a powerlifter physique that were
never shot; the brief tells Zeeshan to trim the self-reference and cover with stock, ask if a trim won't cut.
**Next in this session (Dan's instruction): once he finalises the doc, turn this into a `/editing-doc` skill.**
No dashboard row (his 09-08 rule).

Remaining unedited pool after this batch (10): Belly Fat Emergency, Real Reason You Don't Have Abs, Keep Your Muscle
On Zepbound, Daily Salad, The Vacuum (+ workout-only), Arms & Shoulders workout-only, Why You MUST Workout Every Day,
Intermittent Fasting, How To Work Out At Home On A Budget.

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
