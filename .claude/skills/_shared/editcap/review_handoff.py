"""Recognize an owner-review handoff for the current edit round."""
from datetime import datetime
from math import isfinite


def handoff_time(job):
    if not job or job.get("state") not in ("draft_review", "delivered"):
        return 0
    try:
        if job.get("review_ready_at") is not None:
            when = float(job["review_ready_at"])
            return when if isfinite(when) else 0
    except (TypeError, ValueError, OverflowError):
        return 0
    # Older rows can have only a date. Midnight conservatively preserves any
    # production that started on that day when its order cannot be established.
    try:
        return datetime.fromisoformat(job.get("updated", "")).timestamp()
    except (TypeError, ValueError, OverflowError):
        return 0


def current(entry, ready_at):
    if entry.get("state") not in ("active", "stalled", "promoted", "waiting", "parked"):
        return False
    last_work = max(entry.get(field, 0) for field in
                    ("registered", "active_since", "last_seen", "waiting_since"))
    if entry["state"] in ("waiting", "promoted", "parked"):
        last_work = max(last_work, entry.get("since", 0))
    return ready_at > 0 and ready_at >= last_work


def completed(entry, job):
    """Hide only owner reviews that predate the recorded completion event."""
    if not job or job.get('state') not in ('finalized','uploaded'):return False
    try:
        cutoff=float(job['completed_at']) if job.get('completed_at') is not None else datetime.fromisoformat(job.get('updated','')).timestamp()
        return isfinite(cutoff) and float(entry.get('since',0))<=cutoff
    except (ValueError,TypeError,OverflowError):return False
