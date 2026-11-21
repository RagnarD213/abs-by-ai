#!/usr/bin/env python3
"""Read-only cover preflight of the complete live Blotato queue."""
import json
from collections import Counter
from cover_guard import assert_video_cover
from danrosefit_migration import api_key, fetch_schedules

def main():
    queue = fetch_schedules(api_key())
    issues = []
    for item in queue:
        try:
            assert_video_cover({'post': item['draft']})
        except Exception as exc:
            issues.append({'id': item['id'], 'platform': item['draft']['content']['platform'],
                           'scheduledAt': item['scheduledAt'], 'issue': str(exc)})
    print(json.dumps({'scheduledPosts': len(queue), 'platforms': dict(Counter(i['draft']['content']['platform'] for i in queue)),
                      'issues': issues, 'note': 'Queue preflight only. Public tiles still need a visual release check; TikTok timestamp alone does not verify frame-zero pixels.'}, indent=2))
    return bool(issues)

if __name__ == '__main__':
    raise SystemExit(main())
