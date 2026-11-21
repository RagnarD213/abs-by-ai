# RO-12 "Top 5 Zepbound Tips" setup receipt (2026-10-01)

**Current platform timing (updated 2026-10-07):** YouTube stays Sun Oct 25 at 9 AM CDT. Facebook, Instagram and TikTok moved to Mon Oct 26 at 9 AM CDT, after YouTube. Confirm the YouTube video is public before those social posts release. Original same-day setup details below are historical.

- **Classification:** organic. Closing words (9:03-9:09): "Thank you for watching guys. If you enjoyed this video, subscribe to make sure you get my newest videos as soon as I release them." No tap/click-the-button CTA. `ad_guard.py --scan` CLEAN before and after the Blotato write.
- **Master:** `claude edited long form content/09 - Top 5 Zepbound Tips/Top 5 Zepbound Tips | claude | 16x9 | RO-12.mp4`, 2,419,960,621 bytes, 9:11.42, SHA-256 `7f6766c5e1d82881fb2a56b9b7414f6baa0bbe49f027828e507991d9f7cae67b` (matches the handoff).
- **Backups:** Extreme `/Volumes/Extreme/Claude Content Videos/Top 5 Zepbound Tips - RO-12/` (SHA-256 match); Google Drive `Claude Content Videos/Top 5 Zepbound Tips - RO-12` (byte count match, anyone with the link), https://drive.google.com/open?id=1nOpRxT9nusbHYNFMcBCKRUf7eGOgIuxN
- **Thumbnail:** `social media graphics/youtube/thumbnails/Top 5 Zepbound Tips/Top 5 Zepbound Tips - thumbnail FINAL.jpg` (Codex R3 C, Dan's pick), 1280x720 JPEG, 516 KB, used as is.
- **YouTube:** no holding upload (Blotato-only rule, Dan 2026-10-01, which replaces step 5 of the handoff). Blotato creates the public video at release. Title "Top 5 Zepbound Tips To Lose Fat And Keep Your Muscle". Description: filed `youtube-description.md` (7 chapters, not-medical-advice line, AI-clip line).
- **Blotato (Sun Oct 25 2026, 14:00Z = 9 AM CDT):** Facebook `5046547`, Instagram @danrosefit `5046548` (thumbnail as cover), TikTok `5046549` (cover-first copy, `videoCoverTimestamp: 0`, AI label on), YouTube `5046550` (public release, thumbnail URL set, synthetic media on). Verified on a fresh pull, 0 problems; queue 137 of 200.
- **AI flag on:** three realistic AI clips of people (1:42, 6:54, 7:53), each labelled on screen.
- **Media:** Blotato copy 230,456,780 bytes (h264_videotoolbox 4 Mbps at nice 20, audio stream-copied; 16,526 frames and 25,849 audio packets, same as the master), MD5 `d12537a1…`; TikTok copy 230,606,320 bytes (16,527 frames, audio packets unchanged, cover match 50.5 dB), MD5 `f49c4a27…`; thumbnail MD5 `08b58d6c…`. Every uploaded and re-hosted file matched.
- **Delivery gate:** the known FAIL stamp (gate 2.4.0) did not block any setup script.
- **Edit queue:** RO-12 `uploaded`; new job SL-06 (shorts from this video) added, `ready`.
- **Owed after Oct 25, on the public video:** upload `Top 5 Zepbound Tips.srt` as English captions (Studio, Subtitles, Upload file); publish `sixpackabs/articles/TBD-top-5-zepbound-tips.md`; add the WATCH NEXT card to "How To Keep Your Muscle On Zepbound" (RO-01) once RO-01 is public (lower third at 8:23 names it).
