# HANDOFF — AI Sleep Coach (MVP)

**Status:** MVP SHIPPED to prod July 10, 2026 (commit 06fab14) — Steps 1–6 below are done and verified live. Phase 2/3 remain.
**Date:** July 10, 2026

## Product concept

Sleep trackers (Oura etc.) tell users to "take it easy" after a bad night. The Abs By AI Sleep Coach does the opposite: **whatever the sleep data says, the verdict is always GO HARD — the sleep just changes the justification and the tactics.** Sleep data tells us *how* to attack the day, never *whether* to.

### The Go Hard Anyway briefing — core rules (locked by Dan)

Every daily briefing has the same structure: **acknowledge the sleep → justify going extra hard → tactical adjustments → tonight's fix.**

- **Always tell the user to go extra hard in the gym.** No rest-day or "take it easy" verdicts, ever.
- **Bad night of sleep:** justification for going hard anyway (one bad night doesn't reduce strength; training today is the fastest fix for tonight's sleep). Tactical warnings: **watch your eating today** (poor sleep spikes cravings) and **stay tight** (form focus since reaction time is slightly down).
- **Great night of sleep:** "This is the day to really push a **higher deficit**" — fully recovered, so push harder in the gym AND eat leaner today.
- Trend awareness: a multi-day downtrend gets honest escalation on the *sleep fixes* ("your 2-week average will stall fat loss — here's the protocol"), but the gym verdict is still go hard.
- Safety valve (kept minimal): possible sleep-disorder red flags (snoring + gasping + chronically unrefreshing sleep) get a one-line "worth mentioning to a doctor" note, same disclaimer pattern as Decision Counsel. Not-medical-advice footer under every briefing.

### Cross-feature integration rules (locked by Dan)

- **AI Trainer:** bad night → **extend the warm-up, but the workout does NOT get shorter or lighter.**
- **AI Nutritionist:** bad night → **more protein, zero extra carbs.** Calories go up, but only from protein — this blunts the cravings. Great night → suggest running a higher deficit that day.

## Data input tiers

1. **Manual morning check-in (MVP, everyone):** bedtime, wake time, number of wake-ups, feel score 1–5. ~30 seconds.
2. **Tracker screenshot upload (MVP, the hook):** user uploads a screenshot of their Oura/Whoop/Apple Health/Fitbit sleep screen; Claude vision extracts duration, score, stages, HRV, resting HR. Works with every tracker, zero API integrations. Landing copy leads with this: "Upload your tracker screenshot — we'll out-coach your ring."
3. **Real integrations (Phase 3, NOT in MVP):** Apple HealthKit via the Capacitor iOS app first (aggregates all trackers), direct Oura/Whoop OAuth later.

## MVP execution plan

Follow the established pattern: endpoints in `server.js`, table in `db.js`, screen in `index.html`, membership-gated like Trainer/Nutritionist (free preview → `needsMembership` 402 → membership checkout).

### Step 1 — Database (db.js)

```sql
CREATE TABLE IF NOT EXISTS sleep_entries (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  entry_date DATE NOT NULL,
  source TEXT NOT NULL,            -- 'manual' | 'screenshot'
  data JSONB NOT NULL,             -- normalized: durationMin, bedtime, waketime, wakeups, feelScore, trackerScore, hrv, rhr, stages
  briefing JSONB,                  -- the generated Go Hard briefing
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (user_id, entry_date)
);
```

One row per user per day; re-submitting the same day upserts (lets them redo a check-in).

### Step 2 — System prompt (server.js)

`SLEEP_COACH_SYSTEM_PROMPT` encoding:
- Persona: high-energy but evidence-grounded coach. Cites the actual research framing (single-night sleep loss impairs perceived effort/mood far more than strength or power output; morning training + light are the strongest levers for the next night's sleep).
- The hard rules above (always go hard; bad-night = watch eating + stay tight; great-night = push higher deficit; trend escalation on sleep fixes only; disorder red-flag one-liner).
- Output: strict JSON — `{ verdict, headline, justification, tactics: [..], tonight: [..], trendNote?, redFlag?, parsed: {normalized sleep numbers} }`. Follow the Counsel pattern for parsing (skip thinking block, read the text block, generous max_tokens).

### Step 3 — Endpoints (server.js)

- `POST /api/sleep/checkin` — `aiLimiter, optionalAuth`. Body: either manual form fields or `{ screenshotBase64, screenshotMime }`. For screenshots, one vision call extracts the numbers AND generates the briefing in a single request (cheaper than two calls; downscale image first like the meal analyzer). Pull the user's last 14 `sleep_entries` for trend context. Save entry + briefing if logged in. Non-members get the verdict + headline but tactics/tonight/trend locked (`stripForPreview`, same as programs) → upsell to membership.
- `GET /api/sleep/history` — `requireAuth`. Last 30 entries for the trend view + so the briefing screen can restore today's entry.

### Step 4 — Cross-feature wiring (server.js, small and surgical)

Helper `getTodaysSleep(userId)` → today's normalized entry or null. Then:
- In `/api/program/checkin` and wherever the trainer prompt is assembled (`buildTrainerUserContent` context for members): append a sleep line — "User slept poorly last night: extend warm-up ~5 min; do NOT shorten or lighten the workout."
- In `/api/generate-mealplan` + `/api/mealplan/checkin`: append — bad night: "raise today's calories via protein ONLY, zero added carbs (craving control)"; great night: "suggest a slightly higher deficit today."
- MVP scope: prompt-context injection only. No schema changes to programs/meal_plans.

### Step 5 — Frontend (index.html)

New `#sleepSection` screen following `#trainerSection`/`#nutritionSection` exactly:
- Landing: hero pitch ("Your ring says take it easy. We say go hard — here's why."), two entry buttons: **Upload tracker screenshot** / **30-second check-in**.
- Check-in form: bedtime, wake time, wake-ups, feel 1–5.
- Screenshot path: file input → downscale client-side (reuse the photo-downscale helper from load-time work) → POST.
- Briefing card: big GO HARD verdict, justification, tactics checklist, "Tonight" list, disclaimer footer. Locked sections show the membership upsell like the trainer preview.
- Simple 14-day trend strip (duration bars + feel dots) from `/api/sleep/history` for members.
- Home-screen tile + nav entry alongside Trainer/Nutritionist/Counsel.

### Step 6 — Ship

- Commit + push to main (Railway auto-deploys; no new env vars needed — uses existing `ANTHROPIC_API_KEY`).
- Test on prod (local preview has an invalid Anthropic key): manual check-in good night, manual bad night, Oura screenshot, non-member lock, member full briefing, trainer/mealplan checkin picking up sleep context.

## Phase 2 (after MVP)
- Sleep protocol builder: intake wizard (caffeine timing, screens, alcohol, temp, consistency, stress) → personalized 2-week protocol, top 3–4 highest-leverage fixes only.
- Weekly summary + richer trend view.
- Evening wind-down push nudge ("in bed by 10:40 hits your 7.5h target") — web push infra already exists (`/api/push/*`).

## Phase 3
- Apple HealthKit read in ios-app (auto-sync, replaces screenshots for iOS users).
- Direct Oura/Whoop APIs if demand shows.

## Open items / risks
- Screenshot parsing accuracy varies by tracker UI — briefing should show the parsed numbers so users can correct them (add an "edit numbers" affordance if misreads are common).
- Craving-control protein bump: prompt guidance only in MVP; if mealplan macros need hard enforcement, add a post-generation macro check later.
