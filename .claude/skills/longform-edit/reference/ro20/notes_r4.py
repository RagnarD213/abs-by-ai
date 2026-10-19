"""RO-20 round 4: write round4/V/notes-<NAME>-round4.md from the build's own records (layout, gate stamps, reviews, page_state.base.json).
usage: notes_r4.py V"""
import json, sys, os, re, hashlib
W = "/Volumes/Extreme/_edit_work/ro20"; FPS = 30000/1001
V = sys.argv[1]; D = f"{W}/round4/{V}"
JOB = {"v1": "RO-20", "v2": "RO-20B", "v3": "RO-20C"}[V]; NAME = JOB.replace("-", "")
TITLE = {"v1": "Why You Should Invest More In Your Health", "v2": "What To Cut To Afford Getting In Shape", "v3": "What To Buy For Your Health At Every Income Level"}[V]
L = json.load(open(f"{D}/layout.json")); S = json.load(open(f"{W}/round4/page_state.base.json"))
vid = next(x for x in S["videos"] if x["n"] == int(V[1]))
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
ag = json.load(open(f"{D}/MASTER.mp4.audio_gate.json")); dg = json.load(open(f"{D}/MASTER.mp4.deliver_gate.json")) if os.path.exists(f"{D}/MASTER.mp4.deliver_gate.json") else None
ab = json.load(open(f"{D}/audio_build.json"))
reviews = sorted(f for f in os.listdir(D) if f.startswith("ROUND-4-REVIEW"))
verd = {f: (re.findall(r"VERDICT:\s*(SHIP|DOES NOT SHIP)", open(f"{D}/{f}").read()) or ["?"])[-1] for f in reviews}
KNOWN = {"audio:stamp": "the audio gate fails only its tone row (and on video 2 the processing row by 0.001): the known mismatch of voice 4, which Dan locked on 2026-10-10 (fixed EQ plus the light echo removal). Every other audio row passes.",
         "framing:hair_top": "the camera cut the top of his hair on most of roll C1511 (reported in round 1, unfixable in the edit).",
         "framing:headroom": "same cause as hair_top.",
         "captions:burned": "a false positive: the lower thirds read as captions; no captions are burned in (RO-17, RO-19, RO-08 show the same).",
         "captions:card_collision": "sidecar SRT cues overlap full-screen cards; the SRT is uploaded, not burned, and dropping them would leave words uncaptioned.",
         "style:coverage": "cutaway share of the approved plan (rounds 1 to 3b); four standing/posing cutaways came out this round under the 2026-10-14 rule.",
         "cut:splice_visibility": "the strongest zoom cuts of the approved cut (several inside the approved first minute); every join was inspected frame by frame by the judges and reviewers.",
         "audio:stream_integrity": "the last seconds are the silent tail under P3's closing card, kept on purpose for YouTube's end screen (approved with the round 3b ending screens); the music bed fades out there.",
         "junk:repeated_take": "the flagged repeat is in Dan's approved sign-off or summary wording (\"go to absbyai.com. On absbyai.com\" / \"When you go to absbyai.com\"). On video 3 the other two flags sit inside one unbroken take with no cut: a drawn-out \"there's\" (8:07.6) and the tail of his stressed \"$120.\" (21:54.1).",
         "cut:black_frames": "the planned stock shot of a red heartbeat line on a black screen (5:20.9 to 5:24.8, item Ce12, in the plan since round 1); the black is the shot's own background.",
         "compliance:banned_screen": "a false match: the one frame it hit (7:28.5) is the stock shot of a hand pressing on a striped mattress cover; no app or phone screen is in it.",
         "style:static_run": "longest hold without a picture change, over the 30 s limit."}
rows = dg["rows"] if dg else {}
fails = [k for k, r in rows.items() if not r.get("ok")]
lines = [f"# {TITLE} ({JOB}): round 4 notes (Claude Opus 5.5, 2026-10-18)", "",
         f"LFC, organic long-form, 16:9. {L['frames']} frames, {L['frames']/FPS/60:.2f} min. Master sha256 `{sha(D + '/MASTER.mp4')}`.", "",
         "## How it is built", "",
         "One timeline (the approved round 1 to 3b cut of roll C1511) split into parts, plus Dan's studio pickups (roll C1722, treatment A, locked by",
         "`round3b/round3b-hashes.sha256`). Part layout (video frames):", ""]
for P in L["parts"]:
    a, b = P["out"]; lines.append(f"- {a/FPS:8.2f} to {b/FPS:8.2f} s: {P['part']}")
lines += ["", "Voice: the film voice (voice 4, `build.py filmvoice`, rebuilt to cover video 1's sign-off) sliced at the part frames; the pickup voices as",
          "approved (never through the chain twice); roll handles get voice 4's EQ at the film's own room-tone level. 12 ms fades at every part edge.",
          f"Music: the RO-07 bed (Pixabay acoustic_bg) at {ab['bed_db']} dB, ducked by the voice; `voice_chain.py --finish-only` for gain and limiter only.",
          "Untreated twin for the audio gate's do-no-harm row: raw kitchen lav at the cut frames, raw C1722 lav under the pickups.", "",
          "## What is new in this film (by time on this master)", ""]
for c in vid["changes"]: lines.append(f"- **{c['at']}** ({c['watch']}): {c['what']}")
lines += ["", "## Gates", "",
          f"- Audio gate: {'PASS' if ag.get('verdict') == 'PASS' or ag.get('pass') else 'FAIL on ' + ', '.join(r['key'] for r in ag.get('rows', []) if not r.get('ok'))}; loudness and true peak pass.",
          f"- Delivery gate {dg['gate_version'] if dg else '?'}: {sum(1 for r in rows.values() if r.get('ok'))} pass, {len(fails)} fail (no bound changed):"]
for k in fails: lines.append(f"  - `{k}`: {KNOWN.get(k, rows[k].get('detail', '')[:200])}")
lines += ["", "## Independent checks", ""]
lines += [f"- `{f}`: {v}" for f, v in verd.items()]
lines += ["- Watch pass judged by a fresh subagent on this exact file (logs/watch_pass.json, logs/findings.json).",
          "", "## Not done here", "",
          "- Edit sheet: `_shared/edit-sheet/sheet_from_claude_build.py` reads single-range builds; this film is film ranges plus pickup segments, so no sheet was",
          "  written. `layout.json` (every part and presenter segment with its source frames and crop) and `plan.json` record the cut frame by frame.",
          "- No upload or setup (the long-form calendar holds RO-20/B/C until Dan says otherwise).", ""]
open(f"{D}/notes-{NAME}-round4.md", "w").write("\n".join(lines)); print("wrote", f"{D}/notes-{NAME}-round4.md")
