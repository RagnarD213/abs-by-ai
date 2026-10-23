**SFC.** Task name: `Dr Mike Dial SFC R1`.

# DS-37: "Dr. Mike Says Tirzepatide Is A Dial For Your Body Weight. He's Right.", first cut from raw footage

**Dedicated short · 10/15 shoot · READY.** Added 2026-10-16 at Dan's request. Read `00-RULES.md` first.

## Source (10/15 shoot, called the 10/17 shoot in the planning docs)
Folder: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/`
Read `Docs/SHOOT_1015_FOOTAGE_REPORT.md` first (roll map, measurements, editor warnings). Format: Sony FX30 4K 29.97p **S-Cinetone** (grade as Rec.709). The lav is on the **left channel only**; use `pick_lav.py`'s map. **The lav flat-tops at -0.49 dBFS on loud words**: listen to emphatic lines and prefer a clean take. Every roll has a sidecar beside it (`roll_sidecar.py show`): full transcript, takes, contact sheet.
Scripts: the editing copy with every cue is the shoot doc `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`; what Dan read is Teleprompter 2 - Green Screen `1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ`.

## This video
Rolls: **C1730 12:03 (scripted 13:05, off the cuff 13:56)**.
Set: Green screen, **portrait roll** (rotation -90, decodes 2160x3840; do not add a transpose). A laptop edge sits at the bottom of the frame: crop above it. Dan's eyes drop to the laptop while he watches the clip.
Deliverable: 1080x1920, 45 to 66 s, J2 captions, Soft Blue Light HyperFrames graphics. A dedicated short: nothing is derived from it. Cover images are a separate setup task.

- B-roll on this shoot: the pool demos and equipment (C1732 to C1754, listed in the report). Clip library first for anything else.
- B-roll not filmed yet: drawing up the dose.

## Both versions: scripted and off the cuff
- **One task, two finished Shorts (Dan, 2026-10-23):** *"We'll do both the off-the-cuff and the scripted video at the same time for everything that we have scripted and off-the-cuff."* Build the scripted version and the off-the-cuff version in this same task and deliver both; Dan compares and picks which ships. Both use the locked reaction format (`.claude/skills/_shared/VIDEO-RULES.md`, "Reaction videos: the locked format, start to finish"; worked example `.claude/skills/shorts/reference/ds44-reaction-format/README.md`).
- **Share everything once:** the opening (clip full screen, Dan lower left at 0.40 with the laptop, his real watching footage), the handover, the interview card behind his head, the key plate and calibration (house key; key only each version's own talk range), colour, voice, caption style and graphics family are the same in both. Only Dan's talk section, its cuts, cutaways and key-point graphics differ (the off-the-cuff key points distil what he says in that take, never the scripted wording). Get the shared choices approved once, on one round 1 page, then build both.
- **Off-the-cuff take (C1730 13:55.8):** roll C1730, slate at 835.80 s (13:55.8); use 842.16-908.82 s (14:02.2-15:08.8, the take). Re-transcribe that window with medium.en, measure every cut on energy, remove restarts, repeats, dead air and stumbles (last clean take rule).
- **Length:** the Short ceiling is 66 s and the opening clip runs about 15 s. Get the off-the-cuff cut as close to it as possible by cutting only restarts, repeats and pauses, never a point he makes once; if it still runs over, deliver the shortest clean cut and state its length on the page. If the take has no subscribe line, end where he ends.
- **Delivery:** both finished files in this video's delivery folder (`<task name> - scripted.mp4`, `<task name> - off the cuff.mp4`), every gate and an independent reviewer on EACH file, one review page with the two side by side (lengths shown, one question: which ships), both copied to `Videos to Review/`. Edit queue: one job; it is delivered when both are.
- The clip plays first, with nothing before it (memory `reaction-shorts-clip-first`); clip and times: `10-17 Shoot - Reaction Clips` doc `1BcRpzDQYNCssROEvg10Z9cOL2AtdvBdyqHwvxxwHtQA`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-37-dr-mike-says-tirzepatide-is-a-dial-for-your-body-weight-hes.md`: cut "Dr. Mike Says Tirzepatide Is A Dial For Your Body Weight. He's Right." from 10/15 roll C1730 with /shorts. Edit BOTH versions (scripted and off the cuff) in the locked reaction format, best take of every line, every gate and an independent audit on each, deliver both side by side, send me the review page, update the master list.

**Codex (GPT-6.1 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/DS-37-dr-mike-says-tirzepatide-is-a-dial-for-your-body-weight-hes.md` with `$long-form-content-edit` for take selection/audio/colour and `.claude/skills/shorts/SKILL.md` for vertical finishing. Edit BOTH versions (scripted and off the cuff) in the locked reaction format, every gate and an independent review on each, deliver both side by side, send Dan the review page, update `00-MASTER.md`.
