# Client rounds, review pages and client messages

Each round below is what Joint Vigor actually did, with the change Dan would make next time. Job notes for Joint Vigor
(private SRM repo): `clients/goldenroots-naturals/joint-vigor-vsl/` (`PLAN.md`, `STYLE-OPTIONS-R2.md`,
`SPLIT-PANELS-R3.md`, `HANDOFF-R3-KEY-VISUALS.md`, `TRANSCRIPT-CUTS-R3.md`, `R4-PLAN.md`, `STYLE-LOCK.md`, `STATUS.md`,
`CLIENT-MESSAGE-*.md`). Build folders: `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r1..r4/`.

## Round 0: intake and plan
- Download everything the brief links (spokesperson camera, VO, master + camera + VO scripts, reference VSLs, the
  client's sales page and order page). Verify each download against Drive. Transcribe the start of camera and VO
  offline (Whisper) to find the recording order and slates.
- Joint Vigor's material: 25:47 of 4K 29.97 green-screen camera (white coat, stethoscope), 45:10 of stereo VO MP3,
  17 camera parts and 16 VO parts recorded separately; the master script dictates the order.
- Measure the raw levels (Joint Vigor: camera -13.1 LUFS, VO -10.4, both clipping). Start with the VO about 2.7 dB under
  the camera and level-match by ear-free measurement; never call a clip "needs re-recording" from numbers alone.
- Write `PLAN.md`: the deal (milestones and what each covers, revision rounds), material table, research (reference VSL
  picture-change rates: Joint Vigor's references ran 11, 13 and 19 changes a minute; use 2 to 5 s per cover shot in VO),
  the client's VSL page reveal setting (VTurb), a first-five-minutes table in source time, and a time budget.
- For a substantial plan, Claude and Codex write independent proposals and merge them (memory
  `claude-codex-major-decision-template`); Joint Vigor's merged plan is the model.
- **Intake message:** ask only for what blocks you (Joint Vigor: a trashed image folder) and say what you plan to use
  unless told otherwise (a testimonial clip from his sales page). Do not wait for optional data.

## Round 1: the $5 trial lead
Goal: one usable, captioned first five minutes that shows the client you can make the next 45 minutes of decisions.
1. Edit slot, time log (`TIME-LOG.md`, first line START with the time).
2. Radio edit in master order (EDL), forced alignment, two voice treatments.
3. House chroma key calibrated on this source (coat spill, shadow halo, hands, glasses, stethoscope), full key started
   early as unattended machine time. Key code: `claude-r1/recipe/key16.py` (the locked DS-40 R2/R3 house key, geometry
   re-measured), compositor `comp16.py`, set plates by Codex image on the subscription.
4. First-minute internal review for Dan: the recommended opening in context, two skin/coat grades and two equal-loudness
   voice treatments on the same material, the set at medium and close framing, captions readable from frame one, the
   first mechanism diagram, and the AI frame pairs (START and END together). Dan signs off the minute once.
5. Extend to a natural endpoint near five minutes (Joint Vigor ended at 6:05 to finish the thought). Independent review
   against the master script before Dan's second look.
6. Deliver after Dan approves: captioned MP4, clean MP4, SRT in one Drive folder (anyone with the link, MD5 checked,
   opened logged out), plus the client message, through the trial milestone. Ask the client to fund the next milestone;
   verify it is funded before building beyond the lead.

Joint Vigor: 13:05 to 21:46 CT on 11-06, five internal passes (R1 to R5B), Dan chose version B (full testimonials).

## Round 2: the style options page
One section per area, two to five options each, **every option built on the same source moment** so the only change is
the thing being chosen. Joint Vigor's areas and what Eric picked:

| Area | Options built | Pick |
|---|---|---|
| Opening (first ~19 s) | D1 pain cold open (stock), D2 kinetic text, D3 AI cinematic open (Veo in Flow) | D3 |
| Set and framing | A1 office current framing, A2 office wider (waist-up), A3 current room wider, A4/A5 physician's office | A2 |
| Pace | B0 1.0x, B1 1.1x, B2 1.2x, B3 1.3x (atempo, pitch kept, picture sped to match) with projected runtime and reveal time for each | B1 |
| Music | C1 tense pulse, C2 emotional, C3 documentary urgency (Pixabay beds, ducked from word timings) | C2 |
| Callouts | F1 red punch-in, F2 bold kinetic words, F3 subtle side card | F1 |
| Mechanism animation | V1 the client's requested fix, V2 a second take (split ordinary vs product layer) | V2 |

- Pace projection: script words (Joint Vigor 8,026, 3,682 before the reveal line), measured spokesperson rate on the trial
  (121.3 wpm, 128.0 wpm with pauses over 0.30 s tightened), runtime and reveal at each speed. State the trade-off plainly
  in the message (1.3x was the only speed inside his 45 to 50 minutes).
- Samples: 1920x1080 H.264 yuv420p bt709, AAC 48 kHz; sha256 manifest per page.
- Picks UI: a button per option plus an optional note per section, a summary with **Copy my picks** (clipboard with a
  select fallback); the client pastes it into Upwork. Picks are per-viewer localStorage only.
- Dan gets a private version of the page (`--dan`) that also shows AI frame pairs and internal notes.
- Joint Vigor builder: `claude-r2/work/build_page.py --slug <slug> [--dan]`.

## Round 3: key visuals and script cuts
Three sections on one page:
1. **Replacements for what the client asked to change**, three options each (Joint Vigor: 9 split-screen clips, 3 per
   word, Veo 3.1 Fast in Flow, 2 takes each, 180 credits), plus the full opening rendered three ways at real speed with
   sound. When the client's request is "give me options", his pick is the approval; otherwise START/END frame approval
   applies.
2. **Script cuts.** Read the whole master script; propose verbatim deletions only (whole sentences or a clause ending on a
   spoken pause), never the opening, credentials, studies, quotes, statistics, the reveal, each ingredient's headline
   claim, price, offer, bonuses, guarantee, calls to action or shipping/billing answers. Mark on-camera cuts that need a
   cover shot over the splice. Give two or three options with words removed, reveal time and runtime at the locked pace
   (Joint Vigor: Recommended 1,039 words, reveal 21:47, 49:37; Lighter 198 words; No cuts). **Each cut option is a
   Google Doc copy of the master script with every cut as a Track Changes deletion**, linked from the page with a summary
   and your recommendation. Working file: `TRANSCRIPT-CUTS-R3.md` (every quote verified word for word).
3. **Key visuals: 10 to 15 stills** of the pieces that are new and slow to redo (mechanism animations, study and quote
   cards, product reveal, price, bonuses, guarantee), each with roughly where it appears, the line spoken under it, an
   Approve button, a note box and **Approve all**. Questions for the client in amber. Type that ships is set in code, not
   generated. A study the sources cannot find is marked "to confirm", never invented.

Joint Vigor builder: `claude-r3/work/build_page2.py` (`--all` client page, `--dan` Dan's), key-visual cards
`claude-r3/kv/kv_cards.py`. The client's answer is the input to `STYLE-LOCK.md`
([STYLE-LOCK-TEMPLATE.md](STYLE-LOCK-TEMPLATE.md)), written as the first step of round 4. Revised key visuals he did not
approve go to Dan as a quick look (blind A/B if both AIs made one) and never hold the edit.

## Round 4: the full build
See [PIPELINE.md](PIPELINE.md). Promise a date with a day of padding (Joint Vigor: promised end of Thursday, delivered
Wednesday). Re-estimate from block 1's measured time on day one and tell Dan the same day if the date is at risk. No
review page goes to the client before the full film. Delivery message: the folder link, the runtime and the exact VTurb
reveal time, the cut version's projected length and reveal, what the casting and Dramatization treatment is, a request
for timestamped revisions from the captioned version, the number of included revision rounds, and what comes next.

## Round 5: the recommended-cut split-test render (method; not yet run on Joint Vigor)
- Build round 4 so each cut is a clean lift: cut points on sentence boundaries, cover shots that span a splice.
- Remove the cut pieces from the EDL and shift every later plan event, word and caption earlier by the removed length:
  the same mechanism `assemble_film.py` uses for the testimonial-length change and the false-start cut. On-camera cuts
  get their planned cutaway or punch-in. Re-lint for stills over 5 s and 90 s reuse across the new joins.
- Re-run the finish once on the whole film (music re-flowed over the new dialogue in one pass), re-align captions,
  re-run every gate, a fresh Fable review on the whole cut film, then Dan.
- Give the new reveal time. Joint Vigor projection: about 51:30, reveal about 24:05 (1,039 words at 128 wpm).

## Round 6: upsells and the vertical (method; not yet run on Joint Vigor)
- **Upsells/OTOs:** the same `STYLE-LOCK.md`, one block, the same gates and reviewer. Confirm the final upsell script,
  offer, prices, guarantee and CTA for each version before building (Joint Vigor owes three OTO1 versions; the shared
  segments are built once and the version-specific offer sections swapped).
- **Mobile vertical (1080x1920):** from the clean master of the version the client names. Follow the shared vertical
  rules (the camera lands on the spokesperson and holds; a 16:9 card or clip is never cropped shorter; fill the frame
  when the clip allows). Re-lay captions and callouts for 9:16, re-check card keep-out and chips at the new geometry.

## Review pages: hosting on review.socialresponsemarketing.com
- Cloudflare Pages project `srm-review`, custom domain `review.socialresponsemarketing.com` (DNS CNAME `review` to the
  project's `pages.dev` host, proxied). Root and `robots.txt` block indexing; no login.
- One folder per page, named `<job>-<10 random hex>` (an unguessable slug; Dan's private pages get their own slug).
- Deploy from the page folder, token from `~/.srm-secrets.env` (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`):
  ```bash
  set -a; source ~/.srm-secrets.env; set +a
  npx wrangler@4 pages deploy <site-dir> --project-name srm-review --branch main
  ```
- **Trap: a deploy to `main` replaces the whole live site.** Mirror every live page folder into the deploy folder first,
  or the client's earlier pages disappear. Drafts go to a preview branch (`--branch r3-dan` serves at
  `r3-dan.<project>.pages.dev`), production only after Dan approves.
- Checks before Dan sends the link: every video streams and decodes from the public URL logged out (ffprobe plus a full
  decode over HTTPS, 0 errors), byte-range seeking works, phone width 375 has no sideways scroll, pick / note / summary
  work, desktop playback works, no autoplay, every player paused with sound on, no em or en dash in page copy (the
  builder asserts it).

## Client messages
- Drafted by Claude in Dan's voice, sent only after Dan says so; record the send (time, story id) at the top of the
  draft file and in `STATUS.md`. Dan may edit before sending; keep his edits as the record of his voice.
- Shape (from the four Joint Vigor messages): "Hi <first name>," then one line on what is ready, the link, a numbered
  list of what is on the page or in the folder, the one decision or number he needs (reveal time, runtime trade-off),
  exactly what to do next ("tap the one you like, then Copy my picks and paste it here"), what happens after, "Dan".
- Answer each of his notes by its item number, say what changes in plain words, never argue. Flag a number you got
  wrong earlier yourself (Joint Vigor R3: the 190 words were computed for 1.3x, not 1.1x).
- Before writing a delivery message, re-read the thread for promises made (Joint Vigor: the vertical, three upsell
  versions, two revision rounds, the date).
