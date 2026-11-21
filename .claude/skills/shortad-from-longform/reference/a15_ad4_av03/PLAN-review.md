# Ad 4 "Stop Wasting Money On Supplements": 9:16 and 1:1, full length and 59 s. The plan the delivered files are held to.

Jobs AV-03 (vertical) and AS-02 (square), built together on 2026-10-03 (`Handoffs/handoff-20261001-ad4-other-formats.md`).
This is the plan. The reviewer reads this file, `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` and
`Handoffs/video-editing/00-RULES.md`. The reviewer does NOT read `notes*.md`, `logs/`, earlier audits or any editor file.

## 1. The files

| file (in `/Volumes/Extreme/_edit_work/AV-03/`) | size | frames |
|---|---|---|
| `ad4_9x16.mp4` | 1080x1920, 29.97 | 7,160 (= the reference, to the frame) |
| `cut/ad4_9x16_59s.mp4` | 1080x1920 | 1,714 (57.19 s, must be 59.0 s or under) |
| `ad4_1x1.mp4` | 1080x1080 | 7,160 |
| `cut_sq/ad4_1x1_59s.mp4` | 1080x1080 | 1,714 |

Reference (the editor's approved 16:9 master, the spec for cut, order, graphics text and audio):
`ref/ad4_v4_hd.mp4` (1920x1080, 7,160 frames, NO colour tags: decode it with
`-vf scale=in_color_matrix=bt709:in_range=tv` or its colour reads wrong).

## 2. What each file must be

1. **The same film as the reference, frame for frame on the timeline** (full lengths): same words, same order, his beat
   boundaries, his light-leak flashes, his lower thirds, numbered points, bullets, CTA pills, at his wording.
2. **Audio is his, untouched.** Full lengths carry his AAC stream bit for bit (compare the audio stream md5 with the
   reference). The 59 s cuts carry his mix cut at the seams only. His export peaks at -0.90 dBTP against our -1.0 dBTP
   rule; Dan accepted that audio on 2026-09-11 ("I think the audio sounded fine"), so the `tp` row of the audio stamp
   FAILS by design and is recorded as an exception. Any OTHER audio difference is a defect.
3. **Colour matches the reference as a player shows it** (BT.709 read). Compare skin and overall level on the same
   instants; the files are tagged BT.709.
4. **Talking head:** hair-anchored NEAR/FAR only, hair never touching the top edge, never a wide level; every visible
   same-scene cut carries a level change or an insert (no naked jump cut); in the 9:16 the crop lands centred on him
   after each cut and then holds (it must not chase small movements, and must not let him leave the frame). The last
   shot is his walk-out under the closing pill: he turns away there by design.
5. **Clips and photos fill the frame** unless the sides hold something the clip needs (Dan, 2026-10-01 / 10-02). The
   declared layout is the table in section 3. A card shorter than its source's full height at that width is a defect.
6. **Labels:** every AI image or clip carries AI-GENERATED; every REAL after picture of Dan carries
   "Real picture of me - not AI-generated" (a hyphen, never an em dash); before pictures carry no label. No label over
   his face or his abs, on any frame of the shot (stills push in, so check the last frame as well as the first).
7. **Captions:** word-timed, the lit word is the word being spoken; muted under every graphic that prints its own words
   (bullets, lower thirds, pills, title card, app screens); never over a CTA pill; a black plate sits behind them on
   full-frame pictures. No em dash and no spelling mistake in any burned text. No caption word carried across a 59 s seam.
8. **Standing bans:** no side-by-side before/after app screen, no "Meet the new you" screen, no email-capture form in
   shot (the "Download Your Future Self" screen is allowed with the form out of frame: Dan approved it on the editor's
   cut), same person in any before/after pair, no stick figures, no drug brand names, no AbsByAI.com mark graphic at the
   end, nothing frozen, no black frame, no swipe/whoosh sound.
9. **The 59 s cuts** are selections of their own masters (same picture frame for frame inside each range, with ONE
   declared exception: where a seam would join two talking shots at the same level, the cutdown flips one side NEAR/FAR so
   the seam is a zoom cut; an overlay that would run past a seam fades out before it), 59.0 s or under, each seam a sentence and thought boundary, reading as one script to a viewer who never saw the long version.

10. **Picture timing is his picture's.** Our talking-head frame n shows the raw frame his frame n shows (round 1 found it
    two frames late: fixed), and every talk-to-talk picture cut sits on HIS picture cut, or is held to the next insert
    where he holds it. Round 1's nine jump cuts were cuts on his audio splice; they are the first thing to re-check.
11. **Muhammad's own stock clips** (influencer, library, tub label, pill bottles, supermarket, meal prep) carry no AI
    label: they carry none in his approved master and the project's clip library catalogues them as stock
    (B0057-B0062). The robot clip is ours and is labelled.

12. **Declared differences from his master (not defects):**
    - *After pictures 3 and 4* (4759-4791) are two PORTRAITS of Dan (pool shoot, studio) in place of his two landscape
      photos (park, flag). This was done on 2026-09-11 under Dan's note on the Ad 5 vertical that every real after picture
      is full screen and vertical. It is listed for Dan's ruling on the review page; it is not the reviewer's call.
    - *The real-picture label* is set on two lines in the 9:16 ("Real picture of me" / "not AI-generated") and three in the 1:1
      ("Real picture" / "of me" / "not AI-generated", inside the photo's own width): the line break stands in for the hyphen. On one line it reads "Real picture of me - not AI-generated".
    - *The hook* (0-85) follows his two micro pause trims (cuts at 50 and 59, same framing, two and one frames): ours is in
      step with his mouth to within a frame; his frame-exact map there could not be measured more finely.
    - *The closing shot* (7100-7159) follows his slow-down: his picture advances one source frame every two or three frames,
      so frames repeat in pairs and triples there by design (Dan holds his smile under the pill, as in his master).
    - *His light-leak flashes* are rebuilt from his own luma trace with his blue-white tint, each fading over about ten
      frames after its cut.

## 3. Declared layout (frames on the full-length timeline, 29.97 fps)

| frames | what | 9:16 | 1:1 |
|---|---|---|---|
| 85-262 | AI robot clip, shot 1 | fills | the WHOLE portrait clip in a card (the action runs head to trash can) |
| 262-437 | AI robot clip, shot 2 | fills | fills |
| 437-639 | Dan's real supplement stack, pan | centre square in a card | fills |
| 928-1267, 2016-2304, 2488-2713, 5704-5912 | text screens | Dan above, text below | Dan above, text below, text ending by y 1030 |
| 1307-1477 | influencer + shaker | a 4:3 card, 75 % of the clip's width (holds the shaker with the hand on it at far left and his face right of centre) | the same card, ending above the caption line |
| 1754-1827 | library | fills | fills |
| 3086-3167 | tub label | fills, pushed in so the PROPRIETARY BLENDS highlight clears the caption line | fills |
| 3775-3864 | pill bottles | fills | fills |
| 4186-4219 | before: deck chair | fills | the whole photo, 846 px tall, on the field with the caption under it (a square crop loses his belly; a full-height photo puts the caption on it) |
| 4219-4251 | before: standing with the girl (the RECENTERED 4x5 version Dan approved as a before picture, which has his whole head) | the whole photo in a card (a full-screen crop halves the girl's face) | fills |
| 4251-4289 | before: on the ride | square in a card (second person) | fills |
| 4524-4595, 6836-6909 | AI goal image, AI-GENERATED | fills | the whole image at full height on the field (keeps the caption line off his abs) |
| 4723-4792 | four real after pictures, real-picture label | fill | each whole photo at full height on the field (a 1:1 crop put the caption line across his abs) |
| 5145-5238, 5351-5435, 5534-5704 | app screens in a phone | phone as large as fits | phone as large as fits |
| 5435-5534 | YOU LOCK IN title card | card | card |
| 6041-6206, 6282-6391 | audit phone with Dan | Dan above in a head-and-shoulders panel (y 60-640) at the hold's own level (his FAR to NEAR punch at 6157 shows as a size change), his lower third wholly on the field under the panel (y 654-802), phone below as large as the remaining height allows | Dan left, phone right |
| 6514-6634 | supermarket | fills | fills |
| 6634-6773 | overhead meal prep | centre square in a card | fills |
| 4795-5055, 7036-end | CTA pill over the talking head | | |

## 4. The reviewer's three jobs, per file

1. **The watch pass.** Each file's `watch*/JUDGE_PROMPT.md` and `CHECKLIST.md` describe it: give EVERY sheet, strip and
   pair image a verdict and write `findings.json` beside the watch log named in the prompt
   (`{"entries": [{image, verdict, item?, note?, t?}]}`; verdicts `clean`, `defect`, `expected`).
2. **The negative-events look.** `negscan*/sheet.jpg` beside each file: 30 evenly spaced frames. Say whether any frame
   frames a body with shame or contempt (a before picture shown plainly is not that). Report the frames you looked at.
3. **The independent review** against sections 2 and 3, from evidence you produce yourself (frames at full resolution,
   measurements, a transcript). Say what you could not verify.

## 5. Output

Write `ROUND-4-CHECK-<9x16|1x1>.md` in `/Volumes/Extreme/_edit_work/AV-03/`:

```
VERDICT: SHIP | DOES NOT SHIP   (one line per file)
DEFECTS: numbered, each with file, timecode + frame, what is wrong, the evidence, the rule it breaks
COULD NOT VERIFY: ...
NEGATIVE EVENTS: frames looked at, findings
```
