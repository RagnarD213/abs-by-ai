# DS-43 Terry Crews Fasting SFC R1: two-version reaction build and lessons

Reaction Short in the locked Codex R5 format, cut twice from one shoot roll (scripted and off the cuff) with a shared opening.
Work folder: `/Volumes/Expansion/_edit_work/DS-43/r1/`. `build.sh VERSION` runs one version end to end; `AUDIO_ONLY=1` remixes and
re-burns captions on the existing picture; `gates.sh VERSION` reruns the gate tail. Key: `run_key.sh`. Page: `page.py` + `review/notes.json`.

## Lessons (each cost a rebuild)

- **A long pause can be a restart.** Whisper stretched "I" over a gap and hid "And what I'm... And what I love". Energy alone called it a
  pause, and the reviewer agreed. Before cutting a pause mid-sentence, read the lips on both sides and transcribe the delivered audio.
  Cutting into the second attempt doubles the phrase while the captions hide it. Same trap off the cuff: "If you want, ... if you want to".
- **Check the clip itself for repeats.** News and interview clips often lift a cold-open hook from later in the same video. The silent
  panel must start after that repeat AND after its burned subtitle card clears, or the panel replays the hook.
- **Read the library note, not only the search hit.** `clip_library.py show <ID>` carries bans; A0086 is banned from verticals.
- **A peaky clip cannot be levelled with gain alone.** Peak-capped plain gain left Terry's clip 7 LU under Dan and the film below -15 LUFS.
  Two gentle compressors at 4x rate (no limiter) bring the crest factor to about 14.
- **Key checks: choose T0 so the key and source frames pair.** `-ss` rounds up while `key_frame` rounds to nearest, so a T0 near x.5 frames
  pairs them one frame apart and reads as a bad key (motion-compensated ratio 1.86 against a true 0.75). Confirm with a pixel correlation
  at offsets -2..+2 before believing a bad number.
- **Off-cuff joins: end before the in-breath, start in the quiet before speech.** Pieces ending inside a breath give a level jump at the cut.
- **Card rule:** enter a lower third no more than 0.35 s before its first line lands, or it reads as an empty frosted box. Read the label and
  the headline together: "The Myth" over a true statement reads backwards.
- **`cards` in a gate plan means full-screen cards, as [a, b] lists.** The R5 panel is partial with captions over it, so it belongs in `covered`.
- **Pipefail with a `| head` filter stops the build when grep matches nothing.** End those lines with `|| true`.
- **In the corner opening, what sits behind Dan is the clip.** Terry's lapel mic read as a set clamp beside Dan's elbow. Check the clip before masking the key.

Gate rows that stay failing on this format (reviewed, same as the approved DS-44B): audio tone (the clip's sound is in the measured window;
check the voice alone with `audio_gate.py <voice wav> --video <master> --no-stamp --reference-rows-only`), hair_top on the panel (planned
overlap), splice visibility on zoom cuts, and captions:sync (a handful of cues; compare cue starts to delivered ASR words instead).
