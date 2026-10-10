#!/usr/bin/env python3
"""Scoreboard for the /start video test: WV-01 Version A against Version B ("Fired Them All").

Reads PostHog with the stored query key (POSTHOG_PERSONAL_KEY in ~/.absbyai-secrets.env) and prints one
column per film. The same numbers as the PostHog dashboard "/start video test: A vs B"
(https://us.posthog.com/project/458833/dashboard/2195388). Forced QA views (?vid=a, ?vid=b) and anything not on absbyai.com are left out.

    python3 scripts/posthog/vsl_video_test.py              the table, from the minute the split went live
    python3 scripts/posthog/vsl_video_test.py --trials     also list each trial start with its film
    python3 scripts/posthog/vsl_video_test.py --json       the same numbers as JSON
    python3 scripts/posthog/vsl_video_test.py --since "2026-10-20 00:00"   a later start (America/Chicago)

How the test is read (Dan, 2026-10-10; Docs/VSL_LANDING.md): no winner before day 21. Day 14 or 500 visitors
per film, whichever is later: if B's sound-on rate trails A's by a third or more, set B_SHARE to 0 in
build_live.py and tell Dan. The winner is called on trial starts (about 20 real ones in total, the leader
holding about 15), counted from live Stripe without Dan and test accounts, each matched to its film here.
"""
import argparse, json, os, sys, urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

LIVE_SINCE = '2026-10-10 15:43'  # America/Chicago: the minute the split went live
CT = ZoneInfo('America/Chicago')
HOST = "lower(coalesce(properties.$host, domain(properties.$current_url))) IN ('absbyai.com', 'www.absbyai.com')"
UNFORCED = "ifNull(toString(properties.video_forced), 'false') != 'true'"
ROWS = [  # label, HogQL condition on one event
    ('Visitors (saw the page)', "event = 'vsl_landing_seen'"),
    ('Turned the sound on', "event = 'vsl_sound_on'"),
    ('Watched 30 seconds', "event = 'vsl_video_watch' AND toString(properties.sec) = '30'"),
    ('Watched 60 seconds', "event = 'vsl_video_watch' AND toString(properties.sec) = '60'"),
    ('Watched 2 minutes', "event = 'vsl_video_watch' AND toString(properties.sec) = '120'"),
    ('Got past the opening', "event = 'vsl_opening_done'"),
    ('Watched 4 minutes', "event = 'vsl_video_watch' AND toString(properties.sec) = '240'"),
    ('Watched 8 minutes', "event = 'vsl_video_watch' AND toString(properties.sec) = '480'"),
    ('Reached the end', "event = 'vsl_video_progress' AND toString(properties.pct) = '100'"),
    ('Clicked a trial button', "event = 'vsl_trial_cta_clicked'"),
    ('Saw the cart', "event = 'cart_viewed'"),
    ('Started a trial (PostHog)', "event = 'cart_checkout_completed'"),
]


def secret(name):
    if os.environ.get(name):
        return os.environ[name]
    try:
        for line in open(os.path.expanduser('~/.absbyai-secrets.env')):
            if line.startswith(name + '='):
                return line.split('=', 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return None


def hogql(query):
    key, project = secret('POSTHOG_PERSONAL_KEY') or secret('POSTHOG_API_KEY'), secret('POSTHOG_PROJECT_ID') or '458833'
    if not key:
        sys.exit('No PostHog key: POSTHOG_PERSONAL_KEY is not in ~/.absbyai-secrets.env')
    req = urllib.request.Request(f'https://us.posthog.com/api/projects/{project}/query',
                                 # force_blocking: PostHog otherwise answers a repeated query from its cache, which can be hours old
                                 data=json.dumps({'query': {'kind': 'HogQLQuery', 'query': query}, 'refresh': 'force_blocking'}).encode(),
                                 headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))['results']
    except urllib.error.HTTPError as e:
        sys.exit(f'PostHog query failed: {e.code} {e.read().decode()[:300]}')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--since', default=LIVE_SINCE, help='start, America/Chicago, "YYYY-MM-DD HH:MM"')
    ap.add_argument('--trials', action='store_true'); ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    start = datetime.strptime(a.since, '%Y-%m-%d %H:%M').replace(tzinfo=CT)
    since = start.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    where = f"timestamp >= toDateTime('{since}', 'UTC') AND properties.video_variant IN ('a', 'b') AND {UNFORCED} AND {HOST}"
    cols = ', '.join(f"uniqIf(person_id, {cond})" for _, cond in ROWS)
    by_arm = {r[0]: r[1:] for r in hogql(f"SELECT properties.video_variant AS arm, {cols} FROM events WHERE {where} GROUP BY arm")}
    phone = {r[0]: r[1:] for r in hogql(
        f"SELECT properties.video_variant AS arm, uniqIf(person_id, properties.$device_type = 'Mobile'), uniqIf(person_id, properties.$device_type = 'Desktop') "
        f"FROM events WHERE {where} AND event = 'vsl_landing_seen' GROUP BY arm")}
    both = hogql(f"SELECT count() FROM (SELECT person_id FROM events WHERE {where} AND event = 'vsl_landing_seen' GROUP BY person_id HAVING uniq(properties.video_variant) > 1)")[0][0]
    loose = hogql(f"SELECT uniq(person_id) FROM events WHERE {where} AND event = 'vsl_landing_seen' AND toString(properties.video_sticky) = 'false'")[0][0]
    days = (datetime.now(timezone.utc) - start.astimezone(timezone.utc)).total_seconds() / 86400
    out = {'since_central': a.since, 'days_running': round(days, 1), 'rows': [], 'seen_both_films': both, 'arm_not_stored': loose,
           'phone_desktop': {k: list(v) for k, v in phone.items()}}
    for i, (label, _) in enumerate(ROWS):
        out['rows'].append({'step': label, 'a': by_arm.get('a', [0] * len(ROWS))[i], 'b': by_arm.get('b', [0] * len(ROWS))[i]})
    trials = []
    if a.trials or a.json:
        trials = hogql(
            "SELECT toTimeZone(timestamp, 'America/Chicago') AS t, properties.video_variant, properties.plan, properties.utm_source, "
            "properties.$geoip_city_name, properties.$device_type, toString(person_id) "
            f"FROM events WHERE {where} AND event = 'cart_checkout_completed' ORDER BY timestamp")
        out['trial_starts'] = [dict(zip(('time_central', 'film', 'plan', 'utm_source', 'city', 'device', 'person'), [str(x) if x is not None else None for x in r])) for r in trials]
    if a.json:
        print(json.dumps(out, indent=1)); return

    va, vb = out['rows'][0]['a'], out['rows'][0]['b']
    print(f"/start video test, A against B. Since {a.since} Central ({days:.1f} days). Forced QA views left out.\n")
    print(f"{'':28}{'A':>8}{'':>9}{'B (Fired Them All)':>20}")
    for r in out['rows']:
        pa = f"{100 * r['a'] / va:5.1f}%" if va else '     -'
        pb = f"{100 * r['b'] / vb:5.1f}%" if vb else '     -'
        print(f"{r['step']:28}{r['a']:>8}  {pa:>7}{r['b']:>12}  {pb:>7}")
    for arm in ('a', 'b'):
        m, d = phone.get(arm, (0, 0))
        print(f"  film {arm.upper()}: {m} phone, {d} desktop visitors")
    print(f"\nPeople who saw both films: {both}. Visitors whose browser could not store the film: {loose}.")
    sa, sb = (out['rows'][1]['a'] / va if va else 0), (out['rows'][1]['b'] / vb if vb else 0)
    if min(va, vb) >= 500 and days >= 14:
        print('EARLY WARNING CHECK: ' + ("B's sound-on rate trails A's by a third or more. Set B_SHARE to 0 and tell Dan." if sa and sb <= sa * 2 / 3 else 'B is not trailing by a third. Keep running.'))
    else:
        print(f"Early warning check opens at day 14 and 500 visitors per film (now day {days:.0f}, {va} and {vb}).")
    print('No winner before day 21. The winner is called on real trial starts from Stripe, not on this table.')
    if a.trials:
        print('\nTrial starts (match each to live Stripe; leave out Dan and test accounts):')
        for t in out['trial_starts']:
            print(f"  {t['time_central'][:16]}  film {str(t['film']).upper()}  {t['plan']}  source {t['utm_source']}  {t['city']}  {t['device']}  person {t['person']}")
        if not trials: print('  none yet')


if __name__ == '__main__':
    main()
