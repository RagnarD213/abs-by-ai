#!/usr/bin/env python3
"""Collect private morning-brief inputs. Never commit data, publish, or schedule."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, time, timedelta, timezone
from pathlib import Path

from planning import CHICAGO, read_planning, safe_text, timestamp

CODE_ROOT = Path(__file__).resolve().parents[2]
METRICS = ("free_generations", "email_leads", "trials", "paid")
SITES = ("absbyai.com", "sixpackabs.com")
# These existing browser events do not prove the requested business outcome.
UNVERIFIED_EVENTS = {
    "free_generations": {"generation_started", "generation_verifier", "generation_locked_in"},
    "email_leads": {"email_subscribed", "newsletter_signup", "account_signup"},
    "trials": {"trial_signup_started", "membership_subscribed", "iap_purchase_completed"},
    "paid": {"paid_conversion_reported", "membership_subscribed", "iap_purchase_completed", "purchase_completed"},
}


def secrets(path):
    values = dict(os.environ)
    if path.exists():
        for line in path.read_text().splitlines():
            key, sep, value = line.strip().partition("=")
            if sep and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", key) and key not in values:
                values[key] = value.strip().strip("\"'")
    return values


def redact(value, credentials):
    """Final defense for stored data; HTTP/provider error bodies are never retained."""
    secret_values = [v for k, v in credentials.items() if re.search(r"KEY|TOKEN|SECRET|PASSWORD|DATABASE.*URL", k) and len(v) >= 8]
    def clean(item):
        if isinstance(item, dict):
            return {k: clean(v) for k, v in item.items() if not re.search(r"^(?:authorization|password|access_token|refresh_token|api_key|secret)$", k, re.I)}
        if isinstance(item, list):
            return [clean(v) for v in item]
        if isinstance(item, str):
            for secret in secret_values:
                item = item.replace(secret, "[redacted]")
            return item
        return item
    return clean(value)


def private_directory(path):
    path = path.expanduser().resolve()
    for parent in (path, *path.parents):
        if (parent / ".git").exists():
            raise ValueError("Private state/output must be outside every Git checkout")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path, 0o700)
    return path


def write_private(path, value):
    fd, name = tempfile.mkstemp(prefix=".brief-", dir=str(path.parent))
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def snapshot(path, now, max_age_hours, date_field="generatedAt"):
    if not path.is_file():
        return {"status": "missing", "reason": "Source file unavailable"}
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            raise ValueError()
        source_date = data[date_field]
        if date_field == "last_run" and isinstance(source_date, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", source_date):
            today = str(now.astimezone(CHICAGO).date())
            if source_date != today:
                return {"status": "stale" if source_date < today else "error", "sourceDate": source_date,
                        "reason": "Editor run has date-only precision and is not today"}
            return {"status": "ok", "sourceAt": source_date, "precision": "date", "data": data}
        at = timestamp(source_date)
        age = (now - at).total_seconds() / 3600
        if age < -5 / 60:
            return {"status": "error", "reason": "Source timestamp is in the future"}
        if age > max_age_hours:
            return {"status": "stale", "sourceAt": at.isoformat(), "ageHours": round(age, 2)}
        return {"status": "ok", "sourceAt": at.isoformat(), "data": data}
    except (OSError, ValueError, KeyError, TypeError, OverflowError):
        return {"status": "error", "reason": "Source JSON or timestamp is invalid"}


def select_trello(data, now):
    """A private read-only export adapter until the board IDs/connector are available."""
    if data.get("status") != "ok":
        return data
    try:
        lists = data["data"]["lists"]
        out = {}
        for name in ("dan_in_progress", "dan_queue"):
            cards = lists[name]
            if not isinstance(cards, list):
                raise ValueError()
            normalized = []
            for card in cards:
                if not isinstance(card.get("title"), str) or not card["title"].strip() or type(card.get("position")) not in (int, float) or not math.isfinite(card["position"]) or not card.get("id"):
                    raise ValueError()
                normalized.append({"id": str(card["id"]), "title": safe_text(card["title"]), "position": card["position"]})
            out[name] = sorted(normalized, key=lambda c: c["position"])
        return {"status": "ok", "sourceAt": data["sourceAt"], "lists": out}
    except (KeyError, ValueError, TypeError, AttributeError):
        return {"status": "error", "reason": "Trello export schema invalid; no priority inferred"}


def select_priority(planning, trello):
    if planning.get("priorities"):
        first = min(planning["priorities"], key=lambda p: p["rank"])
        return {"status": "ok", "source": "claude_explicit_plan", **first}
    if trello.get("status") == "ok":
        for name in ("dan_in_progress", "dan_queue"):
            if trello["lists"][name]:
                card = trello["lists"][name][0]
                return {"status": "ok", "source": name, "task": card["title"], "cardId": card["id"]}
        return {"status": "empty", "reason": "Daniel's ranked lists are verified empty"}
    return {"status": "missing", "reason": "No applicable explicit plan and no fresh ranked Trello input"}


def legacy_plan(path, now):
    result = snapshot(path, now, 36, "writtenAt")
    if result.get("status") != "ok":
        return result
    data = result.pop("data")
    if data.get("forDate") != str(now.astimezone(CHICAGO).date()):
        return {"status": "stale", "reason": "Legacy plan is not for today's Chicago date"}
    if not isinstance(data.get("oneThing"), str):
        return {"status": "error", "reason": "Legacy plan schema invalid"}
    return {"status": "ok", "sourceAt": result["sourceAt"], "supportingOnly": True,
            "oneThing": safe_text(data["oneThing"])}


def request_json(url, headers, payload=None):
    encoded = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=encoded, headers=headers, method="POST" if encoded else "GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            if "json" not in response.headers.get("Content-Type", "").lower():
                return {"status": "error", "reason": "Expected JSON; received a different response type"}
            return {"status": "ok", "data": json.load(response)}
    except urllib.error.HTTPError as exc:
        return {"status": "error", "reason": "HTTP read failed", "httpStatus": exc.code}
    except (OSError, ValueError):
        return {"status": "error", "reason": "Network read or JSON decoding failed"}


def dashboard(credentials):
    key = credentials.get("DASH_SECRET")
    if not key:
        return {"status": "missing", "reason": "Dashboard credential unavailable"}
    output = {}
    for name in ("todos", "task-checks"):
        result = request_json("https://absbyai.com/api/" + name, {"X-Dash-Key": key})
        if result["status"] == "ok":
            data = result["data"]
            valid = isinstance(data, dict) and (isinstance(data.get("business"), list) if name == "todos" else isinstance(data.get("checked"), list) and isinstance(data.get("log"), dict))
            if not valid:
                result = {"status": "error", "reason": "Dashboard response schema invalid"}
            elif name == "todos":
                # This supports follow-up facts; it never outranks planning/Trello.
                result["data"] = {k: data.get(k, []) for k in ("business", "handoffs", "assistant")}
        output[name] = result
    return {"status": "ok" if all(x["status"] == "ok" for x in output.values()) else "partial", "reads": output}


def windows(now):
    today = now.astimezone(CHICAGO).date()
    day = today - timedelta(days=1)
    def span(date):
        start = datetime.combine(date, time(), CHICAGO).astimezone(timezone.utc)
        end = datetime.combine(date + timedelta(days=1), time(), CHICAGO).astimezone(timezone.utc)
        return {"from": start.isoformat(), "toExclusive": end.isoformat()}
    return {"day": str(day), "weekFrom": str(day - timedelta(days=6)),
            "yesterday": span(day), "sameWeekdayLastWeek": span(day - timedelta(days=7))}


def posthog(credentials, config, window):
    key = credentials.get("POSTHOG_PERSONAL_KEY") or credentials.get("POSTHOG_API_KEY")
    project = str(credentials.get("POSTHOG_PROJECT_ID") or "458833")
    if not key or not project.isdigit():
        return {"status": "missing", "reason": "PostHog query credential/project unavailable"}
    mapping = config.get("site_events", {})
    if not isinstance(mapping, dict):
        return {"status": "error", "reason": "Invalid site event mapping"}
    for site, fields in mapping.items():
        if site not in SITES or not isinstance(fields, dict):
            return {"status": "error", "reason": "Invalid site event mapping"}
        for metric, event in fields.items():
            if metric not in METRICS or not isinstance(event, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", event):
                return {"status": "error", "reason": "Invalid site event mapping"}
            if event in UNVERIFIED_EVENTS[metric]:
                return {"status": "error", "reason": "Existing browser event does not verify this business outcome; use a precise stage signal or verified aggregate"}
        if len(set(fields.values())) != len(fields):
            return {"status": "error", "reason": "Site outcomes must map to distinct events"}
    output = {}
    for name in ("yesterday", "sameWeekdayLastWeek"):
        span = window[name]
        # Aggregates only: no person IDs, email addresses, URLs, or event payloads.
        host = "lower(coalesce(properties.$host, domain(properties.$current_url)))"
        query = "SELECT if(" + host + " IN ('absbyai.com', 'www.absbyai.com'), 'absbyai.com', 'sixpackabs.com') AS site, event, count(), uniq(person_id) FROM events WHERE timestamp >= '" + span["from"] + "' AND timestamp < '" + span["toExclusive"] + "' AND " + host + " IN ('absbyai.com', 'www.absbyai.com', 'sixpackabs.com', 'www.sixpackabs.com') GROUP BY site, event"
        result = request_json(f"https://us.posthog.com/api/projects/{project}/query", {"Authorization": "Bearer " + key, "Content-Type": "application/json"}, {"query": {"kind": "HogQLQuery", "query": query}})
        if result["status"] != "ok":
            output[name] = result
            continue
        try:
            rows = result["data"]["results"]
            if not isinstance(rows, list):
                raise ValueError()
            sites = {}
            for site in SITES:
                grouped = {}
                for row in rows:
                    if len(row) != 4 or not isinstance(row[0], str) or not isinstance(row[1], str) or not isinstance(row[2], (int, float)) or not isinstance(row[3], (int, float)):
                        raise ValueError()
                    if row[0].removeprefix("www.") == site:
                        grouped.setdefault(row[1], {"events": 0, "uniques": 0})
                        grouped[row[1]]["events"] += row[2]
                        grouped[row[1]]["uniques"] += row[3]
                pageviews = grouped.get("$pageview")
                sites[site] = {"visitors": {"status": "observed" if pageviews else "not_observed", "value": pageviews["uniques"] if pageviews else None,
                                           "definition": "Unique pageview persons per site, grouping www/non-www together"},
                               "observedEvents": grouped}
                for metric in METRICS:
                    event = mapping.get(site, {}).get(metric)
                    sites[site][metric] = {"status": "mapped" if event else "unmapped", "value": grouped.get(event, {}).get("events", 0) if event else None, "event": event}
            output[name] = {"status": "ok", "sites": sites}
        except (KeyError, TypeError, ValueError, AttributeError):
            output[name] = {"status": "error", "reason": "PostHog result schema invalid"}
    return {"status": "partial" if any(r["status"] != "ok" for r in output.values()) or any(set(mapping.get(s, {})) != set(METRICS) for s in SITES) else "ok", "windows": output}


def run_ads(config, window, credentials):
    if not all(credentials.get(key) for key in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_ADS_REFRESH_TOKEN")):
        return {"status": "missing", "reason": "Existing Google Ads read credentials unavailable"}
    try:
        process = subprocess.run(["node", str(CODE_ROOT / "scripts/brief/ads_stats.js"), window["day"], window["weekFrom"]], input=json.dumps(config.get("google_ads", {})), capture_output=True, text=True, timeout=100, env=credentials)
        result = json.loads(process.stdout)
        if not isinstance(result, dict) or result.get("status") not in ("ok", "partial", "error"):
            raise ValueError()
        return result
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return {"status": "error", "reason": "Google Ads reader unavailable, timed out, or returned invalid output"}


def subscriber_leads(project, window, credentials):
    try:
        p = subprocess.run(["node", str(CODE_ROOT / "scripts/brief/subscriber_leads.js"), str(project)],
                           input=json.dumps(window), capture_output=True, text=True, timeout=35, env=credentials)
        result = json.loads(p.stdout)
        if not isinstance(result, dict) or result.get("status") not in ("ok", "missing", "error"):
            raise ValueError()
        if result["status"] == "ok":
            for name in ("yesterday", "sameWeekdayLastWeek"):
                data = result["windows"][name]
                counts = [data["unattributed"], *(data["sites"][s]["value"] for s in SITES)]
                if any(type(n) is not int or n < 0 for n in counts):
                    raise ValueError()
        return result
    except (OSError, ValueError, TypeError, KeyError, subprocess.TimeoutExpired):
        return {"status": "error", "reason": "Subscriber aggregate unavailable; no zero inferred"}


def merge_verified_leads(sites, leads):
    if leads.get("status") != "ok":
        return
    for name, data in sites.get("windows", {}).items():
        if data.get("status") == "ok":
            for site in SITES:
                data["sites"][site]["email_leads"] = {**leads["windows"][name]["sites"][site], "source": "subscribers.subscribed_at"}
            data["unattributedEmailLeads"] = leads["windows"][name]["unattributed"]


def ad_guard(project_root):
    script = project_root / "scripts/blotato/ad_guard.py"
    if not script.is_file():
        return {"status": "missing", "reason": "Organic-ad guard unavailable"}
    try:
        p = subprocess.run([sys.executable, str(script), "--scan"], capture_output=True, text=True, timeout=45, cwd=str(project_root), env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        ids = re.findall(r"AD IN QUEUE\s+schedule\s+(\d+)\b", p.stdout)
        scanned = re.search(r"scanned (\d+) scheduled posts", p.stdout)
        if p.returncode == 0 and scanned and "CLEAN" in p.stdout and not ids:
            return {"status": "ok", "result": "clean", "scanned": int(scanned[1]), "hits": []}
        if p.returncode == 1 and ids and scanned:
            return {"status": "ok", "result": "hits", "scanned": int(scanned[1]), "hits": [{"scheduleId": sid} for sid in ids]}
        return {"status": "error", "reason": "Organic-ad scan failed; no clean result inferred"}
    except (OSError, subprocess.TimeoutExpired):
        return {"status": "error", "reason": "Organic-ad scan unavailable or timed out"}


def collect(args):
    now = timestamp(args.now) if args.now else datetime.now(timezone.utc)
    state_dir = private_directory(Path(args.state_dir))
    config = json.loads(Path(args.config).read_text()) if args.config else {}
    if not isinstance(config, dict):
        raise ValueError("Config must be a JSON object")
    project = Path(args.project_root).expanduser().resolve()
    credentials = secrets(Path(args.secrets_file).expanduser())
    try:
        state = json.loads((state_dir / "planning-state.json").read_text())
        if not isinstance(state, dict) or not isinstance(state.get("files", {}), dict):
            raise ValueError()
    except (FileNotFoundError, ValueError):
        state = {}
    metadata = Path(config.get("claude_metadata_root", str(Path.home() / "Library/Application Support/Claude/claude-code-sessions")))
    transcript = Path(config.get("claude_transcript_root", str(Path.home() / ".claude/projects" / ("-" + str(project).strip("/").replace("/", "-").replace(" ", "-")))))
    planning, state = read_planning(metadata, transcript, project, state, now, session_ids=config.get("planning_session_ids", []))
    trello_path = Path(config.get("trello_snapshot", str(state_dir / "trello.json"))).expanduser()
    trello = select_trello(snapshot(trello_path, now, 24), now)
    sources = {"planning": planning, "trello": trello}
    queue_path = Path(config.get("social_queue_snapshot", str(state_dir / "social-queue.json"))).expanduser()
    sources["social_release_queue"] = snapshot(queue_path, now, 12, "checkedAt")
    sources["legacy_next_day_plan"] = legacy_plan(Path.home() / ".claude/scheduled-tasks/abs-by-ai-morning-brief/next-day-plan.json", now)
    window = windows(now)
    sources["editor_deliveries"] = snapshot(project / ".claude/skills/editor-deliveries/state.json", now, 30, "last_run")
    # A date-only editor run is usable only on that same local date.
    sources["watch_review"] = snapshot(Path.home() / ".absbyai-watch-review/brief-feed.json", now, 8 * 24)
    if sources["watch_review"].get("status") == "ok":
        data = sources["watch_review"].pop("data")
        sources["watch_review"]["watch"] = [{k: safe_text(row.get(k, "")) for k in ("title", "why")} for row in data.get("watch", [])[:2]]
        sources["watch_review"]["actions"] = [{k: safe_text(row.get(k, "")) for k in ("act", "why")} for row in data.get("actions", [])[:2]]
    if args.live:
        sources.update(dashboard=dashboard(credentials), google_ads=run_ads(config, window, credentials), sites=posthog(credentials, config, window), ad_guard=ad_guard(project))
        sources["subscriber_leads"] = subscriber_leads(project, window, credentials)
        merge_verified_leads(sources["sites"], sources["subscriber_leads"])
    else:
        for name in ("dashboard", "google_ads", "sites", "ad_guard", "subscriber_leads"):
            sources[name] = {"status": "not_checked", "reason": "Network reads require --live"}
    for name in ("gmail", "calendar"):
        sources[name] = {"status": "missing", "reason": "Local intake not configured; the brief writer can use its separately connected source"}
    result = {"schemaVersion": 1, "generatedAt": now.isoformat(), "forDate": str(now.astimezone(CHICAGO).date()),
              "timezone": "America/Chicago", "routineEnabled": False, "window": window,
              "priority": select_priority(planning, trello), "sources": sources}
    result = redact(result, credentials)
    write_private(state_dir / "planning-state.json", redact(state, credentials))
    write_private(state_dir / "brief-inputs.json", result)
    return state_dir, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", default=str(Path.home() / ".absbyai-brief"))
    parser.add_argument("--project-root", default=str(Path.home() / "Documents/Claude/Projects/Abs By AI"))
    parser.add_argument("--secrets-file", default=str(Path.home() / ".absbyai-secrets.env"))
    parser.add_argument("--config", help="Optional private JSON mapping/config file")
    parser.add_argument("--live", action="store_true", help="Allow only read-only HTTP/analytics/queue queries")
    parser.add_argument("--now", help="Timezone-aware ISO time for reproducible collection")
    args = parser.parse_args()
    try:
        path, result = collect(args)
    except (OSError, ValueError, TypeError):
        print("Collection failed: config, credentials file access, clock, or private output location needs verification", file=sys.stderr)
        return 1
    # Safe operational summary only. Private source data is never printed.
    print(json.dumps({"output": str(path / "brief-inputs.json"), "forDate": result["forDate"],
                      "prioritySource": result["priority"].get("source"),
                      "sourceStatuses": {name: value["status"] for name, value in result["sources"].items()},
                      "routineEnabled": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
