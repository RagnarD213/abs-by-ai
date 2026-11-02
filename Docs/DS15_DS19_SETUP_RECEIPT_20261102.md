# Jiu Jitsu And Battle Ropes SFC Setup receipt

Updated: 2026-11-02 evening Central

Status: PARTLY DONE. Both covers picked: Jiu Jitsu X3, Battle Ropes X8 text V3. Waiting only on Muhammad's HQ exports (rechecked 2026-11-02 evening: no reply in Upwork room, nothing new in HD folder). Muhammad's two HQ exports are still awaited. Neither Short has been uploaded, queued, waitlisted or scheduled. DS-15 and DS-19 remain finalized, not uploaded.

Review: http://127.0.0.1:8994/

## Delivery check

Read Muhammad's Upwork room through the connected client account, including the latest messages. The latest message remains Dan's November 2, 2026 request at 4:53 PM Central: “Jiu Jitsu and Battle Ropes are both FINALIZED, so please send me the high quality exports of those two.” No later HQ delivery reply was present on the final check.

Listed the actual link-shared HD folder, `1KnomsobnLWvIJISKk4qNoGuXk5WDwrHE`. The listing returned 16 known HD files as a positive control, but neither DS-15 nor DS-19. Snapshot: `Short-form video content/covers/review/jiu-jitsu-battle-ropes-20261102/hd-folder-snapshot.tsv`. Also inspected the Jiu Jitsu supporting-assets folder. Targeted Drive search returned no video results and was not used as evidence that no delivery exists.

Direct metadata reads confirm the existing linked V2 files are the small review copies: 18,487,746 bytes (Jiu Jitsu) and 18,487,815 bytes (Battle Ropes). No HQ file was downloaded or incorrectly filed as final.

| Job | Approved local V2 baseline | MD5 | Video |
|---|---|---|---|
| DS-15 | `/Volumes/Extreme/_edit_work/revisions-20261101/muhammad/dl/ds15_jiujitsu_v2.mp4` | `0919c05e38d83de89b403d7226b0a50d` | 44.911542 s; 1346 frames; 1080x1920; 30000/1001 fps |
| DS-19 | `/Volumes/Extreme/_edit_work/revisions-20261101/muhammad/dl/ds19_ropes_v2.mp4` | `f0492615182b8aa34241ccc43afbb0a4` | 44.811438 s; 1343 frames; 1080x1920; 30000/1001 fps |

The local baselines were hash-checked against the handoff. Their saved final-file transcripts establish ORGANIC dedicated Shorts. Jiu Jitsu closes with nutrition and jiu jitsu as a bonus; Battle Ropes asks viewers for their favorite way to use battle ropes. No button CTA. Preserve both accepted cuts, including Dan's accepted Jiu Jitsu label and Battle Ropes framing/fades. No changes to the approved films.

HQ duration, frame/sampled-picture and audio comparison: NOT PERFORMED because the final HQ files are missing. Existing audio QA is numerical only; no audible listening claim.

## Covers

Built five standard distinct designs per Short plus three comparison choices per Short, displayed together as X1 to X8 in a separate shuffle per Short. Source identities stay private. Every choice has Instagram and YouTube layouts, plus an Instagram 3:4 profile crop. Dan has not picked or approved any cover yet.

Current source mix: two distinct topic-acting AI Dan concepts, one real studio photo, and two history-guided concepts, plus the three comparison designs. Inspected actual DS-01 and SL-08 picks and selected images before planning. The real-photo options retain original studio-white-23 and studio-white-49 person pixels, with resizing/compositing only. All generated Dan portraits used the real identity reference and were face-checked. Text is rendered locally in title capitalization. No website mark or real-photo label.

Review root: `Short-form video content/covers/review/jiu-jitsu-battle-ropes-20261102/blind-review/`.
Build/check/review scripts: `scripts/covers/ds15-ds19-20261102/`.
Prompts, design plan, source images, private blind keys and original final assets are retained under the ignored cover-review folder. Use the originals to install a picked cover, never a normalized blind copy. If the real-photo option is chosen, record it in the cover approval receipt and exclude it from model-comparison scoring.

Checks: all 32 finished covers are RGB 1080x1920, text bounds safe, one detected face, zero text overlap with expanded face/hair regions and zero text/person-mask overlap. All YouTube JPEGs are below 2 MB. Inspected the finished sheets and native face crops. Corrected the oversized real-photo crop before delivery. See each job's `cover-checks.json` and `face-check.jpg`.

Managed review service installed on port 8994, with 53 linked files cached locally. Browser opened and inspected; no horizontal overflow. All 52 image responses matched the local image bytes; range request returned 206. No video/audio player on this cover-only page, no playback. Screenshot: `Short-form video content/covers/review/jiu-jitsu-battle-ropes-20261102/review-page-screenshot.png`.


## Picks (2026-11-02)

- Jiu Jitsu: Dan, "Okay, for Jiu Jitsu, let's go with X3." X3 is design A. Final files: Instagram `ds15/instagram/ds-15_jiu-jitsu_cover-A.png` sha256 `a3955cbc91c34ac9147dbb9f5e2d9696401a9e6d43308ecd5983c761cfa480d3`; YouTube `ds15/youtube/ds-15_jiu-jitsu_cover-A.png` sha256 `b00ed65826c67e06ba486479047a73088f38c5ca47de58b59148dfe3a5b83da6` (plus its `.jpg`). Recorded with `blind.py pick`.
- Battle Ropes: Dan, "let's go with X8, but I want you to redo that text. It looks kind of weird how it's half in the black area, half not. Give me three variations with better-looking text on top." X8 is design H. Recorded with `blind.py pick`.
- Battle Ropes text options V1/V2/V3, same X8 picture moved down so the whole title sits inside the dark ceiling with 45 px or more of clear dark above the wall: V1 X8 look bigger, V2 small green kicker over large white line, V3 green block with dark type. One face, zero text-on-person pixels, Instagram grid-safe. Files: `ds19/x8-text-r2/` (manifest with hashes), builder `scripts/covers/ds15-ds19-20261102/x8_text_r2.py`. Review: http://127.0.0.1:8994/battle-ropes-x8/ . Install only the exact V file Dan picks.
- Battle Ropes final: Dan, "v3". Instagram `ds19/x8-text-r2/instagram/ds-19_battle-ropes_cover-X8-V3.png` sha256 `402685b09b74dfd337ff22446ee7294d9e1155b499734032ce52c45427547c3b`; YouTube `.../youtube/ds-19_battle-ropes_cover-X8-V3.png` sha256 `61002e7aa82e7a6d3a796f96ab55da832f216b979ade0551047badcf557ee01d`, JPEG `46a273e2106ae67b1318a6e17835737e8a05a9754c80dc2ed1a35be24c08aeed`.

## Remaining work

1. DONE: picks recorded (above). Was: record Dan's X pick for each Short with his words and the actual final asset hashes. Use `.claude/skills/_shared/blind-image/blind.py pick` for generated choices; the private key maps the chosen X to its original paired layouts. Requested revisions require showing the changed exact files before installation.
2. Recheck Muhammad's Upwork room and shared HD folder. Once finals arrive, download exact HQ bytes, compare duration/frame count and sampled frames against the approved baselines. A content difference stops setup for Dan. Keep the editor's audio untouched.
3. File verified masters per the original handoff, project + Extreme + anyone-with-link Google Drive. Finish metadata, pinned question, platform media and cover upload/readback.
4. Use the dated release-phase/calendar rules. Both films are pool/patio, not kitchen. Battle Ropes fits the January home-cardio phase. Only reserve a real slot once full setup is ready, then Blotato or shared waitlist with readback. Do not claim a date now. Do not create a per-video automation.
5. Mark uploaded only after the required queue readback; update this receipt and close the existing handoff when setup is complete. Shorts articles and public cover/pinned-comment checks belong to the existing shared routines after release.

No new external message, paid image API call, upload, schedule or waitlist entry was made in this phase.
