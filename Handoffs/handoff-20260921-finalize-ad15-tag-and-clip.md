# Handoff: finalize Ad 15 (AI tag + remove repeated goal image), then swap it live

Written 2026-09-21. Executor: Claude Opus 5, high effort. Read `.claude/skills/_shared/VIDEO-RULES.md` in full first.

## Goal
Dan declared Muhammad's Ad 15 ("I Was the Dad Who Swam in a T-Shirt") FINALIZED on 2026-09-21. The two changes still
needed are ours to make on Muhammad's 1080p export, not his. Deliver a finished master, then replace the older version
running in YouTube and Google Ads.

## Source
- Muhammad's final HD export (2026-09-21): Drive `1V1zsBIQn2XfhDhhJGSKA10F3tV2MQHYU`, 3:27.08, 1920x1080, 29.97 fps,
  about 10.5 Mbps, md5 `92dfae6e35b75379d64fcfe97b7eccb2`, -14.0 LUFS / -0.9 peak. A copy is at
  `/Volumes/Extreme/_edit_work/revisions-20260921/dl/ad15.mp4`.
- The folder copy `Muhammad Ad Videos/i was the dad who swam in a tshirt - ad 15/…ad 15.mp4` is the OLDER 09-16 file
  (md5 `90e71d56…`). It is what is live now. Do not build on it.

## The two changes
1. **3:19 - 3:21 (closing demo, prospect line):** the other man's AI after picture on the phone's "Download Your Future
   Self" screen has no label. Add the small AI-GENERATED tag. Copy the exact tag Muhammad used on Dan's goal image at
   2:28 - 2:31 (black rounded pill, bold white capitals, low right inside the picture). Measure it from that frame.
   It stays up the whole time the picture shows. Keep it off his face. Do not change which man is shown: the line is
   the viewer generating, so it is correctly the recording's man.
2. **About 2:31 - 2:35:** after the 2:23 demo pays off inside the phone, Muhammad inserted an "AI-generated video" clip
   of a hand holding a phone that shows Dan's goal image again. Dan wants the goal image to land once only. **Replace
   that span with camera scene**, meaning the matching talking-head picture under the same audio. Recover it from the
   raw shoot footage by audio cross-correlation (the `/shortad-from-longform` recovery method), matching Muhammad's
   grade and punch-in level on the neighbouring camera shots. Find the exact in/out frames first. If you can't recover
   a clean camera shot, stop and report to Dan. Do not substitute another insert.

## Rules
- Audio: carry Muhammad's audio untouched, bit-exact (memory `editor-audio-untouched`, `--verbatim` gate).
- Change only these two spans. Frame-diff everything else against the source. It must match apart from the two spans.
- Decode with `accurate_rnd`, keep BT.709 (memory `untagged-video-bt601-trap`). Match the source's bitrate and specs.
- No before picture may touch an after picture at either new cut.
- Do not upload anything Public. This is an AD: unlisted YouTube and Google Ads only, never organic.
- No em dashes in anything you write.

## Delivery
1. Replace the folder master with the new file (keep the 09-16 one alongside as `…ad 15 (09-16 superseded).mp4`).
2. Run `/ad-setup`'s version-replacement path. Upload unlisted and swap the Demand Gen ads now on `TqXD2dGgAPs`
   (ids in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, Ad 15 row). Record the new ids there. Do not delete the old video until
   the new ads are serving.
3. Send Dan a 10 s before/after of each changed span as proof.
4. If the Edit Queue page has an Ad 15 AV/AS job, the verticals should be built from this new master, not the 09-16 one.

## Done when
The new master is filed, the ads point at it, both spans are verified at full resolution, and this handoff's lines are
removed from `AI_COORDINATION.md` and `Handoffs/README.md`.
