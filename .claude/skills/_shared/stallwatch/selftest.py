#!/usr/bin/env python3
"""stallwatch self-test: real processes in a temporary work drive, a temporary state folder, no render queue,
no notifications, the real edit-cap registry untouched. `python3 stallwatch.py selftest`."""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "stallwatch.py"
RESULTS = []
BG = dict(start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print("{} {}{}".format("PASS" if ok else "FAIL", name, "" if ok else "  <- " + str(detail)))


def age(folder, minutes):
    """Make every file in a folder look `minutes` old."""
    t = time.time() - minutes * 60
    for dp, _dn, fn in os.walk(str(folder)):
        for f in fn:
            os.utime(os.path.join(dp, f), (t, t))


def age_runs(sw, job, minutes):
    for n in os.listdir(str(sw.DIR / "runs")):
        p = sw.DIR / "runs" / n
        r = json.load(open(p))
        if r["job"] == job:
            for k in ("start", "end"):
                if r.get(k):
                    r[k] -= minutes * 60
            json.dump(r, open(p, "w"))


def row(rows, job):
    return next((r for r in rows if r["job"] == job), None)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="stallwatch-test-"))
    root, state, ecdir = tmp / "drive", tmp / "state", tmp / "editcap"
    work = root / "_edit_work"
    for d in (work, state, ecdir):
        d.mkdir(parents=True)
    env = dict(os.environ, STALLWATCH_DIR=str(state), STALLWATCH_WORKROOTS=str(root), STALLWATCH_NO_RENDERQ="1",
               STALLWATCH_NO_NOTIFY="1", EDITCAP_DIR=str(ecdir), EDITCAP_NO_RENDERQ="1")
    os.environ.update({k: env[k] for k in ("STALLWATCH_WORKROOTS", "STALLWATCH_NO_RENDERQ", "STALLWATCH_NO_NOTIFY",
                                           "EDITCAP_DIR", "EDITCAP_NO_RENDERQ")})
    sys.path.insert(0, str(HERE))
    import stallwatch as sw                                     # noqa: E402
    sw.DIR = state
    procs = []
    try:
        # ---- 1. The 2026-11-04 incident: a chain dies on a SyntaxError in its finish step; the error goes to
        #         final/logs/finish.log, the chain log only shows the last step DONE.
        job = work / "ZZ-91" / "round3"
        (job / "final" / "logs").mkdir(parents=True)
        (job / "finish.py").write_text("def broken(:\n")
        (job / "chain.sh").write_text(
            "set -e\necho 'step 1 picture DONE' >> chain.log\necho 'step 2 finish' >> chain.log\n"
            "python3 finish.py > final/logs/finish.log 2>&1\necho CHAIN_DONE >> chain.log\n")
        cenv = dict(env, CLAUDE_CODE_HOST_SESSION_ID="local_test-crash-session")
        r = subprocess.run([sys.executable, str(SCRIPT), "run", "ZZ-91", "--", "bash", "chain.sh"], cwd=str(job),
                           env=cenv, capture_output=True, text=True)
        check("run passes the chain's exit code through", r.returncode == 1, r.returncode)
        check("run reports CHAIN_FAILED with the finish.log error, not the chain log",
              "CHAIN_FAILED" in r.stdout and "SyntaxError" in r.stdout, r.stdout)
        rows = sw.assess(entries={}, live={})
        check("a fresh failure is not nudged yet (its own run already woke the session)",
              row(rows, "ZZ-91")["status"] == "quiet", row(rows, "ZZ-91"))
        age(job, 25)
        age_runs(sw, "ZZ-91", 25)
        now = time.time()
        rows = sw.assess(now, entries={}, live={})
        r91 = row(rows, "ZZ-91")
        check("crashed chain is STALLED after 20 min", r91["status"] == "stalled", r91)
        check("stall names finish.log and the SyntaxError", "finish.log" in r91["hint"] and
              "SyntaxError" in r91["hint"], r91["hint"])
        acts = [a for a in sw.plan(rows, now, claim=True) if a["job"] == "ZZ-91"]
        check("owning Claude session is nudged once", len(acts) == 1 and acts[0]["kind"] == "nudge" and
              acts[0]["session"] == "local_test-crash-session" and acts[0]["n"] == 1, acts)
        check("nudge says which step and how to restart", "finish.log" in acts[0]["message"] and
              "restart" in acts[0]["message"] and "Nudge 1 of 2" in acts[0]["message"], acts[0]["message"])
        acts = [a for a in sw.plan(sw.assess(now + 60, entries={}, live={}), now + 60, claim=True)
                if a["job"] == "ZZ-91"]
        check("no second nudge 15 min later (30 min spacing)", acts == [], acts)
        acts = [a for a in sw.plan(sw.assess(now + 31 * 60, entries={}, live={}), now + 31 * 60, claim=True)
                if a["job"] == "ZZ-91"]
        check("second nudge after 30 min", len(acts) == 1 and acts[0]["n"] == 2, acts)
        acts = [a for a in sw.plan(sw.assess(now + 62 * 60, entries={}, live={}), now + 62 * 60, claim=True)
                if a["job"] == "ZZ-91"]
        check("after 2 nudges, Dan is told instead", len(acts) == 1 and acts[0]["kind"] == "dan", acts)
        acts = [a for a in sw.plan(sw.assess(now + 93 * 60, entries={}, live={}), now + 93 * 60, claim=True)
                if a["job"] == "ZZ-91"]
        check("Dan is told only once", acts == [], acts)

        # ---- 2. A healthy long render: logs silent for 2 hours, but its ffmpeg-like process is alive.
        job = work / "ZZ-93"
        job.mkdir()
        (job / "render.log").write_text("frame= 100\n")
        age(job, 120)
        p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], cwd=str(job), **BG)
        procs.append(p)
        ent = {"ZZ-93": dict(job="ZZ-93", state="active", ai="claude", wake="local_test-healthy",
                             active_since=time.time() - 3 * 3600)}
        time.sleep(0.5)
        flagged = []
        for k in range(4):
            t = time.time() + k * 31 * 60
            rows = sw.assess(t, entries=ent, live={})
            flagged += [a for a in sw.plan(rows, t, claim=True) if a["job"] == "ZZ-93"]
        r93 = row(rows, "ZZ-93")
        check("healthy long render reads as running", r93["status"] == "running", r93)
        check("healthy long render is never nudged", flagged == [], flagged)

        # ---- 3. Same healthy render through the run wrapper, started outside any work folder.
        outside = tmp / "elsewhere"
        outside.mkdir()
        p = subprocess.Popen([sys.executable, str(SCRIPT), "run", "ZZ-94", "--log", str(outside / "r.log"), "--",
                              sys.executable, "-c", "import time; time.sleep(120)"], cwd=str(outside), env=cenv, **BG)
        procs.append(p)
        time.sleep(1.5)
        (outside / "r.log").write_text("working\n")
        age(outside, 60)
        age_runs(sw, "ZZ-94", 60)
        rows = sw.assess(entries={}, live={})
        check("a recorded run that is still alive is running", row(rows, "ZZ-94")["status"] == "running",
              row(rows, "ZZ-94"))

        # ---- 4. The watcher that missed the incident does not count as life; a review server neither.
        job = work / "ZZ-95"
        job.mkdir()
        (job / "chain.log").write_text("step 1 DONE\nstep 2 finish\n")
        age(job, 30)
        w = subprocess.Popen(["bash", "-c", "while true; do grep -q CHAIN_DONE chain.log; sleep 1; done"],
                             cwd=str(job), **BG)
        procs.append(w)
        ent = {"ZZ-95": dict(job="ZZ-95", state="active", ai="claude", wake="local_test-watcher",
                             active_since=time.time() - 2 * 3600)}
        time.sleep(0.5)
        r95 = row(sw.assess(entries=ent, live={}), "ZZ-95")
        check("a grep/sleep watch loop is not a live job (stalled)", r95["status"] == "stalled", r95)
        seen = [q for q in sw.process_table() if q["pid"] == w.pid]
        check("...and the loop really was seen in the job folder (not missed by path)",
              seen and os.path.realpath(seen[0]["cwd"]) == os.path.realpath(str(job)), seen)
        table = [dict(pid=1001, ppid=1, cmd="/usr/bin/python3 review_server.py 9999 {}".format(job), cwd=str(job))]
        check("a review server is not a live job", sw.job_processes(table, [job], "ZZ-95", set()) == [])

        # ---- 5. Markers and edit-cap state.
        job = work / "ZZ-96"
        job.mkdir()
        (job / "chain.log").write_text("step 1 DONE\nall steps\nCHAIN_DONE\n")
        age(job, 40)
        ent = {"ZZ-96": dict(job="ZZ-96", state="active", ai="claude", wake="local_x",
                             active_since=time.time() - 3600)}
        check("CHAIN_DONE marker = done", row(sw.assess(entries=ent, live={}), "ZZ-96")["status"] == "done")
        (job / "chain.log").write_text("DELIVERY GATE FAIL   (543s)\n\nCHAIN_R3_DONE\n")
        age(job, 40)
        check("CHAIN_R3_DONE (the real RO-31 ending) = done",
              row(sw.assess(entries=ent, live={}), "ZZ-96")["status"] == "done")
        (tmp / "x.log").write_text("step 1 DONE\nstep 2 finish\n")
        check("a per-step DONE above the last line is not done", sw.log_verdict([(0, str(tmp / "x.log"))])[0] is None)
        (tmp / "y.log").write_text("CHAIN_DONE\nrerun\nCHAIN_FAILED at line 9\n")
        check("CHAIN_FAILED after an earlier CHAIN_DONE = failed",
              sw.log_verdict([(0, str(tmp / "y.log"))])[0] == "failed")
        ent["ZZ-96"]["active_since"] = time.time() - 60
        check("logs from before the edit took its slot are ignored (idle, not stalled)",
              row(sw.assess(entries=ent, live={}), "ZZ-96")["status"] == "idle")
        ent = {"ZZ-95": dict(job="ZZ-95", state="with-dan", ai="claude", wake="local_test-watcher")}
        check("an edit with Dan is never watched", row(sw.assess(entries=ent, live={}), "ZZ-95") is None)
        check("render-queue steps = running", row(sw.assess(entries={"ZZ-95": dict(
            job="ZZ-95", state="active", active_since=time.time() - 7200)}, live={"ZZ-95": 1}), "ZZ-95")["status"]
            == "running")
        ent = {"ZZ-95": dict(job="ZZ-95", state="active", ai="codex", wake="019abc",
                             active_since=time.time() - 7200)}
        acts = sw.plan(sw.assess(entries=ent, live={}), claim=True)
        check("a Codex-owned stall goes to Dan with the thread id",
              [a["kind"] for a in acts if a["job"] == "ZZ-95"] == ["dan"] and "019abc" in acts[-1]["message"], acts)

        # ---- 6. ok silences a stall until the job moves again.
        st = json.load(open(state / "state.json"))
        sig = row(sw.assess(entries={}, live={}), "ZZ-91")["signature"]
        st["jobs"]["ZZ-91"] = {"acked": sig}
        json.dump(st, open(state / "state.json", "w"))
        rows = sw.assess(time.time() + 4 * 3600, entries={}, live={})
        acts = [a for a in sw.plan(rows, time.time() + 4 * 3600, claim=True) if a["job"] == "ZZ-91"]
        check("an acknowledged stall stays quiet", acts == [] and row(rows, "ZZ-91")["status"] == "acked",
              (acts, row(rows, "ZZ-91")))
        r = subprocess.run([sys.executable, str(SCRIPT), "check", "ZZ-91"], env=env, capture_output=True, text=True)
        check("check exits 5 on a stalled job", r.returncode == 5, (r.returncode, r.stdout, r.stderr))
    finally:
        for p in procs:
            try:
                os.killpg(p.pid, 9)
                p.wait(timeout=5)
            except Exception:
                pass
        subprocess.run(["rm", "-rf", str(tmp)])
    print("{} of {} checks passed".format(sum(RESULTS), len(RESULTS)))
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
