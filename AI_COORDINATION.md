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

**Google Ads rep tasks (GA4, Search → /start, MCC account) — EXECUTED AND VERIFIED 2026-09-11. TWO CLICKS LEFT FOR DAN.**
✅ **GA4 is live and linked.** Property "Abs By AI" `553864929`, stream absbyai.com `15763007741`, **`G-1M1SY7GGKF`**,
inside GA account SixPackAbs.com `145219380`; linked to Ads `342-717-0837`, personalized advertising on, **no
conversion import** (the gtag actions stay primary — an import double-counts). Installed as a second `gtag('config')`
on the existing Ads loader across all 11 tagged pages (`17a90dc`), live-verified: a real `g/collect` hit with
`tid=G-1M1SY7GGKF` on `/` and `/start`, and GA4 Realtime showed it within a minute. ⚠ Google's "use the tag found on
your site" shortcut was REFUSED on purpose — it warns it overwrites the Ads tag's settings, which carry
`allow_enhanced_conversions`. ⚠ **Native retest:** the wrappers load the same page, so GA4 counts app sessions as web.
✅ **Every ENABLED Search ad now points at `https://absbyai.com/start`** (5 of 5, read back); the 5 home originals are
PAUSED with their URLs updated, so history stays readable. The homepage became a **sitelink** — both Search campaigns
carry four: Abs By AI Home `419963241925`, How It Works `419855564105` (both new), FAQ `401566853985`, Contact Us
`419837287031`. ⚠ A final-URL change re-triggers policy review — run `node scripts/ads/api/client.js policy 24148587722`
and `… 24086091285` on 09-12.
✅ **Callouts recommendation: nothing to do.** All four callouts are ENABLED on BOTH campaigns and the API returns **no
callout recommendation at all** — the card in Dan's screenshot is gone. No duplicates were added.
❌ **DAN: the empty "SixPackAbs.com" MCC account needs you.** Both channels are closed to Claude — the API returns
`DEVELOPER_TOKEN_NOT_APPROVED` ("not allowed with explorer access") and the UI puts a **reCAPTCHA** in front of the
form. MCC `324-458-6445` → Accounts → **+** → *Create new account*, tick the CAPTCHA, then: name **SixPackAbs.com**,
`America/Chicago`, USD, **skip billing**, take the "create an account without a campaign" / Expert Mode link.
⚠ **FOR DAN, unrelated but found in the change log: the "$2.00 CPC ceiling killed Search on 09-10" explanation is
dead — the ceiling is already GONE.** Today 09-11 it was removed from Brand at 14:39 in the Ads UI and from Non-Brand
at 14:46 by **`GOOGLE_ADS_RECOMMENDATIONS` — Google's auto-apply, not a human.** Both campaigns now read
MAXIMIZE_CONVERSIONS with no target CPA and no ceiling, Non-Brand "Eligible (Learning)". Nothing here touched
bidding. Worth knowing that auto-apply can change bid settings on this account by itself.
Docs: `Docs/GOOGLE_ADS_API.md` (new GA4 + MCC sections), `Docs/VSL_LANDING.md` (the home-vs-`/start` A/B is closed).
Memory: `google-ads-ga4-link`, `google-ads-account-creation-blocked`. No dashboard row (his 09-08 rule).
Delete this entry once Dan has made the MCC account and seen the bidding note.

**Video editing strategy — RESEARCH DELIVERED 2026-09-11, Dan picks what to run.** Private report "The Muhammad
Standard" (https://claude.ai/code/artifact/0fac6195-accb-415b-99fa-70e3825d4906): every approval of our video work came
where the design was fixed (verticals/Shorts cut from Muhammad's masters, the locked website recipe). Plan: room acoustic
treatment → shadow-edit every Muhammad delivery + blind review page → Remotion "Muhammad kit" → one shared engine → hand
over formats by blind test. Three starter prompts in the report; nothing executed. ⚠ It recommends folding VQC-B into
the engine rather than firing it as written. Delete once Dan has chosen.

**Zeeshan content batch video 1 (ab wheel workout only) — ROUND 1 DOC WRITTEN 2026-09-11, Dan forwards.** His
"Video 3.mp4" is batch video 1 (his own file count). Round 1 is pasted at the TOP of "Zeeshan Video Revisions"
(`13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk`); Dan added framing / sets-mic / music items, and the music slot now
links Pixabay "Energy Gym Thunder" (knox-gym, rock, 3:32, NOT Content ID registered, AI-generated — Dan listens first).
Paste-ready Upwork message in `/Volumes/Extreme/_edit_work/revisions-0911/out/video1_abwheel_workout.summary.md`.
Delete once the next cut arrives.

**Subscriber list was PUBLIC — BOTH DEPLOYS LIVE AND VERIFIED 2026-09-11. ONE STEP LEFT AND IT IS DAN'S CLICK.**
The newsletter list (`subscribers-data.json`, 28 entries / 23 real addresses) was persisted to THIS PUBLIC repo and
served at `raw.githubusercontent.com` to anyone, no login. It now persists to Postgres (`subscribers` table), and
deploy 2 (`6e1bfc3`, merge of `c08938b`) has removed the file from the tip + gitignored it — `raw.githubusercontent.com`
now returns **404**, Railway deploy SUCCESS, absbyai.com 200.
**Verified BEFORE merging, not just by counts:** `/api/subscribers/status` reads 28 dbRows / 28 inMemory / 21 mailable,
and a field-by-field compare of every Postgres row against the snapshot found **27 entries byte-identical and one
differing in exactly 3 fields** — `h***@melottogroup.com` welcomeStep 4→5, welcomeNextAt →null, welcomeSentAt gaining
`5`, because that person's fifth welcome email was due 22:15Z and sent normally. So the live digest is now
`9dbf07fe248093b9cebcb50f4c10c46a32a0b4fb0f350dd3b094dd29097f4c1f`, not the `1f0cb629…` written here earlier;
`byStep {"0":1,"1":5,"3":4,"4":1,"5":17}`. **Nothing was lost and no welcome progress was reset.**
⚠ The expected-digest trap for anyone re-verifying: the digest covers welcome state, so the sequence advancing
changes it legitimately. Compare the DB against `~/.absbyai-subscribers-snapshot-20260911.json` (0600, outside the
repo, kept because the merge deleted the in-repo copy) rather than trusting a digest match. Reading prod Postgres from
the Mac needs `DATABASE_PUBLIC_URL` from `railway variables --service Postgres` — the cached `DATABASE_URL` is
`postgres.railway.internal` and will not resolve.
**(1) DAN, THE ONLY THING LEFT: make the repo private** (his call 2026-09-11 — Settings → General → Danger Zone; no
API tool for it). The addresses are still readable in git HISTORY, and that is what closes it; it also covers
`monarch-data.json` (net worth + 61 points of history), `credits-data.json` (live Stripe session ids),
`watch-data.json` (resting HR) — audit in `Docs/SUBSCRIBER_STORE.md`. **Checked this session: going private breaks
nothing.** Every GitHub read/write in `server.js` is authenticated with `GITHUB_TOKEN` (monarch, todos, timesheet,
digests, plan, task-checks, push-subs, watch, credits, subscribers), and there is **no unauthenticated
`raw.githubusercontent` fetch anywhere in the tree** — that was the one thing that would have broken. Only moving
part is Railway's GitHub app; after he flips it, push a trivial commit and confirm the deploy, and reconnect in
Railway if it hiccups (the running site stays up either way).
⚠ Armed but not fired: `push-subs.json` gets created in the repo the moment anyone subscribes to web push. No dashboard row.

**studio-blue-89 social variations — DELIVERED 2026-09-10, Dan picks.** Black / white / crimson backgrounds (full +
4:5, original pixels through the existing cutout) and two Muay Thai gym versions (Thai camp, modern gym — AI room, his
original pixels pasted back, 4:5 only) in `photos/finalized social media photos/_variations/studio-blue-89/`; two
alternates in `_alternates/`. $0.97 spent. Recipe in `/background-removal`. No dashboard row. Delete once he has picked.

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

**Ad 5 "Every Diet You've Tried Failed" (Muhammad V3 HD) — FILED + SCHEDULED ON EVERY PLATFORM 2026-09-10, nothing
blocked.** Public Wed 09-16 9 AM CT: YouTube `bwfSQopZy1w` + FB / IG @danrosefit / TikTok via Blotato (@abs.by.ai 09-17; `scripts/blotato/ad5_queue.py`,
queue 197/200). Thumbnail = Dan's pick B2 (clean white backdrop, white-23), live + read back. Optional in Studio: a
pinned comment. Delete once it posts.

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
✅ The iOS **restore** false-conversion is FIXED 2026-09-11 (`549946a`): a restore no longer fires Trial Signup,
`membership_subscribed` or TikTok StartTrial. ⚠ Native retest: one sandbox "Restore purchases" on iOS.
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

**Muhammad round out 2026-09-10 — SIX SECTIONS APPENDED TO HIS DOC, Dan reads and forwards.** Batch doc
`1L2XJKLFrRJHKlcL4Iii70iFvZeiNNeplxYQw2aeAJ_A`, read back byte-intact. **Ad 3 r5 and Ad 4 r3 are APPROVED** (approved-line
sections; audio −13.7 / −14.0 LUFS, no clipping); Ad 8 r2 (2 items: five AI labels 50% bigger), Ad 9 r2 (4), Ad 13 r2 (4),
Ad 15 r1 (10 + audio: −12.6 LUFS, −0.2 dBTP, first cut in the batch that came in OVER). **Ad 5 v3 HD received and verified
final** — frame-identical to the approved cut, 1080p, −14.0 LUFS at −1.0 dBTP, every gate row passes; not yet filed or
uploaded. Md copies in `revision docs/*9-10-26.md`; work dir `/Volumes/Extreme/_edit_work/revisions-0910/`; paste-ready
Upwork messages in `out/*.summary.md`. ⚠ Found: the only "real app recording" (`example generation video.MP4` =
`09_CLIP_app-generate-future-self.mp4`, same 62,300,869 bytes) uploads a STRANGER, not Dan — so every phone demo in the batch
(Ads 6, 8, 9, 10, 13, 14, 15) carries a before picture that is not Dan; the 09-10 items use Dan's Ad 14 form ("use this photo
for the before picture in the clip" + `02_BEFORE-PICTURE_dan-200lb.png`). Dan's calls (not in the doc): Ad 13 whether the
SIXPACKSHORTCUTS.COM watermark also goes; Ad 15 the empty image slot at 0:25.5 and whether Ad 15 runs as an ad at all (the
script note says YouTube content first). Delete this entry once Dan has forwarded the doc and the next cuts arrive.

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
floor marks: Jeff marks spots at the first shoot; installer FILLS the stands' own sandbags — Dan bought sand 09-10).
Stool = the Linon 29" barstool he already has. **Craigslist post: Dan posted it himself 09-10 — do NOT re-post.**
**Duplicate VIVO TV floor stand: return CONFIRMED 09-10** (order 114-5180568-9257862, "Ordered too many", still boxed) —
$11.40 return shipping deducted from the refund. **UPS home pickup BOOKED 09-11 (Dan paid $16.15): Mon 09-14, 10 AM–7 PM,
front door, request # 298404F1F6B, label 1ZY228K59022913823** — Dan prints the label, tapes it on the box, slip inside.
Next: Dan picks an installer from the replies and shares the sheet link. After install: build
the look-A telemetry loop file.

**@danrosefit Meta ads — $50 review DONE 2026-09-11, two calls for Dan.** Private report:
https://claude.ai/code/artifact/18397bc8-efc4-4554-a440-7961cbaa423d. **$2.02/follow** since 09-08 (586 − 566 = +20 on
$40.43, all-in incl. tests; 6.1 % of 329 visits followed) → under $3. **Dan: raise champion ad set `120250753601020682`
$6.50 → $8.00/day?** (not raised). Two dead reel tests paused (macro estimates, lost-weight hour); image tests lead at
$0.07/visit vs the champion's $0.10 — six tests judge 09-13. **Dan: confirm both [DAN] [ENGAGEMENT] campaigns stay OFF**
($96.64 lifetime → 26 profile visits, vs 747 for $80.45 here); leave the 3 IG GEO drafts unpublished, never the global
"Review and publish". The digest's "cost per video view" alarm was a false positive (image tests), fixed `f5feb67`.
Next follower reading Fri 09-18 against the table in `Docs/AUTO_BOOST.md`. Delete once Dan has answered both.

**Ads digest — BOTH PLATFORMS LIVE (Meta 09-02; Google 09-10 via `scripts/ads/api/client.js`, no developer
token); Google half extended 2026-09-11.** `brief-ads.json` reads `platformsLive ["meta","google"]`, `blind []`. Google
now carries `yesterday` / `last7d` spend, clicks, conversions + the ~2x `est*` subscriber estimate beside the raw
column, per platform and per campaign; 56 tests (`scripts/ads/ads-digest.test.js`, section 10 runs the Google leg
offline). Doc `Docs/ADS_DIGEST.md`; the render spec is in the morning-brief task's `SKILL.md`, outside the repo.
⚠ **For Dan: both Search campaigns went dark on 09-10** — Brand 1 impression, Non-brand 4, $0 each, against 7-day
averages of $12.83 and $11.82/day — since the $2.00 CPC ceiling set 09-09 (both still ENABLED/SERVING). The digest
flags both as `spend_stopped`. Raise the ceiling or accept it. Delete this entry once Dan has seen that.

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
approval or a rejection within a day or two. **Still IN_REVIEW 2026-09-10; expedited review requested and
GRANTED that day** (Dan's go; the old Resolution Center thread is closed, so no written note reached Apple). Fallback if they hold the line is spec'd at the bottom of
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

- **`Handoffs/handoff-20260911-codex-video-editing-trial.md`** — Dan's one-month trial through Oct 11: raw footage to Muhammad's standard; first organic ab-wheel + Ad 1, then transfer tests. Codex owns this trial; no dashboard row. Next: independent raw-audio/picture sample of the ab-wheel video.

Swept 2026-09-08. The first four are on the dashboard's **Handoffs to fire** list (Dan's ask, 09-08) with their starter
prompts. Whoever runs one deletes its row there AND removes it here and from `Handoffs/README.md`.

- **Square (1:1) versions of every finalized ad — six per-ad docs + `Handoffs/handoff-20260911-square-ads-00-shared-rules.md`
  (read first).** Rep's ask: 1:1 fills Demand Gen in-feed/Discover/Gmail. Each is a re-layout of the ad's vertical
  build (same EDL/grade/beats/captions, audio bit for bit), 1080×1080, all gates + the audit. Firing order:
  `…-ad1-muhammad.md` (now; Ad 2's is EXECUTED) → `…-ad5-muhammad.md` (after the Ad 5 revisions) →
  `…-ad4-muhammad.md` (after its vertical is approved) → `…-ad3-muhammad.md` (after Muhammad's corrected HD + vertical) →
  `…-ad1-zeeshan.md` (after Dan approves that vertical). Fable 5.1 high each. **Not on the dashboard.**
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
- **`Handoffs/handoff-20260911-video-quality-engine.md`** — **the video-quality work as ONE document**
  (Dan, 2026-09-11: he had four and fired none). Merges VQC-B + VQC-D Phase 5 in full, in build order:
  (1) `_shared/deliver/gate.py`, one version-stamped gate replacing **17 forks / 3,083 lines**; (2) **portable
  framing moved FORWARD into that gate** — it was LAST in the old order, yet framing is **4 of the 11 rejections**
  in the corpus and today's hair check only runs on the 8/28 kitchen set; (3) watch pass mandatory in all six
  skills (hard gate in 1 today, `/shorts` mentions it zero times); (4) a locked kit for ONE format, proven by a
  **blind A/B in front of Dan** using matched pairs already on the Extreme drive. Measured basis: our 11 rejections
  are **5 audio + 4 framing**, and they repeat because `_shared/` has **no picture/framing/cut/caption module at
  all** — a fix lands in 1 of 6 pipelines. Acceptance test throughout: `_shared/qc_corpus/run.py` green.
  Fable 5.1 high, ~3–4 sessions. ✅ VQC-A done (`a696ac4`). Evidence: `…-video-quality-to-muhammad-standard.md`;
  baseline `Docs/VQC_baseline_20260909.md`. **Not on the dashboard** (his 09-08 rule).
- **`Handoffs/handoff-20260911-vqc-phase2-portable-framing.md`** — **PHASE 2, fire next.** Phase 1 of the
  engine doc is DONE and pushed (`eff3896`, `5e10200`). Makes the framing standard portable: today's hair check
  depends on the luma profile of the door behind Dan in the 8/28 kitchen and runs on one set in one skill, while
  `/shortad-from-longform` re-crops him into vertical for every ad with **no framing rule at all**. All five
  `framing:` rows are arithmetic on one per-frame tracker; the corpus already encodes the acceptance test (fail
  rev 2 / rev 3 / `v2-short3-offcentre`, pass rev 4 / 5 / 6). ⚠ **Item 0 first, half a session: the banned-screen
  pairing fix — our compliance scan is BLIND and so are `/ad-edit`'s and `/website-video`'s**; the discriminator is
  already measured (`_shared/deliver/formats.py`, `_BANNED`). Fable 5.1 high, ~2 sessions. **Not on the dashboard.**
- **`Handoffs/handoff-20260909-vqc-C-phase4-cut-technique.md`** — **fire after the engine doc's Phase 1,
  BEFORE its Phase 4.** The measured #1 gap to Muhammad: he cuts picture **1–15 frames off the audio splice on a
  pose-matched frame** (`piccuts.py`, built for Ad 2, never promoted) — plus 0 px landing, dead air paired with a
  picture cut, and the grade. ⚠ **Scope corrected 2026-09-11:** its item 2 (push coverage) is now the engine doc's
  Phase 1 rows, and its item 6 (`picture.json`) is the **input to that doc's Phase 4** — build it first or Phase 4
  re-derives it. Fable 5.1 high, ~1–2 sessions. **Not on the dashboard.**
- **`Handoffs/handoff-20260911-junk-footage-pass.md`** — **fire after the engine doc's Phase 1; parallel-safe with its
  Phases 2–4.** Extracted from VQC-D Phase 6 so nobody has to fire a half-superseded doc. Six junk detectors that
  already work but have never been run together → one pre-render `junk_report.json`, plus **take selection, which
  does not exist at all** (we remove flubs, we never pick the best take). Junk is 1 of the 11 rejections; the test is
  corpus entry `spraytan-longform-rev0`. Cheapest item left. Fable 5.1 high, ~1 session. **Not on the dashboard.**
- **VQC-B and VQC-D are fully superseded** and carry do-not-fire banners; they stay on disk as source material.

Dead, do not run: `handoff-20260901-danrosefit-ad-identity-fix.md` (superseded — the @danrosefit profile-visits
campaign has been live via the API script since 09-02), `handoff-20260902-shorts-centering-queue-fix.md` (done
09-02), `handoff-20260902-google-ads-engagement-champion-automation.md` (LIVE since 2026-09-08 22:00 UTC; operating doc
`Docs/YTADS.md`).

---

# ACTIVE TASK

**Codex one-month video-editing trial — PLAN SAVED LOCALLY (2026-09-11).** Interview/source inspection complete; plan in `Handoffs/handoff-20260911-codex-video-editing-trial.md`, also saved on LOCAL branch `codex/video-trial-plan-private`. Automatic review blocked the push; GitHub confirmed the repo is public, so do not stage/push the plan containing Dan's business details without explicit publication consent. Codex owns the separate trial; next: freeze ab-wheel references and rebuild 60–90 seconds from raw picture/audio, respecting the two-build cap; no trial render yet.

**Video-quality engine PHASE 1 — SHIPPED 2026-09-11 (`eff3896` + follow-up), nothing blocked. Two things for Dan.**
`_shared/deliver/gate.py` is now THE delivery gate for all seven video skills — **30 rows x 7 formats, no holes**
(`gate.py --audit` proves it), every bound in `formats.py` beside the file and date it was measured on, versioned
stamp that invalidates older ones, `NOT MEASURED` and `UNCONFIGURED` both FAIL. Registered in the corpus and PROVEN:
`style:coverage`, `style:static_run`, `cut:uncovered_joins`. New rows nothing had: **`audio:lipsync`** (the
`alimiter` 4.966 ms every loudness-finished master has carried — the audio gate checks length, never alignment) and
**`compliance:labels`** (Dan's 09-11 real-vs-AI rule as a PAIRING check). Exercise-demo calibrated off the 33 shipped
demos. Standing rule in `AGENTS.md`; module README lists every known gap.
⚠ **FOR DAN, a live ads exposure: our banned-screen compliance scan was BLIND, in `/ad-edit` and `/website-video`
too.** It matched the app *recording*, not the *screen*, so a different generation of the same BEFORE/AFTER screen
read 0.526 against a 0.72 bar — the spray-tan longform has carried it at 18:04 all along. Rebuilt as a paired
chrome matcher it now flags it (0.626, 87/91 frames), but an approved master's own app screen reads 0.577, so the
margin is 0.003 and it is **live but NOT corpus-registered**. The next discriminator is measured and written down.
⚠ **The 17 forks are BANNERED, NOT DELETED** — five video builds were in flight tonight (ad1-sq, ad2-sq, ad3-vert,
ad4-vert, ad5-vert) and each fork still holds rows the shared gate has not absorbed. Delete at the end of Phase 3.
Found in passing: `public/exercise-demos/plank.mp4` ships at 960x536 where all 32 others are 960x540.
**Next: Phase 2 (portable framing) in a fresh session** — the handoff records exactly what changed for it, and says
to fix the banned-screen pairing test early. No dashboard row (his 09-08 rule). Delete this entry once Dan has read
the two warnings.


**Ad 2 square (1:1) — DELIVERED 2026-09-11, Dan reviews.** `Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/
… | claude | 1x1 | ad 2.mp4` + 540p/480p review copies, A/B audio, stamp, `notes-square.md`, `recipe-square/`. 1080×1080,
**8,275 frames = his to the frame**, and the audio is the APPROVED VERTICAL's AAC stream **md5-identical** (`muxsq.py` refuses to
write otherwise). No cutdown — Ad 2's vertical never had one. `qc.py` **19/20**; watch pass 88/88; centering median +0 px,
0 sustained runs; hair min 24 px; landing 0 duplicated frames; 0 newly bare splices. **The independent audit returned "does not
ship" with 4 findings after a 20/20 — worst: the conveyor lower third was rendered ENTIRELY OFF FRAME for 4.3 s (a 9:16 default
passed by the caller), so that beat had no words at all. All fixed and re-verified on the delivered frames.**
⚠ **The one red row is qc 20 (caption sync, 98.2 %) and it is the INSTRUMENT, not the captions:** a concurrent session moved
`caption_sync_check.py` to full resolution mid-build, and Muhammad's graded room tone sits inside ±22 of his own olive accent,
so the mask matched 13,347 px where the lit word is ~1,200. **All 12 flagged words were pulled at full res and are correct and
legible.** Recorded in the gate file + `notes-square.md`; NOT tuned away. Optional picture-side fix if Dan wants it: the scrim
([A6].17). Skill: **[A10]** + `reference/a10_sq/`. Dashboard row stays unchecked until Dan approves (verticals rule).
Delete this entry once he has.

**8/28 shoot Drive backup — UPLOADING OVERNIGHT 2026-09-11, self-verifying 09-12. Nothing for Dan to do.** The
267 GB / 259-file 8/28 shoot existed on ONE drive with no backup of any kind — it is the source of every ad in
production. `rclone` (installed at `~/bin/rclone`, remote `gdrive` authorized) is copying it to Drive folder
`1gzGtstw-WGjo4fK4QL11UMbwST9YFw37`, wrapped in `caffeinate`, resumable, `.DS_Store` excluded. Measured ~4 MiB/s
(his uplink, not throttling — zero 403s), so ETA ~13:00-14:00 CT 09-12. Scheduled task `verify-828-drive-backup`
fires 08:30 and either reports progress or runs
`scripts/backup/verify-drive-copy.sh <src> <folder-id>` (MD5 per file; expect 259 files / ~266.5 GiB) and deletes
this entry on PASS. ⚠ Do NOT run the verify script mid-transfer — it reports a false FAIL on an incomplete copy.
Remaining gap after this: the welcome-video first shoot (114 GB), the last irreplaceable folder with no second
copy. Drive is a 5 TB plan, 4.5 TB free. No dashboard row.

**Ad 1 "This Picture Got Me Abs" — 1:1 SQUARE + ≤0:59 square cutdown from the APPROVED 9:16 vertical — IN PROGRESS
(session started 2026-09-11 17:35 CT, owns it).** `Handoffs/handoff-20260911-square-ad1-muhammad.md`; build dir
`/Volumes/Extreme/_edit_work/ad1-sq/` (the attempt-3 pipeline re-laid-out for 1080x1080: `sqlib.py` + `sqassets.py` +
`render.py`). Lands on Muhammad's **6,976** frames (the approved vertical is 6,977 — the frame-count assert postdates it);
audio is the vertical's AAC stream copied bit for bit. ⚠ **A CONCURRENT SESSION owns `/Volumes/Extreme/_edit_work/ad2-sq/`
(the Ad 2 square) — do not touch it, and do not start a third video build** (AGENTS.md cap of two).

**Ad 4 "Stop Wasting Money on Supplements" — 9:16 VERTICAL + ≤0:59 CUTDOWN from MUHAMMAD's V4 HD — REVIEW COPIES DELIVERED
2026-09-11, Dan reviews + ONE CALL.** Folder `Muhammad Ad Videos/stop wasting money on supplements - ad 4/`: his V4 HD filed
(committed `hd_vs_draft.py`: IDENTICAL to the approved r3 draft), our REVIEW 540p/480p of both cuts, both A/B audio clips,
`notes-vertical.md`, `recipe-vertical/`. Master 7,160 frames = his to the frame, cutdown 57.19 s; **his audio untouched**
(full length = his AAC stream md5-identical; cutdown = his mix cut at the seams). `qc.py` **18/20 on both** — the two FAILs
are one finding: **his export peaks at −0.90 dBTP against Dan's −1.0 rule**, so the verbatim stamp cannot pass and
`deliver4.py` refuses the MASTERS (held in `/Volumes/Extreme/_edit_work/ad4-vert/`). Three independent audits: 10 findings,
then 4, then all verified — **audit 3: SHIPS on both files**. **Dan: (1) accept the −0.9 dBTP or have Muhammad re-export at
−1.0 (then a 5-minute re-mux + `deliver4.py` puts the masters in the folder); (2) an ear check on three spots listed at the
end of `notes-vertical.md`.** Dashboard row for the verticals stays unchecked until he approves (his rule). Skill: [A8] +
`reference/a8_ad4/` committed (6128273 + this session's follow-up). Delete this entry once he has approved and the masters
are delivered.

**Muhammad Ad 7 r3 + Ad 10 r2 — APPENDED TO HIS DOC 2026-09-11, Dan reads and forwards.** Batch doc
`1L2XJKLFrRJHKlcL4Iii70iFvZeiNNeplxYQw2aeAJ_A`, read back byte-intact. Ad 7: Photoshop now Dan's face; 3 items + the new "Real
picture of me" label. Dan's 09-11 changes are folded in: the CLOSING demo keeps the stranger (he is Asian) and ends on
that recording's own AI after picture, cropped and uploaded as `13_AFTER_ai-generated_app-demo-man.jpg`
(`1gFwcbYiRvoGQz1WJ7oKj-T7dRAM2zRPp`) — only the 2:00 demo swaps in Dan's before picture — and he deleted the 1:53
adjacency item himself ("it's not really a before and after"), so Ad 7 is 2 items + the label. New standing rule from
this round, in `/revisions` as calibration pass 5: whose generation is on screen follows the SCRIPT (his line → his
pictures, prospect line → an AI stranger), a DIFFERENT generated person in every ad, generated by us when we have none. Ad 10: all 11 round-1 items done; 2 items + the label. Both: the app demos' before picture is the
stranger from the recording (lesson 40). Audio fine on both. Md copies in `revision docs/*9-11-26.md`; work dir
`/Volumes/Extreme/_edit_work/revisions-0911m/`. Delete once Dan has forwarded and the next cuts arrive.

**Ad 3 "Stop Paying Human Trainers" — 9:16 VERTICAL + ≤0:59 CUTDOWN from MUHAMMAD's v6 HD — IN PROGRESS (session started
2026-09-11 14:05 CT, owns it).** /shortad-from-longform on Drive `1qsBpkrm8T7BDaYF67NL1k_x67sTsxsb3` (265.2 s, 29.97);
raw roll C1593 (8/14); build dir `/Volumes/Extreme/_edit_work/ad3-vert/` (a7 pipeline). Ad 4's vertical is a DIFFERENT
session in `ad4-vert/` — do not touch either build dir. **Status 20:00 CT: RENDER 3 BUILT AND WATCHED; render 4 waits
on the second audit.** Render 3 passed every gate (7,948 frames, his audio md5 = his, caption sync 397/397, hair gate,
0 black frames, no duplicated frames at any cut) and carries all 18 audit-1 findings + the 3 from my first watch pass.
My watch pass ON RENDER 3 (42 sheets, 249 boundaries) then found 3 MORE, now coded for render 4: (1) ⚠ **the app card
still showed the stranger** — the floor fixed its opening, but the recording's "Creating your future self" screen puts
that man's photo back on screen full size from source 8.52 s, and the card ran to 10.23; it now ends at 8.45, on the
Generate button (both library recordings are the same session — there is no take with Dan); (2) three ZOOM ISLANDS
(1665, 3407, 7155) where a picture cut landed 4-7 frames before a punch, so the level popped FAR and straight back —
the audit's item 11 in three more places; a new PUNCH_SNAP rule starts a punch AT the cut when one is within 10 frames,
which also matches his own measured ramp starts (fit.json: ~1666, ~3409, ~4819, ~7155); (3) the forced level flip at
1732 did nothing and should not — his scale reads a flat 1.22 either side of his own cut there, so any change would be
ours. Verified fixed on screen: the four moved cuts, window headroom, the workout phone opening on the top, headers
typing on, the real-picture label on all four stills, his flag pop-zoom. Cutdown NOT yet rebuilt (`cut5.sh`; cut/ is a
FORK with its own beats/g3/g5 and an embedded time map). Cutdown true peak −0.90 dBTP vs a −1.0 bar — ✅ Dan accepted
exactly that on Ad 4 on 09-11 ("I think the audio sounded fine"), which likely answers this too.
⚠ **Muhammad's Ad 3 v6 HD is NOT the approved round-5 draft:**
at 2:14.1–2:23.1 the "Because even though I was a personal trainer…" bullet lost "back in my 20s, as a 38 year old dad
running a successful ad agency." (proof `ad3-vert/hdcheck/w4_hd_vs_draft.png`, sent to Dan 14:38). Do NOT file or upload
it as final; Dan asks him to re-export. The vertical rebuilds that graphic with the full text, so it is unaffected.

**Ad 5 "Every Diet You've Tried Failed" — 9:16 VERTICAL + 0:59 CUTDOWN — ROUND 1 REVISIONS RE-DELIVERED 2026-09-11, Dan
reviews.** All three of his asks are in: every real after picture is FULL-BLEED PORTRAIT and carries the new **"Real picture
of me — not AI-generated"** chip, his two LANDSCAPE stills are replaced by pool-shoot portraits (`photo-221`, `photo-247`)
and the two-photo panel is now two full-screen STUDIO shots (`studio-gray-79` then `studio-white-23`); AI pictures keep
AI-GENERATED. **Muhammad's audio untouched** (master stream md5 = his; cutdown = his mix cut only). Cutdown 54.92 s.
`qc.py` **20/20 on both**, corpus 19/19, **three independent audits** (`audit4/5/6`) — the first two returned DOES NOT SHIP
and both blockers are fixed: `studio-white-23` was 218 px off-centre in its own source (now `ox=0.02`), and my first caption
fix (a full-width gradient) fogged the white backdrop, replaced by a caption-sized black plate. Also fixed, pre-existing:
the cutdown's 0:16.7 seam ended two frames inside one of his light leaks (A8.13 ported to `zcutdown.py`).
⚠ **Two shared-gate fixes are in `reference/caption_sync_check.py` and MUST NOT be lost: per-process temp files** (it wrote
`/tmp/_cs.wav`, and with two builds running one graded the OTHER's audio — 8 phantom failures) **and least-washed-frame
sampling** (a word inside an editor's light leak is unreadable on the frame the gate happened to pick). The first fix was
already clobbered once by a concurrent rewrite of that file and has been merged back. **The `ad3-vert/` and `ad4-vert/`
build copies still write the fixed `/tmp` paths and can still collide with each other — those sessions should re-copy the
skill's version.** ⚠ The new `_shared/deliver/gate.py` is NOT yet wired to this build: see the note below. Build dir
`/Volumes/Extreme/_edit_work/ad5-vert/`. Delete this entry once Dan approves the revised cuts.

**`_shared/deliver/gate.py` RUN ON THE AD 5 VERTICAL — master 26 pass / 2 fail, cutdown 27 / 1; three findings for whoever
owns Phase 2.** `plan_build.py` (committed, `reference/`) generates the plan from a build's own files incl. a Whisper
transcript of the FINISHED render. Passing: script_fidelity **100 %**, banned_screen clean over 7,036 frames, uncovered_joins
**0**, jump_cut **0**, click_at_joins 0/58, lipsync 0.000 ms, card_collision 0/86, watch:pass tied by sha256.
(1) **`compliance:labels` cannot be measured on a Muhammad-style build:** it takes ONE chip position per kind, and his card
design puts the AI chip at each card's own bottom-right corner — ours sit at four positions, so the goal-image card (10 px
off) reads 0.23. **`0 carrying the WRONG label`**; the real-picture chip passes on all seven photos, and the row PASSES on
the cutdown. (2) **`cut:min_segment` flags two framing segments of 5 and 3 frames** (68.60 s, 133.17 s) — pre-existing in
the crop Dan approved, surfaced by a gate that postdates it; `zcrop` was not re-run because the EDL did not change. A
one-line merge of each stub into the hold before it would clear it in a future round. (3) **`captions:graphic_clearance`
needs per-graphic MOVs** a Python frame compositor never produces; **`captions:sync` NOT MEASURED** (needs cues after 0.3 s
of silence; this cut has one) — `qc.py` 20 covers it at 99.7 %. ⚠ **Feeding `crop.json`'s `holds` straight into `punch` is
wrong** — 20 of 68 are contiguous same-level splits and read as **8 jump cuts that do not exist**; merge them first.

**sixpackabs.com video-first redesign — LIVE ON PRODUCTION 2026-09-11, Dan confirms.** https://sixpackabs.com now
runs `sixpackabs-child`: video-first homepage (latest long-form plays in place), a page per public video at
/videos/<slug>/, /videos/ + /shorts/ archives, @danrosefit photos, new header/footer site-wide. **URL gate 219/219 = 200,
no redirects**, every page type checked, player/menu/newsletter/PostHog verified on the live site. 18 videos + 6 photos
imported and refreshed hourly. Staging kept for future changes:
https://staging-cac5-danroseconsulting-fedqa.wpcomstaging.com (robots-blocked).
⚠ **Deploys are a ZIP upload, not `deploy.sh`** (SSH never needed; `SPA_SSH_*` still unset) and **every theme update
needs Settings → Caching → Clear all** or WP.com serves the old build to plain URLs. Theme activation can go through
the WP.com connector's `theme.set` — that is how production was switched when the Chrome extension dropped.
⚠ Rollback = re-activate Twenty Twenty-Five; the July DB template overrides are intact and come back untouched, so
do not delete them. **Open for Dan:** whether to update the Yoast homepage title/description to the video-first
positioning (not changed — it affects SEO). Doc: `Docs/SIXPACKABS_SITE.md`; recipe + traps: `sixpackabs/README.md`.

**Demand Gen conversion campaign `24243839443` — LIVE, 6 ad groups (Ad 1 / Ad 2 / Ad 5 × /start / home), $20/day
unchanged, target CPA $30 on Free Generation Started.** First ~18 h (to 09-11 10:00 CT): $20.14, 17 clicks, **0
conversions**, still LEARNING; PostHog shows ~18 visitors landed and none uploaded a photo. **09-11: retry-rule attempt 2
applied** — the limited Zeeshan `1oEcwdp21Fg` ads 824179684065/824179684203 PAUSED, tamer-copy r2 ads 824329225648 /
824329225651 in review. **Ad 5 added** on an UNLISTED ad copy `Yo-6TQik3qY` (thumbnail B2): ad groups 200151423317
/start + 200151529597 home, in review. Next: re-run `node scripts/ads/api/client.js policy 24243839443` ~09-12; if r2 is
limited again, attempt 3 = clean text-free thumbnail on `1oEcwdp21Fg`, then remove the chain. Add Zeeshan's Ad 1
verticals / Claude's Ad 5 verticals only after Dan approves them; Ads 3/4 when Muhammad's HD lands. Record:
`Docs/DGEN_CONVERSION_CAMPAIGN.md`. ⚠ Remarketing campaign 24169507109 spends ~$2.50/day with 0 clicks, 0 conversions
ever ($48.75+ lifetime) — Dan's call whether to pause. Delete this entry once review settles on r2 + Ad 5.

**Ads 3 + 4 — LIVE AND APPROVED 2026-09-11 (new skill `/ad-setup`).** Google approved all four ads ~14:40 CT (no
limited line, no clickbait flag); ad groups ENABLED at $30, campaign $20/day across 10 groups. ✅ **Ad 4's −0.90 dBTP
true peak: DAN ACCEPTED IT AS-IS 09-11** (*"I think the audio sounded fine"*) — no re-export from Muhammad; this
answers the Ad 4 vertical session's question too. Muhammad's HD
finals unlisted: Ad 3 `QWW1oumpNg4`, Ad 4 `R08TPEtkjuQ` (descriptions + chapters, clean thumbnails, O1/O2 alternates in
the thumbnail folders). Ad groups Ad 3 199782847163 /start + 199360345839 home, Ad 4 202812319169 /start + 203842477407
home, $30 each; ids in `Docs/DGEN_CONVERSION_CAMPAIGN.md`. ⚠ Ad 5's *Why My Diets Kept Failing* headline is DISAPPROVED
(CLICKBAIT) — for the Ad 5 owner above. Dashboard row "Add the new finished ads…" left open only for Zeeshan's Ad 1
verticals. Watch spend/conversions on the new groups from 09-12. Delete this entry once they have a few days of data.

**Ad 1 "this picture got me abs" — 9:16 verticals from ZEESHAN's final — RE-DELIVERED 2026-09-10 WITH HIS AUDIO UNTOUCHED,
Dan reviews.** He rejected the second delivery's audio ("Zishan's audio sounds much better… Use Zishan's audio") — it had
lifted his −23.5 LUFS mix +9.9 dB into a limiter and summed it to mono. Now the full length carries his exported track bit
for bit (md5 = his) and the cutdown his mix only cut; both `qc.py` 20/20 in the new `audio_gate.py --verbatim` mode,
corpus PASS 19/19 (both rejected files are entries and fail three verbatim rows; the `muhammad-ad*-vertical-approved`
entries are committed with it). Rule in `AGENTS.md`; skill Step 4 + lesson 26. ⚠ YouTube `rimBWjT9-oo` / `JOZVk4_HDwQ`
carry the REJECTED audio — upload the fixed files only when Dan approves. ⚠ Zeeshan's own cut shows the banned
email-capture screen at 3:09. Check off the dashboard row "Cut 9:16 vertical ads…" ONLY when Dan approves; then delete.

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
