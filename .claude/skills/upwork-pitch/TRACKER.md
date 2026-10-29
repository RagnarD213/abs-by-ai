# Where the pipeline lives

- Approval queue and tracker: https://claude.ai/artifact/8PaJHa8sq1DpB4mf2oU7xT ("Upwork Pipeline", private to Dan).
  Page source: `Docs/upwork-pipeline/upwork-pipeline.html`; republish from that path.
- Collections: `items` (one doc per Upwork job ID `upw-<jobid>` or outreach prospect `out-<slug>`), `spend`.
- Item fields: kind (proposal | outreach | video_card), title, org, url, found_at, score, fit[], connects, offer, price,
  subject (emails), draft_text, final_text, final_subject, dan_note, status, edited, decided_at, updated_at,
  contract_value, revenue, dan_minutes, next_action, batch.
- Dan approves or edits on the page; `final_text` vs `draft_text` is the training signal (SKILL.md, Training loop).
- Upwork profile: https://www.upwork.com/freelancers/~016109a7105ec3bf5d
- Outreach domain: danroseads.com (registered at WordPress.com; mailbox Google Workspace), set up 2026-10.
