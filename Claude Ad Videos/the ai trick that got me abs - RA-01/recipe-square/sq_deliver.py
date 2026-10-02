#!/usr/bin/env python3
"""Lay the square delivery out beside the approved 9:16 / 16:9. Refuses unless every stamp is a
PASS whose sha256 is the delivered bytes ([S1] C: a stamp counts only if it names this file)."""
import hashlib, json, os, shutil, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01-sq")
import ra01lib as L
W = "/Volumes/Extreme/_edit_work/ra01-sq"
DEST = f"{L.REPO}/Claude Ad Videos/the ai trick that got me abs - RA-01"
T = "the ai trick that got me abs"
NAME = f"{T} | claude | 1x1 | RA-01.mp4"
REV = f"{T} | REVIEW 540p 1x1 | RA-01.mp4"
AB = f"{T} | AB audio ref-vs-ours 1x1 | RA-01.mp4"
M = f"{W}/master_1x1.mp4"
sha = hashlib.sha256(open(M, "rb").read()).hexdigest()
for ext in (".audio_gate.json", ".deliver_gate.json", ".labelcheck.json"):
    d = json.load(open(M + ext))
    v = d.get("verdict") or ("PASS" if d.get("ok") else "FAIL")
    assert v == "PASS", (ext, v)
    assert d.get("sha256") == sha, (ext, "stamp is for other bytes")
    shutil.copy2(M + ext, f"{DEST}/{NAME}{ext}")
shutil.copy2(M + ".audio_untreated.json", f"{DEST}/{NAME}.audio_untreated.json")
shutil.copy2(M, f"{DEST}/{NAME}")
assert hashlib.sha256(open(f"{DEST}/{NAME}", "rb").read()).hexdigest() == sha
subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", M, "-vf", "scale=540:540", "-c:v", "libx264",
                "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart", f"{DEST}/{REV}"], check=True)
shutil.copy2(f"{W}/AB_ref-vs-ours.mp4", f"{DEST}/{AB}")
shutil.copy2(f"{W}/notes-square.md", f"{DEST}/notes-square.md")
R = f"{DEST}/recipe-square"
shutil.rmtree(R, ignore_errors=True); os.makedirs(R)
for f in sorted(os.listdir(W)):
    if f.startswith("._"): continue
    if f.endswith((".py", ".sh", ".md")) or f in ("beats.json", "beats_9x16_approved.json", "cut.json", "framing.json",
            "words_aligned.json", "grade.json", "face_src_r3.json", "hard_splices.json", "timeline_1x1.json",
            "audio_identity.json", "caption_states_9x16.json"):
        if f == "notes-square.md": continue
        shutil.copy2(f"{W}/{f}", f"{R}/{f}")
for src, dst in [("recipe-square/gate_plan_1x1.json", "gate_plan_1x1.json"), ("cards_1x1/meta.json", "cards_meta.json"),
                 ("cta_1x1/cta.json", "cta.json"), ("r3/verify_1x1.json", "framing_verify_1x1.json"),
                 ("watchpass_1x1/watch_pass.json", "watch_pass.json"), ("watchpass_1x1/findings.json", "watch_findings.json")]:
    if os.path.exists(f"{W}/{src}"): shutil.copy2(f"{W}/{src}", f"{R}/{dst}")
print(DEST); print(NAME, sha)
