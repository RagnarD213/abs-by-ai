#!/usr/bin/env python3
"""Regression test: the auto content sheets for Ad 10 and Ad 1 against their answer keys (answer_keys/README.md).
  python3 test_answer_keys.py --ad10 BUILD_DIR --ad1 BUILD_DIR [--accept]"""
import argparse, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--ad10"); ap.add_argument("--ad1"); ap.add_argument("--accept", action="store_true")
a = ap.parse_args()
rc = 0
for ad, B in (("ad10", a.ad10), ("ad1", a.ad1)):
    if not B:
        continue
    K = os.path.join(HERE, "answer_keys", ad)
    base = os.path.join(K, "baseline.json")
    out = os.path.join(B, "compare.json")
    cmd = [sys.executable, os.path.join(HERE, "compare_content.py"), "--auto", os.path.join(B, "content.json"),
           "--auto-assets", os.path.join(B, "assets.py"), "--key", os.path.join(K, "content.json"),
           "--key-assets", os.path.join(K, "assets.py"), "--out", out]
    kr = os.path.join(K, "key_root.txt")
    if os.path.exists(kr) and os.path.isdir(open(kr).read().strip()):
        cmd += ["--key-root", open(kr).read().strip()]       # the key's relative media (its build dir's crops)
    if os.path.exists(base) and not a.accept:
        cmd += ["--baseline", base]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"== {ad}: exit {r.returncode}")
    print("\n".join(l for l in r.stdout.splitlines() if "REGRESSION" in l or "HARD" in l or l.startswith("  ")))
    rc = rc or r.returncode
    if a.accept and r.returncode != 2:
        shutil.copy(out, base)
        print(f"   baseline accepted -> {base}")
print("PASS" if rc == 0 else "FAIL")
sys.exit(rc)
