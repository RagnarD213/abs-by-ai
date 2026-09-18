Read `_shared/VIDEO-RULES.md` first.

# Editor card — read this BEFORE the skill, hold it for the whole build

Written 2026-09-17 from two side-by-sides against Codex. **The main one: Codex's C1652 R4 "Why Your Belly Fat Is an
Emergency" (11:14, 16:9)** — Dan: *"this is looking excellent… he did a great job… good enough to ship"*, and the video
where *"Codex significantly exceeded you."* Compared with Claude's long-form `04 - Why You Should Invest More In Your
Health`. Second: Codex's DS-17 short (approved; Dan rates it about equal to Claude's work) vs Claude's DS-04 round 1
(9 defects). **Codex used our audio chain, our gates and our skills. It won on editorial judgment and method.**
Watch the winner before a long-form build: `Media/codex-video-trial/06-organic-r4/C1652_FINAL_APPROVED.mp4`; its
methods: `Media/codex-video-trial/skills/abs-edit-organic/references/c1652-r3-methods.md` and `c1652-r4-methods.md`.

## A. What the picture must do (the part Codex won on)

1. **Show the story Dan is telling, not a stock synonym for a word he said.** C1652 illustrates each scenario with a
   purpose-made scene: the overweight man tying his shoes and walking out the door, the same man LATER in the gym, the
   woman glancing at the fit man by the pool, the dad on the sidelines while the family swims, tired-at-desk →
   energised, the hiring handshake. Claude's 04 used generic Pexels (hands counting money, typing, an ECG strip).
   Budget exists for this: up to $5/video of AI clips (C1652 spent ~$3.70). Frames approved by Dan first; then REAL
   motion for the full action — never a still, a pan on a still, or a fragment plus a held frame.
2. **Graphics label the idea in 2–6 words; they never transcribe the speech.** C1652 has 60 graphics in 11 minutes
   (one per ~11 s) and almost none takes Dan off screen. Claude's 04 cut to black full-screen slides carrying three
   full sentences of what Dan was already saying — a PowerPoint. Do not do that.
3. **Use a vocabulary of graphic types, one palette.** Topic lower-third at the open; numbered lower-thirds for every
   list item (01–07, then 01–05); a full-screen title card per section; a left-third list panel BESIDE Dan with rows
   revealed as he says them; a diagram when the idea is a mechanism (the downward-spiral loop, arrows revealed in
   order; 5/10/15-minute tiles); an anatomy illustration with callouts. Palette, type and motion copied from
   Muhammad's actual moving graphics (olive tab + white bar, dark-green panel) — reuse Codex's
   `06-organic-r4/muhammad_graphics.py`, `palette.py`, `design.py`; do not design a new look.
4. **Every title is self-contained**: someone skipping to it knows the topic ("5 Ways to Fix Your Belly Fat Fast",
   not "What changes").
5. **Dan's own real assets before stock**: his real heavy photo (labelled), the three-vertical-portrait template
   (`three_photo_template.py`), real app screens from ONE capture session inside a phone bezel with Dan still on
   screen beside it (`build_salmon_phone.py`), his own workout footage from FINISHED graded masters, the approved
   same-person AI demo.
6. **Variety is what the viewer sees, not file IDs.** Three doctor beats = three casts and settings. Two exercise
   inserts = two exercises. Claude's 04 showed fried eggs five times. Never blur-pad a vertical stock clip into 16:9,
   and no cross-dissolves ghosting b-roll over Dan's face — hard cuts.
7. **Framing: two sizes (mid / tighter), changed on cuts, Dan shifted aside when a panel needs the room. Zero camera
   motion in horizontal video** — no pan, drift, tracking or recentering, ever (Dan, 2026-09-17; only square and
   vertical reframes need it). Check the RENDERED footage at graphic entries and exits.
8. **Disclosures are part of the design**: AI-GENERATED chip, "Illustrative footage", "Real picture(s) of me — not
   AI-generated" on real physique photos only, "Not medical advice · Talk to your doctor", "My experience: 192 to
   178 lb". Placed on the composed moving frame, clear of faces and abs.
9. **Vertical shorts:** open full-bleed on the strongest MOVING shot of the topic; b-roll on a width-filling stage
   with the whole body, captions in the band below, never on the body part the shot exists to show.

## B. How to work (why Codex converged and Claude did not)

Before transcribing, picking a lav, or building a contact sheet for a source clip, run `.claude/skills/_shared/rolls/roll_sidecar.py show`; if there is no sidecar, run `build` and use its output. When the EDL is final, run `mark-used` for every source range.

10. **Start from the last approved recipe, not a blank directory.** DS-04 wrote 30 new scripts and re-broke solved
    problems. New code is where the defects come from.
11. **Each round with Dan LOCKS what he approved** (C1652: audio, colour, crop sizes, specific panels) and changes
    only the timestamped list. R3→R4 reused 168 of 171 scene caches; approved audio carried byte-for-byte. A specific
    approval beats a general redesign ("enlarge the text, keep everything else").
12. **Record Dan's feedback verbatim with screenshots the moment it arrives**, one short authoritative list of
    requested changes + elements to preserve. Short plans (~600 words), not ones the editor cannot hold.
13. **Inspect at native resolution and full frame rate before anyone else does** — every cut, every generated clip
    before AND after compositing (heads, hair, toes, labels over the crown). Reject your own work first.
14. **Internal review to zero defects, then Dan.** Dan's round is for taste, never for defects. Keep model-QC
    verdicts but check each claim against real frames — reviewers invent defects when primed.
15. **Numbers and taste stay separate.** Report every gate FAIL honestly, never tune a threshold, never reprocess
    approved sound to chase a meter, never claim an improvement a duplicate-control listen cannot hear.
16. **Keep a per-video spend ledger** including failed calls; a revision does not reset it.
