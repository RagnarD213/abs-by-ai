#!/usr/bin/env python3
"""THE MISSING ENFORCEMENT. Every QC and every deliver script calls this before it passes a file.

  python3 require_stamp.py <finished file> [--synthetic-ok]      exit 0 = stamped PASS, else 1
  from require_stamp import require_stamp; require_stamp(path)   raises SystemExit with the reason

Checks: the stamp exists beside the file, its sha256 matches THIS file (a re-render without a
re-gate fails), its verdict is PASS, and it was measured against the currently pinned reference.
Before 2026-09-02 the right-channel rule existed in four SKILL.md files and nothing enforced it;
this is the piece every previous fix lacked.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

META = os.path.join(C.HERE, "reference", "reference.json")


def require_stamp(path, synthetic_ok=True, quiet=False):
    sp = C.stamp_path(path)
    if not os.path.exists(sp):
        raise SystemExit(f"NO AUDIO GATE STAMP for {os.path.basename(path)} -- run "
                         f"_shared/audio/audio_gate.py on the exact delivered file (not deliverable without it)")
    s = json.load(open(sp))
    ref = json.load(open(META)) if os.path.exists(META) else {}
    if s.get("sha256") != C.sha256(path):
        raise SystemExit(f"AUDIO GATE STAMP IS FOR A DIFFERENT BUILD of {os.path.basename(path)} "
                         f"(sha256 mismatch) -- the file changed after it was gated; re-run audio_gate.py")
    if s.get("verdict") != "PASS":
        bad = ", ".join(r["key"] for r in s.get("rows", []) if not r["ok"])
        raise SystemExit(f"AUDIO GATE FAILED on {os.path.basename(path)}: {bad} -- fix the audio, do not deliver")
    if ref and s.get("reference", {}).get("sha256") != ref.get("sha256"):
        raise SystemExit(f"stamp on {os.path.basename(path)} was measured against a different reference "
                         f"fingerprint -- re-run audio_gate.py")
    if s.get("synthetic") and not synthetic_ok:
        raise SystemExit(f"{os.path.basename(path)} carries only a --synthetic stamp; this skill needs the full camera-audio gate")
    if not quiet:
        print(f"  audio gate stamp OK  {os.path.basename(path)}  ({s.get('gated_at')}"
              + (", synthetic" if s.get("synthetic") else "") + ")")
    return s


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a: raise SystemExit(__doc__)
    try:
        require_stamp(a[0], synthetic_ok="--synthetic-ok" in sys.argv or "--strict" not in sys.argv)
    except SystemExit as e:
        if e.code not in (0, None): print(f"  ✗ {e}"); sys.exit(1)
