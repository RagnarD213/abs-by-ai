#!/usr/bin/env python3
"""Back up raw shoot media overnight, then offload shoots marked complete.

Run with --dry-run to inspect the inventory. The launchd job calls --once every
15 minutes, but actual work runs only from 8 pm to 8 am Chicago time. A lock
prevents overlapping runs. Transfers resume on the next tick after an error.
"""

import argparse
import fcntl
import hashlib
import json
import os
import plistlib
import re
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


SOURCE = Path("/Volumes/Extreme")
ARCHIVE = Path("/Volumes/Expansion")
ARCHIVE_ROOT = ARCHIVE / "Abs By AI Raw Footage"
DRIVE_ROOT = "gdrive:Abs By AI Raw Footage"
RCLONE = Path.home() / "bin/rclone"
STATE_DIR = Path.home() / "Library/Application Support/Abs By AI"
STATE_FILE = STATE_DIR / "nightly-footage.json"
LOCK_FILE = STATE_DIR / "nightly-footage.lock"
DRIVE_MARKER = ARCHIVE / ".absbyai-footage-archive-id"
READY_MARKER = "READY_TO_ARCHIVE"
READY_MAX_AGE = 24 * 60 * 60
QUEUE_FILE = Path(__file__).resolve().parents[2] / "Handoffs/video-editing/jobs.json"
LOG_DIR = Path.home() / "Library/Logs/absbyai-footage-offload"
LABEL = "com.absbyai.nightly-footage"
PLIST = Path.home() / "Library/LaunchAgents" / (LABEL + ".plist")
TZ = ZoneInfo("America/Chicago")
RAW_SUFFIXES = {".mp4", ".mov", ".mxf", ".wav", ".xml", ".lrv", ".thm", ".insv", ".jpg", ".jpeg"}
SKIP_DIRS = {".spotlight-v100", ".fseventsd", ".temporaryitems", "system volume information"}

# Existing Drive names differ from the local names. Keep these mappings so the
# nightly copy fills existing shoot folders instead of creating duplicates.
SHOOTS = {
    "abs by ai welcome-video first shoot": {
        "drive": "abs by ai welcome-video first shoot", "raw": ["main camera"],
    },
    "abs by ai 7:8 Jeff Chagrin shoot": {
        "drive": "Test Shoot - July 8 - Jeff Chagrin - YouTube Videos", "raw": ["main camera", "gopro"],
    },
    "abs by ai 8:3 jeff chagrin shoot": {
        "drive": "abs by ai 8／3 jeff chagrin shoot", "raw": ["main camera", "gopro 1", "gopro 2"],
    },
    "abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose": {
        "drive": "abs by ai | 8／14 | teleprompter ads, talking content, workout content | jeff chagrin | dan rose",
        "raw": ["."],
    },
    "abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content": {
        "drive": "abs by ai 8／28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content",
        "raw": ["main camera", "360 gopro", "regular gopro 1", "regular gopro 2"],
    },
    "dan rose fitness 9:23 shoot - vsls, long form content, short form content": {
        "drive": "dan rose fitness 9:23 shoot - vsls, long form content, short form content",
        "raw": ["."],
    },
}

SHOOT_DATES = {
    "abs by ai 7:8 Jeff Chagrin shoot": "7/8",
    "abs by ai 8:3 jeff chagrin shoot": "8/3",
    "abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose": "8/14",
    "abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content": "8/28",
    "dan rose fitness 9:23 shoot - vsls, long form content, short form content": "9/23",
}


def say(message):
    print(datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z"), message, flush=True)


def night_deadline(now):
    if now.hour < 8:
        return now.replace(hour=8, minute=0, second=0, microsecond=0)
    if now.hour >= 20:
        return (now + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
    return None


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"shoots": {}}


def save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=STATE_DIR, prefix="nightly-footage-", delete=False) as out:
        json.dump(state, out, indent=2, sort_keys=True)
        out.write("\n")
        name = out.name
    os.replace(name, STATE_FILE)


def mounted(path):
    return path.is_mount() and path.is_dir()


def archive_id():
    if not mounted(ARCHIVE):
        return None
    if DRIVE_MARKER.exists():
        return DRIVE_MARKER.read_text().strip()
    # The marker keeps a different disk named Expansion from receiving footage.
    result = subprocess.run(["diskutil", "info", "-plist", str(ARCHIVE)], capture_output=True, check=True)
    info = plistlib.loads(result.stdout)
    if int(info.get("TotalSize", 0)) < 20_000_000_000_000:
        raise RuntimeError("Expansion is smaller than the checked 24 TB Seagate")
    ident = str(uuid.uuid4())
    DRIVE_MARKER.write_text(ident + "\n")
    return ident


def eligible_shoots():
    if not mounted(SOURCE):
        return []
    known = dict(SHOOTS)
    for path in SOURCE.iterdir():
        name = path.name
        if name in known or not path.is_dir():
            continue
        low = name.lower()
        if low in {"photo shoots", "abs by ai photo shoots"}:
            continue
        if "shoot" in low and (low.startswith("abs by ai ") or low.startswith("dan rose fitness ")):
            known[name] = {"drive": name, "raw": ["."]}
    # The unbacked welcome shoot comes first, then the newest shoot. Existing
    # Drive shoots are checked after those two.
    order = list(SHOOTS)
    order.remove("dan rose fitness 9:23 shoot - vsls, long form content, short form content")
    order.insert(1, "dan rose fitness 9:23 shoot - vsls, long form content, short form content")
    return [(SOURCE / name, known[name]) for name in order + sorted(set(known) - set(SHOOTS)) if (SOURCE / name).is_dir()]


def raw_files(shoot, config):
    files = []
    for raw in config["raw"]:
        base = shoot if raw == "." else shoot / raw
        if not base.is_dir():
            continue
        for current, dirs, names in os.walk(base):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d.lower() not in SKIP_DIRS
                       and not d.lower().endswith(".roll") and not d.lower().startswith("edited")
                       and "edit" not in d.lower() and "render" not in d.lower()]
            for name in names:
                p = Path(current) / name
                if name.startswith(".") or p.suffix.lower() not in RAW_SUFFIXES or p.is_symlink():
                    continue
                files.append(p)
    return sorted(set(files))


def inventory(shoot, files):
    digest = hashlib.sha256()
    total = 0
    newest = 0
    for p in files:
        st = p.stat()
        total += st.st_size
        newest = max(newest, st.st_mtime)
        digest.update(f"{p.relative_to(shoot)}\0{st.st_size}\0{st.st_mtime_ns}\n".encode())
    return {"fingerprint": digest.hexdigest(), "files": len(files), "bytes": total, "newest": newest}


def pending_jobs(shoot):
    """Return edit queue jobs that may still need this shoot's raw footage."""
    if not QUEUE_FILE.is_file():
        return ["edit queue unavailable"]
    jobs = json.loads(QUEUE_FILE.read_text()).get("jobs", [])
    pending = []
    def date_pattern(value):
        return re.compile(r"(?<!\d)" + re.escape(value).replace("/", "[/：:／]") + r"(?!\d)", re.I)

    shoot_date = SHOOT_DATES.get(shoot.name)
    for job in jobs:
        # List 1 is the queue's raw-footage work. Lists 2 and 3 use finished
        # masters, so they do not keep a camera shoot on the working drive.
        if str(job.get("list")) != "1" or job.get("id", "").startswith("RX-"):
            continue
        if job.get("state") in {"uploaded", "finalized", "cancelled"}:
            continue
        doc = QUEUE_FILE.parent / job.get("file", "")
        content = doc.read_text(errors="ignore") if doc.is_file() else ""
        roll = job.get("roll", "")
        content += "\n" + roll + "\n" + job.get("claude", "") + "\n" + job.get("codex", "")
        # The queue's roll field names the source shoot when it contains a
        # date. Ignore incidental mentions of other shoots in production notes.
        roll_dates = {date for date in SHOOT_DATES.values() if date_pattern(date).search(roll)}
        match = shoot_date in roll_dates if roll_dates else (shoot.name in content or (shoot_date and date_pattern(shoot_date).search(content)))
        if match:
            pending.append(job.get("id", "unknown"))
    return pending


def run_command(args, deadline):
    remaining = int((deadline - datetime.now(TZ)).total_seconds()) - 60
    if remaining < 120:
        raise RuntimeError("overnight window ended; will resume tomorrow")
    say("Running " + " ".join(args[:3]))
    proc = subprocess.run(args, text=True, capture_output=True, timeout=remaining)
    if proc.returncode:
        raise RuntimeError((proc.stderr or proc.stdout)[-1800:])
    return proc.stdout


def rclone_transfer(shoot, dest, files, deadline, verify_only=False):
    with tempfile.NamedTemporaryFile("w", prefix="footage-files-", delete=False) as listing:
        for p in files:
            listing.write(str(p.relative_to(shoot)) + "\n")
        list_path = listing.name
    common = ["--files-from", list_path, "--transfers", "2", "--checkers", "4", "--tpslimit", "3", "--retries", "3"]
    try:
        if not verify_only:
            run_command([str(RCLONE), "copy", str(shoot), dest, *common], deadline)
        run_command([str(RCLONE), "check", str(shoot), dest, "--one-way", "--checksum", *common], deadline)
    finally:
        Path(list_path).unlink(missing_ok=True)


def process_shoot(shoot, config, state, deadline, dry_run):
    files = raw_files(shoot, config)
    if not files:
        return
    snapshot = inventory(shoot, files)
    name = shoot.name
    ready_file = shoot / READY_MARKER
    ready = ready_file.is_file() and time.time() - ready_file.stat().st_mtime <= READY_MAX_AGE
    waiting = pending_jobs(shoot) if ready else []
    say(f"{name}: {snapshot['files']} raw files, {snapshot['bytes'] / 1e9:.1f} GB, archive_ready={ready}")
    if ready_file.is_file() and not ready:
        say(f"{name}: archive decision is older than 24 hours; keeping the Extreme copy")
    if waiting:
        say(f"{name}: archive held for edit queue jobs: {', '.join(waiting)}")
    if dry_run:
        return
    if time.time() - snapshot["newest"] < 1800:
        say(f"{name}: waiting until newest raw file has been unchanged for 30 minutes")
        return
    record = state["shoots"].setdefault(name, {})
    if record.get("fingerprint") != snapshot["fingerprint"]:
        record.clear()
        record["fingerprint"] = snapshot["fingerprint"]
        save_state(state)
    destination = str(ARCHIVE_ROOT / name)
    seagate_id = archive_id() if ready and not waiting else None
    if seagate_id:
        if state.get("archive_id") and state["archive_id"] != seagate_id:
            raise RuntimeError("a different disk is mounted as Expansion")
        state["archive_id"] = seagate_id
        save_state(state)
        if not record.get("seagate_verified"):
            try:
                rclone_transfer(shoot, destination, files, deadline)
                record["seagate_verified"] = datetime.now(TZ).isoformat()
                save_state(state)
                say(f"{name}: Seagate checksum verified")
            except (RuntimeError, subprocess.TimeoutExpired) as exc:
                say(f"{name}: Seagate transfer will retry: {exc}")
    dest = DRIVE_ROOT + "/" + config["drive"]
    if not record.get("drive_verified"):
        rclone_transfer(shoot, dest, files, deadline)
        # Existing folders keep their existing permissions. New folders use
        # the project's anyone-with-link sharing rule.
        if config["drive"] == name:
            run_command([str(RCLONE), "link", dest], deadline)
        record["drive_verified"] = datetime.now(TZ).isoformat()
        save_state(state)
        say(f"{name}: Google Drive checksum verified")
    if not ready or waiting:
        return
    if not seagate_id or not record.get("seagate_verified"):
        say(f"{name}: Seagate absent, keeping the Extreme copy")
        return
    if pending_jobs(shoot):
        raise RuntimeError(f"{name}: edit queue changed; no files removed")
    if not ready_file.is_file() or time.time() - ready_file.stat().st_mtime > READY_MAX_AGE:
        raise RuntimeError(f"{name}: archive decision expired or was withdrawn; no files removed")
    # A prior run's success flag is not enough to remove source files. Confirm
    # both destinations again immediately before unlinking anything.
    rclone_transfer(shoot, destination, files, deadline, verify_only=True)
    rclone_transfer(shoot, dest, files, deadline, verify_only=True)
    # Recheck the source inventory so a newly copied or changed file is kept.
    if inventory(shoot, raw_files(shoot, config))["fingerprint"] != snapshot["fingerprint"]:
        raise RuntimeError(f"{name}: source changed during backup; no files removed")
    for p in files:
        p.unlink()
    record["offloaded"] = datetime.now(TZ).isoformat()
    save_state(state)
    note = shoot / "RAW_FOOTAGE_ARCHIVED.txt"
    note.write_text("Raw footage copied and checksum verified on Seagate Expansion and Google Drive.\n"
                    f"Seagate: {destination}\nGoogle Drive: {dest}\n")
    say(f"{name}: raw files removed from Extreme after both verified copies")


def install():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PLIST.parent.mkdir(parents=True, exist_ok=True)
    python = subprocess.check_output(["xcrun", "--find", "python3"], text=True).strip()
    payload = {
        "Label": LABEL,
        "ProgramArguments": [python, str(Path(__file__).resolve()), "--once"],
        "RunAtLoad": True,
        "StartCalendarInterval": {"Hour": 20, "Minute": 0},
        "StartInterval": 900,
        "StandardOutPath": str(LOG_DIR / "run.log"),
        "StandardErrorPath": str(LOG_DIR / "error.log"),
        "WorkingDirectory": str(Path(__file__).resolve().parents[2]),
    }
    PLIST.write_bytes(plistlib.dumps(payload))
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", domain + "/" + LABEL], capture_output=True)
    subprocess.run(["launchctl", "bootstrap", domain, str(PLIST)], check=True)
    say(f"Installed {LABEL}; starts at 8 pm, retries every 15 minutes, stops at 8 am Chicago time")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if args.install:
        install()
        return 0
    if args.status:
        print(json.dumps(load_state(), indent=2, sort_keys=True))
        return 0
    if not RCLONE.is_file() or not mounted(SOURCE):
        say("Extreme or rclone unavailable; will retry")
        return 1
    deadline = night_deadline(datetime.now(TZ))
    if not args.dry_run and not deadline:
        return 0
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with LOCK_FILE.open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0
        state = load_state()
        errors = 0
        for shoot, config in eligible_shoots():
            try:
                process_shoot(shoot, config, state, deadline, args.dry_run)
            except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
                errors += 1
                say(f"ERROR {shoot.name}: {exc}")
                if deadline and datetime.now(TZ) >= deadline - timedelta(minutes=2):
                    break
        return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
