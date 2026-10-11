# Private Workboard

Standalone `/dash` (the former `/workboard` address redirects to `/dash`), mounted before the product JSON parser and public static files. It starts with ten empty lists. No old dashboard import or sample cards. Local agent dispatch stays disabled until explicit activation.

## Existing identity, isolated data

The board checks the existing `__Host-absbyai_brief` cookie against the hashed session and pinned owner in `brief_sessions` / `brief_owner`. It uses the existing `BRIEF_OWNER_EMAIL`, `BRIEF_GOOGLE_CLIENT_ID` and optional pinned subject configuration. No additional owner, secret, credential or permission is created. When signed out, `/workboard-login` opens the existing Google sign-in in another tab; the user returns and chooses Continue to return to `/dash`. The morning brief's routes, page and authentication code are unchanged.

`workboard_state` stores one versioned JSONB board, including ordered lists/cards, details and the most recent 500 activity entries. `workboard_files` stores private attachment bytes. A Postgres transaction locks the board row, verifies the client's version, updates the document and associated attachment bytes, then commits. An additional compare-and-swap update guards against concurrent overwrites. Stale writes return 409 without replaying the action. The UI keeps the draft and requires an explicit reload of current state before another save. Other tabs do not automatically refresh.

Every page, asset, state response and attachment download requires the same owner session. Browser mutations require the exact site Origin plus a custom action header. Attachment responses use `Content-Disposition: attachment`, `nosniff`, private/no-store caching and a restrictive CSP. File contents must match the allowed type. Limits: 8 MB per file, ten files per card, 100 MB total; PNG/JPEG/PDF/TXT/MD/CSV/SRT. Large video files remain external links in card descriptions. Filenames are bounded and may not contain path separators or control characters.

## Product behavior

- Card and list drag/drop saves immediately. Menus provide explicit list and position choices for keyboard/touch users.
- Title, description, labels and due date use Save changes. Checklists, comments, movement and attachments save individually.
- Closing a card or navigating back with unsaved text asks whether to keep editing or discard. A page reload warns about unsaved changes.
- Archive hides a card/list without deleting its content. Restore a list before restoring its individually archived cards.
- Search matches active card titles, descriptions and label names. Dragging is disabled while filtered to avoid ambiguous ordering.
- Comments are append-only. Checklist items can be edited, checked and removed. Labels have names and six selectable colors.
- Activity retains the latest 500 board changes. It is an activity feed, not a permanent audit log.
- The approved compact dark mockup's CSS is preserved in `baseline.css`; working board styles override it in `style.css`. At 3440 and 1440 pixels the header is 72 pixels tall and the board starts at 86 pixels. Smaller screens scroll the lists horizontally.

## Verification

Run from the repository root with its existing Node dependencies:

```sh
node workboard/tests/api.test.js
node scripts/brief/tests/brief_web.test.js
node scripts/brief/tests/page_render.test.js
```

The API suite uses a fresh `pg-mem` database and synthetic owner. It covers authorization, CSRF, private attachment reads, body/file validation, ordering, archive/restore, persistence through a new store instance, stale-version rejection, and route isolation. Postgres row locks and rollback behavior still require a real-Postgres deployment smoke check; `pg-mem` does not establish those database guarantees.

For browser QA, run `node workboard/tests/preview.js`, then `python3 workboard/tests/browser.py` with an existing Playwright installation. The preview binds only `127.0.0.1:8842`, injects a synthetic owner session and uses disposable memory data. It is not mounted by the production server. Restart it before every full browser suite. The suite covers actual pointer drag/drop, editing/cancel, attachments, search, archive/restore, two-tab conflict recovery, focus, touch movement and 3440/1440/390-pixel layouts. Screenshots are test artifacts, not initial board data.

Deployment requires no dependency installation or new environment variables. New isolated tables initialize on startup; a content-free readiness message confirms the database round trip. Verify the empty live board, owner login, persistence and private file download after deploying. Do not use production cards for synthetic QA without explicit authorization.

## Shared assistant column

`/dash` appends an Assistant column without changing `workboard_state`, its lists, cards, files or version. The toolbar's Assistant button scrolls to it. Tasks, completions, the active clock, unpaid sessions and historical payment records remain in the existing `todos.json`, `task-checks.json` and `timesheet.json` records. The original `/assistant` file, public access, priority sorting, daily schedule, next-morning completion hiding and completion cleanup remain unchanged. `/assign.assistant` is not an implemented route; it falls through to the product page.

Initial board task order follows existing priorities. Once a task is moved, `boardRank` stores the manual board order on the shared task objects; changing priority does not undo that order. The original assistant page continues sorting by priority. Assistant tasks cannot be dragged into unrelated board lists. Additions and priority/rank changes use an owner-only, CSRF-protected narrow endpoint, a task-list revision and the GitHub file SHA. Writes preserve every other list and task field. Completion changes use the existing assistant-scoped endpoint. Time actions call the exact existing start/stop/mark-paid handlers. Mark paid requires an explicit confirmation after payment has happened; it records payment status and does not transfer funds.

The assistant column refreshes its shared data every 30 seconds while visible, on window focus, and on Refresh assistant. Task data read failures are displayed; they are not treated as an empty list or zero balance.

### Read-only unpaid reminder protocol

Preferred scheduled-local lookup, from a connected Mac using the existing credential cache:

```sh
node workboard/unpaid-report.js --env-file /Users/danielrose/.absbyai-secrets.env
```

Alternatively set the existing `GITHUB_TOKEN` in the process environment and run `node workboard/unpaid-report.js`. The helper performs only an authenticated GitHub Contents GET for `RagnarD213/abs-by-ai`, `main/timesheet.json`. It never writes, starts/stops a clock, marks time paid, or triggers a worker. It prints only a summary and source file SHA. Do not expose the credential file or token. No new credentials or access are needed.

The owner-authenticated browser equivalent is `GET /api/workboard/assistant/unpaid`. It uses the existing pinned Google owner session (`__Host-absbyai_brief`) and returns private/no-store responses. An old dashboard key alone is not authentication for this endpoint. It performs a fresh GitHub read and returns 503 if storage cannot be read or validated.

The summary contains `recordedSeconds`, `activeSeconds`, `unpaidSeconds`, `hasUnpaidTime`, `unpaidSessions` (completed unpaid sessions only), `active`, `lastPaidAt`, `asOf`, `source`, and `sourceRevision`. The exact condition is:

```text
recordedSeconds = sum(entries[].seconds)
activeSeconds = active ? max(0, round((asOf - active.startedAt) / 1000)) : 0
unpaidSeconds = recordedSeconds + activeSeconds
hasUnpaidTime = unpaidSeconds > 0
```

Every `entries` session is unpaid; paid sessions live only in `payments`. Include the active session in the reminder balance. Repeat a daily chat reminder while `hasUnpaidTime` is true, suppress the payment reminder when false, and report an unavailable source rather than assuming zero after a read error. There is no wage/rate field, so this is an authoritative time balance, not a dollar calculation. The assistant's running clock can make time newly unpaid immediately after a payment, because the existing payment action closes and reopens an active session.

On October 11, the connected chat automation inventory had one enabled morning-brief task and no unpaid-assistant reminder. The local automation definitions contained no matching assistant/unpaid reminder. No reminder was created by this implementation.

Additional disposable regression suites:

```sh
node workboard/tests/assistant.test.js
node workboard/tests/timer-compat.test.js
```

The first verifies shared records, priority versus rank, persistence, stale/CAS rejection, strict balances, private reads, CSRF and unchanged board data. The second runs the actual production clock/payment handlers against synthetic storage and verifies historical payment preservation and active-session settlement/restart. Neither writes production records.


## Local agent queues

The Agents control connects this authenticated owner tab to a loopback worker at `127.0.0.1:8843`. The worker is bound only to loopback, checks the exact site Origin and Host plus a custom request header, and requires a 30-second signed grant from the authenticated board for each launch, control heartbeat and Desktop action. HMAC signing reuses the existing ADS_FEED_SECRET with a purpose-specific prefix; the secret stays out of browser responses, task files and agent environments. No permanent credential is issued. Owner-cookie authentication and existing CSRF controls protect every remote execution action. No new key, OAuth scope, account, database privilege or provider credit is required. Keep the authenticated tab open. This is a browser-mediated local runner, not a cloud worker or an unattended account token.

Start from this checkout with the installed subscription CLIs:

```sh
node workboard/local-worker.js /absolute/private/runner-state --env-file /path/to/existing/private-env-file
```

The state directory must be outside the repository because the existing product server serves repository files. The helper rejects an in-repository directory and sets private permissions. `WORKBOARD_CLAUDE` and `WORKBOARD_CODEX` can select already-installed CLI paths. It does not install software or change authentication. Claude uses the existing Max login; Codex uses the existing ChatGPT login. API keys are stripped from agent child environments.

Choose Agents, Connect local worker, then Enable new assignments. An existing queue card is idle until its explicit Run action or a move out and back into the agent queue. Creating a card directly in a queue, editing cards, imports, deployment, reload and worker startup do not assign work. Reconnecting and enabling a new activation makes old pending assignments idle; Run assigns them again deliberately. Pause prevents new claims while active work continues; deliberate assignments made while paused remain queued, and Enable resumes them in the same connected tab. Stop run terminates one task; Stop all and disable cancels pending assignments and stops active tasks.

Queue movement arms an execution ID inside the same Postgres transaction as the board movement. Claiming locks the board row and compares the version; it selects the first deliberately armed card in board order, with at most one claimed/running/stopping task per agent. Idle older cards are skipped. A successful claim moves the same card into that agent's in-progress list. Renaming or archiving required routing lists prevents dispatch instead of guessing a destination. Active cards cannot be moved or archived before stopping.

The local journal records launch intent before spawn and never spawns the same run ID twice, including after restart. A separate supervisor watches its heartbeat. Disconnect stops the entire process group after 35 seconds; execution has a one-hour ceiling. Server claims expire to blocked after 90 seconds, with no automatic retry. State reads display expired claims as blocked even without a connected worker. A launch interrupted before its process record becomes blocked. A continuation requires the owner's explicit inspected-changes action, records the prior result, and uses the verified prior local workspace. Paths from card input cannot select a local workspace.

Each run uses an isolated workspace. Claude's restricted file scope and command sandbox stay enabled; unapproved requests are denied rather than bypassed. Codex uses workspace-write with on-request approvals. MCP connectors and inherited provider API credentials are not exposed to these child agents. The task prompt prohibits sensitive external actions without separate human approval. Attachments remain private and preserved on the board; this first runner passes their metadata, not file bytes. A task needing attachment contents or assets outside its workspace must report blocked. Existing project/account work requiring more access needs a separately bounded integration; this implementation does not silently grant it.

The card shows status, bounded progress, a redacted completion summary, session ID, local workspace and log path. Only a zero-exit run with a valid structured completed result and no observed permission denial moves to the agent's review list. Blocked, failed, stopped, connection-lost and uncertain runs remain in progress. Agent review does not mean Done; final approval stays with the owner. Desktop uses the documented Codex `app PATH` workspace launcher with the session ID displayed separately. Claude's CLI exposes terminal resume, but no verified Desktop session-open API, so no speculative deep link is shown. Private local logs are bounded to 5 MB per run and are never copied into card comments.

Verification:

```sh
node workboard/tests/runs.test.js
node workboard/tests/execution-api.test.js
node workboard/tests/supervisor.test.js
node workboard/tests/postgres-claim.test.js /path/to/existing/private-env-file
WORKBOARD_AGENT_E2E=1 node workboard/tests/agent-e2e.js /absolute/private/test-state
```

The Postgres test creates and removes only a unique disposable schema, never production cards. The opt-in real-agent test creates clearly labeled synthetic cards and asks each subscribed agent to create and read back only `proof.txt` in its isolated workspace. It verifies actual session IDs, same-card result writeback, review movement and duplicate launch suppression. Normal activation is separate from these tests.
