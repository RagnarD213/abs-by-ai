# Alcohol And Abs SFL Setup (SL-10): cover review, 2026-11-01

Status: **awaiting Dan's four picks.** Nothing uploaded or scheduled. Review page: http://127.0.0.1:9652/ (managed review service).

- Films: the four approved masters, hashes re-checked against the handoff. Copies: Extreme `Short-form video content/Alcohol And Abs - SL-10/` (SHA-256 match) and [Google Drive](https://drive.google.com/open?id=1t0OUdc4jHBG9grA1vunikZALgqjuaCEZ) (MD5 match, anyone with the link).
- Covers: eight per Short, shuffled, neutral X labels. One real studio photo per Short with original person pixels. Blind sets and keys: `Short-form video content/covers/review/sl10-alcohol-20261101/s1..s4/`. Never show the key.
- Builder, prompts, draft captions and pinned questions: `scripts/covers/sl10-20261101/`.
- Checks: `check.py` 64 of 64 pass (size, text safe areas, text off faces and hair, YouTube JPEG under 2 MB). Face sheet inspected.
- Parent: RO-13 Sun Dec 20, 9 AM Central, on the shared waitlist (config `main` confirmed).
- Planned slots: Your Nightly Wine Is Killing Your Abs Thu Dec 24 9 AM, Your Drinks Should Taste Bad Thu Dec 24 6 PM, What Killed My Urge To Drink Fri Dec 25 9 AM, Stop Drinking 3 Hours Before Bed Fri Dec 25 6 PM.

Next after the picks: `blind.py pick` per Short, copy finals to `covers/approved-sl10/` with picks.json and hashes, TikTok cover-first copies, Blotato media uploads, four configs (`parent_config` and `after` = RO-13), Facebook cover registry, cover_audit and ad_guard, live queue read, then queue or waitlist. Any revision to a pick is a stop point: Dan approves the exact file first.
