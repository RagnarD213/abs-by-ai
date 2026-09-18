#!/usr/bin/env python3
"""Queue-owned schema-1 asset approval packets.

`placeholders.json` is the durable authority for the queue's two-stage edit flow.  This
module is deliberately stdlib-only so the queue, review page and delivery gate all read
the same packet rules instead of growing three slightly different JSON validators.

The public helpers raise PacketError on an unsafe or stale packet.  All writes are
locked, fsynced and atomically replaced.
"""
import argparse
import contextlib
import copy
import datetime
import fcntl
import hashlib
import json
import os
import re
import tempfile

SCHEMA_VERSION = 1
PACKET_NAME = "placeholders.json"
MAX_GENERATION_BUDGET_USD = 5.0
ALLOWED_TYPES = {"ai_motion", "stock", "existing_broll"}
ALLOWED_APPROVALS = {"pending", "approved", "rejected"}
ALLOWED_STATUSES = {"approval_required", "approved", "complete"}
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")


class PacketError(ValueError):
    pass


def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _inside(path, root):
    path, root = os.path.realpath(path), os.path.realpath(root)
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def _roots(workdir, allowed_roots=()):
    roots = [os.path.realpath(workdir)]
    for root in allowed_roots or ():
        if not root:
            continue
        root = os.path.abspath(os.path.expanduser(root))
        if root not in roots:
            roots.append(root)
    return roots


def _safe_path(path, workdir, allowed_roots):
    if not isinstance(path, str) or not os.path.isabs(path):
        raise PacketError(f"packet path must be absolute: {path!r}")
    if not any(_inside(path, root) for root in _roots(workdir, allowed_roots)):
        raise PacketError(f"packet path escapes the job work directory and allowlisted roots: {path}")
    return os.path.realpath(path)


def _file_record(record, label, workdir, allowed_roots, required=True, verify_hashes=True):
    if record is None and not required:
        return None
    if not isinstance(record, dict):
        raise PacketError(f"{label} must be a {{path, sha256}} record")
    path = _safe_path(record.get("path"), workdir, allowed_roots)
    expected = record.get("sha256")
    if not re.fullmatch(r"[0-9a-f]{64}", str(expected or "")):
        raise PacketError(f"{label}.sha256 must be a lowercase SHA-256")
    if not os.path.isfile(path):
        raise PacketError(f"{label} is missing: {path}")
    if verify_hashes:
        actual = sha256(path)
        if actual != expected:
            raise PacketError(f"{label} changed: expected {expected[:12]}, got {actual[:12]}")
    return path


def _num(value, label, minimum=None):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise PacketError(f"{label} must be a number")
    value = float(value)
    if minimum is not None and value < minimum:
        raise PacketError(f"{label} must be at least {minimum}")
    return value


def _texts(value, label, required=False):
    if value is None:
        value = []
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise PacketError(f"{label} must be a list of non-empty strings")
    if required and not value:
        raise PacketError(f"{label} must name at least one affected scene/join")
    if len(value) != len(set(value)):
        raise PacketError(f"{label} contains duplicates")
    return value


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def selection_material(item):
    """The fields whose material change invalidates this item's approval."""
    base = {
        "id": item.get("id"), "type": item.get("type"), "in": item.get("in"),
        "out": item.get("out"), "duration": item.get("duration"),
        "spoken_beat": item.get("spoken_beat"), "intended_action": item.get("intended_action"),
        "estimated_usd": item.get("estimated_usd", 0),
        "reuse_status": item.get("reuse_status", "new"),
        "affected_scenes": item.get("affected_scenes") or [],
        "boundary_joins": item.get("boundary_joins") or [],
    }
    if item.get("type") == "ai_motion":
        base.update(start_frame=item.get("start_frame"), end_frame=item.get("end_frame"))
    else:
        base.update(preview=item.get("preview"), source=item.get("source"))
    return base


def selection_fingerprint(item):
    return hashlib.sha256(_canonical(selection_material(item)).encode()).hexdigest()


def packet_material_fingerprint(packet):
    """Stable across Dan's decisions; changes when the draft or any proposed choice changes."""
    value = {"schema_version": packet.get("schema_version"), "video_id": packet.get("video_id"),
             "revision": packet.get("revision"), "draft": packet.get("draft"),
             "items": [selection_material(x) for x in packet.get("items") or []]}
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


def selected_hashes(item):
    records = ([item.get("start_frame"), item.get("end_frame")] if item.get("type") == "ai_motion"
               else [item.get("preview"), item.get("source")])
    return sorted({r.get("sha256") for r in records if isinstance(r, dict) and r.get("sha256")})


def _validate_source(record, item_id):
    for key in ("trim_in", "trim_out"):
        _num(record.get(key), f"{item_id}.source.{key}", 0)
    if float(record["trim_out"]) <= float(record["trim_in"]):
        raise PacketError(f"{item_id}.source trim_out must be after trim_in")
    trim_seconds = float(record["trim_out"]) - float(record["trim_in"])
    if not 0.5 <= trim_seconds <= 15.0:
        raise PacketError(f"{item_id}.source exact moving preview trim must be 0.5–15 seconds")
    if not isinstance(record.get("crop"), str) or not record["crop"].strip():
        raise PacketError(f"{item_id}.source.crop must describe the exact crop/treatment")
    if not isinstance(record.get("rights"), str) or not record["rights"].strip():
        raise PacketError(f"{item_id}.source.rights must record usage-rights evidence")


def validate_packet(packet, workdir, allowed_roots=(), verify_hashes=True,
                    require_approved=False, require_complete=False, delivered_video=None,
                    watch_log=None):
    """Return the packet after complete validation, or raise PacketError."""
    if not isinstance(packet, dict) or packet.get("schema_version") != SCHEMA_VERSION:
        raise PacketError(f"placeholders.json must use schema_version {SCHEMA_VERSION}")
    if not isinstance(packet.get("video_id"), str) or not packet["video_id"].strip():
        raise PacketError("video_id is required")
    if not isinstance(packet.get("revision"), int) or packet["revision"] < 0:
        raise PacketError("revision must be a non-negative integer")
    if packet.get("status") not in ALLOWED_STATUSES:
        raise PacketError(f"status must be one of {sorted(ALLOWED_STATUSES)}")
    _file_record(packet.get("draft"), "draft", workdir, allowed_roots,
                 required=True, verify_hashes=verify_hashes)
    prior = packet.get("prior_paid_spend_usd")
    if prior is None:
        if not str(packet.get("prior_paid_spend_reason") or "").strip():
            raise PacketError("prior_paid_spend_usd null requires prior_paid_spend_reason")
    else:
        _num(prior, "prior_paid_spend_usd", 0)
    budget = _num(packet.get("generation_budget_usd", MAX_GENERATION_BUDGET_USD),
                  "generation_budget_usd", 0)
    if budget > MAX_GENERATION_BUDGET_USD:
        raise PacketError(f"generation_budget_usd cannot exceed the existing ${MAX_GENERATION_BUDGET_USD:.2f} per-video authorization")
    items = packet.get("items")
    if not isinstance(items, list):
        raise PacketError("items must be a list")
    ids = [x.get("id") for x in items if isinstance(x, dict)]
    if len(ids) != len(items) or len(ids) != len(set(ids)):
        raise PacketError("items must have unique IDs")
    for item in items:
        iid = item.get("id")
        if not ID_RE.fullmatch(str(iid or "")):
            raise PacketError(f"invalid item id: {iid!r}")
        if item.get("type") not in ALLOWED_TYPES:
            raise PacketError(f"{iid}.type must be one of {sorted(ALLOWED_TYPES)}")
        if item.get("reuse_status", "new") not in ("new", "exact_approved_reuse"):
            raise PacketError(f"{iid}.reuse_status must be new or exact_approved_reuse")
        tin = _num(item.get("in"), f"{iid}.in", 0)
        tout = _num(item.get("out"), f"{iid}.out", 0)
        if tout <= tin:
            raise PacketError(f"{iid}.out must be after in")
        dur = _num(item.get("duration", tout - tin), f"{iid}.duration", .01)
        if abs(dur - (tout - tin)) > .02:
            raise PacketError(f"{iid}.duration changed: {dur:.3f} != out-in {tout-tin:.3f}")
        for key in ("spoken_beat", "intended_action"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise PacketError(f"{iid}.{key} is required")
        _texts(item.get("affected_scenes"), f"{iid}.affected_scenes", required=True)
        _texts(item.get("boundary_joins"), f"{iid}.boundary_joins")
        estimated = _num(item.get("estimated_usd", 0), f"{iid}.estimated_usd", 0)
        if item["type"] != "ai_motion" and estimated != 0:
            raise PacketError(f"{iid}.estimated_usd must be 0 for stock/existing B-roll")
        if item.get("reuse_status", "new") == "exact_approved_reuse" and estimated != 0:
            raise PacketError(f"{iid}.estimated_usd must be 0 for an exact approved reuse")
        ph = item.get("placeholder")
        if not isinstance(ph, dict) or not str(ph.get("label") or "").startswith(f"PLACEHOLDER — {iid}"):
            raise PacketError(f"{iid}.placeholder.label must start with 'PLACEHOLDER — {iid}'")
        if ph.get("path"):
            _file_record(ph, f"{iid}.placeholder", workdir, allowed_roots,
                         verify_hashes=verify_hashes)
        elif not re.fullmatch(r"[0-9a-f]{64}", str(ph.get("sha256") or "")):
            raise PacketError(f"{iid}.placeholder needs its rendered-content sha256")
        if item["type"] == "ai_motion":
            _file_record(item.get("start_frame"), f"{iid}.start_frame", workdir, allowed_roots,
                         verify_hashes=verify_hashes)
            _file_record(item.get("end_frame"), f"{iid}.end_frame", workdir, allowed_roots,
                         verify_hashes=verify_hashes)
            if item.get("preview") is not None or item.get("source") is not None:
                raise PacketError(f"{iid}: ai_motion uses start/end frames, not preview/source")
        else:
            _file_record(item.get("preview"), f"{iid}.preview", workdir, allowed_roots,
                         verify_hashes=verify_hashes)
            _file_record(item.get("source"), f"{iid}.source", workdir, allowed_roots,
                         verify_hashes=verify_hashes)
            _validate_source(item["source"], iid)
            seconds = _num((item.get("preview") or {}).get("preview_seconds"),
                           f"{iid}.preview.preview_seconds", 0.5)
            if seconds > 15 or abs(seconds - (float(item["source"]["trim_out"]) -
                                               float(item["source"]["trim_in"]))) > 0.1:
                raise PacketError(f"{iid}.preview must be the exact 0.5–15 second proposed source trim")
            if item.get("start_frame") is not None or item.get("end_frame") is not None:
                raise PacketError(f"{iid}: stock/existing B-roll uses preview/source, not start/end frames")
        approval = item.get("approval")
        if not isinstance(approval, dict) or approval.get("status") not in ALLOWED_APPROVALS:
            raise PacketError(f"{iid}.approval.status must be pending, approved or rejected")
        if approval["status"] == "pending":
            if approval.get("selected_hashes"):
                raise PacketError(f"{iid}: pending approval cannot carry selected_hashes")
        else:
            if not str(approval.get("words") or "").strip() or not approval.get("timestamp"):
                raise PacketError(f"{iid}: decision must preserve exact words and timestamp")
        if approval["status"] == "approved":
            if sorted(approval.get("selected_hashes") or []) != selected_hashes(item):
                raise PacketError(f"{iid}: approved selected hashes are stale or incomplete")
            if approval.get("selection_fingerprint") != selection_fingerprint(item):
                raise PacketError(f"{iid}: material fields changed after approval")
        final = item.get("final_clip")
        if final is not None:
            _file_record(final, f"{iid}.final_clip", workdir, allowed_roots,
                         verify_hashes=verify_hashes)
            if approval["status"] != "approved":
                raise PacketError(f"{iid}: a final clip cannot exist without approval")
            if final.get("inserted_from_fingerprint") != selection_fingerprint(item):
                raise PacketError(f"{iid}: final clip was not built from the approved selection")
    approved = bool(items) and all(x["approval"]["status"] == "approved" for x in items)
    complete = approved and all(x.get("final_clip") for x in items)
    if require_approved and not approved:
        raise PacketError("not every current packet item is approved")
    if packet["status"] == "approved" and not approved:
        raise PacketError("packet says approved but an item is pending/rejected")
    if packet["status"] == "complete" and not complete:
        raise PacketError("packet says complete but an approved final clip is missing")
    if require_complete:
        if packet["status"] != "complete" or not complete:
            raise PacketError("placeholder flow is not complete")
        delivery = packet.get("delivery")
        if not isinstance(delivery, dict):
            raise PacketError("complete packet lacks the hash-bound delivery record")
        _file_record(delivery, "delivery", workdir, allowed_roots,
                     verify_hashes=verify_hashes)
        if delivered_video and os.path.realpath(delivery["path"]) != os.path.realpath(delivered_video):
            raise PacketError("packet delivery path is not the delivered file being checked")
        watch_path = delivery.get("watch_log")
        watch_sha = delivery.get("watch_log_sha256")
        _file_record({"path": watch_path, "sha256": watch_sha}, "delivery.watch_log", workdir,
                     allowed_roots, verify_hashes=verify_hashes)
        if watch_log and os.path.realpath(watch_path) != os.path.realpath(watch_log):
            raise PacketError("packet and delivery check name different watch logs")
    return packet


def read_packet(path, workdir=None, allowed_roots=(), **kwargs):
    try:
        with open(path) as fh:
            packet = json.load(fh)
    except Exception as exc:
        raise PacketError(f"placeholders.json is unreadable: {exc}") from exc
    return validate_packet(packet, workdir or os.path.dirname(os.path.abspath(path)),
                           allowed_roots, **kwargs)


@contextlib.contextmanager
def _locked(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path + ".lock", "a") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _atomic_json(path, value):
    fd, tmp = tempfile.mkstemp(prefix=".placeholders-", suffix=".tmp",
                               dir=os.path.dirname(os.path.abspath(path)))
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(value, fh, indent=2, ensure_ascii=False)
            fh.write("\n"); fh.flush(); os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_packet(path, packet, workdir=None, allowed_roots=()):
    """Create/update a packet, preserving unchanged approved items and resetting changed ones."""
    workdir = workdir or os.path.dirname(os.path.abspath(path))
    packet = copy.deepcopy(packet)
    with _locked(path):
        old = None
        if os.path.exists(path):
            old = read_packet(path, workdir, allowed_roots)
        old_by_id = {x["id"]: x for x in (old or {}).get("items", [])}
        for item in packet.get("items") or []:
            previous = old_by_id.get(item.get("id"))
            if previous and selection_fingerprint(previous) == selection_fingerprint(item):
                if previous.get("approval", {}).get("status") == "approved":
                    item["approval"] = copy.deepcopy(previous["approval"])
                    item["final_clip"] = copy.deepcopy(previous.get("final_clip"))
            else:
                item["approval"] = {"status": "pending", "selected_hashes": [],
                                    "words": None, "timestamp": None,
                                    "selection_fingerprint": None}
                item["final_clip"] = None
        packet.setdefault("created_at", (old or {}).get("created_at") or now_iso())
        packet["updated_at"] = now_iso()
        if packet.get("items") and all(x.get("approval", {}).get("status") == "approved"
                                       for x in packet["items"]):
            packet["status"] = "approved"
        else:
            packet["status"] = "approval_required"
        validate_packet(packet, workdir, allowed_roots)
        _atomic_json(path, packet)
    return packet


def decide(path, decisions, workdir=None, allowed_roots=()):
    """Atomically save one complete batch. Omitted items and rejection without words are refused."""
    workdir = workdir or os.path.dirname(os.path.abspath(path))
    with _locked(path):
        packet = read_packet(path, workdir, allowed_roots)
        if not isinstance(decisions, list):
            raise PacketError("decisions must be a list")
        by_id = {}
        for row in decisions:
            if not isinstance(row, dict) or row.get("id") in by_id:
                raise PacketError("decisions contain a missing or duplicate item ID")
            by_id[row.get("id")] = row
        ids = {x["id"] for x in packet["items"]}
        if set(by_id) != ids:
            raise PacketError(f"submission must decide every current item; expected {sorted(ids)}, got {sorted(by_id)}")
        for item in packet["items"]:
            row = by_id[item["id"]]
            if row.get("status") not in ("approved", "rejected"):
                raise PacketError(f"{item['id']}: decision must be approved or rejected")
            if not str(row.get("words") or "").strip():
                raise PacketError(f"{item['id']}: preserve the exact approval/rejection words")
        approving_ai = any(by_id[x["id"]].get("status") == "approved" and x["type"] == "ai_motion"
                           and x.get("reuse_status", "new") == "new" for x in packet["items"])
        costs = cost_summary(packet)
        approved_estimate = sum(float(x.get("estimated_usd") or 0) for x in packet["items"]
                                if by_id[x["id"]].get("status") == "approved" and x["type"] == "ai_motion"
                                and x.get("reuse_status", "new") == "new")
        if approving_ai and costs["projected_total_usd"] is None:
            raise PacketError("AI motion cannot be approved while prior paid spend is unavailable")
        projected_approved = (packet.get("prior_paid_spend_usd") + approved_estimate
                              if isinstance(packet.get("prior_paid_spend_usd"), (int, float)) else None)
        if (projected_approved is not None and
                projected_approved > costs["generation_budget_usd"] + 1e-9):
            raise PacketError(f"approval would exceed the ${costs['generation_budget_usd']:.2f} per-video generation budget")
        stamp = now_iso()
        for item in packet["items"]:
            row = by_id[item["id"]]
            status = row.get("status")
            words = str(row.get("words") or "")
            item["approval"] = {
                "status": status,
                "selected_hashes": selected_hashes(item) if status == "approved" else [],
                "words": words, "timestamp": stamp,
                "selection_fingerprint": selection_fingerprint(item) if status == "approved" else None,
            }
            if status != "approved":
                item["final_clip"] = None
        packet["status"] = ("approved" if packet["items"] and
                            all(x["approval"]["status"] == "approved" for x in packet["items"])
                            else "approval_required")
        packet["updated_at"] = stamp
        validate_packet(packet, workdir, allowed_roots)
        _atomic_json(path, packet)
    return packet


def mark_complete(path, final_clips, delivered_video, workdir=None, allowed_roots=(), watch_log=None):
    """Bind approved inputs, inserted clips, watch evidence and final render by content hash."""
    workdir = workdir or os.path.dirname(os.path.abspath(path))
    if not watch_log:
        raise PacketError("mark-complete requires the final chronological watch log")
    with _locked(path):
        packet = read_packet(path, workdir, allowed_roots, require_approved=True)
        if not isinstance(final_clips, dict) or set(final_clips) != {x["id"] for x in packet["items"]}:
            raise PacketError("final_clips must name every approved item exactly once")
        for item in packet["items"]:
            clip = _safe_path(final_clips[item["id"]], workdir, allowed_roots)
            if not os.path.isfile(clip):
                raise PacketError(f"{item['id']}: final clip missing: {clip}")
            item["final_clip"] = {"path": clip, "sha256": sha256(clip),
                                  "inserted_from_fingerprint": selection_fingerprint(item)}
        video = _safe_path(delivered_video, workdir, allowed_roots)
        if not os.path.isfile(video):
            raise PacketError(f"delivered file missing: {video}")
        packet["delivery"] = {"path": video, "sha256": sha256(video)}
        wl = _safe_path(watch_log, workdir, allowed_roots)
        if not os.path.isfile(wl):
            raise PacketError(f"watch log missing: {wl}")
        packet["delivery"].update(watch_log=wl, watch_log_sha256=sha256(wl))
        packet["status"] = "complete"
        packet["updated_at"] = now_iso()
        validate_packet(packet, workdir, allowed_roots, require_complete=True,
                        delivered_video=video, watch_log=watch_log)
        _atomic_json(path, packet)
    return packet


def cost_summary(packet):
    estimate = round(sum(float(x.get("estimated_usd") or 0) for x in packet.get("items") or []
                         if x.get("type") == "ai_motion" and x.get("reuse_status", "new") == "new"), 4)
    prior = packet.get("prior_paid_spend_usd")
    budget = float(packet.get("generation_budget_usd", MAX_GENERATION_BUDGET_USD))
    return {"estimated_new_usd": estimate, "prior_paid_spend_usd": prior,
            "projected_total_usd": round(prior + estimate, 4) if isinstance(prior, (int, float)) else None,
            "prior_paid_spend_reason": packet.get("prior_paid_spend_reason"),
            "generation_budget_usd": budget}


def listed_media(packet):
    """Only these hash-bound files may be served by the local review page."""
    rows = []
    if isinstance(packet.get("draft"), dict):
        rows.append(("draft", packet["draft"]))
    for item in packet.get("items") or []:
        for key in ("start_frame", "end_frame", "preview"):
            if isinstance(item.get(key), dict):
                rows.append((f"{item['id']}.{key}", item[key]))
    return rows


def approval_counts(packet):
    statuses = [x.get("approval", {}).get("status") for x in packet.get("items") or []]
    return {s: statuses.count(s) for s in ALLOWED_APPROVALS}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("packet"); v.add_argument("--approved", action="store_true"); v.add_argument("--complete", action="store_true")
    d = sub.add_parser("decide"); d.add_argument("packet"); d.add_argument("decisions_json")
    m = sub.add_parser("mark-complete"); m.add_argument("packet"); m.add_argument("final_clips_json"); m.add_argument("delivered_video"); m.add_argument("--watch-log")
    for p in (v, d, m):
        p.add_argument("--allow-root", action="append", default=[])
    args = ap.parse_args()
    workdir = os.path.dirname(os.path.abspath(args.packet))
    if args.cmd == "validate":
        packet = read_packet(args.packet, workdir, args.allow_root,
                             require_approved=args.approved, require_complete=args.complete)
    elif args.cmd == "decide":
        packet = decide(args.packet, json.load(open(args.decisions_json)), workdir, args.allow_root)
    else:
        packet = mark_complete(args.packet, json.load(open(args.final_clips_json)), args.delivered_video,
                               workdir, args.allow_root, args.watch_log)
    print(json.dumps({"status": packet["status"], "counts": approval_counts(packet),
                      "costs": cost_summary(packet)}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except PacketError as exc:
        raise SystemExit(f"asset approval packet refused: {exc}")
