---
name: no-swipe-sound-effect
description: "Sound effects are judged, not banned (Dan 2026-10-08): the old bright swipe/whoosh stays out, a low soft swoosh on a picture transition works; he wants to try it on Claude and Codex edits"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 21112e48-5a70-4369-a359-fcd1f0d8e3fd
  modified: 2026-10-08T21:52:14.379Z
---

Sound effects on transitions are a judgment call, not a blanket ban.

**What Dan said, 2026-09-23 (RO-05):** "I really hate that swiping sound effect. We need to remember this going forward: never, ever use that swiping sound effect for anything." That was about ONE sound: our synthesized bright, hissy sweep (centred near 4,100 Hz), fired on graphics coming in.

**What Dan said, 2026-10-08 (Zeeshan's Video 5 round 2):** a review asked the editor to take the swoosh off his zoom transitions, citing the rule above. Dan deleted that item: "I thought the sound effect to use on transition actually worked, and in fact, this is something that I want to try on Claude and Codex edits in the future... Not all sound effects are bad, just the ones that we used previously that didn't work. These, I feel like, work, so use a little bit more judgment and subtlety with sound effects rather than just saying no sound effects on transitions as a blanket rule going forward."

**Why:** the first rule was written down wider than what he said (my interpretation: "that swiping sound" became "any sound on any transition"), and it then got enforced against a sound he likes.

**How to apply:**
- The approved one, measured: low and soft (centred near 230 Hz, 95% of energy under 800 Hz), about 0.5 s, about 9 dB under his voice, only on a picture move (a zoom between shots). Reference, never to publish: `Media/sfx/transition-swoosh-reference-zeeshan-video5.wav`.
- Still out: `sfxlib.whoosh()` / `riser()` (they raise; do not unblock), sounds on lower thirds, chips or labels, anything bright, loud or constant.
- Reviewing an editor: never ask for a transition sound off because a rule says so. Item only if it is harsh, loud, mistimed or on graphics; if unsure, one line under "For Dan's call" in the summary.
- Our own edits: he wants to try it. Same character as the reference, picture transitions only, shown to him in the first-minute review the first time a format uses it.
- General lesson: when recording a rule from Dan, keep its scope to what he actually named.

Rule text: `_shared/VIDEO-RULES.md`, "Sound effects on transitions". Related: [[ro05-salad-cut-rejected]], [[motivation-style]].
