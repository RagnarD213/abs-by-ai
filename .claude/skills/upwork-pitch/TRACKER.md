# Where the pipeline lives

- Approval queue and tracker: https://claude.ai/artifact/8PaJHa8sq1DpB4mf2oU7xT ("Upwork Pipeline", private to Dan).
  Page source: `Docs/upwork-pipeline/upwork-pipeline.html`; republish from that path.
- Collections: `items` (one doc per Upwork job ID `upw-<jobid>` or outreach prospect `out-<slug>`), `spend`.
- Item fields: kind (proposal | outreach | video_card), title, org, url, found_at, score, fit[], connects, offer, price,
  subject (emails), draft_text, final_text, final_subject, dan_note, status, edited, decided_at, updated_at,
  contract_value, revenue, dan_minutes, next_action, batch.
- Dan approves or edits on the page; `final_text` vs `draft_text` is the training signal (SKILL.md, Training loop).
- Upwork profile: https://www.upwork.com/freelancers/~016109a7105ec3bf5d
- Outreach domain: danroseads.com, Namecheap (Dan's account, order 218087537, bought 2026-10-29, auto-renew off). DNS edited in Namecheap Advanced DNS via Dan's Chrome. Mailbox: Google Workspace dan@danroseads.com (Dan creates the account).
- Trial listings (Project Catalog, approved 2026-10-29):
  - $75 Ad Hook Fix: https://www.upwork.com/services/product/writing-translation-5-fresh-hooks-and-a-rewritten-opening-for-your-video-ad-2115911710890237840
  - $150 New Version: https://www.upwork.com/services/product/video-audio-a-new-version-of-your-winning-video-ad-2115913230303169467
  - Outreach emails link the profile (shows all 6 listings): https://www.upwork.com/freelancers/~016109a7105ec3bf5d
- Outreach batch 1 (20 prospects) is in `items` as `out-<slug>` (teardown and hooks in its `research` field). Full research JSON with contacts stays off the public repo.
- Upwork connector: added to Dan's claude.ai account 2026-10-29; a session only sees it if it started after that.
- Sender changed 2026-10-30: dan@socialresponsemarketing.com. danroseads.com stays unused.
