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
import datetime, hashlib, json, os, re, signal, subprocess, sys, threading, time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eq_common as eq                                          # noqa: E402
eq.unshadow()
q = eq.sibling("queue")
asset = eq.sibling("asset_approval")
QUEUE_PY = os.path.join(eq.HERE, "queue.py")
FFMPEG = os.path.join(eq.ROOT, "Media", "video_edit", "bin", "ffmpeg")
FFPROBE = os.path.join(eq.ROOT, "Media", "video_edit", "bin", "ffprobe")
BUDGET_EXCEEDED_CODE = -10
OUTER_TIMEOUT_CODE = -9


def qcmd(*args):
    return subprocess.run([sys.executable, QUEUE_PY, *args], capture_output=True, text=True)


def heartbeat_loop(job_id, stop, minutes):
    while not stop.wait(minutes * 60):
        qcmd("heartbeat", job_id)


def run_session(executor, cfg, workdir, prompt, log_path, role, timeout_h, budget_enforced=True):
    """One headless session. Returns (returncode, tail_of_log, wall_hours). Never raises for session failure."""
    with open(os.path.join(workdir, f"queue-prompt-{role}.txt"), "w") as f:
        f.write(prompt)
    began = time.time()
    with open(log_path, "a") as log:
        log.write(f"\n===== {datetime.datetime.now():%Y-%m-%d %H:%M:%S} {role} session: {executor} =====\n")
        start = log.tell()
        try:
            cmd = eq.build_command(executor, cfg, workdir, role)
            log.write("argv: " + json.dumps(cmd) + "\n"); log.flush()
            start = log.tell()
            proc = subprocess.Popen(["/usr/bin/caffeinate", "-i"] + cmd, stdin=subprocess.PIPE, text=True,
                                    stdout=log, stderr=subprocess.STDOUT, cwd=eq.ROOT, start_new_session=True)
            try:
                proc.communicate(prompt, timeout=max(0.01, timeout_h * 3600))
                code = proc.returncode
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                    proc.wait(timeout=5)
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    proc.wait()
                label = "work budget" if budget_enforced else "absolute outer ceiling"
                log.write(f"\n[runner] stopped process group after {timeout_h:g} h ({label})\n")
                code = BUDGET_EXCEEDED_CODE if budget_enforced else OUTER_TIMEOUT_CODE
        except subprocess.TimeoutExpired:
            log.write(f"\n[runner] stopped after {timeout_h:g} h\n")
            code = BUDGET_EXCEEDED_CODE if budget_enforced else OUTER_TIMEOUT_CODE
        except Exception as e:
            log.write(f"\n[runner] could not start {executor}: {e}\n"); code = -1
    with open(log_path, errors="replace") as f:
        f.seek(start)
        return code, f.read()[-6000:], (time.time() - began) / 3600


def classify_failure(code, tail, cfg):
    """Only a session that FAILED is searched for limit/sign-in wording: a good edit's log can say 'rate limit' too."""
    if code == BUDGET_EXCEEDED_CODE:
        return "budget_exceeded"
    if code == OUTER_TIMEOUT_CODE:
        return "timeout"
    low = tail.lower()
    if any(p.lower() in low for p in cfg["auth_failure_patterns"]):
        return "auth_failed"
    if any(p.lower() in low for p in cfg["usage_limit_patterns"]):
        return "usage_limited"
    return "session_failed"


def budget_renders(workdir):
    try:
        return int(eq.load_budget(workdir).get("renders_used") or 0)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def budget_note(hours, workdir, leg="edit"):
    detail = "review clock expired" if leg == "review" else "edit clock expired"
    return f"budget exceeded after {hours:.2f} h, {budget_renders(workdir)} renders; {detail}; see queue-run.log"


def update_budget_file(workdir, edit_hours, review_hours, exceeded):
    """Add measured usage to the launch document without changing its fixed deadlines or caps."""
    path = os.path.join(workdir, eq.BUDGET_NAME)
    try:
        doc = eq.load_budget(workdir)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return {}
    doc.update(hours_used=round(edit_hours, 6), review_hours_used=round(review_hours, 6),
               exceeded=bool(exceeded))
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)
    return doc


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


def _json(path, label):
    try:
        with open(path) as fh:
            return json.load(fh)
    except Exception as exc:
        raise ValueError(f"{label} is unreadable: {exc}") from exc


def validate_draft_delivery(workdir, work_packet, approval_packet):
    errors = []
    path = Path(workdir) / "DRAFT-DELIVERY.json"
    if not path.exists():
        return ["DRAFT-DELIVERY.json is missing for a packet with approval items"]
    try:
        draft = _json(path, "DRAFT-DELIVERY.json")
    except ValueError as exc:
        return [str(exc)]
    if draft.get("schema") != 1:
        errors.append("DRAFT-DELIVERY schema must be 1")
    if draft.get("gate") != "DRAFT":
        errors.append("placeholder stage must record gate DRAFT, never PASS")
    if draft.get("revision_count") != work_packet["revision_number"]:
        errors.append("draft revision_count must equal WORK_PACKET revision")
    if os.path.realpath(str(draft.get("packet") or "")) != os.path.realpath(
            os.path.join(workdir, asset.PACKET_NAME)):
        errors.append("draft marker does not name this job's placeholders.json")
    if draft.get("packet_material_fingerprint") != asset.packet_material_fingerprint(approval_packet):
        errors.append("draft marker is stale: proposed material changed after the draft")
    if draft.get("draft_sha256") != approval_packet["draft"]["sha256"]:
        errors.append("draft marker hash does not match placeholders.json")
    visible = approval_packet.get("created_at")
    ended = draft.get("stage_one_ended")
    try:
        visible_dt = datetime.datetime.fromisoformat(visible)
        ended_dt = datetime.datetime.fromisoformat(ended)
        if visible_dt.tzinfo is None or ended_dt.tzinfo is None:
            errors.append("package/stage-one timestamps must include their UTC offset")
        elif visible_dt >= ended_dt:
            errors.append("asset package must become visible before stage-one completion")
    except (TypeError, ValueError):
        errors.append("package/stage-one timestamps must be ISO-8601")
    if not isinstance(draft.get("full_render_count"), int) or draft["full_render_count"] < 0:
        errors.append("draft full_render_count must be a non-negative integer")
    costs = draft.get("paid_provider_costs")
    if not isinstance(costs, list) or not costs:
        errors.append("draft paid_provider_costs must report itemized costs or an unavailable row")
    if any(x.get("type") in ("stock", "existing_broll") for x in approval_packet.get("items") or []):
        try:
            preview_report = _json(os.path.join(workdir, "PRE_RENDER_CHECK.json"), "PRE_RENDER_CHECK.json")
        except ValueError as exc:
            errors.append(str(exc)); preview_report = {}
        if preview_report.get("status") != "verified":
            errors.append("stock/existing-B-roll approval items require PRE_RENDER_CHECK status verified")
        proved = {(x.get("source_sha256"), x.get("preview_sha256"))
                  for x in preview_report.get("risky_selections") or [] if isinstance(x, dict)}
        for item in approval_packet.get("items") or []:
            if item.get("type") in ("stock", "existing_broll"):
                pair = (item["source"]["sha256"], item["preview"]["sha256"])
                if pair not in proved:
                    errors.append(f"{item['id']} exact source/preview hashes are absent from PRE_RENDER_CHECK")
        errors.extend(validate_pre_render(workdir))
    return errors


def _placeholder_stamp_errors(files):
    """A Phase-2 delivery must carry the current shared-gate PASS for the new row."""
    errors = []
    skills = os.path.join(eq.ROOT, ".claude", "skills")
    if skills not in sys.path:
        sys.path.insert(0, skills)
    try:
        from _shared.deliver import gate as delivery_gate
    except Exception as exc:
        return [f"shared delivery gate could not be loaded: {exc}"]
    for video in files:
        try:
            stamp = delivery_gate.require_stamp(video, quiet=True)
        except SystemExit as exc:
            errors.append(f"{os.path.basename(video)} lacks a current delivery PASS: {exc}")
            continue
        row = (stamp.get("rows") or {}).get("compliance:placeholder") or {}
        if row.get("ok") is not True:
            errors.append(f"{os.path.basename(video)} has no passing compliance:placeholder row")
    return errors


def validate_delivery(info, workdir, packet, cfg=None, launch_state="ready"):
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
    finishing_spend = info.get("generation_spend_usd")
    if not isinstance(finishing_spend, (int, float)) or isinstance(finishing_spend, bool) or finishing_spend < 0:
        errors.append("DELIVERY generation_spend_usd must be a non-negative number for this session")
    packet_path = os.path.join(workdir, asset.PACKET_NAME)
    if os.path.exists(packet_path):
        try:
            approval_packet = asset.read_packet(packet_path, workdir,
                                                eq.asset_allowed_roots(cfg or eq.load_config()))
        except asset.PacketError as exc:
            errors.append(f"placeholders.json refused: {exc}")
            approval_packet = None
        if approval_packet and approval_packet.get("items"):
            if launch_state != "frames_approved":
                errors.append("a placeholder-flow final may only be produced by the frames_approved finishing launch")
            if os.path.realpath(str(info.get("placeholders") or "")) != os.path.realpath(packet_path):
                errors.append("DELIVERY placeholders must name this work directory's placeholders.json")
            final_files = [p for p in (files or []) if isinstance(p, str) and os.path.isfile(p)]
            watch_log = info.get("watch_log")
            if not isinstance(watch_log, str) or not os.path.isfile(watch_log):
                errors.append("DELIVERY watch_log must name the final render's shared watch-pass log")
            try:
                asset.validate_packet(approval_packet, workdir,
                                      eq.asset_allowed_roots(cfg or eq.load_config()),
                                      require_complete=True,
                                      delivered_video=(approval_packet.get("delivery") or {}).get("path"),
                                      watch_log=watch_log if isinstance(watch_log, str) else None)
            except (asset.PacketError, OSError, TypeError) as exc:
                errors.append(f"placeholder flow is not complete and hash-bound: {exc}")
            delivery_path = os.path.realpath(str((approval_packet.get("delivery") or {}).get("path") or ""))
            if not final_files or delivery_path not in {os.path.realpath(p) for p in final_files}:
                errors.append("packet delivery path must be one of DELIVERY.files")
            if any(os.path.basename(p).upper().startswith("DRAFT") for p in final_files):
                errors.append("a DRAFT file can never be delivered")
            try:
                marker = _json(os.path.join(workdir, "DRAFT-DELIVERY.json"), "DRAFT-DELIVERY.json")
                stage_spend = marker.get("generation_spend_usd")
                if not isinstance(stage_spend, (int, float)) or isinstance(stage_spend, bool) or stage_spend < 0:
                    errors.append("DRAFT-DELIVERY generation_spend_usd must be a non-negative number for stage one")
                elif isinstance(finishing_spend, (int, float)) and not isinstance(finishing_spend, bool):
                    total = float(approval_packet.get("prior_paid_spend_usd") or 0) + float(stage_spend) + float(finishing_spend)
                    if total > float(approval_packet.get("generation_budget_usd", asset.MAX_GENERATION_BUDGET_USD)) + 1e-9:
                        errors.append(f"actual paid generation spend ${total:.2f} exceeds the packet's per-video budget")
            except ValueError as exc:
                errors.append(str(exc))
            rebuild = info.get("asset_rebuild")
            expected_scenes = sorted({s for x in approval_packet["items"] for s in x.get("affected_scenes", [])})
            expected_joins = sorted({s for x in approval_packet["items"] for s in x.get("boundary_joins", [])})
            if not isinstance(rebuild, dict):
                errors.append("DELIVERY asset_rebuild evidence is missing")
            else:
                if sorted(rebuild.get("rebuilt_scenes") or []) != expected_scenes:
                    errors.append("asset_rebuild rebuilt_scenes is not exactly the approved affected scenes")
                if sorted(rebuild.get("rebuilt_joins") or []) != expected_joins:
                    errors.append("asset_rebuild rebuilt_joins is not exactly the approved boundary joins")
                if not isinstance(rebuild.get("full_render_count"), int) or rebuild["full_render_count"] < 0:
                    errors.append("asset_rebuild full_render_count must be a non-negative integer")
            errors.extend(_placeholder_stamp_errors(final_files))
    return errors


def prompts(job, executor, cfg, workdir, launch_state="ready"):
    pre = open(eq.PREAMBLE).read().replace("{WORKDIR}", workdir).replace("{JOB}", job["id"])
    if launch_state == "frames_approved":
        pre += ("\n\n## THIS LAUNCH IS FINISHING, NOT A NEW REVISION\n\n"
                "Read the existing placeholders.json and validate it with `asset_approval.py validate --approved` "
                "before any generation or render. Recompute every approved hash; generate motion only for approved "
                "AI items within the remaining per-video budget; insert the exact approved stock/B-roll trims; rebuild "
                "only each item's affected_scenes and boundary_joins. Preserve the draft evidence, remove every "
                "placeholder, append every successful or failed paid attempt to DRAFT-DELIVERY.json's itemized costs, "
                "complete and hash-bind the packet, run the normal shared watch + delivery gates, then "
                "write final DELIVERY.json. This second session is the same logical revision; revision_count does not rise.\n")
    else:
        pre += ("\n\n## THIS LAUNCH IS STAGE ONE WHEN APPROVAL ITEMS EXIST\n\n"
                "Write the scene plan, then create a valid placeholders.json immediately with one best AI frame pair "
                "or the exact moving stock/existing-B-roll preview for every new choice. Continue the entire cut with "
                "labelled exact-duration placeholders. Do not generate AI motion, wait, poll, or start the independent "
                "reviewer. When such items exist, write DRAFT-DELIVERY.json with gate DRAFT and exit; do not write "
                "DELIVERY.json. If there are no approval items, keep the existing one-stage final path.\n")
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
    launch_state = sys.argv[4] if len(sys.argv) > 4 else "ready"
    no_budget = "--no-budget" in sys.argv[5:]
    cfg = eq.load_config()
    job = q.find(q.load(), job_id)
    workdir = eq.work_dir(cfg, job_id)
    os.makedirs(workdir, exist_ok=True)
    try:
        budget_doc = eq.load_budget(workdir)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        budget_doc = eq.start_budget(job, cfg, workdir, run_id, no_budget=no_budget,
                                     preserve_renders=launch_state == "frames_approved")
    log_path = os.path.join(workdir, "queue-run.log")
    if no_budget:
        with open(log_path, "a") as log:
            log.write(f"{q.now_iso()} launch-one --no-budget: per-size time and render caps lifted; "
                      f"{cfg['claims']['max_job_hours']} h outer ceiling remains\n")
    t0 = time.time()
    stop = threading.Event()
    threading.Thread(target=heartbeat_loop, args=(job_id, stop, cfg["claims"]["heartbeat_minutes"]), daemon=True).start()

    outcome, note, verdicts, state = "session_failed", "", [], None
    existing_row = eq.scoreboard_get(run_id) or {}
    usage = list(existing_row.get("model_usage") or [])
    packet = None
    info = {}
    approval_packet = None
    marker = {}
    edit_hours = 0.0
    review_hours = 0.0
    budget_hit = False
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
        packet_path = os.path.join(workdir, asset.PACKET_NAME)
        if launch_state == "frames_approved":
            try:
                approval_packet = asset.read_packet(packet_path, workdir, eq.asset_allowed_roots(cfg),
                                                    require_approved=True)
            except asset.PacketError as exc:
                outcome, state = "parked", "draft_review"
                note = f"Assets need a fresh decision before finishing: {exc}"
        if state is None:
            pre, edit_prompt = prompts(job, executor, cfg, workdir, launch_state)
            role = "finishing" if launch_state == "frames_approved" else "stage-one"
            deadline = datetime.datetime.fromisoformat(budget_doc["deadline"])
            now = datetime.datetime.now(deadline.tzinfo) if deadline.tzinfo else datetime.datetime.now()
            edit_timeout = min(float(cfg["claims"]["max_job_hours"]),
                               max(0.01 / 3600, (deadline - now).total_seconds() / 3600))
            code, tail, edit_hours = run_session(executor, cfg, workdir, edit_prompt, log_path, role,
                                                 edit_timeout, budget_enforced=budget_doc.get("enabled", True))
            usage.append(eq.model_usage_record(executor, cfg,
                                               "finishing editor" if launch_state == "frames_approved" else "stage-one editor",
                                               tail))
        else:
            code, tail = 3, note
        eq.scoreboard_update(run_id, model_usage=usage)
        delivered = os.path.exists(os.path.join(workdir, "DELIVERY.json"))
        if state is not None:
            pass
        elif code == BUDGET_EXCEEDED_CODE:
            budget_hit = True
            outcome, state, note = "budget_exceeded", "needs", budget_note(edit_hours, workdir)
        elif os.path.exists(os.path.join(workdir, "BLOCKED.md")):
            reason = open(os.path.join(workdir, "BLOCKED.md"), errors="replace").readline().strip("# \n")[:200]
            outcome, state, note = "parked", "needs", f"BLOCKED (queue run): {reason}"
        elif launch_state == "ready" and os.path.exists(packet_path):
            try:
                approval_packet = asset.read_packet(packet_path, workdir, eq.asset_allowed_roots(cfg))
            except asset.PacketError as exc:
                outcome, state, note = "parked", "needs", f"Unsafe asset approval packet: {exc}"
            else:
                if approval_packet.get("items"):
                    try:
                        marker = _json(os.path.join(workdir, "DRAFT-DELIVERY.json"), "DRAFT-DELIVERY.json")
                    except ValueError:
                        marker = {}
                    errors = validate_draft_delivery(workdir, packet, approval_packet)
                    if errors:
                        outcome, state = "parked", "needs"
                        note = "Stage-one draft evidence incomplete: " + "; ".join(errors[:6])
                    elif delivered:
                        outcome, state = "parked", "needs"
                        note = "Stage one wrote DELIVERY.json even though approval items remain; a placeholder draft can never deliver."
                    else:
                        fully_approved = approval_packet["status"] == "approved"
                        outcome = "assets_approved" if fully_approved else "draft_review"
                        state = "frames_approved" if fully_approved else "draft_review"
                        note = (f"Asset package approved during stage one; finishing is queued. Packet: {packet_path}"
                                if fully_approved else
                                f"DRAFT only — asset choices are waiting on the review page. Packet: {packet_path}")
        elif not delivered:
            outcome = classify_failure(code, tail, cfg)
            state = "ready" if outcome in ("usage_limited", "auth_failed") and not eq.non_queue_files(workdir) else "stalled"
            note = f"{outcome}: the {executor} session ended without DELIVERY.json or BLOCKED.md (exit {code}); see queue-run.log"
        else:
            info = json.load(open(os.path.join(workdir, "DELIVERY.json")))
            contract_errors = validate_delivery(info, workdir, packet, cfg, launch_state)
            if contract_errors:
                outcome, state = "parked", "needs"
                note = "Efficiency evidence incomplete before review: " + "; ".join(contract_errors[:5])
            else:
                # Exactly one independent review, after the editor's complete candidate and self-QA.
                reviewer = cfg["review"]["reviewer_for"][executor]
                if not eq.auth_ok(reviewer, cfg)[0]:
                    # A fresh process has not seen the build, even if the preferred cross-reviewer is unavailable.
                    reviewer = executor
                    eq.scoreboard_update(run_id, reviewer=f"{executor} (fresh session; cross-reviewer unavailable)")
                brief = (open(eq.REVIEWER_BRIEF).read().replace("{WORKDIR}", workdir).replace("{JOB}", job_id)
                         .replace("{N}", "1").replace("{JOBDOC}", "Handoffs/video-editing/" + job.get("file", "")))
                review_timeout = min(float(cfg["claims"]["max_job_hours"]),
                                     float(budget_doc["review_hours_allowed"]))
                _review_code, review_tail, review_hours = run_session(
                    reviewer, cfg, workdir, brief, log_path, "review-1", review_timeout,
                    budget_enforced=budget_doc.get("enabled", True))
                usage.append(eq.model_usage_record(reviewer, cfg, "independent reviewer", review_tail))
                if _review_code == BUDGET_EXCEEDED_CODE:
                    budget_hit = True
                    outcome, state, note = "budget_exceeded", "needs", budget_note(review_hours, workdir, "review")
                else:
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
        if not info:
            try:
                info = json.load(open(os.path.join(workdir, "DELIVERY.json")))
            except Exception:
                pass
        try:
            marker = json.load(open(os.path.join(workdir, "DRAFT-DELIVERY.json")))
        except Exception:
            marker = marker or {}
        costs = []
        for source in (marker.get("paid_provider_costs"), info.get("paid_provider_costs")):
            if isinstance(source, list):
                costs.extend(source)
        costs = list({json.dumps(row, sort_keys=True, ensure_ascii=False): row for row in costs}.values())
        if not costs:
            costs = [{"provider": "all", "usd": None,
                      "reason": "Per-video paid-provider costs were unavailable because DELIVERY.json did not report them."}]
        prior_hours = float(existing_row.get("wall_hours") or 0) if launch_state == "frames_approved" else 0.0
        flow = dict((eq.scoreboard_get(run_id) or {}).get("asset_flow") or {})
        if approval_packet and approval_packet.get("items"):
            if launch_state == "ready":
                flow.update(packet_visible_at=approval_packet.get("created_at"),
                            stage_one_ended=marker.get("stage_one_ended") or q.now_iso(),
                            full_render_count=int(marker.get("full_render_count") or 0))
                approved_times = [x["approval"].get("timestamp") for x in approval_packet["items"]
                                  if x["approval"].get("status") == "approved"]
                if len(approved_times) == len(approval_packet["items"]):
                    flow["assets_approved_at"] = max(approved_times)
            else:
                rebuild = info.get("asset_rebuild") or {}
                flow.update(finishing_ended=q.now_iso(),
                            full_render_count=int(rebuild.get("full_render_count") or flow.get("full_render_count") or 0),
                            reused_scenes=rebuild.get("reused_scenes") or [],
                            rebuilt_scenes=rebuild.get("rebuilt_scenes") or [],
                            reused_audio=(info.get("reuse") or {}).get("audio"),
                            reused_transcript=(info.get("reuse") or {}).get("transcript"),
                            reused_assets=rebuild.get("reused_assets") or [])
            if flow.get("packet_visible_at") and flow.get("assets_approved_at"):
                try:
                    a = datetime.datetime.fromisoformat(flow["packet_visible_at"])
                    b = datetime.datetime.fromisoformat(flow["assets_approved_at"])
                    flow["human_wait_hours"] = round(max(0, (b - a).total_seconds()) / 3600, 3)
                except ValueError:
                    pass
        spend_rows = [float(x) for x in (marker.get("generation_spend_usd"), info.get("generation_spend_usd"))
                      if isinstance(x, (int, float))]
        budget_doc = update_budget_file(workdir, edit_hours, review_hours, budget_hit)
        existing_budget = existing_row.get("budget") or {}
        recorded_budget = dict((eq.scoreboard_get(run_id) or {}).get("budget") or {})
        recorded_budget.update(
            hours_used=round(float(existing_budget.get("hours_used") or 0) + edit_hours, 6),
            renders_used=int(budget_doc.get("renders_used") or 0),
            review_hours_used=round(float(existing_budget.get("review_hours_used") or 0) + review_hours, 6),
            exceeded=bool(budget_hit),
        )
        eq.scoreboard_update(run_id, ended=q.now_iso(), wall_hours=round(prior_hours + (time.time() - t0) / 3600, 2), outcome=outcome,
                             reviewer_verdicts=verdicts, revision_number=(packet or {}).get("revision_number", 0),
                             revision_rounds=(packet or {}).get("revision_number", 0), model_usage=usage,
                             first_pass_gate=info.get("gate") or marker.get("gate"), paid_provider_costs=costs,
                             generation_spend_usd=sum(spend_rows) if spend_rows else None,
                             asset_flow=flow, budget=recorded_budget, note=note)
        # The claim is the queue's completion signal. Publish the complete logical scoreboard row first,
        # then change state and release, so the next tick/page cannot observe a half-recorded finish.
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
        try:
            eq.sibling("review_page").build()
        except Exception:
            pass


if __name__ == "__main__":
    main()
