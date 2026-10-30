# Google images on Dan's subscription (Flow, Image mode)

Google's still-image model (Nano Banana Pro) is generated in Google Flow on Dan's Google AI Ultra, driving his Chrome, the same
way `_shared/veo/FLOW-RUNBOOK.md` does for video. No API (the paid scripts stay locked; consumer plans cannot use the API).

**Status 2026-10-30: NOT YET MAPPED.** The Flow video steps are mapped; the Image-mode steps are not. The first run maps them:
follow FLOW-RUNBOOK sections 0 to 2 (tab rules, credits, project), then in the composer settings chip choose **Image**
instead of Video, pick the Nano Banana Pro model, set the aspect (16:9, 9:16 or 4:5), x1. Upload reference photos with the
section 4 file-input hook. Download each result at the standard size (never 2K/4K upgrades that cost credits). Then replace this
paragraph with the exact controls, credit cost per image and quirks you found.

Rules that hold from the start:
- Same prompt text and same reference photos as the Codex twin, so the test compares models, not prompts.
- Visible watermarking switch OFF (as for video). If a visible mark still lands on an image, report it: it would give the model away.
- A refusal (shirtless, "reputational risk") is DATA: `blind.py add ... --source google --note "refused: <reason>"` is not possible
  without a file, so write the refusal in the set folder's `google-refusals.txt` and tell the main agent. Never retry by rewording
  around a safety filter; one retry with the plain prompt is enough.
- Credits low or any new agreement/payment screen: stop and report, as in FLOW-RUNBOOK. Never pay.
- Run it as a background `flow-veo`-style sub-agent (Sonnet, run_in_background) so editing continues.
