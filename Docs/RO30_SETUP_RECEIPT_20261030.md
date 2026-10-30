# Love Handles (RO-30): setup complete, waiting for Blotato capacity

October 30, 2026. Owner: Codex chat 01a188fd-a89b-7641-bd9c-6c97531e8e24. Organic long-form.

Dan approved the R6 film October 29, then approved R3 thumbnail variation 2: “Let's go to the middle option. Go ahead and install that”. The exact middle image is installed as the final thumbnail, uploaded and configured for release. No further pick is required.

## Release plan and actual state

| Platform | Saved plan, America/Chicago | State |
|---|---|---|
| YouTube | Sunday January 10, 2027, 9 AM | Automatic waitlist |
| Facebook | Monday January 11, 2027, noon | Automatic waitlist |
| Instagram @danrosefit | Monday January 11, 2027, noon | Automatic waitlist |
| TikTok | Monday January 11, 2027, noon | Automatic waitlist |

Blotato has 197 of 200 slots occupied. Four posts would require 201, so the guarded queue dry run refused the batch before any post creation. All four release slots were clear. No partial batch or native YouTube holding upload was created. There are no saved schedule IDs or public YouTube ID yet. The existing social-queue-daily-refresh routine will queue this batch when space reaches its entry. Its entry is before the January 13 long-form and has approved_release fixed to 2027-01-10T15:00:00.000Z, so it cannot silently move that date. Social plan is 2027-01-11T18:00:00.000Z. No new per-video automation.

Config: scripts/blotato/configs/ro30-love-handles.json. Waitlist: scripts/blotato/video_waitlist.json. The approved dated long-form calendar is updated to waitlist, not booked.

## Approved exact files

- Full film: Codex Content Videos/Love Handles - RO-30/Love Handles | codex | 16x9 | RO-30.mp4. SHA256 bc6a8da6031d1e70ee8737b702532eb358199450020d931c91295abb6cb7b0ee; MD5 330a0be8efd01f372084195b907d8e07; 404,028,119 bytes; 8504 frames; 30000/1001 fps; 1920x1080; 283.750133 seconds. Approved film unchanged.
- Matching SRT: 8186 bytes; SHA256 083ea74b1f747382a77233136680d49e92f634f30808a38d120b54faf0e0c25b; 89 cues, 969 corrected words. Retained exact sidecar.
- Final thumbnail: social media graphics/youtube/thumbnails/The Fastest Way To Lose Stubborn Love Handles/The Fastest Way To Lose Stubborn Love Handles - thumbnail FINAL.jpg. SHA256 c6c1b45f15ba64fd5f66be295779502e7d7788be12253ceb132cd546a0aaa2e1; 270,639 bytes; 1280x720 JPEG. Headline “Lose Stubborn Love Handles”. Exact R3 middle file, original face and headline regions preserved. APPROVAL.json adjacent, approval and cover also beside the filed film.

Project, Extreme and Google Drive retain the full-quality film, SRT, final thumbnail and approval. Drive returned exact matching SHA256 and byte counts for all four files. Drive folder: https://drive.google.com/open?id=1QsNzBhyUtVZVMANA0SK_Vd1DW0W8odjs . Backup evidence: setup/install/backup-final-verification.json. No media is committed to the public source repository.

## Uploaded copies and cover installation

The original film exceeds Blotato's 400 MB upload cap. Hardware-only upload derivatives preserve all 8504 frames, 1080p, frame rate, duration and identical AAC payload. Main 150,820,101 bytes at 4 Mbps; Instagram 73,229,176 bytes at 1.8 Mbps. TikTok 150,894,219 bytes has one added cover frame, 8505 frames total and all 13,302 audio packets retained. Full decode found no errors; first cover frame PSNR 52.85 dB. The full landscape design fits the central 3:4 grid over a blurred background, preserving the approved headline and body shape.

All four assets (cover/main/Instagram/TikTok) were uploaded, downloaded in full and SHA256/byte matched. The shared cover guard passed all four intended payloads. YouTube and Instagram use the exact approved cover URL. TikTok has the verified cover-first media and videoCoverTimestamp 0. Facebook has the exact first caption line and approved JPEG in both repository and live cover installer registries; their image hashes match. Facebook target explicitly uses mediaType reel. AI footage flags are true for realistic generated motion in the approved film.

No scheduled rehosted files exist yet. Public covers are checked after release by the existing cover monitor and Facebook installer; upload URLs cannot prove future public tiles.

## Packaging and release work

Title: The Fastest Way To Lose Stubborn Love Handles. Description includes nine chapters read from the corrected finished transcript and native scene map, homepage UTMs, seven-day trial CTA, AI disclosure and five hashtags. Social captions use FOOD, with @danrosefit only. No retired Instagram mirror. No /start organic links or free-image offer.

Clean Dan-voice CLI calls failed because their existing OAuth session expired. Failure logs are preserved. The documented scripts/voice/write.py --print-prompt fallback supplied clean writers only the sampled real passages, exact finished transcript and plans. Metadata plus two article halves were completed. Only section numbering and supported italic-note formatting were adjusted. Both hard-rule checks passed. No credential changes or metered generation calls in this install phase.

Pinned comment: “What's harder for you: losing weight, or losing the last fat around your waist?”. Posts and pins automatically after release through youtube-pinned-comment-daily.

Article: sixpackabs/articles/TBD-ro30-love-handles.md, 924 words, build.py --check OK. Exact YouTube title, excerpt 120 characters, one CTA with cta_path=/, two internal links. Publishes automatically after release through sixpackabs-article-gap-daily. Article is prepared, not published yet.

English SRT is filed and recorded in config for application once the public YouTube ID exists. Tags are saved in config; Blotato's target has no native tags field, so no native tag application is claimed. Existing release checks must verify YouTube is public before next-day social release and inspect actual public covers. No new schedule or upload approval is needed.

RO-30 remains finalized rev16 while waiting for actual saved platform posts; Drive status-file update verified. Native Claude artifact mirror is pending its own supported writer and was not marked synced. SL-28 remains registered ready, unattended=false, for three Shorts: propose titles/full transcripts for Dan's picks before editing, after parent public. No Shorts worker or new chat launched.

Managed thumbnail page: http://127.0.0.1:8837/ . Browser visibly shows the chosen final image and honest waitlist state. Screenshot saved in setup/install/installed-thumbnail-page.png. Approved full-film review remains http://127.0.0.1:8836/ with prior paused sound-ready handoff preserved. No new playback or audible listen.

Original film QA and known mechanical gate failures remain preserved: full 36/39, phone 35/39, documented framing/composition and optional subtitle/phone-size mismatches. Dan approved the exact film. No rerender, new reviewer, threshold changes or new blanket PASS. All approved assets remain locked.

Evidence root: /Volumes/Extreme/_edit_work/RO-30/setup/install/. Includes approval, writer prompts/outputs/failures, encode/audio proofs, TikTok proof, uploaded byte hashes, backups, four-platform cover/slot preflight, queue refusal and before/after cover/ad audits.

Final shared cover audit: 197 scheduled posts, zero cover issues. Ad guard before/after: clean, 197 posts scanned. Existing waiting-list dry run recognized 52 pending videos and stopped at capacity (three free, four needed), with no writes.
