# Private morning brief inputs

Status: local collection is manually proven. Owner-login, private page and validated publication code are implemented and tested locally. Google client/runtime setup and production proof remain incomplete. Daily delivery is not enabled.

## Requirements settled in the September 30 interview

- Have a private, iPad-first page ready by 7:30 AM America/Chicago every day. Support phone and desktop sessions. Update the page without a daily notification. Reading should take two to three minutes.
- Put one concrete next action first. Use Daniel's latest applicable, explicitly ranked planning priorities from Claude Code desktop. Otherwise use the top ranked Daniel In Progress Trello card, then the top Daniel Queue card. Trello will have separate Queue, In Progress and Completed lists for Daniel, Codex and Claude. Its board is still being built.
- Include genuine Gmail customer, collaboration and sponsorship opportunities regardless of size, plus information that unlocks the current plan. Intake is not limited to contact-form and Stripe labels. A failed inbox read is not an empty inbox.
- Show Google Ads campaign spend and separate free generations, email leads, trials and paid conversions. Show visitor and conversion statistics for absbyai.com and sixpackabs.com. Keep attribution counts separate from backend customer totals. Recommend actions only where the evidence supports them.
- Use YouTube history to identify actions relevant to the current priority. Surface a new model, skill or plugin only when it offers a practical benefit for Daniel's video, photo, writing or core work.
- Yesterday's context must come from verified activity or Daniel's answer. Failure to open the brief does not prove that yesterday's action was ignored. No automatic aging escalation or carryover of old pinned priorities.

Daniel reported that the old brief's first-action concept was useful, but its priorities were wrong because it lacked his current focus. The old page was still a September 16 edition during discovery. Old spend-only output did not help him act, and Gmail was not connected. These observations do not establish every cause of the old routine's failure.

Optional personal imagery remains unconfigured. Keep its references, preferences and prompts outside Git.

## Run the helper

Requires Python 3.9 or later with zoneinfo, and a Node version supporting fetch for live Ads reads. Run from the repository:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/brief/collect_inputs.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/brief/collect_inputs.py --live
```

The default output directory is `~/.absbyai-brief`, with mode 0700. `brief-inputs.json` and `planning-state.json` are written atomically with mode 0600. The helper rejects output anywhere inside a Git checkout. `--state-dir` can select another private directory. Credentials are parsed from `~/.absbyai-secrets.env` at runtime; they are never sourced as shell code or printed. `--secrets-file`, `--project-root`, `--config` and timezone-aware `--now` are supported.

Without `--live`, network sources are `not_checked`. With it, the helper performs dashboard GETs, Google Ads search queries using an existing refresh token, PostHog aggregate queries, and the existing organic-ad guard's read-only scan. It never changes campaigns, queues, accounts or schedules. It does not call the legacy ads-digest writer, which could turn a failed read into apparently empty results.

Exit 0 means private output was written, not that every source succeeded. Read each source's status. `missing`, `stale`, `error`, `partial`, `not_checked` and `no_current_plan` must not be interpreted as zero. The collector reports `scheduleChanged: false` and makes no assertion about an external routine's enabled state. The writer reads private `cloud-routine-state.json` separately.

## Claude planning scope and freshness

Metadata comes from `~/Library/Application Support/Claude/claude-code-sessions/*/*/local_*.json`. Exact project `cwd` or `originCwd` must match before a transcript is opened. Only planning titles or explicitly nominated session IDs are eligible. The default project is `~/Documents/Claude/Projects/Abs By AI`; transcripts come from its corresponding directory in `~/.claude/projects`.

The reader keeps byte offsets, file identity, UUID ancestry and short extracted priorities in private state. It retries unfinished JSONL lines, rescans replaced/truncated files and skips malformed records with a warning. It excludes sidechains, injected skill text and assistant recommendations. A task must come from a human-origin Claude desktop frame with the exact project cwd. An active conversation's UUID ancestry excludes abandoned branches. Archived sessions remain eligible.

The latest applicable explicit priority message wins. Later discussion without ranks does not replace it. Messages older than 36 hours or more than five minutes in the future are excluded. Today/tomorrow scope is checked against Chicago's date. Supported ranks are top/first, second, third and priority 1/2/3. The first task for a repeated rank is retained. Questions and negated priorities are excluded. This conservative parser does not understand every natural-language plan; an unrecognized plan falls back to Trello rather than inventing a ranking. Review extracted tasks during proof runs.

The old next-day-plan file is supporting context only, usable when its `forDate` is today and its `writtenAt` is fresh. It does not override the human planning or Trello rule. Editor deliveries require today's local run date when their timestamp has date-only precision. Watch-review output expires after eight days.

## Private configuration and mapping

Store configuration outside Git and pass it with `--config`. Supported keys are `planning_session_ids`, `claude_metadata_root`, `claude_transcript_root`, `trello_snapshot`, `social_queue_snapshot`, `google_ads` and `site_events`. Paths can be supplied as absolute paths. Do not put credentials in this file.

`google_ads` accepts `customer_id` and `conversion_actions`. Each outcome key (`free_generations`, `email_leads`, `trials`, `paid`) maps to a nonempty array of verified conversion-action IDs. IDs must exist in the current account and cannot overlap outcomes. Available actions and observed attributed counts are included privately for verification. Names alone do not establish whether an action measures a completed generation, captured lead, trial or collected payment. Unmapped outcomes remain null. Fractional attribution is preserved, and YouTube subscribers are never estimated as customers.

`site_events` maps each supported hostname to outcome keys and verified event names. The collector queries full Chicago yesterday and the same weekday last week. It normalizes www/non-www before counting distinct pageview persons. Events are aggregate counts, not unique customer counts. A configured event with no rows returns zero; an unmapped outcome or unobserved visitor stream remains unknown. Mapping must be backed by checked tracking definitions. Host-filtered analytics can miss server events without a hostname, ad-blocked visitors and delayed events, so it is not a payment ledger.

Verified stage definitions and first newsletter-capture aggregates are documented in `Docs/MORNING_BRIEF_MEASUREMENTS.md`. Live collection now also performs one aggregate SELECT inside a read-only database transaction, using existing credentials. It never imports the application's schema initialization or startup jobs. Only site names and counts are returned. Verified first captures override browser email-attempt counts; other business outcomes remain unknown. Precise Ads stage signals are separate from those outcomes.

Until the Trello connector and board/list IDs are available, a fresh private export can be used:

```json
{
  "generatedAt": "2026-09-30T13:00:00Z",
  "lists": {
    "dan_in_progress": [{"id": "card-id", "title": "A verified task", "position": 1}],
    "dan_queue": []
  }
}
```

The timestamp must be timezone-aware and no older than 24 hours. Cards are sorted by position. An absent export is missing, not a fabricated empty board. This helper does not fetch or edit Trello yet. Local Gmail and Calendar intake is missing, but the parent brief writer has separately connected sources and can read them directly. A local missing status does not establish that the dot or parent cannot read Gmail or Calendar.

## Proof and remaining work

The September 30 manual proof selected that day's human sales-page priority; a second planning read consumed zero additional transcript bytes. Live dashboard, Google Ads, PostHog and organic-ad reads succeeded. Stale editor, watch-review and legacy plan inputs were excluded. Trello, Gmail and Calendar remained missing; conversion outcomes stayed unmapped. Private proof data was kept outside Git. Focused Python and Node tests cover freshness, branch ancestry, incremental reads, secret redaction, failed checks and conversion aggregation.

The remaining product work is Trello board/list access, the exact measurement decisions in `Docs/MORNING_BRIEF_MEASUREMENTS.md`, Daniel-only page authorization and persistent sessions, a private path from the linked Mac to the brief writer, and one manually grounded dot brief reviewed by Daniel. The writer can supply its connected Gmail and Calendar evidence without adding local adapters. Current dashboard access uses a shared secret rather than a Daniel-only Google identity; the exact proposed Google setup is in `Docs/MORNING_BRIEF_GOOGLE_SIGN_IN.md`. The proof does not confirm dot access to the Mac or enable any recurring run. No OAuth grants, authentication changes, image generation or schedule were made here.

Exact pushed commit `e3fb909` has no GitHub Actions runs or check runs. The existing Vercel integration automatically attempted a deployment and failed because `ANTHROPIC_API_KEY` references missing secret `anthropic_api_key`. This is not a passing CI result or a local test failure. Daniel approved the scoped follow-up push with that disclosed automatic attempt on October 2. Production is verified on Railway; see `Docs/MORNING_BRIEF_GOOGLE_SIGN_IN.md`. No Vercel secrets/settings are changed as part of this task.

## Private page and writer contract

`scripts/brief/web` replaces the brief route with a separate Google owner gate before existing shared-secret/static routing. Its document validator whitelists text fields, limits the main reading budget, rejects stale/future current-priority claims and unsafe links, and keeps missing counts null. `routineEnabled` is a boolean recording separately confirmed external state; true requires validated cloud schedule metadata. Source statuses stay independent, private automation IDs are discarded, and receipts explicitly report `scheduleChanged: false`. The page shows the edition's real date and warns when it cannot establish today's priority. No raw transcript or arbitrary HTML is rendered.

The writer saves a private schema-version-1 document outside Git, then runs `python3 scripts/brief/publish_brief.py /private/path/edition.json` to validate only. For the manual proof, the signed-in owner can upload that reviewed file at `/brief-publish`; same-origin custom-header validation and the owner session protect publication, without an ingestion secret. The owner's brief session cannot access the older dashboard APIs. Google client configuration and actual owner/device proof must precede private publication.

Adding `--publish` to the CLI uses the fixed production endpoint and a Mac-only Ed25519 signer. Pass `--key-file` for the private local key. Railway holds only `BRIEF_PUBLISH_PUBLIC_KEY`; shared ingestion-secret authentication is removed. The signed machine route fails closed until its public key is configured. See `Docs/MORNING_BRIEF_PUBLISHING.md`. Neither publication mechanism schedules the routine.

The parent-authored September 30 proof is stored outside Git and explicitly retrospective, based on September 29 measurements. A separately validated structured edition preserves that date. Neither establishes an October 2 priority, a production-page proof or a scheduled routine.

## Social release queue

Show urgent/tomorrow review flags, then an expandable next-seven-days queue to keep the main brief short. Each row preserves its source ID, platform/account, scheduled time, title/caption, cover review link when observed, review link when known, and explicit cover/description/link/duplicate/asset-match statuses. `missing`, `unverified` and `not_applicable` are distinct. A Facebook payload with no cover field is unverified, not proof of a missing installed cover.

`social_queue.py` normalizes independently collected private Blotato and YouTube Studio snapshots plus completed URL checks and private reviewer flags. It never requests or mutates a schedule. The collector accepts a normalized private `social_queue_snapshot` and expires it after 12 hours. Native Studio schedules must be checked separately using the existing authorized channel's complete uploads playlist and `videos.list` publish times. Do not treat a missing Studio read as an empty native queue. Duplicate checks preserve rows and compare within verified account mappings; uncertain cross-provider account mapping still requires review.

The October 2 read-only research found 34 Blotato platform releases plus 2 native Studio schedules in its rolling seven-day window. Its private snapshot includes specific preflight review flags. It stays separate from the September 30 retrospective edition. No post was changed. The later routine must recollect before using this snapshot as current.

The October 8 master inventory and iPad calendar use `social_daily.py` for complete read-only Blotato refresh, approval-backed studio imports, exact-byte deduplication and a date-preserving top-up dry run. Run it before intake and again after creating the brief, then publish its `social-queue.json` as the edition's queue. Master records are imported in bounded signed batches to the private website database; the inventory has no storage entry cap. Keep all runtime files outside Git. Native YouTube currently returns 401 and remains unknown. Public profile access alone is not a visual cover match. Scheduling activation is held for the parent's migration-diff review. The full workflow and evidence requirements are in `Docs/SOCIAL_MASTER_REVIEW.md`.
