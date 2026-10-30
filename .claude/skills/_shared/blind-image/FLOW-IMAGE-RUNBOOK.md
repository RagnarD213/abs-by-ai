# Google images on Dan's subscription (Flow, Image mode)

Google's still-image model (Nano Banana Pro) is generated in Google Flow on Dan's Google AI Ultra, driving his Chrome, the same
way `_shared/veo/FLOW-RUNBOOK.md` does for video. No API (the paid scripts stay locked; consumer plans cannot use the API).

**Status 2026-10-30: MAPPED** (first run: three 9:16 Nano Banana Pro images, DS-43 covers, balance 24,162 before and after).

Steps (viewport about 1543x784; find controls by label if coordinates drift):
1. FLOW-RUNBOOK sections 0 to 2: own tab, avatar menu shows credits and Visible watermarking (was OFF), home page **New project** (click by `find` ref, a coordinate click on the banner did not work). Agent pill is grey by default in a new project.
2. Click the settings chip at the right of the prompt box. Popover: **Image | Video** toggle, aspect row (16:9, 4:3, 1:1, 3:4, **9:16**), model dropdown (**Nano Banana Pro**, Nano Banana 2 Lite, Nano Banana 2.1 default), count **x1..x4** (default x2), and "Generating will use N credits". Choose Image, 9:16, open the dropdown and pick Nano Banana Pro, x1. Settings persist for the project. Escape closes.
3. Reference photo: install the file-input hook from FLOW-RUNBOOK section 4, click the **+** left of the Agent pill (asset picker), **Upload media**, `find` "file input", `file_upload` the JPEG, wait about 4 s, click the asset row, **Add to prompt**. The reference chip shows in the prompt box.
4. Type the prompt (click the text area first), click the round arrow. Each submit CLEARS the prompt and DROPS the reference chip: for the next image press **+** again, click `identity-reference.jpg` in the list (the list re-sorts as new results appear, so look before clicking), **Add to prompt**, then type. No re-upload needed in the same project.
5. A 9:16 image finishes in about 20 to 30 s (tile shows a percentage, then the picture). Generations can queue back to back.
6. Download: click a tile to open the editor (filmstrip of all results at top, switch by clicking a thumbnail), click the download arrow top right, choose **1K Original size** (2K and 4K are "Upscaled": never click). It lands in ~/Downloads as `<auto title>_<hash>.jpg`, 768x1376 for 9:16. Convert with `sips -s format png`.

Cost: Ultra showed "0 credits" for Nano Banana Pro x1 and the balance did not move across three images (24,162 before and after). No agreement or payment screens appeared. No visible mark was on the saved images with Visible watermarking OFF (the invisible SynthID mark is not visible).

Rules that hold from the start:
- Same prompt text and same reference photos as the Codex twin, so the test compares models, not prompts.
- Visible watermarking switch OFF (as for video). If a visible mark still lands on an image, report it: it would give the model away.
- A refusal (shirtless, "reputational risk") is DATA: `blind.py add ... --source google --note "refused: <reason>"` is not possible
  without a file, so write the refusal in the set folder's `google-refusals.txt` and tell the main agent. Never retry by rewording
  around a safety filter; one retry with the plain prompt is enough.
- Credits low or any new agreement/payment screen: stop and report, as in FLOW-RUNBOOK. Never pay.
- Run it as a background `flow-veo`-style sub-agent (Sonnet, run_in_background) so editing continues.
