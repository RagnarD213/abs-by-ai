#!/usr/bin/env python3
"""Run ONE queue job inside its slot: one editor -> one cross-review -> hand to Dan or park.

Started detached by dispatcher.py, which has already claimed the job with this process's pid. The claim
stays live for the whole run, so the review (a watch pass counts as a build) happens inside the same slot.
The runner never edits video and never decides quality: it launches sessions, keeps the heartbeat, reads
the files they leave behind, and records the result.

  runner.py <JOB-ID> <executor> <run-id>

Files a session leaves in the work directory (the contract in preamble.md):
  DELIVERY.json          the edit finished: {"files": [...], "review_copy": "...", "gate": "PASS|FAIL|DRAFT", "generation_spend_usd": 0}
  BLOCKED.md             a real blocker; first line is the one-sentence reason
  QUEUE-REVIEW-<n>.md    the reviewer's report; first line `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`
"""
import datetime, hashlib, json, os, re, subprocess, sys, threading, time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eq_common as eq                                          # noqa: E402
eq.unshadow()
q = eq.sibling("queue")
QUEUE_PY = os.path.join(eq.HERE, "queue.py")
FFMPEG = os.path.join(eq.ROOT, "Media", "video_edit", "bin", "ffmpeg")
FFPROBE = os.path.join(eq.ROOT, "Media", "video_edit", "bin", "ffprobe")


def qcmd(*args):
    return subprocess.run([sys.executable, QUEUE_PY, *args], capture_output=True, text=True)


def heartbeat_loop(job_id, stop, minutes):
    while not stop.wait(minutes * 60):
        qcmd("heartbeat", job_id)


def run_session(executor, cfg, workdir, prompt, log_path, role, timeout_h):
    """One headless session. Returns (returncode, tail_of_log). Never raises for a session failure."""
    with open(os.path.join(workdir, f"queue-prompt-{role}.txt"), "w") as f:
        f.write(prompt)
    with open(log_path, "a") as log:
        log.write(f"\n===== {datetime.datetime.now():%Y-%m-%d %H:%M:%S} {role} session: {executor} =====\n")
        try:
            cmd = eq.build_command(executor, cfg, workdir, role)
            log.write("argv: " + json.dumps(cmd) + "\n"); log.flush()
            start = log.tell()
            r = subprocess.run(["/usr/bin/caffeinate", "-i"] + cmd, input=prompt, text=True, stdout=log,
                               stderr=subprocess.STDOUT, cwd=eq.ROOT, timeout=timeout_h * 3600)
            code = r.returncode
        except subprocess.TimeoutExpired:
            log.write(f"\n[runner] killed after {timeout_h} h (claims.max_job_hours)\n"); code, start = -9, 0
        except Exception as e:
            log.write(f"\n[runner] could not start {executor}: {e}\n"); code, start = -1, 0
    with open(log_path, errors="replace") as f:
        f.seek(start)
        return code, f.read()[-6000:]


def classify_failure(code, tail, cfg):
    """Only a session that FAILED is searched for limit/sign-in wording: a good edit's log can say 'rate limit' too."""
    low = tail.lower()
    if any(p.lower() in low for p in cfg["auth_failure_patterns"]):
        return "auth_failed"
    if any(p.lower() in low for p in cfg["usage_limit_patterns"]):
        return "usage_limited"
    return "timeout" if code == -9 else "session_failed"


def read_verdict(workdir, n):
    """A review that did not leave a verdict did not run, and a check that did not run is a failure."""
    path = os.path.join(workdir, f"QUEUE-REVIEW-{n}.md")
    if not os.path.exists(path):
        return "NO VERDICT", path
    with open(path, errors="replace") as fh:
        first = fh.read(400).upper()
    if re.search(r"VERDICT:\s*\**\s*DOES NOT SHIP", first):
        return "DOES NOT SHIP", path
    if re.search(r"VERDICT:\s*\**\s*SHIP", first):
        return "SHIP", path
    return "NO VERDICT", path


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def short_list(value, label, limit=12):
    """Normalize a deliberately short authority list; prose remains one item, not hidden sub-scope."""
    if value is None:
        rows = []
    elif isinstance(value, str):
        rows = [value.strip()] if value.strip() else []
    elif isinstance(value, list):
        rows = [str(v).strip() for v in value if str(v).strip()]
    else:
        raise ValueError(f"{label} must be text or a list of text")
    if len(rows) > limit:
        raise ValueError(f"{label} has {len(rows)} items; consolidate it to {limit} or fewer")
    return rows


def write_work_packet(job, workdir, run_id, prior_delivery=None):
    """Create the one authoritative scope record consumed by the editor and reviewer."""
    revision = job.get("queue_revision") or {}
    old_packet = {}
    packet_path = Path(workdir) / "WORK_PACKET.json"
    if packet_path.exists():
        try:
            old_packet = json.loads(packet_path.read_text())
        except Exception:
            old_packet = {}
    if revision:
        requested = short_list(revision.get("requested_changes") or revision.get("words"), "requested_changes")
    else:
        requested = short_list(job.get("requested_changes"), "requested_changes")
        if not requested:
            requested = [f"Complete only the deliverable described in Handoffs/video-editing/{job.get('file', '')}."]
    approved = short_list(
        revision.get("approved_elements")
        or job.get("approved_elements")
        or (prior_delivery or {}).get("approved_elements")
        or old_packet.get("approved_elements"),
        "approved_elements",
    )
    packet = {
        "schema": 1,
        "job": job["id"],
        "run_id": run_id,
        "revision_number": int(revision.get("round", 0)),
        "requested_changes": requested,
        "approved_elements": approved,
        "scope_rule": "Change requested items only; preserve approved elements and all other fingerprint-matching work.",
        "review_checkpoint": "one independent review after the editor has produced one complete candidate and finished self-QA",
        "prior_delivery": (prior_delivery or {}).get("_archived_path"),
        "reuse_candidates": {
            "files": (prior_delivery or {}).get("files", []),
            "review_copy": (prior_delivery or {}).get("review_copy"),
            "audio": (prior_delivery or {}).get("audio"),
            "transcript": (prior_delivery or {}).get("transcript"),
            "assets": (prior_delivery or {}).get("assets", []),
        },
    }
    packet_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
    return packet


def validate_pre_render(workdir):
    """Require honest source/preview evidence before the queue spends a reviewer session."""
    path = Path(workdir) / "PRE_RENDER_CHECK.json"
    if not path.exists():
        return ["PRE_RENDER_CHECK.json is missing"]
    try:
        report = json.loads(path.read_text())
    except Exception as e:
        return [f"PRE_RENDER_CHECK.json is unreadable: {e}"]
    status = report.get("status")
    if status == "not_applicable":
        return [] if report.get("reason") else ["PRE_RENDER_CHECK not_applicable needs a reason"]
    if status != "verified":
        return ["PRE_RENDER_CHECK status must be verified or not_applicable"]
    rows = report.get("risky_selections") or []
    if not rows:
        return ["PRE_RENDER_CHECK verified without risky_selections"]
    errors = []
    for i, row in enumerate(rows, 1):
        for key in ("description", "source", "source_sha256", "preview", "preview_sha256", "verdict"):
            if not row.get(key):
                errors.append(f"risky selection {i} lacks {key}")
        for key in ("source", "preview"):
            p = row.get(key)
            expected = row.get(key + "_sha256")
            if p and not os.path.isfile(p):
                errors.append(f"risky selection {i} missing {key}: {p}")
            elif p and expected and sha256(p) != expected:
                errors.append(f"risky selection {i} changed after review: {key}")
        seconds = row.get("preview_seconds")
        if not isinstance(seconds, (int, float)) or not 0.5 <= seconds <= 15:
            errors.append(f"risky selection {i} preview_seconds must be 0.5–15")
        preview = row.get("preview")
        if preview and os.path.isfile(preview) and isinstance(seconds, (int, float)):
            try:
                actual = float(subprocess.check_output([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                                                        "-of", "default=nw=1:nk=1", preview], text=True).strip())
                if not 0.5 <= actual <= 15.25 or abs(actual - seconds) > 0.35:
                    errors.append(f"risky selection {i} preview duration {actual:.2f}s disagrees with {seconds}s")
                hashes = subprocess.check_output([FFMPEG, "-v", "error", "-i", preview, "-vf", "fps=2",
                                                  "-f", "framemd5", "-"], text=True)
                frame_hashes = {line.rsplit(",", 1)[-1].strip() for line in hashes.splitlines()
                                if line and not line.startswith("#") and "," in line}
                if len(frame_hashes) < 2:
                    errors.append(f"risky selection {i} preview has no verified frame-to-frame motion")
            except Exception as e:
                errors.append(f"risky selection {i} preview could not be probed: {e!s:.120}")
    return errors


def validate_delivery(info, workdir, packet):
    """Require a real gated candidate plus complete efficiency evidence before review."""
    errors = validate_pre_render(workdir)
    files = info.get("files")
    if not isinstance(files, list) or not files:
        errors.append("DELIVERY files must list at least one delivered video")
    else:
        for delivered in files:
            if not isinstance(delivered, str) or not os.path.isfile(delivered):
                errors.append(f"DELIVERY file is missing: {delivered}")
    review_copy = info.get("review_copy")
    if not isinstance(review_copy, str) or not os.path.isfile(review_copy):
        errors.append(f"DELIVERY review_copy is missing: {review_copy}")
    if info.get("gate") != "PASS":
        errors.append(f"DELIVERY gate must be PASS before independent review (got {info.get('gate')!r})")
    if info.get("revision_count") != packet["revision_number"]:
        errors.append(f"revision_count must equal WORK_PACKET revision {packet['revision_number']}")
    try:
        if "approved_elements" not in info:
            errors.append("DELIVERY approved_elements list is missing")
        short_list(info.get("approved_elements"), "DELIVERY approved_elements")
    except ValueError as e:
        errors.append(str(e))
    reuse = info.get("reuse")
    allowed = {"reused", "rebuilt", "mixed", "not_applicable", "unavailable"}
    if not isinstance(reuse, dict):
        errors.append("DELIVERY reuse report is missing")
    else:
        for name in ("scenes", "audio", "transcript", "assets"):
            row = reuse.get(name)
            if not isinstance(row, dict) or row.get("status") not in allowed:
                errors.append(f"DELIVERY reuse.{name}.status is missing or invalid")
            elif row["status"] in ("not_applicable", "unavailable") and not row.get("reason"):
                errors.append(f"DELIVERY reuse.{name} needs a reason for {row['status']}")
            elif row["status"] in ("reused", "rebuilt", "mixed") and not row.get("evidence"):
                errors.append(f"DELIVERY reuse.{name} needs fingerprint/path evidence for {row['status']}")
    costs = info.get("paid_provider_costs")
    if not isinstance(costs, list) or not costs:
        errors.append("DELIVERY paid_provider_costs must be a non-empty list (use an unavailable row when unknown)")
    else:
        for i, row in enumerate(costs, 1):
            if not isinstance(row, dict) or not row.get("provider") or "usd" not in row:
                errors.append(f"paid_provider_costs row {i} lacks provider/usd")
            elif row.get("usd") is None and not row.get("reason"):
                errors.append(f"paid_provider_costs row {i} has unavailable cost without a reason")
            elif isinstance(row.get("usd"), (int, float)) and row["usd"] < 0:
                errors.append(f"paid_provider_costs row {i} has a negative cost")
    return errors


def prompts(job, executor, cfg, workdir):
    pre = open(eq.PREAMBLE).read().replace("{WORKDIR}", workdir).replace("{JOB}", job["id"])
    edit = pre + "\n\n---\n\n" + job[executor]
    if job.get("queue_revision"):
        rv = job["queue_revision"]
        edit = (pre + f"\n\n---\n\nThis is REVISION round {rv.get('round', 1)} of {job['id']} after Dan watched the delivered cut. "
                "His exact words are below. First record them as a regression-corpus entry (AGENTS.md: a rejection becomes a "
                "corpus entry in the same session, before the fix). WORK_PACKET.json is the authoritative short scope: change only "
                "its requested_changes, preserve its approved_elements and reuse every unchanged fingerprint-matching scene, audio, "
                "transcript and asset. Re-run every gate on the new delivered file and rewrite DELIVERY.json.\n\n"
                f"Dan's words: \"{rv.get('words', '')}\"\n\nThe job, for reference:\n{job[executor]}")
    return pre, edit


def main():
    job_id, executor, run_id = sys.argv[1:4]
    cfg = eq.load_config()
    job = q.find(q.load(), job_id)
    workdir = eq.work_dir(cfg, job_id)
    os.makedirs(workdir, exist_ok=True)
    log_path = os.path.join(workdir, "queue-run.log")
    t0 = time.time()
    stop = threading.Event()
    threading.Thread(target=heartbeat_loop, args=(job_id, stop, cfg["claims"]["heartbeat_minutes"]), daemon=True).start()

    outcome, note, verdicts, state = "session_failed", "", [], None
    usage = []
    packet = None
    try:
        if cfg.get("review", {}).get("reviews_per_candidate") != 1:
            raise ValueError("review.reviews_per_candidate must remain 1; repeated supervisory loops are disabled")
        prior_delivery = None
        for stale in ("DELIVERY.json", "BLOCKED.md"):          # a revision run must earn these again
            p = os.path.join(workdir, stale)
            if os.path.exists(p):
                archived = p + f".before-{run_id}"
                if stale == "DELIVERY.json":
                    try:
                        prior_delivery = json.load(open(p))
                        prior_delivery["_archived_path"] = archived
                    except Exception:
                        prior_delivery = {"_archived_path": archived}
                os.replace(p, archived)
        for name in os.listdir(workdir):
            if re.fullmatch(r"QUEUE-REVIEW-\d+\.md", name):
                os.replace(os.path.join(workdir, name), os.path.join(workdir, name + f".before-{run_id}"))
        packet = write_work_packet(job, workdir, run_id, prior_delivery)
        pre, edit_prompt = prompts(job, executor, cfg, workdir)
        code, tail = run_session(executor, cfg, workdir, edit_prompt, log_path, "edit", cfg["claims"]["max_job_hours"])
        usage.append(eq.model_usage_record(executor, cfg, "editor", tail))
        eq.scoreboard_update(run_id, model_usage=usage)
        reviewer = cfg["review"]["reviewer_for"][executor]
        if not eq.auth_ok(reviewer, cfg)[0]:
            # Independent review still happens: a fresh session of the editor's own tool has not seen the build either.
            reviewer = executor
            eq.scoreboard_update(run_id, reviewer=f"{executor} (fresh session; cross-reviewer unavailable)")
        delivered = os.path.exists(os.path.join(workdir, "DELIVERY.json"))
        if os.path.exists(os.path.join(workdir, "BLOCKED.md")):
            reason = open(os.path.join(workdir, "BLOCKED.md"), errors="replace").readline().strip("# \n")[:200]
            outcome, state, note = "parked", "needs", f"BLOCKED (queue run): {reason}"
        elif not delivered:
            outcome = classify_failure(code, tail, cfg)
            state = "ready" if outcome in ("usage_limited", "auth_failed") and not eq.non_queue_files(workdir) else "stalled"
            note = f"{outcome}: the {executor} session ended without DELIVERY.json or BLOCKED.md (exit {code}); see queue-run.log"
        else:
            info = json.load(open(os.path.join(workdir, "DELIVERY.json")))
            contract_errors = validate_delivery(info, workdir, packet)
            if contract_errors:
                outcome, state = "parked", "needs"
                note = "Efficiency evidence incomplete before review: " + "; ".join(contract_errors[:5])
            else:
                # Exactly one independent review, after the editor's complete candidate and self-QA.
                brief = (open(eq.REVIEWER_BRIEF).read().replace("{WORKDIR}", workdir).replace("{JOB}", job_id)
                         .replace("{N}", "1").replace("{JOBDOC}", "Handoffs/video-editing/" + job.get("file", "")))
                _review_code, review_tail = run_session(reviewer, cfg, workdir, brief, log_path, "review-1", 3)
                usage.append(eq.model_usage_record(reviewer, cfg, "independent reviewer", review_tail))
                verdict, vpath = read_verdict(workdir, 1)
                verdicts.append(verdict)
                eq.scoreboard_update(run_id, reviewer_verdicts=verdicts, model_usage=usage)
                if verdict == "SHIP":
                    outcome, state, note = "delivered", "delivered", f"Queue run {run_id}: independent reviewer ({reviewer}) says SHIP. Review copy in DELIVERY.json."
                else:
                    outcome, state = "parked", "needs"
                    note = f"Reviewer: {verdict}. One consolidated review is attached at {vpath}; no automatic supervision/fix loop ran."
    except Exception as e:
        outcome, state, note = "runner_error", "stalled", f"runner error: {e!s:.200}"
    finally:
        stop.set()
        info = {}
        try:
            info = json.load(open(os.path.join(workdir, "DELIVERY.json")))
        except Exception:
            pass
        if state:
            if state == "stalled":
                qcmd("stall", job_id, "--note", note)
            else:
                qcmd("set", job_id, state, "--by", f"edit queue ({executor})", "--note", note)
        qcmd("release", job_id)
        with q.locked():                       # a finished revision is no longer pending
            data = q.load(); j = q.find(data, job_id)
            if outcome == "delivered":
                j.pop("queue_revision", None)
            q.save(data)
        costs = info.get("paid_provider_costs")
        if not isinstance(costs, list):
            costs = [{"provider": "all", "usd": None,
                      "reason": "Per-video paid-provider costs were unavailable because DELIVERY.json did not report them."}]
        eq.scoreboard_update(run_id, ended=q.now_iso(), wall_hours=round((time.time() - t0) / 3600, 2), outcome=outcome,
                             reviewer_verdicts=verdicts, revision_number=(packet or {}).get("revision_number", 0),
                             revision_rounds=(packet or {}).get("revision_number", 0), model_usage=usage,
                             first_pass_gate=info.get("gate"), paid_provider_costs=costs,
                             generation_spend_usd=info.get("generation_spend_usd"), note=note)
        try:
            eq.sibling("review_page").build()
        except Exception:
            pass


if __name__ == "__main__":
    main()
