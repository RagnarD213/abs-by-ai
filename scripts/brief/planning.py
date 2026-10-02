"""Incremental, project-scoped Claude desktop priority intake. No model calls."""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

CHICAGO = ZoneInfo("America/Chicago")
STATE_VERSION = 1
PLANNING_TITLE = re.compile(r"\b(?:daily priorities|prioriti[sz]e|priorities|planning|plan for|daily.*plan|sales.*plan|plan.*today|plan.*tomorrow)\b", re.I)
UUID = re.compile(r"^[0-9a-f-]{36}$", re.I)
RANK = re.compile(r"\b(?:(top|first|second|third) priority|priority\s*#?\s*([123]))\b", re.I)


def timestamp(value):
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, timezone.utc)
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo:
            return parsed.astimezone(timezone.utc)
    raise ValueError("timestamp must include a timezone")


def safe_text(value):
    """Keep short extracted task statements, without addresses or token-like strings."""
    text = re.sub(r"<[^>]+>", " ", str(value))
    text = re.sub(r"https?://\S+", "[link]", text)
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[email]", text)
    text = re.sub(r"\b(?:sk-|ghp_|github_pat_|Bearer\s+)\S+", "[redacted]", text, flags=re.I)
    text = re.sub(r"\b(?:token|secret|password|api[_ -]?key)\s*[:=]\s*\S+", "[redacted]", text, flags=re.I)
    return " ".join(text.replace("\u2014", ", ").replace("\u2013", " ").split())[:350]


def extract_priorities(text, at, now, max_age_hours=36, defer_day_scope=False):
    """Conservative extraction of explicit ranks; never rank an assistant's advice."""
    at = timestamp(at)
    if at > now + timedelta(minutes=5) or now - at > timedelta(hours=max_age_hours):
        return []
    text = re.sub(r"<[^>]+>", " ", text)
    local_day = at.astimezone(CHICAGO).date()
    applies = None
    day_word = re.search(r"\b(today|tomorrow)\b", text, re.I)
    if day_word and day_word[1].lower() == "tomorrow":
        applies = str(local_day + timedelta(days=1))
    elif day_word:
        applies = str(local_day)
    if not defer_day_scope and applies and applies != str(now.astimezone(CHICAGO).date()):
        return []
    priorities = []
    # Sentence boundaries preserve a preceding task followed by "That's top priority".
    for paragraph in re.split(r"\n+", text):
        previous = ""
        for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
            hit = RANK.search(sentence)
            if hit:
                if sentence.rstrip().endswith("?") or re.search(r"\b(?:not|isn't|isn’t)\b.{0,25}$", sentence[:hit.start()], re.I):
                    previous = sentence
                    continue
                rank = {"top": 1, "first": 1, "second": 2, "third": 3}.get((hit[1] or "").lower(), int(hit[2] or 1))
                if re.match(r"\s*(?:that|this|it)['’]?(?:s| is)?\b", sentence, re.I) and previous:
                    task = previous
                else:
                    task = sentence
                    task = re.sub(r"^\s*(?:(?:today|tomorrow)[, ]+)?(?:my\s+)?(?:top|first|second|third) priority\s*(?:is|:)\s*(?:to\s+)?", "", task, flags=re.I)
                    task = re.sub(r"\s*[,;:]?\s*(?:that\s+is\s+)?(?:definitely\s+)?(?:the\s+)?(?:top|first|second|third) priority[.!]?\s*$", "", task, flags=re.I)
                task = safe_text(task.strip(" *-\t"))
                if task:
                    priorities.append({"rank": rank, "task": task, "statedAt": at.isoformat(), "applicableDate": applies})
            previous = sentence
    # Preserve the first explicit task for each rank. Later clarification of
    # that same rank must not create a second "do this first" item.
    by_rank = {}
    for priority in priorities:
        by_rank.setdefault(priority["rank"], priority)
    return sorted(by_rank.values(), key=lambda p: p["rank"])


def read_planning(metadata_root: Path, transcript_root: Path, project_root: Path,
                  state: dict, now: datetime, max_age_hours=36, session_ids=()):
    """State contains offsets, UUID ancestry and extracted priorities, never transcripts."""
    if not metadata_root.is_dir() or not transcript_root.is_dir():
        return {"status": "missing", "reason": "Claude desktop session directories unavailable", "priorities": []}, state
    if state.get("parserVersion") != STATE_VERSION:
        state = {"parserVersion": STATE_VERSION, "files": {}}
    cache = state.setdefault("files", {})
    selected, warnings, examined, bytes_read = [], [], 0, 0
    try:
        metadata_files = list(metadata_root.glob("*/*/local_*.json"))
        for file in metadata_files:
            if file.is_symlink():
                continue
            try:
                meta = json.loads(file.read_text())
                if not isinstance(meta, dict):
                    raise ValueError()
                # Exact project match before considering title or transcript contents.
                if str(project_root) not in (meta.get("cwd"), meta.get("originCwd")):
                    continue
                if not PLANNING_TITLE.search(meta.get("title", "")) and meta.get("sessionId") not in session_ids:
                    continue
                last = timestamp(meta.get("lastActivityAt"))
                if now - last > timedelta(hours=max_age_hours):
                    continue
                cli_id = meta.get("cliSessionId", "")
                if not UUID.fullmatch(cli_id):
                    raise ValueError()
                transcript = transcript_root / (cli_id + ".jsonl")
                if not transcript.is_file() or transcript.is_symlink():
                    warnings.append("Planning transcript unavailable")
                    continue
                examined += 1
                stat = transcript.stat()
                entry = cache.get(cli_id, {})
                # Replaced/truncated files require a fresh pass, even at the same size.
                if entry.get("inode") != stat.st_ino or stat.st_size < entry.get("offset", 0):
                    entry = {}
                if stat.st_size == entry.get("offset") and stat.st_mtime_ns != entry.get("mtimeNs"):
                    entry = {}
                entry.setdefault("offset", 0)
                parents = entry.setdefault("parents", {})
                candidates = entry.setdefault("candidates", {})
                malformed = False
                with transcript.open("rb") as stream:
                    stream.seek(entry["offset"])
                    while True:
                        start = stream.tell()
                        line = stream.readline()
                        if not line or not line.endswith(b"\n"):
                            entry["offset"] = start  # Retry a partially appended line next run.
                            break
                        bytes_read += len(line)
                        entry["offset"] = stream.tell()
                        try:
                            row = json.loads(line)
                        except (ValueError, UnicodeError):
                            malformed = True
                            continue
                        if not isinstance(row, dict):
                            malformed = True
                            continue
                        if row.get("isSidechain"):
                            continue
                        uid = row.get("uuid")
                        if not uid:
                            continue
                        parents[uid] = row.get("parentUuid")
                        # Attachments/system records can connect conversation UUIDs.
                        # Keep their ancestry, without reading or retaining content.
                        if row.get("type") in ("user", "assistant"):
                            entry["leaf"] = uid
                        if row.get("type") != "user" or (row.get("origin") or {}).get("kind") != "human" or row.get("entrypoint") != "claude-desktop":
                            continue
                        if row.get("cwd") != str(project_root):
                            continue
                        content = row.get("message", {}).get("content", "")
                        if isinstance(content, list):
                            content = "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
                        if not isinstance(content, str):
                            continue
                        try:
                            priorities = extract_priorities(content, row.get("timestamp"), now, max_age_hours, defer_day_scope=True)
                        except (ValueError, TypeError, OverflowError):
                            malformed = True
                            continue
                        if priorities:
                            candidates[uid] = priorities
                entry.update(inode=stat.st_ino, mtimeNs=stat.st_mtime_ns)
                cache[cli_id] = entry
                if malformed:
                    warnings.append("Malformed transcript records skipped")
                leaf = meta.get("lastAssistantUuid")
                if leaf not in parents:
                    leaf = entry.get("leaf")
                else:
                    # A newly submitted human frame can follow the last assistant
                    # before desktop metadata records another assistant response.
                    newer = entry.get("leaf")
                    visited = set()
                    while newer and newer not in visited and newer != leaf:
                        visited.add(newer)
                        newer = parents.get(newer)
                    if newer == leaf:
                        leaf = entry.get("leaf")
                ancestry = set()
                while leaf and leaf not in ancestry:
                    ancestry.add(leaf)
                    leaf = parents.get(leaf)
                for uid, priorities in candidates.items():
                    if uid not in ancestry:
                        continue
                    for priority in priorities:
                        at = timestamp(priority["statedAt"])
                        if at > now + timedelta(minutes=5) or now - at > timedelta(hours=max_age_hours):
                            continue
                        if priority["applicableDate"] not in (None, str(now.astimezone(CHICAGO).date())):
                            continue
                        selected.append({**priority, "sessionId": meta["sessionId"], "messageId": uid})
            except (OSError, ValueError, TypeError, KeyError, AttributeError):
                warnings.append("A session metadata or transcript record could not be read")
    except OSError:
        return {"status": "error", "reason": "Claude desktop metadata could not be read", "priorities": []}, state
    # The latest explicit priority message wins; later chat without ranks does not.
    latest = max((p["statedAt"] for p in selected), default=None)
    priorities = sorted([p for p in selected if p["statedAt"] == latest], key=lambda p: p["rank"])
    result = {"status": "partial" if warnings else ("ok" if priorities else "no_current_plan"),
              "priorities": priorities, "sessionsExamined": examined, "bytesRead": bytes_read,
              "warnings": sorted(set(warnings)), "maxAgeHours": max_age_hours}
    return result, state
