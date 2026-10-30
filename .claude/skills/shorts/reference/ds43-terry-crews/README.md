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

## Round 2 (Dan picked off the cuff; work folder `r2/`, reuses r1's key, audio and source caches by symlink)

Dan's three notes: the laptop must show while he watches, shirtless jacked Terry above him right after the intro, more flexing behind the physique line.

- **Laptop lid layer:** `key/laptop_layer.npy` is the median of the lid across the watching piece, masked below a fitted line along its top edge. It sits at the watch scale flush to the frame bottom, in front of his hands, so Dan keeps his R5 size and hair overlap. Shrinking Dan to fit the real laptop in frame would expose the camera's left and right edges.
- **Panel reel:** `prep_reel.py` builds a silent 1080x608 reel; `reel_bg` plays it behind Dan from the reply on. `S1`/`S2` became `panelresp` shots at two scales, so the zoom cuts survive. A second plate carries the plain title, since the footage is no longer Business Insider's.
- **Reel clips are found footage, so check them hard.** Every failure this round came from them: a shot that was really a phone recording of a monitor, an ad sign in frame the whole time, a readable product, a shot running one frame past its source cut (a flash), and a shot opening mid-dissolve. Before rendering: view the first and last frame of every shot, and scan the built reel for frame-difference spikes against the intended cut list. A contact sheet does not show any of this.
- Land reel cuts exactly on Dan's cuts or well clear of them; two cuts two frames apart read as a stutter.
- Do not re-render until the reel passes. Each full render plus re-judging took about an hour on a loaded machine.
