# SL-11 R2 intro comparison recipe

Read `Docs/SL11_R2_INTRO_COMPARISONS_20261028.md` and immutable external `round2/decisions.json` first. This is the requested two-approach intro comparison, six context clips only, not complete R2 masters. The original R1 recipes and approvals stay unchanged.

`render_intros.py` copies the original title and presenter pixels, substitutes a clear-held current demo or different existing real B0428 draw-in, preserves natural speed, overlays the original caption PNGs and copies R1 AAC packets. It refuses existing output, so a resume cannot silently repeat production. B's final preview cue removes unheard following words only at the excerpt endpoint.

`check_intros.py` verifies AAC packet identity, runs the shared audio gate verbatim against the exact R1 excerpt, decodes every output frame, samples hair at less than0.25s, runs the shared title check and prepares shared watch packets. Dark pixels at the top of an outdoor source can be hedge, not hair; actual person masks plus independent native inspection determine hair containment. Preserve the initial raw-dark alert and raw measurements; no global gate change or threshold relaxation.

`gate_intros.py` refuses unjudged watch logs and runs current shared delivery gates. `page.py` preserves the original R1 page, builds two context players per Short and defaults all players to muted. Task playback checks must verify actual mute before every play/seek/switch/recovery and finish paused/muted; manual unmute stays available. Refresh9411 through the managed review server after any page change.

Acquire the SL-11 edit slot before any production and run each script through the shared render queue. Original locked decisions are not edited to record progress; supplemental round execution/progress files preserve the revision disposition. New Dan picks require the round controller. Exact source/output hashes, native dense frames, independent findings and automated logs are in `/Volumes/Extreme/_edit_work/SL-11/round2/`; no media is committed here.
