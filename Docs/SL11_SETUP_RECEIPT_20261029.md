# The Vacuum Shorts: organic setup, October 29, 2026

Status: **prepared, uploaded and verified; on the shared waiting list, not scheduled.** Dan approved the exact Round4 cover design1 for all three Shorts and both platform layouts. [Approved covers and setup status](http://127.0.0.1:9301/?revision=4).

| Short | Planned release, America/Chicago | State |
|---|---|---|
| A: How To Do A Standing Stomach Vacuum | January 16, 2027, 9 AM | Waiting list |
| B: Stop Holding Your Breath During Stomach Vacuums | January 16, 2027, 6 PM | Waiting list |
| C: Start With One 20-Second Vacuum Every Morning | January 18, 2027, 6 PM | Waiting list |

These are planned slots after the parent RO-02 YouTube release, read back live at January15, 9AM Central. Slots were checked against live posts, existing waiting entries and the approved dated phases. YouTube, Facebook, Instagram @danrosefit and TikTok share each Short's time. Blotato reached **200/200 posts** while setup was running. Zero SL-11 schedules exist. The existing `social-queue-daily-refresh` routine queues waiting videos in order when space opens; no separate task, automation or native YouTube upload was created.

## Files and verification

- Installed six exact approved R4 covers, preserving selected file hashes in `Short-form video content/covers/review/sl11-vacuum-20261028/picks.json`. Approved PNG/JPEG assets live in `Short-form video content/covers/approved-sl11-a`, `approved-sl11-b`, `approved-sl11-c`.
- The twelve approved cover PNG/JPEG files and picks record also match their Extreme and fresh Google Drive backups.
- Uploaded 12 assets to Blotato storage: three unchanged masters, three separate TikTok cover-first copies, three Instagram PNGs and three YouTube JPEGs. Every remote download SHA256 matches the checked local file. The JSON receipt contains exact URLs and hashes.
- All16 approved film/sidecar files still match project, Extreme and fresh Drive metadata. All original picture VCL units and full audio stream hashes are identical in the TikTok copies; each has one additional cover frame, about0.033seconds. Full decoding, frame/packet counts and actual frame0 image checks passed. No film editing, audio processing or audible listening was done.
- All12 planned platform targets passed cover/ad preflight. YouTube covers decode and are under2MB. Facebook's first caption line and chosen cover are registered both in the repository and live installer, with identical image hashes. TikTok timestamp is0 and the actual uploaded first-frame image matches the approved Instagram cover. Before/after live-queue cover audits found zero issues; live ad scan clean.
- Captions, descriptions, tracked organic root links and one pinned question per Short are saved in the three configs. Real footage flag false for synthetic media. No duplicate burned captions.

## Release follow-through

Pinned questions, posted and pinned automatically after release by `youtube-pinned-comment-daily`:

- A: Have you tried a stomach vacuum before?
- B: Can you keep breathing while you hold your stomach vacuum?
- C: How many sets of stomach vacuums do you currently do each morning?

Article: Shorts require no setup draft. Existing `sixpackabs-article-gap-daily` writes a300to500word article after release for a searchable question, or records the supported skip.

Public cover verification: **pending until release** on all four platforms. Supplied URLs and preflights do not prove public tiles. Existing `check-youtube-shorts-covers` checks actual YouTube/Instagram/TikTok/Facebook tiles and repairs where supported. Facebook preferred cover is applied after publication by the existing installer. Keep actual public release checks, pinned-comment gap and article gap checks; do not report them as already observed.

Edit queue: SL-11 remains finalized with setup/HOLD note, not uploaded. Drive status update succeeded. Its native artifact mirror remains for the normal version-guarded Claude sync. Set uploaded only when all12 actual schedules read back.

Exact configs: `scripts/blotato/configs/sl11-a-standing-stomach-vacuum.json`, `sl11-b-stop-holding-your-breath.json`, `sl11-c-one-20-second-vacuum-every-morning.json`. Full receipt: `Docs/SL11_SETUP_RECEIPT_20261029.json`. Local verification evidence: `Short-form video content/covers/review/sl11-vacuum-20261028/setup/`; TikTok upload copies: `/Volumes/Expansion/_edit_work/sl11-publish/`. No further action from Dan is needed.

Repository sync pending: the last safe-push stopped on live changes to `BLOTATO_QUEUE_PROGRESS.md` and `Handoffs/video-editing/jobs.json` (RO-28/SL-27 owner also has pending job edits). Task records/configs are saved locally; do not adopt live unrelated changes. After those owners commit, retry the existing push and commit the remaining owned SL-11 files. Media uploads, live FB installer, local waiting list and Drive edit-status note are already verified. No duplicate uploads or schedules are needed.
