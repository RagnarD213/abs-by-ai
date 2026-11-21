# Joint Vigor VSL R4: apply the Fable review fixes, re-finish, deliver (Codex)

Category: AD (a client VSL for Goldenroots Naturals, client Eric). Job SRM-JV-R4, on the M6 under a dedicated priority reservation. Written 2026-11-17 by Claude (Opus 5.5), the editor.

**Why Codex:** Claude's weekly allowance ran out mid-task. It resets Thu Nov 19 at 10 AM Central, and Eric was promised the full draft by end of day Thursday. Dan's standing rule says a step Claude can't do goes to Codex and Grokbot. Dan authorized this edit, so do the whole step without asking him. Spend is subscriptions only: no paid API.

**Never:** send anything to Eric, upload anything, or publish anything.

## State

The full film is assembled in `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/asm/out/`: JV_R4_cap_1p1.mp4 and JV_R4_clean_1p1.mp4 (59:35.41), the SRTs, gates.json and RECEIPT.md. The VTurb reveal is at 28:25.01 at 1.1x.

Two fresh Fable reviews found fixes:
- `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/asm/REVIEW-FABLE-A.md` covers 0:00-30:30.
- `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/asm/REVIEW-FABLE-B.md` covers 29:30 to the end.

Claude's builder had started the B fixes and was extending the film gate (`/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/build/gates_film.py`) when it stopped. Check `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/asm/` (patchA2, run_A2.sh/log, chunks) for the state it left.

**Tools,** all in `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/build/`:
- `assemble_film.py`: assembly, with three frame-exact cuts.
- `patch_chunks.py`: re-renders chunks.
- `finish_r4.py`: 1.1x speed, music and loudness.
- `gates_film.py`
- `make_fit_cards.py`
- `assemble_r4.py`: block renderer.
- `caption_pass.py`

**Inputs:**
- Plans: `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/blocks/b1..b4/plan_bN.json`.
- Shared rules and decisions: `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/BLOCKS-BRIEF.md`.
- Style lock: /Users/danrrose/Projects/Claude/Projects/Social Response Marketing/clients/goldenroots-naturals/joint-vigor-vsl/STYLE-LOCK.md.
- Captions: `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/asm/words_asm.json`, built from `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/captions/words_film_r4_aligned.json`.
- AI clips: `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/ai/INDEX.json`. Use only clips with a PASS file, inside their usable range.
- Heavy steps go through `python3 .claude/skills/_shared/renderq/renderq.py run --group SRM-JV-R4 --heavy -- CMD`. The internal drive is tight, so keep work on /Volumes/Extreme. If a share drops, a watchdog remounts it within 60 s.

## Do

1. Apply every MUST-FIX and SHOULD-FIX in both review files.

   **A (first half):**
   - Remove the duplicate "every" at 16:09.5.
   - Remove the 7-frame "In just 5 days" callout at 27:21.47.
   - Add the KV4 age labels "Age 30" and "Age 50s" (Montserrat, empty upper left) at 19:14.4, 19:57.5 and 27:47.1.
   - Don't show KV9's bottle or name until the name is spoken (about 28:27.5).
   - Crossfade the music loop seam (it drops out every 188.4 s).
   - Smooth the audio chops at 11:12.10, 16:32.84 and 17:13.95.
   - Replace the frozen V2 knee holds (11:21.2, 31:52) with motion.
   - Build the study cards KV1, KV3 and KV7 line by line, or break their long holds.
   - Wedding scene: at most 2 uses each of the fall still and the dance still, and reception-hall cutaways instead of church pews.
   - Use one consistent Margie.
   - Fix the reuses within 90 s.
   - Spell "LaBeaud" on the card too.
   - Replace the stock shots at 21:35.5 and 22:19.6 (use a Japanese farmer at 22:19.6).
   - Restyle the callouts at 20:10.0 and 24:06.1 in large capitals.
   - Add the missing caption words "A" (18:53.7) and "Their" (25:40.5).
   - Reframe the diagram at 21:15.5.

   **B (second half):**
   - Fix the stray near-black frame at 53:45.12.
   - Keep KV14's $228 total and every card's key text above y=830 in the captioned version.
   - Correct the caption words: "100% safe", "5 to 7 business days", "The attack stops."
   - Everyday Tasks (48:18-48:49): put in the AI clips that passed, or better stock.
   - Margie at 37:15-37:56: one woman.
   - Fix the casting at 43:11, 49:21 and 42:50.
   - Replace the campus aerial at 34:38.
   - Keep the guarantee card and six-bottle holds to about 5 s or less.
   - Fix Rick's 12-frame freeze at 40:32.86.
   - Remove the black band at 49:29.

2. Re-assemble and re-finish once. Then run every gate, plus:
   - a per-frame luma check;
   - the y=830 caption keep-out on cards;
   - music dropouts of 0.5 s or more;
   - the seam scan;
   - a duplicate-word check;
   - video length equal to audio length.

   Overwrite `asm/out` only after the new files pass, and keep the old ones as `asm/out_prev/`.
3. Write `asm/out/RECEIPT-R2.md` with the new sha256s, the gate results, the VTurb reveal timestamp, a fix-by-fix list (each review item, fixed or not and why), and a short revision list with 1.1x timestamps of each changed spot.
4. Build a review page for Dan with `.claude/skills/_shared/review_server.py` (it must seek). The page needs:
   - the captioned 1.1x film, 1080p;
   - chapter jump links to the changed spots and the cut points (33:18, 39:45, 40:33, 49:21);
   - the reveal timestamp;
   - a "for a human ear" list: no one has listened yet; TB2 pitch lifts at three joins; cut points.

   Follow the silent-check and owner-handoff audio rule in AGENTS.md. Record the page's http://127.0.0.1:PORT/ link in RECEIPT-R2.md.
5. When the delivered film passes its gates, release the M6 slot and reservation:
   - `python3 .claude/skills/_shared/editroute/priority.py milestone SRM-JV-R4 checked-preview`
   - `python3 .claude/skills/_shared/editcap/editcap.py release SRM-JV-R4 --review`
   - `touch /Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/.stop_renew`
   - `touch ~/.jv-r4-keepalive-stop`
   - `touch /Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/key/offload/STOP` (the key is complete).

   Then update `/Users/danrrose/Projects/Claude/Projects/Social Response Marketing/clients/goldenroots-naturals/joint-vigor-vsl/STATUS.md`.
6. **Filing:** if any AI takes remain unarchived (`ai/INDEX.json` / `ai/RECEIPT.md`), archive them per `.claude/skills/_shared/cliplib/README.md`.

Finish with a short chat report that includes the review page link.

Superseded 2026-11-17 10:55 CT: Codex was out of usage, so the Claude builder applied every fix in round 2 (claude-r4/asm/out/RECEIPT-R2.md). This handoff is closed.
