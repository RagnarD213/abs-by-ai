#!/usr/bin/env python3
"""Private video-trial evidence, usage accounting and blind media packaging.

Standard library, Python 3.9+. No model calls. ffmpeg/ffprobe only for `blind`.
"""
import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import tempfile

ARMS = ("all_astra", "all_sol", "hybrid")
ASTRA, SOL = "gpt-6-astra", "gpt-6.1-sol"
METRICS = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens",
           "output_tokens", "reasoning_output_tokens", "total_tokens")
CHECKS = ("picture", "audio", "source_fidelity", "independent_review")


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, data):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def slug(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", value):
        raise ValueError("Use a short alphanumeric identifier, hyphens or underscores")
    return value


def media_tool(name):
    found = shutil.which(name)
    if found:
        return found
    for base in (Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents):
        candidate = base / "Media" / "video_edit" / "bin" / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    raise FileNotFoundError("Missing media tool: " + name)


def private_root(path):
    path = Path(path).expanduser().resolve()
    if any((p / ".git").exists() for p in [path, *path.parents]):
        raise ValueError("Trial state and raw logs must stay outside a Git checkout")
    return path


def initialize(root, job, inputs):
    root = private_root(root)
    root.parent.mkdir(parents=True, exist_ok=True)
    root.mkdir(mode=0o700)  # exclusive: never overwrite a prior experiment
    try:
        (root / "frozen").mkdir()
        frozen = {}
        for name, source in inputs.items():
            slug(name)
            source = Path(source).expanduser().resolve(strict=True)
            target = root / "frozen" / (name + source.suffix)
            shutil.copyfile(source, target)
            frozen[name] = {"source": str(source), "copy": str(target.relative_to(root)),
                            "sha256": digest(target)}
        order = list(ARMS)
        secrets.SystemRandom().shuffle(order)
        state = {"schema": 1, "job": job, "created": now(), "status": "prepared",
                 "models": {"astra": ASTRA, "sol": SOL}, "effort": "high",
                 "execution_order": order, "frozen": frozen, "logs": [],
                 "gaps": [], "artifacts": {}, "blind_stages": {}}
        write(root / "trial.json", state)
        return state
    except Exception:
        shutil.rmtree(root)
        raise


def verify(root, state):
    errors = []
    for name, item in state["frozen"].items():
        copy = root / item["copy"]
        if not copy.is_file() or digest(copy) != item["sha256"]:
            errors.append("Frozen input changed/missing: " + name)
    return errors


def parse_log(path):
    """Native snapshots count once; CLI completed-turn usages add once per turn.

    Cached/reasoning counters are subsets, never additional total tokens.
    Unknown fields remain None. Counter regression/mixed formats fail coverage.
    """
    result = {"session_id": None, "models": [], "efforts": [], "tokens": None,
              "issues": [], "started": None, "last_event": None,
              "context_count": 0, "model_evidence_complete": True}
    native, cli = [], []
    model_set, effort_set = set(), set()
    try:
        lines = Path(path).open()
    except OSError as e:
        result["issues"].append("Unreadable log: " + str(e))
        return result
    with lines:
        for number, line in enumerate(lines, 1):
            try:
                event = json.loads(line)
            except ValueError:
                result["issues"].append("Invalid/incomplete JSONL line " + str(number))
                continue
            ty, p = event.get("type"), event.get("payload") or {}
            if event.get("timestamp"):
                result["started"] = result["started"] or event["timestamp"]
                result["last_event"] = event["timestamp"]
            if ty == "session_meta":
                result["session_id"] = p.get("id") or p.get("session_id")
            elif ty == "thread.started":
                result["session_id"] = event.get("thread_id")
            elif ty == "turn_context":
                result["context_count"] += 1
                if not p.get("model"):
                    result["model_evidence_complete"] = False
                if not p.get("model") or not p.get("effort"):
                    result["issues"].append("Model/effort missing on turn_context line " + str(number))
                if p.get("model"):
                    model_set.add(p["model"])
                if p.get("effort"):
                    effort_set.add(p["effort"])
            elif ty == "event_msg" and p.get("type") == "token_count":
                usage = (p.get("info") or {}).get("total_token_usage")
                if isinstance(usage, dict):
                    native.append(usage)
            elif ty == "turn.completed" and isinstance(event.get("usage"), dict):
                cli.append(event["usage"])
    result["models"], result["efforts"] = sorted(model_set), sorted(effort_set)
    result["model_evidence_complete"] &= result["context_count"] > 0
    if native and cli:
        result["issues"].append("Mixed native/CLI token streams; cannot safely combine")
    elif native:
        regressed = any(any(isinstance(a.get(k), int) and isinstance(b.get(k), int)
                            and b[k] < a[k] for k in METRICS)
                        for a, b in zip(native, native[1:]))
        if regressed:
            result["issues"].append("Cumulative counters regressed; totals unavailable")
        else:
            result["tokens"] = {k: native[-1].get(k) for k in METRICS}
    elif cli:
        result["tokens"] = {k: sum(x[k] for x in cli)
                            if all(isinstance(x.get(k), int) for x in cli) else None
                            for k in METRICS}
    else:
        result["issues"].append("No usable usage counters")
    tokens = result["tokens"]
    if tokens:
        for key, value in tokens.items():
            if value is not None and (not isinstance(value, int) or value < 0):
                result["issues"].append("Invalid counter: " + key)
                tokens[key] = None
        # total = input + output; don't add cached input or reasoning again.
        if tokens["total_tokens"] is None and all(tokens[k] is not None for k in ("input_tokens", "output_tokens")):
            tokens["total_tokens"] = tokens["input_tokens"] + tokens["output_tokens"]
        for subset, whole in (("cached_input_tokens", "input_tokens"),
                              ("reasoning_output_tokens", "output_tokens")):
            if tokens[subset] is not None and tokens[whole] is not None and tokens[subset] > tokens[whole]:
                result["issues"].append(subset + " exceeds " + whole)
        if all(tokens[k] is not None for k in ("input_tokens", "output_tokens", "total_tokens")):
            if tokens["total_tokens"] != tokens["input_tokens"] + tokens["output_tokens"]:
                result["issues"].append("Total does not match input + output")
    return result


def expected_model(state, arm, role, override=None):
    if arm == "shared":
        if not override:
            raise ValueError("Shared sessions require --model")
        return override
    if override:
        raise ValueError("Arm models are fixed by the experiment, not --model")
    if arm == "hybrid":
        return state["models"]["sol" if role in ("editor", "helper") else "astra"]
    return state["models"]["astra" if arm == "all_astra" else "sol"]


def register_log(state, arm, role, path, override=None):
    path = str(Path(path).expanduser().resolve(strict=True))
    info = parse_log(path)
    if not info["session_id"]:
        raise ValueError("Cannot register a log without a session ID; record a gap")
    expected = expected_model(state, arm, role, override)
    item = {"arm": arm, "role": role, "path": path, "session_id": info["session_id"],
            "expected_model": expected, "registered": now()}
    for old in state["logs"]:
        if old["session_id"] == item["session_id"] or old["path"] == path:
            if all(old[k] == item[k] for k in ("arm", "role", "path", "expected_model")):
                return  # idempotent resumption
            raise ValueError("Session already registered; cannot count it twice")
    state["logs"].append(item)


def usage_report(state):
    groups = {}
    for arm in (*ARMS, "shared"):
        sessions = []
        for item in state["logs"]:
            if item["arm"] != arm:
                continue
            info = parse_log(item["path"])
            if info["models"] != [item["expected_model"]]:
                info["issues"].append("Observed model missing or differs from " + item["expected_model"])
            if info["efforts"] != [state["effort"]]:
                info["issues"].append("Observed high effort not verified")
            if info["session_id"] != item["session_id"]:
                info["issues"].append("Registered log identity changed")
            sessions.append({**item, **info})
        totals, complete = {}, {}
        for k in METRICS:
            values = [(s.get("tokens") or {}).get(k) for s in sessions]
            known = [x for x in values if x is not None]
            totals[k] = sum(known) if known else None
            complete[k] = bool(values) and len(known) == len(values)
        by_model = {}
        for s in sessions:
            model = s["models"][0] if len(s["models"]) == 1 and s["model_evidence_complete"] else "unknown_or_mixed"
            bucket = by_model.setdefault(model, {k: None for k in METRICS})
            for k, value in (s.get("tokens") or {}).items():
                if value is not None:
                    bucket[k] = (bucket[k] or 0) + value
        groups[arm] = {"sessions": sessions, "known_tokens": totals,
                       "known_tokens_by_observed_model": by_model,
                       "counter_coverage": complete,
                       "model_effort_verified": bool(sessions) and all(not s["issues"] for s in sessions)}
    return {"job": state["job"], "groups": groups, "declared_gaps": state["gaps"],
            "scope": "Registered sessions only; reconcile runtime descendants before drawing conclusions",
            "subscription_credits": None, "dollar_cost": None}


def checks_template():
    return {"status": "incomplete", "stage_scope": "", "review_file_sha256": None,
            "checks": {k: {"status": "incomplete", "evidence": []} for k in CHECKS},
            "first_pass_status": None, "reviewer_findings": [], "repairs": [],
            "approval_rounds": None, "active_seconds": None, "render_seconds": None,
            "queue_seconds": None, "approval_wait_seconds": None,
            "external_spend_usd": None, "flow_credits": None, "missing_evidence": []}


def checked_file(path, checks_path):
    path, checks_path = Path(path).resolve(strict=True), Path(checks_path).resolve(strict=True)
    checks = read(checks_path)
    sha = digest(path)
    if checks.get("review_file_sha256") != sha:
        raise ValueError("Checks must identify the exact file SHA-256")
    evidence = []
    if not checks.get("stage_scope"):
        raise ValueError("Specify exactly what this preview/candidate check covers")
    for name in CHECKS:
        check = checks.get("checks", {}).get(name, {})
        for entry in check.get("evidence", []):
            p = Path(entry).expanduser()
            p = p if p.is_absolute() else checks_path.parent / p
            p = p.resolve(strict=True)
            evidence.append({"check": name, "path": str(p), "sha256": digest(p)})
        if check.get("status") == "pass" and not check.get("evidence"):
            raise ValueError("A pass needs an evidence file: " + name)
    if checks.get("status") == "pass" and not all(checks.get("checks", {}).get(k, {}).get("status") == "pass" for k in CHECKS):
        raise ValueError("Overall pass contradicts an incomplete/failed check")
    if path.suffix.lower() != ".mp4":
        raise ValueError("Record the checked 1080p MP4 review export")
    return {"file": str(path), "sha256": sha, "checks": checks,
            "evidence": evidence, "recorded": now()}


def record_artifact(root, state, arm, stage, path, checks_path):
    slug(stage)
    if stage in state["blind_stages"] or arm in state["artifacts"].get(stage, {}):
        raise ValueError("Stage/arm already recorded; preserve it and use a new stage")
    item = checked_file(path, checks_path)
    state["artifacts"].setdefault(stage, {})[arm] = item


def probe(path):
    p = subprocess.run([media_tool("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                       check=True, capture_output=True, text=True)
    return json.loads(p.stdout)


def blind_package(root, state, stage):
    slug(stage)
    if stage in state["blind_stages"]:
        raise ValueError("Stage already blinded; do not overwrite a reviewed packet")
    artifacts = state["artifacts"].get(stage, {})
    if set(artifacts) != set(ARMS):
        raise ValueError("Need one checked artifact from each of the three arms")
    for item in artifacts.values():
        if item["checks"].get("status") != "pass" or digest(item["file"]) != item["sha256"]:
            raise ValueError("Candidate failed/incomplete or changed after checks")
        for e in item["evidence"]:
            if digest(e["path"]) != e["sha256"]:
                raise ValueError("Check evidence changed after registration")
    dest = root / "review" / stage
    dest.parent.mkdir(exist_ok=True)
    if dest.exists():
        raise ValueError("Review directory already exists")
    temporary = Path(tempfile.mkdtemp(prefix=".blind-", dir=root))
    order = list(ARMS)
    secrets.SystemRandom().shuffle(order)
    mapping, public = {}, []
    try:
        for number, arm in enumerate(order, 1):
            label = "X" + str(number)
            source, target = artifacts[arm]["file"], temporary / (label + ".mp4")
            subprocess.run([media_tool("ffmpeg"), "-nostdin", "-v", "error", "-i", source,
                            "-map", "0:v:0", "-map", "0:a?", "-map_metadata", "-1",
                            "-map_chapters", "-1", "-c", "copy", "-metadata", "encoder=",
                            "-movflags", "+faststart", str(target)], check=True, capture_output=True)
            before, after = probe(source), probe(target)
            v0 = next(s for s in before["streams"] if s["codec_type"] == "video")
            v1 = next(s for s in after["streams"] if s["codec_type"] == "video")
            if any(v0.get(k) != v1.get(k) for k in ("width", "height", "codec_name", "r_frame_rate")):
                raise ValueError("Remux changed the video presentation")
            if max(v1["width"], v1["height"]) < 1920 or min(v1["width"], v1["height"]) < 1080:
                raise ValueError("Blind review requires the default 1080p export")
            tags = json.dumps([after.get("format", {}).get("tags", {}),
                               *[s.get("tags", {}) for s in after["streams"]]]).lower()
            if any(x in tags for x in ("astra", "gpt-6", "codex", "orchestrator", "all_sol", "hybrid")):
                raise ValueError("Identifying metadata remains in neutral media")
            sha = digest(target)
            mapping[label] = {"arm": arm, "source_sha256": artifacts[arm]["sha256"], "review_sha256": sha}
            public.append({"label": label, "file": target.name, "sha256": sha})
        manifest = {"title": state["job"] + " blind review", "stage": stage,
                    "ready_for_owner": False, "versions": public}
        write(temporary / "manifest.json", manifest)
        write(temporary / "ballot-template.json", {"judge": "Dan", "stage": stage,
              "ranking": [], "notes": {x["label"]: "" for x in public},
              "review_sha256": {x["label"]: x["sha256"] for x in public}})
        os.replace(temporary, dest)
        state["blind_stages"][stage] = {"mapping": mapping, "created": now(), "revealed": False,
                                         "neutral_checks": {}}
        return manifest
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def neutral_check(root, state, stage, label, checks_path):
    info = state["blind_stages"][stage]
    path = root / "review" / stage / (label + ".mp4")
    if label not in info["mapping"]:
        raise ValueError("Unknown blind label")
    item = checked_file(path, checks_path)
    if item["sha256"] != info["mapping"][label]["review_sha256"]:
        raise ValueError("Neutral file changed after blinding")
    if item["checks"]["status"] != "pass":
        raise ValueError("Neutral review file needs its own applicable exact-file checks")
    info["neutral_checks"][label] = item
    ready = set(info["neutral_checks"]) == set(info["mapping"])
    if ready:
        for old_label, old in info["neutral_checks"].items():
            if digest(root / "review" / stage / (old_label + ".mp4")) != old["sha256"]:
                raise ValueError("Previously checked neutral file changed")
            for e in old["evidence"]:
                if digest(e["path"]) != e["sha256"]:
                    raise ValueError("Neutral check evidence changed")
    manifest_path = root / "review" / stage / "manifest.json"
    manifest = read(manifest_path)
    manifest["ready_for_owner"] = ready
    write(manifest_path, manifest)
    return {"ready_for_owner": ready, "neutral_checks": len(info["neutral_checks"])}


def reveal(root, state, stage, ballot_path, early_reason=None):
    if not stage.endswith("candidate") and not early_reason:
        raise ValueError("Keep identities sealed until final ratings or explicit early-reveal direction")
    info = state["blind_stages"][stage]
    ballot = read(ballot_path)
    if ballot.get("judge") != "Dan" or ballot.get("stage") != stage:
        raise ValueError("Need Dan's ballot for this exact stage")
    ranking = ballot.get("ranking", [])
    flat = [label for group in ranking for label in (group if isinstance(group, list) else [group])]
    judged = len(flat) == 3 and set(flat) == set(info["mapping"])
    if not judged and not (early_reason and ballot.get("ranking") == []):
        raise ValueError("Record Dan's ranking of all three labels")
    if judged and not read(root / "review" / stage / "manifest.json").get("ready_for_owner"):
        raise ValueError("Exact neutral-file checks must pass before judged delivery")
    expected = {k: v["review_sha256"] for k, v in info["mapping"].items()}
    if ballot.get("review_sha256") != expected:
        raise ValueError("Ballot does not identify the exact reviewed files")
    for label, sha in expected.items():
        if digest(root / "review" / stage / (label + ".mp4")) != sha:
            raise ValueError("Reviewed file changed")
    target = root / (stage + "-Dan-ballot.json")
    if target.exists() and read(target) != ballot:
        raise ValueError("Preserve the original ballot; don't overwrite it")
    write(target, ballot)
    info.update(revealed=True, ballot_sha256=digest(target), early_reveal_reason=early_reason)
    return {"ballot": ballot, "judgment_status": "judged" if judged else "revealed_before_judging",
            "identities": info["mapping"], "usage": usage_report(state),
            "quality": {arm: item["checks"] for arm, item in state["artifacts"][stage].items()}}


@contextlib.contextmanager
def locked(root):
    with (root / ".lock").open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init")
    p.add_argument("root"); p.add_argument("--job", required=True)
    p.add_argument("--brief", required=True); p.add_argument("--source-map", required=True)
    p.add_argument("--input", action="append", default=[], metavar="NAME=PATH")
    sub.add_parser("checks-template")
    for cmd in ("verify", "usage", "gap", "log", "artifact", "blind", "neutral-check", "reveal"):
        p = sub.add_parser(cmd); p.add_argument("root")
        if cmd == "gap": p.add_argument("--text", required=True)
        if cmd in ("log", "artifact"):
            p.add_argument("--arm", choices=(*ARMS, "shared") if cmd == "log" else ARMS, required=True)
            p.add_argument("--file", required=True)
        if cmd == "log":
            p.add_argument("--role", choices=("editor", "coordinator", "reviewer", "helper"), required=True)
            p.add_argument("--model")
        if cmd in ("artifact", "blind", "neutral-check", "reveal"): p.add_argument("--stage", required=True)
        if cmd in ("artifact", "neutral-check"): p.add_argument("--checks", required=True)
        if cmd == "neutral-check": p.add_argument("--label", choices=("X1", "X2", "X3"), required=True)
        if cmd == "reveal":
            p.add_argument("--ballot", required=True); p.add_argument("--early-reveal-reason")
    args = parser.parse_args()
    if args.command == "checks-template":
        result = checks_template()
    elif args.command == "init":
        inputs = {"brief": args.brief, "source-map": args.source_map}
        for extra in args.input:
            name, path = extra.split("=", 1)
            if name in inputs: raise ValueError("Duplicate frozen input name")
            inputs[name] = path
        result = initialize(args.root, args.job, inputs)
    else:
        root = private_root(args.root)
        with locked(root):
            state = read(root / "trial.json")
            errors = verify(root, state)
            if errors: raise ValueError("; ".join(errors))
            if args.command == "verify": result = {"status": "frozen_inputs_intact"}
            elif args.command == "usage": result = usage_report(state)
            elif args.command == "gap":
                state["gaps"].append({"at": now(), "text": args.text}); result = {"status": "gap_recorded"}
            elif args.command == "log":
                register_log(state, args.arm, args.role, args.file, args.model)
                result = {"status": "log_registered", "sessions": len(state["logs"])}
            elif args.command == "artifact":
                record_artifact(root, state, args.arm, args.stage, args.file, args.checks)
                result = {"status": "artifact_recorded"}
            elif args.command == "blind": result = blind_package(root, state, args.stage)
            elif args.command == "neutral-check": result = neutral_check(root, state, args.stage, args.label, args.checks)
            elif args.command == "reveal": result = reveal(root, state, args.stage, args.ballot, args.early_reveal_reason)
            if args.command not in ("verify", "usage"): write(root / "trial.json", state)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc))
