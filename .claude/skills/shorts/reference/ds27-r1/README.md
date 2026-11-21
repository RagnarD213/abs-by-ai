# Home Workouts SFC R1: review packet recipe

Dedicated content Short, DS-27. These are reproduction scripts, not media or approvals. Complete private work/data: `/Volumes/Expansion/_edit_work/DS-27/round1/`. Proposed final:61.428seconds,1841frames,30000/1001. No complete film exists yet.

Copy `recipe/` into an isolated work folder containing the frozen JSONs from the private review ZIP. Scripts resolve their work root as the parent of `recipe/`; do not run them in this reference directory. Source files stay read-only. Respect editcap and the shared render queue. `render.py Opening`, `render.py Equipment-context`, `render.py Daily-workouts-context` rebuild only those narrated previews from frozen data. The shared HyperFrames templates are referenced in place, never copied. `qa.py <excerpt>` creates exact-file audio/watch/delivery evidence; a numerical FAIL stays FAIL.

The historical `prepare.py` builds the early source-ASR map. Do not run it over the corrected cut's word map. Current `words_out.json` is timed from the assembled voice; `caption-overrides/Daily-workouts-context.json` comes from the exact excerpt audio so a source timestamp stretched over silence cannot drop the audible leading words.

Traps verified in this build:

- Cap every excerpt cue's padded end at the next cue start. Recreating ASS from chunks must retain that cap; otherwise two captions overlap for a frame even when the parent ASS was correct.
- A transcription window starting inside an existing word can duplicate that word when merged with the whole-roll map. Replace overlap deliberately; compare actual speech and final caption sequence.
- Check both ends of context clips. A complete word in the source can be lost by a typed excerpt endpoint, and an ASR token starting before an excerpt can still be fully audible after it.
- Map every picture boundary, including short gaps before and after B-roll. Cover the whole source seam. A0.2second camera island between a wide shot and the client insert remains a defect even when its two isolated cuts look acceptable.
- The equipment pan can crop the named kettlebell at its camera edge. Use a source range where that complete item is visible, not merely a clip whose catalog describes the whole setup.
- Shared `landing.py` supplies centres. Dense source hair samples840–924px leave more than100px in tight rendered geometry. The wider approved studio family keeps both complete blue fixtures and can conflict with legacy head-size/headroom bounds. Record that conflict; never adjust the gate.
- Preserve disagreeing model reports. Native source/frame and bounded inset/label geometry can refute a model's claimed overlap or exercise name, but do not turn the model into a full playback PASS.

R1 is a creative approval checkpoint with known audio-reference-tone, legacy framing/caption and unmeasured delivery rows. Dan's exact choices and a complete-film render, gate and independent candidate review remain required. No cover or publication is part of this edit.
