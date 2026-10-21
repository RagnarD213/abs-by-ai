# Video model watch

Monthly check (scheduled task `video-model-watch-monthly`, 1st of each month) for any AI video model, from any company,
that could beat what we use now or match it for less. Dan, 2026-10-21: *"Anything which could beat Google on quality
should be tested if you think there's a significant chance on quality ... we should be trying to test things that have
better quality, even if they're more expensive, and which could generate the same quality for cheaper."*

## The baseline to beat

- **Model:** Veo 3.1 Fast in Google Flow, Frames mode (start + end frame), 8 s, 720p generated, 1080p upscaled download.
- **Cost:** Google AI Ultra 5x, $99.99/mo (Dan subscribed 2026-10-20): 10,000 credits + 50/day; Veo Fast 10 credits, so
  about 1,000 clips a month, roughly $0.10 each. Paid fallback: Replicate Veo 3.1 Fast, $0.80 per 8 s.
- **Proven:** won or tied every pair of the 2026-10-21 blind test against Omni 1.1 Flash. Makes shirtless shots of Dan.
- **Scorecard of Dan's picks:** `python3 .claude/skills/_shared/veo/veo.py picks` (log: `~/.absbyai-video-model-picks.jsonl`).

## What a candidate must do (or it is not tested)

1. Image-to-video from our approved **start AND end frame** (start-only is a weaker fallback; say so).
2. Realistic people, including an AI likeness of Dan and shirtless shots (P6 in the standard set tests refusal).
3. 1080p output, or 720p that upscales cleanly; no visible watermark on the plan we would use.
4. Usable from this Mac: a subscription Dan can buy, or pay per clip on an account we have (Replicate first).

## When to run a blind test

- **Quality:** credible evidence it beats Veo 3.1 Fast on image-to-video with real people: a clear lead on the
  Artificial Analysis image-to-video board (https://artificialanalysis.ai/video/leaderboard/image-to-video), strong
  hands-on reviews of start/end-frame work, or a new version of a model that already came close. Price does not matter here.
- **Cost:** likely equal quality at lower total cost than the baseline at our volume (10 to 20 kept clips a day).
- A new version of a model that already lost (Omni 1.2/2.0, Kling 4, Seedance 3, Veo 4) is always worth a test.
- Leaderboard rank alone is not enough: Omni Flash 1.1 ranked 4th to Veo Fast's 16th and still tied or lost on our shots.

## How to run one

1. Generate the candidate's takes of the **standard pairs** in
   `/Volumes/Extreme/_edit_work/model-bakeoff-standard/pairs.json` (same frames and prompts) into a folder
   `/Volumes/Extreme/_edit_work/model-bakeoff-<model>-<date>/` as `P1.mp4` ... `P6.mp4`. Pay-per-clip runs stay within the
   standing AI-generation authorization ($15 a batch, $25 a session). A model that needs a new subscription: recommend it
   to Dan with price and a one-month test; Dan buys plans himself.
2. `python3 .claude/skills/_shared/veo/bakeoff.py build <folder> --name "<model>"` builds the blind page (seekable, muted,
   sides shuffled, key kept outside the page).
3. Send Dan the link. After his picks, record each with `veo.py pick --kind bakeoff`, reveal, and write the verdict below.

## Candidates already judged

| Date | Model | Result |
|---|---|---|
| 2026-10-21 | Gemini Omni 1.1 Flash (Flow) | Blind, 5 pairs: 2 ties, Veo preferred 3, Omni 0. Refused the shirtless P6 pair. 12 credits vs 10. Used only alongside Veo for >8 s, 4/6 s, one-detail fixes and multi-reference shots (`_shared/veo/README.md`). |
| 2026-10-20 | Kling 3.0 | Not blind-tested. Below Veo Fast on the blind board; already used pay-per-clip on Replicate for planted-feet exercise moves where Veo shifts the feet. Subscription not worth it at our Kling volume. |
| 2026-10-20 | Seedance 2.5 (Dreamina) | Not tested yet. 3rd on the blind board, start/end frames, about $0.32 per 8 s on Dreamina Standard; US output 720p; may block realistic faces. **Next candidate.** |
| 2026-10-20 | MiniMax H3 | 1st on the blind board; pay per second only, no confirmed start/end frame support. Re-check each month. |
| 2026-10-20 | Sora | Consumer app reportedly closed April 2026; no start/end frames; blocks real-person photos. Skip unless it returns. |

## Monthly log

Newest first, one short entry per run: what changed, what was tested or recommended, and why.

- 2026-10-21: watch set up. Baseline Veo 3.1 Fast on Ultra. Next candidate: Seedance 2.5.
