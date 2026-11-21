# Handoff: Post-lock-in "Your analysis" page — video, sliders, body-fat + muscle numbers, body map, trial CTA

**Date:** 2026-09-08
**Project:** Abs By AI (absbyai.com, `public/index.html` + `server.js`)
**Business goal this serves:** profitability — this is the screen that turns a free generation into a 7-day trial.
**Status:** spec'd, NOT executed. No dashboard row (Dan's 09-08 rule: only when he asks).

## Objective

Rebuild the screen a user sees immediately after they tap **"Lock in this goal"** on their generated image. It replaces
the current email-capture screen AND the "benefits bridge" screen. The new page (screen id `analysis`) must:

1. Show Dan's website conversion video at the top (a slot that takes a YouTube id or an mp4 URL; the final file is
   rev 4 of `claude edited long form content/06 - Website Conversion Video (post-generation)/website_video_16x9.mp4`,
   being rebuilt under `Handoffs/handoff-20260908-website-video-rev4.md` — do NOT execute that handoff here).
2. Put two sliders under the video — **height** and **weight** — that the user drags with a thumb on a phone.
3. Show the user's before picture and after picture.
4. **Deliver on the video's promises**, which are (transcript 1:31–1:42 and 2:20): *"Just look near your image, where
   our AI has already estimated how much fat you'll need to lose and how much muscle you'll need to gain to get to your
   goal physique. It's also identified your strong and lagging body parts."* → current body-fat estimate, goal body-fat,
   current lean muscle mass, goal lean muscle mass, fat to lose, muscle to gain.
5. Show a **body map**: where to focus on gaining muscle, and which parts are already strong and need little work.
6. Make the case that the pictures did most of the work (no long questionnaire), tease what the membership contains,
   and show that a little more context would let the AI show the full potential of the program.
7. End on the trial CTA the video points at: *"tap the button below … try Abs by AI completely free for seven days …
   $19.99 per month"* (matches `MEMBERSHIP_PLANS.monthly` = 1999 cents).

## Current State (what exists today — read this before touching anything)

**Funnel today** (`public/index.html`, one page of stacked `<div class="screen">` sections switched by `showScreen()` at
line ~4089; the section list is the array in `renderScreen()` at line ~4059):

- Result screen `resultSection` (line ~1749): before/after grid, an **"Estimated body fat"** row, "Lock in this goal"
  (`loveItBtn`). Handler at line ~5007: `fireConfetti(); showEmailScreen();`.
- Email screen `emailSection` (line ~1919): "Download Your Future Self…" email form → `POST /api/subscribe`
  `{ email, deviceId, before, after }` (server.js line ~4300), sets `localStorage.absbyai_email`, PostHog
  `email_subscribed`; then `showBridgeScreen()`. Skip button → `showBridgeScreen()`.
- Bridge screen `bridgeSection` (line ~1947): before/after pair + five benefit rows + Continue → `showHub()`
  (PostHog `bridge_seen`, `bridge_continue`).
- Hub `hubSection` (line ~2141): preview mode for logged-out / non-member users; tapping a tool → `showTrialGate(feature)`
  (line ~5744) → signup (`showAuthScreen('signup', {trialGate:true})`) → `continueTrialAfterAccountCreation()` (line
  ~5529) → `seedProfileFromFunnel()` + `startQuiz()` (5 questions incl. a height/weight step) → `proceedToTrialGate()`
  → `showMembershipScreen(..., {trialGate:true, planReady})` (line ~7226) → Stripe embedded checkout (web) or IAP (native).

**Where the numbers come from today — and why they do not deliver the promise:**

- The result screen's body-fat row is a **lookup from the body type the user tapped on the form**, not a photo read:
  `BF_BEFORE` / `BF_AFTER` / `BF_AFTER_HEAVIER_FEMALE` / `BUILD_BEFORE_MALE` / `BUILD_AFTER_MALE` at line ~3718, applied
  by `updateBodyFatDisplay()` at line ~4613. Lean/fit men get a "build" label instead of a percentage.
- **Nothing estimates muscle mass.** The only muscle numbers in the app are the prompt's anchor table at line ~3826:
  *"MALE added lean mass compared to the input photo: subtle ≈ +2 lb, moderate ≈ +4 lb, dramatic ≈ +6 lb, max ≈ +8 lb."*
  Use it as the anchor for "muscle to gain" (women: the app's rule is NO added mass — the entire change is lower body
  fat + definition; see the `NO ADDED MASS RULE` at line ~3859).
- **Nothing identifies strong / lagging body parts.** The trainer (`/api/generate-program`, server.js ~7228) and the
  nutritionist (~7778) each do their own photo read later, behind the paywall, via `PROGRAM_ASSESSMENT`
  (`starting_point`, `goal_summary`, `assigned_level`, `starting_stage`) — prose only, no body-part map.

**Data available at the moment the page opens (before any account exists):** `state.photoData`/`state.photoMime`
(before) or `localStorage[LAST_BEFORE_KEY]`; `state.lastAfterDataUrl` or `localStorage[LAST_AFTER_KEY]` (after, saved
on unlocked generations at line ~6017); `state.gender` (male|female); `state.condition`
(heavier|moderate|fit|very_lean); `state.effectiveIntensity || state.intensity` (subtle|moderate|dramatic|max);
`state.photoIsClothed`; `state.description` (optional free text from the form). No weight, no height.

**Server patterns to copy:** the meal analyzer's raw-fetch structured-output call (server.js ~2700): `fetch(
'https://api.anthropic.com/v1/messages')` with `output_config: { format: { type: 'json_schema', schema } }`, an
`AbortController` timeout, `friendlyAIError()`. Auth: `optionalAuth` middleware; rate limit: `aiLimiter` (line 85).
`sniffImageMime()` exists. Profile whitelist: `sanitizeProfilePatch()` + `PROFILE_ENUMS` (line ~5185) — `heightIn`
(36–96) and `weight` (50–1500) are already accepted; unknown keys are silently dropped. Transformations:
`insertTransformation(userId, before, after, settings)` (dedupes on the after image, returns null when unchanged);
`transformations.settings` is JSONB. `GET/POST /api/account/transformation` (line ~5370) mirrors the hero pair into
`users.before_image/after_image` and fires on every login/hub load.

## Key Decisions Already Made (do not reopen)

- **Placement = right after "Lock in this goal", before any account.** Dan's dictation said "logs in"; he confirmed it
  meant *locks in* (Wispr Flow mishear). The page is the first thing after lock-in.
- **Option B: both the email screen and the bridge screen are replaced.** The email ask moves onto the new page as a
  secondary block ("Email me my picture + my analysis"), same `/api/subscribe` call with `source: 'analysis'`.
- **Sliders, not text fields, for height and weight**, under the video. Default height **5'9"** and the weight that
  corresponds to it (BMI by the body type the user picked, see §3). Before the user touches anything the page runs on
  those defaults; the moment a slider moves, every number recomputes from the slider. Weight follows the height slider
  (BMI-linked) until the user touches the weight slider, then it decouples.
- **One new vision call per lock-in**, structured JSON, cached by image hash so reopening never re-bills. Free to the
  user (no generation credit consumed, no `deviceId` billing path).
- **Model for the vision call: `claude-opus-5`** (the `/claude-api` skill's rule: Opus 5 unless a different model is
  explicitly named; load the skill before writing the endpoint and follow its current request shape — adaptive thinking,
  `output_config.effort`, refusal `fallbacks`; the meal analyzer's `claude-sonnet-4-6` string is a legacy pattern, not
  the choice here). Estimated cost ≈ $0.04 per analysis (two images ≈ 3k tokens + ~1.5k prompt in, ~700 out). At 100
  lock-ins/day that is ≈ $4/day — inside the standing AI-spend authorization. Swap to `claude-sonnet-5` is one string
  if Dan later wants it cheaper.
- **Women get definition framing**: no "+lb muscle" number, muscle tile reads "Definition: moderate → sharp", goal
  body fat from the female clamps (heavier women → `BF_AFTER_HEAVIER_FEMALE`).
- **Body-part labels are "already strong" / "focus here" / "not visible in this photo" — never "weak" or "lagging"** on
  screen (the video says "lagging"; the app's tone rule is encouraging, never judgmental).
- **The video block is hidden for real users until the URL lands**, visible as a labelled placeholder on localhost and
  on production with `?vp=1`, so Dan can review the layout without a dead play button on the highest-value screen.
  (Default — Dan can flip it to always-visible.)
- **Page stays reachable**: a hub tile "My body analysis" reopens it (members: the CTA becomes "Build my program →").
- **Disclaimer stays**: every number is "a visual estimate for motivation, not a medical measurement" with the
  `/sources` link — Apple flagged uncited body-fat numbers under 1.4.1 once already.

## Detailed Plan

### 1. Backend — `POST /api/body-analysis` (server.js)

1. Middleware: `aiLimiter`, `optionalAuth`. Body: `{ beforeBase64, beforeMime, afterBase64, afterMime, sex, condition,
   intensity, clothed, description }` (base64 without the `data:` prefix, exactly like `/api/generate-image`). Reject >
   ~6 MB per image; `sniffImageMime()` both.
2. **Cache key** = sha256(beforeBase64) + sha256(afterBase64) + sex + intensity. In-memory `Map` capped at 500 entries
   (evict oldest). If `req.user`, also check the user's transformation rows for `settings.analysis` on the same after
   image before calling the model. Return `{ analysis, cached: true }` on a hit.
3. Load `/claude-api` and write the call in its current shape: model `claude-opus-5`, `output_config: { effort:
   'medium', format: { type: 'json_schema', schema: BODY_ANALYSIS_SCHEMA } }`, `max_tokens: 2000`, adaptive thinking
   (omit the `thinking` param or `{type:'adaptive'}` — never `budget_tokens`), the refusal `fallbacks` the skill
   prescribes, `cache_control` on the system block (verify `usage.cache_read_input_tokens` > 0 on the second call; if
   the prompt is under the model's minimum cacheable prefix it silently won't cache — acceptable). 60 s abort.
4. **`BODY_ANALYSIS_SCHEMA`** (`additionalProperties:false`, all required):
   - `photo_coverage`: `full_body | torso | upper_only`
   - `confidence`: `high | medium | low` (clothed before photo ⇒ never `high`)
   - `bf_now_low`, `bf_now_high` (integers, %), `bf_goal` (integer %, read off the AFTER image)
   - `muscle_base`: `building | moderate | solid | advanced`
   - `muscle_gain_lb` (integer; men: the intensity anchor 2/4/6/8 adjusted ±2 from the photos; women: 0)
   - `regions`: exactly eight objects `{ id, status, note }` with `id ∈ shoulders | chest | arms | upper_abs | lower_abs
     | obliques | back | legs`, `status ∈ strong | focus | maintain | not_visible`, `note` ≤ 90 chars, second person
   - `headline` (≤ 80 chars, second person, encouraging — e.g. "Your frame is ready for abs; the gap is fat, not muscle")
   - `focus_summary` (1–2 sentences), `training_focus` (≤ 120 chars), `nutrition_direction`: `cut | recomp | lean_bulk`,
     `protein_g_per_lb` (0.7–1.0)
5. **System prompt rules** (write it, keep it stable for caching): the BEFORE is a real photo, the AFTER is an
   AI-generated goal image of the same person — judge the gap; ignore tan, lighting, background, camera; never comment on
   face or attractiveness; encouraging and factual, never judgmental; the intensity anchor table for `muscle_gain_lb`;
   women: no added-mass language; mark `not_visible` honestly (legs/back in a torso shot); no medical claims; output
   the JSON only.
6. **Server-side clamps after parse**: men bf 5–45 / women 12–55; `bf_goal` ≥ 6 (men) / 13 (women) and `<
   bf_now_low`; `muscle_gain_lb` 0–10, forced 0 for women; all eight region ids present (fill missing with
   `not_visible`). Log the model's `bf_now` midpoint against the table midpoint for the tapped body type (console +
   PostHog server event if `posthog-node` is wired; else console) — it is the calibration signal for later.
7. On model failure or refusal: `502 { error }`. The CLIENT falls back to the lookup tables (§2.6) — the server does not
   invent numbers.
8. Persist: extend `POST /api/account/transformation` to accept `analysis` and merge it into the hero row's
   `settings.analysis` with a **JS read-modify-write** (pg-mem has no jsonb `||`, memory `member-profile`); extend
   `GET /api/account/transformation` to return `analysis`. Also write `heightIn`/`weight` through `PATCH /api/profile`
   (`source:'funnel'`) when the sliders were touched — the whitelist already accepts them.

### 2. Frontend — the `analysis` screen (public/index.html)

1. Add `analysisSection` to the `renderScreen()` array (the virtual pageview `/vp/analysis` for Google Ads audiences
   then fires by itself). Nav bar: back → `result`, title "Your analysis".
2. **Video slot** at the top. Config near the top of the script: `const ANALYSIS_VIDEO = { youtubeId: '', mp4: '',
   poster: '' };` YouTube → `youtube-nocookie.com/embed/<id>?rel=0&modestbranding=1&playsinline=1`; mp4 → native
   `<video playsinline controls preload="metadata" poster>`. Empty config → block hidden, except on localhost or
   `?vp=1` where a 16:9 placeholder card (poster still of Dan at the kitchen counter, muted "VIDEO PLACEHOLDER" label)
   renders. PostHog: `analysis_video_play`, `analysis_video_progress {pct: 25|50|75|100}` (mp4 via `timeupdate`;
   YouTube via the IFrame API only if cheap — otherwise play only).
3. **Sliders** directly under the video, one card: "Two quick sliders make the numbers yours."
   - Height: `<input type="range" min="58" max="80" step="1">`, label rendered as `5'9"`; default **69** for men,
     **64** for women (OPEN below).
   - Weight: `<input type="range" min="90" max="400" step="1">`, label `185 lb` with a small `84 kg`.
   - Default weight = `round(BMI[sex][condition] × height_in² / 703)` with BMI **men**: very_lean 22, fit 24,
     moderate 27.5, heavier 31.5 (→ 149 / 163 / 186 / 213 lb at 5'9"); **women**: very_lean 20.5, fit 22.5,
     moderate 26.5, heavier 31 (→ 119 / 131 / 154 / 181 lb at 5'4"). Weight tracks the height slider until
     `weightTouched = true`.
   - 44 px thumbs, `input` event for live recompute, `change` event → PostHog `analysis_slider_changed {which}` and
     `localStorage.absbyai_body_sliders = {heightIn, weight, touched}`.
   - The values flow into `seedProfileFromFunnel()` (add `heightIn`, `weight`, `weightUnit:'lb'`) and `startQuiz()`
     skips the `body` step when both are already known (filter `QUIZ_STEPS` at start; do not mutate the const).
4. **Before / after pair** (reuse `.before-after-grid` markup and the "Today / Your goal" labels from the bridge).
5. **"What our AI already knows from your pictures"** — four tiles, recomputed on every slider input:
   ```
   W = weight; bfNow = (low+high)/2/100; bfGoal = goal/100
   leanNow = W(1−bfNow); fatNow = W − leanNow
   gain = sex==='male' ? muscle_gain_lb : 0
   leanGoal = leanNow + gain; goalW = leanGoal/(1−bfGoal)
   fatLoss = max(0, fatNow − (goalW − leanGoal))
   weeks = max(fatLoss/1.25, gain/0.5); show round(0.85·weeks)–round(1.2·weeks), min 4
   protein = round(leanGoal × protein_g_per_lb) g/day
   ```
   Tiles: **Body fat** `22–26% → 10%` · **Lean muscle** `≈142 lb → ≈148 lb (+6 lb)` (women: `Definition: moderate →
   sharp`) · **Fat to lose** `≈27 lb` · **Goal weight** `≈165 lb`. Under them the disclaimer line + `/sources` link
   (copy it from `bodyfatNote`, line ~1801). The `headline` from the model sits above the tiles.
6. **Fallback when the analysis call fails or is slow**: tiles render instantly from the lookup tables (`BF_BEFORE`
   midpoint, `BF_AFTER`/female clamps, intensity anchor for gain), marked "estimate"; when the model result arrives
   (skeleton shimmer on the body map meanwhile, video masks the wait) the tiles update in place. If it never arrives,
   hide the body map and show "Send a clearer, well-lit photo for a body-part read" — never a blank page.
7. **Body map** — "Where your plan will focus": inline SVG front silhouette (simple paths, ~1 KB) with a `<path
   data-region>` per shoulders / chest / arms / upper_abs / lower_abs / obliques / legs; `back` is a chip under the map.
   Fill: strong = `var(--acc)` at 35 %, focus = `#e07b2f`, maintain = `var(--faint)`, not_visible = faint hatch.
   Legend + one row per region with the model's note. Wording: "Already strong", "Focus here", "Maintain", "Not
   visible in this photo — add a full-body shot and we read it too".
8. **"What this means for your plan"**: `training_focus`, nutrition direction in words ("a moderate cut — food you
   like, just less of it"), protein/day, the timeline range with the tease "…narrows to a date once you tell us your
   training history".
9. **"Tell us a little more and it gets sharper"** — five rows, each `what you'd tell us → what it unlocks`:
   training history → the exact starting stage and how fast we progress you; injuries → which focus area we load first
   and what we work around; equipment → a plan for your gym, your dumbbells, or no equipment; lifestyle & time → how
   many days and how long each session; foods you like / allergies → a meal plan you'll actually follow. Closing line in
   Dan's voice: the pictures did most of the work; these five answers take two minutes.
10. **CTA block**: `Start your 7-day free trial →` → `showTrialGate(null)` (works on web and native — native lands on
    the IAP-aware membership screen). Price line "then $19.99/mo · cancel with two taps" gets `app-hide-purchase`; the
    native variant mirrors `hubPreviewAppNote` (trial line only). Secondary: inline email form "Email me my picture +
    my analysis" → same `/api/subscribe` payload as the old screen + `source:'analysis'`, `localStorage.absbyai_email`,
    PostHog `email_subscribed {source:'analysis'}`; hidden when `absbyai_email` is already set. Tertiary text link:
    "Continue to my hub" → `showHub()`. Footer links (Terms · Privacy · Refunds · Contact · Sources) as on the old
    email screen.
11. **Wiring**: `loveItBtn` → `showAnalysisScreen()`; delete `emailSection` + `bridgeSection` markup, their handlers
    (`emailBackBtn`, `emailForm`, `emailSkipBtn`, `bridgeBackBtn`, `bridgeContinueBtn`), `showEmailScreen()`,
    `showBridgeScreen()`, the `.bridge-*` CSS; remove both ids from the `renderScreen()` array. `productBackBtn`'s
    fallback (`showScreen('email')`, line ~5065) → `showScreen('analysis')`; `showHubPrintUpsell` / the print flow's
    `upsell.returnScreen` logic stays. Grep for every remaining `'email'` / `'bridge'` screen name before you finish.
12. **Hub tile** `data-feature="analysis"` ("My body analysis — what your pictures say") after Macro Tracker;
    `openHubFeature('analysis')` → `showAnalysisScreen({from:'hub'})`: loads the analysis from the server (logged in) or
    `localStorage.absbyai_body_analysis`, hides the email block if captured, and for members swaps the CTA to `Build my
    program →` (`openTrainer()`).
13. **Persistence on the client**: `localStorage.absbyai_body_analysis = { afterHash, analysis, at }` (hash = a cheap
    djb2 of the after data-URL; never store base64 twice). When the login/hub sync posts the pair to
    `/api/account/transformation`, include the cached analysis so it lands on the row.
14. **Trainer + nutritionist reuse** (small, do it): when `settings.analysis` exists on the hero row, append one labelled
    line to the trainer and nutritionist prompts through the same additive path as `profileContextBlock` ("Photo
    analysis at lock-in: body fat ~24%, goal 10%, focus: chest, shoulders; strong: arms; coverage: torso"). This is
    what makes "the pictures do the work" true inside the paid features.
15. **Analytics**: `analysis_page_seen {from, has_video}`, `analysis_loaded {ms, cached, confidence, coverage,
    fallback}`, `analysis_video_play`, `analysis_video_progress`, `analysis_slider_changed`, `analysis_cta_clicked
    {target: trial|email|hub|trainer}`. Retire `bridge_seen` / `bridge_continue` (note it in the commit message so
    PostHog funnels get updated).

### 3. Copy (Dan's voice, second person, direct)

Section heads, in order: "You visualized your goal." → "Two quick sliders make the numbers yours" → "What our AI already
knows from your pictures" → "Where your plan will focus" → "What this means for your plan" → "Tell us a little more and
it gets sharper" → CTA. Lift phrases from the video transcript (`/Volumes/Extreme/_edit_work/website-video-828/
qc.whisper.json`): "make that AI-generated image a reality", "just from these pictures, it already knows a lot",
"you can make the program even better by telling our AI about…", "try out the macro tracker, the AI workout program,
the AI nutrition plan, everything in the app", "cancel with two taps and you won't be charged a dime". Women: swap
"muscle you'll need to gain" for "definition you'll build".

### 4. Verify, deploy, close

1. Local: `.claude/launch.json` dev server (`DATABASE_URL=pgmem://local`); the local preview's Anthropic key is invalid
   (memory `load-time-optimizations`) — export `ANTHROPIC_API_KEY` from `~/.absbyai-secrets.env` for the local run so
   the endpoint can be exercised, or test it on prod. Phone viewport 390 px, screenshots of every section, sliders
   dragged, women path (`state.gender='female'`), clothed path, model-failure path (kill the key → table fallback).
2. Prod: one real generation on absbyai.com with the test account (`danroseconsulting+absbyai-test@gmail.com` /
   `livetest123`; costs one generation + one analysis), lock in, confirm the page, the PostHog events, the row's
   `settings.analysis` in Postgres (`DATABASE_URL` in the secrets cache), the hub tile, and the trial CTA reaching the
   membership screen. Then `?vp=1` for the video placeholder.
3. Commit, push `main`, confirm `railway deployment list --service abs-by-ai --json` shows SUCCESS, live-verify.
4. **Native retest trigger — say it to Dan explicitly**: iOS and Android load this page; the lock-in flow, the sliders
   and the trial CTA need a run in the simulator / on his phone (`/iphone-mirroring` or adb).
5. Coordination: delete the HANDOFFS bullet for this doc in `AI_COORDINATION.md`, move it out of the OPEN table in
   `Handoffs/README.md`. Dashboard: check the board (`/dashboard-tasks`) for a row before checking anything off — none
   was added when this was written.

## OPEN (defaults stated — ship the default, ask in the delivery message)

- **Women's default height**: Dan said 5'9"; the default here is 5'4" for women because the app already knows sex and a
  5'9" default reads wrong to most women. Flip to 69 for everyone if he says so.
- **Video visibility before the URL lands**: hidden for real users, `?vp=1` to review (default). Dan may prefer the
  placeholder visible to everyone.
- **Video hosting when rev 4 is approved**: YouTube unlisted (zero setup, Dan uploads — Claude cannot upload files >
  10 MB) vs. an mp4 on Cloudflare R2 / Bunny (clean player, watch-time events, autoplay-muted with the burned captions).
  The slot takes either; recommend YouTube unlisted for launch.

## Things to Avoid / Lessons Learned

- **Fire the analysis on lock-in, never on reveal** — "More dramatic / More subtle" regenerations would multiply the
  calls; the after image changes each time.
- **No `deviceId` on the analysis call, no credit decrement** — it is free by design and must never hit the
  generate-and-lock billing path (`AGENTS.md` spend rule).
- **pg-mem has no jsonb `||`** — merge `settings.analysis` in JS (`writeProfileMerge` is the pattern).
- **`sanitizeProfilePatch` drops unknown keys silently** — do not stash the analysis in the profile; it lives on the
  transformation row. Only `heightIn` / `weight` / `weightUnit` go through the profile.
- **`insertTransformation` returns null on a duplicate after image** — attach the analysis with an UPDATE on the
  matching row, not by re-inserting.
- **`fetchWithRetry` retries only network errors** — keep it that way for the analysis call; retrying model 5xx blindly
  costs money.
- **Never put base64 images in URLs, logs or PostHog properties.** The repo is public (memory `repo-is-public`) — no
  personal photos in fixtures or screenshots committed to git.
- **Apple 1.4.1**: every body-fat / lean-mass figure carries the visual-estimate qualifier and the `/sources` link.
  Never the words "diagnose", "medical", "clinical".
- **Native apps**: never `app-hide-purchase` the trial button itself (the membership screen handles IAP); only the web
  price copy. `IS_NATIVE_APP` is at line ~2844.
- **Wispr Flow**: "logs in their image" in the brief meant "locks in". Do not build a login wall here.
- **Tone**: "already strong / focus here" — the word "weak" never appears on screen.

## Relevant Files & Locations

- `public/index.html` — screens, `renderScreen()` ~4059, `showScreen()` ~4089, BF tables ~3718, `updateBodyFatDisplay`
  ~4613, `loveItBtn` handler ~5007, email/bridge handlers ~5033–5060, `productBackBtn` ~5063, `authApi` ~5255,
  `seedProfileFromFunnel` ~5548, `QUIZ_STEPS` ~5560, `startQuiz` ~5606, `showTrialGate` ~5744, `showHub` ~5760,
  `openHubFeature` ~5511, hub tiles markup ~2207, `fetchWithRetry` ~10339, muscle anchor table ~3826.
- `server.js` — meal analyzer call pattern ~2700, `/api/generate-image` ~3328, `/api/subscribe` ~4300,
  `PROFILE_ENUMS` + `sanitizeProfilePatch` ~5185, `/api/account/transformation` ~5370, `insertTransformation` ~5400,
  `PROGRAM_ASSESSMENT` ~6660, `/api/generate-program` ~7228, nutritionist ~7778, `aiLimiter` line 85.
- `db.js` — `transformations` table line 113 (`settings JSONB`).
- Video: `claude edited long form content/06 - Website Conversion Video (post-generation)/` (rev 3 delivered, rev 4
  pending under `Handoffs/handoff-20260908-website-video-rev4.md`); transcript
  `/Volumes/Extreme/_edit_work/website-video-828/qc.whisper.json`.
- Secrets: `~/.absbyai-secrets.env` (`ANTHROPIC_API_KEY`, `DATABASE_URL`); never paste values anywhere.
- Skills to load in the execution session: `/claude-api` (before writing the endpoint), `/dashboard-tasks` (close-out).
- Memory to respect: `member-profile`, `accounts-member-hub`, `cross-platform-retest-rule`, `native-app-iap-gating`,
  `repo-is-public`, `load-time-optimizations`, `astra-vs-fable-verdict`.

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Fable 5.1, high effort** — Dan's standing choice for Abs By AI (memory `astra-vs-fable-verdict`); included in Max, so the cost is allowance, not dollars. |
| **If Claude usage is high / approaching a limit** | **Claude Sonnet 5, standard thinking** — build the page and endpoint; escalate only the `/api/body-analysis` prompt + schema to Opus 5 if the first real photos come back with unstable numbers. |

Always-Claude override applies regardless of usage: this touches the Anthropic API integration in `server.js` and the
on-screen copy is Dan's brand voice, so Codex is not recommended for it.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260908-post-lockin-analysis-page.md` in the Abs By AI repo. Build the new `analysis`
> screen that replaces the email-capture and benefits-bridge screens right after "Lock in this goal": a video slot at
> the top (hidden until a URL is set, `?vp=1` shows the placeholder), height and weight sliders under it (5'9" default
> and the BMI-matched weight for the tapped body type, weight tracks height until touched), the before/after pair, the
> four numbers the website video promises (body fat now → goal, lean muscle now → goal, fat to lose, goal weight)
> computed live from the sliders, a body map of "already strong / focus here / not visible" regions from a new
> `POST /api/body-analysis` Claude vision call (load `/claude-api` first; `claude-opus-5`, structured JSON, cached by
> image hash, free to the user, table fallback if it fails), the "tell us a little more" tease, and the 7-day trial CTA
> with the email ask folded in underneath. Start by reading the handoff's Current State and Key Decisions, then §1 the
> endpoint, then §2 the screen. Verify locally and with one real generation on production, commit, push, confirm the
> Railway deploy, live-verify on absbyai.com, tell Dan it needs a native retest, and close the coordination entry.
> Do NOT execute the website-video rev-4 handoff — it is context only.

**Recommended:** Fable 5.1, high effort. **Budget:** a few dollars of Opus 5 vision calls during testing, one production
generation (≈ $0.15). Everything else exists.
