# Handoff: Website conversion video — REVISION 4

**Created:** 2026-09-08 (Dan's rev-3 review) · **Runner:** Fable 5.1, extra-high effort (Dan's standing choice for this
video) · **Skill:** `/ad-edit` (read lessons 82–107 first) · **Budget:** ~$12–18 of AI video generation (Veo), see §3
**Working dir (all intermediates, on the Extreme drive):** `/Volumes/Extreme/_edit_work/website-video-828/`
**Delivered rev 3:** `claude edited long form content/06 - Website Conversion Video (post-generation)/website_video_16x9.mp4`
(rev 1 and rev 2 beside it as `*_REV1_REJECTED` / `*_REV2_REJECTED`; rev 3's recipe is in `recipe/`)
**Reference for audio and look:** `Muhammad Ad Videos/this picture got me abs | muhammad | 16x9.mp4`

## ⚠ THE ONE THING THIS REVISION IS ABOUT: THE TOP OF DAN'S HEAD IS CUT OFF, AND IT MUST NEVER BE AGAIN

Dan, 2026-09-08: *"My hair is cut off in the opening scene here and throughout the video. Fix this. We have space above
my head. Never cut off my hair or below my shorts line. Crop so that the top of my head isn't going off screen …
Do a thorough double-check afterwards and make sure the top of my head is never, ever cut off … The most serious
issue with this video is the cropping issue. We have to resolve this. If the video's top is cut off, it's basically
not usable."*

**Measured cause (this session, 2026-09-08).** Rev 3 anchored every crop to a "head top" that was really his
**hairline**. The skin detector needed `r > 120` and only fired 60 px below the true skin edge; the 40 px "hair
allowance" it subtracted came from the same bad grid frame as rev 2's y=40. On his tallest frames the detector said
296–300 (4K px); the **real top of his hair is at 196–215** (`pv/hair_measure.jpg`, contrast-stretched 4K crops with
a 50 px grid — the line sits 90 px inside his hair). His hair band (hair top → skin) is **64 px of 4K**, not 40.
Result on the delivered rev 3, re-measured against the true hair top: **23 of 26 holds crop the hair, by 17–50 px at
1080p** (per-segment table in `pv/hairtrack_probe.json`; the three "clear" holds are detector misses, treat all 26 as
cut). And the rev-3 QC "headroom on the delivered frames" check passed 21–95 px because **it measured to the same
wrong point** — a gate built from the same detector as the plan cannot see the detector's bias (lesson 107).

## Dan's rev-3 review, verbatim (2026-09-08)

> Here are the revisions. My hair is cut off in the opening scene here and throughout the video. Fix this. We have
> space above my head. Never cut off my hair or below my shorts line. Crop so that the top of my head isn't going off
> screen. Video: I also want you to use a little bit closer crops. Avoid that super wide crop, and again, don't cut off
> the top of my head ever. Do a thorough double-check afterwards and make sure the top of my head is never, ever cut off
> and we're never in that super wide crop. At 19 seconds, when I say, "Imagine yourself taking off your shirt at the
> pool," I want you to show a ripped man between 30 and 50, white and Asian, someone who represents the prospect taking
> off a shirt at the pool. His wife looks at him with admiration. Other people around the pool look at him with
> admiration. Make an AI-generated clip visualizing that moment for the prospect. Generate a second AI-generated clip of
> someone who looks like the prospect, again smiling, feeling good because he's ripped and he has abs. Make this a
> shirtless clip, maybe running on the beach or something that shows he's happy, healthy, and feeling good. Clip of
> tracking macros at 56 seconds. We have another short ad from long form, which is currently working on a better version
> of this clip. Wait for the short ad from long form to finish, and then get the clip from them of the better AI macro
> tracking with the more complex meal (where we have the payoff of showing the actual calories and logging it at the
> end). 2:04, I want you to insert another kind of triumph clip series of someone who looks like the prospect (a white or
> Asian man between 30 and 50) who's following a workout program and a diet program and getting great results.
> Visualizing that success for the prospect, that they're locked in with this customized program and they're happy with
> their results. 2:17-2:44. I want a series of AI clips of the successful prospect: a white Asian man between 30 and 50,
> ripped and shirtless with six-pack abs, meal prepping some healthy meals with the food he likes, where he's happy with
> his results. He's eating the food, it's delicious, and he loves it. Make another series of AI clips and put them in
> here to visualize the prospect's success with the nutrition program. 248. When I start naming all the features, I want
> you to slowly scroll through the app members' home screen so they can see all the different features available.
> The most serious issue with this video is the cropping issue. We have to resolve this. If the video's top is cut off,
> it's basically not usable. We cannot cut off the top of my head. We also want to avoid the ultra-wide shot. Never use
> that ultra-wide shot. It's just too much of me on the camera, not broken up. We want to break that up with the AI clips
> that I mentioned here.

**Verdict, in order:** (1) the hair is cut off in every hold — unusable until fixed; (2) the wide level is banned and the
crops get a little closer; (3) AI clips at 0:19, 0:26, 2:04, 2:17–2:44 and the members-home scroll at 2:48 to break up
the talking head; (4) the macro-tracker clip at 0:56 gets swapped for the better one when the short-ad session delivers
it. **Audio is APPROVED and unchanged. The cut (incl. the rev-3 repeat fix), grade, 4K base, captions, and the
lower-third geometry are unchanged.**

## ❓ One reading to confirm with Dan before rendering (do not block on it — the default is stated)

"Never cut off my hair **or below my shorts line**." Two readings; the default below is his own rev-1 definition of the
two frames he likes (*"between my head and my belly button … the top of my head and my shorts visible, with the counter
barely visible"*): a NEAR level that ends at the belly button and a FAR level that shows the waistband and a sliver of
counter. **If Dan means the frame bottom must never go below the waistband**, make the FAR level 1.58× (bottom ON the
waistband, 4K y≈1509–1577) instead of 1.46×; everything else stands. Ask in the delivery message, ship the default.

## 0 — What is locked and must not change

- **Audio chain, verbatim:** `audio3.py` in the work dir (fitted EQ, expander, no compressor, bed −44 dB, gain +
  limiter). Dan: "This is the audio that we want." The shared gate (`_shared/audio/audio_gate.py`) PASSED rev 3 and
  must PASS again on the exact delivered file, A/B rebuilt and sent. ⚠ The skill's reference copy of `audio3.py` is now
  a shim to `voice_chain.py` (audio-unification session); the chain that actually shipped is the work dir's file /
  git `2d182f4`. Use the work dir's.
- The EDL, `tight_cuts.json` (with rev 3's manual cut), `base.mov` (4K), `tight.mov`, the grade, the six lower thirds
  at the bottom (`LT_BOTTOM`), `MV_LIFT=290`, the card designs (`gfx2.py`), the BEFORE/TODAY timing from rev 3.

## 1 — FRAMING (most serious): anchor to the HAIR, closer levels, no wide

### 1.1 Measure the hair top, not the hairline — and prove it before touching a crop

Replace the skin-only head detector with a two-stage **hair-top** detector (`hairtrack.py`, new), on the 4K base
frames (`pv/_htb/`, 960×540 = 4K/4, band 4K x 1900–2060, i.e. columns 475–515):

1. **Skin start** = first row (from the top, rows ≥ 40 4K) where ≥ 50 % of the band is skin with a RELAXED test
   `r > g+10, r > 55, g > b` (the old `r > 120` fired 60 px late on his shadowed forehead).
2. **Hair top** = climb upward from the skin start while the row's mean luma stays below the **doorway header's luma
   minus 3** (measure the header on the same frame, rows 100–150 of the band: it reads ≈(34,38,37), his hair
   ≈(26,28,25) — 8 levels darker and neutral). Stop at the first row that is back at header brightness.
3. **Sanity:** the climb must be **55–75 px of 4K** (measured 64 on every validated frame). A sample whose climb is
   shorter is a MISS and is discarded — **a failed climb reads the hair top LOW, which is the dangerous direction here**
   (the opposite of the look-down misses in the skin track). A segment with no valid sample fails the build.
4. **Validate visually at native scale before anything renders:** a proof sheet of the 8 tallest samples AND 4 median
   ones, contrast-stretched 4K crops (x 1580–2380, y 0–700) with a 50 px grid and the detected hair line drawn — the
   line must sit ON the top edge of his hair in every tile (`pv/hair_measure.jpg` this session is the pattern; the
   rev-3 proof sheets were 480 px tiles where a 90 px error was invisible — lesson 107). Put the sheet in the delivery.
5. Keep the rev-3 machinery: per-segment MINIMUM over the base track AND the delivered-scale refine track
   (`headtrack_refine.py` re-pointed at the hair detector), keyed to the keeps signature.

Measured this session for the level math (4K px): hair top **196** at his tallest, **~284** median, ~340 slouched;
skin/hairline 260–272; waistband **1580–1600**; belly button ≈ 1290–1320 (under the tank top — use 1300);
counter top ≈ 1700; the light from x ≈ 3565 (guard 3530 unchanged).

### 1.2 Two levels, both from Dan's own rev-1 definition; the wide is deleted

`y0 = (segment's minimum hair top) − 0.04 × h` — 4 % above the HAIR at his tallest instant (≈43 px at 1080p; rev 3
used 3 % above the hairline and that is how the hair went). x centred on 1980 except PIP.

| level | zoom | crop w×h | bottom edge at hair 196 / 264 (4K) | shows |
|---|---|---|---|---|
| **NEAR** | 1.85× | 2076×1168 | 1317 / 1385 | hair → belly button (his "head and belly button") |
| **FAR** | 1.46× | 2630×1480 | 1617 / 1685 | hair → waistband + a sliver of counter (his "shorts visible, counter barely") |
| **PIP** | FAR geometry at x0 = 1980 − 0.65·2630 = 270 | 2630×1480 | same | Dan at 65 %, phone beside him |

NEAR/FAR = 1.27× punch — a real framing change across every join. **There is no WIDE level; assert it** (`LEVELS`
has exactly NEAR, FAR, PIP; max crop width 2630; `qc.py` re-asserts on `CROPS`). Alternate NEAR/FAR strictly; the
hook opens on FAR (he needs the room for the name lower third), the AI inserts (§3) now cover many of the joins, so
recompute the punch plan AFTER the insert beats exist (inserts are `covered` beats; forced boundaries at their edges).
Width 2076 at NEAR is still a downscale from the 4K.

### 1.3 The gate that would have caught rev 3 — on the DELIVERED frames, independent of the plan

New `qc_frame.py` check (replaces the rev-3 headroom check, which measured to the hairline):

- Run the two-stage hair detector on the delivered 1080p master every 0.25 s wherever Dan is on camera (skip card
  beats ±0.6 s; band = Dan's centre for that segment). Report the hair top in px below the top edge.
- **FAIL if any valid sample has hair within 20 px of the top edge, or if the top 12 rows of the head band are
  hair-coloured (luma below header −3) on any sample** — that second test does not depend on finding the hairline at
  all, which is the point.
- Per segment, the minimum must be 30–70 px (anchored, not loose); median over the video ≤ 75 px.
- Proof frames: the six tightest and three loosest, at native 1080p crop, into `pv/` and the watch strips; and the
  executor LOOKS at them. Dan's screenshot at 0:05 of rev 3 is the reference failure: hair against the edge.

## 2 — Closer, and never the wide

Already implied by §1.2: the widest crop is 1.46× (rev 3's WIDE was 1.256× with the counter filling the bottom third).
Dan: *"It's just too much of me on the camera, not broken up. We want to break that up with the AI clips."* The
break-up is §3; the FAR level is the widest thing that may ever appear.

## 3 — AI clip inserts (Dan's placements, this is a change of brief: rev 2 said "every insert real")

All timestamps are on the current tight timeline (= rev 3's delivered timeline). Anchor every beat to the PHRASE
(`beats.at()`), never the second. Full-frame inserts, 0.5 s fades, `AI-GENERATED` tag **upper-left at 1.5×** (lesson
17, full-frame rule), captions stay on (the clips carry no text) and lift clear of the tag if they collide (QC 10 covers
it). Every clip: a white or East-Asian man **30–50**, visibly ripped with a six-pack, **NOT a model, NOT anyone famous**
(lesson 49), matched ethnicity across the set, same ambience density across all clips (Step 4.5), handheld / overcast /
slightly-off framing vocabulary, no lettering on garments. **Never a before/after in any clip.** Stills first for
each clip (nano-banana via `_shared/gemini-image.js`, ~$0.13), check hands/faces/signage, then image-to-video with
**Veo 3.1 Fast via `GEMINI_API_KEY`** (`:predictLongRunning`, 6 s, 720p, 16:9, ≈$0.90/clip; `lastFrame` unsupported;
the RAI filter trips on flirtation — write "his wife smiles at him, proud" not anything sexual; filtered attempts are not
charged). Key reachable 2026-09-08 (`models.list` 200); **probe credit with the first still** — Gemini prepaid ran dry on
09-01 (memory `provider-credit-outages`). Kling on Replicate is the fallback and drains too.

| # | tight time / phrase | clips | brief |
|---|---|---|---|
| A | **0:19–0:25** "Imagine yourself taking off your shirt at the pool and revealing the same rock hard abs" | 1 (6 s) | the prospect pulls his t-shirt off at a backyard/hotel pool; his wife, on a lounger, looks up proud and pleased; two or three other people around the pool glance over, impressed. Daylight, overcast or open shade, amateur-photo realism. |
| B | **0:25–0:30** "And picture how good you feel if you were in peak health with your stubborn belly fat finally lost" | 1 (6 s) | the same man, shirtless, jogging along a beach at an easy pace, smiling, relaxed shoulders — healthy and happy, not posing. |
| C | **2:04–2:14** "Once our AI has all this information about you, it can design you a truly personalized workout plan. And when you're following a plan designed precisely for your body and your goal, you'll get far better results." | 2–3 (≈10 s) | the prospect training with the plan on his phone (glancing at it between sets), a home-gym or commercial-gym set, focused; then a quiet moment of satisfaction — towel, water, a small nod. Locked in, not triumphant-cheesy. No mirror before/after. |
| D | **2:26–2:44** "Your AI will also customize your eating plan to focus on your favorite healthy foods … work around any allergies … a meal plan that you can actually follow" | 3 (≈18 s) | the same ripped man, shirtless in his kitchen, meal-prepping food he clearly likes (grilling chicken and vegetables, portioning into containers), tasting it and loving it, eating happily at the counter. Dan asked for 2:17–2:44; the NUM3 lower third ("3 — A nutrition plan built for you") runs 2:16–2:25 — **recommendation: keep Dan under NUM3 and run the clips from "Your AI will also customize" (2:26)**; if Dan prefers the clips from 2:17, drop NUM3's second line to a chip or move it onto the first clip. Say which in the notes. |

Costs: 7–8 clips + stills ≈ $8–10 at first pass; with one regeneration each ≈ $16. **Stay under the $25 session cap,
and any single batch over $15 needs Dan's go-ahead — split into two batches (A+B+C, then D).** Log spend in
`notes.md`. Track every clip in `reference/demo-clip-log.md` (the "3–4 uses then regenerate" rule).

## 4 — The macro-tracker clip at 0:56 (swap when it lands)

Dan: *"We have another short ad from long form, which is currently working on a better version of this clip … the more
complex meal (where we have the payoff of showing the actual calories and logging it at the end)."* As of 2026-09-08
evening there is no board entry and no work dir for it yet — it is the `/shortad-from-longform` session working on
Muhammad's ad ("Mohammed's ad short version" in Dan's session list). **Do not block rev 4 on it.** Check
`AI_COORDINATION.md`, `Muhammad Ad Videos/this picture got me abs - ad 1/` and
`.claude/skills/shortad-from-longform/reference/` for the new recording; if it exists, drop it into the MACRO beat
(0:55.8–1:09.6) through the same phone PiP (`layout.py pip`, `MACRO_SRC` slices re-measured off its contact sheet:
photo → analysing → itemised with the calorie payoff and the log tap at the END). If it does not exist, render rev 4
with the current PiP, say so in the notes, and swapping it later is a one-beat re-render (`pip` → `mix` → audio →
captions → gates). ⚠ Whatever the recording is: scan it for the banned screens (side-by-side before/after, the
email-capture form) before it goes in — QC 8 runs at full frame rate on the delivered file for this reason.

## 5 — The members' home screen scroll at 2:48

Dan: *"When I start naming all the features, I want you to slowly scroll through the app members' home screen so they
can see all the different features available."* Beat: **2:46.2 "We also have an AI sleep coach, the ability to tweak
your goal picture later in the app, if your goal changes, and much, much more" → 2:52.6** (≈6.5 s; "So, how do you know
it works? You don't have to take my word for it" follows on camera, then the TRIAL card at 2:56.3). If the scroll needs
more room, start it on "And that's just the beginning" (2:44.5). No such recording exists in
the asset library (`02 App Screen Recordings and Screenshots` has generate / macro / supplement flows only) — capture
it: the logged-in member home on absbyai.com, on the Apple-review demo account, phone viewport, ONE slow continuous
scroll top → bottom over ~12 s (the /make-ad product-capture recipe via the iOS Simulator, or Chrome mobile emulation
at 2× DPR; `simctl io recordVideo` / screen record). Show it as the phone PiP beside Dan (FAR-geometry PIP level, same
mask/plate as the macro beat), retimed to the beat. Compliance before use: **the hub must not show a side-by-side
before/after or an email form.** ⚠ `server.js` (~line 5400) mirrors `users.before_image` / `after_image` into the
member-hub HOME hero — check what the demo account's hero actually renders; if it shows both, start the recording
BELOW the hero (lesson 45 / Step 4: before → something else → after, never together, not even inside real app UI);
a stray generation on the demo account steals its hero — don't generate, only scroll. If a feature tile
looks lame at 433 px wide, Dan wins over the screen (lesson 84) — say so rather than shipping it.

## 6 — Delivery checklist (do not skip)

1. `hairtrack.py` proof sheet checked BY EYE at native scale before any render; new QC hair gate exists and FAILS on
   rev 3's delivered file (prove the gate on the known-bad file first, as rev 3 did for its two checks).
2. Punch plan recomputed after the insert beats; no WIDE; NEAR/FAR alternation; `hard_splices.py` intersect as before.
3. Audio gate PASSED on the exact delivered file, A/B rebuilt; `qc.py` all checks incl. caption clearance (lifted cues
   vs lower thirds AND vs the AI tag), headroom-to-HAIR, banned screens at full frame rate, the stamp.
4. `watch.py`; exact-grab contact sheet (`sheet.py`) checked for: hair at the edge, any wide frame, black field, caption
   touching a graphic; **plus the human pass: play the review copy and look at the top edge of every talking-head
   hold**. Dan asked for a thorough double-check — do it twice, once by the gate and once by eye.
5. Deliver over the same filename; keep rev 3 beside it as `*_REV3_REJECTED.mp4`. Send the 540p review copy + A/B +
   the hair proof sheet.
6. `notes.md` (spend, clip log, the NUM3 choice, the macro-clip status), coordination entry, commit the recipe + skill.
   Dashboard: Dan's rule since 2026-09-08 is that handoff rows are added only when he asks — check the board for a
   rev-4 row before checking anything off.

## 7 — Things NOT to do (four reviews, distilled)

- **Never anchor a crop to anything but the measured TOP OF THE HAIR, validated by eye at native scale on his tallest
  frames.** A detector line that "looks right" on a 480 px tile can be 90 px inside the hair. Hairline ≠ hair.
- **A QC built from the same detector as the plan cannot catch the detector's bias.** The delivered-frame gate needs an
  independent test (hair-coloured pixels in the top rows) that does not depend on finding anything.
- **Never the wide level.** 1.46× is the widest crop that may appear; the light and the wide-shot asserts stay.
- **Never a frame edge through his hair, and never below the shorts line on the FAR level (default) — see the reading
  question at the top.**
- Audio: don't touch it. Graphics: the rev-3 set stays; the new material is the AI clips and the two phone PiPs.
- Never a before/after anywhere, including inside an AI clip or the hub recording; tag every AI clip.

## Starter prompt (paste into a fresh session)

> Execute `Handoffs/handoff-20260908-website-video-rev4.md` with `/ad-edit`. It is revision 4 of the website conversion
> video from the 8/28 shoot. The one thing that matters most: rev 3 cut off the top of Dan's hair in every hold because
> the head tracker measured the hairline, not the hair — the handoff has the measured hair-top numbers, the two-stage
> hair detector to build, and the two levels (1.85× hair-to-belly-button, 1.46× hair-to-shorts-line, no wide). Build
> the hair detector and prove it on a native-scale proof sheet of his tallest frames BEFORE rendering, and build the
> delivered-frame hair gate and prove it fails rev 3's file. Then add the AI clip inserts at 0:19, 0:26, 2:04 and
> 2:26–2:44 (stills first, Veo 3.1 Fast, ≤$15 per batch), the members-home scroll PiP at 2:46–2:56, and swap the
> macro-tracker clip at 0:56 if the short-ad session's better recording exists. Audio stays exactly as rev 3. Send the
> 540p review copy, the audio A/B and the hair proof sheet when every gate is green, and ask Dan the one framing question
> at the top of the handoff.

Recommended: **Fable 5.1, extra-high effort** (Dan's choice for this video). Budget: **≈$12–18** of Veo/nano-banana
generation, in two batches under $15 each; everything else exists.
