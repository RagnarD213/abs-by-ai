# RO-15 "Sleep Better With Glycine" round 1: independent recheck after the editor's fixes

Reviewer: fresh independent reviewer (did not build this; did not read editor notes or round files).
Date: 2026-11-04. Page: http://127.0.0.1:9715/ (files under `/Volumes/Extreme/_edit_work/RO-15/round1/review/`).
All times below are film times on the current timeline (the rendered blocks, the context clips and the page agree on it).

**Verdict: not ready for Dan yet. 14 of the 17 earlier findings are fixed; 3 are not (G18, L05, the 4:48 join). The changes and a wider look add 3 more fix-level problems (G08, G01, C01 colour). 6 fix-level findings in all, 10 notes.**

## Coverage and method

- Audio: all 8 piece joins plus 1 join that exists only in the rendered blocks (4:12.8, see N2) measured on the treated block audio (`blk_00`, `blk_02`, `blk_03`, `blk_04`, and `one_A8` for the A8 context), at 20 ms and 5 ms resolution, against the source lav (`lav.wav`, cross-correlated to the sample). Whisper medium.en on a 6 s window around every join, small.en where medium dropped a sentence. Nothing played out loud.
- Loudness: first-minute draft -14.3 LUFS, true peak -1.9 dBTP, LRA 2.3 LU; blocks -14.2 to -14.3 LUFS, peaks -1.5 to -2.3 dBFS.
- First-minute draft: 1920x1080, 29.97 fps, BT.709 tagged, 66.366 s, 1989 frames, AAC 48 kHz stereo. sha256 `e15afe60cd958eaea457d2e250ab8758f10487a95173262f3f361d6d3532e577` matches `.audio_gate.json`; stamp `gate_version` 2.0.0 equals current `audio_gate.py`; verdict FAIL on the tone row only (disclosed on the page). Every picture cut found by frame differencing (7: 0:10.94, 0:15.18, 0:28.13, 0:43.44, 0:49.45, 0:56.86, 0:59.09) decoded at full resolution both sides, plus the first and last frame. First 30 s transcribed (medium.en) and read against `script/glycine.txt`: matches, apart from Dan's own small wording. One piece of the roll, so no audio join inside the first minute.
- Hair, first minute: my own every-0.25 s top-of-hair scan of presenter frames (215 samples): closest 39 px at 0:27.25 (native crop inspected), median 57 px. Passes the 20 px rule.
- Graphics: per-frame text-presence curves on the lower-third text row for all 14 lower thirds, on the last line of L05, and frames for G02; accent-bar scan of all five blocks to confirm G05, G09 and G15 are gone.
- Clips: frames and colour stats (black share below luma 16, median saturation, median luma) for all 9 stock clips against the presenter frames beside them; P01 phone screen tiled across its whole duration.
- Context clips: 16 changed items compared with the current blocks at three points each (mean difference 0.1 to 2.2 grey levels: they are cut from the current renders).
- Page: opened in check mode (`?review_mode=automation`): both buttons present, every player muted; a context play stayed muted; "Finish checks for owner" returned ok with all 8 players paused and sound ready. Left in that state.

## The 17 earlier findings

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | J1 4:17.4 "results" / "Once" | Fixed | Out now at source 436.102, after the final "s" of "results" (sibilant burst 435.84 to 435.96). Treated audio: s ends 4:17.27, "Once" starts 4:17.60, about 0.5 s after the voiced end of "results"; room -45 to -51 dB on both sides; no step at the cut. Whisper hears "results." then "Once" 0.5 s later. |
| 2 | J2 4:48.2 "stop taking it" / "But" | Not fixed | "it" is not chopped, but the join is still rough (fix F4). The page's "false alarm, your voice ends a third of a second before that cut" is wrong: it ends about 0.14 s before. |
| 3 | C01 brands, head cut | Fixed, new problem | Pexels capsules into a palm: no brand, no Dan. New colour problem (fix F6). |
| 4 | Same stock scene twice | Fixed | C03 is now a different actor and bedroom (pink headboard, teal duvet, top-down); checked against C05, C06, C07, C08: all distinct. |
| 5 | C03, C05 flat gamma grade | Fixed | C03 6.7 % black, C05 8.7 % black (presenter 8 to 10 %). Both stay darker than the studio (medians 36 and 38 vs 68 to 75): night scenes, note N6. |
| 6 | G15 | Fixed (removed) | No lower-third bar anywhere between 3:43.8 and 3:52.4. |
| 7 | G18 | Not fixed | Fix F1. |
| 8 | G17 | Fixed | Point lands 4:15.31, readable to 4:17.61: 2.3 s. Bar empty about 0.4 s. |
| 9 | G04 | Fixed | "Worth Trying" lands 1:48.54, readable to 1:50.31: 1.8 s. |
| 10 | G05 | Fixed (removed) | No bar between 1:50.5 and 1:57.4. |
| 11 | G06 | Fixed | Point lands 1:58.29, readable to 2:00.23: 1.9 s. Bar empty about 0.6 s. |
| 12 | G07 | Fixed | Point lands 2:07.63, readable to 2:10.80: 3.2 s. |
| 13 | G12 | Fixed | Eyebrow alone about 0.9 s (bar 3:00.2, first part 3:01.02); "I Sleep Best At 63°." lands 3:04.09, readable to 3:06.32: 2.3 s. |
| 14 | G02 | Fixed | Card empty about 0.6 s; citation lands about 1:21.3 and holds to 1:24.6 (about 3.3 s). Eyebrow now "STUDIES IN JAPAN" (the unsaid "2" is gone). |
| 15 | Page silent check / owner handoff | Fixed | Server injects `/__review_player.js`; both buttons work as described above. See note N1. |
| 16 | Ad-lib timestamp | Fixed | Page says 2:03.7, the start of "And if you're overweight, or if you just have a thick build"; "thick" is at 2:05.6. |
| 17 | L05 | Not fixed | Fix F2. |

## Fix-level findings (most severe first)

**F1. G18, 4:22.4 to 4:26.4: still unreadable, still an empty bar.** The bar is up from about 4:22.9 showing only "HOW TO TAKE IT". "Powder, Not Capsules" arrives 4:25.03 to 4:25.16 and is gone by 4:26.33: **1.1 s** to read (needs 1.5 s). The eyebrow sits alone for about 2.1 s first. Simplifying it to one part did not change the timing: it lands on "powder" (4:24.93) and the strip has to clear for A7 at 4:26.87. Frames 4:23.0, 4:24.8 (empty bar), 4:25.3, 4:26.25.

**F2. L05, 1:24.6 to 1:29.7: last line still under 1.5 s.** "Less Sleepy The Next Day" lands 1:28.37 to 1:28.43 and the card fades from 1:29.57 (gone 1:29.64): **1.2 s** (was 0.9 s). The card cannot run past the 1:29.72 join, so the line has to land earlier (Dan starts the clause with "and they were" at 1:28.02).

**F3. G08, 2:12.6 to 2:16.6 (changed item): empty bar, then 1.1 s to read.** The bar shows only "GOOD FOR YOU IF" from about 2:13.0 until "You Lie Awake For 30+ Minutes" arrives 2:14.96 to 2:15.29 (about 2 s empty), then the strip is gone by 2:16.49 for C05: **1.1 s** to read. The same faults the earlier check found on G05, G06, G07, G15 and G18. Frames 2:13.5 (empty bar), 2:15.4, 2:16.4, 2:16.55 (mid-fade).

**F4. J2, 4:48.2 (join "major" to "numbers", start of A8): not a false alarm; tight join with a hard start.** Measured on the treated audio of `blk_03` and of `one_A8` (the A8 context clip):
- The voiced end of "it." decays out by about 4:48.08 (source 470.00); the outgoing side then ends on a rising breath (-60 to -48 dB, noisy) cut at 4:48.22 (source 470.137). The voice ends about 0.14 s before the cut, not a third of a second.
- The incoming piece starts at source 472.839, 40 ms into a short voiced lip noise that comes before "But" (472.80 to 472.85). In 5 ms steps the level jumps from -57 to -40, -36, -35 dB at the first samples after the cut, dips to -53, then "But" at -28: a hard start with a double onset.
- Sentence gap "it." to "But": about 0.18 s (Whisper: 0.12 s). At the same spot in the raw take Dan paused about 0.40 s (voice end 470.00, his restart "But" at 470.40). The two sentences run together the way J1 did before its fix.
- Whisper hears "stop taking it. But if your numbers go up", so no word is lost. I could not listen; a 5 s listen at 4:46 to 4:51 is needed. The page's statement "your voice ends a third of a second before that cut" should come out.

**F5. G01, 0:52.2 to 0:56.7 (first minute, unchanged, missed by the first check): last part 1.3 s.** "Your Core Has To Cool Down" completes at 0:55.32 and is gone by 0:56.62: **1.27 s** to read, under the 1.5 s standard, in the first minute. It lands on its word ("lower its core", about 0:55.0); the limit is C03 at 0:56.86.

**F6. C01, 0:10.9 to 0:15.2 (new clip): not colour matched; the page says it is.** C01 has no grade in the plan. Measured on five frames: 0.0 % of pixels below luma 16, median luma 197, 5th to 95th percentile luma 171 to 203, median saturation 0.17. The presenter shots on either side: 10 % black, median luma 75, saturation 0.38. It is the brightest and flattest shot in the film, a beige wall and a hand, cut between two dark teal studio shots in the first 15 seconds. The page says "Colour matched to the studio by measurement (true blacks kept)", which is not true for C01, and only roughly true for the two regraded bright clips: C08 (3:23.5) 0.5 % black, median 191, saturation 0.04 (the first check measured 206 and 0.03, so the regrade barely moved it); C02 (0:43.4) 0.0 % black, median 178. Grade C01 (and C08) toward the studio by the B-roll rule's measurements, or correct the page.

## Notes

- **N1. Page renders in quirks mode.** `index.html` has no `<head>`, so `review_server.py` inserts its script before `<!doctype html>`; in the browser `document.compatMode` is `BackCompat`. The buttons and audio hooks work; add a `<head>` so the page renders in standards mode.
- **N2. Two timelines in the work folder.** `shots.json` and every rendered block trim 12 frames (0.4 s) of pause between "if you're a hot sleeper." and "I've said this before" (shot `factors.1`, source 431.27 to 431.67), but `piece_map.json` and `assembled_untreated.wav` do not. From 4:12.8 on, the assembled wav runs 0.397 s later than the blocks, the page and the plan (for example its J1 is at 4:17.79 and its J2 at 4:48.62). Any audio gate or join scan run on `assembled_untreated.wav` is measuring a different cut from the one that renders. The extra join itself is clean: it sits in the pause with a short fade, -40 dB at the cut, 0.37 s between sentences, and Whisper hears both sentences. It is in no join list.
- **N3. "Please listen at 5:04":** the possible doubled "If" is at about 5:05.4 on the current timeline (Whisper medium.en hears "If you want" once in my window).
- **N4. P01, 5:09.5 to 5:21.1:** the "$136/mo" banner is gone (no frame shows it). The keep and drop list still shows readable brand names: Thorne, Nutricost, Anthony's and AG1 ("AG1 Next Gen (AG1)", the brand that got C01 replaced), plus "Advanced Testosterone Support (Thorne)" and prices Dan never says (-$15/mo, -$40/mo, -$79/mo, ~$25, ~$32). The page says "nothing branded on screen except the app and the AI chat"; these are inside the app, Dan's call. The first 1.5 s shows the app's AI-generated shirtless "YOUR GOAL IMAGE" at the top of the screen, labelled AI-GENERATED on the picture, off face and abs.
- **N5. G02:** "3 g Before Bed" lands about 1:19.0 on "studies that were done", 2.3 s before Dan says "3 grams" (1:21.28); the citation (not spoken) lands on "3 grams". Swapping the two would land the number on its word. The lab photo still crops the man's face (unchanged).
- **N6. C03 and C05** are darker than the studio (median luma 36 and 38 vs 68 to 75) and C05 is strongly orange (saturation 0.69 vs 0.38). They are night scenes and their blacks are now real; check them beside the studio in motion.
- **N7. G17** stays on 0.3 s across the 4:17.39 framing cut (tight to wide) before it fades; harmless, but it reads as the bar carrying over a cut. Its copy is now an echo of the words under it.
- **N8. C01 content:** the first 0.5 s is an outstretched arm with an almost empty palm; capsules arrive from about 0:11.6. The arm is a person although the plan says `people: none`. It still reads as "supplements".
- **N9. G13 to G14 at 3:34.6:** the 0.15 s blink between two bars is still there (first check N9, unchanged).
- **N10. `words_out.json`** is on the block timeline and matches it; only the piece map and assembled wav are off (N2).

## Not verified

- No audible listen: nothing was played out loud. F4 (4:46 to 4:51), J1 (4:15 to 4:20) and N3 (5:03 to 5:07) need a human ear.
- No full-film render exists; whole-film checks used the blocks and the context clips.
- AI frames were not re-reviewed (unchanged); AI motion does not exist yet.
- Hair was re-measured in the first minute only; the later blocks were spot-checked on the frames I decoded (all with visible room).
