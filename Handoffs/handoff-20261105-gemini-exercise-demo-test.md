# Handoff: Gemini test, three AI-Dan exercise demos for the Abs By AI app (2026-11-05)

**Who:** Gemini (Dan's Google AI Ultra account: Gemini app with Nano Banana Pro for stills and Veo for video, or Google Flow).
**Authorization:** Dan asked for this test on 2026-11-05 ("give me a handoff document to have Gemini try doing three of these. I want to see if Gemini can handle this"). Use the subscription only. Do not pay for anything and do not ask Dan before starting. Do every step yourself.
**Why:** Claude ran a three-exercise pilot on Flow the same day and none passed quality review. Dan wants to see whether Gemini, driving its own tools end to end, does better.

## The three exercises (none has a demo yet)

| id | name | what the demo shows |
|---|---|---|
| `db-hammer-curl` | Hammer Curl | Stand tall, dumbbells at sides, palms facing each other. Curl with a neutral grip, elbows pinned to the ribs, torso dead still, lower under control. Common mistake: elbows drifting forward. |
| `db-floor-press` | Dumbbell Floor Press | Lie on the floor, knees bent, feet flat, dumbbells pressed over the chest. Lower until the upper arms touch the floor (elbows about 45 degrees from the torso, not flared to 90), brief pause, press back up. |
| `bb-hip-thrust` | Barbell Hip Thrust | Upper back on a bench, padded barbell over the hips, feet flat. Drive the hips up until the torso is level with the floor, chin tucked, squeeze the glutes at the top; ribs stay down, no overarching. Lower under control. |

## The character and the look (fixed, do not change)

- **AI-Dan:** the character in this reference photo. Reproduce his face with high fidelity (facial structure, eyes, nose, smile lines, short black-and-gray faded haircut, skin tone). Lean and shredded, not bulky, the same size as the reference.
  Reference: https://drive.google.com/file/d/1QW0JR0bsX2IHJsxKbBT-PEZ2acbRnSDK/view (on the Mac: `Media/exercise-demos/_character/ai-dan-canonical.jpg`).
- Plain black athletic tank top with the white "Abs by AI" shield logo and text on the chest, black shorts, black athletic shoes.
- The same bright modern gym: floor-to-ceiling windows, gray weight machines.
- One person only, a locked-off tripod camera, photorealistic, 16:9, full body head to feet, a calm relaxed face with lips closed (no toothy grin), no talking.

## What each finished demo must be

A silent 16:9 1080p video loop of **one clean repetition** that repeats seamlessly. The app plays it on loop under a voice-over that Claude adds afterwards.

1. **Start and end frames first.** Make a START still (the rest position) and an END still (the far end of the movement), the END made as an edit of the START so the camera, gym and body proportions stay identical. Name every joint angle and contact point in the prompt. State depth aggressively; polite wording comes back shallow. Name the wrong answer when a pose keeps coming back wrong ("this is NOT a ...").
2. **Video from both frames** (Veo with first and last frame), one direction only: "from the very first frame to the very last frame the movement progresses in ONE direction only, at a steady controlled speed; he never pauses partway, never reverses slightly and continues, never does a partial repetition first, never bounces, never makes small adjustment movements." Keep the camera and every machine still.
3. **One repetition, then loop:** cut the clean one-way stretch, then play it forward and reversed (rest, top, rest) so the loop is seamless. Do not change the speed with frame dropping or frame blending (both looked wrong in the Claude pilot); pick the take whose own tempo is 2.5 to 4 s for the full rep.

## The quality bar (what the reviewer will fail)

- **The chest print must read "Abs by AI" in every frame.** This sank the Claude pilot: Flow renders at 720p and upscales, and the small print garbled ("Kim by t") in every full-body side-view take. Try native 1080p generation, or framing where the chest faces the camera so the print is large.
- Feet stay planted exactly where they start (no sliding or skating). Hands keep their grip. No limbs merging, no extra fingers, no shoes doubling.
- Dan's settled form standards: curls have elbows tucked against the ribs and a vertical torso, and any hip swing is a reject. Presses stop just below 90 degrees at the elbow, never a deep flare. Full range to a named endpoint (hip thrust: torso level at the top).
- No background machine moves on its own (weight stacks pumping with nobody on them are a known AI fault).
- Dan's bar for any AI clip of him: would it pass as real camera footage of a calm man? Anything that reads as AI slop is a fail. Regenerate rather than patch.

## Deliver

For each exercise, put into one Google Drive folder named "Gemini exercise demo test 2026-11-05" (shared "anyone with the link can view"):
- `<id>-start.png`, `<id>-end.png`
- `<id>-take-N.mp4` for every video take generated (raw, unedited)
- `<id>-loop.mp4`, the finished seamless loop
- `<id>-notes.txt`: model and settings used, number of attempts, what went wrong, and generation credits used (read the balance before and after)

Then reply with the folder link and one line per exercise: delivered or not, and why.

## What happens after (Claude, not Gemini)

Claude downloads the folder, runs the house frame gate, motion checker and an independent reviewer on every loop, adds Dan's cloned voice-over, builds the app files, and puts any that pass on a review page next to the Claude pilot result. Pilot report for comparison: `Docs/EXERCISE_DEMO_FLOW_PILOT_20261105.md`.
