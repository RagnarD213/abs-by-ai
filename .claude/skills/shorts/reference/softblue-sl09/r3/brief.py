#!/usr/bin/env python3
"""R3: print the independent reviewer brief for one short: brief.py S"""
import sys, hashlib
sys.path.insert(0, "/Volumes/Extreme/_edit_work/sl09/round2")
import plans as P
S = sys.argv[1]
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
V = f"{ROOT}/Short-form video content/{P.NAME[S]}.mp4"
sha = hashlib.sha256(open(V, "rb").read()).hexdigest()
TITLES = {"A": "Train Harder After A Bad Night's Sleep", "I": "Your Sleep Score Shows Who's Toxic In Your Life", "H": "Cut The Adrenaline Before Bed",
          "K": "You're Not Sleeping As Well As You Think", "J": "Oura Ring Or WHOOP? Which One To Buy"}
CHANGED = {
 "A": ["since the latest review: (D1) the stock clip over \"Now, the rationale behind this is that when you are less rested,\" (0:20.39-0:24.62) now plays Pexels 8134383 from 4.6 s, where the man rubs his eyes for the whole slot, cropped higher so his head stays in, with saturation raised toward Dan's footage",
       "earlier in this round (verify they still hold): every talking crop is steady (no pan); one crop through Zeeshan's zoom at 27.7; the punch-in at 0:30.33; the caption \"gonna\" at 0:40.4; the opener runs to the hammer hit; the groggy man framed on his face; stale duplicate files removed from the delivery folder",
       "everything the previous review passed is otherwise unchanged"],
 "K": ["since the latest review: (D1) the yawning opener (0:00-0:04.30) is graded brighter with curves: median brightness about 0.35 (was 0.20; Dan's shots about 0.33), highlights 0.53",
       "earlier in this round (verify they still hold): phone 1 holds its steady sleep screen to the cut at 0:25.46; phone 2 starts on the steady Readiness screen; captions \"gonna\" (0:32.7, 0:35.4) and \"you gotta buy\" (0:39.5); the 0:36 hair moment under phone 2; the punch-in at 0:13.78; no AbsByAI.com mark while a phone is alone on screen; both phone screens fill the rounded display; one steady window through Zeeshan's zoom at 13.2; the eating clip's face above the key point",
       "everything the previous review passed is otherwise unchanged"],
 "H": ["since the latest review (its only defect: Dan's gesturing arm touching the right edge with spare room on the left at three moments): the wide crop 0:08.14-0:10.68 sits 20 px further right (head still 23 source px clear on the left); the wide crop 0:18.89-0:25.19 sits 25 px further right (head 36 px clear left, 72 right); the night drive now runs to 0:34.72 (cut between \"got\" and \"the\"), so Dan's off-centre entry at 34.40 is covered, and the crop after it is centred on his median position",
       "earlier in this round (verify they still hold): the closer crop 0:10.68-0:18.89 steady and centred; the cut to the wider crop in the pause at 0:18.89 before Zeeshan's zoom-in; the key point \"Wind Down Before Bed / Don't Rev Yourself Up\"; Zeeshan's AI Tesla clip at 0:36.40-0:40.61 cropped so his burned text and the speed display never show, with our AI-GENERATED chip; his lower third never shows; captions match Zeeshan's finalized subtitles at both \"bedtime\" lines",
       "everything the previous review passed is otherwise unchanged"],
 "J": ["since the latest review: (D1) the AbsByAI.com mark is now really absent while the phone is alone on screen (that render had started before the change landed); (D2) Dan's recording now fills the whole rounded phone screen (538 x 1200, corner radius matching the screen), cropped at film rows 170-861 so the recording's own white home bar and the black rows under Zeeshan's mock are out; the app's own floating tab bar shows at the bottom as it does on the real phone",
       "earlier in this round: 0:00-0:03.70 the opening phone no longer sits frozen: it plays Dan's real Oura recording where it scrolls through his sleep contributors (film 7:05.3-7:10.9, at 1.5x speed), the phone rises 24 px at a constant speed for its whole time on screen, and the screen crop now ends above the black rows under Zeeshan's phone mock",
       "0:20.6-0:45.6 the comparison card's light sweep now runs through the final frame (previous advisory: it stopped for the last 1.9 s)",
       "earlier in this round: 0.6 s cut from the middle of the 1.32 s pause after \"that's a better location.\" (the delivery gate's dead-air row), and the end stops before Zeeshan's zoom into his outro",
       "previous D2 (show the Oura ring and the WHOOP) is answered by two AI frame ideas for Dan's approval on the review page (J1 opener, J2 at 0:13.8-0:20.6); AI motion is made only after he approves the frames, so this review copy keeps the current pictures there"],
 "I": ["since the latest review: (D1) the caption at about 0:53.2 now prints \"change your behavior\" (forced alignment scores \"your\" -95 against -116 for \"their\"; the free decode reads \"CHANGE OR BEHAVIOR\"; Zeeshan's subtitles print \"your\")",
       "earlier in this round (verify they still hold): no frame of Zeeshan's white flash at 0:35.87; the piece ends at film 1065.17 before his swoosh; the key point \"Nobody Is Worth / Losing Your Sleep Over\"; captions never end before their last word at a cut",
       "everything the previous review passed is otherwise unchanged"],
}
SEC = {"A": "A.", "H": "H.", "I": "I.", "J": "J.", "K": "K."}[S]
chg = "\n".join(f"- {c}" for c in CHANGED[S]) or "- (first review of this file)"
print(f"""You are the independent reviewer of one delivered YouTube Short. Expect it NOT to ship; the builder believes it is fine.

FILE: `{V}` (short {P.ORDER[S]} of 5, "{TITLES[S]}"). sha256 should be {sha}.
CATEGORY: CONTENT, a Short extracted from Zeeshan's finished long-form "My Honest Oura Ring Review After 1.5 Years" (his finished master: `{P.MASTER}`, 1920x1080 29.97 fps, decode BT.709).
SOURCE PIECES (master seconds, played in this order): {P.SEG[S]}.

READ FIRST (and nothing the builder wrote about how it built this short: no editor notes, no build scripts, no shots.json):
- `{ROOT}/AGENTS.md`
- `{ROOT}/Handoffs/video-editing/00-RULES.md`
- `{ROOT}/.claude/skills/_shared/VIDEO-RULES.md`
- `{ROOT}/.claude/skills/_shared/GRAPHICS-STANDARDS.md` (the "Soft Blue shorts standard": title band y 0-310 whole short, picture 1080x1610 below it, key-point bars at 68,1130-1012,1378, captions from y 1412)
- The plan: `{ROOT}/.claude/worktrees/nostalgic-lovelace-274489/Handoffs/handoff-20261018-sl09-oura-shorts-r2-build-a-h-i-j-k.md`, the general sections plus section "{SEC}"
- The previous review of the earlier render, for what it found (verify each item yourself on THIS file, which is a new render): `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/ROUND-2-REVIEW.md` (you will overwrite it).

WHAT THE BUILDER CHANGED SINCE THAT REVIEW (verify each on the delivered file; do not take it on trust):
{chg}

Standing rules to check in particular: Zeeshan's picture and mix carried untouched (audio cut only at seams, --verbatim); his burned graphics whole or absent, never sliced; hair never leaves the top of the frame and Dan's head never cut at the sides; land-then-hold framing (no busy pans, no window change on continuous footage, no jump cuts: a same-framing join must have a real size change or a clip over it); every clip shows what the words say (with sound off, would a stranger see it?); no stock actor who reads as Dan; no repeated stock; no identifiable other car or plate on driving clips; B-roll colour matched to the presenter and never a flat grey or near-black screen; captions print exactly what he says (swearing stays) and never sit on a card or vanish before the word is finished; title capitalization on graphics; every graphic keeps moving for its whole screen time; key points distill, never echo, and never cover a face; the first 5 seconds are attention-getting; length under 0:59; clean start and end (no clipped word, no editor transition leaking in at the end). If the short contains an AI-generated clip, ask the three sense questions of each (cause and effect; would a stranger say what it shows with the sound off; does it show the line) and check its AI-GENERATED chip sits off faces and abs. A stock-only short needs no chip.

JOB 1 (watch pass): follow `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/gate/watch/JUDGE_PROMPT.md` exactly (read CHECKLIST.md, open EVERY sheet, strip and pair image listed in `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/gate/logs/watch_pass.json`, one verdict per image) and write `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/gate/logs/findings.json` in the format it gives. Only judge images that watch_pass.json lists, and check its sha256 matches the file.

JOB 2 (full-resolution audit): decode the delivered file yourself (project ffmpeg `{ROOT}/Media/video_edit/bin/ffmpeg`, BT.709 decode `scale=in_color_matrix=bt709:in_range=tv`, frame-exact `select=eq(n\\,N)` or seek at least 2 s before a target), transcribe its audio with Whisper yourself, compare against the master at the source pieces, and audit every area above. Work in scratch folder `/Volumes/Extreme/_edit_work/sl09/round2/review_{S}3_scratch/` (create it; never write anywhere else except the two output files). Before any heavy decode or Whisper run, check the machine's build cap with `python3 "{ROOT}/.claude/skills/_shared/buildcap.py"` and keep your own work light (nice -n 10). Do not render, do not run gates, do not edit any build file.

Write `/Volumes/Extreme/_edit_work/sl09/round2/build/{S}/ROUND-2-REVIEW.md` (replace the old one) with: file facts (measured), watch pass result, audit by area, the previous review's items one by one (fixed or not), defects that block shipping (output timestamps, what is wrong, what to change), advisories, what you could not verify, and a last line exactly `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`. No em dashes anywhere in what you write. Report back the verdict, each defect with its time, and the findings counts.""")
