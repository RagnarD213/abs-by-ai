# Calories Not Losing Weight Shorts setup receipt, 2026-10-25

CONTENT (SFL), SL-08. **Setup prepared; five entries on the shared waiting list because Blotato has 197/200 posts and each Short needs four slots. No platform schedules have been created yet.** The existing daily top-up routine will queue them as capacity opens; no per-video automation was created. Do not call them scheduled until its four-destination readbacks exist.

Dan approved all five original R6 films on October 25, then chose **C for all five covers** and authorized January 4, 5, 8, 9 and 11, 2027, at 9 AM America/Chicago. These are the exact reviewed C files, with no revision or regeneration. Review archive: http://127.0.0.1:9250/ . All work stayed in the background.

## Release plan and current state

Every planned release is 9 AM Central (15:00 UTC), on YouTube, Facebook, Instagram @danrosefit and TikTok.

| Date in 2027 | Short | State |
|---|---|---|
| January 4 | Why I Fast Until 2 pm Every Day | Shared waitlist, four platform plans ready |
| January 5 | Eat a Salad First to Eat Less | Shared waitlist, four platform plans ready |
| January 8 | Stop Drinking Your Calories | Shared waitlist, four platform plans ready |
| January 9 | Snack on Protein, Not Carbs | Shared waitlist, four platform plans ready |
| January 11 | Make Fasting Easier With Black Coffee | Shared waitlist, four platform plans ready |

The live parent schedule 5287937 was freshly read back as December 27, 2026, 9 AM Central (`2026-12-27T15:00:00.000Z`), YouTube account 46963, with the correct replacement title/media. No parent schedule was changed. Its local config's stale October date was corrected to the live December date so the Shorts' `parent_config` and `after` dependency use the right date. The old YouTube `n_E94JrCKGg` remains Private; no public replacement existed at setup, so descriptions name the parent title without inventing a watch URL.

## Storage and exact files

[Google Drive final backup](https://drive.google.com/open?id=1JSjUUWrHfBXspr3Ek8rMmVPUwlgF_Dob), anyone with the link. All five masters, five per-Short SRTs, ten approved cover images and the pick record were checked by byte count and Drive MD5 against the project files: 21 matching files, zero differences. An unauthenticated ranged download returned HTTP 206, video/mp4 and a valid video header. Project and final Extreme copies of the same 21 files were also SHA-256 checked. Setup evidence is stored alongside the films in `setup records/` and backed up separately.

Subtitle sidecars were exported from each exact Short's delivered cue map, not the parent's SRT. Masters were not re-edited, re-rendered or audio-processed; existing exact-file approval, audio and delivery stamps remain locked. TikTok derivatives prepend one approved cover frame, preserve original AAC payloads exactly, decode cleanly and have precisely one extra video frame. All five actual first frames were inspected; measured cover PSNR was 47.51 to 48.50 dB.

| Short | Master bytes | Approved master SHA-256 |
|---|---:|---|
| 1 | 65786638 | `f8a1ff8a1574542dd380bcdb29eb298d2d060e3a4a82b8987c2aad3c48b39eed` |
| 2 | 127066185 | `4f3bb0e411aef33afddb45dbc5932d32c3c5602f3c3a36f976c8a8eb3663f01e` |
| 3 | 131694826 | `72c98cc9bb88ce9826391659c7f1dcf52c076bececa85502c9a0e91216c0edae` |
| 4 | 77017594 | `28762ad176e04aa8e644e0c03b5df9b8d630982a8b1c06563ed0e53dbb87f6c0` |
| 5 | 85268591 | `99dbc301401f3eb98e6aff6200f9b97dc3459621f7bd4bdf92c283f9b69d4ddf` |

## Approved cover hashes

Instagram PNGs and YouTube JPEGs were copied byte-for-byte from the reviewed exports. Each actual YouTube JPEG is below 2 MB. All 20 media/cover files were uploaded to Blotato storage, downloaded and SHA-256 verified. Files are under `Short-form video content/covers/approved-sl08/`; no rejected or superseded video was used.

| Short | Instagram PNG SHA-256 | YouTube JPEG SHA-256 |
|---|---|---|
| 1 | `e74c15b6b77520abdc4c76e0981df4603e9f38a17233250de87338f5a89cb4e9` | `44c0ad899d61850eb5984ca1ee3a4575b381759b8bb196311f5f407acf5b6cf0` |
| 2 | `fae3894673c4c7156d27d3190fdae85b5072547c191493579b9fe2758dc541c2` | `dd011bfea927084e75830979a23336c49d389307164ff7194c16bd68d65af7dd` |
| 3 | `b663bcde21d1c795467a1405bac84cde9828c47170a2e9e2ece68fc9eda870de` | `a78940d292908e3e151f28a6f97ccd99ebd7c10dc2e2f89a71cfe6ced8916987` |
| 4 | `b97505adef7f38ee1bbbf7ab552323c05852bbbee66dea645bfe439fc6770d50` | `8880787717c0399d8fc1dab6aa580dd122b136058ccc4e0dba8bc1e540202103` |
| 5 | `3bc3c1cda5a39bc3cf8bdfa7ab87465edbbc1d9421d73e448137ed456e46909c` | `f24ca5d09b37ad7247013059aa3294d9f1e1c96da7f39f545426cabfc1ab1d66` |

## Packaging and platform preflight

Five configs in `scripts/blotato/configs/sl08-short<N>-<title-slug>.json` carry organic classification, the exact absolute approved master source, title, short-specific captions, FOOD keyword, platform UTMs to the homepage, pinned question, C cover URLs and hashes, TikTok cover-first media and parent dependency. All four destinations for all five passed the shared cover preflight. Facebook's five approved PNGs are in the repository registry and the live installer's registry with matching hashes; other entries were preserved. The live installer will apply covers after release.

AI video flags: Short 1 true for the approved realistic fasting opener; Shorts 2 through 5 false. Their generated covers do not make the underlying videos realistic AI footage. Classification was checked from each delivered-word ending: all teach the topic and none ends with a button CTA.

Pinned comments (prepared now; the existing youtube-pinned-comment-daily routine posts and pins after release):

- **Why I Fast Until 2 pm Every Day:** What time do you usually eat your first meal?
- **Eat a Salad First to Eat Less:** Would you rather start your meal with a salad or soup?
- **Stop Drinking Your Calories:** Which drink adds the most calories to your day?
- **Snack on Protein, Not Carbs:** Which protein snack do you like the most?
- **Make Fasting Easier With Black Coffee:** Do you drink your coffee black or add cream and sugar?

Article: Shorts need no setup draft. The existing article routine writes a useful short article or records a justified skip after release. No article is claimed published.

## Verified media URLs

### Why I Fast Until 2 pm Every Day

- [Master](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/7d95054d-edf5-41e9-a6cc-75697a206938.mp4)
- [TikTok cover-first copy](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/bf44e1c8-3330-4a9a-8b54-3acad224ae96.mp4)
- [Instagram/Facebook cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/2273b0ef-e6ea-484f-822b-c0db8bc0af19.png)
- [YouTube cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/e769998a-8a00-4eb3-9e9f-34c158b0b170.jpg)

### Eat a Salad First to Eat Less

- [Master](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/cedc6224-d1b7-4403-aae4-465579621301.mp4)
- [TikTok cover-first copy](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/dce22994-c8f3-48af-a0a5-365fcfdf21dd.mp4)
- [Instagram/Facebook cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/61269dea-52eb-4a70-841b-a79bebad321d.png)
- [YouTube cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/acc89509-6754-4ed0-aad9-1cb38c76134f.jpg)

### Stop Drinking Your Calories

- [Master](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/b8a4905a-cb7d-482d-ab19-424f58ebc639.mp4)
- [TikTok cover-first copy](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/352eb5ce-08ce-4c68-b39d-9984400dffbe.mp4)
- [Instagram/Facebook cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/f1b3e819-3510-4401-bc5f-cb625ed8c8d7.png)
- [YouTube cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/dcf61a9c-cc50-4955-a2a0-1706bc392651.jpg)

### Snack on Protein, Not Carbs

- [Master](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/587ab02a-abdd-472c-96a5-dab74635822b.mp4)
- [TikTok cover-first copy](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/e19ca687-ae05-4c8d-8145-9183f35f03fe.mp4)
- [Instagram/Facebook cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/dcdaedfb-bf5c-4a36-b9f0-8163a49c5b25.png)
- [YouTube cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/e9653d98-ddbf-4df8-8519-af6e1b4303f2.jpg)

### Make Fasting Easier With Black Coffee

- [Master](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/ada094b3-a1db-4da3-8dda-93abbef41cf9.mp4)
- [TikTok cover-first copy](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/b4246b6a-926d-4997-8ea1-aebf4f5647ca.mp4)
- [Instagram/Facebook cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/a38b4248-b506-4103-b703-3caed53bc253.png)
- [YouTube cover](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/99bc0ca0-c782-4117-b48e-af584ce874c7.jpg)

## Existing automatic follow-through and remaining checks

The five unique waitlist entries use `kind: short` and the verified parent dependency. Before reporting scheduled, re-read actual times, IDs, media and cover targets on all four destinations. Do not mark the edit job uploaded before those readbacks; it remains finalized while waiting. Parent public release must be verified after December 27. After each Short releases, actual public tiles on all four platforms decide cover success; queued URLs and preflights are not public-tile proof. Pinned questions and any applicable article remain post-release checks through the existing routines. No direct YouTube upload or native publishAt scheduling was performed. Victory Dashboard and the paused edit heartbeat were untouched.

## New default cover standard, requested by Dan October 25

Future five-choice cover/thumbnail sets require two distinct AI images of Dan in the topic, one real photograph from either the pool or studio shoot, and two Codex choices guided by actual selected-cover history. Additional AI Dan is allowed; object-only/no-Dan alternatives are not a quota. Five distinct designs and actual pick approval remain required. The rules are updated in AGENTS.md, VIDEO-RULES.md, IMAGE-GENERATION.md and the coverimage, youtube-packaging, video-setup and ad-setup skills, and pushed to GitHub. This round's C approvals were recorded as five more selected examples. No new images were generated for this setup phase.

Skill validation passed. Original 25-choice generation used the Codex subscription (543,246 reported Codex tokens), no paid image API. This phase reused those approved files. The Claude writing helper's OAuth session was expired; a clean writer using the same prepared real-passage prompt supplied the captions, then the exact transcripts and hard rules were checked. No new personal facts or claims were introduced.
