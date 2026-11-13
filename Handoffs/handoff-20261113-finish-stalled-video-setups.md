# Handoff: finish three stalled video setups (2026-11-13)

**Executed 2026-11-13 by Codex.** DS-15/DS-19 complete on shared waitlist; RO-08 queued Nov27, approved Facebook cover installed. Receipts: `Docs/DS15_DS19_SETUP_RECEIPT_20261102.md`, `Docs/RO08_SETUP_RECEIPT_20261014.md`.

**Category:** CONTENT setup only (two SFC Shorts, one LFC). No editing.
**Owner:** Codex (setup owner for all videos since 2026-11-07). Grokbot may do item 2 if Codex is unavailable.
**Recommended model:** Codex newest Sol (`gpt-6.1-sol`), high effort.
**Written by:** Claude, from an audit of `Handoffs/video-editing/jobs.json`, `editcap.py status`, setup receipts, Blotato configs and the waitlist.

Dan's authorization: he asked for every started-but-unfinished video to be finished now. Do every step below without asking him. All three already have his approved film and approved cover; no new picks are needed.

## 1. Does Jiu Jitsu Get You Abs? (DS-15) and How To Use Battle Ropes (DS-19), SFC

- Stalled since 2026-11-03. Receipt `Docs/DS15_DS19_SETUP_RECEIPT_20261102.md` says PARTLY DONE: covers approved (Jiu Jitsu X3, Battle Ropes X8 text V3), Claude checked both HQ exports Nov 3. **No Blotato config and no waitlist entry exist** (checked 2026-11-13: nothing in `scripts/blotato/configs/` or `scripts/blotato/video_waitlist.json`).
- The earlier "current Codex setup chat owns it" note is 10 days stale; take it over. Do not regenerate covers or ask for picks.
- Spec, file paths and hashes: `Handoffs/handoff-20261102-jiu-jitsu-and-battle-ropes-sfc-setup.md`.
- Do: file the HQ masters (verify against the approved V2 hashes in that handoff), backups (project, Extreme, public Drive, checksummed), metadata, Blotato media uploads, then queue or add to the shared waitlist on the Shorts calendar (`Docs/SHORTS_RELEASE_CALENDAR.md`; neither is kitchen footage). Update the receipt, set both jobs in `jobs.json` to `uploaded`, list them in the receipt.

## 2. Intermittent Fasting: The Best Way To Get Abs (RO-08), LFC

- The daily top-up refuses to queue it: no Facebook cover entry in `scripts/blotato/fb_reel_covers.json` (still 0 matches on 2026-11-13). Its slot is Fri Nov 27, two weeks out, and its Short (SL-16) waits behind it.
- Execute `Handoffs/handoff-20261111-ro08-facebook-cover-blocks-queue.md` exactly (register Dan's approved thumbnail A from 2026-10-14, dry-run `video_topup.py` until it shows no PROBLEM line, check every other waiting long-form for the same gap).

## Done means

- DS-15 and DS-19 queued in Blotato or on the waitlist with readback; receipt says COMPLETE.
- `video_topup.py` dry run lists RO-08 with no PROBLEM line.
- Changed shared files pushed with `scripts/git/safe-push.sh`; this handoff marked executed in `Handoffs/README.md`.
