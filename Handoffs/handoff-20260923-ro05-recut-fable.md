# RO-05 recut from scratch in Claude (Fable 5.1): "How I Make My Daily Salad"

**Written 2026-09-23 by Claude (Opus 5.5) after Dan rejected Claude's cut.** Executor: Claude Code session, **Fable 5.1, effort high** (Fable's monthly spend limit was hit on 2026-09-23; if it is still exhausted, use Opus 5.5 high and say so). Job: RO-05 on
`Handoffs/video-editing/00-MASTER.md`. Goal: a publishable 16:9 organic first cut, 10-15 min, that looks like Muhammad edited it.

## 0. Status and what went wrong
Claude (Opus 5.5) cut RO-05 on 2026-09-22/23. After ten revision rounds the r10 file passed the audio gate 13/13 and Dan rejected
it on 2026-09-23: *"Overall, this is not up to standard. This is not usable. This is not something that we can publish."* He is now
running this recut twice, once in Claude (Fable) and once in Codex (Astra). Start from scratch: do NOT reuse the rejected picture,
grade, graphics, SFX or framing. DO reuse the verified facts and assets in section 4; they cost hours to establish.
Rejected file for reference only (what not to do): `claude edited long form content/07 - How I Make My Daily Salad (Claude r10 REJECTED 09-23)/`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (especially the new section
"RO-05 rejection"), `.claude/skills/_shared/EDITOR-CARD.md` (section C is this job).

## 1. Dan's verdict, his words (2026-09-23)
- **Colour:** "the color correction on this looks off to me. It doesn't look up to Muhammad's standard. It looks a little bit washed out.
  The colors aren't as saturated. I want this to look like Muhammad's video as much as possible. The first thing that we need to work on
  is the color correction."
- **Transitions / SFX:** "I also don't like the transitions. We're back to that swiping sound effect, but I really hate that swiping sound
  effect... never, ever use that swiping sound effect for anything. We need to make the transitions like Muhammad's transitions in the
  AbWheel video. I have a few more examples of his transitions."
- **Graphics:** "The graphics also look very basic and very bad. I don't like the graphics at all. We need to make the graphics the same
  as Muhammad's... We need Muhammad's graphics."
- **Hook:** "For the intro, I want an attention-getting clip. If you have a good clip of me opening the salad and taking a bite out of it,
  or just showing the salad to the camera... I want to see the finished product right at the beginning of the video."
- **Hair:** "my hair frequently goes out of the frame... just include as much of my hair and my head as you can, but I want you to
  double-check that we're not unnecessarily cropping out my hair when it was in frame in the filming."
- **Calories:** "I don't think these calorie estimates are correct. They seem way too low. Double-check those calorie estimates when I
  upload the app clip."
- **3:56 broccolini:** "The shot of the broccolini at 3:56 is a little awkward. I want to use a different shot, or maybe even just a
  clip of broccolini there."
- **English cucumber:** "you missed the main point of what I was saying, which is that it maintains better in these kinds of salads
  when it's cut than the American cucumber. I want to maintain that point in the video."
- **5:27 look-away:** "I'm looking away from the camera as I'm talking. I want you to see if there's a better clip that you can use
  there where I'm looking at the camera."
- **Effort:** "putting effort into it, not doing the color correction, not getting the cropping right, not doing the graphics right,
  that's a big waste of tokens. We need to avoid making any videos like this in the future."

## 2. The mistakes Claude made (avoid every one)
1. **Grade.** Reused the old 8/3 "crush blacks, lift mids" curve so the tracking demo matched. Result: median luma 0.38, saturation
   0.27, flat and washed out. Muhammad's kitchen ads measure median 0.22-0.27 with saturation 0.23-0.39; the approved Codex C1652
   kitchen cut 0.23 / 0.32. Raw rolls here: black 0.035-0.052 (milky), median 0.27-0.38, p99 ~0.79-0.94.
2. **SFX.** A synthesised whoosh or riser on every graphic and cutaway. Banned forever; `sfxlib.whoosh()`/`riser()` now raise.
3. **Graphics.** Built my own layouts on top of Codex's primitives (white bars with olive tabs, "KEY POINT" tabs, numbered ingredient
   cards with dark sub-bars, a full-screen stat card, olive gradient title cards). Dan: "very basic and very bad".
4. **No hook.** Opened on the talking intro; the finished salad first appeared at 11 minutes.
5. **Hair.** Punch-ins were anchored to 3-5 sampled hair tops; on handheld footage his head moves, so crops cut hair the camera had
   captured. Several takes are also framed tight by the operator (not fixable, but never make it worse).
6. **Cut the cucumber's point** ("American cucumber gets mushy... this stays rock solid seven days from now").
7. **Kept an awkward handheld broccolini hold-up** (C1543 ~141-147) and a look-away during the onion tips (C1544 ~137-145).
8. **Calorie cards** used the old app recording's per-ingredient figures (arugula 5, carrots 17, tomatoes 8, broccolini bag 37, onion 9,
   pico 6, olives 11, chicken 173, eggs 162, olive oil 252, vinegar 0, adobo 3; 683 per salad). Dan says they look too low.
9. **Process.** No style checkpoint: rendered the full 15 minutes, then chased gate rows and reviewer defects for ten rounds (framing
   flips, L-cuts, GoPro patches) on a cut whose look Dan rejected on sight.

## 3. Non-negotiables for the recut
1. **Order of work (do not skip):** (a) grade: 6 stills side by side with Muhammad frames, hitting his numbers; (b) graphics + transitions
   style board rebuilt from his actual frames; (c) ONE finished 60-90 s sample section (hook + intro + the arugula step) compared side by
   side against Muhammad; (d) only then the full cut. Put (a) and (b) in the early approval packet to Dan with the B-roll previews
   (`_shared/ASSET-APPROVAL.md`), so he signs off the look before the tokens go into a full render.
2. **Colour:** grade per roll toward median luma ~0.22-0.28, median saturation ~0.32-0.39, blacks at 0, highlights to ~0.98, skin natural.
   Method that matched him before: percentile-matched per-channel curves (`/Volumes/Extreme/_edit_work/abwheel/mrepro/grade_fit.json`
   approach) and the approved C1652 LUT `Media/codex-video-trial/06-organic-r4/assets/source-grade.cube` as a starting point for this
   kitchen, then adjust by measurement. The split-screen demo camera side gets the same grade.
3. **Transitions:** Muhammad's. Reference master: `YouTube Long Form Video Content/The $17 Ab Wheel Beats Every Crunch - READY FOR UPLOAD/
   Muhammad edit/The $17 Ab Wheel Beats Every Crunch - Muhammad edit v2 HD - READY FOR UPLOAD.mp4`. Measured before
   (`/Volumes/Extreme/_edit_work/abwheel/mrepro/notes.md`): white/blue bloom flashes with a double-pulse envelope (silent), whip-pans with
   real directional blur inside cards, hard cuts otherwise. **Ask Dan for his additional Muhammad transition examples before building.**
   No swipe/whoosh/riser sound, from any source.
4. **Graphics:** Muhammad's own, rebuilt from his frames: Poppins Bold pills (white pill + olive #768642 text + olive left tab, or olive
   gradient pill (141,152,97)->(84,93,55) + white text), line 2 revealed by a per-character typewriter fade (~28 cps), numbered chips
   bottom-left, thin white form-cue bars top-centre, frosted stack panels building one item at a time, title cards (near-black grid
   (10,11,5) + corner brackets, olive gradient plate, white BoldItalic caps wiping in with motion blur, key line in a white highlight
   box), instructional media in rounded glow cards. Existing reproductions to start from: `/Volumes/Extreme/_edit_work/abwheel/mrepro/`
   (`orglib.py`, `schedule.json`, `FINAL_mstyle.mp4`, `ab/final/ab_*.png` his-vs-ours stills) and
   `Media/codex-video-trial/06-organic-r4/muhammad_graphics.py`. Graphics distill the point; never over his face or hair (measure on
   rendered frames); follow Dan's KEY POINT wording rule only inside Muhammad's pill design.
5. **Hook:** open on the finished salad. Verified clips: C1550 111.0-113.5 and 115.0-119.5 (dressed salad with the fork, hero close-up),
   C1551 0.0-5.0 (bowl close-up, then Dan's bite and smile, "All right, ready to eat. About to take a bite."), C1550 94-99 (plate
   presentation, headless, weaker). Then the intro (C1535 3.36-38.52, last and most complete take).
6. **Hair:** measure the hair top every 0.25 s across each whole shot (Vision person mask, `shorts/reference/recentre/personmask`);
   a crop's top edge must sit above the highest hair point of the shot or the shot is not punched. Where the operator cut the hair, show
   everything the source has. Horizontal footage stays static (no tracking).
7. **Calories:** Dan will upload a new app clip. Use its numbers; do not show per-ingredient calories from the old recording. If the new
   clip is not available when you reach graphics, ask Dan once, and meanwhile build ingredient pills with names only.
8. **Beat fixes:** 3:56 broccolini: replace the handheld hold-up (C1543 ~141-147) with the broccolini on the board (C1543 ~150-195) or the
   GoPro angle. Cucumber: keep C1543 230.18-240.3 AND 244.44-252.44 ("A traditional cucumber, an American cucumber, is going to get kind
   of mushy seven days from now. This is going to be rock solid seven days from now..."). Onion tips look-away (C1544 ~137-145): there
   is only one take of this section; cover the look-away with onion B-roll (C1544 158.6-164.5 chopping, or the GoPro angle).
9. **Length:** 10-15 min (the rejected cut was 15:06). Keep every ingredient and its reasoning.
10. Standing rules: lav only through `_shared/audio`; SRT sidecar, no burned captions or watermark; no banned app screens; delivery gate
    + watch pass + independent full review before Dan; never raise a threshold.

## 4. Verified facts and assets (reuse; do not rediscover)
- **Script:** Shoot 3 doc `1VeNXATtvHBVe_Y5S3fxmSjllZxva0zwgo5NghW-G_bU`, item 7 (outline; Dan spoke off the cuff).
- **Rolls:** `/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/`. C1533 grocery lineup B-roll (38 s); C1534-C1535 intro takes
  (use C1535); C1536 why (fasting, salad bar); C1537 parts (veg, protein, toppings); C1538 dressing + "I'll show you how I track" (70.66-82.24);
  C1539/C1540 abandoned demo takes; C1541 the demo take; C1542 arugula; C1543 carrots, tomatoes, broccolini, cucumber; C1544 cucumber peel +
  onion; C1545 top-down bowl B-roll (18.5 s); C1546 containers/OXO; C1547 box up, day one, final chop, spices; C1548 oil, vinegar, toss, chicken
  bag; C1549 chicken + eggs + toppings; C1550 olives, pico, toss, finished bowl, hero (108-121); C1551 bowl + bite; C1552 make it your own;
  C1553 "track your macros" reminder (extreme close-up); C1554-C1556 CTA takes (use C1556; skip 67.44-77.46 "our clients" lines).
  Every roll has a Whisper sidecar: `<roll>.roll/words.json`, `<roll>.roll.md`, `contact.jpg`.
- **Take map to start from (not binding):** `.claude/skills/longform-edit/reference/ro05/ranges.py` (119 ranges). Word-edge traps found:
  "Next is the protein" starts at C1537 29.8 (Whisper misses "Next"; use 29.55); oil line: keep C1548 8.16-9.12 "Number one," then 10.55
  "this olive oil has 120 calories" (9.45-10.3 is a false start "oil has"); cucumber "thinner" ends 240.23, the orphan "and" starts 240.5;
  closing C1556 "Thank you, thank you for watching" from 89.15; "salad But let's talk" at C1536 85.8 has no gap (start at "let's", 85.83).
- **Audio:** the lav is **channel 1 on every roll**. `pick_lav.py` picks channel 0 on C1538 and C1550 by arrival time, but a 10-band tone
  match against neighbouring rolls proves channel 1 (0.5 dB vs 2-3 dB off; ~9 dB cleaner). Settings that passed `audio_gate` 13/13 (Dan did
  not criticise the audio): `voice_chain.py` with the fitted EQ in `.claude/skills/longform-edit/reference/ro05/run_r10.sh`, `deesser=i=0.25`,
  `--bed-db -40 --tp -4.0 --oversample 4`; bed Pixabay "Organic Flow" `/Volumes/Extreme/_edit_work/abwheel/r2/music/organic_flow.mp3`
  (swell only where nobody talks). The lav clips often; a lid-clamp snap at C1548 ~81.88-81.99 overshoots after AAC (softened -6 dB over
  140 ms fixed it).
- **GoPro second angle:** `/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/gopro 2/GH010270.MP4`, `GH020270`, `GH030270` are one continuous
  counter-level recording (1920x1440, 30 fps; chapter lengths 1060.5013 / 1060.5013 / 1306.7 s). Audio-synced offsets per camera roll in
  `/Volumes/Extreme/_edit_work/ro05/sync/offsets.json` (gopro time = offset + camera-roll time; covers C1539-C1550; lens covered from gopro
  time ~2380 s). Head is out of frame by design; crop 1280x720 at (320,0) to lose the bottles, bowl and blurry granite.
- **App demo:** rebuild from raw, never reuse the old 05 master's pixels (30 fps, drifts 0.58 s). Camera `C1541.MP4` + screen
  `Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4` (1320x2868, 60 fps) with the 05 per-beat sync map (camera start ->
  screen start): (33.70,8.0) (48.96,24.0) (60.42,36.0) (66.32,41.0) (71.36,47.5) (74.60,53.0) (81.76,57.0) (86.94,63.0) (88.82,66.0)
  (100.86,78.0) (117.04,93.0) (146.50,121.0) (160.64,134.5) (172.58,138.0) (201.98,183.0) (237.96,214.5) (288.08,256.3) (299.58,270.0).
  Screen crop `crop=1320:2500:0:175`. **Banned screens in that recording:** home screen with Dan's before/after side by side at screen
  8-23 s and 286-293 s; iOS "Undo Typing" dialog at 254.8-256.0 (hence 256.3 above). The iOS photo picker and camera are fine. During the
  dictation (C1541 ~146.4-157) Dan holds the phone in front of the camera: show the phone screen full-frame there.
- **Hook / B-roll inventory (each distinct moment used once):** C1550 111.0-113.5, 115.0-119.5 (hero); C1551 0.0-5.0 (bowl + bite);
  C1545 0-18 (top-down bowls: best 4-7.5, 10-14.5); C1533 13.5-19 (vegetable lineup), 31.8-36.8 (oil and vinegar bottles), 1.0-3.4 (eggs,
  olives, chicken); C1548 91.0-93.3 (sealed bowl toss), 116.7-122.5 (chicken out of the bag); C1549 194.0-196.6 (egg pack); C1547 7-37
  (boxing up 7 salads, time-lapse).
- **Old app numbers** (screen recording, for comparison only): per salad 683 cal, 39.3 g protein, 17.1 g carbs, 51.3 g fat; Dan weighed
  ~720. See 3.7.
- **Colour measurements** (median luma / median saturation): Muhammad Ad 1 0.22/0.23; Ad 6 0.27/0.39; Codex C1652 0.23/0.32; rejected r10
  0.38/0.27; raw C1552 0.30/0.24.
- **Gate rows that are known false positives on this footage** (report them, never tune): `captions:burned` fires on egg whites, onion
  highlights and the phone keyboard; `cut:splice_visibility` fires on hard cuts between setups. The three framing rows fail on the
  operator's own tight framing.
- **Also wanted:** the handoff for DS-16 "How To Lose The Last Ten Pounds" uses this shoot's salad footage; note good ranges in your notes.

## 5. Tools, work dir, delivery (Claude)
- Skill: `/longform-edit` (read its new top warning first), shared modules `_shared/audio`, `_shared/deliver` (gate + watch),
  `_shared/rolls/roll_sidecar.py`. Graphics/transition reproduction: start from `mrepro/orglib.py` and Muhammad's frames.
- Work dir: `/Volumes/Extreme/_edit_work/ro05-fable/` (never write into `ro05/`; copy what you need). Two-build machine cap applies.
- Queue: `python3 scripts/edit-queue/queue.py set RO-05 in_progress --by "Claude (Fable recut)"`, then mirror with Artifact write_db
  (`.claude/skills/_shared/edit-queue/README.md`). Codex is running the same job in parallel on purpose (Dan's bake-off); do not stop it.
- Deliver to `claude edited long form content/08 - How I Make My Daily Salad (Fable recut)/`: master `How I Make My Daily Salad | fable |
  16x9 | RO-05.mp4`, `.srt`, chapters, REVIEW 540p, audio A/B, stamps, notes, recipe. Send Dan the review copy; set `delivered`.

## 6. Starter prompt
> Read `Handoffs/handoff-20260923-ro05-recut-fable.md` in full, then `Handoffs/video-editing/00-RULES.md` and `.claude/skills/_shared/VIDEO-RULES.md` (the "RO-05 rejection" section). Recut "How I Make My Daily Salad" (RO-05) from scratch with /longform-edit, in the order the handoff sets: grade stills, then a Muhammad graphics and transitions style board, then one finished 60-90 s sample section, sent to me in one approval packet with the B-roll previews, then the full 16:9 cut. Match Muhammad's colour, graphics and transitions; no swipe sound; open on the finished salad; never crop hair the camera captured. Every gate, watch pass, independent full review, then deliver master + SRT + chapters, send me the review copy, update the master list.
