#!/usr/bin/env python3
"""Self-test for editcap.py: `python3 editcap.py selftest`. Uses a temporary registry, never the live one, and never
touches the render queue (fake queue activity is passed in). Includes a real dry run: a 6th edit waits in a background
`editcap.py wait` process and starts on its own when an active edit finishes."""
import datetime as dt
import fcntl
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import editcap as ec                                            # noqa: E402

TODAY = dt.date(2026, 10, 21)
PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print("  {} {}{}".format("ok  " if ok else "FAIL", name, "  ({})".format(detail) if detail and not ok else ""))


def fresh():
    d = Path(tempfile.mkdtemp(prefix="editcap-test-"))
    ec.DIR = d
    return d


def ctx(rq=None, now=None, cal=None):
    return (now or time.time(), rq or {}, cal or CAL)


def state(job):
    return json.loads((ec.DIR / "registry.json").read_text())["edits"].get(job, {}).get("state")


def main():
    global CAL
    os.environ.pop("CLAUDE_CODE_HOST_SESSION_ID", None)
    os.environ["CLAUDE_CODE_SESSION_ID"] = "selftest"
    CAL = ec.Calendar(today=TODAY)
    print("editcap selftest")

    # 1. job codes
    cases = {"RO-27": "RO-27", "work:ro27": "RO-27", "DS-40-codex": "DS-40", "sl05-short1": "SL-05",
             "work:RO-20C": "RO-20C", "ro20c": "RO-20C", "SHOOT-20261023": "SHOOT-20261023",
             "work:shoot-20261023": "SHOOT-20261023", "SHOOT-202610230": None,
             "pg:12345": None, "work:cheapkey": None, "": None}
    bad = {k: ec.job_code(k) for k, v in cases.items() if ec.job_code(k) != v}
    check("job codes from render-queue groups", not bad, bad)

    # 2. release dates from the real calendars
    want = {"RO-26": "2026-10-25", "SL-09": "2026-11-13", "SL-18": "2026-10-19", "RO-20C": "2026-12-06",
            "RO-22": ec.LATER, "DS-44": ec.UNDATED}
    got = {j: CAL.date(j)[0] for j in want}
    check("release dates (long-form, shorts, parent+1, 2027, undated)", got == want, got)
    n = CAL.nearest()
    check("ads rank with the nearest upcoming release", CAL.date("RA-09")[0] == n and n >= TODAY.isoformat(), n)
    check("explicit --release wins", CAL.date("DS-44", "2026-10-30")[0] == "2026-10-30")

    # 3. five go, the sixth waits
    fresh()
    codes = [ec.acquire(j, ctx=ctx())[0] for j in ("RO-24", "RO-27", "SL-06", "RA-09", "RO-14")]
    check("first five edits get a slot", codes == [0] * 5, codes)
    c, msg = ec.acquire("DS-44", ctx=ctx())
    check("sixth edit waits (exit 3)", c == ec.EXIT_WAIT and state("DS-44") == "waiting", msg)
    check("acquire again while active is a heartbeat (exit 0)", ec.acquire("RO-24", ctx=ctx())[0] == 0)

    # 4. waiters start in release order, not firing order
    for j in ("RO-22", "SL-18"):                                # fired after DS-44
        ec.acquire(j, ctx=ctx())
    reg = json.loads((ec.DIR / "registry.json").read_text())
    line = [e["job"] for e in ec.order(reg, CAL)]
    check("waiting order is by release date", line == ["SL-18", "RO-22", "DS-44"], line)

    # 5. a finished edit frees a slot for the soonest release
    ec.release("RO-14", ctx=ctx())
    check("finish promotes the soonest waiter", state("SL-18") == "promoted" and state("RO-22") == "waiting",
          (state("SL-18"), state("RO-22")))
    check("promoted waiter starts on acquire", ec.acquire("SL-18", ctx=ctx())[0] == 0 and state("SL-18") == "active")

    # 6. review frees the slot; Dan's notes re-queue it by date
    ec.release("RA-09", review=True, ctx=ctx())
    check("review (waiting on Dan) frees the slot", state("RA-09") == "with-dan" and state("RO-22") == "promoted")
    ec.acquire("RO-22", ctx=ctx())
    c, _ = ec.acquire("RA-09", ctx=ctx())
    reg = json.loads((ec.DIR / "registry.json").read_text())
    line = [e["job"] for e in ec.order(reg, CAL)]
    check("Dan's notes arrive while full: waits, front only if soonest", c == 3 and line == ["RA-09", "DS-44"], line)

    # 7. render-queue activity: unregistered videos count; a running one is never stopped
    fresh()
    rq = {"RO-24": {"live": 2, "last": time.time()}, "SL-06": {"live": 1, "last": time.time()}}
    codes = [ec.acquire(j, ctx=ctx(rq))[0] for j in ("RO-27", "RA-09", "RO-14", "DS-44")]
    check("unregistered render-queue videos use slots", codes == [0, 0, 0, 3], codes)
    check("a video already running in the queue is admitted, not stopped", ec.acquire("SL-06", ctx=ctx(rq))[0] == 0)

    fresh()
    batch = ec.job_code("SHOOT-20261023")
    t0 = time.time() - ec.LEASE_S - 120
    ec.acquire(batch, ctx=ctx(now=t0))
    rq = {batch: {"live": 2, "last": time.time()}}
    ec.release("nobody", ctx=ctx(rq))
    reg = json.loads((ec.DIR / "registry.json").read_text())
    check("active footage batch keeps its lease and counts once", state(batch) == "active"
          and ec.occupancy(reg, rq) == {batch})

    # 8. stale slots and unclaimed reservations are given back
    fresh()
    t0 = time.time() - ec.LEASE_S - 120
    for j in ("RO-24", "RO-27", "SL-06", "RA-09", "RO-14"):
        ec.acquire(j, ctx=ctx(now=t0))
    ec.acquire("DS-44", ctx=ctx(now=t0 + 60))
    ec.acquire("RO-24", ctx=ctx(now=t0 + ec.LEASE_S - 60))      # RO-24 keeps its lease by checking in
    ec.release("nobody", ctx=ctx())                             # any call settles
    st = {j: state(j) for j in ("RO-24", "RO-27", "DS-44")}
    check("an edit silent for 3 h loses its slot; the waiter is promoted",
          st == {"RO-24": "active", "RO-27": "stalled", "DS-44": "promoted"}, st)
    reg = json.loads((ec.DIR / "registry.json").read_text())
    reg["edits"]["DS-44"]["since"] = time.time() - ec.RESERVE_S - 60
    (ec.DIR / "registry.json").write_text(json.dumps(reg))
    ec.release("nobody", ctx=ctx())
    check("a reservation not claimed in 90 min expires", state("DS-44") == "stalled")
    rq = {"RO-27": {"live": 0, "last": time.time() - 60}}
    fresh()
    ec.acquire("RO-27", ctx=ctx(now=time.time() - ec.LEASE_S - 600))
    ec.release("nobody", ctx=ctx(rq))
    check("a recent render-queue grant keeps an edit's lease", state("RO-27") == "active")

    # 9. wake list for a promoted waiter with no auto-start process
    fresh()
    os.environ["CLAUDE_CODE_HOST_SESSION_ID"] = "local_test-session"
    for j in ("RO-24", "RO-27", "SL-06", "RA-09", "RO-14", "DS-44"):
        ec.acquire(j, ctx=ctx())
    os.environ.pop("CLAUDE_CODE_HOST_SESSION_ID")
    _, msg = ec.release("RO-14", ctx=ctx())
    check("release prints a wake message for a waiter with no auto-start", "WAKE claude local_test-session" in msg, msg)

    # 10. fail-open
    d = fresh()
    (d / "registry.json").write_text("{not json")
    check("corrupt registry: set aside, edit allowed", ec.acquire("RO-24", ctx=ctx())[0] == 0
          and list(d.glob("registry.corrupt-*.json")))
    fd = os.open(str(d / "registry.lock"), os.O_RDWR | os.O_CREAT)
    fcntl.flock(fd, fcntl.LOCK_EX)
    old, ec.LOCK_TIMEOUT_S = ec.LOCK_TIMEOUT_S, 0.3
    c, msg = ec.acquire("RO-27", ctx=ctx())
    ec.LOCK_TIMEOUT_S = old
    os.close(fd)
    check("registry locked too long: edit allowed (never deadlocks)", c == 0, msg)
    ro = fresh()
    ro.chmod(0o500)
    c, _ = ec.acquire("RO-27", ctx=ctx())
    ro.chmod(0o700)
    check("registry folder not writable: edit allowed", c == 0)
    env = dict(os.environ, EDITCAP_DIR="/dev/null/nope", EDITCAP_NO_RENDERQ="1")
    r = subprocess.run([sys.executable, str(HERE / "editcap.py"), "acquire", "RO-27"], env=env,
                       capture_output=True, text=True)
    check("CLI fail-open on an impossible registry path (exit 0)", r.returncode == 0, r.stderr[-200:])

    # 11. dry run end to end through the CLI: 6th waits in the background, starts when one finishes
    d = fresh()
    env = dict(os.environ, EDITCAP_DIR=str(d), EDITCAP_NO_RENDERQ="1", EDITCAP_POLL="0.3",
               EDITCAP_TODAY=TODAY.isoformat())
    env.pop("CLAUDE_CODE_SESSION_ID", None)
    cli = lambda *a: subprocess.run([sys.executable, str(HERE / "editcap.py")] + list(a), env=env,
                                    capture_output=True, text=True)
    codes = [cli("acquire", j).returncode for j in ("RO-24", "RO-27", "SL-06", "RA-09", "RO-14")]
    six = cli("acquire", "SL-18", "--title", "Wasted Life", "--type", "SFL")
    check("CLI: five go, sixth exits 3", codes == [0] * 5 and six.returncode == 3, six.stdout)
    waiter = subprocess.Popen([sys.executable, str(HERE / "editcap.py"), "wait", "SL-18"], env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1.5)
    st = cli("status").stdout
    check("CLI: status shows the waiter in line with auto-start armed",
          waiter.poll() is None and "1. SL-18" in st and "auto-start armed" in st, st)
    cli("release", "RO-24")
    try:
        out, _ = waiter.communicate(timeout=10)
        ok = waiter.returncode == 0 and "Go" in out
    except subprocess.TimeoutExpired:
        waiter.kill()
        ok, out = False, "timed out"
    st = cli("status").stdout
    check("CLI: finishing one edit starts the waiter by itself", ok and "SL-18" in st.split("WAITING")[0], out)
    check("CLI: status is read-only", cli("status", "--json").returncode == 0)

    print("{} passed, {} failed".format(len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
