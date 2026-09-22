#!/usr/bin/env python3
"""Audit an explicit raw-roll inventory after the background backfill finishes."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import roll_sidecar as rolls


BASELINE_GEMINI_USD = 0.278432  # 284 existing sidecars before the 2026-09-22 continuation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    sources = inventory["rows"]
    mirror = rolls.mirror_content_index()
    missing = []
    changed = []
    for source in sources:
        clip = Path(source["path"])
        if not clip.is_file():
            missing.append(source["path"])
            continue
        if rolls.content_identity(clip)["content_key"] != source["content_key"]:
            changed.append(source["path"])
        if source["content_key"] not in mirror:
            missing.append(source["path"])
    tool = Path(rolls.__file__).resolve()
    tests = tool.parent / "tests" / "test_roll_sidecar.py"
    results = {}
    for name, command, env in [
        ("tests", [sys.executable, str(tests)], None),
        ("verify", [sys.executable, str(tool), "verify"], None),
        ("offline_vacuum", [sys.executable, str(tool), "find", "dramatic vacuum"], {"ROLL_SOURCE_OFFLINE": "1"}),
        ("offline_c1579", [sys.executable, str(tool), "find", "gray cloth"], {"ROLL_SOURCE_OFFLINE": "1"}),
        ("offline_broll", [sys.executable, str(tool), "find", "jump rope", "--shoot", "B-Roll - Real Footage"], {"ROLL_SOURCE_OFFLINE": "1"}),
    ]:
        environment = os.environ.copy()
        if env:
            environment.update(env)
        result = subprocess.run(command, cwd=rolls.repo_root(), env=environment,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
        output = result.stdout[-3000:]
        passed = result.returncode == 0
        if name.startswith("offline_"):
            passed = passed and "drive unplugged" in output
        results[name] = {"passed": passed, "exit_code": result.returncode, "output": output}
    tracked_sidecars = subprocess.run(
        ["git", "ls-files", "--", "Media/footage-index", "*.roll.json", "*.roll.md"],
        cwd=rolls.repo_root(), stdout=subprocess.PIPE, text=True, check=False,
    ).stdout.splitlines()
    ledger = rolls.mirror_root() / "_gemini_usage.jsonl"
    attempts = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()] if ledger.exists() else []
    session_cost = round(sum(float(row.get("estimated_actual_usd") or 0) for row in attempts), 6)
    keys = [row["content_key"] for row in sources]
    report = {
        "source_paths": len(sources), "unique_source_keys": len(set(keys)),
        "indexed_source_paths": len(sources) - len(missing), "missing_source_paths": missing,
        "changed_source_paths": changed, "duplicate_source_paths": len(sources) - len(set(keys)),
        "mirror_sidecars": len(rolls.all_mirror_sidecars()),
        "historical_gemini_estimate_usd": BASELINE_GEMINI_USD,
        "session_gemini_attempts": len(attempts), "session_gemini_estimate_usd": session_cost,
        "total_gemini_estimate_usd": round(BASELINE_GEMINI_USD + session_cost, 6),
        "tracked_sidecars": tracked_sidecars, "checks": results,
    }
    report["passed"] = not missing and not changed and not tracked_sidecars and all(row["passed"] for row in results.values())
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Backfill {}: {}/{} source paths, {} unique keys, {} mirror sidecars, Gemini ${:.6f} total".format(
        "PASS" if report["passed"] else "FAIL", report["indexed_source_paths"], len(sources),
        report["unique_source_keys"], report["mirror_sidecars"], report["total_gemini_estimate_usd"]), flush=True)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
