# DS-49 Why I Stopped Drinking Coconut Water: cover review (2026-10-29)

Status: **awaiting Dan's pick.** Nothing uploaded or scheduled. Review page: http://127.0.0.1:9549/ (managed review service).

- Film: approved R2 master `Short-form video content/Coconut Water - DS-49/Coconut Water SFC R2 - complete Short.mp4`, SHA-256 40e0c4d5a2fd4f6daa8a31124b87da0e705120eff76045ef20eb30fc89d342b0 (project and Extreme copies match).
- Google Drive backup DONE: `gdrive:Short-form video content/Coconut Water - DS-49/`, mp4 md5 dd1f13c9ea8bfeb27c0834fe529ed909 and srt md5 693f80c60ed8e4c55d0d5ce93c8e502c match local; anyone-with-link folder https://drive.google.com/open?id=1Vpf09WxGyCKoGQJxpTLwfWpHGVvRmLnx
- Covers: five designs, same copy "Why I Stopped Drinking / Coconut Water". Codex subscription, gpt-6.1-sol high, 5 images (~145k Codex tokens). A/B/D/E AI Dan with the real identity reference + film pool frame; C real studio-blue-222 cutout over a Codex plate (person pixels preserved).
  - A AI Dan pouring coconut water into a trash can, yellow band (recommended). B coconut water vs red can, white/cyan Impact. C real studio photo, navy plaque. D pointing at sugar cubes, bottom title. E "no thanks" to a fresh coconut, white/gold serif.
- Checks: `scripts/covers/ds49-20261029/check.py` all pass (1080x1920, text off face/hair and person, Instagram 240-1680, YouTube JPEG < 2 MB); face sheet inspected, all five read as Dan.
- Files: `Short-form video content/covers/review/ds49-coconut-water-20261029/ds49/{instagram,youtube}/`, manifest `Short-form video content/covers/review/ds49-coconut-water-20261029/ds49/manifest.json`. Builder: `scripts/covers/ds49-20261029/`.
- Planned slot: **Mon Dec 21, 6 PM Central** (next free Short slot; Nov 23 is held for DS-84; 7 days after SL-19 coconut water Short on Dec 14).

Next after the pick: copy pick to `Short-form video content/covers/approved-ds49/` with picks.json + hashes, TikTok cover-first copy, Blotato media uploads, config `scripts/blotato/configs/ds49-coconut-water.json` (copy ds76), FB cover registry, cover_audit + ad_guard, then `organic_short_queue.py` or the shared waitlist if Blotato is full; receipt `Docs/DS49_SETUP_RECEIPT_<date>.md`.

## Round 2 (Dan, 2026-10-29)

Dan: "I like A, but it doesn't really make sense to pour this out in the trash. I want three new designs similar to A, but where I'm pouring out the coconut water into a sink. Make two of these designs in an outdoor kitchen and one in an indoor kitchen."
- Built F (outdoor kitchen by the pool, bottle into a steel sink, glass of ice water; recommended), G (outdoor kitchen under a pergola at golden hour, carton into a black sink, thumbs up), H (indoor white kitchen, farmhouse sink). All use A's yellow band and copy. 3 more Codex images (gpt-6.1-sol high), `generate-r2.sh`. check.py all pass; faces inspected.
- Review page (same link) now leads with F, G, H; round 1 kept below for reference. Still awaiting Dan's pick; nothing uploaded or scheduled.

**Picked 2026-10-29: G** ("Let's go with G. Install G on all platforms."). Setup: `Docs/DS49_SETUP_RECEIPT_20261029.md`.
