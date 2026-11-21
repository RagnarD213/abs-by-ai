# Handoff: Codex makes three AI-Dan exercise demos for the trainer app (2026-11-07)

**Type:** in-app exercise demo (not a content video, not an ad). **Owner:** Codex, newest Sol (`gpt-6.1-sol`) at high effort.
**Authorization:** Dan, 2026-11-07: "Give me a handoff for Codex to do three. Make sure they're not ones already done or in progress." Dan approved paid native 1080p Veo for these demos on 2026-11-05 ("Try paid 1080p"). Spend up to $10 of paid Veo in this run. Do every step yourself without asking. Stop only for Dan's review.
**Why:** Claude shipped three demos on 2026-11-06, Gemini is testing three and Claude has a handoff for three more. Dan wants to see what Codex can do on three different ones.

## The three exercises

None of these has been done or started. Picked 2026-11-07; Dan can swap them.

| id | name | library text (`public/exercises.js`) | camera |
|---|---|---|---|
| `db-shrug` | Dumbbell Shrug | Stand tall, heavy dumbbells at the sides. Shrug the shoulders straight up toward the ears, pause, lower slowly. Mistake: rolling the shoulders in circles. | three-quarter front, so the chest print is large and the shrug is easy to see |
| `ez-bar-curl` | EZ-Bar Curl | Grip the EZ bar at the angled sections, elbows at the sides. Curl to shoulder height, lower over about 3 s. Mistake: leaning back to swing the bar. | three-quarter front |
| `machine-chest-press` | Machine Chest Press | Seat set so the handles line up with mid-chest. Press to full extension without slamming the stack, return under control. Mistake: shoulders rolling forward. | three-quarter front, seated |

**Do not touch these**, because they are done or owned by someone else:
- Everything already in `EXERCISE_DEMO_IDS` in `public/index.html`, including chair-squat, db-lunge and bicycle-crunch.
- Gemini's three: db-hammer-curl, db-floor-press and bb-hip-thrust.
- Claude's three: db-tricep-extension, db-fly and db-crunch (`handoff-20261106-exercise-demos-three-more.md`).

## Character and look (fixed)

- **Character.** AI-Dan from `Media/exercise-demos/_character/ai-dan-canonical.jpg`, also public on Drive: https://drive.google.com/file/d/1QW0JR0bsX2IHJsxKbBT-PEZ2acbRnSDK/view. Lean and shredded, not bulky.
- **Clothes.** Black tank top with the white "Abs by AI" shield and text on the chest, black shorts, black shoes.
- **Gym.** The canonical bright gym: floor-to-ceiling windows, gray machines. Copy the setting from any shipped demo poster in `public/exercise-demos/*.jpg`.
- **Shot.** One person, a locked tripod, 16:9, full body, a calm face with lips closed, no talking.

## Method that worked (read first)

Read these before starting:
- `.claude/skills/exercisegeneration/SKILL.md`, the full house method.
- `Docs/EXERCISE_DEMO_FLOW_PILOT_20261105.md`, especially the round 3 section.
- The working folder of the shipped three, `Media/exercise-demos/_flowpilot/`. It holds `build.sh`, `finish.sh`, `gen-vo.js`, `mkpage.py`, `entries.json` and `app-staging/`. Copy these into a new folder, `Media/exercise-demos/_codex3/`.

Steps:
1. **Make the frames.** Make START and END stills with `.claude/skills/_shared/codex-image.sh` on the subscription.
   - Make END as an edit of START, then copy START's background into it with `lockstill.py`.
   - Name every joint angle and contact point.
   - State the range aggressively: shrug shoulders at the ears, curl bar at shoulder height, press arms fully straight.
   - Name the wrong pose ("this is NOT a ...").
2. **Gate the frames.** Run `python3 .claude/skills/_shared/framecheck/gate.py START END --spec spec.json`.
   - The spec needs `person: {"side": ...}`. An empty `{}` counts his body as background.
   - Set `camera: "locked"` and list the props (dumbbells, EZ bar, machine).
   - Then get an **independent review** from a fresh Claude call for every pair and every retry. Use the AGENTS.md command (`claude -p ... --model claude-opus-5-5 --permission-mode bypassPermissions`) with a brief that says: "Act as the frame-reviewer agent in `.claude/agents/frame-reviewer.md`. Review START/END <paths> against <spec>; write REVIEW.md ending in VERDICT."
   - Then run `gate.py ... --review REVIEW.md`. `veo.py add` refuses frames without a gate pass and a reviewer PASS.
3. **Generate the video.** Use paid native 1080p Veo, Replicate `google/veo-3.1-fast`, 4 s ($0.40 a take): `python3 .claude/skills/_shared/veo/veo.py api JOBDIR ID --paid-ok "Try paid 1080p (Dan, 2026-11-05)"`.
   - Give each parallel call its own job folder, because two api calls on one job collide.
   - Do not use Flow: its 720p garbles the chest print.
4. **Build the loop at native speed.** Never change speed with setpts or minterpolate; both looked wrong.
   - Cut the clean one-way stretch and make a palindrome unit (`_batch5/cutunit.py`).
   - Run the background lock: `rm -f <id>/r2-unit-preghost.mp4`, then `_r2/lockbg.py <id>`.
   - Run the stray-motion scan (`reference/ghost.py`) and the double-pump check (`reference/mono.py qcunit`). Run qcunit on a copy on the internal drive, because the Seagate's `._` files break it.
5. **Check the motion.** Run `clipcheck.py TAKE --spec --frames A:B`, then a fresh Claude frame-reviewer call on the sampled frames, then `--review`.
   - Faults seen in the pilot: a hand crossing the face; the logo garbling or morphing; the face drifting (eyes close, mouth opens, stubble appears); feet sliding; a machine moving on its own.
   - The machine chest press needs extra care: the stack and handles must move only with his press.
6. **Voice and app files.** Make the voice-over with MiniMax `speech-02-hd`, voice `R8_NE3EBC2N`, from the library's setup, execution and mistake lines, using `gen-vo.js` with a new vo json. Then run `finish.sh`, which handles:
   - room tone;
   - `audio_gate.py --synthetic --profile in-app-demo`;
   - a 960x540 mono 32 kHz encode;
   - the delivery gate, format `exercise-demo`.
7. **Attempts.** Up to 5 takes per exercise. Fix the frame or prompt between takes; don't just re-roll. If one fault repeats in 3 takes, stop that exercise and report it.
8. **Edit cap.** Run `python3 .claude/skills/_shared/editcap/editcap.py acquire EXDEMO-CODEX3` before the first generation. When the page is ready, run `release EXDEMO-CODEX3 --review`.

## Shipping bar and delivery

Dan's bar for app demos is "better than a stick figure."
1. Put the best take of each exercise on a review page, even if the reviewer fails it.
   - Start it with `python3 .claude/skills/_shared/review_server.py PORT DIR`. Re-run it after any edit, because the server caches the page.
   - Next to each video, write in plain words what is right and what is still off.
   - Check it silently: open with `?review_mode=automation` at 1080p, then call `AbsReviewAudio.handoff()` so it is left paused with sound ready.
2. In chat, give Dan:
   - the page link;
   - one line per exercise;
   - the spend, both paid Veo and subscription images;
   - the two wrap-up boxes.
3. **Install nothing until Dan says ship.** Then do it the way commits 944ef64 and 68cdd00 did:
   - Copy `<id>-vN.mp4` to `public/exercise-demos/<id>.mp4` (chmod 644).
   - Make a poster jpg at 1.0 s.
   - Re-run the audio and delivery gates on the public file, then move their stamp json files out of `public/`.
   - Add the id to `EXERCISE_DEMO_IDS` in `public/index.html` (around line 9294).
   - Push, confirm the Railway deploy, and check that the demo plays on absbyai.com.

## State at handoff

- Shipped in the app and committed locally in the main folder: chair-squat, db-lunge and bicycle-crunch. The push is blocked by the main folder's 12-file merge jam; the next successful safe-push carries them.
- Gemini's test and Claude's three-more handoff are both still open in `Handoffs/README.md`.
