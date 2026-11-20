# Quality gates, and what each Joint Vigor review found

Joint Vigor took seven fresh Fable 5.2 reviews to reach SHIP: block 1, then A and B (two halves of the first full
film), then C, D, E and F on the whole film. Review files: `claude-r4/asm/REVIEW-FABLE-A.md` to `-F.md`; fixes in
`asm/out/RECEIPT-R2.md`. Most findings were classes that a check can catch. **Run every gate below before the first
reviewer sees the film**; the reviewer should be finding judgement calls, not defects a script could have found.

## The gates, in run order
| # | Gate | Tool (Joint Vigor kit, `claude-r4/...`) | Pass |
|---|---|---|---|
| 0 | **Client ledger** | `.claude/skills/client-vsl/tools/client_ledger.py gate <job> --stage build` (before the first render), `--stage review` (before the reviewer), `--stage deliver --file FILE --rows ROWS.json` (before Dan's page and any send) | PASSED line in the receipt. Every client instruction done with a frame from the master and a reviewer PASS, or waived in his own words; no unsupported "approved by the client"; thread swept within 24 h |
| 1 | Plan lint | `build/lint_plans.py` all plans | no still over 5 s in VO, no source reused within 90 s (keyed by file NAME, not path), no missing asset |
| 2 | Casting audit, whole film | `build/casting_audit.py --master <clean 1.1x> --out asm/castN` then read every sheet by eye | every featured person fits the client's casting rule; professionals and background listed for Dan |
| 3 | Dramatization chip sweep | native-size crops of the top-left corner on the first and last frame of every AI shot of people (Joint Vigor: `asm/checkE/chip/`) | every AI clip, AI still, AI testimonial and client-supplied AI image of people carries the chip, clear of faces |
| 4 | Story-scene read | frames at 0.5 s steps through every narrative scene | one location, one cast, the featured character in frame, beats in script order (nobody on the floor before the fall) |
| 5 | Line match | one frame per shot against its line | the shot shows what is said (sex, age, mood, object); text visible in an insert is in English and on topic; nothing out of focus |
| 6 | Frame and length | `build/gates_film.py --dir asm/out --name <NAME>` | frame counts at 1x and paced; video length = audio length |
| 7 | Per-frame luma | `gates_film.py` | no isolated dark frame, no dark run, no one-frame flash, no shot mostly below luma 16 |
| 8 | BT.709 decode check | after ANY patch round: mean level of untouched reference frames (office wall, a dark shot) against the first render | difference under about 1 level; every decoder states `in_color_matrix=bt709` |
| 9 | Patch boundaries | `build/verify_patches.py` | 0 stale frames (mean absolute difference 12 or less) at the first and last frame of every patch range and one either side |
| 10 | Spokesperson continuity | coat, skin and wall measured on every doctor frame; `build/holdcheck.py` | no colour step at a cut (camera white-balance steps fixed by per-channel gain); no one-frame pose jump |
| 11 | Black, freeze | `gates_film.py` (blackdetect, freezes over 1.2 s) | none, or each one is still stock under a push-in and listed |
| 12 | Card keep-out | `gates_film.py` (edge density in the caption band of the clean master, threshold 0.02) | no card TEXT in the caption band (product photo bottoms may flag; list them) |
| 13 | Captions | `gates_film.py` | SRT words = burned words; onsets on speech (Joint Vigor 99.96%); no doubled word; no dash characters |
| 14 | Reveal | `gates_film.py` plus a frame strip | first frame of the product lands on the spoken product word; no product or product name anywhere before it |
| 15 | Audio | `_shared/audio/seamscan.py` on every EDL join of the paced master; `gates_film.py` music dropouts (side signal under -58 dBFS for 0.5 s or more); EBU R128 | join flags none; no dropout; -13.5 LUFS +/- 0.5, true peak at most -1 dBTP |
| 16 | B-roll in the finished film | frames pulled from the final master at every insert changed this round, beside the spokesperson | corrected, not flat, washed out, crushed or neon (VIDEO-RULES, 2026-11-16) |
| 17 | Shared stamps | `_shared/deliver/gate.py` (format `ad16x9`) and `_shared/audio/audio_gate.py` on the delivered masters; sha256 written into each `.finish.json` | record the verdicts; a Dan-specific check that cannot apply to a client spokesperson is noted, not forced |
| 18 | Dan's page | `review_server.py`, owner hand-off | seekable; button text exactly `Full screen` opens VLC; tested at 800 and 1150 px; paused with sound ready |

Gate 17 is the one Joint Vigor never ran (reviews C, E and F each noted the missing `GATE_VERSION` stamp). Run it next time.

## What each review found, and the check that now catches it
| Defect class | Joint Vigor example | Found in | Caught now by |
|---|---|---|---|
| **The client's written feedback not applied** | Eric's 19 timestamp notes on the trial lead and his no-sales-letter-images rule: lead reused as "approved by Eric", 80 such images in the film, reviews never saw his doc | the client, the day after delivery | gate 0; [CLIENT-LEDGER.md](CLIENT-LEDGER.md) |
| Picture shorter than the sound | block 1's picture ended 2 s early | block 1 | gate 6 |
| Flash at a chunk or opening join | a 4-frame CLOSE flash at the opening seam | block 1 (editor's own frame check) | gate 7, plus a frame strip across every chunk join and the opening seam |
| See-through coat | hand shadows on the white coat read as holes on the grey plate | block 1 | `coat_scan.py` + compositor `coat_lift` (PIPELINE step 1) |
| Stock fallback left in a story scene | wedding shown with unrelated stock | block 1, A9, C S3 | gate 4; AI needs for a story scene queued first |
| Caption timing drift | captions late after 5:32 | block 1 | forced alignment (PIPELINE step 3), gate 13 |
| Doubled caption word | "every every" at 16:09 | A1 | gate 13 |
| Callout flashing or off the frame | one-frame "In just 5 days"; callouts running off the right edge | A2, block 1 | callouts on spokesperson spans only; gate 7 catches one-frame pop-ins |
| Missing key-visual label | KV4 age labels missing | A3 | key-visual stills compared with the approved ones before render |
| Product before the reveal | KV9 showed the bottle early | A4 | gate 14 |
| Music hole at the loop | 1.3 s near-silence at every loop point | A5 | trim the track's fading tail before the crossfade; gate 15 dropouts |
| Chopped sounds at joins | 30 to 50 ms stubs after "began to dance" | A6 | gate 15 seam scan; `join_scan_r4.py` at the dialogue step |
| Frozen or long-held stills | knee animation frozen; study cards held up to 16.8 s; guarantee card held | A7, A8, B10 | gate 1 (5 s rule); KVs broken up with cutaways |
| Source reused within 90 s | walking woman, knee close-up, lab shots; later the same client photo spelled two ways | A11, D, F2 | gate 1 keyed by file NAME |
| Name spelled two ways | "Labeaud" caption vs "LaBeaud" card | A12, C17 | card and caption names checked against the published source |
| Casting break | yellow-backdrop man, young pharmacist, East-Asian-reading stairs couple x4, Black guest front and centre, young nurse, young sprinter, stilettos | A13, B8, C5 to C7, D MUST 1 and 2, D10, E7 | gate 2 on the WHOLE film, not only changed shots (Joint Vigor's audit read 586 shots and replaced 7 more) |
| Caption mishears | "A 2025 study", "100% safe", "5 to 7 business days" | A16, B5 | script-corrected words, forced alignment, `lowconf_whisper.py` |
| Text in the caption band | KV14 $228 total, Boswellia card, ingredient grid, diagram labels under the captions | A17, B2 to B4 | contain-fit cards at 78 to 88%, top-anchored; gate 12 |
| Stray black frame | a clip's black first frame at 53:45 | B1 | gate 7; in-points moved past black first frames |
| Testimonial freeze | 12-frame freeze at the end of Rick's clip | B11 | let the clip run on through the pause; gate 11 |
| One-frame patch leftovers | old frames at 26:28.45 and 35:51.95 | C MUST 1 | patch ranges rounded to whole frames; gate 9 |
| Card sliced by a cover crop | Rheumatologist card read "umatologist" | C MUST 2 | contain-fit every card with text (PIPELINE step 8) |
| Replacement landed on the wrong shot | fix covered half the old shot, or the shot before it | C S4, S6, S8 | map each review time 0.1 to 0.2 s inside the flagged shot; check frames from the final master at every flagged time |
| Out of focus or near-black insert | "papers" shot blurred for 4.5 s; near-black silhouette | C S9, S10 | gates 5 and 7 |
| Wrong sex or mood for the line | a man doing arm swings under Margie's pain | C S11 | gate 5 |
| **Patch rounds darkening the film** | splice and caption tools decoded BT.709 chunks as BT.601: 2 to 3% darker per round, chunk B mean 74 to 61 after seven rounds | found by the luma gate after C | gate 8; `rebuild_chunks.py` in one generation |
| Spokesperson colour step | camera white balance stepped at source frame 16138: coat cream before 23:55, cold after | D S7 | gate 10 |
| One-frame pose jumps | hands jump for one frame at three doctor cuts | D S6 | `holdcheck.py`, gate 10 |
| Washed-out stock | stairs shot clipping to white | D S5 | gate 16 |
| Foreign text on screen | a Spanish novel under "medical journals" | D S8 | gate 5 |
| AI people without the chip | crops of an AI clip pushed the chip out of frame; four wedding stills; 15 client AI photos | D S4, E MUST | gate 3 over the whole film, client images included |
| Upscale halo | tight crops of AI stills enlarged with sharpening: white edge lines | E S2 | crops at most 2x, plain bicubic, no sharpening; native-pixel look |
| Story beat out of order or a different person | Margie already on the floor before "she crashed"; a different woman in a different place mid-scene | E S4, F1 | gate 4 |
| Frame filled by a body part | a bare calf filling the frame under "without holding the railing" | E S6 | gate 5 (check the last frames of every new insert) |
| Client-supplied generated people unchipped | the customer wall of generated people holding the bottle | E S8, F3 | gate 3; ask the client whether his AI images are dramatizations |

## Process lessons (fewer rounds next time)
- A reviewer line such as "I could not establish whether the client approved this" (Joint Vigor review F said it three
  times) is a stop: answer it from the ledger before Dan sees the film. It was the last warning before the miss.
- No check may measure the new film against an earlier cut of ours as "approved" (Joint Vigor's `approved_check_r4.py`
  and block 1's "58 of 58 cuts matched" proved the film matched the un-revised trial).
- Run a full-film reviewer on the first finished block: it caught four systematic faults before blocks 2 to 4 rendered.
- Every fix round: fix ALL items (MUST and SHOULD), then run the whole-film sweeps (casting, chips, luma, BT.709) again,
  not only the changed spots. Joint Vigor's D and E MUSTs were classes C's fixes could have swept.
- Re-finish once per round; never ship a master that a gate has not read.
- Give the reviewer the previous review, and ask it to verify every earlier item in the new file.
- "For Dan" items (professionals not matching the casting rule, client art, inherited approved material) are listed,
  not silently fixed or silently kept.
