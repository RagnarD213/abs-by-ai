# SL-12 Keep Your Muscle, A/B asset review

Dan chose A and B only on 2026-11-02. Exact new A opening: "Here's why lifting weights is mandatory if you're taking weight loss medication." It needs a studio/clip-on-mic recording; no replacement voice was authorized. See `Docs/SL12_PICKUP.txt`.

This recipe builds **asset-context excerpts only**, not final Shorts. Runtime and decisions: `/Volumes/Extreme/_edit_work/SL-12/round1/`. Review: http://127.0.0.1:9954/ . Source is the locked RO-01 R10 master, SHA256 `fa99ac5b8b7dfdd704d3256aa54c156acc842b54e77e3814e2f149579c7b631f`. Source look/mix stay approved. No upload; parent-public gate is Dec 6, 2026, 9 AM Chicago or later, verified public first.

Run from project root through renderq: `packet.py`, then `qa_excerpts.py`, then `page.py` and the managed review server. `packet.py` reuses shared HyperFrames title/recap templates and SL-03/SL-15 geometry, with Wav2Vec2 CTC matching SL-09's method. Graphic review precedes complete assembly. Final rendering should adapt the existing finished-master Shorts recipe, preserving this exact approved asset set and adding the actual A pickup. Do not treat these snippets as finished Shorts.

## Traps caught before delivery

- The background composition must be 1080x1920. A 310-high header alone makes the entire overlay canvas only 310 high. Probe dimensions and exact frame count before any review; the driver asserts both now.
- Poppins header font line boxes can overlap while native glyphs are separate. At 88px type use 1.0 CSS line height with half-leading position compensation (y104/200 and eyebrow51) to preserve the approved glyph positions. Independent native still inspection measured an 11px gap; explicit intentional-overlap metadata is on header text spans only. Shared templates/gates were untouched.
- Decode parent BT.709 and untagged HF BT.601 separately to RGB; composite in RGB, then encode BT.709.
- A source's declared picture timing can differ by five frames from its actual cut. Full native review caught the presenter tail in A's exercise span. Use continuing motion from the same approved graded `ro01/assets/dan-pushups.mp4`, offset0.1678. Reference match MSE5.61, about40.6dB PSNR. Never fill the tail with a frozen frame.
- A teaching card must cover the whole intended excerpt, including its last native frame. A's 12-frame presenter island was removed by extending actual HF motion. B's new card starts before the original study graphic; native frame88 otherwise leaks a cropped source graphic.
- Decimal input length 16.38s rounds UP to 491 frames. Its effective overlay clock can extend just past the decimal boundary, causing a one-frame final presenter flash. Pad the card enable window past the excerpt end, with enough real moving card frames. Recheck the exact encoded tail; do not rely on requested decimal duration.
- CTC's two low-scoring "you're gonna" words agree with independent source Whisper word onsets within 53ms. The source actually says "gonna". Do not force "going to" into two unspoken caption words.

## Evidence and remaining work

`excerpt-qa.json`: exact dimensions/fps/frame counts, source PCM correlations0.999964–0.999982; not an audible listen. `still-review.json` and `repaired-excerpt-review.json`: independent native reviews, no remaining visible excerpt defects. The original findings and hashes remain in `excerpt-independent-review.json`.

Audio module selftest ran with four missing-fixture/reference-path failures, recorded in `audio-selftest.log`. No threshold or voice chain changed. Complete-file audio/delivery checks are still required on final Shorts. These previews have no final delivery stamp or Dan approval.

No new AI generation or metered calls. Source roll sidecar built locally, no Gemini description, $0.00. A intro is real B0031 curls with the approved SL-07 brightness treatment. A ends on complete decline-push-up action. B uses a phone-readable calculation card. Covers remain a later setup task.
