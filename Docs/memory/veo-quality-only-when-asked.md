---
name: veo-quality-only-when-asked
description: Veo 3.1 Quality (10x Fast credits) only when Dan names it; Fast is the default for every AI clip
metadata:
  type: feedback
---
Use Veo 3.1 Fast for every AI clip. Veo 3.1 Quality only when Dan asks for it by name: never "just in case", never as a twin take, never in an unrequested bake-off.

**Why:** the 10,000-credit Ultra allowance ran out in three days (2026-10-20 to 10-23); 48 Quality clips used two-thirds of the logged credits, and Fast won or tied every blind test. Dan, 2026-10-25: "let's make that the standing rule."

**How to apply:** `veo.py add --model quality` refuses without `--dan-asked "<his words>"`. Rule text: `.claude/skills/_shared/veo/README.md`. Related: [[veo-subscription-first]], [[ai-clips-subscription-ask-before-paying]].
