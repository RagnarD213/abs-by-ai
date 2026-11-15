# DS-107 setup receipt, November 15, 2026

CONTENT (SFC). Owner: Codex, “Metabolism Not The Reason Setup”, M2.

**Current status: new cover round 2 ready, awaiting Dan's pick.** The previous set is rejected and preserved. Five new designs have checked Instagram and YouTube layouts. Three extra blind options remain unavailable after a fresh subscription-browser retry. No cover is approved or installed. Film, existing metadata and release state are unchanged.

**Current cover review: http://127.0.0.1:9804/**, same link on M2 and M6. Reply **Round 2 X1 through X5**. Dan has not yet reviewed this new set. The old http://127.0.0.1:9803/ set is retained only as rejected evidence and must never be installed. Its comparison key is permanently retired.

## Approved film

- Title: **Your Metabolism Is Not The Reason You're Fat**.
- Master: `Short-form video content/Metabolism Not The Reason - DS-107/Metabolism Not The Reason SFC R2.mp4`.
- SHA-256: `173a329050ec95f84e80db82e4ed32f929630bc4143aec5411171d5d6b2d8c78`, re-read during this setup. 51,796,831 bytes.
- SRT: `Metabolism Not The Reason SFC R2.srt`, 3,728 bytes, SHA-256 `6ba41da4e827e88c74eb296227d6e668f3d249812ed4345ef3d15551ce7b8f34`.
- Dan's approval: `dan-approval-20261115.json` beside the film, November 15: “This looks great ... This clip is attention-getting. This is approved. Go ahead and make that note for future edits and finalize this video. Proceed to set up.”
- No film render, remix, recut, gate modification or new playback was performed. Existing approval and delivery evidence retained.

## Historical first cover package (rejected)

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

1. Use only the new round 2 comparison set, `Short-form video content/covers/review/ds107-20261115-r2/comparison/`. Never read a selection from, rebuild, append to or install using the rejected set's key. If another round is requested, give it another new directory/key.
2. Record Dan's exact selection with `blind.py pick`; install from the original paired layouts, never the normalized review copy. A requested revision must be shown in both layouts and approved before installation.
3. Register/sync the Facebook cover, make the TikTok frame-0 derivative from the unchanged original master, upload master/derivative/covers and verify full downloads. Recheck the live queue, release calendar and `release_phases.py`. This is green screen, not kitchen.
4. Current queue: **199/200**, read November 15 during setup, insufficient room for four posts. No date reserved yet. If still full after the pick, complete all media/config verification, clear the cover hold and add one entry to the existing `scripts/blotato/video_waitlist.json`. Existing daily top-up owns scheduling; never create a per-video routine. Otherwise queue with the shared organic Short helper and fresh readbacks. Never create a direct or native-scheduled YouTube upload.
5. Keep DS-107 FINALIZED until the required verified upload/schedule conditions are met. Then use `scripts/edit-queue/queue.py set DS-107 uploaded`, mirror the queue page, and record actual readbacks. Update this receipt, the setup handoff index and the single board line.

Post-release public-cover verification and pinned-comment checks remain with the existing shared monitors. A queued thumbnail URL is not proof of a correct public tile.

## Historical repository checkpoint

Setup work saved in local commit `c95112b`. Shared safe-push stopped before merging because another session is actively editing `.claude/skills/_shared/editcap/editcap.py` (modified November 15 at 09:23). No other session's changes were altered. GitHub push remains pending; retry the shared safe-push after that live edit clears. This does not block the mirrored review link or verified backups.


## Cover rejection and new round, November 15

Dan rejected every cover at http://127.0.0.1:9803/. Exact dictated words, preserved without reinterpretation:

> Okay, I don't like any of these four new designs. All of them have me talking to an overweight guy in his 50s with a mountain of junk food in front of him. There is a speech bubble from him saying, 'My metabolism slowed down,' and a speech bubble from me saying, 'No.' Two variations are shirtless, and two variations are with a tank top.

The rejected source images, both layouts, public review files and private key are retained in `Short-form video content/covers/review/ds107-20261115/`. Their pre-rejection hashes are saved in `scripts/covers/ds107-20261115-r2/prior-round-rejection.json`. Its key is retired and must never be reused. The new round uses a separate folder and newly built key. Drop the entire argument scene, second character, junk-food pile and speech bubbles. Film, existing metadata and release state remain untouched.


## New cover round 2 delivery

- **Review:** http://127.0.0.1:9804/, chosen by a fresh `editroute.py free-port` call and served with the required managed `review_server.py`. Mirrored to M6. Both Macs return the same page and all 16 linked image files with matching SHA-256 values. This verifies network delivery; CUA browser visual inspection remains unavailable. The source images and ten finished phone layouts were visually inspected offline.
- **Five genuinely different designs:** natural meal preparation with a yellow condensed headline; climbing stairs with a pale rounded title card; original real studio portrait with large three-line bottom type; a standing dumbbell workout with dramatic white/cyan headline; rested Dan opening the curtains with a light teal type treatment. All show Dan alone. No second character, argument, junk-food pile or speech bubbles. Copy remains “It's Not Your Metabolism”, capitalizing every word.
- **Required mix:** two distinct AI Dan topic-action images, one original real studio photo (`studio-white-49`, original person pixels preserved), two history-guided AI Dan choices. Four new subscription image generations. No rejected generated source reused. Recent `approved-ds42`, `approved-sl21` and `approved-sl08` pick records and selected final images informed the concepts and typography.
- **Blind key:** created from scratch in the round 2 directory with `blind.py`. Shuffled X1 through X5; real-photo choice excluded from comparison scoring. No pick logged. No source-to-label mapping is shown on the page or in this receipt.
- **Google subscription retry:** fresh CUA inventory again returned “The browser access host is unavailable” with no browser surfaces. Native Chrome retry returned `cgWindowNotFound`, error `-10005`. Flow could not be opened, so none of the three intended extras was submitted. Zero Google image submissions, no credit or paid API charges. Specific failure saved in the new round's `comparison-unavailable.txt`. The absent extras are not counted as offered.
- **Checks:** all ten outputs are 1080 × 1920 RGB; JPEGs under 2 MB. One face detected per layout; zero text pixels intersect an expanded face/hair region. Both layouts visually checked for complete hair, readable type and clear abs at phone size. All four native AI sources inspected for identity, anatomy and natural action. Real studio cutout is composited locally without redrawing the person.
- **Preservation:** approved master, saved Blotato metadata config, existing description and pinned question are byte-identical to the pre-round snapshot. All 99 original evidence files, including the retired key, remain byte-identical. Proof: `scripts/covers/ds107-20261115-r2/protected-after.json`. No queue or scheduling commands, media uploads or film processing were performed this round.
- **New sources/build:** `Short-form video content/covers/review/ds107-20261115-r2/` and `scripts/covers/ds107-20261115-r2/`. Public page contains only neutral filenames and still images. Await Dan's pick before any further setup.

Round 2 repository checkpoint: local commit `123eca7` saves the new round and exact rejection. Shared safe-push is blocked before merging by live changes in `Docs/memory/MEMORY.md` and `scripts/edit-dashboard/review_handoff.py`; `AGENTS.md` also differs. Those files were left untouched. Push remains pending; the review service and both Macs' copies work independently. Retry after those owners finish.
