---
name: local-funnel-test-recipe
description: "How to exercise post-generation screens locally without a real generation — live-key launch config, seeding the before/after pair from public/img/proof in the browser, admin test account for member paths"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2e38e42c-56c9-43f2-99b1-70197a934707
  modified: 2026-09-08T22:59:48.550Z
---

Verified 2026-09-08 while building the post-lock-in analysis page.

- `.claude/launch.json` has an UNCOMMITTED local config `abs-by-ai-live-keys` (port 3011) that pulls the real
  `ANTHROPIC_API_KEY` out of `~/.absbyai-secrets.env` at start (GEMINI stays dummy, DB is pgmem). Use it when an
  endpoint needs Claude; the committed `abs-by-ai` config has a dummy key and is the failure-path test.
  Port 3000 is often held by a stale `node server.js` — autoPort handles it.
- Seed the funnel without generating: in the page's JS, `fetch('/img/proof/male-before.webp')` (+ `-after`,
  also `female-*`) → FileReader data URL → `localStorage.absbyai_last_before/after`, `absbyai_last_owner='anon'`,
  set `state.gender/condition/intensity/effectiveIntensity/lastAfterDataUrl`, then call the screen function
  (e.g. `showAnalysisScreen({from:'lockin'})`). No base64 has to pass through the tool call.
- Member paths: `ADMIN_EMAILS=hub@local.test` in the launch config → sign up that email via
  `authApi('/api/auth/signup', …)` + `setLoggedIn(data)` + `refreshMembership()` and `hasMemberAccess()` is true.
- The Browser pane's `window.fetch` override does NOT intercept the app's calls (isolated world) — test failure
  paths with the dummy-key server instead.
- The pane's `computer` scroll/screenshot time out or paint blank while the pane is hidden; `tabs_select` first,
  and use `javascript_tool` reads of `innerText` for verification.

**How to apply:** for any funnel/result/hub screen change, verify locally this way before spending a real
production generation; [[load-time-optimizations]] still applies (local key invalid unless the live-keys config is used).
