# Review history — what Dan rejected, in his words, and the rule each one became

Six rounds on the first website conversion video (2026-09-01 → 2026-09-09). Read this before cutting: it is the
list of things Dan looks for, and every item is now a gate or a checklist line in `SKILL.md`. Rev 6 was approved
("you nailed it, this is perfect, this video is finalized").

| rev | what Dan said | what it actually was, measured | the rule now |
|---|---|---|---|
| 1 | "the two-channel issue" on the audio | Not the mics. `loudnorm` went DYNAMIC (premix could not reach −14 linearly), a −23 dB bed sat 9.5 dB over his floor, a 3:1 compressor with makeup and two air shelves. | Measured gain + `alimiter`, never loudnorm. Bed ≤ −44 dB. No compressor. EQ fitted to HIS file per roll. Gate rows: floor, tone, comb, L/R. |
| 1 | "I don't want to use this wide shot ever… shot in 4K intentionally so we have room to punch in" | The full kitchen frame with the light in shot. | No wide level exists. Every crop asserted narrower than FAR and left of the light. |
| 1 | "a graphic on the left and a huge amount of black space… just a bunch of text, generic… horrible" | J2 panels on a near-black field. | Graphics sparingly. App screens as phone PiPs beside Dan; cards fill the frame. No plate on black. |
| 1 | the trainer screen with stick figures: "awful" | The workout list with SVG exercise icons. | If a feature looks lame on screen, don't show it. Today: only exercises with real AI demos, stick figures off. |
| 2 | "very, very bad crop" — headroom | 168–232 px of headroom at 1080p; crops anchored to a frame grid, not to his head. | Crops anchored to the measured head, later the measured HAIR (rev 3). |
| 2 | the repeated line at 0:32 | Whisper stitched a restart into one 1.75 s token; orphan scan passed because the token covered the energy. | `repeat_scan.py` (stretched words, repeated 4-grams) before the EDL; re-transcribe flagged spans in isolation; cut the first attempt. |
| 2 | "move the graphics down so they don't overlap with the captions. Let's make this a standing rule." | 49 px of overlap on every lower third. | Lower thirds at the bottom (box ~852–1000), captions lifted, clearance measured in pixels on the delivered frame, ≥ 20 px. |
| 2 | audio: "you got it nailed. This is the audio that we want" | The fitted EQ + expander + no compressor + bed −44. | That chain is the base. Changes to it must beat it on the gate AND ship an A/B. |
| 3 | "My hair is cut off in the opening scene here and throughout the video… Never cut off my hair or below my shorts line… use a little bit closer crops. Avoid that super wide crop." | The "head top" detector read the HAIRLINE (skin), 90 px inside the hair; the proof sheets were 480-px tiles where a line at the hairline and at the hair top are two pixels apart. 23 of 26 holds cut the hair. | `hairdet.py` climbs to the true hair top against the door's per-column luma; proof sheets at NATIVE scale; `hairgate.py` on delivered frames + a detector-free top-rows test; the wide level deleted. |
| 4 | "The framing and the cropping are all looking good. You nailed it with this one. Let's lock that in and crop all the videos like this going forward." | — | FRAMING LOCKED. |
| 4 | the grilling clip: smoke from his mouth | The prompt asked him to "breathe in the smell"; Veo rendered breath as smoke in the last second. | Never prompt breath/smell/steam near the face. Frame strips of the first and last second of every clip, looked at. |
| 4 | the containers sliding and vanishing | The shot ended on a static row of objects; Veo drifts static objects. | Never end a beat on static objects; the man is still working at the end of every shot. |
| 4 | remove the goal-image card at 3:36: "keep the emphasis on the prospect and not on me" | — | No goal-image card at the close. |
| 5 | "the audio is pretty good, but I feel like there's room for improvement… more like Muhammad's" | The chain never dereverbed: room 77 ms vs his 40; everything else already close. | Dereverb with the parameters he approved by ear on 2026-09-09 (alpha .30 / floor −10 / smooth .45). Room ≤ 50 ms. The strong setting ("underwater") is banned. |
| 5 | the pale patch beside his mouth: "so my face looks even, but still looks natural and not like I edited my face" | A flat ×1.15 lift on the cheek (viewer's left), ~38 px. | Landmark-anchored feathered gain ×0.90 (under-corrected), ships as A/B with a face-region clip. Never a brightest-blob search (it finds the doorframe). |
| 5 | "the way he's doing these curls is a little bit unnatural-looking… toe-touches at home without weight" | The curl clip had 23 of the watch pass's 30 flagged jumps. | AI clips that read as unnatural are regenerated, not kept. Home clips have no equipment. The watch pass's jump count per clip is a tell. |
| 5 | "remove the graphic and replace this with scrolling through the workout program… where we have the AI demos right there. Don't show any of the stick figures… make this look impressive" | A lower third where a real product demo belonged. | Real Trainer capture: day view + exercise sheets with the demos playing, seeded through the app's own storage on the fixture server. |
| 5 | "change the protein from chicken to steak… everything else the same" | — | In-place edits of the approved stills so only the named thing changes. Steak. |
| 6 | "you nailed it, this is perfect, this video is finalized" | — | This skill. |

## Things that never reached Dan because a gate caught them (keep the gates)

- Rev 5: a beat edge moved and the rule said re-punch; a frame-by-frame plan diff showed the only 29 changed frames sat
  under an opaque insert, so the 20-minute punch was skipped (lesson 116).
- Rev 5: the 21-input mix livelocked ffmpeg (336 threads parked); staged into three passes through lossless
  intermediates (lesson 117).
- Rev 6: the retouch pass's RGB round trip darkened every pixel 1.4 levels and failed the hair gate on border rows —
  the gate was right, the pass was rewritten in YUV (lesson 119).
- Rev 6: a frame inside an insert's fade handed the face detector the AI man's face; the proof sheet showed it before
  anything rendered (lesson 119).
- Rev 6: the Trainer capture found the analysis page's unclosed div — the member hub had been blank for logged-in
  members for 18 hours (lesson 121). A capture of the real app is also a smoke test of the real app.
