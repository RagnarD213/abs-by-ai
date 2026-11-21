#!/usr/bin/env python3
"""THE MISSING ENFORCEMENT. Every QC and every deliver script calls this before it passes a file.

  python3 require_stamp.py <finished file> [--allow-synthetic]     exit 0 = stamped PASS, else 1
  from require_stamp import require_stamp; require_stamp(path)     raises SystemExit with the reason

Checks: the stamp exists beside the file, its sha256 matches THIS file (a re-render without a
re-gate fails), its verdict is PASS, and it was measured against the currently pinned reference.
Before 2026-09-02 the right-channel rule existed in four SKILL.md files and nothing enforced it;
this is the piece every previous fix lacked.

⚠ STRICT IS THE DEFAULT (2026-09-09, Phase 0 of the video-quality programme). This used to default
to synthetic_ok=True and require an opt-IN `--strict` that NO SKILL.md ever passed -- so a weakened
4-row `--synthetic` stamp (loudness / true peak / silence / length only, no room, tone, comb,
artifacts or do-no-harm) silently satisfied every caller that wanted the full 11-row camera gate.
A bypass nobody opts out of is not a safeguard. Now camera audio must carry the full stamp, and the
three skills whose voice is genuinely synthetic (`make-ad`, `exercisegeneration`, `findassets`) say
so explicitly with `--allow-synthetic` / synthetic_ok=True at the call site, where a reader can see it.
`--strict` is still accepted and is a no-op.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

META = os.path.join(C.HERE, "reference", "reference.json")


def require_stamp(path, synthetic_ok=False, quiet=False):
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
        raise SystemExit(f"{os.path.basename(path)} carries only a --synthetic stamp (loudness / true peak / "
                         f"silence / length; no room, tone, comb, artifacts or do-no-harm) and this caller "
                         f"needs the full camera-audio gate -- re-gate without --synthetic, or pass "
                         f"--allow-synthetic here if this really is an AI voice")
    if not quiet:
        print(f"  audio gate stamp OK  {os.path.basename(path)}  ({s.get('gated_at')}"
              + (", synthetic" if s.get("synthetic") else "") + ")")
    return s


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a: raise SystemExit(__doc__)
    allow = "--allow-synthetic" in sys.argv or "--synthetic-ok" in sys.argv
    try:
        require_stamp(a[0], synthetic_ok=allow)
    except SystemExit as e:
        if e.code not in (0, None): print(f"  ✗ {e}"); sys.exit(1)
