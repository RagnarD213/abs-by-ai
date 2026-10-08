# Master social inventory and daily review

The private master inventory retains every imported placement without a storage entry cap. Blotato remains the posting service and holds at most 200 queued platform entries across all accounts. The inventory is separate from that limit. Media references, captions, approval evidence, collection snapshots, database files and receipts stay outside the public repository.

The first import reads the complete live Blotato schedule and the approved studio-photo plan. A live schedule is recorded as an observed scheduled placement, with its source ID and collection time. It does not establish original approval or permission to recreate a missing post. The October 3 studio handoff explicitly approves its 27 posts, with 54 platform placements. Drafts outside that evidence are not promoted to approved content.

Every placement retains platform, account, exact authorized date, caption, media, cover, content kind and provenance. Imports are idempotent. Blotato re-hosts media per post, so the studio import joins a live placement only when its account, platform, caption and time agree and every uploaded image's SHA-256 matches the approved manifest. Ambiguous collisions stay separate for review. Their original evidence is retained even after a verified alias joins them.

The Mac uses a private SQLite inventory. The website has an additive PostgreSQL mirror in `brief_social_master`, behind the existing Google owner gate. Signed edition publication accepts optional `socialMasterImports` batches of up to 100 records. This bounds a request, not inventory storage. Repeat batches upsert the same identities; they never truncate the inventory. The normal edition excludes these import batches after validation. The owner can browse the complete mirror through paginated inventory reads.

## Daily sequence

Run `scripts/brief/social_daily.py` from the deployed code checkout with `--project-root` pointing to the existing Abs By AI project, `--state-dir` pointing to a private directory outside every Git checkout, and `--live`. The worker uses the existing Blotato key for GET requests only. It imports, verifies approved photo twins, checks upcoming assets, writes `social-queue.json` and `migration-plan.json`, and reports its counts. The existing collector can read that queue path through `social_queue_snapshot` in its private configuration.

Run the same read-only review after the brief is assembled, then include the resulting seven-day queue in the signed edition. Import changed master records in bounded signed batches with the same edition text and hero provenance. Check matching publication receipts and stored readback. Source timestamps retain their actual collection times. Updating the queue does not refresh business text or establish a new priority.

The new top-up planner considers only explicitly approved content with exact authorized future dates inside the next 30 days. It never moves an expired date, fills an arbitrary free day, replaces media, deletes a post or corrects a queued release. It holds unknown content types, absent approval, stale or inaccessible media, account/time collisions, ads rejected by the existing guard and unverified TikTok covers. Capacity includes every existing queued platform entry, even outside the 30-day window. Excess eligible items are reported as overflow and remain in the master list.

Activation is held for parent review of the private migration diff. There is no `--apply` CLI. The reusable reconciliation function requires the reviewed plan digest, takes a fresh full schedule count before every create, and records an uncertain submission before making a single non-retried POST. A timeout or failed readback stays held until reconciled. Successful creation requires a fresh schedule with the exact payload and date. Repeat runs do not repost confirmed placements. The caller must hold the inventory's process lock for the entire reconciliation. External writers do not share this lock; Blotato's own cap is the final account-wide guard.

## Release rules and evidence

New organic YouTube long-form releases are Sunday at 9 AM America/Chicago, at most one per week. A replacement counts as that week's release. The other platform copies cannot precede Monday at 9 AM and require verified public YouTube release. The planner reports violations and unknown first-release evidence. It does not fix them. Existing accepted posts, including the October 5 Facebook photo exception, are retained without a deletion or replacement recommendation. Photos are not subjected to the long-form cadence.

TikTok needs the approved tall cover embedded at frame zero and `videoCoverTimestamp: 0`. A zero timestamp alone does not prove the cover image or crop is correct. Follow `Docs/TIKTOK_COVERS.md` and the existing build verification before activation. No automatic cover rebuild or schedule replacement occurs here.

The calendar shows seven local Chicago dates, including the 23- and 25-hour DST days. Cover and video previews use authenticated same-origin requests. The media reader accepts only stored references on exact supported provider paths, does not follow redirects, supports a single byte range for inline iPad playback, and forwards no owner cookies or credentials upstream. Preview errors are visible and original-media links remain available to the owner.

Missing Facebook API cover fields do not prove a missing installed cover. A HEAD response proves availability only, not correct crop or visual match. Authentication failures, rate limits, old checks and inaccessible sources stay unverified. A confirmed 404 or 410 is reported as broken. Crop and asset identity remain unknown without specific evidence.

Public tile comparison is read-only. The private `public-tile-evidence.json` maps placement IDs to evidence identifying the exact public post, approved cover SHA-256, observed tile SHA-256, observation time and `public_profile_tile` surface. Equal observed bytes can establish a match. Different bytes alone cannot establish a mismatch because compression and grid crop can differ. A visual mismatch requires a recorded reviewer, normalized crop, assessment and reason. Wrong identity, stale evidence or unavailable platform access remains unknown. No correction, replacement or deletion is authorized by a finding.

Native YouTube reads are currently blocked by HTTP 401 `authError`, with reconnect owned by the parent. This worker does not refresh or replace those credentials. Native schedules and public release state are unknown, not zero. Public profile access on YouTube Shorts, TikTok, Facebook and Instagram must be separately observed; unavailable checks do not become invented matches.

## Verification

Run the brief Python unittest suite and the Node tests in `scripts/brief/tests`. The social tests cover more than 200 stored entries, duplicate and re-hosted imports, approval provenance, repeat top-ups, uncertain writes, changing capacity, locks, expired dates, Chicago/DST windows, Sunday releases, stale assets and mismatch false positives. Website tests cover owner denial, private caching, range playback, exact provider URLs and unchanged hero publication. Browser review checks the calendar at iPad and phone widths, preview failures and inventory paging.
