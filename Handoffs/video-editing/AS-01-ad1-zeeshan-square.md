# AS-01 — Ad 1 "This Picture Got Me Abs (Zeeshan's cut)": 1:1 square full + ≤0:59 square cutdown

**List 3 · ad variant · BLOCKED: Dan hasn't approved the Zeeshan Ad 1 vertical yet (delivered 09-10, audio untouched).** Read `00-RULES.md` first.

## What a square is here
A 1080×1080 **re-layout of the approved vertical build**, not a third recovery of the editor's cut. It keeps the vertical's
timeline, EDL, beats, grade, labels, caption timing and audio **bit for bit**, and reuses its `cut_plan.json` for the cutdown.
Only the geometry and the per-beat renderers change. Copy the approved vertical build dir to `_edit_work/AS-01/`.

**Read, in order:** `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` (the square translation rules), `Handoffs/handoff-20260911-square-ad1-zeeshan.md`,
`.claude/skills/shortad-from-longform/SKILL.md` [S1] START HERE + `reference/a11_sq_ad1/` (the approved Ad 1 square template),
and `.claude/skills/_shared/framing-motion.md` (steady wider shots, updated 09-16). The Ad 3 square R2.1 (`_edit_work/ad3-sq-r2/`,
uploaded 09-16) is the most recent approved square. Its `notes-square-r2.md` records what Dan rejected in R1.

## This ad's specifics
* Source vertical: `Zeeshan Ad Videos/this picture got me abs - ad 1/… | claude | 9x16 | ad 1.mp4` + 59s; build `/Volumes/Extreme/_edit_work/ad1-zee-vert/`.
* **24 fps**, not 29.97. The email-capture screen at 188.75–190.33 s is replaced (keep the vertical's replacement). His audio verbatim.
* ⚠ YouTube `rimBWjT9-oo` / `JOZVk4_HDwQ` carry the rejected audio. Replacing them is an `/ad-setup` step after approval, not this job.
* **Low priority:** Muhammad's Ad 1 already has an approved square live. Confirm with Dan that he wants a second Ad 1 square before building.

## Gates and deliver
Every gate on both delivered files at the current `GATE_VERSION`, the independent audit, then
`Zeeshan Ad Videos/this picture got me abs - ad 1/this picture got me abs | claude | 1x1 | ad 1.mp4` + `Zeeshan Ad Videos/this picture got me abs - ad 1/this picture got me abs | claude | 1x1 59s | ad 1.mp4`, REVIEW 540p copies, the audio A/B vs the approved
vertical, stamps, `notes-square.md`, `recipe-square/` into the ad's folder. Send Dan the review copies.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AS-01-ad1-zeeshan-square.md`: first confirm its blocker is cleared, then build the 1:1 square and ≤0:59 square cutdown of Ad 1 as a re-layout of the approved vertical build with /shortad-from-longform [S1], same timeline, grade, labels and audio, steady wider framing, labels off my face and abs. Every gate, independent audit, deliver, send me the review copies, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table) and `Handoffs/handoff-20260914-ad3-square-codex.md` (the Ad 3 square you built, which Dan shipped: reuse its method), then execute `Handoffs/video-editing/AS-01-ad1-zeeshan-square.md`. Confirm the blocker is cleared first. Deliver, send Dan the review copies, update `00-MASTER.md`.
