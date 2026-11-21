# RO-26 Top 1 Percent setup receipt, 2026-10-17

**October 18 release dependency update:** RO-25 is public and processing succeeded at https://www.youtube.com/watch?v=xyi-B_5tccw. Its previous-video URL is now in the RO-26 config and the release hold has been cleared in both the config and video waitlist. Earlier statements below that RO-25 is not public are historical setup observations. RO-26 still requires its own live queue readback before anyone calls it scheduled or released.

**CONTENT, long-form. State: approved thumbnail installed in the release package; media uploaded and verified; release on explicit hold. No YouTube, Facebook, Instagram or TikTok post is queued or public from this setup.**

## Approval and selected cover

Dan: "A frosted glass, go ahead and install that" on 2026-10-17. Selected R4 A Frosted Glass, the AI yacht image with rounded translucent white panel, upright dark blue text and the exact headline "I'm 41. I'm Top 1%. How I Did It."

Final file: `social media graphics/youtube/thumbnails/Top 1 Percent/Top 1 Percent - thumbnail FINAL.jpg`. 1280x720, 385,181 bytes, SHA256 `e646fa30bb4f7a45f42b67ec0aa4c8e820e8790c6005667fb9c6493b4f686153`. Approval record and sources are adjacent. Original choices preserved. Hosted cover downloaded, decoded, visually checked and byte-hash matched. YouTube and Instagram config cover URLs both point at that exact approved JPEG.

## Source and classification

Source: `Codex Content Videos/Top 1 Percent - RO-26/Top 1 Percent | codex | 16x9 | RO-26.mp4`. 169,874,229 bytes; 5:03.7367667; 1920x1080; H.264, 30000/1001 fps, 9,103 frames; AAC stereo 48 kHz. SHA256 `395cd8fb4c99d0c235e9df691c8256e333d21a0f4efa09b60be53126fd6d24ce`. Project and Extreme files verified against the exact approved hashes. No film editing, grade, voice, graphic, label or subtitle burn-in.

Organic classification verified from exact-hash finished ASR and closing speech: "It's called I'm 41. I wasted my life. And I'll link to it in the description. Check that video out now. I think you'll learn a lot from it." No tap-the-button ad CTA. `content_type: organic`, actual source path retained. Ad scans before and after are clean.

The disclosed R5 exact-file delivery gate remains FAIL, 31 PASS / 8 FAIL. Dan approved the exact film as-is; no stamp was modified, relabeled or bypassed, and no edit/gate cycle was reopened.

## Backup verification

- Project delivery folder above, with selected cover, approval, description and chapters.
- Extreme: `/Volumes/Extreme/Codex Content Videos/Top 1 Percent - RO-26/`, matching master, SRT and approved cover.
- Google Drive: [Top 1 Percent - RO-26](https://drive.google.com/open?id=1R-AIr3qZhzGoh_b9rxN4rE9oUHSrkikz). Master, SRT, positioned ASS/VTT, selected JPEG and approval records are uploaded. Drive file hashes match the approved source. Live Google permission reads confirmed anyone-reader access on the folder, film and thumbnail. Description/chapters are also backed up.

SRT SHA256 `149d655016e8e82a5401e5c4ddef39f004a677dc14b21003d5fb9580a30d2a08`, 111 cues. ASS `01f654472445b3fc9ab8ff00bad239572442e813da2cfaf90c1e0a93c196d698`; positioned VTT `aed1da86f09dab564b73e38cffd2bc529c003a8a6d84593c7b3f0c6f630e0082`. Preserve positioned caption files; plain SRT cannot retain placement.

## Packaging and media

Title: **I'm 41. I'm Top 1%. How I Did It.**

Config: `scripts/blotato/configs/ro26-top-1-percent.json`. Description and chapters also adjacent to the master. Chapters checked against the exact finished ASR and extracted final-film frames: 0:00 introduction, 0:37 workout, 1:27 nutrition, 2:12 businesses, 3:31 martial arts, 4:18 recap, 4:44 closing. No continuous full-film human watch is claimed by this setup check.

Root organic link with YouTube/Facebook/Instagram/TikTok UTMs, `utm_campaign=longform`, `utm_content=ro26-top-1-percent`. New platform captions use the current seven-day free trial ask through per-config CTA fields, avoiding the helper's legacy free-image-preview defaults. Other video configs retain their existing behavior.

`ai_generated: true` because the film contains realistic AI clips, not merely because its thumbnail is AI-generated. YouTube containsSyntheticMedia and TikTok isAiGenerated verified in the prepared payload. YouTube keyword tags are saved in `youtube_tags` for the post-release Studio step; the current Blotato helper does not send that optional metadata.

Pinned comment: "Working out, nutrition, starting a business, or martial arts: which one do you need to work on?". Written through the clean-writer workflow. Posts and pins after release through existing `youtube-pinned-comment-daily`; no comment was posted now.

- cover: https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/118f59e9-6a0a-4f75-bf75-223bd5ca95b0.jpg (385,181 bytes; SHA256 `e646fa30bb4f7a45f42b67ec0aa4c8e820e8790c6005667fb9c6493b4f686153`). Uploaded and downloaded bytes matched.
- master: https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/62f1f94a-670c-45e8-8fb2-4a5de0b75c99.mp4 (169,874,229 bytes; SHA256 `395cd8fb4c99d0c235e9df691c8256e333d21a0f4efa09b60be53126fd6d24ce`). Uploaded and downloaded bytes matched.
- tiktok: https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/79cbf1b1-2eb2-4b59-b9d1-4a8c5ffbc88d.mp4 (169,952,478 bytes; SHA256 `8cac5cd02dba74562aae07a1e51be529218b4849c344f93df39e9907f9df90f6`). Uploaded and downloaded bytes matched.

Instagram uses the unmodified master, comfortably below 300 MB. No compression derivative was needed for YouTube, Facebook or Instagram.

TikTok has a separate cover-first derivative, not a replacement master. 9,103 source frames -> 9,104 output frames; all 14,239 audio packets retained; no decode errors; first-frame cover PSNR 51.51 dB. Actual decoded frame zero inspected. Landscape cover remains intact in the center safe area, with blurred fill. Source and derivative audio payload SHA256 both `7964f3e160bbd2247d9efe85af2798dc40169a9f3e1fce49f07e76e189b04662`. `videoCoverTimestamp: 0` verified in the prepared target.

Facebook cover registered under the exact first caption line from the config's hook in `scripts/blotato/fb_reel_covers.json` and the live installer registry. Matching approved image copied to `~/.absbyai/fb-reel-covers/covers/ro26-top-1-percent-frosted.jpg`, hash checked. Existing installer unchanged. Public preferred thumbnail verification awaits release.

Article: `sixpackabs/articles/TBD-ro26-top-1-percent.md`, 1,108 words, `build.py --check` OK; voice hard-rule check OK. Two internal links returned HTTP 200 and correct titles. Publishes automatically after release through existing `sixpackabs-article-gap-daily`. Native Claude clean-writer calls could not authenticate because their OAuth session expired. The documented `--print-prompt` clean-agent fallback completed article and packaging from the same five real passages, content plans and exact-film transcript. No voice rules were added to those writer calls.

## Release dependency and waiting list

Current approved calendar supersedes the handoff's older Sunday-only rule. RO-26 target is **Sunday October 25, 2026, 9 AM America/Chicago**; Facebook, Instagram and TikTok follow **Monday October 26 at 9 AM**. These are held targets, not actual schedules. Live queue at setup: 199/200, only one free slot; all four copies would need four slots. October 25 had no long-form conflict.

RO-25 "I'm 41. I Wasted My Life." is not public and not queued at this check. Its job is still draft_review; the current editing chat is [I'm 41 Wasted Life LFC R7](codex://threads/01a14b62-5b05-76c1-ba2e-e121a707fd39). The live YouTube read checked all 44 public channel videos and found no matching previous video. Its planned October 18 release in the calendar is not a released film or a promised watch URL.

**No previous-video URL was invented.** The description contains the explicit marker `[RO25_PUBLIC_URL_PENDING]` and `previous_video.url` is null. `release_hold` is set in BOTH the config and waiting-list entry. The normal queue helper and the existing top-up routine refuse/skip this hold. Direct helper refusal was verified without creating posts. Four-platform payloads separately passed cover/caption preflight. The queue dry run also refused the dependency hold before reaching capacity checks.

Once RO-25 is public, its setup/release operator must:

1. Read its actual public title, watch URL and release time from YouTube. Confirm it precedes RO-26.
2. Replace `[RO25_PUBLIC_URL_PENDING]` in the config/description with that exact watch URL, set previous_video.url/status and clear the config and waiting-list release_hold fields. Recheck the calendar and live slot if the date has moved.
3. Let the existing daily queue top-up queue this entry when four slots are available, or run the normal helper after its preflight. No new per-video automation.
4. Re-read all four saved schedules, then set RO-26 uploaded and sync the queue. Until then RO-26 remains finalized.

## Post-release work

No YouTube holding upload, native schedule, manual Public upload, media publication, or new automation. Blotato creates the only public YouTube video at release time. No YouTube ID exists for this setup yet.

- Existing cross-platform cover monitor checks actual public tiles after release; supplied URLs and API success are not public-tile verification. Facebook installer applies its cover after publication. TikTok static grid must show the selected cover.
- Confirm YouTube is public before the Monday posts. If delayed, postpone other platforms.
- Upload positioned English captions after the YouTube ID exists and inspect opening-photo/recap placement. Preserve the plain SRT sidecar, but do not imply it preserves positions. Add saved YouTube tags and the RO-25 end-screen link after release.
- Check pinned-comment and article routines after publication; no current publication claimed. No thumbnail A/B requested after the final single choice.

## Edit queue and remaining sync

RO-26 stays finalized, rev 24. The Drive status file was uploaded. Separate Shorts extraction job **SL-17** registered, ready for a segment shortlist and Dan's picks; no Shorts rendered. Its job doc is `Handoffs/video-editing/SL-17-top-1-percent-shorts.md`. The paused dispatcher was not restarted. Codex cannot access the Claude artifact database, so pending mirror writes remain pending rather than falsely marked synced.

Source code/config/article commits include `8e62d12` and `cc49ab4`. Safe-push is blocked by live other-owner changes in `.claude/skills/_shared/qc_corpus/corpus.json` and `Handoffs/README.md`; `Docs/DAN_DECISIONS.md` and the RA-16 recipe also have pending edits. Facebook registry already contained other-job changes before this task; those were preserved. No foreign work was adopted or forced through. Exact final sync attempt recorded below.

Full setup evidence: `/Volumes/Extreme/_edit_work/ro26-setup-20261017/` (verification JSON, original writer prompts, media readbacks, live queue snapshot, sharing checks and chapter stills).

The executed setup handoff was moved out of the OPEN index into Recently retired. Handoffs/README.md and fb_reel_covers.json include other owners' pre-existing edits, so those mixed files are preserved locally rather than adopting foreign changes in this task's commit. Both local operational records already include RO-26.

Final safe-push attempt: local commit `26275a9` retained; exit 2 before merging because three mixed/live files belonged to active work. No push completed. Local commits and operational files remain intact. The final receipt was refreshed in both delivery folders and backed up to Drive.

## 2026-10-18: RO-25 linked, RO-26 queued (Claude, scheduled task)

- RO-25 "I'm 41. I Wasted My Life." is public: https://www.youtube.com/watch?v=xyi-B_5tccw (published 2026-10-18 9:00 AM Central, processed). An earlier session today had already put that URL in the config and cleared both release holds.
- The top-up routine reads the waiting list in file order, so RO-26 sat behind November films. RO-26's entry was moved to just after RO-25. RO-19 (My First Spray Tan, Oct 21) stays waiting: its run failed because its Facebook cover is not in `fb_reel_covers.json`.
- `video_topup.py --apply` queued RO-26, verified 198 of 200. Blotato read-back: YouTube 5723694 Sun Oct 25 9:00 AM Central (description carries the RO-25 link); Facebook 5723691, Instagram 5723692, TikTok 5723693, all Mon Oct 26 12:00 PM Central.
- Edit Queue: RO-26 set to uploaded (rev 25), mirrored to the page and marked synced.
