---
name: browser-task-fallback
description: "When Claude in Chrome disconnects mid-task, immediately move logged-out work to the in-app Browser pane instead of making Dan troubleshoot; Dan threatened to switch to ChatGPT over this (2026-09-10)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 40972f7d-d291-4769-b379-262cbe6c3366
  modified: 2026-09-10T19:32:38.550Z
---

On 2026-09-10 the Claude in Chrome extension dropped repeatedly mid-task (Amazon return + Craigslist post) and stayed at 0 connected browsers even after Dan opened the side panel and toggled the extension. Several turns were spent asking Dan to click things. He said: "You need to get better at handling browser tasks like this, or else I'm going to switch to ChatGPT."

**Why:** Dan's cost is his attention. Every "try this and say go" turn is a failure from his side, even when the cause is the extension.

**How to apply:**
- After ONE failed reconnect check, stop diagnosing. Route anything that needs no login (Craigslist posts, research, public forms) to the in-app Browser pane (`mcp__Claude_Browser__*`, `preview_start {url}`) and keep going.
- Only work that needs his logged-in sessions (Amazon, Google Ads, Gmail web) waits for Chrome. Give him ONE fix to try (reload the extension at chrome://extensions, or quit/reopen Chrome), not a ladder of steps.
- Batch every step that needs him (payment, packaging answers, logins) into a single ask at the end.
- Tool results that come back "[BLOCKED: Cookie/query string data]" mean the output contained a URL with a query string. Return only the needed text, never hrefs.
- Craigslist radio buttons and submit buttons ignore ref clicks. Set `checked` and call `form.requestSubmit()` in JS, then confirm the breadcrumb, because a label-text match picked the wrong category once.
- Amazon's return center (React) ignores ref clicks, and JS text-match clicks hit hidden duplicate buttons (6 invisible copies of "Yes"). Coordinate clicks from a 0.55-scale screenshot work: divide by 0.55 (e.g. the yellow Continue at (581,65) goes to (1056,118)). Take a fresh screenshot after navigating, because the layout shifts. The only return method offered for a seller-fulfilled "Ordered too many" was UPS drop-off with $11.40 deducted from the refund.
- If Chrome reconnects after a toggle, it comes back as a NEW tab group, so old tab ids are dead. Call tabs_context_mcp first.
- Dan may finish a task himself while Claude is blocked ("Already finished the Craigslist job. Don't do that again."). Before resuming a paused outward-facing task, confirm it's still wanted; never re-post.
Related: [[local-hiring-reliability]], [[computer-takeover-frustration]].
