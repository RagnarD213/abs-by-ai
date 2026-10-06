# Private Workboard

Standalone `/dash` (the former `/workboard` address redirects to `/dash`), mounted before the product JSON parser and public static files. It starts with ten empty lists. No old dashboard import, sample cards, AI runners or dispatch actions.

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
