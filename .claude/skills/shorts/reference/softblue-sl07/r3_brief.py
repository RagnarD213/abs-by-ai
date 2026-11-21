#!/usr/bin/env python3
"""print the round 3 independent-review brief for one short (plan + standing rules only, no editor notes)"""
import json, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/sl07"); import plans as P
S = sys.argv[1]; W = "/Volumes/Extreme/_edit_work/sl07"; FPS = 30000 / 1001
V = f"/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/belly-fat-90-days-{P.NAME[S]}.mp4"
sh = json.load(open(f"{W}/build/{S}/shots.json")); man = json.load(open(f"{W}/build/{S}/hf/manifest.json"))
DESC = {"scale": "stock: overhead view, feet on a bathroom scale", "scale2": "stock: overhead view, feet on a bathroom scale", "study": "rebuilt film graphic: the study card (daily weighers lost about 13 lb more)",
        "needle": "AI clip (approved frames): a man stands still on an analog scale, only the needle swings back and forth", "chart": "rebuilt film graphic: daily weight dots and the 7-day average line",
        "pray": "AI clip (approved frames): a man kneels and prays to a bathroom scale", "candles": "AI clip (approved frames): same man bows to the scale, two candles beside it",
        "jumprope": "real B-roll of Dan: fast jump rope by the pool", "rope": "real B-roll of Dan: fast jump rope by the pool", "stairs": "library AI clip A0159: a heavier man eases down stairs, sore",
        "abwheel": "real B-roll of Dan: ab wheel rollout by the pool, shown as a full-width card (his travel is about 1,400 px sideways)", "morning": "stock: early morning scene",
        "curls": "real B-roll of Dan: alternating dumbbell curls by the pool", "traffic": "stock: traffic / commute", "family": "stock: a dad and his daughter in a kitchen",
        "beer": "AI clip (approved frames): a fit man raises a beer on a patio",
        "salad": "library B-roll B0019: salad packed into meal containers",
        "cups": "AI clip (approved frames): a tired man at a kitchen counter with a food scale, a binder and a tower of measuring cups turns a page and slumps onto the binder",
        "photo": "the app on a phone beside Dan: photographing food, the calories and macros appear", "log": "the app on a phone beside Dan: the day's meal log"}
rows = []
for s in sh:
    a, b = s["f0"] / FPS, s["f1"] / FPS
    if s["kind"] == "talk": rows.append(f"- {a:6.2f} to {b:6.2f}: Dan on camera ({s.get('win')} window)")
    else: c = s["cover"]; rows.append(f"- {a:6.2f} to {b:6.2f}: {DESC.get(c['id'], c['id'])}" + (" [AI-GENERATED chip expected]" if c.get("ai") else ""))
bars = "\n".join(f"- {m['a']:.2f} to {m['b']:.2f}: {m['topic']} / " + " / ".join(p[0] for p in m["parts"]) for m in man)
pk = P.PICKUP.get(S)
pick = (f"""
THE OPENING PICKUP (new this round, check it hardest). The first sentence, "{pk['text']}", is a separate recording: Dan read it on 10/15 on the
green screen set with the shoot's clip-on mic (roll C1722), treated with {"the film's voice EQ" if S == "D" else "a band-by-band tone match to the film voice plus a light de-esser"}, level matched to the film line after it, peak capped,
8 ms fade in; its last 60 ms crossfade into the film's own room sound from just before the film line{' (plus 0.2 s more of the film pause)' if S == 'D' else ''}. Everything after it is the long-form film's approved mix, cut only. Picture under the pickup is B-roll (the green screen
must never show). Judge: are all words whole and clean; is the join to the film line natural in timing (compare his normal sentence pause in this
same file); does the pickup sound like a different recording (tone, room, level, noise)? Report what you hear and measure, plainly. The raw take is
`{W}/pickups/studio1015/{'B2' if S == 'B' else 'D2'}_raw.wav` if you want to compare. A tone difference is a NOTE for Dan's ear, not a defect, unless it is
gross (clipping, distortion, a word cut, a click, a level jump you can hear).""" if pk else "")
print(f"""You are the INDEPENDENT REVIEWER (fresh, round 3) for one delivered vertical Short of the Abs By AI channel. You have never seen it.
Judge only the delivered file against the plan below and the standing rules. Do NOT read any editor notes, review pages, earlier review files,
handoffs, `notes_*.py`, `page_*.py`, or anything under `{W}/r2/` or `{W}/r3/review`. The session that built it believes it is fine; be skeptical.

FILE: `{V}`
TITLE: "{' '.join(P.TITLE[S][1])}" (title band at the top all the way through). CONTENT short cut from Dan's long-form "If I Had Belly Fat, Here's How I'd Lose It In 90 Days".
WORDS (as spoken; `shown{{spoken}}` = how numbers are captioned; ` | ` = an audio join):
{P.TEXT[S]}

PICTURE PLAN (output seconds):
{chr(10).join(rows)}

KEY-POINT LOWER THIRDS:
{bars}
{pick}

YOUR SCRATCH FOLDER (use only this for frames, audio, anything you write): `/private/tmp/sl07_r3b/scratch_{S}/` (create it; the external drive is full, so never write frames there).
Tools: ffmpeg/ffprobe at `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/`. Python 3 with numpy, PIL, whisper available.

DO ALL OF THIS:
1. The watch-pass judge job: follow `{W}/build/{S}/gate/watch/JUDGE_PROMPT.md` exactly (every sheet and strip image, one at a time, checklist
   `{W}/build/{S}/gate/watch/CHECKLIST.md`), and write `{W}/build/{S}/gate/logs/findings.json` in the format it gives, with ONE ENTRY FOR
   EVERY IMAGE listed in `{W}/build/{S}/gate/logs/watch_pass.json`, pair_* images included, each opened on its own with the Read tool. Do not run `--judge` yourself.
2. Watch the whole file yourself (decode frames sequentially; check every cut at full resolution with the frames on both sides) and listen to all of it.
3. Standing rules to check on the delivered file:
   - Every AI clip: ask the three sense questions at playback speed and answer each in one line per clip: (1) does everything obey cause and
     effect (nothing vanishes, appears, melts or changes by itself)? (2) with the sound off, would a stranger say what it shows? (3) does it show
     the line being said? Also: AI-GENERATED chip present for the whole clip, readable, not over a face or hair, not off the frame.
   - Never a shot of Dan just standing, posing or waiting; never junk footage between takes (drinking water, looking away). Exercise clips show
     the movement from the first second. A cutaway shows the thing the line names.
   - Dan's hair never touches or leaves the top of the picture area on any frame of a talking shot. No jump cut between two same-size shots of him.
   - Clips fill the frame unless a reason (a card must keep the clip's full height; no rows cropped off a card).
   - B-roll brightness sits with the studio presenter frames (nothing visibly darker).
   - Captions: match the spoken words, no caption across a cut by more than a few frames, nothing over his face, first and last word not clipped.
   - Key points: readable, not over his face, line 1 alone must not say something wrong, stays up long enough to read.
   - The ending: the last word is whole (check the waveform to 10 ms against the words).
   - No belly-fat close-ups or pinching; no stick figures; no em dashes in any on-screen text.
4. Write `{W}/r3/reviews/ROUND-3C-REVIEW-{S}.md`. First line exactly `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`. Then the file sha256, what you
   checked and how, every defect with exact time and a concrete fix, then notes (non-blocking). The delivery gate runs AFTER your review, so
   a missing `.deliver_gate.json` is expected, not a defect. Only a real defect a viewer would notice, or a
   rule break, is DOES NOT SHIP.
5. Reply with: verdict, the findings.json counts (clean / expected / defect), every defect with time, and the pickup verdict if there is one.""")
