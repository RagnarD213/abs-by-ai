#!/usr/bin/env python3
"""Shared pieces of the overnight edit queue: config, routing, executor commands, the scoreboard.

Nothing here decides anything. `dispatcher.py` decides what to launch, `runner.py` runs one job, and
`queue.py` stays the only writer of job state. Procedure and the plain-language tour: README.md here.

⚠ This folder holds a file named queue.py, which shadows Python's standard `queue` module for any script
started from here (logging.handlers and concurrent.futures import it). Every script in this folder calls
`unshadow()` first and loads its siblings with `sibling()`, never with a bare `import queue`.
"""
import contextlib, datetime, fcntl, glob, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CONFIG = os.environ.get("EDIT_QUEUE_CONFIG") or os.path.join(HERE, "config.json")   # env override: tests only
SCOREBOARD = os.environ.get("EDIT_QUEUE_SCOREBOARD") or os.path.join(HERE, "scoreboard.json")
PAUSE_FILE = os.environ.get("EDIT_QUEUE_PAUSE_FILE") or os.path.join(HERE, "PAUSE")
PREAMBLE = os.path.join(HERE, "preamble.md")
REVIEWER_BRIEF = os.path.join(HERE, "reviewer-brief.md")
BUDGET_NAME = "BUDGET.json"


def unshadow():
    sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]


def sibling(name):
    """Load scripts/edit-queue/<name>.py under the module name eq_<name>."""
    alias = "eq_" + name
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


def load_config(path=None):
    with open(path or CONFIG) as f:
        return json.load(f)


def save_config(cfg, path=None):
    path = path or CONFIG
    with open(path + ".tmp", "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(path + ".tmp", path)


# ---------------------------------------------------------------- routing

def group_of(job_id):
    return job_id.split("-")[0].upper()


def executor_for(job_id, cfg):
    """Dan's routing table. None = this group is never launched by the queue (RX, or an unknown prefix)."""
    g = group_of(job_id)
    if g in cfg.get("not_queued", []):
        return None
    ex = cfg["routing"].get(g)
    return ex if ex in cfg["executors"] else None


def paused_reason(job_id, executor, cfg):
    """Circuit breaker: a group paused for one executor (or for 'any')."""
    for p in cfg.get("paused_groups", []):
        if p.get("group") == group_of(job_id) and p.get("executor") in (executor, "any"):
            return p.get("reason") or "paused"
    return None


# ---------------------------------------------------------------- work directories

def work_dir(cfg, job_id):
    return os.path.join(cfg["work_root"], job_id)


def asset_allowed_roots(cfg):
    """Resolve the explicit packet source roots. Relative entries are repo-relative."""
    out = []
    for root in cfg.get("asset_approval", {}).get("allowed_source_roots", []):
        root = os.path.expanduser(root)
        out.append(os.path.abspath(root if os.path.isabs(root) else os.path.join(ROOT, root)))
    return out


def non_queue_files(path):
    """Anything in a work directory that the queue itself did not write = a session started building there."""
    try:
        owned = {"WORK_PACKET.json", BUDGET_NAME, BUDGET_NAME + ".lock"}
        return [n for n in os.listdir(path) if n not in owned and not n.startswith(("queue-", "._", ".DS_Store"))]
    except OSError:
        return []


def existing_work_dirs(cfg, job_id):
    """Hand-fired jobs named their folders ra01, ds-17, AV-01. One with a build in it means: someone has
    been here, so the queue keeps out. A folder holding only the queue's own logs does not count."""
    want = {job_id.lower(), job_id.lower().replace("-", "")}
    try:
        names = os.listdir(cfg["work_root"])
    except OSError:
        return []
    return [n for n in names if n.lower() in want and non_queue_files(os.path.join(cfg["work_root"], n))]


# ---------------------------------------------------------------- per-job work budgets

def job_budget(job, cfg, no_budget=False):
    """Resolve the size row, then apply a job's explicit override. The absolute ceiling always wins."""
    size = job.get("size")
    try:
        values = dict(cfg["budget"]["sizes"][size])
    except KeyError as exc:
        raise ValueError(f"no budget is configured for job size {size!r}") from exc
    override = job.get("budget") or {}
    if not isinstance(override, dict):
        raise ValueError("job budget override must be an object")
    unknown = set(override) - {"edit_hours", "full_renders", "review_hours"}
    if unknown:
        raise ValueError(f"unknown job budget field(s): {', '.join(sorted(unknown))}")
    values.update(override)
    for key in ("edit_hours", "review_hours"):
        if not isinstance(values.get(key), (int, float)) or isinstance(values.get(key), bool) or values[key] <= 0:
            raise ValueError(f"budget {key} must be a positive number")
    if (not isinstance(values.get("full_renders"), int) or isinstance(values.get("full_renders"), bool)
            or values["full_renders"] < 1):
        raise ValueError("budget full_renders must be a positive integer")
    outer = float(cfg["claims"]["max_job_hours"])
    soft = float(cfg["budget"].get("soft_deadline_fraction", 0.7))
    if not 0 < soft < 1:
        raise ValueError("budget soft_deadline_fraction must be between 0 and 1")
    source = "no-budget override" if no_budget else ("job override" if override else f"size {size}")
    return {
        "enabled": not no_budget,
        "source": source,
        "edit_hours": outer if no_budget else min(float(values["edit_hours"]), outer),
        "review_hours": outer if no_budget else min(float(values["review_hours"]), outer),
        "full_renders": None if no_budget else int(values["full_renders"]),
        "soft_deadline_fraction": soft,
    }


def start_budget(job, cfg, workdir, run_id, no_budget=False, preserve_renders=False, now=None):
    """Write the launch's clock before its runner starts. Preserve render use for Phase 2 finishing."""
    values = job_budget(job, cfg, no_budget)
    now = now or datetime.datetime.now().astimezone()
    if now.tzinfo is None:
        now = now.astimezone()
    path = os.path.join(workdir, BUDGET_NAME)
    renders_used = 0
    if preserve_renders and os.path.exists(path):
        try:
            with open(path) as fh:
                renders_used = int(json.load(fh).get("renders_used") or 0)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            renders_used = 0
    deadline = now + datetime.timedelta(hours=values["edit_hours"])
    soft = now + datetime.timedelta(hours=values["edit_hours"] * values["soft_deadline_fraction"])
    doc = {
        "schema": 1,
        "job": job["id"],
        "run_id": run_id,
        "size": job.get("size"),
        "enabled": values["enabled"],
        "source": values["source"],
        "started": now.isoformat(timespec="seconds"),
        "deadline": deadline.isoformat(timespec="seconds"),
        "soft_deadline": soft.isoformat(timespec="seconds"),
        "hours_allowed": values["edit_hours"],
        "review_hours_allowed": values["review_hours"],
        "max_full_renders": values["full_renders"],
        "renders_used": renders_used,
        "hours_used": 0.0,
        "review_hours_used": 0.0,
        "exceeded": False,
    }
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)
    return doc


def load_budget(workdir):
    with open(os.path.join(workdir, BUDGET_NAME)) as fh:
        return json.load(fh)


def scoreboard_budget(doc):
    return {
        "hours_allowed": doc["hours_allowed"],
        "hours_used": 0.0,
        "renders_allowed": doc["max_full_renders"],
        "renders_used": doc["renders_used"],
        "review_hours_allowed": doc["review_hours_allowed"],
        "review_hours_used": 0.0,
        "exceeded": False,
        "enabled": doc["enabled"],
        "source": doc["source"],
    }


# ---------------------------------------------------------------- executors

def _version_key(path):
    m = re.search(r"/claude-code/([0-9.]+)/", path)
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def resolve_binary(executor, cfg):
    ex = cfg["executors"][executor]
    if ex.get("binary"):
        return os.path.expanduser(ex["binary"])
    # The desktop app's Claude Code lives in a versioned folder that changes on every app update.
    hits = sorted(glob.glob(os.path.expanduser(ex["binary_glob"])), key=_version_key)
    return hits[-1] if hits else None


def build_command(executor, cfg, workdir, role="edit"):
    """The exact argv that ran (Codex) or is expected to run (Claude) with no human prompt. Prompt goes on stdin."""
    ex = cfg["executors"][executor]
    binary = resolve_binary(executor, cfg)
    if not binary:
        raise FileNotFoundError(f"no {executor} binary found")
    if executor == "codex":
        cmd = [binary, "exec", "-C", ROOT, "-s", ex.get("sandbox", "workspace-write"),
               "-c", 'approval_policy="never"', "-c", "sandbox_workspace_write.network_access=true",
               "--add-dir", workdir]
        for d in ex.get("extra_writable_dirs", []):
            d = os.path.expanduser(d)
            if os.path.isdir(d):
                cmd += ["--add-dir", d]
        if ex.get("model"):
            cmd += ["-m", ex["model"]]
        if ex.get("effort"):
            cmd += ["-c", f'model_reasoning_effort="{ex["effort"]}"']
        return cmd + ["-"]
    cmd = [binary, "-p", "--permission-mode", ex.get("permission_mode", "bypassPermissions"),
           "--add-dir", workdir, "--output-format", "text"]
    if ex.get("model"):
        cmd += ["--model", ex["model"]]
    if ex.get("effort"):
        cmd += ["--effort", ex["effort"]]
    if ex.get("no_mcp_servers"):
        cmd += ["--strict-mcp-config"]     # no connectors at all: nothing to post, send or upload with
    if ex.get("disallowed_tools"):
        cmd += ["--disallowedTools", ",".join(ex["disallowed_tools"])]
    if role.startswith("review") and ex.get("reviewer_agent"):
        cmd += ["--agent", ex["reviewer_agent"]]
    return cmd


def auth_ok(executor, cfg, run=None):
    """Free sign-in check (no tokens). True / False, plus a sentence for the page."""
    import subprocess
    ex = cfg["executors"][executor]
    binary = resolve_binary(executor, cfg)
    if not binary or not os.path.exists(binary):
        return False, f"{executor}: program not found"
    if not ex.get("auth_check"):
        return True, ""
    try:
        r = (run or subprocess.run)([binary] + ex["auth_check"], capture_output=True, text=True, timeout=60)
        if json.loads(r.stdout).get("loggedIn"):
            return True, ""
        return False, f"{executor}: not signed in. Dan signs in once: run the program in Terminal and type /login"
    except Exception as e:   # unreadable answer = not proven = not OK
        return False, f"{executor}: sign-in check failed ({e!s:.200})"


# ---------------------------------------------------------------- scoreboard

@contextlib.contextmanager
def _sb_lock():
    with open(SCOREBOARD + ".lock", "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def scoreboard_load():
    if not os.path.exists(SCOREBOARD):
        return {"schema": 1, "runs": []}
    with open(SCOREBOARD) as f:
        return json.load(f)


def _sb_save(sb):
    with open(SCOREBOARD + ".tmp", "w") as f:
        json.dump(sb, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(SCOREBOARD + ".tmp", SCOREBOARD)


def scoreboard_add(row):
    with _sb_lock():
        sb = scoreboard_load()
        sb["runs"].append(row)
        _sb_save(sb)


def scoreboard_update(run_id, **fields):
    with _sb_lock():
        sb = scoreboard_load()
        for r in sb["runs"]:
            if r["run_id"] == run_id:
                r.update(fields)
        _sb_save(sb)


def scoreboard_latest(job_id):
    runs = [r for r in scoreboard_load()["runs"] if r["job"] == job_id]
    return runs[-1] if runs else None


def scoreboard_get(run_id):
    return next((r for r in scoreboard_load()["runs"] if r["run_id"] == run_id), None)


def new_run_row(job, executor, cfg, now=None, budget_doc=None):
    now = now or datetime.datetime.now()
    revision_number = int((job.get("queue_revision") or {}).get("round", 0))
    if budget_doc is None:
        values = job_budget(job, cfg)
        budget_doc = {
            "hours_allowed": values["edit_hours"], "review_hours_allowed": values["review_hours"],
            "max_full_renders": values["full_renders"], "renders_used": 0,
            "enabled": values["enabled"], "source": values["source"],
        }
    return {
        "run_id": f"{job['id']}-{now.strftime('%Y%m%d-%H%M%S')}", "job": job["id"], "group": group_of(job["id"]),
        "title": job.get("title", ""), "size": job.get("size", ""), "executor": executor,
        "reviewer": cfg["review"]["reviewer_for"].get(executor, ""), "started": now.isoformat(timespec="seconds"),
        "ended": None, "wall_hours": None, "outcome": "running", "reviewer_verdicts": [],
        "first_pass_gate": None, "revision_number": revision_number, "revision_rounds": revision_number,
        "model_usage": [], "paid_provider_costs": None, "generation_spend_usd": None,
        "budget": scoreboard_budget(budget_doc) if budget_doc else None,
        "dan_verdict": None, "dan_words": None, "systemic_reason": None, "corpus_entry": None,
        "asset_flow": {
            "schema": 1, "launch_state": job.get("state"), "packet_visible_at": None,
            "stage_one_ended": None, "assets_approved_at": None, "finishing_started": None,
            "finishing_ended": None, "human_wait_hours": None,
            "approval_submissions": 0, "approval_rejections": 0,
            "full_render_count": 0, "reused_scenes": [], "rebuilt_scenes": [],
            "reused_audio": None, "reused_transcript": None, "reused_assets": [],
        },
        "log": os.path.join(work_dir(cfg, job["id"]), "queue-run.log"),
    }


def model_usage_record(executor, cfg, role, output=""):
    """Record only per-session usage the launcher actually exposes."""
    ex = cfg["executors"][executor]
    match = re.search(r"tokens used\s*[\r\n]+\s*([\d,]+)", output or "", re.I)
    return {
        "role": role,
        "executor": executor,
        "model": ex.get("model") or None,
        "effort": ex.get("effort") or None,
        "total_tokens": int(match.group(1).replace(",", "")) if match else None,
        "input_tokens": None,
        "cached_input_tokens": None,
        "output_tokens": None,
        "available_tokens": None,
        "measurement": "available_total_only" if match else "unavailable",
        "reason": ("CLI exposed only total tokens; input/output/cache split is unavailable."
                   if match else "Per-session token counts were not exposed in this CLI output; account-wide allowance is not attributed to one video."),
        "available_tokens_reason": "The executors do not expose a per-session or per-video remaining-token allowance.",
    }
