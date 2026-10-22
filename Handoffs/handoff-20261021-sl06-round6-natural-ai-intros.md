CONTENT | SL-06 | Top 5 Zepbound Tips SFL R6

# SL-06 R6: regenerate all six AI intro clips so they look natural (relaxed closed-mouth smile, no shaking, no flexing)

Written 2026-10-21 by Claude (Opus 5.5) from the "Top 5 Zepbound Tips SFL R5" task, after Dan rejected R5's six intro clips.
**Recommended: Claude Opus 5.5, high effort** (this video started on Claude; AGENTS.md "video stays with the AI it started on").

## Dan's reply (verbatim): `/Volumes/Extreme/_edit_work/sl06/round6/DAN_R5_NOTES.md`

> all of these clips are rejected... the smile is weird. We need just a regular, relaxed, closed-mouth smile. He's also shaking
> and flexing too hard. Regenerate all of these clips: no shaking, no flexing, closed mouth, relaxed smile. Make it look natural...
> This looks like AI slop... be a little more picky about what you bring to me for review and regenerate if you get some slop.

New standing rule from this: VIDEO-RULES top section "AI clips of Dan look natural, or they never reach review" (commit 14aae16)
and memory `ai-clips-natural-or-regenerate`. Read both first.

## What stays (do not redo)

- The six shorts' bodies (round 2, approved), C's two credited YouTube clips (Seattle Children's 2.84-5.77, SynergenX 5.77-9.56,
  zoom 1.2 framed low so the needle shows above the Step 1 bar), F's intro ending at o1.93 (the pause after "appetite,"),
  title band off during every intro, AI-GENERATED chip positions, the approved poster/gym/vial look and poses.
- Build: `/Volumes/Extreme/_edit_work/sl06/` (`batch.py`, `plans.py` COVERS `ai_intro` entries point at `clips/intro_{S}.mp4`;
  swap the files, nothing else). Repo copies: `.claude/skills/shorts/reference/softblue-sl06/` (README sections "Round 4" and
  "Round 5 motion" hold every trap).

## Why R5 failed (so R6 does not repeat it)

- The approved frames carry a wide toothy grin, and the prompts asked for a "proud grin" and "squeeze the flex tighter": Veo
  produced a growing grin, a straining arm and tremor. Then `mouth_hold.py` pasted a held smile over C, E, F, which read as fake.
- The gate and reviewers checked vanishing objects, talking and text, never "does this look like a real relaxed person".

## The work

1. **Frames (Codex subscription, `_shared/codex-image.sh --model gpt-6.1-sol --effort high`):** edit each intro's start frame to
   a regular, relaxed, CLOSED-MOUTH smile and a calm, un-strained hold of the pose (arm up showing the vial, muscles relaxed, not
   squeezing). For A, B, C, E start from the approved END frames (fingertip already on the poster's corner): Veo kept moving a
   pointing hand near the body to his chest. F keeps its start-frame pointing; D keeps the double biceps. Everything else in the
   frame stays (poster text, vial, calendar, gym, shorts height, D's leaner build). Gate (`framecheck/gate.py`, a `still` spec
   is enough since the motion is minimal) and a fresh `frame-reviewer` each. Default reading of "no flexing": keep the approved
   poses but held loosely with no squeeze; if a take still reads as straining, also try the vial held up at the shoulder with
   the arm relaxed, and show Dan that option on the page.
2. **Motion on the Flow subscription** (`_shared/veo/veo.py add` START only, 9:16, then the `flow-veo` agent; Dan's Flow has
   "Return silent videos" ON; tell the agent to confirm 9:16 before EVERY submit, the selector resets). Prompt for stillness:
   "holds the pose calmly, relaxed closed-mouth smile the whole time, lips together, gentle breathing, a slight natural weight
   shift, no squeezing, no trembling, the pointing fingertip stays on the poster's corner". No talk/speech words. **3 to 4 takes
   per clip**; keep only the most natural. Credits: check first; if out, ask Dan once (paid Veo 3.1 Fast: $0.60 per 6 s take,
   with negative prompt "trembling, shaking, straining, flexing harder, grinning, teeth, talking, mouth moving, pointing at
   himself, looking down").
3. **QC, stricter than R5:** `fix_take.py` for the vial label and D's calendar only (text restores are allowed); **no mouth or
   face patching**. Measure tremor: track the vial and the fingertip frame to frame and reject any take whose high-frequency
   jitter is visible (compare against the start-frame hold). `clipcheck.py` + a fresh `frame-reviewer` per take whose brief asks,
   at playback speed, "does this look like real footage of a relaxed person, or like AI?"; an AI answer is a FAIL. Look at each
   take yourself at speed before sending it on.
4. **Rebuild the six** under one render-queue slot each: `renderq.py run --label "sl06 render S" -- nice -n 5 python3 batch.py render S`
   (without it a render crawls), then `deliver_watch.sh S` (check its log shows the AUDIO GATE and plan lines; a silent failure
   left round 2's plan once), a Sonnet watch judge, `rungate.sh S`, then one fresh `ra-reviewer` on all six.
5. **Page:** a round6 page on port 8821 (copy `round5/page_r5b.py`; `review_server.py 8821 --remove` then re-register), new frames
   beside each short, each intro's watch range. Replace the R5 copies in `Videos to Review/` with `Top 5 Zepbound Tips SFL R6 - ...`.
   No covers, no upload.

## State at handoff

- R5 deliverables (rejected intros): `Short-form video content/zepbound-tips-short*.mp4`, `Videos to Review/Top 5 Zepbound Tips SFL R5 - ...`,
  page http://127.0.0.1:8821/. Intro takes and tools: `/Volumes/Extreme/_edit_work/sl06/round5/` (`veo/`, `fix/`).
- Spend so far: $1.20 paid (A10, B10, Dan's OK). Flow credits were near zero on 2026-10-20 (shared with other jobs).
- Stale round-2 duplicates were moved out of the Short-form folder to `round5/stale_r2_duplicates/`.

## Starter prompt

> Name this task "Top 5 Zepbound Tips SFL R6". This is CONTENT. Read `Handoffs/handoff-20261021-sl06-round6-natural-ai-intros.md`, `/Volumes/Extreme/_edit_work/sl06/round6/DAN_R5_NOTES.md` and the new top section of `.claude/skills/_shared/VIDEO-RULES.md`, then execute it: regenerate all six AI intro clips so they look like natural footage (relaxed closed-mouth smile, no shaking, no flexing), starting with closed-mouth frames made on the Codex subscription and motion on my Google Flow subscription. Be picky: several takes per clip, no mouth patching, reject anything that looks like AI. Rebuild the six shorts, run the gates and an independent review, and give me one page. No covers, no upload.
