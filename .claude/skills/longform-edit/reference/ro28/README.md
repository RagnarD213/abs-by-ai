# RO-28 "Why Zepbound Improves Your Health Even If You're Ripped" (10/15 C1771): round 1 recipe (Claude Opus 5.5, 2026-10-20)

First Claude film on the **10/15 studio set** (dark green backdrop, two cyan tubes, desk; Codex cut RO-25/26/27 there). One 10:18 roll,
cut to 6:26. Starts from RO-18's round 1 recipe (`../ro18/`); only the files that differ are kept here. Work dir (Extreme was full, 66 GB):
`/Volumes/Expansion/_edit_work/ro28/round1/` (`/Volumes/Extreme/_edit_work/ro28` links to it). Never commit media.

## The set (measured)
- Lav left channel only (`pan=mono|c0=c0`); room tone for joins C1771 51.0-54.3 s (-54.9 dB, steady).
- **Hair top: 84 px from the top of the 4K frame at its highest** (person mask every 0.5 s of the whole roll, `framing/hair_roll.json`,
  verified on a native frame). So W2 (3552x1998 @144) sits at y 0-21 and T2 (2704x1521 @568) at y 9-42 per shot (4.5 % + 6 px), never the
  RO-25 y 80 / 50 (RO-27 R1's clipped-hair rejection came from fixed y). `framing/crops.json` + `crop_y.json`; `frames.py` reads both.
- No room to slide the crop left under a side card (Dan's left edge sits at x 978-1180 of 3840): `build.all_segments` cards take W2 + wall
  stretch only.
- Colour options: A Rich Balanced (the approved RO-25 grade, recommended), B RO-27's Richer, C A + warm skin (`frames.GRADES`).
- Voice: RO-27's "warm bass" EQ (Dan's 10-20 pick on this set) came first in 11 blind Gemini listens (5.7) over warm bass + 3 dB at 120 Hz
  (5.5), untreated (5.0, room heard 7/11) and the chain default (3.7). `audio_options28.py`, `listen_trials.py`.

## Traps this round paid for
1. **The render queue: wrap the whole HyperFrames pass as ONE `renderq.py run --group` step.** `from_plan.py --render` alone queued each of
   27 graphics separately (#23 in line for the first one); the wrapped job got its slot once (after 112 min on a busy night) and rendered all
   27. Once a group is running, its next wrapped step is near the head of the line.
2. **Lower-third topics come out UPPERCASE unless every `lt` item carries `topic_case="preserve"`** (16:9 template default is upper;
   VIDEO-RULES 2026-10-16 says title case, never auto caps). Caught on the stills; 14 lower thirds re-rendered.
3. **Side-list headings wrap past about 13 characters at this size** ("Abs Lower Your Risk / Of", "What It Helps / Prevent"). from_plan's fit
   check does not cover l3 headings; read the stills.
4. **Fact-card copy limits (before-card, 16:9):** eyebrow about 20 characters at 64 px, headline about 15 at 84 px, detail about 30 at 46 px.
   from_plan asserts them; a count needs the headline to START with the number, and the phrase must match the token ("58%" not "58").
5. **`patch_words.py` region edges drop real words** that start just before the region ("diabetes", "by"); re-add by hand (`word_fixes.py`)
   and print film-time sentences after every patch.
6. **Pexels 9902352 ("man taking pill with water"): the drinking shot reads as red wine.** Use its first seconds (pill in an open palm).
   Library B0015's tube rack carries a brand name ("A-PRF").
7. **Dan's 10/15 pool B-roll is a wide shot (Dan about a quarter of the frame): crop the source window** (`crop=(w, h, x, y)` on a clip item,
   `gfx.clip_vf`), keeping headroom above his hair (person-mask box per roll in `framing/broll/`). Jump rope and squats need the whole body.
8. **A Gemini whole-cut junk listen called a natural 0.6 s pause inside "72% ... of American adults" an unnatural join.** It was one
   continuous take (level strip); check the EDL before cutting on a listener's word.
