---
name: posthog-api-access
description: "PostHog access from a session: both stored keys run HogQL queries only (no dashboard, insight, annotation or flag scopes), and no browser is signed in; read numbers with scripts/posthog/, dashboards are built from Dan's signed-in Chrome tab (recipe inside)"
metadata:
  type: reference
---

Verified 2026-10-10 (project 458833, us.posthog.com), while setting up the /start video test:

- `POSTHOG_PERSONAL_KEY` and `POSTHOG_API_KEY` in `~/.absbyai-secrets.env` (Railway has the same two, nothing else) can call
  `POST /api/projects/458833/query` with a HogQL query. Every other endpoint answers 403: missing scope `dashboard:read`,
  `insight:read`, `annotation:read`, `feature_flag:read`. So a session cannot create a dashboard, an insight, an annotation
  or a flag through the API.
- Neither Dan's Chrome nor the built-in browser pane was signed in to PostHog that day, and signing in is Dan's to do
  (password or Google sign-in).
- What works today: a small script that runs HogQL and prints the table. `scripts/posthog/vsl_video_test.py` is the pattern
  (key read from the secrets file, host filter on absbyai.com, people counted with `uniqIf(person_id, ...)`).
- The query endpoint answers a repeated query from a cache. Send `"refresh": "force_blocking"` beside the query or the
  numbers can be stale (2026-10-10: the script showed 1 visitor while the dashboard, correctly, showed 2).
- Testing a page's events with an automated browser: posthog-js drops events when `navigator.webdriver` is true or the user
  agent says HeadlessChrome. Hide both, or nothing is sent. Events fired as a page leaves ride a beacon that Playwright does
  not always catch; check those in PostHog itself.

- With Dan signed in to PostHog in Chrome, a session can build everything from inside that tab: `fetch('/api/projects/458833/...')`
  with `credentials: 'same-origin'` and the `X-CSRFToken` header taken from the `posthog_csrftoken` cookie. Insights are
  `{name, description, query: {kind: 'InsightVizNode', source: {kind: 'TrendsQuery' | 'FunnelsQuery', ...}}, dashboards: [id]}`;
  a text note is `PATCH dashboards/<id>/ {tiles: [{text: {body}}]}`; tile positions are `{tiles: [{id, layouts: {sm: {x, y, w, h}}}]}`.
  Check each tile with `GET insights/<id>/?refresh=blocking`: a background Chrome tab leaves charts as grey placeholders.
  The helper is lost on every page navigation; define it again. Worked 2026-10-10 (dashboard 2195388).

**How to apply:** when a task says "build a PostHog dashboard", check for a signed-in browser first; if there is none, deliver
the numbers by script, finish everything else, and ask Dan once to sign in. Related: [[vsl-landing-page]].
