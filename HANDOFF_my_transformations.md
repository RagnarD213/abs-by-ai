# HANDOFF — My Transformations (gallery + hero swap + share + print upsell)

Build the "My Transformations" feature for absbyai.com: a before/after gallery of every
transformation a member has generated, with (1) interactive drag sliders on each card,
(2) share/download of a branded composite image, (3) set-as-hero with a "rebuild my
program for this goal" cross-sell, and (4) a per-card print upsell reusing the existing
Printify flow.

Scope agreed with Dan: items 1, 2, 4, 5 from the brainstorm — slider cards, share/download,
goal-context program regen on hero swap, print upsell per card. NOT in scope: real-progress
photo check-ins, compare mode, object storage migration.

---

## Current state of the code (verified July 2026)

Everything lives in two files: `server.js` (Express backend, ~3970 lines) and `index.html`
(entire SPA frontend, ~5830 lines). `db.js` holds the Postgres schema (`initDb()`).

### How transformations work today
- Only ONE pair is stored, on the `users` row: `before_image`, `after_image` (base64 data
  URLs) — `db.js:41-42`.
- `GET/POST /api/account/transformation` (`server.js:1964-1988`) reads/overwrites that pair.
- Frontend keeps the latest pair in localStorage under `absbyai_last_before` /
  `absbyai_last_after` (`LAST_BEFORE_KEY` / `LAST_AFTER_KEY`, `index.html:2929-2930`).
- After every successful generation, `storeTransformationLocally()` +
  `saveTransformationIfLoggedIn()` run (`index.html:3085-3102`), called from `generate()`
  (`index.html:5262-5263`) and `adjustIntensity()` (`index.html:5313-5314`).
- The member-hub hero (`#hubHero`, `index.html:1558-1568`) shows the pair side-by-side
  ("Today" / "Your Goal"), rendered by `renderHubHero()` (`index.html:3062-3082`):
  localStorage first, falls back to `GET /api/account/transformation`.
- The hub tile for the gallery already exists as a "Coming soon" placeholder:
  `data-feature="transformations"` at `index.html:1596-1600`. Hub tile clicks are handled
  around `index.html:3172` (tiles with `data-soon` show `#hubSoonNote`).

### Generation state available at save time (for settings metadata)
In `generate()`/`adjustIntensity()`: `state.effectiveIntensity`, `state.condition`,
`state.photoMime`. Save these into the new row's `settings` JSONB.

### Screen navigation
`showScreen(name)` (`index.html:2262`) toggles a hardcoded list of `*Section` div ids.
A new screen means: add `<div id="transformationsSection" class="screen" style="display:none">`
and add `'transformationsSection'` to the array at `index.html:2263`.

### Auth helpers
`authApi(path, opts)` — fetch with session token; `isLoggedIn()`; `requireAuth` middleware
server-side. Gallery is account-only.

### Trainer program (for the goal-context cross-sell)
- Programs stored in `programs` table (`db.js:61-70`), one row per 4-week block.
- `POST /api/generate-program` (`server.js:2494`, `optionalAuth`) takes
  `{ intake, photos: { beforeBase64, beforeMime, afterBase64, afterMime }, photoConsent }`
  and builds the program around the gap between before and after photos
  (`buildTrainerUserContent`, `server.js:2346`).
- Frontend calls it at `index.html:3512` (intake flow) and `index.html:3588` (regenerate
  from saved intake after login). The saved intake for regen lives in the program row's
  `intake` JSONB — the pattern at `index.html:3583-3604` is the one to copy for the
  "rebuild for this goal" flow.
- Membership check: `isActiveMembership(req.user)` (`server.js:2054`). Full program is
  members-only; free users get a preview (`stripProgramForPreview`).

### Print upsell (Printify) — already built for the post-generation flow
- Client flow: `showProductSection()` → `selectProduct(type)` → `handleCheckout()`
  (`index.html:2564-2725`). It reads the after image from `state.lastAfterDataUrl`,
  uploads via `POST /api/printify/upload-image` (`server.js:4038`), then
  `POST /api/stripe/create-checkout` (`server.js:4067`) with product metadata; the Stripe
  webhook creates the Printify order.
- `UPSELL_PRICES` config exists client-side; product/size UI screens already exist
  (`productSection`, `customizeSection`).
- KEY INSIGHT: the only coupling to the generation flow is `state.lastAfterDataUrl`
  (read at `index.html:2565`, `2580`, `2655`) and the back-button targets
  (`productBackBtn` → `'email'` at `index.html:2861`, `customizeBackBtn` → `'product'`).
  To reuse from the gallery, refactor to a parameter or set `state.lastAfterDataUrl`
  before entering, and make the back buttons return to the caller (track an
  `upsell.returnScreen`).

### Image size / storage notes
- Before photos are already downscaled client-side before upload (see load-time
  optimization work). After images are Gemini PNG output, ~1-2 MB base64.
- Base64-in-Postgres is acceptable at current scale, but cap gallery size: keep the
  most recent 30 transformations per user (delete oldest on insert past cap).
- List endpoint must NOT return all full images at once — paginate or return
  the newest N with LIMIT, and consider `created_at DESC`.

### PostHog
`posthog.capture(...)` is used throughout (e.g. `index.html:3031`, `2647`). Add events
for the new feature (names below).

### Deploy
Railway auto-deploys from GitHub `main`. Commit and push without asking (memory:
auto-commit-push; pull --rebase first). `initDb()` uses CREATE TABLE IF NOT EXISTS —
new tables just work on deploy. pg-mem local dev: keep DDL simple (it chokes on some
syntax; follow the existing ADD COLUMN IF NOT EXISTS fallback pattern in db.js).

---

## Build plan

### Phase 1 — Schema + endpoints

**db.js** — add to `initDb()`:

```sql
CREATE TABLE IF NOT EXISTS transformations (
  id           SERIAL PRIMARY KEY,
  user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  before_image TEXT NOT NULL,
  after_image  TEXT NOT NULL,
  settings     JSONB NOT NULL DEFAULT '{}',
  is_hero      BOOLEAN NOT NULL DEFAULT false,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS transformations_user_idx ON transformations (user_id, id DESC);
```

**server.js** — new endpoints (all `requireAuth`):

1. `GET /api/transformations?before=<id>` — newest-first page of ~10 rows
   (`id, before_image, after_image, settings, is_hero, created_at`), plus `hasMore`.
   Lazy migration on first call: if the user has zero rows but `users.before_image`
   AND `users.after_image` are set, insert them as a row with `is_hero = true`,
   `settings = {"migrated": true}`.
2. `POST /api/transformations` — body `{ before, after, settings }`. Validate both are
   `data:image/` strings (copy validation at `server.js:1976-1980`). Insert; mark the
   new row `is_hero = true` and clear the flag elsewhere (matching today's behavior where
   the latest generation becomes the hub hero); also mirror into
   `users.before_image/after_image` so the legacy endpoint keeps working. Enforce the
   30-row cap (delete oldest non-hero rows past 30). Return the new row's id.
3. `POST /api/transformations/:id/hero` — set `is_hero = true` on that row (ownership
   check: `user_id = req.user.id`), false on the user's others, AND update
   `users.before_image/after_image` to this pair (keeps `renderHubHero`'s server
   fallback and the trainer photo pathway consistent). Return `{ ok: true }`.
4. `DELETE /api/transformations/:id` — ownership check. If deleting the hero, promote
   the newest remaining row to hero (and mirror to users columns); if none remain,
   null out `users.before_image/after_image`.

Keep `GET/POST /api/account/transformation` untouched (other flows read it).
Change: in the existing `POST /api/account/transformation` handler, ALSO insert into
`transformations` (same dedupe caution: `saveTransformationIfLoggedIn()` fires on every
login/hub load with the same localStorage pair — dedupe by skipping insert when the
newest row's `after_image` is identical).

### Phase 2 — Gallery screen with slider cards

**index.html**:

- New screen `#transformationsSection` styled like the other screens (nav-bar with back
  button → `showHub()`). Register in `showScreen` (`index.html:2263`).
- Flip the hub tile live: remove `data-soon` at `index.html:1596`, add the chevron svg
  (copy an active tile), and route `data-feature="transformations"` →
  `showTransformations()` in the hub tile click handler near `index.html:3172`.
- `showTransformations()`: fetch page 1, render cards newest-first, "Load more" button
  when `hasMore`. Empty state: friendly copy + "Generate your first transformation"
  button → `showScreen('form')`.

**Card layout** (one per transformation):
- Slider viewer (below), date label ("July 10"), intensity chip from `settings.intensity`
  if present.
- Hero badge "⭐ On your home screen" on the `is_hero` card.
- Action row: `Set as my goal` (hidden on hero card) · `Share` · `Print` · `Delete`
  (trash icon, `confirm()` before calling DELETE).

**Slider implementation** (~25 lines JS + CSS, no libraries):
- Container `position:relative; overflow:hidden; aspect-ratio` from the image.
- Before `<img>` fills the container; after `<img>` in an absolutely-positioned wrapper
  with `clip-path: inset(0 50% 0 0)`; a divider handle absolutely positioned at 50%.
- Pointer events (`pointerdown/move/up` + `setPointerCapture`) on the container update
  clip-path + handle left as a percentage; clamp 2–98%. `touch-action: none` and
  `user-select: none` on the container (mobile is most traffic).
- Corner labels "Before" (right) / "After" (left) as small pills.
- IMPORTANT: before and after images can have different aspect ratios (Gemini output
  isn't guaranteed to match input). Use `object-fit: cover` on both images with a fixed
  3/4 aspect container so they overlay cleanly.
- Lazy-load images (`loading="lazy"`) — cards hold large base64 strings; render pages
  of 10.

### Phase 3 — Share / download

Per-card **Share** button:
- Compose a single branded image on an offscreen `<canvas>`: before left, after right
  (side-by-side reads better as a static shared image than a half-slid slider),
  "BEFORE" / "AFTER" labels, footer strip with the logo/wordmark + "absbyai.com".
  Target ~1200×900. Draw both with cover-fit cropping.
- `canvas.toBlob()` → if `navigator.canShare({ files })` (iOS/Android), use
  `navigator.share({ files: [file], text: 'My transformation — absbyai.com' })`;
  otherwise fall back to a download link (`a[download="my-transformation.png"]`).
- Reuse the same composite for a **Download** fallback — one button labeled "Share"
  that downloads when share isn't available is fine; follow the pattern of
  `resultDownloadBtn` if a separate download control looks better in the card.
- PostHog: `transformation_shared` (with `{ method: 'share' | 'download' }`).

### Phase 4 — Goal context on hero swap (program cross-sell)

When `Set as my goal` succeeds:
1. Re-render the card badges + refresh localStorage keys (`LAST_BEFORE_KEY`/
   `LAST_AFTER_KEY`) with the new pair so `renderHubHero()` shows it instantly.
2. If the user has a program (`GET /api/program` returns one — endpoint at
   `server.js:2549`), show an inline prompt card under the gallery header (not a modal):
   "New goal, new plan? Your training program was built for your old goal image.
   Rebuild it for this one." with buttons `Rebuild my program` / `Keep current program`.
3. `Rebuild my program`: reuse the regenerate pattern at `index.html:3583-3604` — take
   the newest program row's saved `intake`, call `POST /api/generate-program` with the
   NEW before/after pair as `photos` (strip data-URL prefixes to base64 + mime, same
   parse helper used at `index.html:3499-3500`), `photoConsent: true` only if the
   original intake had consent (`a.photo_consent !== false` pattern, `index.html:3492`).
   On success → `showScreen('program')` with the fresh block.
4. Gate: full rebuild is members-only (same as trainer). If not a member, route into the
   existing trainer paywall flow rather than silently failing.
5. PostHog: `transformation_hero_swapped`, `program_rebuilt_for_new_goal`.

### Phase 5 — Print upsell per card

- Refactor the upsell entry point: `showProductSection()` and `handleCheckout()` read
  `state.lastAfterDataUrl` (`index.html:2565, 2580, 2655`). Add
  `upsell.imageDataUrl` and `upsell.returnScreen`; have those three sites read
  `upsell.imageDataUrl || state.lastAfterDataUrl`. Set both fields when entering from a
  gallery card's `Print` button (`upsell.returnScreen = 'transformations'`).
- Back buttons: `productBackBtn` currently goes to `'email'` (`index.html:2861`) —
  change to `showScreen(upsell.returnScreen || 'email')`. Post-purchase confirmation
  screen can stay as-is.
- The print uses the AFTER image only (matches the existing product mockups).
- PostHog: `print_upsell_opened_from_gallery`.

### Phase 6 — Wire generation saves to the gallery

- In `saveTransformationIfLoggedIn()` (`index.html:3093`), switch the POST to the new
  `/api/transformations` endpoint with
  `settings: { intensity: state.effectiveIntensity, condition: state.condition }`
  when those state fields exist (they won't on login-restore calls — send `{}`).
  Server-side dedupe (Phase 1) handles the repeat-fire on login/hub load.
- Anonymous users: unchanged (localStorage only). The gallery tile for logged-out users
  doesn't exist (hub is members/accounts only) — no extra gating needed beyond
  `requireAuth`.

---

## Verification checklist

Local: `DATABASE_URL=pgmem:// node server.js` (note: local Anthropic key is invalid —
Claude endpoints only testable on prod; nothing in this feature needs Claude, and the
Gemini generation flow can be bypassed by seeding localStorage keys with small data URLs).

1. Sign up fresh → generate (or seed) → gallery shows 1 card, marked hero, hub hero matches.
2. Legacy migration: user with only `users.before_image/after_image` set → first gallery
   load creates the row.
3. Generate again → 2 cards, newest is hero (matches current app behavior).
4. Slider drags with mouse and touch (preview_resize mobile), clamps at edges.
5. Set-as-hero on the older card → hub hero swaps instantly (localStorage) and survives
   a fresh login on another "device" (clear localStorage, log in, check hub).
6. Rebuild-program prompt appears only when a program exists; rebuild produces a new
   block using the new after image; non-member hits the paywall.
7. Share button: download fallback produces the branded composite (check labels +
   watermark, both orientations of input photo).
8. Print from gallery card → product screen shows that card's after image; back button
   returns to gallery, not the email screen; complete a Stripe test checkout.
9. Delete: non-hero delete just removes; hero delete promotes newest remaining; deleting
   the last card empties the hub hero gracefully (hubHero hidden, no JS errors).
10. Login-restore fires `saveTransformationIfLoggedIn()` — confirm NO duplicate row is
    created (dedupe works).
11. pg-mem: all new DDL runs clean on `pgmem://` startup.

When done: commit and push to main (Railway auto-deploys); verify on absbyai.com.
