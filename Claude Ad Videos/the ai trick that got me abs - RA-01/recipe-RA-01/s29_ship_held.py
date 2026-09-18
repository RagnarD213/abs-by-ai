#!/usr/bin/env python3
"""RA-01 round 1 delivery, HELD-MASTER path (the Ad 4 precedent).

A master whose audio-gate or delivery-gate stamp reads FAIL is NOT put in the delivery folder and
is NOT forced through the delivery script. It stays in the work dir. What Dan still gets is
everything he needs to make the call:

    the two REVIEW 540p copies, the audio A/B clip, notes-RA-01.md, recipe-RA-01/ and
    measurements-RA-01.json

Run:  python3 s29_ship_held.py            (builds the review copies, then lays the folder out)
      python3 s29_ship_held.py --masters  (ALSO copies the masters -- only when both stamps PASS)
"""
import json, os, shutil, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L

W = "/Volumes/Extreme/_edit_work/ra01"
DEST = f"{L.REPO}/Claude Ad Videos/the ai trick that got me abs - RA-01"
TITLE = "the ai trick that got me abs"
NAME = {"9x16": f"{TITLE} | claude | 9x16 | RA-01.mp4",
        "16x9": f"{TITLE} | claude | 16x9 | RA-01.mp4"}
REV = {"9x16": f"{TITLE} | REVIEW 540p 9x16 | RA-01.mp4",
       "16x9": f"{TITLE} | REVIEW 540p 16x9 | RA-01.mp4"}
AB = f"{TITLE} | AB audio ref-vs-ours | RA-01.mp4"
SCALE = {"9x16": "scale=540:960", "16x9": "scale=960:540"}
WANT_MASTERS = "--masters" in sys.argv

os.makedirs(DEST, exist_ok=True)


def stamps(key):
    """(audio verdict, deliver verdict) for master_<key>.mp4, or None when a stamp is absent."""
    out = []
    for ext in (".audio_gate.json", ".deliver_gate.json"):
        p = f"{W}/master_{key}.mp4{ext}"
        if not os.path.exists(p):
            out.append(None); continue
        d = json.load(open(p))
        out.append(d.get("verdict") or ("PASS" if d.get("ok") else "FAIL"))
    return tuple(out)


held = {}
for key in ("9x16", "16x9"):
    a, g = stamps(key)
    held[key] = not (a == "PASS" and g == "PASS")
    print(f"master_{key}.mp4   audio_gate {a}   deliver_gate {g}   -> "
          f"{'HELD in the work dir' if held[key] else 'deliverable'}")

# --- REVIEW 540p copies, built from the master in the WORK DIR (held or not) -------------------
for key in ("9x16", "16x9"):
    src, dst = f"{W}/master_{key}.mp4", f"{DEST}/{REV[key]}"
    if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
        print(f"  (review {key} already current)"); continue
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", src, "-vf", SCALE[key],
                    "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", dst], check=True)
    print(f"  {REV[key]}")

# --- everything else --------------------------------------------------------------------------
# round 2 also carries the grade evidence (R5) and the delivered-frame verification (R2/R5)
for src, dst in [(f"{W}/AB_ref-vs-ours.mp4", AB),
                 (f"{W}/notes-RA-01.md", "notes-RA-01.md"),
                 (f"{W}/measurements-RA-01.json", "measurements-RA-01.json"),
                 (f"{W}/flux_diagnosis.json", "flux_diagnosis.json"),
                 (f"{W}/grade.json", "grade.json"),
                 (f"{W}/r2/grade/proof.jpg", "grade_proof.jpg"),
                 (f"{W}/r2/verify_9x16.json", "verify_9x16.json"),
                 (f"{W}/r2/verify_16x9.json", "verify_16x9.json"),
                 (f"{W}/ROUND-2-EDITOR.md", "ROUND-2-EDITOR.md"),
                 # round 3 (plan section 13): the proof for the four things it changed
                 (f"{W}/ROUND-3-EDITOR.md", "ROUND-3-EDITOR.md"),
                 (f"{W}/r3/verify_9x16.json", "r3_framing_9x16.json"),
                 (f"{W}/r3/verify_16x9.json", "r3_framing_16x9.json"),
                 (f"{W}/r3/bed_fix.json", "r3_music_bed_fix.json"),
                 (f"{W}/r3/tail_envelope.json", "r3_music_tail_envelope.json"),
                 (f"{W}/r3/pill16.jpg", "r3_cta_pill_16x9_proof.jpg"),
                 (f"{W}/r3/pill16.json", "r3_cta_pill_16x9.json")]:
    if not os.path.exists(src):
        print(f"  MISSING {src}"); continue
    shutil.copy2(src, f"{DEST}/{dst}")
    print(f"  {dst}")

# the stamps travel even when the master does not -- they are the evidence for the hold
for key in ("9x16", "16x9"):
    for ext in (".audio_gate.json", ".deliver_gate.json", ".audio_untreated.json"):
        p = f"{W}/master_{key}.mp4{ext}"
        if os.path.exists(p):
            shutil.copy2(p, f"{DEST}/{NAME[key]}{ext}")
            print(f"  {NAME[key]}{ext}")

if os.path.isdir(f"{W}/recipe-RA-01"):
    shutil.rmtree(f"{DEST}/recipe-RA-01", ignore_errors=True)
    shutil.copytree(f"{W}/recipe-RA-01", f"{DEST}/recipe-RA-01")
    if os.path.exists(f"{W}/r2/grade/proof.jpg"):
        shutil.copy2(f"{W}/r2/grade/proof.jpg", f"{DEST}/recipe-RA-01/grade_proof.jpg")
    print("  recipe-RA-01/")

for key in ("9x16", "16x9"):
    tgt = f"{DEST}/{NAME[key]}"
    if held[key]:
        if os.path.exists(tgt):
            os.remove(tgt)
            print(f"  removed a previously placed {NAME[key]} -- it is HELD")
        continue
    if WANT_MASTERS:
        shutil.copy2(f"{W}/master_{key}.mp4", tgt)
        print(f"  {NAME[key]}")
    else:
        print(f"  {NAME[key]} is deliverable -- re-run with --masters to place it")

print("\n" + DEST)
