# /ai-clip-ideas — concept clips for a line in a video

---
name: ai-clip-ideas
description: Brainstorm AI-generated concept-clip ideas to illustrate a specific line or moment in one of Dan's videos, generate START and END keyframes for EVERY idea up front, then — after Dan picks — generate the keyframe-locked video clip. Use whenever Dan asks for "AI clip ideas", "an AI-generated clip for this line", a visual gag to open a video, or to illustrate a concept in an ad or content video — even if he doesn't say "/ai-clip-ideas". For exercise demos use /exercisegeneration; for full AI-generated ads use /make-ad; for finding EXISTING footage use /findassets.
---

Proven end-to-end on 2026-08-31 (Ad 2 "nutritionists obsolete" museum-exhibit opener — Dan: "This
process worked well, and I like the result"). Follow the flow exactly; every step below earned its
place in that session.

## The flow

1. **Ideas** — deliver ~5 ideas. Each idea is **one visual joke, not a scene with a story**:
   it must land in a single ~8-second clip, readable in one frame if possible.
2. **Frames for ALL ideas, immediately, without being asked** — Dan's standing instruction:
   on the FIRST response, generate a start frame and an end frame for **every** idea. Do not
   deliver a text-only idea list and wait; do not ask whether to generate frames. Ideas and
   frame pairs arrive together.
3. Dan picks an idea (and any frame tweaks — a tweak is one cheap re-roll).
4. **Video** — generate the clip keyframe-locked from the approved pair, QC it, save it
   durably next to the target video, send it in chat.
5. On his approval, splicing it into the video is an /ad-edit or /longform-edit revision job,
   not part of this skill.

## Step 1 — ideas

- Ground in the exact spoken line: quote it, time it (Dan speaks ~198–222 wpm), and note that
  the clip will be trimmed to the line at edit time — an 8s generation covers a 5–6s line with
  editing room.
- Idea shapes that worked: the **museum exhibit** (obsolete thing in a display case with a
  dated brass plaque), the **sad packing-up**, the **yard-sale table of obsolete tech**, the
  **hologram replacing the person mid-consultation**, the **speed mismatch** (human toiling,
  phone finishing instantly). Ranked recommendation, with one line of reasoning each.
- Compliance is designed in at the idea stage: **no side-by-side before/after**, no email-capture
  screens, nothing from the banned-screens list, no celebrity likeness (Veo's safety filter also
  rejects real-person faces). Humor register: deadpan, one-gag, same family as the fat-trainer /
  robot-trainer / supplements-in-the-bin gags.
- On-scene text (plaques, price tags, signs) is an asset, not a risk — Nano Banana Pro renders
  short quoted strings exactly. Put the punchline in the set dressing where it survives with the
  sound off. Keep each string short and QUOTE it exactly in the prompt.

## Step 2 — frames (all ideas, one pass)

**Aspect matches the target video** (16:9 for the ads; 9:16 if the clip is for a vertical).
Draft tier 2K. Cost: ~$0.14/image ⇒ ~$1.50 for five pairs.

1. **Start frames: text-to-image**, one per idea, in parallel.
   - Primary route: `_shared/gemini-image.js generate --tier draft --aspect 16:9` (the
     `--aspect` flag was added 2026-08-31).
   - ⚠ **Google-direct 503s under load ("high demand") and retries don't help. The Replicate
     route to the SAME model works when it does** — `reference/rep-t2i.js` (text-to-image) and
     `photo-edit/scripts/replicate-edit.js` (edits). Try Replicate before concluding anything
     was refused. This has now saved two sessions in two days.
   - Prompt form: "Photorealistic cinematic still, 16:9 widescreen." + full scene, camera
     position, lighting, every on-screen text string quoted exactly, "No watermark".
2. **End frames: an EDIT of that idea's own start frame — never a fresh generation.** This is
   what makes the pair Veo-interpolable: scene, camera and characters are identical by
   construction. Prompt skeleton (lock INTENT, not pixels — same lesson as the photo skills):
   - Open: *"This image is the FIRST frame of a locked-off video shot. Produce the LAST frame
     of the same shot. The camera does not move: [enumerate everything that must stay] must
     remain PIXEL-FOR-PIXEL identical. Changing any of those is a complete failure."*
   - Then: *"The ONLY change[s]: ..."* — describe the changed elements limb-by-limb /
     object-by-object, including where each moved person now is relative to the frame edge.
   - Close: *"Nothing else changes."*
   - Model: `google/nano-banana-pro`, `--resolution 2K`, aspect `match_input_image`.
3. **Inspect every frame before sending.** Check the quoted text rendered, the end frame didn't
   invent objects (one end frame added phantom "MEAL PLANS" binders on a cabinet — flag such
   deviations to Dan and offer a re-roll BEFORE video, they will survive into the clip).
4. Build START|END pair sheets with `reference/pairsheet.py` and send ALL pairs in one
   SendUserFile with the idea list.

## Step 4 — video

- `reference/gen-veo-keyframes.js --start s.jpg --end e.jpg --prompt-file motion.txt --out clip.mp4`
  — Replicate `google/veo-3.1-fast`, 8s, 1080p, `generate_audio:false` (the ad carries its own
  mix; audio also costs extra). ~$1.20/clip. Step up to `google/veo-3.1` only if fast
  disappoints on a chosen idea.
- ⚠ **The Gemini-direct API has NO last_frame support** — keyframe pairs go through Replicate,
  full stop. (Gemini-direct is only for start-frame-only generation, e.g. the reverse-generation
  trick in /exercisegeneration.)
- Motion prompt: restate the locked-off camera ("camera does not move at all"), declare what is
  static ("it is a wax statue and must never move, blink or breathe"), quote on-scene text that
  must stay legible, then describe the ONE motion from start pose to end pose. Deadpan tone words
  help ("Quiet, deadpan, cinematic").
- **QC on the delivered file, not the plan:**
  - probe duration/resolution/fps;
  - frame tile across the runtime (`select='not(mod(n\,24))'` at 24fps = 1/s) — check the
    motion path and that text stayed legible;
  - **static-subject stability strip**: crop the region that must not move, tile it 1/s, and
    look — pose drift, blinks, or re-rendering of a "statue" fails the clip;
  - last frame vs the approved end keyframe.
- **Save durably before sending** — the scratchpad dies with the session. Copy clip + both
  keyframes + all three prompts + the gen script into the target video's folder under `aigen/`
  (ads live on the Extreme drive: `EDITED ADS 8-20-26/<ad>/aigen/`). md5-verify the copy.
  If the destination is inside the repo, confirm gitignore (public repo).
- Send the mp4 in chat with: what was checked, the cost tally, and the reminder that the
  **AI-GENERATED label is burned in at edit time** per the standing rule — the raw clip is
  correctly clean.

## Cost + spend rules

Frames ~$0.14 ea (2K), video ~$1.20 (veo-3.1-fast 8s no-audio) / ~$3.20 (veo-3.1). A full run
(5 pairs + 1 clip) is ~$2.70. State the estimate before the batch; all well inside the $25
session cap.

## Lessons

1. **(2026-08-31)** Generating frames for all ideas up front is the standing default — Dan made
   it explicit: never make him ask for the frames after the idea list.
2. **(2026-08-31)** End-frame-as-edit + "The ONLY change" scene lock held on 5/5 pairs with zero
   re-rolls; the one blemish (phantom binders) was an invented OBJECT, not a broken scene —
   inspect for additions, not just changes.
3. **(2026-08-31)** Veo kept a "wax statue" human perfectly frozen for 8s when the prompt said
   it "must never move, blink or breathe" — declaring what is static matters as much as
   describing the motion.
4. **(2026-08-31)** Brass-plaque text ("HUMAN NUTRITIONIST 1985–2025") survived t2i, the edit,
   AND the video legibly — put the joke in set-dressing text with the string quoted in every
   prompt of the chain.
