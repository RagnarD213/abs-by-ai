# The long-form green-screen standard: Reacting To Celebrity Ozempic Transformations R5

**Locked by Dan on 2026-10-30 after the full film (RO-24 round 5).** *"I'm real happy with how this turned out. Let's lock
this in as our standard way to do the long-form green screen videos."* `approval.json` holds his words and scope.

The authority is the exact approved master: `claude edited long form content/25 - Reacting To Celebrity Ozempic
Transformations/`, the `claude round 5 | 16x9 | RO-24` file, SHA-256
`950120846b3b9a3b3d7ad418995a4138a998cefb10deacd281858dfe4703e2d3`: 1920x1080, 30000/1001, 15452 frames, 8:35.58, -14.5 LUFS.
Watch the master when in doubt; this page is the summary. It extends the background template lock of 2026-10-27
(`_shared/greenscreen-bg/`, whose style stays closed) from the backgrounds to the whole film. Binds Claude and Codex on every
long-form green-screen commentary or reaction film. Reaction SHORTS keep the Bill Maher Codex R5 format
(`shorts/reference/ds40-codex-r5-reaction-format/`). A new film changes its facts, script, photos, clips and clip windows,
not the way it is built.

## The shape of the film

| part | R5 times | how it is built |
|---|---|---|
| Hook | 0:00-0:06 | Full-screen AI clip over the first two lines (a camera open needs a reason), AI-GENERATED chip on. The cut between shots sits in the pause between lines. |
| Promise | 0:06-0:22 | Dan on camera over type 6 `cards` (one person per card), then type 3 `wall`. |
| Each person, in turn | 0:22-6:50 | His pickup line ("Let's start with...", "Next up is..."), a real photo card if the person needs naming, then their interview clip FULL SCREEN WITH ITS OWN SOUND. Then the same clip rolls on muted in type 2 `corner` with Dan reacting and a lower third with the person and the fact. Then whichever fits what he says: type 4 `panel` (before/after, weight lost, medication), 2b `side`, 1 `soft`, 7 `bigtype` when he says a number, 8 `set` for longer commentary. |
| Proof points | any | Real photo full screen on the exact words, credited on screen (Amy Schumer's post at 4:14). A study gets a full-screen Soft Blue card with bars drawn to scale (4:32); a graph card for a trial (6:54). |
| What to do | 5:45-6:04, 7:02-8:01 | Rules as a left-third list with Dan to the side (`soft` behind), big type for doses. |
| Recap and close | 8:01-8:36 | Full-screen title recap of the numbered steps, then `soft`, the spoken subscribe and SixPackAbs.com ask, end screen. |

## The rhythm to match

- 8:36 film: 30 background segments, 8 types, none twice in a row; they run 5 to 17 s (mean about 11 s), and the rest of the
  time is full-screen clips, cards, photos and inserts. The picture never sits still for long and the background always
  relates to the words.
- 6 interview clips with sound, 22 graphics, 5 AI or B-roll inserts, 8 real-photo scenes.
- Dan's cuts are W and T framings of the same take (fixed, no pans), so a cut is a punch, never a jump. Clear hair in both.
- AI inserts run under 6 s, full screen, chip on, at real speed, and each one shows its line. Keep a card readable if an insert
  lands inside it (A8 sits beside the G12 list).

## Locks underneath it (each has its own home)

- Key: the house key (`_shared/chroma-key/README.md`) with the 16:9 geometry and refined variant in `ro24/README.md`; calibrate per source.
- Backgrounds and planner: `_shared/greenscreen-bg/README.md`. Grade: `warm` (the build stamp beside the master's work files; Dan's foreground is graded once). Voice: Dan's RO-24 pick was the Bill Maher voice plus the bass lift; a new roll still gets its own audio procedure and picks.
- Graphics: moving Soft Blue Light HyperFrames. A film entirely about weight-loss drugs may name the drugs on graphics (Dan, 2026-10-28); other films stay away from them.
- Subtitles are a sidecar `.srt`, never burned in: Dan's words from Whisper on the delivered audio, each clip's words from its own transcript.

## The order that worked

1. Key, audio and colour on the first minute; lock them before anything else.
2. Script and clip windows: clean full-source windows only, no burned quote boxes behind his head.
3. Facts file, then `planner.py` per section, then override with a written why. `ro24/round4/README.md` lists the traps.
4. AI frames through the frame gate and a fresh `frame-reviewer`, then motion in Flow. Regenerate; never ship a Flow-altered frame.
5. Full render only (`assemble --reuse` darkens frames), then audio gate, watch judge, negative-events judge, delivery gate and a fresh `ra-reviewer` until SHIP.

Recipe by round: `ro24/README.md` (key), `ro24/round2` to `ro24/round5`; `round5/README.md` carries the newest traps (background
windows must outlast a lengthened segment, no switch sliver before an insert, pin subtitle wording against the prior round).
These are provenance, not a launcher: copy into the new job and adapt paths. The master's raw gate rows, including its known
failures, are in the gate stamps beside it; this lock waives nothing on a future film.
