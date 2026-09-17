#!/usr/bin/env python3
"""Run ONE queue job inside its slot: edit -> cross-review -> (one revision -> review) -> hand to Dan or park.

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
import datetime, json, os, re, subprocess, sys, threading, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eq_common as eq                                          # noqa: E402
eq.unshadow()
q = eq.sibling("queue")
QUEUE_PY = os.path.join(eq.HERE, "queue.py")


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


def prompts(job, executor, cfg, workdir):
    pre = open(eq.PREAMBLE).read().replace("{WORKDIR}", workdir).replace("{JOB}", job["id"])
    edit = pre + "\n\n---\n\n" + job[executor]
    if job.get("queue_revision"):
        rv = job["queue_revision"]
        edit = (pre + f"\n\n---\n\nThis is REVISION round {rv.get('round', 1)} of {job['id']} after Dan watched the delivered cut. "
                "His exact words are below. First record them as a regression-corpus entry (AGENTS.md: a rejection becomes a "
                "corpus entry in the same session, before the fix). Then work in the existing work directory, change only what "
                "he asked for, re-run every gate on the new delivered file and rewrite DELIVERY.json.\n\n"
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

    outcome, note, verdicts, rounds, state = "session_failed", "", [], 0, None
    try:
        for stale in ("DELIVERY.json", "BLOCKED.md"):          # a revision run must earn these again
            p = os.path.join(workdir, stale)
            if os.path.exists(p):
                os.replace(p, p + f".before-{run_id}")
        pre, edit_prompt = prompts(job, executor, cfg, workdir)
        code, tail = run_session(executor, cfg, workdir, edit_prompt, log_path, "edit", cfg["claims"]["max_job_hours"])
        reviewer = cfg["review"]["reviewer_for"][executor]
        if not eq.auth_ok(reviewer, cfg)[0]:
            # Independent review still happens: a fresh session of the editor's own tool has not seen the build either.
            reviewer = executor
            eq.scoreboard_update(run_id, reviewer=f"{executor} (fresh session; cross-reviewer unavailable)")

        while True:
            delivered = os.path.exists(os.path.join(workdir, "DELIVERY.json"))
            if os.path.exists(os.path.join(workdir, "BLOCKED.md")):
                reason = open(os.path.join(workdir, "BLOCKED.md"), errors="replace").readline().strip("# \n")[:200]
                outcome, state, note = "parked", "needs", f"BLOCKED (queue run): {reason}"
                break
            if not delivered:
                outcome = classify_failure(code, tail, cfg)
                state = "ready" if outcome in ("usage_limited", "auth_failed") and not eq.non_queue_files(workdir) else "stalled"
                note = f"{outcome}: the {executor} session ended without DELIVERY.json or BLOCKED.md (exit {code}); see queue-run.log"
                break
            n = len(verdicts) + 1
            brief = (open(eq.REVIEWER_BRIEF).read().replace("{WORKDIR}", workdir).replace("{JOB}", job_id)
                     .replace("{N}", str(n)).replace("{JOBDOC}", "Handoffs/video-editing/" + job.get("file", "")))
            run_session(reviewer, cfg, workdir, brief, log_path, f"review-{n}", 3)
            verdict, vpath = read_verdict(workdir, n)
            verdicts.append(verdict)
            eq.scoreboard_update(run_id, reviewer_verdicts=verdicts)
            if verdict == "SHIP":
                outcome, state, note = "delivered", "delivered", f"Queue run {run_id}: independent reviewer ({reviewer}) says SHIP. Review copy in DELIVERY.json."
                break
            if verdict == "DOES NOT SHIP" and rounds < cfg["review"]["auto_revision_rounds"]:
                rounds += 1
                fix = (pre + f"\n\n---\n\nThe independent reviewer watched your delivery of {job_id} and says it DOES NOT SHIP. Read "
                       f"`{vpath}` and fix every defect it lists, in the same work directory. Re-run every gate on the new delivered "
                       "file and rewrite DELIVERY.json. Do not argue with the review in notes; fix or, if a finding is factually "
                       "wrong, say why in one line in notes.md. This is the only automatic revision round.")
                os.replace(os.path.join(workdir, "DELIVERY.json"), os.path.join(workdir, f"DELIVERY.round{rounds}.json"))
                code, tail = run_session(executor, cfg, workdir, fix, log_path, f"revision-{rounds}", cfg["claims"]["max_job_hours"])
                continue
            outcome, state = "parked", "needs"
            note = (f"Reviewer: {verdict} after {rounds} automatic revision round(s). Review attached: {vpath}")
            break
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
        eq.scoreboard_update(run_id, ended=q.now_iso(), wall_hours=round((time.time() - t0) / 3600, 2), outcome=outcome,
                             reviewer_verdicts=verdicts, revision_rounds=rounds, first_pass_gate=info.get("gate"),
                             generation_spend_usd=info.get("generation_spend_usd"), note=note)
        try:
            eq.sibling("review_page").build()
        except Exception:
            pass


if __name__ == "__main__":
    main()
