# RO-15 "Sleep Better With Glycine" round 1: independent check

Reviewer: fresh independent reviewer (did not build this; did not read editor notes or round files).
Date: 2026-11-04. Page: http://127.0.0.1:9715/ (files under `/Volumes/Extreme/_edit_work/RO-15/round1/review/`).

**Verdict: the page should not go to Dan as is. 17 fix-level findings, 17 notes.**

## Coverage

- Items checked: 41 of 41 in `plan_resolved.json` (8 AI slots, 9 clips, 1 phone scene, 18 lower thirds, 5 side cards, 1 fact card). Every context clip decoded at its in, out, inside and every reveal (311 frames, `ctx/fr/sheet_<ID>.jpg` in my scratchpad).
- AI start frames checked: 12 files across 8 ideas (A1 X1; A2 X1, X2; A3 X1, X2; A4 X1; A5 X1, X2; A6 X1; A7 X1; A8 X1, X2), plus the 8 placeholder slots in their context clips.
- First-minute joins checked: 14 picture joins (0:04.8, 0:10.9, 0:15.2, 0:19.7, 0:22.9, 0:28.1, 0:39.5, 0:43.4, 0:49.4, 0:52.2, 0:56.7, 0:56.9, 0:59.1, 1:02.2) decoded at full 1080p on both sides, plus the first and last frame. The first minute is one continuous piece of the roll, so it has no audio join inside it.
- Whole film: all 23 presenter cuts in `blk_00.mp4` decoded frame-accurately (frames n-2 to n+1) and differenced; all 9 audio joins in `assembled_untreated.wav` measured (20 ms envelope, sample step, voicing) and transcribed twice (Whisper small.en on the whole film, medium.en on suspect windows).
- Delivered draft: 1920x1080, 29.97 fps, BT.709 tagged, 66.366 s, 1989 frames; sha256 `59e04fab41fc497c3e4290065af57dc56a697e8a170eba07b24df8be4eda3cc9` matches the audio-gate stamp; stamp `gate_version` 2.0.0 equals the current `audio_gate.py` GATE_VERSION. Loudness -14.3 LUFS, true peak -1.9 dBTP, LRA 2.3 LU.
- Hair: my own coarse every-0.25 s top-of-hair scan of every presenter frame of `blk_00.mp4` and `blk_01.mp4` (869 + 87 samples): closest 40 px at 0:27.4 (native crop inspected), median 61 px. Passes the 20 px rule.

## Fix-level findings (most severe first)

1. **J1, 4:17.1 (join factors to major, under G17).** "of your results. Once you have" is chopped: both Whisper models independently hear "your **result.**" (the final s is cut; the factors piece ends at source 435.84 s while the word runs to about 435.90 s). The join has no pause: voiced sound runs right through the cut (voicing 0.81 in the 80 ms after it), then a 0.13 s noisy burst, then "Once". Two sentences crammed together with a clipped word. Plays in the G17 context clip.
2. **J2, 4:47.8 (join major to numbers, start of A8).** The cut lands inside the voiced end of "stop taking it" at about -33 dB with no fade; the sample step at the cut is 3.5 times the local median (0.0063 vs 0.0018). The source cut (470.14 s) is 40 ms before the word's end (470.18 s). Likely a clipped "it" and a hard edge; needs a 5 s listen at 4:45 to 4:50, I could not listen.
3. **C01, 0:10.9 to 0:15.2.** Readable brand names fill the shot: AG1 (large), ISOPURE, Thorne, Nutricost Vitamin B6, Anthony's. The page says "nothing branded on screen except the app and the AI chat", which is false. Dan is in the shot only as a standing torso behind the counter with hands clasped, his face cut off by the top of the frame for the whole clip (a Dan cutaway that is him standing, head cut).
4. **C03 (0:56.8) and C05 (2:16.6): the same stock scene twice.** Pexels 6944078 and 6944070 are the same actor in the same bedroom (quilted headboard, tripod lamp, beige bedding). Rule: no repeated stock scene in one video.
5. **C03 and C05: gamma-lift grade, flat and washed.** Plan grades are `eq=...gamma=1.25` and `gamma=1.2`. Measured: 0.0 % of pixels below luma 16 in both clips (presenter frames around them: 7.6 to 10.9 %); both read flat orange-brown next to the studio. VIDEO-RULES: never a gamma lift alone, match black share, saturation and brightness to the approved look.
6. **G15, 3:44.0 to 3:51.9.** "Glycine Is No Cure-All." rises at 3:51.6, the same moment the strip starts fading (page beat sheet and frames 3:51.86, 3:52.0). The second part is never readable. The bar also sits empty for 2.2 s before "I Track It."
7. **G18, 4:22.0 to 4:26.0.** "Not Capsules" rises 4:25.3, strip fades 4:25.7: 0.4 s readable. The bar shows only the eyebrow for 2.5 s before "Powder,".
8. **G17, 4:14.5 to 4:17.7.** "Of Your Results" rises 4:16.7, strip fades 4:17.4: 0.7 s readable (frame 4:17.65 is mid-fade).
9. **G04, 1:44.9 to 1:49.5.** "Worth Trying" rises 1:48.3, strip fades 1:49.2: 0.9 s readable.
10. **G05, 1:51.6 to 1:56.7.** "Based On How It Works" rises 1:55.2, fades 1:56.4: 1.2 s. The bar sits empty (eyebrow only) for 2.9 s first. The copy also just repeats the words under it, and the eyebrow "WHO IT'S FOR" does not match a point about opinion.
11. **G06, 1:57.4 to 2:00.4.** "You Run Hot At Night" rises 1:58.8, fades 2:00.1: 1.3 s (under 1.5 s).
12. **G07, 2:06.8 to 2:09.8.** "Bigger Guys Run Hotter" rises 2:08.2, fades 2:09.5: 1.3 s (under 1.5 s).
13. **G12, 2:55.3 to 3:06.5.** The strip shows only the eyebrow "MY BEDROOM" for 5.6 s (2:55.3 to 3:00.9) before "AC Bottoms Out At 67°." lands. An empty bar on screen that long looks broken.
14. **G02, 1:16.3 to 1:23.6.** The citation line "Yamadera 2007 and Bannai 2012" lands 1:22.6 and the card is gone at 1:23.6: about 1 s to read a citation. The glass card is also empty for 2.7 s at the start (1:16.3 to 1:19.0).
15. **Page: no silent-check mode or owner handoff.** `index.html` has no `review_player.js`, no "Start silent checks" / "Finish checks for owner" controls and no `AbsReviewAudio` hooks; its only script calls `v.play()` with sound on any still click. AGENTS.md (2026-10-28) requires both on review pages. Because of this I did not play anything in the browser.
16. **Page decision 6 timestamp is wrong.** It says the ad-lib "or if you just have a thick build like I do" is at 1:44; it is at 2:03.7 (words_out 123.67 s, confirmed by my transcript at 2:04.6). Dan will look in the wrong place.
17. **L05, 1:23.6 to 1:29.7.** Last item "Less Sleepy The Next Day" lands 1:28.5 and the card fades from 1:29.4: about 0.9 s to read the final line (side card, same 1.5 s standard).

## Notes

- N1, 5:04.9 to 5:05.4: possible half-start before "If you want a full supplement plan". Whisper small.en hears "If you / If you want"; medium.en hears it once; the source word "If" runs 0.62 s and there is a 60 ms burst at 5:05.36 before the speech. Listen.
- N2: echo graphics. G06, G08, G09, G10, G13 (and G05 above) print the words he is saying rather than distilling a point. G03, G11, G14, G16 and G18 are fine.
- N3, G02: "2 STUDIES IN JAPAN" prints a number Dan never says (he says "the studies that were done in Japan"); "3 g" here vs "3 Grams" on G10 and L04; the lab photo is a faceless man at a bench, not the two studies the script cue asks to show.
- N4, L02 1:06.4: heading wraps as "How Glycine Cools / You", one word alone on line 2.
- N5, L01 0:37.6: "Grams Of It In Your Food Daily" reads awkwardly ("A Couple Grams A Day In Food" says it).
- N6, P01 5:16 to 5:20.6: the results screen shows a big "~$136/mo" savings banner Dan never says, plus Thorne and Nutricost names. Real app screen, Dan's call. (Phone shell verified fully inside the frame with about 28 px top margin.)
- N7, C06 2:40.9: shows a sleeper with a watch and phone, not an Oura ring, on "I wear an Oura ring" (already decision 5 on the page).
- N8: off-look stock next to the studio: C08 (3:23.5) median luma 206 and saturation 0.03 vs presenter about 60 to 75; C02 (0:43.4) bright cyan, median 189; C07 (3:20.9) median 39. Consider a grade.
- N9, 3:34.6: G13 ends 214.56 s and G14 starts 214.71 s, a 0.15 s blink between two bars across a picture cut.
- N10, 0:56.7: G01 leaves 0.1 s (3 frames) before the cut to C03.
- N11: lower thirds sit over Dan's hands and waist; his hands pass behind the translucent bar (G01 0:55 to 0:56.7, G15). Not face or abs, but busy.
- N12, AI frames: A3 X1 has a dark hole-like patch at the groin in the thermal render; A8 X2's reaching arm looks long (shoulder to fingertip about 3 head heights); A4 X1 is small and very dark (the man fills little of the frame). All read clearly with the sound off and fit their lines; A1 X1 (supplement graveyard), A2 X1, A5 X1/X2, A6 X1 (thermostat war, the joke lands) and A7 X1 are good. No belly framing in any frame.
- N13: first-minute audio gate verdict is FAIL (tone row only; disclosed on the page as the known bass-lift mismatch). No `deliver/gate.py` (2.6.3) run on the draft; the page says it comes with the full film.
- N14: `options/` holds 540p "REVIEW" copies of the colour options, against the 1080p-only default (they are not linked on the page).
- N15: `blocks/blk_01.mp4` (an internal render) carries an "AbsByAI.com" chip during P01 that the plan turns off (`site_chip=False`); the page's P01 context is clean. Make sure the full film is built from the plan, not that block.
- N16: C01 is kitchen-set footage (Dan behind his kitchen counter) inside a studio film; check against the kitchen release rule when scheduling.
- N17: C09 shows a readable ChatGPT screen; acceptable since Dan names it, and nobody is looking at the phone.

## Checked and clean

- Whole-film speech against `script/glycine.txt`: every script line is present; none of the listed restarts remains ("So wh-", "Now I want you to keep this", the first "If you rarely", "now I'm usually in the se-", both "I've found that factors", "Once you have the major thing-", "But if your numbers go up, you've-"); the ad-lib is kept as decided.
- First 30 s word for word (Whisper medium.en on the delivered draft) matches the script apart from Dan's own small wording ("when you learn", "a little white powder"). No burned captions (by design, stated on the page).
- No jump cuts: every presenter cut alternates framing (all 23 show a framing change between frames n-1 and n; 0:39.5 has no change because the source is continuous; 2:22.2 is covered by C05).
- Side cards L01 to L05: Dan's arms and hands never touch or pass under a card in any sampled frame; every card starts and ends on a picture cut or a reframe to the card layout.
- No presenter flash under 0.5 s between cutaways; no belly close-up or fat pinch anywhere; AI-GENERATED label on every AI placeholder, off faces.
- Options: three colour options at the same moments (wide and tight), clearly different (mean RGB C 64/75/68, rich 59/74/63, bright 78/88/81); five voice options are the same 30 s passage (lag 0), level matched (-14.3 to -14.5 LUFS, peaks -2.7 dBFS) and genuinely different (low-band share 0.086 to 0.148, floor -45 to -52 dBFS).
- All 112 page links resolve (HTTP 200) and the server answers range requests (206).

## Not verified

- No audible listen: by instruction nothing was played out loud. J1, J2 and N1 need a human listen at 4:15 to 4:20, 4:45 to 4:50 and 5:03 to 5:07.
- AI motion does not exist yet; only start frames were judged.
- No full-film render exists, so whole-film picture checks used `blocks/blk_00.mp4`, `blk_01.mp4` and the context clips, not a delivered master.
