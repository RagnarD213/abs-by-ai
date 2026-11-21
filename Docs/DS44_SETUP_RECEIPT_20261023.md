# CONTENT: Hormozi Fat Guy SFC Setup

Updated: 2026-10-27. Job: DS-44 (+ DS-44B). Status: scheduled on all four organic destinations, **off-the-cuff R2 version**.

## 2026-10-27: off-the-cuff R2 swapped in (current)

Dan picked the off-the-cuff take, approved round 2 and said: "This is finalized... replace what we have in the queue with this."
- Film: `Short-form video content/Hormozi Fat Guy - DS-44/Hormozi Fat Guy Off-Cuff SFC R2 - complete Short.mp4`, 64.865 s,
  67,283,653 bytes, SHA-256 starts `eb63aaecc8c09c21` (1.135x, Codex titled panel; independent review SHIP). No AI footage:
  `ai_generated: false` (YouTube containsSyntheticMedia and TikTok isAiGenerated false), no AI line in any caption.
- TikTok cover-first copy: `... Off-Cuff SFC R2 - tiktok cover-first.mp4`, SHA-256 starts `fa22fcbe4090dab6` (1944 to 1945
  frames, 3041 audio packets unchanged, cover PSNR 49.3 dB).
- Same title, same approved covers (round 4 option 1), same slot **Thu Dec 17, 2026, 9 AM Chicago**. New copy (dan-voice-writer,
  matches what he says in this take), new pinned question: "When you eat, do you stop at the right point, or do you go a
  little bit too far?" Config `scripts/blotato/configs/ds44-hormozi-fat-guy.json` (scripted config backed up in
  `scripts/blotato/swap_backup/ds44-hormozi-fat-guy.scripted-r2.config.json`).
- Old schedules 5948215-5948218 backed up (`scripts/blotato/swap_backup/59482xx.ds44-scripted.json`) and deleted; new:

| Destination | Account | Saved schedule |
|---|---|---|
| facebook | 47105 | 6108255 (cover by installer; registry match updated to the new first line, repo + live copy) |
| instagram @danrosefit | 67203 | 6108259 |
| tiktok | 58181 | 6108260 (cover-first copy, timestamp 0) |
| youtube | 46963 | 6108262 |

- Read back: all four at 2026-12-17T15:00Z; each Blotato media copy downloaded and SHA-256 matched (master; TikTok copy);
  AI flags false; YouTube title and thumbnail kept. `ad_guard.py --scan` clean before and after. Queue 192 of 200.
- Backups: Extreme `/Volumes/Extreme/Short-form video content/Hormozi Fat Guy - DS-44/` (master hash matches, SRT, TikTok copy);
  Google Drive folder above (master MD5 matches, SRT).
- The scripted R2 stays filed, unqueued.

## Earlier record (scripted R2, superseded 2026-10-27)

**Version note (read first).** The setup handoff held installation until Dan chose between the scripted R2 and the
off-the-cuff take (DS-44B, still being edited). On 2026-10-23 Dan picked the cover and said: "Let's go with one. Go ahead
and finalize and install one." The scripted R2 is the only approved film, so it is what is queued. **If Dan later picks
the off-the-cuff version, swap the media on all four posts with `scripts/blotato/swap_media.py`** (rebuild the TikTok
cover-first copy from it, re-hash every per-post copy, set `ai_generated` from that cut: true only if it keeps A0197 or
other realistic AI footage) and update this receipt. Covers stay as they are: the cover works for either version.

## Approved cover

Round 4, option 1 (Dan: "Let's go with one"): design A (Hormozi on top, black band with yellow ALEX HORMOZI'S over white
WEIGHT LOSS MENTAL SHIFT, the caller below, shifted right) with Dan keyed small in the lower left, looking at the camera,
shocked, both hands out (keyed talking frame A394 of the approved R2, same corner scale as the film). Real frames, no AI.
Rounds: five Codex covers (rejected for a new brief), three split-screen designs (A picked), A with the looking-down corner
Dan (changed to camera-facing), two camera-facing variants (1 picked).

- YouTube: `Short-form video content/Hormozi Fat Guy - DS-44/covers/Hormozi Fat Guy - cover FINAL - youtube.jpg`,
  466,221 bytes, SHA-256 `8523a8f6b073571d6cdcc6d1a37caef6b897a0151d91653dca9d91f89a4ee057`.
- Instagram grid / Facebook: `... - cover FINAL - instagram.jpg`, 443,989 bytes, SHA-256 `98c649262e42cb072283e3f0e9f74e384c44cd60f334e4e39e0550d9d53a4cc0`.
- Build: `Handoffs/video-editing/DS-44-cover-review/build_a_corner.py A394` (uses `build_split.py`, `corner_dan.py`).

## Saved release

**Thursday, December 17, 2026, 9 AM America/Chicago** (`2026-12-17T15:00:00.000Z`), the first Thursday held by a not-yet-edited
DS; calendar updated (DS-13, DS-16 one Thursday later, DS-01 to Jan 7 2027). Queue 196 to 200 of 200.

| Destination | Account | Saved schedule | Cover |
|---|---|---|---|
| facebook | 47105 | 5948215 | instagram layout (repo registry + live installer `~/.absbyai/fb-reel-covers/covers/ds44-hormozi-fat-guy-cover-A1.jpg`) |
| instagram @danrosefit | 67203 | 5948216 | instagram layout |
| tiktok | 58181 | 5948217 | cover as frame 0, `videoCoverTimestamp: 0` |
| youtube | 46963 | 5948218 | youtube layout |

Title: **Alex Hormozi Asks A Fat Guy Why He Isn't 200 Pounds Heavier. He's Right.** (the cover text is "Alex Hormozi's Weight
Loss Mental Shift"; Dan was asked whether the title should change too and has not said; change it in schedule 5948218 before
Dec 17 if he does). Config: `scripts/blotato/configs/ds44-hormozi-fat-guy.json` (organic, exact source, `ai_generated: true`
for library AI clip A0197, keyword TRACK, UTM campaign `hormozi-fat-guy`). Copy by dan-voice-writer, no dashes.

## Verification

- Film: exact approved R2 master, 60,367,549 bytes, SHA-256 starts `9d8deb8da3d5eb2b`. Not re-rendered.
- TikTok copy (`tiktok_cover.build`): 1,835 to 1,836 frames, 2,871 audio packets unchanged, no decode errors, cover PSNR 48.9 dB;
  its uploaded frame 0 decoded and compared with the cover (mean difference 2.1 of 255). SHA-256 starts `d7212bd36ed2f2ea`.
- Uploads downloaded back and hash-matched (master, TikTok copy, both covers). Blotato's per-post media copies downloaded and
  hashed: YouTube, Facebook, Instagram equal the master; TikTok equals the cover-first copy.
- Read back: all four at 2026-12-17T15:00Z; YouTube title, cover URL and AI flag; TikTok AI flag and timestamp 0; Instagram cover.
- `ad_guard.py --scan` before and after: clean. `cover_audit.py` after: zero issues (queue check only, not public tiles).

## Backups

Extreme: `/Volumes/Extreme/Short-form video content/Hormozi Fat Guy - DS-44/` (master hash matches, SRT, final covers).
Google Drive (anyone with the link): https://drive.google.com/open?id=1A6ykI6tJj2tW2xfqnGABqAMWe7UqfBro (byte counts confirmed).

## Release follow-through

Pinned comment: "Do you weigh yourself every morning right now, or only once in a while?" Posts and pins automatically after
release (routine youtube-pinned-comment-daily).

Article: dedicated Short; handled after release by `sixpackabs-article-gap-daily` (article or recorded skip).

Public cover checks remain until release (existing `check-youtube-shorts-covers` monitor covers all four). A wrong YouTube tile
is fixed in desktop Studio, never by re-uploading.

Edit Queue: DS-44 `uploaded` (Drive status file and artifact db mirrored). Videos to Review copies of the scripted Short were
left in place because Dan still compares it with the off-the-cuff take (DS-44B); remove both once he picks.

Codex image use: round 1, 3 images (studio plate, AI Dan, Codex concept). No paid spend.
