# RO-28 "Got Abs? You need to see this." slight re-edit: setup (thumbnail, upload, ads)

Updated: 2026-11-18. CONTENT (LFC). Edit owner: Claude (Opus 5.5 high), done. Setup owner: Codex (default, Dan 2026-11-07).

## Why this exists
Google Ads disapproved/limited the Zepbound engagement ads for RO-28 (yt:eLV6EluvyD0) for restricted drug terms. Dan, 2026-11-18: re-edit slightly so Google does not read it as the same video, give it the neutral title **"Got Abs? You need to see this."**, and keep every drug term out of the title, description, thumbnail and ad text. All 7 old ads were paused and removed from Google Ads the same day (record: `scripts/ads/api/dgen-ads/remove-eLV6EluvyD0-20261118.*.json`). Standing rule now in AGENTS.md: "Advertised videos: no Zepbound or GLP-1 imagery in title, description, thumbnail or ad text".

## Approved film (Dan approved 2026-11-18 on review page http://127.0.0.1:9931/)
- `/Volumes/Extreme/Claude Content Videos/Got Abs Zepbound reedit - RO-28 R1/Got Abs - You need to see this - RO-28 reedit R1.mp4`
- SHA256 `d0d0fdbdb0c55ac066116d27647aeed88990812f2cfa456844972a31d297d7bc`; 387,228,582 bytes; 1920x1080; 385.962 s; 11,567 frames; -14.2 LUFS, peak -1.5 dBFS. Never edit it.
- Same folder: SRT (timing identical to the old film), chapters, APPROVAL.json. Source master untouched (`c5886ad4...`). Work folder on the M2: `/Users/danielrose/Projects/_edit_work/RO-28-REEDIT/r1/`.
- Spoken "Zepbound" and in-film graphics are unchanged (rule covers metadata only). If Google flags the film itself, tell Dan.

## To do (all of it, in order)
1. **Chapters:** the chapters file still reads "Why I think ripped men should take Zepbound", "Why I'm staying on it for life", "How I take it". Rewrite neutral (no drug name, no "take it"); keep timestamps.
2. **Thumbnail:** five checked choices per `/youtube-packaging` rules (two AI Dan acting the topic, one real photo, two history-guided), headline built on "Got Abs?" style. **No Zepbound, GLP-1, needle, pen, vial, pill or pharmacy scene anywhere.** Stop for Dan's pick. Show the YouTube layout.
3. **Metadata:** title "Got Abs? You need to see this."; description, tags and hashtags with no drug names (no Zepbound, Tirzepatide, GLP-1, Ozempic, weight-loss drug). Pinned comment follows `Docs/PINNED_COMMENTS.md`, also neutral. sixpackabs.com article: new neutral title/slug, no drug terms.
4. **Release date:** Dan said "repost". The original is already public (Nov 18 9 AM). Long-form days Nov 22 and Nov 25 are taken, so propose the next free Blotato slot from `scripts/blotato/release_phases.py` and the live queue, then wait for Dan's date pick before scheduling. YouTube first, others next day at noon. Never upload Public yourself; Blotato creates the release.
5. **Ads:** once the new video is public, create the seven "AT ·" engagement ads (tier1, tier2, us, rmktg-site, rmktg-yt, us-rmktg-site, us-rmktg-yt) with neutral headlines, long headlines and descriptions. Check the live account for missing instances.
6. **The old public copy:** ask Dan whether to unlist or delete the original RO-28 YouTube video (duplicate content). Do not touch it before he answers. Its title and thumbnail may name the drug only because it is no longer advertised.
7. Backups (project, Extreme, Drive, checksummed), setup receipt, board entry.

## Dan's later instructions, 2026-11-18 (read first; they change steps 4 to 6)
- The old Zepbound video (eLV6EluvyD0) is now **Private** on YouTube (confirmed by API), its sixpackabs.com page is draft, and its three social schedules (Facebook 6213006, Instagram 6213007, TikTok 6213008, all Thu Nov 19 noon Central) were **cancelled** and saved in `output/social-engagement-20261117/ro28-cancelled-socials-20261118.json`. Nothing of the old video is left to schedule or advertise. Skip step 6's question: it is already private.
- Dan: **"Post the re-edited video instead."** So the re-edited film takes the cancelled slot: aim for YouTube as early as Dan's thumbnail pick allows (Thu Nov 19 9 AM Central is the target), and Facebook, Instagram and TikTok at Thu Nov 19 noon Central once the YouTube video is verified public (Dan's override of the usual next-day rule; if the YouTube copy is not public by noon, postpone the three). Confirm the slot is free in the live Blotato queue and `release_phases.py` before scheduling; only the thumbnail pick is still Dan's.
- The old page on sixpackabs.com is draft; the new video gets its own page when public (sync does it).

## Starter prompt and model
Model: Codex GPT-6.2 Sol, High. Start now (Dan approved the film).
```
Read Handoffs/handoff-20261118-ro28-got-abs-reedit-setup.md in the Abs By AI project and do the whole setup. Dan approved the re-edited film today; use the exact file and hash listed. Follow the standing rule that no Zepbound, GLP-1, needle, vial or pharmacy words or imagery appear in the title, description, chapters, thumbnail or ad text. Make the five thumbnail choices and stop for Dan's pick; propose release dates and stop for his pick; then upload, schedule through Blotato, build the seven engagement ads, back up and write the receipt.
```
