# Subscriber store — the marketing list

**Found 2026-09-10, fixed 2026-09-11.** The newsletter list lived in
`subscribers-data.json` at the repo root, persisted by PUTting the whole file to the GitHub
contents API on every signup. `RagnarD213/abs-by-ai` is **public**, so the file was served to
anyone at

```
https://raw.githubusercontent.com/RagnarD213/abs-by-ai/main/subscribers-data.json
```

with no token and no login — 28 entries, 23 of them real people's email addresses, plus the
device id and signup timestamp for each. Verified 200 OK before the fix.

The design was never wrong about needing to own the raw list. It was wrong about one fact:
`Docs/EMAIL_MARKETING_PLAN.md` wrote down "the repo must stay private", and the repo is not
private. Every signup from absbyai.com and from the sixpackabs.com newsletter form added
another address to a public file.

## What it is now

One row per address in Postgres, `subscribers` (see `db.js`). The in-memory
`subscribersStore` and the entry shape are unchanged, so `/api/subscribe`, the Resend welcome
sweep, `/api/unsubscribe` and the account-deletion path all read and write exactly what they
did before — only the persistence underneath moved.

| entry key | column | notes |
|---|---|---|
| `subscribedAt` | `subscribed_at` | TIMESTAMPTZ, normalised back to an ISO string on read |
| `deviceId` | `device_id` | |
| `source` | `source` | e.g. `sixpackabs` |
| `synced` | `synced` | legacy MailerLite flag; MailerLite was retired 2026-07-17 |
| `welcomeStep` | `welcome_step` | **NULL means absent, not 0** — see below |
| `welcomeNextAt` | `welcome_next_at` | `null` = sequence finished |
| `welcomeSentAt` | `welcome_sent_at` | JSONB, `{"1": iso, ...}` |
| `unsubscribed` / `unsubscribedAt` | `unsubscribed` / `unsubscribed_at` | |
| `excluded` | `excluded` | `@example.com` test rows |
| `deletedAccount` | `deleted_account` | set by account deletion |
| *anything else* | `extra` (JSONB) | catch-all, so a new field can never be silently dropped |

### The one trap

`welcome_step` **must** be NULL — not 0 — for an entry that predates the welcome sequence.
`ensureWelcomeFields()` decides whether to enrol someone by testing `welcomeStep === undefined`.
Store 0, or read NULL back as 0, and that subscriber is silently never enrolled. `extra`
exists for the mirror-image mistake: a field added to the entry shape without a column would
otherwise vanish on the next save.

## Verifying a migration

`scripts/subscribers/digest.js` and the gated `GET /api/subscribers/status` compute the **same**
fingerprint over the list — sorted keys at every level, `null` and absent treated as the same
thing, timestamps compared as ISO-8601. Counting rows is not proof: it misses a dropped welcome
step, which would re-send five marketing emails to people who already finished the sequence.
The digest covers addresses without revealing them, so it is safe to paste anywhere.

```bash
node scripts/subscribers/digest.js subscribers-data.json
curl -s -H "X-Dash-Key: $DASH_SECRET" https://absbyai.com/api/subscribers/status
```

Baseline at the commit that shipped this change (28 entries, 0 due for a send, so the digest is
stable across the first sweep):

```
digest       1f0cb629799fa9f75573111eec22374a3c6f5b0829d5bf2c0df0c1d7d3cbb404
dbRows       28        inMemory 28
excluded      5        unsubscribed 2        mailable 21
byStep       {"0":1, "1":5, "3":4, "4":2, "5":16}
```

## ⚠ This ships in TWO deploys, in this order

The migration seeds the table from the legacy JSON on the first boot that finds the table
empty — reading the file from the deployed checkout, and from the GitHub contents API as a
fallback. Both sources are the file itself.

1. **Deploy 1 — the code, with `subscribers-data.json` still tracked.** On boot the table is
   empty, the file is present, and the list is copied in. Logs
   `Subscribers migrated to Postgres: 28 of 28 row(s)`. Verify with the digest above.
2. **Deploy 2 — delete `subscribers-data.json` from the tip of `main`.** By now the table is
   populated, so the legacy read is never consulted again.

**Landing both in one deploy loses the app's copy of the list**: the container would have the
new code, no file on disk, and a 404 from GitHub, so it would seed from nothing.

Measured, not assumed — booted with an empty table and no legacy file, the store loads 0
subscribers and the welcome sweep sends **zero** emails. It iterates the store, so an empty
store is silent. Nobody is re-mailed; the failure is quiet, not loud, which is its own hazard.
Recovery is to re-seed from any copy of the file (git history has every version) via
`SUBSCRIBERS_LEGACY_FILE` with the table empty.

So the two-deploy order is cheap insurance rather than a disaster preventer — but it costs
nothing and it is the difference between a verified migration and a hoped-for one, so do it in
order anyway.

Deleting the file from the tip does **not** remove it from git history. Whether to purge the
history (needs a force-push) or make the repo private is Dan's call — see the audit below.

To rebuild the table from a backup copy of the file, set `SUBSCRIBERS_LEGACY_FILE` to its path
and restart with the table empty.

## Audit — what else the public repo exposes (2026-09-11)

`subscribers-data.json` was the only tracked file containing **other people's** personal data.
The rest is Dan's own, or business internals. Every one of these is written by the same
GitHub-contents-API persistence pattern, and all are world-readable today:

| file | what is in it | how bad |
|---|---|---|
| `subscribers-data.json` | 23 real email addresses + device ids | **Fixed by this change.** Third-party PII |
| `monarch-data.json` | Dan's **net worth**, 61 points of net-worth history, spending by category, yesterday's transactions | **Worst remaining.** Personal financial data |
| `credits-data.json` | device ids, per-device credit balances and meal counts, ~8 live Stripe `cs_live_…` checkout session ids | Pseudonymous, but ties identifiers to real purchases |
| `watch-data.json` | Dan's resting heart rate, steps, exercise minutes | Personal health data |
| `gmail-digest.json` | his mail digest — senders and subjects. Empty right now, leaks whenever it is populated | Third-party PII when non-empty |
| `timesheet.json` | the assistant's worked hours and payments (no name in the file) | Employment records |
| `brief-ads.json` | 79 KB of ad spend, campaign names, CPCs, conversions | Competitive intelligence |
| `todos.json`, `task-checks.json`, `plan.json`, `brief-ask.json` | the task board and daily plan | Business internals |

**`push-subs.json` — FIXED 2026-09-11, the same day, before it ever fired.** It was never in the
repo, only because nobody had subscribed to web push yet; `savePushSubs()` would have PUT it
there on the first subscription, and a push subscription carries the endpoint URL plus its
`p256dh` and `auth` keys — enough for anyone who reads the file to send notifications to that
person's device. It now lives in the `push_subscriptions` table (`db.js`), one row per endpoint,
seeded from the legacy file on the first boot that finds the table empty (`PUSH_SUBS_LEGACY_FILE`
overrides the source path) — in production there was nothing to seed, which is the expected case.
The GitHub PUT is gone, `push-subs.json` is in `.gitignore`, and `scripts/push/push-subs.test.js`
(38 checks, pg-mem) asserts zero writes to the contents API for it. Unlike the marketing list this
needed **one** deploy, not two: there was no file to keep in the tree while the table filled.

One behaviour changed for the better on the way: an endpoint the push service reports as gone
(404/410) is now DELETED from the table on both send paths. Under the whole-file persistence a
failed save meant the dead endpoint came back on the next boot and was retried forever.
