# Jiu Jitsu And Battle Ropes SFC Setup receipt

Updated: 2026-11-13, setup completion by Codex

Status: COMPLETE. Approved HQ masters and covers filed/backed up, metadata and pinned questions saved, all eight platform assets uploaded and downloaded/hash-verified. Both complete Shorts are on the shared waiting list with readback: Battle Ropes January 7, 2027 at 6 PM Central; Jiu Jitsu January 9 at 9 AM Central. These are planned waiting-list dates, not live Blotato schedules. The existing top-up routine owns scheduling.

Review: http://127.0.0.1:8994/

## Delivery check

At the November 2 check, read Muhammad's Upwork room through the connected client account, including the latest messages. The latest message was Dan's November 2, 2026 request at 4:53 PM Central: “Jiu Jitsu and Battle Ropes are both FINALIZED, so please send me the high quality exports of those two.” No later HQ delivery reply was present on the final check.

Listed the actual link-shared HD folder, `1KnomsobnLWvIJISKk4qNoGuXk5WDwrHE`. The listing returned 16 known HD files as a positive control, but neither DS-15 nor DS-19. Snapshot: `Short-form video content/covers/review/jiu-jitsu-battle-ropes-20261102/hd-folder-snapshot.tsv`. Also inspected the Jiu Jitsu supporting-assets folder. Targeted Drive search returned no video results and was not used as evidence that no delivery exists.

Direct metadata reads confirm the existing linked V2 files are the small review copies: 18,487,746 bytes (Jiu Jitsu) and 18,487,815 bytes (Battle Ropes). No HQ file was downloaded or incorrectly filed as final.

| Job | Approved local V2 baseline | MD5 | Video |
|---|---|---|---|
| DS-15 | `/Volumes/Extreme/_edit_work/revisions-20261101/muhammad/dl/ds15_jiujitsu_v2.mp4` | `0919c05e38d83de89b403d7226b0a50d` | 44.911542 s; 1346 frames; 1080x1920; 30000/1001 fps |
| DS-19 | `/Volumes/Extreme/_edit_work/revisions-20261101/muhammad/dl/ds19_ropes_v2.mp4` | `f0492615182b8aa34241ccc43afbb0a4` | 44.811438 s; 1343 frames; 1080x1920; 30000/1001 fps |

The local baselines were hash-checked against the handoff. Their saved final-file transcripts establish ORGANIC dedicated Shorts. Jiu Jitsu closes with nutrition and jiu jitsu as a bonus; Battle Ropes asks viewers for their favorite way to use battle ropes. No button CTA. Preserve both accepted cuts, including Dan's accepted Jiu Jitsu label and Battle Ropes framing/fades. No changes to the approved films.

At the November 2 setup phase, HQ comparison could not run because the files were missing. On November 3, Claude downloaded both HQ exports and recorded matching duration/frame count plus picture-difference checks in the setup handoff. This duplication audit did not rerun those checks. Audio review remains numerical only; no audible listening claim.

## Covers

Built five standard distinct designs per Short plus three comparison choices per Short, displayed together as X1 to X8 in a separate shuffle per Short. Source identities stay private. Every choice has Instagram and YouTube layouts, plus an Instagram 3:4 profile crop. Dan approved Jiu Jitsu X3 and Battle Ropes X8 with text revision V3 in the Claude setup chat, as recorded below.

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

## Previous remaining work (closed November 13, see completion below)

1. DONE: picks recorded (above). Was: record Dan's X pick for each Short with his words and the actual final asset hashes. Use `.claude/skills/_shared/blind-image/blind.py pick` for generated choices; the private key maps the chosen X to its original paired layouts. Requested revisions require showing the changed exact files before installation.
2. DONE by Claude on November 3: HQ exports received and compared against V2. Use the verified HQ paths and hashes from the original setup handoff; keep the editor's audio untouched. No new cover generation or choice request is needed.
3. File verified masters per the original handoff, project + Extreme + anyone-with-link Google Drive. Finish metadata, pinned question, platform media and cover upload/readback.
4. Use the dated release-phase/calendar rules. Both films are pool/patio, not kitchen. Battle Ropes fits the January home-cardio phase. Only reserve a real slot once full setup is ready, then Blotato or shared waitlist with readback. Do not claim a date now. Do not create a per-video automation.
5. Mark uploaded only after the required queue readback; update this receipt and close the existing handoff when setup is complete. Shorts articles and public cover/pinned-comment checks belong to the existing shared routines after release.

No new external message, paid image API call, upload, schedule or waitlist entry was made in this phase.

## Duplication audit, November 3, 2026

Read the actual Claude conversation logs. The chat titled “Jiu Jitsu and Battle Ropes SFC setup” (session `b982f8a1-b8bc-49a0-aceb-691b2789a1df`) received the same setup prompt on November 2. It explicitly reused this Codex chat's existing cover set, generated no duplicate cover set, recorded Dan's X3/X8 picks, built the requested Battle Ropes title variations and recorded his V3 approval. Its final response at 5:36 PM Central said queueing was still waiting on the HQ exports.

The separate Claude chat “Revisions review” (session `a7b901b0-481b-4354-b22d-c12486b330f1`) downloaded the HQ exports and recorded its matching-cut checks on November 3, completing its response at 9:05 AM Central. It explicitly directed the existing Codex setup chat to finish setup using the updated handoff.

The two setup chats overlap, but the initial cover images were not generated twice. Cover picks and the later HQ checks are already complete. No DS-15 or DS-19 config, waiting-list entry or completed scheduling record was found in the project setup records during this audit. Live Blotato was not queried. Continue only the remaining filing, backups, packaging and queue work using the approved covers and verified exports.


## Setup completion pass, November 13, 2026 (Codex)

**COMPLETE, waiting-list readback recorded below.** Dan explicitly authorized finishing both previously approved films and covers without new picks.

### DS-15 Does Jiu Jitsu Get You Abs?

- Project master: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/Does Jiu Jitsu Get You Abs? - DS-15/Does Jiu Jitsu Get You Abs? | muhammad | 9x16 | V2 HD.mp4`
- Extreme master: `/Volumes/Extreme/Short-form video content/Does Jiu Jitsu Get You Abs? - DS-15/Does Jiu Jitsu Get You Abs? | muhammad | 9x16 | V2 HD.mp4`
- Master MD5 `aa5d5a216c1ddf34c288978f1645a1fc`, SHA-256 `a0779c2c82f45dce9eca6ee4fb8a97461f75f30a867b77e7f8452853bbc359a5`, 120,772,677 bytes. Both filed copies match the accepted HQ export. Approved V2 baseline MD5 rechecked too; inherited November 3 HQ comparison has matching frame count/duration and only encoding differences. No film changes.
- Public Drive backup: https://drive.google.com/open?id=1pzpkz25qCB-BEcsCKSRJRG6BhFnowMzA. `rclone link` enabled anyone-with-link access; checksum readback passed for the initial master/transcript backup. Metadata and approved covers also copied. Final folder checksum readback recorded below.
- Approved cover originals copied unchanged to `Short-form video content/covers/approved-ds15/instagram.png` and `youtube.jpg`; Facebook repo/live installers receive those same approved Instagram pixels.
### DS-19 How To Use Battle Ropes

- Project master: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/How To Use Battle Ropes - DS-19/How To Use Battle Ropes | muhammad | 9x16 | V2 HD.mp4`
- Extreme master: `/Volumes/Extreme/Short-form video content/How To Use Battle Ropes - DS-19/How To Use Battle Ropes | muhammad | 9x16 | V2 HD.mp4`
- Master MD5 `572d9a53f05293afd6f36483ba40e354`, SHA-256 `ff5e92b6248b5e00c0aa8ab73ff28d35c1846a2ec159f5d743e7932d8ea17468`, 61,594,872 bytes. Both filed copies match the accepted HQ export. Approved V2 baseline MD5 rechecked too; inherited November 3 HQ comparison has matching frame count/duration and only encoding differences. No film changes.
- Public Drive backup: https://drive.google.com/open?id=1N8TZDQm9YShcRhT0krESelxDP3ym51Fj. `rclone link` enabled anyone-with-link access; checksum readback passed for the initial master/transcript backup. Metadata and approved covers also copied. Final folder checksum readback recorded below.
- Approved cover originals copied unchanged to `Short-form video content/covers/approved-ds19/instagram.png` and `youtube.jpg`; Facebook repo/live installers receive those same approved Instagram pixels.

Classification: organic from the saved final transcript. DS-15 closes: "So if you want abs, focus on your nutrition. But if you love jujitsu, burning extra calories and getting in a great ab workout is a good bonus to the sport." DS-19 closes: "Leave me a comment below to let me know your favorite way to do battle ropes." No button CTA. Silent still inspection shows real pool/patio, exercise and stock footage; upload AI flags OFF, AI cover artwork alone does not trigger them.

Metadata was written through the clean `scripts/voice/write.py` workflow from the final transcripts, not invented content. Full final transcripts and YouTube descriptions filed beside each master. Editor audio and picture retained unchanged. No separate editor SRT was supplied; subtitles are burned into the approved films. Audio review remains the inherited numerical-only check, with no audible-listening claim.

Shorts articles are handled by the existing post-release article routine. Actual public cover checks and pinned questions remain with the existing shared release routines; queued cover URLs are not proof of public tiles. No new per-video automation or external message.


### Final readback, November 13

| Job | Approved cover | Shared waitlist plan (Central) | Config |
|---|---|---|---|
| DS-19 | X8 text V3 | Thu January 7, 2027, 6 PM | `scripts/blotato/configs/ds19-battle-ropes.json` |
| DS-15 | X3 (design A) | Sat January 9, 2027, 9 AM | `scripts/blotato/configs/ds15-jiu-jitsu-abs.json` |

Both `kind: short`, `kitchen: false` entries were read back from `scripts/blotato/video_waitlist.json`. Configs carry all four platform targets through the normal helper. Chosen January slots were free in the live queue and waiting configs and fit the January fitness phase. Queue now 181/200; the 19 open slots are consumed by older pending entries in the normal top-up preview, so these new jobs retain their place in the shared waiting list. No direct scheduling jumped older entries.

All four platform cover preflights PASS for each Short; both normal `organic_short_queue.py` dry runs show four creates, no clash, no cap issue. YouTube covers 345,131 / 316,244 bytes, under 2 MB; approved image URLs and exact download SHA-256 values are retained in the config and machine receipt. Facebook images are installed in both registries with the exact caption first line and approval/hash.

TikTok full-file checks: DS-15 1,346 original frames + 1 cover frame = 1,347; 2,106 audio packets unchanged; cover PSNR 48.86 dB; zero decode errors. DS-19 1,343 + 1 = 1,344; 2,101 audio packets unchanged; cover PSNR 51.08 dB; zero decode errors. Every audio packet SHA-256 equals the approved HQ original for both. The two verified derivative files were uploaded and fully downloaded/hash-checked too. The checks ran together in one admitted render-queue job, with no resource-gate bypass.

Final backups: each public Drive folder reports **six matching files, zero differences**. All six files also match project to Extreme by SHA-256. Files: master, transcript, metadata, YouTube description, Instagram cover, YouTube cover. No extra editor SRT was supplied.

- **DS19 pinned comment:** "Which do you like better, alternating waves or two arm slams?". Posts and pins automatically after release through the existing shared routine.
- **DS15 pinned comment:** "How long have you been training jiu jitsu?". Posts and pins automatically after release through the existing shared routine.

Article: dedicated Shorts require no setup draft; the existing post-release article routine writes a searchable article or records a skip. Actual public thumbnails, pinned questions and articles remain release-time checks.

Machine verification receipt: `Docs/DS15_DS19_SETUP_VERIFICATION_20261113.json` (all eight asset URLs, sizes and SHA-256 values, master hashes, packet verification and cover-first checks). Post-write queue audit: 181 schedules, ad guard CLEAN; cover audit has no issues. No film was re-edited, no cover was regenerated, no new approval was needed, no paid generation or new automation.

Final expanded-capacity top-up dry run preserved DS-19 Jan7 6PM and DS-15 Jan9 9AM Central, with no PROBLEM line and no re-slotting. Both jobs were set `uploaded` (rev5); RO-08 set `uploaded` (rev11) after its three live schedules read back. All three status-file uploads to Drive confirmed successful. Native artifact-db mirroring remains with the existing Claude bridge, as required for Codex updates.
