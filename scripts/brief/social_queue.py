"""Normalize independently verified private queue snapshots. Never change posts."""
from datetime import timedelta
import re
from planning import timestamp


def normalize(blotato, youtube, heads, now, flags=None):
    flags = flags or {}
    end = now + timedelta(days=7)
    coverage = {"blotato": "missing", "youtubeStudio": "missing"}
    rows, times, media = [], {}, {}
    head_status = {row.get("url"): row.get("status") for row in (heads or [])}

    def checked(data):
        if not data:
            return False
        age = (now - timestamp(data["checkedAt"])).total_seconds()
        return -300 <= age <= 12 * 3600

    def add(row, key, urls):
        identity = (key, row["scheduledAt"])
        collisions = times.setdefault(identity, [])
        collisions.append(row)
        for url in set(urls):
            media.setdefault((key, url), []).append(row)
        f = flags.get(row["id"], {})
        row["notes"] = f.get("notes", [])[:5]
        for name, value in f.get("preflight", {}).items():
            if name in row["preflight"]:
                row["preflight"][name] = value
        rows.append(row)

    if blotato:
        coverage["blotato"] = "ok" if checked(blotato) else "stale"
        for item in blotato["items"]:
            at = timestamp(item["scheduledAt"])
            if not now <= at < end:
                continue
            draft, account = item["draft"], item["account"]
            content, target = draft["content"], draft["target"]
            platform, caption = content["platform"], content.get("text", "")
            urls = content.get("mediaUrls", [])
            thumb = target.get("thumbnailUrl") or target.get("coverImageUrl")
            cover = "verified" if thumb and head_status.get(thumb) == 200 else "unverified"
            # Facebook payload omits installed covers. Absence is not proof missing.
            links = re.findall(r'https://[^\s<>"\)]+', caption)
            links = [url.rstrip(".,!;") for url in links]
            link_state = "not_applicable" if not links else ("verified" if all(head_status.get(url) == 200 for url in links) else "unverified")
            if any(isinstance(head_status.get(url), int) and head_status[url] >= 400 for url in links):
                link_state = "broken"
            row = {"id": str(item["id"]), "platform": platform, "account": account.get("username") or account.get("name") or platform,
                   "scheduledAt": at.isoformat(), "title": (target.get("title") or (caption.splitlines() or ["Scheduled release"])[0])[:220],
                   "caption": caption[:1000], "reviewUrl": None, "coverReviewUrl": thumb,
                   "preflight": {"cover": cover, "description": "verified" if platform == "youtube" and caption.strip() else ("missing" if platform == "youtube" else "not_applicable"),
                                 "links": link_state, "duplicates": "verified", "assetMatch": "unverified"}}
            add(row, (platform, str(draft["accountId"])), urls)
    if youtube:
        coverage["youtubeStudio"] = "ok" if checked(youtube) else "stale"
        for item in youtube["videos"]:
            scheduled = item["status"].get("publishAt")
            if not scheduled:
                continue
            at = timestamp(scheduled)
            if not now <= at < end:
                continue
            snippet = item["snippet"]
            thumbnails = snippet.get("thumbnails", {})
            thumb = next((thumbnails[key]["url"] for key in ("maxres", "standard", "high", "medium", "default") if key in thumbnails), None)
            caption = snippet.get("description", "")
            links = [u.rstrip(".,!;") for u in re.findall(r'https://[^\s<>"\)]+', caption)]
            link_state = "not_applicable" if not links else ("verified" if all(head_status.get(url) == 200 for url in links) else "unverified")
            if any(isinstance(head_status.get(url), int) and head_status[url] >= 400 for url in links):
                link_state = "broken"
            row = {"id": "youtube:" + item["id"], "platform": "youtube", "account": snippet.get("channelTitle", "YouTube"),
                   "scheduledAt": at.isoformat(), "title": snippet["title"][:220], "caption": caption[:1000],
                   "reviewUrl": "https://studio.youtube.com/video/" + item["id"] + "/edit", "coverReviewUrl": thumb,
                   "preflight": {"cover": "verified" if thumb and head_status.get(thumb) == 200 else "unverified",
                                 "description": "verified" if caption.strip() else "missing", "links": link_state, "duplicates": "verified", "assetMatch": "unverified"}}
            add(row, ("youtube", snippet.get("channelId", "unverified-channel")), ["youtube:" + item["id"]])
    for group in [*times.values(), *media.values()]:
        if len(group) > 1:
            for row in group:
                row["preflight"]["duplicates"] = "duplicate"
    rows.sort(key=lambda row: row["scheduledAt"])
    # Missing Studio coverage must not masquerade as a verified empty native queue.
    return {"status": "ok" if all(v == "ok" for v in coverage.values()) else "partial",
            "checkedAt": min((data["checkedAt"] for data in (blotato, youtube) if data), default=None),
            "windowFrom": now.isoformat(), "windowTo": end.isoformat(), "sourceCoverage": coverage, "rows": rows}
