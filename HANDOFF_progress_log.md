# HANDOFF — Weight & Progress Log

**Status:** NOT STARTED — plan approved by Dan July 10, 2026. Build exactly as specified below.
**Date:** July 10, 2026

## Product concept

A daily weight log + weekly progress-photo ritual that becomes the user's visual and numeric record of their transformation. The headline number is never the raw scale weight — it's a smoothed **7-day trend weight**, which prevents the #1 logging killer ("I was good all week and the scale went UP"). Weekly photo day adds a waist measurement and (for members) an AI recap that ties together weight trend, waist, sleep, and workout adherence.

### Locked scope (decided by Dan)

**IN:**
- **Daily weight** — one number per day, upsert (re-weighing replaces that day's entry). lbs or kg.
- **Trend weight** — 7-day rolling average shown as the headline number and chart line; raw daily weights as faint dots behind it.
- **Weekly progress photo** — user picks a "photo day" (day of week) at setup; front pose minimum, optional side/back. Push reminder on photo day.
- **Weekly waist measurement** — logged on photo day alongside the photo. Tape around the navel.
- **Contextual flags** — optional one-tap chips on the daily weight log: `high-sodium`, `poor-sleep`, `period`, `traveling`. Fed to the AI recap so scale spikes get explained, never required.

**OUT (explicitly cut — do not build):**
- Optional extra measurements (hips/chest/arms/thighs) and body-fat % — too complicated for v1.
- Daily photos, calorie logging (Nutritionist owns food), daily measurements.

**Photo storage:** keep photos in Postgres as base64 TEXT, same as the `transformations` table. S3/Cloudflare R2 migration is a later project — do NOT build object storage now.

### Design rules (locked)

- **Trend weight is the headline everywhere.** Raw daily weight is secondary/faint. Rate-of-change readout: "Trending −1.1 lbs/week over the last 30 days."
- **Soft streaks only:** show "logged 12 of the last 14 days" — never a hard streak that resets to zero on a missed day.
- **Reminder etiquette:** optional daily weigh-in nudge (morning, user's local time); photo-day push reminder; if photo day is missed, ONE gentle follow-up the next day, then stop. No nagging.
- **Logging must take <30 seconds:** one screen — number pad for weight, flag chips, save. On photo day the same screen also asks for photo + waist inline.

## Gating

- **Free (account required):** logging, trend chart, photo timeline, side-by-side compare. This is the retention/data moat.
- **Membership:** AI weekly recap (photo-day analysis of the week's data). Same `needsMembership` 402 → checkout pattern as Trainer/Nutritionist/Sleep.
- Not logged in: feature screen shows pitch + signup prompt (data must live on the account, so no anonymous logging).

## Execution plan

Follow the established pattern: tables in `db.js`, endpoints in `server.js`, screen in `index.html`, gating like Trainer/Sleep.

### Step 1 — Database (db.js)

```sql
CREATE TABLE IF NOT EXISTS weight_logs (
  id         SERIAL PRIMARY KEY,
  user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  entry_date DATE NOT NULL,
  weight     NUMERIC(6,2) NOT NULL,   -- stored in the unit the user logs
  unit       TEXT NOT NULL DEFAULT 'lb',  -- 'lb' | 'kg'
  flags      JSONB NOT NULL DEFAULT '[]', -- e.g. ["high-sodium","poor-sleep"]
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (user_id, entry_date)
);
CREATE INDEX IF NOT EXISTS weight_logs_user_idx ON weight_logs (user_id, entry_date);

CREATE TABLE IF NOT EXISTS progress_entries (
  id          SERIAL PRIMARY KEY,
  user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  entry_date  DATE NOT NULL,           -- the photo day this entry belongs to
  photo_front TEXT NOT NULL,           -- base64 data URL, downscaled client-side
  photo_side  TEXT,                    -- optional
  photo_back  TEXT,                    -- optional
  waist       NUMERIC(5,2),            -- inches or cm per waist_unit
  waist_unit  TEXT DEFAULT 'in',
  recap       JSONB,                   -- AI weekly recap (members)
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (user_id, entry_date)
);
CREATE INDEX IF NOT EXISTS progress_entries_user_idx ON progress_entries (user_id, entry_date);
```

User settings — add columns to `users` via the existing ADD COLUMN IF NOT EXISTS loop:
- `photo_day INTEGER` — 0–6 (Sunday=0); null until the user picks one during progress setup.
- `weigh_reminder BOOLEAN DEFAULT false` — daily morning weigh-in nudge opt-in.

Upsert both tables with `ON CONFLICT (user_id, entry_date) DO UPDATE` (same pattern as `sleep_entries`).

### Step 2 — Trend math (server.js helper, not AI)

`computeTrend(rows)` — pure JS, no API call:
- Trend weight for a date = mean of the raw weights in the trailing 7-day window (use whatever entries exist in the window; require ≥1). Simple rolling mean — do not overthink with exponential smoothing in v1.
- Rate of change = linear-regression slope of trend weight over the last 30 days, expressed as lbs (or kg)/week. Need ≥7 logged days in the window, otherwise return null and the UI says "keep logging to unlock your trend."
- Consistency stat: count of logged days in the last 14.
- Mixed units: convert everything to the user's current unit at read time (1 kg = 2.20462 lb).

### Step 3 — Endpoints (server.js)

- `POST /api/progress/weight` — `requireAuth`. Body `{ date?, weight, unit, flags }` (date defaults to today, user-local date string from client). Upsert. Returns the updated summary (below) so the UI refreshes in one round-trip.
- `GET /api/progress/summary?range=30|90|all` — `requireAuth`. Returns `{ entries: [{date, weight, trend, flags}], rate, unit, consistency: {logged, window}, photoDay, isPhotoDayToday, latestPhotoEntry, photoTimeline: [{id, date, waist, hasRecap}] }`. Photo timeline returns metadata only — NOT the base64 photos (they'd blow up the payload).
- `GET /api/progress/photo/:id` — `requireAuth`, ownership check. Returns one entry's photos + waist + recap. Fetched lazily when the user taps a timeline thumbnail. (Also return a tiny thumbnail field in the timeline if strip previews are wanted — generate client-side at upload: save both a ~200px `thumb_front` column and the full image. Add `thumb_front TEXT` to the table.)
- `POST /api/progress/photo` — `requireAuth`. Body `{ date?, photoFront, photoSide?, photoBack?, thumbFront, waist, waistUnit }`. Photos downscaled client-side before upload (reuse the existing photo-downscale helper, same as meal analyzer / sleep screenshots — cap ~1280px, JPEG). Upsert on (user, date).
- `POST /api/progress/settings` — `requireAuth`. Body `{ photoDay, weighReminder }`.
- `POST /api/progress/recap` — `aiLimiter, requireAuth`, **membership-gated** (non-members get 402 `needsMembership`). Generates the AI weekly recap for the latest photo entry and saves it into `progress_entries.recap`. Idempotent: if a recap already exists for that entry, return it unless `force: true`.

### Step 4 — AI weekly recap (server.js)

`PROGRESS_RECAP_SYSTEM_PROMPT`:
- Persona: same evidence-grounded, go-hard coach voice as Trainer/Sleep.
- Input assembled server-side: last 30 days of weight rows + trend + rate, this week's waist vs. prior weeks' waists, this week's flags, plus cross-feature context — program adherence (from `programs.progress`), last 7 nights from `sleep_entries` (reuse/extend `getTodaysSleep`-style helper).
- Rules: interpret the TREND, never the daily number. If flags explain a spike (sodium/period/travel/poor sleep), say so explicitly and defuse it. If weight stalls but waist drops → call out recomposition as a win. If both stall 2+ weeks → concrete adjustment (reference their program/meal plan), still encouraging. Never recommend under-eating or punishing cardio.
- Output: strict JSON `{ headline, weekStory, scaleVsWaist, adjustments: [..], photoNote, encouragement }`. Parse using the Counsel pattern (skip thinking block, read text block, generous max_tokens). No vision call in v1 — `photoNote` is generic pose/lighting-consistency coaching, not image analysis. (Photo vision analysis = Phase 2.)
- Text-only call, so it's cheap; still behind `aiLimiter`.

### Step 5 — Reminders (server.js, reuse existing push infra `/api/push/*`)

- Store timezone offset or IANA zone with the push subscription if not already there (check `push_subscriptions` handling — if there's no per-user schedule concept yet, simplest v1: a daily cron-style `setInterval` sweep every 15 min that finds users whose local time just crossed 8:00 AM and sends: weigh-in nudge if `weigh_reminder` and no `weight_logs` row today; photo reminder if today is `photo_day` and no `progress_entries` row today).
- Missed photo day: next-day sweep sends ONE follow-up ("Yesterday was photo day — 2 minutes, same spot, same lighting"), only if still no entry. Track with a `last_photo_nudge DATE` column on users so it never repeats.
- Copy: "📸 It's photo day — same spot, same lighting, same pose."

### Step 6 — Frontend (index.html)

New `#progressSection` screen following `#sleepSection`/`#trainerSection` structure exactly, plus home-screen tile + nav entry.

1. **First-run setup (no photo_day yet):** short pitch → pick photo day (day-of-week chips, suggest "the day you're most consistently home in the morning") → toggle daily weigh-in reminder → optional: log first weight + take Day-1 photo + waist right now ("your before starts today").
2. **Log screen (default view):** big weight input (numeric keypad, prefilled with last weight), unit toggle lb/kg, flag chips, Save. If today is photo day (or the missed-day follow-up window): inline photo capture card — front (required), side/back (optional, collapsed), waist input. Client-side downscale before upload + generate ~200px thumbnail.
3. **Chart:** trend line (bold, brand color) over raw dots (faint), range tabs 30/90/all, rate-of-change readout, consistency line ("logged 12 of the last 14 days"). Plain canvas/SVG — no chart library; the sleep trend strip is the precedent.
4. **Photo timeline:** horizontal strip of weekly thumbnails with dates + waist. Tap → full view (lazy fetch `/api/progress/photo/:id`). "Compare" mode: tap two → side-by-side with dates, weights (trend), and waists overlaid.
5. **AI recap panel:** on/after photo day, members see the recap card (headline, week story, scale-vs-waist, adjustments, photo note). Non-members see the locked-card upsell (same as trainer preview) → membership checkout.
6. **My Transformations tie-in:** in compare mode, a "Save as Transformation" button POSTs the two selected photos to the existing `/api/transformations` endpoint — first-vs-latest pair flows straight into the gallery (and its existing print upsell). No new backend needed.

### Step 7 — Cross-feature context injection (server.js, small and surgical)

Same pattern as the sleep-context injection: helper `getWeightContext(userId)` → `{ trend, rate, latestWaist, waistDelta }` or null. Append a line to the Trainer (`buildTrainerUserContent` / program check-in) and Nutritionist (mealplan generate/check-in) prompts: e.g. "User's 7-day trend weight is 182.4 lb, moving −1.1 lb/week; waist down 0.5 in over 3 weeks — plan is working, do not cut calories further." Prompt-context only; no schema changes to programs/meal_plans.

### Step 8 — Ship

- Commit + push to main (Railway auto-deploys). No new env vars — uses existing `ANTHROPIC_API_KEY`, `DATABASE_URL`, push VAPID keys.
- Test on prod (local preview has an invalid Anthropic key, so recap must be tested live):
  1. Setup flow: pick photo day, log first weight + photo + waist.
  2. Log weight on several days (backfill via date param) → trend line, rate, consistency render correctly; upsert works (re-log today).
  3. kg/lb toggle with mixed-unit history.
  4. Photo day: inline photo card appears; upload front-only; upload front+side; timeline + lazy full view + compare mode.
  5. Non-member: recap card locked with upsell; member: recap generates, saves, idempotent on refresh.
  6. Push: weigh-in nudge, photo-day reminder, single missed-day follow-up (and that it doesn't repeat).
  7. Trainer/Nutritionist prompts pick up the weight context line.
  8. "Save as Transformation" lands the pair in the My Transformations gallery.

## Phase 2 (do NOT build now)

- Photo vision analysis in the recap (Claude vision on this week vs. 4-weeks-ago photo).
- Optional extra measurements (hips/chest/arms/thighs), body-fat %.
- Move photos to S3/Cloudflare R2 (weekly photos accumulate ~50–150 KB × 52/user/year in Postgres — fine for now, migrate before scale).
- Milestone celebrations (every −5 lb trend, every −1 in waist) + share cards.
- Apple Health weight auto-sync via the Capacitor iOS app.

## Open items / risks

- **Payload size:** never return base64 photos in list endpoints — timeline is metadata + thumbnails only; full photos always lazy-loaded per entry. This is the main perf trap.
- **Timezone correctness for "today":** the client sends its local date string for logs; reminders need per-user local-time logic (Step 5). Don't use server UTC date for upsert keys.
- **Trend with sparse data:** users who log 2×/week still get a trend (window mean handles gaps) but rate-of-change stays null under 7 points — make the "keep logging" empty state encouraging, not scolding.
- **pg-mem:** verify NUMERIC and DATE upserts behave under pgmem:// for local preview; if pg-mem chokes on NUMERIC, store weight as REAL.
