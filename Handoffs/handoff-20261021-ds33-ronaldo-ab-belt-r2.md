**SFC.** Task name: `Ronaldo Ab Belt SFC R2`. Model: Claude Opus 5.5, high (the video started on Claude).

# DS-33 "Cristiano Ronaldo Sells An Ab Belt. It's Harder Than A Workout." Round 2

Content, dedicated Short. Round 1 delivered 2026-10-21 (review page http://127.0.0.1:9033/, master sha256
`2bb0a2bea1bdf9c70c4b074156f821e5354f20752d8a6c3855b5f105c9b30b5d`, 58.16 s). Dan reviewed it and gave the notes below.
Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (in full) and the shorts skill's section
"Green-screen reaction shorts: what DS-33 (Ronaldo Ab Belt) cost" before starting.

## Dan's round 1 notes (verbatim, 2026-10-21)

> In the intro clip, I want this to be a vertical full-screen crop of the clip I'm reacting to. I want you to put me in the
> upper-left-hand corner, and I want to have some of the laptop visible when I'm reacting. I want you to see I'm looking at
> a laptop and not just looking down. It looks like I'm just looking down right now, away from the clip. Make me very small
> in the upper-left-hand corner while the main clip plays behind me. Let's go with the warm color and the balanced voice.
> Play a few seconds more of the clip. I feel like it wasn't really enough of the clip. Okay, once the main clip is done, I
> want you to continue playing it silently in horizontal orientation above my head and move me down. Basically, like the
> same crop you used for the intro on this one. That's what I want after the intro clip is done. Play the clip until about
> 27 or 30 seconds, depending on how long you extend that intro clip. About halfway through the video, then you can edit it
> normally, but keep that clip playing horizontally in the background above my head until that point.

## Decisions locked by Dan

- Colour: **Warm** (grade.py `warm`, as in R1). Voice: **Balanced** (as in R1; no bass lift). Do not show options again.
- Everything else in R1 he did not mention stays: take choices, captions style, the four Soft Blue lower thirds' copy
  (G01 source tag, G02 THE CATCH, G03 BELLY FAT, G04 MORE AB TIPS), B-roll B0427, framing method, headroom.

## What to build

1. **Intro (clip-first, Dan silent): the ad full screen, vertical.** A 9:16 full-screen crop of the ad (1080x1920) with Dan
   keyed and VERY SMALL in the upper-left corner (picture in picture), the ad behind him. Show part of the laptop in his
   window so the viewer reads that he is watching a screen, not looking down. The laptop is not green, so it survives the
   key; widen his window downward to include its top edge and some of the lid (C1730 laptop top edge ~2620 px in the 0.75
   keyed space, ~3490 native). Keep his face clear of the ad's subject where possible; no captions in this part.
   - Crop each ad shot on its subject (centred Ronaldo for the full-body shots; the 9:16 window is 405x720 of the 1280x720
     source), steady per shot, never cropping a shot shorter. Source is 720p: a full-screen 9:16 crop is a 2.67x upscale.
     First spend 10 minutes searching for a higher-resolution upload of this exact 2015 SIXPAD TV ad (YouTube, Vimeo,
     Japanese uploads; downloads are standing-authorized); use the best found and say which.
   - **Longer: "a few seconds more".** R1 played 10.4 s (ad frames 60-504, title card 208-320 skipped). Aim for about 14-16 s.
     Ad shot map (l3re1wcd0Bg, 29.97 fps, cut times in s): A torso 0-4.54, B face 4.54-5.91, C finger on button 5.94-6.94,
     D "Body Revolution" title 6.94-10.71, E belt on CR7 abs 10.71-14.01, F full body with pulse graphics 14.01-16.82,
     G side view 16.82-19.72, H abs with belt, side-lit 19.72-23.77, quick cuts 23.77-25.27, then more shots; the woman's
     scenes start about 30 s; Ronaldo returns about 49-55 s, product and logo about 56-60 s.
   - Watching footage: C1730 ~172-187 s (R1 used 174.00-184.38: fist pressed into his stomach, wincing). Extend to match.
   - Sound: the ad's own audio, one continuous stretch, plain gain (no limiter), folded to mono; the R1 recipe handles it.
2. **After the intro, until about the halfway point (~27-30 s of the film):** the ad keeps playing **silently**, horizontal
   (its whole 16:9 frame, never height-cropped) **above Dan's head**, with Dan keyed below it at full width: the same split
   layout R1 used during the intro (ad card on top, Dan below). Continue the ad's picture from where the intro left off;
   avoid repeating shots already shown in the intro where the ad has enough footage. Dan's line "Cristiano Ronaldo will
   sell you a belt that shocks your abs, but does it really work? Here's my take." and onwards play over this layout.
   - Because the ad is on screen, R1's ad cutaway C01 (12.58-16.05) is redundant: drop it. The take-1/take-2 join it
     covered then needs another cover: a framing change of Dan inside the split (wider/tighter window), or keep the
     tightened pause.
   - Re-place captions, G01 and G02 for the split layout (clear of his face and of the ad card; captions still never cross
     a join). G01 (source tag) can move to the split section or the intro, wherever it reads best.
   - End the split at a sentence boundary near 27-30 s (R1: "...do the workout." ends ~27.4, "Also, remember..." follows).
3. **From there to the end: R1's normal edit** (S3 onward: G03 BELLY FAT, B0427 card with "So skip the belt.", G04 subscribe),
   re-timed to the new opening length.

## Chroma key: the standard changed on 2026-10-21

R1 used the Codex R3 key. The house standard is now **Claude's Bill Maher R2 key**: `.claude/skills/_shared/chroma-key/README.md`
(method `reference/ds40-claude-r2/`, `calibrate.py` on excerpts, `keyonce.py` to key each piece once, gate with
`mcflicker.py` and `measure_r2.py`). Re-key C1729 (talking pieces) and C1730 (watching) with it; calibrate plate, crop rows and
hold-out boxes (watch, glasses) to these rolls. Claude's Bill Maher R3 (`/Volumes/Expansion/_edit_work/ds40/r3/`) is building
almost this exact opening (clip full screen, Dan small, then large): read its notes and reuse its layout code if it fits.

## Where things are

- R1 work and recipe: `/Volumes/Expansion/_edit_work/DS-33/r1/` (moved off the full Extreme drive). `recipe/` has prep, framing,
  render_key (R3 key, superseded), captions, graphics, assemble (`card()` for rounded clip cards on the light field), gateplan,
  page. Delivery copy: `Short-form video content/Ronaldo Ab Belt - DS-33/` (notes, reviews 4 and 5, recipe copy).
- R1 film timeline: ad + watching 0-10.38; talk P1a (take 1, C1729 14.62-19.44), P1b (19.84-20.70), P2 (50.84-70.34),
  P3 (76.14-90.20), P4 (93.35-97.50), P5 (101.50-105.98); P3/P4 audio joined by a 40 ms crossfade. Words on the film
  timeline: `words_out.json`.
- Ad source: `r1/src/l3re1wcd0Bg.mp4` (720p) and `l3re_audio.webm`.
- Five R1 independent reviews: `r1/ROUND-1-REVIEW*.md`. Known gate rows on this pipeline: `audio:stamp` (tone) and
  `captions:sync` (-450 ms on 5 cues; the real offset is ~+35 ms); report, never tune.

## Steps

1. Rename the chat `Ronaldo Ab Belt SFC R2`; `queue.py set DS-33 in_progress --by Claude`; board entry.
2. HD search for the ad; then key calibration on excerpts (watching piece with the laptop included, and one talking piece).
3. Show Dan a **first-30-seconds draft** of the new opening (full-screen intro with Dan small top left, then the split
   with the silent ad above him to ~27-30 s), with the measured key and framing checks, on a review page. Short-form rule:
   if everything else is already approved and nothing new is uncertain, build the whole Short in this round instead.
4. Full build, every gate (audio, delivery, watch pass with a fresh judge), independent review (fresh `ra-reviewer`), VLC copy
   in `Videos to Review/`, review page, `queue.py set DS-33 delivered`, revision list with timestamps in chat.
