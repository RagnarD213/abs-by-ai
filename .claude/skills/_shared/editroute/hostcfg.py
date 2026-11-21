"""Per-Mac numbers from hosts.json, for editcap.py (edit slots), renderq.py (cores) and editroute.py.

Everything here fails open: on any error it returns None and the caller keeps its old default (5 slots, all cores
but 2), so a broken config file never stops an edit. Handoff 03 (two-Mac edit routing), 2026-11-14.

Overrides for tests: EDITROUTE_HOSTS (another hosts.json), EDITROUTE_HOST (pretend to be this Mac),
EDITROUTE_IDLE_S (seconds since Dan last touched the keyboard or mouse), EDITROUTE_HOUR (the clock hour).
"""
import datetime as dt
import json
import os
import re
import socket
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDLE_CACHE = Path(os.environ.get("EDITROUTE_IDLE_CACHE") or "/tmp/absbyai-editroute-idle.json")
IDLE_CACHE_S = 15.0
# /away (Dan, 2026-11-15): "I am leaving now" switch, so the away core budget starts at once instead of after 30 min idle.
AWAY_FILE = Path(os.environ.get("EDITROUTE_AWAY_FILE") or Path.home() / ".absbyai-away.json")
AWAY_GRACE_S = 120.0                                  # time to walk away after typing /away before input cancels it
_cfg = [None, None]                                   # (mtime, parsed)


def config_path():
    return Path(os.environ.get("EDITROUTE_HOSTS") or HERE / "hosts.json")


def load():
    """The parsed hosts.json, or {} when it is missing or broken."""
    p = config_path()
    try:
        m = p.stat().st_mtime
        if _cfg[0] != (str(p), m):
            _cfg[0], _cfg[1] = (str(p), m), json.loads(p.read_text())
        return _cfg[1] or {}
    except (OSError, ValueError):
        return {}


def _local_names():
    out = []
    try:
        out.append(socket.gethostname().split(".")[0])
    except OSError:
        pass
    try:
        r = subprocess.run(["scutil", "--get", "LocalHostName"], capture_output=True, text=True, timeout=2)
        if r.returncode == 0:
            out.append(r.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return [n for n in out if n]


def this_host(cfg=None):
    """'m6', 'm2', or None on a Mac hosts.json does not know."""
    cfg = load() if cfg is None else cfg
    hosts = cfg.get("hosts") or {}
    forced = os.environ.get("EDITROUTE_HOST")
    if forced:
        return forced if forced in hosts else None
    names = [n.lower() for n in _local_names()]
    for key, h in hosts.items():
        if key.lower() in names or any(n.lower() in names for n in h.get("names", ())):
            return key
    return None


def host(name=None, cfg=None):
    cfg = load() if cfg is None else cfg
    name = name or this_host(cfg)
    return (cfg.get("hosts") or {}).get(name) if name else None


def slots(name=None):
    """Edit slots on this Mac (EDITCAP_MAX), or None."""
    h = host(name)
    try:
        return int(h["slots"]) if h and h.get("slots") else None
    except (TypeError, ValueError):
        return None


def idle_seconds():
    """Seconds since the last keyboard or mouse input on this Mac (ioreg IOHIDSystem HIDIdleTime), or None."""
    if os.environ.get("EDITROUTE_IDLE_S"):
        return float(os.environ["EDITROUTE_IDLE_S"])
    now = time.time()
    try:
        c = json.loads(IDLE_CACHE.read_text())
        if now - c["t"] < IDLE_CACHE_S:
            return c["idle"] + (now - c["t"])
    except (OSError, ValueError, KeyError, TypeError):
        pass
    try:
        r = subprocess.run(["/usr/sbin/ioreg", "-c", "IOHIDSystem", "-d", "4"], capture_output=True, text=True,
                           timeout=3)
        m = re.search(r'"HIDIdleTime"\s*=\s*(\d+)', r.stdout)
        if not m:
            return None
        idle = int(m.group(1)) / 1e9
    except (OSError, subprocess.SubprocessError, ValueError):
        return None
    try:
        tmp = IDLE_CACHE.with_name(IDLE_CACHE.name + ".{}".format(os.getpid()))
        tmp.write_text(json.dumps({"t": now, "idle": idle}))
        os.replace(str(tmp), str(IDLE_CACHE))
        os.chmod(str(IDLE_CACHE), 0o666)
    except OSError:
        pass
    return idle


def is_night(h, hour=None):
    if hour is None:
        hour = int(os.environ["EDITROUTE_HOUR"]) if os.environ.get("EDITROUTE_HOUR") else dt.datetime.now().hour
    start, end = (h.get("night") or [22, 7])[:2]
    return hour >= start or hour < end if start > end else start <= hour < end


def away_set(hours=8.0):
    """Dan says he is leaving: away budget from now until he touches the Mac again (after the grace) or `hours` pass."""
    now = time.time()
    d = {"t": now, "until": now + float(hours) * 3600, "grace_s": AWAY_GRACE_S}
    tmp = AWAY_FILE.with_name(AWAY_FILE.name + ".{}".format(os.getpid()))
    tmp.write_text(json.dumps(d))
    os.replace(str(tmp), str(AWAY_FILE))
    return d


def away_clear():
    try:
        AWAY_FILE.unlink()
        return True
    except OSError:
        return False


def away_override(idle=None):
    """(True, why) while Dan's /away switch holds. It ends, and removes itself, when its time is up or when the
    keyboard or mouse is used after the grace period: he is back, so the Mac goes back to the present budget."""
    try:
        d = json.loads(AWAY_FILE.read_text())
        t, until, grace = float(d["t"]), float(d["until"]), float(d.get("grace_s", AWAY_GRACE_S))
    except (OSError, ValueError, KeyError, TypeError):
        return False, ""
    now = time.time()
    if now >= until:
        away_clear()
        return False, ""
    since_grace = now - (t + grace)
    if since_grace > 0:
        if idle is None:
            idle = idle_seconds()
        if idle is not None and idle < since_grace - IDLE_CACHE_S:    # input after the grace (cache can lag 15 s)
            away_clear()
            return False, ""
    return True, "Dan said he is away ({} min ago, up to {:.1f} h more)".format(int((now - t) // 60), (until - now) / 3600)


def presence(name=None, hour=None, idle=None):
    """('away' | 'present', why). Away = Dan has not touched this Mac for away_after_min minutes, or it is night."""
    h = host(name)
    if not h:
        return "present", "unknown Mac"
    if idle is None:
        idle = idle_seconds()
    ok, why = away_override(idle)
    if ok:
        return "away", why
    limit = float(h.get("away_after_min") or 30) * 60
    if idle is None:
        return "present", "idle time unknown, assuming Dan is here"
    if idle >= limit:
        return "away", "no keyboard or mouse for {} min".format(int(idle // 60))
    return "present", "keyboard or mouse used {} min ago".format(int(idle // 60))


def core_budget(name=None, hour=None, idle=None):
    """Cores the render queue may hand out on this Mac now, or None (caller keeps its own default)."""
    h = host(name)
    if not h:
        return None
    try:
        present, away = int(h["cores_present"]), int(h.get("cores_away") or h["cores_present"])
    except (KeyError, TypeError, ValueError):
        return None
    if present == away:
        return max(2, present)
    state, _ = presence(name, hour, idle)
    return max(2, away if state == "away" else present)


def work_before_internal(name=None):
    """Work drives that come before this Mac's internal SSD for a NEW job folder (M2: the Extreme)."""
    h = host(name)
    return list(h.get("work_before_internal") or []) if h else []
