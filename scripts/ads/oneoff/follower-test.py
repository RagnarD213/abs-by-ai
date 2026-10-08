#!/usr/bin/env python3
"""
@danrosefit follower test, Oct 2026 (Dan's call, 2026-10-08): do the Instagram
profile-visit ads actually add followers?

  OFF 1   Oct 9  - Oct 15   no ads at all
  ON      Oct 16 - Oct 22   one ad at $40/day (Meta starts and stops it by itself)
  OFF 2   Oct 23 - Oct 29   no ads at all

Read-only. Two commands:

  python3 scripts/ads/oneoff/follower-test.py status   # what is running and spending right now
  python3 scripts/ads/oneoff/follower-test.py report   # the three weeks side by side

New followers come from Instagram's `follower_count` (per day, all sources). A day
is trusted once it is 2 days old. Detail and ids: Docs/AUTO_BOOST.md, "Follower test".
"""
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v21.0/"
ACT = "act_2143998876461525"
CAMPAIGN = "120250753198730682"          # [AUTO] IG PROFILE VISITS - danrosefit
TEST_ADSET = "120251407001680682"        # FOLLOWTEST, $40/day, Oct 16 00:00 - Oct 23 00:00 CT
IG_USER_ID = "17841401601139982"         # @danrosefit
WINDOWS = [("OFF 1", "2026-10-09", "2026-10-15"),
           ("ON $40/day", "2026-10-16", "2026-10-22"),
           ("OFF 2", "2026-10-23", "2026-10-29")]
NOISE_PER_WEEK = 28                      # followers; a smaller week-to-week gap is normal bounce
SETTLE_DAYS = 2
SECRETS = os.path.expanduser("~/.absbyai-secrets.env")
_env = open(SECRETS).read()


def secret(key):
    if os.environ.get(key):
        return os.environ[key]
    m = re.search(r"^(?:export )?%s=(.*)$" % re.escape(key), _env, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else None


TOKEN = secret("META_ADS_TOKEN")
PROOF = hmac.new(secret("META_APP_SECRET").encode(), TOKEN.encode(), hashlib.sha256).hexdigest()


def meta(path, _all=True, **params):
    params.update(access_token=TOKEN, appsecret_proof=PROOF)
    url, rows = API + path + "?" + urllib.parse.urlencode(params), []
    while url:
        try:
            r = json.loads(urllib.request.urlopen(url).read().decode())
        except urllib.error.HTTPError as e:
            sys.exit("Meta error on %s: %s" % (path, e.read().decode()[:300]))
        if "data" not in r:
            return r
        rows += r["data"]
        url = r.get("paging", {}).get("next") if _all else None
    return rows


def posthog(sql):
    body = json.dumps({"query": {"kind": "HogQLQuery", "query": sql}}).encode()
    req = urllib.request.Request(
        "https://us.posthog.com/api/projects/%s/query/" % secret("POSTHOG_PROJECT_ID"), data=body,
        headers={"Authorization": "Bearer " + secret("POSTHOG_PERSONAL_KEY"), "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req).read().decode()).get("results") or []
    except urllib.error.HTTPError as e:
        return [["PostHog error: " + e.read().decode()[:120]]]


def follower_days():
    """{'YYYY-MM-DD': new followers}. Each value's end_time is the END of its day (07:00 UTC)."""
    now = dt.datetime.now(dt.timezone.utc)
    # one page only: Instagram's "next" link points past today and errors
    rows = meta(IG_USER_ID + "/insights", _all=False, metric="follower_count", period="day",
                since=int((now - dt.timedelta(days=29)).timestamp()), until=int(now.timestamp()))
    out = {}
    for v in (rows[0]["values"] if rows else []):
        end = dt.datetime.strptime(v["end_time"][:19], "%Y-%m-%dT%H:%M:%S")
        out[(end - dt.timedelta(days=1)).strftime("%Y-%m-%d")] = v["value"]
    return out


def ad_days():
    """{'YYYY-MM-DD': (spend, profile visits)} for the whole ad account."""
    rows = meta(ACT + "/insights", time_increment=1, fields="spend,instagram_profile_visits",
                time_range=json.dumps({"since": WINDOWS[0][1], "until": WINDOWS[-1][2]}), limit=100)
    return {r["date_start"]: (float(r["spend"]), int(r.get("instagram_profile_visits") or 0)) for r in rows}


def site_from_instagram(start, end):
    ig = ("select distinct person_id from events where event='$pageview' "
          "and toDate(toTimeZone(timestamp,'America/Chicago')) between '%s' and '%s' "
          "and (lower(toString(properties.utm_source)) in ('instagram','ig') "
          "or properties.$referring_domain ilike '%%instagram%%')" % (start, end))
    people = posthog("select count() from (%s)" % ig)
    trials = posthog("select count(distinct person_id) from events where event in "
                     "('trial_signup_started','cart_checkout_opened') and timestamp >= '%s' and person_id in (%s)" % (start, ig))
    return people[0][0] if people else "?", trials[0][0] if trials else "?"


def status():
    today = dt.date.today().isoformat()
    a = meta(TEST_ADSET, fields="name,status,effective_status,daily_budget,start_time,end_time")
    print("Test ad set: %s | %s | $%.2f/day | %s to %s" % (
        a["effective_status"], a["name"][:60], int(a["daily_budget"]) / 100, a["start_time"][:16], a["end_time"][:16]))
    sets = meta(CAMPAIGN + "/adsets", fields="id,name,status,effective_status", limit=200)
    live = [s for s in sets if s["status"] == "ACTIVE" and s["id"] != TEST_ADSET]
    print("Other ad sets switched on in the campaign: %d %s" % (len(live), [s["name"][:40] for s in live]))
    other = [c for c in meta(ACT + "/campaigns", fields="id,name,effective_status") if c["effective_status"] == "ACTIVE" and c["id"] != CAMPAIGN]
    print("Other active Meta campaigns: %d %s" % (len(other), [c["name"] for c in other]))
    rows = meta(ACT + "/insights", time_increment=1, fields="spend,instagram_profile_visits",
                time_range=json.dumps({"since": WINDOWS[0][1], "until": max(today, WINDOWS[0][1])}), limit=100)
    for r in rows:
        print("  %s  spend $%s  profile visits %s" % (r["date_start"], r["spend"], r.get("instagram_profile_visits", 0)))
    if not rows:
        print("  no spend since %s" % WINDOWS[0][1])


def report():
    follows, ads = follower_days(), ad_days()
    settled = (dt.date.today() - dt.timedelta(days=SETTLE_DAYS)).isoformat()
    res = []
    print("%-11s %-13s %5s %10s %10s %9s %7s %9s %7s" % ("week", "dates", "days", "followers", "per day", "spend", "visits", "IG->site", "trials"))
    for label, start, end in WINDOWS:
        days = [d for d in sorted(follows) if start <= d <= min(end, settled)]
        total = sum(follows[d] for d in days)
        spend = sum(ads.get(d, (0, 0))[0] for d in days)
        visits = sum(ads.get(d, (0, 0))[1] for d in days)
        people, trials = site_from_instagram(start, end) if days else ("-", "-")
        res.append({"label": label, "days": len(days), "followers": total, "spend": spend})
        print("%-11s %-13s %5d %10d %10s %9s %7d %9s %7s" % (
            label, start[5:] + " to " + end[5:], len(days), total, ("%.1f" % (total / len(days))) if days else "-",
            "$%.2f" % spend, visits, people, trials))
    print("Followers by day: " + ", ".join("%s %s" % (d[5:], follows[d]) for d in sorted(follows) if d >= WINDOWS[0][1]))
    off = [r for r in (res[0], res[2]) if r["days"]]
    on = res[1]
    if on["days"] < 7 or not off:
        print("\nNot finished: the ON week has %d of 7 settled days. Run again after %s." % (on["days"], "2026-10-31"))
        return
    base = sum(r["followers"] / r["days"] for r in off) / len(off) * 7
    extra = on["followers"] - base
    print("\nBaseline (average OFF week): %.0f followers. ON week: %d. Extra from ads: %+.0f." % (base, on["followers"], extra))
    if extra < NOISE_PER_WEEK:
        print("VERDICT: no detectable effect (a gap under %d a week is normal bounce). $%.2f bought nothing measurable. Leave it off." % (NOISE_PER_WEEK, on["spend"]))
    else:
        print("VERDICT: the ads added about %.0f followers for $%.2f = $%.2f per extra follower." % (extra, on["spend"], on["spend"] / extra))
    if len(off) < 2 or res[2]["days"] < 7:
        print("Note: OFF 2 has %d of 7 settled days, so the baseline is not final yet." % res[2]["days"])


if __name__ == "__main__":
    {"status": status, "report": report}.get(sys.argv[1] if len(sys.argv) > 1 else "status", status)()
