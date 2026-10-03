# Studio posts queue receipt, 2026-10-03

Executed `Handoffs/handoff-20261003-approved-studio-posts-27-blotato.md` (approved by Dan 2026-10-03). Organic feed photos and carousels only; Instagram @danrosefit (67203) and Facebook Page Abs by AI (47105, page 1294282227094660). Retired @abs.by.ai (65632) not used.

## Result

- **27 editorial posts approved, 51 images, 54 platform placements planned.**
- **40 of 54 placements queued:** all 27 Instagram placements and 13 of 27 Facebook placements.
- **14 Facebook placements NOT queued.** Blotato refused the 41st write: `422 code 20010: maximum number of scheduled posts (200) for your plan`. The queue went 160 to 200. Nothing was deleted or moved to make room; capacity is not purchased.
- Still to queue (Facebook, in plan order): S07-B, S04-B, S06-B, S09-B, S01-B, S06-C, S04-C, S07-C, S01-C, S05-C, S09-C, S02-C, S08-C, S03-C. Their planned slots are in `scripts/blotato/studio27_plan.json`. Resume with `python3 scripts/blotato/studio27_queue.py create` once the queue has room (it frees one slot per post published; IG posts in the queue publish from Oct 3 on). Slots not yet used will need re-planning if their date passes: rerun `plan` first.

## Method

- Manifest validated: `posts.json` SHA256 matches; all 51 local JPEGs match manifest hashes; captions in the queue equal the manifest captions exactly (no title prefix, no first comment, no link, no hashtags added).
- Each JPEG uploaded once to Blotato storage and re-downloaded: bytes SHA256-match the approved file.
- Slots: Mon/Wed/Fri 5:00 PM America/Chicago (22:00Z before Nov 1, 23:00Z after), earliest days with no existing post on that account. Rotation: manifest's 27-post order (Block A, B, C). Instagram's free M/W/F days begin Oct 26. Facebook's M/W/F days are all occupied through Jan 1 2027, so Facebook starts Jan 4 2027. Result: IG and FB do NOT share dates for this batch (no same-date pairing was possible without moving existing posts).
- Singles are plain feed photos; the six carousels (S07-A/B/C, S08-A/B/C) are one post per platform with five images in order. No mediaType (no Reel/Story). Ad guard ran before (160 clean) and after (200 clean); each payload was checked with `assert_organic`.

## Verification (server state re-read after writes)

- All 160 original items unchanged (time and draft identical).
- 40 new items: correct account, scheduled time, caption, platform and target; media count and order match; every re-hosted image SHA256 equals the approved file.
- No duplicate account/time photo slots.
- Before snapshot: `scripts/blotato/studio27_queue_before_20261003.json`; after: `studio27_queue_after.json`; per-item check: `studio27_verified.json`; state: `studio27_state.json`.

## Placements

| Post | Title | Account | Local time | UTC | Schedule ID | Submission ID | Images |
|---|---|---|---|---|---|---|---|
| S01-A | Put your workout on the calendar | Instagram @danrosefit | 2026-10-26 17:00 CT | 2026-10-26T22:00:00.000Z | 5119908 | 49283163-dc53-4e6e-a238-a0ed2548b8ce | 1 |
| S07-A | YOUR NEXT
7 DAYS. | Instagram @danrosefit | 2026-10-28 17:00 CT | 2026-10-28T22:00:00.000Z | 5119909 | 9555821d-d8d5-4db7-b07f-c879ef064dfa | 5 |
| S03-A | The workout starts before you arrive | Instagram @danrosefit | 2026-10-30 17:00 CT | 2026-10-30T22:00:00.000Z | 5119910 | bef91730-c76b-4b31-994e-628a5236da94 | 1 |
| S06-A | TOO BUSY
TO TRAIN? | Instagram @danrosefit | 2026-11-02 17:00 CT | 2026-11-02T23:00:00.000Z | 5119911 | fe4cd978-7081-41e8-9bdf-0daa44e2dd4b | 1 |
| S02-A | Make lunch the easy decision | Instagram @danrosefit | 2026-11-04 17:00 CT | 2026-11-04T23:00:00.000Z | 5119914 | 9fb885b8-722e-4b1c-ba61-c76c54cc16c7 | 1 |
| S08-A | I need a free hour. | Instagram @danrosefit | 2026-11-06 17:00 CT | 2026-11-06T23:00:00.000Z | 5119916 | db444c27-5644-4fdb-a441-07916b3dc262 | 5 |
| S04-A | Choose a place you want to train | Instagram @danrosefit | 2026-11-09 17:00 CT | 2026-11-09T23:00:00.000Z | 5119919 | 6bf1477a-4bc0-434d-804d-6a3d4bf94edd | 1 |
| S05-A | MAKE TIME | Instagram @danrosefit | 2026-11-11 17:00 CT | 2026-11-11T23:00:00.000Z | 5119921 | 98d44d7c-7053-435b-9600-b560281d1abb | 1 |
| S09-A | MAKE TIME.
GET STRONG. | Instagram @danrosefit | 2026-11-13 17:00 CT | 2026-11-13T23:00:00.000Z | 5119924 | 7a8ef434-0b98-44f1-916d-1235c41e59a4 | 1 |
| S03-B | A plan that fits your life | Instagram @danrosefit | 2026-11-16 17:00 CT | 2026-11-16T23:00:00.000Z | 5119926 | d71d186d-06ed-4286-bd9e-8f7c06804d37 | 1 |
| S08-B | Every meal must be different. | Instagram @danrosefit | 2026-11-18 17:00 CT | 2026-11-18T23:00:00.000Z | 5119927 | c40a5d1a-fcb9-46eb-b46a-50b424c3c136 | 5 |
| S02-B | Fewer food decisions | Instagram @danrosefit | 2026-11-20 17:00 CT | 2026-11-20T23:00:00.000Z | 5119929 | 9fbd50ff-3cd0-403a-8772-eb44909bcfa7 | 1 |
| S05-B | FEWER DECISIONS | Instagram @danrosefit | 2026-11-23 17:00 CT | 2026-11-23T23:00:00.000Z | 5119930 | c2fc1797-145f-4d1c-85c8-b30958e9448b | 1 |
| S07-B | LUNCH,
PLANNED. | Instagram @danrosefit | 2026-11-25 17:00 CT | 2026-11-25T23:00:00.000Z | 5119932 | 559d084e-4953-4a4f-ac1d-25e4b936decb | 5 |
| S04-B | Sort dinner before you head out | Instagram @danrosefit | 2026-11-27 17:00 CT | 2026-11-27T23:00:00.000Z | 5119935 | d4f79096-bebf-4f41-9190-696c0697a1bf | 1 |
| S06-B | LUNCH.
SORTED. | Instagram @danrosefit | 2026-11-30 17:00 CT | 2026-11-30T23:00:00.000Z | 5119940 | a1964b74-e7a8-4165-854a-46afa2eb27a9 | 1 |
| S09-B | LUNCH.
HANDLED. | Instagram @danrosefit | 2026-12-02 17:00 CT | 2026-12-02T23:00:00.000Z | 5119942 | 54dbf734-25ab-4f15-ab84-55fedbe96632 | 1 |
| S01-B | Make the next meal easier | Instagram @danrosefit | 2026-12-04 17:00 CT | 2026-12-04T23:00:00.000Z | 5119943 | 0aecbe88-922d-40dd-849a-a4ab95752532 | 1 |
| S06-C | MISSED
A DAY? | Instagram @danrosefit | 2026-12-07 17:00 CT | 2026-12-07T23:00:00.000Z | 5119944 | a7748c53-cd9c-460b-ac03-c656272f9139 | 1 |
| S04-C | Train martial arts. Lift weights too. | Instagram @danrosefit | 2026-12-09 17:00 CT | 2026-12-09T23:00:00.000Z | 5119945 | 03b6244a-755a-4d99-99e2-c16db8a36728 | 1 |
| S07-C | YOUR
PLAN B. | Instagram @danrosefit | 2026-12-11 17:00 CT | 2026-12-11T23:00:00.000Z | 5119946 | 07eabed8-884b-4d44-8e48-5743594e86ba | 5 |
| S01-C | Missed a day? Keep going | Instagram @danrosefit | 2026-12-14 17:00 CT | 2026-12-14T23:00:00.000Z | 5119947 | 5c15d15e-13a7-4c7a-8b6e-503e3b9d4373 | 1 |
| S05-C | START AGAIN | Instagram @danrosefit | 2026-12-16 17:00 CT | 2026-12-16T23:00:00.000Z | 5119948 | ecd1035a-1687-47f0-8935-88ccef6fd628 | 1 |
| S09-C | TRAIN HARD.
LIFT TOO. | Instagram @danrosefit | 2026-12-18 17:00 CT | 2026-12-18T23:00:00.000Z | 5119950 | 58c7efad-0b7a-4a20-8288-794a24acb3ca | 1 |
| S02-C | Give the week a second chance | Instagram @danrosefit | 2026-12-21 17:00 CT | 2026-12-21T23:00:00.000Z | 5119952 | cc63b01c-f088-48d1-98a0-331bc48c635e | 1 |
| S08-C | I missed Monday. | Instagram @danrosefit | 2026-12-23 17:00 CT | 2026-12-23T23:00:00.000Z | 5119953 | 9ab4fa73-8c9a-4548-b4fb-8c23325ee789 | 5 |
| S03-C | Your next session still counts | Instagram @danrosefit | 2026-12-25 17:00 CT | 2026-12-25T23:00:00.000Z | 5119955 | bd1f3595-9c91-4f5b-9d27-5dba526788ce | 1 |
| S01-A | Put your workout on the calendar | Facebook Abs by AI | 2027-01-04 17:00 CT | 2027-01-04T23:00:00.000Z | 5119956 | 1bedd27b-ea5a-4cdc-abe9-809b062c88b0 | 1 |
| S07-A | YOUR NEXT
7 DAYS. | Facebook Abs by AI | 2027-01-06 17:00 CT | 2027-01-06T23:00:00.000Z | 5119958 | 406a9083-42fa-4f39-abd8-2ea5cba683ca | 5 |
| S03-A | The workout starts before you arrive | Facebook Abs by AI | 2027-01-08 17:00 CT | 2027-01-08T23:00:00.000Z | 5119960 | 895a2f65-9993-4f68-92f1-84b6849c96bf | 1 |
| S06-A | TOO BUSY
TO TRAIN? | Facebook Abs by AI | 2027-01-11 17:00 CT | 2027-01-11T23:00:00.000Z | 5119961 | 5493afc2-bfa5-4e1b-aeaa-d9657f20c23c | 1 |
| S02-A | Make lunch the easy decision | Facebook Abs by AI | 2027-01-13 17:00 CT | 2027-01-13T23:00:00.000Z | 5119962 | 21c20aa0-d314-4a7b-88d2-35948c6d6e9e | 1 |
| S08-A | I need a free hour. | Facebook Abs by AI | 2027-01-15 17:00 CT | 2027-01-15T23:00:00.000Z | 5119963 | a0fa5dc9-47ab-4774-a5d3-7a803e809371 | 5 |
| S04-A | Choose a place you want to train | Facebook Abs by AI | 2027-01-18 17:00 CT | 2027-01-18T23:00:00.000Z | 5119964 | 3129a5d4-eba9-4700-903a-b561099bbdb5 | 1 |
| S05-A | MAKE TIME | Facebook Abs by AI | 2027-01-20 17:00 CT | 2027-01-20T23:00:00.000Z | 5119965 | 7eb221f6-b13e-4836-9d45-a9f5f8cdb05c | 1 |
| S09-A | MAKE TIME.
GET STRONG. | Facebook Abs by AI | 2027-01-22 17:00 CT | 2027-01-22T23:00:00.000Z | 5119966 | fc6b0d55-761e-430c-85a3-219b7fec1574 | 1 |
| S03-B | A plan that fits your life | Facebook Abs by AI | 2027-01-25 17:00 CT | 2027-01-25T23:00:00.000Z | 5119967 | 227354c2-e25f-4bc4-96bc-cc6ca1a52c8f | 1 |
| S08-B | Every meal must be different. | Facebook Abs by AI | 2027-01-27 17:00 CT | 2027-01-27T23:00:00.000Z | 5119969 | d8fe6d33-5743-40eb-a525-5ec86fc73372 | 5 |
| S02-B | Fewer food decisions | Facebook Abs by AI | 2027-01-29 17:00 CT | 2027-01-29T23:00:00.000Z | 5119970 | 650e1128-c94f-4921-9e6b-2d35fc815688 | 1 |
| S05-B | FEWER DECISIONS | Facebook Abs by AI | 2027-02-01 17:00 CT | 2027-02-01T23:00:00.000Z | 5119973 | 84c5fd06-1096-49eb-9a8c-9d706065c6b1 | 1 |
| S07-B | LUNCH,
PLANNED. | Facebook Abs by AI | 2027-02-03 17:00 CT (planned) | 2027-02-03T23:00:00.000Z | NOT QUEUED (cap) | | 5 |
| S04-B | Sort dinner before you head out | Facebook Abs by AI | 2027-02-05 17:00 CT (planned) | 2027-02-05T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S06-B | LUNCH.
SORTED. | Facebook Abs by AI | 2027-02-08 17:00 CT (planned) | 2027-02-08T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S09-B | LUNCH.
HANDLED. | Facebook Abs by AI | 2027-02-10 17:00 CT (planned) | 2027-02-10T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S01-B | Make the next meal easier | Facebook Abs by AI | 2027-02-12 17:00 CT (planned) | 2027-02-12T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S06-C | MISSED
A DAY? | Facebook Abs by AI | 2027-02-15 17:00 CT (planned) | 2027-02-15T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S04-C | Train martial arts. Lift weights too. | Facebook Abs by AI | 2027-02-17 17:00 CT (planned) | 2027-02-17T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S07-C | YOUR
PLAN B. | Facebook Abs by AI | 2027-02-19 17:00 CT (planned) | 2027-02-19T23:00:00.000Z | NOT QUEUED (cap) | | 5 |
| S01-C | Missed a day? Keep going | Facebook Abs by AI | 2027-02-22 17:00 CT (planned) | 2027-02-22T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S05-C | START AGAIN | Facebook Abs by AI | 2027-02-24 17:00 CT (planned) | 2027-02-24T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S09-C | TRAIN HARD.
LIFT TOO. | Facebook Abs by AI | 2027-02-26 17:00 CT (planned) | 2027-02-26T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S02-C | Give the week a second chance | Facebook Abs by AI | 2027-03-01 17:00 CT (planned) | 2027-03-01T23:00:00.000Z | NOT QUEUED (cap) | | 1 |
| S08-C | I missed Monday. | Facebook Abs by AI | 2027-03-03 17:00 CT (planned) | 2027-03-03T23:00:00.000Z | NOT QUEUED (cap) | | 5 |
| S03-C | Your next session still counts | Facebook Abs by AI | 2027-03-05 17:00 CT (planned) | 2027-03-05T23:00:00.000Z | NOT QUEUED (cap) | | 1 |

## Media URLs in order

Per placement, in `scripts/blotato/studio27_verified.json` (slide order preserved).

