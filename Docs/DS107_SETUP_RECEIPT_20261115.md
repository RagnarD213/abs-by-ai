# DS-107 setup receipt, November 15, 2026

CONTENT (SFC). Owner: Codex, “Metabolism Not The Reason Setup”, M2.

**Status: partly prepared, awaiting Dan's cover pick.** Film approved. Five standard covers checked and served. Three additional blind comparison images could not be generated because subscription browser access is unavailable. No cover approved or installed, no social media uploaded, no release scheduled or waitlisted. Edit Queue remains FINALIZED.

**Cover review: http://127.0.0.1:9803/**. Same link on the M2 and M6. Reply X1 through X5 to choose a finished pair. Nothing in the page identifies a generated option's provider. The real-photo option is excluded from model-comparison scoring. Dan has not yet reviewed or picked this set.

## Approved film

- Title: **Your Metabolism Is Not The Reason You're Fat**.
- Master: `Short-form video content/Metabolism Not The Reason - DS-107/Metabolism Not The Reason SFC R2.mp4`.
- SHA-256: `173a329050ec95f84e80db82e4ed32f929630bc4143aec5411171d5d6b2d8c78`, re-read during this setup. 51,796,831 bytes.
- SRT: `Metabolism Not The Reason SFC R2.srt`, 3,728 bytes, SHA-256 `6ba41da4e827e88c74eb296227d6e668f3d249812ed4345ef3d15551ce7b8f34`.
- Dan's approval: `dan-approval-20261115.json` beside the film, November 15: “This looks great ... This clip is attention-getting. This is approved. Go ahead and make that note for future edits and finalize this video. Proceed to set up.”
- No film render, remix, recut, gate modification or new playback was performed. Existing approval and delivery evidence retained.

## Covers and review verification

- Five distinct designs, each with separate 1080 × 1920 Instagram and YouTube layouts. Full-size YouTube JPEGs are under 2 MB. Copy: “It's Not Your Metabolism”, first letter of each word capitalized.
- Required mix: two topic-action AI Dan concepts, one original real pool photograph, two history-guided discretionary concepts. Past picks and selected images inspected before planning. The real photograph retains original face/body pixels, cropped above the brief leg openings.
- Source faces, physique and complete paired layouts visually inspected at phone size. All ten outputs have one detected face and zero text overlap with the expanded face/hair region. Headline and physique visibility checked. Evidence: `Short-form video content/covers/review/ds107-20261115/cover-qa.json`.
- Extra blind options: **incomplete**. On this attempt CUA inventory returned “The browser access host is unavailable”, with no browser surfaces. Native Chrome returned `cgWindowNotFound` (`-10005`). No Flow generation or credit charge occurred. Failure and the three intended concepts are saved; no paid API fallback used. This is an access failure, not a Google quality result.
- Actual generation: four subscription image calls, no paid image API. The real-photo choice required no generation. Current local model catalog confirmed `gpt-6.1-sol`; calls used high effort. Local Lanczos resize to 1080 × 1920.
- Shuffled with the shared `blind.py`, using its documented comparison-unavailable evidence option. No scorecard result inferred and no pick logged yet. Private comparison key remains in the ignored review folder; do not expose it.
- Served with `.claude/skills/_shared/review_server.py`, port **9803**, selected by `editroute.py free-port`. Review assets cached and mirrored to M6 by that service. Page and sample-image hashes match on both Macs. All 16 linked images return 200 and match local bytes on M2. Page contains no video/audio players. Browser visual inspection was unavailable; the finished still files were inspected offline.
- Build and evidence: `scripts/covers/ds107-20261115/`; public folder: `Short-form video content/covers/review/ds107-20261115/public/`.

## Backups: complete and verified

| Copy | Verification |
|---|---|
| Project delivery folder on shared Seagate | Approved master and SRT SHA-256 re-read |
| `/Volumes/Extreme/Short-form video content/Metabolism Not The Reason - DS-107/` | Both files match source bytes and SHA-256 |
| [Google Drive backup folder](https://drive.google.com/open?id=1mkfvq9MGT70LeJ4SZwD2C_haWu24Slay) | Both files match Drive SHA-256 and byte counts; full download comparison reports 2 matches, 0 differences |

Drive folder made anyone-with-link viewable using `rclone link`; unauthenticated subtitle download returns the exact SRT bytes/hash. Master Drive file ID `1gYVIUIXTgNd855btH9e18-9bRZf7n6B5`; subtitle ID `1WFfPCPqqv1Ghog1NA1WhZ55ZvGVT764U`. Originals retained. Local checksum records and download-check output saved in the build folder.

## Metadata and classification: prepared

- Config: `scripts/blotato/configs/ds107-metabolism-not-the-reason.json`. Contains the title, platform descriptions, tags, pinned question and source/hash. A saved `release_hold` blocks release while the cover is unpicked; media URLs and date remain unassigned.
- Organic classification comes from the final SRT's exact close: “Subscribe to my channel and go to SixPackAbs.com for all my newest videos.” No button CTA. `ad_guard.assert_organic` passes for the planned metadata/source. Live queue scan: 199 schedules, no ad content found.
- `ai_generated: true`, because the approved recipe contains realistic AI video inserts A0063, A0242, A0072 and A0182. This flag is based on the film, independently of its cover.
- Descriptions use the film's own points and SixPackAbs.com root links with platform UTMs. No em/en dashes, unsupported new fact or free-offer claim. Metadata hard-rule checks passed.
- Clean voice writer: local and remote Claude CLI attempts both returned “Not logged in”. Used the documented clean-writer fallback with the prepared five-passage prompts. No sign-in or account change attempted.
- **Pinned comment:** “Which has been hardest for you after 40: stress, food, moving less or sleeping worse?” Saved as `pinned_comment` in the config. The shared `youtube-pinned-comment-daily` routine posts and pins it after release. It has not been posted or pinned yet.
- **Article:** handled after release by `sixpackabs-article-gap-daily`, under the dedicated-Short rule; no setup article required.

## Continue after the pick

1. If Dan wants the absent comparison options before choosing, retry Flow when supported browser access is available, then extend and rebuild the neutral set. Do not manufacture a comparison result. Preserve existing labels while Dan is reviewing; explicitly issue a new review if the set changes.
2. Record Dan's exact selection with `blind.py pick`; install from the original paired layouts, never the normalized review copy. A requested revision must be shown in both layouts and approved before installation.
3. Register/sync the Facebook cover, make the TikTok frame-0 derivative from the unchanged original master, upload master/derivative/covers and verify full downloads. Recheck the live queue, release calendar and `release_phases.py`. This is green screen, not kitchen.
4. Current queue: **199/200**, read November 15 during setup, insufficient room for four posts. No date reserved yet. If still full after the pick, complete all media/config verification, clear the cover hold and add one entry to the existing `scripts/blotato/video_waitlist.json`. Existing daily top-up owns scheduling; never create a per-video routine. Otherwise queue with the shared organic Short helper and fresh readbacks. Never create a direct or native-scheduled YouTube upload.
5. Keep DS-107 FINALIZED until the required verified upload/schedule conditions are met. Then use `scripts/edit-queue/queue.py set DS-107 uploaded`, mirror the queue page, and record actual readbacks. Update this receipt, the setup handoff index and the single board line.

Post-release public-cover verification and pinned-comment checks remain with the existing shared monitors. A queued thumbnail URL is not proof of a correct public tile.

## Repository checkpoint

Setup work saved in local commit `c95112b`. Shared safe-push stopped before merging because another session is actively editing `.claude/skills/_shared/editcap/editcap.py` (modified November 15 at 09:23). No other session's changes were altered. GitHub push remains pending; retry the shared safe-push after that live edit clears. This does not block the mirrored review link or verified backups.
