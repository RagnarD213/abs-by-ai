# Handoff: WV-06 "Great Again T Upsell 3: Electro-Creatine" moves from Claude to Codex (2026-11-20)

**Type: AD** (Great Again T upsell video, shown after the GAT VSL purchase). **Round: R1 delivered, waiting on Dan.**
Next chat name: `GAT Upsell 3 AD R2` (the next round, since this is a handoff to a new task).

Why it moved: Dan, 2026-11-20, relayed by another Claude session: "Can you message all active edits here and tell them to
pause work and create a handoff document to transfer the edit to ChatGPT?" He is upgrading to the $500 ChatGPT plan because
Claude's weekly limit is nearly used up (resets Thu Nov 26). This is his explicit request to move the video to Codex.
**Do not start until Dan's ChatGPT upgrade is active and Dan says to.**

## Where everything is

- Mac: **M2 Pro** (headless; Codex there via `ssh m2 codex exec`). Job folder: `/Volumes/Extreme/_edit_work/WV-06/`
  (Extreme drive on the M2). Do all job I/O on the M2, never over the SMB share from the M6.
- Source: 11/13 green-screen shoot, roll `C1904.MP4` in `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/`,
  roll seconds about 1878-2680 (Upsell 3 section). Lav is audio stream 0 channel 0.
- Job brief: `Handoffs/video-editing/WV-06-great-again-t-upsell-3-electro-creatine.md`. Queue row: `Handoffs/video-editing/jobs.json`
  (state `draft_review`). Script: `script/upsell3.txt` (approved copy), `script/doc_full.txt`.
- Notes from the Claude chat: `RESUME.md`, `PAUSED-20261118.md`, `PAUSED-20261118-2.md`, `PAUSED_BY_DAN.json` (all in the job folder).
- The build was cloned from Upsell 1 (WV-04, `/Volumes/Expansion/_edit_work/WV-04/`), which Dan has reviewed through R3.
  When in doubt, do what WV-04 did; its round 2 and 3 notes and reviews hold his upsell feedback.

## What Dan has approved

**Nothing in WV-06 is approved yet.** Round 1 is waiting on his picks. Do not treat silence as approval.
Inherited and locked from earlier work (not reopened):
- House chroma key (Bill Maher R2), `.claude/skills/_shared/chroma-key/README.md`, calibrated on this roll (`key/cal_A/sheet.jpg`).
- Wood Kitchen 1 background, same room as the VSL and Upsell 1. Soft Blue Light cards with HyperFrames motion all the time on screen.
- Burned captions in the same style as the VSL and Upsell 1. The close framing by default, wide only under a key-point card.

## Dan's upsell preferences (from his Upsell 1 rounds and the brief; apply all of them)

- Cleaner and less busy: more Dan on camera, fewer AI clips, graphics only on key points.
- Key-point cards about 60 px type and about 880 px wide (bigger than the VSL's), above his head on the wide shot.
- Fewer cuts and longer takes. Tighten only pauses over 1 s; cut repeated restarts (use his last clean try).
- Give more options even if he rejects them (optional cards are offered, marked optional).
- Packages in V formation (1, 3, 6 tubs) and an order-page-style button look; Best Value on 6.
- The end text says tap the button BELOW the video, never "on" the video.
- Real gym B-roll first (library), colour corrected and checked in the final frame (CLAUDE.md B-roll rule).
- No em dashes in any on-screen text. AI imagery labels follow the deception-risk rule (hands-only drink needs none).

## Current state (all built, nothing running, slot released)

- Transcript and take map: `cut/words_roll.json`, `cut/medium_lines.txt`. Opening = his third read of "Hey, it's Dan again"
  (reads 1 and 2 were stopped, "Roll it back").
- EDL: `film/work/edl/edl_tight.json` (sha256 f3da8b726bf6e4eb...), 28 segments, 444.61 s (7:25). Built by `film/recipe/edl_build.py`.
  Manual splits remove "Thousands of studies" x3 (roll 2049-2055), "And if somehow you don't love" x3 (2578-2585), a double "Honestly".
- Key: ALL 13 pieces A-M keyed and plated: `key/<P>.done`, `key/logs/plate_<P>.ok`, plates `key/plates/<P>_fg_straight_alpha_ungraded_rim3.mov`
  and `<P>_lav_mono.wav`. Map film time to pieces via the EDL (src_in/src_out/cut_in/cut_out) and `key/pieces.json` (frame_t0/frame_t1).
- Voice: `film/work/voice_film.wav` (House bass chain), raw `voice_film_raw_lav.wav`. Options: `look/VOICE_WV06.json` (A untreated,
  B chain default, C house bass, D Maher bass, level matched). Colour: `look/LOOK_WV06.json` (matched, neutral, warm).
- Graphics plan: `film/work/graphics_manifest.json` (sha c189481f21d51d8e...), builders in `film/recipe/graphics.py`.
  K01-K14 key-point cards, S01 (Bemben 2001 study, shows 5.2/8.7/19.6% while he says "almost 5, 9, 20"), S02 (Nissen and Sharp 2003,
  "#1 of 250+"), P01 (real tub, Made In The USA, facility line), P02 (5 g creatine + sodium 1,000 / potassium 200 / magnesium 60 mg),
  O01 (offer, $67 struck, 1/$47, 3/$99, 6/$177 Best Value), G01 (gold 1-year seal), R01/R02/R03 real gym clips (B0624 leg press,
  B0697 incline press, B0683 curls). Optional (rec False): K03, K06, K07, K09, K11, K14, R03.
  Word "creatine" must never appear on screen before he says "It's creatine" (K08 is the reveal).
- First minute (film 0-60.83): `round1/GAT Upsell 3 AD R1 - First Minute.mp4`, sha256 **eb9f8deebab9ca99...**, 1080x1920 29.97,
  hair min 77 px, arm separation median 33, opaque frames 0. Copy in Videos to Review: "GAT Upsell 3 AD R1 - first minute.mp4".
  Audio gate: FAIL only on tone (House bass) and edt 83 vs 80 ms (untreated itself 80). Same as Upsell 1, where Dan accepted it.
  do_no_harm PASS. Baseline: `...First Minute.mp4.audio_untreated.json`.
- Context clips: `round1/context/<ID>-context.mp4` for all 23 items + XSCOOP (each item a-4 to b+4 s, real render). Stills in `round1/stills/`.
- AI idea X-SCOOP (scoop of powder into iced lemon water, hands only, no tub) for "It mixes perfectly... a cold lemon drink":
  two blind START+END pairs X1/X2, both passed the frame gate and a frame reviewer: `round1/frames/X-SCOOP/blind_set/blind/`.
  `.blind-key.json` there is private: never tell Dan which is Google or Codex until he asks for the scorecard.
  No motion generated yet (no video takes, so nothing to file in the clip library yet). AI ideas for weight/reps lines were dropped.
- Spend so far: $0.

## Review page waiting on Dan

**http://127.0.0.1:9879/** (managed `review_server.py`, M2, mirrored to M6; 200/206/seek proven; handed off paused with sound ready).
Built by `round1/review/make_inputs.py` -> `inputs/page.json` -> `round1/review/build_page.py`. His five questions:
1. Colour: Matched (rec) / Neutral / Warm. 2. Voice: House bass (rec) / Untreated / Chain default / Maher bass.
3. Key: approve or notes. 4. Cards: recommended set, add/drop by ID. 5. Drink clip: X1 (rec) / X2 / none.

## Exact next action (after Dan's reply only)

1. `editcap.py acquire WV-06 ...` (run `editroute.py`/`resume.py check WV-06` first; the job lives on the M2).
2. Apply his picks: colour/voice into the render config, card set into `graphics_manifest.json` (rec flags), caption fixes below.
3. If he picks X1 or X2: generate motion on the Google subscription (Flow) first, START+END pair, then archive every take
   (CLAUDE.md "Every generated AI clip is filed") and show the motion for approval before it goes in the film.
4. Full render: `film/recipe/render_film.py W1 --t0 0 --end 444.6108 --out <path>` through `renderq.py run --group WV-06`.
   Then audio gate with `--untreated`, picture checks, an independent reviewer pass (ra-reviewer equivalent), delivery page,
   `queue.py set WV-06 delivered`, and the Codex setup handoff on final approval. No covers, uploads or scheduling in the edit.

## Traps hit

- `key/<P>.done` is written BEFORE the plate export finishes; wait for `key/logs/plate_<P>.ok` (`render_ctx_auto.py` does).
- ffmpeg/ffprobe are not on PATH: `~/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/`.
- The audio gate needs a baseline JSON: stash with `common.stash_untreated(<file>, pcm(raw))`, else do_no_harm "NOT MEASURED".
- The M2 render queue is saturated (WV-03, WV-04 also); light steps waited up to 9 h. Use `--priority` only with a live reservation.
- Captions still need fixes: Whisper writes "Grady Gente" / "a lecture or" (Great Again T / Electro), capital "Because" mid-sentence
  at roll 2010.36, missing first words at some joins; "shows power in a man" uses the script wording. Check `captions.py` TEXT_FIX.
- `review_server.py` refused port 9810 (cached review); try ports until one starts.
- The batch ledger row chat-WV-06-R1 is terminal: do not re-enqueue it.

## Starter prompt (Codex GPT-6.2 Sol, High; only after Dan's ChatGPT upgrade is active and he says go)

```
AD (Great Again T upsell video). Name this chat "GAT Upsell 3 AD R2". You are taking over WV-06 "Great Again T Upsell 3:
Electro-Creatine" from Claude at Dan's request (2026-11-20). Read AGENTS.md, .claude/skills/_shared/VIDEO-RULES.md and
Handoffs/handoff-20261120-wv06-transfer-to-codex.md in full. The job lives on the M2 at /Volumes/Extreme/_edit_work/WV-06/.
Round 1 review http://127.0.0.1:9879/ is waiting on Dan's five picks (colour, voice, key, card set by ID, drink clip X1/X2/none).
If his picks are not in this chat yet, ask him for them and stop. Once he answers, follow the handoff's "Exact next action":
acquire the edit slot, apply his picks, make the drink-clip motion only if he picked one, render the full film, run every gate
and an independent review, deliver the review page and update the queue. Do not upload, schedule or make covers.
```
